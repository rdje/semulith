# The evidence path, exercised — P3-BREADTH.3, slice 2 (2026-10-01)

The survey (slice 1) said DSP56300's path is complete on paper; this slice demonstrates it
HERE — pinned, on-volume, headless — without any Semulith DSP model existing. Every leg of
the differential workflow this project already uses for `rv64i-lab-v0` (assemble a guest →
execute on the reference → compare canonical architectural state) is run once, for real.

## The pin

- Reference: `mborgerson/dsp56300`, commit `c60aeedb6a6014850204c71e53bc0cf5b3104222`
  (main @ 2026-09-27), MIT license (re-fetched and read).
- Acquired: `https://github.com/mborgerson/dsp56300/archive/c60aeedb….tar.gz` →
  `target/refs/dsp56300-c60aeedb.tar.gz`, sha256
  `46b0e3e532e774859ee59b861901ac53b94a31ca5c924c61f8f32b26d6b308c9` — untracked, on-volume,
  exactly the `target/refs/` discipline the RISC-V references follow. The ledger integration
  (`profiles/<dsp>/references.sexp` driving `fetch_references.sh`) is `.4`'s, with the profile
  dossier it belongs to.
- Build: `cargo build --release --bin dsp56300-asm --bin difftest`, on-volume
  (`CARGO_HOME=.app-data/cargo-home`, `CARGO_TARGET_DIR=target/refs/dsp56300-build`), 31.7 s.
  ⚠️ Toolchain note: the upstream pins 1.98.1 in `rust-toolchain.toml`; this host carries
  1.98.0 (which satisfies the crate's `rust-version = "1.98"` floor), so the build ran under
  `RUSTUP_TOOLCHAIN=1.98.0-aarch64-apple-darwin` rather than installing 1.98.1 into the
  OFF-VOLUME rustup store (§13). The demonstration's claim is functional; the exact-toolchain
  policy is `.4`'s to set when the reference becomes a ledger entry.

## The guest and the run

The micro guest (tracked: `dsp56300-demo/micro.a56` + `micro.meta` beside this document)
exercises the shapes the findings need a target for: 24-bit immediates, a `mpy`+`mac` into
the 56-bit accumulator `A2:A1:A0`, stores into BOTH the X and Y data spaces, and a
zero-overhead `do` loop. It is a SYNTHETIC program: evidence about the path, never about any
real DSP software.

```
$ dsp56300-asm micro.a56 -o micro.lod -f lod -v
1 segment, 22 words total
  P:$000100  22 words                                   # rc=0; the LOD IS difftest's dialect

$ difftest corpus micro.lod micro.meta                  # case micro 000100 000115 100
case micro
steps 16
pc 000115
sr c00310
…
x0 123456
x1 050000
y0 0abcde
a0 515280
a1 1f253d
a2 000000
…
cyc 29
end                                                # rc=0 — canonical state, headless
```

## The verification (three independent legs)

1. **Arithmetic, by hand via Python** — with MPY/MAC's fractional ×2 and the four `asl`
   passes: `2 * (0x123456*0x0abcde + 0x050000*0x0abcde) << 4 = 0x001f253d515280` — and the
   dump's `a2:a1:a0 = 00:1f253d:515280` is exactly that. ✓
2. **The write path** — `difftest corpus … --dump-mem` shows `xm0200 01f253` (a1 pre-loop),
   `ym0300 01f253` (the Y-space copy), `xm0202 1f253d` (a1 post-loop), and no `xm0201`
   (a2 was 0 — deviation encoding omits it): the stores landed in the right SPACES at the
   right addresses with the right values. ✓
3. **The one surprising value traced to the manual** — `move #$5,x1` yielded `x1 050000`,
   not `000005`. Not a bug: DSP56300FM §3.4.1.3 — an 8-bit immediate short operand to
   X0/X1/Y0/Y1 is a signed FRACTION stored in bits 23–16 ("the eight MSBs of a 16-bit
   number"). Quoted from the extracted manual (`target/dsp-review/dsp56300.txt`, lines
   3241–3243). The toolchain's behaviour matches the family manual. ✓

## What this demonstrates — and what it does not

- **Demonstrated:** the full evidence path for the DSP56300 slice exists and runs here —
  pinnable MIT reference, MIT assembler, headless canonical-state dumps (registers + memory
  deviations + stack slots available), per-case step counts, a corpus/meta format a Semulith
  harness can drive exactly as it drives the RISC-V comparisons.
- **Not demonstrated / not claimed:** any DSP compatibility of any Semulith model (none
  exists); cycle/timing fidelity (the reference's `cyc` is informational — its LIMITATIONS.md
  lists pipeline interlocks as unmodelled); a second INDEPENDENT oracle for this family on
  this volume (the GPL-3.0 dsp56300-org core and the proprietary `sim56300` are the recorded
  candidates; `EVD-04` ancestry note: asm and emu here share one project — its authors'
  silicon-sealed corpus is the independent leg, and adopting any of its goldens would be a
  provenance-recorded proof artifact, not a re-derivation).
- `.4`'s bounded subset can now be chosen against a measured path; the reference's
  documented gaps bound which behaviours the slice may claim.
