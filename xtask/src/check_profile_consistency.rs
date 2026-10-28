//! The `PROFILE-CONSISTENCY` doctrine's driver, ported from `scripts/check_profile_consistency.sh` (`XTASK.6` slice `6ar`),
//! which is now a shim of `cargo xtask check-profile-consistency`.
//!
//! A profile dossier is a set of claims about a specification: the declared counts must equal their enumerations, every
//! decision must carry an authority and a source, an empty `hidden_state` must be backed by a census, `state.sexp` and
//! `profile.sexp` must agree, the reference dossier must earn every `obtained` and name every pair's independence. The
//! judge is the driver's 330-line inline Python (`check_profiles`, over the pinned dossier reader and verification
//! modules); it runs verbatim through `python3 -`, as the script ran it, and is not ported — nor are the four tools the
//! real run consults first (the retained-statement verifiers, the requirement-status derivation, the policy review), nor
//! the forty-odd probe suites the controls score. The controls' fixture surgery (the script's `sed`, `grep -v`, `printf`
//! and string composition) is the same literal text manipulation; the `XTASK.8` prefetch keeps its shape — every probe
//! invocation is recorded on a first pass, run in parallel by `scripts/doctrine_prefetch.py`, and answered from the
//! record on the scoring pass (`PROFILE_CONSISTENCY_PREFETCH=0` restores the live run, `…_MISSES=<file>` logs the
//! argv answered live, `…_RECORD_ARGV=<file>` records and scores nothing, as the script's shadow did). The quiet run
//! keeps the controls' output in `target/profile-consistency-selftest.log` and shows its MISS lines on a refusal, as the
//! script did. Each self-test arm is one `tally.arm(` call and each scored probe one `tally.score(` call — the mode
//! loops keep their one GREEN and one RED call each, as the script's did — the idioms the `DERIVED-COUNTS` arm total
//! counts.

use std::ffi::OsStr;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{on_path, scratch};

const SELF_TEST_LOG: &str = "target/profile-consistency-selftest.log";

/// The judge, verbatim: `python3 - <root>` from the repository root (`scripts/` on its path) — the findings, then
/// `__CHECKED__ N`; exit 1 on a finding. `python3 - --csr-cross <profile-dir> <state>` is its cross-document csr check.
const JUDGE: &str = r###"import sys, pathlib
sys.path.insert(0, "scripts")
import dossier_sexp as D
import experiment_verification as V
import experiment_artifacts as A
import records_sexp as R
import sexp as S
import credit_records as CR

# P4-SYSTEM.2 slice (c1): the csr-set rule applied OUTSIDE a unit directory — the staged
# rv64gc state document lives at a scratch path until the route flip, and must validate
# from there (the same comparison, the same verdict shape).
if sys.argv[1] == "--csr-cross":
    prof_dir, state_path = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
    d = D.load(prof_dir / "profile.sexp")
    st = D.load(state_path)
    want = set(d.get("state", {}).get("csrs", []) or [])
    got = {c["id"] for c in st.get("csr", [])}
    if want == got:
        print(f"csr-cross: ok ({len(got)} csr(s) agree, both directions)")
        sys.exit(0)
    print(f"CSR SET MISMATCH: profile-only {sorted(want - got)}; doc-only {sorted(got - want)}")
    sys.exit(1)

root = pathlib.Path(sys.argv[1])
AUTHORITIES = {"architecture", "execution-environment", "laboratory"}
# `software-convention` is legal only in state.sexp, for ABI roles: the calling convention is
# neither architecture nor an EEI choice, and recording an ABI name as architectural is the
# mistake `docs/INFORMATION_CATALOG.md` §6 names explicitly.
STATE_AUTHORITIES = AUTHORITIES | {"software-convention"}
findings, checked = [], 0

for profile_path in sorted(root.glob("*/profile.sexp")):
    name = profile_path.parent.name
    checked += 1
    try:
        d = D.load(profile_path)
    except D.DossierError as e:
        findings.append(f"UNPARSEABLE {name}/profile.sexp — {e}")
        continue

    scope = d.get("scope")
    if not isinstance(scope, dict):
        findings.append(f"NO SCOPE   {name}: profile.sexp has no (scope …) table")
    else:
        listed = sum(len(v) for v in scope.values() if isinstance(v, list))
        declared = scope.get("count_total")
        if declared is None:
            findings.append(f"NO COUNT   {name}: (scope …) declares no count_total to check")
        elif listed != declared:
            findings.append(
                f"COUNT DRIFT {name}: (scope …) enumerates {listed} mnemonic(s), "
                f"count_total = {declared}")
        # the part-counts must also add up to the whole: the base split, plus — since
        # P4-SYSTEM.2 slice (e) — the extension family lists when the profile carries them
        # (the rv64gc census: base 40 + rv64i 12 + zicsr 6 + system 4 + zicntr 3 = 65;
        # P4-SYSTEM.4 slice (e): + a_atomics 22 = 87; P4-SYSTEM.6 slice (b): + zifencei_fencei 1 = 88;
        # P4-SYSTEM.7 slice (c6): + f_single 30 = 118; slice (d5): + d_double 32 = 150;
        # P4-SYSTEM.11 slice (b): + m_muldiv 13 = 163; .12 e2c: + c_compressed 37 = 200)
        a, b = scope.get("count_base"), scope.get("count_rv64i_additions")
        if a is not None and b is not None and declared is not None:
            ext = sum(len(scope.get(k) or [])
                      for k in ("zicsr_csrs", "system_privileged", "zicntr_counters",
                                "a_atomics", "zifencei_fencei", "f_single", "d_double",
                                "m_muldiv", "c_compressed"))
            if a + b + ext != declared:
                findings.append(
                    f"PARTS DRIFT {name}: count_base {a} + count_rv64i_additions {b}"
                    + (f" + extension families {ext}" if ext else "")
                    + f" != {declared}")

    # ---- state.sexp, when present: agreement with profile.sexp, and an earned census ----
    state_path = profile_path.parent / "state.sexp"
    if state_path.is_file():
        try:
            st = D.load(state_path)
        except D.DossierError as e:
            findings.append(f"UNPARSEABLE {name}/state.sexp — {e}")
            st = None
        if st is not None:
            if st.get("profile_id") != d.get("profile", {}).get("id"):
                findings.append(
                    f"ID MISMATCH {name}: state.sexp profile_id "
                    f"{st.get('profile_id')!r} != profile.sexp id {d.get('profile', {}).get('id')!r}")
            if st.get("xlen") != d.get("profile", {}).get("xlen"):
                findings.append(
                    f"XLEN MISMATCH {name}: state.sexp {st.get('xlen')} != profile.sexp "
                    f"{d.get('profile', {}).get('xlen')}")
            want_regs = d.get("state", {}).get("integer_registers")
            got_regs = (st.get("integer_registers") or {}).get("count")
            if want_regs is not None and got_regs != want_regs:
                findings.append(
                    f"REG COUNT MISMATCH {name}: state.sexp {got_regs} != profile.sexp {want_regs}")
            # P4-SYSTEM.2 slice (c1): the (csrs …) enumeration and the state document's CSR
            # set are one fact stated twice — they must agree exactly, both directions.
            want_csrs = set(d.get("state", {}).get("csrs", []) or [])
            got_csrs = {c["id"] for c in st.get("csr", [])}
            if want_csrs != got_csrs:
                findings.append(
                    f"CSR SET MISMATCH {name}: profile.sexp declares "
                    f"{sorted(want_csrs - got_csrs) or 'nothing extra'} the state document "
                    f"does not carry, and the state document carries "
                    f"{sorted(got_csrs - want_csrs) or 'nothing extra'} profile.sexp does "
                    f"not declare — one CSR set, stated once each way")
            def authorities(o):
                if isinstance(o, dict):
                    if "authority" in o and isinstance(o["authority"], str):
                        yield o["authority"]
                    for v in o.values():
                        yield from authorities(v)
                elif isinstance(o, list):
                    for v in o:
                        yield from authorities(v)
            for a in authorities(st):
                if a not in STATE_AUTHORITIES:
                    findings.append(
                        f"BAD AUTHORITY {name}/state.sexp: '{a}' not in {sorted(STATE_AUTHORITIES)}")
            if "hidden_state" in st and not st["hidden_state"]:
                census = st.get("hidden_state_census")
                cands = (census or {}).get("candidates_checked") or []
                if not cands:
                    findings.append(
                        f"UNEARNED NONE {name}/state.sexp: hidden_state is empty with no census. "
                        f"'nothing else can influence a future observation' is a claim over a set, "
                        f"false the moment one exists — enumerate what was considered.")
                else:
                    for c in cands:
                        if "present" not in c or not c.get("why"):
                            findings.append(
                                f"THIN CENSUS {name}/state.sexp: candidate "
                                f"{c.get('candidate','<unnamed>')!r} lacks present/why")

    # ---- references.sexp, when present: the reference candidate dossier ----------------
    refs_path = profile_path.parent / "references.sexp"
    if refs_path.is_file():
        STATUSES = {"obtained", "not obtained", "reachable, not acquired",
                    "acquired (sparse partial)"}
        # An `obtained` candidate claims we HAVE it. These are the fields that make the claim
        # checkable rather than remembered.
        OBTAINED_REQUIRED = ("binary", "binary_sha256", "invocation", "trace_granularity",
                             "injection", "terms")
        try:
            rf = D.load(refs_path)
        except D.DossierError as e:
            findings.append(f"UNPARSEABLE {name}/references.sexp — {e}")
            rf = None
        if rf is not None:
            if rf.get("profile") != d.get("profile", {}).get("id"):
                findings.append(
                    f"REF PROFILE MISMATCH {name}: references.sexp profile "
                    f"{rf.get('profile')!r} != profile.sexp id {d.get('profile', {}).get('id')!r}")
            cands = rf.get("candidate", [])
            if not cands:
                findings.append(
                    f"NO CANDIDATES {name}/references.sexp: a reference dossier with no candidate "
                    f"records nothing — an empty list is not the same as an examined one")
            seen = set()
            for c in cands:
                cid = c.get("id", "<unnamed>")
                if cid in seen:
                    findings.append(f"DUPLICATE CANDIDATE {name}: '{cid}' appears twice")
                seen.add(cid)
                st = c.get("status")
                if st not in STATUSES:
                    findings.append(
                        f"BAD STATUS {name}/{cid}: '{st}' not in {sorted(STATUSES)}")
                if not c.get("role"):
                    findings.append(f"NO ROLE    {name}/{cid}: candidate states no role")
                if not c.get("origin"):
                    findings.append(f"NO ORIGIN  {name}/{cid}: candidate cites no origin")
                if not c.get("lineage"):
                    findings.append(
                        f"NO LINEAGE {name}/{cid}: EVD-04 asks whether two comparators share "
                        f"semantic ancestry; a candidate with no lineage field leaves that "
                        f"unasked, and unasked reads exactly like independent")
                # 5b. a scalar standing for a configuration declares its scope and its source
                if c.get("matched_isa_string"):
                    for k in ("matched_scope", "matched_isa_string_source"):
                        if not c.get(k):
                            findings.append(
                                f"UNSCOPED SCALAR {name}/{cid}: pins 'matched_isa_string' with no "
                                f"'{k}'. A scalar standing for a configuration must say what it "
                                f"does NOT establish and where it was read from — an instrument "
                                f"answering a narrower question than the one asked is the harder "
                                f"defect, because its answer is correct")
                if st == "obtained":
                    for k in OBTAINED_REQUIRED:
                        if not c.get(k):
                            findings.append(
                                f"UNEARNED OBTAINED {name}/{cid}: status is 'obtained' with no "
                                f"'{k}' — SRC-03 forbids recording availability that has not "
                                f"been established")
                elif not c.get("status_reason"):
                    findings.append(
                        f"NO REASON  {name}/{cid}: status is '{st}' with no status_reason; "
                        f"SRC-02 makes an honest 'no route' legitimate, but it has to say why")
            experiment_ids = set()
            verification_scope = None
            raw_experiments = []
            if any("verification" in x for x in rf.get("experiment", [])):
                try:
                    verification_scope = V.load_scope(profile_path.parent,
                        d.get("profile", {}).get("id"), seen)
                    raw_references = next(f for f in S.read_file(refs_path)
                                          if isinstance(f, list) and f and f[0] == "references")
                    raw_experiments = S.children(raw_references, "experiment")
                    if len(raw_experiments) != len(rf.get("experiment", [])):
                        raise ValueError("reference experiment count changed during validation")
                except (OSError, R.RecordRefused, S.SexpError, SystemExit,
                        KeyError, ValueError, StopIteration) as error:
                    findings.append(f"VERIFICATION SCOPE UNAVAILABLE {name}: {error}")
                    verification_scope = None
            for experiment_index, x in enumerate(rf.get("experiment", [])):
                xid = x.get("id", "<unnamed>")
                if xid in experiment_ids:
                    findings.append(
                        f"DUPLICATE EXPERIMENT ID {name}/{xid}: identity appears twice")
                experiment_ids.add(xid)
                if "verification" in x:
                    if verification_scope is not None:
                        graph_findings = V.check_experiment(raw_experiments[experiment_index],
                                                            verification_scope)
                        findings.extend(f"{name}/{xid}: {finding}" for finding in graph_findings)
                        if not graph_findings:
                            for pin in A.check_files(pathlib.Path.cwd(), x["verification"]):
                                if pin.disposition != "matched":
                                    findings.append(f"VERIFICATION ARTIFACT {name}/{xid}/"
                                        f"{pin.record_kind}/{pin.record_id}: {pin.disposition}: {pin.reason}")
                    # a42bc: qualified exactly when a CURRENT credit record names the case and the record is
                    # the case's measured record (credit_records.dossier_qualification); otherwise the
                    # refusal stands, naming why. Matching pins alone still give no qualification.
                    why = CR.dossier_qualification(pathlib.Path.cwd(), profile_path.parent,
                                                   raw_experiments[experiment_index]
                                                   if experiment_index < len(raw_experiments) else None)
                    if why:
                        findings.append(
                            f"UNQUALIFIED EXPERIMENT VERIFICATION {name}/{xid}: " + "; ".join(why))
                models = x.get("models") or []
                if len(models) != len(set(models)):
                    findings.append(
                        f"REPEATED EXPERIMENT MODEL {name}/{xid}: models must be distinct")
                for model in models:
                    if model not in seen:
                        findings.append(
                            f"UNKNOWN EXPERIMENT MODEL {name}/{xid}: '{model}' is not a candidate")
                for k in ("program", "models", "verdict", "reproduced"):
                    if not x.get(k):
                        findings.append(
                            f"THIN EXPERIMENT {name}/{xid}: no '{k}' — an experiment record "
                            f"without it cannot be re-run or judged")
                if not x.get("control"):
                    findings.append(
                        f"NO CONTROL {name}/{xid}: the experiment reports a verdict with no "
                        f"control that was observed FAILING. A comparison never seen to diverge "
                        f"is not known to detect divergence")
            # 7. every compared pair has an independence row (the verdict may be anything)
            INDEPENDENCE_VERDICTS = {
                "shared", "not-shared", "no-evidence-of-sharing", "not-examined"}
            examined: set[frozenset] = set()
            for ind in rf.get("independence", []):
                pair = ind.get("pair") or []
                label = "/".join(pair) if pair else "<unpaired>"
                if len(pair) != 2 or len(set(pair)) != 2:
                    findings.append(
                        f"BAD PAIR   {name}/{label}: an independence record names "
                        f"{len(pair)} model(s), {len(set(pair))} distinct; "
                        f"independence is a property of two distinct candidates")
                else:
                    examined.add(frozenset(pair))
                    for m in pair:
                        if m not in seen:
                            findings.append(
                                f"UNKNOWN MODEL {name}/{label}: '{m}' is not a candidate "
                                f"in this dossier")
                if ind.get("verdict") not in INDEPENDENCE_VERDICTS:
                    findings.append(
                        f"BAD VERDICT {name}/{label}: '{ind.get('verdict')}' not in "
                        f"{sorted(INDEPENDENCE_VERDICTS)}")
                for k in ("subsystem", "evidence", "consequence"):
                    if not ind.get(k):
                        findings.append(
                            f"THIN INDEPENDENCE {name}/{label}: no '{k}' — "
                            f"EVD-04 asks for the examination, not the conclusion")
            for x in rf.get("experiment", []):
                models = x.get("models") or []
                for i in range(len(models)):
                    for j in range(i + 1, len(models)):
                        if frozenset((models[i], models[j])) not in examined:
                            findings.append(
                                f"UNEXAMINED PAIR {name}/{x.get('id','<unnamed>')}: the "
                                f"experiment compares '{models[i]}' with '{models[j]}' and no "
                                f"independence record examines that pair. Recording that two "
                                f"models agree takes a position on their independence whether "
                                f"or not anyone looked; 'not-examined' is a legal verdict, "
                                f"silence is not")
            for dfn in rf.get("difference", []):
                did2 = dfn.get("id", "<unnamed>")
                for k in ("kind", "observed", "resolution"):
                    if not dfn.get(k):
                        findings.append(
                            f"THIN DIFFERENCE {name}/{did2}: no '{k}' — gate G0 asks for "
                            f"differences to be enumerated, which means stated and dispositioned")
            for a in rf.get("attempt", []):
                for k in ("what", "outcome", "consequence"):
                    if not a.get(k):
                        findings.append(
                            f"THIN ATTEMPT {name}/references.sexp: an attempt record lacks '{k}' "
                            f"— an attempt without its consequence is a note, not evidence")

    decisions = d.get("decision", [])
    if not decisions:
        findings.append(f"NO DECISIONS {name}: a profile with no recorded decision records nothing")
    ids = set()
    for dec in decisions:
        did = dec.get("id", "<unnamed>")
        if did in ids:
            findings.append(f"DUPLICATE ID {name}: decision id '{did}' appears twice")
        ids.add(did)
        auth = dec.get("authority")
        if auth not in AUTHORITIES:
            findings.append(
                f"BAD AUTHORITY {name}/{did}: '{auth}' not in {sorted(AUTHORITIES)}")
        if not dec.get("source"):
            findings.append(f"NO SOURCE  {name}/{did}: decision cites nothing")
        if not dec.get("statement"):
            findings.append(f"NO STATEMENT {name}/{did}: decision states nothing")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
