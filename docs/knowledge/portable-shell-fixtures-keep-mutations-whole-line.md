# Portable shell fixtures keep mutations whole-line

A gate's self-test fixture is built twice: once by the author, and once per mutation arm. If
the arms use `sed`/`grep` to remove or edit a field, the fixture must be shaped so every
mutation is a WHOLE-LINE operation — one field per line, and every closing paren on its own
line, never riding on a field's line.

## Why this is a rule

Three failures from one session (`SOT-FORMAT.4`, re-firing `PROFILE-CONSISTENCY`'s arms on
converted fixtures), each a different face of the same shape mistake:

1. **A field line that also closes its form.** `grep -v 'matched_scope'` removed the line that
   carried the candidate's close paren, and the fixture went unbalanced — the arm under test
   never ran, and the gate reported "unparseable" for the wrong reason entirely.
2. **`sed` multiline replacements are not portable.** BSD sed (macOS) refuses a replacement
   containing a literal newline — `unterminated 's' command` — while GNU sed (Linux, CI)
   accepts it. Code written against one fails on the other, so multiline `sed` is a
   dependency on whichever sed you happened to test with. (`gsed` existing on the author's
   machine does not help: CI does not have it.)
3. **`${var/pat/repl}` with quotes in the pattern terminates early.** The inner `"` closes the
   outer double-quoted expansion; the pattern that actually matches is a truncated prefix, the
   replacement silently does nothing, and the arm tests the unmutated fixture.

The fix in every case was the same: make the fixture one-field-per-line with closes on their
own lines, and use only `grep -v <field-line>`, `sed 's/(field old)/(field new)/'`, and
`sed '$i\…'` (insert before the closing line). Those work identically under BSD and GNU sed.

## The underlying principle

A mutation arm and the defect it simulates must fail for the SAME reason. When the mutation
mechanism can also break the fixture's syntax, a red arm no longer discriminates "the gate
caught the defect" from "the author broke the fixture" — and a gate whose RED arms can mean
either is not known to work.
