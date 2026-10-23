#!/usr/bin/env bash
# scripts/check_requirements.sh — RECORD-SCHEMA (project doctrine).
#
# `schemas/` holds this project's data contracts and `EVD-01` makes machine-readable requirement,
# evidence and obligation records the spine of traceability. A record file that has drifted from
# its schema, or that cites a source the project never pinned, is worse than no catalogue: it is a
# catalogue that looks checkable and is not.
#
# Two tracks, since `SOT-FORMAT.3` moved the profile catalogues behind the schema layer:
#
#   JSONL — every tracked `.jsonl` record file validates against its declared JSON schema
#           (the frozen `examples/` delivery artifacts stay JSONL on purpose), on TWO engines:
#           the tracked Python validator below, AND the workspace's own Rust checker
#           (`semulith check-examples`, P1-LAB.7) once the Python phase is green — the
#           PACKAGE_CHECKS schema results re-derived in Rust (RUST-01), never only cited.
#           Power: structural.
#   SEXP  — every `requirements.sexp` / `contract-obligations.sexp` catalogue validates against
#           its schema-layer schema (`schema/requirements.sexp`, `schema/contract-obligations.sexp`)
#           AND carries the cross-checks, now read through scripts/records_sexp.py:
#     2. CITED      every `source_refs.source_id` names a source the profile's `sources.sexp` pins.
#                   `SRC-03` again, one layer up: a locator into a document nobody acquired is
#                   not a citation.
#     3. RESOLVED   a record claiming `research_status: resolved` may not also carry an `OPEN:` note.
#                   ⭐ "Resolved with a known open question" is the single most convenient lie a
#                   requirements catalogue can tell, because both halves are individually true.
#     4. COVERAGE   every (decision …) in `profile.sexp` has a requirement, and the requirement's
#                   statement is IDENTICAL to the decision's. Two files stating the same rule in
#                   different words is how a catalogue quietly stops describing its profile.
#     5. LINKED     every id in `dependencies` names a record that exists in the same file.
#     6. OBLIGED    every `obligation_ids` entry names an obligation the profile's contract defines,
#                   and every obligation carries BOTH a positive and a negative required check.
#                   ⭐ Positive-only checks are how a contract comes to describe only the cases
#                   that already work: `docs/CPU_ENVIRONMENT.md` §4 asks for negative fixtures that
#                   must be reported as CONTRACT VIOLATIONS rather than target exceptions.
#     7. AUTHORITY  an obligation whose requirement is architecturally `defined` must itself carry
#                   `authority: architecture`. ⛔ This is the mechanical form of the contract's
#                   first rule — *laboratory policy cannot override an architectural requirement* —
#                   and it bites in the direction that matters: labelling an ISA rule as a harness
#                   choice is what turns a defect into a "profile difference" and makes it
#                   unfalsifiable.
#     8. UNIQUE-ID  a catalogue may not carry two records with the same id. Found by SOT-FORMAT.5
#                   (design probe, `target/doctrine_scratch/dupprobe`): the id → record map used
#                   for the cross-checks silently collapsed duplicates (last wins), so a catalogue
#                   could contradict itself — same id, different content — and stay green, rc=0.
#                   A catalogue that repeats an id is a catalogue lying about its own identity,
#                   and every rule below would have checked only the survivor.
#     9. MIRROR     an obligation carrying parameters.requirement_id restates that requirement's
#                   statement, so the pair must state EXACTLY the same fact — the obligation is a
#                   derived mirror, and a mirror that drifts is a fact stated in two ungoverned
#                   (MODEL-METHOD.7). An unchanged frozen mirror may instead resolve through
#                   authenticated version supersession to a current mirror of that requirement.
#                   The arm keys on the parameter, not the direction.
#    10. UNITS       the modelled-unit registry (materials/units.sexp) is never empty — a census
#                   over no units is a claim about nothing (MODEL-METHOD.2).
#    11. LAYERS      a category-need dispositioned `missing` owes a reason, a `covered` row names
#                   its material, and a board-layer category may not be `missing` for a processor
#                   unit — `missing` means the unit REQUIRED it; the honest words for never-needed
#                   is `out-of-scope`, and for P5-BOARD's categories `deferred-to-board`
#                   (MODEL-METHOD.2/3). Checked against the units registry beside the catalogue:
#                   layer claims without a registry prove nothing.
#    12. MATERIAL    a category-need naming a `material` names one catalog.sexp actually holds —
#                   a covered-by that names no document is the same lie as a citation into a
#                   document nobody acquired (MODEL-METHOD.3).
#    13. CAMPAIGN    the ACT4 external-campaign record (profiles/*/act4.sexp) carries only
#                   counts its own rows re-derive, and its verdict vocabulary is closed —
#                   a recorded experiment whose summary disagrees with its rows is a catalogue
#                   lying about its own census (P2-SCALAR.5).
#    14. MIRROR-DERIVE a `base-requirements (UNIT)` / `base-obligations (UNIT)` row in
#                   doctrine/fact_ownership.tsv registers that UNIT's base-corpus records are
#                   byte-verbatim DERIVED mirrors of the owner unit's catalogue (P4-SYSTEM.2
#                   slice e — the rv64gc base corpus derives from rv64i's); the mirrored set is
#                   re-derived (the owner's base-covering records + their dependency closure),
#                   every shared field must be equal, the profile-scoped fields must name the
#                   mirror's unit, and an authored base record outside the closure is refused.
#
# ✅ The gap `P0-PROFILE.3` declared here — obligation ids checked against nothing — is CLOSED by
# rules 6 and 7, which `P0-PROFILE.4` added along with the contract that defines them.
#
# ⛔ Both validators REFUSE rather than guess: the JSON one on any keyword it does not implement;
# the schema layer by name on an undeclared construct, field, arity, value type or FACET
# (pattern / min-length / min / unique — SOT-FORMAT.3). A schema gaining power breaks the gate
# loudly rather than silently widening what passes.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "RECORD-SCHEMA: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_records() {
python3 - "$1" <<'PY'
import hashlib, json, pathlib, sys
sys.path.insert(0, "scripts")
from validate_records import validate_jsonl, UnsupportedSchema
import sexp as S
import records_sexp as R
import record_catalog as C
import dossier_sexp as D
import check_sexp_schema as K

root = pathlib.Path(sys.argv[1])
findings, checked = [], []

# which JSON schema governs which JSONL record file, by basename
SCHEMA_FOR = {
    "requirements.jsonl": "requirement.schema.json",
    "evidence.jsonl": "evidence.schema.json",
    "contract-obligations.jsonl": "contract-obligation.schema.json",
}
# which schema-layer schema governs which converted catalogue, by basename
SEXP_SCHEMA_FOR = {
    "requirements.sexp": "schema/requirements.sexp",
    "contract-obligations.sexp": "schema/contract-obligations.sexp",
    "credits.sexp": "schema/credits.sexp",
    "units.sexp": "schema/units.sexp",
    "category-needs.sexp": "schema/category-needs.sexp",
    "act4.sexp": "schema/act4.sexp",
}
ARCH_AUTHORITY = "architecture"

