#!/usr/bin/env python3
"""Measure the retained DIV case against the evidence policy's legs; measurement only, no credit.

`profiles/<profile>/EVIDENCE_POLICY.md` names, for a requirement's source-semantic category and
risk, the evidence a credited disposition needs. This consumer measures which of those legs
the retained bytes already satisfy, from the predeclaration, the expectation file, the
derived receipt, the dependency manifest and the catalogue, on top of the finite method
review (`review_div_method`). It reads bounded tracked files, launches no process, writes
nothing, and never grants credit: `credited` is always false. A satisfied measurement is
the input a later, separately owned crediting record would cite; a pending one names the
legs still missing.

Legs (policy sections "Source-semantic dispositions", "Risk and feature obligations",
"Records, controls and currentness"):

  source-located-expectations  every expectation step carries a derivation and a source; the
                               witness step cites the requirement's source; the expected
                               producer reads no reference-only input (no model output as
                               its own expectation).
  statement-trace              every clause of the requirement's statement names a witness or a limit the case states, and every
                               declared property stands for some clause (scripts/statement_trace.py; a49-1)
  boundary-fixtures            directed boundary rows (a step whose source cites a table row or
                               carries a `(boundary: …)` tag) are present AND each is predeclared
                               as a property.
  matched-reference-comparison the finite method is satisfied and the baseline agrees under
                               the declared comparison rule and named observation vocabulary; and the
                               requirement's category row holds: `defined` asks nothing more,
                               `implementation-defined` the selection recorded in the catalogue and a
                               behavior-changing control (`_config_effect`), `source-specific` a disposition declared
                               for the requirement and naming the case's own control; a category with no branch
                               here stays pending and is named (P4-SYSTEM.14 a43b-3g).
  repeated-execution           a repeat run agrees.
  discriminating-control       the control diverges at the step and register of the one property
                               the control_run names — it fails for the stated reason (wrong
                               defined result).
  record-linkage               requirement, effective obligation, tracked runner, expectation
                               producer, receipt identity and limitations are all named.
  currentness                  the policy document is pinned by the dependency manifest and
                               its current bytes equal the pin; the method binding matched.
  risk-method                  low/medium risk needs no second method; high/critical needs the
                               case's declared second method and adversarial case, judged against
                               the record by five conditions (P4-SYSTEM.14 a43b-2b); a declaration
                               is judged at any risk, never ignored.
  feature-rules                the obligation's feature disposition is declared below.
  form-coverage                every form the requirement names is exercised AND predeclared; a
                               state requirement naming no form is satisfied vacuously, and says so.

Exit 0: measured (satisfied, pending or invalidated). Exit 1: a finding — the receipt
claims `qualification` the legs refuse, or the finite method is refused, unavailable or
unsupported (blocked). A `stale` finite method — a pinned input moved since the capture —
is the policy's currentness rule doing its work ("changes invalidate dependent evidence"):
the measurement is `invalidated`, the legs that depend on the method stay pending, the
moved input is named, and nothing is refused unless the receipt still claims qualification
(P4-SYSTEM.14 a42as, the director's ruling of 2026-10-22). An invalidated case grants
nothing and locks nothing: the next capture supersedes it.
Exit 2: refused/unavailable/unsupported (bounds, unreadable inputs, another case).
`--every-retained` measures every case the finite method review holds a reviewed capture for, one line
each, and exits with the worst code (P4-SYSTEM.14 a43a-2f; PROFILE-CONSISTENCY's real run).
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import credit_records as CR  # noqa: E402
import records_sexp as R  # noqa: E402
import sexp as S  # noqa: E402
import statement_trace as ST  # noqa: E402

FORMAT = "div-policy-review-v1"
CASE_ID = "rv64gc-m-forms-v7"  # the default retained case (a42ax: v3; a44-5: v4; a43b-2e: v5; a43e-5: v6; a49-3: v7); a consumer constant no case pins
DOCUMENT_BYTES = 65536
# An expectation step whose source cites a chapter table row (M's Table 1) or carries a `(boundary: …)` tag (the XLEN
# guest's ten, a43a-2d) is a directed boundary fixture. The tag occurs in no M expectation, so M's rows do not move.
BOUNDARY_MARKERS = ("Table", "(boundary")
LOW_RISK = ("low", "medium")
# The policy's four named second methods ("Risk and feature obligations"), one token each; its text stays the authority.
SECOND_METHODS = ("independent-exact-expectation", "bounded-exhaustive-check", "source-grounded-invariant-check",
                  "qualified-hardware-observation")
# Declared feature dispositions (policy "the following feature rules apply regardless of the risk
# field"). An obligation absent here has no disposition and stays pending — never inferred.
FEATURE_DISPOSITIONS = {
    "OB-GC-M": "none applies: integer multiply/divide touches no privilege, translation, atomic, "
               "floating-point, counter, fetch or environment rule (P4-SYSTEM.14 a42aq, 2026-10-21)",
    "OB-XLEN": "none applies: the register width and the 64-bit address space touch no privilege, translation, "
               "atomic, floating-point, counter, fetch or environment rule; the access fault at 2^40 and the "
               "handler's CSRRS of mtval are the route that observes the address, not a claimed trap, CSR or "
               "protection behaviour (the fault's selection is REQ-D-FAULT-PRIORITY's, mtval's presence "
               "REQ-D-CSR-SET's, the read REQ-GC-CSR-ACCESS's) (P4-SYSTEM.14 a43a-2f, 2026-10-29)",
    "OB-CSR-SET": "the privilege and CSR rule applies, and the case's properties cover it: legal and refused modes (s-reads-sstatus, "
                  "s-reads-sscratch, u-reads-fflags; refused-csrrw-cause, refused-csrrs-cause, s-refused-cause, u-refused-cause), "
                  "aliases (alias-sie-mie, csr-sip-alias, alias-sip-clear, alias-sstatus-mstatus, alias-fcsr, fs-dirty-sd) and "
                  "preserved state read back after every refusal, so a forbidden write commits neither its destination nor its rd "
                  "(mhartid-kept, s-refused-mscratch-kept, u-refused-sscratch-kept, refused-csrrw-rd-kept, refused-csrrs-rd-kept, "
                  "s-refused-rd-kept, u-refused-rd-kept). The counter and floating-point rules stay with their own requirements: "
                  "each counter and fflags, frm and fcsr are witnessed as members of the set, not their scheduling or numerics "
                  "(REQ-D-ZICNTR; the F and D cases) (P4-SYSTEM.14 a43b-3g, 2026-11-04)",
    "OB-ZICNTR": "the counter rule and the privilege and CSR rule apply, and the case's properties cover them. The counter rule: the schedule "
                 "is the step boundary itself, a guest count and never host time, and each value is recorded at its declared boundary (m-reads-cycle, "
                 "m-reads-time, m-reads-instret, m-reads-mcycle, m-reads-minstret, instret-progress, cycle-progress); the suppression "
                 "is the trap that retires nothing (trap-retires-nothing); nothing is delivered, since no interrupt or wait is scheduled, "
                 "so timer delivery stays REQ-D-SSTC's and rates the environment contract's. The privilege and CSR rule: legal and refused "
                 "modes (s-cy-reads-cycle, s-reads-time, s-reads-instret, u-reads-cycle, u-reads-time, u-reads-instret; s-closed-cycle-cause, "
                 "s-closed-time-cause, s-closed-instret-cause, u-closed-cycle-cause, u-m-closed-instret-cause, ro-csrrw-cause), aliases "
                 "(alias-mcycle-cycle, alias-minstret-instret) and preserved state read back after every refusal, so a refused read or write "
                 "commits no rd (s-closed-cycle-rd-kept, u-closed-cycle-rd-kept, u-m-closed-instret-rd-kept, ro-csrrw-rd-kept) "
                 "(P4-SYSTEM.14 a43c-5, 2026-11-05)",
    "OB-SSTC": "the counter rule and the privilege and CSR rule apply, and the case's properties cover them, all 39. The counter rule, its three parts. "
               "Scheduled time and events: guest counts at declared boundaries, never host time (m-reads-time, s-reads-the-time, scheduled-count), and "
               "pending below and at the compare (not-pending-below-compare, pending-at-compare). Delivery boundaries: from S (delivered-scause, delivered-sepc, "
               "delivered-spp, delivered-acknowledged, delivery-resumes), on a schedule (scheduled-scause, scheduled-sepc, scheduled-acknowledged), from U "
               "(u-delivered-scause, u-delivered-sepc, u-delivered-spp, u-acknowledged, u-resumes) and to M (undelegated-mcause, undelegated-mepc, undelegated-resumes). "
               "Suppression cases: STIE clear, SIE clear in S, delegated while in M, STCE clear (suppressed-stie-clear, suppressed-sie-clear, suppressed-delegated-in-m, "
               "m-still-pending, suppressed-stce-clear, stce-clear-not-delivered). A scheduled delivery's exact boundary is what both producers do on this configuration, "
               "not a latency claim, since the statement guarantees a changed comparison reaches STIP only eventually. No wait is scheduled, so wfi's wake stays "
               "P4-SYSTEM.5's. The privilege and CSR rule: legal and refused modes (m-stimecmp-reset, m-stimecmp-64bits, s-reads-stimecmp, s-programs-own; "
               "s-tm-stce-clear-cause, s-stce-clear-cause, s-tm-clear-cause, u-refused-cause) and preserved state read back after every refusal, so a refused access "
               "commits no rd (s-tm-stce-clear-rd-kept, s-stce-clear-rd-kept, s-tm-clear-rd-kept, u-refused-rd-kept). stimecmp has no alias to witness "
               "(P4-SYSTEM.14 a43e-5, 2026-11-05)",
}
FEATURE_DISPOSITIONS.update({
    "OB-ALU-IMM": "none applies: register-immediate arithmetic touches no privilege, translation, atomic, floating-point, counter, fetch or environment rule (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-ALU-REG": "none applies: register-register arithmetic touches no privilege, translation, atomic, floating-point, counter, fetch or environment rule (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-LUI-AUIPC": "none applies: LUI and AUIPC touch no privilege, translation, atomic, floating-point, counter or environment rule, and the fetch rule's parcel boundaries are not in play: AUIPC reads the address of a four-byte instruction (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-SHAMT": "none applies: shift amounts touch no privilege, translation, atomic, floating-point, counter, fetch or environment rule (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-WSUFFIX": "none applies: word arithmetic touches no privilege, translation, atomic, floating-point, counter, fetch or environment rule (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-JALR-LSB": "none applies: every target in the case is word-aligned once its least-significant bit clears, so the fetch rule's parcel and width boundaries are not in play; a halfword target is REQ-D-IALIGN-16's and REQ-GC-C's (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-NO-DELAY-SLOTS": "none applies: every transfer in the case lands on a word-aligned target in sequence, so the fetch rule's parcel and width boundaries are not in play; a halfword target is REQ-D-IALIGN-16's and REQ-GC-C's (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-LOAD-EXT": "none applies: translation is off and every access is aligned to readable memory, so the translation and protection rule is not in play; a misaligned or faulting access, and an atomic one, are other requirements' (P4-SYSTEM.14 a46-4, 2026-11-06)",
    "OB-LOAD-X0": "none applies as a claim: the access fault at 2^40 and the handler's CSR reads and MRET are the route that observes the fault, not a claimed trap, CSR or protection behaviour (the fault's selection is REQ-D-FAULT-PRIORITY's, the reads REQ-GC-CSR-ACCESS's, the return REQ-GC-PRIV-INSNS's); translation is off, and the requirement's other side effects are named in the limitations (P4-SYSTEM.14 a46-4, 2026-11-06)",
})
FEATURE_DISPOSITIONS.update({
    "OB-GC-ECALL-EBREAK-V3": "the privilege, CSR, trap and return rule applies, and the case's properties cover it: each mode's cause (m-ecall-cause, m-ebreak-cause, s-ecall-cause, s-ebreak-cause, u-ecall-cause, u-ebreak-cause, u-ecall-delegated-cause, u-ebreak-delegated-cause, u-illegal-cause), its trap value and exception PC, and the mode taking it, delegated or not. A delegated cause taken in M stays in M (m-ebreak-cause), so a trap never moves to a lower mode (P4-SYSTEM.14 a47-3, 2026-11-06)",
    "OB-GC-CSR-ACCESS": "the privilege, CSR, trap and return rule applies, and the case's properties cover it: legal and refused modes (csrrs-x0-no-write, csrrsi-zero-no-write, s-reaches-own; refused-cause-0, refused-cause-1, refused-cause-2, refused-cause-3) and preserved state read back after every refusal, so a refused access commits no rd (refused-csrrw-rd-kept, refused-csrrs-rd-kept, refused-csrrsi-rd-kept, s-refused-rd-kept). Aliases are REQ-D-CSR-SET's and counter gates REQ-GC-COUNTERS' (P4-SYSTEM.14 a47-3, 2026-11-06)",
    "OB-GC-COUNTERS": "the counter rule and the privilege and CSR rule apply, and the case's properties cover them. The counter rule: each read at its declared boundary, a guest count and never host time (m-reads-cycle, m-reads-time, m-reads-instret, s-open-reads, u-open-reads); nothing is scheduled or delivered, so that stays REQ-D-SSTC's and rates the environment contract's. The privilege and CSR rule: each gate bit deciding the read, and a refused read committing no rd (s-closed-rd-kept, s-time-gate-own-bit, u-needs-scounteren) (P4-SYSTEM.14 a47-3, 2026-11-06)",
    "OB-IALIGN-16": "the fetch rule applies, and the case's properties cover its parcel and width boundaries: a 32-bit instruction on a halfword (jalr-halfword-landing), each kind of transfer to a halfword target with no misaligned exception (jalr-halfword-link, branch-halfword-landing, jal-halfword-link, jal-halfword-landing), and a 16-bit form advancing the PC by two (c-form-advances-two). Each compressed form's expansion is REQ-GC-C's (P4-SYSTEM.14 a47-3, 2026-11-06)",
    "OB-GC-FENCEI": "the fetch rule's instruction visibility applies, and the case's properties cover it: a store ordered before a later fetch, so the patched instruction runs (fence-i-orders-the-store), and FENCE.I itself retiring with no other effect (fence-i-no-other-effect). That a fetch with no FENCE.I may read either value is not witnessed, since this machine re-reads memory on every fetch (P4-SYSTEM.14 a47-3, 2026-11-06)",
})
MAX_PROPERTIES = 96  # matched_gpr_relations.MAX_PROPERTIES, held equal by the probe: this review imports no pinned tool (a49-1)
FEATURE_DISPOSITIONS.update({
    "OB-GC-ATOMICS": "the atomics rule and the translation rule apply, and the case's properties cover them. Width: both widths, a word sign-extended, its upper word kept and rs2's ignored (amoadd-w-old, amoadd-d-old, lr-w-sign-extends, lr-d-reads, word-amo-keeps-upper, word-amo-ignores-rs2-upper). Destination and source aliases (rd-equals-rs2-old, rd-equals-rs2-sum, rd-equals-rs1-old, rd-equals-rs1-sum). Reservation history (sc-w-succeeds, sc-w-stored, second-sc-fails, lr-fault-reserves-nothing, sc-d-succeeds, sc-d-stored). Completion against faults and refused stores (amo-fault-cause, amo-fault-keeps-rd, lr-fault-cause, lr-fault-keeps-rd, failed-sc-stores-nothing). One store-rules translation (amo-unreadable-cause, amo-unreadable-stval, translated-amo-reads, translated-amo-writes). The ordering bits decode and order nothing this hart can observe (amoadd-aq-decodes, amoadd-rl-decodes, amoadd-aqrl-decodes, lr-aqrl-decodes, sc-aq-decodes). Address and physical aliases are REQ-D-RESERVATION's, not witnessed here, and one hart earns no multicore or weak-memory claim (P4-SYSTEM.14 a49-1, 2026-11-06)",
    "OB-GC-C": "the compressed rule and the fetch rule apply, and the case's properties cover them. Parcel and width boundaries: a sixteen-bit form advancing two bytes, and running from a page's last parcel with nothing mapped after it (c-nop-advances-two, c-jalr-links-next-parcel, parcel-before-page-end, one-parcel-at-page-end, next-fetch-faults-there, second-parcel-cause, second-parcel-tval, second-parcel-epc, second-parcel-no-effect). Original instruction diagnostics: reserved encodings and the wider prefix keep their own bits in mtval (reserved-c-lwsp, reserved-c-jr, all-ones-keeps-ilen, c-fld-fs-off, c-fsdsp-fs-off). Old-source aliases (c-jalr-takes-old-source). No-effect and refusal cases (hints-advance-only, hints-keep-state, all-zero-parcel, c-fld-off-writes-nothing, c-ebreak-cause, c-ebreak-epc). A valid C form keeps a reservation (c-keeps-reservation). Every reserved code point is not enumerated, and the fetch width stands on what ran, never on counting the environment's requests (P4-SYSTEM.14 a49-1, 2026-11-06)",
    "OB-GC-F": "the floating-point rule and the privilege and CSR rule apply, and the case's properties cover them. The numeric expected results come from scripts/specfp, a tracked spec-side producer distinct from the backend under test, and the matched reference is a second one. Bits (fmv-x-w-moves-bits, fmv-w-x-boxes, transfers-keep-payload, sgnj-keeps-payload, fsw-stores). Rounding (fdiv-s, static-rounding, dynamic-rounding, static-rtz, fcvt-w-rounds, fcvt-w-rtz, fcvt-w-rdn, fcvt-w-rup, fcvt-w-rmm). Flags (exact-sets-no-flag, inexact-flag, flags-accrue, invalid-flag, overflow-flag, underflow-flag, not-tiny-after-rounding, sgnj-sets-no-flag, fmin-signaling-invalid, fused-invalid-flag, feq-quiet, flt-signaling, fcvt-invalid-flag). Boxing (improper-box-is-nan, fmv-w-x-boxes). Exceptional cases (div-by-zero, invalid-is-canonical, fused-invalid, fmin-one-nan, fmin-both-nan, fmin-signaling-other, tininess-after-rounding, fcvt-wu-saturates, fcvt-w-nan, fcvt-wu-nan, fcvt-l-nan, fcvt-w-too-large, fcvt-w-negative-infinity, fcvt-l-too-large, fcvt-lu-negative, fclass-negative-infinity, fclass-negative-normal, fclass-negative-subnormal, fclass-negative-zero, fclass-positive-zero, fclass-positive-subnormal, fclass-positive-infinity, fclass-signaling, fclass-quiet). Legal and refused modes, and the FS state (reserved-static-5, reserved-static-6, reserved-dynamic, reserved-dynamic-6, reserved-dynamic-7, reserved-writes-nothing, fs-off-cause, fs-off-keeps-rd, fs-off-load, fs-off-arithmetic, fs-dirty, fs-clean-stays, fs-flags-dirty, fs-dirty-sd). Numeric results stand at these values, and earn no claim of exhaustiveness (P4-SYSTEM.14 a49-1, 2026-11-06)",
    "OB-GC-D": "the floating-point rule and the privilege and CSR rule apply, and the case's properties cover them. The numeric expected results come from scripts/specfp, a tracked spec-side producer distinct from the backend under test, and the matched reference is a second one. Bits (fmv-x-d-moves-bits, transfers-keep-payload, sgnj-keeps-payload, sgnj-sets-no-flag, fsd-stores). Rounding (fdiv-d, static-rounding, dynamic-rounding, static-rtz, fcvt-s-d, fcvt-s-d-rounds, fcvt-w-rounds, fcvt-w-rtz, fcvt-w-rdn, fcvt-w-rup, fcvt-w-rmm). Flags (exact-sets-no-flag, inexact-flag, flags-accrue, invalid-flag, overflow-flag, underflow-flag, not-tiny-after-rounding, fmin-signaling-invalid, fused-invalid-flag, feq-quiet, flt-signaling, fcvt-invalid-flag, snan-conversion-invalid). Boxing (box-is-a-quiet-nan, fcvt-d-s, fcvt-d-s-unboxed, snan-conversion-canonical). Exceptional cases (div-by-zero, invalid-is-canonical, fused-invalid, fmin-one-nan, fmin-both-nan, fmin-signaling-other, tininess-after-rounding, fcvt-wu-saturates, fcvt-w-nan, fcvt-wu-nan, fcvt-l-nan, fcvt-w-too-large, fcvt-w-negative-infinity, fcvt-l-too-large, fcvt-lu-negative, fclass-negative-infinity, fclass-negative-normal, fclass-negative-subnormal, fclass-negative-zero, fclass-positive-zero, fclass-positive-subnormal, fclass-positive-infinity, fclass-signaling, fclass-quiet). Legal and refused modes, and the FS state (reserved-where-nothing-rounds, reserved-on-widening, reserved-dynamic, reserved-writes-nothing, fs-off-cause, fs-off-keeps-rd, fs-off-load, fs-off-arithmetic, fs-dirty, fs-clean-stays, fs-flags-dirty, fs-dirty-sd). Numeric results stand at these values, and earn no claim of exhaustiveness (P4-SYSTEM.14 a49-1, 2026-11-06)",
})
FEATURE_DISPOSITIONS.update({
    "OB-SVADE": "the translation rule and the fault rule apply, and the case's properties cover them. A load, a store and a fetch with A clear, and a store with D clear, each raising its page fault with its address (a-clear-load-cause, a-clear-store-cause, a-clear-fetch-cause, d-clear-store-cause); what needs no update completing (both-set-loads, both-set-stores, d-clear-load-completes); each PTE read back unchanged (pte-a-still-clear, pte-d-still-clear, pte-fetch-still-clear); and ADUE staying clear (adue-stays-clear). The other scheme is the retained effect's.",
    "OB-ATOMIC-MISALIGN": "the atomics rule and the fault rule apply, and the case's properties cover them. LR's access fault and SC and AMO's by kind at both widths, each with its address (lr-w-cause, lr-d-cause, sc-w-cause, sc-d-cause, amoadd-w-cause, amoswap-d-cause); nothing written or stored (rd-kept, memory-kept); and each judged before translation, an aligned access on the same page reaching it (translation-lr-cause, translation-sc-cause, translation-amo-cause, aligned-lr-cause, aligned-amo-cause).",
    "OB-GC-FAULT-PRIORITY-V2": "the fault rule applies, and the case's properties cover it: each adjacent pair the profile can raise, in one program. Fetch faults over decode and access (fetch-page-over-decode-cause, fetch-page-over-access-cause, fetch-access-over-decode-cause); illegal-instruction over misaligned, translation and access (illegal-over-misaligned-cause, illegal-over-translation-cause, illegal-over-access-cause); misaligned over page and access (misaligned-over-page-load-cause, misaligned-over-access-load-cause), and the atomics at the same point (atomic-lr-same-point-cause, atomic-amo-same-point-cause); translation over access (translation-over-access-load-cause); and the physical access last (physical-last-load-cause).",
    "OB-PRIV-MODES": "the privilege and CSR rule applies, and the case's properties cover it. Three modes named by misa, H not (misa-names-the-modes, misa-no-h, no-h-state); an environment call from each with its own cause (ecall-from-m, ecall-from-s, ecall-from-u); MPP holding each and a trap recording where it came from (mpp-holds-u, mpp-holds-s, trap-recorded-s, trap-recorded-u); and each mode's CSR refused below it (s-cannot-read-m, u-cannot-read-s).",
    "OB-SV39": "the translation rule applies, and the case's properties cover it. Bare at reset, Sv48 and Sv57 refused with no field moving, Sv39 taken (bare-at-reset, sv48-from-bare, sv57-from-bare, sv39-taken, sv48-over-sv39); a walk of each depth (walk-4k, walk-2m, walk-1g); and a non-canonical address and a misaligned superpage faulting (not-canonical-cause, misaligned-superpage-cause).",
    "OB-GC-RESERVATION-V2": "the atomics rule applies, and the case's properties cover it. Exactly the LR's word, on its own overlay (exact-address, same-address-pairs, doubleword-pairs); LR replacing and SC invalidating either way (lr-replaces-old, lr-replaces-new, failure-invalidates, success-invalidates); each target fault keeping it (misaligned-keeps-reservation, permission-keeps-reservation, translation-keeps-reservation); aliases (alias-pairs); and six ordinary instructions preserving it (sw-preserves, sd-preserves, fsd-preserves, amoadd-preserves, addi-preserves, fence-preserves). Exact width is past the reference and named in the case's limitation.",
    "OB-GC-SC-DETERMINISTIC-V2": "the atomics rule applies, and the case's properties cover it. An exact pair succeeding with no spurious failure, and what it stores (sc-w-result, sc-w-low-bytes, sc-d-result, sc-d-all-bytes); each failure writing 1 and storing nothing (beside-fails, failure-stores-nothing, completed-clears, no-second-store); the destination aliases (rd-is-rs2-result, rd-is-rs1-result, rd-x0-stored); store permission before the failure code (permission-before-failure, translation-before-failure); and a target fault's address and what it keeps (target-fault-vaddr, fault-keeps-destination, target-fault-keeps-reservation).",
})
FEATURE_DISPOSITIONS.update({
    "OB-GC-COMPOSITION": "none applies: this states what the profile holds, and each extension's behaviour is that extension's own credit. misa names the letters and the base's width is witnessed (misa-letters, rv64i-width), and one form of each member executes (m-present, a-present, a-stored, f-present, d-present, c-present, zicsr-present, zifencei-present, zicntr-present, sstc-present).",
    "OB-EXT-CLOSURE": "the floating-point rule and the fetch rule apply, and the case's properties cover them as far as this statement reaches. D and F share registers, with boxing (d-narrows-to-f, f-boxed-in-d, f-reads-unboxed-as-nan); F's flags and rounding mode go through Zicsr (fcsr-holds-flags, fflags-through-zicsr, frm-through-zicsr, fcsr-composes); and C's parts by parcel, with the encoding Zcf would own read as C.LD (zca-present, zcd-stores, zcd-loads, zcf-absent-rd, zcf-absent-fd).",
    "OB-PRIV-REVISION": "the privilege and CSR rule applies, and the case's properties cover it as far as a revision shows. The CSRs this revision names read and hold as it says, in M and in S (mstatus-xlen-fields, menvcfg-exists, menvcfg-holds-stce, sstatus-view, stimecmp-in-s).",
    "OB-RVWMO": "the atomics rule applies, and the case's properties cover what one hart sees of it; a single hart earns no multicore or weak-memory claim, and the limitation says so. A hart's own store and three fences (own-store, fence-all, fence-rw, fence-tso); each annotation on an AMO and on LR and SC (amo-plain, amo-aq, amo-rl, amo-aqrl, amo-all-stored, lr-aq, sc-rl).",
    "OB-PRIV-INSNS": "the privilege and CSR rule applies, and the case's properties cover what this statement names: each of the four executes where it may (mret-executes, sret-executes, wfi-retires, sfence-retires). Refusal below their modes is REQ-GC-PRIV-INSNS's case.",
    "OB-GC-PRIV-INSNS-V3": "the privilege and CSR rule and the wait rule apply, and the case's properties cover them. Each return at and below its mode and under TSR (mret-in-s, mret-in-u, sret-in-u, sret-tsr, sret-in-m, sret-reached-u, ecall-from-s); what each pops and where each lands, MPRV among them (mret-pops, sret-pops, mret-clears-mprv, mret-sets-pc, sret-sets-pc); wfi waking regardless of the global enables and of mideleg, and refused in U and under TW, on a reference whose own wfi waits (wfi-wakes-undelegated, wfi-wakes-delegated, wfi-in-s, wfi-tw, wfi-in-u); sfence.vma refused, and its rs1 and rs2 cases, with no write to the page's data between fences (sfence-in-u, sfence-tvm, before-the-fences, sfence-all, sfence-va, sfence-asid, sfence-va-asid).",
})
FEATURE_DISPOSITIONS.update({
    "OB-NO-H": "the privilege and CSR rule applies, and the case's properties cover what a hart without H shows. misa's bit and the state H would add, each read back after a write that tried to set it (misa-no-h, mstatus-no-h-bits, mideleg-no-vs, mie-no-vs), on the one hart (one-hart). A hart with H is the retained effect's.",
    "OB-NO-PMP": "the translation and protection rule applies, and the case's properties cover what a hart without PMP shows: a load and a store at S's privilege and at U's reach memory with nothing configured (s-load, s-store, u-load, u-store). A hart with entries implemented is the retained effect's.",
})
LEG_ORDER = ("source-located-expectations", "boundary-fixtures", "matched-reference-comparison",
             "repeated-execution", "discriminating-control", "record-linkage", "currentness",
             "risk-method", "feature-rules", "form-coverage", "statement-trace")


class Refused(Exception):
    """The inputs cannot be measured honestly; nothing is reported as pending or satisfied."""


@dataclass(frozen=True)
class Leg:
    id: str
    disposition: str  # satisfied | pending
    measured: str


def _require(condition, reason: str) -> None:
    if not condition:
        raise Refused(reason)


def _bounded_bytes(path: Path, limit: int = DOCUMENT_BYTES) -> bytes:
    try:
        size = path.stat().st_size
    except OSError as error:
        raise Refused(f"unavailable: {path}: {type(error).__name__}") from error
    _require(0 < size <= limit, f"{path} is {size} bytes, outside 1..{limit}")
    return path.read_bytes()


def _forms(path: Path) -> list:
    try:
        return S.parse(_bounded_bytes(path).decode("utf-8"), str(path))
    except (S.SexpError, UnicodeError) as error:
        raise Refused(f"unreadable {path}: {error}") from error


def _one_form(path: Path, head: str):
    found = [f for f in _forms(path) if isinstance(f, list) and f and str(f[0]) == head]
    _require(len(found) == 1, f"exactly one ({head} …) expected in {path}")
    return found[0]


def _one(form, name):
    found = S.children(form, name)
    return found[0][1] if len(found) == 1 and len(found[0]) == 2 else None


def _strings(form, name) -> list[str]:
    return [str(c[1]) for c in S.children(form, name) if len(c) == 2]


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _leg(legs: list[Leg], leg_id: str, ok: bool, measured: str) -> None:
    legs.append(Leg(leg_id, "satisfied" if ok else "pending", measured))


def _declared_forms(case_dir: Path):
    """The case declaration's `second_method` and `adversarial` forms, each `None` when undeclared.

    Read structurally, as the planned record is: the finite method review validates the declaration through the
    case reader when it prepares the case, and its manifest pins it. A directory without one declares neither.
    """
    path = case_dir / "case.sexp"
    if not path.is_file():
        return None, None
    top = _one_form(path, "case")
    found = [S.children(top, name) for name in ("second_method", "adversarial")]
    _require(all(len(forms) <= 1 for forms in found), "a case declares at most one second method and one adversarial case")
    return tuple(forms[0] if forms else None for forms in found)


def _declared_limitation(case_dir):
    """What the case's own declaration says it does not witness: the limits a statement trace may name."""
    path = case_dir / "case.sexp"
    return str(_one(_one_form(path, "case"), "limitation") or "") if path.is_file() else ""


