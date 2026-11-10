# XTASK ordinary history — part 9

Ordinary, directly readable task history: the narrative paragraphs of `XTASK.13` slices d to g, retained verbatim
from `docs/tasks/XTASK.md` as staged for `SEMULITH-XTASK-0090` on top of commit `276ce805d7308e1bd8d0465331ba93b9ed5d3081`. The live tree keeps one pointer line per node. Relative links inside the
retained text are written from `docs/tasks/`, their original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive part is the
task family's standing mechanism (decision_containment-reset, 2026-10-21).

| Span | Bytes | SHA256 |
| --- | --- | --- |
| slice paragraphs 13d-13g | 7334 | `db24931990afa9df608cb411dfca7108ace1e08d128172ad426b2d2891fb346f` |

<a id="slice-paragraphs-13d-to-13g"></a>

## slice-paragraphs-13d-to-13g

  Slice g (`2026-11-07`, `SEMULITH-XTASK-0085`; on clean e0f03ac9; evidence target/xtask/xt0085): `EXERCISE-COVERAGE`'s controls judge frozen fragments, so a damaged real one fails by its own name. The 5:1 turn, after a50-4 and two maintenance units. **The change.** `scripts/fixtures/exercise-coverage/definitions/riscv/` holds the three fragments the controls compose, verbatim. A missing frozen copy is named before any arm runs, where the old `let _ = fs::copy` would have swallowed it. The 23 arms and the real check are otherwise unchanged. Each state judged by the binary before and after on throwaway clones:

  | Damaged state | Before | After |
  | --- | --- | --- |
  | none | `rc=0` | `rc=0`, `19/19 200/200 …` |
  | `rv64i.sexp` deleted | `rc=2`, self-test miss | `rc=1`, `UNMET DEPENDENCY`, naming the fragment |
  | `zicsr.sexp` deleted | `rc=2`, self-test miss | `rc=1`, `UNMET DEPENDENCY`, naming the fragment |
  | `zicntr.sexp` deleted | `rc=2`, self-test miss | `rc=1`, `UNMET DEPENDENCY`, naming the fragment |
  | `rv64i.sexp` truncated | `rc=2`, self-test miss | `rc=1`, `UNMET DEPENDENCY`, its unterminated list |
  | a stray parenthesis in `rv64i.sexp` | `rc=2`, self-test miss | `rc=1`, `UNMET DEPENDENCY`, its line 98 |
  | a frozen copy deleted | no such copy | `rc=2`, naming the frozen fragment |

  No path a case pins moved. Next at the 5:1 turn: CONTRACT-FREEZE.
  Slice f (`2026-11-06`, `SEMULITH-XTASK-0084`; on clean b52965bf; evidence target/xtask/xt0084): `MATERIALS-BILL`'s controls judge frozen dossiers, so a damaged real one fails by its own name. The 5:1 turn, after a49-3. **The change.** `scripts/fixtures/materials-bill/` holds what the generator reads of the processor's dossier, with three of its guests, the UART's and the board's, the processor's book, and three small renamed cases, 29 files, 245,396 B; the self-test re-roots those. `test_gen_model_book.py`'s case-index tests judge the frozen cases, with `G.REPO` patched, and name no real case. **What freezing alone would have left:** `emit_cases` read the real `evidence/` for any processor shape, so a re-rooted frozen dossier still read every real case: a dossier outside this repository's `profiles/` now holds no case. **Two tracebacks made names:** a board dossier that lost `board.sexp` crashed the generator, which then read it as a processor by its default shape, and crashed the judge; a dossier declaring neither `profile.sexp` nor `board.sexp` is now refused by name, the judge names the unit, a twelfth arm and an eleventh generator test hold it. **Measured** (`red-states.txt`, each binary built in its own throwaway clone, because a binary carries its repository root at compile time, so a copied one reads the wrong tree):

  | Damaged state | Before | After |
  | --- | --- | --- |
  | none | `rc=0` | `rc=0` |
  | `rv64i`'s `references.sexp` deleted | `rc=2`, self-test failed | `rc=1`, `CANNOT JUDGE rv64i-lab-v0` |
  | the UART's `sources.sexp` deleted | `rc=2`, self-test miss | `rc=1`, `CANNOT JUDGE sifive-uart-lab-v0` |
  | the board's `board.sexp` deleted | `rc=2`, a traceback | `rc=1`, `CANNOT JUDGE netboard-lab-v0` |
  | a does-not-supply statement removed from `rv64i`'s bill | `rc=2`, self-test miss | `rc=1`, `NO DOES-NOT-SUPPLY rv64i-lab-v0` |
  | a case's declaration deleted | `rc=1` | `rc=1`, `DRIFT rv64gc-lab-v0` |

  Moving the generator moved its digest in all 25 fragments of six books, regenerated, each otherwise unchanged. No path a case pins moved: `gen_model_book.py` is not among the 73 manifest children. Next at the 5:1 turn: EXERCISE-COVERAGE.
  Slice e (`2026-11-06`, `SEMULITH-XTASK-0082`; on clean 979a5b14; evidence target/xtask/xt0082): `PLATFORM-GEN`'s controls judge a small frozen tree, so a damaged real board or dossier fails by its own name. The 5:1 turn, after a47-3. **The change.** The self-test reads `BOARD-VERDICT`'s frozen definition and composed obligations and a frozen `rv64i-lab-v0/profile.sexp` in `scripts/fixtures/platform-gen/`, 16,542 B, which `read_processor` prefers to the repository's; not beside `BOARD-GEN`'s parts, since RECORD-SCHEMA reads a catalogue with a profile beside it as a whole unit, which refused the first gate. The dossier pin stays load-bearing: the scratch directory is untracked, so its digest is the empty one, the frozen board is pinned to that, and the stale-pin arm still fires. **Two arms passed for the wrong reason, found reading them.** `RED a hand-edited platform.sexp` and `RED a moved definition` copied the committed manifest and ran `--check` from another directory, so the fingerprint's path alone made it DRIFT, with or without the edit: each would have stayed green had the check stopped reading the bytes it claims to. Both now judge the generation the `GREEN … in sync` arm just passed, changing one thing. **The hole freezing would have opened**, as at slices c and d: `ok (no board declares itself yet)` for a deleted definition; a `platform.sexp` with no `board.sexp` beside it now fails by name. Two new arms, 13 in all. **Measured** (`red-states.txt`, both binaries, each state restored): a deleted `board.sexp`, composed obligations or profile go from `rc=2`, a missed control over a scratch path, to `rc=1` naming the file; a deleted `platform.sexp` from the same miss to `rc=1`, `missing (never generated)`; a hand-edited one stays `rc=1` DRIFT; a damaged frozen profile `rc=2`. **Maintenance in the same commit:** `CHANGELOG.md` sharded at 65,178 of 65,536 B. Next slice: MATERIALS-BILL.
  Slice d (`2026-11-06`, `SEMULITH-XTASK-0081`; on clean 506788a6; evidence target/xtask/xt0081): `BOARD-GEN`'s controls judge a small frozen tree, so a damaged real board or part fails by its own name. The 5:1 turn, taken after feature 5, with a46-3's captures waiting behind it: no board or part unit is among the 93 distinct manifest children of all 22 cases, and `git diff --name-only 506788a6 --cached` ∩ them is empty. **The change.** The self-test copies `BOARD-VERDICT`'s frozen `board.sexp`, byte-identical to the real one, so no definition is duplicated, and `scripts/fixtures/board-gen/` holds three tiny part units, one requirement and one obligation each, 18 KB, which `gen_board.part_dirs` prefers to the repository's. **What freezing alone would have broken, read before it was made:** the real run answered `BOARD-GEN: ok (no board declares itself yet)` whenever no `board.sexp` was found, so once the controls stopped reading the real one, only that line would have stood between a deleted definition and a green gate: the BOOK-INDEX hole again. `composition.sexp` is only ever generated from a board, so a manifest with no `board.sexp` beside it now fails by name, and a tree with neither still reads as no board. Two new arms, 11 in all. **Measured** (`red-states.txt`, both binaries on the real tree, each state restored): the deleted `board.sexp` goes from `rc=2`, a missed control over a scratch path, to `rc=1`, `profiles/netboard-lab-v0/board.sexp: missing, though its generated composition.sexp is present`; a part's deleted `requirements.sexp` from the same miss to `rc=1`, each `DANGLING DEP` naming the unit and the requirement; a hand-edited `hardware.sexp` and a moved definition stay `rc=1` DRIFT; a damaged frozen part `rc=2`, the control refusing. Next slice: PLATFORM-GEN.
