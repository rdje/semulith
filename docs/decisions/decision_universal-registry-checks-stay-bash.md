# The four universal-registry checks the project owns stay bash; XTASK.6 closes on the project registry

- **Type:** `decision`
- **Date:** `2026-10-28`
- **Status:** `active`
- **Owner / source:** `XTASK.6` slice 6av, the leaf's closing review (`SEMULITH-XTASK-0060`), ruled under the
  delegation of 2026-10-26 (`decision_four-rulings-delegated.md`, authority `review`): a design choice the
  measurements settle — no profile claim, retained case or policy changes. Evidence: target/xtask/xt0060/census.txt.
answers: Why do MEMORY-ARCH, README-STABILITY, TASK-ACCEPTANCE and GAP-CLAIM-CENSUS stay bash when every project driver moved behind `cargo xtask`?

## The fact / decision

`XTASK.6` ported the drivers of the **project** registry (`scripts/check_doctrines.project.sh`): 41 entries, 41
of them shims of `cargo xtask`. It closes there. The **universal** registry (`scripts/check_doctrines.sh`, eleven
checks) stays bash — the seven scripts `scripts/update_scaffold.sh` re-syncs from the bedrock (its `NEUTRAL` list)
and the four whose copies the project owns and holds local: `scripts/check_memory_architecture.sh`,
`scripts/check_readme_stability.sh`, `scripts/check_task_acceptance.sh`, `scripts/check_gap_claims.sh`. No shim, no
port. `cargo xtask focused` already runs three of them by their bash paths, and README-ROUTES runs the fourth.

## Why

1. **The spine needs no toolchain.** The universal registry is the git-level layer every clone and every
   harness runs from the pre-commit hook. None of its eleven scripts invokes cargo: `grep -c cargo` finds two
   lines in all eleven, and both are evidence vocabulary — `cargo (test|…` in TASK-ACCEPTANCE's `DEFAULT_SIG` and
   `cargo ` in GAP-CLAIM-CENSUS's `CENSUS_RE`. The universal pass takes 3.1 s on bash, git and python3 alone
   (`XTASK.8`'s measurement). A shim would put a cold build of the xtask crate in front of the spine's first check.
2. **Each of the four is read or run as text, outside the crate.**
   - MEMORY-ARCH: `scripts/qualify_orientation_indexes.py` writes the script into a fixture with no crate, mutates
     one refusal line (`no-row-membership`) and runs it with bash.
   - README-STABILITY: README-ROUTES copies the script into its fixture repositories and runs it with bash, and
     reads its text for the hint targets it emits.
   - TASK-ACCEPTANCE: SEAM-INTEGRITY asks it for its effective rules (`--print-sig`, `--print-code-re`) and extracts
     its built-in defaults from its text; `scripts/probe_temporary_locality.py` reads its text.
   - GAP-CLAIM-CENSUS: SEAM-INTEGRITY reads its census vocabulary (`CENSUS_RE`) from its text.
   - All four: `scripts/probe_handoff_census.py` holds their bytes across a scaffold sync.
   A shim would empty the text these readers parse. Each reader would need rewiring and re-qualifying, and each
   fixture a crate. That is risk with no behaviour gained.
3. **Two carry repairs owed upstream.** TASK-ACCEPTANCE and GAP-CLAIM-CENSUS carry the source fixes for defects
   1–3 of `reference_upstream-spine-defects.md`, which is why `update_scaffold.sh` removed them from `NEUTRAL`.
   The bedrock template is bash, so a port to Rust would leave those repairs with no way back upstream.
   README-STABILITY (D54's text-metrics wiring) and MEMORY-ARCH (the D74/D75 map and decision-index readers, removed
   from `NEUTRAL` by `LIVE-CONTAINMENT.4`) are held local for the same kind of reason: project-owned repairs to
   universal checks that a sync would silently revert.

## How to apply

- Do not port or shim a script the universal registry names. The seven `NEUTRAL` scripts belong to the bedrock;
  the four project-owned copies stay bash, and a repair to one lands in bash, measured as before.
- A repair that is true of every adopter of the template joins the upstream list in
  `reference_upstream-spine-defects.md`.
- Revisit only if the bedrock itself ships its spine in Rust, or the director rules that the spine may depend on
  cargo. Related: `decision_rust-native-tooling.md`, `decision_alternate-port-and-features.md`.

## Correction (2026-10-28, `XTASK.4` slice 4b)

The universal registry has a twelfth, conditional entry this record left out: `KNOWLEDGE-MAP`
(`knowledge-map/scripts/check_knowledge_map.sh`, added when the subsystem exists). `XTASK.6` slice 6av called it "a submodule,
read-only" — wrong: `git ls-files -s knowledge-map` lists ordinary tracked files and `.gitmodules` names `vendor/linkedspec`
alone. It stays bash by this record's own reasons: it invokes no cargo; `scripts/update_scaffold.sh` holds it and its generator
local since `LIVE-CONTAINMENT.4` (the D74/D75 map readers); and `scripts/qualify_orientation_indexes.py` writes both into a
crate-less fixture, mutates their refusal lines and runs them with bash.
