;; dispositions.sexp — rv64gc-lab-v0's declared alternative dispositions (schema/dispositions.sexp; decision_the-seventeen-called.md).
;; Each states why the implementation-defined row's two arms cannot be met here and what control stands for them, before its qualification run.
;; The requirement's category stays what its source says.

(disposition (id "DS-ENDIAN") (requirement_id "REQ-D-ENDIAN") (kind case) (source_id "RVI-RV32I") (source_locator "§1.1.6")
  (argument "The specification delegates byte order to the EEI. The implementation-defined row asks for a reference configuration with a behaviour-changing control, or an observed and justified difference. The pinned binary has no key for byte order and its MBE, SBE and UBE read 0, so there is no configuration to select otherwise and no difference to justify. What that control is for, showing the comparison would see the other choice, the case's own control does.")
  (controls "the case's declared control, a big-endian byte 0, diverging at its witness")
  (controls "MBE, SBE and UBE each written and read back, so a hart that could select otherwise would differ")
  (control_property "byte-0"))

(disposition (id "DS-FENCE") (requirement_id "REQ-D-FENCE") (kind case) (source_id "RVI-RV32I") (source_locator "§1.1.7")
  (argument "The profile's reading is the one the specification states for reserved configurations, and the pinned binary has no key for fences: it executes each form this case runs the same way the laboratory does. So there is no configuration to select otherwise and no difference to justify. What a behaviour-changing control is for, showing the comparison would see the other choice, the case's own control does.")
  (controls "the case's declared control, a reserved fm that trapped, diverging at its witness")
  (controls "each of the configurations read through the next row, so a fence that trapped or wrote a register would differ")
  (control_property "fence-fm-reserved"))

(disposition (id "DS-WALK-IMPLICIT") (requirement_id "REQ-D-WALK-IMPLICIT") (kind case) (source_id "RVP-SUPERVISOR") (source_locator "§11.1.3.2") (walk_record yes)
  (argument "The specification defines the implicit accesses, and the boundary's spelling of them is the laboratory's. The pinned binary has no other scheme of implicit reads to select, and the other A and D scheme is REQ-D-SVADE's measured effect. The policy's translation rule says a successful final load cannot establish the absence of an extra access, and a GPR comparison cannot see one, so this needs more than the case: a retained record comparing what each producer's walks read.")
  (controls "the case's declared control, a walk reaching another page, diverging at its witness")
  (controls "the retained walk record: the same PTEs and values on both producers, 8 bytes each, at most 3 per walk, none written from the first walk on, each judged on every read")
  (control_property "walk-three"))

(disposition (id "DS-PARTIAL-PROGRESS") (requirement_id "REQ-GC-PARTIAL-PROGRESS") (kind case) (source_id "RVI-INTRO") (source_locator "Exceptions, Traps, and Interrupts")
  (argument "The specification leaves preciseness to the EEI and recommends it, and the laboratory declares it. The pinned binary is precise on each fault this case raises and has no key to be otherwise, so there is no configuration to select otherwise and no difference to justify. What a behaviour-changing control is for, showing the comparison would see a partial commit, the case's own control does. Faults injected at a chosen suboperation are past the reference, and stay the corpus's.")
  (controls "the case's declared control, a faulting load that wrote rd, diverging at its witness")
  (controls "each kept state read back after a sentinel, so a commit of any of them would differ")
  (control_property "load-rd-kept"))
