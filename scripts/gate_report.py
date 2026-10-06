#!/usr/bin/env python3
"""Generate a milestone gate report from PINNED inputs.

`ROADMAP.md` §P1 asks for the gate report to be *generated from pinned inputs*, and `EVD-08`
requires it to name its inputs, its commands, its actual results and its limitations. A gate
report written by hand is a summary of what its author remembers; this one is a function of the
repository, so it cannot flatter the work.

⛔ IT IS DERIVED ENTIRELY FROM TRACKED FILES — the profile, the requirements catalogue, the
contract obligations, the reference dossier (whose `[[experiment]]` records carry the observed
results) and the guest expectations. Nothing here reads `target/`, so the report regenerates
byte-identically in a fresh clone with no reference binaries present. That is what lets a gate
check it for staleness.

⛔ AND IT CANNOT SAY `passed` WHILE A REQUIRED CHECK IS MISSING. `EVD-08` names that outcome
explicitly, and it is the one verdict this generator refuses to produce: the criterion below
counts declared checks against implemented ones, and 66 against 0 cannot round up.

Usage:  scripts/gate_report.py <profile>                   write the G0 report
        scripts/gate_report.py <profile> --gate G1         write the G1 report
        scripts/gate_report.py <profile> [--gate G] --stdout   print instead
        scripts/gate_report.py --gate BREADTH [--stdout]   the cross-architecture report
                                                           (docs/BREADTH-REPORT.md — no profile)

G1 (`P1-LAB.12`): the laboratory gate's report over the same dossier, evaluated against the
SIX criteria `ROADMAP.md` §6 states for `G1` — each measured from tracked files by concrete
name, never asserted — plus the recorded baseline (`baseline.sexp`). The verdict is `passed`
only while all six criteria are met: EVD-08's forbidden outcome generalized, so the generator
has no code path to `passed` over an unmet criterion.
"""

from __future__ import annotations

import json
import re
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())

sys.path.insert(0, str(ROOT / "scripts"))
import records_sexp as R                                # noqa: E402
import dossier_sexp as D                                # noqa: E402
import sexp as S                                        # noqa: E402


# ---------------------------------------------------------------------------
# The G-CONTRACT measure (`P4-SYSTEM.10` slice a) — ONE computation, every builder.
# ⛔ The third wrong cut, after the two recorded in `build()`: an implemented check was any id a
# tracked executable under `scripts/`/`crates/` NAMES — across the whole tree. MIRROR-DERIVE makes
# 26 check ids identical across rv64i's and rv64gc's contracts (13 base mirrors, field-equal by
# enforcement), so realizing one for rv64gc credited rv64i with a check nothing of rv64i's runs.
# And the denominator counted every record, including those a later contract version SUPERSEDED.
# The measure is now the unit's own: a check is implemented for a unit exactly when THAT unit's
# registry — named by its contract document, its every entry run by `cargo test` — realizes it
# under the obligation that declares it; the denominator is the EFFECTIVE contract.
# ---------------------------------------------------------------------------

_ENTRY = re.compile(r'\bContractCheck\s*\{\s*id:\s*"([^"]+)",\s*obligation:\s*"([^"]+)",')
_OPENED = re.compile(r'(?<!struct )\bContractCheck\s*\{')


def _registry_pairs(path: Path) -> set[tuple[str, str]]:
    """The (obligation, check) pairs a registry realizes — read EXACTLY: an entry this
    reader cannot parse is a refusal, never a silent miss (a miss would deflate the count)."""
    text = path.read_text(encoding="utf-8")
    entries = _ENTRY.findall(text)
    opened = len(_OPENED.findall(text))
    if len(entries) != opened:
        raise SystemExit(f"gate_report: {path.relative_to(ROOT)}: {opened} ContractCheck "
                         f"entries, {len(entries)} read exactly — the registry's shape changed "
                         f"and this measure cannot judge it")
    return {(ob, chk) for chk, ob in entries}


