# LS-003 — three first-consumer papercuts in the integration guide

| | |
| --- | --- |
| **ID** | `LS-003` |
| **Project** | LinkedSpec (`rdje/linkedspec`) |
| **Component** | `docs/linkedspec-book/src/public-api/integration-rust.md` |
| **Severity** | `low` — nothing here is wrong; each cost us one failed attempt |
| **State** | `verified` `2026-09-26` — guide remedies re-read and exercised, see `evidence/verified-a8d34c845.txt` |
| **Raised** | `2026-09-20` |
| **Affects** | `ad290bdb4` |
| **Reproduce** | not scripted — documentation observations. Verbatim errors and measurements in [`evidence.txt`](evidence.txt) |

⚠️ **Two of these three are our fault, not the document's**, and are reported only because we are
the first consumer and the next one will arrive the same way.

## 1. A Cargo workspace absorbs the submodule

Adding `vendor/linkedspec` inside a host project that already has a `[workspace]` makes **every**
build fail — LinkedSpec's own example included:

```
error: current package believes it's in a workspace when it's not:
current:   .../vendor/linkedspec/examples/integration/rust/Cargo.toml
workspace: .../Cargo.toml
```

One line in the host's root manifest fixes it, and the guide's *"For an existing Rust application,
merge these entries into its dependency table"* is where a reader expects to meet it:

```toml
[workspace]
exclude = ["vendor"]
```

## 2. The file-parsing section is reachable without its prerequisites

*"Parse Lispish files in your application"* (line 198) opens with "Add the following direct
dependencies…", a `cp`, and a build command. A reader sent straight to that section gets:

```
error: couldn't read `.../generated/return_annotation_parser.rs`: No such file or directory
```

because *Initial PGEN preparation* is ~100 lines earlier. The guide **does** say *"Checkout does
not generate PGEN's parser inputs"* — we simply had not read that far. One back-reference at the
top of the section would close it for the next reader who is pointed at a line number.

## 3. `--recursive` is costlier than the note suggests

The guide says `git submodule update --init --recursive` "also works, but retrieves additional
optional dependency/test repositories which this native Rust example does not need." Measured:

```
--recursive            1.7 GB, 30 nested submodules
                       (riscv-arch-test, neorv32, VeeR-EL2, cocotb, picolibc, pcre2, sljit, …)
documented two-step    the dependency closure the build actually uses
```

Naming the size at the point of decision would make the choice obvious.

## One thing that worked exactly as written

The PGEN bootstrap produced `ebnf.rs`, `regex_parser.rs`, `return_annotation_parser.rs` and
`semantic_annotation_parser.rs` — precisely the four products the section promises — and the
subsequent build took 32.15s, within the range the evidence section describes. The deliberate
`CARGO_TARGET_DIR` override is explained in the guide, and the explanation is why we did not
"fix" it.
