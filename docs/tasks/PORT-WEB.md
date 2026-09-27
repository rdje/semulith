# PORT-WEB: run everything in the browser — JS + Wasm as a first-class target

## Metadata

- Tree ID: `PORT-WEB`
- Status: `done` (1/1 leaves complete `2026-09-27`; the browser target holds from the first crate)
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
| — | — | — | the tree is complete (1/1 leaves done); the Wasm build gate holds from the first crate |

## Task Tree

- ID: `PORT-WEB`
  Status: `done`
  Goal: the browser is a first-class target, proven by a Wasm build from the first crate
  Children: `PORT-WEB.1`

- ID: `PORT-WEB.1` — **the crate skeleton builds for Wasm from day one**
  Status: `done`
  Goal: `P1-LAB`'s crate skeleton builds for `wasm32-unknown-unknown` (and for the host)
  from its first slice; a check proves it, fired RED before registration.
  Acceptance: a Wasm build of the P1 crate skeleton succeeds in the same commit that
  creates the crate; a tracked check fails if the Wasm build breaks; host-only APIs are
  absent or feature-gated, demonstrated by the build itself.
  Result: met, `2026-09-27`, in the same commit that creates the crates (`SEMILITH-PL-0001`,
  with `P1-LAB.1`). `scripts/check_wasm_build.sh` (doctrine `PORT-WEB`, 20th registered)
  builds the whole workspace for `wasm32-unknown-unknown` on every commit; its `--self-test`
  (4 arms) builds scratch crates and asserts verdict AND reason; it was fired RED against the
  real workspace — a `std::os::unix` import in `semulith-core` — before registration. No
  host-only API exists yet, and the build itself is the standing proof of that (no seams
  needed at the skeleton).

  ## Acceptance Checklist (leaf PORT-WEB.1)

  - [x] **REPRODUCE / ISSUE** — the browser target was a decision without an instrument:

    ```
    $ git ls-files scripts | grep -c wasm
    0                                     # nothing checked the Wasm build
    $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
        Finished `dev` profile ...        # it built — by luck, not by gate
    ```

  - [x] **ROOT CAUSE (WHY + WHERE)** — `decision_browser-wasm-target` named the constraint but
    nothing enforced it; a host-only API added next commit would build fine on the host and
    break the browser silently. WHERE, measured: the driver registries
    (`scripts/check_doctrines*.sh`) carried no Wasm check — `grep -c PORT-WEB` → 0 in both.

  - [x] **FIX** — `scripts/check_wasm_build.sh`: preflight refuses with install instructions
    when the rustup target is absent (exit 2, never a silent pass); re-runs its 4-arm
    self-test before judging (refuses if it stops discriminating); `cargo build --workspace
    --target wasm32-unknown-unknown` is the verdict. Registered as the 20th project doctrine;
    CI (`doctrines.yml`) now installs the target; mirrors updated
    (`DOCTRINE_ENFORCEMENT.md`, the book's doctrines chapter, `TOOLBOX.md`).

  - [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

    ```
    $ bash scripts/check_wasm_build.sh --self-test
    PORT-WEB --self-test: 4 pass / 0 fail
    $ bash scripts/check_wasm_build.sh
    PORT-WEB: ok (workspace builds for wasm32-unknown-unknown)
    $ # fired RED against the real workspace before registration:
    $ printf '\nuse std::os::unix::ffi::OsStrExt as _;\n' >> crates/semulith-core/src/lib.rs
    $ bash scripts/check_wasm_build.sh; echo "rc=$?"
    PORT-WEB: FAIL — ... error[E0433]: cannot find `unix` in `os`  --> crates/semulith-core/src/lib.rs:13:14
    rc=1                                  # the import reverted the same minute
    ```

  - [x] **NO REGRESSION** — `make gate` re-run after registration (20 doctrines):
    `=== all doctrines green ===`; `make check` host suite green (5 suites, 0 warnings).
    The check's first cut was caught by its own harness — `bin` crates write `src/main.rs`
    not `src/bin.rs`, and cargo fails builds with rc=101, not 1: self-test reported
    `1 pass / 3 fail` until both were fixed. A control never run RED is not known to work.

  - [x] **LOCKSTEP** — `scripts/check_doctrines.project.sh`, `DOCTRINE_ENFORCEMENT.md`,
    `docs/book/src/working/doctrines.md`, `TOOLBOX.md`, `LIVE_STATUS.md` (20 registered, 231
    arms), `.github/workflows/doctrines.yml`, the book's P1 chapter, and this leaf — one commit.

  - `promotion: declined (both notes are recorded in this leaf's checklist and are per-slice history, not question-shaped lessons).`

  Verification: `PORT-WEB --self-test: 4 pass / 0 fail`; real run
  `PORT-WEB: ok (workspace builds for wasm32-unknown-unknown)`; RED fire rc=1 naming
  `crates/semulith-core/src/lib.rs:13`; `make gate` green after registration.
  Commit: `SEMILITH-PL-0001` (with `P1-LAB.1`, per this leaf's acceptance).
