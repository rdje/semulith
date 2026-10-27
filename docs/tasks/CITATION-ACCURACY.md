# CITATION-ACCURACY: a quoted citation names the section that holds the quote

## Metadata

- Tree ID: `CITATION-ACCURACY`
- Status: `done` (`2026-10-27` — both leaves complete)
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
  Status: `done` (`2026-10-27`, `SEMULITH-CA-0002`; feature 13 of the alternation's third cycle,
  `decision_alternate-port-and-features.md`)
  Goal: measure the attribution grammar of the tracked Markdown documents that quote the
  pinned specification (dossiers, decision records, the book) — and extend the corpus only
  to a shape the census proves decidable.
  Acceptance: a census of quoted phrases under `ID §N` locators in tracked `.md`, each
  shape dispositioned (decidable → judged; undecidable → counted with its reason); any
  extension RED-proven before it judges.
  Result: **met.** The census over every tracked `.md` (89 `ID §N` locator mentions, 64 in the 408 live documents, 25
  in history under docs/tasks/archive/ and docs/changelog/, which is never edited and not judged): two shapes are
  decidable, both adjacency — MD-R1, a quoted phrase immediately followed by a parenthesized locator; MD-R5, a
  possessive locator immediately before it (`RVI-F §20.1.4's "after rounding"`). A quoted phrase elsewhere in a
  paragraph that names one locator is NOT decidable in prose: the prototype's paragraph rule attributed 61 such
  quotes and they were the laboratory's own wording (`'nothing retired'`, `'a later leaf'` under RVP-MACHINE §2.1.4
  — false misses), so that shape is counted, never judged; 51 locators have no quoted phrase near them; 36 cite ids
  that are not pinned specification sources (ARCHITECTURE, ARCH, HTML, LIMITATIONS, FM); 8 sit beside two or more
  locators. Code spans and fenced blocks are not quotations; a phrase may wrap a line, never a blank line; double,
  typographic and single quotes are read. The gate extends to the live `.md` under the two shapes: 1 attributed quote
  judged (MD-R5 1), 0 findings, 17 counted, uncheckable ARCHITECTURE ×1 (a project document) and SIFIVE-FU540-C000 ×1
  (a PDF pin; the dossier spelled it `FU540` — corrected to the pinned id); the `.sexp` line unchanged (115 judged,
  0 findings). Seven RED/GREEN arms join the wrapper's self-test (22 pass / 0 fail): MD-R1 in section, MD-R1 wrong
  section refused naming §1.2, MD-R5 in section, MD-R5 wrong section refused, a code-span quote not judged, a
  one-locator paragraph quote counted, a wrapped phrase one phrase. DERIVED-COUNTS re-derived the arm total 1685 →
  1692. Evidence target/citation-accuracy (md_census.py, md_scan.py, apply_md.py, selftest.log, corpus.log).
  Verification: `2026-10-27` — the Verification Log below.
  Commit: `SEMULITH-CA-0002`
  `promotion: declined (the grammar is mechanized — the census's dispositions are the gate's rules and its arms).`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | 2/2 leaves complete — the tree closes; a new quoting shape joins as a new leaf with its own RED arm |

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

