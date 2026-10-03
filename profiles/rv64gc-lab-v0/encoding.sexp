;; encoding.sexp — rv64gc-lab-v0's composed encoding, STAGED (P4-SYSTEM.2 slice e): the
;; flip's artifact, authored here because a state/encoding document under
;; profiles/rv64gc-lab-v0/ is a refused route contradiction until the atomic flip
;; (slice h). The fragment-root is the FLIP's relative path — the scratch validation runs
;; through target/p4-system-2/definitions (a symlink), so these bytes are the flip's bytes.
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (comment "The composed definition: the RV64I base + Zicsr + Zicntr + the privileged system instructions — 62 instructions plus 3 pseudo spellings, the flip's initial composition. The slots declare the unbound holes: M/A/F/D/C/Zifencei are in the profile (D-GC-COMPOSITION) but not yet evidenced — M's sem file is its own evidence leaf's (the .2 brief), A is .4's, F/D are .7's, C and Zifencei ride their leaves; partial is DECLARED, never inferred from silence (MODEL-COMPOSE.4).")
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr")
    (extensions "riscv/zicntr")
    (extensions "riscv/system")
    (status partial)
    (slot (id m) (requires "riscv/m"))
    (slot (id a) (requires "riscv/a"))
    (slot (id f) (requires "riscv/f"))
    (slot (id d) (requires "riscv/d"))
    (slot (id c) (requires "riscv/c"))
    (slot (id zifencei) (requires "riscv/zifencei")))
  (fragment-root "definitions"))
