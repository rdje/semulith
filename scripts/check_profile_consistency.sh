#!/usr/bin/env bash
# scripts/check_profile_consistency.sh — PROFILE-CONSISTENCY (project doctrine).
#
# A profile dossier is a set of claims about a specification. Two of them can go wrong quietly:
#
#   1. A DECLARED COUNT drifts from the ENUMERATION it summarises. `count_total = 52` beside a
#      list of 51 mnemonics is a contract number that is simply false, and nothing about the
#      file's appearance reveals it. `CLAIM_VERIFICATION.md` §5B: a constant that is a function
#      of the repository is derived or gated, never carried.
#   2. A DECISION loses its authority or its source. The whole point of the `authority` field is
#      that a `laboratory` policy must never be mistaken for an `architecture` rule — an
#      unsourced decision is exactly how that mistake becomes permanent.
#   3. An EMPTY `hidden_state` list in `state.sexp` is a universal claim over a set — "nothing
#      else can influence a future observation" — and it is false the moment one such thing
#      exists. So an empty list must be backed by a CENSUS that enumerates what was considered
#      and found absent. This is `GAP-CLAIM-CENSUS` applied to data rather than to prose: an
#      unearned "none" is indistinguishable from a "none" nobody looked for.
#   4. `state.sexp` and `profile.sexp` must AGREE. Two files describing the same processor is
#      the cheapest place for a contradiction to hide.
#   5. `references.sexp` records REFERENCE CANDIDATES, and a candidate list is the easiest
#      document in a project to fill in from reputation. `SRC-03` forbids recording availability
#      that has not been established, so an `obtained` candidate must name the binary AND its
#      digest AND how it is invoked. ⭐ And every candidate must carry a `lineage` field, because
#      `EVD-04`'s question — do two comparators share semantic ancestry? — is precisely the field
#      that gets skipped when three models are sitting there apparently agreeing.
#   6. An EXPERIMENT that claims agreement must record the CONTROL that was observed failing.
#      ⭐ This is `TOOLBOX.md`'s rule one level up: a gate never seen RED is not known to work,
#      and a *comparison* never seen to diverge is not known to detect divergence.
#      Experiment IDs are unique and every compared model names a distinct candidate. An
#      experiment row saying "the two models agree" with no control is the most convincing
#      wrong record a project can hold, because it is true and worthless at the same time.
#   7. Every PAIR of models an experiment compares must have an INDEPENDENCE row. ⭐ This is the
#      rule with real teeth, and it is `EVD-04` made mechanical: two tools with different names
#      are not two opinions, and the moment a project records "model A and model B agree" it has
#      taken a position on their independence whether or not it has looked. An unexamined pair
#      reads exactly like an independent one, so the gate requires the row to EXIST — it does not
#      require the verdict to be favourable. `not-examined` is a legal, honest answer; silence
#      is not.
#
# ⚠️ HONEST LIMIT, stated rather than implied: this proves the file is INTERNALLY consistent and
# that every decision cites something. It cannot check the citation against the specification —
# that is a human reading, and `scripts/fetch_sources.sh` exists to make the artifact being read
# identifiable.
#
# ⛔ SINCE `SOT-FORMAT.4` the dossier is S-expression, read through scripts/dossier_sexp.py —
# the single owner of the mapping. The gate receives exactly the dicts `tomllib`/`json` produced
# before the move; its findings, arms and messages are unchanged, re-fired against the converted
# form.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "PROFILE-CONSISTENCY: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_profiles() {
python3 - "$@" <<'PY'
import sys, pathlib
sys.path.insert(0, "scripts")
import dossier_sexp as D
import experiment_verification as V
import experiment_artifacts as A
import records_sexp as R
import sexp as S

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
                    findings.append(
                        f"UNQUALIFIED EXPERIMENT VERIFICATION {name}/{xid}: "
                        "complete method/policy adequacy pending; matching pins give no qualification")
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
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/p"
  # ⛔ STRICT ARITY — docs/knowledge/self-test-arms-that-never-ran.md. A helper that ignores
  # surplus arguments swallows the whole following command when a `;` is missing, silently.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'PROFILE-CONSISTENCY self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # name expected_rc expected_substring
    argc 3 "$#" arm || return
    out="$(check_profiles "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'PROFILE-CONSISTENCY self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'PROFILE-CONSISTENCY self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }
  score() { # name actual_rc expected_rc output reason
    argc 5 "$#" score || return
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'PROFILE-CONSISTENCY self-test MISS: %s expected rc=%s reason=%s got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }
  # Fixtures are written as the converted form (one document form, multi-line for greppable
  # mutation), the way convert_dossier.py emits them — the arms fire against the format the
  # gate now reads.
  good() { cat > "$t/p/profile.sexp" <<'EOF'
(profile (id "p1") (xlen 64)
  (state (integer_registers 4))
  (scope (count_base 2) (count_rv64i_additions 1) (count_total 3)
         (base_op "X") (base_op "Y") (base_jumps "Z"))
  (decision (id "D-1")
            (authority architecture)
            (statement "s")
            (source "§1")
  )
)
EOF
  }
  good_state() { cat > "$t/p/state.sexp" <<'EOF'
(state (profile_id "p1") (xlen 64) (note "n")
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
EOF
  }
  # ---- a consistent dossier ----------------------------------------------------------------------
  good;                                                       arm "GREEN consistent profile"  0 "__CHECKED__ 1"
  # ---- state.sexp arms ----------------------------------------------------------------------------
  good; good_state
                                                              arm "GREEN state agrees with profile" 0 "__CHECKED__ 1"
  good; good_state; grep -v 'hidden_state_census' "$t/p/state.sexp" > "$t/p/x" && mv "$t/p/x" "$t/p/state.sexp"
                                                              arm "RED   empty hidden_state, no census" 1 "UNEARNED NONE"
  good; good_state; sed -i.bak 's/(xlen 64)/(xlen 32)/' "$t/p/state.sexp"
                                                              arm "RED   xlen disagrees"        1 "XLEN MISMATCH"
  good; good_state; sed -i.bak 's/(count 4)/(count 9)/' "$t/p/state.sexp"
                                                              arm "RED   register count disagrees" 1 "REG COUNT MISMATCH"
  # P4-SYSTEM.2 slice (c1): the profile's (csrs …) enumeration and the state document's csr
  # set are one fact stated twice — agreement is gated, both directions.
  good_csr() { sed -i.bak 's/(state (integer_registers 4))/(state (integer_registers 4) (csrs "mstatus") (csrs "mcycle"))/' "$t/p/profile.sexp"
    cat > "$t/p/state.sexp" <<'EOF'
(state (profile_id "p1") (xlen 64) (note "n")
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
EOF
  }
  good; good_csr;                                            arm "GREEN the csr set agrees, both directions" 0 "__CHECKED__ 1"
  good; good_csr; sed -i.bak 's/(id "mcycle")/(id "mtime")/' "$t/p/state.sexp"
                                                              arm "RED   a csr the state document carries but the profile does not declare" 1 "CSR SET MISMATCH"
  good; good_csr; sed -i.bak 's/ (csrs "mcycle")//' "$t/p/profile.sexp"
                                                              arm "RED   a csr the profile declares but the state document does not carry" 1 "CSR SET MISMATCH"
  rm -f "$t/p/state.sexp" "$t/p/profile.sexp.bak" "$t/p/state.sexp.bak"  good; good_state; sed -i.bak 's/(authority architecture)/(authority vibes)/' "$t/p/state.sexp"
                                                              arm "RED   state authority unknown" 1 "BAD AUTHORITY"
  good; rm -f "$t/p/state.sexp"
  # ---- profile.sexp arms --------------------------------------------------------------------------
  good; sed -i.bak 's/(count_total 3)/(count_total 4)/' "$t/p/profile.sexp"
                                                              arm "RED   count drifts from enumeration" 1 "COUNT DRIFT"
  good; sed -i.bak 's/(count_base 2)/(count_base 9)/' "$t/p/profile.sexp"
                                                              arm "RED   parts do not sum"     1 "PARTS DRIFT"
  good; sed -i.bak 's/(count_total 3)/(count_total 4)/; s/(count_rv64i_additions 1)/(count_rv64i_additions 1) (c_compressed "C.NOP")/' "$t/p/profile.sexp"
                                                              arm "GREEN C contributes to the extension census" 0 "__CHECKED__ 1"
  sed -i.bak 's/(count_base 2)/(count_base 3)/' "$t/p/profile.sexp"
                                                              arm "RED   C does not hide a wrong base part" 1 "PARTS DRIFT"
  good; sed -i.bak 's/(authority architecture)/(authority vibes)/' "$t/p/profile.sexp"
                                                              arm "RED   unknown authority"    1 "BAD AUTHORITY"
  good; sed -i.bak '/(source /d' "$t/p/profile.sexp"
                                                              arm "RED   decision cites nothing" 1 "NO SOURCE"
  good; sed -i.bak '$i\  (decision (id "D-1") (authority laboratory) (statement "s") (source "x"))' "$t/p/profile.sexp"
                                                              arm "RED   duplicate decision id" 1 "DUPLICATE ID"
  good; sed '/^  (decision /,/^  )$/d' "$t/p/profile.sexp" > "$t/p/x" && mv "$t/p/x" "$t/p/profile.sexp"
                                                              arm "RED   no decisions at all"  1 "NO DECISIONS"
  printf 'not = toml = at = all\n' > "$t/p/profile.sexp";     arm "RED   unparseable profile"  1 "UNPARSEABLE"
  # ---- references.sexp: the reference candidate dossier --------------------------------------------
  # BASE is the dossier WITHOUT its closing paren: experiment/difference/candidate rows
  # are appended INSIDE the form, then the arm closes it.
  BASE='(references (profile "p1")
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
'
  good; printf '%s)\n' "$BASE" > "$t/p/references.sexp"
                                                              arm "GREEN complete reference dossier" 0 "__CHECKED__ 1"
  refs() { argc 1 "$#" refs || return; printf '%s\n' "$1" > "$t/p/references.sexp"; }
  FULL="$BASE)" 
  refs "$(printf '%s' "$FULL" | grep -v 'lineage')";           arm "RED   a candidate with no lineage" 1 "NO LINEAGE"
  refs "$(printf '%s' "$FULL" | grep -v 'binary_sha256')";     arm "RED   obtained with no digest"   1 "UNEARNED OBTAINED"
  refs "$(printf '%s' "$FULL" | grep -v 'invocation')";        arm "RED   obtained with no invocation" 1 "UNEARNED OBTAINED"
  refs "$(printf '%s' "$FULL" | sed 's/(status "obtained")/(status "rumoured")/')"
                                                              arm "RED   an unknown status"         1 "BAD STATUS"
  refs "$(printf '%s' "$FULL" | sed 's/(status "obtained")/(status "not obtained")/')"
                                                              arm "RED   not obtained with no reason" 1 "NO REASON"
  refs "$(printf '%s' "$FULL" | grep -v 'role')";              arm "RED   a candidate with no role"  1 "NO ROLE"
  refs "$(printf '%s' "$FULL" | grep -v 'origin')";            arm "RED   a candidate citing nothing" 1 "NO ORIGIN"
  refs "$(printf '%s' "$FULL" | sed 's/(profile "p1")/(profile "other")/')"
                                                              arm "RED   dossier names another profile" 1 "REF PROFILE MISMATCH"
  refs "$(printf '%s' "$FULL" | grep -v 'consequence')";       arm "RED   an attempt with no consequence" 1 "THIN ATTEMPT"
  refs '(references (profile "p1"))';                           arm "RED   a dossier with no candidate" 1 "NO CANDIDATES"
  refs "$BASE
  (candidate (id \"c1\") (role \"dup\") (status \"not obtained\")
             (status_reason \"r\") (origin \"o\") (lineage \"l\"))
)"
                                                              arm "RED   a duplicate candidate id" 1 "DUPLICATE CANDIDATE"
  refs 'not = toml = at = all';                                 arm "RED   an unparseable dossier"    1 "UNPARSEABLE"
  EXP="$BASE
  (experiment (id \"e1\")
              (program \"g.s\")
              (models \"c1\")
              (verdict \"AGREE\")
              (reproduced \"yes\")
              (control \"observed failing when a value was falsified\")
  )
  (difference (id \"d1\")
              (kind \"harness\")
              (observed \"they differ\")
              (resolution \"normalized\")
  )"
  refs "$EXP)";                                                 arm "GREEN a complete experiment record" 0 "__CHECKED__ 1"
  # A schema-conforming block cannot receive qualification credit from
  # relationship/artifact/byte checks before full method/policy adequacy.
  VERIFIED_EXP="$(python3 "$ROOT/scripts/probe_experiment_verification.py" --emit-experiment)"
  refs "$BASE$VERIFIED_EXP)";                                   arm "RED   new verification remains closed pending full adequacy" 1 "UNQUALIFIED EXPERIMENT VERIFICATION"
  refs "$(printf '%s' "$EXP" | grep -v 'control'))";            arm "RED   agreement with no control" 1 "NO CONTROL"
  refs "$(printf '%s' "$EXP" | grep -v 'reproduced'))";        arm "RED   an experiment that never reproduced" 1 "THIN EXPERIMENT"
  refs "$(printf '%s' "$EXP" | grep -v 'observed'))";          arm "RED   a difference with nothing observed" 1 "THIN DIFFERENCE"
  # ---- independence (EVD-04) -------------------------------------------------------------
  C2='
  (candidate (id "c2") (role "second") (status "not obtained")
             (status_reason "not needed for this fixture") (origin "https://example.invalid/2")
             (lineage "unknown"))'
  IND_ROW='
  (independence (subsystem "integer")
                (pair "c1")
                (pair "c2")
                (verdict "not-examined")
                (evidence "none")
                (consequence "owner named"))'
  # Stable experiment identities must resolve to distinct declared candidates.
  refs "$(printf '%s' "$EXP" | sed 's/(models "c1")/(models "c9")/'))"
                                                              arm "RED   a single experiment model is undeclared" 1 "UNKNOWN EXPERIMENT MODEL"
  DUP_EXP='
  (experiment (id "e1") (program "other.s") (models "c1")
              (verdict "DIVERGE") (reproduced "yes") (control "different result observed"))'
  refs "$EXP$DUP_EXP)";                                        arm "RED   conflicting experiments share an identity" 1 "DUPLICATE EXPERIMENT ID"
  SELF_IND="$(printf '%s' "$IND_ROW" | sed 's/(pair "c2")/(pair "c1")/')"
  refs "$(printf '%s' "$EXP" | sed 's/(models "c1")/(models "c1") (models "c1")/')$C2$SELF_IND)"
                                                              arm "RED   repeated experiment models cannot fake a comparison" 1 "REPEATED EXPERIMENT MODEL"
  refs "$EXP$C2$SELF_IND)";                                     arm "RED   independence needs two distinct identities" 1 "BAD PAIR"

  refs "$EXP$C2$IND_ROW)";                                      arm "GREEN an independence record parses" 0 "__CHECKED__ 1"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed 's/not-examined/probably fine/'))"
                                                              arm "RED   an unknown independence verdict" 1 "BAD VERDICT"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | grep -v '(pair "c2")'))"
                                                              arm "RED   independence claimed of one model" 1 "BAD PAIR"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed '/(evidence /d'))"
                                                              arm "RED   an independence verdict with no examination" 1 "THIN INDEPENDENCE"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed 's/(pair "c2")/(pair "c9")/'))"
                                                              arm "RED   independence names a model that is not a candidate" 1 "UNKNOWN MODEL"
  # ---- 5b: a scalar standing for a configuration declares its scope ------------------------
  SC1='(references (profile "p1")
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
  )'
  refs "$SC1$C2$IND_ROW)"
                                                              arm "GREEN a scoped scalar"        0 "__CHECKED__ 1"
  refs "$(printf '%s' "$SC1" | grep -v 'matched_scope')$C2$IND_ROW)"
                                                              arm "RED   a scalar with no scope" 1 "UNSCOPED SCALAR"
  refs "$(printf '%s' "$SC1" | grep -v 'matched_isa_string_source')$C2$IND_ROW)"
                                                              arm "RED   a scalar with no source" 1 "UNSCOPED SCALAR"
  # an experiment comparing TWO models with no independence record for that pair
  refs "$(printf '%s' "$EXP" | sed 's/(models "c1")/(models "c1") (models "c2")/')$C2)"
                                                              arm "RED   two models compared, pair never examined" 1 "UNEXAMINED PAIR"
  rm -f "$t/p/references.sexp"

  # ---- the device-shaped dossier (P5-BOARD.2, case sifive-uart-lab-v0) ---------------------
  # No xlen, no integer_registers — a device has neither — an mmio_registers scope census,
  # and a state.sexp whose "none" is earned. The check's logic is unchanged: the count
  # rule and the census rule already generalize.
  device() { cat > "$t/p/profile.sexp" <<'EOF'
(profile (id "p1")
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
EOF
  }
  device_state() { cat > "$t/p/state.sexp" <<'EOF'
(state (profile_id "p1") (note "n")
  (special_registers (register (id "uart_rxdata") (width_bits 8) (holds "h")
                      (authority architecture) (source "s") (reset "r")
                      (reset_authority laboratory)))
  (hidden_state_census (question "q") (answer "No") (candidates (checked (candidate "c") (present false) (why "w"))) (consequence "c"))
)
EOF
  }
  device; device_state
                                                              arm "GREEN a device-shaped dossier: no xlen, mmio census, earned none" 0 "__CHECKED__ 1"
  device; device_state; sed -i.bak 's/(count_total 2)/(count_total 3)/' "$t/p/profile.sexp"
                                                              arm "RED   a device scope whose count drifts from its enumeration" 1 "COUNT DRIFT"
  rm -f "$t/p/state.sexp" "$t/p/profile.sexp.bak" "$t/p/state.sexp.bak"

  rm -rf "$t"
  out="$(python3 "$ROOT/scripts/probe_experiment_graph.py" 2>&1)"; rc=$?
  score "GREEN structured verification identity and edge controls" "$rc" 0 "$out" "EXPERIMENT-GRAPH: 74 pass / 0 fail"
  out="$(python3 "$ROOT/scripts/probe_experiment_graph.py" --mutation ignore-witness-budget 2>&1)"; rc=$?
  score "RED omitted witness budget guard loses four named refusals" "$rc" 1 "$out" "EXPERIMENT-GRAPH: 70 pass / 4 fail"
  out="$(python3 "$ROOT/scripts/probe_experiment_graph.py" --mutation ignore-witness-kind 2>&1)"; rc=$?
  score "RED omitted witness kind guard loses its named refusal" "$rc" 1 "$out" "EXPERIMENT-GRAPH: 73 pass / 1 fail"
  out="$(python3 "$ROOT/scripts/probe_experiment_graph.py" --mutation ignore-control-baseline 2>&1)"; rc=$?
  score "RED omitted control baseline guard loses three named refusals" "$rc" 1 "$out" "EXPERIMENT-GRAPH: 71 pass / 3 fail"
  out="$(python3 "$ROOT/scripts/probe_experiment_artifacts.py" 2>&1)"; rc=$?
  score "GREEN structured artifact pin controls" "$rc" 0 "$out" "EXPERIMENT-ARTIFACTS: 39 pass / 0 fail; descriptors/fixture cleaned"
  out="$(python3 "$ROOT/scripts/probe_experiment_snapshots.py" 2>&1)"; rc=$?
  score "GREEN bounded authenticated snapshot controls" "$rc" 0 "$out" "EXPERIMENT-SNAPSHOTS: 24 pass / 0 fail; descriptors/fixture cleaned"
  out="$(python3 "$ROOT/scripts/probe_experiment_read_limits.py" 2>&1)"; rc=$?
  score "GREEN explicit pin and snapshot read-budget controls" "$rc" 0 "$out" "EXPERIMENT-READ-LIMITS: 53 pass / 0 fail; descriptors/fixture cleaned"
  out="$(python3 "$ROOT/scripts/probe_experiment_read_limits.py" --mutation ignore-pin-limit 2>&1)"; rc=$?
  score "RED omitted pin limit reads an oversized payload" "$rc" 1 "$out" "READ-LIMIT MISS oversized pin refuses before reading"
  out="$(python3 "$ROOT/scripts/probe_experiment_read_limits.py" --mutation ignore-invalid-pin-limit 2>&1)"; rc=$?
  score "RED omitted pin-limit validation opens a path" "$rc" 1 "$out" "READ-LIMIT MISS invalid pin limit -1"
  out="$(python3 "$ROOT/scripts/probe_experiment_read_limits.py" --mutation ignore-sentinel-budget 2>&1)"; rc=$?
  score "RED unbounded growth sentinel exceeds snapshot cap" "$rc" 1 "$out" "READ-LIMIT MISS snapshot growth-at-cap consumes at most bound"
  out="$(python3 "$ROOT/scripts/probe_experiment_read_limits.py" --mutation retain-pin-payload 2>&1)"; rc=$?
  score "RED pin-only path retaining snapshot payload is detected" "$rc" 1 "$out" "READ-LIMIT MISS pin-only creates no snapshot payload"
  # P4-SYSTEM.14 a30: finite identity authentication, not execution/qualification.
  # Keep every outer arm literal: DERIVED-COUNTS enumerates call sites.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" 2>&1)"; rc=$?
  score "GREEN normal authenticated reference identity" "$rc" 0 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED normal omitted identity guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED normal omitted identity guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation raw-schema 2>&1)"; rc=$?
  score "RED normal omitted identity guard raw-schema" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 5 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation root-count 2>&1)"; rc=$?
  score "RED normal omitted identity guard root-count" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation candidate-count 2>&1)"; rc=$?
  score "RED normal omitted identity guard candidate-count" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation experiment-free 2>&1)"; rc=$?
  score "RED normal omitted identity guard experiment-free" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation identity-equality 2>&1)"; rc=$?
  score "RED normal omitted identity guard identity-equality" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 20 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation optional-presence 2>&1)"; rc=$?
  score "RED normal omitted identity guard optional-presence" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 17 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" 2>&1)"; rc=$?
  score "GREEN optimized authenticated reference identity" "$rc" 0 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED optimized omitted identity guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED optimized omitted identity guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation raw-schema 2>&1)"; rc=$?
  score "RED optimized omitted identity guard raw-schema" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 5 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation root-count 2>&1)"; rc=$?
  score "RED optimized omitted identity guard root-count" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation candidate-count 2>&1)"; rc=$?
  score "RED optimized omitted identity guard candidate-count" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation experiment-free 2>&1)"; rc=$?
  score "RED optimized omitted identity guard experiment-free" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation identity-equality 2>&1)"; rc=$?
  score "RED optimized omitted identity guard identity-equality" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 20 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_identity.py" --mutation optional-presence 2>&1)"; rc=$?
  score "RED optimized omitted identity guard optional-presence" "$rc" 1 "$out" "MATCHED-GPR-IDENTITY: 40 tests / 17 failures / 0 errors; fixtures cleaned"
  # P4-SYSTEM.14 a31: receipt pin/binding is separate from process/method success.
  # Literal arms preserve DERIVED-COUNTS's documented enumeration contract.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" 2>&1)"; rc=$?
  score "GREEN normal authenticated receipt binding" "$rc" 0 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation schema-tool 2>&1)"; rc=$?
  score "RED normal omitted receipt guard schema-tool" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED normal omitted receipt guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED normal omitted receipt guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation context-counts 2>&1)"; rc=$?
  score "RED normal omitted receipt guard context-counts" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation context-edges 2>&1)"; rc=$?
  score "RED normal omitted receipt guard context-edges" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation scalar-binding 2>&1)"; rc=$?
  score "RED normal omitted receipt guard scalar-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation argv-binding 2>&1)"; rc=$?
  score "RED normal omitted receipt guard argv-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation input-binding 2>&1)"; rc=$?
  score "RED normal omitted receipt guard input-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation output-binding 2>&1)"; rc=$?
  score "RED normal omitted receipt guard output-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 5 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation output-roles 2>&1)"; rc=$?
  score "RED normal omitted receipt guard output-roles" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation collector-role 2>&1)"; rc=$?
  score "RED normal omitted receipt guard collector-role" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" 2>&1)"; rc=$?
  score "GREEN optimized authenticated receipt binding" "$rc" 0 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation schema-tool 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard schema-tool" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation context-counts 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard context-counts" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation context-edges 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard context-edges" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation scalar-binding 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard scalar-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation argv-binding 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard argv-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation input-binding 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard input-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation output-binding 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard output-binding" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 5 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation output-roles 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard output-roles" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_receipt.py" --mutation collector-role 2>&1)"; rc=$?
  score "RED optimized omitted receipt guard collector-role" "$rc" 1 "$out" "MATCHED-GPR-RECEIPT: 43 tests / 1 failures / 0 errors; fixtures cleaned"
  # P4-SYSTEM.14 a32: pure execution bindings, never complete method credit.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" 2>&1)"; rc=$?
  score "GREEN normal fixed execution bindings" "$rc" 0 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation budget 2>&1)"; rc=$?
  score "RED normal omitted execution guard budget" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED normal omitted execution guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 8 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation reference-pin 2>&1)"; rc=$?
  score "RED normal omitted execution guard reference-pin" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation run-reference 2>&1)"; rc=$?
  score "RED normal omitted execution guard run-reference" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation repeat-edge 2>&1)"; rc=$?
  score "RED normal omitted execution guard repeat-edge" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation spurious-repeat 2>&1)"; rc=$?
  score "RED normal omitted execution guard spurious-repeat" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation output-ownership 2>&1)"; rc=$?
  score "RED normal omitted execution guard output-ownership" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation fixed-argv 2>&1)"; rc=$?
  score "RED normal omitted execution guard fixed-argv" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 44 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation repeat-selection 2>&1)"; rc=$?
  score "RED normal omitted execution guard repeat-selection" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation control-expectation 2>&1)"; rc=$?
  score "RED normal omitted execution guard control-expectation" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation control-producer 2>&1)"; rc=$?
  score "RED normal omitted execution guard control-producer" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation reference-inputs 2>&1)"; rc=$?
  score "RED normal omitted execution guard reference-inputs" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation fixture-count-cleanup 2>&1)"; rc=$?
  score "RED normal omitted execution guard fixture-count-cleanup" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation fixture-argv-cleanup 2>&1)"; rc=$?
  score "RED normal omitted execution guard fixture-argv-cleanup" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" 2>&1)"; rc=$?
  score "GREEN optimized fixed execution bindings" "$rc" 0 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation budget 2>&1)"; rc=$?
  score "RED optimized omitted execution guard budget" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED optimized omitted execution guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 8 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation reference-pin 2>&1)"; rc=$?
  score "RED optimized omitted execution guard reference-pin" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation run-reference 2>&1)"; rc=$?
  score "RED optimized omitted execution guard run-reference" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation repeat-edge 2>&1)"; rc=$?
  score "RED optimized omitted execution guard repeat-edge" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation spurious-repeat 2>&1)"; rc=$?
  score "RED optimized omitted execution guard spurious-repeat" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation output-ownership 2>&1)"; rc=$?
  score "RED optimized omitted execution guard output-ownership" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation fixed-argv 2>&1)"; rc=$?
  score "RED optimized omitted execution guard fixed-argv" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 44 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation repeat-selection 2>&1)"; rc=$?
  score "RED optimized omitted execution guard repeat-selection" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation control-expectation 2>&1)"; rc=$?
  score "RED optimized omitted execution guard control-expectation" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation control-producer 2>&1)"; rc=$?
  score "RED optimized omitted execution guard control-producer" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation reference-inputs 2>&1)"; rc=$?
  score "RED optimized omitted execution guard reference-inputs" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation fixture-count-cleanup 2>&1)"; rc=$?
  score "RED optimized omitted execution guard fixture-count-cleanup" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_execution.py" --mutation fixture-argv-cleanup 2>&1)"; rc=$?
  score "RED optimized omitted execution guard fixture-argv-cleanup" "$rc" 1 "$out" "MATCHED-GPR-EXECUTION: 48 tests / 1 failures / 0 errors; synthetic only"
  # P4-SYSTEM.14 a33: declared method relations and assertion-safe fixture controls.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" 2>&1)"; rc=$?
  score "GREEN normal declared method relations" "$rc" 0 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED normal omitted relation guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation gpr-only 2>&1)"; rc=$?
  score "RED normal omitted relation guard gpr-only" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation witness-budget 2>&1)"; rc=$?
  score "RED normal omitted relation guard witness-budget" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation witness-register 2>&1)"; rc=$?
  score "RED normal omitted relation guard witness-register" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-runs 2>&1)"; rc=$?
  score "RED normal omitted relation guard control-runs" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-property 2>&1)"; rc=$?
  score "RED normal omitted relation guard control-property" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation property-count 2>&1)"; rc=$?
  score "RED normal omitted relation guard property-count" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation witness-unique 2>&1)"; rc=$?
  score "RED normal omitted relation guard witness-unique" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-mutation 2>&1)"; rc=$?
  score "RED normal omitted relation guard control-mutation" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-intent 2>&1)"; rc=$?
  score "RED normal omitted relation guard control-intent" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-observed 2>&1)"; rc=$?
  score "RED normal omitted relation guard control-observed" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-version 2>&1)"; rc=$?
  score "RED normal omitted relation guard expected-version" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-selection 2>&1)"; rc=$?
  score "RED normal omitted relation guard expected-selection" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-consumes 2>&1)"; rc=$?
  score "RED normal omitted relation guard expected-consumes" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-common 2>&1)"; rc=$?
  score "RED normal omitted relation guard expected-common" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation pair-endpoints 2>&1)"; rc=$?
  score "RED normal omitted relation guard pair-endpoints" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation pair-sharing 2>&1)"; rc=$?
  score "RED normal omitted relation guard pair-sharing" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation fixture-count-cleanup 2>&1)"; rc=$?
  score "RED normal omitted relation guard fixture-count-cleanup" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation fixture-version-cleanup 2>&1)"; rc=$?
  score "RED normal omitted relation guard fixture-version-cleanup" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" 2>&1)"; rc=$?
  score "GREEN optimized declared method relations" "$rc" 0 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED optimized omitted relation guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation gpr-only 2>&1)"; rc=$?
  score "RED optimized omitted relation guard gpr-only" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation witness-budget 2>&1)"; rc=$?
  score "RED optimized omitted relation guard witness-budget" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation witness-register 2>&1)"; rc=$?
  score "RED optimized omitted relation guard witness-register" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-runs 2>&1)"; rc=$?
  score "RED optimized omitted relation guard control-runs" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-property 2>&1)"; rc=$?
  score "RED optimized omitted relation guard control-property" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation property-count 2>&1)"; rc=$?
  score "RED optimized omitted relation guard property-count" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation witness-unique 2>&1)"; rc=$?
  score "RED optimized omitted relation guard witness-unique" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-mutation 2>&1)"; rc=$?
  score "RED optimized omitted relation guard control-mutation" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-intent 2>&1)"; rc=$?
  score "RED optimized omitted relation guard control-intent" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation control-observed 2>&1)"; rc=$?
  score "RED optimized omitted relation guard control-observed" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-version 2>&1)"; rc=$?
  score "RED optimized omitted relation guard expected-version" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-selection 2>&1)"; rc=$?
  score "RED optimized omitted relation guard expected-selection" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-consumes 2>&1)"; rc=$?
  score "RED optimized omitted relation guard expected-consumes" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation expected-common 2>&1)"; rc=$?
  score "RED optimized omitted relation guard expected-common" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation pair-endpoints 2>&1)"; rc=$?
  score "RED optimized omitted relation guard pair-endpoints" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation pair-sharing 2>&1)"; rc=$?
  score "RED optimized omitted relation guard pair-sharing" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation fixture-count-cleanup 2>&1)"; rc=$?
  score "RED optimized omitted relation guard fixture-count-cleanup" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_relations.py" --mutation fixture-version-cleanup 2>&1)"; rc=$?
  score "RED optimized omitted relation guard fixture-version-cleanup" "$rc" 1 "$out" "MATCHED-GPR-RELATIONS: 42 tests / 1 failures / 0 errors; synthetic only"
  # P4-SYSTEM.14 a34: authenticate/bind only the manifest, never its leaves.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" 2>&1)"; rc=$?
  score "GREEN normal authenticated manifest binding" "$rc" 0 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED normal omitted manifest guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED normal omitted manifest guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation manifest-codec 2>&1)"; rc=$?
  score "RED normal omitted manifest guard manifest-codec" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 16 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation principal-overlap 2>&1)"; rc=$?
  score "RED normal omitted manifest guard principal-overlap" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation path-alias 2>&1)"; rc=$?
  score "RED normal omitted manifest guard path-alias" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation output-alias 2>&1)"; rc=$?
  score "RED normal omitted manifest guard output-alias" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation context-freeze 2>&1)"; rc=$?
  score "RED normal omitted manifest guard context-freeze" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation schema-tool 2>&1)"; rc=$?
  score "RED normal omitted manifest guard schema-tool" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" 2>&1)"; rc=$?
  score "GREEN optimized authenticated manifest binding" "$rc" 0 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation manifest-codec 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard manifest-codec" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 16 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation principal-overlap 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard principal-overlap" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation path-alias 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard path-alias" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation output-alias 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard output-alias" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation context-freeze 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard context-freeze" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_manifest.py" --mutation schema-tool 2>&1)"; rc=$?
  score "RED optimized omitted manifest guard schema-tool" "$rc" 1 "$out" "MATCHED-GPR-MANIFEST: 33 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" 2>&1)"; rc=$?
  score "GREEN normal selected dependency leaf" "$rc" 0 "$out" "MATCHED-GPR-LEAF: 50 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED normal omitted leaf guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation selected-edge 2>&1)"; rc=$?
  score "RED normal omitted leaf guard selected-edge" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation selected-binding 2>&1)"; rc=$?
  score "RED normal omitted leaf guard selected-binding" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation manifest-selection 2>&1)"; rc=$?
  score "RED normal omitted leaf guard manifest-selection" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation byte-limit 2>&1)"; rc=$?
  score "RED normal omitted leaf guard byte-limit" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED normal omitted leaf guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED normal omitted leaf guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation payload-consistency 2>&1)"; rc=$?
  score "RED normal omitted leaf guard payload-consistency" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation document-classification 2>&1)"; rc=$?
  score "RED normal omitted leaf guard document-classification" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 11 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation no-nesting 2>&1)"; rc=$?
  score "RED normal omitted leaf guard no-nesting" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation snapshot-reopen 2>&1)"; rc=$?
  score "RED normal omitted leaf guard snapshot-reopen" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation immutable-result 2>&1)"; rc=$?
  score "RED normal omitted leaf guard immutable-result" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation document-bound 2>&1)"; rc=$?
  score "RED normal omitted leaf guard document-bound" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation schema-preflight 2>&1)"; rc=$?
  score "RED normal omitted leaf guard schema-preflight" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation schema-before-map 2>&1)"; rc=$?
  score "RED normal omitted leaf guard schema-before-map" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" 2>&1)"; rc=$?
  score "GREEN optimized selected dependency leaf" "$rc" 0 "$out" "MATCHED-GPR-LEAF: 50 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation selected-edge 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard selected-edge" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation selected-binding 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard selected-binding" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation manifest-selection 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard manifest-selection" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation byte-limit 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard byte-limit" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation read-bound 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard read-bound" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation pin-status 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard pin-status" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation payload-consistency 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard payload-consistency" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation document-classification 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard document-classification" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 11 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation no-nesting 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard no-nesting" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation snapshot-reopen 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard snapshot-reopen" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation immutable-result 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard immutable-result" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation document-bound 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard document-bound" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation schema-preflight 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard schema-preflight" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_leaf.py" --mutation schema-before-map 2>&1)"; rc=$?
  score "RED optimized omitted leaf guard schema-before-map" "$rc" 1 "$out" "MATCHED-GPR-LEAF: 50 tests / 2 failures / 0 errors; fixtures cleaned"
  # P4.14 a42d2: opt-in source/image snapshots share the original ledger and rebuild room.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" 2>&1)"; rc=$?
  score "GREEN normal source/image files controls" "$rc" 0 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation flag-type 2>&1)"; rc=$?
  score "RED normal source/image files omitted flag-type" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation default 2>&1)"; rc=$?
  score "RED normal source/image files omitted default" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation forward 2>&1)"; rc=$?
  score "RED normal source/image files omitted forward" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 11 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation retain-source 2>&1)"; rc=$?
  score "RED normal source/image files omitted retain-source" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 10 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation retain-image 2>&1)"; rc=$?
  score "RED normal source/image files omitted retain-image" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 9 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation source-cap 2>&1)"; rc=$?
  score "RED normal source/image files omitted source-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation image-cap 2>&1)"; rc=$?
  score "RED normal source/image files omitted image-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation reserve 2>&1)"; rc=$?
  score "RED normal source/image files omitted reserve" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation reserve-debit 2>&1)"; rc=$?
  score "RED normal source/image files omitted reserve-debit" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 5 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation seed-peak 2>&1)"; rc=$?
  score "RED normal source/image files omitted seed-peak" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation snapshot-cap 2>&1)"; rc=$?
  score "RED normal source/image files omitted snapshot-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation read-cap 2>&1)"; rc=$?
  score "RED normal source/image files omitted read-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation drop-failed-payloads 2>&1)"; rc=$?
  score "RED normal source/image files omitted drop-failed-payloads" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation immutable-facts 2>&1)"; rc=$?
  score "RED normal source/image files omitted immutable-facts" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation immutable-result 2>&1)"; rc=$?
  score "RED normal source/image files omitted immutable-result" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation reservation-counter 2>&1)"; rc=$?
  score "RED normal source/image files omitted reservation-counter" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" 2>&1)"; rc=$?
  score "GREEN optimized source/image files controls" "$rc" 0 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation flag-type 2>&1)"; rc=$?
  score "RED optimized source/image files omitted flag-type" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation default 2>&1)"; rc=$?
  score "RED optimized source/image files omitted default" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation forward 2>&1)"; rc=$?
  score "RED optimized source/image files omitted forward" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 11 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation retain-source 2>&1)"; rc=$?
  score "RED optimized source/image files omitted retain-source" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 10 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation retain-image 2>&1)"; rc=$?
  score "RED optimized source/image files omitted retain-image" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 9 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation source-cap 2>&1)"; rc=$?
  score "RED optimized source/image files omitted source-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation image-cap 2>&1)"; rc=$?
  score "RED optimized source/image files omitted image-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation reserve 2>&1)"; rc=$?
  score "RED optimized source/image files omitted reserve" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 7 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation reserve-debit 2>&1)"; rc=$?
  score "RED optimized source/image files omitted reserve-debit" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 5 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation seed-peak 2>&1)"; rc=$?
  score "RED optimized source/image files omitted seed-peak" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation snapshot-cap 2>&1)"; rc=$?
  score "RED optimized source/image files omitted snapshot-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation read-cap 2>&1)"; rc=$?
  score "RED optimized source/image files omitted read-cap" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation drop-failed-payloads 2>&1)"; rc=$?
  score "RED optimized source/image files omitted drop-failed-payloads" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation immutable-facts 2>&1)"; rc=$?
  score "RED optimized source/image files omitted immutable-facts" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation immutable-result 2>&1)"; rc=$?
  score "RED optimized source/image files omitted immutable-result" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_guest_files.py" --mutation reservation-counter 2>&1)"; rc=$?
  score "RED optimized source/image files omitted reservation-counter" "$rc" 1 "$out" "MATCHED-GPR-GUEST-FILES: 24 tests / 6 failures / 0 errors; fixtures cleaned"
  # End P4.14 a42d2.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" 2>&1)"; rc=$?
  score "GREEN normal aggregate declared file set" "$rc" 0 "$out" "MATCHED-GPR-FILES: 49 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation aggregate-limits 2>&1)"; rc=$?
  score "RED normal omitted file-set guard aggregate-limits" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 14 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation seed-budget 2>&1)"; rc=$?
  score "RED normal omitted file-set guard seed-budget" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation seed-snapshot-peak 2>&1)"; rc=$?
  score "RED normal omitted file-set guard seed-snapshot-peak" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation snapshot-consistency 2>&1)"; rc=$?
  score "RED normal omitted file-set guard snapshot-consistency" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED normal omitted file-set guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-count 2>&1)"; rc=$?
  score "RED normal omitted file-set guard observation-count" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation execution-counts 2>&1)"; rc=$?
  score "RED normal omitted file-set guard execution-counts" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation child-identities 2>&1)"; rc=$?
  score "RED normal omitted file-set guard child-identities" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation union-identities 2>&1)"; rc=$?
  score "RED normal omitted file-set guard union-identities" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation union-membership 2>&1)"; rc=$?
  score "RED normal omitted file-set guard union-membership" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation principal-identity 2>&1)"; rc=$?
  score "RED normal omitted file-set guard principal-identity" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation manifest-selection 2>&1)"; rc=$?
  score "RED normal omitted file-set guard manifest-selection" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation manifest-seed 2>&1)"; rc=$?
  score "RED normal omitted file-set guard manifest-seed" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-selection 2>&1)"; rc=$?
  score "RED normal omitted file-set guard observation-selection" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-unique 2>&1)"; rc=$?
  score "RED normal omitted file-set guard observation-unique" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-size 2>&1)"; rc=$?
  score "RED normal omitted file-set guard observation-size" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation output-alias 2>&1)"; rc=$?
  score "RED normal omitted file-set guard output-alias" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation read-cap 2>&1)"; rc=$?
  score "RED normal omitted file-set guard read-cap" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation snapshot-cap 2>&1)"; rc=$?
  score "RED normal omitted file-set guard snapshot-cap" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation seed-charge 2>&1)"; rc=$?
  score "RED normal omitted file-set guard seed-charge" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 10 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation failed-charge 2>&1)"; rc=$?
  score "RED normal omitted file-set guard failed-charge" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation stop-after-failure 2>&1)"; rc=$?
  score "RED normal omitted file-set guard stop-after-failure" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 12 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation drop-failed-payloads 2>&1)"; rc=$?
  score "RED normal omitted file-set guard drop-failed-payloads" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation transient-first 2>&1)"; rc=$?
  score "RED normal omitted file-set guard transient-first" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 11 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation transient-release 2>&1)"; rc=$?
  score "RED normal omitted file-set guard transient-release" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation nested-classification 2>&1)"; rc=$?
  score "RED normal omitted file-set guard nested-classification" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation immutable-result 2>&1)"; rc=$?
  score "RED normal omitted file-set guard immutable-result" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation immutable-facts 2>&1)"; rc=$?
  score "RED normal omitted file-set guard immutable-facts" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation context-freeze 2>&1)"; rc=$?
  score "RED normal omitted file-set guard context-freeze" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation manifest-reopen 2>&1)"; rc=$?
  score "RED normal omitted file-set guard manifest-reopen" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 13 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_files.py" --mutation legacy-pin 2>&1)"; rc=$?
  score "RED normal omitted file-set guard legacy-pin" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" 2>&1)"; rc=$?
  score "GREEN optimized aggregate declared file set" "$rc" 0 "$out" "MATCHED-GPR-FILES: 49 tests / 0 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation aggregate-limits 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard aggregate-limits" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 14 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation seed-budget 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard seed-budget" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation seed-snapshot-peak 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard seed-snapshot-peak" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation snapshot-consistency 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard snapshot-consistency" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation family-counts 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard family-counts" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-count 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard observation-count" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation execution-counts 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard execution-counts" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation child-identities 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard child-identities" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation union-identities 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard union-identities" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation union-membership 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard union-membership" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation principal-identity 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard principal-identity" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation manifest-selection 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard manifest-selection" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation manifest-seed 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard manifest-seed" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 8 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-selection 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard observation-selection" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-unique 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard observation-unique" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation observation-size 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard observation-size" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation output-alias 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard output-alias" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation read-cap 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard read-cap" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation snapshot-cap 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard snapshot-cap" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation seed-charge 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard seed-charge" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 10 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation failed-charge 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard failed-charge" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 6 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation stop-after-failure 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard stop-after-failure" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 12 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation drop-failed-payloads 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard drop-failed-payloads" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 4 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation transient-first 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard transient-first" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 11 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation transient-release 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard transient-release" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation nested-classification 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard nested-classification" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 3 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation immutable-result 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard immutable-result" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation immutable-facts 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard immutable-facts" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation context-freeze 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard context-freeze" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 1 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation manifest-reopen 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard manifest-reopen" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 13 failures / 0 errors; fixtures cleaned"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_files.py" --mutation legacy-pin 2>&1)"; rc=$?
  score "RED optimized omitted file-set guard legacy-pin" "$rc" 1 "$out" "MATCHED-GPR-FILES: 49 tests / 2 failures / 0 errors; fixtures cleaned"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" 2>&1)"; rc=$?
  score "GREEN normal frozen byte consumers" "$rc" 0 "$out" "MATCHED-GPR-BYTES: 22 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-freeze 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-freeze" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 19 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-string-freeze 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-string-freeze" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-context 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-context" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-path 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-path" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-fields 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-fields" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-count 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-count" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-canonical 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-canonical" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-parser 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-parser" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-frozen 2>&1)"; rc=$?
  score "RED normal omitted byte guard identity-frozen" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-binder 2>&1)"; rc=$?
  score "RED normal omitted byte guard receipt-binder" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-context 2>&1)"; rc=$?
  score "RED normal omitted byte guard receipt-context" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-parser 2>&1)"; rc=$?
  score "RED normal omitted byte guard receipt-parser" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 14 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-claim 2>&1)"; rc=$?
  score "RED normal omitted byte guard receipt-claim" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-frozen 2>&1)"; rc=$?
  score "RED normal omitted byte guard receipt-frozen" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" 2>&1)"; rc=$?
  score "GREEN optimized frozen byte consumers" "$rc" 0 "$out" "MATCHED-GPR-BYTES: 22 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-freeze 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-freeze" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 19 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-string-freeze 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-string-freeze" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-context 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-context" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-path 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-path" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-fields 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-fields" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-count 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-count" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-canonical 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-canonical" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-parser 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-parser" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation identity-frozen 2>&1)"; rc=$?
  score "RED optimized omitted byte guard identity-frozen" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-binder 2>&1)"; rc=$?
  score "RED optimized omitted byte guard receipt-binder" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 13 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-context 2>&1)"; rc=$?
  score "RED optimized omitted byte guard receipt-context" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-parser 2>&1)"; rc=$?
  score "RED optimized omitted byte guard receipt-parser" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 14 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-claim 2>&1)"; rc=$?
  score "RED optimized omitted byte guard receipt-claim" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_bytes.py" --mutation receipt-frozen 2>&1)"; rc=$?
  score "RED optimized omitted byte guard receipt-frozen" "$rc" 1 "$out" "MATCHED-GPR-BYTES: 22 tests / 1 failures / 0 errors; synthetic only"
  # P4.14 a42d3b: authenticated source/image composition keeps separate findings.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" 2>&1)"; rc=$?
  score "GREEN normal image evaluation controls" "$rc" 0 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation retention 2>&1)"; rc=$?
  score "RED normal image evaluation omitted retention" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-budget 2>&1)"; rc=$?
  score "RED normal image evaluation omitted context-budget" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-program 2>&1)"; rc=$?
  score "RED normal image evaluation omitted context-program" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-validation 2>&1)"; rc=$?
  score "RED normal image evaluation omitted context-validation" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 10 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-refusal 2>&1)"; rc=$?
  score "RED normal image evaluation omitted context-refusal" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation source-selection 2>&1)"; rc=$?
  score "RED normal image evaluation omitted source-selection" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 18 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-selection 2>&1)"; rc=$?
  score "RED normal image evaluation omitted image-selection" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 16 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation source-reopen 2>&1)"; rc=$?
  score "RED normal image evaluation omitted source-reopen" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-reopen 2>&1)"; rc=$?
  score "RED normal image evaluation omitted image-reopen" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation entry-forward 2>&1)"; rc=$?
  score "RED normal image evaluation omitted entry-forward" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-label 2>&1)"; rc=$?
  score "RED normal image evaluation omitted image-label" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-status 2>&1)"; rc=$?
  score "RED normal image evaluation omitted image-status" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 11 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-finding 2>&1)"; rc=$?
  score "RED normal image evaluation omitted image-finding" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation comparison-order 2>&1)"; rc=$?
  score "RED normal image evaluation omitted comparison-order" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" 2>&1)"; rc=$?
  score "GREEN optimized image evaluation controls" "$rc" 0 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation retention 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted retention" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-budget 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted context-budget" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-program 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted context-program" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-validation 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted context-validation" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 10 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation context-refusal 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted context-refusal" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation source-selection 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted source-selection" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 18 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-selection 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted image-selection" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 16 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation source-reopen 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted source-reopen" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-reopen 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted image-reopen" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation entry-forward 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted entry-forward" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-label 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted image-label" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-status 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted image-status" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 11 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation image-finding 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted image-finding" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 22 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_image_evaluation.py" --mutation comparison-order 2>&1)"; rc=$?
  score "RED optimized image evaluation omitted comparison-order" "$rc" 1 "$out" "MATCHED-GPR-IMAGE-EVALUATION: 26 tests / 2 failures / 0 errors; synthetic only"
  # End P4.14 a42d3b.
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" 2>&1)"; rc=$?
  score "GREEN normal authenticated byte evaluation" "$rc" 0 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation scope 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard scope" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation raw-check 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard raw-check" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation raw-findings 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard raw-findings" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation schema-tool 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard schema-tool" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation candidate-freeze 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard candidate-freeze" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation relations-status 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard relations-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation observation-freeze 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard observation-freeze" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-context 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard receipt-context" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation manifest-status 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard manifest-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation manifest-relations 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard manifest-relations" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation manifest-reopen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard manifest-reopen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation file-status 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard file-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation payload-release 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard payload-release" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 27 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation snapshot-account 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard snapshot-account" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation identity-status 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard identity-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation identity-reopen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard identity-reopen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-status 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard receipt-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-reopen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard receipt-reopen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation process-facts 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard process-facts" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation control-selection 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard control-selection" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 15 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation comparison-refusal 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard comparison-refusal" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation comparison-completeness 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard comparison-completeness" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation verdict-binding 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard verdict-binding" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation comparison-status 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard comparison-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation qualification 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard qualification" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 10 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation result-frozen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard result-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation record-frozen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard record-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation authentication-frozen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard authentication-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-frozen 2>&1)"; rc=$?
  score "RED normal omitted evaluation guard receipt-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" 2>&1)"; rc=$?
  score "GREEN optimized authenticated byte evaluation" "$rc" 0 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation scope 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard scope" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation raw-check 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard raw-check" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation raw-findings 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard raw-findings" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation schema-tool 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard schema-tool" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation candidate-freeze 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard candidate-freeze" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation relations-status 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard relations-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation observation-freeze 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard observation-freeze" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-context 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard receipt-context" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation manifest-status 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard manifest-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation manifest-relations 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard manifest-relations" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation manifest-reopen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard manifest-reopen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation file-status 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard file-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation payload-release 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard payload-release" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 27 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation snapshot-account 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard snapshot-account" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation identity-status 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard identity-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation identity-reopen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard identity-reopen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-status 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard receipt-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-reopen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard receipt-reopen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation process-facts 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard process-facts" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation control-selection 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard control-selection" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 15 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation comparison-refusal 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard comparison-refusal" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation comparison-completeness 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard comparison-completeness" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 3 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation verdict-binding 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard verdict-binding" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation comparison-status 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard comparison-status" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation qualification 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard qualification" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 10 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation result-frozen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard result-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation record-frozen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard record-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation authentication-frozen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard authentication-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_evaluation.py" --mutation receipt-frozen 2>&1)"; rc=$?
  score "RED optimized omitted evaluation guard receipt-frozen" "$rc" 1 "$out" "MATCHED-GPR-EVALUATION: 42 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" 2>&1)"; rc=$?
  score "GREEN normal parent-program controls" "$rc" 0 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-type 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-type" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-binding 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-binding" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 13 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-forward 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-forward" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-freeze 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-freeze" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-bound 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-bound" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-plain 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-plain" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-selection 2>&1)"; rc=$?
  score "RED normal omitted parent-program guard program-selection" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" 2>&1)"; rc=$?
  score "GREEN optimized parent-program controls" "$rc" 0 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-type 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-type" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-binding 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-binding" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 13 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-forward 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-forward" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 5 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-freeze 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-freeze" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-bound 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-bound" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-plain 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-plain" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_matched_gpr_program.py" --mutation program-selection 2>&1)"; rc=$?
  score "RED optimized omitted parent-program guard program-selection" "$rc" 1 "$out" "MATCHED-GPR-PROGRAM: 23 tests / 1 failures / 0 errors; synthetic only"
  # a42g: bounded conservative old/new graph impact; synthetic projections only.
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" 2>&1)"; rc=$?
  score "GREEN normal change-impact controls" "$rc" 0 "$out" "CHANGE-IMPACT: 34 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation content-seeds 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard content-seeds" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 17 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation edge-seeds 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard edge-seeds" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation path-seeds 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard path-seeds" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation unmapped-insertion 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard unmapped-insertion" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation unmapped-broad 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard unmapped-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation uncertain-broad 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard uncertain-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation scope-broad 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard scope-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation unknown-broad 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard unknown-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation shared-broad 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard shared-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 16 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation broad-expansion 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard broad-expansion" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 18 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation reverse-closure 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard reverse-closure" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation node-bound 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard node-bound" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation edge-bound 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard edge-bound" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation plain-bool 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard plain-bool" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation node-unique 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard node-unique" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation edge-unique 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard edge-unique" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation edge-scope 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard edge-scope" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 "$ROOT/scripts/probe_change_impact.py" --mutation result-frozen 2>&1)"; rc=$?
  score "RED normal omitted change-impact guard result-frozen" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" 2>&1)"; rc=$?
  score "GREEN optimized change-impact controls" "$rc" 0 "$out" "CHANGE-IMPACT: 34 tests / 0 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation content-seeds 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard content-seeds" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 17 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation edge-seeds 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard edge-seeds" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 4 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation path-seeds 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard path-seeds" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 6 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation unmapped-insertion 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard unmapped-insertion" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation unmapped-broad 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard unmapped-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation uncertain-broad 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard uncertain-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation scope-broad 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard scope-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation unknown-broad 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard unknown-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation shared-broad 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard shared-broad" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 16 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation broad-expansion 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard broad-expansion" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 18 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation reverse-closure 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard reverse-closure" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 7 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation node-bound 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard node-bound" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation edge-bound 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard edge-bound" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation plain-bool 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard plain-bool" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation node-unique 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard node-unique" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 2 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation edge-unique 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard edge-unique" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation edge-scope 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard edge-scope" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  out="$(python3 -O "$ROOT/scripts/probe_change_impact.py" --mutation result-frozen 2>&1)"; rc=$?
  score "RED optimized omitted change-impact guard result-frozen" "$rc" 1 "$out" "CHANGE-IMPACT: 34 tests / 1 failures / 0 errors; synthetic only"
  # P4-SYSTEM.14 a42m: caller-reviewed inventory is a separate authority.
  local review_mode review_mutation review_failures
  local -a review_command
  for review_mode in normal optimized; do
    review_command=(python3)
    [ "$review_mode" = optimized ] && review_command+=(-O)
    out="$("${review_command[@]}" "$ROOT/scripts/probe_matched_gpr_input_review.py" 2>&1)"; rc=$?
    score "GREEN $review_mode reviewed-input controls" "$rc" 0 "$out" "MATCHED-GPR-INPUT-REVIEW: 20 tests / 0 failures / 0 errors; synthetic only"
    while IFS=: read -r review_mutation review_failures; do
      out="$("${review_command[@]}" "$ROOT/scripts/probe_matched_gpr_input_review.py" --mutation "$review_mutation" 2>&1)"; rc=$?
      score "RED $review_mode omitted input-review guard $review_mutation" "$rc" 1 "$out" "MATCHED-GPR-INPUT-REVIEW: 20 tests / $review_failures failures / 0 errors; synthetic only"
    done <<'INPUT_REVIEW_CASES'
