#!/usr/bin/env bash
# scripts/check_rustdoc.sh — API-DOCS doctrine: the API reference is rustdoc, and its links and HTML are sound.
#
# The director's direction (decision_rust-native-tooling, 2026-10-23): SEMULITH's API reference is
# produced by rustdoc from the code (tree RUSTDOC). A reference whose intra-doc links point nowhere,
# point at private items a reader cannot open, or whose prose swallows text into an unclosed HTML tag
# is a reference that lies quietly. This check builds the workspace's docs offline with exactly three
# rustdoc lints denied — broken_intra_doc_links, private_intra_doc_links, invalid_html_tags — and
# refuses any occurrence, naming file, line and lint. Missing documentation is NOT denied here: that
# is a ratchet of its own (RUSTDOC.3), and denying it now would fail on 268 pre-existing gaps.
#
# Measured at adoption (RUSTDOC.1, 2026-10-23): the real tree carried 19 such defects (9 unresolved
# links, 4 links to private items, 6 unclosed HTML tags); the check was fired RED on it before the
# repair. A check with arms: --self-test documents scratch crates and asserts verdict AND reason.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
LINTS="-D rustdoc::broken_intra_doc_links -D rustdoc::private_intra_doc_links -D rustdoc::invalid_html_tags"

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

out="$(RUSTDOCFLAGS="$LINTS" cargo doc --workspace --no-deps --offline 2>&1)"; rc=$?
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
crates="$(printf '%s\n' "$out" | grep -c ' Documenting ')"
printf 'API-DOCS: ok (%s crate(s) documented; no broken or private intra-doc link, no invalid HTML)\n' "$crates"
exit 0
