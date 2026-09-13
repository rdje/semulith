#!/usr/bin/env bash
# scripts/check_readme_routes.sh — README-ROUTING-CLOSURE (project doctrine).
#
# README_POLICY.md, "Routing pressure closure": moving content OUT of the landing page is not
# sufficient if the destination can become an unbounded neighbouring sink. In one measured
# adoption, README status/history guidance routed overflow into an unchecked neighbouring
# status file; that file reached 1,547,057 bytes, 94.7% of it dated changelog content. The cap
# had displaced the pressure, not removed it.
#
# So this check closes the loop:
#
#   1. Every relative destination the landing page LINKS to is governed by a registry row.
#   2. Every path-shaped destination the README guard ACTUALLY EMITS in its failure guidance
#      is governed too — derived from the guard's real output, not from a hand-kept list,
#      because a hint that names an ungoverned sink is exactly how the pressure escapes.
#   3. Every governed destination exists and carries a known lifecycle class.
#   4. Declared ceilings are ENFORCED and declared health targets are REPORTED. The two tiers
#      are deliberate: a health target is advice, a ceiling blocks, and conflating them either
#      makes the guard noise or makes it a wall with no remedy.
#   5. The registry — not this script, and not prose — owns the landing page's own caps, which
#      are applied by re-running the README guard with them.
#
# ⛔ Raising a ceiling requires a reviewed decision that the surface's contract expanded, in a
# task leaf. Never raise one to land content.
#
# ⚠️ HONEST LIMIT: this proves every route has an owner and a bound, and that the bounds hold.
# It does not judge whether the content went to the RIGHT destination.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

REGISTRY="doctrine/readme_routes.tsv"
KNOWN_LIFECYCLES="hot_live partitioned generated_index append_history frozen normative"
KNOWN_ROUTE_CLASSES="reader_navigation author_overflow both"

# ── destinations the landing page links to (relative targets only) ───────────────────────────
readme_link_targets() {
  python3 - "$1" <<'PY'
import re, sys, pathlib
s = pathlib.Path(sys.argv[1]).read_text()
out = set()
for _, t in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', s):
    if t.startswith(("http://", "https://", "#", "mailto:")):
        continue
    out.add(t.split("#")[0])
print("\n".join(sorted(x for x in out if x)))
PY
}

# ── destinations the README guard ACTUALLY emits in its routing guidance ─────────────────────
# Forced red via a zero cap so the hint is produced; read-only, and the real verdict is never
# taken from this run.
emitted_hint_targets() {
  README_LINE_CAP=0 README_BYTE_CAP=0 scripts/check_readme_stability.sh 2>&1 \
    | grep -oE '(^| )[A-Za-z_][A-Za-z0-9_.-]*(/[A-Za-z0-9_.-]*)+|(^| )[A-Z][A-Z0-9_]*\.md' \
    | tr -d ' ' | sort -u
}

# ── governed? exact row, or a directory row that is a prefix ─────────────────────────────────
governed() { # $1 target  $2 file with one destination per line
  local t="$1" d
  while IFS= read -r d; do
    [ -n "$d" ] || continue
    [ "$t" = "$d" ] && return 0
    case "$d" in */) case "$t" in "$d"*) return 0 ;; esac ;; esac
  done < "$2"
  return 1
}

# Count a directory family's members. The registry governs the REPOSITORY, so the real run
# counts TRACKED files: `docs/book/` measured 92 files / 2,738,590 bytes with `find` because
# mdbook's build output sits inside it, against 3 tracked files — a generated artifact would
# otherwise fire a ceiling written for authored content.
family_files() { # $1 base  $2 dest  $3 mode(git|find)
  if [ "$3" = git ]; then git -C "$1" ls-files -- "$2" | sed "s|^|$1/|"
  else find "$1/$2" -type f; fi
}

