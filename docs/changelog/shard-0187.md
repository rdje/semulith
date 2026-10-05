# CHANGELOG shard — SEMULITH-P4-0009 … SEMULITH-P4-0009

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0009 (leaf P4-SYSTEM.2, slice e) — the 65-form census (dual edit), the base-corpus mirror + authored records, the flip's staged encoding

- The scope census grows 52→65 by the mandated dual edit (`schema/profile.sexp` +
  `dossier_sexp._SCOPE_LISTS`: +zicsr_csrs, +system_privileged, +zicntr_counters). The
  pseudo-census decision, recorded in the profile's scope comment: the Zicntr counter
  reads ARE census forms (the spec's Zicntr listings name them), the encoding realizes
  them as csrrs specializations (the fragment's pseudos), and EXERCISE-COVERAGE observes
  the spelling in the expectations' insn text — measured. EXTRACTION's integrative claim
  now counts the composition's pseudo names (+2 self-test arms, 11 total).
- The requirements growth: the base-corpus mirror is derived by closure, not typed — the
  9 instruction family records + fence/ecall-ebreak + the XLEN/ENDIAN dependencies (13)
  and their 13 obligations, byte-verbatim but for the profile-scoped fields, with
  `mirrored_from` provenance, plus 3 authored requirement records (Zicsr access model +
  permission refusals; the privileged four's per-mode legality; the Zicntr reads + gating)
  and their obligations with POS+NEG check pairs — 34/34 in rv64gc's catalogues. The
  governor: RECORD-SCHEMA rule 14 (MIRROR-DERIVE), registry-driven by two new
  FACT-OWNERSHIP rows (63 kinds), its four RED arms fired (drift, missing,
  ungoverned-authored, owner's-contract-kept).
- The flip's encoding.sexp is staged at `target/p4-system-2/profiles/rv64gc-lab-v0/` with
  the flip's own bytes (relative fragment-root, the definitions symlink, `(status
  partial)` + six slots for m/a/f/d/c/zifencei), validated: schema conform, the union
  collision-free (62 instructions + 3 pseudos), the holes honestly declared; the slice-(d)
  execution proof regenerated from the staged bytes and re-run (26/26). The staged
  payload's README records the flip mapping.
- Measured in execution, fixed at root: the dropped-`(extensions …)`-form bug's census
  found two MORE readers (check_exercise_coverage.sh, gen_model_book.py — six sites, the
  pattern now extinct, `git grep` clean); PROFILE-CONSISTENCY's PARTS DRIFT learned the
  extension families (it fired honestly on 40+12≠65 mid-edit); fetch_references' scope leg
  covers the pinned tables, pseudo-aware (rv64gc 65==65, rv64i 52==52 unchanged). The
  docs/tasks/ aggregate ceiling fired (63 files / 1,575,182 B > 1.5 MiB — the slice
  checklists are the designed growth) and was re-derived to 3 MiB by decision record.
  `make gate` green (DERIVED-COUNTS 404→408 arms). Next: slice (f) — the guests corpus.