def frozen_mirror_replacement(cat, obs, original):
    """Resolve a pinned historical mirror; every other mismatch stays a rejection.

    CONTRACT-FREEZE owns the complete version inventory. This narrow check independently
    authenticates the historical bytes and the active inheritance/supersession route before
    allowing a historical statement to differ from its requirement's current statement.
    """
    manifest = cat.parent / "contract.sexp"
    if not manifest.is_file():
        raise ValueError("no version manifest")
    schema = root / "schema/contract.sexp"
    constructs, operators = K.load_schema(schema)
    text = manifest.read_text()
    if K.validate_text(text, constructs, operators, str(manifest)):
        raise ValueError("invalid version manifest")
    versions, numbers, owners = {}, set(), {}
    for form in S.parse(text, str(manifest)):
        if S.head(form) != "contract":
            continue
        vid, number = S.field(form, "id"), int(S.field(form, "version"))
        if vid in versions or number in numbers:
            raise ValueError("ambiguous version identity")
        numbers.add(number)
        members = {}
        for member in S.children(form, "member"):
            oid = S.field(member, "id")
            if oid in owners:
                raise ValueError("record has multiple version owners")
            owners[oid] = vid
            pins = S.children(member, "sha256")
            members[oid] = pins[0][1] if pins else None
        parent = S.children(form, "extends")
        versions[vid] = dict(number=number, status=S.field(form, "status"),
                             parent=parent[0][1] if parent else None,
                             members=members, supers=S.children(form, "supersede"))
    if not versions:
        raise ValueError("no declared versions")
    oid = original["id"]
    owner = owners.get(oid)
    if owner is None or versions[owner]["status"] != "frozen":
        raise ValueError("historical mirror is not frozen")
    if (original["contract_id"], int(original["contract_version"])) != (
            owner, versions[owner]["number"]):
        raise ValueError("historical mirror belongs to another version")
    lines = [line for line in C.text(cat.parent / "contract-obligations.sexp",
                                    root=root).splitlines()
             if line.startswith(f'(obligation (id "{oid}") ')]
    if len(lines) != 1 or hashlib.sha256(lines[0].encode()).hexdigest() != \
            versions[owner]["members"][oid]:
        raise ValueError("historical mirror does not match its frozen pin")
    chain, current = [], max(versions, key=lambda key: versions[key]["number"])
    while current is not None:
        if current not in versions or current in chain:
            raise ValueError("broken version inheritance")
        chain.append(current)
        parent = versions[current]["parent"]
        if parent is not None and (parent not in versions or
                versions[parent]["number"] + 1 != versions[current]["number"]):
            raise ValueError("broken version inheritance")
        current = parent
    if owner not in chain:
        raise ValueError("historical mirror is outside the active version chain")
    effective, redirects = set(), {}
    by_ob = {o["id"]: o for o in obs}
    for vid in reversed(chain):
        version = versions[vid]
        own = set(version["members"])
        for member in own:
            record = by_ob.get(member)
            if record is None or (record["contract_id"], int(record["contract_version"])) != (
                    vid, version["number"]):
                raise ValueError("version member has no matching record")
        for supersede in version["supers"]:
            old, new = S.field(supersede, "record"), S.field(supersede, "by")
            if old not in effective or new not in own or old in redirects:
                raise ValueError("invalid historical-mirror supersession")
            effective.remove(old)
            redirects[old] = new
        effective.update(own)
    replacement = oid
    while replacement in redirects:
        replacement = redirects[replacement]
    if replacement == oid or replacement not in effective:
        raise ValueError("no effective replacement for the historical mirror")
    record = by_ob[replacement]
    if (record.get("parameters") or {}).get("requirement_id") != \
            (original.get("parameters") or {}).get("requirement_id"):
        raise ValueError("replacement does not mirror the same requirement")
    return record

# ⛔ Exclude `target/` only when it is the FIRST component RELATIVE TO ROOT (the self-test
# fixtures live under target/doctrine-selftest/, and an absolute-path test would filter every
# fixture away and fail the arms with "nothing found"). `vendor` joins it for the same reason
# and a sharper one: a vendored submodule is ANOTHER PROJECT'S tree.
def _excluded(p):
    rel = p.relative_to(root).parts
    return bool(rel) and rel[0] in ("target", "vendor")

# ---------------------------------------------------------------- the JSONL track (unchanged)
jsonl_files = sorted(p for p in root.rglob("*.jsonl") if not _excluded(p))
for rf in jsonl_files:
    schema_name = SCHEMA_FOR.get(rf.name)
    if schema_name is None:
        findings.append(f"UNGOVERNED {rf}: no schema is declared for this record file")
        continue
    schema = root / "schemas" / schema_name
    if not schema.is_file():
        findings.append(f"NO SCHEMA  {rf}: {schema} does not exist")
        continue
    checked.append(str(rf.relative_to(root)))
    try:
        for err in validate_jsonl(rf, schema):
            findings.append(f"INVALID    {err}")
    except UnsupportedSchema as exc:
        print(f"UNSUPPORTED {exc}"); print("__CHECKED__ 0"); sys.exit(2)

# ------------------------------------------------------- the SEXP track (the profile records)
# A file named requirements.sexp / contract-obligations.sexp is a catalogue everywhere EXCEPT
# under schema/ — the schemas themselves carry the same basenames, and judging a schema as its
# own target is how a gate reports its own grammar as a records violation.
schema_dir = root / "schema"
catalogues = sorted({p for name in SEXP_SCHEMA_FOR for p in root.rglob(name)
                     if not _excluded(p) and schema_dir not in p.parents})
