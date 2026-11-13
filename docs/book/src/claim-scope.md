# What is claimed, and what is not

This page exists because the difference between *"we built an emulator"* and *"this exact
profile behaves as this exact specification revision permits, and here is the evidence"* is the
entire value of the project. Getting that difference wrong once costs more than every feature
gained by overstating it.

## Claimed today

**One accepted processor profile: `rv64gc-lab-v0` version 0, accepted on 2026-11-10 and
verified at commit `194437d6`.** There, gate `CPU-SYSTEM` reads `passed` over its dossier, and the release decision
(`decision_release-rv64gc-lab-v0.md`) pins that dossier's digest. The generated report,
`profiles/rv64gc-lab-v0/GS-REPORT.md` (the unit's own book shows it), verifies the decision at
every commit, so the claim cannot outlive the bytes it was made about: one changed dossier file
and the gate reads `incomplete` again.

**The live tree is version 1's window, and it says so.** `P4-SYSTEM.20` moved the version label
out of `profile.sexp`, which every matched case pins, into `identity.sexp`, which none does, and
retired the 42 case credits that move lapsed. The live report therefore reads `incomplete`, with
`G-STATE`, `G-TRACE`, `G-OBLIGATIONS` and `G-RELEASE` open and each owned by that leaf, and it
says of the decision above: "the decision is of `rv64gc-lab-v0` version `0`, not `rv64gc-lab-v0`
version `1`". To check version 0's claim, check out `194437d6` and read its `GS-REPORT.md`.
Version 1 is accepted only by its own decision, after its cases are captured and credited again.

What the ten axes measured at `194437d6`, in one line each:

| Axis | What stands behind it |
| --- | --- |
| scope | RV64I with M, A, F, D, C, Zicsr, Zicntr, Zifencei, Sstc and Svade: 200 spellings, all exercised |
| state | every hidden-state candidate answered; 4 of 4 state requirements implemented |
| contract | 114 of 114 environment-contract checks realized; contract version 3 frozen |
| trace | 42 matched cases, each with a baseline, a byte-identical repeat and a control seen to diverge |
| obligations | 48 requirements: 46 implemented by current credits, 2 not applicable |
| interactions | 28 of 28 fault, alias, boundary, event, progress and restart cells resolved |
| regression | 210 directed guests; the arch-test suites I, M, Zaamo, Zalrsc, Zca, F and D; generated vectors; 30 of 30 mutants caught; 4 compiled C workloads |
| portability | the tests pass and the 210 guests' digests match, natively on arm64 and x86-64; Miri passes for the host and for big-endian powerpc64 |
| replay | determinism, replay bundles, snapshots and divergence reduction |
| release | the named decision, the declared limits, the digest-pinned dossier |

**This is finite tested evidence, not proof** (`EVD-01`). It says the model agrees with one
pinned reference on the declared observations of the programs the evidence names, within the
limits the report lists.

The rest of the project's claims are smaller and named as such:

- `rv64i-lab-v0` is an **experimental release** (`decision_release-rv64i-lab-v0.md`): its
  `CPU-LAB` report reads `incomplete`.
- `G1`, the laboratory gate, reads `passed` since 2026-09-30.
- `BREADTH` reads `passed` over a bounded, experimental DSP56300 subset.

## Not claimed

| Not claimed | Why it matters |
| --- | --- |
| A conformance result | Nothing here is certified by RISC-V International, and "supports RV64GC" appears nowhere. `CPU-SYSTEM` is this project's own gate, run on its own evidence. |
| Anything past the declared limits | The report lists them: one hart; no board, boot, multicore or weak-memory exploration; one reference; `wfi`'s stall and injected suboperation faults uncredited; the ABI as the pinned compiler builds it; and the next pinned window's open list. |
| Reference *independence* | Every case is matched against one pinned sail-riscv build whose ancestry is unexamined. The arch-test suites and workloads carry Sail-derived expectations, with spike as the control pair: one semantics answering twice, never a second opinion (`EVD-04`). |
| A board, a boot or Linux | The board on file composes `rv64i-lab-v0`, the experimental unit, so this acceptance does not reach it. Linux is P6. |
| Acceptance of any other unit | `rv64i-lab-v0` and `dsp56300-lab-v0` stay experimental. |
| Published evidence beyond this repository | The decision is a local commit until the director approves a push. |
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

And two mechanical habits. A gate that reports `incomplete` is never rewritten as `passed`
because the missing infrastructure is "coming". And an accepted profile stays accepted only
while the bytes it was accepted on stay the same: the report re-checks the decision's digest at
every commit.
