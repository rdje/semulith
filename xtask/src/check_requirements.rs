//! The `RECORD-SCHEMA` doctrine's driver, ported from `scripts/check_requirements.sh` (`XTASK.6` slice `6ap`), which is
//! now a shim of `cargo xtask check-requirements`.
//!
//! Every tracked record file — the JSONL delivery artifacts and the schema-layer catalogues (requirements, obligations,
//! credits, units, category needs, the ACT4 and workload campaign records) — validates against its schema and carries the
//! fifteen cross-checks; the JSONL track is re-derived by the workspace's own Rust checker once the Python phase is green.
//! The judge is the driver's 670-line inline Python (`check_records`, over the pinned validators and readers); it runs
//! verbatim through `python3 -`, as the script ran it, and is not ported — nor are the controls' fixture writers (the
//! `python3 -c` programs the script composed around its JSON records, re-composed here with the same text), the
//! versioned-mirror and mirror-derive fixture programs, the two probes, or the `--audit` report. Each self-test arm is one
//! `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, on_path, scratch};

/// The judge, verbatim: `python3 - <root>` from the repository root (`scripts/` on its path) — the findings, then
/// `__CHECKED__ N`; exit 1 on a finding, 2 when it cannot judge.
const JUDGE: &str = r####"import hashlib, json, pathlib, sys
sys.path.insert(0, "scripts")
from validate_records import validate_jsonl, UnsupportedSchema
import sexp as S
import records_sexp as R
import record_catalog as C
import credit_records as CR
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
    "workload.sexp": "schema/workload.sexp",
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
    if cat.name == "workload.sexp":
        # 15. WORKLOAD — the workload-campaign record (P4-SYSTEM.15 slice f) is a RECORDED
        # experiment like the ACT4 record: every carried count is re-derived from the rows
        # and the verdict vocabulary is confined (rule 13's shape, the row head `workload`).
        def _field(f, name):
            for c in f[1:]:
                if isinstance(c, list) and c and str(c[0]) == name:
                    return c
            return None
        def _val(f, name):
            c = _field(f, name)
            return c[1] if c is not None and len(c) == 2 else None
        forms = [f for f in S.read_file(cat)
                 if not (isinstance(f, list) and f and str(f[0]) == "comment")]
        root_form = forms[0] if len(forms) == 1 else None
        rows = [c for c in (root_form or [None])[1:]
                if isinstance(c, list) and c and str(c[0]) == "workload"]
        run_f = _field(root_form, "run") if root_form else None
        if root_form is None or str(root_form[0]) != "workload-campaign" or run_f is None:
            findings.append(f"WORKLOAD ROOT {cat.name}: no single workload-campaign form "
                            f"with a run block")
            continue
        seen_files = set()
        for r in rows:
            fn = _val(r, "file")
            if fn in seen_files:
                findings.append(f"WORKLOAD DUPLICATE {cat.name}: workload '{fn}' appears twice")
            seen_files.add(fn)
            for k in ("verdict_semulith", "verdict_sail", "verdict_spike"):
                if str(_val(r, k)) not in ("pass", "fail"):
                    findings.append(f"WORKLOAD VOCABULARY {cat.name} [{fn}]: {k} is "
                                    f"'{_val(r, k)}', not pass|fail")
            for k in ("signature", "control"):
                if str(_val(r, k)) not in ("agree", "mismatch"):
                    findings.append(f"WORKLOAD VOCABULARY {cat.name} [{fn}]: {k} is "
                                    f"'{_val(r, k)}', not agree|mismatch")
            if int(_val(r, "compressed")) > int(_val(r, "instructions")):
                findings.append(f"WORKLOAD CENSUS {cat.name} [{fn}]: more compressed instructions "
                                f"than instructions")
        if int(_val(run_f, "workloads")) != len(rows):
            findings.append(f"WORKLOAD COUNT {cat.name}: run.workloads = "
                            f"{_val(run_f, 'workloads')} but the record carries {len(rows)} row(s)")
        slots = sum(int(_val(r, "signature_slots")) for r in rows)
        if int(_val(run_f, "signature_slots")) != slots:
            findings.append(f"WORKLOAD SLOTS {cat.name}: run.signature_slots = "
                            f"{_val(run_f, 'signature_slots')} but the rows carry {slots}")
        passed = sum(1 for r in rows
                     if str(_val(r, "verdict_semulith")) == "pass"
                     and str(_val(r, "verdict_sail")) == "pass"
                     and str(_val(r, "verdict_spike")) == "pass"
                     and str(_val(r, "signature")) == "agree"
                     and str(_val(r, "control")) == "agree")
        derived = f"{passed} pass / {len(rows) - passed} fail"
        if str(_val(run_f, "verdicts")) != derived:
            findings.append(f"WORKLOAD VERDICTS {cat.name}: run.verdicts = "
                            f"'{_val(run_f, 'verdicts')}' but the rows derive '{derived}'")
        continue
    if cat.name == "credits.sexp":
        # 14. CREDITS — the credited-disposition catalogue (a42ay) is read by its own unpinned
        #     reader, never by the pinned records reader, which refuses the `credit` head by
        #     design. The reader re-validates the schema, bounds the file and refuses a
        #     duplicate id; what each record grants is requirement_status.py's derivation,
        #     which authenticates every pin on every read (decision_credit-is-a-catalogue-record).
        try:
            credits = CR.load_credits(root, cat.parent)
        except (CR.CreditRefused, S.SexpError) as exc:
            findings.append(f"UNREADABLE {cat.relative_to(root)}: conforms to its schema but does "
                            f"not read as credits — {exc}")
            continue
        if not credits:
            findings.append(f"INVALID    {cat.relative_to(root)}: contains no records — an empty "
                            f"catalogue is not a valid one")
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
"####;
/// `versioned_mirror <scenario>`, verbatim: `python3 - <t> <scenario>`.
const VERSIONED_MIRROR: &str = r####"import hashlib, json, pathlib, sys
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
"####;
/// The mirror-derive fixtures, verbatim: `python3 - <t> <root>` each.
const DERIVE_FIXTURE: &str = r####"import json, pathlib, sys
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
"####;
const DERIVE_EDITED: &str = r####"import pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
p = pathlib.Path(sys.argv[1]) / "m/requirements.sexp"
recs = R.load(p)
recs[0]["statement"] = "S — edited after the copy"
p.write_text(R.dump(recs))
"####;
const DERIVE_DROPPED: &str = r####"import pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
t = pathlib.Path(sys.argv[1])
# restore, then drop the mirrored obligation record
own = R.load(t / "o/requirements.sexp")
mir = dict(own[0]); mir["profile_ids"] = ["m"]
(t / "m/requirements.sexp").write_text(R.dump([mir]))
(t / "m/contract-obligations.sexp").write_text(R.dump([]))
"####;
const DERIVE_OWNER_CONTRACT: &str = r####"import pathlib, sys
sys.path.insert(0, sys.argv[2] + "/scripts")
import records_sexp as R
t = pathlib.Path(sys.argv[1])
own_ob = R.load(t / "o/contract-obligations.sexp")
mir_ob = dict(own_ob[0]); mir_ob["profile_ids"] = ["m"]  # contract_id NOT remapped
(t / "m/contract-obligations.sexp").write_text(R.dump([mir_ob]))
"####;
/// `--audit`, verbatim: `python3 -` from the repository root, its report through.
const AUDIT: &str = r####"import json, pathlib, sys
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
"####;