"###;

/// The fixtures, written as the converted form the gate reads (the script's heredocs, verbatim).
const GOOD: &str = r##"(profile (id "p1") (xlen 64)
  (state (integer_registers 4))
  (scope (count_base 2) (count_rv64i_additions 1) (count_total 3)
         (base_op "X") (base_op "Y") (base_jumps "Z"))
  (decision (id "D-1")
            (authority architecture)
            (statement "s")
            (source "§1")
  )
)
"##;
const GOOD_STATE: &str = r##"(state (profile_id "p1") (xlen 64) (note "n")
  (integer_registers (count 4) (width_bits 64) (ids "x0..x3")
    (authority architecture) (source "s")
    (x0 (hardwired_zero true) (authority architecture) (source "s") (statement "x"))
    (named_by_the_isa_chapter (named-register (reg "x1") (role "r")
                               (authority software-convention) (source "s"))))
  (special_registers (register (id "pc") (width_bits 64) (holds "h")
                      (authority architecture) (source "s") (reset "r")
                      (reset_authority laboratory)))
  (hidden_state_census (question "q") (answer "No") (candidates (checked (candidate "c") (present false) (why "w"))) (consequence "c"))
)
"##;
/// `good_csr`'s state document (the profile side is a `sed` on `GOOD`).
const CSR_STATE: &str = r##"(state (profile_id "p1") (xlen 64) (note "n")
  (integer_registers (count 4) (width_bits 64) (ids "x0..x3")
    (authority architecture) (source "s")
    (x0 (hardwired_zero true) (authority architecture) (source "s") (statement "x"))
    (named_by_the_isa_chapter (named-register (reg "x1") (role "r")
                               (authority software-convention) (source "s"))))
  (special_registers (register (id "pc") (width_bits 64) (holds "h")
                      (authority architecture) (source "s") (reset "r")
                      (reset_authority laboratory)))
  (csr (id "mstatus") (address 768) (width_bits 64) (authority architecture) (source "s")
    (reset (value "0") (authority laboratory) (source "s") (statement "x")))
  (csr (id "mcycle") (address 2816) (width_bits 64) (authority architecture) (source "s")
    (reset (value "0") (authority laboratory) (source "s") (statement "x")))
  (hidden_state_census (question "q") (answer "No") (candidates (checked (candidate "c") (present false) (why "w"))) (consequence "c"))
)
"##;
const DEVICE: &str = r##"(profile (id "p1")
  (state (authority architecture) (source "s"))
  (vehicle (route device-model) (comparison register-expectations)
           (authority laboratory) (source "s"))
  (scope (count_base 2) (count_total 2)
         (mmio_registers "UART_RXDATA") (mmio_registers "UART_TXDATA"))
  (decision (id "D-1")
            (authority laboratory)
            (statement "s")
            (source "§1")
  )
)
"##;
const DEVICE_STATE: &str = r##"(state (profile_id "p1") (note "n")
  (special_registers (register (id "uart_rxdata") (width_bits 8) (holds "h")
                      (authority architecture) (source "s") (reset "r")
                      (reset_authority laboratory)))
  (hidden_state_census (question "q") (answer "No") (candidates (checked (candidate "c") (present false) (why "w"))) (consequence "c"))
)
"##;
/// The reference dossier WITHOUT its closing paren: rows are appended INSIDE the form, then the arm closes it.
const BASE: &str = r#"(references (profile "p1")
  (candidate (id "c1")
             (role "oracle")
             (status "obtained")
             (origin "https://example.invalid")
             (lineage "written independently")
             (binary "b")
             (binary_sha256 "deadbeef")
             (invocation "b --run")
             (trace_granularity "per instruction")
             (injection "gdb")
             (terms "BSD-2-Clause"))
  (attempt (what "tried x")
           (outcome "failed")
           (consequence "recorded")
  )
"#;
/// The experiment and difference rows appended to `BASE` (`EXP`).
const EXP_TAIL: &str = r#"
  (experiment (id "e1")
              (program "g.s")
              (models "c1")
              (verdict "AGREE")
              (reproduced "yes")
              (control "observed failing when a value was falsified")
  )
  (difference (id "d1")
              (kind "harness")
              (observed "they differ")
              (resolution "normalized")
  )"#;
/// A second candidate with the first's id, and the closing paren.
const DUP_CAND_TAIL: &str = r#"
  (candidate (id "c1") (role "dup") (status "not obtained")
             (status_reason "r") (origin "o") (lineage "l"))
)"#;
const C2: &str = r#"
  (candidate (id "c2") (role "second") (status "not obtained")
             (status_reason "not needed for this fixture") (origin "https://example.invalid/2")
             (lineage "unknown"))"#;
const IND_ROW: &str = r#"
  (independence (subsystem "integer")
                (pair "c1")
                (pair "c2")
                (verdict "not-examined")
                (evidence "none")
                (consequence "owner named"))"#;
const DUP_EXP: &str = r#"
  (experiment (id "e1") (program "other.s") (models "c1")
              (verdict "DIVERGE") (reproduced "yes") (control "different result observed"))"#;
/// The scoped-scalar dossier (5b), without its closing paren.
const SC1: &str = r#"(references (profile "p1")
  (candidate (id "c1")
             (role "oracle")
             (status "obtained")
             (origin "https://example.invalid")
             (lineage "written independently")
             (binary "b")
             (binary_sha256 "deadbeef")
             (invocation "b --run")
             (trace_granularity "per instruction")
             (injection "gdb")
             (terms "BSD-2-Clause")
             (matched_isa_string "rv64i")
             (matched_isa_string_source "observed")
             (matched_scope "the instruction set only")
  )
  (attempt (what "tried x")
           (outcome "failed")
           (consequence "recorded")
  )"#;

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `printf '%s' "$X" | grep -v 'NEEDLE'`, captured: the lines not carrying the needle, joined, no trailing newline.
fn without(text: &str, needle: &str) -> String {
    let kept: Vec<&str> = text.split('\n').filter(|l| !l.contains(needle)).collect();
    kept.join("\n").trim_end_matches('\n').to_owned()
}

