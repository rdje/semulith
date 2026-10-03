# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — a board specification is data with its absences declared, and a label is not a source (P5-BOARD.1)

`netboard-lab-v0` is the first board and `schema/board.sexp` the first non-processor
source-of-truth schema. Two design decisions are worth the ink:

**An absence the contract depends on is data, not prose.** `rv64i-lab-env-v0` v0 admits no
guest-reachable time source and no asynchronous event — and both absences must be *platform*
properties to be real (the CPU contract's own lesson: excluding CSR instructions does not
exclude reading `mtime` over MMIO). So the schema gives `timers` and `interrupt-controller`
explicit `(present false)` forms carrying the reason and the obligation ids they satisfy;
an undocumented absence would read as an oversight, and an oversight is how a CLINT slips
in as a "feature" and becomes a `.4` composition rejection. The `satisfies` fields
pre-wire `scripts/discharge_assumptions.py`'s verdict without computing it — declaration
here, computation there.

**Verify the label against the artifact before you inherit it.** The design brief named the
serial device "16550-compatible (source SIFIVE-FU540-C000 v1p5)". A `pdftotext` census of
the pinned PDF: zero occurrences of "16550"; §13 is the SiFive UART (txdata/rxdata/txctrl/
rxctrl/ie/ip/div, 8-entry FIFOs, 32-bit-aligned only). The pin was the intent, the label
was wrong — so the board adopts the SiFive UART and the label is corrected at every record
(`materials/catalog.sexp`, `D-BOARD-UART-KIND`; the tree keeps the brief's original lines
with a dated correction, per the house pattern). Consequence that mattered: the UART's
sourced instance address (`0x1001_0000`, Table 58) collided with the pre-verification
sketch's NIC address — measuring first caught that too. Memory map: RAM 2 GiB at
`0x8000_0000` (the harness's existing DEFAULT_BASE/SIZE, so laboratory guests run
unchanged), UART at the FU540 instance address, the LAN9118 in a 256-byte window at
`0x1002_0000` (Table 5-1's direct-register span, offsets 0x00–0xFC).

Scope routing: registration of the board unit (`materials/units.sexp`, the `kind` edit,
the per-unit book) is deferred to `.3` — the registry admits a new kind "the day a real
unit needs one", and registration day carries UNIT-BOOKS / MATERIALS-BILL /
book-generator / BREADTH-prose consequences (all censused before deciding) that belong to
the materialization leaf, not to a specification. The third `profiles/` directory
re-derived the family bound to 3× by the standing arithmetic; nothing fired (142 < 240).

## _(2026-10-02)_ — the book's index is a function of the book, not a page someone keeps (BOOK-APPARATUS.1)

The director's apparatus directive audited against the real book: the glossary cannot fork
(`docs/book/src/glossary.md` splices the canonical `docs/GLOSSARY.md` at build time), the two
annexes already match the directive's definition — and the **index was absent**. It now exists
the only way this repository tolerates a fact about a changing population: derived.
`scripts/gen_book_index.py` reads `SUMMARY.md` (the chapter set, in reading order), the
canonical glossary plus the book's acronym table (the term set), and every chapter's text (the
occurrence set, case-insensitive and word-bounded); `scripts/check_book_index.sh` — the 31st
project doctrine, `BOOK-INDEX` — regenerates in memory and refuses drift, with six self-test
arms fired RED before registration (hand-edit DRIFT, stale-behind-edited-chapters DRIFT,
missing chapter and missing SUMMARY refused **by name**). The generator refuses what it cannot
emit rather than guessing, per house style. One build-exposed defect fixed at root: the
generator's printed term count was a fudge factor (`47` against the real `40`) — now derived
from the emitted rows. The annex policy is stated where a reader meets it
(`docs/book/src/introduction.md`): chapters stay readable top to bottom; what is too technical
for the main line lives in an annex. The directive's second half (incremental buildup, both
audiences engaged) became `decision_mdbook-incremental-engaging` + `BOOK-APPARATUS.2`; the TOC
request was withdrawn by the director — the mdBook sidebar is the TOC, and the contents page
built to satisfy it was reverted as redundant.

Validation: `gen_book_index.py` → 15,019 B / 40 terms; `mdbook build docs/book` rc 0;
`check_book_index.sh --self-test` 6/6; `check_doctrines.sh` all green.

