# The method: from datasheet to device contract

The route from the pinned document to this unit is the dossier machinery's device route,
exercised here for the first time (`P5-BOARD.2`) — deliberately on the simplest contract
on the board, so the machinery was proven before the LAN9118 inherited it.

**1. Pin the source, name the issue.** `sources.sexp` pins the artifact by sha256 through
the materials corpus, names the issue (v1p5, not the circulating v1p0/v1p3/v1p4), and
records what the document does *not* supply. Every fact in the dossier was read against
the digest-verified cache, and one label the design brief carried ("16550-compatible")
was measured false against the artifact — a `pdftotext` census found zero occurrences —
and corrected at its records before it could ossify.

**2. Record the contract as requirements — including the silences.** Nineteen records:
each defined behaviour stated with its §13 locator, and each measured silence recorded
as a requirement of *non-commitment*. The watermark gap is the model case: the dossier
first drafted "level conditions", measured the two strict sentences, and corrected
itself — the expectations pin a watermark bit only when its raised condition holds under
every reading of §13.8.

**3. Mirror, don't paraphrase.** Every decision in `profile.sexp` and every obligation in
`contract-obligations.sexp` restates its requirement *verbatim* — one fact, three
surfaces, one wording — and RECORD-SCHEMA refuses drift mechanically (statement equality,
the mechanical `D-X` ↔ `REQ-D-X` mapping, authority rules: a datasheet-defined fact may
not be claimed at laboratory authority).

**4. Earn the state census.** `state.sexp`'s hidden-state census asks SEM-08's question
of the device: what state beyond the seven registers must a model carry to reproduce
every MMIO-visible behaviour? The measured answer — the FIFOs' contents and occupancies,
and nothing else — is *earned*: the baud counter phase, shift registers, sampler and pin
latch are each enumerated and shown unreachable from MMIO, so "nothing else" is a
measured claim, not a hope.

**5. Derive expectations before any model exists.** The three documents under
`expectations/` are datasheet-derived register-read predictions (EVD-05's shape at the
device layer): cold-reset reads of the four stated resets, the TX FIFO's full-flag
behaviour across the 8-entry boundary, and the RX watermark/dequeue sequence — with the
X-marked values and the watermark boundary deliberately unpinned, reasons recorded.

The applicability machinery deserves its own sentence: the gates that attach by glob the
day the documents land (DOSSIER-SCHEMA, RECORD-SCHEMA, PROFILE-CONSISTENCY, EXTRACTION's
device leg, EXERCISE-COVERAGE, INTERACTION-MATRIX) derive what applies from the unit's
`vehicle` declaration — and a document contradicting the declaration (an encoding space,
a guest corpus) is a finding, not a pass. The device is not a lower tier
(`docs/EVIDENCE_AND_GATES.md` §8); it is a different shape, decided by declaration.
