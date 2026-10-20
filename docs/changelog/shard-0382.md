# DEV_NOTES shard — _(2026-10-19)_ … _(2026-10-19)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-19)_ — carry one allowance through evaluation (P4-SYSTEM.14 a42ab)

The three-run collector exposes a conservative charge, but the evaluator's
manifest seed and later ledger used independent fixed defaults. Add optional
inclusive plain-int max_read_bytes before record/schema or manifest binding I/O.
Evaluation accepts0..128MiB, delegates min(remaining,64KiB) to the manifest, then
passes the same aggregate allowance to the file ledger. Its existing seed charge
counts once. Defaults,16MiB snapshots, per-role limits, findings and frozen public
result fields stay exact. Invalid limits refuse with an unchecked record.

A caller reserves its delegated allowance before evaluation. Detailed ledger
charges cover failed-read reservations; before that ledger is available, retain
the full reservation. A schema-valid oversized trace declaration reproduces433B
of actual manifest reads with a zero authentication charge: file-set preflight
refuses before its ledger starts. Validate seed-inclusive accounting before any
refund, even when an authentication summary exists. Preserve this legacy result;
add a control and own the validation as P1 for the next combined driver. No new
early-failure counter or combined driver is claimed.
The tracked probe counts actual os.read payloads over23 real fixture files,
including the real DIV excerpt/guest/expectations and synthetic observations.
It checks exact/short/zero and invalid limits, clamping/document ceilings, stale/
missing children, unchanged defaults and modeled collection-charge subtraction.
Initial mutation harness sentinels escaped as errors; catch type escapes and use
caught I/O/binding sentinels with numeric no-call checks. All ten omissions now
fail cleanly. Legacy manifest/evaluator mutation seams follow the new call syntax.

The source-reviewed capture remains35modules/27data/63children/66files; changed
producer pins total947184B and work from a copy with no materials cache. Preserve
three complete closed task records/3428B with source/owner inverses, old history
and fixed caps. Add a bounded book chapter and executable examples without losing
existing examples. Canonical driver/reference identity/output retention, exact
predeclared manifest and full policy remain pending; no capture/qualification.
Promotion declined: existing budget/source/locality contracts apply. Runtime
controller blocked-state observation is separately owned P2 in the task; cause
unestablished, repository implementation continues.

Validation:130 normal/O control runs;15 allowance controls/ten omissions and
33/42/22 legacy matrices retain exact findings.16 focused checks/seven books/ten
complete examples pass. 1535 other files/1Gitlink/93 old entries exact;
three whole task records3428B, source/owner inverse2/seven damaged refusals.
Whole-oldest DEV3993B to0356 and CH2211B to0357; fixed caps and CPU/BOARD/replay
statuses preserved. LIVE's static arm count is freshly derived1608.

