# The FP model layer's acceptance — correctness at scale, the second engine, the measured cost

- **Type:** `reference`
- **Date:** `2026-10-06`
- **Status:** `active`
- **Owner / source:** measured by `P4-SYSTEM.7` slice (e3) (the leaf's acceptance), closing
  [`decision_fp-backend-qualification.md`](decision_fp-backend-qualification.md); re-run at
  HEAD `c377bcc` (the tree's (e3) checklist carries the commands)

## The fact

The decision stands: rustc_apfloat `=0.2.3` behind the model layer `fp.rs`, which owns the
RISC-V policy and patches the backend's two genuine flag deviations. F (30 forms) and D (32)
execute in the tracked rv64gc engine through it. The evidence the acceptance asks for:

- **Correctness, spec-side and tracked** (FP-VECTORS gates both tables against the
  exact-rational reference `scripts/specfp.py` — neither SoftFloat, APFloat nor MPFR — which
  is itself re-checked against the host's hardware IEEE every run, agree 2131): 230 directed
  vectors (the rules) and 3,168 seeded fixtures across all 21 model-layer operations × both
  formats × every rounding mode (the breadth) — all pass.
- **Correctness at corpus scale** (scratch `fpcheck`, re-run at slice d3): `fp.rs` over the
  63,752-case slice-(a) corpus disagrees with the exact-rational reference on **0** cases;
  with MPFR on exactly the 24 signaling-NaN conversions this record's second amendment
  attributes to the oracle.
- **The engine end to end**: the 22 F/D guests (+ the two FP-state guests) satisfy their
  spec-derived expectations on the tracked engine (125/125 corpus) and on Sail 0.14 — **24
  AGREE of 24**, 927 steps. Sail's FP is SoftFloat, so that agreement is the ENCODING/STATE
  match (decode, the FS gate, NaN-boxing, flag accrual, reserved rounding modes) plus one
  more numeric opinion — the numeric independence is the fixtures' (EVD-04).
- **Performance on this host** (release, 2M iterations, black_box operands): the model
  layer costs f64 add 47.8 / mul 47.4 / div 122.7 ns, f32 add 46.2, fma 65.8, sqrt 83.7
  (f64) / 58.7 (f32), convert d→s 27.2 / s→d 6.8, to_int 5.5, from_int 8.2, min 4.3 — 2.8–6.9×
  the raw backend on the arithmetic core (8.3 / 6.9 / 44.5 ns measured in the same run). The
  premium is the exact OF/UF: every rounded result is evaluated a second time at the same
  precision over a 15-bit exponent. Acceptable for a laboratory model; a cheaper guard
  (re-evaluate only when the delivered result sits at a range edge) is named, not taken.
- **Ancestry**, unchanged: TestFloat's computed expectations are SoftFloat's and were never
  counted (`RK07`, EVD-04); the lineages that carry THIS closing evidence are LLVM APFloat
  (the backend), the exact-rational reference (written from the chapters), and the host's
  hardware IEEE (the reference's own judge) — slice (a)'s MPFR and softfloat legs stand as recorded above.