# $1 = registry path, $2 = README path, $3 = 1 to enforce ceilings, $4 = root the destinations
# resolve against, $5 = family listing mode (git|find).
# ⛔ The base is a PARAMETER, not an environment variable. It was an env var for one revision,
# and `VAR=x verify_routes …` in the self-test leaked VAR into the caller — bash keeps an
# assignment that prefixes a *function* invocation — so the real run then resolved every
# destination against the self-test's already-deleted temp directory and reported all 24 as
# MISSING. A control must not be able to contaminate the thing it checks.
verify_routes() {
  local registry="$1" readme="$2" enforce="$3" base="$4" mode="${5:-find}" bad=0 tmp
  [ -f "$registry" ] || { echo "  MISSING registry $registry"; return 1; }
  [ -f "$readme" ]   || { echo "  MISSING landing page $readme"; return 1; }
  tmp="$(mktemp -d)"
  awk -F'\t' '!/^#/ && NF>=9 {print $1}' "$registry" > "$tmp/destinations"
  [ -s "$tmp/destinations" ] || { echo "  EMPTY registry $registry"; rm -rf "$tmp"; return 1; }

  # (1) every linked destination is governed
  local t
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    governed "$t" "$tmp/destinations" || { echo "  UNGOVERNED link target '$t' — no registry row"; bad=1; }
  done < <(readme_link_targets "$readme")

  # (3)+(4) rows: existence, classes, ceilings, health
  local dest rclass life owner hl hb cl cb cp n b line big
  # ⛔ NOT `IFS=$'\t' read`: tab is IFS *whitespace*, so consecutive tabs COLLAPSE and every
  # column after an empty field shifts left — silently, and the row still parses. Measured by
  # this script's own "no owner declared" arm, which passed while reading the owner as `0`.
  # Translating to a non-whitespace separator first preserves empty fields.
  while IFS= read -r line; do
    case "$line" in ''|'#'*) continue ;; esac
    IFS=$'\x1f' read -r dest rclass life owner hl hb cl cb cp <<<"${line//$'\t'/$'\x1f'}"
    case "$dest" in ''|'#'*) continue ;; esac
    case " $KNOWN_ROUTE_CLASSES " in *" $rclass "*) ;; *)
      echo "  UNKNOWN route_class '$rclass' for $dest"; bad=1 ;; esac
    case " $KNOWN_LIFECYCLES " in *" $life "*) ;; *)
      echo "  UNKNOWN lifecycle '$life' for $dest"; bad=1 ;; esac
    [ -n "$owner" ] || { echo "  NO OWNER declared for $dest"; bad=1; }
    case "$dest" in
      */)
          [ -d "$base/$dest" ] || { echo "  MISSING destination directory $dest"; bad=1; continue; }
          [ "$enforce" = 1 ] || continue
          # For a PARTITIONED family the policy's required control is a bounded index plus
          # file-count and aggregate ceilings, so the two numeric axes mean files and total
          # bytes here rather than lines and bytes. Splitting a monolith without bounding the
          # resulting collection just moves the same append pressure one level down.
          n=$(family_files "$base" "$dest" "$mode" | wc -l | tr -d ' ')
          b=$(family_files "$base" "$dest" "$mode" | tr '\n' '\0' | xargs -0 cat 2>/dev/null | wc -c | tr -d ' ')
          if [ "${cl:-0}" -gt 0 ] && [ "$n" -gt "$cl" ]; then
            echo "  OVER CEILING $dest: $n files > $cl"; bad=1; fi
          if [ "${cb:-0}" -gt 0 ] && [ "$b" -gt "$cb" ]; then
            echo "  OVER CEILING $dest: $b aggregate bytes > $cb"; bad=1; fi
          if [ "${hl:-0}" -gt 0 ] && [ "$n" -gt "$hl" ]; then
            echo "  health: $dest holds $n files (target $hl)"; fi
          if [ "${hb:-0}" -gt 0 ] && [ "$b" -gt "$hb" ]; then
            echo "  health: $dest holds $b aggregate bytes (target $hb)"; fi
          # Per-PART ceiling. A partitioned family's required control is a bounded index PLUS
          # per-part, file-count and aggregate ceilings: an aggregate bound alone permits one
          # member to become the monolith the split was meant to avoid.
          if [ "${cp:-0}" -gt 0 ]; then
            big="$(family_files "$base" "$dest" "$mode" | while IFS= read -r one; do
                     printf '%s\t%s\n' "$(wc -c < "$one" | tr -d ' ')" "$one"; done | sort -rn | head -1)"
            # Report the member RELATIVE to the base. An absolute path here is unusable as
            # evidence: the DOCPATH doctrine refuses a checkout-specific path in a tracked
            # document, so an author pasting this line into a task leaf would be blocked by a
            # different gate for a defect in this one.
            if [ -n "$big" ] && [ "${big%%	*}" -gt "$cp" ]; then
              echo "  OVER CEILING $dest: part ${big#*	}" | sed "s|$base/||"
              echo "    ${big%%	*} bytes > $cp"; bad=1; fi
          fi
          ;;
      *)  [ -f "$base/$dest" ] || { echo "  MISSING destination file $dest"; bad=1; continue; }
          [ "$enforce" = 1 ] || continue
          n=$(wc -l < "$base/$dest" | tr -d ' ')
          b=$(wc -c < "$base/$dest" | tr -d ' ')
          if [ "${cl:-0}" -gt 0 ] && [ "$n" -gt "$cl" ]; then
            echo "  OVER CEILING $dest: $n lines > $cl"; bad=1; fi
          if [ "${cb:-0}" -gt 0 ] && [ "$b" -gt "$cb" ]; then
            echo "  OVER CEILING $dest: $b bytes > $cb"; bad=1; fi
          if [ "${hl:-0}" -gt 0 ] && [ "$n" -gt "$hl" ]; then
            echo "  health: $dest is $n lines (target $hl)"; fi
          if [ "${hb:-0}" -gt 0 ] && [ "$b" -gt "$hb" ]; then
            echo "  health: $dest is $b bytes (target $hb)"; fi
          ;;
    esac
  done < "$registry"

  rm -rf "$tmp"
  return "$bad"
}

