# The C guest lands in P2-SCALAR.5, built by the two toolchains already on the host

- **Type:** `decision`
- **Date:** `2026-09-30`
- **Status:** `active`
- **Owner / source:** director delegation `2026-09-30` ("make the call yourself … sota,
  signoff and production-grade"), answering the routing question `P1-LAB.12`'s ROUTING
  EVIDENCE left open and the toolchain half of `P2-SCALAR.5`'s blocker (b).

## The fact / decision

1. **Routing:** the compiled-C guest is owned by **`P2-SCALAR.5`** (external and directed
   campaigns). `P1-LAB` stays `done`; gate `G1`'s verdict stays `incomplete` — criterion 6
   named — until the C guest's evidence lands and the report regenerates.
2. **Toolchain:** the C guest is compiled by the **already-installed** Homebrew
   `llvm@21` clang 21.1.8 (RISC-V backend) and linked by **zig 0.16.0's** bundled
   `ld.lld` 21.1.8. Nothing new is installed.

## Why

- **Routing** follows the measured G0 precedent: `P0-PROFILE` closed with G0 `incomplete`,
  and `P1-LAB.12` applied the same rule — the tree completes, the gate keeps the unmet
  criterion visible on every commit through `GATE-REPORT`, and `EVD-08` makes
  `passed`-with-a-missing-criterion mechanically unreachable. Reopening `P1-LAB` would
  relocate bookkeeping, not evidence: the guest, the differential and the verdict
  mechanism are identical in either tree, and `P2-SCALAR.5`'s own goal independently names
  "compiled freestanding programs".
- **Toolchain** was measured, not assumed (`2026-09-30`):
  - Apple clang 21.0.0 has **no RISC-V backend** — `--target=riscv64-unknown-elf` fails:
    `unable to create target: 'No available targets are compatible with triple
    "riscv64-unknown-unknown-elf"'`.
  - Homebrew `llvm@21` clang 21.1.8 compiles `-march=rv64i -mabi=lp64 -nostdlib
    -ffreestanding` to correct RV64I code (verified by `llvm-objdump -d`).
  - The keg ships no linker; `zig ld.lld --version` reports Homebrew LLD 21.1.8.
- Rejected alternatives: a system-wide GNU riscv toolchain install (multi-GB, off-volume
  mutation, zero evidence gain over two tools already present); routing clang's `-S`
  output through the project's own assembler (dialect-mismatch risk, and the criterion
  wants a genuinely *compiled* artifact); extending `riscv_asm.py` (it is an assembler —
  compiling C is not its contract).

## How to apply

- The `.c` guest's ELF is a **build artifact** (untracked, on-volume under
  `target/refs/guests/`), with the same standing as the reference binaries and the bench
  wasm: the live differential needs it, the commit gate does not. The tracked facts are
  the `.c` source, the build script, and the pinned toolchain identity (clang 21.1.8 +
  lld 21.1.8) recorded in the leaf's evidence.
- Toolchain use is read-only and off-volume — the `LIVE_STATUS`/session-directive §13
  exception class (a strictly necessary, explicitly identified, evidenced toolchain
  dependency). If either tool disappears from a host, the C-guest build refuses by name;
  it never silently substitutes another compiler.
- Related: [[decision_reference-acquisition-route]] (a binary is not evidence),
  [[reference_what-running-real-rust-actually-requires]] (why C is the first guest path),
  [[decision_push-cadence]] (unchanged — 124/300).

## Enforcement repair — 2026-10-09 (P4-SYSTEM.13 b4)

The original script probed RISC-V capability and printed versions, but did not
validate the pins above. An isolated copy accepted explicit tools reporting
clang/LLD 99.0.0 and built an ELF. The ACT4 duplicate also crashed on an absent
explicit compiler path. Both are repaired through `scripts/riscv_toolchain.py`:

- Validate clang 21.1.8 and LLD 21.1.8 identities before creating a backend probe.
  The Zig driver, when used, must report 0.16.0 via its public `version` command.
  ACT4 additionally validates the matching LLVM 21.1.8 symbol reader.
- An explicit `SEMULITH_RISCV_CLANG` or `SEMULITH_RISCV_LLD` is authoritative.
  Missing tools, wrong identities or a failed backend probe refuse by name;
  discovery never bypasses a bad override. Without overrides, discovery may find
  an installed tool with the same pinned identity; it installs nothing.
- Probe files use unique temporary directories under the caller's repository-local
  output directory and are removed on success or refusal. Identity refusals leave
  existing guest objects and ELF files untouched.

`bash scripts/build_c_guest.sh c-scope` remains the public C-build entry point.
`scripts/probe_riscv_toolchain.py` supplies 20 isolated controls; GUEST-GEN also
runs an identity-bypass mutant. The real pinned build's ELF remained byte-identical.
This legacy guest uses RV64I/LP64. It is not evidence of an implemented GC LP64D
firmware or operating-system environment.
