# The `evidence/` family re-derived for two declared cases — one directory per reviewed finite case

- **Type:** `decision`
- **Date:** `2026-10-22`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42au, `SEMULITH-P4-0289` — the declaration of the m-forms case
  `rv64gc-m-forms-v3` beside the retained `rv64gc-signed-div-truncation-v2`. The family's bounds were set
  by a42af (2026-10-14) for exactly one case: `evidence/README.md` said "Preparation grants no permission
  to grow the family to another case", and the registry row read 22 files / 16 MiB, health 20 / 14 MiB.
  Precedent and the rule for a raise under pressure:
  [`decision_profiles-family-corpus-second-rederivation.md`](decision_profiles-family-corpus-second-rederivation.md)
  — reviewed, with its numbers, never silent.
answers: Why does the evidence family hold two case directories, and what bounds govern it now?

## What was measured

| When | Files | Bytes | Against 22 files / 16,777,216 B |
| --- | --- | --- | --- |
| `830bdce` (2026-10-22), before a42au | 22 | 99,878 | 1.000× of the file ceiling, 0.006× of the bytes |
| a42au staged: `rv64gc-m-forms-v3/` declared (4 prepared inputs + 3 declarations), the index rewritten | 29 | 176,314 | **1.318× — over** the file ceiling |
| both cases captured (the a42av layout: 2 × 21 slots + the index) | 43 | ≤ 27,529,216 | 1.955× / 1.641× |

Measured with `git ls-tree -r -l HEAD evidence/` and the working-tree sizes of the seven new files
(4,440 + 7,609 + 7,937 + 7,440 + 16,915 + 14,488 + 17,043 B = 75,872 B) and the rewritten index (3,762 B). The file ceiling fires on the first
declaration, as it should: the one-case envelope was exact (22 of 22) by design, and a second case is
exactly the growth the a42af wording reserved for a decision.

## The decision

The policy's crediting capture (a42aq: predeclare every Table 1 row and every M form) is a second case,
and an invalidated case is superseded, never rerun or replaced (`evidence/README.md`; the retained bytes
are an immutable terminal). So the family grows by one directory per reviewed finite case, each with the
same 21 declared slots, and the index names every member in a literal table.

| Axis | Was | Now | At staging |
| --- | --- | --- | --- |
| `ceiling_lines` (file count) | 22 | **43** = 2 × 21 slots + the index | 29: 0.674× |
| `health_lines` | 20 | **40** | below: the line fires once more before the ceiling |
| `ceiling_bytes` (aggregate) | 16,777,216 (16 MiB) | **33,554,432** (32 MiB) | 176,314: 0.005× |
| `health_bytes` | 14,680,064 (14 MiB) | **29,360,128** (28 MiB) | the same 0.875 ratio of its ceiling as before |
| `ceiling_part_bytes` | 4,194,304 | **4,194,304** | unchanged: a trace is at most 4 MiB |
| `evidence/README.md` | 64 lines / 3,072 B health, 80 / 4,096 ceiling | 64 / **3,890** health, 80 / 4,096 ceiling | 53 lines / 3,762 B: the hot-live target sits just above the reviewed size |

The maximum a case can hold is 13,762,560 B (three 4 MiB traces, nine 64 KiB streams and receipts, nine
64 KiB prepared and metadata slots); two cases and the 4 KiB index are at most 27,529,216 B, below 28 MiB.
The byte ceiling keeps the one-case headroom ratio rather than tracking the bytes actually used, because
the traces arrive in one capture, not by accretion.

## Why not the alternatives

- Replacing the v2 directory with v3 would delete retained observations; the policy supersedes an
  invalidated case, it does not erase it, and the captured bytes are the only record of what the
  reference did on 2026-10-19.
- Leaving the ceiling at 22 and declaring v3 outside `evidence/` would put a case's declarations in an
  unbounded neighbour, which is the routing failure the registry exists to refuse.
- Ungoverning the aggregate (the director's reading for the task family) is one row away and applies on
  the director's word only; this record does not extend it.

## How to apply

- A third case is a third re-derivation: the ceiling moves by 21 files per case, by a reviewed record in
  the leaf that declares it, and the index table gains one row.
- `scripts/probe_div_capture_inputs.py` holds the census (every member of every declared case, 43 files,
  32 MiB) and refuses an undeclared sibling or an undeclared member.
- The `evidence/README.md` health target moves with each reviewed rewrite; its 4 KiB / 80-line ceiling does
  not.

## Addendum (2026-10-28, `P4-SYSTEM.14` a44-2a): the case declaration joins each case

Each case gains one slot, `case.sexp` — its declaration as data (`decision_case-declarations-as-data.md`), read by
`scripts/matched_gpr_case.py` and reserved 64 KiB like the other metadata slots. By this record's own rule the file
ceiling is 2 × 22 slots + the index = **45** and the health line stays three below it, **42**; the byte bounds are
unchanged (the declared limits sum to 27,660,288 B, under 32 MiB). The input probe's `FAMILY_FILES`, its summed
limits and its member census move with it; `evidence/README.md` stays under its 4,096 B cap. A third case (the M
case's v4 capture) is the next re-derivation.
