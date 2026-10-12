# Include readers and source-validity assessment — LC.4i2b3a

Owner: `LIVE-CONTAINMENT.4i2b3a / SEMULITH-LC-0028`.
D65 repair: priority1 `.4i2b3b / SEMULITH-LC-0029`, before wider graph review.
Contract: `docs/tasks/artifacts/live-containment/inventory-contract.md`.
This closes an assessment; include-reader signoff and full adoption remain open.

## Closed inputs and actual consumers

Immutable revision `cad73f376766572119490b157a98b69ce5ad04f7`:
1,425 identities, 1,424 regular blobs and opaque `vendor/linkedspec` Gitlink;
473 Markdown sources and 54 literal include candidates. NUL source-wire SHA256:
`e975d5d8798b71d460e63dac1f931afee0b2d30be9569943b1d0212341435414`.
Fresh collector JSON is byte-identical normal/O, SHA256:
`89534a7efe1e055b83803cf0598b9bc443736739f7630407fb0644cfd3ea1dfd`.
The difference from LC0023's selected source is exactly fourteen added identities,
eleven new Markdown files and one graph-receipt teaching candidate; none removed.
CH shards0292–0299, the ordinary LIVE-CONTAINMENT archive, graph-census/task-claims
receipts and three project Python sources account for the complete added set.
Thirteen existing members change; their complete old/new records are in
source-body-delta.json. They are separately pinned, not silently treated as old.
Changed paths: CHANGELOG/DEV_NOTES/LIVE_STATUS/MEMORY; TASK_TREE_CLOSED;
book status/task-trees; SHARDS manifest; doctrine/toolbox governance;
LIVE-CONTAINMENT; check_frontier_sync/check_tree_claims. Their exact path/old/new
record JSON SHA256 is
`20fb60c7438a2e93e4eab346cbddd9f52785c96ee39eb4ab8ec011689bac83a0`.

The measured working view starts with only two owned task/pointer changes.
Every executed chapter and include target matches its immutable source blob,
physical SHA256 and Git mode. Complete tracked HEAD/index/physical identities,
modes and opaque Gitlink are equal before/after each capture/fixture matrix.
Only ignored diagnostic outputs change. Final book/tracker edits are a separate
proposed view, checked through ordinary focused builds; historical output bytes
are not claimed for that later view.

Fourteen actual `mdbook build` calls (seven books normal/O) use the public
preprocessor command override to capture the protocol immediately after built-in
`links`, before unchanged `scripts/book_navigation.py`. The wrapper forwards
supports requests, original stdin, stdout, stderr and exit status. Every actual
consumer returns0. Context records retain repository-relative book identity;
raw context with checkout-specific paths is hashed rather than persisted.
The API reports mdbook0.5.4 and `book.items`/Chapter/sub_items. A first diagnostic
assumed an older `sections` field, then was corrected from actual protocol and
project-owned consumer source; no product defect was inferred from that error.

Seven consumers supply 93 complete source chapters. All 344 output files,
including assets, are byte-identical to a separate fresh uninstrumented bundle
in each mode. Actual whole chapter payloads agree normal/O. Independent source
selection/substitution reconciles all 93 full expanded chapter texts, including
chapters without includes: 49 executed occurrences, 42 whole-file and seven
named-anchor selections, into 48 unique regular targets. Every selected anchor
has one ordered opener/closer. All target bodies have zero literal include
prefixes, closing this observed include transitive edge set; this does not
qualify other directives, index/query readers or generated-resource routes.

## Complete executed edge ledger

Each row identifies one source occurrence and its resolved repository-relative
target. `whole` retains anchor comments. Offsets, exact marker/source/target
Git OIDs and SHA256, selected text bytes/digests, complete chapter expansion
pins, consumers and the five other candidates are retained in reader-ledger.json.
Its 80,700-byte SHA256 is:
`b4be9b9a4d1896f8439b94f2bf0b820b3d98f3a6758d805668407c960cc3cda5`.
The immutable source revision plus the explicit rows below are the durable
reconstruction inputs; ignored captures are diagnostic evidence, not promised
permanent storage or a new archive authority.

