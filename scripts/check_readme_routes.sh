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
ROOT="$(git rev-parse --show-toplevel)" || exit 2; cd "$ROOT"
# All scratch, including child-tool defaults, stays on the repository volume.
mkdir -p "$ROOT/target/tmp" || exit 2
export TMPDIR="$ROOT/target/tmp"
source "$ROOT/scripts/read_text_metrics.bash" || exit 2

REGISTRY="doctrine/readme_routes.tsv"
KNOWN_LIFECYCLES="hot_live partitioned generated_index append_history frozen normative archive_terminal"

# The two-tier per-part rule (decision_derived-members-of-bounded-families, P5-BOARD.12):
# the per-part byte ceiling's founding failure mode is silent accretion in hand-maintained
# files — a property a regeneration-gated derived file CANNOT have (every byte is
# re-derived on every commit; its size is a pure function of already-bounded inputs). A
# family part over the authored ceiling is EXEMPT as a checked property, never a
# declaration: it must be registered in doctrine/fact_ownership.tsv as a MIRROR whose
# governor is a member of the closed regeneration-doctrine set below (each re-derives
# bytes byte-exact on every commit). An authored file cannot smuggle under the exemption
# — nothing regenerates it; a mirror governed by a validation gate (RECORD-SCHEMA & kin)
# keeps the authored ceiling. The set is closed: the day a new regeneration doctrine is
# registered, its leaf adds it here.
REGEN_GOVERNORS="STATE-GEN DEF-GEN GUEST-GEN BOARD-GEN GATE-REPORT MATERIALS-BILL BOOK-INDEX PLATFORM-GEN"

# Every regen-set member must be a REGISTERED project doctrine — a set/driver disagreement
# would silently widen the exemption, so it refuses by name instead.
regen_set_registered() { # $1 = project driver path
  local g
  for g in $REGEN_GOVERNORS; do
    grep -q "^  \"$g|" "$1" || { echo "  REGEN SET DRIFT: $g is in the regeneration set but not registered in $1"; return 1; }
  done
  return 0
}

# The exemption, resolved: $1 = member path relative to the base, $2 = fact-ownership
# registry (empty/missing = no exemptions). A member qualifies only as a MIRROR with a
# regeneration-doctrine governor — ownership of the fact is not the property; being
# byte-re-derived is.
derived_exempt() { # $1 member  $2 fact-ownership registry
  local member="$1" reg="$2" line kind owner mirror gov
  [ -n "$reg" ] && [ -f "$reg" ] || return 1
  while IFS= read -r line; do
    case "$line" in ''|'#'*) continue ;; esac
    IFS=$'\x1f' read -r kind owner mirror gov <<<"${line//$'\t'/$'\x1f'}"
    [ "$mirror" = "$member" ] || continue
    case " $REGEN_GOVERNORS " in *" $gov "*) return 0 ;; esac
  done < "$reg"
  return 1
}
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
  local producer="${1:-scripts/check_readme_stability.sh}" hint_raw hint_status hint_targets
  hint_raw="$(README_LINE_CAP=0 README_BYTE_CAP=0 "$producer" 2>&1)"
  hint_status=$?
  if [ "$hint_status" -ne 1 ] || [[ "$hint_raw" != *"Route the new detail to its canonical home"* ]]; then
    echo "UNREADABLE emitted-hint producer: expected a forced ceiling breach with routing guidance." >&2
    return 2
  fi
  local hint_errors
  hint_errors="$(mktemp "$ROOT/target/tmp/hint-errors.XXXXXX")" || return 2
  hint_targets="$( { printf '%s\n' "$hint_raw" \
    | grep -oE '(^| )[A-Za-z_][A-Za-z0-9_.-]*(/[A-Za-z0-9_.-]*)+|(^| )[A-Z][A-Z0-9_]*\.md' \
    | tr -d ' ' | sort -u; } 2> "$hint_errors")"
  hint_status=$?
  if [ "$hint_status" -ne 0 ] || [ -s "$hint_errors" ] || [ -z "$hint_targets" ]; then
    rm -f "$hint_errors"
    echo "UNREADABLE emitted-hint destinations" >&2
    return 2
  fi
  rm -f "$hint_errors"
  printf '%s\n' "$hint_targets"
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

# Measure a complete family once. Git supplies NUL-delimited tracked paths; fixture
# mode walks only its local tree. No count or byte total is published on a failed
# read, and paths never escape the base or cross a symlink, volume or Git boundary.
family_measure() { # $1 base  $2 destination directory  $3 mode(git|find)
  python3 - "$1" "$2" "$3" <<'PY'
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys

base = Path(sys.argv[1])
dest, mode = sys.argv[2:]

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def safe(name):
    p = PurePosixPath(name)
    require(name != '.' and not p.is_absolute() and str(p) == name and '..' not in p.parts
            and '\\' not in name and all(32 <= ord(c) != 127 for c in name),
            'unsafe member path')
    return p

def owned(name):
    cursor = base
    for part in safe(name).parts:
        cursor /= part
        info = cursor.lstat()
        require(not stat.S_ISLNK(info.st_mode), 'symlink member or parent: ' + name)
        require(info.st_dev == device, 'off-volume member or parent: ' + name)
        marker = cursor / '.git'
        require(not marker.is_symlink() and not marker.exists(),
                'nested Git boundary: ' + name)
    return cursor, info

def identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)

