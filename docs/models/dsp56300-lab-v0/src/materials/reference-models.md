<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/dsp56300-lab-v0/references.sexp`  `3f844efe5200c8456596e083fa568bdf00b044e60bf9c7a3072b3b7c6aede372`
     Generator: `scripts/gen_model_book.py` (sha256 `4a782e2fd828d743f1edf8e9ff7162f6228e4054a5717eb5e0a8b14ead8d21bb`) -->

| ID | Role | Status | Kind | Version | sha256 | Terms |
| --- | --- | --- | --- | --- | --- | --- |
| `dsp56300` | primary oracle — silicon-validated emulator + assembler, one MIT project | obtained | source tarball + on-volume cargo build | — | `728f3f7650b5599d881b6c7e31120bec566cc44e3ea40c70708b8da30702af03` | MIT (© 2026 Matt Borgerson) — the LICENSE was re-fetched and read 2026-10-01 (P3-BREADTH.3 slice 1). The tarball is fetched into the untracked target/refs/ working area; no copy is committed and nothing is redistributed. |
| `dsp56300-asm` | the assembler leg of the dsp56300 reference (the candidate above) — turns a guest's .a56 source into the .lod image | obtained | component binary of the dsp56300 source build | — | `180f91fbce614a15fbd3e5b0386d52d37124135e6e8c624eb9fb78d27248282f` | MIT |
| `dsp56300-emu` | the emulator leg of the dsp56300 reference — the difftest corpus runner that produces the canonical end-state dump | obtained | component binary of the dsp56300 source build | — | `728f3f7650b5599d881b6c7e31120bec566cc44e3ea40c70708b8da30702af03` | MIT |
| `gearmulator` | the family's second implementation (dsp56300/gearmulator, The Usual Suspects) — the potential second oracle | not obtained | — | — | — | — |

How each is invoked when exercised, as recorded:

- **`dsp56300`** — `dsp56300-asm <guest.a56> -o <guest.lod> -f lod — then — difftest corpus <guest.lod> <case.meta> [--dump-mem] [--dump-stack]; the meta names the case, the load base, the stop pc and the step budget (`case micro 000100 000115 100`).`
- **`dsp56300-asm`** — `dsp56300-asm <guest.a56> -o <guest.lod> -f lod`
- **`dsp56300-emu`** — `difftest corpus <guest.lod> <case.meta> [--dump-mem] [--dump-stack]`
- **`gearmulator`** — not exercised; no invocation exists (not obtained)
