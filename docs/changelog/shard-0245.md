# DEV_NOTES shard — _(2026-10-11)_ … _(2026-10-10)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-11)_ — authenticate file pins (P4-SYSTEM.14 a15)

experiment_artifacts.py reuses is_canonical_path. Descriptor-anchored traversal
refuses symlinks, special files, nested Git markers and foreign devices. Regular
files stream in1MiB chunks, bounded by initial size plus one. Descriptor, filename,
parent and renewed Git-boundary checks refuse replacement. ExitStack attempts all
close callbacks; callback failure cannot yield a match.

Pin39/0 (also optimized), graph63/0/profile53/0 and focused13 pass. Real on-volume
fixtures exercise streaming, timed replacement and descriptor cleanup; foreign
devices and I/O/close errors are injected. Marker-only fixtures never initialize
another repository. Twelve independent predicate omissions expose intended
controls, with cleanup even for mutants. Actual checker integration diagnoses bad
hashes/missing files; matching files still receive the pending comparison refusal.

Pins establish check-time bytes, not execution, comparison, currentness or adequacy.
No capture/store/canonical/runtime/generated/archive/cap/acceptance change. Seven
books and rendered examples pass. The final route check caught live-note overflow;
this entry was tightened without raising its ceiling. Evidence target/p4-system-14/a15.
promotion: matched-experiment decision and GC book own the contract and limits.

## _(2026-10-10)_ — check declared capture edges before artifact qualification (P4-SYSTEM.14 a14)

Add experiment_verification.py with one raw-form entrypoint: schema validation
precedes the existing mapper. Check scoped requirements/effective obligations,
unique child IDs, producer/model/input relationships, run observations and repeat
edges, control relationships and pair assessments. load_scope reuses the public
gate_report.contract_measure selector and filters profile membership. Keep failed
controls and ancestry uncertainty honestly representable; these checks confer no
adequacy/independence credit. Lexical paths/nonnegative sizes are checked; actual
filesystem, pin, process, comparison and policy validation remain pending.

Graph63/0 and PROFILE-CONSISTENCY52/0 pass. Nine separately removed predicates
expose their intended controls, including effective-version filtering. Refine the
reused-observation/control endpoint assertions to require their own diagnostic,
so an orphan side effect cannot mask the omitted predicate. Actual checker
integration against predecessor9ec6bfe shows newly specific missing-repeat and
raw-duplicate refusals; a consistent graph still gets only the pending qualifier
refusal. An added U+0085 case reproduces a false GREEN in the initial C0/DEL-only
path predicate; cover C1 as well and retain the regression. Graph63/0 also passes
under Python optimization. Focused13 and seven books/rendered explanation pass;
protected existing files/canonical data/generated consumers/archive/caps stay exact.
No fresh capture or acceptance credit; artifact/comparison evaluation follows.

Evidence target/p4-system-14/a14. promotion: the matched-experiment decision and
its live GC book explanation retain the implemented scope, examples and limits.

