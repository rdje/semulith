#!/usr/bin/env bash
# scripts/check_rustdoc.sh — API-DOCS doctrine: the API reference is rustdoc, and its links and HTML are sound.
#
# The director's direction (decision_rust-native-tooling, 2026-10-23): SEMULITH's API reference is
# produced by rustdoc from the code (tree RUSTDOC). A reference whose intra-doc links point nowhere,
# point at private items a reader cannot open, or whose prose swallows text into an unclosed HTML tag
# is a reference that lies quietly. This check builds the workspace's docs offline with exactly three
# rustdoc lints denied — broken_intra_doc_links, private_intra_doc_links, invalid_html_tags — and
# refuses any occurrence, naming file, line and lint.
#
# Missing documentation is a RATCHET, not a denial (RUSTDOC.3): the same build warns on `missing_docs`,
# the check counts the undocumented public items per crate directory under crates/ and compares each
# count with doctrine/undocumented_items.tsv. A rise is refused with the crate's undocumented items
# listed; a fall is refused until the row is lowered to the new count, so the ratchet only tightens and
# the record always states the measured truth (267 at adoption: core 61, verify 86, dsp56300 120).
#
# Measured at adoption (RUSTDOC.1, 2026-10-23): the real tree carried 19 such defects (9 unresolved
# links, 4 links to private items, 6 unclosed HTML tags); the check was fired RED on it before the
# repair. A check with arms: --self-test documents scratch crates and asserts verdict AND reason.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
LINTS="-D rustdoc::broken_intra_doc_links -D rustdoc::private_intra_doc_links -D rustdoc::invalid_html_tags"
RECORD="doctrine/undocumented_items.tsv"

# ratchet RECORD CRATE... < cargo-doc-output — prints the total, or the problems; rc 0 / 1 / 2 (malformed record)
ratchet() {
  python3 -c '
import re, sys
record_path, crates = sys.argv[1], sys.argv[2:]
log = sys.stdin.read().split("\n")
counts = {c: 0 for c in crates}; where = {c: [] for c in crates}; stray = []
for i, line in enumerate(log):
    if not line.startswith("warning: missing documentation for"):
        continue
    loc = next((x.strip()[4:] for x in log[i + 1:i + 4] if x.strip().startswith("-->")), "")
    m = re.match(r"(?:crates/([^/]+)|(xtask))/", loc)  # a crate under crates/, or the xtask front door (XTASK.1)
    crate = m and (m.group(1) or m.group(2))
    if crate in counts:
        counts[crate] += 1; where[crate].append(loc + "  " + line[len("warning: "):])
    else:
        stray.append(loc or "?")
rows = {}
try:
    lines = open(record_path, encoding="utf-8").read().split("\n")
except OSError as error:
    print("unreadable record: " + str(error)); sys.exit(2)
for line in lines:
    if not line.strip() or line.startswith("#"):
        continue
    parts = line.split("\t")
    if len(parts) != 2 or not parts[1].isdigit() or parts[0] in rows:
        print("malformed record row: " + repr(line)); sys.exit(2)
    rows[parts[0]] = int(parts[1])
problems = []
if stray:
    problems.append("%d undocumented item(s) outside a workspace crate directory: %s" % (len(stray), stray[:3]))
for crate in sorted(set(rows) - set(crates)):
    problems.append(crate + ": recorded, but not a workspace crate directory")
for crate in crates:
    if crate not in rows:
        problems.append("%s: no recorded count (measured %d)" % (crate, counts[crate]))
    elif counts[crate] > rows[crate]:
        problems.append("%s: %d undocumented > recorded %d; document the new item(s):%s" % (
            crate, counts[crate], rows[crate], "".join("\n    " + w for w in where[crate][:20])))
    elif counts[crate] < rows[crate]:
        problems.append("%s: %d undocumented < recorded %d; lower the record to %d (the ratchet only tightens)" % (
            crate, counts[crate], rows[crate], counts[crate]))
if problems:
    print("\n".join(problems)); sys.exit(1)
print(sum(counts.values()))
' "$@"
}

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

mkcrate() { # $1 = dir, $2 = name, $3 = src/lib.rs content; a stand-alone package (own [workspace])
  mkdir -p "$1/src"
  cat > "$1/Cargo.toml" <<EOF
[package]
name = "$2"
version = "0.1.0"
edition = "2021"

[workspace]
EOF
  printf '%s\n' "$3" > "$1/src/lib.rs"
}

