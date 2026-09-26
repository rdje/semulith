# LinkedSpec — issues raised by semulith

semulith is LinkedSpec's **first consumer of the Rust backend**, integrating `specs/Lispish.spec`
as the reader for its own source-of-truth format. Everything below was found by doing that
integration, following the published guide.

## A word on the guide, before the defects

`docs/linkedspec-book/src/public-api/integration-rust.md` is unusually good: it states its limits
before its features, it says plainly that *"a successful value does not establish that the complete
file is valid"*, and it names unimplemented work rather than leaving a consumer to discover it.
Two of the three issues below are findable **only because** the guide is that explicit, and
`LS-003` is a set of papercuts, not errors. `LS-001` is a real defect and is not the guide's fault.

## Issues

| ID | Title | Severity | State | Fix validated by us? |
| --- | --- | --- | --- | --- |
| [`LS-001`](LS-001-multiline-string/REPORT.md) | a double-quoted string containing LF is not one string | `high` | `verified` | **yes** — upstream shipped the reported patch (`8259719f8` @ `a8d34c845`); our repro re-ran 8/0 and all 5 tracked files agree |
| [`LS-002`](LS-002-atom-typing/REPORT.md) | quoted and bare atoms are indistinguishable | `medium` | `acknowledged` | no — design question; upstream owns it (`.83.1 owned`) |
| [`LS-003`](LS-003-guide-papercuts/REPORT.md) | three first-consumer papercuts in the integration guide | `low` | `verified` | n/a — documentation; all three remedies exercised at the new pin, evidence captured |

## The environment every issue here was found in

```
linkedspec      ad290bdb427bc19a5af81de0f0b07e119c8999ff
  rgx           8763a0e6bea97879f027237439d57725f83ead23
    subs/pgen   db6f8c6836fefa5a57b1337d3ffbf6f15774089f
    subs/pcre2  f454e231fe5006dd7ff8f4693fd2b8eb94333429
specs/Lispish.spec   sha256 36eec88385994e3d80148c621008a36b661f1eec67ae6603c0ebb7f06aacfa9d
rustc 1.95.0 (59807616e 2026-04-14)        Darwin arm64
consumer: examples/integration/rust/src/bin/lispish_file.rs, built via tools/run_cargo_local.sh
          after the documented PGEN bootstrap; 32.15s
```

## Every issue is a self-contained sub-tree

An issue directory carries everything needed to reproduce **and** validate it, so it can be copied
out of this repository and used on its own:

```
LS-001-multiline-string/
  REPORT.md           the finding: symptom, root cause, severity, what we did and did not verify
  VALIDATE.md         what is in the sub-tree, how to reproduce, how to check the candidate fix
  repro.sh            runs every case against YOUR binary, compares to cases/EXPECTED.tsv
  cases/              one file per case — four controls that pass, four that fail
  cases/EXPECTED.tsv  the expected value per case
  evidence/           our captured runs: shipped.txt (4/4 differ), patched.txt (8/0)
  fix/dotall.patch    the candidate fix as a unified diff against specs/Lispish.spec
```

```sh
bash <issue-dir>/repro.sh <path to your lispish_file> [path to your Lispish.spec]
```

⛔ Verified self-contained: each sub-tree was copied to a scratch directory outside this
repository and its reproduction re-run there, producing identical output. No semulith code, no
semulith data, no relative escape.

## What we looked for and did NOT find

Recorded so these can be discounted rather than chased. All behaved correctly at the pin above:

- `;` inside a double-quoted string is **not** treated as a comment.
- `(` and `)` inside a **one-line** double-quoted string do not affect structure.
- Non-ASCII content (`§`, `—`, `⛔`, `⭐`) round-trips exactly.
- The four documented `generated/` products appeared exactly as the bootstrap section promises.
- RGX and PGEN pinned at the revisions the guide's evidence section names.
- On our four files with no multi-line strings, LinkedSpec's reader and ours agree **node for
  node** — 438, 1550, 1716 and 18 nodes, zero differences.