def _declared_cells(case_dir):
    """Each property's cell, from the case's own declaration: the planned record does not carry it."""
    path = case_dir / "case.sexp"
    if not path.is_file():
        return {}
    return {str(_one(p, "id")): str(_one(p, "cell")) for p in S.children(_one_form(path, "case"), "property")}


def _risk_method(risk, second, adversarial, producers, pairs, witnesses, baseline):
    """The risk-method leg as (satisfied, measured) — P4-SYSTEM.14 a43b-2a, D2.

    Undeclared, low and medium risk need no second method and high or critical risk stays pending. A declaration
    is judged at any risk by five conditions read from the record, never restated by it: (1) a second method of a
    named kind and an adversarial case are both declared; (2) its producers are two or more producers of the record
    with distinct versions ("Two wrappers around one producer do not satisfy this requirement"); (3) every pair of
    them is a recorded producer pair and their shared inputs are exactly the declared common inputs ("the producers
    and common inputs recorded"); (4) no such pair is recorded as sharing the subsystem, and what is independently
    derived is named — reported beside the recorded ancestry, which earns no independence credit; (5) every
    adversarial property is a declared property of a capture whose baseline agrees (executed, not only named).
    """
    if second is None and adversarial is None:
        return risk in LOW_RISK, f"risk {risk}: " + (
            "no second method required" if risk in LOW_RISK else "second method and adversarial case undeclared")
    kind = str(_one(second, "kind")) if second is not None else None
    ids = _strings(second, "producer_ids") if second is not None else []
    common = sorted(_strings(second, "common_input_ids")) if second is not None else []
    derived = str(_one(second, "independently_derived") or "").strip() if second is not None else ""
    versions = {str(_one(producers[i], "version")) for i in ids if i in producers}
    recorded = {frozenset((str(_one(p, "left")), str(_one(p, "right")))): p for p in pairs}
    joined = [recorded.get(frozenset(pair)) for pair in combinations(ids, 2)]
    found = [p for p in joined if p is not None]
    shared = sorted(set.intersection(*(set(_strings(p, "shared_input_ids")) for p in found))) if found else []
    ancestry = sorted({str(_one(p, "assessment")) for p in found})
    props = _strings(adversarial, "property_ids") if adversarial is not None else []
    c1 = second is not None and adversarial is not None and kind in SECOND_METHODS
    c2 = len(ids) >= 2 and all(i in producers for i in ids) and len(versions) == len(ids)
    c3 = bool(joined) and len(found) == len(joined) and bool(common) and shared == common
    c4 = bool(found) and "shared" not in ancestry and bool(derived)
    c5 = bool(props) and set(props) <= set(witnesses) and baseline == "AGREE"
    failed = [text for ok, text in (
        (c1, "(1) a second method of a named kind and an adversarial case are not both declared"),
        (c2, f"(2) producers {ids} are not two or more producers of the record with distinct versions"),
        (c3, f"(3) common inputs {common} are not the recorded pairs' shared inputs {shared}"),
        (c4, f"(4) ancestry {ancestry or '(no recorded pair)'}: a pair recorded as shared, or nothing independently "
             "derived named"),
        (c5, f"(5) adversarial properties {props} are not all declared properties of an agreeing capture "
             f"(baseline {baseline})"),
    ) if not ok]
    if failed:
        return False, f"risk {risk}: second method not satisfied — " + "; ".join(failed)
    return True, (f"risk {risk}: second method {kind} by {ids} on common inputs {common}; independently derived: "
                  f"{derived}; ancestry {ancestry}: no independence credit; adversarial {props} "
                  f"({str(_one(adversarial, 'failure_mode') or '')}) executed, baseline {baseline}")