def walk_error(error):
    raise error

try:
    device = base.stat().st_dev
    require(dest.endswith('/') and str(safe(dest[:-1])) == dest[:-1],
            'unsafe family destination')
    directory, info = owned(dest[:-1])
    require(stat.S_ISDIR(info.st_mode), 'family is not a directory')
    if mode == 'git':
        result = subprocess.run(['git', '-C', str(base), 'ls-files', '-z', '--', dest],
                                capture_output=True, timeout=30)
        require(result.returncode == 0 and not result.stderr,
                'Git inventory failed or wrote stderr (status ' + str(result.returncode) + ')')
        raw = result.stdout
        require(not raw or raw.endswith(b'\0'), 'incomplete NUL inventory')
        names = [v.decode('utf-8') for v in raw.split(b'\0')[:-1]]
    elif mode == 'find':
        names = []
        for parent, directories, files in os.walk(directory, onerror=walk_error):
            for child in directories:
                owned((Path(parent) / child).relative_to(base).as_posix())
            names.extend((Path(parent) / child).relative_to(base).as_posix()
                         for child in files)
    else:
        raise ValueError('unknown family listing mode')
    require(len(names) == len(set(names)), 'duplicate family member')
    measured = []
    for name in sorted(names):
        safe(name)
        require(name.startswith(dest), 'member outside family: ' + name)
        path, info = owned(name)
        require(stat.S_ISREG(info.st_mode), 'non-regular family member: ' + name)
        measured.append((name, path, identity(info), info.st_size))
    for name, path, before, size in measured:
        require(identity(path.lstat()) == before, 'member changed during measurement: ' + name)
    print('@totals\t' + str(len(measured)) + '\t' + str(sum(row[3] for row in measured)))
    for name, path, before, size in measured:
        print(str(size) + '\t' + name)
except (OSError, ValueError, subprocess.SubprocessError) as error:
    reason = error.strerror if isinstance(error, OSError) else str(error)
    print('  UNREADABLE family ' + dest + ': ' + reason, file=sys.stderr)
    sys.exit(2)
PY
}

# Reject binary/control data before Bash command substitution can discard NULs.
registry_text() {
  python3 - "$1" <<'PYCODE'
from pathlib import Path
import sys
try:
    text = Path(sys.argv[1]).read_bytes().decode('utf-8').replace('\r\n', '\n')
    if any((ord(c) < 32 and c not in '\t\n') or ord(c) == 127 for c in text):
        raise ValueError('unexpected control character')
    sys.stdout.write(text)
except (OSError, UnicodeError, ValueError) as error:
    print('UNREADABLE registry text: ' + str(error), file=sys.stderr)
    sys.exit(2)
PYCODE
}

# Load the complete registry before publishing any projection. Numeric policy
# fields are decimal, nonnegative signed-64-bit values; normalize leading zeros
# before Bash comparisons. Keep class/owner breaches in verify_routes (status1).
read_registry_rows() {
  local file="$1" error data rc line tabs dest rclass life owner hl hb cl cb cp
  local value output="" seen=$'\n' row LC_ALL=C
  local normalized=()
  error="$(mktemp "$ROOT/target/tmp/registry-errors.XXXXXX")" || return 2
  data="$(registry_text "$file" 2> "$error")"; rc=$?
  if [ "$rc" -ne 0 ] || [ -s "$error" ]; then
    rm -f "$error"
    echo "  UNREADABLE registry read: failed status or diagnostics" >&2
    return 2
  fi
  rm -f "$error"
  while IFS= read -r line; do
    case "$line" in ''|'#'*) continue ;; esac
    tabs="${line//[^$'\t']/}"
    if [ "${#tabs}" -ne 8 ]; then
      echo "  UNREADABLE registry row: expected nine tab-separated fields" >&2
      return 2
    fi
    IFS=$'\x1f' read -r dest rclass life owner hl hb cl cb cp <<<"${line//$'\t'/$'\x1f'}"
    case "$dest" in ''|.|/*|./*|../*|*/../*|*/..|*/./*|*/.|*//*|*\\*)
      echo "  UNREADABLE registry row: destination must be a normalized relative path" >&2
      return 2 ;; esac
    case "$seen" in *$'\n'"$dest"$'\n'*)
      echo "  UNREADABLE registry row: duplicate destination" >&2; return 2 ;; esac
    seen+="$dest"$'\n'
    normalized=()
    for value in "$hl" "$hb" "$cl" "$cb" "$cp"; do
      if ! [[ "$value" =~ ^[0-9]+$ ]]; then
        echo "  UNREADABLE registry limits: expected nonnegative decimal integers" >&2
        return 2
      fi
      value="${value#"${value%%[!0]*}"}"; value="${value:-0}"
      if [ "${#value}" -gt 19 ] ||
         { [ "${#value}" -eq 19 ] && [[ "$value" > 9223372036854775807 ]]; }; then
        echo "  UNREADABLE registry limits: integer exceeds signed-64-bit range" >&2
        return 2
      fi
      normalized+=("$value")
    done
    printf -v row '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$dest" "$rclass" "$life" "$owner" "${normalized[@]}"
    output+="$row"
  done <<< "$data"
  printf '%s' "$output"
}

