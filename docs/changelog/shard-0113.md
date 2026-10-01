# CHANGELOG shard — SEMULITH-PX-0001 … SEMULITH-MM-0059

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PX-0001 (leaf PREFIX-DISCIPLINE.1) — the SEMULITH- prefix, pinned at the boundary and watched

- The director ruled the work-unit prefix is SEMULITH, never SEMILITH. Measured drift at
  ruling time: 123 commits carry both spellings across 10+ areas; exactly one subject
  ("Initial commit") carries neither. History is immutable, so enforcement is
  forward-looking: the `commit-msg` hook now refuses any leading work-unit id not beginning
  with `SEMULITH-`, with `SEMULITH` named in the refusal.
- `COMMIT-PREFIX` (#29, `scripts/check_commit_prefix.sh`) probes the hook BEHAVIOURALLY on
  every commit — the pin lives in a neutral scaffold file a sync can revert, and carrying it
  upstream is unavailable by policy, so a silent revert turns the next commit RED, named.
  Fired RED against the real tree before the pin existed; self-test 4/0.
- The ruling is recorded: `decision_work-unit-prefix-semulith.md` + INDEX; COMMIT.md states
  the pinned prefix; both registry mirrors carry the row; LIVE_STATUS re-derived
  (29 doctrines / 301 arms). The tree closes 1/1.
- `make gate` all green. DEV_NOTES.md crossed its 48 KiB ceiling with this slice's note and
  was sharded (the DOC-SHARDING machinery, completeness exact).

## SEMULITH-MM-0059 (leaf MODEL-METHOD.17) — the channel answers: the poller fix measured, the heard gaps reconciled

- chipdoc fixed the poller deafness `.16` surfaced (corpus `6bfabf2`): the poller descends
  into the `(materials …)` wrapper and READS this catalogue's nested gaps. Measured here,
  not accepted: `semulith_gaps_open: 2` pre-reconcile — the signal `.16` could not get.
- The two heard records were already dispositioned here: `GAP-INTEL-SDM-VOL1` (closed by
  `.13`'s catalogued material) and `GAP-RISCV-JAN-2026-PDF` (closed by `.12`'s recorded
  decline decision). Both now carry `(status resolved)` with evidence; post-reconcile the
  poller reports 0 open, 0 unmirrored.
- The v20260120 gap's deafness claim updated to the fixed channel; corpus re-pinned
  `f33d330` → `92a73b6` (5313 files / 257 PDFs re-derived by the same path sweep, unchanged);
  the channel snapshot refreshed (feed 68/14; REQ-008 at `2026-09-29`).
- The channel is now TWO-WAY: a new gap filed in `materials/catalog.sexp` surfaces to
  chipdoc without an operator relay.
- `make gate` all green. CHANGELOG.md crossed its 64 KiB ceiling with this entry and was
  sharded (the DOC-SHARDING machinery, completeness exact).

