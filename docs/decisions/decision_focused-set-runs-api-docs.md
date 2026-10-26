# The focused check set runs API-DOCS

- **Type:** `decision`
- **Date:** `2026-10-26`
- **Status:** `active`
- **Owner / source:** the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md);
  the open question in `docs/tasks/XTASK.md` since `XTASK.3` (2026-10-23).
answers: Does `cargo xtask focused` run the rustdoc check before a gated commit?

## The fact / decision

Yes. `API-DOCS` joins the `FOCUSED` table of `xtask/src/main.rs` through its registered driver path
(`bash scripts/check_rustdoc.sh`, a shim of `cargo xtask check-rustdoc`), placed before `make book` so the
book's copy of the reference follows a green check. The set becomes 27 checks. Executed by `XTASK.7`.

## Why

- `XTASK.3`'s gate refused for a private intra-doc link the focused set would have caught; every refusal
  costs a gate run (about an hour) and leaves a red commit attempt in the evidence.
- Since `XTASK.6` slice `6d` the check is Rust and runs in about 3 s on a warm tree, with its self-test.
- The focused set is the pre-commit stage every unit runs; a doctrine that fails only in the gate is a
  doctrine the workflow discovers late.

## How to apply

- Documentation commits no longer need a separate `bash scripts/check_rustdoc.sh`; the focused run covers it.
- A new doctrine with a cheap check is added to `FOCUSED` in the unit that registers it, unless its cost is
  measured and recorded as the reason not to.
