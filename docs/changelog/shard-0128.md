# CHANGELOG shard — SEMULITH-PS-0084 … SEMULITH-PS-0082

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PS-0084 (leaf P2-SCALAR.9, slice c) — the CPU-LAB report stands; the tree CLOSES 9/9

- `gate_report.py` gained `build_cpulab`: the full processor-gate series per axis
  (SCP-05 — never rolled up; "supports RV64I" appears nowhere), every probe static over
  tracked artifacts (byte-stable in a fresh clone), the dossier content digest as the
  versioned artifact's identity. The generated `GC-REPORT.md` reads **`incomplete`**,
  naming the measured open axes: G-CONTRACT (0/72 obligation checks implemented) and
  G-OBLIGATIONS (28 requirements `planned`, 1 `partial`). Green with their measurements:
  G-TRACE, G-INTERACTIONS (21/21), G-REGRESSION (ACT4 51/51 + the corpus + the mutation
  suite), G-PORTABILITY (`passed` under the bridge), G-REPLAY (bundles + snapshots).
- The named release decision (`decision_release-rv64i-lab-v0`): **rv64i-lab-v0 v0 is an
  EXPERIMENTAL release of the versioned evidence artifact — NOT an accepted profile**;
  the closing conditions are named (the 72 fixtures, the status re-derivation, the
  bare-metal CI leg).
- One defect fixed in flight: the G0 generator's hardcoded "No CPU model exists" — prose
  written at P0, stale since the interpreter landed; the limitation now reads true, and
  GATE-REPORT holds all three generated reports in sync. MEMORY.md's active-trees count
  had drifted at 6/9 across two commits — corrected at closure.

## SEMULITH-PS-0082 (leaf P2-SCALAR.9, slice b) — the Rosetta proof: the x86-64 leg green, `portability: passed`

- The director's Rosetta install landed (VLC's Intel build triggered it); re-measured
  live: `arch -x86_64` prints `x86_64`. The instrument's x86-64 leg learned the bridge
  path: cross-compile `x86_64-apple-darwin`, run under translation, and compare the
  digest manifest against the aarch64 recording — **byte-identical** (`0670a01b…`).
- The full four-leg run reads **passed** (native green, x86-64 green under translation,
  Miri green, cross-endian green); `portability.sexp` re-measured to `passed`, with the
  translation-vs-bare-metal nuance and the fall-2027 horizon on the record.
- Slice (a)'s checklist claimed a `plan/p2.md` line that commit did not carry — the
  drift is recorded and the `.9` book section lands with this commit instead.

