#!/usr/bin/env bash
# scripts/check_delivery_provenance.sh — DELIVERY-PROVENANCE (project doctrine).
#
# A supplied package arrives with a `MANIFEST.sha256`. That manifest is a record of WHAT WAS
# DELIVERED, and some of its rows name files this repository exists to change. Left as a
# root-level artifact it invites `shasum -c` while containing rows whose failure is already
# scheduled — and a check whose failure is expected trains its reader to skip it, after which
# it silently stops covering the rows that were still meaningful.
#
# So every manifest row carries exactly one DISPOSITION, declared as DATA in the package's
# `dispositions.tsv` (not as prose), and this check re-derives the ones that are supposed to
# hold:
#
#   frozen-in-place  the delivered bytes, still at the delivered path   -> hash re-derived
#   relocated        the delivered bytes, moved to `current_path`       -> hash re-derived
#   live             this repository owns it now; drift is expected     -> existence only
#
# ⛔ There is no fourth, unstated category. A manifest row with no disposition, or a
# disposition naming a path the manifest does not list, is a BREACH — that asymmetry is the
# whole point: it is how a row quietly leaves coverage.
#
# ⚠️ HONEST LIMIT: this proves the delivered bytes are still the bytes, and that every row's
# treatment was declared. It says nothing about whether the delivered content was CORRECT.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

# ── hashing helper: refuse rather than skip if no hasher exists ──────────────────────────────
sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  elif command -v shasum   >/dev/null 2>&1; then shasum -a 256 "$1" | cut -d' ' -f1
  else return 3; fi
}
if ! sha256_of /dev/null >/dev/null 2>&1; then
  echo "DELIVERY-PROVENANCE: REFUSED — no sha256sum or shasum on PATH; this check cannot judge." >&2
  exit 2
fi

# ── verify one package directory, resolving paths against $2 ────────────────────────────────
# $1 = package directory (holds MANIFEST.sha256 + dispositions.tsv)
# $2 = root the manifest/disposition paths are relative to
# Writes findings to stdout; returns nonzero on breach.
verify_package() {
  local pkg="$1" base="$2" bad=0
  local manifest="$pkg/MANIFEST.sha256" disp="$pkg/dispositions.tsv"

  [ -f "$manifest" ] || { echo "  MISSING $manifest"; return 1; }
  [ -f "$disp" ]     || { echo "  MISSING $disp (the dispositions are DATA, not prose)"; return 1; }

  local tmp; tmp="$(mktemp -d)"
  awk 'NF>=2 {print $2}' "$manifest" | sort > "$tmp/manifest_paths"
  awk -F'\t' '!/^#/ && NF>=3 {print $2}' "$disp" | sort > "$tmp/disposed_paths"

  local undeclared extra
  undeclared="$(comm -23 "$tmp/manifest_paths" "$tmp/disposed_paths")"
  extra="$(comm -13 "$tmp/manifest_paths" "$tmp/disposed_paths")"
  if [ -n "$undeclared" ]; then
    echo "  UNDECLARED manifest row(s) — no disposition, so their treatment is unstated:"
    printf '%s\n' "$undeclared" | sed 's/^/    /'; bad=1
  fi
  if [ -n "$extra" ]; then
    echo "  ORPHAN disposition(s) — declared for a path the manifest does not list:"
    printf '%s\n' "$extra" | sed 's/^/    /'; bad=1
  fi

  local frozen=0 relocated=0 live=0 line
  # ⛔ NOT `IFS=$'\t' read`: tab is IFS *whitespace*, so an empty field collapses and shifts
  # every later column — a row with a missing `current_path` would parse as a different row
  # entirely. Translate to a non-whitespace separator first. (Found by the sibling routing
  # checker's own RED arm; fixed here too because it is the same defect class, not a symptom.)
  while IFS= read -r line; do
    case "$line" in ''|'#'*) continue ;; esac
    IFS=$'\x1f' read -r kind mpath cpath <<<"${line//$'\t'/$'\x1f'}"
    case "$kind" in ''|'#'*) continue ;; esac
    [ -n "$cpath" ] || { echo "  INCOMPLETE disposition row for '$mpath' — no current_path"; bad=1; continue; }
    local want target
    want="$(awk -v p="$mpath" 'NF>=2 && $2==p {print $1}' "$manifest")"
    target="$base/$cpath"
    case "$kind" in
      frozen-in-place|relocated)
        if [ ! -f "$target" ]; then
          echo "  MISSING ($kind) $cpath"; bad=1; continue
        fi
        local got; got="$(sha256_of "$target")"
        if [ "$got" != "$want" ]; then
          echo "  DRIFTED ($kind) $cpath"
          echo "    delivered $want"
          echo "    current   $got"
          bad=1; continue
        fi
        [ "$kind" = frozen-in-place ] && frozen=$((frozen+1)) || relocated=$((relocated+1))
        ;;
      live)
        [ -f "$target" ] || { echo "  MISSING (live) $cpath"; bad=1; continue; }
        live=$((live+1))
        ;;
      *)
        echo "  UNKNOWN disposition '$kind' for $mpath (expected frozen-in-place|relocated|live)"
        bad=1
        ;;
    esac
  done < "$disp"

  rm -rf "$tmp"
  echo "  $pkg: $frozen frozen-in-place, $relocated relocated re-derived; $live live row(s) declared"
  return "$bad"
}