missing:2
unreviewed:2
changed:4
profile:2
experiment:2
bindings-copy:2
input-bound:2
input-type:2
id-unique:1
path-unique:1
result-frozen:1
review-frozen:2
declared-validation:1
plan-binding:3
review-freeze:4
INPUT_REVIEW_CASES
  done
  # P4-SYSTEM.14 a42n: graph/input bindings remain conditional caller review.
  local impact_mode impact_mutation impact_failures
  local -a impact_command
  for impact_mode in normal optimized; do
    impact_command=(python3)
    [ "$impact_mode" = optimized ] && impact_command+=(-O)
    out="$("${impact_command[@]}" "$ROOT/scripts/probe_matched_gpr_impact.py" 2>&1)"; rc=$?
    score "GREEN $impact_mode retained-input impact controls" "$rc" 0 "$out" "MATCHED-GPR-IMPACT: 24 tests / 0 failures / 0 errors; synthetic only"
    while IFS=: read -r impact_mutation impact_failures; do
      out="$("${impact_command[@]}" "$ROOT/scripts/probe_matched_gpr_impact.py" --mutation "$impact_mutation" 2>&1)"; rc=$?
      score "RED $impact_mode omitted impact guard $impact_mutation" "$rc" 1 "$out" "MATCHED-GPR-IMPACT: 24 tests / $impact_failures failures / 0 errors; synthetic only"
    done <<'INPUT_IMPACT_CASES'
