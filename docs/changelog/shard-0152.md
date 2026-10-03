# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — an answered channel still reads `open` until you flip it (P5-BOARD.9)

The second chipdoc incident, from our side: the acquisition agent answered all ten
P5-BOARD.8 requests (5 fulfilled, 5 measured negatives, chipdoc `542a14b`), and
semulith's `requests.sexp` kept saying `open` — because the seam is hard (chipdoc never
writes here) and only WE flip our own statuses. CHANNEL.md §0.3/§0.5 (re-read on the
director's pointer) closes exactly that gap: `catalog/responses.sexp` re-keys every
answer by OUR ids, and `build_responses.py --report` prints the join (run live before
any edit: 5/5, exit 0). The adoption kept the house rules: digests re-verified at
fetch, never trusted from the feed (`materials.py --verify` 52/0); the corpus re-pinned
with the same census (`c4ad8a2`, 5696/293); the proposals feed's records adopted
verbatim in our syntax. The five blocked answers are recorded as RESULTS — each names
what was tried, what returned, and the consequence (LAN9118 is the wired-NIC primary;
SARA-R4 the cellular primary; the AR9271 probe's negative IS its answer) — and the
channel's exactly-once rule means they are never re-filed without a new route. Two
knowledge cards covered the channel with overlapping, drifting scope; the refreshed
split is: `the-chipdoc-request-channel.md` owns the full ask→answer loop,
`the-chipdoc-channel.md` keeps the measured history and cross-links. `P5-BOARD.1`
inherits five sourced network-device candidates plus five closed alternatives.

Validation: `build_responses.py --report` exit 0; `materials.py --fetch` 5× sha256
verified; `materials.py --verify` 52/0; `make gate` all-doctrines-green.

## _(2026-10-01)_ — the capability report is the capstone, and the registry is its claim list (P3-BREADTH.6 slice 3)

The slice order was measured, not planned: a BREADTH report generated before the unit
registration read "1 registered unit" and listed the DSP56300 family — whose evidence
anchors axis 1 had just measured green — as UNCLAIMED. The claim list IS the unit
registry, so the report had to be the leaf's last slice. With slice 2's registration
landed, the builder's three axes are the roadmap's gate text measured from tracked
files by concrete artifact name: axis 1 counts six anchors for the DSP subset (the
declared scope + vehicle, the `.a56`+`.meta` corpus, the crate's 17 tests, the
differential driver, the recorded comparison contract, the registered smoke-agreement
mechanism) plus the scalar unit's GC record; axis 2 requires each of the nine
exercised-case constructs to be DECLARED in its schema AND CARRIED by `dossier_sexp`
(the silent-drop class `.2` eliminated); axis 3 parses the pinned oracle survey for
its per-family verdicts and lists every family no registered unit backs as
**unclaimed**, explicitly — TI C6000 (ABSENT for execution), ADI SHARC (PARTIAL) —
plus the blanket rule: the registry is complete, everything else is unclaimed by
omission. EVD-08's shape holds by construction: no code path to `passed` while an
axis's anchors are absent.

Placement needed a rule, now written in `check_gate_report.sh`'s header: per-profile
reports live under `profiles/<id>/`; a CROSS-ARCHITECTURE gate's report lives at the
repo level (`docs/BREADTH-REPORT.md`) because no profile directory may own it. The
repo-level leg enforces the same regenerate-never-edit rule with the same three
controls; the self-test covers it (12/12; 4 reports in sync — G0/G1/GC regenerate
byte-identical). One cosmetic bug caught by reading the rendered report: doubled
backticks around the probe list (nested f-string quoting). Verdict: `passed` — and
the report's own "what passed does NOT mean" bounds it: exercised cases only, no
DSP56300 family compatibility, no RISC-V conformance upgrade, the slice-gated `.1`
legs named. The tree closes 8/8.

Validation: `gate_report.py --gate BREADTH` → `passed` (5,789 B); GATE-REPORT
self-test 12/12, 4 reports in sync; `make gate` all-doctrines-green.

