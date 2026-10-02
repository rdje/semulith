# The materials bill

Everything `lan9118-lab-v0` is built from, in one place: the one pinned datasheet, and
the internal contracts the dossier itself carries — each pinned by exact identity, each
with what it supplies **and what it does not**.

Two rules govern this chapter, and they are why it can be trusted:

- **The tables are generated.** `scripts/gen_model_book.py` reads the pinned dossier and
  emits the identity tables below — digests, byte counts, record counts. Nothing in a
  table is retyped, so a digest cannot rot: the `MATERIALS-BILL` doctrine regenerates the
  tables in memory on every commit and fails if they differ from what is committed.
- **The prose is authored, and it is where the judgement lives.** Every material below
  carries its negative statement, because a bill that lists only what things provide is
  how a project comes to believe it has information it never acquired.

## The pinned specification artifact

{{#include materials/pinned-specifications.md}}

### `MICROCHIP-LAN9118`

The LAN9118 datasheet, DS00002266B (2018-11-30): the host bus interface (§1.10, §3.6 —
programmed I/O only, 32/16-bit), the direct register map (Figure 5-1, Table 5-1), the
FIFO port semantics (§5.2), every system CSR (§5.3), the indexed MAC CSRs (§5.4), the PHY
registers (§5.5), the TX/RX data paths with their command and status formats
(§3.12/§3.13), the five reset sources (§3.11), the EEPROM interface and MAC-address
auto-load (§3.9). Acquired through the chipdoc channel (`P5-BOARD.8`/`.9`) and
re-verified from the materials cache; the artifact is read, not redistributed.

**Does not supply:** the configuration straps' values (D32/nD16, SPEED_SEL — the board's
composition choice, `REQ-D-NIC-STRAP-RESETS`); the PHY ID2 model/revision nibbles (blank
in the document, `REQ-D-NIC-PHY-ID`); reserved-location read values (§5.1's "random
value"); any access width other than 32/16-bit (`REQ-D-NIC-WIDTH`); a clean unit for
§3.11's soft-reset completion time (the PDF's own text layer mis-renders it — the µ
mis-mapping is hexdump-verified, and only the cleanly stated figures are pinned,
`REQ-D-NIC-RESETS`); and ADDRL/ADDRH's reset value, caught between Table 5-6's listed
defaults and §5.4.2's "undefined until loaded" (`REQ-D-NIC-MAC-ADDR` — with no EEPROM on
this board, the host programs the address).

## The encoding and reference surfaces, honestly absent

A device has no instruction encodings and pins no reference models — the two fragments
below say so by declaration, because an honest absence in the bill is what keeps the
device dossier from quietly masquerading as a processor-shaped one.

{{#include materials/encoding-tables.md}}

{{#include materials/reference-models.md}}

## The internal contracts

The dossier's own documents, with their record counts derived from the tracked files.

{{#include materials/internal-contracts.md}}

### `profile.sexp`

The unit's declaration: the 28-member scope census (the whole direct host-bus surface —
4 FIFO port groups + 24 named CSRs, the RESERVED slots deliberately excluded as
absences), the 52 decision mirrors, the `device-model` vehicle declaration.

**Does not supply:** the indexed spaces as scope members — the 12 MAC CSRs and 13 PHY
registers are MMIO-reachable state carried in `state.sexp`, reached through the
synchronizer and MII indirections, not direct map members; and any instruction pipeline.

### `state.sexp`

The device-state document: 49 registers across three indexing levels plus the four FIFO
families, with the hidden-state census that earns the "and nothing else" claim — the TX
command-parser state and the 16-bit pairing latch are present (the TXE length check and
§3.6's pairing rule make them MMIO-observable); the MIL FIFOs are absent by the
datasheet's own words ("not visible to the host processor").

**Does not supply:** the wire domain — PHY link training and auto-negotiation surface
only as register bits whose scene the replay backend declares (`REQ-D-NIC-PHY-LINK`);
and the time-source registers carry the composition's frozen disposition
(`REQ-D-NIC-TIME-SOURCES`), never wall-clock.

### `requirements.sexp`

The 52 predeclared requirement records: 46 datasheet-defined statements plus the
reserved/unspecified/implementation-defined silences and deferrals, each with its
datasheet locator.

**Does not supply:** latitude — the strap-determined resets name `.4`'s composition
verdict as their owner rather than guessing a strap, and the unspecified width/Reserved
records promise what the model must NOT invent.

### `contract-obligations.sexp`

The device contract `lan9118-v0` v0: 52 obligations in the `device-guarantee` direction —
what a composing board may rely on, and (for the silences) what it may not. The three
composition dispositions (`OB-NIC-TIME-SOURCES`, `OB-NIC-PHY-LINK`, `OB-NIC-GPIO-PINS`)
carry `laboratory` authority — the one place the contract speaks for the board's
deterministic discipline rather than the datasheet.

**Does not supply:** a discharge by itself — the board definition's `satisfies` fields
and P5-BOARD.4's composition verdict consume these ids.

### `expectations/`

The EVD-05 register-read corpus: three documents (cold-reset reads; the exact TX
free-space accounting with TX_ON = 0 — §3.12.5's rules make TDFREE arithmetic pinable
without a wire; the recorded-trace RX path with pop/PEEK and the underrun → RXE →
soft-reset discipline), derived from the datasheet **before any model exists**.

**Does not supply:** probe results — nothing here ran against an implementation; and
where the datasheet defers (the strap bit, the blank ID2 nibbles, the undefined MAC
address), the documents deliberately pin nothing.