if not jsonl_files and not catalogues:
    print("NO RECORDS no .jsonl record file and no converted catalogue found — "
          "this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

for cat in catalogues:
    schema_rel = SEXP_SCHEMA_FOR[cat.name]
    schema = root / schema_rel
    if not schema.is_file():
        findings.append(f"NO SCHEMA  {cat}: {schema} does not exist")
        continue
    checked.append(str(cat.relative_to(root)))
    # 1. SCHEMA — the schema layer refuses by name: undeclared construct/field, wrong arity,
    #    wrong value type, and every FACET the record contracts carry.
    try:
        constructs, operators = K.load_schema(schema)
    except (K.SchemaError, S.SexpError) as exc:
        print(f"UNSUPPORTED {schema_rel}: {exc}"); print("__CHECKED__ 0"); sys.exit(2)
    try:
        sources = {}
        C.text(cat, root=root, source_texts=sources)
        errors = []
        for source, text in sources.items():
            errors += K.validate_text(text, constructs, operators,
                                      source.relative_to(root.resolve()).as_posix(),
                                      parse_where=str(source))
    except (C.CatalogRefused, S.SexpError) as exc:
        findings.append(f"INVALID    {cat.relative_to(root)}: does not even parse or expand: {exc}")
        continue
    for e in errors:
        findings.append(f"INVALID    {e}")
    if errors:
        continue                    # a catalogue the layer refuses cannot be cross-checked

    if cat.name == "act4.sexp":
        # 13. CAMPAIGN — the ACT4 external-campaign record (P2-SCALAR.5 strand 2) is a
        # RECORDED experiment: its inputs are untracked, so the gate re-derives every
        # carried count from the rows (a count that disagrees with its own rows is the
        # record lying about its own census) and confines the verdict vocabulary. The
        # schema has already pinned the structure, so navigation is field-by-name.
        def _field(f, name):
            for c in f[1:]:
                if isinstance(c, list) and c and str(c[0]) == name:
                    return c
            return None
        def _val(f, name):                      # the single value of an atom field
            c = _field(f, name)
            return c[1] if c is not None and len(c) == 2 else None
        forms = [f for f in S.read_file(cat)
                 if not (isinstance(f, list) and f and str(f[0]) == "comment")]
        root_form = forms[0] if len(forms) == 1 else None
        rows = [c for c in (root_form or [None])[1:]
                if isinstance(c, list) and c and str(c[0]) == "test"]
        run_f = _field(root_form, "run") if root_form else None
        if root_form is None or str(root_form[0]) != "act4-campaign" or run_f is None:
            findings.append(f"CAMPAIGN ROOT {cat.name}: no single act4-campaign form "
                            f"with a run block")
            continue
        seen_files = set()
        for r in rows:
            fn = _val(r, "file")
            if fn in seen_files:
                findings.append(f"CAMPAIGN DUPLICATE {cat.name}: test file '{fn}' "
                                f"appears twice")
            seen_files.add(fn)
            for k in ("verdict_semulith", "verdict_sail", "verdict_spike"):
                if str(_val(r, k)) not in ("pass", "fail"):
                    findings.append(f"CAMPAIGN VOCABULARY {cat.name} [{fn}]: {k} is "
                                    f"'{_val(r, k)}', not pass|fail")
            for k in ("signature", "control"):
                if str(_val(r, k)) not in ("agree", "mismatch"):
                    findings.append(f"CAMPAIGN VOCABULARY {cat.name} [{fn}]: {k} is "
                                    f"'{_val(r, k)}', not agree|mismatch")
        if int(_val(run_f, "tests")) != len(rows):
            findings.append(f"CAMPAIGN COUNT {cat.name}: run.tests = "
                            f"{_val(run_f, 'tests')} but the record carries {len(rows)} "
                            f"test row(s)")
        slots = sum(int(_val(r, "signature_slots")) for r in rows)
        if int(_val(run_f, "signature_slots")) != slots:
            findings.append(f"CAMPAIGN SLOTS {cat.name}: run.signature_slots = "
                            f"{_val(run_f, 'signature_slots')} but the rows carry {slots}")
        passed = sum(1 for r in rows
                     if str(_val(r, "verdict_semulith")) == "pass"
                     and str(_val(r, "verdict_sail")) == "pass"
                     and str(_val(r, "verdict_spike")) == "pass"
                     and str(_val(r, "signature")) == "agree"
                     and str(_val(r, "control")) == "agree")
        derived = f"{passed} pass / {len(rows) - passed} fail"
        if str(_val(run_f, "verdicts")) != derived:
            findings.append(f"CAMPAIGN VERDICTS {cat.name}: run.verdicts = "
                            f"'{_val(run_f, 'verdicts')}' but the rows derive "
                            f"'{derived}'")
        continue
    try:
        recs = R.load(cat, root=root)
    except (R.RecordRefused, S.SexpError) as exc:
        findings.append(f"UNREADABLE {cat.relative_to(root)}: conforms to its schema but does "
                        f"not map to records — {exc}")
        continue
    if not recs:
        findings.append(f"INVALID    {cat.relative_to(root)}: contains no records — an empty "
                        f"catalogue is not a valid one")
        continue
    # 8. UNIQUE-ID — the cross-checks index records by id; a duplicate silently collapses
    #    (last wins) and every rule below would check only the survivor. Refuse, naming both.
    #    Category-need records key on (category, unit) — they carry no id field.
    by_id: dict = {}
    for r in recs:
        rid = r.get("id") or (r.get("category"), r.get("unit"))
        if rid in by_id:
            findings.append(
                f"DUPLICATE ID {cat.relative_to(root)}: record '{rid}' appears more than "
                f"once — a catalogue that contradicts itself cannot be checked; the later "
                f"record silently overwrote the earlier one")
        else:
            by_id[rid] = r

    if cat.name == "requirements.sexp":
        # 2. CITED — beside a profile's sources.sexp (`SOT-FORMAT.4`: read via the mapping)
        sources_sexp = cat.parent / "sources.sexp"
        if sources_sexp.is_file():
            try:
                pinned = {s["id"] for s in D.load_sources(sources_sexp).get("source", [])}
            except D.DossierError:
                pinned = None
            if pinned is None:
                findings.append(
                    f"UNREADABLE {sources_sexp.name}: the pinned-source ledger does not map — "
                    f"a catalogue citing documents a ledger nobody can read proves nothing")
            else:
                for r in recs:
                    for sr in r.get("source_refs", []):
                        if sr["source_id"] not in pinned:
                            findings.append(
                                f"UNPINNED SOURCE {cat.name} [{r['id']}]: cites "
                                f"'{sr['source_id']}', which {sources_sexp.name} does not pin — "
                                f"a locator into a document nobody acquired is not a citation")
        for r in recs:
            # 3. RESOLVED
            detail = (r.get("source_semantics") or {}).get("detail", "")
            if r.get("research_status") == "resolved" and "OPEN:" in detail:
                findings.append(
                    f"RESOLVED WITH AN OPEN QUESTION {cat.name} [{r['id']}]: research_status "
                    f"is 'resolved' and the record still carries an OPEN note. Both halves can "
                    f"be true separately; together they are a catalogue lying about its own "
                    f"completeness")
            # 5. LINKED
            for dep in r.get("dependencies", []):
                if dep not in by_id:
                    findings.append(
                        f"DANGLING DEP {cat.name} [{r['id']}]: depends on '{dep}', which no "
                        f"record in this file defines")

        # 6 + 7. OBLIGED / AUTHORITY — against the contract in the same PROFILE directory
        ob_file = cat.parent / "contract-obligations.sexp"
        if ob_file.is_file() and (cat.parent / "profile.sexp").is_file():
            try:
                obs = R.load(ob_file, root=root)
            except (R.RecordRefused, S.SexpError):
                obs = None
            if obs is not None:
                by_ob = {o.get("id"): o for o in obs}
                for o in obs:
                    checks = o.get("required_checks", [])
                    if not any(c.endswith("-POS") for c in checks) or \
                       not any(c.endswith("-NEG") for c in checks):
                        findings.append(
                            f"NO NEGATIVE CHECK contract-obligations.sexp [{o.get('id')}]: "
                            f"required_checks {checks} lack a positive AND a negative fixture — "
                            f"a contract with only positive checks describes the cases that "
                            f"already work")
                for r in recs:
                    for oid in r.get("obligation_ids", []):
                        o = by_ob.get(oid)
                        if o is None:
                            findings.append(
                                f"UNDEFINED OBLIGATION {cat.name} [{r['id']}]: names '{oid}', "
                                f"which contract-obligations.sexp does not define")
                            continue
                        cat_ = (r.get("source_semantics") or {}).get("category")
                        if cat_ == "defined" and o.get("authority") != ARCH_AUTHORITY:
                            findings.append(
                                f"AUTHORITY DOWNGRADE contract-obligations.sexp [{oid}]: its "
                                f"requirement '{r['id']}' is architecturally 'defined', but the "
                                f"obligation claims authority '{o.get('authority')}'. Laboratory "
                                f"policy cannot override an architectural requirement, and "
                                f"mislabelling one is how a defect becomes an unfalsifiable "
                                f"'profile difference'")
                # 9. MIRROR — an obligation that names its requirement restates it; the two must
                #    state the same fact (MODEL-METHOD.7). Keyed on the obligation's own
                #    parameter, not the direction: environment-assumptions keep their statements.
                for o in obs:
                    mirror_rid = (o.get("parameters") or {}).get("requirement_id")
                    if not mirror_rid:
                        continue
                    r = by_id.get(mirror_rid)
                    # Rule 7 also follows explicit mirrors: a versioned replacement
                    # may not be listed in the requirement's historical obligation_ids.
                    if (r is not None
                            and o.get("id") not in r.get("obligation_ids", [])
                            and (r.get("source_semantics") or {}).get("category") == "defined"
                            and o.get("authority") != ARCH_AUTHORITY):
                        findings.append(
                            f"AUTHORITY DOWNGRADE contract-obligations.sexp [{o.get('id')}]: "
                            f"its explicit requirement mirror '{mirror_rid}' is architecturally "
                            f"'defined', but the obligation claims authority '{o.get('authority')}'")
                    if r is None:
                        findings.append(
                            f"MIRROR WITHOUT SOURCE contract-obligations.sexp [{o.get('id')}]: "
                            f"names '{mirror_rid}' as its requirement, which "
                            f"{cat.name} does not define — a mirror of nothing")
                    elif o.get("statement") != r.get("statement"):
                        try:
                            replacement = frozen_mirror_replacement(cat, obs, o)
                            if replacement.get("statement") == r.get("statement"):
                                continue
                            reason = "effective replacement also drifts"
                        except (ValueError, OSError, K.SchemaError, S.SexpError,
                                C.CatalogRefused) as error:
                            reason = str(error)
                        findings.append(
                            f"MIRROR DRIFT contract-obligations.sexp [{o.get('id')}]: names "
                            f"'{mirror_rid}' as its requirement but states a different fact. "
                            f"An obligation is a derived mirror of its requirement; a mirror "
                            f"that drifts is one fact stated two ways ({reason})")

        # 4. COVERAGE — against the profile this catalogue belongs to
        prof = cat.parent / "profile.sexp"
        if prof.is_file():
            try:
                decisions = D.load_profile(prof).get("decision", [])
            except D.DossierError:
                decisions = None
            if decisions is None:
                findings.append(
                    f"UNREADABLE {prof.name}: the profile's decisions do not map — coverage "
                    f"against a dossier nobody can read proves nothing")
            else:
                for dec in decisions:
                    rid = f"REQ-{dec['id']}"
                    if rid not in by_id:
                        findings.append(
                            f"UNCOVERED DECISION {cat.name}: profile.sexp decision '{dec['id']}' "
                            f"has no requirement '{rid}'")
                    elif by_id[rid].get("statement") != dec.get("statement"):
                        findings.append(
                            f"STATEMENT DRIFT {cat.name} [{rid}]: the requirement no longer "
                            f"states what profile.sexp's '{dec['id']}' states")

    elif cat.name == "units.sexp":
        if not recs:
            findings.append(f"EMPTY REGISTRY {cat.relative_to(root)}: the modelled-unit "
                            f"registry carries no unit — a census over nothing")

    elif cat.name == "category-needs.sexp":
        # MODEL-METHOD.2: layer × disposition honesty. A `missing` row means the unit REQUIRES
        # the category (so a reason is owed); a board-layer category dispositioned `missing`
        # for a processor unit is a lie about what was required — the unit never owed
        # board-layer information, and the honest word is `out-of-scope`.
        unit_kinds: dict[str, str] = {}
        units_path = cat.parent / "units.sexp"
        if units_path.is_file():
            try:
                unit_kinds = {u.get("id"): u.get("kind") for u in R.load(units_path, root=root)}
            except (R.RecordRefused, S.SexpError):
                findings.append(
                    f"UNREADABLE {units_path.name}: the unit registry beside {cat.name} does "
                    f"not map — layer checks against a registry nobody can read prove nothing")
        else:
            findings.append(
                f"NO REGISTRY {cat.relative_to(root)}: no units.sexp beside {cat.name} — "
                f"layer dispositions cannot be checked without the registry they describe")
        material_ids: set[str] = set()
        catalog_path = cat.parent / "catalog.sexp"
        if catalog_path.is_file():
            try:
                cat_root = S.read_file(catalog_path)[0]
                material_ids = {str(S.field(m, "id"))
                                for m in S.children(cat_root, "material")}
            except (S.SexpError, IndexError):
                findings.append(
                    f"UNREADABLE {catalog_path.name}: the materials catalogue beside "
                    f"{cat.name} does not map — material references against a catalogue "
                    f"nobody can read prove nothing")
        else:
            findings.append(
                f"NO CATALOGUE {cat.relative_to(root)}: no catalog.sexp beside {cat.name} "
                f"— material references cannot be resolved without the catalogue they name")
        for r in recs:
            where = f"{cat.name} [{r.get('category')} for {r.get('unit')}]"
            kind = r.get("disposition")
            if kind == "missing":
                if not r.get("reason"):
                    findings.append(
                        f"REASONLESS MISSING {where}: disposition 'missing' claims the unit "
                        f"requires this category — say why it is owed and absent")
                if r.get("layer") == "board" and \
                        unit_kinds.get(r.get("unit")) == "processor":
                    findings.append(
                        f"LAYER LIE {where}: a board-layer category dispositioned 'missing' "
                        f"for a processor unit — the unit never owed board-layer information. "
                        f"The honest disposition is 'deferred-to-board' (P5-BOARD owns it and "
                        f"the CPU records an assumption in its place) or 'out-of-scope'; "
                        f"'missing' smuggles a requirement in through the back door")
            if kind == "covered" and not r.get("material"):
                findings.append(
                    f"UNEVIDENCED COVERED {where}: disposition 'covered' names no material — "
                    f"covered by WHAT?")
            # 12. MATERIAL: a row naming a material names one the catalogue actually holds —
            #    a covered-by that names nothing is the same lie as a citation into a document
            #    nobody acquired (MODEL-METHOD.3).
            if r.get("material") and r["material"] not in material_ids:
                findings.append(
                    f"UNRESOLVED MATERIAL {where}: names '{r['material']}', which "
                    f"catalog.sexp does not hold — covered by a document nobody acquired is "
                    f"not covered")

    else:  # contract-obligations.sexp — the NO NEGATIVE CHECK arm is fired standalone too
        for o in recs:
            checks = o.get("required_checks", [])
            if not any(c.endswith("-POS") for c in checks) or \
               not any(c.endswith("-NEG") for c in checks):
                findings.append(
                    f"NO NEGATIVE CHECK {cat.name} [{o.get('id')}]: required_checks {checks} "
                    f"lack a positive AND a negative fixture")

# ---- 14. MIRROR-DERIVE — the base-corpus mirrors, registry-driven (P4-SYSTEM.2 slice e) ------
# doctrine/fact_ownership.tsv's `base-requirements (UNIT)` / `base-obligations (UNIT)` rows
# register that UNIT's base-corpus records are DERIVED mirrors of the owner's catalogue. A
# mirror record must equal the owner's record on every field but the profile-scoped ones —
# byte-verbatim, the probe's rule — and the mirror may not drift: a record that was copied
# and then edited is a fact stated in two ungoverned ways (MODEL-METHOD.7).
reg_path = root / "doctrine" / "fact_ownership.tsv"
if reg_path.is_file():
    for line in reg_path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        kind, owner_rel, mirror_rel = parts[0], parts[1], parts[2]
        mm = __import__("re").match(r"base-(requirements|obligations) \((.+)\)", kind)
        if not mm or mirror_rel == "-":
            continue
        which, unit = mm.group(1), mm.group(2)
        owner_p, mirror_p = root / owner_rel, root / mirror_rel
        if not owner_p.is_file() or not mirror_p.is_file():
            continue                        # existence is the FACT-OWNERSHIP gate's leg
        checked.append(kind)
        owner_recs = R.load(owner_p, root=root)
        mirror_by_id = {r["id"]: r for r in R.load(mirror_p, root=root)}
        owner_by_id = {r["id"]: r for r in owner_recs}
        if which == "requirements":
            # the mirrored set, re-derived: the owner's records covering a base-form
            # instruction, plus their dependency closure
            owner_scope = D.load_profile(owner_p.parent / "profile.sexp")["scope"]
            base = {m.lower() for v in owner_scope.values()
                    if isinstance(v, list) for m in v}
            covering = [r["id"] for r in owner_recs if set(r.get("insns", [])) & base]
            closure = set(covering)
            frontier = list(closure)
            while frontier:
                rid = frontier.pop()
                for dep in owner_by_id.get(rid, {}).get("dependencies", []):
                    if dep not in closure:
                        closure.add(dep)
                        if dep in owner_by_id:
                            frontier.append(dep)
            for rid in sorted(closure):
                want, got = owner_by_id[rid], mirror_by_id.get(rid)
                if got is None:
                    findings.append(f"MISSING MIRROR {mirror_p.name} [{rid}]: the base-corpus "
                                    f"mirror does not carry the record — the derivation is "
                                    f"incomplete")
                    continue
                for f_ in set(want) - {"profile_ids"}:
                    if got.get(f_) != want.get(f_):
                        findings.append(f"MIRROR DRIFT {mirror_p.name} [{rid}]: field {f_!r} "
                                        f"differs from the owner's record — a derived mirror "
                                        f"may not drift")
                if got.get("profile_ids") != [unit]:
                    findings.append(f"MIRROR DRIFT {mirror_p.name} [{rid}]: profile_ids "
                                    f"{got.get('profile_ids')} != [{unit!r}] — the mirror's "
                                    f"scope field is the one legal difference")
            base_in_mirror = {r["id"] for r in mirror_by_id.values()
                              if set(r.get("insns", [])) & base}
            for rid in sorted(base_in_mirror - closure):
                findings.append(f"UNGOVERNED BASE RECORD {mirror_p.name} [{rid}]: covers a "
                                f"base form but is not in the owner's mirror closure — an "
                                f"authored base record outside the derivation")
        else:
            # obligations mirror the mirrored requirements' obligations: the requirement
            # closure (the owner's base-covering records + their dependencies) computed
            # from the owner's requirements catalogue, then the obligations they name.
            req_cat = owner_p.parent / "requirements.sexp"
            owner_reqs = R.load(req_cat, root=root)
            owner_req_by_id = {r["id"]: r for r in owner_reqs}
            owner_scope = D.load_profile(owner_p.parent / "profile.sexp")["scope"]
            base = {m.lower() for v in owner_scope.values()
                    if isinstance(v, list) for m in v}
            closure = {r["id"] for r in owner_reqs if set(r.get("insns", [])) & base}
            frontier = list(closure)
            while frontier:
                rid = frontier.pop()
                for dep in owner_req_by_id.get(rid, {}).get("dependencies", []):
                    if dep not in closure:
                        closure.add(dep)
                        if dep in owner_req_by_id:
                            frontier.append(dep)
            ob_ids = sorted({o for rid in closure
                             for o in owner_req_by_id[rid].get("obligation_ids", [])})
            for oid in ob_ids:
                want, got = owner_by_id.get(oid), mirror_by_id.get(oid)
                if want is None:
                    continue                # a dangling obligation id is rule 6/7's leg
                if got is None:
                    findings.append(f"MISSING MIRROR {mirror_p.name} [{oid}]: the base-corpus "
                                    f"obligation mirror does not carry the record")
                    continue
                for f_ in set(want) - {"contract_id", "profile_ids"}:
                    w, g = want.get(f_), got.get(f_)
                    if f_ == "parameters":
                        w = dict(w or {}); g = dict(g or {})
                        g.pop("mirrored_from", None)
                    if g != w:
                        findings.append(f"MIRROR DRIFT {mirror_p.name} [{oid}]: field {f_!r} "
                                        f"differs from the owner's record — a derived mirror "
                                        f"may not drift")
                if got.get("profile_ids") != [unit]:
                    findings.append(f"MIRROR DRIFT {mirror_p.name} [{oid}]: profile_ids "
                                    f"{got.get('profile_ids')} != [{unit!r}]")
                if got.get("contract_id") == want.get("contract_id"):
                    findings.append(f"MIRROR DRIFT {mirror_p.name} [{oid}]: the mirror keeps "
                                    f"the owner's contract_id — the obligation would bill the "
                                    f"wrong contract")

for f in findings:
    print(f)
print(f"__CHECKED__ {len(checked)}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/schemas" "$t/p"
  cp schemas/requirement.schema.json schemas/contract-obligation.schema.json "$t/schemas/"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'RECORD-SCHEMA self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  REQ='{"id":"REQ-D-A","profile_ids":["p"],"kind":"state","statement":"S","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"applicability":"included","research_status":"resolved","implementation_status":"planned","source_semantics":{"category":"defined","detail":"d"},"risk":"low","obligation_ids":["OB-A"],"dependencies":[],"implementation_refs":[],"evidence_ids":[]}'
  OB='{"id":"OB-A","contract_id":"c","contract_version":"0","profile_ids":["p"],"direction":"cpu-guarantee","statement":"S","authority":"architecture","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"parameters":{},"dependencies":[],"required_checks":["CHK-A-POS","CHK-A-NEG"]}'

  arm_command=(check_records "$t")
  arm() {
    argc 3 "$#" arm || return
    out="$("${arm_command[@]}" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'RECORD-SCHEMA self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'RECORD-SCHEMA self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  sources() { argc 1 "$#" sources || return; printf '%s\n' "$1" > "$t/p/sources.sexp"; }
  profile() { argc 1 "$#" profile || return; printf '%s\n' "$1" > "$t/p/profile.sexp"; }
  reqs()    { argc 1 "$#" reqs || return; python3 -c "
import json, pathlib, sys
sys.path.insert(0, '$ROOT/scripts')
import records_sexp as R
recs = [json.loads(l) for l in '''$1'''.split('|||') if l.strip()]
pathlib.Path('$t/p/requirements.sexp').write_text(R.dump(recs))"; }
  obs()     { argc 1 "$#" obs || return; python3 -c "
import json, pathlib, sys
sys.path.insert(0, '$ROOT/scripts')
import records_sexp as R
recs = [json.loads(l) for l in '''$1'''.split('|||') if l.strip()]
pathlib.Path('$t/p/contract-obligations.sexp').write_text(R.dump(recs))"; }
  # schema-layer access: the fixture root must SEE schema/ for load_schema — symlink it
  ln -sfn "$ROOT/schema" "$t/schema"

  sources '(sources (source (id "SRC-A") (file "a.html")))'
  profile '(profile (decision (id "D-A") (authority architecture) (statement "S") (source "SRC-A §1")))'
  reqs "$REQ";                                                arm "GREEN a covered, cited, valid record" 0 "__CHECKED__ 1"
  # ---- the schema layer's own refusals, on the converted form -------------------------------
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['risk']='apocalyptic'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a record the schema layer refuses (bad enum symbol)" 1 "is not one of"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['source_refs']=[]; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an empty citation list — min 1 (an empty list is not a citation)" 1 "min is 1"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['obligation_ids']=['OB-A','OB-A']; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a duplicated obligation — unique" 1 "unique"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['id']='1BAD'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an id the pattern refuses" 1 "does not match"
  reqs "$REQ|||$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['risk']='critical'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a catalogue with a duplicated id — last-wins collapses it" 1 "DUPLICATE ID"
  printf '%s\n' '(requirement (id "REQ-D-A") (broken' > "$t/p/requirements.sexp"
                                                              arm "RED   a record that does not even parse" 1 "does not even parse"
  : > "$t/p/requirements.sexp";                               arm "RED   an empty catalogue" 1 "contains no records"
  # ---- the cross-checks on the converted form ------------------------------------------------
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['source_refs']=[{'source_id':'SRC-NOWHERE','locator':'§1'}]; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   cites a source nobody pinned" 1 "UNPINNED SOURCE"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['source_semantics']['detail']='d OPEN: something'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   resolved while carrying an open question" 1 "RESOLVED WITH AN OPEN QUESTION"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['dependencies']=['REQ-D-GHOST']; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   depends on a record that does not exist" 1 "DANGLING DEP"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['statement']='something else'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   the requirement no longer states the decision" 1 "STATEMENT DRIFT"
  profile '(profile (decision (id "D-B") (authority architecture) (statement "T") (source "SRC-A §2")))'
  reqs "$REQ";                                                arm "RED   a profile decision with no requirement" 1 "UNCOVERED DECISION"
  profile '(profile (decision (id "D-A") (authority architecture) (statement "S") (source "SRC-A §1")))'
  reqs "$REQ"; obs "$OB";                                     arm "GREEN requirement, contract and profile agree" 0 "__CHECKED__ 2"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['required_checks']=['CHK-A-POS']; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an obligation with no negative fixture" 1 "NO NEGATIVE CHECK"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['id']='OB-OTHER'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a requirement names an undefined obligation" 1 "UNDEFINED OBLIGATION"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['authority']='laboratory'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an architectural rule labelled a laboratory choice" 1 "AUTHORITY DOWNGRADE"
  obs "$OB"
  rm -f "$t/p/requirements.sexp";                             arm "RED   an obligation catalogue alone still checks" 0 "__CHECKED__ 1"
  # Partitioned catalogs retain schema validation and cross-record identity checks.
  mv "$t/p/contract-obligations.sexp" "$t/p/part.obligations.sexp"
  printf '(include-obligations (path "p/part.obligations.sexp"))\n' > "$t/p/contract-obligations.sexp"
                                                              arm "GREEN an included obligation is schema checked and linked" 0 "__CHECKED__ 1"
  sed 's/cpu-guarantee/unknown-direction/' "$t/p/part.obligations.sexp" > "$t/p/bad.obligations.sexp"
  printf '(include-obligations (path "p/bad.obligations.sexp"))\n' > "$t/p/contract-obligations.sexp"
                                                              arm "RED   an included invalid record names its origin" 1 "p/bad.obligations.sexp"
  cp "$t/p/part.obligations.sexp" "$t/p/second.obligations.sexp"
  printf '(include-obligations (path "p/part.obligations.sexp"))\n(include-obligations (path "p/second.obligations.sexp"))\n' > "$t/p/contract-obligations.sexp"
                                                              arm "RED   duplicate ids across distinct parts remain refused" 1 "DUPLICATE ID"
  mv "$t/p/part.obligations.sexp" "$t/p/contract-obligations.sexp"
  rm -f "$t/p/bad.obligations.sexp" "$t/p/second.obligations.sexp"
  reqs "$REQ"; rm -f "$t/p/contract-obligations.sexp"
  # ---- rule 9 MIRROR: an obligation naming its requirement restates it ------------------------
  reqs "$REQ"; obs "$OB"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-A'}; r['statement']='S'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "GREEN an obligation mirrored on its requirement" 0 "__CHECKED__ 2"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-A'}; r['statement']='something else'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an obligation that drifted from its requirement" 1 "MIRROR DRIFT"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-GHOST'}; r['statement']='S'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a mirror of a requirement that does not exist" 1 "MIRROR WITHOUT SOURCE"
  # A frozen mirror is history only with an authenticated active replacement route.
  versioned_mirror() {
    argc 1 "$#" versioned_mirror || return
    python3 - "$t" "$1" <<'PYFIXTURE'
import hashlib, json, pathlib, sys
sys.path.insert(0, "scripts")
import records_sexp as R
root, scenario = pathlib.Path(sys.argv[1]), sys.argv[2]
base = {"profile_ids": ["p"], "direction": "cpu-guarantee", "authority": "architecture",
        "source_refs": [{"source_id": "SRC-A", "locator": "§1"}],
        "parameters": {"requirement_id": "REQ-D-A"}, "dependencies": [],
        "required_checks": ["CHK-A-POS", "CHK-A-NEG"]}
records = [dict(base, id=oid, contract_id=f"p-env-v{n}", contract_version=str(n), statement=statement)
           for n, oid, statement in [(0, "OB-A", "Historical"),
                                     (1, "OB-A-MID", "Intermediate"),
                                     (2, "OB-A-V2", "S")]]
lines = R.dump(records).splitlines()
pins = [hashlib.sha256(line.encode()).hexdigest() for line in lines]
status, pin, parent = "frozen", pins[0], "p-env-v1"
old, new, middle = "OB-A-MID", "OB-A-V2", "OB-A-MID"
if scenario == "unfrozen": status = "open"
if scenario == "pin": pin = "0" * 64
if scenario == "drift": records[2]["statement"] = "wrong"
if scenario == "authority": records[2]["authority"] = "laboratory"
if scenario == "no-mirror": records[2]["parameters"] = {}
if scenario == "other-requirement": records[2]["parameters"] = {"requirement_id": "REQ-D-OTHER"}
if scenario == "inheritance": parent = "p-env-v0"
if scenario == "member": records[2]["contract_id"] = "p-env-v0"
if scenario == "absent": new = "OB-GHOST"
if scenario == "duplicate": middle = "OB-A"
if scenario == "live": records[2]["statement"] = "wrong"; records[0]["statement"] = "S"; records[1]["statement"] = "S"
lines = R.dump(records).splitlines()
if scenario == "live": pins = [hashlib.sha256(line.encode()).hexdigest() for line in lines]; pin = pins[0]
versions = [f'(contract (id "p-env-v0") (version "0") (profile_ids "p") (status {status}) (statement "v0") (member (id "OB-A") (sha256 "{pin}")))',
            f'(contract (id "p-env-v1") (version "1") (profile_ids "p") (extends "p-env-v0") (status frozen) (statement "v1") (member (id "{middle}") (sha256 "{pins[1]}")) (supersede (record "OB-A") (by "{middle}") (why "replacement")))',
            f'(contract (id "p-env-v2") (version "2") (profile_ids "p") (extends "{parent}") (status open) (statement "v2") (member (id "OB-A-V2")) (supersede (record "{old}") (by "{new}") (why "replacement")))']
if scenario == "no-route": versions[2] = versions[2].replace(f' (supersede (record "{old}") (by "{new}") (why "replacement"))', '')
if scenario == "schema": versions[2] = versions[2].replace('(status open)', '(status invented)')
(root / "p/contract-obligations.sexp").write_text(R.dump(records))
(root / "p/contract.sexp").write_text("\n".join(versions) + "\n")
PYFIXTURE
  }
  reqs "$REQ"
  versioned_mirror valid;       arm "GREEN a frozen mirror follows two authenticated replacements" 0 "__CHECKED__ 2"
  versioned_mirror no-route;    arm "RED   historical mirror has no effective replacement" 1 "effective replacement also drifts"
  versioned_mirror unfrozen;    arm "RED   an open historical record is still a live mirror" 1 "historical mirror is not frozen"
  versioned_mirror pin;         arm "RED   changed frozen bytes are never exempt" 1 "does not match its frozen pin"
  versioned_mirror drift;       arm "RED   the active replacement must match the current requirement" 1 "effective replacement also drifts"
  versioned_mirror no-mirror;   arm "RED   a replacement must explicitly mirror the same requirement" 1 "does not mirror the same requirement"
  versioned_mirror other-requirement; arm "RED   a replacement cannot mirror another requirement" 1 "does not mirror the same requirement"
  versioned_mirror inheritance; arm "RED   a replacement must follow consecutive inheritance" 1 "broken version inheritance"
  versioned_mirror member;      arm "RED   a replacement must belong to its declared version" 1 "version member has no matching record"
  versioned_mirror absent;      arm "RED   a supersession target must be a current member" 1 "invalid historical-mirror supersession"
  versioned_mirror duplicate;   arm "RED   version ownership must be unambiguous" 1 "multiple version owners"
  versioned_mirror schema;      arm "RED   a malformed manifest grants no mirror exemption" 1 "invalid version manifest"
  versioned_mirror live;        arm "RED   an effective open mirror still rejects ordinary drift" 1 "historical mirror is not frozen"
  versioned_mirror authority;   arm "RED   a replacement cannot downgrade architectural authority" 1 "AUTHORITY DOWNGRADE"
  rm -f "$t/p/contract.sexp"
  rm -f "$t/p/contract-obligations.sexp"
  # ---- rule 14 MIRROR-DERIVE: the base-corpus mirror, registry-driven ---------------------------
  # Fixture: an owner unit o/ and a mirror unit m/ beside a registry row. The owner's
  # profile declares a one-form base census; the owner's record covers it.
  mkdir -p "$t/o" "$t/m" "$t/doctrine"
  cat > "$t/o/profile.sexp" <<'EOF'
(profile (scope (count_base 1) (count_total 1) (authority architecture) (source "s") (base_op "ADD")))
EOF
  python3 - "$t" "$ROOT" <<'PY'
import json, pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
t = pathlib.Path(sys.argv[1])
own = {"id": "REQ-D-A", "profile_ids": ["o"], "kind": "instruction", "statement": "S",
       "insns": ["add"], "source_refs": [{"source_id": "SRC-A", "locator": "§1"}],
       "applicability": "included", "research_status": "resolved",
       "implementation_status": "planned",
       "source_semantics": {"category": "defined", "detail": "d"}, "risk": "low",
       "obligation_ids": ["OB-A"], "dependencies": [], "implementation_refs": [],
       "evidence_ids": []}
own_ob = {"id": "OB-A", "contract_id": "o-env-v0", "contract_version": "0",
          "profile_ids": ["o"], "direction": "cpu-guarantee", "statement": "S",
          "authority": "architecture",
          "source_refs": [{"source_id": "SRC-A", "locator": "§1"}],
          "parameters": {"requirement_id": "REQ-D-A"}, "dependencies": ["REQ-D-A"],
          "required_checks": ["CHK-A-POS", "CHK-A-NEG"]}
(t / "o/requirements.sexp").write_text(R.dump([own]))
(t / "o/contract-obligations.sexp").write_text(R.dump([own_ob]))
mir = dict(own); mir["profile_ids"] = ["m"]
mir_ob = dict(own_ob); mir_ob["contract_id"] = "m-env-v0"; mir_ob["profile_ids"] = ["m"]
mir_ob["parameters"] = {"requirement_id": "REQ-D-A", "mirrored_from": "o"}
(t / "m/requirements.sexp").write_text(R.dump([mir]))
(t / "m/contract-obligations.sexp").write_text(R.dump([mir_ob]))
PY
  # the registry names repo-relative paths (the fixture root stands in for the repo root)
  printf 'base-requirements (m)\to/requirements.sexp\tm/requirements.sexp\tRECORD-SCHEMA\nbase-obligations (m)\to/contract-obligations.sexp\tm/contract-obligations.sexp\tRECORD-SCHEMA\n' > "$t/doctrine/fact_ownership.tsv"
                                                              arm "GREEN the faithful mirror checks" 0 "__CHECKED__ 7"
  python3 - "$t" "$ROOT" <<'PY'
import pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
p = pathlib.Path(sys.argv[1]) / "m/requirements.sexp"
recs = R.load(p)
recs[0]["statement"] = "S — edited after the copy"
p.write_text(R.dump(recs))
PY
                                                              arm "RED   a mirror record edited after the copy" 1 "MIRROR DRIFT"
  python3 - "$t" "$ROOT" <<'PY'
import pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
t = pathlib.Path(sys.argv[1])
# restore, then drop the mirrored obligation record
own = R.load(t / "o/requirements.sexp")
mir = dict(own[0]); mir["profile_ids"] = ["m"]
(t / "m/requirements.sexp").write_text(R.dump([mir]))
(t / "m/contract-obligations.sexp").write_text(R.dump([]))
PY
                                                              arm "RED   the mirror missing the obligation record" 1 "MISSING MIRROR"
  python3 - "$t" "$ROOT" <<'PY'
import pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
t = pathlib.Path(sys.argv[1])
own_ob = R.load(t / "o/contract-obligations.sexp")
mir_ob = dict(own_ob[0]); mir_ob["profile_ids"] = ["m"]  # contract_id NOT remapped
(t / "m/contract-obligations.sexp").write_text(R.dump([mir_ob]))
PY
                                                              arm "RED   the mirror keeping the owner's contract" 1 "the mirror keeps"
  rm -rf "$t/o" "$t/m" "$t/doctrine"
  # ---- rules 10+11: the unit registry and the layer rule (MODEL-METHOD.2) ---------------------
  units() { argc 1 "$#" units || return; python3 -c "
import json, pathlib, sys
sys.path.insert(0, '$ROOT/scripts')
import records_sexp as R
recs = [json.loads(l) for l in '''$1'''.split('|||') if l.strip()]
pathlib.Path('$t/p/units.sexp').write_text(R.dump(recs))"; }
  needs() { argc 1 "$#" needs || return; python3 -c "
import json, pathlib, sys
sys.path.insert(0, '$ROOT/scripts')
import records_sexp as R
recs = [json.loads(l) for l in '''$1'''.split('|||') if l.strip()]
pathlib.Path('$t/p/category-needs.sexp').write_text(R.dump(recs))"; }
  rm -f "$t/p/units.sexp" "$t/p/category-needs.sexp"
  BOARD_MISSING='{"category":"C19","layer":"board","kind":"datasheet","unit":"p","disposition":"missing","reason":"x"}'
  needs "$BOARD_MISSING";                                      arm "RED   layer claims without the registry they describe" 1 "NO REGISTRY"
  units '{"id":"p","kind":"processor","layer":"processor","book":"b"}'
  needs "$BOARD_MISSING";                                      arm "RED   the acceptance's rule: a board-layer 'missing' for a processor" 1 "LAYER LIE"
  needs '{"category":"C07","layer":"processor","kind":"isa-manual","unit":"p","disposition":"missing"}'
                                                               arm "RED   a 'missing' that owes no reason" 1 "REASONLESS MISSING"
  needs '{"category":"C01","layer":"processor","kind":"isa-manual","unit":"p","disposition":"covered"}'
                                                               arm "RED   a 'covered' naming no material" 1 "UNEVIDENCED COVERED"
  python3 - <<PYEOF
import pathlib
pathlib.Path('$t/p/catalog.sexp').write_text(
    '(materials (schema-version 1) (cache-root ".materials")\n'
    '(material (id "M") (title "t") (revision "r") (release-kind ratified) (kind snapshot)\n'
    '(licence "l") (corpus-path "c") (cache-path "c") (sha256 "' + 'a' * 64 + '")))\n')
PYEOF
  needs '{"category":"C01","layer":"processor","kind":"isa-manual","unit":"p","disposition":"covered","material":"GHOST-DOC"}'
                                                               arm "RED   a covered-by that names no held document" 1 "UNRESOLVED MATERIAL"
  needs '{"category":"C01","layer":"processor","kind":"isa-manual","unit":"p","disposition":"covered","material":"M"}|||{"category":"C07","layer":"processor","kind":"isa-manual","unit":"p","disposition":"missing","reason":"F/D excluded"}'
                                                               arm "GREEN a registry and an honest census" 0 "__CHECKED__ 3"
  : > "$t/p/units.sexp"; needs "$BOARD_MISSING";                          arm "RED   an empty unit registry" 1 "contains no records"
  rm -f "$t/p/units.sexp" "$t/p/category-needs.sexp"
  # ---- rule 13 CAMPAIGN: the ACT4 record carries only counts its rows re-derive -----------
  campaign_fixed() { argc 1 "$#" campaign_fixed || return; python3 -c "
import pathlib, sys
text = '''$BASE_CAMPAIGN'''
text = text.replace(*'''$1'''.split('@@@', 1)) if '''$1''' else text
pathlib.Path('$t/p/act4.sexp').write_text(text)"; }
  BASE_CAMPAIGN='(act4-campaign (profile "p") (suite (origin "o") (branch "act4") (pin "0123456789012345678901234567890123456789") (sparse_paths "tests/env")) (toolchain (compiler "c") (linker "l")) (run (date "2026-09-30") (tests 2) (signature_slots 5) (verdicts "1 pass / 1 fail")) (evidence_note "n") (test (file "I-add-00.S") (signature_slots 2) (verdict_semulith "pass") (verdict_sail "pass") (verdict_spike "pass") (signature "agree") (control "agree")) (test (file "I-sub-00.S") (signature_slots 3) (verdict_semulith "fail") (verdict_sail "pass") (verdict_spike "pass") (signature "mismatch") (control "agree")))'
  campaign_fixed "";                                        arm "GREEN a consistent campaign record — one failing test, honestly recorded" 0 "__CHECKED__ 2"
  campaign_fixed '(tests 2)@@@(tests 3)';                   arm "RED   a carried test count the rows contradict" 1 "CAMPAIGN COUNT"
  campaign_fixed '(signature_slots 5)@@@(signature_slots 6)'; arm "RED   a carried slot total the rows contradict" 1 "CAMPAIGN SLOTS"
  campaign_fixed '"1 pass / 1 fail"@@@"2 pass / 0 fail"';   arm "RED   a verdict summary the rows contradict" 1 "CAMPAIGN VERDICTS"
  campaign_fixed 'verdict_semulith "pass"@@@verdict_semulith "green"'; arm "RED   a verdict outside the closed vocabulary" 1 "CAMPAIGN VOCABULARY"
  campaign_fixed '(signature "agree")@@@(signature "fine")'; arm "RED   a comparison verdict outside the closed vocabulary" 1 "CAMPAIGN VOCABULARY"
  rm -f "$t/p/act4.sexp"
  # ---- the JSONL track (examples stay JSONL) -------------------------------------------------
  printf '%s\n' "$REQ" > "$t/p/requirements.jsonl";           arm "GREEN a JSONL record validates on the old track" 0 "__CHECKED__ 2"
  printf 'not json at all\n' > "$t/p/mystery.jsonl";          arm "RED   a record file no schema governs" 1 "UNGOVERNED"
  rm -f "$t/p/mystery.jsonl"
  printf 'not json at all\n' > "$t/p/requirements.jsonl";     arm "RED   a malformed JSONL line" 1 "not valid JSON"
  : > "$t/p/requirements.jsonl";                              arm "RED   an empty JSONL record file" 1 "contains no records"
  rm -f "$t/p/requirements.jsonl" "$t/p/requirements.sexp" "$t/p/contract-obligations.sexp"
                                                              arm "REFUSE nothing to check at all" 2 "NO RECORDS"

  arm_command=(python3 scripts/probe_record_catalog.py)
  arm "GREEN catalog reader controls" 0 "31 pass / 0 fail"
  arm_command=(python3 scripts/probe_record_catalog.py --mutation ignore-includes)
  arm "RED lost include expansion" 1 "CONTROL-MISSED"
  # All project token patterns, and the public kernel's deliberate search contract.
  # a42ay: schema/credits.sexp adds 9 anchored facets (25 schemas / 100 facets): loose-end 96 → 105, ignore-pattern 552 → 606.
  arm_command=(python3 scripts/probe_schema_token_facets.py)
  arm "GREEN exact-token facets normal" 0 "Ran 7 tests"
  arm_command=(python3 scripts/probe_schema_token_facets.py --mutation loose-end)
  arm "RED normal token loose-end mutation" 1 "FAILED (failures=105)"
  arm_command=(python3 scripts/probe_schema_token_facets.py --mutation ignore-pattern)
  arm "RED normal token ignore-pattern mutation" 1 "FAILED (failures=606)"
  arm_command=(python3 scripts/probe_schema_token_facets.py --mutation fullmatch)
  arm "RED normal token fullmatch mutation" 1 "FAILED (failures=1)"
  arm_command=(python3 -O scripts/probe_schema_token_facets.py)
  arm "GREEN exact-token facets optimized" 0 "Ran 7 tests"
  arm_command=(python3 -O scripts/probe_schema_token_facets.py --mutation loose-end)
  arm "RED optimized token loose-end mutation" 1 "FAILED (failures=105)"
  arm_command=(python3 -O scripts/probe_schema_token_facets.py --mutation ignore-pattern)
  arm "RED optimized token ignore-pattern mutation" 1 "FAILED (failures=606)"
  arm_command=(python3 -O scripts/probe_schema_token_facets.py --mutation fullmatch)
  arm "RED optimized token fullmatch mutation" 1 "FAILED (failures=1)"
  rm -rf "$t"
  printf 'RECORD-SCHEMA --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

# --audit: report referential problems in record files the gate deliberately does NOT enforce,
# so a known gap stays re-derivable instead of becoming prose someone has to remember.
if [ "${1:-}" = "--audit" ]; then
python3 - <<'AUDITPY'
import json, pathlib, sys
sys.path.insert(0, "scripts")
import records_sexp as R
_SKIP = {"target", "vendor", "schema"}
dirs = sorted({p.parent for p in pathlib.Path(".").rglob("*")
               if p.suffix in (".jsonl", ".sexp") and not _SKIP & set(p.parts)})
for d in dirs:
    rq = d / "requirements.sexp"
    ob = d / "contract-obligations.sexp"
    if not (rq.is_file() or ob.is_file() or (d / "requirements.jsonl").is_file()):
        continue
    enforced = (d / "profile.sexp").is_file()
    def load(p):
        if p.is_file():
            return R.load(p) if p.suffix == ".sexp" else \
                [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
        return None
    reqs = load(rq) or load(d / "requirements.jsonl") or []
    obs = load(ob) or load(d / "contract-obligations.jsonl") or []
    print(f"{d}/  ({'ENFORCED' if enforced else 'advisory - frozen delivery artifacts'})")
    print(f"  requirements {len(reqs)} | obligations {len(obs)}")
    defined = {o["id"] for o in obs}
    named = {oid for r in reqs for oid in r.get("obligation_ids", [])}
    print(f"  named but undefined : {sorted(named - defined) or 'none'}")
    by_dir = {o["id"]: o.get("direction") for o in obs}
    unnamed = sorted(defined - named)
    print(f"  unnamed environment-assumptions (expected) : "
          f"{[i for i in unnamed if by_dir.get(i) == 'environment-assumption'] or 'none'}")
    print(f"  unnamed cpu-guarantees (a finding)        : "
          f"{[i for i in unnamed if by_dir.get(i) != 'environment-assumption'] or 'none'}")
    missing_neg = [o["id"] for o in obs
                   if not any(c.endswith("-NEG") for c in o.get("required_checks", []))]
    print(f"  obligations with no negative check : {missing_neg or 'none'}")
AUDITPY
  exit 0
fi

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -d schemas ] || { echo "RECORD-SCHEMA: ok (no schemas/ yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "RECORD-SCHEMA: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_records .)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "RECORD-SCHEMA: REFUSED — the record corpus or a schema could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "RECORD-SCHEMA: a record file contradicts its schema, its sources, or its profile."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The SCHEMA and the PROFILE are authoritative. Fix the record, not the contract."; } >&2
  exit 1
fi

# ---- JSONL track, engine 2: the workspace's own Rust checker (P1-LAB.7) -----------------------
# The Python phase above decides schema validity; the Rust engine re-derives the same rows and
# then checks the §3 graph invariants over the examples bundle. It runs only where the bundle
# it is built around lives; a tree without `examples/` stays a Python-only decision.
if [ -f examples/fixture-context.json ]; then
  command -v cargo >/dev/null 2>&1 || {
    echo "RECORD-SCHEMA: REFUSED — cargo is not on PATH; the Rust engine cannot judge." >&2; exit 2; }
  rust_out="$(cargo run --quiet --offline -p semulith-cli -- check-examples 2>&1)"
  rust_rc=$?
  if [ "$rust_rc" -eq 2 ]; then
    { echo "RECORD-SCHEMA: REFUSED — the Rust checker could not judge (inputs or usage)."
      printf '%s\n' "$rust_out" | sed 's/^/  /'; } >&2
    exit 2
  fi
  if [ "$rust_rc" -ne 0 ]; then
    { echo "RECORD-SCHEMA: the Rust graph checker rejects the JSONL records."
      printf '%s\n' "$rust_out" | sed 's/^/  /'
      echo "  The RECORDS are the only mutable side; the schemas, the ledger and the graph"
      echo "  rules are the contract."; } >&2
    exit 1
  fi
  printf 'RECORD-SCHEMA: ok (%s record file(s) validate and agree with their profile; the Rust graph checker accepts the examples bundle)\n' "${count:-0}"
  exit 0
fi
printf 'RECORD-SCHEMA: ok (%s record file(s) validate and agree with their profile)\n' "${count:-0}"
exit 0