SELFTEST_TMP() {  # repo-volume scratch: project-created temporary workspaces must not
  # land on another filesystem (and $TMPDIR is one). /target is already untracked.
  local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"
}

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/docs"
  printf '# L\n\nSee [a](docs/) and [b](KEEP.md).\n' > "$t/README.md"
  printf 'x\n' > "$t/KEEP.md"; printf 'y\n' > "$t/docs/inner.md"
  reg() { printf '%s\n' "$@" > "$t/routes.tsv"; }
  R_DOCS=$'docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t0'
  R_KEEP=$'KEEP.md\tboth\thot_live\towner\t0\t0\t5\t64\t0'
  arm() { # name expected_rc expected_substring
    out="$(verify_routes "$t/routes.tsv" "$t/README.md" 1 "$t" find 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'README-ROUTING-CLOSURE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif [ -n "$3" ] && ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'README-ROUTING-CLOSURE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }
  reg "$R_DOCS" "$R_KEEP";                       arm "GREEN every route governed"   0 ""
  reg "$R_DOCS";                                 arm "RED   link target ungoverned" 1 "UNGOVERNED link target 'KEEP.md'"
  reg "$R_DOCS" "$R_KEEP" $'GONE.md\tboth\thot_live\towner\t0\t0\t0\t0\t0'
                                                 arm "RED   destination missing"    1 "MISSING destination file GONE.md"
  reg "$R_DOCS" "$R_KEEP" $'nosuch/\tauthor_overflow\tpartitioned\towner\t0\t0\t0\t0\t0'
                                                 arm "RED   directory destination missing" 1 "MISSING destination directory nosuch/"
  reg $'docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t1\t0' "$R_KEEP"
                                                 arm "RED   family over aggregate bytes" 1 "OVER CEILING docs/: 2 aggregate bytes > 1"
  reg $'docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t1' "$R_KEEP"
                                                 arm "RED   family part over per-part ceiling" 1 "OVER CEILING docs/: part"
  reg $'docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t0' "$R_KEEP"
                                                 arm "GREEN family within its bounds"   0 ""
  reg "$R_DOCS" $'KEEP.md\tinvented\thot_live\towner\t0\t0\t0\t0\t0'
                                                 arm "RED   unknown route_class"    1 "UNKNOWN route_class 'invented'"
  reg "$R_DOCS" $'KEEP.md\tboth\tinvented\towner\t0\t0\t0\t0\t0'
                                                 arm "RED   unknown lifecycle"      1 "UNKNOWN lifecycle 'invented'"
  reg "$R_DOCS" $'KEEP.md\tboth\thot_live\t\t0\t0\t0\t0\t0'
                                                 arm "RED   no owner declared"      1 "NO OWNER declared for KEEP.md"
  reg "$R_DOCS" $'KEEP.md\tboth\thot_live\towner\t0\t0\t0\t1\t0'
                                                 arm "RED   byte ceiling exceeded"  1 "OVER CEILING KEEP.md: 2 bytes > 1"
  printf 'x\nx\nx\n' > "$t/KEEP.md"
  reg "$R_DOCS" $'KEEP.md\tboth\thot_live\towner\t1\t0\t9\t0\t0'
                                                 arm "GREEN health target only warns" 0 "health: KEEP.md is 3 lines (target 1)"
  rm -rf "$t"
  printf 'README-ROUTING-CLOSURE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "README-ROUTING-CLOSURE: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2
}

