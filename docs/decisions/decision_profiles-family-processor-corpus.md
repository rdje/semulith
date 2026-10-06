# The `profiles/` aggregate bound re-derived for the processor's evidence corpus — a unit's directed corpus, not the unit count, drives the family now

- **Type:** `decision`
- **Date:** `2026-10-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.11` slice (b) — the M bind lands four guests (30,889 B) and
  the family crosses its aggregate ceiling. The family's recorded policy: *"the bound scales
  with the measured unit count, never ahead of it"*
  ([`decision_profiles-family-five-units.md`](decision_profiles-family-five-units.md)), and
  its rule for a raise under pressure: reviewed, with its numbers, never silent.

## What changed

The aggregate byte bound bites — and for the first time the cause is **not** a new unit.
Measured with `git ls-tree -r -l`:

| When | Files | Bytes | Against the 5× bound (2,867,200 B) |
| --- | --- | --- | --- |
| the 5× bound set (`3071ae8`, 2026-10-02) | 160 | 845,819 | 0.29× |
| `HEAD` before the M bind (`b943d35`, 2026-10-06) | 455 | 2,850,535 | 0.994× (health target 2,450,000 already passed) |
| with the M bind staged | 463 | 2,885,149 | **1.006× — over** |

The growth is one unit's: `profiles/rv64gc-lab-v0/` is 1,796,305 B (293 files), of which its
guest corpus is 1,516,594 B — 139 guests whose expectations (1,186,518 B) carry, per step,
the value derived spec-side and the derivation and locator it came from (EVD-05). The other
five directories total 1,088,844 B. The unit-count arithmetic assumed units of comparable
size; measured, they span 64,028 B (`dsp56300-lab-v0`) to 1,796,305 B, and the processor's
corpus grows **by design** with every extension the profile binds — each leaf of
`P4-SYSTEM` adds the directed evidence the processor gate's G-REGRESSION axis requires.

## The re-derived bound

- `ceiling_bytes`: 2,867,200 → **3,145,728** (3 MiB) — 0.917× with the M bind landed; the
  headroom (260,579 B) is about eight corpus slices of the M bind's size — the remaining
  binds and realizations of `P4-SYSTEM.12`–`.13`, measured, not guessed.
- `health_bytes`: 2,450,000 → **2,690,000** — the standing health/ceiling ratio (~0.855).
  The family stays ABOVE it, deliberately: the health warning keeps firing until the
  structural fix below lands, so the pressure stays visible.
- Unchanged: `ceiling_lines` 600 / `health_lines` 590 (463 files), `ceiling_part_bytes` 65,536.

## Why a raise under pressure is honest here — and why it is not the fix

The content is measured, and its size is the house's own discipline: a directed corpus whose
every expected value carries its derivation and locator, re-derived spec-side before any
engine runs. The only way to shrink it is to evidence less. But the unit-count rule no longer
models the family: one processor unit holds 62% of it, and its corpus will keep growing until
the CPU-SYSTEM gate passes. **The structural fix** is to govern the evidence corpora as their
own family — `profiles/*/guests/` with a per-guest part bound and a corpus-size ceiling
derived from the profile's scope — and to take them out of the dossier aggregate. That
changes the routing doctrine (a nested route is not subtracted from its parent today), so it
is proposed, not done here. The next re-derivation of this bound is due when the corpus
reaches the health ceiling again, or when that fix lands — reviewed, never silent.