role-fingerprint:2
digest-fingerprint:2
profile:1
experiment:2
input-path:3
input-fingerprint:2
input-kind:2
input-profile:1
old-evidence:1
evidence-kind:1
reachability:1
graph-copy:2
node-envelope:1
edge-envelope:1
profile-envelope:1
result-frozen:1
context-frozen:1
binding-status:1
stale-status:1
current-review:1
finding:4
frozen-context:1
INPUT_IMPACT_CASES
  done
  # P4-SYSTEM.14 a42q: retained source-value composition; qualification stays pending.
  local value_mode value_mutation value_losses
  local -a value_python
  for value_mode in normal optimized; do
    value_python=(python3)
    [ "$value_mode" = optimized ] && value_python+=(-O)
    out="$("${value_python[@]}" scripts/probe_matched_gpr_value_evaluation.py 2>&1)"; rc=$?
    score "GREEN source-value evaluation $value_mode" "$rc" 0 "$out" "MATCHED-GPR-VALUE-EVALUATION: 19 tests / 0 failures / 0 errors; synthetic only"
    while IFS=: read -r value_mutation value_losses; do
      out="$("${value_python[@]}" scripts/probe_matched_gpr_value_evaluation.py --mutation "$value_mutation" 2>&1)"; rc=$?
      score "RED source-value evaluation $value_mutation $value_mode" "$rc" 1 "$out" "MATCHED-GPR-VALUE-EVALUATION: 19 tests / $value_losses failures / 0 errors; synthetic only"
    done <<'VALUE_EVALUATION_CASES'
