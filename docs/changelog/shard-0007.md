# CHANGELOG shard — _(2026-09-04)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-04)_ — a template's trial must include the first commit

- Every gate was green on the generated project and the first commit still failed: the doctrines judge STAGED
  code, and nothing had been staged until the user tried. Trial the path a user walks, to its end.
- `grep -c` prints `0` and exits 1. `$(grep -c … || echo 0)` therefore yields `0⏎0` — a second line — which
  here started a flush-left line inside a checklist bullet and hid its evidence from the box-scoped extractor.
  Capture the count, then default the empty case; never append a fallback to grep's own output.

## _(2026-09-04)_ — a green gate that judges nothing is the class a template must not ship

- Two of the four doctrine ports in `.2.6` were wrong on first run and their own RED self-test arms said so:
  a `python3 - <<'PY'` detector whose stdin was the heredoc (every arm read 0 rows), and a `grep -c … | grep -qx 0`
  control under `pipefail` (`grep -c` prints 0 and exits 1). A self-test with only GREEN arms would have passed both.
- The neutrality bar is measured, not felt: `grep -ciE 'grammar|parser|…'` over each ported script → 0, after the
  generic uses of "corpus" and "grammar" were re-worded ("tree", "syntax") so the count means what it says.

## _(2026-09-14)_ — a parser's error paths say nothing about the content it returns

- `"".join(buf).encode().decode("unicode_escape")` is a **Latin-1** decoder. Every `§` in this
  project's semantics fragment came back as `Â§`, every `—` as three characters of noise — all 52
  specification citations, corrupted on read, by a reader that raised no error and by a suite in
  which no instrument was pointed at fidelity. Promoted to
  [`a-parse-without-error-is-not-a-faithful-read`](docs/knowledge/a-parse-without-error-is-not-a-faithful-read.md).
- The reader every source of truth in the repository depends on had **no self-test at all**, and
  I was one leaf away from building a schema layer on top of it. Read the foundation before you
  stand on it; 18 arms cost twenty minutes and the first three were RED.