# $1 = registry path, $2 = README path, $3 = 1 to enforce ceilings, $4 = root the destinations
# resolve against, $5 = family listing mode (git|find), $6 = fact-ownership registry for
# the two-tier per-part exemption (optional; empty or missing = no exemptions).
# ⛔ The base is a PARAMETER, not an environment variable. It was an env var for one revision,
# and `VAR=x verify_routes …` in the self-test leaked VAR into the caller — bash keeps an
# assignment that prefixes a *function* invocation — so the real run then resolved every
# destination against the self-test's already-deleted temp directory and reported all 24 as
# MISSING. A control must not be able to contaminate the thing it checks.
verify_routes() {
  local registry="$1" readme="$2" enforce="$3" base="$4" mode="${5:-find}" fo="${6:-}" bad=0 unreadable=0 tmp metrics totals_tag
  [ -f "$registry" ] || { echo "  MISSING registry $registry"; return 1; }
  [ -f "$readme" ]   || { echo "  MISSING landing page $readme"; return 1; }
  tmp="$(mktemp -d "$ROOT/target/tmp/check_readme_routes.XXXXXX")" || return 2
  local registry_rows registry_line
  if ! registry_rows="$(read_registry_rows "$registry")"; then rm -rf "$tmp"; return 2; fi
  if [ -z "$registry_rows" ]; then echo "  EMPTY registry $registry"; rm -rf "$tmp"; return 1; fi
  : > "$tmp/destinations"
  while IFS= read -r registry_line; do
    printf '%s\n' "${registry_line%%$'\t'*}" >> "$tmp/destinations" || { rm -rf "$tmp"; return 2; }
  done <<< "$registry_rows"

  # (1) every linked destination is governed
  local t
  if ! readme_link_targets "$readme" > "$tmp/links" 2> "$tmp/link-errors" || [ -s "$tmp/link-errors" ]; then
    echo "  UNREADABLE landing-page links"
    unreadable=1
  else
    while IFS= read -r t; do
      [ -n "$t" ] || continue
      governed "$t" "$tmp/destinations" || { echo "  UNGOVERNED link target '$t' — no registry row"; bad=1; }
    done < "$tmp/links"
  fi

  # (3)+(4) rows: existence, classes, ceilings, health
  local dest rclass life owner hl hb cl cb cp n b line big rel
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
          if ! family_measure "$base" "$dest" "$mode" > "$tmp/parts" 2> "$tmp/read-errors"; then
            cat "$tmp/read-errors"
            unreadable=1; continue
          fi
          if ! IFS=$'\t' read -r totals_tag n b < "$tmp/parts" ||
             [ "$totals_tag" != @totals ] || ! [[ "$n" =~ ^[0-9]+$ ]] || ! [[ "$b" =~ ^[0-9]+$ ]]; then
            echo "  UNREADABLE family totals for $dest"
            unreadable=1; continue
          fi
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
          # member to become the monolith the split was meant to avoid. TWO-TIER
          # (P5-BOARD.12): the ceiling applies to AUTHORED members; a member registered in
          # the fact-ownership registry as a mirror with a regeneration-doctrine governor
          # is exempt as a checked property, reported as proof, never failed.
          if [ "${cp:-0}" -gt 0 ]; then
            while IFS= read -r big; do
              case "$big" in @totals$'\t'*) continue ;; esac
              [ -n "$big" ] || continue
              [ "${big%%	*}" -gt "$cp" ] || continue
              # Report the member RELATIVE to the base. An absolute path here is unusable as
              # evidence: the DOCPATH doctrine refuses a checkout-specific path in a tracked
              # document, so an author pasting this line into a task leaf would be blocked by
              # a different gate for a defect in this one.
              rel="${big#*	}"; rel="${rel#$base/}"
              if derived_exempt "$rel" "$fo"; then
                echo "  derived: $rel (${big%%	*} bytes > $cp authored per-part) is regeneration-gated — exempt (decision_derived-members-of-bounded-families)"
              else
                echo "  OVER CEILING $dest: part $rel"
                echo "    ${big%%	*} bytes > $cp"; bad=1
              fi
            done < "$tmp/parts"
          fi
          ;;
      *)  [ -f "$base/$dest" ] || { echo "  MISSING destination file $dest"; bad=1; continue; }
          [ "$enforce" = 1 ] || continue
          if ! metrics="$(read_text_metrics "$ROOT" "$base/$dest" 2>&1)"; then
            printf '  %s (%s)\n' "$metrics" "$dest"
            unreadable=1; continue
          fi
          IFS=$'\t' read -r n b <<< "$metrics"
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
  done <<< "$registry_rows"

  rm -rf "$tmp"
  [ "$unreadable" -eq 0 ] || return 2
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
  arm() { # name expected_rc expected_substring [cmd...] — default probe: verify_routes
    local name="$1" erc="$2" sub="$3"; shift 3
    if [ "$#" -gt 0 ]; then
      out="$("$@" 2>&1)"; rc=$?
    else
      out="$(verify_routes "$t/routes.tsv" "$t/README.md" 1 "$t" find "$t/fact.tsv" 2>&1)"; rc=$?
    fi
    if [ "$rc" != "$erc" ]; then
      fail=$((fail+1)); printf 'README-ROUTING-CLOSURE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$name" "$erc" "$rc" "$out" >&2
    elif [ -n "$sub" ] && ! printf '%s' "$out" | grep -qF "$sub"; then
      fail=$((fail+1)); printf 'README-ROUTING-CLOSURE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$name" "$sub" "$out" >&2
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
  # The two-tier per-part exemption (P5-BOARD.12): authored members keep the ceiling; a
  # member registered in the fact-ownership registry as a MIRROR with a regeneration
  # governor is exempt as a checked property — everything else over the ceiling fails.
  printf '%0100d' 0 | tr '0' 'x' > "$t/docs/big.gen"
  R_CP50=$'docs/\treader_navigation\tpartitioned\towner\t0\t0\t0\t0\t50'
  printf '# fixture registry\nkind\tdocs/source.sexp\tdocs/big.gen\tBOARD-GEN\n' > "$t/fact.tsv"
  reg "$R_CP50" "$R_KEEP"
                                                 arm "GREEN an over-ceiling part registered as regeneration-gated is exempt, reported as proof" 0 "derived: docs/big.gen"
  printf '# fixture registry\nkind\tdocs/source.sexp\tdocs/big.gen\tRECORD-SCHEMA\n' > "$t/fact.tsv"
  reg "$R_CP50" "$R_KEEP"
                                                 arm "RED   an over-ceiling part with a validation governor keeps the authored ceiling" 1 "OVER CEILING docs/: part"
  printf '# fixture registry\nkind\tdocs/source.sexp\tdocs/other.gen\tBOARD-GEN\n' > "$t/fact.tsv"
  reg "$R_CP50" "$R_KEEP"
                                                 arm "RED   no exemption by adjacency — the registry row must name the member" 1 "OVER CEILING docs/: part"
  rm -f "$t/fact.tsv" "$t/docs/big.gen"
  arm "GREEN the regen set agrees with the doctrine driver" 0 "" regen_set_registered scripts/check_doctrines.project.sh
  printf 'x\n' > "$t/driver.sh"
  arm "RED   a set/driver disagreement refuses, naming the drift" 1 "REGEN SET DRIFT" regen_set_registered "$t/driver.sh"
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
  # Synthetic Git data exercises the real inventory subprocess without creating
  # another repository or leaking PATH into the caller (the subshell owns it).
  mkdir -p "$t/bin"
  cat > "$t/bin/git" <<'PY'
#!/usr/bin/env python3
import os, sys
mode = os.environ['ROUTE_FIXTURE_MODE']
names = {
    'empty': [], 'duplicate': ['docs/inner.md', 'docs/inner.md'],
    'outside': ['KEEP.md'], 'traversal': ['docs/../KEEP.md'],
    'missing': ['docs/missing.md'], 'symlink': ['docs/link.md'],
    'directory': ['docs/subdir'], 'unicode': ['docs/café name.md'],
}.get(mode, ['docs/inner.md', 'docs/space name.md'])
if mode in {'failed', 'partial_stderr', 'failed_partial'}:
    sys.stderr.write('controlled inventory error\n')
if mode in {'failed', 'failed_silent'}: sys.exit(73)
if mode == 'partial_stderr': names = names[:1]
sys.stdout.buffer.write(b'\0'.join(n.encode() for n in names) + (b'\0' if names else b''))
if mode == 'malformed': sys.stdout.buffer.write(b'unterminated')
if mode == 'failed_partial': sys.exit(73)
PY
  chmod +x "$t/bin/git"
  printf 'xyz' > "$t/docs/space name.md"
  printf 'xy' > "$t/docs/café name.md"
  mkdir "$t/docs/subdir"
  ln -s ../KEEP.md "$t/docs/link.md"
  git_fixture() { (
    export PATH="$t/bin:$PATH" ROUTE_FIXTURE_MODE="$1"
    verify_routes "$t/routes.tsv" "$t/README.md" 1 "$t" git "$t/fact.tsv"
  ); }
  R_MEASURED=$'docs/\treader_navigation\tpartitioned\towner\t0\t0\t2\t5\t3'
  reg "$R_MEASURED" "$R_KEEP"
  arm "GREEN exact count/aggregate/part boundary and spaced member" 0 "" git_fixture baseline
  arm "GREEN successful empty tracked family" 0 "" git_fixture empty
  arm "RED failed empty inventory" 2 "UNREADABLE family docs/: Git inventory failed" git_fixture failed
  arm "RED silent nonzero inventory status" 2 "UNREADABLE family docs/: Git inventory failed" git_fixture failed_silent
  arm "RED partial listing with stderr and successful status" 2 "UNREADABLE family docs/: Git inventory failed" git_fixture partial_stderr
  arm "RED failed nonempty inventory" 2 "UNREADABLE family docs/: Git inventory failed" git_fixture failed_partial
  arm "RED unterminated NUL inventory" 2 "incomplete NUL inventory" git_fixture malformed
  arm "RED duplicate inventory member" 2 "duplicate family member" git_fixture duplicate
  arm "RED member outside family" 2 "member outside family" git_fixture outside
  arm "RED traversal in member" 2 "unsafe member path" git_fixture traversal
  arm "RED missing listed member" 2 "UNREADABLE family docs/:" git_fixture missing
  arm "RED symlink member" 2 "symlink member or parent" git_fixture symlink
  arm "RED directory listed as member" 2 "non-regular family member" git_fixture directory
  arm "GREEN Unicode and spaced member" 0 "" git_fixture unicode
  reg $'docs/\treader_navigation\tpartitioned\towner\t0\t0\t1\t5\t3' "$R_KEEP"
  arm "RED one file beyond count boundary" 1 "OVER CEILING docs/: 2 files > 1" git_fixture baseline
  # Remaining input paths: fixtures fail exactly one reader; no PATH changes
  # escape their subshells. The README provider runs its published CLI in a
  # project-local fixture with a synthetic root lookup, not another Git repo.
  rm -f "$t/docs/link.md"
  rmdir "$t/docs/subdir"
  local read_wc read_python read_sort read_grep
  read_wc="$(command -v wc)"; read_python="$(command -v python3)"; read_sort="$(command -v sort)"; read_grep="$(command -v grep)"
  cat > "$t/bin/wc" <<'SH'
#!/bin/sh
if [ "$1" = -c ]; then
 case "$ROUTE_READ_MODE" in
 file_status) printf 'controlled measurement failure\n' >&2; exit 73 ;;
 file_silent) exit 73 ;;
 file_failed_value) "$ROUTE_READ_WC" "$@"; exit 73 ;;
 file_stderr) "$ROUTE_READ_WC" "$@"; printf 'controlled measurement diagnostic\n' >&2; exit 0 ;;
 file_bad) printf 'invalid\n'; exit 0 ;;
 file_extra) printf '1\n2\n'; exit 0 ;;
 esac
