;; profile.sexp — DRAFT for dsp56300-lab-v0 (P3-BREADTH.5 slice 2, 2026-10-01).
;;
;; NOT LANDED in profiles/. Landing attaches EXTRACTION, EXERCISE-COVERAGE and
;; INTERACTION-MATRIX to this unit; their measured verdicts are recorded in
;; docs/tasks/P3-BREADTH.md (.5 slice 2) — the document lands with the slice that can
;; keep those gates green honestly. Validate:
;;   python3 scripts/check_sexp_schema.py \
;;     docs/tasks/artifacts/p3-breadth/dsp56300-dossier/profile.sexp schema/profile.sexp

(profile (id "dsp56300-lab-v0") (version "0") (status "experimental") (architecture "DSP56300") (base "DSP56300") (chapter_version "DSP56300FM Rev. 5") (spec_revision "Rev. 5") (harts 1) (ilen 24) (ialign 24)
  (comment "No xlen: the DSP56300 has no XLEN concept — the data word is 24-bit (FM §3.1)."
           "No privilege modes, no extensions: both lists are empty by the .3 rule," "and the absence is earned by the state census beside this file.")
  (sources "NXP-DSP56300-FAMILY-MANUAL")
  (state (program_counter "pc") (authority architecture) (source "DSP56300FM §3.1, §5")
         (comment "No integer_registers / register_width_bits here: the register census is families"
                  "(data-ALU, accumulators with parts, AGU address/offset/modifier), carried in"
                  "state.sexp's register_family forms — P3-BREADTH.5 slice 1's constructs."))
  (scope (count_base 19) (count_total 19) (authority laboratory) (source "decision_dsp56300-lab-v0-subset; DSP56300FM §13")
    (comment "Subset v0 is a LABORATORY-bounded subset of the architecture's instruction set —"
             "the exclusions (parallel moves, condition-code branches, rounding multiplies,"
             "bit-field ops, modulo/reverse-carry addressing, interrupts, modes, stack"
             "extension, peripherals, timing) are named in the subset decision.")
    (moves "move")
    (alu_core "add") (alu_core "sub") (alu_core "cmp") (alu_core "and") (alu_core "or") (alu_core "eor") (alu_core "asl") (alu_core "asr") (alu_core "lsr")
    (multiplies "mpy") (multiplies "mac")
    (flow "nop") (flow "jmp") (flow "jsr") (flow "rts")
    (loops "do") (loops "enddo") (loops "rep"))
  (decision (id "D-SUBSET-V0") (authority laboratory) (statement "Subset v0 is non-parallel moves (including the A2/B2 extension readout), the immediate/register data-ALU core, signed mpy/mac, nop/jmp/jsr/rts, do/enddo/rep, and linear addressing only; every exclusion is named with its reason in the selection record.") (source "decision_dsp56300-lab-v0-subset; docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md"))
  (decision (id "D-ACC-READOUT") (authority architecture) (statement "A2/B2 read as the sign-extended extension byte; A1/B1 read RAW — the shifter/limiter sits on the whole-accumulator read path only (measured: the alu guest stores $FE00FF from A1 with L clear; the FM's limiting prose over-applies to the A1/B1 path).") (source "DSP56300FM §3.4.1.2; measured against the pinned reference, P3-BREADTH.4 slice 4"))
  (decision (id "D-SHORTIMM-ACC") (authority architecture) (statement "A short immediate moved to a whole accumulator sign-extends the 8-bit signed fraction through the extension byte — the FM's 'the remaining bits are zeroed' (13-113) does NOT hold for A2 (measured: move #$80,a leaves A2=$FF).") (source "DSP56300FM §3.4.1.3 / 13-113; measured against the pinned reference, P3-BREADTH.4 slice 4"))
  (decision (id "D-RTS-PC-ONLY") (authority architecture) (statement "RTS restores PC only (SSH → PC; SP − 1 → SP); SR is NOT pulled — that is RTI's shape (13-167).") (source "DSP56300FM 13-168; pinned by the jsr guest (U survives both returns)"))
  (decision (id "D-SBIT-LOCUS") (authority architecture) (statement "The sticky S bit sets only on whole-accumulator reads to the XDB/YDB bus; subset v0 decodes no such read, so S never leaves reset (measured: an ASR of a negative accumulator does not set it).") (source "DSP56300FM Table 5-1; measured against the pinned reference, P3-BREADTH.4 slice 4"))
  (decision (id "D-COMPARISON") (authority laboratory) (statement "The comparison surface is checkpoint-level canonical end-state equality against the pinned reference's difftest dump: registers, deviation-encoded X/Y windows, 15 stack slots; steps compared, cyc never (timing is informational upstream).") (source "references.sexp trace_granularity; tools/difftest/README.md at the pinned commit"))
  (decision (id "D-RESET-STATE") (authority laboratory) (statement "Reset: SR $C00300 (CP=11, I1=I0=1, CCR clear), OMR $000300, LA and all M registers $FFFFFF, everything else zero; pc is set by the runner from the case's load base.") (source "DSP56300FM Table 5-1 and §3/§5 reset states, cross-checked against the reference's observed reset dump"))
)
