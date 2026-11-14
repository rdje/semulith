# The expectations author reads a new file and the self-tests break — where should its path come from?

**Short answer:** from the encoding the caller is deriving with, found when the file is needed. The self-tests do not run
`scripts/derive_rv64gc_expectations.py` where it lives: they run it on a frozen copy of the encoding (`DERIVE_ENCODING`,
XTASK.13), from a scratch root under `target/p4-system-12`, or as a mutated module whose `ENCODING` a probe repoints
after import. A path built from the module's own `REPO`, or computed once at import, names a file that does not exist
in any of those places.

## The founding measurements

`P4-SYSTEM.20` slice b1 (2026-11-14) made the author write `medeleg`, `mtvec` and `stvec` by the state table. The first
draft read `REPO / "profiles/rv64gc-lab-v0/state.sexp"`: in the repository it worked, and the commit gate's GUEST-GEN
self-test refused at 8 arms, `[Errno 2] No such file or directory: '…/target/p4-system-12/profiles/rv64gc-lab-v0/state.sexp'`.
The fix took the table from the assembler the derivation uses (`state_beside(asm)`, which `scripts/riscv_asm.py`'s
`Assembler.source` makes possible). Slice b2 then let a hart outside any derivation fall back to a default computed at
import, and `scripts/probe_gc_author.py`'s control copies, which set `module.ENCODING` after import, refused at 8 arms
again. The default is now `default_state()`, read at the moment a hart needs it.

## How to apply

- A new input beside the encoding (a state table, a profile document) is located from the encoding in use: the
  derivation's assembler, or `ENCODING` read at call time, never `REPO` and never a module-level constant.
- Run GUEST-GEN (`bash scripts/check_guest_gen.sh`, about four minutes) before the commit chain whenever the author's
  inputs change: it is the check that runs the author from copies.
