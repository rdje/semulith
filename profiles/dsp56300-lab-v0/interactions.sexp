;; interactions.sexp — the interaction matrix for `dsp56300-lab-v0` subset v0
;; (P3-BREADTH.7 slice 2). Six axes, 21 cells, every disposition resolving to a measured
;; mechanism or a cannot-arise reason. The axes are the subset's honest interaction
;; surface: progress (stepping + the step counter), stop (the typed ModelStop boundary),
;; loop (DO/REP machinery), stack (the 16-level hardware stack), alias (accumulator parts
;; and the SSH/SSL stack-top views), state (the canonical-dump / replay surface — the F6
;; census's consequence). Subset v0 claims nothing about interrupts, modes, or timing —
;; those axes do not exist here, and none is silently omitted from what IS declared.
;;
;; Guests are checkpoint-compared .a56 sources, so cells resolve through mechanisms
;; (the smoke agreement and the typed-stop discipline), not per-step expectation
;; documents — the vehicle declaration in profile.sexp carries the why.

(interactions (profile "dsp56300-lab-v0")
  (axis (id "progress") (covers "instruction stepping and the steps counter"))
  (axis (id "stop") (covers "the typed ModelStop boundary: outside-subset word, out-of-window access, stack overflow, budget exhausted, input refusal"))
  (axis (id "loop") (covers "DO/REP machinery: LA/LC/LF, the stacked loop levels, the end-of-pass rule"))
  (axis (id "stack") (covers "the 16-level hardware stack: JSR/RTS/DO pushes and pops, stale slots"))
  (axis (id "alias") (covers "accumulator parts (A2:A1:A0, B2:B1:B0) vs the whole accumulators; SSH/SSL as views of stack[SP]"))
  (axis (id "state") (covers "the canonical end-state dump — the observation and replay surface (the F6 census measured it complete)"))

  (cell (axis "progress") (axis "progress") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "progress") (axis "stop") (mechanism "dsp56300-typed-stop"))
  (cell (axis "progress") (axis "loop") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "progress") (axis "stack") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "progress") (axis "alias") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "progress") (axis "state") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "stop") (axis "stop") (degenerate "a stopped machine does not stop again — the runner halts at the first typed stop"))
  (cell (axis "stop") (axis "loop") (mechanism "dsp56300-typed-stop"))
  (cell (axis "stop") (axis "stack") (mechanism "dsp56300-typed-stop"))
  (cell (axis "stop") (axis "alias") (degenerate "accumulator-part move destinations refuse at decode, before any state change — no alias interaction can arise from a stopped instruction"))
  (cell (axis "stop") (axis "state") (mechanism "dsp56300-typed-stop"))
  (cell (axis "loop") (axis "loop") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "loop") (axis "stack") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "loop") (axis "alias") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "loop") (axis "state") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "stack") (axis "stack") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "stack") (axis "alias") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "stack") (axis "state") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "alias") (axis "alias") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "alias") (axis "state") (mechanism "dsp56300-smoke-agreement"))
  (cell (axis "state") (axis "state") (mechanism "dsp56300-smoke-agreement"))
)
