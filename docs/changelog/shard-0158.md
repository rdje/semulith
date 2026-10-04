# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — the second device dossier: content only, and the PDF text layer lies (P5-BOARD.10)

The LAN9118 dossier (`lan9118-lab-v0`) needed **no machinery edit** — the `.2`
by-declaration generalization was measured sufficient at the design brief, and the
measurement held: every gate derived the device route from the `vehicle` declaration on
first contact. The leaf's substance was the datasheet itself (109 pages; a real MAC+PHY,
not a UART): 52 mirrored records against the UART's 19, three indexing levels (direct
CSRs → MAC_CSR synchronizer → MII PHY bridge), and mirrors **generated** from
requirements.sexp (`target/gen_nic_mirrors.py`) so the 52/52/52 verbatim discipline is
impossible to break by hand — the gate would refuse drift anyway, but not hand-writing
it is the stronger guarantee.

The two extraction hazards, both measured and both now durable: (1) `pdftotext -layout`
and `-raw` **disagree on Table 5-1's Default column** (two-column pages scramble row
pairing) — per-register sections are the authority, and arithmetic cross-checks confirm
(TDFREE `1200h` = Table 5-3's 4608 B at the default split); (2) §3.11's "2 s"/"100 s"
reset times are **the PDF's own text layer mis-mapping µ to ASCII s** (hexdump-verified —
not an extraction drop), internally contradicted by §5.3.13's clean "100us" and §3.11.4's
own 100 ms bound. Only cleanly stated figures were pinned; the defect is recorded in
`REQ-D-NIC-RESETS`.

The composition findings are the leaf's sharpest output: FREE_RUN/GPT_CNT/INT_DEAS are
guest-readable time sources inside a device whose CPU contract excludes all of them
(`REQ-D-NIC-TIME-SOURCES` — frozen/deterministic, never wall-clock, never the retired-
instruction count; `.4` owns the verdict), and the PHY link scene under a recorded-trace
wire (`REQ-D-NIC-PHY-LINK`). The `profiles/` per-part bound bit for the first time
(32→64 KiB; `decision_profiles-family-five-units`).

Lesson: **promoted** — `docs/knowledge/a-pdf-text-layer-is-not-the-page.md` (the two
text-layer failure modes and the verify-with-hexdump rule).

