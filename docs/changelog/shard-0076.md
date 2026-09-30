# CHANGELOG shard — SEMILITH-DS-0003 … SEMILITH-DS-0003

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-DS-0003 (leaf DOC-SHARDING.2) — DEV_NOTES joins the shard family

- `DEV_NOTES.md` gets `CHANGELOG.md`'s lifecycle, by generalization rather than a fork: `scripts/shard_history.py` writes a shard header naming the head it was cut from and that head's own registry ceiling (`# DEV_NOTES shard … 48 KiB`; CHANGELOG's `.1` header shape stays byte-identical, self-test arm), and `scripts/check_changelog_shards.sh` learns the two-head family — one COVERAGE/FROZEN/APPEND-ONLY scan over the shared `docs/changelog/` manifest, UNIQUE across both live heads + shards. First event: 2 entries to `shard-0027.md`, `31 == 29+2` proved at the event, head 48,954 → 46,212, 29-row manifest frozen.
- Both tools fired RED on the real tree pre-commit (a scratch shard carrying a live DEV_NOTES heading; the old sharder writing CHANGELOG-provenanced DEV_NOTES shards). The new UNIQUE leg then exposed two stray duplicate headings inside DEV_NOTES.md itself — removed; each entry exists exactly once. The registry comment that claimed DEV_NOTES was already sharded (designed end-state stated as present fact) is corrected.
- Verification: sharder self-test 12/0, SHARD-FREEZE self-test 14/0, gate green; doctrine mirrors and the routed-destination count (31, unchanged — one family, not a new directory) in sync.

