# The method: from datasheet to device contract

The route is the dossier machinery's device route, inherited from the UART's
hardening (`P5-BOARD.2`) with **no machinery edit** — the by-declaration generalization
covered the NIC on first contact, measured at the `.10` design brief and held in
execution. What the NIC added was scale and two extraction hazards worth a reader's
attention.

**1. Pin the source, name the issue.** `sources.sexp` pins DS00002266B by sha256 through
the materials corpus and names the issue (the B revision, not the 2005 SMSC A issue).

**2. Read the document with its hazards measured.** Two were found and handled at root
(the retrievable lesson: `docs/knowledge/a-pdf-text-layer-is-not-the-page.md`).
`pdftotext`'s two modes *disagree* on Table 5-1's Default column — two-column pages
scramble row pairing — so every reset value in the dossier comes from each register's
own §5.3.x/§5.4.x/§5.5.x section, cross-checked arithmetically where an independent
statement exists (TX_FIFO_INF.TDFREE = `1200h` = 4608 B = Table 5-3's row at the
TX_FIF_SZ = 5 default: two statements, one number). And §3.11's "2 s"/"100 s" reset
times are the PDF's *own text layer* mis-mapping the micro sign — hexdump-verified,
internally contradicted — so the dossier pins only the cleanly stated 22 ms POR and
100 µs PHY-hold figures (`REQ-D-NIC-RESETS`).

**3. Record the contract as requirements — including the silences and the deferrals.**
52 records: 46 defined statements, the reserved/unspecified silences, and the
implementation-defined deferrals (the straps, the time sources, the link scene, the pin
tie-offs) whose owners are named, not guessed.

**4. Mirror mechanically.** The 52 obligations and 52 decisions were **generated** from
requirements.sexp — the verbatim mirror discipline (one fact, three surfaces, one
wording) is impossible to break by hand, and RECORD-SCHEMA would refuse the drift
regardless. A contract this size is exactly where hand-copying fails.

**5. Earn the state census.** The hidden-state census measured what the model must carry
beyond the 49 registers: the four FIFOs' contents and occupancies, the TX command-parser
state (the TXE length check and §3.12.5's accounting observe it), and the 16-bit pairing
latch (the board declares 16-bit accesses, and §3.6's pairing rule makes the pending
half observable) — and nothing else. The MIL FIFOs are excluded by the datasheet's own
"not visible to the host processor"; the wire-domain machines are excluded because the
replay backend owns their scene.

**6. Derive expectations before any model exists.** Three documents: cold-reset reads
(the stated resets, the EPC-Busy transient, the strap bit and blank nibbles deliberately
unpinned), the exact TDFREE accounting (§3.12.5's rules give closed arithmetic — 4608 →
4540 → 4528 → 4416 → dump → 4608), and the RX replay path (the status-word format for a
declared broadcast frame, the pop/PEEK semantics, and the underrun → RXE discipline).
