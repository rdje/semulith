# CHANGELOG shard — SEMILITH-SF-0059 … SEMILITH-SF-0057

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-SF-0059 (leaf SOT-FORMAT.4) — the dossier moves behind the schema layer, commentary and all

The profile dossier retires its last TOML/JSON: `profile.toml` (26 decisions), `state.json`,
`sources.toml`, `references.toml`, the matched Sail override and the four guest expectation
files are now one S-expression document form each — `profile.sexp`, `state.sexp`,
`sources.sexp`, `references.sexp`, `reference/sail-rv64i-lab-v0.override.sexp`,
`guests/*.expected.sexp` — validated by six new schemas (`schema/{profile,state,sources,
references,override,expectations}.sexp`). `convert_dossier.py --verify` proves the migration
the way `.3` did: every document re-derives field-for-field from its source, and the comment
census is exact line by line.

⭐ **Comments became first-class forms.** The schema kernel reserves one head — `(comment "…")`,
inert at any position, never declared, never forbidden — and the dossier's 158 comment lines
(the warnings, the provenance, the "why" of 26 decisions) survive as data a merge can carry
instead of syntax a parser drops. A typo'd `commment` is still refused by name; a construct,
operator or field named `comment` is refused as dead vocabulary. The open question the tree
carried — do comments belong to the form or the file — is answered: to the file, as an ordered
annotation stream.

**Consumers changed at the seam, not in their logic.** Every gate and tool keeps receiving the
exact dicts `tomllib`/`json` produced, now through the single mapping owner
`scripts/dossier_sexp.py` — which is what makes the verdicts mechanical rather than hopeful:
`PROFILE-CONSISTENCY`'s 39 arms re-fire on converted fixtures (rule 5b included), `run_smoke`
and `compare_platforms` are unmoved, the regenerated G0 report's diff is input names only, and
the Sail override's JSON is *derived* from the tracked `.sexp` on every run — byte-identical to
the original it replaces, the `.sexp` the single source of truth. `compare_readers` sweeps 28
of 28 files across all three readers. Measured en route: the DOSSIER's "no gate has been run"
was stale (`G0` has run; verdict `incomplete`) — corrected; `schema/` reached its file-count
ceiling at exactly 12 and was re-derived to 24, grounds recorded in the registry; the
`profiles/` per-part re-derivation `.3` carried open was not needed (`references.sexp` is
30,012 B against 32,768).

====

## SEMILITH-SF-0058 (leaf SOT-FORMAT.3) — the records move behind the schema layer

`profiles/rv64i-lab-v0/{requirements,contract-obligations}.jsonl` (26 + 34 records) retire into
`{requirements,contract-obligations}.sexp`, one form per record, JSON keys verbatim as field
names. The losslessness the acceptance demands is a comparison, not a review:
`convert_records.py --verify` re-derives the JSONL from the converted files **byte-identical**,
field by field, both catalogues.

⭐ **The schema layer grew four field facets rather than go weaker than the contract it
replaces** — `(pattern …)`, `(min-length N)`, `(min N)`, `(unique yes)` on `(field …)`, the
`.2` boundary one level down (a new declaration KIND would change the kernel; facets on the
existing kind are the language; the fixpoint declares them). And `parameters` stopped being a
lie: the old JSON schema's `additionalProperties` banned the very arrays three obligations
write and the validator never descended into it — the new format types every value
(`(int …)/(str …)/(true)/(false)/(null)/(ints …)/(strs …)`) and refuses a float, a mixed list
or a nested value by name.

**`RECORD-SCHEMA` reads both tracks now**: the frozen `examples/` JSONL on the tracked JSON
validator; the converted catalogues through the single mapping owner `scripts/records_sexp.py`,
validated by the schema layer plus every cross-check (CITED / RESOLVED / COVERAGE / LINKED /
OBLIGED / AUTHORITY) re-fired against the converted form — 22 arms where 15 stood, each RED arm
naming its reason. `gate_report.py` reads the same mapping; the G0 report diff is input names
only (26 requirements, 34 obligations, 68 checks, verdict untouched). `compare_readers` sweeps
13 of 13 with the catalogues and the two new schemas in corpus; `run_smoke` and the 52-of-52
verdict are unmoved. Measured en route: `LIVE_STATUS.md` had carried the contract as 33
obligations / 66 checks since before `P0-PROFILE.10`; re-derived to 34 / 68.