def _config_effect(root: Path, case_dir: Path, profile_dir: Path, case_id: str, expectation_path: Path, producers: dict,
                   declared_steps: set) -> tuple[bool, str]:
    """The `implementation-defined` row's behavior-changing control, as (satisfied, measured) (decision_reference-config-per-case.md).

    `<case>.effect.sexp` names what ran, beside its raw trace (`measure_config_effect.py`); it carries no verdict and
    none is trusted. The pins are read against the case's own bytes, and the first difference is re-derived from the
    retained trace and the case's baseline expectation: it must fall at a declared property's step. No process runs.
    """
    record_path = profile_dir / "reference" / f"{case_id}.effect.sexp"
    if not record_path.is_file():
        return False, "no retained configuration effect"
    import measure_config_effect as Effect
    record = _one_form(record_path, "config_effect")
    trace = _bounded_bytes(record_path.with_name(f"{case_id}.effect.trace"), Effect.TRACE_BYTES)
    case_config = _digest(_bounded_bytes(case_dir / "reference-config.json"))
    alternative = _one(record, "alternative_config_sha256")
    try:
        declared, named = Effect.alternative_config(root, case_id)
    except Effect.REFUSALS as refused:
        return False, f"the case's declared alternative refuses: {refused}"
    reference = producers.get("reference")
    pins = (("its case", _one(record, "case_id") == case_id),
            ("the guest", _one(record, "guest_sha256") == _digest(_bounded_bytes(case_dir / "guest.elf"))),
            ("the case's configuration", _one(record, "case_config_sha256") == case_config),
            ("the reference producer's binary", reference is not None and f"sha256:{_one(record, 'binary_sha256')}" == str(_one(reference, "version"))),
            ("a different configuration", alternative != case_config),
            (named, alternative == _digest(declared)),
            ("its trace", _one(record, "trace_sha256") == _digest(trace) and _one(record, "trace_bytes") == len(trace)))
    unpinned = [name for name, held in pins if not held]
    if unpinned:
        return False, "the retained effect does not pin " + ", ".join(unpinned)
    try:
        result = Effect.Sail.compare_observations(Effect.D.load_expectations(expectation_path), trace.decode("utf-8"))
    except (Effect.Sail.SailError, Effect.D.DossierError, UnicodeError) as error:
        return False, f"the retained effect does not compare: {error}"
    difference = result.gpr_difference
    if result.verdict != "DIVERGE" or difference is None:
        return False, f"the retained effect reads {result.verdict}: no observed effect"
    if difference.step_n not in declared_steps:
        return False, f"the retained effect first differs at step {difference.step_n}, no declared property's"
    return True, f"observed effect under {named}: {result.detail}"


