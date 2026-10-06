# CITATION-ACCURACY: a quoted citation names the section that holds the quote

## Metadata

- Tree ID: `CITATION-ACCURACY`
- Status: `active`
- Roadmap lane: cross-cutting evidence discipline (`ROADMAP.md` — the evidence/traceability
  contract, `docs/EVIDENCE_AND_GATES.md`; `RULES.md` SRC-*: a claim cites the exact source)
- Gate: the project doctrine this tree registers (`CITATION-QUOTES`)
- Created: `2026-10-06`
- Owner: repo-local workflow

## Goal

Make citation ACCURACY mechanical where it is decidable: whenever a tracked source-of-truth
document attributes a QUOTED phrase to a pinned section (`'…' (RVI-F §20.1.2 …)`, a
`(source "RVI-A §12.1.2 — '…'")`, an expectation step's derivation under its step source),
the phrase must occur — in order, ellipses honoured — inside that section of the pinned
artifact. A locator that resolves but names the wrong section is refused, and the refusal
names the section where the phrase actually is.

## Non-Goals

- **Not locator existence** — `scripts/check_citations.py` (SEMANTICS) owns that, for the
  semantics files; this tree does not re-own it.
- **Not paraphrase accuracy.** An unquoted claim ("the reservation is cleared — §12.1.2")
  cannot be decided by string matching; it stays a reviewer's question. Only quotes are
  judged, and only quotes with a decidable attribution.
- **Not Markdown prose in v1.** `.md` documents (dossiers, the book, decision records) quote
  the specification too; their attribution grammar is freer and is a later leaf's question
  (Open Questions), not smuggled into this one.
- **Not the PDF pins.** A source pinned as a declared non-snapshot artifact (`http_status 0` —
  the FU540 manual, the psABI) has no HTML section structure here; quotes attributed to
  one are counted UNCHECKABLE by name, never passed.

## Acceptance Criteria

1. A tracked tool decides, for every tracked `.sexp`, which quoted phrases carry a decidable
   attribution and whether each occurs in its cited section; misses are refused naming the
   file, the phrase, the cited section, and where the phrase does occur.
2. The tool's controls fire RED for the right reasons (`--self-test`), and the doctrine is
   observed RED against the REAL pre-fix corpus — the two locator defects `P4-SYSTEM.7` slice
   (c3) part 1 fixed (`SEMULITH-P4-0043`) — before it is registered.
3. Registered as a project doctrine with the materials-cache named skip (the SEMANTICS
   CITATIONS arm's precedent: a check that cannot judge never reports green), mirrored in
   the doctrine documents and the book.

## Task Tree

- ID: `CITATION-ACCURACY`
  Status: `active`
  Goal: quoted citations are checked against the section they cite
  Children: `CITATION-ACCURACY.1`, `CITATION-ACCURACY.2`

- ID: `CITATION-ACCURACY.1` — **the quoted-phrase-in-section gate**
  Status: `done` (`2026-10-06`, `SEMULITH-CA-0001`)
  Goal: `scripts/check_citation_quotes.py` + its doctrine wrapper `CITATION-QUOTES`, over every
  tracked `.sexp`, with the four attribution rules below; RED on the real pre-fix corpus;
  registered.
  Acceptance: criteria 1–3 above.
  Result: **met.** The tool judges every tracked `.sexp` string atom: 24 attributed quotes
  (R1 1, R2 12, R3 5, R4 6), 0 findings at HEAD, 89 unattributed counted, the PDF pins
  (DS00002266B ×2) and one non-source locator (LIMITATIONS ×1) counted UNCHECKABLE by name.
  Against the REAL pre-fix files (the tree at `113df99`): 6 MISS findings, every one naming
  "found in §20.1.2" — the two defects `SEMULITH-P4-0043` fixed, plus the guest derivations
  that quoted the fcsr paragraph under the same wrong locator. The wrapper's 14 controls pass
  and a mutation (the matcher forced to always-match) turns 6 RED arms red. Registered as the
  35th project doctrine with the materials-cache NAMED SKIP.
  Verification: `2026-10-06` — the Verification Log below.
  Commit: `SEMULITH-CA-0001`
  `promotion: declined (the lesson is mechanized — the CITATION-QUOTES row in DOCTRINE_ENFORCEMENT.md states it and the gate enforces it).`

- ID: `CITATION-ACCURACY.2` — **the Markdown census**
  Status: `proposed`
  Goal: measure the attribution grammar of the tracked Markdown documents that quote the
  pinned specification (dossiers, decision records, the book) — and extend the corpus only
  to a shape the census proves decidable.
  Acceptance: a census of quoted phrases under `ID §N` locators in tracked `.md`, each
  shape dispositioned (decidable → judged; undecidable → counted with its reason); any
  extension RED-proven before it judges.
  Verification: pending
  Commit: pending

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `CITATION-ACCURACY.2` | `proposed` | the corpus's remaining quoting surface (Markdown); `.1` landed the gate over every tracked `.sexp` |

## Decisions

- `2026-10-06` (the design, recorded before code; sources: the scratch census
  `target/citation-accuracy/proto.py` over every tracked `.sexp` string atom; the two defects
  of `SEMULITH-P4-0043`; `scripts/check_citations.py` read in full):
  **The measured population.** 108 single-quoted phrases (≥ 6 chars) sit in tracked `.sexp`
  strings; 24 carry a decidable attribution under the rules below and all 24 occur in their
  cited sections at HEAD (after the c3-part-1 fix); 3 sit in strings naming two or more
  locators with no adjacency (the U54-manual quote — a PDF pin, uncheckable anyway); 81 carry
  no locator at all (laboratory terms, quotes of other tools). Two normalization facts were
  measured, not assumed: the pinned HTML renders code literals in quotes (`('pc'+4)`) and
  inserts zero-width spaces (`7—​5`), so matching is case-, whitespace- and
  quote-character-insensitive, with typographic dashes folded.
  **The attribution rules** (a phrase is judged only when one fires; otherwise it is counted,
  never judged): R1 — a quote immediately followed by a parenthesized locator
  (`'…' (RVI-F §20.1.2`); R2 — a quote inside a `(source "ID §N …")` string; R3 — a quote in an
  expectation step's `(derivation …)`, under that step's `(source …)`; R4 — a quote in a string
  that names exactly ONE distinct locator. An ellipsis (`…`/`...`) or an editorial bracket
  (`[it]`) splits a phrase into pieces that must occur IN ORDER.
  **The section**: a numbered heading's text through the next heading that is neither it nor
  its descendant (a §12.1 citation includes §12.1.2's text). **A miss names the cure**: the
  refusal searches the cited artifact's other sections and prints where the phrase does occur.
  **The gate placement**: a project doctrine with the SEMANTICS precedent's cache route — the
  pinned pages are an untracked, network-acquired cache, so a clone without them prints a NAMED
  SKIP; the self-test judges synthetic pages and always runs.

## Open Questions

- Do Markdown documents join the corpus (the dossiers and decision records quote the
  specification under `RVI-* §N` locators)? Owned by `.2` (proposed): the grammar is measured
  first, and only a decidable shape is judged.

## Blockers

- None.

## Acceptance Checklist (required for any leaf that lands a CODE change)

`CITATION-ACCURACY.1` — the quoted-phrase-in-section gate (`2026-10-06`, `SEMULITH-CA-0001`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the gap, measured: `grep -n "glob" scripts/check_citations.py`
  → line 180 globs `definitions/**/*.sem.sexp` only, and its check is `num not in have[sid]` —
  EXISTENCE of the section. State documents, guest derivations and statements are read by no
  citation gate, and no gate reads a quote. The census (`target/citation-accuracy/proto.py`):
  108 quoted phrases in tracked `.sexp` strings, 24 with a decidable attribution.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_citation_quotes.py (the real pre-fix files, the tree at 113df99):
    MISS …fp-fcsr-view.expected.sexp [R3]: 'implementations shall ignore writes to these
    bits' is not in RVI-F §20.1.1 — found in §20.1.2   (… 6 findings, every one → §20.1.2)
    CITATION-QUOTES: 7 attributed quote(s) judged … 6 finding(s)   rc= 1
  $ bash scripts/check_citation_quotes.sh (HEAD) → CITATION-QUOTES: 24 attributed quote(s)
    judged (R1 1, R2 12, R3 5, R4 6); 0 finding(s); 89 unattributed; uncheckable (no HTML
    pin): DS00002266B ×2, LIMITATIONS ×1   rc=0
  $ bash scripts/check_citation_quotes.sh --self-test → CITATION-QUOTES --self-test: 14 pass / 0 fail
  mutation (occurs() forced True) → 8 pass / 6 fail — the six RED arms go red; restored 14/0
  ```

- [x] **NO REGRESSION** — `bash scripts/check_registry_mirror.sh` → REGISTRY-MIRROR: ok;
  DERIVED-COUNTS re-derived (doctrines 34 → 35, arms 431 → 445); `make gate` → `=== all
  doctrines green ===`. No Rust touched.

- [x] **FIX** — `scripts/check_citation_quotes.py` (the judge: R1–R4, in-order pieces, the
  measured normalizations, the cure-naming miss); `scripts/check_citation_quotes.sh` (the
  doctrine: 14 controls on synthetic pages, the cache named skip); registered in
  `scripts/check_doctrines.project.sh`.

- [x] **LOCKSTEP** — `DOCTRINE_ENFORCEMENT.md` + the book's `working/doctrines.md` rows (the
  registry mirror), `TOOLBOX.md` row, `LIVE_STATUS.md` (35 / 445), `docs/TASK_TREE.md` row,
  `MEMORY.md` (active trees), `CHANGELOG.md`, `DEV_NOTES.md` (+ its shard).

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-06` | `.1` | the gap measured (check_citations' scope: sem files, existence); the census (108 quotes, 24 attributable); the tool against the real pre-fix files (6 MISS → §20.1.2) and HEAD (24 judged, 0 findings); 14 controls + the mutation (6 RED arms red); registration mirrors | **met** — CITATION-QUOTES registered (35th doctrine); quotes now checked against the section they cite |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.1` | `SEMULITH-CA-0001 (leaf CITATION-ACCURACY.1): the quoted-phrase-in-section gate — CITATION-QUOTES registered, RED on the real pre-fix corpus (6 misses, each naming §20.1.2)` | the tool + wrapper + registration; `.2` proposed for Markdown |

## Changelog

- `2026-10-06`: `.1` done (`SEMULITH-CA-0001`) — CITATION-QUOTES registered: 24 attributed quotes
  judged across every tracked `.sexp`, RED-proven on the real pre-fix corpus; `.2` (the
  Markdown census) proposed.
- `2026-10-06`: Created, owning the gap `P4-SYSTEM.7` slice (c3) part 1 measured
  (`SEMULITH-P4-0043`): two locator defects resolved fine and named the wrong sections, and no
  gate could see the class.
