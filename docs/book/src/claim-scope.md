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
Four independently encoded guest programs run on it, and their observations — register
writes, the store, the misaligned-load trap, the no-device access fault — agree with two
independently built reference models (sail-riscv 0.14, spike 1.1.1-dev) on all 34 aligned
steps, and reproduce byte-identically on re-run. The evidence machinery that makes a number
checkable lives here too: the records re-validate on two engines on every commit, and the
guest expectations are specification-derived values the commit gate re-checks offline.

Every one of those claims is **finite tested evidence, explicitly not universal proof**
(`EVD-01`): four programs, two references, one host. Nothing on this page upgrades them.

## Not claimed

| Not claimed | Why it matters |
| --- | --- |
| A validated CPU profile | P2's `CPU-LAB` gate has not been run. The evidence covers four guest programs, not the profile's whole declared scope — no directed sequences, no coverage campaign, no ACT suite, no privilege modes. Executing correctly is a beginning, not a validation. |
| A conformance result | No gate reads `passed`. `G0` ran with verdict `incomplete` (its declared checks are still largely unimplemented); `G1` has not been run at all. |
| An accepted processor profile | `rv64i-lab-v0` is a development profile. Acceptance attaches evidence to an exact versioned profile; none has been accepted. |
| Reference *independence* beyond the inventory | Both comparators are acquired and matched-profile exercised on the smoke set — but ACT4 is deliberately not acquired, QEMU is unexamined, and the two models' floating-point cores share source (`EVD-04`'s inventory is the record). Agreement on 34 steps is two implementations agreeing, not three opinions. |
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
