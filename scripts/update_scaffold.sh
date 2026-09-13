#!/usr/bin/env bash
# scripts/update_scaffold.sh — pull the latest project-NEUTRAL spine from the bedrock
# template into THIS project, WITHOUT touching your roadmap, task-trees, decisions, or code.
#
#   scripts/update_scaffold.sh <bedrock-repo-url-or-local-path>
#
# Only the files listed in NEUTRAL below are re-synced. Everything project-owned
# (CLAUDE.md, README.md, ROADMAP.md, the live-docs, the project doctrine slot, the curated
# subsystems.md, and all of docs/tasks/ + docs/decisions/ records) is deliberately left
# alone. After syncing: review `git diff`, run `make gate`, and commit.
set -euo pipefail
URL="${1:-}"
[ -n "$URL" ] || { echo "usage: scripts/update_scaffold.sh <bedrock-repo-url-or-local-path>" >&2; exit 2; }
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
if [ -d "$URL/.git" ]; then
  cp -R "$URL" "$tmp/bedrock"
else
  git clone --depth 1 "$URL" "$tmp/bedrock" >/dev/null 2>&1 || { echo "clone failed: $URL" >&2; exit 1; }
fi

# The project-NEUTRAL spine — safe to overwrite because it never carries project content.
#
# ⛔ scripts/check_task_acceptance.sh and scripts/check_gap_claims.sh were REMOVED from this
# list. This repository carries source fixes in them (an unanchored `src/` that classified 28
# files of mdBook prose as code; three families of behaviour-governing files the default could
# not see; and a signature set that refused the census instruments its sibling gate recommends).
# Re-syncing them would silently revert those fixes — and a fix whose disappearance is
# undetectable is not a fix. SEAM-INTEGRITY would still catch the revert behaviourally, but a
# tool should not be quietly undoing a repair and relying on another tool to notice.
# See docs/decisions/reference_upstream-spine-defects.md; carry the fixes upstream instead.
NEUTRAL=(
  MEMORY_ARCHITECTURE.md
  DOCTRINE_ENFORCEMENT.md
  TOOLBOX.md
  README_POLICY.md
  COMMIT.md
  AGENTS.md
  docs/TASK_TREE.md
  docs/TASK_TREE_README.md
  docs/tasks/TEMPLATE.md
  docs/decisions/TEMPLATE.md
  .githooks/pre-commit
  .githooks/commit-msg
  scripts/check_doctrines.sh
  scripts/check_memory_architecture.sh
  scripts/check_live_doc_currency.sh
  scripts/check_no_background_jobs.sh
  scripts/check_lesson_promotion.sh
  scripts/check_routing_evidence.sh
  scripts/check_table_arity.sh
  scripts/check_readme_stability.sh
  scripts/check_waiver_routing.sh
  .doctrine/README.md
  scripts/check_docpaths.sh
  scripts/check_task_tree_ownership.sh
  knowledge-map/scripts/gen_knowledge_map.sh
  knowledge-map/scripts/check_knowledge_map.sh
  DOCTRINE_VERSION
)

n=0
for f in "${NEUTRAL[@]}"; do
  if [ -f "$tmp/bedrock/$f" ]; then
    mkdir -p "$(dirname "$f")"
    cp "$tmp/bedrock/$f" "$f"
    echo "  synced $f"
    n=$((n+1))
  fi
done
chmod +x scripts/*.sh knowledge-map/scripts/*.sh .githooks/pre-commit .githooks/commit-msg 2>/dev/null || true

echo "✓ $n scaffold file(s) synced to $(cat DOCTRINE_VERSION 2>/dev/null || echo '?')."
echo "  Review 'git diff', run 'make gate', then commit."
