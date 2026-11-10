# scripts/doctrine_skip.sh — when the commit gate may answer a check from its last green run (sourced, never run).
#
# XTASK.8 slice d (docs/decisions/decision_docs-only-gate-path.md) let a check skip on a commit that staged nothing
# inside the check's DECLARED INPUTS. That is sound only while the declaration is complete, and it was not, twice:
#   - the six declared checks' drivers moved into xtask/ on 2026-10-27 and 28 and no declaration named xtask/, so a
#     commit that changed only a driver could skip that driver's own check (11 commits could);
#   - PROFILE-CONSISTENCY reads four documents — three decision records the dossier's selections name, and a
#     unit-book page a probe opens — and its declaration named no document.
#
# The declaration is turned round (XTASK.16, measured in target/xtask/xt0090). The gate declares the LEDGER: the few
# documentation paths that record the work and that no skipping check reads. A skipping check is answered from its
# last green run only when EVERY staged path is ledger, and every tracked byte outside the ledger is identical to
# that run. Everything else runs the check: xtask/, crates/, the manifests, the hooks, a unit book, a document nobody
# listed, a directory added next year. Nothing has to list code, and a wrong omission costs time, never soundness.
#
# A ledger document that tracked data names is not ledger: a dossier that reads or pins a document makes it an input.
# That set is derived from the index at every commit, so a new selection naming a decision record needs no edit here.
#
# The measurement the ledger rests on: with every documentation file absent from the working tree, CONTRACT-FREEZE,
# DEF-GEN, ARTIFACT-COHORT, RECORD-SCHEMA and GUEST-GEN pass, and PROFILE-CONSISTENCY passes with its four present.
# `scripts/probe_ledger_independence.sh` repeats it; run it when a check gains a document.
#
# Callers set `staged` (one path per line: `git diff --cached --name-only`) and run inside the committing repository,
# whose index — the hook's GIT_INDEX_FILE — is the one these functions must describe. Nothing here unsets a GIT_*.

# A trailing slash is a directory; anything else is one file.
DOCTRINE_LEDGER="docs/tasks/ docs/changelog/ docs/decisions/ docs/knowledge/ docs/TASK_TREE.md docs/TASK_TREE_CLOSED.md docs/ARTIFACT_CLEANUP.md CHANGELOG.md MEMORY.md LIVE_STATUS.md KNOWLEDGE_MAP.md DEV_NOTES.md"

# id -> exit 0 for a check that may be answered from its last green run on a ledger-only commit
doctrine_skips() {
  case "$1" in
    PROFILE-CONSISTENCY|GUEST-GEN|RECORD-SCHEMA|ARTIFACT-COHORT|DEF-GEN|CONTRACT-FREEZE) return 0;;
    *) return 1;;
  esac
}

# -> the documents tracked data names, one per line: every quoted docs/ path in an indexed file of the data families
doctrine_named_documents() {
  git grep --cached -h -o -E '"docs/[A-Za-z0-9_./-]+"' -- profiles evidence schema definitions materials 2>/dev/null \
    | tr -d '"' | LC_ALL=C sort -u
}

# path, entry -> exit 0 when the entry (a directory with its slash, or one file) covers the path
doctrine_covers() {
  case "$2" in */) case "$1" in "$2"*) return 0;; esac; return 1;; *) [ "$1" = "$2" ];; esac
}

# path, the named documents -> exit 0 when the path is ledger that no tracked data names
doctrine_is_ledger() {
  local entry
  while IFS= read -r entry; do
    [ -n "$entry" ] || continue
    doctrine_covers "$1" "$entry" && return 1
  done <<< "$2"
  for entry in $DOCTRINE_LEDGER; do
    doctrine_covers "$1" "$entry" && return 0
  done
  return 1
}

# the named documents -> exit 0 when something is staged and every staged path is ledger
doctrine_only_ledger() {
  local path seen=0
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    seen=1
    doctrine_is_ledger "$path" "$1" || return 1
  done <<< "$staged"
  [ "$seen" = 1 ]
}

# the named documents -> the digest of everything tracked outside the ledger, as the index carries it (each
# `git ls-files -s` line: mode, blob id, path); nothing when it cannot be computed, and every check then runs
doctrine_inputs_key() {
  local listing named
  # one line for awk: BSD awk refuses a newline inside a -v string, and a named path holds no space by its pattern
  named="$(printf '%s' "$1" | tr '\n' ' ')"
  listing="$(git ls-files -s 2>/dev/null | awk -v ledger="$DOCTRINE_LEDGER" -v named="$named" '
    function covers(path, entry) { return entry ~ /\/$/ ? index(path, entry) == 1 : path == entry }
    BEGIN { nl = split(ledger, L, " "); nn = split(named, N, " ") }
    { path = $0; sub(/^[^\t]*\t/, "", path); led = 0
      for (i = 1; i <= nl; i++) if (covers(path, L[i])) { led = 1; break }
      if (led) for (i = 1; i <= nn; i++) if (N[i] != "" && covers(path, N[i])) { led = 0; break }
      if (!led) print }')" || return 0
  [ -n "$listing" ] || return 0
  if command -v shasum >/dev/null 2>&1; then printf '%s\n' "$listing" | shasum -a 256 | cut -c1-64
  elif command -v sha256sum >/dev/null 2>&1; then printf '%s\n' "$listing" | sha256sum | cut -c1-64
  else printf '%s\n' "$listing" | python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())' 2>/dev/null; fi
}