- `2026-10-27` (`.2`, the census before the extension; sources: target/citation-accuracy/md_census.py over
  every tracked `.md`, md_scan.py over the live ones, both reusing the gate's matcher and pinned pages):
  **The measured grammar.** 89 locator mentions (64 live, 25 historical); 51 with no quoted phrase in their
  paragraph; 36 under ids that are not pinned specification sources; 8 beside two or more locators; 61 in a
  paragraph naming exactly one locator — judged as if attributed, those produced false misses on the
  laboratory's own wording, so paragraph scope is undecidable in prose where a single `.sexp` string was
  decidable (R4). **The decidable shapes**: adjacency only — MD-R1 (quote then `(ID §N`) and MD-R5
  (`ID §N's` then the quote); live population 1, judged OK. **Exclusions**: code spans and fenced blocks
  (code is not a quotation), history parts (never edited after the move), a blank line ends a phrase.

## Open Questions

- Do Markdown documents join the corpus? **Answered by `.2`** (`2026-10-27`): yes, under the two
  adjacency shapes the census proved decidable; paragraph-scope attribution stays counted, never
  judged — a new shape joins only with its own RED arm.

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

`CITATION-ACCURACY.2` — the Markdown census (`2026-10-27`, `SEMULITH-CA-0002`):

- [x] **ROOT CAUSE (WHY + WHERE)** — at 9cdfdc50: `grep -c 'MD-R' scripts/check_citation_quotes.py` = 0 and `main()` judged `git ls-files '*.sexp'` only; the census (target/citation-accuracy/md_census.py): 89 locator mentions in tracked `.md`, 61 quotes in one-locator paragraphs a paragraph rule misattributes (false misses on the laboratory's wording), 2 adjacency quotes.
- [x] **FIX** — scripts/check_citation_quotes.py: `markdown_prose`, `markdown_attributions` (MD-R1, MD-R5), `judge_markdown`, the live `.md` corpus in `main` (history excluded), `--pages` accepting `.md`; scripts/check_citation_quotes.sh: `mdoc`/`runmd` and seven arms (`grep -c 'runmd ' scripts/check_citation_quotes.sh` = 7); profiles/rv64gc-lab-v0/DOSSIER.md: `FU540 §4.7` → the pinned `SIFIVE-FU540-C000 §4.7`.
- [x] **ADDRESSED (verified)** — `bash scripts/check_citation_quotes.sh --self-test` → `CITATION-QUOTES --self-test: 22 pass / 0 fail`; `python3 scripts/check_citation_quotes.py` → `CITATION-QUOTES (markdown): 408 document(s); 1 attributed quote(s) judged (MD-R1 0, MD-R5 1); 0 finding(s); 17 counted (a locator near, no adjacency); uncheckable (no HTML pin): ARCHITECTURE ×1, SIFIVE-FU540-C000 ×1`; the two RED arms fire on the synthetic wrong-section fixtures (`found in §1.2`, `found in §1.1`).
- [x] **NO REGRESSION** — `bash scripts/check_citation_quotes.sh` rc=0 with the `.sexp` verdict byte-identical: `CITATION-QUOTES: 115 attributed quote(s) judged (R1 1, R2 108, R3 3, R4 3); 0 finding(s)`; `bash scripts/check_derived_counts.sh` → ok once LIVE_STATUS re-derived 1685 → 1692; `bash scripts/check_materials_bill.sh` → ok after the dossier edit (model book regenerated).
- [x] **LOCKSTEP** — docs/toolbox/definition.md row (Markdown named); the tree (`.2` done, the tree done, the frontier closed), docs/TASK_TREE.md (the row leaves the index) and docs/TASK_TREE_CLOSED.md (the closed-tree register gains it — FRONTIER-SYNC refused the bare removal first, then a register row naming leaf ids), LIVE_STATUS (arm total), CHANGELOG, MEMORY; profiles/rv64gc-lab-v0/GS-REPORT.md regenerated — the dossier is a profile source file, so its one-locator edit moved the GS content digest (GATE-REPORT refused the first chain).

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-27` | `.2` | the census over every tracked `.md` (89 locator mentions; 61 paragraph-scope quotes shown undecidable; 2 adjacency shapes); the extended tool over the live `.md` (1 judged, 0 findings) and the unchanged `.sexp` corpus; 22 controls (7 new, 2 RED) | met |
| `2026-10-06` | `.1` | the gap measured (check_citations' scope: sem files, existence); the census (108 quotes, 24 attributable); the tool against the real pre-fix files (6 MISS → §20.1.2) and HEAD (24 judged, 0 findings); 14 controls + the mutation (6 RED arms red); registration mirrors | **met** — CITATION-QUOTES registered (35th doctrine); quotes now checked against the section they cite |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.2` | `SEMULITH-CA-0002 (leaf CITATION-ACCURACY.2): the Markdown census — two adjacency shapes decidable and judged, paragraph scope counted` | the census, the two rules, seven arms, the dossier locator; the tree closes |
| `.1` | `SEMULITH-CA-0001 (leaf CITATION-ACCURACY.1): the quoted-phrase-in-section gate — CITATION-QUOTES registered, RED on the real pre-fix corpus (6 misses, each naming §20.1.2)` | the tool + wrapper + registration; `.2` proposed for Markdown |

## Changelog

- `2026-10-27`: `.2` done (`SEMULITH-CA-0002`) — the Markdown census: two adjacency shapes decidable
  and judged (1 live quote), paragraph-scope attribution shown undecidable in prose and counted; the
  tree closes.
- `2026-10-06`: `.1` done (`SEMULITH-CA-0001`) — CITATION-QUOTES registered: 24 attributed quotes
  judged across every tracked `.sexp`, RED-proven on the real pre-fix corpus; `.2` (the
  Markdown census) proposed.
- `2026-10-06`: Created, owning the gap `P4-SYSTEM.7` slice (c3) part 1 measured
  (`SEMULITH-P4-0043`): two locator defects resolved fine and named the wrong sections, and no
  gate could see the class.
