# CHANGELOG shard — SEMILITH-MM-0046 … SEMILITH-MM-0045

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-MM-0046 (leaf MODEL-METHOD.2) — the materials requirement: what each unit owes its model

The catalogue of documents gains the requirement layer: `schema/units.sexp` +
`schema/category-needs.sexp` declare two record families (zero kernel lines), and
`materials/units.sexp` + `materials/category-needs.sexp` carry the one-row registry and all 24
INFORMATION_CATALOG categories for `rv64i-lab-v0` — each bound to the material kind that
supplies it, at its layer, with an honest disposition. The vocabulary distinguishes ABSENT from
NEVER-NEEDED: `missing` (a reason is owed — C07/C08/C12/C15/C16/C18, excluded subsystems) versus
`out-of-scope` (C17/C19–C21, board-layer facts a processor never owed). RECORD-SCHEMA rules 10–11
enforce it — the acceptance's shape, a board-layer `missing` for a processor, refuses as
`LAYER LIE` — 6 new arms, 32 total, 7 record files green. The DSP-specific questions of the
catalog's §5 ride as their own D-category ids, admitted by the schema and pre-built for nobody.

## SEMILITH-MM-0045 (leaf MODEL-METHOD.7) — the no-duplicated-fact rule is a registry, and every mirror is governed

"Single source of truth" now means one owner per fact, mechanized. `doctrine/fact_ownership.tsv`
names the one owning file per fact kind (8 kinds — configuration, state, encodings, semantics,
requirements, obligations, pinned sources, materials), each legal derived mirror, and the
doctrine governing every owner→mirror pair; `FACT-OWNERSHIP` (18th doctrine, 8 arms) verifies one
owner each, owners exist, every governor is a registered doctrine that runs, and the corpus's four
restatement pairs are all named. The acceptance's shape — a fact stated in two, refused — fires as
`UNGOVERNED MIRROR` and `UNREGISTERED MIRROR PAIR`.

⭐ The inventory found what the rule exists to catch: the corpus's mirrors were mostly governed
(decision↔requirement by RECORD-SCHEMA; state↔profile by PROFILE-CONSISTENCY; composition↔fragments
by UNIT-COMPOSITION), but 28 obligations restate their requirement's statement — all matching
today, nothing refusing the day one drifts. RECORD-SCHEMA gains rule 9 (MIRROR) with 3 arms; 26
total. An ungoverned mirror is how one fact quietly becomes two; the registry makes that a verdict.

