# A case's reference configuration is the case's own: the pinned Sail implements Zicntr, and CSR-SET witnesses all 33 CSRs

- **Type:** `decision`
- **Date:** `2026-11-03`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43b-3a, `SEMULITH-P4-0333`; decided by the workflow under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) as a design choice the measurements decide; corrects the
  addendum of [`decision_state-capture-plan.md`](decision_state-capture-plan.md); answers the question
  [`decision_director-rulings-2026-10-28.md`](decision_director-rulings-2026-10-28.md) left open for ZICNTR with an option it did not list,
  **raised to the director, who may overrule**.
answers: Does the pinned reference really lack Zicntr, how does CSR-SET witness all 33 CSRs, and what does it cost?

## The fact

"The reference has no Zicntr" was a statement about our override, recorded as one about the reference. Measured on the pinned
binary, `sail_riscv_sim` 0.14, `16de42a8…`, through its public configuration only (evidence: target/p4-system-14/a43b-3a):

| Configuration | Result |
| --- | --- |
| The profile override (Zicntr off) | `csrrs x20, mcycle, x0` traps illegal-instruction (`DIVERGE step 34`) |
| Zicntr on | refused: "Zicntr is enabled but there is no source of time" |
| + CLINT, no region | refused: "The CLINT (platform.clint) for the platform is not in a defined memory region." |
| + a CLINT device region | accepted; `mcycle` reads 2 where the laboratory reads 4 (Sail counts ticks, `instructions_per_tick` 2) |
| + `instructions_per_tick` 1 | all five counters agree step for step |

Over the 171 guests, this variant against the profile override:

| Guests | Profile override → variant |
| --- | --- |
| 151 | AGREE → AGREE |
| 13 | no change: 8 DIVERGE, 4 REFUSED, 1 outside the comparison |
| `mm-counters` (52 steps), `mm-csr-ro-counters` (49), `c-irq` (19) | not agreeing → AGREE |
| `csr-set`, `w-sw` | AGREE → DIVERGE, both at a `mip` read |
| `w-deleg`, `w-timer` | between DIVERGE and REFUSED |

The `mip` loss is the one real difference: the reference's CLINT resets `mtimecmp` to 0, so `mip.MTIP` reads set, while the laboratory
declares no such device. So this is not a profile-wide change, and it is not free.

## The decision

1. **A case may carry its own reference configuration, as data.** `profiles/<profile>/reference/<case-id>.overlay.sexp` is applied over the
   mapped profile override by `scripts/prepare_div_inputs.py`, and the result is the case's prepared `reference-config.json`, pinned as
   every case's is. The profile override does not move.
2. **CSR-SET is declared on that configuration and witnesses all 33 CSRs**: 32 values, and `mip` by presence (`rd` = x0, then a marker)
   with its value witnessed through the `sip` alias.
3. **The category row is judged.** The policy review's `matched-reference-comparison` leg measured `defined`'s row for every case. For
   `implementation-defined` it now requires the selection recorded in the catalogue and a behavior-changing control: a retained trace of
   the same guest under the profile override, first differing at a declared property's step. A category with no branch reads pending.
4. **ZICNTR and SSTC follow on the same route.** ZICNTR's program no longer waits for a re-pin.

## Why

- A credit for "the committed minimum of 33" resting on 28 would be `implemented` over five uncompared CSRs: the derivation would allow
  it, and a sign-off reviewer should not. The policy's own row asks for a "pinned matching reference configuration": one with Zicntr
  disabled does not match a profile that selects it.
- It costs no lapse. Measured over both current manifests: `prepare_div_inputs.py` is pinned by neither, the override by neither, and
  `dossier_sexp.py` by both — so the closed mapping stays as it is and the overlay is applied in the unpinned tool. CR-GC-M-3 and
  CR-D-XLEN-2 stay current.
- It is the same reference identity: one binary and one trace vocabulary, so nothing here adds a producer or claims independence.

## How to apply

- The overlay is small and reviewed, like an override: it enables what the case needs and says why. A new configuration is a new case's
  file, never an edit of a retained case's.
- A `mip` read into a GPR diverges under this configuration. Read `mip` with `rd` = x0 and witness its bits through `sip`.
- The time-source overlay brings a device the laboratory does not declare. Do not read a passing case as a claim about a CLINT: name the
  device in the case's limitations.
- Check a recorded reference limit against the binary's public configuration before planning around it: a limit measured under one
  configuration is that configuration's.
