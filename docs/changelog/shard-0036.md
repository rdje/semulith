# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-27)_ — the dossier moves behind the schema layer (SOT-FORMAT.4)

- All nine dossier documents converted — `profile.sexp` (26 decisions), `state.sexp`,
  `sources.sexp`, `references.sexp`, the matched override and the four guest expectations —
  each verified field-for-field against its retired TOML/JSON with the comment census exact
  (158 comment lines survive as first-class `(comment …)` forms). Kernel: one reserved comment
  head, 7 new arms (50/0). `PROFILE-CONSISTENCY`: 39 arms re-fired on the converted form.
  Consumers changed at the seam via the new mapping owner `scripts/dossier_sexp.py`; the Sail
  JSON derives from the tracked `.sexp` byte-identically; `run_smoke`/`compare_platforms`
  unmoved.
- ⭐ **A mutation arm and the defect it simulates must fail for the same reason.** Three
  fixture-shape failures while re-firing the 39 arms — a field line carrying its form's close
  paren (a `grep -v` arm unbalanced the fixture), BSD sed refusing multiline replacements
  (CI runs GNU sed; `gsed` on the author's machine is not a dependency the gate may take), and
  `${var/pat/repl}` terminating at an inner quote (the replacement silently never happened).
  Every fix was the same shape: one field per line, closes on their own lines, whole-line
  mutations only. Promoted to
  [`docs/knowledge/portable-shell-fixtures-keep-mutations-whole-line.md`](docs/knowledge/portable-shell-fixtures-keep-mutations-whole-line.md).

## _(2026-09-27)_ — the fired ceiling gets its sharder, and the freeze gets its proof (DOC-SHARDING.1)

- `CHANGELOG.md` crossed its 64 KiB ceiling with 9 bytes of headroom; this slice built the
  remedy the registry's owner column had always named: `scripts/shard_history.py` (moves the
  oldest whole `## ` entries byte-verbatim into `docs/changelog/shard-NNNN.md`, rewrites the
  head under target, regenerates `SHARDS.sha256`), the adoption manifest covering the two
  existing date-named shards, and the `SHARD-FREEZE` doctrine check. One entry (`P0-0031`,
  3.4 KiB) moved; the head went 65,527 → 62,086 bytes — leaving room for this entry itself.
- ⭐ **The completeness proof belongs to the shard event; the freeze proof belongs to the
  manifest.** The tool can assert "head-before == head-after + shard, order and bytes exact"
  because it holds both sides at the event; no later check can, the past head is gone. What the
  durable check can prove is everything after: every shard hashes to its row (an edit fails with
  both digests named), the manifest only grows against `git show HEAD:…`, and no `## ` heading
  appears twice across head and shards. Splitting the two halves is what makes each half
  checkable.
- Fired RED on the real tree before registration — the manifest did not exist yet, so the check
  reported both existing shards `UNMANIFESTED` (rc 1), the exact adoption gap. 12 self-test
  arms; the full gate re-run after registration moved `LIVE_STATUS.md`'s derived counts
  (12 → 13 doctrines, 157 → 169 arms) — re-derived by `check_derived_counts.sh --list`, never
  incremented by hand.