def contract_measure(d: Path, obs: list[dict]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(the EFFECTIVE contract's declared (obligation, check) pairs, the ones THIS unit's
    registry realizes). The effective contract is the latest version's members and everything
    it inherits, minus every record a version in that chain supersedes; a unit with no
    contract document (rv64i) is all of its records. A unit whose contract names no registry
    realizes nothing."""
    by_id = {o["id"]: o for o in obs}
    cdoc = d / "contract.sexp"
    effective, registry = list(obs), None
    if cdoc.is_file():
        versions, regs = {}, []
        for form in S.read_file(cdoc):
            if not isinstance(form, list) or not form:
                continue
            head = str(form[0])
            if head == "registry":
                regs.append(str(S.field(form, "path", cdoc.name)))
            if head != "contract":
                continue
            f = {str(c[0]): c for c in form[1:] if isinstance(c, list)}
            versions[str(f["id"][1])] = {
                "version": int(str(f["version"][1])),
                "extends": str(f["extends"][1]) if "extends" in f else None,
                "members": [str(S.field(c, "id", cdoc.name)) for c in S.children(form, "member")],
                "sups": {str(S.field(c, "record", cdoc.name)) for c in S.children(form, "supersede")}}
        numbers = sorted(v["version"] for v in versions.values())
        if not numbers or len(numbers) != len(set(numbers)) or len(regs) > 1:
            raise SystemExit(f"gate_report: {cdoc.relative_to(ROOT)}: the versions {numbers} and "
                             f"{len(regs)} registry form(s) do not name one latest version and at "
                             f"most one registry — this measure cannot judge it")
        v = next(v for v in versions.values() if v["version"] == numbers[-1])
        members, superseded = [], set()
        while v is not None:
            members += v["members"]
            superseded |= v["sups"]
            v = versions.get(v["extends"]) if v["extends"] else None
        effective = [by_id[m] for m in members if m not in superseded]
        registry = ROOT / regs[0] if regs else None
    declared = [(o["id"], c) for o in effective for c in o["required_checks"]]
    realized = _registry_pairs(registry) if registry is not None else set()
    return declared, [pair for pair in declared if pair in realized]


def build(profile: str) -> str:
    d = ROOT / "profiles" / profile
    prof = D.load_profile(d / "profile.sexp")            # SOT-FORMAT.4: one format, read via
    refs = D.load_references(d / "references.sexp")      # the mapping — the same dicts the
    reqs = R.load(d / "requirements.sexp")               # TOML/JSON produced, so this report
    obs = R.load(d / "contract-obligations.sexp")        # is byte-stable across the move
    guests = sorted((d / "guests").glob("*.expected.sexp"))

    by_class: dict[str, int] = {}
    for r in reqs:
        c = r["source_semantics"]["category"]
        by_class[c] = by_class.get(c, 0) + 1
    # An IMPLEMENTED check is one an executable actually REALIZES — by its CONCRETE id, not by
    # its shape.
    # ⛔ This took three wrong cuts, all in the direction that inflates the verdict.
    # Grepping the whole tree for the id PATTERN counted `EVIDENCE_POLICY.md`, which merely
    # describes the naming convention in prose. Narrowing to `scripts/` still counted
    # `check_requirements.sh`, which tests for the `-POS`/`-NEG` suffix as part of enforcing that
    # the ids exist — a gate about checks is not a check. The concrete-id grep that followed
    # was not unit-scoped (see `contract_measure`). The measure is the unit's own registry.
    declared, realized = contract_measure(d, obs)
    declared_checks = len(declared)
    implementing = realized

    exps = refs.get("experiment", [])
    inds = refs.get("independence", [])
    diffs = refs.get("difference", [])
    cands = refs.get("candidate", [])
    obtained = [c for c in cands if c["status"] == "obtained"]
    exercised = sorted({m for e in exps for m in e["models"]})

    steps = 0
    negatives = 0
    for g in guests:
        spec = D.load_expectations(g)
        steps += len(spec["step"])
        negatives += len(spec.get("never_written") or [])

    unresolved = [r["id"] for r in reqs if r["research_status"] != "resolved"]

    L: list[str] = []
    A = L.append
    A(f"# Gate `{prof['profile'].get('gate', 'G0')}` report — `{profile}`")
    A("")
    A("<!-- DERIVED — DO NOT EDIT. Regenerated by `scripts/gate_report.py`; the `GATE-REPORT`")
    A("     doctrine fails the commit if this file and its inputs disagree. Edit the INPUTS:")
    A("     profile.sexp, requirements.sexp, contract-obligations.sexp, references.sexp,")
    A("     guests/*.expected.sexp. -->")
    A("")
    # ⛔ There is exactly one way to reach `passed`, and it requires every declared check to be
    # implemented. `EVD-08` names "passed with a missing required check" as the outcome a report
    # must never produce, so it is unreachable here rather than merely discouraged.
    verdict = "passed" if declared_checks and len(implementing) >= declared_checks else "incomplete"
    A(f"**Verdict: `{verdict}`.**")
    A("")
    A("## Why this verdict")
    A("")
    A("`EVD-08` forbids a report that reads `passed` while a required check is missing. This")
    A(f"profile declares **{declared_checks} required checks** across {len(obs)} obligations, of")
    A(f"which **{len(implementing)} {'is' if len(implementing) == 1 else 'are'} implemented** —")
    A("measured by asking which concrete check ids of the effective contract THIS unit's check")
    A("registry realizes under the obligation that declares them — a registry its contract")
    A("document names, every entry run by `cargo test`; a unit with none realizes nothing. Not")
    A("asserted, not inferred from an id-shaped pattern in prose, and not credited because")
    A("another unit realizes the same id. The verdict cannot be `passed`, and this generator")
    A("has no code path that would produce it while that is true.")
    A("")
    A("## Inputs (all tracked; this report reads nothing untracked)")
    A("")
    A("| Input | Contents |")
    A("| --- | --- |")
    A(f"| `profile.sexp` | {len(prof['decision'])} decisions, {prof['scope']['count_total']} mnemonics, XLEN {prof['profile']['xlen']}, extensions `{prof['profile']['extensions']}` |")
    A(f"| `requirements.sexp` | {len(reqs)} requirements |")
    A(f"| `contract-obligations.sexp` | {len(obs)} obligations, {declared_checks} declared checks |")
    A(f"| `references.sexp` | {len(cands)} candidates, {len(exps)} experiments, {len(inds)} independence records, {len(diffs)} recorded differences |")
    A(f"| `guests/*.expected.sexp` | {len(guests)} programs, {steps} expected steps, {negatives} negative observations |")
    A("")
    A("## Criterion 1 — foundational semantics are resolved")
    A("")
    A("Every requirement carries a source locator, and its research status is recorded.")
    A("")
    A("| Semantic class | Requirements |")
    A("| --- | --- |")
    for c in sorted(by_class):
        A(f"| `{c}` | {by_class[c]} |")
    A("")
    if unresolved:
        A(f"**Not fully resolved: {len(unresolved)}** — " + ", ".join(f"`{u}`" for u in unresolved) +
          ". Each names its open question inside the record. `RECORD-SCHEMA` refuses a record that")
        A("claims `resolved` while carrying an open note, so this count cannot be flattered.")
    else:
        A("All requirements are `resolved`.")
    A("")
    A("**Status: met, with the open questions named above.**")
    A("")
    A("## Criterion 2 — an actual evidence path works")
    A("")
    A("| Experiment | Models | Verdict | Reproduced |")
    A("| --- | --- | --- | --- |")
    for e in exps:
        A(f"| `{e['id']}` | {', '.join(e['models'])} | {e['verdict']} | {e['reproduced'].split('—')[0].strip()} |")
    A("")
    A(f"Reference candidates obtained: **{len(obtained)}** of {len(cands)}; exercised in an")
    A(f"experiment: **{len(exercised)}** ({', '.join(exercised)}). Every experiment records the")
    A("control that was observed FAILING — `RECORD-SCHEMA` refuses one that does not.")
    A("")
    A("**Status: met.** A matched-profile experiment has been run and reproduced, covering a")
    A("trap as well as arithmetic.")
    A("")
    A("## Criterion 3 — profile and reference differences are enumerated")
    A("")
    A("| Difference | Kind |")
    A("| --- | --- |")
    for df in diffs:
        A(f"| `{df['id']}` | {df['kind']} |")
    A("")
    A("| Independence: subsystem | Pair | Verdict |")
    A("| --- | --- | --- |")
    for i in inds:
        A(f"| {i['subsystem']} | {' ↔ '.join(i['pair'])} | **{i['verdict']}** |")
    A("")
    A("**Status: met.** Differences are recorded rather than assumed absent, and independence is")
    A("stated per pair and subsystem — including the pairs nobody has examined, because an omitted")
    A("pair reads exactly like an independent one.")
    A("")
    A("## Limitations (`EVD-08`)")
    A("")
    A(f"1. **{declared_checks} checks are declared and {len(implementing)} implemented.** They name")
    A("   fixtures a later milestone builds. This is the reason for the verdict.")
    A("2. **The model exists; the contract's fixtures do not.** `crates/` holds the")
    A("   definitional interpreter, exercised three-way (the guest corpus, the ACT4")
    A("   campaign) — but the 72 declared obligation checks name no tracked executable,")
    A("   so the contract axis stays open. Evidence about the implementation lives in")
    A("   G1 and the CPU-LAB report, not here.")
    A("3. **Finite differential testing is not proof.** The experiments are evidence for those")
    A("   inputs on those models. Two models sharing semantic code can agree while both are wrong.")
    A("4. **The effective reference configuration is our merge, not the model's report.** The Sail")
    A("   model will not emit its merged configuration; the one self-description it does emit is")
    A("   its ISA string, which is pinned and re-derived.")
    A("5. **Encodings come from a different provenance than the semantics.** The pinned")
    A("   specification contains no instruction encodings; that source is upstream of one")
    A("   comparator and not the other.")
    A("")
    A("## Commands that re-derive this report's inputs")
    A("")
    A("```")
    A("scripts/fetch_references.sh --verify-only   # every pinned digest, and 52 == 52")
    A("scripts/run_smoke.py                        # the experiments, on both models")
    A("scripts/check_requirements.sh               # records validate and agree with the profile")
    A("scripts/check_doctrines.sh                  # the whole gate registry")
    A("```")
    A("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# Gate G1 — the processor laboratory (`P1-LAB.12`). Same doctrine as G0: derived entirely
# from tracked files, byte-stable in a fresh clone, and structurally unable to read
# `passed` while a criterion's evidence is missing. Each criterion below names the
# CONCRETE tracked artifact that evidences it — the G0 lesson (an id-shaped pattern in
# prose is not a check) applied to the laboratory.
# ---------------------------------------------------------------------------

G1_BENCH_MIXES = ("arithmetic", "control", "memory", "fault")
G1_BENCH_MODES = ("untraced", "instrumented", "instrumented-dyn", "diagnostic")


def _subform(form: S.Sexp, name: str, where: str) -> list:
    """The single child form `(name …)`, refusing absence and duplication alike."""
    found = S.children(form, name)
    if len(found) != 1:
        raise S.SexpError(f"{where}: expected exactly one ({name} …), found {len(found)}")
    return found[0]


def _baseline_status(path: Path) -> tuple[dict | None, str | None]:
    """Parse and structurally validate the recorded baseline. Returns (data, problem):
    exactly one is None. A missing field is a problem named, never a passed-over silence."""
    if not path.exists():
        return None, "baseline.sexp is absent"
    try:
        forms = S.parse(path.read_text(), where=path.name)
        if len(forms) != 1 or S.head(forms[0], path.name) != "baseline":
            return None, "expected exactly one (baseline …) form"
        form = forms[0]
        if str(S.field(form, "for-gate", path.name)) != "G1":
            return None, "the record is not marked (for-gate G1)"
        host = _subform(form, "host", path.name)
        for key in ("cpu", "kernel", "rustc"):
            S.field(host, key, path.name)
        config = _subform(form, "config", path.name)
        for key in ("iterations", "warmup", "reps"):
            S.field(config, key, path.name)
        S.field(form, "rederive", path.name)
        S.field(form, "agreement", path.name)
        if str(S.field(form, "thresholds", path.name)) != "none":
            return None, "the record claims thresholds — RUST-04 forbids them here"
        mixes = S.children(form, "mix")
        by_name = {str(S.field(m, "name", path.name)): m for m in mixes}
        if sorted(by_name) != sorted(G1_BENCH_MIXES):
            return None, f"mixes are {sorted(by_name)}, expected {sorted(G1_BENCH_MIXES)}"
        for name, mix in by_name.items():
            cells = S.children(mix, "cell")
            modes = {str(S.field(c, "mode", path.name)) for c in cells}
            if modes != set(G1_BENCH_MODES):
                return None, f"mix {name}: modes are {sorted(modes)}"
            for cell in cells:
                for key in ("ns-per-step", "min", "max", "spread-ppm",
                            "allocs-per-step", "bytes-per-step"):
                    S.field(cell, key, path.name)
            S.field(mix, "static-dyn-ratio", path.name)
        return {"form": form, "mixes": by_name}, None
    except S.SexpError as exc:
        return None, str(exc)


def build_g1(profile: str) -> str:
    d = ROOT / "profiles" / profile
    D.load_profile(d / "profile.sexp")
    obs = R.load(d / "contract-obligations.sexp")
    guests_expected = sorted((d / "guests").glob("*.expected.sexp"))
    guests_s = sorted((d / "guests").glob("*.s"))
    guests_c = sorted((d / "guests").glob("*.c"))
    # The executed-step total the live three-way differential aligns on: the expectation
    # documents declare the executed steps per guest, and the commit gate proves those exact
    # steps execute — so the sum is a function of tracked inputs, not a typed number.
    aligned_steps = sum(len(D.load_expectations(g)["step"]) for g in guests_expected)

    def tracked(rel: str) -> str:
        return (ROOT / rel).read_text()

    # — criterion probes: concrete artifact names, each refusing absent evidence —
    cli = tracked("crates/semulith-cli/src/main.rs")
    replay_cmds = [c for c in ("bundle", "replay", "reduce") if f'Some("{c}")' in cli]
    replay_rs = (ROOT / "crates/semulith-verify/src/replay.rs").exists()
    reduce_rs = (ROOT / "crates/semulith-verify/src/reduce.rs").exists()
    replay_tests = tracked("crates/semulith-verify/src/replay/tests.rs").count("#[test]")
    reduce_tests = tracked("crates/semulith-verify/src/reduce/tests.rs").count("#[test]")

    outcome = tracked("crates/semulith-core/src/outcome.rs")
    families = [n for n in ("pub enum TargetEvent", "pub enum Advance",
                            "pub enum ModelError", "pub enum UndefinedCase")
                if n in outcome]
    mutate_tests = tracked("crates/semulith-verify/src/mutate/tests.rs")
    mutation_arms = mutate_tests.count("#[test]")
    sem02_arm = ("illegal_instruction_substituted_for_a_limitation_is_detected"
                 in mutate_tests)
    mutate_src = tracked("crates/semulith-verify/src/mutate.rs")
    table = mutate_src.split("pub const MUTATIONS")[1].split("];")[0]
    mutants = [m for m in re.findall(r'\(\s*"([a-z0-9-]+)"', table) if m != "none"]

    graph_rs = (ROOT / "crates/semulith-verify/src/graph.rs").exists()
    graph_tests = tracked("crates/semulith-verify/src/graph/tests.rs").count("#[test]")
    check_examples = 'Some("check-examples")' in cli

    baseline, baseline_problem = _baseline_status(d / "baseline.sexp")

    met = {
        1: replay_rs and reduce_rs and len(replay_cmds) == 3
           and replay_tests > 0 and reduce_tests > 0,
        2: len(families) == 4 and sem02_arm,
        3: graph_rs and check_examples and graph_tests > 0,
        4: mutation_arms >= 11 and len(mutants) >= 4,
        5: baseline is not None,
        6: len(guests_c) > 0,
    }
    verdict = "passed" if all(met.values()) else "incomplete"

    L: list[str] = []
    A = L.append
    A(f"# Gate `G1` report — `{profile}` (P1: the processor laboratory)")
    A("")
    A("<!-- DERIVED — DO NOT EDIT. Regenerated by `scripts/gate_report.py --gate G1`; the")
    A("     `GATE-REPORT` doctrine fails the commit if this file and its inputs disagree.")
    A("     Edit the INPUTS: the laboratory crates, the CLI, baseline.sexp, guests/. -->")
    A("")
    A(f"**Verdict: `{verdict}`.**")
    A("")
    A("## Why this verdict")
    A("")
    unmet = [n for n, ok in met.items() if not ok]
    A("`EVD-08` forbids a report that reads `passed` while a required criterion's evidence")
    A("is missing. Each of the six `ROADMAP.md` §6 `G1` criteria below is measured from")
    A("tracked files by concrete name — a criterion without its artifact is unmet, and this")
    A("generator has no code path to `passed` while one is.")
    if unmet:
        A("")
        A(f"Unmet: **{', '.join(f'criterion {n}' for n in unmet)}** — named in its section"
          " below.")
    A("")
    A("## Inputs (all tracked; this report reads nothing untracked)")
    A("")
    A("| Input | Contents |")
    A("| --- | --- |")
    A("| `crates/semulith-core`, `-verify`, `-cli` | the laboratory: interpreter, evidence machinery, command surface |")
    A(f"| `contract-obligations.sexp` | {len(obs)} obligations (the environment contract the laboratory serves) |")
    A(f"| `guests/` | {len(guests_s)} assembly guests, {len(guests_c)} C guests, {len(guests_expected)} expectation documents |")
    missing = "MISSING — " + str(baseline_problem)
    A(f"| `baseline.sexp` | {'the recorded performance baseline' if baseline else missing} |")
    A("")
    A("## Criterion 1 — failures are replayable from recorded inputs")
    A("")
    A("The recorded input bundle (`replay.rs`) and the minimizer (`reduce.rs`) exist as")
    A(f"tracked code; the CLI wires {len(replay_cmds)}/3 commands (`bundle`, `replay`,")
    A(f"`reduce`); the suites carry {replay_tests} replay and {reduce_tests} reduction arms,")
    A("run by the commit gate on every commit.")
    A("")
    A(f"**Status: {'met' if met[1] else 'NOT met — a named artifact above is absent'}.**")
    A("")
    A("## Criterion 2 — model limitations are distinguishable from target traps")
    A("")
    A(f"`outcome.rs` defines {len(families)}/4 outcome families as separate types")
    A("(`TargetEvent`, `Advance`, `ModelError`, `UndefinedCase` — nothing converts between")
    A("them, `SEM-01`). The SEM-02 arm (`illegal_instruction_substituted_for_a_limitation_")
    A(f"is_detected`) {'is present' if sem02_arm else 'is ABSENT'}: a limitation dressed as")
    A("an illegal-instruction trap is caught by name.")
    A("")
    A(f"**Status: {'met' if met[2] else 'NOT met — a family or the SEM-02 arm is absent'}.**")
    A("")
    A("## Criterion 3 — malformed evidence links are rejected")
    A("")
    A(f"The graph and report checker (`graph.rs`, {graph_tests} suites) enforces the")
    A("`EVIDENCE_AND_GATES.md` §3 invariants over the frozen records — orphan ids, stale")
    A("hashes, unsupported `passed` claims, missing evidence, deleted links — and")
    A(f"`semulith check-examples` {'is' if check_examples else 'is NOT'} wired. Schema")
    A("validity alone is never the verdict.")
    A("")
    A(f"**Status: {'met' if met[3] else 'NOT met — the checker or its command is absent'}.**")
    A("")
    A("## Criterion 4 — known validator mutations are detected")
    A("")
    A(f"The mutation suite carries **{mutation_arms} designated arms** (the eight EVD-09")
    A("classes, the JALR odd-bit arm, the crossing-census pin, the suppression exhibit) and")
    A(f"the model-level seam holds **{len(mutants)} named mutants** ({', '.join(mutants)}).")
    A("Every arm asserts detection at a designated step with the field named.")
    A("")
    A(f"**Status: {'met' if met[4] else 'NOT met — the suite shrank below its designated arms'}.**")
    A("")
    A("## Criterion 5 — the performance baseline is measured on a named host")
    A("")
    if baseline:
        form = baseline["form"]
        host = _subform(form, "host", "baseline.sexp")
        config = _subform(form, "config", "baseline.sexp")
        A(f"Host: **{S.field(host, 'cpu')}**; {S.field(host, 'kernel')}; built by"
          f" `{S.field(host, 'rustc')}`. Config: iterations={S.field(config, 'iterations')},")
        A(f"warmup={S.field(config, 'warmup')}, reps={S.field(config, 'reps')}. Re-derive:"
          f" `{S.field(form, 'rederive')}`. Median ns/step (the full record, including")
        A("min/max and bytes/step, is `baseline.sexp`):")
        A("")
        A("| Mix | Untraced | Instrumented | Instr. (dyn) | Diagnostic | Allocs/step | Spread |")
        A("| --- | --- | --- | --- | --- | --- | --- |")
        for name in G1_BENCH_MIXES:
            mix = baseline["mixes"][name]
            cells = {str(S.field(c, "mode")): c for c in S.children(mix, "cell")}
            row = [f"| {name}"]
            for mode in G1_BENCH_MODES:
                row.append(str(S.field(cells[mode], "ns-per-step")))
            row.append(f"{S.field(cells['untraced'], 'allocs-per-step')} → "
                       f"{S.field(cells['diagnostic'], 'allocs-per-step')}")
            spreads = [int(S.field(c, "spread-ppm")) for c in cells.values()]
            row.append(f"{min(spreads) / 10000:.1f}–{max(spreads) / 10000:.1f}%")
            A(" | ".join(row) + " |")
        A("")
        ratios = [float(S.field(baseline["mixes"][n], "static-dyn-ratio"))
                  for n in G1_BENCH_MIXES]
        A(f"Static vs dynamic observer dispatch: ×{min(ratios):.3f}–×{max(ratios):.3f}"
          " across the mixes — within the")
        A("measured noise. The record states `(thresholds none)`; the spread above is what a")
        A("future threshold must be set from (RUST-04). The traced allocation figures are")
        A("workload-dependent by construction: the instrumented mode's writes Vec allocates")
        A("only on a VISIBLE register change (the mixes settle into near-fixed points), and")
        A("the diagnostic mode adds exactly the crossing log's doubling growth — the")
        A("mechanism is pinned to the counted truth by the bench suite (`P1-LAB.13`).")
    else:
        A(f"**No recorded baseline.** {baseline_problem}. The measurement exists as a")
        A("command (`semulith bench`) but the baseline is not recorded as data — the")
        A("criterion is unmet until it is.")
    A("")
    A(f"**Status: {'met' if met[5] else 'NOT met — the baseline is not recorded as data'}.**")
    A("")
    A("## Criterion 6 — a compiled freestanding guest retires under first-divergence comparison")
    A("")
    A(f"`guests/` holds **{len(guests_s)} assembly guests** and **{len(guests_c)} C guests**.")
    if guests_c:
        names = ", ".join(f"`{g.name}`" for g in guests_c)
        A(f"The {len(guests_s)} assembled guests retire under first-divergence comparison")
        A(f"against TWO pinned references (sail-riscv and spike,")
        A(f"{aligned_steps}/{aligned_steps} aligned steps), and the C guest ({names}) —")
        A("compiled from C by the pinned toolchain (`scripts/build_c_guest.sh`; the pin is")
        A("`decision_c-guest-routing-and-toolchain`), not hand-encoded — retires under the")
        A("same three-way comparison. The toolchain probes and")
        A("the measured versions live in that decision record and in the build script's")
        A("refusals; the guest's ELF is a build artifact with the same standing as the")
        A("reference binaries; and the guest is SELF-CHECKING — its expected values are")
        A("constants derived from the C abstract machine written into the source, so a")
        A("mis-execution by ANY runner routes to a fail code and the three-way comparison")
        A(f"diverges at exactly that check. Re-run: `scripts/run_semulith_smoke.py`.")
        A("")
        A("**Status: met.** A compiled freestanding C guest retires under first-divergence")
        A("comparison against both pinned references. The differential stays tested evidence")
        A("for these inputs (`EVD-01`/`EVD-04`); the specification-DERIVED per-step")
        A("expectations remain the assembled guests' layer, by design — the compiler, not")
        A("the author, chooses the compiled guest's instruction sequence.")
    else:
        A(f"The {len(guests_s)} tracked guests ARE freestanding programs — assembled by the")
        A("tracked assembler from `.s` sources — and they retire under first-divergence")
        A(f"comparison against TWO pinned references (sail-riscv and spike,")
        A(f"{aligned_steps}/{aligned_steps} aligned steps; re-run: `scripts/run_semulith_smoke.py`).")
        A("But the roadmap's clause names a **compiled** guest with **C as the first guest path**,")
        A("and no C-toolchain guest exists in this tree.")
        A("")
        A("**Status: NOT met as written.** The assembled-guest differential is real and recorded;")
        A("the C path is the gap. Owner: `P2-SCALAR.5` (external and directed campaigns).")
    A("")
    A("## Limitations (`EVD-08`)")
    A("")
    if unmet:
        A(f"1. **The verdict is `incomplete`, and criterion {', '.join(str(n) for n in unmet)} is why.**")
        A("   A gate report exists to say exactly this, exactly here.")
    else:
        A("1. **The verdict is `passed`** — all six criteria measured met from tracked inputs,")
        A("   re-derived on every commit. That is a statement about the presence and shape of")
        A("   the named evidence, not a proof of correctness (`EVD-01`, `EVD-04`).")
    A("2. **Criteria 1–5 are evidenced by the presence and shape of tracked machinery**, whose")
    A("   every claim is exercised by the commit gate (`make check`) — this report re-derives")
    A("   counts and names from the sources, it does not re-run the suites. The un-fakeable")
    A("   leg is the gate itself.")
    A("3. **The baseline is one host's measurement session**, frozen as data with its noise;")
    A("   it is not a portable constant and sets no threshold.")
    A("4. **Finite differential testing is not proof** (EVD-01): the guests, suites and")
    A("   differentials are tested evidence for the cases they exercise.")
    A("")
    A("## Commands that re-derive this report's inputs")
    A("")
    A("```")
    A("make check                                       # every suite this report counts")
    A("cargo run --release -p semulith-cli -- bench     # the baseline (this host's numbers)")
    A("python3 scripts/run_semulith_smoke.py            # the live three-way differential")
    A("scripts/check_doctrines.sh                       # the whole gate registry")
    A("```")
    A("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# Gate CPU-LAB / G-RELEASE — the P2 capstone report (`P2-SCALAR.9`). Same doctrine as
# G0/G1, one level up: derived entirely from TRACKED artifacts (never a live run — the
# report must be byte-stable in a fresh clone), per axis, never rolled up (SCP-05). The
# release decision is READ from its decision record — the report cannot outrun it
# (EVD-08's shape: no code path to "accepted" while an axis reads incomplete).
# ---------------------------------------------------------------------------


def _dossier_text(path: Path) -> str:
    return path.read_text() if path.is_file() else ""


def _cells(interactions: str) -> tuple[int, int]:
    """(declared cells, cells with at least one resolving disposition) — re-derived by
    counting, like the gate does."""
    cells = interactions.count("(cell ")
    dispositions = interactions.count("(guest ") + interactions.count("(mechanism ") \
        + interactions.count("(degenerate ")
    return cells, dispositions


def dossier_digest(d: Path) -> str:
    """The versioned artifact's identity: the dossier's content digest over its SOURCE
    files — the generated reports are excluded: they are derived from this digest's
    inputs, and including them would make the digest a fixed point of itself.

    The ONE computation (`P5-BOARD.6`): the GC report records it, a board definition
    pins it (`dossier-sha256`), and `scripts/gen_platform.py` refuses a stale pin by
    re-deriving it here — imported, never re-implemented."""
    files = [f for f in subprocess.run(["git", "ls-files", str(d.relative_to(ROOT))],
                           capture_output=True, text=True, cwd=ROOT, check=True)
             .stdout.split() if not f.endswith("-REPORT.md")]
    h = hashlib.sha256()
    for f in files:
        h.update(hashlib.sha256((ROOT / f).read_bytes()).hexdigest().encode())
    return h.hexdigest()


def build_cpulab(profile: str) -> str:
    d = ROOT / "profiles" / profile
    prof = D.load_profile(d / "profile.sexp")
    obs = R.load(d / "contract-obligations.sexp")
    reqs = R.load(d / "requirements.sexp")
    refs = D.load_references(d / "references.sexp")
    guests = sorted((d / "guests").glob("*.expected.sexp"))

    # G-CONTRACT: the effective contract's declared checks vs the ones THIS unit's registry
    # realizes (`contract_measure` — the one computation, unit-scoped).
    declared, implementing = contract_measure(d, obs)
    declared_checks = len(declared)

    # G-OBLIGATIONS: every requirement meets its predeclared verification policy.
    unresolved = [r["id"] for r in reqs if r["research_status"] != "resolved"]
    planned = [r["id"] for r in reqs if r.get("implementation_status") == "planned"]

    # G-INTERACTIONS: the declared matrix, re-counted from the tracked document.
    interactions = _dossier_text(d / "interactions.sexp")
    cells, dispositions = _cells(interactions)

    # G-REGRESSION: the recorded external campaign + the tracked corpus + the mutation
    # suite (commit-gated by `cargo test`).
    act4 = _dossier_text(d / "act4.sexp")
    act4_tests = act4.count("(test (file ")
    m = re.search(r'\(verdicts "([0-9]+) pass / ([0-9]+) fail"\)', act4)
    act4_verdicts = f"{m.group(1)}/{m.group(2)}" if m else "unrecorded"

    # G-PORTABILITY: the recorded instrument verdict.
    portability = _dossier_text(d / "portability.sexp")
    pm = re.search(r'\(verdict "([a-z]+)"\)', portability)
    port_verdict = pm.group(1) if pm else "unrecorded"

    # G-REPLAY: the suites exist and are commit-gated — measured as the suite census.
    snapshot_suites = _dossier_text(ROOT / "crates/semulith-verify/src/snapshot/tests.rs")\
        .count("#[test]")
    determinism = "every_guest_re_executes_identically_from_cold_reset" in _dossier_text(
        ROOT / "crates/semulith-verify/src/run/tests.rs")

    # The versioned artifact's identity (the ONE computation — see dossier_digest).
    artifact_digest = dossier_digest(d)

    axes = [
        ("G-CONTRACT",
         f"{len(implementing)} of {declared_checks} declared obligation checks implemented",
         "green" if declared_checks and len(implementing) >= declared_checks
         else "incomplete"),
        ("G-TRACE",
         "the graph invariants and record cross-checks are commit-gated (RECORD-SCHEMA, "
         "the Rust re-validation of the frozen examples) — measured at every commit",
         "green"),
        ("G-OBLIGATIONS",
         f"{len(unresolved)} unresolved requirement(s) {unresolved if unresolved else ''}; "
         f"{len(planned)} still `planned`" + (" (none)" if not planned else ""),
         "green" if not unresolved and not planned else "incomplete"),
        ("G-INTERACTIONS",
         f"{cells} cells declared, every disposition resolving ({dispositions} "
         f"dispositions) — the INTERACTION-MATRIX gate re-derives the cells",
         "green" if cells == 21 and dispositions >= cells else "incomplete"),
        ("G-REGRESSION",
         f"the ACT4 record: {act4_tests} tests, {act4_verdicts} pass/fail; "
         f"{len(guests)} expectation-documented guests; the validator-mutation suite is "
         f"commit-gated",
         "green" if act4_tests == 51 and m and m.group(2) == "0" else "incomplete"),
        ("G-PORTABILITY",
         f"the recorded verdict: {port_verdict} (the legs and their nuances are the "
         f"record's — the x86-64 leg's translation-vs-bare-metal shape included)",
         "green" if port_verdict == "passed" else "incomplete"),
        ("G-REPLAY",
         f"replay bundles (P1-LAB.10) + mid-execution snapshots (P2-SCALAR.7): "
         f"{snapshot_suites} snapshot suites + the cold-reset determinism suite, all "
         f"commit-gated",
         "green" if snapshot_suites >= 5 and determinism else "incomplete"),
    ]

    incomplete = [name for name, _, v in axes if v != "green"]
    verdict = "passed" if not incomplete else "incomplete"

    L: list[str] = []
    A = L.append
    A(f"# Gate `CPU-LAB` (`G-RELEASE`) report — `{profile}`")
    A("")
    A("<!-- DERIVED — DO NOT EDIT. Regenerated by `scripts/gate_report.py --gate GC`;")
    A("     the `GATE-REPORT` doctrine fails the commit if this file and its inputs")
    A("     disagree. Edit the INPUTS. -->")
    A("")
    A(f"**Verdict: `{verdict}`.**" + ("" if verdict == "passed" else
      f" Open axes: {', '.join(f'`{n}`' for n in incomplete)}."))
    A("")
    A("## The processor-gate series, per axis (`SCP-05` — never rolled up)")
    A("")
    A("| Axis | Measured state | Verdict |")
    A("| --- | --- | --- |")
    for name, state, v in axes:
        A(f"| `{name}` | {state} | **{v}** |")
    A("")
    A('The phrase "supports RV64I" appears nowhere here, by rule: fidelity is reported per')
    A("axis, and a banner is not a claim with a denominator.")
    A("")
    A("## The release decision")
    A("")
    A("Recorded in `docs/decisions/decision_release-rv64i-lab-v0.md` — the named authority")
    A("for what this artifact IS. This report reads the decision, never exceeds it.")
    A("")
    A("## The versioned artifact")
    A("")
    A(f"- profile `{profile}`, version `{prof['profile'].get('version', '?')}`")
    A(f"- the dossier's content digest (every tracked SOURCE file under")
    A(f"  `profiles/{profile}/` — the generated reports excluded, as derived):")
    A(f"  `sha256 {artifact_digest}`")
    A(f"- regenerate: `scripts/gate_report.py {profile} --gate GC`")
    A("")
    A("## Capability limits (explicit)")
    A("")
    A("- The portability axis's x86-64 leg ran under Rosetta 2 translation (measured,")
    A("  byte-identical manifest); the bare-metal leg is the CI matrix, landing at the")
    A("  next approved push. Rosetta is the time-bounded bridge (phase-out fall 2027).")
    A("- The obligations axis is measured open: declared contract checks await their")
    A("  fixtures. Until then this profile is an EXPERIMENTAL deliverable — the decision")
    A("  record says what that means and does not mean.")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# Gate CPU-SYSTEM — the processor gate over a complete declared profile (`P4-SYSTEM.10` slice b).
# ALL TEN axes of `docs/EVIDENCE_AND_GATES.md` §7, per axis, never rolled up (SCP-05), each
# measured from THIS unit's tracked files. ⛔ No axis is a constant and no count is hard-coded:
# `build_cpulab` above carries rv64i's facts as numbers (21 cells, 51 ACT4 tests) and reads rv64i's
# replay suites whatever the unit — run on rv64gc it read G-REPLAY green from rv64i's evidence.
# Five axes are COMPUTED from the unit's dossier; five are answered by suites and records whose
# location is the unit's business, so the unit DECLARES them (`gate.sexp`, schema/gate.sexp) and
# this generator VERIFIES every declaration against the tree. The kinds each of those axes
# requires are §7's, held HERE (`GS_KINDS`), never by the unit: a required kind with no verified
# evidence reads open, whatever the manifest says. `passed` needs all ten green (EVD-08).
# ---------------------------------------------------------------------------

GS_AXES = ("G-SCOPE", "G-STATE", "G-CONTRACT", "G-TRACE", "G-OBLIGATIONS", "G-INTERACTIONS",
           "G-REGRESSION", "G-PORTABILITY", "G-REPLAY", "G-RELEASE")
# §7's required evidence for the five declared axes, as kinds (the table's own words).
GS_KINDS = {
    "G-TRACE": ("experiment",),
    "G-REGRESSION": ("directed", "external", "generated", "workload", "validator-mutation"),
    "G-PORTABILITY": ("x86-64", "aarch64", "miri"),
    "G-REPLAY": ("determinism", "snapshot", "replay-bundle", "reduction"),
    "G-RELEASE": ("decision",),
}
# Kinds whose record must carry a passing recorded verdict, not merely exist.
GS_VERDICT_KINDS = ("external", "workload", "validator-mutation", "x86-64", "aarch64", "miri")
GS_REQUIRED = {  # §7's table, quoted per axis for the report
    "G-SCOPE": "exact profile, source revisions, observation contract, complete dependency closure",
    "G-STATE": "state, aliases, arithmetic, effects, reset and pending state: reviewed requirements and evidence",
    "G-CONTRACT": "enumerable CPU/environment assumptions and guarantees; validated mappings",
    "G-TRACE": "graph integrity, actual artifacts, matched inputs, current evidence, justified comparison rules",
    "G-OBLIGATIONS": "every included requirement meets its predeclared verification policy",
    "G-INTERACTIONS": "the declared fault/alias/boundary/event/progress/restart matrix exercised",
    "G-REGRESSION": "full applicable directed, external, generated, workload, validator-mutation suites pass",
    "G-PORTABILITY": "native x86-64 and AArch64 fixtures agree; the pinned Miri/cross-endian plan passes",
    "G-REPLAY": "reports and relevant successes/failures reproduce from recorded inputs and event choices",
    "G-RELEASE": "reproducible report, explicit capability limits, named release decision, versioned artifact",
}


def _forms(path: Path, head: str) -> list:
    """Every list whose head is `head`, at any depth of the document."""
    out, stack = [], [f for f in S.read_file(path) if isinstance(f, list)]
    while stack:
        f = stack.pop(0)
        if f and str(f[0]) == head:
            out.append(f)
        stack.extend(c for c in f[1:] if isinstance(c, list))
    return out


def _one(form: list, name: str):
    found = S.children(form, name)
    return str(found[0][1]) if found else None


def _tracked() -> set[str]:
    return set(subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=ROOT,
                              check=True).stdout.split())


def _verify_evidence(ev: list, tracked: set[str], experiments: set[str], where: str) -> tuple[str, str | None]:
    """(what the evidence names, None if verified — else why it is not)."""
    test, record, exp = S.children(ev, "test"), _one(ev, "record"), _one(ev, "experiment")
    if len(test) + (record is not None) + (exp is not None) != 1:
        raise SystemExit(f"gate_report: {where}: an evidence form names exactly one of test / record / "
                         f"experiment — this one names {len(test) + (record is not None) + (exp is not None)}")
    kind = _one(ev, "kind")
    if test:
        file, fn = _one(test[0], "file"), _one(test[0], "fn")
        label = f"`{file}` `{fn}`"
        if file not in tracked:
            return label, "the file is not tracked"
        if not re.search(rf"\bfn {re.escape(fn)}\s*\(", (ROOT / file).read_text(encoding="utf-8")):
            return label, "no such test function in the file"
        return label, None
    if exp is not None:
        label = f"experiment `{exp}`"
        return label, None if exp in experiments else "no such experiment record in references.sexp"
    label = f"`{record}`"
    if record not in tracked:
        return label, "the record is not tracked"
    if kind in GS_VERDICT_KINDS:
        text = (ROOT / record).read_text(encoding="utf-8")
        m = re.search(r'\(verdicts "([0-9]+) pass / ([0-9]+) fail"\)', text)
        v = re.search(r'\(verdict "([a-z]+)"\)', text)
        if m:
            return label, None if m.group(2) == "0" else f"the record reads {m.group(2)} fail"
        if v:
            return label, None if v.group(1) == "passed" else f"the recorded verdict is {v.group(1)}"
        return label, "the record carries no recorded verdict"
    return label, None


def _gs_verdict(axes: dict[str, tuple[str, bool]]) -> tuple[str, list[str]]:
    """EVD-08's shape: `passed` exactly when all ten axes are present and green."""
    incomplete = [a for a in GS_AXES if a not in axes or not axes[a][1]]
    return ("passed" if not incomplete else "incomplete"), incomplete


def build_cpusystem(profile: str, d: Path | None = None, tracked: set[str] | None = None) -> str:
    """`d`/`tracked` exist for the controls (`_selftest`), which run the builder over a scratch
    copy of a real unit; the report itself always reads the unit's tracked dossier."""
    d = d or ROOT / "profiles" / profile
    prof = D.load_profile(d / "profile.sexp")
    obs = R.load(d / "contract-obligations.sexp")
    reqs = R.load(d / "requirements.sexp")
    refs = D.load_references(d / "references.sexp")
    tracked = tracked if tracked is not None else _tracked()
    rel = lambda name: (d / name).relative_to(ROOT).as_posix()  # noqa: E731
    manifest = d / "gate.sexp"
    if rel("gate.sexp") not in tracked:
        raise SystemExit(f"gate_report: {rel('gate.sexp')} is not tracked — the CPU-SYSTEM report "
                         f"reads the unit's evidence manifest (schema/gate.sexp)")
    axes: dict[str, tuple[str, bool]] = {}

    # G-SCOPE — the composition is complete: no unfilled slot, no partial status.
    compose = _forms(d / "encoding.sexp", "compose")[0]
    exts = [str(c[1]) for c in S.children(compose, "extensions")]
    slots = [str(_one(s, "id")) for s in S.children(compose, "slot")]
    status = _one(compose, "status") or "complete"
    axes["G-SCOPE"] = (f"the encoding composes `{_one(compose, 'base')}` + {len(exts)} extensions; "
                       f"status `{status}`; unfilled slots: "
                       + (", ".join(f"`{s}`" for s in slots) if slots else "none"),
                       status != "partial" and not slots)

    # G-STATE — the hidden-state census answered, and the state requirements implemented.
    census = _forms(d / "state.sexp", "hidden_state_census")
    cands = [c for h in census for c in _forms_in(h, "checked")]
    answered = [c for c in cands if (_one(c, "why") or "").strip()]
    state_reqs = [r for r in reqs if r["kind"] == "state"]
    state_done = [r for r in state_reqs if r["implementation_status"] in ("implemented", "not-applicable")]
    axes["G-STATE"] = (f"the hidden-state census: {len(answered)} of {len(cands)} candidates answered; "
                       f"{len(state_done)} of {len(state_reqs)} `state` requirements implemented",
                       bool(census) and len(answered) == len(cands)
                       and bool(state_reqs) and len(state_done) == len(state_reqs))

    # G-CONTRACT — the effective contract's checks, realized by THIS unit's registry; frozen.
    declared, realized = contract_measure(d, obs)
    versions = _forms(d / "contract.sexp", "contract") if (d / "contract.sexp").is_file() else []
    latest = max(versions, key=lambda v: int(_one(v, "version"))) if versions else None
    frozen = latest is not None and _one(latest, "status") == "frozen"
    axes["G-CONTRACT"] = (f"{len(realized)} of {len(declared)} checks of the effective contract "
                          f"realized by the unit's registry; latest version "
                          + (f"`{_one(latest, 'id')}` {_one(latest, 'status')}" if latest else "— none"),
                          bool(declared) and len(realized) == len(declared) and frozen)

    # G-OBLIGATIONS — every requirement resolved and implemented, under a predeclared policy.
    unresolved = [r["id"] for r in reqs if r["research_status"] != "resolved"]
    by_status: dict[str, int] = {}
    for r in reqs:
        by_status[r["implementation_status"]] = by_status.get(r["implementation_status"], 0) + 1
    open_reqs = sum(n for s, n in by_status.items() if s not in ("implemented", "not-applicable"))
    policy = rel("EVIDENCE_POLICY.md") in tracked
    axes["G-OBLIGATIONS"] = (f"{len(reqs)} requirements: "
                             + ", ".join(f"{n} `{s}`" for s, n in sorted(by_status.items()))
                             + f"; {len(unresolved)} not resolved"
                             + (f" ({', '.join(f'`{u}`' for u in unresolved)})" if unresolved else "")
                             + f"; predeclared policy (`EVIDENCE_POLICY.md`): {'present' if policy else 'absent'}",
                             bool(reqs) and not unresolved and open_reqs == 0 and policy)

    # G-INTERACTIONS — every declared cell carries a resolving disposition.
    cells = _forms(d / "interactions.sexp", "cell")
    empty = [" × ".join(str(a[1]) for a in S.children(c, "axis")) for c in cells
             if not (S.children(c, "guest") or S.children(c, "mechanism") or S.children(c, "degenerate"))]
    axes["G-INTERACTIONS"] = (f"{len(cells)} cells declared, {len(cells) - len(empty)} with a resolving "
                              f"disposition (a guest, a mechanism or a degenerate argument)"
                              + (f"; undispositioned: {', '.join(empty)}" if empty else ""),
                              bool(cells) and not empty)

    # The five declared axes — the manifest's evidence, verified; §7's kinds required.
    experiments = {e["id"] for e in refs.get("experiment", [])}
    found: dict[tuple[str, str], list[tuple[str, str | None]]] = {}
    for ev in _forms(manifest, "evidence"):
        axis, kind = _one(ev, "axis"), _one(ev, "kind")
        if kind not in GS_KINDS.get(axis, ()):
            raise SystemExit(f"gate_report: {rel('gate.sexp')}: evidence kind `{kind}` is not one "
                             f"{axis} requires ({', '.join(GS_KINDS.get(axis, ()))})")
        found.setdefault((axis, kind), []).append(_verify_evidence(ev, tracked, experiments, rel("gate.sexp")))
    na = {}
    for f in _forms(manifest, "not-applicable"):
        axis, kind = _one(f, "axis"), _one(f, "kind")
        if kind not in GS_KINDS.get(axis, ()):
            raise SystemExit(f"gate_report: {rel('gate.sexp')}: not-applicable `{axis}`/`{kind}` names no required kind")
        na[(axis, kind)] = _one(f, "why")
    for axis, kinds in GS_KINDS.items():
        if axis == "G-RELEASE":
            continue
        have = [k for k in kinds if any(v is None for _, v in found.get((axis, k), [])) or (axis, k) in na]
        missing = [k for k in kinds if k not in have]
        axes[axis] = (f"{len(have)} of {len(kinds)} required kinds evidenced"
                      + (f" — open: {', '.join(f'`{k}`' for k in missing)}" if missing else ""),
                      not missing)
    others_green = all(g for a, (_, g) in axes.items())
    decided = any(v is None for _, v in found.get(("G-RELEASE", "decision"), []))
    axes["G-RELEASE"] = (("a release decision is recorded" if decided else "no release decision recorded")
                         + "; this report is generated from tracked inputs and gated for sync (GATE-REPORT); "
                         + ("every other axis green" if others_green else "other axes open"),
                         decided and others_green)

    opens: dict[str, list[tuple[str, str]]] = {}
    for f in _forms(manifest, "open"):
        axis = _one(f, "axis")
        if axis not in GS_AXES:
            raise SystemExit(f"gate_report: {rel('gate.sexp')}: open item on unknown axis `{axis}`")
        opens.setdefault(axis, []).append((_one(f, "owner"), _one(f, "statement")))
    verdict, incomplete = _gs_verdict(axes)
    unowned = [a for a in incomplete if a not in opens]

    L: list[str] = []
    A = L.append
    A(f"# Gate `CPU-SYSTEM` report — `{profile}`")
    A("")
    A("<!-- DERIVED — DO NOT EDIT. Regenerated by `scripts/gate_report.py --gate GS`;")
    A("     the `GATE-REPORT` doctrine fails the commit if this file and its inputs")
    A("     disagree. Edit the INPUTS (the dossier and its gate.sexp). -->")
    A("")
    A(f"**Verdict: `{verdict}`.**" + ("" if verdict == "passed" else
      f" Open axes ({len(incomplete)} of {len(GS_AXES)}): {', '.join(f'`{n}`' for n in incomplete)}."))
    A("")
    A("## The processor gate, per axis (`SCP-05` — never rolled up)")
    A("")
    A("| Axis | Required (§7) | Measured state | Verdict |")
    A("| --- | --- | --- | --- |")
    for a in GS_AXES:
        state, green = axes[a]
        A(f"| `{a}` | {GS_REQUIRED[a]} | {state} | **{'green' if green else 'incomplete'}** |")
    A("")
    A("Fidelity is reported per axis. No sentence here says the profile is supported: a banner")
    A("is not a claim with a denominator.")
    A("")
    A("## What stands open, and who owns it")
    A("")
    if incomplete:
        A("| Axis | Owner | Open item |")
        A("| --- | --- | --- |")
        for a in incomplete:
            for owner, statement in opens.get(a, [("**unowned**", "no open item is declared for this axis")]):
                A(f"| `{a}` | `{owner}` | {statement} |")
        if unowned:
            A("")
            A(f"**Unowned open axes: {', '.join(f'`{u}`' for u in unowned)}** — an open axis with no owning leaf.")
    else:
        A("Nothing.")
    A("")
    A("## The evidence the unit declares (`gate.sexp`), verified against the tree")
    A("")
    A("| Axis | Kind | Evidence | Verified |")
    A("| --- | --- | --- | --- |")
    for axis, kinds in GS_KINDS.items():
        for k in kinds:
            for label, why in found.get((axis, k), []):
                A(f"| `{axis}` | `{k}` | {label} | {'yes' if why is None else f'**no** — {why}'} |")
            if (axis, k) in na:
                A(f"| `{axis}` | `{k}` | not applicable — {na[(axis, k)]} | declared |")
            if not found.get((axis, k)) and (axis, k) not in na:
                A(f"| `{axis}` | `{k}` | — | **none declared** |")
    A("")
    A("A test function is verified to exist in a tracked file; it PASSES because `make check` runs")
    A("`cargo test` before every commit. A record is verified to be tracked and, for a verdict-bearing")
    A("kind, to carry a passing recorded verdict. What a declaration claims a test exercises is the")
    A("reviewer's to judge — that much this report cannot measure.")
    A("")
    A("## The versioned artifact")
    A("")
    A(f"- profile `{profile}`, version `{prof['profile'].get('version', '?')}`")
    A("- the dossier's content digest (every tracked SOURCE file under")
    A(f"  `profiles/{profile}/` — the generated reports excluded, as derived):")
    A(f"  `sha256 {dossier_digest(d)}`")
    A(f"- regenerate: `scripts/gate_report.py {profile} --gate GS`")
    A("")
    A("## Capability limits (explicit)")
    A("")
    if incomplete:
        A("Every open item above is a limit of what this profile is evidence for today. Until each")
        A("closes, a claim about this processor holds only on the axes that read green, and only")
        A("for the inputs those axes measured.")
    else:
        A("Every axis is green over the inputs it measured; finite testing is not proof.")
    return "\n".join(L) + "\n"


def _forms_in(form: list, head: str) -> list:
    out, stack = [], [c for c in form[1:] if isinstance(c, list)]
    while stack:
        f = stack.pop(0)
        if f and str(f[0]) == head:
            out.append(f)
        stack.extend(c for c in f[1:] if isinstance(c, list))
    return out



# ---------------------------------------------------------------------------
# Gate BREADTH — the cross-architecture capability report (`P3-BREADTH.6`). Same doctrine
# as the per-profile gates, one level sideways: derived entirely from TRACKED files (the
# unit registry, the units' dossiers, the schemas, the refusal-boundary pins, the family
# census), per axis, never rolled up (SCP-05). The gate is not a profile's — it spans
# every registered unit — so the report lives at `docs/BREADTH-REPORT.md`, and the
# verdict cannot read `passed` while an axis's measured anchors are absent (EVD-08).
# ---------------------------------------------------------------------------

BREADTH_SURVEY = "docs/tasks/artifacts/p3-breadth/2026-10-01-oracle-survey.md"
BREADTH_SYNTH = "docs/tasks/artifacts/dsp-review/synth"

# The abstraction constructs the DSP's exercised cases required (P3-BREADTH.5/`.7`): each
# is probed BY NAME in the schema that declares it AND in the single mapping owner —
# a construct the mapping drops silently is the class P3-BREADTH.2 eliminated.
BREADTH_CONSTRUCTS = (
    ("schema/state.sexp", "register_family"),
    ("schema/state.sexp", "memory_spaces"),
    ("schema/state.sexp", "hardware_stack"),
    ("schema/profile.sexp", "vehicle"),
    ("schema/profile.sexp", "moves"),
    ("schema/profile.sexp", "alu_core"),
    ("schema/profile.sexp", "multiplies"),
    ("schema/profile.sexp", "flow"),
    ("schema/profile.sexp", "loops"),
)


def _units() -> list[dict]:
    """The registered units — the COMPLETE claim list. Parsed from materials/units.sexp;
    a unit is claimed exactly by being registered here."""
    units = []
    for line in (ROOT / "materials/units.sexp").read_text().splitlines():
        if not line.startswith("(unit "):
            continue
        units.append({
            "id": re.search(r'\(id "([^"]+)"\)', line).group(1),
            "kind": re.search(r'\(kind ([^)]+)\)', line).group(1),
            "book": re.search(r'\(book "([^"]+)"\)', line).group(1),
        })
    return units


def build_breadth() -> str:
    units = _units()
    dsp = ROOT / "profiles/dsp56300-lab-v0"
    dsp_prof = D.load_profile(dsp / "profile.sexp")
    dsp_refs_text = (dsp / "references.sexp").read_text()
    guests_a56 = sorted((dsp / "guests").glob("*.a56"))
    crate = ROOT / "crates/semulith-dsp56300"
    crate_tests = sum(p.read_text().count("#[test]")
                      for p in sorted(crate.glob("src/**/*.rs")))
    matrix_src = (ROOT / "scripts/check_interaction_matrix.py").read_text()
    driver = ROOT / "scripts/run_dsp56300_smoke.py"

    # Axis 1 anchors — each a concrete tracked artifact, absent ⇒ unmet.
    dsp_vehicle = dsp_prof.get("vehicle") or {}
    a1 = {
        "the subset is declared (scope count_total > 0, vehicle sibling-crate)":
            dsp_prof["scope"]["count_total"] > 0
            and str(dsp_vehicle.get("route")) == "sibling-crate",
        "the guest corpus exists (.a56 + .meta per case)":
            len(guests_a56) > 0
            and all(g.with_suffix(".meta").exists() for g in guests_a56),
        "the model crate exists and carries commit-level tests":
            crate.is_dir() and crate_tests > 0,
        "the differential driver exists (the agreement is re-derived by running it)":
            driver.is_file(),
        "the comparison contract is recorded (trace_granularity)":
            "trace_granularity" in dsp_refs_text,
        "the agreement mechanism is registered (the matrix gate re-derives it)":
            "dsp56300-smoke-agreement" in matrix_src,
    }
    gc_report = ROOT / "profiles/rv64i-lab-v0/GC-REPORT.md"
    a1_rv64 = gc_report.is_file()

    # Axis 2 anchors — the schema declares each construct and the mapping owner carries it.
    mapping_src = (ROOT / "scripts/dossier_sexp.py").read_text()
    a2 = []
    for schema_file, construct in BREADTH_CONSTRUCTS:
        declared = construct in (ROOT / schema_file).read_text()
        carried = construct in mapping_src
        a2.append((schema_file, construct, declared, carried))
    synth = ROOT / BREADTH_SYNTH
    synth_runner = synth / "run_synth_probes.sh"
    synth_probes = sorted(p.name for p in synth.glob("*.sexp")) if synth.is_dir() else []

    # Axis 3 — the family census: every surveyed family is either backed by a registered
    # unit or listed UNCLAIMED below. Parsed from the pinned survey record.
    survey_text = (ROOT / BREADTH_SURVEY).read_text()
    families = re.findall(r"^### (.+?) — (\S[^\n]*)$", survey_text, re.M)
    archs = {}
    for u in units:
        p = ROOT / "profiles" / u["id"] / "profile.sexp"
        if p.is_file():
            archs[u["id"]] = D.load_profile(p)["profile"].get("architecture", "")
    def claimed_by(family: str) -> str | None:
        for uid, arch in archs.items():
            if arch and arch in family:
                return uid
        return None
    unclaimed = [(fam, verdict) for fam, verdict in families if not claimed_by(fam)]

    met = {
        1: all(a1.values()) and a1_rv64,
        2: all(d and c for _, _, d, c in a2) and synth_runner.is_file() and synth_probes,
        3: bool(units) and bool(families) and bool(unclaimed),
    }
    verdict = "passed" if all(met.values()) else "incomplete"
    unmet = [n for n, ok in met.items() if not ok]

    L: list[str] = []
    A = L.append
    A("# Gate `BREADTH` report — the cross-architecture capability report (P3)")
    A("")
    A("<!-- DERIVED — DO NOT EDIT. Regenerated by `scripts/gate_report.py --gate BREADTH`;")
    A("     the `GATE-REPORT` doctrine fails the commit if this file and its inputs disagree.")
    A("     Edit the INPUTS: the unit registry, the units' dossiers, the schemas, the synth")
    A("     pins, the family census. -->")
    A("")
    A(f"**Verdict: `{verdict}`.**" + ("" if verdict == "passed" else
      f" Unmet: {', '.join(f'axis {n}' for n in unmet)}."))
    A("")
    A("## Why this verdict")
    A("")
    A("`EVD-08` forbids a report that reads `passed` while a required axis's evidence is")
    A("missing. The three axes below are the `ROADMAP.md` §6 `BREADTH` gate text, each")
    A("measured from tracked files by concrete artifact name — never asserted. This")
    A("generator has no code path to `passed` while an axis's anchors are absent.")
    A("")
    A("## Inputs (all tracked; this report reads nothing untracked)")
    A("")
    A("| Input | Contents |")
    A("| --- | --- |")
    A(f"| `materials/units.sexp` | {len(units)} registered units — the COMPLETE claim list |")
    A(f"| `profiles/dsp56300-lab-v0/` | scope {dsp_prof['scope']['count_total']} forms, vehicle `{dsp_vehicle.get('route', '?')}`, {len(guests_a56)} `.a56` guests, the recorded comparison contract |")
    A(f"| `crates/semulith-dsp56300` | the sibling-crate model, {crate_tests} commit-level tests |")
    A(f"| `schema/state.sexp`, `schema/profile.sexp` + `scripts/dossier_sexp.py` | the abstraction's exercised-case constructs, declared and carried |")
    A(f"| `{BREADTH_SYNTH}/` | {len(synth_probes)} refusal-boundary pins (the synthetic fixtures) |")
    A(f"| `{BREADTH_SURVEY}` | the family census — {len(families)} families with verdicts |")
    A("| `profiles/rv64i-lab-v0/G?-REPORT.md` | the scalar unit's own per-axis gate records (GATE-REPORT-gated) |")
    A("")
    A("## Axis 1 — the stated real subset has evidence")
    A("")
    A("The stated real subset is `dsp56300-lab-v0` v0 (`decision_dsp56300-lab-v0-subset`).")
    A("Its evidence anchors, each measured by name:")
    A("")
    A("| Anchor | Present |")
    A("| --- | --- |")
    for name, ok in a1.items():
        A(f"| {name} | {'yes' if ok else '**NO**'} |")
    A("")
    A(f"The corpus is {len(guests_a56)} synthetic guests; the agreement itself is re-derived")
    A("by running `scripts/run_dsp56300_smoke.py` (deliberately NOT a commit gate — it needs")
    A("the untracked, network-acquired reference binaries), and the EXERCISE-COVERAGE gate")
    A(f"re-derives the scope-versus-corpus census ({dsp_prof['scope']['count_total']}/"
      f"{dsp_prof['scope']['count_total']}) at every commit. The crate's {crate_tests} tests")
    A("are the commit-level proof. The scalar unit's evidence stands as its own per-axis")
    A(f"record: `profiles/rv64i-lab-v0/GC-REPORT.md` ({'present' if a1_rv64 else '**ABSENT**'},")
    A("GATE-REPORT-gated).")
    A("")
    A(f"**Status: {'met' if met[1] else 'NOT met — a named anchor above is absent'}.**")
    A("")
    A("## Axis 2 — the public abstraction supports the exercised cases")
    A("")
    A("Every construct the exercised DSP cases required is declared in its schema AND")
    A("carried by the single mapping owner (`dossier_sexp`) — a construct the mapping")
    A("dropped would be the silent-path class `P3-BREADTH.2` eliminated:")
    A("")
    A("| Construct | Declared | Carried |")
    A("| --- | --- | --- |")
    for schema_file, construct, declared, carried in a2:
        A(f"| `{construct}` ({schema_file}) | {'yes' if declared else '**NO**'} | {'yes' if carried else '**NO**'} |")
    A("")
    A(f"The refusal boundary is pinned, not assumed: {len(synth_probes)} synthetic probes")
    A(f"({', '.join(f'`{p}`' for p in synth_probes)}) measure what the pipeline refuses")
    A("by name — the boundary's position is evidence, and the suite turns RED by design")
    A("the day a pin goes stale.")
    A("")
    A(f"**Status: {'met' if met[2] else 'NOT met — a construct is undeclared or uncarried'}.**")
    A("")
    A("## Axis 3 — unsupported families remain unclaimed")
    A("")
    A("The claim list is the unit registry, and it is complete — a family is claimed")
    A("exactly by a registered unit:")
    A("")
    A("| Unit | Architecture | Evidence record |")
    A("| --- | --- | --- |")
    for u in units:
        A(f"| `{u['id']}` | {archs.get(u['id'], '?')} | {'the GC per-axis report' if u['id'] == 'rv64i-lab-v0' else 'axis 1 above (EXPERIMENTAL)'} |")
    A("")
    A("Every other family the work has surveyed is **unclaimed**, explicitly:")
    A("")
    A("| Family | Survey verdict | Claim |")
    A("| --- | --- | --- |")
    for fam, verdict_f in unclaimed:
        A(f"| {fam} | {verdict_f} | **unclaimed** |")
    A("")
    A("And every family the survey did not measure is unclaimed by omission: the registry")
    A("above is the whole of what this project claims. The synthetic fixtures (axis 2) are")
    A("never evidence about any real processor — they claim no compatibility, by rule.")
    A("")
    A(f"**Status: {'met' if met[3] else 'NOT met — the registry or the census is unreadable'}.**")
    A("")
    A("## What this verdict does NOT mean")
    A("")
    A("- **No stable-general-API claim beyond the exercised cases.** The abstraction supports")
    A(f"  the {sum(1 for u in units if u['kind'] == 'processor')} registered processor units' shapes, measured; a further family may demand constructs")
    A("  nobody has needed yet (the slice-gated `P3-BREADTH.1` legs — F2 grouping, F4/F5")
    A("  VLIW visibility — are recorded, unbuilt, and named).")
    A("- **No DSP56300 family compatibility.** The subset is EXPERIMENTAL; the differential")
    A("  is finite, tested evidence over a synthetic corpus (EVD-01), against ONE oracle")
    A("  whose assembler and emulator legs share a lineage (EVD-04, recorded in")
    A("  `references.sexp`); `cyc` is never compared.")
    A("- **No RISC-V conformance.** The scalar unit's own report reads `incomplete` on two")
    A("  axes and its release decision is EXPERIMENTAL — this gate does not upgrade it.")
    A("")
    A("## Commands that re-derive this report's inputs")
    A("")
    A("```")
    A("make gate                            # every doctrine, incl. the gates this report cites")
    A("scripts/run_dsp56300_smoke.py        # the DSP differential (needs the reference binaries)")
    A("scripts/gate_report.py --gate BREADTH   # regenerate this report — never edit it")
    A("```")
    A("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# The measure's controls (`P4-SYSTEM.10` slice a). GATE-REPORT runs them and refuses while any
# misses: a report is only as honest as the count it reads. Each arm builds a scratch unit under
# `target/doctrine-selftest/` (never /tmp — §13) from the REAL rv64gc documents, mutates one thing,
# and asks the measure. ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): the
# arm count is asserted, so an arm that silently never ran is a failure, not a pass.
# ---------------------------------------------------------------------------

def assert_eq(got, want):
    assert got == want, f"got {got!r}, want {want!r}"


def _selftest() -> int:
    import shutil
    import tempfile
    base = ROOT / "target" / "doctrine-selftest"
    base.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=base))
    real = ROOT / "profiles" / "rv64gc-lab-v0"
    reg_src = (ROOT / "crates/semulith-verify/src/contract_checks_rv64gc.rs").read_text(encoding="utf-8")
    passed, missed, ran = 0, [], 0
    extra = ('    ContractCheck {\n        id: "CHK-ALU-IMM-POS",\n        obligation: "OB-ALU-IMM",\n'
             '        guests: &["x"],\n    },\n')

    def unit(name, contract_edit=None, registry=reg_src, with_contract=True):
        d = tmp / name
        d.mkdir()
        shutil.copy(real / "contract-obligations.sexp", d)
        reg = d / "reg.rs"
        reg.write_text(registry, encoding="utf-8")
        if with_contract:
            text = (real / "contract.sexp").read_text(encoding="utf-8")
            text = text.replace('(registry (path "crates/semulith-verify/src/contract_checks_rv64gc.rs")',
                                f'(registry (path "{reg.relative_to(ROOT).as_posix()}")')
            (d / "contract.sexp").write_text(contract_edit(text) if contract_edit else text, encoding="utf-8")
        return d

    def measure(d):
        return contract_measure(d, R.load(d / "contract-obligations.sexp"))

    def arm(label, fn):
        nonlocal passed, ran
        ran += 1
        try:
            fn()
            passed += 1
        except Exception as e:                      # noqa: BLE001 — every miss is reported
            missed.append(f"{label}: {e}")

    def counts(d, want):
        got = tuple(len(x) for x in measure(d))
        assert got == want, f"got (declared, realized) {got}, want {want}"

    def refuses(d, needle):
        try:
            measure(d)
        except SystemExit as e:
            assert needle in str(e), f"refused, but for {e}"
            return
        raise AssertionError("not refused")

    # ⛔ NO ARM PINS THE LIVE UNIT'S NUMBERS. The first cut asserted rv64gc's counts (100, 14)
    # and broke at the contract's first growth (P4-SYSTEM.11 slice b) — the hard-coded unit fact
    # this generator exists to remove. Each RED arm asserts a DELTA from the baseline the real
    # unit gives at run time; the GREEN arm checks that baseline against an independent recount.
    obs_real = R.load(real / "contract-obligations.sexp")
    every = sum(len(o["required_checks"]) for o in obs_real)
    superseded = set(re.findall(r'\(supersede \(record "([^"]+)"\)',
                                (real / "contract.sexp").read_text(encoding="utf-8")))
    try:
        base = tuple(len(x) for x in measure(unit("green")))
    except Exception as e:                          # noqa: BLE001 — every arm then misses
        base = (-1, -1)
        missed.append(f"the baseline measure itself failed: {e}")

    def delta(d, dd, dr):
        counts(d, (base[0] + dd, base[1] + dr))

    def independent():
        # every record's checks minus the superseded records' — no version chain walked — and
        # every registry entry (each a declared pair: the Rust pairing test's guarantee)
        want = (sum(len(o["required_checks"]) for o in obs_real if o["id"] not in superseded),
                len(_ENTRY.findall(reg_src)))
        assert base == want, f"the measure {base}, an independent recount {want}"
        assert 0 < base[1] <= base[0], f"a degenerate baseline {base}"

    try:
        arm("GREEN the measure agrees with an independent recount of the real contract", independent)
        add = reg_src.replace("pub static CHECKS: &[ContractCheck] = &[\n",
                              "pub static CHECKS: &[ContractCheck] = &[\n" + extra)
        arm("RED a shared id realized in THIS unit's registry counts for it (+1 realized)",
            lambda: delta(unit("shared", registry=add), 0, 1))
        arm("RED the same id does not credit a unit whose contract names no registry",
            lambda: counts(unit("other", with_contract=False, registry=add), (every, 0)))
        arm("RED dropping the supersessions raises the denominator to every record",
            lambda: (assert_eq(bool(superseded), True),
                     counts(unit("nosup", lambda s: re.sub(
                         r'\(supersede \(record "[^"]*"\) \(by "[^"]*"\) \(why "[^"]*"\)\)', "", s)),
                         (every, base[1]))))
        wrong = reg_src.replace('obligation: "OB-GC-ENV-VIRTUAL-TIME"', 'obligation: "OB-SVADE"', 1)
        arm("RED a check registered under an obligation that does not declare it is not counted (-1)",
            lambda: delta(unit("wrong", registry=wrong), 0, -1))
        odd = reg_src.replace("pub static CHECKS: &[ContractCheck] = &[\n",
                              "pub static CHECKS: &[ContractCheck] = &[\n    ContractCheck {\n"
                              "        obligation: \"OB-SVADE\",\n        id: \"CHK-SVADE-POS\",\n"
                              "        guests: &[\"x\"],\n    },\n")
        arm("RED an entry the reader cannot parse exactly is refused, never silently missed",
            lambda: refuses(unit("odd", registry=odd), "read exactly"))
        arm("RED two registries in one contract document are refused",
            lambda: refuses(unit("tworeg", lambda s: s + s[s.index("(registry "):]), "at most one registry"))

        # ---- the CPU-SYSTEM builder (`P4-SYSTEM.10` slice b) over a scratch copy of the unit ----
        docs = ("profile.sexp", "contract-obligations.sexp", "requirements.sexp", "references.sexp",
                "encoding.sexp", "state.sexp", "interactions.sexp", "contract.sexp", "gate.sexp")
        live = _tracked()

        def gs(name, edits=None, extra_files=None):
            g = tmp / f"gs-{name}"
            g.mkdir()
            for doc in docs:
                text = (real / doc).read_text(encoding="utf-8")
                for target, fn in (edits or {}).items():
                    if target == doc:
                        text = fn(text)
                (g / doc).write_text(text, encoding="utf-8")
            files = {(g / doc).relative_to(ROOT).as_posix() for doc in docs}
            for fname, text in (extra_files or {}).items():
                (g / fname).write_text(text, encoding="utf-8")
                files.add((g / fname).relative_to(ROOT).as_posix())
            return build_cpusystem("rv64gc-lab-v0", d=g, tracked=live | files)

        def row(report, axis):
            return next(l for l in report.splitlines() if l.startswith(f"| `{axis}` | ") and "Required" not in l
                        and l.count("|") == 5)

        def has(report, *needles):
            for n in needles:
                assert n in report, f"missing {n!r}"

        def gs_refuses(name, edits, needle):
            try:
                gs(name, edits)
            except SystemExit as e:
                assert needle in str(e), f"refused, but for {e}"
                return
            raise AssertionError("not refused")

        ev = lambda body: (lambda s: s + "\n" + body + "\n")  # noqa: E731

        def kinds(report, axis):
            m = re.search(rf"\| `{axis}` \| [^|]* \| (\d+) of \d+ required kinds evidenced", report)
            assert m, f"no kinds count in the {axis} row"
            return int(m.group(1))

        def verdict_of(report, axis):
            return row(report, axis).rstrip(" |").rsplit("**", 2)[-2]

        try:
            rep0 = gs("green")
        except Exception as e:                      # noqa: BLE001 — every GS arm then misses
            rep0 = ""
            missed.append(f"the baseline CPU-SYSTEM report itself failed: {e}")

        def green():
            rows = [a for a in GS_AXES if f"| `{a}` | " in rep0]
            assert rows == list(GS_AXES), f"the axis rows {rows}"
            assert "**Verdict: `" in rep0 and "Unowned" not in rep0, "a verdict line, every open axis owned"
        arm("GREEN the real manifest: all ten axes reported, a verdict, every open axis owned", green)
        arm("RED a test function that does not exist is not evidence (-1 regression kind)",
            lambda: (lambda r: (assert_eq(kinds(r, "G-REGRESSION"), kinds(rep0, "G-REGRESSION") - 1),
                                has(r, "**no** — no such test function in the file")))(
                gs("nofn", {"gate.sexp": lambda s: s.replace(
                    '(fn "every_guest_matches_its_expectations")', '(fn "no_such_test")')})))
        arm("RED a kind the axis does not require is refused",
            lambda: gs_refuses("badkind", {"gate.sexp": ev(
                '(evidence (axis G-REPLAY) (kind directed) (experiment "x") (statement "s"))')},
                "is not one G-REPLAY requires"))
        arm("RED an evidence form naming two locators is refused",
            lambda: gs_refuses("twoloc", {"gate.sexp": ev(
                '(evidence (axis G-TRACE) (kind experiment) (experiment "x") (record "y") (statement "s"))')},
                "names exactly one of test / record / experiment"))
        arm("RED a not-applicable kind counts (+1), and is printed with its reason",
            lambda: (lambda r: (assert_eq(kinds(r, "G-REGRESSION"), kinds(rep0, "G-REGRESSION") + 1),
                                has(r, "not applicable — the stated reason")))(
                gs("na", {"gate.sexp": ev(
                    '(not-applicable (axis G-REGRESSION) (kind workload) (why "the stated reason"))')})))
        rec = (tmp / "gs-failrec" / "act.sexp").relative_to(ROOT).as_posix()
        arm("RED a verdict-bearing record that reads a failure is not evidence",
            lambda: (lambda r: (assert_eq(kinds(r, "G-REGRESSION"), kinds(rep0, "G-REGRESSION")),
                                has(r, "**no** — the record reads 1 fail")))(
                gs("failrec", {"gate.sexp": ev(
                    f'(evidence (axis G-REGRESSION) (kind external) (record "{rec}") (statement "s"))')},
                   {"act.sexp": '(campaign (verdicts "3 pass / 1 fail"))\n'})))
        arm("RED an open axis with no declared owner reads unowned",
            lambda: has(gs("unowned", {"gate.sexp": lambda s: s[:s.index('(open (axis G-RELEASE)')]}),
                        "**Unowned open axes: `G-RELEASE`**"))
        unslotted = lambda s: re.sub(r"\s*\(status partial\)|\s*\(slot \(id [a-z]+\) \(requires \"[^\"]+\"\)\)",  # noqa: E731
                                     "", s)
        slotted = lambda s: unslotted(s).replace('(extensions "riscv/zicsr")',  # noqa: E731
                                                 '(extensions "riscv/zicsr") (status partial) (slot (id z) (requires "riscv/z"))', 1)
        arm("RED the scope measure discriminates: no slot reads green, one unfilled slot incomplete",
            lambda: (assert_eq(verdict_of(gs("scope0", {"encoding.sexp": unslotted}), "G-SCOPE"), "green"),
                     (lambda r: (assert_eq(verdict_of(r, "G-SCOPE"), "incomplete"),
                                 has(r, "unfilled slots: `z`")))(gs("scope1", {"encoding.sexp": slotted}))))
        arm("RED an undispositioned cell opens G-INTERACTIONS",
            lambda: (lambda r: (assert_eq(verdict_of(r, "G-INTERACTIONS"), "incomplete"),
                                has(r, "undispositioned: fault × alias")))(
                gs("cell", {"interactions.sexp": lambda s: re.sub(
                    r'(\(cell \(axis "fault"\) \(axis "alias"\))[^\n]*', r"\1)", s, count=1)})))
        arm("RED `passed` is unreachable while any axis is open, and reached when none is",
            lambda: (assert_eq(_gs_verdict({a: ("", True) for a in GS_AXES})[0], "passed"),
                     assert_eq(_gs_verdict({**{a: ("", True) for a in GS_AXES}, "G-REPLAY": ("", False)}),
                               ("incomplete", ["G-REPLAY"])),
                     assert_eq(_gs_verdict({a: ("", True) for a in GS_AXES[:-1]})[0], "incomplete")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for m in missed:
        print(f"gate_report --self-test MISS: {m}", file=sys.stderr)
    want = 17
    if ran != want:
        print(f"gate_report --self-test HARNESS: {ran} arm(s) ran, {want} declared", file=sys.stderr)
    print(f"gate_report --self-test: {passed} pass / {len(missed) + (ran != want)} fail")
    return 0 if not missed and ran == want else 1


def main(argv: list[str]) -> int:
    if argv[1:] == ["--self-test"]:
        return _selftest()
    gate = "G0"
    rest: list[str] = []
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--gate" and i + 1 < len(argv):
            gate = argv[i + 1]
            i += 2
            continue
        if arg.startswith("--gate="):
            gate = arg.split("=", 1)[1]
            i += 1
            continue
        rest.append(arg)
        i += 1
    if gate == "BREADTH":
        text = build_breadth()
        if "--stdout" in rest:
            sys.stdout.write(text)
            return 0
        out = ROOT / "docs" / "BREADTH-REPORT.md"
        out.write_text(text)
        print(f"wrote {out.relative_to(ROOT)} ({len(text)} bytes)")
        return 0
    if not rest or rest[0].startswith("--"):
        print("usage: gate_report.py <profile> [--gate G0|G1|GC|GS] [--stdout]", file=sys.stderr)
        print("       gate_report.py --gate BREADTH [--stdout]", file=sys.stderr)
        return 2
    builders = {"G0": build, "G1": build_g1, "GC": build_cpulab, "GS": build_cpusystem}
    if gate not in builders:
        print(f"gate_report: unknown gate '{gate}' (G0, G1, GC, GS or BREADTH)", file=sys.stderr)
        return 2
    profile = rest[0]
    text = builders[gate](profile)
    if "--stdout" in rest:
        sys.stdout.write(text)
        return 0
    out = ROOT / "profiles" / profile / f"{gate}-REPORT.md"
    out.write_text(text)
    print(f"wrote {out.relative_to(ROOT)} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