def _walk_record(case_dir: Path, profile_dir: Path, case_id: str, producers: dict) -> tuple[bool, str]:
    """A retained comparison of the case's page-table reads, re-derived from its two raw traces; no process runs."""
    import measure_walk_trace as Walk
    record_path = profile_dir / "reference" / f"{case_id}.walk.sexp"
    if not record_path.is_file():
        return False, "no retained page-table comparison"
    record = _one_form(record_path, "walk_trace")
    reference = _bounded_bytes(record_path.with_name(f"{case_id}.walk.trace"), Walk.TRACE_BYTES)
    engine = _bounded_bytes(record_path.with_name(f"{case_id}.walk.lab"), Walk.TRACE_BYTES)
    producer = producers.get("reference")
    pins = (("its case", _one(record, "case_id") == case_id),
            ("the guest", _one(record, "guest_sha256") == _digest(_bounded_bytes(case_dir / "guest.elf"))),
            ("the case's configuration", _one(record, "case_config_sha256") == _digest(_bounded_bytes(case_dir / "reference-config.json"))),
            ("the reference producer's binary", producer is not None and f"sha256:{_one(record, 'binary_sha256')}" == str(_one(producer, "version"))),
            ("the reference's trace", _one(record, "reference_trace_sha256") == _digest(reference)),
            ("the engine's trace", _one(record, "engine_trace_sha256") == _digest(engine)))
    unpinned = [name for name, held in pins if not held]
    if unpinned:
        return False, "the retained page-table comparison does not pin " + ", ".join(unpinned)
    try:
        return Walk.compare(reference.decode("utf-8"), engine.decode("utf-8"))
    except UnicodeError as error:
        return False, f"the retained page-table comparison does not read: {error}"