doc_crate() { # $1 = crate dir; the doc build stays inside the scratch dir and takes ONLY the
              # three lints — an inherited RUSTDOCFLAGS must not decide a self-test verdict.
  ( cd "$1" && RUSTDOCFLAGS="$LINTS" cargo doc --offline --no-deps --target-dir "$1/.wt" 2>&1 )
}

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'API-DOCS self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring; "!x" asserts x is ABSENT>
    argc 5 "$#" arm || return
    local want="$5"
    if [ "${want:0:1}" = "!" ]; then
      if [ "$2" = "$3" ] && ! printf '%s' "$4" | grep -qF "${want:1}"; then pass=$((pass+1))
      else fail=$((fail+1)); printf 'API-DOCS self-test MISS: %s — expected rc=%s WITHOUT %q, got rc=%s\n%s\n' \
        "$1" "$3" "${want:1}" "$2" "$4" >&2; fi
    elif [ "$2" = "$3" ] && { [ "$want" = "-" ] || printf '%s' "$4" | grep -qF "$want"; }; then pass=$((pass+1))
    else fail=$((fail+1)); printf 'API-DOCS self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
      "$1" "$3" "$want" "$2" "$4" >&2; fi
  }

  mkcrate "$t/good" "probe-good" '//! A documented crate.
/// Returns [`ANSWER`].
pub fn probe() -> u32 { ANSWER }
/// The answer.
pub const ANSWER: u32 = 42;'
  out="$(doc_crate "$t/good")"; rc=$?
  arm "GREEN a crate whose links resolve and whose prose is sound" "$rc" 0 "$out" "-"

  mkcrate "$t/broken" "probe-broken" '/// See [`nowhere`].
pub fn probe() -> u32 { 42 }'
  out="$(doc_crate "$t/broken")"; rc=$?
  arm "RED an intra-doc link to nothing is refused, naming the lint" "$rc" 101 "$out" "rustdoc::broken-intra-doc-links"

  mkcrate "$t/private" "probe-private" '/// Delegates to [`helper`].
pub fn probe() -> u32 { helper() }
fn helper() -> u32 { 42 }'
  out="$(doc_crate "$t/private")"; rc=$?
  arm "RED a public doc linking a private item is refused, naming the lint" "$rc" 101 "$out" "rustdoc::private-intra-doc-links"

  mkcrate "$t/html" "probe-html" '/// Takes a Vec<u8> of bytes.
