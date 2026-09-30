#!/usr/bin/env python3
"""Run the ACT4 external campaign (P2-SCALAR.5 strand 2): the pinned riscv-arch-test
RV64I suite against semulith, with Sail-derived expectations and spike as the control.

Per test file (`tests/rv64i/I/I-*.S` of the pinned sparse clone): assemble + link with
the pinned toolchain (clang 21.1.8 + ld.lld, the `build_c_guest.sh` discovery) against
the laboratory's own DUT-side pieces (`profiles/rv64i-lab-v0/act4/`), run the
SIGNATURE-mode ELF on all three models, and extract from each store trace:

  - the SIGNATURE — the ordered stores into `[begin_signature, end_signature)`; each
    8-byte slot is one RVTEST_SIGUPD result word. sail-riscv 0.14's signature IS the
    expected values (ACT derives its expectations from a configured Sail model — the
    `references.sexp` independence inventory records that shared ancestry; this is
    EXTERNAL-TEST evidence, never a second independent semantics, `EVD-04`);
  - the VERDICT — the HTIF pair (store of 1|3 to `tohost` low word, then 0 to the high
    word); a console pair stores the byte low and 0x01010000 high;
  - the comparison — semulith's signature against the Sail-derived one, word by word
    (first mismatch is the minimized discrepancy, `EVD-02`, named by sigupd ordinal),
    and spike's against sail's (the control pair: the genuine differential).

⛔ NOT A COMMIT GATE. It needs the untracked sparse clone (`scripts/fetch_act4.sh`) and
the reference binaries (`scripts/fetch_references.sh`) — the same standing as
`run_semulith_smoke.py`. The commit-gate side of the campaign is the recorded dossier
(`profiles/rv64i-lab-v0/act4.sexp`) and its schema check.

usage: run_act4_campaign.py [I-add-00 ...]   (default: I-add-00 — the slice-(b) probe)
       run_act4_campaign.py --all            (the full RV64I suite)
       run_act4_campaign.py --self-test      (the RED/GREEN controls)
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dossier_sexp as D

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
PROFILE = "rv64i-lab-v0"
ACT4 = ROOT / "target/refs/riscv-arch-test"
ACT4_PIN = "e2216915d9a17acc142610831d88de8b65683866"
DUT = ROOT / f"profiles/{PROFILE}/act4"
SAIL = ROOT / "target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim"
SPIKE = ROOT / "target/refs/spike-build/spike"
OUT = ROOT / "target/refs/guests/act4"
SUITE = ACT4 / "tests/rv64i/I"

failures: list[str] = []


def say(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{('  ' + detail) if detail else ''}")
    if not ok:
        failures.append(label)


class Refusal(Exception):
    """A missing input or an unparseable observation — never an empty pass."""


def require() -> None:
    if not ACT4.is_dir():
        raise Refusal(f"{ACT4} is absent — fetch it with scripts/fetch_act4.sh")
    head = subprocess.run(["git", "-C", str(ACT4), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=False).stdout.strip()
    if head != ACT4_PIN:
        raise Refusal(f"the ACT4 clone is at {head or '?<unreadable>'}, not the pinned "
                      f"{ACT4_PIN} — re-run scripts/fetch_act4.sh")
    for tool, hint in ((SAIL, "fetch_references.sh"), (SPIKE, "fetch_references.sh")):
        if not tool.exists():
            raise Refusal(f"{tool} is missing — {hint}")


def toolchain() -> tuple[str, list[str], str]:
    """The pinned toolchain, probed exactly as scripts/build_c_guest.sh does."""
    import os
    probe_out = OUT / ".probe.o"
    OUT.mkdir(parents=True, exist_ok=True)
    clang = None
    candidates = [os.environ.get("SEMULITH_RISCV_CLANG") or "",
                  "/opt/homebrew/opt/llvm@21/bin/clang", "clang"]
    for cand in candidates:
        if not cand:
            continue
        proc = subprocess.run(
            [cand, "--target=riscv64-unknown-elf", "-march=rv64i", "-mabi=lp64",
             "-x", "c", "-c", "-o", str(probe_out), "-"],
            input=b"int f(int a, int b) { return a + b; }\n",
            capture_output=True, check=False)
        if proc.returncode == 0:
            clang = cand
            break
    probe_out.unlink(missing_ok=True)
    if clang is None:
        raise Refusal("no clang with a RISC-V backend (probed $SEMULITH_RISCV_CLANG, "
                      "/opt/homebrew/opt/llvm@21/bin/clang, clang) — see "
                      "docs/decisions/decision_c-guest-routing-and-toolchain.md")
    if os.environ.get("SEMULITH_RISCV_LLD"):
        lld = [os.environ["SEMULITH_RISCV_LLD"]]
    elif subprocess.run(["command", "-v", "ld.lld"], capture_output=True,
                        check=False).returncode == 0:
        lld = ["ld.lld"]
    elif subprocess.run(["command", "-v", "zig"], capture_output=True,
                        check=False).returncode == 0:
        lld = ["zig", "ld.lld"]
    else:
        raise Refusal("no ld.lld (probed $SEMULITH_RISCV_LLD, ld.lld, zig)")
    nm = str(Path(clang).parent / "llvm-nm")
    if not Path(nm).exists():
        raise Refusal(f"{nm} is missing — the symbol reader comes from the pinned "
                      f"clang's own LLVM keg")
    return clang, lld, nm


def build(clang: str, lld: list[str], name: str) -> Path:
    src = SUITE / f"{name}.S"
    if not src.is_file():
        raise Refusal(f"{src} is not in the sparse clone")
    obj, elf = OUT / f"{name}.o", OUT / f"{name}.elf"
    march = None
    for line in src.read_text().splitlines():
        m = re.match(r"# MARCH: (\S+)", line)
        if m:
            march = m.group(1)
            break
    if march is None:
        raise Refusal(f"{name}: no MARCH key in the test-config header")
    proc = subprocess.run(
        [clang, "--target=riscv64-unknown-elf", f"-march={march}", "-mabi=lp64",
         "-mno-relax", f"-I{ACT4}/tests/env", f"-I{DUT}",
         f"-DTEST_FILE=\"{name}.S\"", "-DTEST_FLEN=32",
         "-DSAIL_CLINT_BASE_ADDRESS=0x2000000",
         "-DSAIL_SIMPLE_INTERRUPT_GENERATOR_BASE_ADDRESS=0xC000000",
         "-c", str(src), "-o", str(obj)],
        capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise Refusal(f"{name}: clang refused the build:\n{proc.stderr[:2000]}")
    proc = subprocess.run([*lld, "-T", str(DUT / "link.ld"), "-o", str(elf), str(obj)],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise Refusal(f"{name}: ld.lld refused the link:\n{proc.stderr[:2000]}")
    return elf


def symbols(nm: str, elf: Path) -> dict[str, int]:
    out = subprocess.run([nm, str(elf)], capture_output=True, text=True,
                         check=True).stdout
    syms = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[2] in ("begin_signature", "end_signature",
                                            "tohost", "rvtest_entry_point"):
            syms[parts[2]] = int(parts[0], 16)
    missing = {"begin_signature", "end_signature", "tohost",
               "rvtest_entry_point"} - syms.keys()
    if missing:
        raise Refusal(f"{elf.name}: the ELF exports no {sorted(missing)} — the "
                      f"signature region and the verdict channel are unobservable")
    return syms


# ---- the three store vocabularies, each MEASURED (P2-SCALAR.5 strand 2b) -------------
# semulith --trace-stores:  mem[8,0x0000000080015e20] <- 0x0000000000000001   (width ours)
# sail --trace-mem:         mem[W,0x0000000080015E28] <- 0x7CFF6728488620D9   (W = write)
# spike -l --log-commits:   core   0: 3 0x... (0x...) mem 0x0000000080015e28 0x7cff...
#                           (a load's line ends `mem 0xADDR` with NO value — the
#                           anchored two-group match below can only take a store)
_SEMULITH_STORE = re.compile(r"^mem\[\d+,0x([0-9a-f]+)\] <- 0x([0-9a-f]+)$")
_SAIL_STORE = re.compile(r"^mem\[W,0x([0-9A-Fa-f]+)\] <- 0x([0-9A-Fa-f]+)$")
_SPIKE_STORE = re.compile(r"^core\s+\d+:.*\smem 0x([0-9a-f]+) 0x([0-9a-f]+)$")


def stores(text: str, pattern: re.Pattern[str], who: str) -> list[tuple[int, int]]:
    out = [(int(m.group(1), 16), int(m.group(2), 16))
           for line in text.splitlines() if (m := pattern.match(line.strip()))]
    if not out:
        raise Refusal(f"{who}: no store crossings parsed — an unparseable trace is "
                      f"never an empty match")
    return out


def signature(st: list[tuple[int, int]], lo: int, hi: int) -> list[tuple[int, int]]:
    return [(a, v) for a, v in st if lo <= a < hi]


def verdict(st: list[tuple[int, int]], tohost: int) -> tuple[int, str]:
    """The first HTIF verdict pair: (tohost <- 1|3) immediately followed by
    (tohost+4 <- 0). A console pair stores the byte low and 0x01010000 high, so the
    high-word value is what distinguishes the channels."""
    console = bytearray()
    for i in range(len(st) - 1):
        (a0, v0), (a1, v1) = st[i], st[i + 1]
        if a0 == tohost and a1 == tohost + 4:
            if v1 == 0 and v0 in (1, 3):
                return v0, console.decode(errors="replace")
            if v1 == 0x01010000:
                console.append(v0 & 0xFF)
    raise Refusal("no HTIF verdict pair in the store trace — the test neither passed "
                  "nor failed observably (a hang, a wrong tohost, or a truncated run)")


def run_model(model: str, elf: Path, budget: int | None) -> list[tuple[int, int]]:
    trace = OUT / f"{elf.stem}.{model}.trace"
    if model == "semulith":
        assert budget is not None
        proc = subprocess.run(
            ["cargo", "run", "--quiet", "-p", "semulith-cli", "--", "run", str(elf),
             f"--steps={budget}", "--trace-stores"],
            capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise Refusal(f"semulith run failed (rc={proc.returncode}):\n{proc.stderr}")
        return stores(proc.stdout, _SEMULITH_STORE, model)
    if model == "sail":
        subprocess.run(
            [str(SAIL), "--config-override",
             str(D.materialize_sail_override(ROOT, PROFILE)),
             "--inst-limit", str(budget or 10_000_000),
             "--trace-instr", "--trace-mem", "--trace-output", str(trace), str(elf)],
            capture_output=True, text=True, check=False)
        return stores(trace.read_text(), _SAIL_STORE, model)
    if model == "spike":
        subprocess.run(
            [str(SPIKE), "--isa=rv64i", "--priv=m", "-l", "--log-commits",
             f"--log={trace}",
             f"--instructions={(budget or 10_000_000) + 5}", str(elf)],
            capture_output=True, text=True, check=False)
        return stores(trace.read_text(), _SPIKE_STORE, model)
    raise AssertionError(model)


def first_mismatch(a: list[tuple[int, int]], b: list[tuple[int, int]],
                   names: tuple[str, str]) -> str | None:
    """None on agreement; the minimized discrepancy otherwise (EVD-02). The slot index
    names the RVTEST_SIGUPD ordinal — the testcase."""
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return (f"sigupd #{i}: {names[0]} stored 0x{a[i][1]:016x} at "
                    f"0x{a[i][0]:016x}, {names[1]} stored 0x{b[i][1]:016x} at "
                    f"0x{b[i][0]:016x}")
    if len(a) != len(b):
        return (f"LENGTH MISMATCH: {names[0]} wrote {len(a)} signature slot(s), "
                f"{names[1]} wrote {len(b)} — a shorter signature is not agreement")
    return None


def experiment(clang: str, lld: list[str], nm: str, name: str) -> dict:
    print(f"\n== {name} ==")
    elf = build(clang, lld, name)
    syms = symbols(nm, elf)
    lo, hi, tohost = syms["begin_signature"], syms["end_signature"], syms["tohost"]
    say(True, f"{name}: built",
        f"entry {syms['rvtest_entry_point']:#x}, signature [{lo:#x}, {hi:#x}) "
        f"({(hi - lo) // 8} slots incl. canaries/offsets), tohost {tohost:#x}")

    # sail first, WITH instruction tracing: its executed step count sets semulith's
    # budget (sail and spike self-terminate on the HTIF verdict; semulith's halt is a
    # store loop stopped only by the budget — a fixed budget would spin it into a
    # giant trace). The margin covers the halt loop and any scheduling asymmetry.
    sail_trace = OUT / f"{elf.stem}.sail.trace"
    sail_st = run_model("sail", elf, None)
    spike_st = run_model("spike", elf, None)
    sail_steps = sum(1 for line in sail_trace.read_text().splitlines()
                     if re.match(r"^\[\d+\]\s+\[\w+\]:", line.strip()))
    if sail_steps == 0:
        raise Refusal(f"{name}: sail executed no instruction — an unparseable trace "
                      f"is never an empty match")
    budget = 4 * sail_steps + 10_000
    semulith_st = run_model("semulith", elf, budget)
    say(True, f"{name}: budgets", f"sail executed {sail_steps} steps; semulith ran "
        f"with a budget of {budget}")

    sigs = {}
    verdicts = {}
    for model, st in (("sail", sail_st), ("spike", spike_st),
                      ("semulith", semulith_st)):
        v, console = verdict(st, tohost)
        verdicts[model] = v
        sigs[model] = signature(st, lo, hi)
        say(v == 1, f"{name}: {model} HTIF verdict", console.strip().splitlines()[-1]
            if console else f"tohost <- {v}")

    # The evidence: semulith vs the SAIL-DERIVED signature (external tests, EVD-04 —
    # never a second opinion); the control: spike vs sail (the genuine differential).
    comparisons = {}
    for left, right, key, label in (
            ("semulith", "sail", "signature", "semulith vs the Sail-derived signature"),
            ("spike", "sail", "control", "spike vs sail — the control pair")):
        mismatch = first_mismatch(sigs[left], sigs[right], (left, right))
        comparisons[key] = mismatch
        say(mismatch is None, f"{name}: {label}",
            f"{len(sigs[left])} slots agree" if mismatch is None else mismatch)
    return {"file": f"{name}.S", "signature_slots": len(sigs["sail"]),
            "verdict_semulith": "pass" if verdicts["semulith"] == 1 else "fail",
            "verdict_sail": "pass" if verdicts["sail"] == 1 else "fail",
            "verdict_spike": "pass" if verdicts["spike"] == 1 else "fail",
            "signature": "agree" if comparisons["signature"] is None else "mismatch",
            "control": "agree" if comparisons["control"] is None else "mismatch"}


def self_test() -> int:
    """RED/GREEN controls for the extractor and the comparator — a campaign that has
    only ever said AGREE is not known to disagree (the `NO CONTROL` doctrine)."""
    npass = nfail = 0

    def arm(name: str, ok: bool, want_sub: str, detail: str) -> None:
        nonlocal npass, nfail
        if ok and want_sub in detail:
            npass += 1
        else:
            nfail += 1
            print(f"run_act4_campaign self-test MISS: {name} "
                  f"(ok={ok}, detail={detail!r})", file=sys.stderr)

    sig = [(0x1000 + 8 * i, 0xA000 + i) for i in range(4)]
    arm("GREEN identical signatures", (m := first_mismatch(sig, sig, ("a", "b"))) is None,
        "", m or "")
    arm("RED   a wrong value is caught at its ordinal",
        (m := first_mismatch(sig, sig[:2] + [(0x1010, 0xDEAD)] + sig[3:], ("a", "b"))) is not None,
        "sigupd #2", m or "")
    arm("RED   a shorter signature is not agreement",
        (m := first_mismatch(sig, sig[:3], ("a", "b"))) is not None,
        "LENGTH MISMATCH", m or "")

    tohost = 0x2000
    pass_seq = sig + [(tohost, 1), (tohost + 4, 0)]
    console_then_fail = (sig + [(tohost, 0x52), (tohost + 4, 0x01010000),
                                (tohost, 3), (tohost + 4, 0)])
    v, _ = verdict(pass_seq, tohost)
    arm("GREEN the pass verdict is read", v == 1, "", f"v={v}")
    v, con = verdict(console_then_fail, tohost)
    arm("GREEN a console byte is not a verdict; the fail verdict follows it",
        v == 3 and con == "R", "", f"v={v} console={con!r}")
    try:
        verdict(sig, tohost)
        arm("RED   no verdict pair refuses", False, "", "no refusal")
    except Refusal as exc:
        arm("RED   no verdict pair refuses", True, "no HTIF verdict", str(exc))
    arm("RED   a store-less trace refuses", True, "no store crossings",
        _refused(lambda: stores("", _SAIL_STORE, "sail")))

    print(f"run_act4_campaign --self-test: {npass} pass / {nfail} fail")
    return 0 if nfail == 0 else 1


def _refused(fn) -> str:
    try:
        fn()
    except Refusal as exc:
        return str(exc)
    return ""


def write_record(results: list[dict], clang: str, lld: list[str]) -> Path:
    """Emit the campaign dossier `profiles/<unit>/act4.sexp` from the MEASURED rows —
    a recorded experiment (schema `schema/act4.sexp`; the `run` counts re-derived from
    the rows here so the dossier never carries a number its rows contradict)."""
    compiler = subprocess.run([clang, "--version"], capture_output=True, text=True,
                              check=True).stdout.splitlines()[0]
    linker = subprocess.run([*lld, "--version"], capture_output=True, text=True,
                            check=True).stdout.splitlines()[0]
    passed = sum(1 for r in results
                 if r["verdict_semulith"] == r["verdict_sail"] == r["verdict_spike"]
                 == "pass" and r["signature"] == r["control"] == "agree")
    rows = []
    for r in results:
        rows.append(
            f'  (test (file "{r["file"]}") (signature_slots {r["signature_slots"]})\n'
            f'        (verdict_semulith "{r["verdict_semulith"]}") '
            f'(verdict_sail "{r["verdict_sail"]}") (verdict_spike "{r["verdict_spike"]}")\n'
            f'        (signature "{r["signature"]}") (control "{r["control"]}"))')
    import datetime
    doc = f"""(comment "GENERATED by scripts/run_act4_campaign.py --record from a live three-way run."
         "Canonical inputs: the pinned sparse clone (suite.pin), the DUT-side pieces"
         " profiles/rv64i-lab-v0/act4/, the pinned reference binaries (references.sexp)."
         " The inputs are untracked by design: this is a RECORDED experiment — the commit"
         " gate checks shape and internal consistency (RECORD-SCHEMA rule 13), never"
         " re-execution. Re-run: scripts/fetch_act4.sh && python3"
         " scripts/run_act4_campaign.py --record.")