def _source_specific_row(case_dir: Path, profile_dir: Path, root: Path, case_id: str, requirement_id: str, control_property: str, producers: dict) -> tuple[bool, str]:
    """The `source-specific` row: a disposition declared for this requirement, naming this case's own control (decision_the-seventeen-called.md)."""
    import dispositions as Dis
    try:
        row = Dis.load(root, profile_dir).get(requirement_id)
    except Dis.DispositionRefused as refused:
        return False, f"its dispositions refuse: {refused}"
    if row is None:
        return False, f"no disposition declared for {requirement_id}"
    if row["kind"] != "case":
        return False, f"{row['id']} closes through a record, not a case"
    if row["control_property"] != control_property:
        return False, f"{row['id']} names the control {row['control_property']}, and this case's is {control_property}"
    measured = f"disposition {row['id']} declared, its control {control_property}"
    if not row["walk_record"]:
        return True, measured
    held, walks = _walk_record(case_dir, profile_dir, case_id, producers)
    return held, f"{measured}; {walks}"


def _category_row(root: Path, case_dir: Path, profile_dir: Path, case_id: str, semantics: dict, expectation_path: Path,
                  producers: dict, declared_steps: set, requirement_id: str, control_property: str) -> tuple[bool, str]:
    """The policy's source-semantic row beyond the matched comparison, as (satisfied, measured text to append)."""
    category = semantics["category"]
    if category == "defined":
        return True, ""
    if category == "implementation-defined":
        selection = bool(str(semantics.get("detail") or "").strip())
        effect, measured = _config_effect(root, case_dir, profile_dir, case_id, expectation_path, producers, declared_steps)
        return selection and effect, f"; category {category}: selection {'recorded' if selection else 'unrecorded'}; {measured}"
    if category == "source-specific":
        held, measured = _source_specific_row(case_dir, profile_dir, root, case_id, requirement_id, control_property, producers)
        return held, f"; category {category}: {measured}"
    return False, f"; category {category}: no row measured for it here"


