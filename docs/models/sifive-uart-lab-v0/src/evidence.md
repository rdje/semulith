# The evidence shape: expectations before a model

A device's evidence cannot be a per-step instruction trace — there are no instructions.
This unit's evidence shape is the one its `vehicle` block declares: `(comparison
register-expectations)`.

**What exists today** is the corpus of datasheet-derived register-read expectations under
`profiles/sifive-uart-lab-v0/expectations/`: three documents, each step carrying its
derivation and its §13 locator, recorded before any implementation exists. They are
predictions an implementation must reproduce — the cold-reset register values, the TX
FIFO's full flag at the 8-entry boundary and its ignore-while-full rule, the RX
dequeue order and the empty flag — and, just as load-bearing, the places they refuse to
predict: the X-marked resets and the watermark `==` boundary carry the empty
`(writes)` marker with the reason, because an expectation that pins what the datasheet
leaves undetermined is a fabricated fact.

**What consumes them** comes later, with named owners: the device model (the dossier's
model route) is checked against these expectations; the firmware probes (`P5-BOARD.5`,
gated on the CPU's acceptance trajectory) exercise the real accesses — the interaction
matrix attaches with the probe corpus, by the same declaration that derived its
absence here.

**What this unit's evidence never is:** a reference implementation's output adopted as
truth. QEMU's sifive_uart exists and reads §13.8 combinationally — an independent
*reading*, cited in the dossier as exactly that, and never a source. A reference that
shares an ancestor with the claim is not a second opinion
(`docs/EVIDENCE_AND_GATES.md`).