source-values-selection:10
baseline-values-selection:10
source-values-reopen:1
budget-forward:2
witness-forward:9
program-forward:12
source-result-shape:4
source-binding-shape:3
source-context-binding:7
source-status:3
unsupported-credit:1
source-finding:13
VALUE_EVALUATION_CASES
  done

  # P4-SYSTEM.14 a42r: reviewed-author metadata, no execution attestation.
  local author_mode author_mutation author_losses
  local -a author_python
  for author_mode in normal optimized; do
    author_python=(python3)
    [ "$author_mode" = optimized ] && author_python+=(-O)
    out="$("${author_python[@]}" scripts/probe_matched_gpr_expected_author.py 2>&1)"; rc=$?
    score "GREEN reviewed expected author $author_mode" "$rc" 0 "$out" "MATCHED-GPR-EXPECTED-AUTHOR: 21 tests / 0 failures / 0 errors; synthetic only"
    while IFS=: read -r author_mutation author_losses; do
      out="$("${author_python[@]}" scripts/probe_matched_gpr_expected_author.py --mutation "$author_mutation" 2>&1)"; rc=$?
      score "RED reviewed expected author $author_mutation $author_mode" "$rc" 1 "$out" "MATCHED-GPR-EXPECTED-AUTHOR: 21 tests / $author_losses failures / 0 errors; synthetic only"
    done <<'EXPECTED_AUTHOR_CASES'