fail=0
out="$(verify_routes "$REGISTRY" README.md 1 "$ROOT" git)" || fail=1

# (2) every path-shaped destination the guard actually emits must be governed
dests="$(mktemp)"; awk -F'\t' '!/^#/ && NF>=9 {print $1}' "$REGISTRY" > "$dests"
while IFS= read -r t; do
  [ -n "$t" ] || continue
  governed "$t" "$dests" || { out="$out"$'\n'"  UNGOVERNED emitted-hint destination '$t' — the guard routes authors there and nothing bounds it"; fail=1; }
done < <(emitted_hint_targets)
rm -f "$dests"

# (5) the registry owns the landing page's own caps
lc="$(awk -F'\t' '$1=="README.md" {print $7}' "$REGISTRY")"
bc="$(awk -F'\t' '$1=="README.md" {print $8}' "$REGISTRY")"
if [ -n "$lc" ] && [ -n "$bc" ] && [ "$lc" -gt 0 ] && [ "$bc" -gt 0 ]; then
  if ! capout="$(README_LINE_CAP="$lc" README_BYTE_CAP="$bc" scripts/check_readme_stability.sh 2>&1)"; then
    out="$out"$'\n'"  $capout"; fail=1
  else
    out="$out"$'\n'"  registry caps applied: $capout"
  fi
else
  out="$out"$'\n'"  README.md has no enforced caps in the registry — the landing page must be bounded"; fail=1
fi

if [ "$fail" -ne 0 ]; then
  { echo "README-ROUTING-CLOSURE: a routed destination is ungoverned, missing, or over its ceiling."
    printf '%s\n' "$out" | grep -v '^$'
    echo "  Give it a row in $REGISTRY with a class, an owner and a bound — or move the content."
    echo "  Raising a ceiling needs a reviewed decision that the surface's contract expanded."
  } >&2
  exit 1
fi
printf 'README-ROUTING-CLOSURE: ok (%s governed destination(s))\n' \
  "$(awk -F'\t' '!/^#/ && NF>=9' "$REGISTRY" | wc -l | tr -d ' ')"
printf '%s\n' "$out" | grep -E '^  (health:|registry caps applied:)' || true
exit 0
