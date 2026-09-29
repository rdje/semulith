# CHANGELOG shard — SEMILITH-SF-0060 … SEMILITH-SF-0060

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-SF-0060 (leaf SOT-FORMAT.5) — the record merge is definable, and it decides

The union this tree exists for is now checked: `scripts/merge_records.py` merges two units'
requirements, obligations and pinned sources by id — the same id must carry the same content
(`profile_ids` excepted: it is membership, and it unions), a source id must pin the same
bytes, and every dependency, obligation link and citation must resolve across the union. Two
units compose, or the refusal names the conflicting fact, both values, both units. The real
profile composes with itself (26 + 34 + 3); one edited statement in a copied unit is refused
naming the field; an extension unit whose requirement depends on the base's `REQ-D-XLEN`
composes — and is refused by name when the base is withheld. `MODEL-COMPOSE.3` reads the merged
view (`merge_units(…)` plus the direction census: 26 cpu-guarantee, 8 environment-assumption).

⭐ **Two defects found by probe before any code, both closed.** RECORD-SCHEMA never refused
duplicate record ids — its id → record map collapsed them last-wins, so a catalogue could
contradict itself and stay green (`rc=0`, measured) — rule 8 (UNIQUE-ID) now refuses, 23 arms.
And obligation `dependencies` were checked against nothing: the corpus's cpu-guarantees depend
on requirements while its environment-assumptions depend on guarantees — a mixed namespace the
new closure resolves against requirements ∪ obligations, measured on all 42 records, zero
dangling.