| Source chapter | Byte offset | Target | Selection |
| --- | ---: | --- | --- |
| `docs/book/src/status.md` | 65 | `LIVE_STATUS.md` | `whole` |
| `docs/book/src/plan/p4/gate.md` | 4080 | `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md` | `policy` |
| `docs/book/src/contracts/method.md` | 556 | `docs/METHOD.md` | `whole` |
| `docs/book/src/contracts/rules.md` | 1077 | `RULES.md` | `whole` |
| `docs/book/src/contracts/architecture.md` | 1019 | `docs/ARCHITECTURE.md` | `whole` |
| `docs/book/src/contracts/cpu-environment.md` | 1174 | `docs/CPU_ENVIRONMENT.md` | `whole` |
| `docs/book/src/contracts/evidence-and-gates.md` | 1508 | `docs/EVIDENCE_AND_GATES.md` | `whole` |
| `docs/book/src/contracts/archogen.md` | 1841 | `docs/ARCHOGEN_INTEGRATION.md` | `whole` |
| `docs/book/src/contracts/information-catalog.md` | 1221 | `docs/INFORMATION_CATALOG.md` | `whole` |
| `docs/book/src/contracts/risks.md` | 907 | `docs/RISKS_AND_DECISIONS.md` | `whole` |
| `docs/book/src/contracts/sources.md` | 982 | `docs/SOURCES_AND_NAMING.md` | `whole` |
| `docs/book/src/contracts/review-disposition.md` | 1189 | `docs/REVIEW_DISPOSITION.md` | `whole` |
| `docs/book/src/working/task-trees.md` | 2102 | `docs/ARTIFACT_CLEANUP.md` | `latest` |
| `docs/book/src/working/task-trees.md` | 4824 | `LIVE_DOCUMENT_SIZE_CONTAINMENT.md` | `whole` |
| `docs/book/src/working/task-trees.md` | 4981 | `docs/TASK_TREE.md` | `trees` |
| `docs/book/src/working/task-trees.md` | 5172 | `docs/TASK_TREE_CLOSED.md` | `closed` |
| `docs/book/src/working/task-trees.md` | 16804 | `docs/decisions/reference_temporary-allocation-controls.md` | `controls` |
| `docs/book/src/glossary.md` | 159 | `docs/GLOSSARY.md` | `whole` |
| `docs/models/rv64i-lab-v0/src/materials.md` | 1953 | `docs/models/rv64i-lab-v0/src/materials/pinned-specifications.md` | `whole` |
| `docs/models/rv64i-lab-v0/src/materials.md` | 4500 | `docs/models/rv64i-lab-v0/src/materials/encoding-tables.md` | `whole` |
| `docs/models/rv64i-lab-v0/src/materials.md` | 6234 | `docs/models/rv64i-lab-v0/src/materials/reference-models.md` | `whole` |
| `docs/models/rv64i-lab-v0/src/materials.md` | 10467 | `docs/models/rv64i-lab-v0/src/materials/internal-contracts.md` | `whole` |
| `docs/models/dsp56300-lab-v0/src/materials.md` | 1599 | `docs/models/dsp56300-lab-v0/src/materials/pinned-specifications.md` | `whole` |
| `docs/models/dsp56300-lab-v0/src/materials.md` | 3034 | `docs/models/dsp56300-lab-v0/src/materials/encoding-tables.md` | `whole` |
| `docs/models/dsp56300-lab-v0/src/materials.md` | 4501 | `docs/models/dsp56300-lab-v0/src/materials/reference-models.md` | `whole` |
| `docs/models/dsp56300-lab-v0/src/materials.md` | 7751 | `docs/models/dsp56300-lab-v0/src/materials/internal-contracts.md` | `whole` |
| `docs/models/netboard-lab-v0/src/materials.md` | 690 | `docs/models/netboard-lab-v0/src/materials/pinned-specifications.md` | `whole` |
| `docs/models/netboard-lab-v0/src/materials.md` | 2741 | `docs/models/netboard-lab-v0/src/materials/encoding-tables.md` | `whole` |
| `docs/models/netboard-lab-v0/src/materials.md` | 2784 | `docs/models/netboard-lab-v0/src/materials/reference-models.md` | `whole` |
| `docs/models/netboard-lab-v0/src/materials.md` | 2855 | `docs/models/netboard-lab-v0/src/materials/internal-contracts.md` | `whole` |
| `docs/models/netboard-lab-v0/src/the-map.md` | 627 | `profiles/netboard-lab-v0/map.md` | `whole` |
| `docs/models/netboard-lab-v0/src/the-verdict.md` | 594 | `profiles/netboard-lab-v0/COMPOSITION-VERDICT.md` | `whole` |
| `docs/models/netboard-lab-v0/src/the-export.md` | 1644 | `profiles/netboard-lab-v0/platform.sexp` | `whole` |
| `docs/models/sifive-uart-lab-v0/src/materials.md` | 1196 | `docs/models/sifive-uart-lab-v0/src/materials/pinned-specifications.md` | `whole` |
| `docs/models/sifive-uart-lab-v0/src/materials.md` | 2509 | `docs/models/sifive-uart-lab-v0/src/materials/encoding-tables.md` | `whole` |
| `docs/models/sifive-uart-lab-v0/src/materials.md` | 2552 | `docs/models/sifive-uart-lab-v0/src/materials/reference-models.md` | `whole` |
| `docs/models/sifive-uart-lab-v0/src/materials.md` | 2710 | `docs/models/sifive-uart-lab-v0/src/materials/internal-contracts.md` | `whole` |
| `docs/models/lan9118-lab-v0/src/materials.md` | 952 | `docs/models/lan9118-lab-v0/src/materials/pinned-specifications.md` | `whole` |
| `docs/models/lan9118-lab-v0/src/materials.md` | 2663 | `docs/models/lan9118-lab-v0/src/materials/encoding-tables.md` | `whole` |
| `docs/models/lan9118-lab-v0/src/materials.md` | 2706 | `docs/models/lan9118-lab-v0/src/materials/reference-models.md` | `whole` |
| `docs/models/lan9118-lab-v0/src/materials.md` | 2864 | `docs/models/lan9118-lab-v0/src/materials/internal-contracts.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/materials.md` | 648 | `docs/models/rv64gc-lab-v0/src/materials/pinned-specifications.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/materials.md` | 5909 | `docs/models/rv64gc-lab-v0/src/materials/encoding-tables.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/materials.md` | 6637 | `docs/models/rv64gc-lab-v0/src/materials/reference-models.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/materials.md` | 7825 | `docs/models/rv64gc-lab-v0/src/materials/internal-contracts.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/policy.md` | 336 | `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/evidence.md` | 384 | `profiles/rv64gc-lab-v0/GS-REPORT.md` | `whole` |
| `docs/models/rv64gc-lab-v0/src/evidence.md` | 4251 | `docs/decisions/decision_qualified-matched-experiment-contract.md` | `contract` |
| `docs/models/rv64gc-lab-v0/src/evidence.md` | 4763 | `docs/decisions/decision_sail-gpr-comparison-method.md` | `method` |

