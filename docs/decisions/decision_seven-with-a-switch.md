# The seven with a real switch, declared, and what writing them found

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a50-2, `SEMULITH-P4-0373`; the step [`decision_obligations-route.md`](decision_obligations-route.md) scheduled after the `defined` remainder, on the tool of [`decision_declared-alternative-configuration.md`](decision_declared-alternative-configuration.md); a call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: What does each of the seven `implementation-defined` cases witness and leave out, what selects otherwise for each, what did writing them find, and what happens to the pinned override?

## The fact / decision

| Case | Program | Steps | Witnesses | Control | Selects otherwise | First difference |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-svade-v1` | `svade-forms.s` | 137 | 15 | a PTE with A set | its alternative: `Svade` off | step 93, `scause` |
| `rv64gc-atomic-misalign-v1` | `atomic-misalign.s` | 180 | 26 | the misaligned cause | its alternative: LR/SC and AMO `AlignmentException` | step 24, `mcause` 4, expected 5 |
| `rv64gc-fault-priority-v1` | `fault-priority.s` | 271 | 37 | misaligned judged low | its alternative: `load_store None` | step 159, `scause` 13, expected 4 |
| `rv64gc-priv-modes-v1` | `priv-modes.s` | 109 | 15 | `misa` with S clear | its alternative: `S`, `Sv39`, `Svade`, `Sstc` off | step 5, `misa` |
| `rv64gc-sv39-v1` | `sv39-modes.s` | 135 | 11 | `satp` taking Sv48 | its alternative: `Sv48` on | step 17, `satp` |
| `rv64gc-reservation-v1` | `reservation-forms.s` | 190 | 24 | an eight-byte set | the profile override | step 23, the SC beside the LR |
| `rv64gc-sc-deterministic-v1` | `sc-deterministic.s` | 159 | 21 | an SC past its address | the profile override | step 21, the SC beside the LR |

Each program was written for its statement, clause by clause, because a guest already in the corpus either carried no source per step or held only part of a statement. All three producers agree: the spec-side author, the lab engine (`every_guest_matches_its_expectations`, 198 guests) and the pinned Sail on the case's configuration. Nothing is captured or credited at this unit.

**Rehearsed before declaring,** on a throwaway clone of the staged tree (`target/p4-system-14/a50-2/rehearse.txt`): seven captured in 10 s, each baseline and repeat AGREE, each control DIVERGE at its witness, each effect retained, and each case reading 11 of 11 legs.

## What writing them found

1. **The pinned override does not judge a misaligned AMO before translation.** The statement says it is judged before translation, and the lab does so. Under the override the pinned binary raises the store page fault, 15, for a misaligned AMO on an invalid page, where the lab raises 7. The override sets only `memory.misaligned.exceptions.load_store`, and the binary's default for `amo` is no check before translation; the region's `amo AccessFault` is read after it. No guest had that cell: of the 190 guests compared before these seven, 0 moved when the setting changed.
2. **The lab and the statement are right, and the configuration was incomplete.** The specification allows either order: "Load/store/AMO address-misaligned exceptions may have either higher or lower priority". The profile chose high, so a reference matching the profile must select it too. `misaligned_amo AccessFault` does, and both cases that need it carry it in an overlay.
3. **The override does not move now.** Moving it would move every case's pinned configuration and lapse all 23 credits, for one setting no credited case observes: the credited `atomics-forms` and every other guest read the same under both. It rides with the next pinned edit a window needs anyway, and it is recorded here so that window takes it. This is the same rule as [`decision_dossier-copies-retire-at-the-next-window.md`](decision_dossier-copies-retire-at-the-next-window.md).
4. **An exact reservation is available, so it is selected.** `REQ-D-RESERVATION` says the reservation covers exactly the LR's word. The binary's default set is eight bytes, so an SC to the word beside the LR pairs. `require_exact_reservation_addr` makes the reference agree, so "covering exactly" is witnessed instead of named as a limit, and the override becomes what selects otherwise, at a witness.
5. **Exact width is past the reference.** With the exact address selected, the binary still pairs `lr.w` with `sc.d` and `lr.d` with `sc.w` at the same address (`target/p4-system-14/a50-2/width.py`), where the lab writes 1. That is the difference `decision_obligations-route.md` named as a selection. Both cases state it as a limit, and neither compares it.
6. **An alternative's first difference has to land on a witness, and that shaped two programs.** A fault boundary writes nothing, so no witness can sit on it. So `svade-forms` makes its first A-clear load `ld x0`, and under the other scheme the difference appears at the handler's read of `scause`, which is witnessed. `sv39-modes` writes Sv39 back after the refused Sv48 write, so the alternative's run stays in a translation it can finish.
7. **The binary stopped a run at its eleventh trap with no xRET between them** ("possible trap loop detected", exit 1), and with S's handler returning by `sret` it ran through. A `--disable-trap-loop-detection` exists; it was not used, because it would change what the capture runs.

## How to apply

- **The two reservation cases and the two AMO cases carry overlays with no device.** `schema/overlay.sexp` now allows that, and refuses an overlay that changes nothing. The four existing overlays render byte-identically: `prepare_div_inputs.py --verify` `rc=0` each.
- **The next window takes the override's AMO setting.** When it does, `atomic-misalign` and `fault-priority` need no overlay for it, and the existing cases' traces should not move: 0 of the 190 guests compared before these seven moved under the setting (`target/p4-system-14/a50-0/more2.txt`).
- **Four guests now read DIVERGE under the bare override**, by design: those four cases' own configurations are what they run on. A census of the override alone reads 19 and not 15 for that reason.
