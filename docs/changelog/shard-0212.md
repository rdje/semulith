# DEV_NOTES shard — _(2026-10-06)_ … _(2026-10-06)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-06)_ — the identity proof's RED control is what makes it a proof (P4-SYSTEM.7 slice b)

Slice (b)'s byte-level identity proof (101 pre-slice guests, both CLIs — the
parent worktree's build vs the post-slice build) came back "101 byte-identical,
0 diverge" on its first run. It was also worthless: the harness had passed
`--profile NAME` where the CLI wants `--profile=NAME`, so every one of the 202
runs had failed with the SAME usage-error text — and identical failure output
compares byte-identical. What caught it was the control the proof carried by
design: the two NEW guests (fp-fs-off, fp-fcsr-view) MUST diverge on the parent
engine — the FS gate and the fcsr composition did not exist there — and they
"didn't". A comparison harness whose failure mode is identical on both sides
reports identity on garbage; the must-diverge control is the only arm that can
see it (the a-shorter-trace lesson's sibling: prefix agreement was the green
there, identical errors here). After the fix: 101 byte-identical for real
(5,491 trace lines), both new guests diverging on the parent as required.

Also measured this slice, for the record: Sail puts the FS gate on the DECODE
clause (`encdec … when currentlyEnabled(Ext_F)` — a dynamic state gate at
legality, never a static encoding property), which settled where ours lives
(the permission model for the FP CSRs now; `fp_enabled()` for the binds' arms);
and Sail's `write_fcsr` marks the context Dirty on every FP-CSR write
(fdext_regs.sail:455), the discipline our csr_write now follows.

- **Validation:** the fixed harness re-ran green with the control RED where it
  must be; `cargo test -p semulith-verify run_rv64gc` 4/4 (103/103); STATE-GEN
  29/29 with the new RED arm; `make check` rc=0, `make gate` green
  (DERIVED-COUNTS 430→431 re-derived).
- Promotion: PROMOTED — the must-diverge-control lesson is retrievable
  (docs/knowledge/an-identity-proof-needs-a-must-diverge-control.md + INDEX;
  the map regenerated). The Sail placements are recorded in the leaf's own
  checklist and need no card.