def measure_policy(root: Path, *, method: dict, case_id: str = CASE_ID) -> dict:
    """The leg table for one retained case, given the finite method review's plain result."""
    root = Path(root)
    _require(isinstance(method, dict) and isinstance(method.get("disposition"), str), "method result is not a plain record")
    case_dir = root / "evidence" / case_id
    planned = _one_form(case_dir / "planned-experiment.sexp", "experiment")
    _require(_one(planned, "id") == case_id, "planned experiment id differs from the case")
    try:
        receipt = json.loads(_bounded_bytes(case_dir / "verification.json").decode("utf-8"))
    except (ValueError, UnicodeError) as error:
        raise Refused(f"unreadable receipt: {error}") from error
    _require(isinstance(receipt, dict) and receipt.get("case_id") == case_id, "receipt is not this case's object")
    profile = receipt.get("profile_id")
    _require(isinstance(profile, str) and profile, "receipt names no profile")
    _require(isinstance(receipt.get("qualification"), bool), "receipt lacks boolean qualification")
    verification = S.children(planned, "verification")
    _require(len(verification) == 1, "planned experiment needs exactly one verification form")
    properties = S.children(verification[0], "property")
    _require(1 <= len(properties) <= MAX_PROPERTIES, f"planned experiment declares no property, or more than {MAX_PROPERTIES}")
    graph = verification[0]  # the scoped graph: properties, inputs, producers and observations
    inputs = {str(_one(i, "id")): i for i in S.children(graph, "input")}
    producers = {str(_one(p, "id")): p for p in S.children(graph, "producer")}
    roles = {name: str(_one(form, "role")) for name, form in inputs.items()}

    profile_dir = root / "profiles" / profile
    try:
        reqs = {r["id"]: r for r in R.load(profile_dir / "requirements.sexp", root=root)}
        obligations = {o["id"]: o for o in R.load(profile_dir / "contract-obligations.sexp", root=root)}
    except (R.RecordRefused, S.SexpError, OSError) as error:
        raise Refused(f"{profile}: unreadable catalogue: {error}") from error
    first = properties[0]
    req_id = str(_one(first, "requirement_id"))
    _require(req_id in reqs, f"property names unknown requirement {req_id}")
    requirement = reqs[req_id]
    obligation_ids = _strings(first, "obligation_ids")
    for prop in properties[1:]:
        _require(str(_one(prop, "requirement_id")) == req_id, "every property must address the one requirement")
    category = requirement["source_semantics"]["category"]
    risk = requirement["risk"]

    # Expectation steps: the source-located expected observations.
    expectation_ids = [name for name, role in roles.items() if role == "expectation" and name != "mutant-expectation"]
    _require(len(expectation_ids) == 1, "exactly one baseline expectation input expected")
    expectation_path = root / str(_one(inputs[expectation_ids[0]], "path"))
    expectations = _one_form(expectation_path, "expectations")
    steps = {}
    for step in S.children(expectations, "step"):
        n = _one(step, "n")
        _require(isinstance(n, int) and n not in steps, "expectation steps must carry unique integer n")
        steps[n] = dict(insn=str(_one(step, "insn") or ""), derivation=str(_one(step, "derivation") or ""),
                        source=str(_one(step, "source") or ""), writes=any(S.children(w, "write") for w in S.children(step, "writes")))
    _require(steps, "expectation file declares no step")
    witnesses = {}
    for prop in properties:
        gw = S.children(prop, "gpr_witness")
        _require(len(gw) == 1, "every property needs exactly one gpr_witness")
        step_n, register = _one(gw[0], "step_n"), str(_one(gw[0], "register"))
        _require(isinstance(step_n, int) and step_n in steps, "witness step is not an expectation step")
        witnesses[str(_one(prop, "id"))] = (step_n, register)
    controls = S.children(graph, "control_run")
    _require(len(controls) == 1, "planned experiment needs exactly one control_run")
    named = _strings(controls[0], "property_ids")
    _require(len(named) == 1 and named[0] in witnesses, "control_run must name one declared property")
    witness_step, witness_register = witnesses[named[0]]

    legs: list[Leg] = []
    # source-located-expectations
    unlocated = [n for n, s in steps.items() if not (s["source"].strip() and s["derivation"].strip())]
    refs = requirement["source_refs"]
    cited = any(r["source_id"] in steps[witness_step]["source"] and r["locator"] in steps[witness_step]["source"] for r in refs)
    expected = producers.get("expected")
    reference_only = {name for name, role in roles.items() if role in ("reference-config", "reference-identity")}
    expected_inputs = set(_strings(expected, "input_ids")) if expected is not None else set()
    own_output = expected is None or bool(expected_inputs & reference_only) or not (expected_inputs & set(expectation_ids))
    _leg(legs, "source-located-expectations", not unlocated and cited and not own_output,
         f"{len(steps) - len(unlocated)} of {len(steps)} steps carry derivation+source; witness step {witness_step} "
         f"{'cites' if cited else 'does not cite'} {req_id}'s source; expected producer "
         f"{'reads only its own inputs' if not own_output else 'is missing or reads reference inputs'}")
    # boundary-fixtures
    boundary_steps = sorted(n for n, s in steps.items() if any(marker in s["source"] for marker in BOUNDARY_MARKERS))
    declared_steps = {step for step, _ in witnesses.values()}
    undeclared = [n for n in boundary_steps if n not in declared_steps]
    _leg(legs, "boundary-fixtures", bool(boundary_steps) and not undeclared,
         f"{len(boundary_steps)} directed boundary rows present at steps {boundary_steps}; "
         f"{len(boundary_steps) - len(undeclared)} predeclared as properties")
    # runs from the receipt
    comparison = receipt.get("comparison") if isinstance(receipt.get("comparison"), dict) else {}
    runs = {r.get("run_kind"): r for r in comparison.get("runs", []) if isinstance(r, dict)}

    def verdict(kind):
        run = runs.get(kind) or {}
        inner = run.get("comparison") if isinstance(run.get("comparison"), dict) else {}
        return inner.get("verdict"), inner.get("gpr_difference")

    method_ok = (method.get("disposition") == "satisfied" and method.get("capture_binding") == "matched"
                 and method.get("record_disposition") == "valid")
    rule = str(_one(verification[0], "comparison_rule") or "")
    kinds = _strings(first, "observation_kinds")
    baseline, _ = verdict("baseline")
    row, row_measured = _category_row(root, case_dir, profile_dir, case_id, requirement["source_semantics"], expectation_path,
                                      producers, declared_steps, requirement["id"], named[0])
    _leg(legs, "matched-reference-comparison", method_ok and baseline == "AGREE" and bool(rule) and bool(kinds) and row,
         f"method {method.get('disposition')}; baseline {baseline}; rule {rule or '(none)'}; vocabulary {kinds or '(unnamed)'}{row_measured}")
    repeat, _ = verdict("repeat")
    _leg(legs, "repeated-execution", repeat == "AGREE", f"repeat {repeat}")
    control, diff = verdict("control")
    diff = diff if isinstance(diff, dict) else {}
    observed = {str(pair[0]) for pair in diff.get("observed", []) if isinstance(pair, (list, tuple)) and pair}
    at_witness = diff.get("step_n") == witness_step and observed == {witness_register}
    _leg(legs, "discriminating-control", control == "DIVERGE" and at_witness,
         f"control {control} at step {diff.get('step_n')} registers {sorted(observed)}; witness step {witness_step} {witness_register}")
    # record-linkage
    unknown = [ob for ob in obligation_ids if ob not in obligations]
    unnamed = [ob for ob in obligation_ids if ob in obligations and ob not in requirement["obligation_ids"]]
    runner = any(role == "collector" for role in roles.values())
    limitations = receipt.get("limitations")
    linked = (bool(obligation_ids) and not unknown and not unnamed and runner and expected is not None
              and isinstance(limitations, list) and bool(limitations))
    _leg(legs, "record-linkage", linked,
         f"obligations {obligation_ids} ({'effective and named' if not unknown and not unnamed else 'unknown ' + str(unknown) + ' unnamed ' + str(unnamed)}); "
         f"tracked runner {'named' if runner else 'missing'}; expectation producer {'named' if expected is not None else 'missing'}; "
         f"{len(limitations) if isinstance(limitations, list) else 0} limitation(s)")
    # currentness
    manifest = _one_form(case_dir / "dependencies.sexp", "dependencies")
    policy_rel = f"profiles/{profile}/EVIDENCE_POLICY.md"
    pins = {str(_one(i, "path")): str(_one(i, "sha256")) for i in S.children(manifest, "input")}
    policy_pin = pins.get(policy_rel)
    policy_now = _digest(_bounded_bytes(root / policy_rel)) if (root / policy_rel).is_file() else None
    _leg(legs, "currentness", policy_pin is not None and policy_pin == policy_now and method_ok,
         f"policy {'pinned' if policy_pin else 'unpinned'} and {'current' if policy_pin and policy_pin == policy_now else 'changed since the pin'}; "
         f"method binding {method.get('capture_binding')}")
    # risk-method (a43b-2a, D2): the case's declared second method and adversarial case, judged against the record
    second, adversarial = _declared_forms(case_dir)
    _leg(legs, "risk-method", *_risk_method(risk, second, adversarial, producers, S.children(graph, "producer_pair"),
                                            witnesses, baseline))
    # feature-rules
    feature = [FEATURE_DISPOSITIONS.get(ob) for ob in obligation_ids]
    _leg(legs, "feature-rules", bool(obligation_ids) and all(feature),
         "; ".join(f"{ob}: {d or 'feature disposition undeclared'}" for ob, d in zip(obligation_ids, feature)) or "no obligation")
    # form-coverage
    required = sorted(requirement["insns"])
    mnemonic = lambda s: s["insn"].split()[0].lower() if s["insn"].split() else ""
    exercised = sorted({mnemonic(s) for s in steps.values()} & set(required))
    # A form that writes no GPR (a branch, a store, a load to x0) has no change to witness at its own step. In this vocabulary it is
    # predeclared when a property's cell names it and that property's witness comes after a step of the form (P4-SYSTEM.14 a46-4):
    # the read that observes it, stated by the property. A form with any GPR write, or never exercised, gets no such route.
    silent = {f for f in required if not any(s["writes"] for s in steps.values() if mnemonic(s) == f)}
    cells = _declared_cells(case_dir)
    read_after = sorted({f for f in silent for pid, (n, _) in witnesses.items()
                         if cells.get(pid) == "form:" + f and any(mnemonic(steps[m]) == f for m in steps if m < n)})
    predeclared = sorted(({mnemonic(steps[n]) for n in declared_steps} | set(read_after)) & set(required))
    # a43a-2f: a state requirement (REQ-D-XLEN: the register width and the address space) names no form, so there is
    # none to cover; its predeclared witnesses are its coverage. a47-3: so does a configuration requirement (REQ-D-IALIGN-16:
    # where an instruction may start). a51-1: so does a memory requirement (REQ-D-RVWMO: what one hart sees of the model). An instruction
    # or event requirement naming no form stays pending: it is a catalogue fault, and REQ-D-PRIV-INSNS's was fixed at a51-1.
    vacuous = requirement["kind"] in ("state", "configuration", "memory") and not required
    _leg(legs, "form-coverage", vacuous or (bool(required) and predeclared == required),
         f"a {requirement['kind']} requirement names no form: coverage is vacuous, its {len(witnesses)} predeclared witnesses stand for it"
         if vacuous else
         f"{len(predeclared)} of {len(required)} forms predeclared {predeclared}; {len(exercised)} exercised {exercised}"
         + (f"; writing no GPR, read after their own step: {read_after}" if read_after else ""))

    # statement-trace (a49-1): every clause of the requirement's statement, in order, names a witness or a limit the case states.
    try:
        clauses = ST.load_trace(root, profile_dir).get(req_id)
    except ST.TraceRefused as error:
        raise Refused(f"{profile}: unreadable statement trace: {error}") from error
    traced, trace_measured = (False, f"{req_id} has no statement trace") if clauses is None else ST.measure(
        requirement["statement"], clauses, list(witnesses), _declared_limitation(case_dir))
    _leg(legs, "statement-trace", traced, trace_measured)

    assert [leg.id for leg in legs] == list(LEG_ORDER)
    missing = [leg.id for leg in legs if leg.disposition != "satisfied"]
    stale = method.get("disposition") == "stale"
    findings = []
    if receipt.get("qualification") is True and missing:
        findings.append("receipt claims qualification the policy legs refuse: " + ", ".join(missing))
    if not method_ok and not stale:
        findings.append(f"finite method not satisfied ({method.get('disposition')}); legs measured but blocked")
    if stale:
        disposition = "invalidated"
    elif not method_ok:
        disposition = "blocked"
    else:
        disposition = "satisfied" if not missing else "pending"
    # a42ay: the credit is a record in the profile's credits.sexp (scripts/credit_records.py), never a
    # flag of this measurement or of the receipt. A current record naming this case and requirement
    # reports `credited`; one over a measurement that is not `satisfied` is a finding.
    try:
        credits = CR.current_credits(root, profile_dir)
    except CR.CreditRefused as error:
        raise Refused(f"{profile}: {error}") from error
    naming = [c for c in credits if c["case_id"] == case_id and c["requirement_id"] == req_id]
    credited_now = any(c["disposition"] == "current" for c in naming)
    for c in naming:
        if c["disposition"] != "current":
            findings.append(f"credit {c['id']} names this case but lapsed: {c['reasons'][0]}")
        elif disposition != "satisfied":
            findings.append(f"credit {c['id']} names this case while its measurement is {disposition}")
    return dict(format_version=FORMAT, case_id=case_id, profile_id=profile, requirement_id=req_id,
                obligation_ids=obligation_ids, category=category, risk=risk,
                method={k: method.get(k) for k in ("disposition", "reason", "capture_binding", "record_disposition",
                                                    "charged_read_bytes", "record_sha256", "planned_sha256")},
                invalidated_by=(str(method.get("reason") or "finite method stale") if stale else None),
                legs=[asdict(leg) for leg in legs], missing=missing, findings=findings,
                coverage=dict(required=required, exercised=exercised, predeclared=predeclared),
                boundary=dict(present=boundary_steps, predeclared=sorted(declared_steps & set(boundary_steps))),
                disposition=disposition, credited=credited_now, credit_ids=[c["id"] for c in naming],
                limitations=["measurement of declared bytes only; grants no qualification, obligation or CPU credit",
                             "a crediting disposition is a separately owned record (credits.sexp) that cites a satisfied measurement; `credited` reports that record, never this measurement",
                             "an invalidated measurement is superseded by the next capture, never repaired by relabelling",
                             "boundary rows and forms are read from the expectation file, not inferred from the chapter"])