fi
if [ "$1" = -l ] && [ "$ROUTE_READ_MODE" = file_line_status ]; then exit 73; fi
exec "$ROUTE_READ_WC" "$@"
SH
  cat > "$t/bin/python3" <<'SH'
#!/bin/sh
if [ "$#" -eq 2 ] && [ "$1" = - ] && [ "$2" = "$ROUTE_READ_FIXTURE/README.md" ]; then
 case "$ROUTE_READ_MODE" in
 parser_status) printf 'controlled parser failure\n' >&2; exit 73 ;;
 parser_silent) exit 73 ;;
 parser_stderr) printf 'KEEP.md\n'; printf 'controlled partial parser\n' >&2; exit 0 ;;
 esac
fi
exec "$ROUTE_READ_PYTHON" "$@"
SH
  cat > "$t/hint-provider" <<'SH'
#!/bin/sh
case "$ROUTE_READ_MODE" in
 hint_empty) exit 1 ;;
 hint_no_contract) printf 'README_POLICY.md\n' >&2; exit 1 ;;
esac
printf 'Route the new detail to its canonical home\n' >&2
if [ "$ROUTE_READ_MODE" != hint_no_destinations ]; then printf 'README_POLICY.md\n' >&2; fi
case "$ROUTE_READ_MODE" in hint_status) exit 73 ;; hint_success) exit 0 ;; esac
exit 1
SH
  cat > "$t/bin/sort" <<'SH'
