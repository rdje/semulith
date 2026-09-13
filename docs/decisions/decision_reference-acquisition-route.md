# The reference route for `rv64i-lab-v0`: three obtained models, and no independence claim

- **Type:** `decision`
- **Date:** `2026-09-14`
- **Status:** `active`
- **Owner / source:** established by `P0-PROFILE.5`; every field re-derivable with
  `scripts/fetch_references.sh --verify-only`

## The decision

The reference route is **Sail RISC-V as the primary oracle candidate, with Spike and QEMU as
second and third implementations**, all three obtained and runnable on the development host, and
**ACT deliberately not acquired yet**. Recorded in `profiles/rv64i-lab-v0/references.toml`.

| Candidate | Status | Matched by | Self-report |
| --- | --- | --- | --- |
| Sail RISC-V 0.14 (prebuilt `Mac-arm64`) | obtained | tracked JSON override | `rv64i_zvl32b` |
| Spike 1.1.1-dev (source build `1e05ddac`) | obtained | `--isa=rv64i --priv=m` | `rv64i` |
| QEMU 11.1.1 (pre-existing host toolchain) | obtained | `-cpu rv64i` | none emitted |
| ACT, `act4` branch | reachable, not acquired | — | — |

## What this supersedes

`ROADMAP.md` §1 and the `P0-PROFILE` tree both priced reference acquisition as the first activity
whose cost was *not obviously bounded*, on the assumption that Sail required an OCaml/opam
toolchain built under a repository-local `OPAMROOT`. **That assumption is obsolete for running
the model.** Release 0.14 publishes a native binary for this host's architecture, so Sail became
the cheapest candidate rather than the most expensive. Building Sail from source remains the
route if the model must be *modified*, and that route is unattempted — so no claim is made about
its tractability.

The roadmap's *reasoning* is untouched and was correct: acquisition is work with observable
outcomes. This record changes the estimate, not the discipline.

## What it explicitly does NOT decide

- **Not which reference is the primary oracle.** That is resolved by `P0-PROFILE.6` running a
  matched experiment, not by this record and not by preference.
- **Not that any reference is usable.** `docs/EVIDENCE_AND_GATES.md` §5 makes a reproduced
  matched-profile experiment the condition. Having a binary is not having evidence.
- **Not that the three models are independent.** ACT derives its expected results from a
  *configured Sail model*, so ACT and Sail agreeing is one semantics answering twice. Spike and
  QEMU are *plausibly* independent of Sail and of each other; `EVD-04` requires shared ancestry
  to be examined per subsystem, and `P0-PROFILE.7` owns it. Every candidate carries a `lineage`
  field for that leaf to consume, and `PROFILE-CONSISTENCY` refuses a candidate that omits one.

## Two limits recorded at acquisition time

1. **The Sail model cannot be configured to exactly `extensions = []`.** Driven down from 96
   supported extensions it reaches `rv64i_zvl32b`: the base plus a vestigial minimum
   vector-length class the model instantiates even with the vector unit `Disabled`. No vector
   instruction decodes, so it is believed benign — recorded rather than rounded away, because
   `G0` asks for differences to be enumerated, not assumed absent.
2. **The Sail model will not emit its effective configuration.** `--print-default-config` ignores
   `--config-override`; the dumps are byte-identical. So the effective configuration is
   *(release 0.14 default) + (the tracked override)* and **that merge is ours, not the model's
   report of itself**. The model's one self-description is `--print-isa-string`, which is pinned
   and re-derived. A later leaf must not silently upgrade our merge into the model's own word.

## Data locality

The repository volume and the shared package-manager prefix are **different volumes** on this
host. Every artifact this project owns — the Sail release, the Spike clone, its build tree and
prefix — lives under `target/refs/` on the repository volume, and nothing was installed into the
shared prefix. Two pre-existing host toolchains are used **read-only** and recorded as
cross-volume in `references.toml`: `dtc` (Spike's build prerequisite) and `qemu-system-riscv64`.

## How to apply

- Re-derive before trusting any recorded hash: `scripts/fetch_references.sh --verify-only`. It
  checks the release asset, both binaries, the Spike source commit, the read-only QEMU binary,
  **and** that the tracked override still configures Sail to `rv64i_zvl32b`.
- When adding a candidate, fill in `lineage` first and `status` last. A candidate marked
  `obtained` must name its binary, digest, invocation, trace granularity, injection capability
  and terms, or the gate refuses it — `SRC-03` forbids recording availability that has not been
  established.
- When a candidate cannot be obtained, say so with the attempt and its consequence. `SRC-02`
  makes an honest *"no route"* a legitimate result that bounds the claim.

Related: [[decision_claim-verification-adopted]], [[reference_upstream-spine-defects]].
