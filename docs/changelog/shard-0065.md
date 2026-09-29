# CHANGELOG shard — SEMILITH-PL-0002 … SEMILITH-PL-0002

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PL-0002 (leaf P1-LAB.2) — target arithmetic primitives, verified exhaustively at reduced width

- `semulith-core::arith`: 18 SEM-03 primitives — ALU register/immediate ops, shifts with the REQ-D-SHAMT masks as named functions, the `*W` word ops (REQ-D-WSUFFIX), `sext`/`bits` extraction and extension, LUI/AUIPC offset formation. Each contract states width, signedness, intermediate precision, truncation, exceptional behavior; each doc comment source-links the requirement record and pinned locator (REQ-D-ALU-REG/IMM, REQ-D-SHAMT, REQ-D-WSUFFIX, REQ-D-LUI-AUIPC, REQ-D-LOAD-EXT, REQ-D-XLEN). Unmasked shift amounts panic in debug instead of silently wrapping.
- Verification, the acceptance's shape: boundary suites at full XLEN; an **8-bit exhaustive layer** (every `(x, y)` for the binary ops, every `(x, shamt)`, every `(x, from_bits)`, every `(lo, hi)` window) against references formulated on a different host width; a 100k-draw boundary-heavy sweep of the word ops against a u64-width reference. 12 suites green; clippy `-D warnings` clean.
- The exhaustive layer failed on its first run for exactly the reason the acceptance exists: `slt`/`sar` are width-sensitive, and the naive low-byte comparison of signed ops is wrong — fixed by embedding the narrow signed view at XLEN. The lesson is promoted to `docs/knowledge/reduced-width-verification-of-signed-ops.md` (LESSON-PROMOTION satisfied in-commit).
- Scope, stated: the requirements' `implementation_status` stays `planned` — these are the executable halves; instruction-level obligation checks need the interpreter slice (`.8`). The frontier moves to `.3` (architectural state).

Validation: `cargo test -p semulith-core` 12/0; `cargo clippy --all-targets --all-features -- -D warnings` clean; `make gate` → `=== all doctrines green ===`.

