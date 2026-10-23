# Rust-native tooling: rustdoc for the API reference, an incremental and extremely careful move to xtask

- **Type:** `decision`
- **Date:** `2026-10-23`
- **Status:** `active`
- **Owner / source:** the director, 2026-10-23, in session: "I would like SEMULITH to use rustdoc to create the
  API reference and cargo xtask"; "Migration to xtask shall be done with extrem care, and incrementally for not
  breaking anything. I talked about rustdoc and xtask because they are made for Rust project which SEMULITH is."
  The measured assessment that preceded it: target/rustdoc-xtask-assessment/ (rustdoc build log and coverage).
answers: How does SEMULITH adopt rustdoc and cargo xtask, and what may the xtask migration never do?

## The fact / decision

1. **Rustdoc is the API reference.** The workspace's public API is documented with rustdoc and the reference is
   built from it, not written by hand. Measured 2026-10-23: `cargo doc --workspace --no-deps --offline` builds
   with no error in about 4 s (20 MB of HTML); documented items semulith-core 553 (90.1%), semulith-verify 404
   (82.4%), semulith-dsp56300 66 (35.5%); 287 warnings, of which 19 are defects (9 unresolved links, 4 links to
   private items, 6 unclosed HTML tags) and the rest missing docs (179 struct fields, 53 variants); 0% doc examples.
   Tree: `RUSTDOC`.
2. **xtask becomes the developer front door, incrementally and with extreme care.** Tree: `XTASK`. Every step is
   behaviour-preserving and measured: the same exit codes and the same output lines the gate matches, before and
   after; the old path stays as a shim until every gate arm that names it has moved and been fired RED again; one
   leaf per commit; no gate is weakened, no arm deleted to make a port pass.
3. **What the migration never touches without a planned new capture:** the 35 scripts pinned by the retained M
   case (`evidence/rv64gc-m-forms-v3/dependencies.sexp`); their bytes are part of the evidence's identity.
4. **Constraints carried from the measurement:** no new crate dependency (the vendored Cargo.lock identity and
   the offline build stay as they are); the wasm check builds the whole workspace for wasm32, so xtask is excluded
   there or compiles for it; the git hooks stay bash and offline-safe until xtask has proved itself.

## Why

SEMULITH is a Rust project; rustdoc and cargo xtask are the ecosystem's own tools for an API reference and for
project automation. The repository carries about 94,000 lines of Python and shell tooling beside about 68,000
lines of Rust, much of it bound into a 1,655-arm self-tested gate and into retained evidence, so an abrupt
rewrite would break the very checks that keep the project honest. Incremental, shimmed, measured steps keep
every check green while the front door moves.

## How to apply

- Before any RUSTDOC or XTASK leaf lands, it states the behaviour it preserves and measures it before and after.
- New tooling should be born in Rust under xtask once XTASK.1 exists (confirmed as policy by the director, or
  revised, before it is enforced).
- The pinned evidence scripts and their probes stay Python unless a capture is planned anyway.
