#!/usr/bin/env python3
"""The rv64gc WORKLOAD campaign (P4-SYSTEM.15 slice f; G-REGRESSION's `workload` kind).

Four compiled, self-checking, freestanding C workloads — `profiles/rv64gc-lab-v0/workload/wl-*.c`, built by the
pinned toolchain on the laboratory's HTIF and signature conventions (`wl-start.S`, `wl-link.ld`) — run three-way
exactly as the ACT4 external campaign runs its tests: the Sail reference sets the step budget, every model's store
trace yields its HTIF verdict and its signature, semulith is judged against the Sail-derived signature (EVD-04: one
semantics answering twice, never a second independent one) and spike against sail is the control pair. Each
workload writes every computed result into its signature region AND checks it against a constant derived from the
C abstract machine (`scripts/derive_workload_constants.py`, re-derived before every build — a drifted constant
refuses the campaign); a failed check routes to the HTIF fail verdict, so a wrong executor diverges at the slot
and in the verdict. The instruction census of each ELF (instructions, compressed, the extension families present)
is recorded as the ELF's fact — what the compiler emitted, not what the source intended.

    python3 scripts/run_workload_campaign.py                 # every workload, verdicts and comparisons
    python3 scripts/run_workload_campaign.py wl-float        # one workload
    python3 scripts/run_workload_campaign.py --record        # … and write profiles/rv64gc-lab-v0/workload.sexp
    python3 scripts/run_workload_campaign.py --self-test     # RED/GREEN controls

⛔ NOT A COMMIT GATE: it needs the reference binaries under target/refs (scripts/fetch_references.sh) and the
pinned toolchain. The record is a RECORDED experiment; RECORD-SCHEMA rule 15 checks its shape and that its counts
re-derive from its rows, never re-execution.
"""
from __future__ import annotations

import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_act4_campaign as A  # noqa: E402 — the measured helpers: toolchain, symbols, stores, verdict, run_model

ROOT = Path(__file__).resolve().parent.parent
PROFILE = "rv64gc-lab-v0"
WORKLOAD = ROOT / f"profiles/{PROFILE}/workload"
OUT = ROOT / "target/workload-campaign"
WORKLOADS = ("wl-integer", "wl-memory", "wl-float", "wl-calls")
CFLAGS = ["--target=riscv64-unknown-elf", "-march=rv64gc", "-mabi=lp64d", "-mno-relax", "-mcmodel=medany",
          "-O2", "-ffreestanding", "-fno-builtin", "-nostdlib", "-Wall", "-Wextra", "-Werror"]
FAMILY = {
    "M": re.compile(r"^(mul|mulh|mulhu|mulhsu|mulw|div|divu|divw|divuw|rem|remu|remw|remuw)$"),
    "F": re.compile(r"^f[a-z]+\.s$|^f(lw|sw|mv\.w\.x|mv\.x\.w|mv\.s)$"),
    "D": re.compile(r"^f[a-z]+\.d$|^f(ld|sd|mv\.d\.x|mv\.x\.d|mv\.d|cvt\.d\.[a-z]+|cvt\.[a-z]+\.d)$"),
    "A": re.compile(r"^(lr|sc|amo[a-z]+)\.[wd](\.aq|\.rl|\.aqrl)?$"),
}
Refusal = A.Refusal


def configure() -> None:
    """The ACT4 helpers read their profile and scratch from module globals; this campaign sets them once."""
    A.PROFILE = PROFILE
    A.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)


def derive_check() -> None:
    proc = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/derive_workload_constants.py"), "--check"],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise Refusal("the workloads' expected constants drift from their derivation:\n" + proc.stdout + proc.stderr)


