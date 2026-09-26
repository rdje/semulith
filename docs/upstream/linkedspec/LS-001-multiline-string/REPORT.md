# LS-001 — a double-quoted string containing LF is not read as one string

| | |
| --- | --- |
| **ID** | `LS-001` |
| **Project** | LinkedSpec (`rdje/linkedspec`) |
| **Component** | `specs/Lispish.spec`, lines 69 and 71 |
| **Severity** | `high` — wrong results with **no error**; the consumer cannot detect it |
| **State** | `verified` `2026-09-26` — re-run against the adopted pin, see *Resolution* below |
| **Raised** | `2026-09-20` by semulith, first consumer of the Rust backend |
| **Affects** | `ad290bdb4` (rgx `8763a0e6bea9`, pgen `db6f8c6836fe`); see `../README.md` |
| **Blocks** | semulith leaf `SOT-FORMAT.9` — two readers of one format must agree |
| **Fix** | upstream `8259719f8`, shipped at `a8d34c845` — the reported `(?s)` DOTALL form, verbatim; candidate at [`fix/dotall.patch`](fix/dotall.patch) |
| **Reproduce** | `bash repro.sh <lispish_file> [Lispish.spec]` |
| **Validate** | [`VALIDATE.md`](VALIDATE.md) — what is in this sub-tree, how to reproduce, how to check the fix |

## Resolution

`2026-09-26`, on the director's instruction after upstream shipped the fix: semulith advanced its
pin to `a8d34c84595d46c24cd1820d5fc0414261706412`, rebuilt the consumer per the guide, and re-ran
this sub-tree's own reproduction against the new binary and grammar:

```
$ bash repro.sh <new lispish_file> <new Lispish.spec>
  LS-001: 8 matched / 0 differed
```

The readers then agreed on **all five** of semulith's tracked `.sexp` files (5 of 5 under the
consumer's two-reader comparison), which is what discharged `SOT-FORMAT.9`. The only residue is
two documented CLASS families (quoted-numeric typing, escape retention) that follow from
Lispish's published extraction contract — enumerated by that comparison, tracked upstream as
LS-002, not this defect.

## Summary

A double-quoted string that contains a line feed is not lexed as a string. It does not merely lose
its newline — it **stops being a string**, and its remaining text is re-lexed as syntax. A `)` in
the continuation then closes a form that was never open, so following siblings are absorbed into
the wrong parent.

The reader exits **0** and prints a plausible value. That is what makes this `high`: a consumer has
nothing to test for.

## Evidence

Captured runs are in [`evidence/`](evidence/). With the shipped grammar, `4 matched / 4 differed`:

```
  MATCH     01-control-one-line.sexp     ["r",["a","x y"]]
  MATCH     02-control-parens.sexp       ["r",["a","see (2) ok"]]
  MATCH     03-control-tab.sexp          ["r",["a","x\ty"]]
  MATCH     04-control-cr.sexp           ["r",["a","x\ry"]]
  DIFFERS   05-lf-data-only.sexp
              want: ["r",["a","x\ny"]]
              got : ["r",["a","x","y"]]                  (exit 0)
  DIFFERS   07-lf-sibling-follows.sexp
              want: ["r",["a","x\n   y"],["b","z"]]
              got : ["r",["a","x","y) (b z"]]            (exit 0)
  DIFFERS   08-lf-close-paren.sexp
              want: ["r",["a","p\n   q) r"],["b","z"]]
              got : ["r",["a","p","q"],"r) (b z"]        (exit 0)
```

⭐ The four controls are the point of the case set: spaces, parentheses, **TAB and CR** inside a
one-line string all round-trip correctly. Only LF fails, which is what localises the cause.

## Effect on a real file

semulith's 43-form catalogue (`materials/catalog.sexp`, 43 KB, prose fields wrapped across lines)
read as **6 top-level forms**, with 37 of them silently nested inside the fifth. Exit 0. Our own
reader returns 43. That file is not in this directory because the reproduction does not need it —
`07` and `08` are the same defect in nine bytes.

## Root cause

```
specs/Lispish.spec:69   dquotes: /"(.*?)(?<!\\)"/
specs/Lispish.spec:71   squotes: /'(.*?)(?<!\\)'/
specs/Lispish.spec:84   others:  /[^\s"{}()\[\];]+/
```

`.` does not match LF without DOTALL, so the `dquotes` token cannot match a multi-line string. The
text then falls through to `others`, which splits on whitespace — exactly the observed behaviour,
and the reason `(` and `)` in the continuation become structural.

⛔ **Located by refutation, not by inspection.** Two hypotheses were tested first and both were
wrong: that `;` inside a string was starting a comment, and that parentheses inside a string were
affecting structure. Both are handled correctly. They are listed under *what we did not find* in
`../README.md` so nobody re-chases them.

## Candidate fix, and what we did and did not verify

```diff
-dquotes: /"(.*?)(?<!\\)"/
+dquotes: /(?s)"(.*?)(?<!\\)"/
-squotes: /'(.*?)(?<!\\)'/
+squotes: /(?s)'(.*?)(?<!\\)'/
```

Verified: `8 matched / 0 differed` on the cases here ([`evidence/patched.txt`](evidence/patched.txt)),
and all five of semulith's tracked `.sexp` files then agree with our own reader node-for-node,
including the catalogue that had failed.

⚠️ **Not** verified, and outside what we can judge from here:

- whether a lazy DOTALL match changes the failure mode on an **unterminated** quote — today the
  limits table says such a quote can be skipped, and that behaviour may be relied on;
- whether any existing corpus depends on a quoted string *not* spanning lines;
- any effect on `sbrackets`, `curlyb` or the adjacency-joining rule.

We tested the patch on a **copy** of the spec. The pinned submodule in semulith is untouched:
patching a pin is how a consumer's pin becomes a fork.

## Suggested state transitions

`draft` → `reported` when sent. If it reproduces on your side, `acknowledged`. We move it to
`verified` only after re-running `repro.sh` against a new pin ourselves.
