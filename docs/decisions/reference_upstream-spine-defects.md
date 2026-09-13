# Defects found in the bedrock spine — fixed at source here, unfixed upstream

- **Type:** `reference`
- **Date:** `2026-09-13`
- **Status:** `active`
- **Owner / source:** found while executing `SEMULITH-PKG` and `P0-PROFILE`; each was worked
  around locally through a sanctioned `.doctrine/` seam, never by editing a neutral check

## The fact

This repository is built on `bedrock-scaffold 0.6.1`. Four defects in that **template** were
found by using it, not by reading it. **All four are now fixed in this repository's own copies
of the affected files.** None is fixed upstream, because upstream is a separate project this
repository does not own.

⛔ **They were first fixed through `.doctrine/` seams, and that was not good enough.** Moving
both seam files aside and re-running the full enforcer produced `=== all doctrines green ===`,
`rc=0` — every fix silently reverted and nothing said a word. *A fix whose disappearance is
undetectable is not a fix; it is a configuration that happens to be present.* The seams remain,
carrying the genuinely project-specific part, but the defects themselves are repaired in the
checks.

| # | Defect | Evidence | Local handling |
| --- | --- | --- | --- |
| 1 | `TASK-ACCEPTANCE`'s default evidence signatures do not recognise `git grep` or `grep -c`, while its sibling `GAP-CLAIM-CENSUS` prints `git grep -n … \| wc -l` in its own failure hint and accepts it as a census. Obeying one gate produces evidence the other refuses. | `grep -o "git (ls-files[^\|]*\|[^)]*)" scripts/check_task_acceptance.sh` → `git (ls-files\|log -S\|…\|show )`; `grep -n "git grep" scripts/check_gap_claims.sh` → its `CENSUS_RE` and its printed hint | **fixed at source**: `check_task_acceptance.sh` now imports `CENSUS_RE` from `check_gap_claims.sh`, so the two gates share one vocabulary by construction — 19 instruments the acceptance gate previously refused |
| 2 | The default `code_paths` pattern `(^\|/)(crates\|src\|scripts)/…` classifies mdBook prose as code, because `docs/book/src/` contains the segment `src/`. | `git ls-files \| grep -E "$DEFAULT" \| grep -c '^docs/book/src/'` → `28` of `125` tracked files | **fixed at source**: the default pattern anchors `src/` to the repository root. A `src/` at the root is a source tree; one deep inside a docs tree is not |
| 3 | That same default **misses** files that genuinely change behaviour: `.githooks/*`, `.github/workflows/*`, `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `.doctrine/*`, and any gate-data registry. | the set difference in the same census → `12` files the default cannot see | **fixed at source**: `^\.githooks/`, `^\.github/workflows/` and `^Cargo\.(toml\|lock)$` added to the default — behaviour-governing in any git/Rust project, so neutral-safe |
| 4 | `README_POLICY.md` as shipped predates the *Routing pressure closure* section, so a project adopting it bounds its landing page without bounding the destinations that page routes to. | shipped copy 74 lines / 7,669 bytes; the director's current revision 159 lines / 8,279 bytes | refreshed under a fenced adoption note; `README-ROUTING-CLOSURE` added as a project doctrine |

## What is fixed where, and why the split is not arbitrary

| Lives in | Carries | Why there |
| --- | --- | --- |
| `scripts/check_task_acceptance.sh` | the anchored `src/`, the three universal behaviour families, the imported census vocabulary, the gate-verdict shape | true of **every** consumer of the template; hardcoding them is a repair, not a fork |
| `.doctrine/code_paths.txt` | `^\.doctrine/`, `^doctrine/.*\.tsv$`, `^docs/provenance/[^/]+/dispositions\.tsv$`, `^rust-toolchain\.toml$` | this project's own gate **data**; a neutral check cannot know these exist |
| `.doctrine/evidence_tokens.txt` | this project's tool signatures (`probes:`, hashes, `--self-test`, the Python failure banner) | this project's instruments |
| `scripts/update_scaffold.sh` | both repaired checks **removed** from the `NEUTRAL` re-sync list | they now carry project-owned repairs; re-syncing would silently revert them |
| `scripts/check_seam_integrity.sh` | the gate that makes every line above non-silent | a repair nothing watches is a repair with an expiry date nobody knows |

Measured with **both seam files moved aside**, so only the source fixes are in play: prose
classified as code `0` (was 28); hooks, workflows and manifest covered `6/6` (was 0); census
instruments accepted `5/5`. The defects are gone, not compensated.

## Why this is worth recording rather than just fixing

Defects 1–3 are all the same shape: **a neutral check's built-in assumption about a project it
has never seen.** The seams exist precisely for that, and using them is correct. But a seam
edit is invisible to the next project that copies the template, so every adopter re-discovers
the same three refusals. That is a template defect, not an adopter defect.

Defect 1 also has a second lesson, which is the one worth carrying: two gates written at
different times share no vocabulary unless something forces them to.

## How to apply

- When a gate refuses honest evidence here, **do not weaken the evidence and do not waive**.
  Check whether a sibling doctrine already blesses the instrument, declare it in `.doctrine/`,
  and then **fire the gate RED** to prove the widening did not make it vacuous.
- If you are declaring a token for the third time, the declaration is the wrong shape — match
  the shape the tools print, not the instances.
- If `bedrock` is ever updated from this project, these four are the changes to carry upstream —
  and the two repaired checks are **off** the `update_scaffold.sh` re-sync list, so a scaffold
  update will not quietly undo them.
- `SEAM-INTEGRITY` asserts the **behaviour**, not the presence of a file, so it catches a revert
  from any direction: a deleted seam, a narrowed pattern, a scaffold overwrite, or a spine
  update that stops consuming the seam altogether.

Related: [[decision_readme-routing-closure]], [[decision_claim-verification-adopted]].