authority-shape:1
authority-scope:6
authority-copy:4
author-selection:3
review-route:3
inventory-binding:5
child-membership:1
principal-binding:3
producer-version:4
source-consumption:1
manifest-consumption:1
snapshot-author:3
snapshot-source:1
snapshot-budget:4
frozen-results:3
metadata-finding:4
EXPECTED_AUTHOR_CASES
  done

  # P4-SYSTEM.14 a42s: retained reviewed-author composition; qualification pending.
  local author_eval_mode author_eval_mutation author_eval_losses
  local -a author_eval_python
  for author_eval_mode in normal optimized; do
    author_eval_python=(python3)
    [ "$author_eval_mode" = optimized ] && author_eval_python+=(-O)
    out="$("${author_eval_python[@]}" scripts/probe_matched_gpr_author_evaluation.py 2>&1)"; rc=$?
    score "GREEN expected-author evaluation $author_eval_mode" "$rc" 0 "$out" "MATCHED-GPR-AUTHOR-EVALUATION: 19 tests / 0 failures / 0 errors; synthetic only"
    while IFS=: read -r author_eval_mutation author_eval_losses; do
      out="$("${author_eval_python[@]}" scripts/probe_matched_gpr_author_evaluation.py --mutation "$author_eval_mutation" 2>&1)"; rc=$?
      score "RED expected-author evaluation $author_eval_mutation $author_eval_mode" "$rc" 1 "$out" "MATCHED-GPR-AUTHOR-EVALUATION: 19 tests / $author_eval_losses failures / 0 errors; synthetic only"
    done <<'AUTHOR_EVALUATION_CASES'
