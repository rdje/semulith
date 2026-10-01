# A design brief names a device — can I trust the label, or must I measure it?

**Measure it against the pinned artifact before it reaches a source of truth. A label
inherited from a brief, a catalog, or an earlier session is a *claim*, and this project's
own claim-verification policy applies to design inputs exactly as it applies to results:
re-derive, falsify, then record. The pin (material id, revision, sha256) is what a brief
is really asserting; the natural-language label riding beside it is unverified prose until
someone checks it — and the check is cheap: `pdftotext` the pinned PDF and grep.**

Recorded `2026-10-02` at `P5-BOARD.1`. The design brief named the first board's serial
device "16550-compatible UART (source `SIFIVE-FU540-C000` v1p5)" — a label that had
already survived a catalog's `supplies` text and a task-tree decision. A `pdftotext`
census of the pinned artifact: **zero occurrences of "16550"**; the manual's §13 is the
SiFive UART (txdata/rxdata/txctrl/rxctrl/ie/ip/div, 8-entry FIFOs, 32-bit-aligned only) —
a different register model, different access widths, different driver contract. Had the
label reached the device dossier, the dossier would have been written against a device
the source never describes, and every downstream claim would have inherited the error.
The pin was the intent; the label was wrong.

The shape of the fix, reusable:

1. **Re-derive the label from the artifact, not from the last document that repeated
   it.** A claim repeated in two of your own files is one claim twice, not two opinions —
   the catalog and the brief shared an ancestor.
2. **Falsify with the strongest cheap instrument.** "Zero hits" is only meaningful when
   the instrument can see the thing — `pdftotext` renders the pinned PDF's selectable
   text, so a zero-hit census over it is a measured negative, not blindness (see
   [`zero-hits-absence-or-blindness.md`](zero-hits-absence-or-blindness.md)).
3. **Correct at every record, and keep the correction dated.** The brief's original lines
   stay as history; the catalog text is fixed; the board definition carries the
   correction as a decision record (`D-BOARD-UART-KIND`). Editing the past out of the
   record would hide how the defect nearly propagated.

Bonus measurement the same habit caught: the pre-verification sketch had placed the NIC
at the address the *actual* UART source assigns to UART0 (`0x1001_0000`, Table 58) —
measuring first turned a silent memory-map collision into a non-event.
