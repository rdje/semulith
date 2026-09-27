# PORT-WEB: run everything in the browser — JS + Wasm as a first-class target

## Metadata

- Tree ID: `PORT-WEB`
- Status: `proposed`
- Roadmap lane: portability — the browser/Wasm target (`ROADMAP.md` §1, `decision_browser-wasm-target`)
- Gate: contributes the Wasm build to `P1-LAB`'s G1; no doctrine gate of its own
- Consumed by: `P1-LAB` — the crate skeleton must build for `wasm32-unknown-unknown` from
  its first slice; the browser harness itself is consumed later by the per-model mdBook
  (dual-mandate demos) and, much later, archogen-in-browser
- Depends on: director vision `2026-09-27` — *"run everything in the browser (JS + Wasm)"*
- Unlocks: browser-hosted teaching demos; an install-free consumer of every model
- Created: `2026-09-27`
- Owner: repo-local workflow

## Goal

Make the browser a first-class delivery target for every Semulith model. The engine stays
Rust compiled to `wasm32`; the data-driven interpreter is the portable core; host-native is
a build mode, not the architecture. The lane starts with the build constraint at P1 and
grows the harness only after the target holds.

## Non-Goals

- **Not a JavaScript rewrite.** JS is the host the Wasm module talks to, not an engine.
- **Not a GUI.** A graphical desktop is already out of the first-CPU scope; this lane owns
  the Wasm target and a minimal runner, not a UI programme.
- **Not host-side tooling in the browser.** The Python doctrine/tooling layer is
  build-time machinery and stays host-side.
- **Not now.** The tree is `proposed`: its first leaf activates with `P1-LAB.1`.

## Acceptance Criteria

1. The engine crate builds for `wasm32-unknown-unknown` from P1's first slice, enforced the
   way the house enforces things — a check with arms, fired RED before it is trusted, not a
   statement.
2. Anything that cannot meet the Wasm target (host-only capability) sits behind an explicit
   seam the Wasm build proves unused.
3. Each completed leaf is committed through `COMMIT.md`; live docs and the mdBook carry the
   target where they describe what ships.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `PORT-WEB.1` | `pending` | activates with `P1-LAB.1` — the crate skeleton builds for `wasm32-unknown-unknown` from the first slice |

## Task Tree

- ID: `PORT-WEB`
  Status: `active`
  Goal: the browser is a first-class target, proven by a Wasm build from the first crate
  Children: `PORT-WEB.1`

- ID: `PORT-WEB.1` — **the crate skeleton builds for Wasm from day one**
  Status: `pending`
  Goal: `P1-LAB`'s crate skeleton builds for `wasm32-unknown-unknown` (and for the host)
  from its first slice; a check proves it, fired RED before registration.
  Acceptance: a Wasm build of the P1 crate skeleton succeeds in the same commit that
  creates the crate; a tracked check fails if the Wasm build breaks; host-only APIs are
  absent or feature-gated, demonstrated by the build itself.
  Verification: `pending`
  Commit: `pending`