def build(clang: str, lld: list[str], name: str, source_dir: Path = WORKLOAD) -> Path:
    src = source_dir / f"{name}.c"
    if not src.is_file():
        raise Refusal(f"{src} is not a tracked workload")
    objs = []
    for unit in (source_dir / "wl-start.S", src):
        obj = OUT / (unit.stem + (".start.o" if unit.suffix == ".S" else ".o"))
        proc = subprocess.run([clang, *CFLAGS, f"-I{source_dir}", f"-I{ROOT / f'profiles/{PROFILE}/act4'}",
                               "-c", str(unit), "-o", str(obj)], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise Refusal(f"{name}: clang refused {unit.name}:\n{proc.stderr[:2000]}")
        objs.append(obj)
    elf = OUT / f"{name}.elf"
    proc = subprocess.run([*lld, "-T", str(source_dir / "wl-link.ld"), "-o", str(elf), *map(str, objs)],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise Refusal(f"{name}: ld.lld refused the link:\n{proc.stderr[:2000]}")
    return elf


def census(objdump: str, elf: Path) -> dict:
    """What the ELF contains: instruction count, compressed count, the extension families present."""
    proc = subprocess.run([objdump, "-d", str(elf)], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise Refusal(f"{elf.name}: llvm-objdump refused the file (rc={proc.returncode}): {proc.stderr.strip()[:300]} — the "
                      f"disassembly census found no instruction")
    text = proc.stdout
    insns = [line for line in text.splitlines() if re.match(r"^[0-9a-f]+: ([0-9a-f]{4}|[0-9a-f]{8})\s", line)]
    mnemonics = [line.split()[2] for line in insns if len(line.split()) > 2]
    families = [f for f, pattern in FAMILY.items() if any(pattern.match(m) for m in mnemonics)]
    if not insns:
        raise Refusal(f"{elf.name}: the disassembly census found no instruction — an unparseable dump is never an empty ELF")
    return {"instructions": len(insns),
            "compressed": sum(1 for line in insns if re.match(r"^[0-9a-f]+: [0-9a-f]{4}\s", line)),
            "families": "".join(sorted(families)) or "I"}


def experiment(clang: str, lld: list[str], nm: str, name: str, source_dir: Path = WORKLOAD) -> dict:
    print(f"\n== {name} ==")
    elf = build(clang, lld, name, source_dir)
    syms = A.symbols(nm, elf)
    lo, hi, tohost = syms["begin_signature"], syms["end_signature"], syms["tohost"]
    cen = census(str(Path(clang).parent / "llvm-objdump"), elf)
    A.say(True, f"{name}: built", f"{cen['instructions']} instructions ({cen['compressed']} compressed), "
          f"families {cen['families']}, signature [{lo:#x}, {hi:#x}), tohost {tohost:#x}")
    sail_st = A.run_model("sail", elf, None)
    spike_st = A.run_model("spike", elf, None)
    sail_steps = sum(1 for line in (OUT / f"{elf.stem}.sail.trace").read_text().splitlines()
                     if re.match(r"^\[\d+\]\s+\[\w+\]:", line.strip()))
    if sail_steps == 0:
        raise Refusal(f"{name}: sail executed no instruction — an unparseable trace is never an empty match")
    budget = 4 * sail_steps + 10_000
    semulith_st = A.run_model("semulith", elf, budget)
    A.say(True, f"{name}: budgets", f"sail executed {sail_steps} steps; semulith ran with a budget of {budget}")
    verdicts, sigs = {}, {}
    for model, st in (("sail", sail_st), ("spike", spike_st), ("semulith", semulith_st)):
        v, console = A.verdict(st, tohost)
        verdicts[model] = v
        sigs[model] = A.signature(st, lo, hi)
        A.say(v == 1, f"{name}: {model} HTIF verdict", f"tohost <- {v}")
    comparisons = {}
    for left, right, key, label in (("semulith", "sail", "signature", "semulith vs the Sail-derived signature"),
                                    ("spike", "sail", "control", "spike vs sail — the control pair")):
        mismatch = A.first_mismatch(sigs[left], sigs[right], (left, right))
        comparisons[key] = mismatch
        A.say(mismatch is None, f"{name}: {label}", f"{len(sigs[left])} slots agree" if mismatch is None else mismatch)
    return {"file": f"{name}.c", "signature_slots": len(sigs["sail"]), "sail_steps": sail_steps, **cen,
            "verdict_semulith": "pass" if verdicts["semulith"] == 1 else "fail",
            "verdict_sail": "pass" if verdicts["sail"] == 1 else "fail",
            "verdict_spike": "pass" if verdicts["spike"] == 1 else "fail",
            "signature": "agree" if comparisons["signature"] is None else "mismatch",
            "control": "agree" if comparisons["control"] is None else "mismatch"}


def all_pass(results: list[dict]) -> bool:
    """The record's gate: every verdict pass and every comparison agree — the same predicate --record uses."""
    return all(r["verdict_semulith"] == r["verdict_sail"] == r["verdict_spike"] == "pass"
               and r["signature"] == r["control"] == "agree" for r in results)


def write_record(results: list[dict], clang: str, lld: list[str]) -> Path:
    compiler = subprocess.run([clang, "--version"], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    linker = subprocess.run([*lld, "--version"], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    passed = sum(1 for r in results if r["verdict_semulith"] == r["verdict_sail"] == r["verdict_spike"] == "pass"
                 and r["signature"] == r["control"] == "agree")
    rows = "\n".join(
        f'  (workload (file "{r["file"]}") (instructions {r["instructions"]}) (compressed {r["compressed"]})\n'
        f'            (families "{r["families"]}") (sail_steps {r["sail_steps"]}) (signature_slots {r["signature_slots"]})\n'
        f'            (verdict_semulith "{r["verdict_semulith"]}") (verdict_sail "{r["verdict_sail"]}") '
        f'(verdict_spike "{r["verdict_spike"]}")\n'
        f'            (signature "{r["signature"]}") (control "{r["control"]}"))' for r in results)
    doc = f"""(comment "GENERATED by scripts/run_workload_campaign.py --record from a live three-way run."
         "Canonical inputs: the tracked workload sources profiles/{PROFILE}/workload/ (their expected"
         " constants re-derived by scripts/derive_workload_constants.py), the pinned toolchain, the pinned"
         " reference binaries (references.sexp). The references are untracked by design: this is a RECORDED"
         " experiment — the commit gate checks shape and internal consistency (RECORD-SCHEMA rule 15), never"
         " re-execution. Re-run: python3 scripts/run_workload_campaign.py --record.")
(workload-campaign
  (profile "{PROFILE}")
  (toolchain (compiler "{compiler}") (linker "{linker}"))
  (run (date "{datetime.date.today().isoformat()}") (workloads {len(results)})
       (signature_slots {sum(r["signature_slots"] for r in results)})
       (verdicts "{passed} pass / {len(results) - passed} fail"))
  (evidence_note "Compiled, self-checking workloads judged against the Sail-derived signature — one semantics answering twice, never a second independent semantics (EVD-04); spike against sail is the control pair. Each expected constant is derived from the C abstract machine before any model runs (EVD-05); the instruction census is the ELF's fact, not the source's.")
{rows})
"""
    out = ROOT / f"profiles/{PROFILE}/workload.sexp"
    out.write_text(doc)
    return out


def self_test() -> int:
    """RED/GREEN controls: a wrong expected constant is caught by every model's verdict and recorded as a
    failing row (and `--record` refuses it); a drifted derivation refuses before any build; a workload
    without the signature symbols refuses; the census refuses an empty disassembly."""
    import shutil, tempfile
    npass = nfail = 0

    def arm(name: str, ok: bool, want_sub: str, detail: str) -> None:
        nonlocal npass, nfail
        if ok and want_sub in detail:
            npass += 1
        else:
            nfail += 1
            print(f"run_workload_campaign self-test MISS: {name} (ok={ok}, detail={detail!r})", file=sys.stderr)

    configure()
    clang, lld, nm = A.toolchain()
    with tempfile.TemporaryDirectory(prefix="workload-selftest-", dir=OUT) as td:
        scratch = Path(td)
        for piece in ("wl-start.S", "wl-link.ld", "wl-common.h"):
            shutil.copy(WORKLOAD / piece, scratch / piece)
        # RED: a wrong constant — the workload's own check fails on every model, honestly recorded
        wrong = (WORKLOAD / "wl-calls.c").read_text().replace("EMIT(fib(opaque(15)), 610);", "EMIT(fib(opaque(15)), 611);")
        if wrong == (WORKLOAD / "wl-calls.c").read_text():
            raise Refusal("self-test: the fib constant to mutate is not where the control expects it")
        (scratch / "wl-calls.c").write_text(wrong)
        row = experiment(clang, lld, nm, "wl-calls", scratch)
        arm("RED   a wrong expected constant fails every model's verdict",
            row["verdict_semulith"] == row["verdict_sail"] == row["verdict_spike"] == "fail", "", str(row))
        arm("RED   … while the three models still agree on the signature (the control holds)",
            row["signature"] == "agree" and row["control"] == "agree", "", str(row))
        arm("RED   the record's gate refuses a failing row", not all_pass([row]), "", str(all_pass([row])))
        # RED: no signature symbols — the labels themselves are gone, not merely their visibility
        shim = (WORKLOAD / "wl-start.S").read_text().replace("begin_signature", "begin_sig").replace("end_signature", "end_sig")
        (scratch / "wl-start.S").write_text(shim)
        try:
            experiment(clang, lld, nm, "wl-calls", scratch)
            arm("RED   a workload without signature symbols refuses", False, "", "no refusal")
        except Refusal as exc:
            arm("RED   a workload without signature symbols refuses", True, "exports no", str(exc))
    # RED: a census over something that is not code — the linker script — finds no instruction and refuses
    arm("RED   an empty disassembly refuses", True, "no instruction",
        A._refused(lambda: census(str(Path(clang).parent / "llvm-objdump"), WORKLOAD / "wl-link.ld")))
    print(f"run_workload_campaign --self-test: {npass} pass / {nfail} fail")
    return 0 if nfail == 0 else 1


def main(argv: list[str]) -> int:
    names = argv[1:]
    if names == ["--self-test"]:
        try:
            return self_test()
        except Refusal as exc:
            print(f"run_workload_campaign: REFUSED — {exc}", file=sys.stderr)
            return 2
    record = "--record" in names
    if record:
        names.remove("--record")
    names = names or list(WORKLOADS)
    for name in names:
        if name not in WORKLOADS:
            print(f"run_workload_campaign: REFUSED — no workload named '{name}' ({', '.join(WORKLOADS)})", file=sys.stderr)
            return 2
    try:
        configure()
        derive_check()
        clang, lld, nm = A.toolchain()
        results = [experiment(clang, lld, nm, name) for name in names]
    except Refusal as exc:
        print(f"\nrun_workload_campaign: REFUSED — {exc}", file=sys.stderr)
        return 2
    ok = all_pass(results)
    print()
    if not ok:
        print("run_workload_campaign: FAILED — a verdict or a comparison did not pass (see the lines above)", file=sys.stderr)
        return 1
    print("run_workload_campaign: ok — every verdict is pass and every signature agrees (semulith vs the Sail-derived "
          "expectations; spike vs sail, the control)")
    if record:
        if set(names) != set(WORKLOADS):
            print("run_workload_campaign: REFUSED — --record needs every workload, not a selection", file=sys.stderr)
            return 2
        out = write_record(results, clang, lld)
        print(f"run_workload_campaign: recorded {out.relative_to(ROOT)} ({len(results)} workload rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