#!/bin/sh
case "$ROUTE_READ_MODE" in
 hint_sort_status) cat; exit 73 ;;
 hint_sort_stderr) cat; printf 'controlled extraction diagnostic\n' >&2; exit 0 ;;
esac
exec "$ROUTE_READ_SORT" "$@"
SH
  cat > "$t/bin/grep" <<'SH'
#!/bin/sh
if [ "$1" = -cE ]; then
 case "$ROUTE_READ_MODE" in
 date_status) printf '0\n'; exit 73 ;;
 date_stderr) printf '0\n'; printf 'controlled date diagnostic\n' >&2; exit 0 ;;
 date_empty) exit 0 ;;
 esac
fi
if [ "$1" = -cF ]; then
 case "$ROUTE_READ_MODE" in
 policy_status) printf '1\n'; exit 73 ;;
 policy_stderr) printf '1\n'; printf 'controlled policy diagnostic\n' >&2; exit 0 ;;
 policy_empty) exit 0 ;;
 esac
fi
exec "$ROUTE_READ_GREP" "$@"
SH
  chmod +x "$t/bin/wc" "$t/bin/python3" "$t/bin/sort" "$t/bin/grep" "$t/hint-provider"
  input_fixture() { (
    export PATH="$t/bin:$PATH" ROUTE_READ_MODE="$1" ROUTE_READ_FIXTURE="$t"
    export ROUTE_READ_WC="$read_wc" ROUTE_READ_PYTHON="$read_python" ROUTE_READ_GREP="$read_grep"
    verify_routes "$t/routes.tsv" "${2:-$t/README.md}" 1 "$t" find "$t/fact.tsv"
  ); }
  hint_fixture() { (
    export ROUTE_READ_MODE="$1" PATH="$t/bin:$PATH" ROUTE_READ_SORT="$read_sort"
    export ROUTE_READ_PYTHON="$read_python" ROUTE_READ_WC="$read_wc" ROUTE_READ_GREP="$read_grep"
    emitted_hint_targets "$t/hint-provider"
  ); }
  reg "$R_DOCS" "$R_KEEP"
  arm "GREEN all fixture input readers work" 0 "" input_fixture baseline
  arm "RED text byte measurement failed status" 2 "UNREADABLE text measurement" input_fixture file_status
  arm "RED text byte measurement silent failed status" 2 "UNREADABLE text measurement" input_fixture file_silent
  arm "RED failed measurement despite plausible numeric output" 2 "UNREADABLE text measurement" input_fixture file_failed_value
  arm "RED text byte measurement diagnostic" 2 "UNREADABLE text measurement" input_fixture file_stderr
  arm "RED text measurement invalid integer" 2 "UNREADABLE text measurement" input_fixture file_bad
  arm "RED text measurement extra integer" 2 "UNREADABLE text measurement" input_fixture file_extra
  arm "RED text line measurement silent failed status" 2 "UNREADABLE text measurement" input_fixture file_line_status
  arm "RED linked destination parser failed status" 2 "UNREADABLE landing-page links" input_fixture parser_status
  arm "RED linked destination parser silent failed status" 2 "UNREADABLE landing-page links" input_fixture parser_silent
  arm "RED linked destination parser partial diagnostic" 2 "UNREADABLE landing-page links" input_fixture parser_stderr
  printf '# Empty landing page\n' > "$t/empty-readme.md"
  arm "GREEN successful link parse can have no links" 0 "" input_fixture baseline "$t/empty-readme.md"
  arm "GREEN forced-red provider emits destinations" 0 "README_POLICY.md" hint_fixture baseline
  arm "RED hint provider failed despite plausible guidance" 2 "UNREADABLE emitted-hint producer" hint_fixture hint_status
  arm "RED hint provider unexpectedly successful despite guidance" 2 "UNREADABLE emitted-hint producer" hint_fixture hint_success
  arm "RED hint provider returned no guidance" 2 "UNREADABLE emitted-hint producer" hint_fixture hint_empty
  arm "RED hint provider returned paths without its guidance contract" 2 "UNREADABLE emitted-hint producer" hint_fixture hint_no_contract
  arm "RED hint extraction returned no destinations" 2 "UNREADABLE emitted-hint destinations" hint_fixture hint_no_destinations
  arm "RED extraction failed despite nonempty destinations" 2 "UNREADABLE emitted-hint destinations" hint_fixture hint_sort_status
  arm "RED extraction emitted diagnostics with nonempty destinations" 2 "UNREADABLE emitted-hint destinations" hint_fixture hint_sort_stderr

  mkdir -p "$t/readme-project/scripts" "$t/readme-bin"
  cp "$ROOT/scripts/check_readme_stability.sh" "$t/readme-project/scripts/"
  cp "$ROOT/scripts/read_text_metrics.bash" "$t/readme-project/scripts/"
  printf 'See README_POLICY.md\n' > "$t/readme-project/README.md"
  printf 'fixture policy\n' > "$t/readme-project/README_POLICY.md"
  cat > "$t/readme-bin/git" <<'SH'
