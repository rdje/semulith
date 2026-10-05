# CHANGELOG shard — SEMULITH-P4-0007 … SEMULITH-P4-0007

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0007 (leaf P4-SYSTEM.2, slice c2) — the rv64gc module's tracked landing is flip-bound; the scratch engine proof recorded

- The (c2) judgment, measured rather than assumed: STATE-GEN proves rv64i's state.rs
  byte-exact from its TRACKED descriptor in a fresh clone; a tracked rv64gc module
  generated from the staged (untracked) document would be unjudgeable there — a copy, not
  a derivation. The three alternatives were each measured dishonest (a skip-if-absent
  gate leg = a standing hole in the byte-exact property; a hand-written interim module =
  a second owner, OWN-01; a non-unit descriptor home = a category lie). So the module
  lands with the descriptor at the flip (slice h), in one green commit, with STATE-GEN's
  census and the FACT-OWNERSHIP rows extending there. Recorded as
  `decision_generated-mirror-needs-tracked-input`; constrains slice (d) the same way.
- The interim evidence, at scratch: the generated module (40,198 bytes) compiles
  standalone and a `rustc --test` harness exercises it behaviorally — reset per the
  document (mode M, mstatus `0xA0000000`, misa at the declared value), the 33-CSR address
  lookup, the view discipline, the field tables (the medeleg 11/16 read-only-0 rows, TSR
  at bit 22 per the pinned encoding.h), x0 hardwired, mode transitions — 4 passed / 0
  failed. Harness and module at `target/p4-system-2/gen/` (untracked, by design).

