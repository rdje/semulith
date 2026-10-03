# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — the second unit's contract records, and the fixture that noticed (P3-BREADTH.6 slice 1)

The DSP profile's `requirements.sexp`/`contract-obligations.sexp` landed as governed
documents, closing the DOSSIER's records row. The shape is RECORD-SCHEMA's rules applied,
not invented: COVERAGE forced each requirement's statement to be its decision's
byte-identical text (seven decisions → seven `REQ-D-*`), MIRROR forced each mirror
obligation to restate it verbatim, AUTHORITY forced `defined` ⇒ `architecture` (the three
laboratory decisions take `laboratory`), and OBLIGED forced the ±POS/NEG pair per
obligation — 26 declared checks over contract `dsp56300-lab-env-v0`. The six `OB-ENV-*`
records carry the laboratory's half of the contract: no guest-reachable time source (`cyc`
is informational and never compared), sequential scalar issue (the F5 pending-writes
window measured ABSENT by the F6 census), cold reset to D-RESET-STATE's values, one 24-bit
P-space word per fetch, no asynchronous events (interrupts are a named subset exclusion),
and instruction-level atomicity. RECORD-SCHEMA attached with zero gate edits — the
catalogue auto-discovery found the new files and every cross-rule passed on the first run
(10 record files).

The interesting failure was FACT-OWNERSHIP's self-test, which did exactly what it exists
to do: its GREEN fixture's pair spec globs the REAL corpus
(`profiles/*/contract-obligations.sexp` × same-unit `requirements.sexp`), so landing the
DSP catalogues turned the fixture RED — `UNREGISTERED MIRROR PAIR`, the fixture registry
named only rv64i's pair. The re-pin names both units (`__CHECKED__ 5 → 6`) with the reason
in the check's comment — the same designed staleness the synth probes carry: a fixture
calibrated to a corpus the work just outgrew. Validation: both catalogues schema-validate
ok; RECORD-SCHEMA ok (10 files); FACT-OWNERSHIP ok (25 kinds), self-test 10/10;
`make gate` all-doctrines-green. The rv64i catalogues are byte-untouched.

## _(2026-10-01)_ — ask through the channel, and write down how asking works (P5-BOARD.8)

The director offered CHIPDOC's web-scorching for the network-connected board's component
documentation. The useful engineering content was the survey BEFORE the ask: the
snapshotted feed already holds a complete register-level Ethernet contract (TI-DP83816),
the ESP32 register maps, both SiFive SoC manuals, and the AM335x TRM — so the ten
requests only cover what is genuinely missing, each with a QEMU-oracle note or an
explicit probe flag (the AR9271 request expects a measured negative, which is itself the
answer to "is any WiFi baseband documented"). The process defect found and fixed: the
filing mechanics (requests.sexp preferred, gaps the false-positive-prone fallback,
exactly-once ids, the watcher firing on file change) lived only in the corpus-side
CHANNEL.md — a session had to re-derive them, and the director noticed. The fix is a
knowledge card, not a complaint: the next session reads
`docs/knowledge/the-chipdoc-request-channel.md` and files in one step. Verification
worth naming: chipdoc's poller was RUN (read-only, its own documented interface) and saw
exactly the ten new ids — the channel measured live, not assumed.

## _(2026-10-01)_ — the landing is the boring part when the measurement came first (P3-BREADTH.7 slice 3)

After slices 1–2 measured every attaching gate against the drafts, the landing itself was
a rename plus the ownership rows: `git mv` semantics for the three documents, five rows
in `fact_ownership.tsv`, and two census arms that only exist post-landing (they measure
the real two-unit corpus: a GREEN pair-registered arm and a RED unregistered-pair arm —
a gate whose arms depend on the corpus they judge is only writable after the corpus
lands, which is why they were scheduled, not forgotten, in slice 2). The one judgment
worth recording: the DSP's `guests/` registered as a fact owner with NO mirror — the
rv64 guest kind has a generated mirror (`guests.rs`, GUEST-GEN), and the DSP's honestly
has none yet; the registry's "mirror `-`" spelling is the honest zero, not a gap. The
DOSSIER's deferral rows now name `.6` for requirements and unit registration — the
earlier "lands with the model slice" wording was stale the day the model slice closed
without them, and two slices carried the correction.