#!/bin/sh
if [ "$#" -eq 2 ] && [ "$1" = rev-parse ] && [ "$2" = --show-toplevel ]; then
 printf '%s\n' "$ROUTE_READ_PROJECT"; exit 0
fi
exit 73
SH
  chmod +x "$t/readme-bin/git"
  readme_fixture() { (
    export PATH="$t/readme-bin:$t/bin:$PATH" ROUTE_READ_MODE="$1"
    export ROUTE_READ_WC="$read_wc" ROUTE_READ_PYTHON="$read_python" ROUTE_READ_GREP="$read_grep"
    export ROUTE_READ_FIXTURE="$t" ROUTE_READ_PROJECT="$t/readme-project"
    cd "$ROUTE_READ_PROJECT" || exit 2
    case "$1" in
      policy_lookalike) printf 'See README_POLICYxmd\n' > README.md ;;
      policy_absent) printf 'See another policy\n' > README.md ;;
      dated_page) printf 'See README_POLICY.md on 2026-01-01\n' > README.md ;;
      *) printf 'See README_POLICY.md\n' > README.md ;;
    esac
    bash scripts/check_readme_stability.sh
  ); }
  arm "GREEN standalone README CLI measures its page" 0 "README-STABILITY: OK" readme_fixture baseline
  arm "RED standalone README CLI refuses byte failure" 2 "README-STABILITY: REFUSED" readme_fixture file_silent
  arm "RED standalone README CLI refuses line failure" 2 "README-STABILITY: REFUSED" readme_fixture file_line_status
  arm "RED standalone README CLI refuses measurement stderr" 2 "README-STABILITY: REFUSED" readme_fixture file_stderr
  arm "RED standalone date count failed with plausible zero" 2 "dated-annotation count unavailable" readme_fixture date_status
  arm "RED standalone date count reported diagnostics" 2 "dated-annotation count unavailable" readme_fixture date_stderr
  arm "RED standalone date count returned no integer" 2 "dated-annotation count unavailable" readme_fixture date_empty
  arm "RED standalone policy count failed with plausible integer" 2 "policy-name count unavailable" readme_fixture policy_status
  arm "RED standalone policy count reported diagnostics" 2 "policy-name count unavailable" readme_fixture policy_stderr
  arm "RED standalone policy count returned no integer" 2 "policy-name count unavailable" readme_fixture policy_empty
  arm "RED policy lookalike is not its literal name" 1 "no longer links README_POLICY.md" readme_fixture policy_lookalike
  arm "RED legitimate policy no-match remains a breach" 1 "no longer links README_POLICY.md" readme_fixture policy_absent
  arm "RED legitimate dated annotation remains a breach" 1 "date-stamped line(s)" readme_fixture dated_page

  table_fixture() { (
    family_measure() {
      case "$ROUTE_TABLE_MODE" in
        empty) return 0 ;;
        bad_count) printf '@totals\tinvalid\t2\n' ;;
        extra) printf '@totals\t1\t2\textra\n' ;;
      esac
    }
    export ROUTE_TABLE_MODE="$1"
    verify_routes "$t/routes.tsv" "$t/README.md" 1 "$t" find "$t/fact.tsv"
  ); }
  arm "RED producer table missing its totals" 2 "UNREADABLE family totals" table_fixture empty
  arm "RED producer table has invalid count" 2 "UNREADABLE family totals" table_fixture bad_count
  arm "RED producer table has surplus totals field" 2 "UNREADABLE family totals" table_fixture extra
  registry_fixture() { (
    local registry_case_mode="$1" registry_case="$t/registry-case.tsv" registry_readme="$t/registry-readme.md" row captured registry_rc
    printf 'See [keep](KEEP.md).\n' > "$registry_readme"
    row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t64\t0'
    case "$registry_case_mode" in
      invalid_line) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\tinvalid\t64\t0' ;;
      invalid_byte) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\tinvalid\t0' ;;
      negative_health) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t-1\t0\t5\t64\t0' ;;
      negative_ceiling) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t-1\t64\t0' ;;
      overflow) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t99999999999999999999999999999999999\t0' ;;
      max_plus_one) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t9223372036854775808\t0' ;;
      max) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t9223372036854775807\t9223372036854775807\t0' ;;
      zeros) row=$'KEEP.md\treader_navigation\thot_live\tfixture\t000\t000\t0000000000000000000000000000000000005\t00000000000000000000000000000000000064\t000' ;;
      extra) row+=$'\textra' ;;
      missing) row="${row%$'\t'*}" ;;
      unsafe) row=$'../KEEP.md\treader_navigation\thot_live\tfixture\t0\t0\t5\t64\t0' ;;
    esac
    printf '%s\n' "$row" > "$registry_case"
    case "$registry_case_mode" in
      duplicate) printf '%s\n' "$row" >> "$registry_case" ;;
      no_lf) printf '%s' "$row" > "$registry_case" ;;
      crlf) printf '%s\r\n' "$row" > "$registry_case" ;;
      nul) printf '\000' >> "$registry_case" ;;
      control) printf '\037' >> "$registry_case" ;;
      invalid_utf8) printf 'KEEP.md\treader_navigation\thot_live\tfi\377xture\t0\t0\t5\t64\t0\n' > "$registry_case" ;;
      status|diagnostic|silent)
        registry_text() {
          [ "$registry_case_mode" = silent ] || cat "$1"
          [ "$registry_case_mode" != diagnostic ] || { echo 'controlled registry diagnostic' >&2; return 0; }
          return 73
        } ;;
      no_partial)
        printf 'extra.md\treader_navigation\thot_live\tfixture\t0\t0\tbad\t64\t0\n' >> "$registry_case"
        captured="$(read_registry_rows "$registry_case" 2> "$t/registry-case-error")"; registry_rc=$?
        [ "$registry_rc" -eq 2 ] && [ -z "$captured" ] || return 1
        printf 'invalid suffix publishes no rows\n'; return 0 ;;
    esac
    verify_routes "$registry_case" "$registry_readme" 1 "$t" find "$t/fact.tsv"
  ); }
  arm "GREEN registry baseline retains existing semantics" 0 "" registry_fixture baseline
  arm "RED registry producer failed despite healthy rows" 2 "UNREADABLE registry read" registry_fixture status
  arm "RED registry producer diagnostic despite healthy rows" 2 "UNREADABLE registry read" registry_fixture diagnostic
  arm "RED registry producer silent failure" 2 "UNREADABLE registry read" registry_fixture silent
  arm "RED registry line limit is not an integer" 2 "UNREADABLE registry limits" registry_fixture invalid_line
  arm "RED registry byte limit is not an integer" 2 "UNREADABLE registry limits" registry_fixture invalid_byte
  arm "RED registry health limit is negative" 2 "UNREADABLE registry limits" registry_fixture negative_health
  arm "RED registry ceiling is negative" 2 "UNREADABLE registry limits" registry_fixture negative_ceiling
  arm "RED registry integer overflows Bash comparisons" 2 "signed-64-bit range" registry_fixture overflow
  arm "RED registry integer one above maximum" 2 "signed-64-bit range" registry_fixture max_plus_one
  arm "GREEN registry exact signed-64-bit maximum" 0 "" registry_fixture max
  arm "GREEN registry decimal leading zeros normalize" 0 "" registry_fixture zeros
  arm "RED registry surplus field" 2 "nine tab-separated fields" registry_fixture extra
  arm "RED registry missing field" 2 "nine tab-separated fields" registry_fixture missing
  arm "RED registry duplicate destination" 2 "duplicate destination" registry_fixture duplicate
  arm "RED registry unsafe relative destination" 2 "normalized relative path" registry_fixture unsafe
  arm "GREEN registry last row needs no LF" 0 "" registry_fixture no_lf
  arm "GREEN registry CRLF normalizes" 0 "" registry_fixture crlf
  arm "RED registry NUL cannot disappear in substitution" 2 "UNREADABLE registry read" registry_fixture nul
  arm "RED registry separator control character" 2 "UNREADABLE registry read" registry_fixture control
  arm "RED registry invalid UTF-8" 2 "UNREADABLE registry read" registry_fixture invalid_utf8
  arm "GREEN invalid registry suffix publishes no prefix" 0 "publishes no rows" registry_fixture no_partial
  registry_main_fixture() { (
    local registry_entry_mode="$1" main_root="$t/readme-project"
    export PATH="$t/readme-bin:$PATH" ROUTE_READ_PROJECT="$main_root"
    cd "$main_root" || exit 2
    ROOT="$PWD"; REGISTRY=routes.tsv
    mkdir -p "$ROOT/target/tmp" || exit 2
    printf 'See README_POLICY.md\n' > README.md
    printf 'fixture policy\n' > README_POLICY.md
    printf 'README.md\treader_navigation\thot_live\tfixture\t0\t0\t100\t65536\t0\nREADME_POLICY.md\treader_navigation\tnormative\tfixture\t0\t0\t0\t0\t0\n' > "$REGISTRY"
    regen_set_registered() { return 0; }
    emitted_hint_targets() { printf 'README_POLICY.md\n'; }
    case "$registry_entry_mode" in
      status|diagnostic)
        registry_text() {
          cat "$1"
          [ "$registry_entry_mode" != diagnostic ] || { echo 'controlled main registry diagnostic' >&2; return 0; }
          return 73
        } ;;
      malformed) printf 'extra.md\treader_navigation\tnormative\tfixture\t0\t0\tbad\t0\t0\n' >> "$REGISTRY" ;;
    esac
    main_routes
  ); }
  arm "GREEN entry flow derives exact destination count and README caps" 0 "ok (2 governed destination(s))" registry_main_fixture baseline
  arm "RED entry flow propagates failed registry producer" 2 "REFUSED — registry inputs unavailable" registry_main_fixture status
  arm "RED entry flow propagates registry diagnostics" 2 "REFUSED — registry inputs unavailable" registry_main_fixture diagnostic
  arm "RED entry flow rejects malformed registry suffix" 2 "REFUSED — registry inputs unavailable" registry_main_fixture malformed
  rm -rf "$t"
  printf 'README-ROUTING-CLOSURE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