author-freeze:6
current-inventory:12
review-agreement:1
frozen-scope:1
author-scope:12
manifest-reopen:2
derivation-selection:1
author-order:1
author-result-shape:8
author-fact-binding:9
author-status:3
author-finding:12
unsupported-credit:1
AUTHOR_EVALUATION_CASES
  done

  # P4-SYSTEM.14 a42t: finite source meaning and noncircular semantic authority.
  # a42at: one case with many predeclared properties (the m-forms case, 25 of them); each value held to the derivation.
  local source_property_mode source_property_mutation source_property_losses
  local -a source_property_python
  for source_property_mode in normal optimized; do
    source_property_python=(python3)
    [ "$source_property_mode" = optimized ] && source_property_python+=(-O)
    out="$("${source_property_python[@]}" scripts/probe_matched_gpr_property.py 2>&1)"; rc=$?
    score "GREEN finite source property $source_property_mode" "$rc" 0 "$out" "MATCHED-GPR-PROPERTY: 34 tests / 0 failures / 0 errors; synthetic metadata, finite source witnesses only"
    while IFS=: read -r source_property_mutation source_property_losses; do
      out="$("${source_property_python[@]}" scripts/probe_matched_gpr_property.py --mutation "$source_property_mutation" 2>&1)"; rc=$?
      score "RED finite source property $source_property_mutation $source_property_mode" "$rc" 1 "$out" "MATCHED-GPR-PROPERTY: 34 tests / $source_property_losses failures / 0 errors; synthetic metadata, finite source witnesses only"
    done <<'SOURCE_PROPERTY_CASES'
publication-authority:36
record-roundtrip:1
authority-string-bound:1
authority-byte-bound:1
context-scope:1
authority-shape:1
claim-count:1
claim-identity:1
claim-witness:1
control-claim:2
claim-binding:13
semantic-authority:9
relation-binding:6
normative-pin:6
guest-source:1
baseline-binding:1
witness-value:3
budget-binding:2
source-identity:5
reviewed-words:8
claim-values:3
authority-node-bound:1
authority-depth-bound:1
derived-status:2
derived-links:1
requirement-meaning:6
obligation-meaning:4
context-copy:7
claim-copy:6
source-fact-copy:1
authority-fact-copy:1
case-selection:2
source-unsupported:1
frozen-results:8
finite-finding:11
SOURCE_PROPERTY_CASES
  done

  # P4-SYSTEM.14 a42u: actual-property context and retained finite source findings.
  # a42at: one claim per declared property; the control's observed value must equal the source finding's (control-value).
  # a42av: the caller names the case the properties bind to (case-pass-through).
  local property_eval_mode property_eval_mutation property_eval_losses
  local -a property_eval_python
  for property_eval_mode in normal optimized; do
    property_eval_python=(python3)
    [ "$property_eval_mode" = optimized ] && property_eval_python+=(-O)
    out="$("${property_eval_python[@]}" scripts/probe_matched_gpr_property_evaluation.py 2>&1)"; rc=$?
    score "GREEN finite-property evaluation $property_eval_mode" "$rc" 0 "$out" "MATCHED-GPR-PROPERTY-EVALUATION: 25 tests / 0 failures / 0 errors; actual retained excerpt, synthetic observations, no capture credit"
    while IFS=: read -r property_eval_mutation property_eval_losses; do
      out="$("${property_eval_python[@]}" scripts/probe_matched_gpr_property_evaluation.py --mutation "$property_eval_mutation" 2>&1)"; rc=$?
      score "RED finite-property evaluation $property_eval_mutation $property_eval_mode" "$rc" 1 "$out" "MATCHED-GPR-PROPERTY-EVALUATION: 25 tests / $property_eval_losses failures / 0 errors; actual retained excerpt, synthetic observations, no capture credit"
    done <<'PROPERTY_EVALUATION_CASES'
author-prerequisite:1
obligation-bound:1
actual-statement:2
actual-requirement:1
actual-obligations:1
actual-program:1
property-order:1
property-finding:17
property-status:6
unsupported-credit:2
context-freeze:7
property-result-shape:18
property-fact-binding:19
actual-context-binding:1
case-pass-through:1
control-value:1
PROPERTY_EVALUATION_CASES
  done

  # P4-SYSTEM.14 a42v: real synthetic children, observed files and owned cleanup.
  local collector_mode collector_mutation collector_losses
  local -a collector_python
  for collector_mode in normal optimized; do
    collector_python=(python3)
    [ "$collector_mode" = optimized ] && collector_python+=(-O)
    out="$("${collector_python[@]}" scripts/probe_matched_gpr_collector.py 2>&1)"; rc=$?
    score "GREEN fresh process collector $collector_mode" "$rc" 0 "$out" "MATCHED-GPR-COLLECTOR: 25 tests / 0 failures / 0 errors; synthetic child processes, no Sail capture credit"
    while IFS=: read -r collector_mutation collector_losses; do
      out="$("${collector_python[@]}" scripts/probe_matched_gpr_collector.py --mutation "$collector_mutation" 2>&1)"; rc=$?
      score "RED fresh process collector $collector_mutation $collector_mode" "$rc" 1 "$out" "MATCHED-GPR-COLLECTOR: 25 tests / $collector_losses failures / 0 errors; synthetic child processes, no Sail capture credit"
    done <<'COLLECTOR_CASES'
physical-input-alias:1
physical-output-alias:1
exclusive-reservations:1
observation-mode:9
output-finding:1
request-freeze:1
owned-clear:14
pre-pins:9
post-pins:2
fixed-argv:1
output-alias:1
selected-outputs:1
special-output:1
nested-git:2
stream-bound:1
hard-file-bound:1
group-cleanup:1
deadline:1
COLLECTOR_CASES
  done

  # P4-SYSTEM.14 a42w: fresh receipt publication, including failed-process data.
  local publication_mode publication_mutation publication_losses
  local -a publication_python
  for publication_mode in normal optimized; do
    publication_python=(python3)
    [ "$publication_mode" = optimized ] && publication_python+=(-O)
    out="$("${publication_python[@]}" scripts/probe_matched_gpr_publication.py 2>&1)"; rc=$?
    score "GREEN fresh receipt publication $publication_mode" "$rc" 0 "$out" "MATCHED-GPR-PUBLICATION: 23 tests / 0 failures / 0 errors; synthetic process receipts, qualification closed"
    while IFS=: read -r publication_mutation publication_losses; do
      out="$("${publication_python[@]}" scripts/probe_matched_gpr_publication.py --mutation "$publication_mutation" 2>&1)"; rc=$?
      score "RED fresh receipt publication $publication_mutation $publication_mode" "$rc" 1 "$out" "MATCHED-GPR-PUBLICATION: 23 tests / $publication_losses failures / 0 errors; synthetic process receipts, qualification closed"
    done <<'PUBLICATION_CASES'
