#!/usr/bin/env bash
# run_synth_probes.sh — the DSP-REVIEW.6 synthetic stress fixture (task card T010).
#
# ⛔ SYNTHETIC. The `synth24` descriptors below describe NO real processor — they exist to
# measure where this project's pipeline refuses shapes a DSP would need. Its passing
# evidence may NEVER be cited for a real DSP claim (the leaf's acceptance).
#
# Four shapes pushed through the REAL pipeline (the state generator and the schema layer),
# each pinned to its measured refusal. The suite is GREEN exactly while the boundary is
# where the pins say; the day the pipeline genuinely supports a shape, the pin goes stale
# and the suite turns RED — the fixture's purpose is measuring the boundary moving.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
DIR="docs/tasks/artifacts/dsp-review/synth"
pass=0; fail=0

probe() { # $1 label  $2 expected rc  $3 expected substring  $4… the command
  local label="$1" want_rc="$2" want="$3"; shift 3
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" = "$want_rc" ] && printf '%s' "$out" | grep -qF "$want"; then
    pass=$((pass+1)); printf '  PASS  %s\n' "$label"
  else
    fail=$((fail+1)); printf '  FAIL  %s (rc=%s, want %s; wanted %s)\n%s\n' \
      "$label" "$rc" "$want_rc" "$want" "$out" >&2
  fi
}

probe "nonstandard width (24-bit) refuses by name" 2 \
  "masked fixed-width storage for nonstandard widths is generator work" \
  python3 scripts/gen_state.py --state "$DIR/state.sexp" \
    --arith crates/semulith-core/src/arith.rs --out /dev/null
probe "a second address space refuses by name" 1 'undeclared field "memory_spaces"' \
  python3 scripts/check_sexp_schema.py "$DIR/state-spaces.sexp" schema/state.sexp
probe "a packet construct refuses by name" 1 'undeclared field "packet"' \
  python3 scripts/check_sexp_schema.py "$DIR/packet.sexp" schema/fragment.sexp
probe "a delayed effect refuses by name" 1 'undeclared operator "delay"' \
  python3 scripts/check_sexp_schema.py "$DIR/delayed.sem.sexp" schema/semantics.sexp

echo "synth probes: $pass pass / $fail fail"
[ "$fail" -eq 0 ]