The five remaining literal occurrences are in BOOK-APPARATUS (two), P5-BOARD,
SEMULITH-PKG and graph-census.md (one each), all under docs/tasks. None is an
actual source_path in any captured chapter or any of the 48 included targets.
They therefore do not execute through this observed include graph. They remain
inputs to other-reader review; directory/fence membership alone did not exclude
them. Fences do not protect an executed chapter's include marker from mdBook.

## Public behavior and D65

Twelve isolated public mdBook fixtures/mode exercise whole text with/without a
terminal LF, two terminal LFs, CRLF, named/nested anchors, whole-file anchors,
line range, fenced and nested includes, and the three failures below.
Whole decoding normalizes CRLF and omits exactly one final LF. Anchor selection
strips anchor marker lines; whole-file selection retains them. Range2:4 selects
lines2–4. Fenced and nested includes execute. These finite observed cases are
not a complete syntax/format or semantic-completeness claim.

| Bad source | mdbook0.5.4 result | Public Python checker | Public Bash guard |
| --- | --- | --- | --- |
| Missing target file | rc0; token survives; stderr logs ERROR/WARN | rc0 | rc0 |
| Missing selected anchor | rc0; empty expansion; no warning/error | rc0 | rc0 |
| Duplicate selected anchor | rc0; first region only | rc0 | rc0 |

Every bad case is exercised in both the project and registered model book,
normal/O: twelve bad corpus/mode cases, 24 false-green interface evaluations.
One valid selected-anchor case per mode returns0 on both interfaces (four greens).
The actual components are `python3 scripts/unit_books.py CORPUS_ROOT` and
`bash scripts/check_unit_books.sh`. The Bash fixture uses a repository-relative
symlink to these same project scripts and a narrow Git facade supplying only
its owned fixture root; unsupported Git calls exit73. No real chapter, Git
boundary or toolchain implementation is amended. All existing guard self-tests
pass before each public fixture verdict. A diagnostic initially failed Python
compilation for one missing closing bracket; only the ignored diagnostic was
corrected before any product verdict was recorded.

**D65 root cause:** project check_books uses mdbook return status for build
success and checks rendered navigation, without validating include source or
anchor selections. Successful-build stderr is not a failure input. Missing and
duplicate anchors are silent, so stderr-only repair cannot close the gap.
UNIT-BOOKS explicitly promises catalogue/build/navigation, with semantic/chapter
completeness separate. The uncovered source-integrity requirement is now owned;
this assessment does not retroactively widen the original guard's stated scope.
Impact: a removed or ambiguous included contract can disappear or be truncated
from the director's review surface while the commit check reports green.
Current real includes reconcile completely; no broken real include is claimed.

**Required next repair:** project-owned source/selection validation through
actual build inputs; qualify whole/anchor/range/fenced/nested positives, missing
and duplicate selectors, unavailable/unsafe sources and omission controls,
normal/O. Preserve original controls, public book output, source ownership,
caps and archive contracts. Public mdBook behavior is an integration boundary;
never inspect or amend its implementation or any other repository.

