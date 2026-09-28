#!/usr/bin/env bash
# scripts/check_changelog_shards.sh — SHARD-FREEZE (project doctrine).
#
# `CHANGELOG.md` and `DEV_NOTES.md` are append_history surfaces: when one crosses its ceiling,
# its oldest entries move to frozen shards under `docs/changelog/` (`scripts/shard_history.py`)
# — one shard family carries both heads (the registry row says so; a shard's first line names
# the head it was cut from). A shard is a promise — its bytes never change after the shard
# event — and a manifest is only as good as the check that reads it. This is that check.
#
# What is proved, durable past the shard event itself (the tool proves completeness AT the event;
# these legs keep the promise afterwards):
#   1. COVERAGE    every *.md under docs/changelog/ carries a manifest row, and every row names an
#                  existing shard there — an unmanifested shard is frozen by nobody; a row pointing
#                  at nothing is a promise about a file that does not exist.
#   2. FROZEN      every shard hashes to its row — one edited byte after the shard fails here,
#                  with the file and both digests named.
#   3. APPEND-ONLY every row committed at HEAD is present, unchanged, in the working manifest —
#                  history may grow, it may never be rewritten. Judged against
#                  `git show HEAD:docs/changelog/SHARDS.sha256`.
#   4. UNIQUE      no `## ` entry heading appears twice across the live heads and the shards —
#                  the heads are independent histories, but a heading carried twice anywhere in
#                  the family means the partition lost or copied an entry (or a head repeats its
#                  own), and with unit-id/date-prefixed headings a real collision cannot fire
#                  spuriously.
#
# ⛔ Fired RED on the real tree before registration: the adoption commit adds the manifest, so the
# tree without it reports every shard UNMANIFESTED (shown in the task leaf DOC-SHARDING.1).
# ⛔ Fired RED again when DOC-SHARDING.2 taught the check the two-head family: a scratch shard
# carrying a live DEV_NOTES.md heading was flagged DUPLICATED ENTRY (probe recorded in the leaf).
#
# ⚠️ HONEST LIMIT: it proves the partition is frozen, complete and unrewritten from the first
# committed manifest onward. The shard EVENT's completeness (head-before == head-after + shard,
# order and bytes exact) is the tool's proof, printed at the event and recorded in the tree.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "SHARD-FREEZE: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

# $1 root  $2 shard dir rel  $3 manifest rel  $4 previous-manifest file ("" = none)
# $5... live append-history heads (rels)
check_shards() {
python3 - "$@" <<'PY'
import hashlib, re, sys, pathlib

root = pathlib.Path(sys.argv[1])
shard_rel, manifest_rel, prev_path = sys.argv[2:5]
heads = [root / h for h in sys.argv[5:]]
shard_dir = root / shard_rel
manifest = root / manifest_rel
findings = []

ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>\S+)$")
ENTRY = re.compile(r"^## (.+)$", re.M)

shards = sorted(shard_dir.glob("*.md")) if shard_dir.is_dir() else []
rows: list[tuple[str, str, int]] = []           # (digest, path, lineno)
if manifest.is_file():
    for n, line in enumerate(manifest.read_text().splitlines(), 1):
        if not line.strip():
            continue
        m = ROW.match(line)
        if not m:
            findings.append(f"MALFORMED  {manifest_rel}:{n}: not a sha256sum row — "
                            f"'{line}' — the manifest is data, not prose")
            continue
        rows.append((m.group("digest"), m.group("path"), n))