/// `printf '%s' "$X" | sed 's/A/B/'`, captured: the first occurrence on every line replaced, no trailing newline.
fn sub_first(text: &str, from: &str, to: &str) -> String {
    let lines: Vec<String> = text.split('\n').map(|l| l.replacen(from, to, 1)).collect();
    lines.join("\n").trim_end_matches('\n').to_owned()
}

/// `sed -i.bak 's/A/B/[; s/C/D/]' path`: the original kept beside as `.bak`, each substitution's first occurrence
/// replaced on every line.
fn sed_i_bak(path: &Path, subs: &[(&str, &str)]) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let _ = fs::write(bak(path), &text);
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        let mut l = line.to_owned();
        for (from, to) in subs {
            l = l.replacen(from, to, 1);
        }
        out.push_str(&l);
    }
    let _ = fs::write(path, out);
}

/// `sed -i.bak '/NEEDLE/d' path`.
fn sed_i_bak_delete(path: &Path, needle: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let _ = fs::write(bak(path), &text);
    let kept: String = text
        .split_inclusive('\n')
        .filter(|l| !l.contains(needle))
        .collect();
    let _ = fs::write(path, kept);
}

/// `sed -i.bak '$i\LINE' path`: the line inserted before the last one.
fn sed_i_bak_insert_before_last(path: &Path, line: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let _ = fs::write(bak(path), &text);
    let mut lines: Vec<&str> = text.split_inclusive('\n').collect();
    let at = lines.len().saturating_sub(1);
    let inserted = format!("{line}\n");
    lines.insert(at, &inserted);
    let _ = fs::write(path, lines.concat());
}

/// `sed '/^START/,/^END$/d' path > x && mv x path`: every range from a line starting with `start` through the next line
/// equal to `end`, inclusive, deleted.
fn delete_ranges(path: &Path, start: &str, end: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    let mut inside = false;
    for line in text.split_inclusive('\n') {
        let bare = line.trim_end_matches('\n');
        if inside {
            if bare == end {
                inside = false;
            }
            continue;
        }
        if bare.starts_with(start) {
            inside = true;
            continue;
        }
        out.push_str(line);
    }
    let _ = fs::write(path, out);
}

/// `grep -v 'NEEDLE' path > x && mv x path`.
fn drop_lines(path: &Path, needle: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let kept: String = text
        .split_inclusive('\n')
        .filter(|l| !l.contains(needle))
        .collect();
    let _ = fs::write(path, kept);
}

fn bak(path: &Path) -> PathBuf {
    let mut name = path
        .file_name()
        .map(|n| n.to_os_string())
        .unwrap_or_default();
    name.push(".bak");
    path.with_file_name(name)
}

/// Where the controls' own chatter goes: the terminal when the self-test is the command, the script's log when the
/// real run re-runs the controls, nowhere on the recording pass (`( … ) >/dev/null 2>&1`).
enum Report {
    Terminal,
    Log(fs::File),
    Null,
}

impl Report {
    fn line(&mut self, text: &str) {
        match self {
            Report::Terminal => eprintln!("{text}"),
            Report::Log(file) => {
                let _ = writeln!(file, "{text}");
            }
            Report::Null => {}
        }
    }

    fn out(&mut self, text: &str) {
        match self {
            Report::Terminal => println!("{text}"),
            Report::Log(file) => {
                let _ = writeln!(file, "{text}");
            }
            Report::Null => {}
        }
    }
}

/// The `python3` shadow of XTASK.8: how a probe invocation is answered.
enum Prober {
    /// Every probe runs live.
    Live,
    /// The recording pass: the argv is kept, nothing runs, the answer is `0` with no output.
    Record(Vec<Vec<String>>),
    /// `PROFILE_CONSISTENCY_RECORD_ARGV`: the argv appended to that file, nothing runs.
    RecordTo(PathBuf),
    /// The scoring pass: an exact argv is answered from the prefetch record, anything else runs live (and is logged to
    /// `PROFILE_CONSISTENCY_PREFETCH_MISSES` when set).
    Answer {
        dir: PathBuf,
        misses: Option<PathBuf>,
    },
}

/// The record's key: the argv U+001F-joined with `/` as U+001E (`doctrine_prefetch.key`).
fn record_key(argv: &[String]) -> String {
    argv.join("\u{1f}").replace('/', "\u{1e}")
}

/// `python3 <argv…>` from the repository root — stdout and stderr merged (`2>&1`) or stdout alone with stderr through.
fn live(repo: &Path, argv: &[String], merge: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command.args(argv).current_dir(repo).stdin(Stdio::null());
    if !merge {
        command.stderr(Stdio::inherit());
    }
    match command.output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            if merge {
                text.push_str(&String::from_utf8_lossy(&o.stderr));
            }
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

impl Prober {
    /// A probe invocation (`python3 [-B] [-O] scripts/probe_*.py …`), its `2>&1` output and exit status.
    fn probe(&mut self, repo: &Path, argv: Vec<String>) -> (i32, String) {
        self.probe_with(repo, argv, true)
    }

    fn probe_with(&mut self, repo: &Path, argv: Vec<String>, merge: bool) -> (i32, String) {
        match self {
            Prober::Live => live(repo, &argv, merge),
            Prober::Record(seen) => {
                seen.push(argv);
                (0, String::new())
            }
            Prober::RecordTo(path) => {
                if let Ok(mut f) = fs::OpenOptions::new().append(true).create(true).open(path) {
                    let _ = writeln!(f, "{}", argv.join("\u{1f}"));
                }
                (0, String::new())
            }
            Prober::Answer { dir, misses } => {
                let key = record_key(&argv);
                if let Some(code) = fs::read_to_string(dir.join(format!("{key}.rc")))
                    .ok()
                    .and_then(|s| s.trim().parse::<i32>().ok())
                {
                    let out = fs::read(dir.join(format!("{key}.out"))).unwrap_or_default();
                    return (code, String::from_utf8_lossy(&out).into_owned());
                }
                if let Some(path) = misses {
                    if let Ok(mut f) = fs::OpenOptions::new().append(true).create(true).open(path) {
                        let _ = writeln!(f, "python3 {}", argv.join(" "));
                    }
                }
                live(repo, &argv, merge)
            }
        }
    }
}

/// `check_profiles <args…>`: the judge on stdin from the repository root; stdout and stderr merged when `merge`,
/// stderr through otherwise.
fn check_profiles(repo: &Path, args: &[&OsStr], merge: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .args(args)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if merge {
            Stdio::piped()
        } else {
            Stdio::inherit()
        });
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(JUDGE.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            if merge {
                text.push_str(&String::from_utf8_lossy(&o.stderr));
            }
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

struct Tally<'a> {
    repo: &'a Path,
    t: &'a Path,
    pass: u32,
    fail: u32,
    report: &'a mut Report,
}

impl Tally<'_> {
    /// `arm <name> <expected-rc> <reason>`: `check_profiles "$t" 2>&1` must exit `expected` and mention `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let (rc, raw) = check_profiles(self.repo, &[self.t.as_os_str()], true);
        let out = captured(&raw);
        if rc != expected {
            self.fail += 1;
            self.report.line(&format!("PROFILE-CONSISTENCY self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}"));
        } else if !out.contains(want) {
            self.fail += 1;
            self.report.line(&format!("PROFILE-CONSISTENCY self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}"));
        } else {
            self.pass += 1;
        }
    }

    /// `score <name> <rc> <expected-rc> <output> <reason>`: a probe's answer must exit `expected` and mention `want`.
    fn score(&mut self, name: &str, (rc, raw): (i32, String), expected: i32, want: &str) {
        let out = captured(&raw);
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report.line(&format!("PROFILE-CONSISTENCY self-test MISS: {name} expected rc={expected} reason={want} got rc={rc}\n{out}"));
        }
    }
}

