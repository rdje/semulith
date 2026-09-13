# Defects found in the bedrock spine, which this project cannot fix at source

- **Type:** `reference`
- **Date:** `2026-09-13`
- **Status:** `active`
- **Owner / source:** found while executing `SEMULITH-PKG` and `P0-PROFILE`; each was worked
  around locally through a sanctioned `.doctrine/` seam, never by editing a neutral check

## The fact

This repository is built on `bedrock-scaffold 0.6.1`. Four defects in that **template** were
found by using it, not by reading it. Each is fixed locally; none is fixed upstream, because
upstream is a separate project this repository does not own. They are recorded here so that
whoever maintains `bedrock` can act on them, and so a future agent here does not re-diagnose
them.

| # | Defect | Evidence | Local handling |
| --- | --- | --- | --- |
| 1 | `TASK-ACCEPTANCE`'s default evidence signatures do not recognise `git grep` or `grep -c`, while its sibling `GAP-CLAIM-CENSUS` prints `git grep -n … \| wc -l` in its own failure hint and accepts it as a census. Obeying one gate produces evidence the other refuses. | `grep -o "git (ls-files[^\|]*\|[^)]*)" scripts/check_task_acceptance.sh` → `git (ls-files\|log -S\|…\|show )`; `grep -n "git grep" scripts/check_gap_claims.sh` → its `CENSUS_RE` and its printed hint | declared in `.doctrine/evidence_tokens.txt`; refused **three** times before the declaration was given the right *shape* rather than another name |
| 2 | The default `code_paths` pattern `(^\|/)(crates\|src\|scripts)/…` classifies mdBook prose as code, because `docs/book/src/` contains the segment `src/`. | `git ls-files \| grep -E "$DEFAULT" \| grep -c '^docs/book/src/'` → `28` of `125` tracked files | `.doctrine/code_paths.txt` declares an allow-list; all three outcomes fired and observed |
| 3 | That same default **misses** files that genuinely change behaviour: `.githooks/*`, `.github/workflows/*`, `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `.doctrine/*`, and any gate-data registry. | the set difference in the same census → `12` files the default cannot see | same declaration; the declared set is the default **+12 −28** |
| 4 | `README_POLICY.md` as shipped predates the *Routing pressure closure* section, so a project adopting it bounds its landing page without bounding the destinations that page routes to. | shipped copy 74 lines / 7,669 bytes; the director's current revision 159 lines / 8,279 bytes | refreshed under a fenced adoption note; `README-ROUTING-CLOSURE` added as a project doctrine |

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
- If `bedrock` is ever updated from this project, these four are the changes to carry upstream.

Related: [[decision_readme-routing-closure]], [[decision_claim-verification-adopted]].
