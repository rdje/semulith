# LS-001 — how to reproduce and how to validate the fix

Everything needed is in this directory. Nothing here reads semulith code or semulith data.

## What is in this sub-tree

| Path | What it is |
| --- | --- |
| `REPORT.md` | the finding: symptom, root cause, severity, what we did and did not verify |
| `repro.sh` | runs every case against **your** binary and compares to `cases/EXPECTED.tsv` |
| `cases/*.sexp` | one file per case — four controls that pass, four that fail |
| `cases/EXPECTED.tsv` | the expected value per case, tab-separated |
| `evidence/shipped.txt` | our captured run at pin `ad290bdb4`: `4 matched / 4 differed` |
| `evidence/patched.txt` | our captured run with the candidate fix: `8 matched / 0 differed` |
| `fix/dotall.patch` | the candidate fix as a unified diff against `specs/Lispish.spec` |

## 1. Reproduce

Build the file consumer as your own guide prescribes
(`docs/linkedspec-book/src/public-api/integration-rust.md` — remember *Initial PGEN preparation*),
then:

```sh
bash repro.sh "$CARGO_TARGET_DIR/debug/lispish_file" specs/Lispish.spec
```

Expected at pin `ad290bdb4`: **`LS-001: 4 matched / 4 differed`**, matching `evidence/shipped.txt`.

If you get 8 matched, the defect does not reproduce on your build and we would like to know — the
difference would then be in the toolchain or in the PCRE2 pin, not in the grammar.

## 2. Validate the candidate fix

```sh
git apply --check docs/.../fix/dotall.patch   # or apply by hand: (?s) on lines 69 and 71
cp specs/Lispish.spec /tmp/Lispish-dotall.spec
#   dquotes: /(?s)"(.*?)(?<!\\)"/
#   squotes: /(?s)'(.*?)(?<!\\)'/
bash repro.sh "$CARGO_TARGET_DIR/debug/lispish_file" /tmp/Lispish-dotall.spec
```

Expected: **`LS-001: 8 matched / 0 differed`**, matching `evidence/patched.txt`.

⚠️ The grammar is data, so no rebuild is needed between the two runs — which is also why we could
validate the fix without touching the pinned submodule.

## 3. What we could not validate, and would want your regression suite to answer

- Does a lazy DOTALL match change behaviour on an **unterminated** quote? Your limits table says
  such a quote can be skipped today, and something may depend on that.
- Does any existing corpus rely on a quoted string *not* spanning lines?
- Any interaction with `sbrackets`, `curlyb`, or the adjacency-joining rule.

## 4. Closing the loop

When a fix ships, tell us the new pin. We re-run `repro.sh` against it and only then move this
issue from `fixed-upstream` to `verified` — a fix we have not re-run is a claim, and our tracker
keeps those two states apart on purpose (`docs/upstream/README.md`).
