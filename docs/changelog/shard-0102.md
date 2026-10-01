# CHANGELOG shard — SEMULITH-UT-0053 … SEMULITH-UT-0053

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-UT-0053 (leaf UPSTREAM-TRACK.3) — age and exposure, derived; the tree closes (4/4)

- `scripts/upstream_exposure.py`: from each issue record's dated history, DERIVES — at run
  time, never stored — every tracked issue's state, its age in days (earliest dated event
  → today), and its exposure (the record's `blocks` field). Today: `0 open / 3 resolved /
  3 tracked` (all three LS issues verified). Open = the unresolved half of the declared
  state vocabulary (draft/reported/acknowledged/disputed/fixed-upstream); `verified` is
  resolved because WE re-ran it (the `.2` discipline). `--open-count` feeds the gate.
- The `UPSTREAM-INDEX` gate learns the field: `blocks` is now REQUIRED on every record,
  and each entry must have the leaf-id shape (BAD BLOCKS) and name a leaf that EXISTS in
  `docs/tasks/` (DANGLING BLOCKS — an exposure naming nothing is a lie about what is
  blocked). Self-test 17 → 21 arms, all RED named.
- `DERIVED-COUNTS` owns the figure: a new claim (`open upstream issues`, enumerator
  `upstream_exposure.py --open-count`), carried by MEMORY.md's Blockers line and
  re-derived every commit.
- ⛔ Defect found in flight, owned: DERIVED-COUNTS' `self-test arms` claim matched NO live
  document (its pattern never matched LIVE_STATUS's "N arms" wording) — the arms figure
  had never been re-derived and was silently stale (280 carried vs 291 real). Fixed in the
  document, not the gate; the gate went from re-deriving 3 claims to 5.
- The tree closes (4/4): criteria 1–3 from `.1`, criterion 4 from `.2` (strengthened by
  `.4`), criterion 5 — dated history answerable — is this leaf's derived figure.
- `make gate` all green (27 doctrines / 291 self-test arms, now genuinely re-derived);
  `check_upstream_index.sh --self-test` 21/0.

