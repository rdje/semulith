# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the PDF re-sourcing probe: measured adopt-in-principle (MODEL-METHOD.14)

The probe answered the cost question by attempting the whole sweep rather than sampling:
the naive in-order parser over pdftotext's layout-fragmented output (one field per line)
recovered every opcode (the per-page mnemonic row zips with the page's 7-bit opcode row)
and both funct streams for 37/52 forms; the 15 misses are all parser-side ordering gaps
(f7/f3 streams need page-local alignment), none a value conflict and none a document
absence — and every gap was caught by the incumbent comparison, demonstrating the control
a completed re-source would rely on. The numbering trap (PDF ch.2/ch.4 vs pinned HTML
§1.1/§3.1) was handled by keying on content. Decision: adopt-in-principle; the re-source
is a later reviewed leaf under .8's ownership. Housekeeping: the closure sweep found .15
and .17 still marked `active` with Results landed — tree-internal drift, corrected.

Lesson: `promotion: declined` (recorded in the leaf; the probe numbers live there and in
the decision record).

## _(2026-09-30)_ — min-fencei: the one-word retained divergence (P2-SCALAR.6)

Implementation matched the design exactly — the expected-divergence protocol
(at_step 0, vacuous prefix), the adapters' run-off-the-end handling, and the stop-reason
tables all predated this leaf, so no instrument needed to change: the guest, its
expectation document, one test suite, the census arm, the matrix cell. The live run shows
the protocol working at the boundary: EXPECTED DIVERGENCE at aligned step 0 vs each
reference; sail vs spike AGREE over their full 2 steps (fence.i nop + the illegal zero
word). The one tight spot: references.sexp sat 49 B under its per-part ceiling, so the
retention note is written to fit (32,765/32,768) rather than moving the ceiling for a
sentence. Validation: 175/175 verify suites; smoke green incl. the four-step protocol;
bench 53 arms; gate green.

Lesson: `promotion: declined` (recorded in the leaf).

