# Before-links include validator — LC.4i2b3b1

Owner: LIVE-CONTAINMENT.4i2b3b1 / SEMULITH-LC-0029.
This qualifies the standalone source component. D65 remains open until LC0030
integrates and verifies both public project guards and default seven-book builds.
Earlier assessment: docs/tasks/artifacts/live-containment/include-readers.md.

## Retained complete closed book receipts

These two complete paragraphs retain their original source identities and inverse
instructions. Their underlying ordinary archive records stay byte/mode exact.
They are reader receipts, not changed processor evidence or archive authority.

<!-- LC0029 retained reader receipts -->
````text
A later privilege-timeline containment applies the same complete-source inverse
at one span. Its map in `docs/tasks/archive/P4-SYSTEM-book-c32b0.md` records
source `21a997f`, 14,486 bytes and SHA-256
`bc97a1b69d515c5a9b0af2dd9022084bac7c08e8dc8955720e2901756595382f`.
Check the retained chapter's proposed digest, replace the exact replacement at
the recorded byte offset with the marked original 8,436-byte payload, then
verify the entire restored source against that commit. Corruption, a missing
marker or an omitted payload must refuse. Current features and CSR examples
stay in the book; historical checkpoint counts stay in the immutable archive.

The FP timeline provides another full-source inverse:
`docs/tasks/archive/P4-SYSTEM-book-c33b0.md` authenticates source `07e14ae`,
24,259 bytes, SHA-256
`ef2fd2d2d8395dbbf848d6b6a37b914c3b6d4499b60812d98db507edd8ad0db1`.
Verify proposed chapter bytes/SHA, replace the mapped span with the marked
10,576-byte original introduction, then verify the entire restored chapter
against Git. Its semantic code fence and current feature/witness sections
remain in the book. Damaged payloads or missing markers cannot receive credit.

````
<!-- LC0029 end retained reader receipts -->

## Whole source inverse

```json
{
  "source": "docs/book/src/working/task-trees.md",
  "source_commit": "b6a21234d47bc1423883c4dc4425bfe42b6df632",
  "source_bytes": 16891,
  "source_sha256": "5ce0d6b214e1c7ffc8fe562e6b0a46fbf57c9870fd9df42d691ee63d75fed1c3",
  "offset": 10474,
  "payload_bytes": 1179,
  "payload_sha256": "c9850d906c9ef289b121c2bdae9b67cf8c7f068434d467a12380bae5fcdafa81",
  "replacement": "The complete privilege/FP timeline-containment receipts and inverse instructions\nare retained with the include-validator evidence:\n\n```sh\ncat docs/tasks/artifacts/live-containment/include-source-validator.md\n```\n\n**Include source validation (component).** Whole text, ASCII anchors and one-based\nline selections (`:2`, `::10`, `:2:`, `:2:10`) are checked before expansion.\nMissing/ambiguous selections fail1; unsupported/unsafe/unreadable inputs refuse2.\nValid input returns the same book. Spaces after # refuse2. Fences expand;\nnested includes follow selected text relative to the included file. Cycles fail;\nempty files and empty named regions are valid. CRLF becomes LF; bare CR/Unicode\nseparators stay inside physical lines. This checks source integrity, not prose truth.\n\nFrom the repository root, qualify controls and opt into the project-book check:\n\n```sh\npython3 scripts/probe_book_includes.py\npython3 -O scripts/probe_book_includes.py\nMDBOOK_PREPROCESSOR__SOURCE_CHECK__COMMAND='python3 ../../scripts/book_includes.py' \\\nMDBOOK_PREPROCESSOR__SOURCE_CHECK__BEFORE='[\"links\"]' \\\nmdbook build docs/book\n```\n\nDefault UNIT-BOOKS still needs LC0030 integration; D65 remains open.\n\n",
  "proposed_bytes": 16897,
  "proposed_sha256": "3dd9d8e07ced05dea99c4e41c58b0d244751e0d4fe92b596ebe6aae24412b6d1",
  "book_delta": 6
}
```

## Component contract and qualification

Immutable component input: b6a21234d47bc1423883c4dc4425bfe42b6df632,
1427 tracked identities. Actual execution pins include the four new Python
modules, this owned record and two new whole history shards; the final working
qualification covers1434 identities from the actual index and physical pins. The complete index, physical sources and modes
are checked before/after every replay. Earlier public fixtures qualify installed
mdbook0.5.4 ordering, selected nested paths and LF/CRLF/bare-CR/Unicode behavior.
The validator preserves the complete JSON book object. It reads actual chapter
sources and selected transitive include inputs, not a guessed chapter catalogue.