request-freeze:2
host-freeze:1
actual-exit:2
receipt-bound:1
byte-binding:2
pre-outputs:1
post-outputs:2
exclusive-write:1
partial-cleanup:4
cleanup-identity:1
receipt-pin:2
PUBLICATION_CASES
  done

  # P4-SYSTEM.14 a42x: three fresh processes, one conservative read allowance.
  local unit_capture_mode unit_capture_mutation unit_capture_losses
  local -a unit_capture_python
  for unit_capture_mode in normal optimized; do
    unit_capture_python=(python3)
    [ "$unit_capture_mode" = optimized ] && unit_capture_python+=(-O)
    out="$("${unit_capture_python[@]}" scripts/probe_matched_gpr_unit_collector.py 2>&1)"; rc=$?
    score "GREEN bounded unit collection $unit_capture_mode" "$rc" 0 "$out" "MATCHED-GPR-UNIT-COLLECTOR: 26 tests / 0 failures / 0 errors; synthetic unit processes, qualification closed"
    while IFS=: read -r unit_capture_mutation unit_capture_losses; do
      out="$("${unit_capture_python[@]}" scripts/probe_matched_gpr_unit_collector.py --mutation "$unit_capture_mutation" 2>&1)"; rc=$?
      score "RED bounded unit collection $unit_capture_mutation $unit_capture_mode" "$rc" 1 "$out" "MATCHED-GPR-UNIT-COLLECTOR: 26 tests / $unit_capture_losses failures / 0 errors; synthetic unit processes, qualification closed"
    done <<'UNIT_CAPTURE_CASES'
unit-freeze:1
unit-shared-limit:2
unit-charge:3
unit-accounting:2
unit-output-binding:1
unit-unique-pid:1
unit-failed-exit:2
unit-existing-output:12
unit-exclusive-reservations:1
unit-cleanup-identity:1
unit-cleanup-boundary:1
pin-charge:4
observation-charge:4
publication-process-charge:9
publication-read-charge:3
failed-pin-charge:1
UNIT_CAPTURE_CASES
  done

  # P4-SYSTEM.14 a42y: independently selected producer/data population.
  local div_review_mode div_review_mutation div_review_losses
  local -a div_review_python
  for div_review_mode in normal optimized; do
    div_review_python=(python3)
    [ "$div_review_mode" = optimized ] && div_review_python+=(-O)
    out="$("${div_review_python[@]}" scripts/probe_div_capture_review.py 2>&1)"; rc=$?
    score "GREEN DIV dependency review $div_review_mode" "$rc" 0 "$out" "DIV-CAPTURE-REVIEW: 31 tests / 0 failures / 0 errors; synthetic population controls, no capture credit"
    while IFS=: read -r div_review_mutation div_review_losses; do
      out="$("${div_review_python[@]}" scripts/probe_div_capture_review.py --mutation "$div_review_mutation" 2>&1)"; rc=$?
      score "RED DIV dependency review $div_review_mutation $div_review_mode" "$rc" 1 "$out" "DIV-CAPTURE-REVIEW: 31 tests / $div_review_losses failures / 0 errors; synthetic population controls, no capture credit"
    done <<'DIV_REVIEW_CASES'
module-population:2
dynamic-import:2
external-import:1
data-population:2
child-bound:1
symlink:2
git-boundary:1
file-bound:1
aggregate-bound:1
byte-recheck:2
retained-identity:3
publication-authority:2
retained-pin:1
authority-declaration:1
authority-preopen:1
authority-readonly:1
authority-view-pin:1
authority-process:1
DIV_REVIEW_CASES
  done

  # P4-SYSTEM.14 a42z: bounded licensed statement curation, no property/capture credit.
  local div_retention_mode div_retention_mutation div_retention_losses
  local -a div_retention_python
  for div_retention_mode in normal optimized; do
    div_retention_python=(python3)
    [ "$div_retention_mode" = optimized ] && div_retention_python+=(-O)
    out="$("${div_retention_python[@]}" scripts/probe_div_statement_retention.py 2>&1)"; rc=$?
    score "GREEN DIV statement retention $div_retention_mode" "$rc" 0 "$out" "DIV-STATEMENT-RETENTION: 20 tests / 0 failures / 0 errors; synthetic curation controls, no capture credit"
    while IFS=: read -r div_retention_mutation div_retention_losses; do
      out="$("${div_retention_python[@]}" scripts/probe_div_statement_retention.py --mutation "$div_retention_mutation" 2>&1)"; rc=$?
      score "RED DIV statement retention $div_retention_mutation $div_retention_mode" "$rc" 1 "$out" "DIV-STATEMENT-RETENTION: 20 tests / $div_retention_losses failures / 0 errors; synthetic curation controls, no capture credit"
    done <<'DIV_RETENTION_CASES'
input-pins:2
input-bounds:2
licence-statement:1
unique-statement:1
closing-span:1
span-bound:1
retained-bound:1
exact-span:4
retained-pin:1
DIV_RETENTION_CASES
  done

  # P4-SYSTEM.14 a42ab: delegate one allowance through manifest and evaluation.
  local allowance_mode allowance_mutation allowance_losses
  local -a allowance_python
  for allowance_mode in normal optimized; do
    allowance_python=(python3)
    [ "$allowance_mode" = optimized ] && allowance_python+=(-O)
    out="$("${allowance_python[@]}" scripts/probe_matched_gpr_read_allowance.py 2>&1)"; rc=$?
    score "GREEN delegated read allowance $allowance_mode" "$rc" 0 "$out" "MATCHED-GPR-READ-ALLOWANCE: 15 tests / 0 failures / 0 errors; actual bounded reads, synthetic observations, no capture credit"
    while IFS=: read -r allowance_mutation allowance_losses; do
      out="$("${allowance_python[@]}" scripts/probe_matched_gpr_read_allowance.py --mutation "$allowance_mutation" 2>&1)"; rc=$?
      score "RED delegated read allowance $allowance_mutation $allowance_mode" "$rc" 1 "$out" "MATCHED-GPR-READ-ALLOWANCE: 15 tests / $allowance_losses failures / 0 errors; actual bounded reads, synthetic observations, no capture credit"
    done <<'READ_ALLOWANCE_CASES'
evaluation-type:6
evaluation-domain:3
manifest-type:6
manifest-domain:3
initial-allowance:3
manifest-envelope:2
file-allowance:4
seed-double-charge:2
manifest-read-cap:5
manifest-extra-byte:4
READ_ALLOWANCE_CASES
  done

  # P4-SYSTEM.14 a42ac: bounded selected identity emission, no capture credit.
  local identity_emission_mode identity_emission_mutation identity_emission_losses
  local -a identity_emission_python
  for identity_emission_mode in normal optimized; do
    identity_emission_python=(python3)
    [ "$identity_emission_mode" = optimized ] && identity_emission_python+=(-O)
    out="$("${identity_emission_python[@]}" scripts/probe_reference_identity_emission.py 2>&1)"; rc=$?
    score "GREEN selected identity emission $identity_emission_mode" "$rc" 0 "$out" "REFERENCE-IDENTITY-EMISSION: 19 tests / 0 failures / 0 errors; synthetic descriptor metadata, no capture credit"
    while IFS=: read -r identity_emission_mutation identity_emission_losses; do
      out="$("${identity_emission_python[@]}" scripts/probe_reference_identity_emission.py --mutation "$identity_emission_mutation" 2>&1)"; rc=$?
      score "RED selected identity emission $identity_emission_mutation $identity_emission_mode" "$rc" 1 "$out" "REFERENCE-IDENTITY-EMISSION: 19 tests / $identity_emission_losses failures / 0 errors; synthetic descriptor metadata, no capture credit"
    done <<'IDENTITY_EMISSION_CASES'
context-type:2
context-shape:2
unknown-field:1
host-shape:1
metadata-type:16
text-bound:2
path-bound:3
canonical-fields:6
host-freeze:1
optional-emission:2
encoded-bound:2
round-trip:2
IDENTITY_EMISSION_CASES
  done

  # P4-SYSTEM.14 a42ad: fresh unit collection and evaluation share one allowance.
  local unit_eval_mode unit_eval_mutation unit_eval_losses
  local -a unit_eval_python
  for unit_eval_mode in normal optimized; do
    unit_eval_python=(python3)
    [ "$unit_eval_mode" = optimized ] && unit_eval_python+=(-O)
    out="$("${unit_eval_python[@]}" scripts/probe_matched_gpr_unit_evaluation.py 2>&1)"; rc=$?
    score "GREEN combined collection/evaluation $unit_eval_mode" "$rc" 0 "$out" "MATCHED-GPR-UNIT-EVALUATION: 30 tests / 0 failures / 0 errors; actual synthetic processes/read bytes, qualification closed"
    while IFS=: read -r unit_eval_mutation unit_eval_losses; do
      out="$("${unit_eval_python[@]}" scripts/probe_matched_gpr_unit_evaluation.py --mutation "$unit_eval_mutation" 2>&1)"; rc=$?
      score "RED combined collection/evaluation $unit_eval_mutation $unit_eval_mode" "$rc" 1 "$out" "MATCHED-GPR-UNIT-EVALUATION: 30 tests / $unit_eval_losses failures / 0 errors; actual synthetic processes/read bytes, qualification closed"
    done <<'UNIT_EVALUATION_CASES'
planned-bound:2
scope-envelope:2
scope-freeze:1
raw-schema:1
candidate-freeze:1
author-freeze:3
property-freeze:1
impact-freeze:1
collection-limit:2
collection-debit:5
captured-pid:1
captured-output:1
captured-charge:2
measured-bound:1
evaluation-limit:2
evaluation-debit:2
seed-accounting:1
evaluation-envelope:1
snapshot-envelope:1
failed-collection-refund:3
failed-evaluation-refund:2
attach-invalid-collection:15
attach-invalid-evaluation:13
structured-comments:2
unsupported-finding:1
case-forward:1
UNIT_EVALUATION_CASES
  done

  # P4-SYSTEM.14 a42ae: published selected descriptor, cache-free current binding.
  local retained_identity_mode
  local -a retained_identity_python
  for retained_identity_mode in normal optimized; do
    retained_identity_python=(python3)
    [ "$retained_identity_mode" = optimized ] && retained_identity_python+=(-O)
    out="$("${retained_identity_python[@]}" scripts/probe_retained_sail_identity.py 2>&1)"; rc=$?
    score "GREEN published Sail identity $retained_identity_mode" "$rc" 0 "$out" "RETAINED-SAIL-IDENTITY: 11 tests / 0 failures / 0 errors; published descriptor, offline, no capture credit"
  done

  # P4-SYSTEM.14 a42af: prepared finite DIV inputs, no reference process.
  # a42au: every reviewed case's prepared inputs (the retained case and the declared m-forms case), the family census at 43 / 32 MiB.
  local div_inputs_mode
  local -a div_inputs_python
  for div_inputs_mode in normal optimized; do
    div_inputs_python=(python3)
    [ "$div_inputs_mode" = optimized ] && div_inputs_python+=(-O)
    out="$("${div_inputs_python[@]}" scripts/probe_div_capture_inputs.py 2>&1)"; rc=$?
    score "GREEN prepared DIV capture inputs $div_inputs_mode" "$rc" 0 "$out" "DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors; prepared artifacts of every reviewed case, no reference process or capture credit"
    out="$("${div_inputs_python[@]}" scripts/probe_div_capture_inputs.py --mutation actual-layout 2>&1)"; rc=$?
    score "RED omitted actual DIV layout $div_inputs_mode" "$rc" 1 "$out" "DIV-CAPTURE-INPUTS: 34 tests / 6 failures / 0 errors; prepared artifacts of every reviewed case, no reference process or capture credit"
  done

  # P4-SYSTEM.14 a42ai: current semantic views, no capture or qualification.
  local div_authority_mode div_authority_mutation div_authority_losses
  local -a div_authority_python
  for div_authority_mode in normal optimized; do
    div_authority_python=(python3)
    [ "$div_authority_mode" = optimized ] && div_authority_python+=(-O)
    out="$("${div_authority_python[@]}" scripts/probe_div_authorities.py 2>&1)"; rc=$?
    score "GREEN current DIV authorities $div_authority_mode" "$rc" 0 "$out" "DIV-AUTHORITIES: 18 tests / 0 failures / 0 errors; current views, no capture credit"
    for div_authority_mutation in raw-validation registry-binding authority-binding; do
      div_authority_losses=3
      [ "$div_authority_mutation" = registry-binding ] && div_authority_losses=1
      out="$("${div_authority_python[@]}" scripts/probe_div_authorities.py --mutation "$div_authority_mutation" 2>&1)"; rc=$?
      score "RED omitted DIV authority $div_authority_mutation $div_authority_mode" "$rc" 1 "$out" "DIV-AUTHORITIES: 18 tests / $div_authority_losses failures / 0 errors; current views, no capture credit"
    done
  done

  # P4-SYSTEM.14 a42ak: copied command and synthetic execution, never Sail.
  local div_command_mode div_command_mutation div_command_losses
  local -a div_command_python
  for div_command_mode in normal optimized; do
    div_command_python=(python3)
    [ "$div_command_mode" = optimized ] && div_command_python+=(-O)
    out="$("${div_command_python[@]}" scripts/probe_div_command.py 2>&1)"; rc=$?
    score "GREEN composed DIV command $div_command_mode" "$rc" 0 "$out" "DIV-COMMAND: 19 tests / 0 failures / 0 errors; synthetic processes, no Sail or qualification"
    while IFS=: read -r div_command_mutation div_command_losses; do
      out="$("${div_command_python[@]}" scripts/probe_div_command.py --mutation "$div_command_mutation" 2>&1)"; rc=$?
      score "RED omitted DIV command $div_command_mutation $div_command_mode" "$rc" 1 "$out" "DIV-COMMAND: 19 tests / $div_command_losses failures / 0 errors; synthetic processes, no Sail or qualification"
    done <<'DIV_COMMAND_CASES'