pub fn probe() -> u32 { 42 }'
  out="$(doc_crate "$t/html")"; rc=$?
  arm "RED an unclosed HTML tag in prose is refused, naming the lint" "$rc" 101 "$out" "rustdoc::invalid-html-tags"

  mkcrate "$t/undocumented" "probe-undocumented" 'pub fn probe() -> u32 { 42 }'
  out="$(doc_crate "$t/undocumented")"; rc=$?
  arm "GREEN missing docs alone are not this check's business (RUSTDOC.3 owns them)" "$rc" 0 "$out" "-"

  mkcrate "$t/syntax" "probe-syntax" 'pub fn broken( {'
  out="$(doc_crate "$t/syntax")"; rc=$?
  arm "REFUSE a failure with an unrelated cause is not read as a link defect" "$rc" 101 "$out" "!rustdoc::"

  out="$(RUSTDOCFLAGS="-D missing_docs" bash -c 'cd "$1" && RUSTDOCFLAGS="$2" cargo doc --offline --no-deps --target-dir "$1/.wt" 2>&1' _ "$t/undocumented" "$LINTS")"; rc=$?
  arm "GREEN an inherited RUSTDOCFLAGS does not leak into the verdict" "$rc" 0 "$out" "-"

  # The ratchet, on a two-crate workspace laid out as crates/<dir>/: one crate with two undocumented
  # public items (a function and a struct field), one fully documented.
  mkdir -p "$t/ws/crates/probe/src" "$t/ws/crates/clean/src"
  printf '[workspace]\nresolver = "2"\nmembers = ["crates/probe", "crates/clean"]\n' > "$t/ws/Cargo.toml"
  printf '[package]\nname = "probe"\nversion = "0.1.0"\nedition = "2021"\n' > "$t/ws/crates/probe/Cargo.toml"
  printf '[package]\nname = "clean"\nversion = "0.1.0"\nedition = "2021"\n' > "$t/ws/crates/clean/Cargo.toml"
  printf '//! A probe.\npub fn bare() {}\n/// Documented.\npub struct S {\n    pub field: u8,\n}\n' > "$t/ws/crates/probe/src/lib.rs"
  printf '//! Clean.\n/// One.\npub fn one() {}\n' > "$t/ws/crates/clean/src/lib.rs"
  local doc rec; doc="$t/ws.doc"; rec="$t/rec.tsv"
  ( cd "$t/ws" && RUSTDOCFLAGS="$LINTS -W missing_docs" cargo doc --workspace --offline --no-deps --target-dir "$t/ws/.wt" > "$doc" 2>&1 )
  printf 'probe\t2\nclean\t0\n' > "$rec"; out="$(ratchet "$rec" probe clean < "$doc")"; rc=$?
  arm "GREEN the ratchet holds when every crate's count equals its row" "$rc" 0 "$out" "2"
  printf 'probe\t1\nclean\t0\n' > "$rec"; out="$(ratchet "$rec" probe clean < "$doc")"; rc=$?
  arm "RED a rise is refused, listing the crate's undocumented items" "$rc" 1 "$out" "document the new item(s)"
  printf 'probe\t3\nclean\t0\n' > "$rec"; out="$(ratchet "$rec" probe clean < "$doc")"; rc=$?
  arm "RED a fall is refused until the row is lowered" "$rc" 1 "$out" "lower the record to 2"
  printf 'probe\t2\n' > "$rec"; out="$(ratchet "$rec" probe clean < "$doc")"; rc=$?
  arm "RED a crate without a row is refused" "$rc" 1 "$out" "clean: no recorded count"
  printf 'probe\t2\nclean\t0\nghost\t0\n' > "$rec"; out="$(ratchet "$rec" probe clean < "$doc")"; rc=$?
  arm "RED a row naming no workspace crate is refused" "$rc" 1 "$out" "ghost: recorded, but not a workspace crate directory"
  printf 'probe 2\n' > "$rec"; out="$(ratchet "$rec" probe clean < "$doc")"; rc=$?
  arm "REFUSE a malformed record cannot be judged" "$rc" 2 "$out" "malformed record row"

  rm -rf "$t"
  printf 'API-DOCS --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse, not pass.
self_test >/dev/null 2>&1 || {
  echo "API-DOCS: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2
}

out="$(RUSTDOCFLAGS="$LINTS -W missing_docs" cargo doc --workspace --no-deps --offline 2>&1)"; rc=$?
if [ "$rc" -ne 0 ]; then
  {
    echo "API-DOCS: FAIL — the workspace's rustdoc carries link or HTML defects (decision_rust-native-tooling):"
    # one line per defect: the location that follows each diagnostic, then its message
    printf '%s\n' "$out" | awk '/^(error|warning): / && !/could not document/ { msg=$0; sub(/^(error|warning): /, "", msg); want=1; next }
                               want && /^ *--> / { loc=$0; sub(/^ *--> /, "", loc); printf "  %s  %s\n", loc, msg; want=0 }' | head -60
    echo "  Fix the doc comment (or its generator) — never allow the lint."
  } >&2
  exit 1
fi
# Count crates from the workspace's crate directories: a fresh build prints no "Documenting" line,
# while cargo replays the cached warnings, so the ratchet's count is the same either way.
dirs=(); for d in crates/*/; do [ -f "$d/Cargo.toml" ] && dirs+=("$(basename "$d")"); done
[ -f xtask/Cargo.toml ] && dirs+=("xtask")  # the automation front door is a workspace member too (XTASK.1)
crates="${#dirs[@]}"
verdict="$(printf '%s\n' "$out" | ratchet "$RECORD" "${dirs[@]}")"; vrc=$?
if [ "$vrc" -eq 2 ]; then
  printf 'API-DOCS: REFUSED — %s cannot be judged: %s\n' "$RECORD" "$verdict" >&2; exit 2
elif [ "$vrc" -ne 0 ]; then
  { echo "API-DOCS: FAIL — the undocumented public items no longer match $RECORD (the RUSTDOC.3 ratchet):"
    printf '%s\n' "$verdict" | sed 's/^/  /'; } >&2
  exit 1
fi
printf 'API-DOCS: ok (%s crate(s) documented; no broken or private intra-doc link, no invalid HTML; %s undocumented public item(s), each crate at its recorded count)\n' "$crates" "$verdict"
exit 0