## Reproduce and falsify

The public collector can be rerun with the named source and a fresh output:

```sh
python3 scripts/collect_containment_graph.py --revision cad73f3 \
  --output target/live-containment/include-readers/replay
```

For a minimal actual Python-interface reproduction, run the following at the
repository root. It creates only owned target inputs. At LC0028 the bad selected
anchor returned0; after D65 repair it must be rejected. Use a fresh directory
name when repeating. Change `absent` to `selected` for the positive control;
remove fragment.txt for missing-file, or append a second selected region for
duplicate-anchor. Put the token in project/models.md to exercise the other role.

```sh
python3 - <<'PYREPRO'
from pathlib import Path
import subprocess
r = Path('target/live-containment/include-readers/reproduce-anchor')
(r / 'materials').mkdir(parents=True, exist_ok=False)
(r / 'materials/units.sexp').write_text(
    '(unit (id "u1") (kind processor) (layer processor) '
    '(book "docs/models/u1"))\n')
for book, chapter in [('docs/book', 'models.md'), ('docs/models/u1', 'intro.md')]:
    p = r / book
    (p / 'src').mkdir(parents=True)
    (p / 'book.toml').write_text('[book]\ntitle = "Owned fixture"\nsrc = "src"\n')
    (p / 'src/SUMMARY.md').write_text('# Summary\n\n[One](' + chapter + ')\n')
    body = '# One\n' + ('- **`u1`** (kind: processor)\n' if book == 'docs/book' else '')
    (p / 'src' / chapter).write_text(body)
p = r / 'docs/models/u1/src'
(p / 'fragment.txt').write_text('// ANCHOR: selected\ncontract\n// ANCHOR_END: selected\n')
with (p / 'intro.md').open('a') as f:
    f.write('\n' + '{' * 2 + '#include fragment.txt:absent' + '}' * 2 + '\n')
for flag in [[], ['-O']]:
    result = subprocess.run(['python3', *flag, 'scripts/unit_books.py', str(r)])
    print('optimized' if flag else 'normal', 'verdict', result.returncode)
PYREPRO
```

Three actual copied ledger diagnostics omit metadata append, selected-content
substitution or chapter append. Each fails its named population/full-text
check with exit1, normal/O; real inputs and successful ledger bytes stay exact.
These qualify this assessment instrument, not a repaired integration gate.
The current project guard's false greens are deliberately preserved evidence.

Local outputs: `target/live-containment/include-readers` holds source/captures,
fixtures, public matrices, reader ledger, before/after state and raw streams.
Pinned helpers/results below use SHA256; all are ignored diagnostics. Their
byte pins establish which instruments ran, not an independent semantic oracle.

| Diagnostic/result | SHA256 |
| --- | --- |
| `capture_preprocessor.py` | `3b13b1f37bbdb56b2e0e01f0c0fdaeaf2e339991c81ab3fb82f5feb42866067f` |
| `capture_all.py` | `a9df9047f32b336fa6ec3e3aab78b39350f108bb78bf23e025e4b3887d82000b` |
| `capture_plain.py` | `0ea7ef6e25259d0638279eb98511bdc603155d82bae12979498baf11b14834df` |
| `fixtures.py` | `1e675cbaab4e13780112b2c7714f049763199e8c7b4220e2ea6f7899d995e162` |
| `public_guard.py` | `4bee1c7469c099dd387e8761618836eb2e3f7500e603f8e9ae039b5218d1007c` |
| `ledger.py` | `a0810e3d6cddd2d710a251fcba50aaee86a32195af0cf43733d9c74b750eabb3` |
| `fixtures-results.json` | `2b387244a1a374c1c867b0ee4fd85e568e2a90685bbc87d78e14fe4e2fec231f` |
| `public-unit-result.json` | `59450675c8ced9136fe5c735e2358f22dc39f39352269b437ea7d2c8fb23525a` |
| `capture-results.json` | `88fd23b2ddd68e4f37076a5b29b41b8afc712b4842a1efb1a242d23fcef2d087` |
| `input-delta.json` | `863b9697657290ac4695eb468f1d47a38b212b73cb6ffc5711e2fdd9412927b2` |
| `ledger-omissions.json` | `126ed8be8ca0ecf2b153dbda60e3160988064f04f50bfe1e331f8494be320650` |

Qualification remains finite. Capturing every current source chapter and exact
whole output does not establish future syntax support, historical truth,
semantic completeness, remote availability, lifecycle/utility decisions or
complete reader/author-route graph coverage. Those remain explicit LC.4 work.
