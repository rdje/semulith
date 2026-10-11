# DEV_NOTES shard — _(2026-10-11)_ … _(2026-10-11)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-11)_ — normalize shared-reader refusals (P4-SYSTEM.14 a35)

D35-REFUSALS: public parse leaked ValueError for5000-digit decimal and0x_/0b_;
CLI also leaked empty/nested-list head SexpError and missing/decode exceptions.
Before diagnostic records all seven escapes. Normalize only integer conversion
ValueError to source/line/base/length SexpError; no whole-token echo or host-limit
change. Preserve valid integer/symbol values, two-argument _atom consumers and
library read_file I/O contract. CLI computes its head summary inside the expected
SexpError/OSError/UnicodeError refusal boundary; success and usage stay stable.

D35-HEAD-DIAGNOSTIC: valid5000-digit hexadecimal head parses, then full-form repr
leaks decimal-display ValueError. Replace error rendering with bounded type/shape;
valid head/accessor semantics stay exact. D35-OPT-CREDIT: exact old self-test with
parsed12 replaced13 reports17/1 rc1 normally but18/0 rc0 optimized. Replace four
removable asserts in one/refuses/_eq/_raises with explicit checks. Wrong-value,
extra-form and wrong-reason controls exercise the actual legacy test in both modes.

29 controls pass normal/O; eight omissions6/3/3/3/2/2/1/2 fail without errors.
SOURCE-FORMAT25/0 registers18 literal outer arms:39 doctrines/1011 arms.
Normalize the span test's expected conversion escape to a failure before counting
omissions. Host-disabled before probe skipped a case and changed omission6→5: scope/restore
one real decimal-limit fixture in finally; default/disabled normal/O stay29/0/0
with no skips and identical omission counts. Production limits never change.
New GC examples teach parser/CLI/library and byte-budget boundaries;
main lesson links the built HTML route, after the fresh gate rejects an unsupported
main-to-model source route. No navigation contract or architecture change.

D35-HISTORY-EDIT: whole-file new-note23/0→25/0 replacement also changed two old
a24 gate receipts. Public predecessor guard refused. Restore complete entries
from HEAD and limit all subsequent updates to the new entry. Full inverse and
actual original/moved/published receipt edits with updated digests must refuse;
never accept corrected-history counts. DECLINED new decision promotion: existing
refusal/assertion-safe/history contracts own these repairs; task/toolbox/book
retain the commands and lessons.

DEV measured51367B; public sharder moves two whole3141B entries into0245,
22=20+2, immediate head48226B; shard3374B/
d6783a698a7554a60f0f9fc2eaa5492d165dacecead2f891d83f7b7de78d6f73.
37live+210sealed=247logical. Preserve340 raw parses/types,243 dictionaries,
1311 other files,101 prior entries and whole reader/checker/method/task/teaching.
Focused17/sharder12/0/seven books/3076 links/all6 literal blocks and real CLI20
cases pass; final exact-source/hooks/brief0/censuses required. Fixed caps/seals/
canonical/qualification/CPU unchanged. Full CI follows the clean repair commit,
then a36 bounded leaf inspection and aggregate evaluator/collector/captures.


