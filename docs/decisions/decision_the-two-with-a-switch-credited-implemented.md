# `REQ-D-NO-H` and `REQ-D-NO-PMP` are credited `implemented`, each measured against a hart that has it

- **Type:** `decision`
- **Date:** `2026-11-07`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a51-6, `SEMULITH-P4-0384`; the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md) and [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md), carrying out track 2 of [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md).
answers: Who signs these two credits, what does each finite case claim, and what does each leave out?

## The fact / decision

1. **Authority.** Each record in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`.
2. **Sufficiency.** One finite case per requirement, each `DIV-POLICY: satisfied — 11 of 11 legs satisfied`. That is sufficient for `implemented` and for nothing more: the M rulings' reading of the derivation.
3. **What each claims, and what it leaves out** (each record's `limitations`):

   | Credit | Requirement, risk | Witnesses | Control | Compared with, first difference | Not claimed |
   | --- | --- | --- | --- | --- | --- |
   | `CR-D-NO-H-1` | `REQ-D-NO-H`, low | 5 | a hart with H | `H` on, step 5, `misa` | `hstatus` and the other H state, past the pinned author's vocabulary; why no consumer needs it |
   | `CR-D-NO-PMP-1` | `REQ-D-NO-PMP`, low | 4 | a load a PMP unit refused | 16 PMP entries, step 22, a load at S's privilege | a fetch at S's or U's privilege against the alternative, since a refused fetch reads as absent evidence; `pmpcfg0` itself, past the vocabulary; why the first boot contract does not need it |

4. **What the route thought could not be done.** [`decision_obligations-route.md`](decision_obligations-route.md) called these selections with no behaviour to compare. Each is now a real comparison against a real hart that selects otherwise.
5. **No dossier copy.** `G-TRACE` lists all 38 credited cases, reading each from `evidence/`.

## How to apply

- Any pin movement lapses these credits as it does the other 36: the three pins and every input of the case's manifest.
- When a window widens the author's vocabulary, `hstatus` and `pmpcfg0` can be read directly, and these limitations narrow. That is on the list in [`decision_csr-write-three-producers.md`](decision_csr-write-three-producers.md).