## SEMULITH-DS-0002 (leaf DOC-SHARDING.1) — the fired ceiling gets its sharder, and the freeze gets its proof

**Measured trigger.** `CHANGELOG.md` sat at 65,527 of 65,536 bytes — 9 bytes of headroom, recorded
at adoption as transition debt with this leaf as its named owner. The registry's owner column
promised *shard when the ceiling fires*; this slice is the sharder, not another compressed entry.

**What landed.** `scripts/shard_history.py` moves the oldest whole `## ` entries — byte-verbatim,
a file is preamble plus concatenated blocks, so head-after + shard == head-before exactly,
asserted and printed at the event (29 entries: 28 kept + 1 moved, order and bytes exact). One
entry moved (`SEMILITH-P0-0031`, 3.4 KiB); the head rewrote 65,527 → 62,086 bytes, under target
with room for this entry. Re-running is a no-op. The two existing date-named shards stay
untouched — a shard's entries are never edited — and join the new freeze manifest
`docs/changelog/SHARDS.sha256` (3 rows, sha256sum format, paths repo-root-relative).

**`SHARD-FREEZE`** — the 13th project doctrine, 12 self-test arms, each RED arm naming its reason —
proves the durable half: every shard hashes to its manifest row (one edited byte after the event
fails with both digests named); the manifest only grows against `git show HEAD:…`; no `## `
heading appears twice across head and shards. ⛔ Fired RED on the real tree before registration:
with no manifest yet, both existing shards reported `UNMANIFESTED` — the adoption gap itself, not
a synthetic stand-in. ⭐ The completeness proof belongs to the shard event (the tool holds both
sides exactly once); the freeze proof belongs to the manifest (it holds every side forever) —
splitting the two halves is what makes each half checkable.

**Lockstep, because mirrors rot.** Both doctrine mirrors gain the row (`DOCTRINE_ENFORCEMENT.md`
and the book chapter, per `REGISTRY-MIRROR`); `LIVE_STATUS.md`'s derived counts move 12 → 13
doctrines and 157 → 169 self-test arms — re-derived by `check_derived_counts.sh --list`, never
incremented by hand; `README_POLICY.md`'s transition-debt note records the discharged half and
leaves `DEV_NOTES.md` its still-live trigger for the day its ceiling fires.

## SEMULITH-RM-0060 — browser/Wasm target

`decision_browser-wasm-target`; lane `PORT-WEB` (consumed by `P1-LAB`).

## SEMILITH-SF-0057 (leaf SOT-FORMAT.2) — the constructs already in use, declared as data

The schema layer leaves paper: `schema/encoding.sexp`, `schema/fragment.sexp` and
`schema/semantics.sexp` declare every construct the three corpus families write — records and
positional mini-languages alike. The schema language gains exactly one new declaration kind,
`(operator (name SYM) (fixed N) | (variadic) [(min N)] [(arg SPEC)])`, for the shapes no record
grammar can state: `(fixed (31 25 0x0) …)` triples, `(operands rd rs1 rs2)` lists, the
`(pieces (12 12) …)` pairs, and the semantics effect expressions. `scripts/check_semantics.py`
now loads its 32-form table from `schema/semantics.sexp` — a new semantic form is a schema
edit, zero lines of Python (demonstrated with a 33rd form, then reverted). The `52 of 52`
verdict is byte-identical; the four MODEL-METHOD.9 controls still fire RED. Kernel self-test
`16 → 31 arms`; the whole corpus validates against its schema; `compare_readers` sweeps the
three new files the moment they are tracked (`9 of 9 agree`, document layer zero class notes).
The layer that never reads a second file: operand scoping stays in the checker. Gate
registration stays deferred to `SOT-FORMAT.6` per the tree's frontier. Tree `SOT-FORMAT` at
5/10.