const REQ: &str = r#"{"id":"REQ-D-A","profile_ids":["p"],"kind":"state","statement":"S","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"applicability":"included","research_status":"resolved","implementation_status":"planned","source_semantics":{"category":"defined","detail":"d"},"risk":"low","obligation_ids":["OB-A"],"dependencies":[],"implementation_refs":[],"evidence_ids":[]}"#;
const OB: &str = r#"{"id":"OB-A","contract_id":"c","contract_version":"0","profile_ids":["p"],"direction":"cpu-guarantee","statement":"S","authority":"architecture","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"parameters":{},"dependencies":[],"required_checks":["CHK-A-POS","CHK-A-NEG"]}"#;
const BOARD_MISSING: &str = r#"{"category":"C19","layer":"board","kind":"datasheet","unit":"p","disposition":"missing","reason":"x"}"#;
const BASE_CAMPAIGN: &str = r#"(act4-campaign (profile "p") (suite (origin "o") (branch "act4") (pin "0123456789012345678901234567890123456789") (sparse_paths "tests/env")) (toolchain (compiler "c") (linker "l")) (run (date "2026-09-30") (tests 2) (signature_slots 5) (verdicts "1 pass / 1 fail")) (evidence_note "n") (test (file "I-add-00.S") (signature_slots 2) (verdict_semulith "pass") (verdict_sail "pass") (verdict_spike "pass") (signature "agree") (control "agree")) (test (file "I-sub-00.S") (signature_slots 3) (verdict_semulith "fail") (verdict_sail "pass") (verdict_spike "pass") (signature "mismatch") (control "agree")))"#;
const BASE_WORKLOAD: &str = r#"(workload-campaign (profile "p") (toolchain (compiler "c") (linker "l")) (run (date "2026-10-27") (workloads 2) (signature_slots 5) (verdicts "1 pass / 1 fail")) (evidence_note "n") (workload (file "wl-a.c") (instructions 10) (compressed 4) (families "IM") (sail_steps 7) (signature_slots 2) (verdict_semulith "pass") (verdict_sail "pass") (verdict_spike "pass") (signature "agree") (control "agree")) (workload (file "wl-b.c") (instructions 9) (compressed 3) (families "I") (sail_steps 5) (signature_slots 3) (verdict_semulith "fail") (verdict_sail "fail") (verdict_spike "fail") (signature "agree") (control "agree")))"#;

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `python3 - <args…> <<'…'`: a program on stdin from the repository root; stdout and stderr merged and captured
/// (`2>&1`) when `capture`, through when the self-test is the command and silenced otherwise.
fn python_stdin(
    repo: &Path,
    program: &str,
    args: &[&str],
    capture: bool,
    verbose: bool,
) -> (i32, String) {
    let through = || {
        if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        }
    };
    let mut command = Command::new("python3");
    command
        .arg("-")
        .args(args)
        .current_dir(repo)
        .stdin(Stdio::piped());
    if capture {
        command.stdout(Stdio::piped()).stderr(Stdio::piped());
    } else {
        command.stdout(through()).stderr(through());
    }
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(program.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&o.stderr));
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// `printf '%s' "$json" | python3 -c "<mutation>"`: one JSON record rewritten by the script's one-line program; the
/// program's own stderr through when the self-test is the command, silenced otherwise.
fn mutated(repo: &Path, json: &str, program: &str, verbose: bool) -> String {
    let mut command = Command::new("python3");
    command
        .arg("-c")
        .arg(program)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        });
    let Ok(mut child) = command.spawn() else {
        return String::new();
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(json.as_bytes());
    }
    child
        .wait_with_output()
        .map(|o| captured(&String::from_utf8_lossy(&o.stdout)).to_owned())
        .unwrap_or_default()
}