/// The RED/GREEN controls against synthetic fixtures, then the scored probe suites. The report carries the controls'
/// chatter; the prober answers the probes (live, recording, or from the prefetch record).
fn self_test(repo: &Path, report: &mut Report, prober: &mut Prober) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "profileconsistency") else {
        report.line("PROFILE-CONSISTENCY self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let p = t.join("p");
    let _ = fs::create_dir_all(&p);
    let profile = p.join("profile.sexp");
    let state = p.join("state.sexp");
    let references = p.join("references.sexp");
    let mut tally = Tally {
        repo,
        t: &t,
        pass: 0,
        fail: 0,
        report: &mut *report,
    };
    let good = || {
        let _ = fs::write(&profile, GOOD);
    };
    let good_state = || {
        let _ = fs::write(&state, GOOD_STATE);
    };
    let good_csr = || {
        sed_i_bak(
            &profile,
            &[(
                "(state (integer_registers 4))",
                "(state (integer_registers 4) (csrs \"mstatus\") (csrs \"mcycle\"))",
            )],
        );
        let _ = fs::write(&state, CSR_STATE);
    };
    let refs = |text: &str| {
        let _ = fs::write(&references, format!("{text}\n"));
    };
    let device = || {
        let _ = fs::write(&profile, DEVICE);
    };
    let device_state = || {
        let _ = fs::write(&state, DEVICE_STATE);
    };
    // ---- a consistent dossier ----------------------------------------------------------------------
    good();
    tally.arm("GREEN consistent profile", 0, "__CHECKED__ 1");
    // ---- state.sexp arms ----------------------------------------------------------------------------
    good();
    good_state();
    tally.arm("GREEN state agrees with profile", 0, "__CHECKED__ 1");
    good();
    good_state();
    drop_lines(&state, "hidden_state_census");
    tally.arm("RED   empty hidden_state, no census", 1, "UNEARNED NONE");
    good();
    good_state();
    sed_i_bak(&state, &[("(xlen 64)", "(xlen 32)")]);
    tally.arm("RED   xlen disagrees", 1, "XLEN MISMATCH");
    good();
    good_state();
    sed_i_bak(&state, &[("(count 4)", "(count 9)")]);
    tally.arm("RED   register count disagrees", 1, "REG COUNT MISMATCH");
    // P4-SYSTEM.2 slice (c1): the profile's (csrs …) enumeration and the state document's csr set are one fact stated
    // twice — they must agree exactly, both directions.
    good();
    good_csr();
    tally.arm(
        "GREEN the csr set agrees, both directions",
        0,
        "__CHECKED__ 1",
    );
    good();
    good_csr();
    sed_i_bak(&state, &[("(id \"mcycle\")", "(id \"mtime\")")]);
    tally.arm(
        "RED   a csr the state document carries but the profile does not declare",
        1,
        "CSR SET MISMATCH",
    );
    good();
    good_csr();
    sed_i_bak(&profile, &[(" (csrs \"mcycle\")", "")]);
    tally.arm(
        "RED   a csr the profile declares but the state document does not carry",
        1,
        "CSR SET MISMATCH",
    );
    let _ = fs::remove_file(&state);
    let _ = fs::remove_file(bak(&profile));
    let _ = fs::remove_file(bak(&state));
    good();
    good_state();
    sed_i_bak(&state, &[("(authority architecture)", "(authority vibes)")]);
    tally.arm("RED   state authority unknown", 1, "BAD AUTHORITY");
    good();
    let _ = fs::remove_file(&state);
    // ---- profile.sexp arms --------------------------------------------------------------------------
    good();
    sed_i_bak(&profile, &[("(count_total 3)", "(count_total 4)")]);
    tally.arm("RED   count drifts from enumeration", 1, "COUNT DRIFT");
    good();
    sed_i_bak(&profile, &[("(count_base 2)", "(count_base 9)")]);
    tally.arm("RED   parts do not sum", 1, "PARTS DRIFT");
    good();
    sed_i_bak(
        &profile,
        &[
            ("(count_total 3)", "(count_total 4)"),
            (
                "(count_rv64i_additions 1)",
                "(count_rv64i_additions 1) (c_compressed \"C.NOP\")",
            ),
        ],
    );
    tally.arm(
        "GREEN C contributes to the extension census",
        0,
        "__CHECKED__ 1",
    );
    sed_i_bak(&profile, &[("(count_base 2)", "(count_base 3)")]);
    tally.arm("RED   C does not hide a wrong base part", 1, "PARTS DRIFT");
    good();
    sed_i_bak(
        &profile,
        &[("(authority architecture)", "(authority vibes)")],
    );
    tally.arm("RED   unknown authority", 1, "BAD AUTHORITY");
    good();
    sed_i_bak_delete(&profile, "(source ");
    tally.arm("RED   decision cites nothing", 1, "NO SOURCE");
    good();
    sed_i_bak_insert_before_last(
        &profile,
        "  (decision (id \"D-1\") (authority laboratory) (statement \"s\") (source \"x\"))",
    );
    tally.arm("RED   duplicate decision id", 1, "DUPLICATE ID");
    good();
    delete_ranges(&profile, "  (decision ", "  )");
    tally.arm("RED   no decisions at all", 1, "NO DECISIONS");
    let _ = fs::write(&profile, "not = toml = at = all\n");
    tally.arm("RED   unparseable profile", 1, "UNPARSEABLE");
    // ---- references.sexp: the reference candidate dossier --------------------------------------------
    good();
    let _ = fs::write(&references, format!("{BASE})\n"));
    tally.arm("GREEN complete reference dossier", 0, "__CHECKED__ 1");
    let full = format!("{BASE})");
    refs(&without(&full, "lineage"));
    tally.arm("RED   a candidate with no lineage", 1, "NO LINEAGE");
    refs(&without(&full, "binary_sha256"));
    tally.arm("RED   obtained with no digest", 1, "UNEARNED OBTAINED");
    refs(&without(&full, "invocation"));
    tally.arm("RED   obtained with no invocation", 1, "UNEARNED OBTAINED");
    refs(&sub_first(
        &full,
        "(status \"obtained\")",
        "(status \"rumoured\")",
    ));
    tally.arm("RED   an unknown status", 1, "BAD STATUS");
    refs(&sub_first(
        &full,
        "(status \"obtained\")",
        "(status \"not obtained\")",
    ));
    tally.arm("RED   not obtained with no reason", 1, "NO REASON");
    refs(&without(&full, "role"));
    tally.arm("RED   a candidate with no role", 1, "NO ROLE");
    refs(&without(&full, "origin"));
    tally.arm("RED   a candidate citing nothing", 1, "NO ORIGIN");
    refs(&sub_first(&full, "(profile \"p1\")", "(profile \"other\")"));
    tally.arm(
        "RED   dossier names another profile",
        1,
        "REF PROFILE MISMATCH",
    );
    refs(&without(&full, "consequence"));
    tally.arm("RED   an attempt with no consequence", 1, "THIN ATTEMPT");
    refs("(references (profile \"p1\"))");
    tally.arm("RED   a dossier with no candidate", 1, "NO CANDIDATES");
    refs(&format!("{BASE}{DUP_CAND_TAIL}"));
    tally.arm("RED   a duplicate candidate id", 1, "DUPLICATE CANDIDATE");
    refs("not = toml = at = all");
    tally.arm("RED   an unparseable dossier", 1, "UNPARSEABLE");
    let exp = format!("{BASE}{EXP_TAIL}");
    refs(&format!("{exp})"));
    tally.arm("GREEN a complete experiment record", 0, "__CHECKED__ 1");
    // A schema-conforming block cannot receive qualification credit from relationship/artifact/byte checks before full
    // method/policy adequacy.
    let (_, emitted) = prober.probe_with(
        repo,
        vec![
            repo.join("scripts/probe_experiment_verification.py")
                .display()
                .to_string(),
            "--emit-experiment".to_owned(),
        ],
        false,
    );
    let verified_exp = captured(&emitted).to_owned();
    refs(&format!("{BASE}{verified_exp})"));
    tally.arm(
        "RED   a verification block with no current credit stays unqualified",
        1,
        "UNQUALIFIED EXPERIMENT VERIFICATION",
    );
    refs(&format!("{})", without(&exp, "control")));
    tally.arm("RED   agreement with no control", 1, "NO CONTROL");
    refs(&format!("{})", without(&exp, "reproduced")));
    tally.arm(
        "RED   an experiment that never reproduced",
        1,
        "THIN EXPERIMENT",
    );
    refs(&format!("{})", without(&exp, "observed")));
    tally.arm(
        "RED   a difference with nothing observed",
        1,
        "THIN DIFFERENCE",
    );
    // ---- independence (EVD-04) -------------------------------------------------------------
    // Stable experiment identities must resolve to distinct declared candidates.
    refs(&format!(
        "{})",
        sub_first(&exp, "(models \"c1\")", "(models \"c9\")")
    ));
    tally.arm(
        "RED   a single experiment model is undeclared",
        1,
        "UNKNOWN EXPERIMENT MODEL",
    );
    refs(&format!("{exp}{DUP_EXP})"));
    tally.arm(
        "RED   conflicting experiments share an identity",
        1,
        "DUPLICATE EXPERIMENT ID",
    );
    let self_ind = sub_first(IND_ROW, "(pair \"c2\")", "(pair \"c1\")");
    refs(&format!(
        "{}{C2}{self_ind})",
        sub_first(&exp, "(models \"c1\")", "(models \"c1\") (models \"c1\")")
    ));
    tally.arm(
        "RED   repeated experiment models cannot fake a comparison",
        1,
        "REPEATED EXPERIMENT MODEL",
    );
    refs(&format!("{exp}{C2}{self_ind})"));
    tally.arm(
        "RED   independence needs two distinct identities",
        1,
        "BAD PAIR",
    );
    refs(&format!("{exp}{C2}{IND_ROW})"));
    tally.arm("GREEN an independence record parses", 0, "__CHECKED__ 1");
    refs(&format!(
        "{exp}{C2}{})",
        sub_first(IND_ROW, "not-examined", "probably fine")
    ));
    tally.arm("RED   an unknown independence verdict", 1, "BAD VERDICT");
    refs(&format!("{exp}{C2}{})", without(IND_ROW, "(pair \"c2\")")));
    tally.arm("RED   independence claimed of one model", 1, "BAD PAIR");
    refs(&format!("{exp}{C2}{})", without(IND_ROW, "(evidence ")));
    tally.arm(
        "RED   an independence verdict with no examination",
        1,
        "THIN INDEPENDENCE",
    );
    refs(&format!(
        "{exp}{C2}{})",
        sub_first(IND_ROW, "(pair \"c2\")", "(pair \"c9\")")
    ));
    tally.arm(
        "RED   independence names a model that is not a candidate",
        1,
        "UNKNOWN MODEL",
    );
    // ---- 5b: a scalar standing for a configuration declares its scope ------------------------
    refs(&format!("{SC1}{C2}{IND_ROW})"));
    tally.arm("GREEN a scoped scalar", 0, "__CHECKED__ 1");
    refs(&format!("{}{C2}{IND_ROW})", without(SC1, "matched_scope")));
    tally.arm("RED   a scalar with no scope", 1, "UNSCOPED SCALAR");
    refs(&format!(
        "{}{C2}{IND_ROW})",
        without(SC1, "matched_isa_string_source")
    ));
    tally.arm("RED   a scalar with no source", 1, "UNSCOPED SCALAR");
    // an experiment comparing TWO models with no independence record for that pair
    refs(&format!(
        "{}{C2})",
        sub_first(&exp, "(models \"c1\")", "(models \"c1\") (models \"c2\")")
    ));
    tally.arm(
        "RED   two models compared, pair never examined",
        1,
        "UNEXAMINED PAIR",
    );
    let _ = fs::remove_file(&references);
    // ---- the device-shaped dossier (P5-BOARD.2, case sifive-uart-lab-v0) ---------------------
    device();
    device_state();
    tally.arm(
        "GREEN a device-shaped dossier: no xlen, mmio census, earned none",
        0,
        "__CHECKED__ 1",
    );
    device();
    device_state();
    sed_i_bak(&profile, &[("(count_total 2)", "(count_total 3)")]);
    tally.arm(
        "RED   a device scope whose count drifts from its enumeration",
        1,
        "COUNT DRIFT",
    );
    let _ = fs::remove_file(&state);
    let _ = fs::remove_file(bak(&profile));
    let _ = fs::remove_file(bak(&state));
    let _ = fs::remove_dir_all(&t);
    tally.score(
        "GREEN structured verification identity and edge controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_experiment_graph.py")
                .display()
                .to_string()],
        ),
        0,
        "EXPERIMENT-GRAPH: 74 pass / 0 fail",
    );
    tally.score(
        "RED omitted witness budget guard loses four named refusals",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_graph.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "ignore-witness-budget".to_owned(),
            ],
        ),
        1,
        "EXPERIMENT-GRAPH: 70 pass / 4 fail",
    );
    tally.score(
        "RED omitted witness kind guard loses its named refusal",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_graph.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "ignore-witness-kind".to_owned(),
            ],
        ),
        1,
        "EXPERIMENT-GRAPH: 73 pass / 1 fail",
    );
    tally.score(
        "RED omitted control baseline guard loses three named refusals",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_graph.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "ignore-control-baseline".to_owned(),
            ],
        ),
        1,
        "EXPERIMENT-GRAPH: 71 pass / 3 fail",
    );
    tally.score(
        "GREEN structured artifact pin controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_experiment_artifacts.py")
                .display()
                .to_string()],
        ),
        0,
        "EXPERIMENT-ARTIFACTS: 39 pass / 0 fail; descriptors/fixture cleaned",
    );
    tally.score(
        "GREEN bounded authenticated snapshot controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_experiment_snapshots.py")
                .display()
                .to_string()],
        ),
        0,
        "EXPERIMENT-SNAPSHOTS: 24 pass / 0 fail; descriptors/fixture cleaned",
    );
    tally.score(
        "GREEN explicit pin and snapshot read-budget controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_experiment_read_limits.py")
                .display()
                .to_string()],
        ),
        0,
        "EXPERIMENT-READ-LIMITS: 53 pass / 0 fail; descriptors/fixture cleaned",
    );
    tally.score(
        "RED omitted pin limit reads an oversized payload",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_read_limits.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "ignore-pin-limit".to_owned(),
            ],
        ),
        1,
        "READ-LIMIT MISS oversized pin refuses before reading",
    );
    tally.score(
        "RED omitted pin-limit validation opens a path",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_read_limits.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "ignore-invalid-pin-limit".to_owned(),
            ],
        ),
        1,
        "READ-LIMIT MISS invalid pin limit -1",
    );
    tally.score(
        "RED unbounded growth sentinel exceeds snapshot cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_read_limits.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "ignore-sentinel-budget".to_owned(),
            ],
        ),
        1,
        "READ-LIMIT MISS snapshot growth-at-cap consumes at most bound",
    );
    tally.score(
        "RED pin-only path retaining snapshot payload is detected",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_experiment_read_limits.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retain-pin-payload".to_owned(),
            ],
        ),
        1,
        "READ-LIMIT MISS pin-only creates no snapshot payload",
    );
    // P4-SYSTEM.14 a30: finite identity authentication, not execution/qualification.
    // Keep every outer arm literal: DERIVED-COUNTS enumerates call sites.
    tally.score(
        "GREEN normal authenticated reference identity",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_identity.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-IDENTITY: 40 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard pin-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard read-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard raw-schema",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "raw-schema".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 5 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard root-count",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "root-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard candidate-count",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "candidate-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard experiment-free",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "experiment-free".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard identity-equality",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-equality".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 20 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted identity guard optional-presence",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "optional-presence".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 17 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN optimized authenticated reference identity",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-IDENTITY: 40 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard pin-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard read-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard raw-schema",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "raw-schema".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 5 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard root-count",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "root-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard candidate-count",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "candidate-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard experiment-free",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "experiment-free".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard identity-equality",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-equality".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 20 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted identity guard optional-presence",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_identity.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "optional-presence".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IDENTITY: 40 tests / 17 failures / 0 errors; fixtures cleaned",
    );
    // P4-SYSTEM.14 a31: receipt pin/binding is separate from process/method success.
    // Literal arms preserve DERIVED-COUNTS's documented enumeration contract.
    tally.score(
        "GREEN normal authenticated receipt binding",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_receipt.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-RECEIPT: 43 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard schema-tool",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-tool".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard pin-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard read-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard context-counts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard context-edges",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-edges".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard scalar-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "scalar-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard argv-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "argv-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard input-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "input-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard output-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 5 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard output-roles",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-roles".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted receipt guard collector-role",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "collector-role".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN optimized authenticated receipt binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-RECEIPT: 43 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard schema-tool",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-tool".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard pin-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard read-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard context-counts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard context-edges",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-edges".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard scalar-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "scalar-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard argv-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "argv-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard input-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "input-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard output-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 5 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard output-roles",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-roles".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted receipt guard collector-role",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_receipt.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "collector-role".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    // P4-SYSTEM.14 a32: pure execution bindings, never complete method credit.
    tally.score(
        "GREEN normal fixed execution bindings",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_execution.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-EXECUTION: 48 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard budget",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard family-counts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 8 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard reference-pin",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reference-pin".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard run-reference",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "run-reference".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard repeat-edge",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "repeat-edge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard spurious-repeat",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "spurious-repeat".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard output-ownership",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-ownership".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard fixed-argv",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixed-argv".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 44 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard repeat-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "repeat-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard control-expectation",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-expectation".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard control-producer",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-producer".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard reference-inputs",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reference-inputs".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard fixture-count-cleanup",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-count-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted execution guard fixture-argv-cleanup",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-argv-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized fixed execution bindings",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-EXECUTION: 48 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard budget",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard family-counts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 8 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard reference-pin",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reference-pin".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard run-reference",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "run-reference".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard repeat-edge",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "repeat-edge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard spurious-repeat",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "spurious-repeat".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard output-ownership",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-ownership".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard fixed-argv",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixed-argv".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 44 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard repeat-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "repeat-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard control-expectation",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-expectation".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard control-producer",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-producer".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard reference-inputs",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reference-inputs".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard fixture-count-cleanup",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-count-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted execution guard fixture-argv-cleanup",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_execution.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-argv-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only",
    );
    // P4-SYSTEM.14 a33: declared method relations and assertion-safe fixture controls.
    tally.score(
        "GREEN normal declared method relations",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_relations.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-RELATIONS: 42 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard family-counts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard gpr-only",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "gpr-only".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard witness-budget",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "witness-budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard witness-register",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "witness-register".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard control-runs",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-runs".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard control-property",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-property".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard property-count",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "property-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard witness-unique",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "witness-unique".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard control-mutation",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-mutation".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard control-intent",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-intent".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard control-observed",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-observed".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard expected-version",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-version".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard expected-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard expected-consumes",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-consumes".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard expected-common",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-common".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard pair-endpoints",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pair-endpoints".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard pair-sharing",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pair-sharing".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard fixture-count-cleanup",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-count-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted relation guard fixture-version-cleanup",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-version-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized declared method relations",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-RELATIONS: 42 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard family-counts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard gpr-only",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "gpr-only".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard witness-budget",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "witness-budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard witness-register",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "witness-register".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard control-runs",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-runs".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard control-property",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-property".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard property-count",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "property-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard witness-unique",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "witness-unique".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard control-mutation",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-mutation".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard control-intent",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-intent".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard control-observed",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-observed".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard expected-version",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-version".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard expected-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard expected-consumes",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-consumes".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard expected-common",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "expected-common".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard pair-endpoints",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pair-endpoints".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard pair-sharing",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pair-sharing".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard fixture-count-cleanup",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-count-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted relation guard fixture-version-cleanup",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_relations.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "fixture-version-cleanup".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    // P4-SYSTEM.14 a34: authenticate/bind only the manifest, never its leaves.
    tally.score(
        "GREEN normal authenticated manifest binding",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_manifest.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-MANIFEST: 33 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard pin-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard read-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard manifest-codec",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-codec".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 16 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard principal-overlap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "principal-overlap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard path-alias",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "path-alias".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard output-alias",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-alias".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard context-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted manifest guard schema-tool",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-tool".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN optimized authenticated manifest binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-MANIFEST: 33 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard pin-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard read-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard manifest-codec",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-codec".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 16 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard principal-overlap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "principal-overlap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard path-alias",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "path-alias".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard output-alias",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-alias".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard context-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted manifest guard schema-tool",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_manifest.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-tool".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN normal selected dependency leaf",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_leaf.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-LEAF: 50 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard family-counts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard selected-edge",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "selected-edge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard selected-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "selected-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard manifest-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard byte-limit",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "byte-limit".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard read-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard pin-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard payload-consistency",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "payload-consistency".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard document-classification",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "document-classification".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 11 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard no-nesting",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "no-nesting".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard snapshot-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard immutable-result",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-result".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard document-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "document-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard schema-preflight",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-preflight".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted leaf guard schema-before-map",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-before-map".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN optimized selected dependency leaf",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-LEAF: 50 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard family-counts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard selected-edge",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "selected-edge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard selected-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "selected-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard manifest-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard byte-limit",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "byte-limit".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard read-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard pin-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "pin-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard payload-consistency",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "payload-consistency".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard document-classification",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "document-classification".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 11 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard no-nesting",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "no-nesting".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard snapshot-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard immutable-result",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-result".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard document-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "document-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard schema-preflight",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-preflight".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted leaf guard schema-before-map",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_leaf.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-before-map".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    // P4.14 a42d2: opt-in source/image snapshots share the original ledger and rebuild room.
    tally.score(
        "GREEN normal source/image files controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_guest_files.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted flag-type",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "flag-type".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted default",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "default".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted forward",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "forward".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 11 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted retain-source",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retain-source".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 10 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted retain-image",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retain-image".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 9 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted source-cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "source-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted image-cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted reserve",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reserve".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted reserve-debit",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reserve-debit".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 5 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted seed-peak",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-peak".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted snapshot-cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted read-cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted drop-failed-payloads",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "drop-failed-payloads".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted immutable-facts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-facts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted immutable-result",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-result".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal source/image files omitted reservation-counter",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reservation-counter".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN optimized source/image files controls",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted flag-type",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "flag-type".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted default",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "default".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted forward",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "forward".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 11 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted retain-source",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retain-source".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 10 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted retain-image",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retain-image".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 9 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted source-cap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "source-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted image-cap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted reserve",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reserve".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted reserve-debit",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reserve-debit".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 5 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted seed-peak",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-peak".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted snapshot-cap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted read-cap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted drop-failed-payloads",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "drop-failed-payloads".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted immutable-facts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-facts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted immutable-result",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-result".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized source/image files omitted reservation-counter",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_guest_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reservation-counter".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-GUEST-FILES: 24 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    // End P4.14 a42d2.
    tally.score(
        "GREEN normal aggregate declared file set",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_files.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-FILES: 49 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard aggregate-limits",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "aggregate-limits".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 14 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard seed-budget",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard seed-snapshot-peak",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-snapshot-peak".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard snapshot-consistency",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-consistency".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard family-counts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard observation-count",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard execution-counts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "execution-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard child-identities",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "child-identities".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard union-identities",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "union-identities".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard union-membership",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "union-membership".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard principal-identity",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "principal-identity".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard manifest-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard manifest-seed",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-seed".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard observation-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard observation-unique",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-unique".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard observation-size",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-size".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard output-alias",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-alias".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard read-cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard snapshot-cap",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard seed-charge",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-charge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 10 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard failed-charge",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "failed-charge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard stop-after-failure",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "stop-after-failure".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 12 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard drop-failed-payloads",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "drop-failed-payloads".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard transient-first",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "transient-first".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 11 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard transient-release",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "transient-release".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard nested-classification",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "nested-classification".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard immutable-result",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-result".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard immutable-facts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-facts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard context-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard manifest-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 13 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED normal omitted file-set guard legacy-pin",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "legacy-pin".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN optimized aggregate declared file set",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-FILES: 49 tests / 0 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard aggregate-limits",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "aggregate-limits".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 14 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard seed-budget",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard seed-snapshot-peak",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-snapshot-peak".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard snapshot-consistency",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-consistency".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard family-counts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "family-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard observation-count",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard execution-counts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "execution-counts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard child-identities",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "child-identities".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard union-identities",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "union-identities".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard union-membership",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "union-membership".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard principal-identity",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "principal-identity".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard manifest-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard manifest-seed",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-seed".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 8 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard observation-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard observation-unique",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-unique".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard observation-size",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-size".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard output-alias",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "output-alias".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard read-cap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "read-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard snapshot-cap",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-cap".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard seed-charge",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "seed-charge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 10 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard failed-charge",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "failed-charge".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard stop-after-failure",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "stop-after-failure".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 12 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard drop-failed-payloads",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "drop-failed-payloads".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard transient-first",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "transient-first".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 11 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard transient-release",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "transient-release".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard nested-classification",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "nested-classification".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard immutable-result",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-result".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard immutable-facts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "immutable-facts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard context-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard manifest-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 13 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "RED optimized omitted file-set guard legacy-pin",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_files.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "legacy-pin".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned",
    );
    tally.score(
        "GREEN normal frozen byte consumers",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_bytes.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-BYTES: 22 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 19 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-string-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-string-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-context",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-context".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-path",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-path".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-fields",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-fields".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-count",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-canonical",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-canonical".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-parser",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-parser".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard identity-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard receipt-binder",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-binder".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard receipt-context",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-context".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard receipt-parser",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-parser".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 14 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard receipt-claim",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-claim".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted byte guard receipt-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized frozen byte consumers",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-BYTES: 22 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 19 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-string-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-string-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-context",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-context".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-path",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-path".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-fields",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-fields".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-count",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-count".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-canonical",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-canonical".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-parser",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-parser".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard identity-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard receipt-binder",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-binder".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard receipt-context",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-context".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard receipt-parser",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-parser".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 14 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard receipt-claim",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-claim".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted byte guard receipt-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_bytes.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only",
    );
    // P4.14 a42d3b: authenticated source/image composition keeps separate findings.
    tally.score(
        "GREEN normal image evaluation controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_image_evaluation.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted retention",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retention".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted context-budget",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted context-program",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-program".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted context-validation",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-validation".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 10 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted context-refusal",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-refusal".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted source-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "source-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 18 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted image-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 16 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted source-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "source-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted image-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted entry-forward",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "entry-forward".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted image-label",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-label".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted image-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 11 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted image-finding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-finding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal image evaluation omitted comparison-order",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-order".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized image evaluation controls",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted retention",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "retention".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted context-budget",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-budget".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted context-program",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-program".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted context-validation",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-validation".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 10 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted context-refusal",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "context-refusal".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted source-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "source-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 18 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted image-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 16 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted source-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "source-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted image-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted entry-forward",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "entry-forward".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted image-label",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-label".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted image-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 11 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted image-finding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "image-finding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized image evaluation omitted comparison-order",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_image_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-order".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 2 failures / 0 errors; synthetic only",
    );
    // End P4.14 a42d3b.
    tally.score(
        "GREEN normal authenticated byte evaluation",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_evaluation.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-EVALUATION: 42 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard scope",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "scope".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard raw-check",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "raw-check".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard raw-findings",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "raw-findings".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard schema-tool",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-tool".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard candidate-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "candidate-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard relations-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "relations-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard observation-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard receipt-context",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-context".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard manifest-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard manifest-relations",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-relations".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard manifest-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard file-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "file-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard payload-release",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "payload-release".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 27 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard snapshot-account",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-account".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard identity-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard identity-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard receipt-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard receipt-reopen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard process-facts",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "process-facts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard control-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 15 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard comparison-refusal",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-refusal".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard comparison-completeness",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-completeness".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard verdict-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "verdict-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard comparison-status",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard qualification",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "qualification".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 10 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard result-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "result-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard record-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "record-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard authentication-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "authentication-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted evaluation guard receipt-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized authenticated byte evaluation",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-EVALUATION: 42 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard scope",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "scope".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard raw-check",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "raw-check".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard raw-findings",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "raw-findings".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard schema-tool",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "schema-tool".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard candidate-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "candidate-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard relations-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "relations-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard observation-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "observation-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard receipt-context",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-context".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard manifest-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard manifest-relations",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-relations".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard manifest-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "manifest-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard file-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "file-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard payload-release",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "payload-release".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 27 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard snapshot-account",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "snapshot-account".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard identity-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard identity-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "identity-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard receipt-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard receipt-reopen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-reopen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard process-facts",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "process-facts".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard control-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "control-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 15 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard comparison-refusal",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-refusal".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard comparison-completeness",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-completeness".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard verdict-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "verdict-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard comparison-status",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "comparison-status".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard qualification",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "qualification".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 10 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard result-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "result-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard record-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "record-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard authentication-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "authentication-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted evaluation guard receipt-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_evaluation.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "receipt-frozen".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN normal parent-program controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_matched_gpr_program.py")
                .display()
                .to_string()],
        ),
        0,
        "MATCHED-GPR-PROGRAM: 23 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-type",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-type".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-binding",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 13 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-forward",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-forward".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-freeze",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-plain",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-plain".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted parent-program guard program-selection",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized parent-program controls",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "MATCHED-GPR-PROGRAM: 23 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-type",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-type".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-binding",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-binding".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 13 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-forward",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-forward".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 5 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-freeze",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-freeze".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-bound".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-plain",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-plain".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted parent-program guard program-selection",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_matched_gpr_program.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "program-selection".to_owned(),
            ],
        ),
        1,
        "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only",
    );
    // a42g: bounded conservative old/new graph impact; synthetic projections only.
    tally.score(
        "GREEN normal change-impact controls",
        prober.probe(
            repo,
            vec![repo
                .join("scripts/probe_change_impact.py")
                .display()
                .to_string()],
        ),
        0,
        "CHANGE-IMPACT: 34 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard content-seeds",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "content-seeds".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 17 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard edge-seeds",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-seeds".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard path-seeds",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "path-seeds".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard unmapped-insertion",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "unmapped-insertion".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard unmapped-broad",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "unmapped-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard uncertain-broad",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "uncertain-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard scope-broad",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "scope-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard unknown-broad",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "unknown-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard shared-broad",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "shared-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 16 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard broad-expansion",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "broad-expansion".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 18 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard reverse-closure",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reverse-closure".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard node-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "node-bound".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard edge-bound",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-bound".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard plain-bool",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "plain-bool".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard node-unique",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "node-unique".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard edge-unique",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-unique".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard edge-scope",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-scope".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED normal omitted change-impact guard result-frozen",
        prober.probe(
            repo,
            vec![
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "result-frozen".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "GREEN optimized change-impact controls",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
            ],
        ),
        0,
        "CHANGE-IMPACT: 34 tests / 0 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard content-seeds",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "content-seeds".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 17 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard edge-seeds",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-seeds".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 4 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard path-seeds",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "path-seeds".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 6 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard unmapped-insertion",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "unmapped-insertion".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard unmapped-broad",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "unmapped-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard uncertain-broad",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "uncertain-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard scope-broad",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "scope-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard unknown-broad",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "unknown-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard shared-broad",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "shared-broad".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 16 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard broad-expansion",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "broad-expansion".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 18 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard reverse-closure",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "reverse-closure".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 7 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard node-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "node-bound".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard edge-bound",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-bound".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard plain-bool",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "plain-bool".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard node-unique",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "node-unique".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard edge-unique",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-unique".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard edge-scope",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "edge-scope".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    tally.score(
        "RED optimized omitted change-impact guard result-frozen",
        prober.probe(
            repo,
            vec![
                "-O".to_owned(),
                repo.join("scripts/probe_change_impact.py")
                    .display()
                    .to_string(),
                "--mutation".to_owned(),
                "result-frozen".to_owned(),
            ],
        ),
        1,
        "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only",
    );
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec![repo
            .join("scripts/probe_matched_gpr_input_review.py")
            .display()
            .to_string()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(
            &format!("GREEN {mode} reviewed-input controls"),
            prober.probe(repo, argv.clone()),
            0,
            "MATCHED-GPR-INPUT-REVIEW: 20 tests / 0 failures / 0 errors; synthetic only",
        );
        for (mutation, losses) in [
            ("missing", "2"),
            ("unreviewed", "2"),
            ("changed", "4"),
            ("profile", "2"),
            ("experiment", "2"),
            ("bindings-copy", "2"),
            ("input-bound", "2"),
            ("input-type", "2"),
            ("id-unique", "1"),
            ("path-unique", "1"),
            ("result-frozen", "1"),
            ("review-frozen", "2"),
            ("declared-validation", "1"),
            ("plan-binding", "3"),
            ("review-freeze", "4"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED {mode} omitted input-review guard {mutation}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-INPUT-REVIEW: 20 tests / {losses} failures / 0 errors; synthetic only"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec![repo
            .join("scripts/probe_matched_gpr_impact.py")
            .display()
            .to_string()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(
            &format!("GREEN {mode} retained-input impact controls"),
            prober.probe(repo, argv.clone()),
            0,
            "MATCHED-GPR-IMPACT: 24 tests / 0 failures / 0 errors; synthetic only",
        );
        for (mutation, losses) in [
            ("role-fingerprint", "2"),
            ("digest-fingerprint", "2"),
            ("profile", "1"),
            ("experiment", "2"),
            ("input-path", "3"),
            ("input-fingerprint", "2"),
            ("input-kind", "2"),
            ("input-profile", "1"),
            ("old-evidence", "1"),
            ("evidence-kind", "1"),
            ("reachability", "1"),
            ("graph-copy", "2"),
            ("node-envelope", "1"),
            ("edge-envelope", "1"),
            ("profile-envelope", "1"),
            ("result-frozen", "1"),
            ("context-frozen", "1"),
            ("binding-status", "1"),
            ("stale-status", "1"),
            ("current-review", "1"),
            ("finding", "4"),
            ("frozen-context", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(
                &format!("RED {mode} omitted impact guard {mutation}"),
                prober.probe(repo, mutated),
                1,
                &format!(
                    "MATCHED-GPR-IMPACT: 24 tests / {losses} failures / 0 errors; synthetic only"
                ),
            );
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> =
            vec!["scripts/probe_matched_gpr_value_evaluation.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(
            &format!("GREEN source-value evaluation {mode}"),
            prober.probe(repo, argv.clone()),
            0,
            "MATCHED-GPR-VALUE-EVALUATION: 19 tests / 0 failures / 0 errors; synthetic only",
        );
        for (mutation, losses) in [
            ("source-values-selection", "10"),
            ("baseline-values-selection", "10"),
            ("source-values-reopen", "1"),
            ("budget-forward", "2"),
            ("witness-forward", "9"),
            ("program-forward", "12"),
            ("source-result-shape", "4"),
            ("source-binding-shape", "3"),
            ("source-context-binding", "7"),
            ("source-status", "3"),
            ("unsupported-credit", "1"),
            ("source-finding", "13"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED source-value evaluation {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-VALUE-EVALUATION: 19 tests / {losses} failures / 0 errors; synthetic only"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_expected_author.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(
            &format!("GREEN reviewed expected author {mode}"),
            prober.probe(repo, argv.clone()),
            0,
            "MATCHED-GPR-EXPECTED-AUTHOR: 21 tests / 0 failures / 0 errors; synthetic only",
        );
        for (mutation, losses) in [
            ("authority-shape", "1"),
            ("authority-scope", "6"),
            ("authority-copy", "4"),
            ("author-selection", "3"),
            ("review-route", "3"),
            ("inventory-binding", "5"),
            ("child-membership", "1"),
            ("principal-binding", "3"),
            ("producer-version", "4"),
            ("source-consumption", "1"),
            ("manifest-consumption", "1"),
            ("snapshot-author", "3"),
            ("snapshot-source", "1"),
            ("snapshot-budget", "4"),
            ("frozen-results", "3"),
            ("metadata-finding", "4"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED reviewed expected author {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-EXPECTED-AUTHOR: 21 tests / {losses} failures / 0 errors; synthetic only"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> =
            vec!["scripts/probe_matched_gpr_author_evaluation.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(
            &format!("GREEN expected-author evaluation {mode}"),
            prober.probe(repo, argv.clone()),
            0,
            "MATCHED-GPR-AUTHOR-EVALUATION: 19 tests / 0 failures / 0 errors; synthetic only",
        );
        for (mutation, losses) in [
            ("author-freeze", "6"),
            ("current-inventory", "12"),
            ("review-agreement", "1"),
            ("frozen-scope", "1"),
            ("author-scope", "12"),
            ("manifest-reopen", "2"),
            ("derivation-selection", "1"),
            ("author-order", "1"),
            ("author-result-shape", "8"),
            ("author-fact-binding", "9"),
            ("author-status", "3"),
            ("author-finding", "12"),
            ("unsupported-credit", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED expected-author evaluation {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-AUTHOR-EVALUATION: 19 tests / {losses} failures / 0 errors; synthetic only"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_property.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN finite source property {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-PROPERTY: 34 tests / 0 failures / 0 errors; synthetic metadata, finite source witnesses only");
        for (mutation, losses) in [
            ("publication-authority", "36"),
            ("record-roundtrip", "1"),
            ("authority-string-bound", "1"),
            ("authority-byte-bound", "1"),
            ("context-scope", "1"),
            ("authority-shape", "1"),
            ("claim-count", "1"),
            ("claim-identity", "1"),
            ("claim-witness", "1"),
            ("control-claim", "2"),
            ("claim-binding", "13"),
            ("semantic-authority", "9"),
            ("relation-binding", "6"),
            ("normative-pin", "6"),
            ("guest-source", "1"),
            ("baseline-binding", "1"),
            ("witness-value", "3"),
            ("budget-binding", "2"),
            ("source-identity", "5"),
            ("reviewed-words", "8"),
            ("claim-values", "3"),
            ("authority-node-bound", "1"),
            ("authority-depth-bound", "1"),
            ("derived-status", "36"),
            ("derived-links", "1"),
            ("requirement-meaning", "6"),
            ("obligation-meaning", "4"),
            ("context-copy", "7"),
            ("claim-copy", "6"),
            ("source-fact-copy", "1"),
            ("authority-fact-copy", "1"),
            ("case-selection", "2"),
            ("source-unsupported", "1"),
            ("frozen-results", "8"),
            ("finite-finding", "11"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED finite source property {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-PROPERTY: 34 tests / {losses} failures / 0 errors; synthetic metadata, finite source witnesses only"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> =
            vec!["scripts/probe_matched_gpr_property_evaluation.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN finite-property evaluation {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-PROPERTY-EVALUATION: 25 tests / 0 failures / 0 errors; actual retained excerpt, synthetic observations, no capture credit");
        for (mutation, losses) in [
            ("author-prerequisite", "1"),
            ("obligation-bound", "1"),
            ("actual-statement", "2"),
            ("actual-requirement", "1"),
            ("actual-obligations", "1"),
            ("actual-program", "1"),
            ("property-order", "1"),
            ("property-finding", "17"),
            ("property-status", "6"),
            ("unsupported-credit", "2"),
            ("context-freeze", "7"),
            ("property-result-shape", "18"),
            ("property-fact-binding", "19"),
            ("actual-context-binding", "1"),
            ("case-pass-through", "1"),
            ("control-value", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED finite-property evaluation {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-PROPERTY-EVALUATION: 25 tests / {losses} failures / 0 errors; actual retained excerpt, synthetic observations, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_collector.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN fresh process collector {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-COLLECTOR: 25 tests / 0 failures / 0 errors; synthetic child processes, no Sail capture credit");
        for (mutation, losses) in [
            ("physical-input-alias", "1"),
            ("physical-output-alias", "1"),
            ("exclusive-reservations", "1"),
            ("observation-mode", "9"),
            ("output-finding", "1"),
            ("request-freeze", "1"),
            ("owned-clear", "14"),
            ("pre-pins", "9"),
            ("post-pins", "2"),
            ("fixed-argv", "1"),
            ("output-alias", "1"),
            ("selected-outputs", "1"),
            ("special-output", "1"),
            ("nested-git", "2"),
            ("stream-bound", "1"),
            ("hard-file-bound", "1"),
            ("group-cleanup", "1"),
            ("deadline", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED fresh process collector {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-COLLECTOR: 25 tests / {losses} failures / 0 errors; synthetic child processes, no Sail capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_publication.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN fresh receipt publication {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-PUBLICATION: 23 tests / 0 failures / 0 errors; synthetic process receipts, qualification closed");
        for (mutation, losses) in [
            ("request-freeze", "2"),
            ("host-freeze", "1"),
            ("actual-exit", "2"),
            ("receipt-bound", "1"),
            ("byte-binding", "2"),
            ("pre-outputs", "1"),
            ("post-outputs", "2"),
            ("exclusive-write", "1"),
            ("partial-cleanup", "4"),
            ("cleanup-identity", "1"),
            ("receipt-pin", "2"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED fresh receipt publication {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-PUBLICATION: 23 tests / {losses} failures / 0 errors; synthetic process receipts, qualification closed"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_unit_collector.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN bounded unit collection {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-UNIT-COLLECTOR: 26 tests / 0 failures / 0 errors; synthetic unit processes, qualification closed");
        for (mutation, losses) in [
            ("unit-freeze", "1"),
            ("unit-shared-limit", "2"),
            ("unit-charge", "3"),
            ("unit-accounting", "2"),
            ("unit-output-binding", "1"),
            ("unit-unique-pid", "1"),
            ("unit-failed-exit", "2"),
            ("unit-existing-output", "12"),
            ("unit-exclusive-reservations", "1"),
            ("unit-cleanup-identity", "1"),
            ("unit-cleanup-boundary", "1"),
            ("pin-charge", "4"),
            ("observation-charge", "4"),
            ("publication-process-charge", "9"),
            ("publication-read-charge", "3"),
            ("failed-pin-charge", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED bounded unit collection {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-UNIT-COLLECTOR: 26 tests / {losses} failures / 0 errors; synthetic unit processes, qualification closed"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_capture_review.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN DIV dependency review {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-CAPTURE-REVIEW: 31 tests / 0 failures / 0 errors; synthetic population controls, no capture credit");
        for (mutation, losses) in [
            ("module-population", "2"),
            ("dynamic-import", "2"),
            ("external-import", "1"),
            ("data-population", "2"),
            ("child-bound", "1"),
            ("symlink", "2"),
            ("git-boundary", "1"),
            ("file-bound", "1"),
            ("aggregate-bound", "1"),
            ("byte-recheck", "2"),
            ("retained-identity", "3"),
            ("publication-authority", "2"),
            ("retained-pin", "1"),
            ("authority-declaration", "1"),
            ("authority-preopen", "1"),
            ("authority-readonly", "1"),
            ("authority-view-pin", "1"),
            ("authority-process", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED DIV dependency review {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("DIV-CAPTURE-REVIEW: 31 tests / {losses} failures / 0 errors; synthetic population controls, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_statement_retention.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN DIV statement retention {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-STATEMENT-RETENTION: 20 tests / 0 failures / 0 errors; synthetic curation controls, no capture credit");
        for (mutation, losses) in [
            ("input-pins", "2"),
            ("input-bounds", "2"),
            ("licence-statement", "1"),
            ("unique-statement", "1"),
            ("closing-span", "1"),
            ("span-bound", "1"),
            ("retained-bound", "1"),
            ("exact-span", "4"),
            ("retained-pin", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED DIV statement retention {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("DIV-STATEMENT-RETENTION: 20 tests / {losses} failures / 0 errors; synthetic curation controls, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec![
            "-B".to_owned(),
            "scripts/probe_m_statement_retention.py".to_owned(),
        ];
        if optimized {
            argv.insert(1, "-O".to_owned());
        }
        tally.score(&format!("GREEN M statement retention {mode}"), prober.probe(repo, argv.clone()), 0, "M-STATEMENT-RETENTION: 20 tests / 0 failures / 0 errors; synthetic curation controls, no capture credit");
        for (mutation, losses) in [
            ("input-pins", "1"),
            ("licence-statement", "1"),
            ("unique-statement", "1"),
            ("closing-span", "1"),
            ("span-markup", "3"),
            ("table-markup", "4"),
            ("style-shape", "1"),
            ("table-caption", "1"),
            ("retained-bound", "1"),
            ("retained-pin", "2"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED M statement retention {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("M-STATEMENT-RETENTION: 20 tests / {losses} failures / 0 errors; synthetic curation controls, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_read_allowance.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN delegated read allowance {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-READ-ALLOWANCE: 15 tests / 0 failures / 0 errors; actual bounded reads, synthetic observations, no capture credit");
        for (mutation, losses) in [
            ("evaluation-type", "6"),
            ("evaluation-domain", "3"),
            ("manifest-type", "6"),
            ("manifest-domain", "3"),
            ("initial-allowance", "3"),
            ("manifest-envelope", "2"),
            ("file-allowance", "4"),
            ("seed-double-charge", "2"),
            ("manifest-read-cap", "5"),
            ("manifest-extra-byte", "4"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED delegated read allowance {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-READ-ALLOWANCE: 15 tests / {losses} failures / 0 errors; actual bounded reads, synthetic observations, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_reference_identity_emission.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN selected identity emission {mode}"), prober.probe(repo, argv.clone()), 0, "REFERENCE-IDENTITY-EMISSION: 19 tests / 0 failures / 0 errors; synthetic descriptor metadata, no capture credit");
        for (mutation, losses) in [
            ("context-type", "2"),
            ("context-shape", "2"),
            ("unknown-field", "1"),
            ("host-shape", "1"),
            ("metadata-type", "16"),
            ("text-bound", "2"),
            ("path-bound", "3"),
            ("canonical-fields", "6"),
            ("host-freeze", "1"),
            ("optional-emission", "2"),
            ("encoded-bound", "2"),
            ("round-trip", "2"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED selected identity emission {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("REFERENCE-IDENTITY-EMISSION: 19 tests / {losses} failures / 0 errors; synthetic descriptor metadata, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_matched_gpr_unit_evaluation.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN combined collection/evaluation {mode}"), prober.probe(repo, argv.clone()), 0, "MATCHED-GPR-UNIT-EVALUATION: 30 tests / 0 failures / 0 errors; actual synthetic processes/read bytes, qualification closed");
        for (mutation, losses) in [
            ("planned-bound", "2"),
            ("scope-envelope", "2"),
            ("scope-freeze", "1"),
            ("raw-schema", "1"),
            ("candidate-freeze", "1"),
            ("author-freeze", "3"),
            ("property-freeze", "1"),
            ("impact-freeze", "1"),
            ("collection-limit", "2"),
            ("collection-debit", "5"),
            ("captured-pid", "1"),
            ("captured-output", "1"),
            ("captured-charge", "2"),
            ("measured-bound", "1"),
            ("evaluation-limit", "2"),
            ("evaluation-debit", "2"),
            ("seed-accounting", "1"),
            ("evaluation-envelope", "1"),
            ("snapshot-envelope", "1"),
            ("failed-collection-refund", "3"),
            ("failed-evaluation-refund", "2"),
            ("attach-invalid-collection", "15"),
            ("attach-invalid-evaluation", "13"),
            ("structured-comments", "2"),
            ("unsupported-finding", "1"),
            ("case-forward", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED combined collection/evaluation {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("MATCHED-GPR-UNIT-EVALUATION: 30 tests / {losses} failures / 0 errors; actual synthetic processes/read bytes, qualification closed"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_retained_sail_identity.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN published Sail identity {mode}"), prober.probe(repo, argv.clone()), 0, "RETAINED-SAIL-IDENTITY: 11 tests / 0 failures / 0 errors; published descriptor, offline, no capture credit");
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_capture_inputs.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN prepared DIV capture inputs {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors; prepared artifacts of every reviewed case, no reference process or capture credit");
        let mut mutated = argv.clone();
        mutated.extend(["--mutation".to_owned(), "actual-layout".to_owned()]);
        tally.score(&format!("RED omitted actual DIV layout {mode}"), prober.probe(repo, mutated), 1, "DIV-CAPTURE-INPUTS: 34 tests / 6 failures / 0 errors; prepared artifacts of every reviewed case, no reference process or capture credit");
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_authorities.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(
            &format!("GREEN current DIV authorities {mode}"),
            prober.probe(repo, argv.clone()),
            0,
            "DIV-AUTHORITIES: 18 tests / 0 failures / 0 errors; current views, no capture credit",
        );
        for mutation in ["raw-validation", "registry-binding", "authority-binding"] {
            let losses = if mutation == "registry-binding" { 1 } else { 3 };
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted DIV authority {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("DIV-AUTHORITIES: 18 tests / {losses} failures / 0 errors; current views, no capture credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_command.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN composed DIV command {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-COMMAND: 19 tests / 0 failures / 0 errors; synthetic processes, no Sail or qualification");
        for (mutation, losses) in [
            ("native-declarations", "6"),
            ("authority-stability", "1"),
            ("retained-identity", "1"),
            ("planned-schema", "1"),
            ("author-delegation", "2"),
            ("impact-delegation", "1"),
            ("property-delegation", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted DIV command {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("DIV-COMMAND: 19 tests / {losses} failures / 0 errors; synthetic processes, no Sail or qualification"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_capture_retention.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN capture retention {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-CAPTURE-RETENTION: 11 tests / 0 failures / 0 errors; synthetic processes, no Sail or qualification");
        for (mutation, losses) in [
            ("outputs-absent", "1"),
            ("declaration-regeneration", "1"),
            ("binary-identity", "1"),
            ("object-id", "2"),
            ("exclusive-publish", "1"),
            ("receipt-qualification", "1"),
            ("measured-pin", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted capture retention {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("DIV-CAPTURE-RETENTION: 11 tests / {losses} failures / 0 errors; synthetic processes, no Sail or qualification"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["scripts/probe_div_method.py".to_owned()];
        if optimized {
            argv.insert(0, "-O".to_owned());
        }
        tally.score(&format!("GREEN retained DIV method {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-METHOD: 21 tests / 0 failures / 0 errors; retained finite method, no Sail or policy credit");
        for (mutation, losses) in [
            ("declaration-binding", "4"),
            ("capture-origin", "1"),
            ("record-binding", "4"),
            ("influence-selection", "2"),
            ("finding-completeness", "2"),
            ("evaluation-selection", "1"),
            ("artifact-selection", "2"),
            ("typed-findings", "1"),
            ("shared-budget", "3"),
            ("evaluation-accounting", "4"),
            ("checker-census", "1"),
            ("checker-recheck", "1"),
            ("runtime-root", "1"),
            ("native-envelope", "1"),
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted DIV method {mutation} {mode}"), prober.probe(repo, mutated), 1, &format!("DIV-METHOD: 1 tests / {losses} failures / 0 errors; retained finite method, no Sail or policy credit"));
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec![
            "-B".to_owned(),
            "scripts/probe_requirement_status.py".to_owned(),
        ];
        if optimized {
            argv.insert(1, "-O".to_owned());
        }
        tally.score(&format!("GREEN requirement status derivation {mode}"), prober.probe(repo, argv.clone()), 0, "REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors; derivation only, no qualification credit");
        for mutation in [
            "credit-pending",
            "ignore-drift",
            "skip-supersession",
            "unresolved-closes",
            "argument-optional",
            "unknown-case-credit",
            "qualification-word",
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted requirement status {mutation} {mode}"), prober.probe(repo, mutated), 1, "REQUIREMENT-STATUS-PROBE: 1 tests / 1 failures / 0 errors; derivation only, no qualification credit");
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec!["-B".to_owned(), "scripts/probe_div_policy.py".to_owned()];
        if optimized {
            argv.insert(1, "-O".to_owned());
        }
        tally.score(&format!("GREEN policy legs measured {mode}"), prober.probe(repo, argv.clone()), 0, "DIV-POLICY-PROBE: 25 tests / 0 failures / 0 errors; measurement only, no qualification credit");
        for mutation in [
            "credit-pending",
            "trust-receipt",
            "infer-feature",
            "any-control",
            "coverage-optional",
            "lock-stale",
            "first-property",
            "credit-any",
        ] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted policy legs {mutation} {mode}"), prober.probe(repo, mutated), 1, "DIV-POLICY-PROBE: 1 tests / 1 failures / 0 errors; measurement only, no qualification credit");
        }
    }
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        let mut argv: Vec<String> = vec![
            "-B".to_owned(),
            "scripts/probe_dossier_qualification.py".to_owned(),
        ];
        if optimized {
            argv.insert(1, "-O".to_owned());
        }
        tally.score(&format!("GREEN dossier qualification through a current credit {mode}"), prober.probe(repo, argv.clone()), 0, "DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors; the credit decides, never the record");
        for mutation in ["credit-any", "mirror-any", "id-any"] {
            let mut mutated = argv.clone();
            mutated.extend(["--mutation".to_owned(), mutation.to_owned()]);
            tally.score(&format!("RED omitted dossier qualification {mutation} {mode}"), prober.probe(repo, mutated), 1, "DOSSIER-QUALIFICATION-PROBE: 1 tests / 1 failures / 0 errors; the credit decides, never the record");
        }
    }
    let (pass, fail) = (tally.pass, tally.fail);
    report.out(&format!(
        "PROFILE-CONSISTENCY --self-test: {pass} pass / {fail} fail"
    ));
    fail == 0
}

/// The controls with the XTASK.8 prefetch: a recording pass, the recorded argv run in parallel by
/// `scripts/doctrine_prefetch.py`, then the scoring pass answering from the record. `PROFILE_CONSISTENCY_PREFETCH=0`
/// runs every probe live; `PROFILE_CONSISTENCY_RECORD_ARGV=<file>` records to that file and scores nothing.
fn self_test_prefetched(repo: &Path, report: &mut Report) -> bool {
    if let Some(path) = std::env::var_os("PROFILE_CONSISTENCY_RECORD_ARGV") {
        return self_test(repo, report, &mut Prober::RecordTo(PathBuf::from(path)));
    }
    let wanted = !matches!(
        std::env::var("PROFILE_CONSISTENCY_PREFETCH").as_deref(),
        Ok("0")
    );
    if !(wanted && repo.join("scripts/doctrine_prefetch.py").is_file()) {
        return self_test(repo, report, &mut Prober::Live);
    }
    let Ok(base) = scratch(repo, "target/doctrine-selftest", "prefetch") else {
        return self_test(repo, report, &mut Prober::Live);
    };
    let dir = base.join("prefetch");
    let argv_file = base.join("prefetch.argv");
    let _ = fs::create_dir_all(&dir);
    // pass 1: record — every probe argv, nothing scored, the output discarded
    let mut recorder = Prober::Record(Vec::new());
    let _ = self_test(repo, &mut Report::Null, &mut recorder);
    let Prober::Record(seen) = recorder else {
        unreachable!()
    };
    let lines: String = seen
        .iter()
        .map(|a| format!("{}\n", a.join("\u{1f}")))
        .collect();
    let _ = fs::write(&argv_file, lines);
    // pass 2: the recorded argv in parallel; a failed prefetch is no prefetch — every arm runs live
    let prefetched = Command::new("python3")
        .arg("-B")
        .arg(repo.join("scripts/doctrine_prefetch.py"))
        .arg(&argv_file)
        .arg(&dir)
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|s| s.success());
    let mut prober = if prefetched {
        Prober::Answer {
            dir,
            misses: std::env::var_os("PROFILE_CONSISTENCY_PREFETCH_MISSES").map(PathBuf::from),
        }
    } else {
        let _ = fs::remove_dir_all(&base);
        Prober::Live
    };
    // pass 3: the controls for real, answered from the record
    let ok = self_test(repo, report, &mut prober);
    let _ = fs::remove_dir_all(&base);
    ok
}

/// One of the four tools the real run consults before the dossiers: `$(python3 [-B] scripts/<tool> …  2>&1)`.
fn tool(root: &Path, dash_b: bool, args: &[&str]) -> (i32, String) {
    let mut argv: Vec<String> = Vec::new();
    if dash_b {
        argv.push("-B".to_owned());
    }
    argv.extend(args.iter().map(|a| (*a).to_owned()));
    let (rc, raw) = live(root, &argv, true);
    (rc, captured(&raw).to_owned())
}

/// `printf '%s\n' "$text" | sed 's/^/  /'` on stderr.
fn indented(text: &str) {
    for line in text.split('\n') {
        eprintln!("  {line}");
    }
}

/// `grep -n -A3 "self-test MISS" <log> | head -40 | sed 's/^/  /'`: the MISS lines with three lines of context each,
/// numbered, `--` between separated groups, the first forty lines.
fn miss_excerpt(log: &str) -> Vec<String> {
    let lines: Vec<&str> = log.lines().collect();
    let mut out: Vec<String> = Vec::new();
    let mut printed_through: Option<usize> = None;
    for (i, line) in lines.iter().enumerate() {
        if !line.contains("self-test MISS") {
            continue;
        }
        let end = (i + 3).min(lines.len() - 1);
        let from = match printed_through {
            Some(last) if i <= last + 1 => last + 1,
            Some(_) => {
                out.push("--".to_owned());
                i
            }
            None => i,
        };
        for (j, text) in lines.iter().enumerate().take(end + 1).skip(from) {
            let mark = if text.contains("self-test MISS") {
                ':'
            } else {
                '-'
            };
            out.push(format!("{}{mark}{text}", j + 1));
        }
        printed_through = Some(end);
    }
    out.truncate(40);
    out.into_iter().map(|l| format!("  {l}")).collect()
}

/// `cargo xtask check-profile-consistency [--self-test|--csr-cross <profile-dir> <state>]`: the shell driver's verdict
/// lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!(
            "PROFILE-CONSISTENCY: REFUSED — python3 is not on PATH; this check cannot judge."
        );
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        let mut report = Report::Terminal;
        return if self_test_prefetched(root, &mut report) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // The curated source is tracked: its pin check must not depend on acquired pages.
    let (rc, out) = tool(
        root,
        false,
        &["scripts/retain_div_statement.py", "--verify"],
    );
    if rc != 0 {
        eprintln!("PROFILE-CONSISTENCY: retained DIV statement refused: {out}");
        return ExitCode::from(1);
    }
    // a42bb: the other eleven M statements and Table 1, authenticated the same way.
    let (rc, out) = tool(root, true, &["scripts/retain_m_statements.py", "--verify"]);
    if rc != 0 {
        eprintln!("PROFILE-CONSISTENCY: retained M statements refused: {out}");
        return ExitCode::from(1);
    }
    // P4-SYSTEM.14 a42ap: every policy-declaring profile's recorded requirement statuses equal their derivation.
    let (rc, out) = tool(root, true, &["scripts/requirement_status.py"]);
    if rc != 0 {
        eprintln!("PROFILE-CONSISTENCY: a recorded requirement status drifts from its derivation, or the graph refuses.");
        indented(&out);
        eprintln!("  The GRAPH is authoritative: change the evidence or the catalogue record, never the status alone.");
        return ExitCode::from(u8::try_from(rc).unwrap_or(1));
    }
    // P4-SYSTEM.14 a42aq: the retained DIV case's policy legs are measured from its own bytes.
    let (rc, out) = tool(root, true, &["scripts/review_div_policy.py"]);
    if rc != 0 {
        eprintln!("PROFILE-CONSISTENCY: the retained case's policy legs refuse its receipt, or cannot be measured.");
        indented(&out);
        eprintln!("  The LEGS are measured from declared bytes: predeclare and capture, never relabel a receipt.");
        return ExitCode::from(u8::try_from(rc).unwrap_or(1));
    }
    // P4-SYSTEM.2 slice (c1): probe the csr-set rule against a staged state document at a scratch path.
    if args.first().is_some_and(|arg| arg == "--csr-cross") {
        let mut command = Command::new("python3");
        command
            .arg("-")
            .args(args)
            .current_dir(root)
            .stdin(Stdio::piped());
        let Ok(mut child) = command.spawn() else {
            return ExitCode::from(2);
        };
        if let Some(mut stdin) = child.stdin.take() {
            let _ = stdin.write_all(JUDGE.as_bytes());
        }
        let code = child.wait().ok().and_then(|s| s.code()).unwrap_or(1);
        return ExitCode::from(u8::try_from(code).unwrap_or(1));
    }
    if !root.join("profiles").is_dir() {
        println!("PROFILE-CONSISTENCY: ok (no profiles/ yet)");
        return ExitCode::SUCCESS;
    }
    // The self-test's output is KEPT (a42ax, 2026-10-23): the MISS lines name the failing arm.
    let log_path = root.join(SELF_TEST_LOG);
    let _ = fs::create_dir_all(root.join("target"));
    let Ok(log) = fs::File::create(&log_path) else {
        return ExitCode::from(2);
    };
    let mut report = Report::Log(log);
    if !self_test_prefetched(root, &mut report) {
        drop(report);
        eprintln!(
            "PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed)."
        );
        for line in miss_excerpt(&fs::read_to_string(&log_path).unwrap_or_default()) {
            eprintln!("{line}");
        }
        eprintln!(
            "  the self-test's complete output is kept at target/profile-consistency-selftest.log"
        );
        return ExitCode::from(2);
    }
    drop(report);
    // `out="$(check_profiles profiles)"`: stdout captured, stderr through.
    let (rc, raw) = check_profiles(root, &[OsStr::new("profiles")], false);
    let out = captured(&raw);
    let count = out
        .lines()
        .filter_map(|line| line.strip_prefix("__CHECKED__ "))
        .collect::<Vec<_>>()
        .join("\n");
    let body = out
        .lines()
        .filter(|line| !line.starts_with("__CHECKED__ "))
        .collect::<Vec<_>>()
        .join("\n");
    let body = captured(&body);
    if rc != 0 {
        eprintln!("PROFILE-CONSISTENCY: a profile dossier contradicts itself or cites nothing.");
        indented(body);
        eprintln!(
            "  The SOURCE is authoritative: fix the enumeration, the citation or the evidence —"
        );
        eprintln!("  never the summary alone to make the two agree.");
        return ExitCode::from(1);
    }
    let count = if count.is_empty() {
        "0"
    } else {
        count.as_str()
    };
    println!("PROFILE-CONSISTENCY: ok ({count} profile dossier(s) internally consistent)");
    ExitCode::SUCCESS
}
