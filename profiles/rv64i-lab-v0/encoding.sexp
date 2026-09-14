;; encoding.sexp — this unit's encoding COMPOSITION.
;;
;; ⭐ The unit does not carry a copy of any instruction. It names the fragments it composes, and
;; the fragments own the facts — which is the no-duplicated-fact rule from
;; `decision_canonical-definition-input` applied to the thing most tempting to copy. A second
;; RV64 profile reuses `riscv/rv64i` rather than duplicating 52 instructions that would then have
;; to be kept equal.
;;
;; ⛔ A composition is legal only if the union is conflict-free. `scripts/check_encoding_disjoint.py`
;; decides that — exhaustively, because a sampled answer is not a decision — and the check runs
;; before a fragment is adopted, not after a decoder misbehaves.
;;
;; The extension list is EMPTY on purpose. `rv64i-lab-v0` is RV64I with no extensions at all, which
;; is a deliberately constrained target: no `M` means the compiler must emit runtime calls for
;; multiply and divide, and that constraint is part of what this model exists to teach.

(encoding
  (profile "rv64i-lab-v0")
  (ilen 32)
  (compose
    (base "riscv/rv64i")
    (extensions))                    ; none — see the note above
  (fragment-root "definitions"))
