# The `profiles/` family bound re-derived for five units — the second device dossier lands, and the per-part bound bites for the first time

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.10` stages the fifth unit directory
  (`profiles/lan9118-lab-v0/` — the second *device* dossier). The family's recorded
  policy: *"the bound scales with the measured unit count, never ahead of it"*
  ([`decision_profiles-family-four-units.md`](decision_profiles-family-four-units.md),
  which named this re-derivation before execution). The `.10` design brief
  (`docs/tasks/P5-BOARD.md`, Decisions, `2026-10-02`) recorded it as part of the leaf's
  mechanical re-pins.

## What changed

Two things, one of each kind:

1. **The unit count: 4 → 5.** Measured at staging: **160 files / 845,819 B** tracked
   under `profiles/` (147 prior + 13 `lan9118-lab-v0`: the dossier's six documents plus
   three expectation files… `DOSSIER.md`, `sources.sexp`, `requirements.sexp`,
   `contract-obligations.sexp`, `state.sexp`, `profile.sexp`, and
   `expectations/` × 3 — 13 files, ~209 KiB) against the 4× bound of 480 files /
   2,293,760 B. Nothing approached the aggregate bounds (0.33× files, 0.37× bytes); the
   contract expansion is the family's designed growth — a second device beside the first.
2. **The per-part bound BITES — the first time.** `ceiling_part_bytes` was 32,768, and
   the NIC's mirrored-record catalogues exceed it: `contract-obligations.sexp` is
   **60,112 B**, `requirements.sexp` **59,022 B**, `profile.sexp` **40,113 B**. The cause
   is structural, not bloat: the RECORD-SCHEMA mirror discipline (one fact, three
   surfaces, one wording) makes a dossier's byte size proportional to its contract
   surface, and the LAN9118's surface — 52 mirrored records against the UART's 19 — is
   what a real Ethernet MAC+PHY carries. The four-units record's note ("the largest new
   member … is nowhere near it") no longer holds; the per-part must move.

## The re-derived bound

The same arithmetic as the three predecessors for the aggregates; a reviewed raise for
the per-part:

- `ceiling_lines`: 480 → **600** (5 × 120)
- `health_lines`: 472 → **590** (the standing health/ceiling ratio, 0.983)
- `ceiling_bytes`: 2,293,760 → **2,867,200** (5 × 573,440)
- `health_bytes`: 1,960,000 → **2,450,000** (the standing ratio, ~0.854)
- `ceiling_part_bytes`: 32,768 → **65,536** — a doubling, the family's first per-part
  raise. The largest member (`contract-obligations.sexp`, 60,112 B) sits at **0.92×** of
  it. The thinner-than-usual margin is recorded deliberately: dossier catalogues do not
  grow in place (a unit's records change only with its contract), and the next unit's
  landing re-derives the bound again by the standing rule — if a future device's
  catalogue approaches 64 KiB, that re-derivation is where the raise belongs, reviewed,
  never silent.

## Why a raise under pressure is honest here

The gate's rule is *"never raise one to land content"* — and this raise is exactly the
reviewed alternative to it: the content is measured, its size is explained by the mirror
discipline the house itself mandates (the only way to shrink the files is to mirror fewer
facts — a smaller dossier, not a leaner one), and the raise is recorded as a decision with
its numbers rather than smuggled past the ceiling. The aggregate bounds follow the unit
count as before; the per-part follows the measured largest member with the margin stated
in the open. The next re-derivation (6×) waits for the next measured unit — never ahead
of it.
