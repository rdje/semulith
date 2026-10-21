# The `profiles/` bounds re-derived a second time for the corpus — the ceiling fired before the health line could

- **Type:** `decision`
- **Date:** `2026-10-21`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42ar, `SEMULITH-P4-0286` — the crediting M corpus program
  (`profiles/rv64gc-lab-v0/guests/m-forms.s` and its expectation file, 11,849 B) puts the family
  8,516 B over its aggregate ceiling: `bash scripts/check_readme_routes.sh` prints
  `OVER CEILING profiles/: 3154244 aggregate bytes > 3145728`
  (`target/p4-system-14/a42ar/routes-red.log`). Precedent and the rule for a raise under
  pressure: [`decision_profiles-family-processor-corpus.md`](decision_profiles-family-processor-corpus.md)
  (2026-10-06) — reviewed, with its numbers, never silent; its own words scheduled this
  re-derivation "when the corpus reaches the health ceiling again, or when that fix lands".
answers: Why did the profiles/ aggregate ceiling fire before its health target, and what bounds hold now?

## What was measured

Measured with `git ls-tree -r -l` on `profiles/`, the registry's aggregate:

| When | Files | Bytes | Against 3,145,728 B |
| --- | --- | --- | --- |
| the 3 MiB bound set, M bind landed (2026-10-06) | 463 | 2,885,149 | 0.917× |
| `8676d88` (2026-10-09), the remaining binds of `.12`–`.13` landed | 521 | 3,133,371 | 0.996× |
| `b469800` (2026-10-21), HEAD before a42ar | 524 | 3,142,395 | 0.999× |
| a42ar staged (`m-forms.s` + `m-forms.expected.sexp`) | 526 | 3,154,244 | **1.003× — over** |

At staging `profiles/rv64gc-lab-v0/` is 356 files / 2,063,462 B, of which the guest corpus is
337 files / 1,714,049 B; the other five units total 170 files / 1,090,782 B. The headroom the
2026-10-06 record named as "about eight corpus slices" (260,579 B) was spent in three days: the
binds that followed added 248,222 B by 2026-10-09. From there to `b469800` the family grew
9,024 B in twelve days, because `P4-SYSTEM.14` is evidence-method work, not binding. The corpus
grows in bursts tied to binds, not at a rate a calendar can carry.

## Why the ceiling fired without a warning

The 2026-10-06 record set `health_bytes` to 2,690,000 with the family already above it, "so the
pressure stays visible". A health target the family is above cannot fire again: its line had been
printed on every run since, and the next event the gate could report was the ceiling itself, inside
an evidence unit's commit, on the first new guest. The second axis was about to do the same:
`ceiling_lines` 600 was still the unit-count arithmetic (5 × 120) that the same record said no
longer models the family, and at 526 files (0.877×) its 74 remaining files are 37 guest pairs.

## The re-derived bounds

| Axis | Was | Now | At staging |
| --- | --- | --- | --- |
| `ceiling_bytes` | 3,145,728 (3 MiB) | **4,194,304** (4 MiB) | 0.752×; headroom 1,040,060 B — 87 program pairs of a42ar's size, or 33 binds of the M bind's |
| `health_bytes` | 2,690,000 | **3,586,000** | 0.880× of it: below, so the line fires once, with 432 KB of corpus still to go before the ceiling |
| `ceiling_lines` | 600 | **800** | 0.658× |
| `health_lines` | 590 | **684** | 0.769× of it |
| `ceiling_part_bytes` | 65,536 | **65,536** | unchanged; two-tier, derived members exempt ([`decision_derived-members-of-bounded-families.md`](decision_derived-members-of-bounded-families.md)) |

The health targets sit at the standing 0.855 ratio of their ceilings and the family is below both,
which is what makes them a warning again.

## Why re-derive, and what the director may still choose

- The registry's rule is that a ceiling moves only by a reviewed decision in a task leaf, and the
  2026-10-06 precedent was exactly that, owned by the leaf whose bind caused the crossing. This
  record is the same mechanism, applied by the leaf whose program caused it.
- The director's ruling of 2026-10-21
  ([`decision_containment-reset.md`](decision_containment-reset.md)) ungoverned the task family's
  aggregate because an aggregate over designed growth measures only how much the project carries,
  and it said "nothing else about the gate changes". The same reasoning fits a directed corpus whose
  every member is regeneration-gated and whose size is the house's own discipline, but the ruling
  named its surfaces, so this record does not extend it. The alternative stands one row away:
  `ceiling_lines` and `ceiling_bytes` 0 for `profiles/`, per-part 65,536 kept — the task family's
  shape. The director's word applies it; the agent does not.
- The structural fix proposed on 2026-10-06 — the evidence corpora `profiles/*/guests/` as a
  registered family of their own, out of the dossier aggregate — stays proposed. It changes the
  routing doctrine (a nested route is not subtracted from its parent) and touches GUEST-GEN, the
  generator and the runners: a unit of its own.

## How to apply

- The next re-derivation is due when the health line fires (3,586,000 B or 684 files), raised
  before the ceiling by the leaf whose bind reaches it — or never, if the director ungoverns the
  aggregate or the corpus family lands.
- A health target is set below the measured value only when it is meant to fire now; left there, it
  is not a warning but a line in every log.
- Related: [[profiles-family-processor-corpus]], [[containment-reset]],
  [[derived-members-of-bounded-families]].
