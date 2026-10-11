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
    for name, path, before, size in measured:
        print(str(size) + '\t' + name)
except (OSError, ValueError, subprocess.SubprocessError) as error:
    reason = error.strerror if isinstance(error, OSError) else str(error)
    print('  UNREADABLE family ' + dest + ': ' + reason, file=sys.stderr)
    sys.exit(2)
PY
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
  local registry="$1" readme="$2" enforce="$3" base="$4" mode="${5:-find}" fo="${6:-}" bad=0 unreadable=0 tmp
  [ -f "$registry" ] || { echo "  MISSING registry $registry"; return 1; }
  [ -f "$readme" ]   || { echo "  MISSING landing page $readme"; return 1; }
  tmp="$(mktemp -d "$ROOT/target/tmp/check_readme_routes.XXXXXX")" || return 2
  awk -F'\t' '!/^#/ && NF>=9 {print $1}' "$registry" > "$tmp/destinations"
  [ -s "$tmp/destinations" ] || { echo "  EMPTY registry $registry"; rm -rf "$tmp"; return 1; }

  # (1) every linked destination is governed
  local t
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    governed "$t" "$tmp/destinations" || { echo "  UNGOVERNED link target '$t' — no registry row"; bad=1; }
  done < <(readme_link_targets "$readme")

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
          n=$(wc -l < "$tmp/parts" | tr -d ' ')
          b=$(awk -F'\t' '{total += $1} END {printf "%.0f", total}' "$tmp/parts")
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
            sort -rn "$tmp/parts" > "$tmp/sorted-parts"
            while IFS= read -r big; do
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
            done < "$tmp/sorted-parts"
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
# The two-tier per-part exemption consumes the fact-ownership registry, and the regen set
# must agree with the doctrine driver — a disagreement refuses, never silently widens.
regen_set_registered scripts/check_doctrines.project.sh || {
  echo "README-ROUTING-CLOSURE: REFUSED — the regeneration-doctrine set and the driver disagree." >&2
  exit 2; }
out="$(verify_routes "$REGISTRY" README.md 1 "$ROOT" git doctrine/fact_ownership.tsv)"
route_status=$?
if [ "$route_status" -eq 2 ]; then
  printf 'README-ROUTING-CLOSURE: REFUSED — family measurement unavailable.\n%s\n' "$out" >&2
  exit 2
fi
[ "$route_status" -eq 0 ] || fail=1

# (2) every path-shaped destination the guard actually emits must be governed
dests="$(mktemp "$ROOT/target/tmp/check_readme_routes.XXXXXX")" || exit 2; awk -F'\t' '!/^#/ && NF>=9 {print $1}' "$REGISTRY" > "$dests"
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
printf '%s\n' "$out" | grep -E '^  (health:|derived:|registry caps applied:)' || true
exit 0
