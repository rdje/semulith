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

## Addendum (2026-10-29, `P4-SYSTEM.14` a44-3): the third case — the M case re-captured as v4

By ruling 1 (`decision_case-declarations-as-data.md`) the M case is re-captured once under the declaration-as-data
manifest, as `rv64gc-m-forms-v4`: a third case directory, the third re-derivation this record's rule reserves. Neither
earlier case is removed — both are `invalidated` history, never rerun or replaced. Measured: a case holds at most
13,828,096 B (three 4 MiB traces, nine 64 KiB streams and receipts, ten 64 KiB prepared and metadata slots), so three
cases and the 4 KiB index hold at most 41,488,384 B (`retention_limits()` sums exactly that), above the 32 MiB
ceiling. The bounds move to **67** files (3 × 22 + the index; health **64**, three below) and **50,331,648** B (48 MiB;
health **44,040,192** B, 42 MiB, the same 0.875 ratio); the 4 MiB part bound is unchanged. At declaration the family
holds 53 files (v4's eight declared ones), 67 after its capture. `evidence/README.md` keeps its 4,096 B / 80-line cap:
its text was compressed to hold the third row (3,383 B). A fourth case is a fourth re-derivation.

## Addendum (2026-10-29, `P4-SYSTEM.14` a43a-2b): the fourth case — XLEN, the first non-M case

`rv64gc-xlen-forms-v1` (REQ-D-XLEN, on RVI-RV64I's own authority) is the fourth case directory and the fourth
re-derivation: **89** files (4 × 22 + the index; health **86**) and **67,108,864** B (64 MiB; health **58,720,256** B,
56 MiB, the 0.875 ratio); four cases and the index hold at most 55,316,480 B (`retention_limits()`). At declaration the
family holds 72 files (the XLEN case's case file and four prepared inputs). The index stays under its 4,096 B cap.


## Addendum (2026-11-02, `P4-SYSTEM.14` a43b-2c): the fifth and sixth cases — v5 and xlen-v2

The planned lapse that opens CSR-SET re-captures the M and XLEN cases once each
([`decision_producer-debt-paid-before-the-next-case.md`](decision_producer-debt-paid-before-the-next-case.md)), so two
case directories are declared together, `rv64gc-m-forms-v5` and `rv64gc-xlen-forms-v2`: the fifth re-derivation,
covering both. No earlier case is removed — v2, v3, v4 and xlen-v1 stay `invalidated` history. Measured: a case still
holds at most 13,828,096 B, so six cases and the index hold at most 82,972,672 B (`retention_limits()`), above the
64 MiB ceiling. The bounds move to **133** files (6 × 22 + the index; health **130**, three below) and **83,886,080** B
(80 MiB; health **73,400,320** B, 70 MiB, the 0.875 ratio); the 4 MiB part bound is unchanged. At declaration the family
holds 105 files (each new case's case file, four prepared inputs and three declarations), 133 after both captures.
`evidence/README.md` was compressed to hold the two rows (3,795 B of its 4,096 B cap). A seventh case is a sixth
re-derivation.

## Addendum (2026-11-03, `P4-SYSTEM.14` a43b-3d): the seventh case — CSR-SET

`rv64gc-csr-set-v1` is REQ-D-CSR-SET's case, the sixth re-derivation. No earlier case is removed. Measured: a case still holds at most
13,828,096 B, so seven cases and the index hold at most 96,800,768 B (`retention_limits()`), above the 80 MiB ceiling. The bounds move to **155**
files (7 × 22 + the index; health **152**, three below) and **100,663,296** B (96 MiB; health **88,080,384** B, 84 MiB, the 0.875 ratio); the
4 MiB part bound is unchanged. The family holds 138 files with the case file and four prepared inputs, 141 at its declarations (a43b-3e), 155 after its capture. An eighth case
is a seventh re-derivation.

## Addendum (2026-11-04, `P4-SYSTEM.14` a43c-2): the eighth case — ZICNTR

`rv64gc-zicntr-v1` is REQ-D-ZICNTR's case, the seventh re-derivation. No earlier case is removed. Measured: a case still holds at most 13,828,096 B, so eight cases and the index hold at most
110,628,864 B (`retention_limits()`), above the 96 MiB ceiling. The bounds move to **177** files (8 × 22 + the index; health **174**, three below) and **117,440,512** B (112 MiB; health **102,760,448** B, 98 MiB, the 0.875 ratio); the
4 MiB part bound is unchanged. At declaration the family holds 160 files (the case file and four prepared inputs), 177 after its capture. A ninth case, SSTC's, is an eighth re-derivation.
