# DEV_NOTES shard — _(2026-10-05)_ … _(2026-10-05)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-05)_ — the mirror's byte-identity is the point, and a bind can be invisible in its own trace (P4-SYSTEM.6 slice b)

Execution of the `.6` brief's checkpoint (b) measured:

- **The mirror holds .s byte-identical ALWAYS — and that is the discipline, not
  an obstacle.** My first draft restated four .s headers to the bound state, and
  the governor measured every one as MIRROR DRIFT: the base mirror's rule is
  that rv64gc's .s files are byte-identical to rv64i's owners with NO exception
  list, while an .expected.sexp may differ only for a RECORDED re-derivation.
  The `.2` slice-(g) shape was already the answer: the rv64gc-specific reading
  lives in the expectation comment block, never in the mirrored source. The
  decision-3 corrections (dir-selfmod-fence's data fence is not the fetch
  synchronization; fault-selfmod's stale "without Zifencei") landed exactly
  there, with both names joining MIRROR_REDERIVED and the reason recorded
  beside the slice-(f)/(g) reasons (promotion: declined — the durability is the
  machinery: the governor names drift on every gate run).
- **A bind can be invisible in its own trace.** min-fencei's demo trace is
  byte-identical pre- and post-bind: the pre-bind ReservedDecode delivery wrote
  no register and vectored to mtvec=0, so the recorded step (pc, mode, writes)
  is the same tuple as the post-bind retiring nop. The semantic change (a
  trap-conversion vs a retirement) is real and shows in the expectations; the
  trace just has no slot for it. it-fencei carries the visible half: the
  continuation marker commits now (x2 ← 7), exactly as on both references.
- **Memory-backed fetch is a derivation-level discipline too.** The new
  fencei-selfmod guest needs the spec-side model to re-read the patched word —
  the store's effect lands in the program map with the patch named in the insn
  text (the `.2` comment convention, tooled at last). The engine always re-read
  (D-CODE-VISIBILITY); the derivation tool simply had to catch up — a guest
  whose patch the model ignores would derive the WRONG patched step silently.

promotion: declined (the durability is the machinery — the mirror governor and
the 101-guest corpus re-run every one of these).