if not shards and not rows:
    print(f"NO SHARDS  {shard_rel} holds no shard and {manifest_rel} no rows — "
          f"a freeze check with nothing frozen cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

# 1. COVERAGE ----------------------------------------------------------------------
by_path = {}
for digest, rel, n in rows:
    by_path.setdefault(rel, []).append((digest, n))
for rel, dups in sorted(by_path.items()):
    if len(dups) > 1:
        findings.append(f"DUPLICATE ROW {manifest_rel}: '{rel}' is manifested "
                        f"{len(dups)} times (lines {[n for _, n in dups]})")
for p in shards:
    rel = p.relative_to(root).as_posix()
    if rel not in by_path:
        findings.append(f"UNMANIFESTED {rel}: a shard with no manifest row is frozen by nobody")
for rel, entries in sorted(by_path.items()):
    p = root / rel
    if not p.is_file():
        findings.append(f"MISSING     {rel}: manifested but does not exist")
    elif p.parent != shard_dir:
        findings.append(f"NOT A SHARD {rel}: the manifest may only freeze *.md files directly "
                        f"under {shard_rel}/ — {rel} escapes the partition")
    elif p not in shards:
        findings.append(f"NOT A SHARD {rel}: manifested but is not a *.md shard")

# 2. FROZEN ------------------------------------------------------------------------
for digest, rel, n in rows:
    p = root / rel
    if p.is_file() and p.parent == shard_dir:
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != digest:
            findings.append(f"THAWED      {rel}: the shard changed after the shard event — "
                            f"manifest {digest[:12]}…, file {actual[:12]}… "
                            f"(manifest line {n}). Entries in a shard are never edited")

# 3. APPEND-ONLY -------------------------------------------------------------------
if prev_path:
    prev = pathlib.Path(prev_path)
    if prev.is_file():
        current = {}
        for digest, rel, n in rows:
            current[rel] = digest
        for line in prev.read_text().splitlines():
            m = ROW.match(line)
            if not m:
                continue
            rel, digest = m.group("path"), m.group("digest")
            if rel not in current:
                findings.append(f"REMOVED ROW {rel}: a manifest row committed at HEAD is gone — "
                                f"the manifest only grows, history is never rewritten")
            elif current[rel] != digest:
                findings.append(f"MODIFIED ROW {rel}: the manifest row changed after being "
                                f"committed — frozen means frozen, including the manifest")

# 4. UNIQUE ------------------------------------------------------------------------
seen: dict[str, str] = {}
for label, path in [(h.name, h) for h in heads] + [(p.name, p) for p in shards]:
    if not path.is_file():
        continue
    for eid in ENTRY.findall(path.read_text()):
        if eid in seen:
            findings.append(f"DUPLICATED ENTRY '{eid}': appears in both {seen[eid]} and "
                            f"{label} — the partition must hold every entry exactly once")
        else:
            seen[eid] = label

for f in findings:
    print(f)
print(f"__CHECKED__ {len(rows)}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/docs/changelog"

  # ⛔ STRICT ARITY — docs/knowledge/self-test-arms-that-never-ran.md. A helper that ignores
  # surplus arguments swallows a whole following command when a `;` is missing, silently.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'SHARD-FREEZE self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }

  HEAD="$t/CHANGELOG.md"; HEAD2="$t/DEV_NOTES.md"; SDIR="$t/docs/changelog"; MAN="$t/docs/changelog/SHARDS.sha256"
  FAKE64="$(head -c 64 /dev/zero | tr '\0' 'a')"
  prev() { argc 1 "$#" prev || return; printf '%s' "$1" > "$t/prev.sha256"; }

  shard1() { printf '# shard\n\n## entry-old\nbody\n' > "$SDIR/2026-09-a.md"; }
  shard2() { printf '# shard\n\n## entry-older\nbody\n' > "$SDIR/shard-0001.md"; }
  headf()  { printf '# CHANGELOG.md\n\n## entry-new\nbody\n' > "$HEAD"
             printf '# DEV_NOTES.md\n\n## entry-live\nbody\n' > "$HEAD2"; }
  manifest() { # manifest <extra-rows...>
    rm -f "$t/prev.sha256"
    { sha256sum "$SDIR"/*.md 2>/dev/null | sed "s|$t/||"
      for extra in "$@"; do printf '%s\n' "$extra"; done; } > "$MAN"
  }
  run() { check_shards "$t" "docs/changelog" "docs/changelog/SHARDS.sha256" \
            "$([ -f "$t/prev.sha256" ] && printf '%s' "$t/prev.sha256")" \
            "CHANGELOG.md" "DEV_NOTES.md"; }
  arm() { # arm <name> <expected-rc> <expected-substring>
    argc 3 "$#" arm || return
    out="$(run 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'SHARD-FREEZE self-test MISS: %s expected rc=%s got rc=%s\n%s\n' \
        "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'SHARD-FREEZE self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' \
        "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  rm -f "$t/prev.sha256"
  shard1; shard2; headf; manifest
                                                              arm "GREEN frozen shards and a true manifest" 0 "__CHECKED__ 2"
  shard1; shard2; headf; manifest
  printf 'x' >> "$SDIR/shard-0001.md"
                                                              arm "RED   a shard edited after the event" 1 "THAWED"
  shard1; shard2; headf; manifest
  prev "$(sha256sum "$SDIR/2026-09-a.md" | sed "s|$t/||")
$(printf '0%s  docs/changelog/shard-0001.md' "$(sha256sum "$SDIR/shard-0001.md" | awk '{print $1}' | cut -c2-)")"
                                                              arm "RED   a committed row's content changed" 1 "MODIFIED ROW"
  shard1; shard2; headf
  printf '# shard\n\n## entry-oldest\nbody\n' > "$SDIR/shard-0002.md"
  manifest                                                       # 3 rows
  cp "$MAN" "$t/prev.sha256"                                     # the committed manifest
  rm "$SDIR/shard-0002.md"
  { sha256sum "$SDIR"/*.md | sed "s|$t/||"; } > "$MAN"           # 2 rows, prev untouched
                                                              arm "RED   a committed row removed" 1 "REMOVED ROW"
  shard1; shard2; headf; manifest
  rm "$SDIR/shard-0001.md"
                                                              arm "RED   a manifested shard deleted" 1 "MISSING"
  shard1; shard2; headf; manifest
  rm "$MAN"
                                                              arm "RED   shards nothing manifests" 1 "UNMANIFESTED"
  shard1; shard2; headf; manifest "$FAKE64  docs/changelog/ghost.md"
                                                              arm "RED   a row for a file that does not exist" 1 "MISSING"
  shard1; shard2; headf; manifest "$FAKE64  docs/other.md"
  printf 'x\n' > "$t/docs/other.md"
                                                              arm "RED   a row escaping the shard directory" 1 "NOT A SHARD"
  shard1; shard2; headf; manifest "not-a-hash row"
                                                              arm "RED   a malformed manifest line" 1 "MALFORMED"
  shard1; shard2; headf; manifest "$(sha256sum "$SDIR/2026-09-a.md" | sed "s|$t/||")"
                                                              arm "RED   the same shard manifested twice" 1 "DUPLICATE ROW"
  shard1; shard2; headf; printf '# CHANGELOG.md\n\n## entry-old\nalso here\n' > "$HEAD"
  manifest
                                                              arm "RED   an entry duplicated across head and shard" 1 "DUPLICATED ENTRY"
  # DOC-SHARDING.2 — the family carries two live heads; every heading is unique across
  # heads and shards (unit-id/date prefixes make a spurious collision impossible).
  shard1; shard2; headf; manifest
                                                              arm "GREEN two live heads share one frozen partition" 0 "__CHECKED__ 2"
  shard1; shard2; headf
  printf '# DEV_NOTES shard — probe\n\n## entry-live\nstolen from the live head\n' > "$SDIR/shard-0002.md"
  manifest
                                                              arm "RED   a shard carrying either live head's entry" 1 "DUPLICATED ENTRY"
  rm "$SDIR/shard-0002.md"; shard1; shard2; headf; manifest
  cp "$MAN" "$t/prev.sha256"
                                                              arm "GREEN committed rows unchanged under an append-only manifest" 0 "__CHECKED__ 2"
  rm -rf "$t"
  printf 'SHARD-FREEZE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -f CHANGELOG.md ] || { echo "SHARD-FREEZE: ok (no CHANGELOG.md yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "SHARD-FREEZE: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

prev="$(mktemp)"
if git show HEAD:"docs/changelog/SHARDS.sha256" > "$prev" 2>/dev/null; then :; else rm -f "$prev"; prev=""; fi
out="$(check_shards "$ROOT" "docs/changelog" "docs/changelog/SHARDS.sha256" "$prev" \
        "CHANGELOG.md" "DEV_NOTES.md")"
rc=$?
rm -f "$prev"
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "SHARD-FREEZE: REFUSED — the shard corpus could not be read, so the freeze cannot be judged."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "SHARD-FREEZE: the sharded history is thawed, incomplete, or rewritten."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The SHARDS are authoritative. Restore the bytes — never edit a shard or its manifest"
    echo "  to make the check pass; shard_history.py grows the partition, it never rewrites it."; } >&2
  exit 1
fi
printf 'SHARD-FREEZE: ok (%s shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)\n' "${count:-0}"
exit 0