`scripts/book_includes.py` accepts public `[context, book]` stdin and implements
`supports html`. Exit0 emits the unchanged book; missing files, absent/duplicate/
inverted anchors, nonexistent/inverted line ranges and cycles fail1. Unsupported
helpers/selectors, malformed protocol, unsafe paths, symlinks, other Git boundaries,
other volumes, invalid UTF-8, failed reads and changed inputs refuse2. Failures emit
no stdout. Explicit source-less drafts cannot contain includes; a missing source
field refuses. Whole text removes one final LF; CRLF becomes LF, bare CR and Unicode
LS/NEL remain inside physical LF lines. Named selection strips anchor-marker lines;
only selected text contributes nested inputs. Whole selection preserves marker text.

Supported named selectors are ASCII letters/digits/underscore/hyphen, excluding
all-decimal names reserved for line selection. Whole text and `:2`, `::2`, `:2:`,
`:1:2` cover the documented one-based single/inclusive/open-ended forms. Malformed,
multiline or unsupported helper syntax is explicitly refused rather than assumed
valid. This is source-integrity evidence, not prose correctness, general Markdown
semantics, full containment coverage or an accepted processor profile. Unique
selected file/selector nodes are memoized; direct chapter occurrences and edges
of unique selected nodes are recorded with normalized character offsets, not raw
byte offsets. Chapter-population completeness is a separate catalogue contract.

The shared `scripts/book_paths.py` contains the original unit_books path predicate
bodies verbatim. `unit_books.py` retains the public names through imports; only that
extraction/import changed. The original 23 unit-book and 26 navigation controls
pass normal/O. There is no circular dependency or default integration in this unit.

22 component methods pass normal/O. Thirteen copied component omissions fail the
actual copied probe in both modes (26 failures1): include following, anchor uniqueness,
line bounds, required source field, lexical book-root route, nested inputs, final
source stability, UTF-8, duplicate JSON keys, non-JSON constants, shared symlink/Git
component checks, shared volume checks and the after-# spacing predicate. These finite controls discriminate the
named omissions; they do not prove every possible mutation is detected.

The tracked producer's public fixtures run twelve valid cases and five invalid
cases in each mode: whole LF/no-LF/double-LF/CRLF, named/nested anchors, whole anchor
comments, ranges, fences, nested includes; missing file/anchor and duplicate anchor
stop with mdbook101 before the expanded witness. Before-# spacing and argument
spaces/tabs expand normally. After-# spacing remains literal in unvalidated
public baseline builds; the validator refuses2 and those builds stop101. All24 positive expanded chapter
strings match independent fixture constants. Eight actual public source-fault cases
(chapter/include × read/change × normal/O) refuse2 with empty stdout and exactly one
injection marker. Virtual-volume and post-read source changes also have dedicated
component controls. No tracked or external source is altered by these faults.

Both modes execute the actual component before links in all seven current books:
93 complete chapters,49 include edges and344 complete generated files. Captured
and uninstrumented builds have identical full output populations and bytes;
complete raw and expanded chapter payloads and component reports agree normal/O.
The working input includes the lossless book-receipt move recorded above.
D67 repairs permissive after-# spacing recognition: keep broad candidate
detection but refuse syntax the actual links preprocessor leaves unexpanded.
The new control failed before repair; an actual copied grammar omission fails
after repair. The interrupted first commit was not a green or completed commit.
Earlier pre-move captures remain separate evidence and are not substituted for this view.

## D66 — tracked replay repair

LC0028 named three ignored producers. Their old pins retained observations but
could not alone satisfy the tracked-producer policy. The replacement producer is
`scripts/qualify_book_includes.py`, routed in `docs/toolbox/governance.md`; its
capture protocol, historical projection, public fixture/fault recipes and actual
copied-omission recipes are tracked together. D66 is fixed by this publication;
LC0028's original observation is preserved, with this durability correction.

Historical replay accepts only reviewed cad73f376766572119490b157a98b69ce5ad04f7.
Checked local Git source supplies1425 identities; regular project blobs are copied
byte/mode-exact into a fresh owned non-Git target workspace. Gitlinks stay opaque
and unmaterialized. GIT_NO_LAZY_FETCH=1 prevents implicit acquisition. Unavailable
source refuses2; nothing fetches or writes into another repository. The copied
project's own published preprocessors run through public mdbook interfaces.

Actual raw and expanded captures reconcile all93 complete chapters,49 occurrences,
48 targets and five other literal candidates, then compare all344 output files to
a fresh uninstrumented build. Both modes emit the exact original80700-byte ledger:
SHA-256 b4be9b9a4d1896f8439b94f2bf0b820b3d98f3a6758d805668407c960cc3cda5.
This is a fresh build of immutable source, not retained historical toolchain output.
The historical independent projection is deliberately limited to the observed
whole/HTML-anchor subset; transitive or unsupported historical forms refuse.