/// `python3 -c "<program>"`: a composed program, its own output through when the self-test is the command.
fn python_c(repo: &Path, program: &str, verbose: bool) {
    let through = || {
        if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        }
    };
    let _ = Command::new("python3")
        .arg("-c")
        .arg(program)
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(through())
        .stderr(through())
        .status();
}

/// `sed 's/PAT/REPL/' src > dst`: the first occurrence on every line, the patterns being literal text.
fn sed_first(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        out.push_str(&line.replacen(pattern, replacement, 1));
    }
    let _ = fs::write(dst, out);
}

/// The fixture: the scratch tree, its unit `p/`, and the script's composed writers.
struct Fixture<'a> {
    repo: &'a Path,
    t: &'a Path,
    verbose: bool,
}

impl Fixture<'_> {
    /// `reqs`/`obs`/`units`/`needs`: the script's `python3 -c` program around the records' JSON, the `|||`-separated
    /// records dumped through the pinned `records_sexp` into `p/<file>`.
    fn records(&self, file: &str, json: &str) {
        let program = format!(
            "\nimport json, pathlib, sys\nsys.path.insert(0, '{root}/scripts')\nimport records_sexp as R\nrecs = [json.loads(l) for l in '''{json}'''.split('|||') if l.strip()]\npathlib.Path('{t}/p/{file}').write_text(R.dump(recs))",
            root = self.repo.display(),
            t = self.t.display(),
        );
        python_c(self.repo, &program, self.verbose);
    }

    /// `campaign_fixed`/`workload_fixed <edit>`: the base record with one `old@@@new` replacement, into `p/<file>`.
    fn fixed(&self, file: &str, base: &str, edit: &str) {
        let program = format!(
            "\nimport pathlib, sys\ntext = '''{base}'''\ntext = text.replace(*'''{edit}'''.split('@@@', 1)) if '''{edit}''' else text\npathlib.Path('{t}/p/{file}').write_text(text)",
            t = self.t.display(),
        );
        python_c(self.repo, &program, self.verbose);
    }

    /// `sources`/`profile`: `printf '%s\n' "$1" > p/<file>`.
    fn text(&self, file: &str, text: &str) {
        let _ = fs::write(self.t.join("p").join(file), format!("{text}\n"));
    }

    /// A fixture program on stdin with `<t>` (and `<root>`) as its arguments.
    fn program(&self, program: &str, args: &[&str]) {
        let _ = python_stdin(self.repo, program, args, false, self.verbose);
    }

    /// `check_records "$t" 2>&1`, captured.
    fn judge(&self) -> (i32, String) {
        let t = self.t.display().to_string();
        python_stdin(self.repo, JUDGE, &[&t], true, self.verbose)
    }
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the command's exit status must be `expected` and its merged output must contain `want`.
    fn arm(&mut self, name: &str, (rc, raw): (i32, String), expected: i32, want: &str) {
        let out = captured(&raw);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("RECORD-SCHEMA self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("RECORD-SCHEMA self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// `python3 [-O] scripts/<probe> [--mutation …] 2>&1`, captured.
fn probe(repo: &Path, optimized: bool, script: &str, mutation: Option<&str>) -> (i32, String) {
    let mut command = Command::new("python3");
    if optimized {
        command.arg("-O");
    }
    command.arg(script);
    if let Some(m) = mutation {
        command.arg("--mutation").arg(m);
    }
    command.current_dir(repo);
    combined(&mut command)
}

/// The RED/GREEN controls against synthetic fixtures. Quiet unless `verbose` (the script ran it `>/dev/null 2>&1`
/// before the real judgement).
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "recordschema") else {
        if verbose {
            eprintln!("RECORD-SCHEMA self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let _ = fs::create_dir_all(t.join("schemas"));
    let _ = fs::create_dir_all(t.join("p"));
    for s in ["requirement.schema.json", "contract-obligation.schema.json"] {
        let _ = fs::copy(repo.join("schemas").join(s), t.join("schemas").join(s));
    }
    let fx = Fixture {
        repo,
        t: &t,
        verbose,
    };
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let p = t.join("p");
    // schema-layer access: the fixture root must SEE schema/ for load_schema — symlink it
    #[cfg(unix)]
    let _ = std::os::unix::fs::symlink(repo.join("schema"), t.join("schema"));
    fx.text(
        "sources.sexp",
        r#"(sources (source (id "SRC-A") (file "a.html")))"#,
    );
    fx.text("profile.sexp", r#"(profile (decision (id "D-A") (authority architecture) (statement "S") (source "SRC-A §1")))"#);
    fx.records("requirements.sexp", REQ);
    tally.arm(
        "GREEN a covered, cited, valid record",
        fx.judge(),
        0,
        "__CHECKED__ 1",
    );
    // ---- the schema layer's own refusals, on the converted form -------------------------------
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['risk']='apocalyptic'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   a record the schema layer refuses (bad enum symbol)",
        fx.judge(),
        1,
        "is not one of",
    );
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['source_refs']=[]; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   an empty citation list — min 1 (an empty list is not a citation)",
        fx.judge(),
        1,
        "min is 1",
    );
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['obligation_ids']=['OB-A','OB-A']; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   a duplicated obligation — unique",
        fx.judge(),
        1,
        "unique",
    );
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['id']='1BAD'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   an id the pattern refuses",
        fx.judge(),
        1,
        "does not match",
    );
    let critical = mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['risk']='critical'; print(json.dumps(r,ensure_ascii=False))", verbose);
    fx.records("requirements.sexp", &format!("{REQ}|||{critical}"));
    tally.arm(
        "RED   a catalogue with a duplicated id — last-wins collapses it",
        fx.judge(),
        1,
        "DUPLICATE ID",
    );
    fx.text(
        "requirements.sexp",
        r#"(requirement (id "REQ-D-A") (broken"#,
    );
    tally.arm(
        "RED   a record that does not even parse",
        fx.judge(),
        1,
        "does not even parse",
    );
    let _ = fs::write(p.join("requirements.sexp"), "");
    tally.arm(
        "RED   an empty catalogue",
        fx.judge(),
        1,
        "contains no records",
    );
    // ---- the cross-checks on the converted form ------------------------------------------------
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['source_refs']=[{'source_id':'SRC-NOWHERE','locator':'§1'}]; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   cites a source nobody pinned",
        fx.judge(),
        1,
        "UNPINNED SOURCE",
    );
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['source_semantics']['detail']='d OPEN: something'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   resolved while carrying an open question",
        fx.judge(),
        1,
        "RESOLVED WITH AN OPEN QUESTION",
    );
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['dependencies']=['REQ-D-GHOST']; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   depends on a record that does not exist",
        fx.judge(),
        1,
        "DANGLING DEP",
    );
    fx.records("requirements.sexp", &mutated(repo, REQ, "import json,sys; r=json.load(sys.stdin); r['statement']='something else'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   the requirement no longer states the decision",
        fx.judge(),
        1,
        "STATEMENT DRIFT",
    );
    fx.text("profile.sexp", r#"(profile (decision (id "D-B") (authority architecture) (statement "T") (source "SRC-A §2")))"#);
    fx.records("requirements.sexp", REQ);
    tally.arm(
        "RED   a profile decision with no requirement",
        fx.judge(),
        1,
        "UNCOVERED DECISION",
    );
    fx.text("profile.sexp", r#"(profile (decision (id "D-A") (authority architecture) (statement "S") (source "SRC-A §1")))"#);
    fx.records("requirements.sexp", REQ);
    fx.records("contract-obligations.sexp", OB);
    tally.arm(
        "GREEN requirement, contract and profile agree",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    fx.records("contract-obligations.sexp", &mutated(repo, OB, "import json,sys; r=json.load(sys.stdin); r['required_checks']=['CHK-A-POS']; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   an obligation with no negative fixture",
        fx.judge(),
        1,
        "NO NEGATIVE CHECK",
    );
    fx.records("contract-obligations.sexp", &mutated(repo, OB, "import json,sys; r=json.load(sys.stdin); r['id']='OB-OTHER'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   a requirement names an undefined obligation",
        fx.judge(),
        1,
        "UNDEFINED OBLIGATION",
    );
    fx.records("contract-obligations.sexp", &mutated(repo, OB, "import json,sys; r=json.load(sys.stdin); r['authority']='laboratory'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   an architectural rule labelled a laboratory choice",
        fx.judge(),
        1,
        "AUTHORITY DOWNGRADE",
    );
    fx.records("contract-obligations.sexp", OB);
    let _ = fs::remove_file(p.join("requirements.sexp"));
    tally.arm(
        "RED   an obligation catalogue alone still checks",
        fx.judge(),
        0,
        "__CHECKED__ 1",
    );
    // Partitioned catalogs retain schema validation and cross-record identity checks.
    let _ = fs::rename(
        p.join("contract-obligations.sexp"),
        p.join("part.obligations.sexp"),
    );
    let _ = fs::write(
        p.join("contract-obligations.sexp"),
        "(include-obligations (path \"p/part.obligations.sexp\"))\n",
    );
    tally.arm(
        "GREEN an included obligation is schema checked and linked",
        fx.judge(),
        0,
        "__CHECKED__ 1",
    );
    sed_first(
        &p.join("part.obligations.sexp"),
        &p.join("bad.obligations.sexp"),
        "cpu-guarantee",
        "unknown-direction",
    );
    let _ = fs::write(
        p.join("contract-obligations.sexp"),
        "(include-obligations (path \"p/bad.obligations.sexp\"))\n",
    );
    tally.arm(
        "RED   an included invalid record names its origin",
        fx.judge(),
        1,
        "p/bad.obligations.sexp",
    );
    let _ = fs::copy(
        p.join("part.obligations.sexp"),
        p.join("second.obligations.sexp"),
    );
    let _ = fs::write(p.join("contract-obligations.sexp"), "(include-obligations (path \"p/part.obligations.sexp\"))\n(include-obligations (path \"p/second.obligations.sexp\"))\n");
    tally.arm(
        "RED   duplicate ids across distinct parts remain refused",
        fx.judge(),
        1,
        "DUPLICATE ID",
    );
    let _ = fs::rename(
        p.join("part.obligations.sexp"),
        p.join("contract-obligations.sexp"),
    );
    let _ = fs::remove_file(p.join("bad.obligations.sexp"));
    let _ = fs::remove_file(p.join("second.obligations.sexp"));
    fx.records("requirements.sexp", REQ);
    let _ = fs::remove_file(p.join("contract-obligations.sexp"));
    // ---- rule 9 MIRROR: an obligation naming its requirement restates it ------------------------
    fx.records("requirements.sexp", REQ);
    fx.records("contract-obligations.sexp", OB);
    fx.records("contract-obligations.sexp", &mutated(repo, OB, "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-A'}; r['statement']='S'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "GREEN an obligation mirrored on its requirement",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    fx.records("contract-obligations.sexp", &mutated(repo, OB, "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-A'}; r['statement']='something else'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   an obligation that drifted from its requirement",
        fx.judge(),
        1,
        "MIRROR DRIFT",
    );
    fx.records("contract-obligations.sexp", &mutated(repo, OB, "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-GHOST'}; r['statement']='S'; print(json.dumps(r,ensure_ascii=False))", verbose));
    tally.arm(
        "RED   a mirror of a requirement that does not exist",
        fx.judge(),
        1,
        "MIRROR WITHOUT SOURCE",
    );
    // A frozen mirror is history only with an authenticated active replacement route.
    let ts = t.display().to_string();
    let versioned_mirror = |scenario: &str| fx.program(VERSIONED_MIRROR, &[&ts, scenario]);
    fx.records("requirements.sexp", REQ);
    versioned_mirror("valid");
    tally.arm(
        "GREEN a frozen mirror follows two authenticated replacements",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    versioned_mirror("no-route");
    tally.arm(
        "RED   historical mirror has no effective replacement",
        fx.judge(),
        1,
        "effective replacement also drifts",
    );
    versioned_mirror("unfrozen");
    tally.arm(
        "RED   an open historical record is still a live mirror",
        fx.judge(),
        1,
        "historical mirror is not frozen",
    );
    versioned_mirror("pin");
    tally.arm(
        "RED   changed frozen bytes are never exempt",
        fx.judge(),
        1,
        "does not match its frozen pin",
    );
    versioned_mirror("drift");
    tally.arm(
        "RED   the active replacement must match the current requirement",
        fx.judge(),
        1,
        "effective replacement also drifts",
    );
    versioned_mirror("no-mirror");
    tally.arm(
        "RED   a replacement must explicitly mirror the same requirement",
        fx.judge(),
        1,
        "does not mirror the same requirement",
    );
    versioned_mirror("other-requirement");
    tally.arm(
        "RED   a replacement cannot mirror another requirement",
        fx.judge(),
        1,
        "does not mirror the same requirement",
    );
    versioned_mirror("inheritance");
    tally.arm(
        "RED   a replacement must follow consecutive inheritance",
        fx.judge(),
        1,
        "broken version inheritance",
    );
    versioned_mirror("member");
    tally.arm(
        "RED   a replacement must belong to its declared version",
        fx.judge(),
        1,
        "version member has no matching record",
    );
    versioned_mirror("absent");
    tally.arm(
        "RED   a supersession target must be a current member",
        fx.judge(),
        1,
        "invalid historical-mirror supersession",
    );
    versioned_mirror("duplicate");
    tally.arm(
        "RED   version ownership must be unambiguous",
        fx.judge(),
        1,
        "multiple version owners",
    );
    versioned_mirror("schema");
    tally.arm(
        "RED   a malformed manifest grants no mirror exemption",
        fx.judge(),
        1,
        "invalid version manifest",
    );
    versioned_mirror("live");
    tally.arm(
        "RED   an effective open mirror still rejects ordinary drift",
        fx.judge(),
        1,
        "historical mirror is not frozen",
    );
    versioned_mirror("authority");
    tally.arm(
        "RED   a replacement cannot downgrade architectural authority",
        fx.judge(),
        1,
        "AUTHORITY DOWNGRADE",
    );
    let _ = fs::remove_file(p.join("contract.sexp"));
    let _ = fs::remove_file(p.join("contract-obligations.sexp"));
    // ---- rule 14 MIRROR-DERIVE: the base-corpus mirror, registry-driven ---------------------------
    // Fixture: an owner unit o/ and a mirror unit m/ beside a registry row. The owner's profile declares a one-form base
    // census; the owner's record covers it.
    for d in ["o", "m", "doctrine"] {
        let _ = fs::create_dir_all(t.join(d));
    }
    let _ = fs::write(t.join("o/profile.sexp"), "(profile (scope (count_base 1) (count_total 1) (authority architecture) (source \"s\") (base_op \"ADD\")))\n");
    let root_s = repo.display().to_string();
    fx.program(DERIVE_FIXTURE, &[&ts, &root_s]);
    // the registry names repo-relative paths (the fixture root stands in for the repo root)
    let _ = fs::write(t.join("doctrine/fact_ownership.tsv"), "base-requirements (m)\to/requirements.sexp\tm/requirements.sexp\tRECORD-SCHEMA\nbase-obligations (m)\to/contract-obligations.sexp\tm/contract-obligations.sexp\tRECORD-SCHEMA\n");
    tally.arm(
        "GREEN the faithful mirror checks",
        fx.judge(),
        0,
        "__CHECKED__ 7",
    );
    fx.program(DERIVE_EDITED, &[&ts, &root_s]);
    tally.arm(
        "RED   a mirror record edited after the copy",
        fx.judge(),
        1,
        "MIRROR DRIFT",
    );
    fx.program(DERIVE_DROPPED, &[&ts, &root_s]);
    tally.arm(
        "RED   the mirror missing the obligation record",
        fx.judge(),
        1,
        "MISSING MIRROR",
    );
    fx.program(DERIVE_OWNER_CONTRACT, &[&ts, &root_s]);
    tally.arm(
        "RED   the mirror keeping the owner's contract",
        fx.judge(),
        1,
        "the mirror keeps",
    );
    for d in ["o", "m", "doctrine"] {
        let _ = fs::remove_dir_all(t.join(d));
    }
    // ---- rules 10+11: the unit registry and the layer rule (MODEL-METHOD.2) ---------------------
    let _ = fs::remove_file(p.join("units.sexp"));
    let _ = fs::remove_file(p.join("category-needs.sexp"));
    fx.records("category-needs.sexp", BOARD_MISSING);
    tally.arm(
        "RED   layer claims without the registry they describe",
        fx.judge(),
        1,
        "NO REGISTRY",
    );
    fx.records(
        "units.sexp",
        r#"{"id":"p","kind":"processor","layer":"processor","book":"b"}"#,
    );
    fx.records("category-needs.sexp", BOARD_MISSING);
    tally.arm(
        "RED   the acceptance's rule: a board-layer 'missing' for a processor",
        fx.judge(),
        1,
        "LAYER LIE",
    );
    fx.records("category-needs.sexp", r#"{"category":"C07","layer":"processor","kind":"isa-manual","unit":"p","disposition":"missing"}"#);
    tally.arm(
        "RED   a 'missing' that owes no reason",
        fx.judge(),
        1,
        "REASONLESS MISSING",
    );
    fx.records("category-needs.sexp", r#"{"category":"C01","layer":"processor","kind":"isa-manual","unit":"p","disposition":"covered"}"#);
    tally.arm(
        "RED   a 'covered' naming no material",
        fx.judge(),
        1,
        "UNEVIDENCED COVERED",
    );
    // `python3 - <<PYEOF` (unquoted: `$t` expanded, the rest literal) — the materials catalogue beside the census.
    let catalog_program = format!(
        "import pathlib\npathlib.Path('{t}/p/catalog.sexp').write_text(\n    '(materials (schema-version 1) (cache-root \".materials\")\\n'\n    '(material (id \"M\") (title \"t\") (revision \"r\") (release-kind ratified) (kind snapshot)\\n'\n    '(licence \"l\") (corpus-path \"c\") (cache-path \"c\") (sha256 \"' + 'a' * 64 + '\")))\\n')\n",
        t = t.display()
    );
    let _ = python_stdin(repo, &catalog_program, &[], false, verbose);
    fx.records("category-needs.sexp", r#"{"category":"C01","layer":"processor","kind":"isa-manual","unit":"p","disposition":"covered","material":"GHOST-DOC"}"#);
    tally.arm(
        "RED   a covered-by that names no held document",
        fx.judge(),
        1,
        "UNRESOLVED MATERIAL",
    );
    fx.records("category-needs.sexp", r#"{"category":"C01","layer":"processor","kind":"isa-manual","unit":"p","disposition":"covered","material":"M"}|||{"category":"C07","layer":"processor","kind":"isa-manual","unit":"p","disposition":"missing","reason":"F/D excluded"}"#);
    tally.arm(
        "GREEN a registry and an honest census",
        fx.judge(),
        0,
        "__CHECKED__ 3",
    );
    let _ = fs::write(p.join("units.sexp"), "");
    fx.records("category-needs.sexp", BOARD_MISSING);
    tally.arm(
        "RED   an empty unit registry",
        fx.judge(),
        1,
        "contains no records",
    );
    let _ = fs::remove_file(p.join("units.sexp"));
    let _ = fs::remove_file(p.join("category-needs.sexp"));
    // ---- rule 13 CAMPAIGN: the ACT4 record carries only counts its rows re-derive -----------
    fx.fixed("act4.sexp", BASE_CAMPAIGN, "");
    tally.arm(
        "GREEN a consistent campaign record — one failing test, honestly recorded",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    fx.fixed("act4.sexp", BASE_CAMPAIGN, "(tests 2)@@@(tests 3)");
    tally.arm(
        "RED   a carried test count the rows contradict",
        fx.judge(),
        1,
        "CAMPAIGN COUNT",
    );
    fx.fixed(
        "act4.sexp",
        BASE_CAMPAIGN,
        "(signature_slots 5)@@@(signature_slots 6)",
    );
    tally.arm(
        "RED   a carried slot total the rows contradict",
        fx.judge(),
        1,
        "CAMPAIGN SLOTS",
    );
    fx.fixed(
        "act4.sexp",
        BASE_CAMPAIGN,
        "\"1 pass / 1 fail\"@@@\"2 pass / 0 fail\"",
    );
    tally.arm(
        "RED   a verdict summary the rows contradict",
        fx.judge(),
        1,
        "CAMPAIGN VERDICTS",
    );
    fx.fixed(
        "act4.sexp",
        BASE_CAMPAIGN,
        "verdict_semulith \"pass\"@@@verdict_semulith \"green\"",
    );
    tally.arm(
        "RED   a verdict outside the closed vocabulary",
        fx.judge(),
        1,
        "CAMPAIGN VOCABULARY",
    );
    fx.fixed(
        "act4.sexp",
        BASE_CAMPAIGN,
        "(signature \"agree\")@@@(signature \"fine\")",
    );
    tally.arm(
        "RED   a comparison verdict outside the closed vocabulary",
        fx.judge(),
        1,
        "CAMPAIGN VOCABULARY",
    );
    let _ = fs::remove_file(p.join("act4.sexp"));
    // ---- rule 15 WORKLOAD: the workload record carries only counts its rows re-derive -------
    fx.fixed("workload.sexp", BASE_WORKLOAD, "");
    tally.arm(
        "GREEN a consistent workload record — one failing workload, honestly recorded",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    fx.fixed(
        "workload.sexp",
        BASE_WORKLOAD,
        "(workloads 2)@@@(workloads 3)",
    );
    tally.arm(
        "RED   a carried workload count the rows contradict",
        fx.judge(),
        1,
        "WORKLOAD COUNT",
    );
    fx.fixed(
        "workload.sexp",
        BASE_WORKLOAD,
        "(signature_slots 5)@@@(signature_slots 6)",
    );
    tally.arm(
        "RED   a carried slot total the rows contradict",
        fx.judge(),
        1,
        "WORKLOAD SLOTS",
    );
    fx.fixed(
        "workload.sexp",
        BASE_WORKLOAD,
        "\"1 pass / 1 fail\"@@@\"2 pass / 0 fail\"",
    );
    tally.arm(
        "RED   a verdict summary the rows contradict",
        fx.judge(),
        1,
        "WORKLOAD VERDICTS",
    );
    fx.fixed(
        "workload.sexp",
        BASE_WORKLOAD,
        "verdict_sail \"pass\"@@@verdict_sail \"green\"",
    );
    tally.arm(
        "RED   a verdict outside the closed vocabulary",
        fx.judge(),
        1,
        "WORKLOAD VOCABULARY",
    );
    fx.fixed(
        "workload.sexp",
        BASE_WORKLOAD,
        "(compressed 4)@@@(compressed 40)",
    );
    tally.arm(
        "RED   a census with more compressed than instructions",
        fx.judge(),
        1,
        "WORKLOAD CENSUS",
    );
    let _ = fs::remove_file(p.join("workload.sexp"));
    // ---- rule 14 CREDITS: the credit catalogue reads through its own reader, never the pinned one -
    // ($t/schema is the fixture's link to the real schema directory: never copy into or remove under it)
    let credit = format!(
        "(credit (id \"CR-1\") (profile_ids \"p\") (requirement_id \"REQ-D-A\") (obligation_ids \"OB-A\") (case_id \"case\") (measured (pin (path \"m\") (sha256 \"{a}\") (byte_size 1))) (receipt (pin (path \"r\") (sha256 \"{b}\") (byte_size 1))) (policy (pin (path \"p\") (sha256 \"{c}\") (byte_size 1))) (retained_sources \"S\") (authority review) (date \"2026-10-26\") (decision \"decision_x.md\") (legs 10) (limitations \"l\"))",
        a = "a".repeat(64),
        b = "b".repeat(64),
        c = "c".repeat(64)
    );
    let _ = fs::write(p.join("credits.sexp"), format!("{credit}\n"));
    tally.arm(
        "GREEN a credit catalogue reads through its own reader",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    let _ = fs::write(p.join("credits.sexp"), format!("{credit}\n{credit}\n"));
    tally.arm(
        "RED   a duplicate credit id",
        fx.judge(),
        1,
        "duplicate credit id",
    );
    let _ = fs::write(p.join("credits.sexp"), "");
    tally.arm(
        "RED   an empty credit catalogue",
        fx.judge(),
        1,
        "contains no records",
    );
    let _ = fs::remove_file(p.join("credits.sexp"));
    // ---- the JSONL track (examples stay JSONL) -------------------------------------------------
    let _ = fs::write(p.join("requirements.jsonl"), format!("{REQ}\n"));
    tally.arm(
        "GREEN a JSONL record validates on the old track",
        fx.judge(),
        0,
        "__CHECKED__ 2",
    );
    let _ = fs::write(p.join("mystery.jsonl"), "not json at all\n");
    tally.arm(
        "RED   a record file no schema governs",
        fx.judge(),
        1,
        "UNGOVERNED",
    );
    let _ = fs::remove_file(p.join("mystery.jsonl"));
    let _ = fs::write(p.join("requirements.jsonl"), "not json at all\n");
    tally.arm(
        "RED   a malformed JSONL line",
        fx.judge(),
        1,
        "not valid JSON",
    );
    let _ = fs::write(p.join("requirements.jsonl"), "");
    tally.arm(
        "RED   an empty JSONL record file",
        fx.judge(),
        1,
        "contains no records",
    );
    for f in [
        "requirements.jsonl",
        "requirements.sexp",
        "contract-obligations.sexp",
    ] {
        let _ = fs::remove_file(p.join(f));
    }
    tally.arm(
        "REFUSE nothing to check at all",
        fx.judge(),
        2,
        "NO RECORDS",
    );

    tally.arm(
        "GREEN catalog reader controls",
        probe(repo, false, "scripts/probe_record_catalog.py", None),
        0,
        "31 pass / 0 fail",
    );
    tally.arm(
        "RED lost include expansion",
        probe(
            repo,
            false,
            "scripts/probe_record_catalog.py",
            Some("ignore-includes"),
        ),
        1,
        "CONTROL-MISSED",
    );
    // All project token patterns, and the public kernel's deliberate search contract.
    tally.arm(
        "GREEN exact-token facets normal",
        probe(repo, false, "scripts/probe_schema_token_facets.py", None),
        0,
        "Ran 7 tests",
    );
    tally.arm(
        "RED normal token loose-end mutation",
        probe(
            repo,
            false,
            "scripts/probe_schema_token_facets.py",
            Some("loose-end"),
        ),
        1,
        "FAILED (failures=106)",
    );
    tally.arm(
        "RED normal token ignore-pattern mutation",
        probe(
            repo,
            false,
            "scripts/probe_schema_token_facets.py",
            Some("ignore-pattern"),
        ),
        1,
        "FAILED (failures=612)",
    );
    tally.arm(
        "RED normal token fullmatch mutation",
        probe(
            repo,
            false,
            "scripts/probe_schema_token_facets.py",
            Some("fullmatch"),
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "GREEN exact-token facets optimized",
        probe(repo, true, "scripts/probe_schema_token_facets.py", None),
        0,
        "Ran 7 tests",
    );
    tally.arm(
        "RED optimized token loose-end mutation",
        probe(
            repo,
            true,
            "scripts/probe_schema_token_facets.py",
            Some("loose-end"),
        ),
        1,
        "FAILED (failures=106)",
    );
    tally.arm(
        "RED optimized token ignore-pattern mutation",
        probe(
            repo,
            true,
            "scripts/probe_schema_token_facets.py",
            Some("ignore-pattern"),
        ),
        1,
        "FAILED (failures=612)",
    );
    tally.arm(
        "RED optimized token fullmatch mutation",
        probe(
            repo,
            true,
            "scripts/probe_schema_token_facets.py",
            Some("fullmatch"),
        ),
        1,
        "FAILED (failures=1)",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "RECORD-SCHEMA --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// The body lines of the judge's output indented two spaces on stderr (`printf '%s\n' "$body" | sed 's/^/  /'`).
fn indented(body: &str) {
    for line in body.split('\n') {
        eprintln!("  {line}");
    }
}

/// `cargo xtask check-requirements [--self-test|--audit]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!("RECORD-SCHEMA: REFUSED — python3 is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    // --audit: report referential problems in record files the gate deliberately does NOT enforce.
    if args.first().is_some_and(|arg| arg == "--audit") {
        let mut command = Command::new("python3");
        command.arg("-").current_dir(root).stdin(Stdio::piped());
        if let Ok(mut child) = command.spawn() {
            if let Some(mut stdin) = child.stdin.take() {
                let _ = stdin.write_all(AUDIT.as_bytes());
            }
            let _ = child.wait();
        }
        return ExitCode::SUCCESS;
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join("schemas").is_dir() {
        println!("RECORD-SCHEMA: ok (no schemas/ yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("RECORD-SCHEMA: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    // `out="$(check_records .)"`: the root as `.`, stdout captured, stderr through.
    let (rc, raw) = {
        let mut command = Command::new("python3");
        command
            .arg("-")
            .arg(".")
            .current_dir(root)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit());
        match command.spawn() {
            Ok(mut child) => {
                if let Some(mut stdin) = child.stdin.take() {
                    let _ = stdin.write_all(JUDGE.as_bytes());
                }
                match child.wait_with_output() {
                    Ok(o) => (
                        o.status.code().unwrap_or(-1),
                        String::from_utf8_lossy(&o.stdout).into_owned(),
                    ),
                    Err(e) => (-1, e.to_string()),
                }
            }
            Err(_) => (-1, "cannot run python3".to_owned()),
        }
    };
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
    if rc == 2 {
        eprintln!("RECORD-SCHEMA: REFUSED — the record corpus or a schema could not be read.");
        indented(body);
        return ExitCode::from(2);
    }
    if rc != 0 {
        eprintln!(
            "RECORD-SCHEMA: a record file contradicts its schema, its sources, or its profile."
        );
        indented(body);
        eprintln!(
            "  The SCHEMA and the PROFILE are authoritative. Fix the record, not the contract."
        );
        return ExitCode::from(1);
    }
    let count = if count.is_empty() {
        "0"
    } else {
        count.as_str()
    };
    // ---- JSONL track, engine 2: the workspace's own Rust checker (P1-LAB.7) -----------------------
    if root.join("examples/fixture-context.json").is_file() {
        if !on_path("cargo") {
            eprintln!(
                "RECORD-SCHEMA: REFUSED — cargo is not on PATH; the Rust engine cannot judge."
            );
            return ExitCode::from(2);
        }
        let (rust_rc, rust_raw) = combined(
            Command::new("cargo")
                .args([
                    "run",
                    "--quiet",
                    "--offline",
                    "-p",
                    "semulith-cli",
                    "--",
                    "check-examples",
                ])
                .current_dir(root),
        );
        let rust_out = captured(&rust_raw);
        if rust_rc == 2 {
            eprintln!(
                "RECORD-SCHEMA: REFUSED — the Rust checker could not judge (inputs or usage)."
            );
            indented(rust_out);
            return ExitCode::from(2);
        }
        if rust_rc != 0 {
            eprintln!("RECORD-SCHEMA: the Rust graph checker rejects the JSONL records.");
            indented(rust_out);
            eprintln!(
                "  The RECORDS are the only mutable side; the schemas, the ledger and the graph"
            );
            eprintln!("  rules are the contract.");
            return ExitCode::from(1);
        }
        println!("RECORD-SCHEMA: ok ({count} record file(s) validate and agree with their profile; the Rust graph checker accepts the examples bundle)");
        return ExitCode::SUCCESS;
    }
    println!("RECORD-SCHEMA: ok ({count} record file(s) validate and agree with their profile)");
    ExitCode::SUCCESS
}