# Shared entry flow: self-tests invoke this same body in isolated fixtures.
main_routes() {
  fail=0
  # The two-tier per-part exemption consumes the fact-ownership registry, and the regen set
  # must agree with the doctrine driver — a disagreement refuses, never silently widens.
  regen_set_registered scripts/check_doctrines.project.sh || {
    echo "README-ROUTING-CLOSURE: REFUSED — the regeneration-doctrine set and the driver disagree." >&2
    exit 2; }
  registry_work="$(mktemp -d "$ROOT/target/tmp/registry-snapshot.XXXXXX")" || exit 2
  trap 'rm -rf "$registry_work"' EXIT
  if ! registry_rows="$(read_registry_rows "$REGISTRY")"; then
    echo "README-ROUTING-CLOSURE: REFUSED — registry inputs unavailable." >&2
    exit 2
  fi
  printf '%s\n' "$registry_rows" > "$registry_work/rows" || exit 2
  out="$(verify_routes "$registry_work/rows" README.md 1 "$ROOT" git doctrine/fact_ownership.tsv)"
  route_status=$?
  if [ "$route_status" -eq 2 ]; then
    printf 'README-ROUTING-CLOSURE: REFUSED — routed inputs unavailable.\n%s\n' "$out" >&2
    exit 2
  fi
  [ "$route_status" -eq 0 ] || fail=1

  # (2) every path-shaped destination the guard actually emits must be governed
  dests="$registry_work/destinations"
  : > "$dests" || exit 2
  lc=0; bc=0; governed_count=0
  while IFS= read -r registry_line; do
    [ -n "$registry_line" ] || continue
    IFS=$'\x1f' read -r dest rclass life owner hl hb cl cb cp <<<"${registry_line//$'\t'/$'\x1f'}"
    printf '%s\n' "$dest" >> "$dests" || exit 2
    governed_count=$((governed_count + 1))
    if [ "$dest" = README.md ]; then lc="$cl"; bc="$cb"; fi
  done <<< "$registry_rows"
  if ! hints="$(emitted_hint_targets 2>&1)"; then
    rm -f "$dests"
    printf 'README-ROUTING-CLOSURE: REFUSED — emitted routing guidance unavailable.\n%s\n' "$hints" >&2
    exit 2
  fi
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    governed "$t" "$dests" || { out="$out"$'\n'"  UNGOVERNED emitted-hint destination '$t' — the guard routes authors there and nothing bounds it"; fail=1; }
  done <<< "$hints"
  rm -f "$dests"

  # (5) the registry owns the landing page's own caps
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
  printf 'README-ROUTING-CLOSURE: ok (%s governed destination(s))\n' "$governed_count"
  printf '%s\n' "$out" | grep -E '^  (health:|derived:|registry caps applied:)' || true
  exit 0
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "README-ROUTING-CLOSURE: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2
}

main_routes