Ten producer controls pass normal/O. Four copied producer omissions (regular
source population, body SHA, complete literal-candidate population and complete
output population/bytes) fail named controls with refusal2 and empty stdout in both
modes. Missing immutable source also refuses2/empty stdout in both modes. All
actual working identities/index/modes and copied regular source bytes/modes remain
exact. No full graph, utility, lifecycle, archive, capacity or processor authority
is granted. D65 remains open until LC0030 qualifies both actual public guards and
all seven default configurations.

## Reproduce from a committed checkout

Run from the repository root with the documented mdbook tool available. Each output
must be a fresh `target/` path; a reused or unsafe output refuses2. All persisted
project paths are repository-relative. The tools derive absolute paths at runtime.
During an uncommitted qualification, enumerate each owned new input with
`--addition PATH`; after publication those files are in the tracked population.

```sh
python3 scripts/probe_book_includes.py
python3 -O scripts/probe_book_includes.py
python3 scripts/qualify_book_includes.py --self-test
python3 -O scripts/qualify_book_includes.py --self-test
python3 scripts/qualify_book_includes.py --output target/include-replay-normal
python3 -O scripts/qualify_book_includes.py --output target/include-replay-optimized
python3 scripts/qualify_book_includes.py --working --output target/include-working-normal
python3 -O scripts/qualify_book_includes.py --working --output target/include-working-optimized
python3 scripts/qualify_book_includes.py --fixtures --output target/include-fixtures-normal
python3 -O scripts/qualify_book_includes.py --fixtures --output target/include-fixtures-optimized
python3 scripts/qualify_book_includes.py --omissions --output target/include-omissions-normal
python3 -O scripts/qualify_book_includes.py --omissions --output target/include-omissions-optimized
```

The historical `reader-ledger.json` is the closed LC0028 projection. Current
`working-report.json` contains every actual component chapter/edge/input pin;
`output-files.json` records the complete fresh output population. Fixture and
omission result files retain verdicts and injection/mutant identities. Generated
outputs remain ignored; tracked producers, source identities and the following
pins retain the qualification. A stale producer or source must be requalified.

## Publication pins

| Input or generated receipt | Bytes | SHA-256 |
| --- | --- | --- |
| `scripts/book_paths.py` | 2063 | `3b5fd6b262efd33f801e573c053c603f4c54c3f695bc5165c920a4be84638044` |
| `scripts/book_includes.py` | 13458 | `26f74899da50b516efb4091a967ebd73c038d51ed449d12d1b8d39202cf975a5` |
| `scripts/probe_book_includes.py` | 14952 | `679ac858bbe633d0d48f598e6cf75b8cf3276a6876816a07afcbf118712af930` |
| `scripts/qualify_book_includes.py` | 36505 | `9a5af667f696ca84c1dd909892b4b494d0bb9f157dffda47225fffa86494daa4` |
| `target/live-containment/include-source-validator/d67-replay-normal/reader-ledger.json` | 80700 | `b4be9b9a4d1896f8439b94f2bf0b820b3d98f3a6758d805668407c960cc3cda5` |
| `target/live-containment/include-source-validator/d67-replay-normal/result.json` | 396 | `6afe5fc73a3d614e413178f1303e552f755be238266c21ccfaa7e10bd3f040e8` |
| `target/live-containment/include-source-validator/d67-replay-optimized/result.json` | 396 | `6afe5fc73a3d614e413178f1303e552f755be238266c21ccfaa7e10bd3f040e8` |
| `target/live-containment/include-source-validator/d67-working-normal/result.json` | 325 | `1118f877b23dbee3f3b2bfe718b7484d16ffffcb1f461c445688e37a42d79faa` |
| `target/live-containment/include-source-validator/d67-working-optimized/result.json` | 325 | `1118f877b23dbee3f3b2bfe718b7484d16ffffcb1f461c445688e37a42d79faa` |
| `target/live-containment/include-source-validator/d67-public-normal/fixtures-result.json` | 2119 | `82f9ded7179b3e4be3a9b0038771a6e914ee7d81d2796f8fafae72114adffcee` |
| `target/live-containment/include-source-validator/d67-public-optimized/fixtures-result.json` | 2122 | `8625f3a755de708c2bc60dc65be082062eb6dee730e3928286f7a44a940d7653` |
| `target/live-containment/include-source-validator/d67-mutants-normal/omissions-result.json` | 4979 | `0abb00c596fa1761c94650baf21ebd7a286396320c51ed942b5df61c7d753bab` |
| `target/live-containment/include-source-validator/d67-mutants-optimized/omissions-result.json` | 4982 | `01b5dcfa030d8a78ac5b6bb2ba8095afe3c103385ab87b888a607b1c84e373ae` |
