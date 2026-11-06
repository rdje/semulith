# A case may declare what selects otherwise, and its effect is measured against that

- **Type:** `decision`
- **Date:** `2026-11-06`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a50-1, `SEMULITH-P4-0372`; the tool [`decision_obligations-route.md`](decision_obligations-route.md) scheduled for the seven `implementation-defined` requirements with a real switch, built on [`decision_reference-config-per-case.md`](decision_reference-config-per-case.md).
answers: How does a requirement whose selection is already the profile override show a behaviour-changing control, what may an alternative say, what did the pinned binary do with each switch, and what does this not prove?

## The fact / decision

1. **A case may declare an alternative.** `profiles/<profile>/reference/<case-id>.alternative.sexp` (`schema/alternative.sexp`) states, with its reason, the choice the profile did not make. `scripts/prepare_div_inputs.py` applies it over the case's own configuration, and `scripts/measure_config_effect.py` runs the same guest through the same binary under the result, once, retained. Without one, the tool compares with the profile override as it always has, and the eight retained effects' reads do not move.
2. **The review pins it.** `_config_effect` re-renders the alternative and holds the record's `alternative_config_sha256` to it, so an effect measured under anything else reads pending, by name. It carries no verdict: the first difference is re-derived from the raw trace on every read, and it must fall at a declared property's step. An alternative the tool refuses leaves the leg pending, by name.
3. **The vocabulary is closed, and each knob was measured.** `extension_off`, `extension_on`, `misaligned_load_store`, `misaligned_lrsc`, `misaligned_amo` (two more knobs left at a50-2, below). A switch that changes nothing refuses, as does an alternative with no switch at all, one that names another case, and any knob or value the schema does not list. A new knob is a schema change a reviewer sees.
4. **The alternative selects no capture.** A case's `reference-config.json`, the override and every other case stay as they were. `measure_config_effect.py`, the review, the schema and `prepare_div_inputs.py` are not among the files a case pins, so no credit lapses: 23 current before and after.

## What the pinned binary does, measured

`target/p4-system-14/a50-0/` ran the 190 guests that take part in the cross-model comparison under each candidate (`switches.txt`, `more.txt`, `more2.txt`), and `target/p4-system-14/a50-1/census-*.txt` repeated the seven chosen through the real tool.

| Requirement | Switch | Binary | Guests moved | First difference |
| --- | --- | --- | --- | --- |
| `SVADE` | `Svade` off | accepts | 1 | `sv39-svade` step 90: the load succeeds where a fault is declared |
| `FAULT-PRIORITY` | `misaligned_load_store None` | accepts | 1 | `prio-sv39` step 72: `mcause` 13, expected 4 |
| `ATOMIC-MISALIGN` | `misaligned_lrsc` and `misaligned_amo` `AlignmentException` | accepts | 1 | `a-lrsc-fault` step 11: `mcause` 4, expected 5 |
| `PRIV-MODES` | `S`, `Sv39`, `Svade`, `Sstc` off | accepts | 53 | `mm-ecall-modes` step 28: `mcause` 8, expected 9 |
| `SV39` | `Sv48` on | accepts | 0 | none yet: no guest witnesses a rejected mode |
| `RESERVATION` | `invalidate_on_same_hart_store` | accepts | 0 | none yet: no guest keeps a reservation across a store it then pairs |
| `SC-DETERMINISTIC` | `reservation_set_size_exp 4` | accepts | 0 among agreeing guests | `a-lrsc-mustfail` moves, from another divergence to step 11 |

Three things the route's first table could not show:

- **The binary refuses some switches alone.** `U`, `S`, or `Sv39` turned off singly is refused as an invalid configuration, and `Sv39` off with `Sv48` on too. So `PRIV-MODES` turns off the family together, and `SV39` selects otherwise by adding a mode, not by removing its own. That is why an alternative holds a set.
- **The region's own misaligned attribute changes nothing here.** With `memory.misaligned.exceptions` set, `load_store` under the region's attributes moved 0 guests. Only the global check moves them, so the vocabulary names that one.
- **Two agreeing corpora say nothing about two switches.** Zero guests moved under `Sv48` and under `invalidate_on_same_hart_store`. That is a hole in the corpus, not evidence the switch does nothing: each needs a guest written to witness it.

**What the cases changed (a50-2).** Writing the three programs the table left open moved two rows. `RESERVATION` and `SC-DETERMINISTIC` do not use an alternative: the pinned binary's `require_exact_reservation_addr` matches the statement, so each case carries it in an overlay and the override is what selects otherwise, at a witness. So `reservation_set_size_exp` and `invalidate_on_same_hart_store` left the vocabulary, which holds what a case uses. `decision_seven-with-a-switch.md` carries the rest.

## What this does not prove

An observed effect shows that this configuration matters to this guest at this step. It does not show that the profile's selection is right, and it does not show that the alternative is a coherent machine: it shows only that the pinned binary accepts it. The selection stands on its statement and its source, and the statement-trace leg still has to reach every clause.

## How to apply

- **Read a switch before declaring it:** `python3 -B scripts/census_reference_config.py --case <id> --alternative`. It needs only the alternative's file, and it says what moves across the corpus. A case without one refuses by name.
- **An alternative is for a case that needs one.** A case on its own overlay is already compared with the override, and it may still declare one if the override is not the choice the statement is about.
- The next units: `SV39`, `RESERVATION` and `SC-DETERMINISTIC` each need a new guest, and all seven are declared, captured once and credited through the ordinary route.