# ── self-test: the controls must be seen RED, or they are not known to work ──────────────────
self_test() {
  local t pass=0 fail=0 out
  t="$(mktemp -d)"; mkdir -p "$t/pkg" "$t/tree/moved"
  printf 'good\n' > "$t/tree/frozen.txt"
  printf 'good\n' > "$t/tree/moved/reloc.txt"
  printf 'anything\n' > "$t/tree/live.txt"
  local h; h="$(sha256_of "$t/tree/frozen.txt")"
  {
    printf '%s  frozen.txt\n' "$h"
    printf '%s  reloc.txt\n'  "$h"
    printf '%s  live.txt\n'   "$(sha256_of "$t/tree/live.txt")"
  } > "$t/pkg/MANIFEST.sha256"
  base_disp() {
    printf 'frozen-in-place\tfrozen.txt\tfrozen.txt\n'
    printf 'relocated\treloc.txt\tmoved/reloc.txt\n'
    printf 'live\tlive.txt\tlive.txt\n'
  }
  # ⛔ An arm asserts the VERDICT *and* the reason. A control that goes red for the wrong
  # reason is a control that cannot fail on the thing it was written for.
  arm() { # name expected_rc expected_substring
    out="$(verify_package "$t/pkg" "$t/tree" 2>&1)"; local rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1))
      printf 'DELIVERY-PROVENANCE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' \
        "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1))
      printf 'DELIVERY-PROVENANCE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' \
        "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }
  base_disp > "$t/pkg/dispositions.tsv"
  arm "GREEN all rows verify"          0 "1 frozen-in-place, 1 relocated"
  printf 'tampered\n' > "$t/tree/frozen.txt"
  arm "RED frozen row byte changed"    1 "DRIFTED (frozen-in-place) frozen.txt"
  printf 'good\n'     > "$t/tree/frozen.txt"
  printf 'tampered\n' > "$t/tree/moved/reloc.txt"
  arm "RED relocated row byte changed" 1 "DRIFTED (relocated) moved/reloc.txt"
  printf 'good\n'     > "$t/tree/moved/reloc.txt"
  printf 'changed-freely\n' > "$t/tree/live.txt"
  arm "GREEN live row may drift"       0 "1 live row(s) declared"
  base_disp | grep -v '^frozen-in-place' > "$t/pkg/dispositions.tsv"
  arm "RED manifest row undeclared"    1 "UNDECLARED manifest row"
  { base_disp; printf 'frozen-in-place\tghost.txt\tghost.txt\n'; } > "$t/pkg/dispositions.tsv"
  arm "RED orphan disposition"         1 "ORPHAN disposition"
  { base_disp | grep -v '^relocated'; printf 'relocated\treloc.txt\tnowhere/reloc.txt\n'; } > "$t/pkg/dispositions.tsv"
  arm "RED relocated target missing"   1 "MISSING (relocated) nowhere/reloc.txt"
  base_disp | sed 's/^live/invented/' > "$t/pkg/dispositions.tsv"
  arm "RED unknown disposition name"   1 "UNKNOWN disposition 'invented'"
  # The empty-field arm: with `IFS=$'\t' read` this row silently parsed as a DIFFERENT row.
  { base_disp | grep -v '^live'; printf 'live\tlive.txt\t\n'; } > "$t/pkg/dispositions.tsv"
  arm "RED disposition row incomplete" 1 "INCOMPLETE disposition row for 'live.txt'"
  rm -rf "$t"
  printf 'DELIVERY-PROVENANCE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

# ── the real run: every package directory under docs/provenance/ ─────────────────────────────
shopt -s nullglob
packages=(docs/provenance/*/)
if [ "${#packages[@]}" -eq 0 ]; then
  echo "DELIVERY-PROVENANCE: ok (no packages under docs/provenance/)"
  exit 0
fi
self_test >/dev/null 2>&1 || {
  echo "DELIVERY-PROVENANCE: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2
}
fail=0; report=""
for pkg in "${packages[@]}"; do
  pkg="${pkg%/}"
  out="$(verify_package "$pkg" "$ROOT")" || fail=1
  report="$report$out"$'\n'
done
if [ "$fail" -ne 0 ]; then
  { echo "DELIVERY-PROVENANCE: a delivered package no longer matches its declared dispositions."
    printf '%s' "$report"
    echo "  Fix the tree, or change the row's disposition in dispositions.tsv AND say why in DELIVERY.md."
    echo "  Never edit a frozen record to make it agree with the tree." ; } >&2
  exit 1
fi
printf 'DELIVERY-PROVENANCE: ok\n%s' "$report"
exit 0
