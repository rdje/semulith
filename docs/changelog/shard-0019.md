# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — a partial validator must refuse, not skip

- No JSON Schema library exists on this host and installing one would put a dependency store off
  the repository volume, so the validator is 180 tracked lines covering exactly the 17 keywords a
  census of `schemas/*.json` found. ⛔ **The soundness property is the REFUSAL.** A partial
  validator that silently ignores an unimplemented keyword reports `valid` for a document it never
  fully checked — so this one raises `UnsupportedSchema`, and a schema gaining a keyword breaks
  the gate loudly instead of widening what passes.
- ⭐ `source_semantics.category` is **not** a function of the profile's `authority`. `laboratory`
  covers both "the spec says UNSPECIFIED and we chose" and "the spec delegates to the EEI and we
  chose"; collapsing them records a laboratory policy as an architectural rule.
- The sharpest gate rule this leaf adds: `research_status: resolved` may not coexist with an
  `OPEN:` note. Both halves are true separately, which is what makes the pair convenient.
- ⛔ Two defects in the new gate were found by its own arms, not by review. It excluded `target/`
  by ABSOLUTE path — and its own fixtures live under `target/doctrine-selftest/`, so all ten arms
  failed with "no .jsonl record file found". And the cross-checks re-parsed a file that had
  already failed to parse, crashing the gate rather than failing it: a traceback is not a verdict.
- Promotion is explicitly declined in the owning leaf, with the reason.

