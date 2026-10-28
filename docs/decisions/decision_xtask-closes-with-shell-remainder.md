# XTASK closes with its 13 remaining scripts in shell

- **Type:** `decision`
- **Date:** `2026-10-28`
- **Status:** `active`
- **Owner / source:** the director, 2026-10-28, granting `XTASK.4` slice 4b's proposal
  ([`decision_director-rulings-2026-10-28.md`](decision_director-rulings-2026-10-28.md)). Authority `director`.
answers: Does every shell script have to move behind cargo xtask before the XTASK tree closes?

## The fact / decision

No. `XTASK.4` closes with one script of fourteen ported (`build_bench.sh`, slice 4a) and 13 in shell, each for
the constraint slice 4b measured (target/xtask/xt0062/census.txt): the hook family (pre-push, its body, the
push cadence, the knowledge-map generator the pre-commit hook runs), three network fetchers, a script a capture
reads as text, the template's updater, a one-line forwarder, the handoff census, the bootstrap, and the
portability instrument whose controls stub `cargo` on PATH. The tree closes once its open questions are
answered or routed (the doctrine questions by `decision_doctrine-controls-refuse-and-freeze.md`).

## Why

Every remaining port would trade a measured property (a hook's stability, an offline measurement, a pinned
reader, a toolchain-free bootstrap, a working control) for no behaviour gained.

## How to apply

- New project doctrine drivers keep the XTASK.6 shape (a module behind a held shim); the spine and the 13
  stay shell. A reason to port one of the 13 later is a new leaf, measured like any other.
