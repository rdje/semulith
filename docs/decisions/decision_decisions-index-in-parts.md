# The decisions index continues in parts: INDEX.md names each, and every record is listed exactly once

- **Type:** `decision`
- **Date:** `2026-11-14`
- **Status:** `active`
- **Owner / source:** `LIVE-CONTAINMENT.6`, `SEMULITH-LC-0057` (evidence target/live-containment/lc0057). Found by `P4-SYSTEM.20` slice f's brief (`SEMULITH-P4-0413`), whose one new row took `docs/decisions/INDEX.md` over the family's per-part ceiling. The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Where does a new decision record's index row go now that one file cannot list them all, and what keeps every record listed exactly once?

## What was measured

At `34fe03a0`, `docs/decisions/INDEX.md` held 134 rows in 32,745 B: 372 B of heading and introduction, the rows averaging 242 B. The family's per-part ceiling is 32,768 B (`doctrine/readme_routes.tsv`, row `docs/decisions/`), so 23 B remained and the next record's row would refuse the routes check. Every record must have a row (MEMORY-ARCH), so the index grows with the family and no ceiling holds it for long. The family itself stood at 136 files of its 160-file ceiling and 672,974 B of its 1,048,576 B aggregate.

## The decision

1. **The index is `INDEX.md` and its parts under `docs/decisions/index/`.** `INDEX.md` keeps its introduction and its first 67 rows. Part 2 (`index/part-2.md`) holds rows 68 to 134 in their order, each byte-identical except that its record link leads one level up (`../<file>`).
2. **A new record's row goes at the end of the last part.** A part that would cross the per-part ceiling is followed by the next (`index/part-3.md`), and `INDEX.md` names it. No ceiling moves.
3. **MEMORY-ARCH reads `INDEX.md` and every part.** A record listed in no part fails, as before. A record listed twice, in one file or across two, now fails too: two rows are two hooks that can disagree. A part that `INDEX.md` does not name fails, since no reader would be sent to it. A part that is a symbolic link is refused.

## Why this shape

- **A subdirectory, not an `INDEX-2.md` beside the records.** MEMORY-ARCH's record census and the Knowledge Map's inventory both read `docs/decisions/*.md`, minus `INDEX.md` and `TEMPLATE.md`, as the records. A part beside them would read as a record in both.
- **Live parts, not frozen shards like the changelog's.** A row changes when its record does: a status turns `closed` or `superseded`, or a hook is corrected. Every part stays editable.
- **Not a raised per-part ceiling.** 32,768 B bounds one member of the family. An index that lists every record grows without limit, and raising the bound would only postpone the next refusal. Parts keep every member bounded.
- **Halves.** After the move each file sits near half the ceiling, so editing a row in `INDEX.md` never refuses, and part 2 has room for about 70 more rows.

## Room after the move

`INDEX.md` 17,996 B (0.55× of the per-part ceiling); `index/part-2.md` with this record's row, about 15.8 KB (0.48×), room for about 70 rows at the measured 242 B each. The family's file count bites first: 138 files after this unit, so 22 more records reach the 160-file ceiling. That firing will be a new measurement and a new record.

## How to apply

- **New record:** copy `TEMPLATE.md`, fill it in, and add its row at the end of the last part `INDEX.md` names, linking `../<file>`.
- **When the last part nears 32,768 B:** open the next part and name it in `INDEX.md`'s introduction. MEMORY-ARCH reads every file under `docs/decisions/index/` and fails on any that `INDEX.md` leaves out.
- **Readers:** `cat docs/decisions/INDEX.md docs/decisions/index/*.md` shows the whole index.
