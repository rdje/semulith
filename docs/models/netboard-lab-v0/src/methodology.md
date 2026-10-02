# The method: composition as the contract

A board's method is not extraction from one document but **composition of pinned units
against a contract** — and the discipline that keeps a composition honest is that every
choice is data, versioned, with its reason.

**1. Pin versions, not names.** The processor pin is unit id + version `0` + the
GATE-REPORT-gated dossier content digest; each device pin is its datasheet's material id
+ revision + sha256. A name drifts; a digest cannot. The digest half is why the processor
pin survives a documentation edit: the dossier's content is what is pinned, and the gate
report is what vouches for it.

**2. The definition is one S-expression source of truth.** `board.sexp` under
`schema/board.sexp` — the house shape: authored once, schema-gated, narrated by
`DOSSIER.md`, with generated mirrors (this book's tables) gated against drift. Every
element of the roadmap's P5 line — memory, reset, serial console, timers, interrupt
controller — is dispositioned as data, including the two absences, each with its reason
and the obligation it satisfies.

**3. Measure the labels against the sources.** The design brief's "16550-compatible
UART" label survived review and was measured false against the pinned artifact (zero
occurrences of "16550" in FU540-C000 v1p5) before it could ossify into a device dossier;
the board adopted the SiFive UART the manual actually documents, and the correction is
recorded as `D-BOARD-UART-KIND` — a defect corrected with evidence, not edited out of
history.

**4. The composition constraint flows downhill.** The CPU contract's eight environment
assumptions are the board's design inputs, not its afterthoughts: the no-timer/no-IRQ
absences, the cold-only reset, the RAM-only fetch, the access-width policy, and the
recorded-trace network backend each exist *because* an assumption demands it — and the
`satisfies` fields record the wiring so `P5-BOARD.4`'s verdict is a match, not a
re-derivation. The same constraint was found *inside* a device during the NIC's
dossiering (the LAN9118's MMIO-readable counters are guest-readable time sources), and
is recorded as contract data (`REQ-D-NIC-TIME-SOURCES`) rather than discovered at the
verdict.

**5. The verdict is separate from the definition.** This book deliberately carries no
evidence chapter yet: the composition verdict (`.4`) and the firmware probes (`.5`) are
the board's evidence, and the board can never outrank its processor — an EXPERIMENTAL
CPU composes into an EXPERIMENTAL board, and every claim reads as conditional on the
CPU's own acceptance trajectory.
