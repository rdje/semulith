;; encoding.sexp — rv64gc-lab-v0's composed encoding, STAGED (P4-SYSTEM.2 slice e): the
;; flip's artifact, authored here because a state/encoding document under
;; profiles/rv64gc-lab-v0/ is a refused route contradiction until the atomic flip
;; (slice h). The fragment-root is the FLIP's relative path — the scratch validation runs
;; through target/p4-system-2/definitions (a symlink), so these bytes are the flip's bytes.
(encoding (profile "rv64gc-lab-v0") (ilen 32)
  (comment "The composed definition: the RV64I base + Zicsr + Zicntr + the privileged system instructions + A + Zifencei + F + D + M — 160 instructions plus 3 pseudo spellings — A bound at P4-SYSTEM.4 slice (e), Zifencei bound at P4-SYSTEM.6 slice (b), F bound at P4-SYSTEM.7 slice (c6), D at slice (d5), M at P4-SYSTEM.11 slice (b). The slot declares the one unbound hole: C is in the profile (D-GC-COMPOSITION) but not yet evidenced — it rides its own leaf (P4-SYSTEM.12); partial is DECLARED, never inferred from silence (MODEL-COMPOSE.4).")
  (compose (base "riscv/rv64i")
    (extensions "riscv/zicsr")
    (extensions "riscv/zicntr")
    (extensions "riscv/system")
    (extensions "riscv/a")
    (extensions "riscv/zifencei")
    (extensions "riscv/f")
    (extensions "riscv/d")
    (extensions "riscv/m")
    (status partial)
    (slot (id c) (requires "riscv/c")))
  (fragment-root "definitions"))
