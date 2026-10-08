# CI-RECOVERY: repair the pushed GitHub workflow failures

## Metadata

- Tree ID: `CI-RECOVERY`
- Status: `active`
- Roadmap lane: cross-cutting verification / zero-defect ownership; no milestone credit
- Created: `2026-10-08`
- Owner: repo-local workflow

## Goal

Repair the three latest failed workflows and the additional cross-endian defect;
verify their exact cold-run triggers and distinguish local evidence from hosted results.

## Non-Goals

- Do not weaken strict Clippy, skip books, or turn missing mandatory legs into passes.
- Do not claim GitHub green before the repaired commit has a successful hosted run.
- No exceptional push without the director's explicit approval act per COMMIT.md.

## Acceptance Criteria

1. Each reported failure is reproduced and repaired with focused controls.
2. Cold CI provisioning matches the tools and paths the checks actually need.
3. Local full CI passes; hosted verification remains explicit until a permitted push.
4. Every slice commits separately with live docs and book reflecting measured evidence.

## Task Tree

- ID: `CI-RECOVERY`
  Status: `active`
  Goal: restore hosted CI and truthful validation claims
  Children: `CI-RECOVERY.1`, `CI-RECOVERY.2`, `CI-RECOVERY.3`, `CI-RECOVERY.4`

- ID: `CI-RECOVERY.1` — strict stable Clippy
  Status: `proposed`
  Goal: replace the map_or identity in bench.rs with its equivalent unwrap_or; run
  strict lint and meaningful benchmark diagnostics on the current/tested toolchain.
  Acceptance: no lint suppression; same first-difference behavior; strict lint green.
  Verification: pending
  Commit: pending

- ID: `CI-RECOVERY.2` — provision the doctrine runner
  Status: `proposed`
  Goal: explicitly install a compatible mdbook in the clean GitHub job and audit the
  enforcer's other mandatory provisioning requirements using public tool interfaces.
  Acceptance: required book tool exists before the gate; cold provisioning verified.
  Verification: pending
  Commit: pending

- ID: `CI-RECOVERY.3` — portable cold Miri/endian legs
  Status: `proposed`
  Goal: create the output directory before redirections; remove the macOS-specific
  nightly name from the cross-endian target query; audit single-leg cold execution.
  Acceptance: hand stub controls on Linux/macOS shapes discriminate both old defects;
  the actual nightly/Miri result and any remaining provisioning gap are stated exactly.
  Verification: pending
  Commit: pending

- ID: `CI-RECOVERY.4` — local/hosted evidence and follow-through
  Status: `proposed`
  Goal: run make ci after all repairs, record toolchain differences and omitted/absent
  legs honestly, and observe all workflows after the next cadence/approved push.
  Acceptance: no remote-green claim from local checks; failures owned until verified.
  Verification: pending
  Commit: pending

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `CI-RECOVERY.1` | `proposed` | after LIVE-CONTAINMENT.4 slice (a) restores commit headroom |

## Decisions

- `2026-10-08`: read GitHub runs via authenticated gh. The latest pushed revision
  e1fe37942cba2eb4014a7a0f30dc7b9c8e0734e7 has three failures, and the current f356d76
  changes none of their affected files (`git diff e1fe379..HEAD -- .github/workflows
  crates/semulith-verify/src/bench.rs scripts/check_portability.sh`: empty).
  Root evidence:
  - Rust run https://github.com/rdje/semulith/actions/runs/37749540668: stable Rust
    1.99.0 Clippy map_or_identity at bench.rs:929–933; local Rust/Clippy is 1.95.0.
  - Doctrines https://github.com/rdje/semulith/actions/runs/37749541005: UNIT-BOOKS
    REFUSED, mdbook absent from PATH. Workflow provisions wasm/vendor but not mdbook.
  - Portability https://github.com/rdje/semulith/actions/runs/37749540622: miri.log
    redirection fails because target/portability does not exist in the cold Miri job.
  - `sed -n '180,200p' scripts/check_portability.sh` also exposes a macOS-only
    nightly-aarch64-apple-darwin target query used unconditionally on Linux; repair
    before claiming cross-endian verification. These are repository-owned defects.
  Priority: urgent before the next push; archive transition first, then these repairs,
  then P4 C/count staging. No interpretation of the archive approval authorizes a push.

## Open Questions

- Hosted verification waits for a permitted cadence or director-approved exceptional push.

## Blockers

- Hosted result waits for a permitted push; the archive transition restores local commit headroom.

## Acceptance Checklist

Discovery receipt only; the four repair leaves remain proposed and unverified.

- [x] **ROOT CAUSE** — `gh run view --log-failed` located `clippy::map_or_identity`
  on Rust 1.99.0, `UNIT-BOOKS: REFUSED` for missing mdbook, and the cold Miri log
  redirection failure. The run URLs and affected paths are recorded above.
- [x] **ADDRESSED (discovery)** — `git diff e1fe379..HEAD -- .github/workflows
  crates/semulith-verify/src/bench.rs scripts/check_portability.sh` returned no changes;
  all three failures remain. Four owned repair leaves now precede P4 staging.
  This checks ownership and scheduling, without claiming a repaired workflow.
- [x] **NO REGRESSION (discovery)** — the same `git diff` is empty: this discovery
  changes no workflow, Rust code or portability implementation. Archive verification
  remains with LIVE-CONTAINMENT.4 slice (a), not with this future repair tree.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-08` | discovery | gh run list/view, current-path diff, toolchain versions | three failures remain; roots and priority owned above |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| discovery | included in LIVE-CONTAINMENT.4 slice (a) | owned before any CI code changes |

## Changelog

- `2026-10-08`: Created from the director's hosted-CI status question; four repairs scheduled.
