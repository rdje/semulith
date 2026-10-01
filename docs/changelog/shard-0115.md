# CHANGELOG shard — SEMULITH-PS-0063 … SEMULITH-PS-0062

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0063 (leaf P2-SCALAR.5, strand 1) — the compiled C guest retires three-way; G1 reads `passed`

- `guests/c-scope.c` is the first COMPILED guest: a self-checking freestanding C tour of
  the declared scope (64/32-bit ALU, every load/store width, branches and a counted loop,
  real calls through the argument registers and an indirect jump, variable shifts),
  compiled by the pinned toolchain (`scripts/build_c_guest.sh` — clang 21.1.8 with the
  RISC-V backend plus `ld.lld` 21.1.8, both probed, refused by name if absent, nothing
  installed) and retiring under first-divergence comparison against sail-riscv AND spike:
  **129/129 aligned steps, byte-identical reproduction**.
- Two in-flight REDs, both authoring-side, never a model defect: the guest's own
  self-check caught `w32 << 33` (UB in C — clang deleted the rest of the program; proven
  by bisect, the `-fno-strict-aliasing` control innocent), and the three-way comparison
  surfaced a comparator gap the hand-written corpus never exercised — the references log
  no-change writes (`li a0, 0`), semulith's declared visible-change vocabulary does not.
  The comparator now reduces every trace to the declared vocabulary (`_visible_changes`
  in `align`, +2 self-test arms, 19/0).
- `gate_report.py`'s criterion 6 gained its met branch — **G1's verdict is `passed`**, the
  same instrument that said `incomplete` while the C path was missing. The report names
  the guest, the build script and the decision record; the toolchain versions keep their
  ONE owner (the decision record + the script's refusals).
- Lockstep: the smoke's `.c` path (build → budget run → `e_entry` from the ELF header),
  LIVE_STATUS (P1 `passed`), MEMORY, both books, P1-LAB's metadata, the model book.
  `make gate` all green; the full smoke 221 PASS / 0 FAIL.

## SEMULITH-PS-0062 (leaf P2-SCALAR.5) — the routing answered, the toolchain measured: .5 unblocked, design before code

- Director delegation `2026-09-30`: the C-guest routing and toolchain call is the
  engineer's. Recorded in `decision_c-guest-routing-and-toolchain`: the C guest lands in
  `P2-SCALAR.5` (the G0 precedent — the tree completes, the gate keeps criterion 6
  visible every commit, `EVD-08` forbids `passed` over a missing check); `P1-LAB` stays
  `done`.
- The toolchain was measured, not installed: Apple clang has no RISC-V backend (exact
  error recorded); Homebrew `llvm@21` clang 21.1.8 compiles RV64I correctly
  (objdump-verified); zig 0.16.0's bundled `ld.lld` 21.1.8 links.
- `.5` blocked → active; the three-strand design recorded before code (strand 1: the C
  guest; strand 2: the ACT4 generated suite; strand 3: directed sequences). Docs-only
  commit; `make gate` green.

