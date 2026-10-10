# My search returned zero hits — is that absence, or is my instrument blind?

A zero needs a measured search scope and a positive control. It can support
absence within the observable domain only after the instrument has demonstrated
that it can detect the kind of hit being sought. A successful query over the
wrong domain is still a non-answer.

## The corrected reference example

The earlier story used binary string/symbol searches, then an internal source
census, to conclude that Sail and Spike shared an FP implementation. That
implementation-lineage conclusion and the advice to clone/read dependency
internals are withdrawn. The complete original card is preserved in
`docs/tasks/archive/P4-SYSTEM-reference-a6.md` (`zero-hits`).

A symbol count alone does not establish which implementation facts a binary
exposes. An absent name cannot rule out a shared ancestor; many available names
also do not guarantee complete semantic coverage. Use authorized public
contracts or artifacts with positive and negative controls. If those cannot
answer the lineage question, record it as unexamined and limit the claim.

## Check reach before interpreting zero

| Observation | Necessary companion |
| --- | --- |
| A text search returns no hits | Name the exact files searched and a known-present hit the same search detects. |
| An API query returns no rows | Establish authentication, scope and a known-present result. |
| A suite reports zero failures | Report how many tests actually ran and a deliberate failing control. |
| A gate reports no findings | Show that its enumerated set includes the intended files. |

Report the denominator with the numerator. The denominator describes reach;
it does not by itself prove the instrument can detect the relevant defect.
Respect repository and dependency boundaries when choosing another instrument.

Related: [[self-test-arms-that-never-ran]], [[availability-is-not-identity]],
[[a-shorter-trace-is-not-agreement]].

## Measured again — a green gate over a set that lacked the new files (2026-10-06)

P4-SYSTEM.7 slice (c6) added 22 untracked corpus files. `make gate` ran green twice with them
present but unstaged; the commit's pre-commit run, after `git add`, refused one
(`f-sgnj.expected.sexp`: an empty `derivation` — the authored comment began `|sNaN|:`, and `|`
is the directive's derivation/source separator). DOSSIER-SCHEMA enumerates with
`git ls-files -- 'profiles/*/*.sexp'` (`scripts/check_dossier_schema.sh:44`), and its verdict
prints the denominator: **202** documents judged while the files were untracked, **213** once
staged (`git ls-files … | wc -l`: 204 → 215, 2 skipped). The green runs were green over a set
that did not contain the defect — the same rule, one level up: read the count next to "ok".
A tracked-only sweep is right for a commit gate (it judges what will be committed); stage, or
`git add -N`, new files before the run you intend to cite (probed: an untracked file is absent
from `git ls-files`, an intent-to-add one is listed).
