# What is claimed, and what is not

This page exists because the difference between *"we built an emulator"* and *"this exact
profile behaves as this exact specification revision permits, and here is the evidence"* is the
entire value of the project. Getting that difference wrong once costs more than every feature
gained by overstating it.

## Claimed today

Still nothing about a *processor product*: no conformance result, no accepted profile, no
gate reading `passed`.

What exists is a **laboratory with first evidence**. The three-crate workspace executes the
`rv64i-lab-v0` definition: all 52 declared instructions evaluate directly from the semantics
data, under the environment contract, with the outcome families the architecture requires.
Forty independently encoded guest programs run on it — the four P1 smoke guests, the five
`P2-SCALAR.1` scope-completion guests, the five `P2-SCALAR.2` boundary guests, the
eighteen `P2-SCALAR.3` fault guests, and the eight `P2-SCALAR.4` interaction guests, so every
one of the 52 declared forms is executed, the shift-amount domains are exhausted, the
fault, suppression and reserved cases behave as the source classifies them, and the declared
fault × alias × boundary × event × progress × restart matrix's 21 cells all resolve —
and their observations agree with two
independently built reference models (sail-riscv 0.14, spike 1.1.1-dev) on all 492 aligned
steps (plus one *declared* expected divergence, `it-fencei`, where the references execute
a word this profile declares reserved), and reproduce byte-identically on re-run. The evidence machinery that makes a number
checkable lives here too: the records re-validate on two engines on every commit, and the
guest expectations are specification-derived values the commit gate re-checks offline.

Every one of those claims is **finite tested evidence, explicitly not universal proof**
(`EVD-01`): forty-one programs, two references, one host. Nothing on this page upgrades them.

## Not claimed

| Not claimed | Why it matters |
| --- | --- |
| A validated CPU profile | P2's `CPU-LAB` gate has not been run. The evidence covers the guest corpus, its declared, exercised interaction matrix, and the ACT4 RV64I external campaign (51 test files, Sail-derived expectations — one semantics by construction) — but no directed campaigns, no privileged-mode tests, no portability matrix. Executing correctly is a beginning, not a validation. |
| A conformance result | `G1` reads `passed` since `2026-09-30` (criterion 6 met by the `c-scope` compiled C guest, `P2-SCALAR.5`) — a laboratory gate, not a conformance claim. `G0` ran with verdict `incomplete` (its declared checks are still largely unimplemented), and the `CPU-LAB` processor gate has not run. |
| An accepted processor profile | `rv64i-lab-v0` is a development profile. Acceptance attaches evidence to an exact versioned profile; none has been accepted. |
| Reference *independence* beyond the inventory | Both comparators are acquired and matched-profile exercised on the guest corpus; ACT4 is acquired (a sparse partial pinned at `e2216915…`, `P2-SCALAR.5` strand 2) but not yet run, QEMU is unexamined, and the two models' floating-point cores share source (`EVD-04`'s inventory is the record). Agreement on 492 steps is two implementations agreeing, not three opinions. |
| Complete in-repository claim tooling | The frozen `examples/` records re-validate in Rust per `RUST-01`, and the guests' expectations re-check offline — but the profile dossier still rides the Python track, and `CLAIM_VERIFICATION.md`'s tag and constant sweep are not mechanized. |
| The name | *Semulith* is proposed. No crate, repository, domain, or trademark has been reserved or cleared. |

## The rules that keep it that way

Three of the project's normative rules exist specifically to stop this page from quietly
becoming false:

- **`SRC-03`** — never fabricate source hashes, test results, tool availability, namespace
  availability, or accepted gate status.
- **`EVD-01`** — finite testing, including deterministic differential testing, establishes
  *tested evidence* and is never labelled universal proof.
- **`AI-03`** — AI review and agreement are criticism and workflow aids, not independent
  conformance evidence.

And one mechanical habit: a gate that reports `incomplete` is never rewritten as `passed`
because the missing infrastructure is "coming". No *when available* clause turns an incomplete
message into a pass — and no *we executed it* clause turns a development profile into an
accepted one.
