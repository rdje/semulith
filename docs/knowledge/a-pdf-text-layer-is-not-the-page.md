# A PDF's text layer disagrees with its own page — which do I trust?

**Short answer:** neither, until measured. The text layer a PDF exposes to extraction
tools is a *separate artefact* from the rendered page, produced by the publisher's own
toolchain, and it can be wrong in at least two structurally different ways. Dossier work
that cites reset values or timing figures from extraction output must verify against the
document's own redundancies — and, when a figure looks wrong, against the raw bytes.

## The two measured failure modes (LAN9118 DS00002266B, 2026-10-02)

1. **Extraction modes disagree with each other on tables.** `pdftotext -layout` and
   `pdftotext -raw` rendered the LAN9118's Table 5-1 *Default* column with different
   register↔value pairings (the two-column page layout scrambles row pairing; one mode
   had `FIFO_INT = 87654321h`, the other `BYTE_TEST = 87654321h`). The correct pairing
   came from each register's *own* §5.3.x section — and the whole-register arithmetic
   cross-check confirmed it: `TX_FIFO_INF.TDFREE = 1200h` = 4608 bytes = Table 5-3's TX
   data FIFO size at the TX_FIF_SZ = 5 default. Two independent statements, one number.
   **Rule: never cite a big summary table's column when the per-section text exists;
   and when two independent statements of the same number exist, check they agree.**

2. **The text layer itself mis-maps glyphs.** §3.11.4/§3.11.5.1's reset completion times
   extracted as "2 s" and "100 s" — in *both* pdftotext modes. A hexdump of the raw
   extracted bytes showed plain ASCII `73` (`s`): the mis-mapping (a symbol-font µ
   rendered as `s` in the ToUnicode layer) is the *producer's*, not the extractor's.
   The same datasheet states the identical PHY reset as a clean "minimum of 100us" in
   §5.3.13, and §3.11.4's own application note bounds readiness to 100 ms — so "2 s"/"100
   s" cannot be seconds. **Rule: when a figure is internally contradicted, verify the
   text layer with a hexdump before trusting either reading; pin only the cleanly stated
   figure and record the defect** (`REQ-D-NIC-RESETS`).

## Evidence

- `profiles/lan9118-lab-v0/requirements.sexp` — `REQ-D-NIC-RESETS`'s detail records the
  hexdump measurement and the internal contradiction.
- `docs/tasks/P5-BOARD.md` — the `.10` design brief (the extraction-mode disagreement)
  and the `.10` leaf result (both hazards handled at root).
- The UART dossier's equivalent discipline: `profiles/sifive-uart-lab-v0/` (the 16550
  census — zero occurrences measured against the pinned artifact, `D-BOARD-UART-KIND`).