native-declarations:6
authority-stability:1
retained-identity:1
planned-schema:1
author-delegation:2
impact-delegation:1
property-delegation:1
DIV_COMMAND_CASES
  done

  # P4-SYSTEM.14 a42aw: capture a declared case once and retain its results; synthetic processes, never Sail.
  local div_retention_mode div_retention_mutation div_retention_losses
  local -a div_retention_python
  for div_retention_mode in normal optimized; do
    div_retention_python=(python3)
    [ "$div_retention_mode" = optimized ] && div_retention_python+=(-O)
    out="$("${div_retention_python[@]}" scripts/probe_div_capture_retention.py 2>&1)"; rc=$?
    score "GREEN capture retention $div_retention_mode" "$rc" 0 "$out" "DIV-CAPTURE-RETENTION: 11 tests / 0 failures / 0 errors; synthetic processes, no Sail or qualification"
    while IFS=: read -r div_retention_mutation div_retention_losses; do
      out="$("${div_retention_python[@]}" scripts/probe_div_capture_retention.py --mutation "$div_retention_mutation" 2>&1)"; rc=$?
      score "RED omitted capture retention $div_retention_mutation $div_retention_mode" "$rc" 1 "$out" "DIV-CAPTURE-RETENTION: 11 tests / $div_retention_losses failures / 0 errors; synthetic processes, no Sail or qualification"
    done <<'DIV_RETENTION_CASES'
outputs-absent:1
declaration-regeneration:1
binary-identity:1
object-id:2
exclusive-publish:1
receipt-qualification:1
measured-pin:1
DIV_RETENTION_CASES
  done

  # P4-SYSTEM.14 a42ao: retained finite method, with no reference process. a42as: the deep arms run
  # against a synthetic current capture built in the copy, so every seam stays reachable while the
  # curated capture is invalidated; one real-tree arm asserts satisfied or stale as the manifest predicts.
  # a42ax: the fixture, the synthetic reference and the real-tree arm follow the review's retained case
  # (`review_div_method.RETAINED_CASE_ID`, the m-forms capture); the seam counts are unchanged.
  local div_method_mode div_method_mutation div_method_losses
  local -a div_method_python
  for div_method_mode in normal optimized; do
    div_method_python=(python3)
    [ "$div_method_mode" = optimized ] && div_method_python+=(-O)
    out="$("${div_method_python[@]}" scripts/probe_div_method.py 2>&1)"; rc=$?
    score "GREEN retained DIV method $div_method_mode" "$rc" 0 "$out" "DIV-METHOD: 21 tests / 0 failures / 0 errors; retained finite method, no Sail or policy credit"
    while IFS=: read -r div_method_mutation div_method_losses; do
      out="$("${div_method_python[@]}" scripts/probe_div_method.py --mutation "$div_method_mutation" 2>&1)"; rc=$?
      score "RED omitted DIV method $div_method_mutation $div_method_mode" "$rc" 1 "$out" "DIV-METHOD: 1 tests / $div_method_losses failures / 0 errors; retained finite method, no Sail or policy credit"
    done <<'DIV_METHOD_CASES'
declaration-binding:4
capture-origin:1
record-binding:4
influence-selection:2
finding-completeness:2
evaluation-selection:1
artifact-selection:2
typed-findings:1
shared-budget:3
evaluation-accounting:4
checker-census:1
checker-recheck:1
runtime-root:1
native-envelope:1
DIV_METHOD_CASES
  done

  # P4-SYSTEM.14 a42ap: requirement status derived from the evidence graph and drift-checked.
  # a42ay: a case is credited only through a current credit record (credits.sexp); a receipt's own
  # qualification is a finding (qualification-word seam); a lapsed record credits nothing (credit-pending).
  local status_mode status_mutation
  local -a status_python
  for status_mode in normal optimized; do
    status_python=(python3 -B)
    [ "$status_mode" = optimized ] && status_python+=(-O)
    out="$("${status_python[@]}" scripts/probe_requirement_status.py 2>&1)"; rc=$?
    score "GREEN requirement status derivation $status_mode" "$rc" 0 "$out" "REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors; derivation only, no qualification credit"
    for status_mutation in credit-pending ignore-drift skip-supersession unresolved-closes argument-optional unknown-case-credit qualification-word; do
      out="$("${status_python[@]}" scripts/probe_requirement_status.py --mutation "$status_mutation" 2>&1)"; rc=$?
      score "RED omitted requirement status $status_mutation $status_mode" "$rc" 1 "$out" "REQUIREMENT-STATUS-PROBE: 1 tests / 1 failures / 0 errors; derivation only, no qualification credit"
    done
  done

  # P4-SYSTEM.14 a42aq: the retained case's policy legs are measured; measurement grants no credit.
  # a42as: a stale finite method is `invalidated` with exit 0 (lock-stale seam); the real-tree arm
  # predicts pending or invalidated from the manifest, so a moved pinned input is not a refusal.
  # a42at: the discriminating-control leg reads the property the control_run names (first-property seam).
  # a42ax: the retained case is the m-forms capture; the real-tree arm asserts its ten legs satisfied and
  # `credited` false while every pin is current, `invalidated` missing the two method legs once one moves.
  local policy_mode policy_mutation
  local -a policy_python
  for policy_mode in normal optimized; do
    policy_python=(python3 -B)
    [ "$policy_mode" = optimized ] && policy_python+=(-O)
    out="$("${policy_python[@]}" scripts/probe_div_policy.py 2>&1)"; rc=$?
    score "GREEN policy legs measured $policy_mode" "$rc" 0 "$out" "DIV-POLICY-PROBE: 25 tests / 0 failures / 0 errors; measurement only, no qualification credit"
    for policy_mutation in credit-pending trust-receipt infer-feature any-control coverage-optional lock-stale first-property credit-any; do
      out="$("${policy_python[@]}" scripts/probe_div_policy.py --mutation "$policy_mutation" 2>&1)"; rc=$?
      score "RED omitted policy legs $policy_mutation $policy_mode" "$rc" 1 "$out" "DIV-POLICY-PROBE: 1 tests / 1 failures / 0 errors; measurement only, no qualification credit"
    done
  done

  printf 'PROFILE-CONSISTENCY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

# The curated source is tracked: its pin check must not depend on acquired pages.
div_retained_result="$(python3 scripts/retain_div_statement.py --verify 2>&1)"; div_retained_rc=$?
if [ "$div_retained_rc" -ne 0 ]; then
  printf 'PROFILE-CONSISTENCY: retained DIV statement refused: %s\n' "$div_retained_result" >&2
  exit 1
fi

# P4-SYSTEM.14 a42ap: every policy-declaring profile's recorded requirement statuses equal their
# derivation from the evidence graph (EVIDENCE_POLICY.md "Status and supersession").
status_result="$(python3 -B scripts/requirement_status.py 2>&1)"; status_rc=$?
if [ "$status_rc" -ne 0 ]; then
  { echo "PROFILE-CONSISTENCY: a recorded requirement status drifts from its derivation, or the graph refuses."
    printf '%s\n' "$status_result" | sed 's/^/  /'
    echo "  The GRAPH is authoritative: change the evidence or the catalogue record, never the status alone."; } >&2
  exit "$status_rc"
fi

# P4-SYSTEM.14 a42aq: the retained DIV case's policy legs are measured from its own bytes; a receipt
# claiming qualification the legs refuse, or a refused/unavailable/unsupported finite method, fails
# the gate. A stale method — a pinned input moved — is `invalidated`, exit 0, the moved declaration
# named (a42as, the director's ruling of 2026-10-22): a status of the evidence, not a lock. No credit.
policy_result="$(python3 -B scripts/review_div_policy.py 2>&1)"; policy_rc=$?
if [ "$policy_rc" -ne 0 ]; then
  { echo "PROFILE-CONSISTENCY: the retained case's policy legs refuse its receipt, or cannot be measured."
    printf '%s\n' "$policy_result" | sed 's/^/  /'
    echo "  The LEGS are measured from declared bytes: predeclare and capture, never relabel a receipt."; } >&2
  exit "$policy_rc"
fi

# P4-SYSTEM.2 slice (c1): probe the csr-set rule against a staged state document at a
# scratch path (the rv64gc unit's own state.sexp is a route contradiction until the flip).
[ "${1:-}" = "--csr-cross" ] && { check_profiles "$@"; exit $?; }

[ -d profiles ] || { echo "PROFILE-CONSISTENCY: ok (no profiles/ yet)"; exit 0; }
# The self-test's output is KEPT (a42ax, 2026-10-23): two gate refusals (2026-10-21, 2026-10-23) had
# discarded the MISS lines that name the failing arm, and neither reproduced from the shell.
selftest_log="$ROOT/target/profile-consistency-selftest.log"
mkdir -p "$ROOT/target"
self_test >"$selftest_log" 2>&1 || {
  { echo "PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed)."
    grep -n -A3 "self-test MISS" "$selftest_log" | head -40 | sed 's/^/  /'
    echo "  the self-test's complete output is kept at target/profile-consistency-selftest.log"; } >&2
  exit 2; }

out="$(check_profiles profiles)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -ne 0 ]; then
  { echo "PROFILE-CONSISTENCY: a profile dossier contradicts itself or cites nothing."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The SOURCE is authoritative: fix the enumeration, the citation or the evidence —"
    echo "  never the summary alone to make the two agree."; } >&2
  exit 1
fi
printf 'PROFILE-CONSISTENCY: ok (%s profile dossier(s) internally consistent)\n' "${count:-0}"
exit 0
