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
#      and a *comparison* never seen to diverge is not known to detect divergence. An
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
        # P4-SYSTEM.7 slice (c6): + f_single 30 = 118; slice (d5): + d_double 32 = 150)
        a, b = scope.get("count_base"), scope.get("count_rv64i_additions")
        if a is not None and b is not None and declared is not None:
            ext = sum(len(scope.get(k) or [])
                      for k in ("zicsr_csrs", "system_privileged", "zicntr_counters",
                                "a_atomics", "zifencei_fencei", "f_single", "d_double"))
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
            for x in rf.get("experiment", []):
                xid = x.get("id", "<unnamed>")
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
                if len(pair) != 2:
                    findings.append(
                        f"BAD PAIR   {name}/{label}: an independence record names "
                        f"{len(pair)} model(s); independence is a property of a PAIR")
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
  printf 'PROFILE-CONSISTENCY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

# P4-SYSTEM.2 slice (c1): probe the csr-set rule against a staged state document at a
# scratch path (the rv64gc unit's own state.sexp is a route contradiction until the flip).
[ "${1:-}" = "--csr-cross" ] && { check_profiles "$@"; exit $?; }

[ -d profiles ] || { echo "PROFILE-CONSISTENCY: ok (no profiles/ yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

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