(act4-campaign
  (profile "{PROFILE}")
  (suite (origin "https://github.com/riscv/riscv-arch-test") (branch "act4")
         (pin "{ACT4_PIN}")
         (sparse_paths "tests/env") (sparse_paths "tests/rv64i/I")
         (sparse_paths "config"))
  (toolchain (compiler "{compiler}") (linker "{linker}"))
  (run (date "{datetime.date.today().isoformat()}") (tests {len(results)})
       (signature_slots {sum(r["signature_slots"] for r in results)})
       (verdicts "{passed} pass / {len(results) - passed} fail"))
  (evidence_note "External tests with Sail-derived expectations — ACT derives its expected results from a configured Sail model, so agreement with sail-riscv is one semantics answering twice (EVD-04; the shared ancestry is the recorded independence row in references.sexp). spike vs sail is the control pair: the genuine differential. A slot is one RVTEST_SIGUPD result word, read from the store trace's writes into [begin_signature, end_signature).")
{chr(10).join(rows)})
"""
    out = ROOT / f"profiles/{PROFILE}/act4.sexp"
    out.write_text(doc)
    return out


def main(argv: list[str]) -> int:
    names = argv[1:]
    if names == ["--self-test"]:
        return self_test()
    record = False
    if "--record" in names:
        names.remove("--record")
        record = True
    if names == ["--all"] or (record and not names):
        names = sorted(p.stem for p in SUITE.glob("I-*.S"))
    if record and len(names) != 51:
        print("run_act4_campaign: --record requires the full fleet (--all) — a partial "
              "record would masquerade as the campaign", file=sys.stderr)
        return 2
    if not names:
        names = ["I-add-00"]
    print(f"the ACT4 external campaign for {PROFILE} "
          f"(pinned riscv-arch-test {ACT4_PIN[:12]}…, {len(names)} test file(s))")
    results = []
    try:
        require()
        clang, lld, nm = toolchain()
        for name in names:
            results.append(experiment(clang, lld, nm, name))
    except Refusal as exc:
        print(f"run_act4_campaign: REFUSED — {exc}", file=sys.stderr)
        return 2
    print()
    if failures:
        print(f"run_act4_campaign: FAILED ({len(failures)} check(s)): "
              f"{', '.join(failures)}", file=sys.stderr)
        return 1
    print("run_act4_campaign: ok — every verdict is pass and every signature agrees "
          "(semulith vs the Sail-derived expectations; spike vs sail, the control)")
    if record:
        out = write_record(results, clang, lld)
        print(f"run_act4_campaign: recorded {out.relative_to(ROOT)} "
              f"({len(results)} test rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