def review_policy(root: Path, *, case_id: str = CASE_ID) -> dict:
    """Compose the finite method review on the real tree, then measure the legs."""
    import review_div_method as Method
    _require(Path(root).resolve() == Method.ROOT.resolve(), "the finite method review is bound to the repository root")
    _require(case_id in Method.RETAINED_CAPTURES, f"unsupported: no reviewed capture for {case_id}")
    return measure_policy(root, method=asdict(Method.review_method(case_id=case_id)), case_id=case_id)


def review_every(root: Path) -> list[dict]:
    """Every case the finite method review holds a reviewed capture for, in its order (a43a-2f)."""
    import review_div_method as Method
    return [review_policy(root, case_id=case_id) for case_id in Method.RETAINED_CAPTURES]


def summary(table: dict) -> tuple[int, str]:
    satisfied = sum(1 for leg in table["legs"] if leg["disposition"] == "satisfied")
    line = (f"DIV-POLICY: {table['disposition']} — {satisfied} of {len(table['legs'])} legs satisfied"
            + (f"; missing {', '.join(table['missing'])}" if table["missing"] else "")
            + (f"; invalidated by {table['invalidated_by']}" if table.get("invalidated_by") else "")
            + (f"; FINDING {'; '.join(table['findings'])}" if table["findings"] else "")
            + (f"; credited by {', '.join(table['credit_ids'])}" if table.get("credited") else "; no qualification credit"))
    return (1 if table["findings"] else 0), line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure the retained DIV case against the policy legs.")
    parser.add_argument("--root", default=str(HERE.parent))
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--case", default=CASE_ID)
    selection.add_argument("--every-retained", action="store_true",
                           help="every case with a reviewed capture, one summary line each; the worst exit code")
    parser.add_argument("--method-json", help="a plain method result file instead of running the finite method review")
    parser.add_argument("--json", action="store_true", help="the leg table on stdout, the summary on stderr")
    args = parser.parse_args(argv)
    if args.every_retained and args.method_json:
        parser.error("--every-retained runs the finite method review itself; --method-json selects one case")
    try:
        if args.every_retained:
            tables = review_every(Path(args.root))
            payload = json.dumps(tables, indent=2) + "\n"
            _require(len(payload.encode()) <= DOCUMENT_BYTES * len(tables), "leg tables exceed 64 KiB per case")
        elif args.method_json:
            try:
                method = json.loads(_bounded_bytes(Path(args.method_json)).decode("utf-8"))
            except (ValueError, UnicodeError) as error:
                raise Refused(f"unreadable method result: {error}") from error
            table = measure_policy(Path(args.root), method=method, case_id=args.case)
        else:
            table = review_policy(Path(args.root), case_id=args.case)
    except Refused as error:
        print(f"DIV-POLICY: refused — {error}", file=sys.stderr)
        return 2
    if args.every_retained:
        results = [(table["case_id"], *summary(table)) for table in tables]
        if args.json:
            sys.stdout.write(payload)
        for case_id, _, line in results:
            print(f"{case_id}: {line}", file=sys.stderr if args.json else sys.stdout)
        return max(code for _, code, _ in results)
    code, line = summary(table)
    if args.json:
        payload = json.dumps(table, indent=2) + "\n"
        _require(len(payload.encode()) <= DOCUMENT_BYTES, "leg table exceeds the 64 KiB document bound")
        sys.stdout.write(payload)
        print(line, file=sys.stderr)
    else:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
