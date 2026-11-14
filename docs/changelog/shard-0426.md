# CHANGELOG shard — SEMULITH-P4-0343 … SEMULITH-P4-0328

> Sharded from `CHANGELOG.md` under its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0343 (leaf P4-SYSTEM.14 a43c-3) — the ZICNTR case's three declarations, and the director's ruling on the dossier copies

a43c-3: planned experiment, dependency manifest (67 children, two of them the case's own) and authority record, from `capture_div.py --declare`; this commit is the declaration commit. **The director ruled (a43b-c3):** no dossier copy for a new case until the next pinned window, which retires them all (`decision_dossier-copies-retire-at-the-next-window.md`). Measured while recording it: `experiment_verification.py:39` is the one import that makes `gate_report.py` a pinned input of every experiment, so the window moves that function out too, and editing a report never lapses evidence again. Next: a43c-4, the capture.

## SEMULITH-P4-0342 (leaf P4-SYSTEM.14 a43c-2) — the ZICNTR program and its case: 292 steps, 44 predeclared witnesses, in M, S and U

a43c-2: `zicntr.s` enters the corpus, all three producers agreeing (the author, the lab engine, the reference under the case's overlay, whose configuration is byte-identical to CSR-SET's). `rv64gc-zicntr-v1`: 44 witnesses, 26 boundary rows, control `refused-read-committed` (x21 at boundary 109, 21 against the wrong 102). The family's seventh re-derivation: 177 files, 112 MiB, 160 present. No retained case moved. Next: a43c-3, the declarations.

## SEMULITH-P4-0341 (leaf P4-SYSTEM.14 a43c-1) — the ZICNTR case designed, and its normative statements retained

a43c-1: CSR-SET's route for `REQ-D-ZICNTR`, in five units. A draft program, 163 instructions and 292 steps, agrees with the reference under the overlay and first differs at `rdcycle x5` under the profile override. Retained: `RVI-ZICNTR-STATEMENTS` (§6.1, §6.1.1), the normative input, and `RVP-COUNTEREN-STATEMENTS` (§2.1.1.11), what the refused reads rest on; `scounteren`'s statement has no anchor to select, so it is cited. Out of scope, named for the limitations: a write through `mcycle` or `minstret` (the pinned deriver refuses it) and Zihpm's absence. Next: a43c-2.

## SEMULITH-XTASK-0077 (leaf XTASK.13 slice b4) — GUEST-GEN's author probes judge a frozen owned corpus, and its real check re-derives the live one

`scripts/fixtures/guest-gen/owned/` holds the 42 owned guests, laid out as the repository is; `scripts/frozen_owned.py` points the pinned deriver's `REPO` and `ENCODING` at them for the one call, so the deriver does not move. Eight author probes and `probe_gc_owned_extent` take them. `--check-owned` is now a real-run step, measured RED: a mirrored record's value edit goes from a refusal (`391 pass / 9 fail`) to `MIRROR DRIFT — inj-walk-l0.s` at 400 of 400, and one line of silent prose, which only this step can read, goes from a silent `rc=0` to `DRIFT — inj-walk-l0`. The probes' other corpus reads are still live: slice b5. Next: features, ZICNTR (a43c).

## SEMULITH-P4-0340 (leaf P4-SYSTEM.14 a43b-3h) — `REQ-D-CSR-SET` credited `implemented`: the first `implementation-defined` requirement, G-STATE 2 of 4

a43b-3h: `CR-D-CSR-SET-1`, `authority review`, on one finite case of 53 witnesses: 45 planned, 3 implemented, 3 of 3 records current, 0 drift. Its limitations name what it does not claim: `mip`'s value directly, a CLINT or any device, a non-member address trapping, field semantics, counter rates, timer delivery, numerics. **Raised to the director (a43b-c3):** the dossier copy and its `G-TRACE` row are left out, a departure from the capture plan's step (iii): `references.sexp` would reach 77,669 B against the per-part 65,536 B, and moving the copies edits a tool all three manifests pin. Next: XTASK.13 b4, then ZICNTR.

## SEMULITH-P4-0339 (leaf P4-SYSTEM.14 a43b-3g) — the reviews read the CSR-SET case, and the comparison leg reads the requirement's category: 10 of 10

a43b-3g: `review_div_policy.py`'s comparison leg measured `defined`'s row for every category, so a configuration alone would have satisfied it, against the policy's words. It now reads the category: `defined` is unchanged to the byte; `implementation-defined` needs the recorded selection and a retained effect, seven pins read against the case's own bytes and the first difference re-derived offline at a declared property's step; any other category stays pending and is named. `RETAINED_CAPTURES` names the case: method `satisfied` over 88 files; policy `satisfied`, 10 of 10 legs, no credit yet. `FEATURE_DISPOSITIONS["OB-CSR-SET"]` is the first that says a rule applies. `DIV-POLICY-PROBE`: 48 tests, 27 seams. Next: a43b-3h, the credit.

## SEMULITH-P4-0338 (leaf P4-SYSTEM.14 a43b-3f) — the CSR-SET case captured exactly once, and its configuration's effect retained

a43b-3f: `rv64gc-csr-set-v1` ran once on a quiet host behind its guards: 157 steps, baseline and repeat AGREE, the control DIVERGE at its declared step 130 (x28 5 against the wrong 9), complete, qualification false, three traces byte-identical, 14 files retained; the family holds all 155; the case `pending`, both credits current. `scripts/measure_config_effect.py` (new; `schema/config-effect.sexp`; `scripts/probe_config_effect.py`, 10 tests and nine omissions) ran the same guest under the profile override, once, and retained the raw trace and what ran by digest, no verdict: `step 34 (csrrs x20, mcycle, x0): Sail {}, expectations {'x20': 34}`, the observed effect the policy's `implementation-defined` row asks for. Next: a43b-3g, the reviews.

## SEMULITH-P4-0337 (leaf P4-SYSTEM.14 a43b-3e) — the CSR-SET case's three declarations, committed before its capture

a43b-3e: planned experiment, dependency manifest (67 children, two of them the case's own) and authority record, from `capture_div.py --declare`; preflight `ready`; 7 cases, 1 declared, crediting nothing. The 67 children and 13 authority views are frozen until the capture.

## SEMULITH-P4-0336 (leaf P4-SYSTEM.14 a43b-3d) — the CSR-SET program and its case: all 33 CSRs, 53 predeclared witnesses, in M, S and U

a43b-3d: `csr-set.s` rewritten before any capture (136 instructions, 157 steps), judged three ways: the spec-side author, the lab fixture, the pinned Sail under the overlay. `evidence/rv64gc-csr-set-v1/`: the case (second method and adversarial case declared, the first to do so), its prepared inputs. The evidence family re-derived for seven cases (155 files, 96 MiB). Uncaptured; status unchanged.

## SEMULITH-XTASK-0076 (leaf XTASK.13 slice b3) — GUEST-GEN's parcel author probe judges frozen copies

`scripts/fixtures/guest-gen/parcel-legacy/` holds the five legacy guests and the probe composes over DEF-GEN's frozen encoding, state and definitions; `--cold` copies what it reads. A deleted live guest now reaches the generator's refusal naming the file, the self-test at 400 of 400. A real-run `--check-owned` step was drafted and taken back: six author probes still read the live owned corpus, so it could not fire. That is slice b4.

## SEMULITH-P4-0335 (leaf P4-SYSTEM.14 a43b-3c) — a case's reference configuration, as data: the overlay, its controls and the census tool

a43b-3c: `schema/overlay.sexp` and the first overlay; `prepare_div_inputs.reference_config` applies it over the mapped profile override and refuses any overlay that changes nothing, overlaps or names another case (14 tests, nine omissions in PROFILE-CONSISTENCY). `scripts/census_reference_config.py` re-derives a43b-3a's table from the tracked route, identically. No lapse: v5 and xlen-v2 still `--verify` equal. Two defects logged and scheduled: 37 stale guest citations (a43b-c1) and the deriver's literal `{new}` (a43b-c2).

## SEMULITH-P4-0334 (leaf P4-SYSTEM.14 a43b-3b) — CSR-SET's normative statements retained: RVP-CSR §1.1.1, the first from the privileged volume

a43b-3b: five exact statements of §1.1.1 in `profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html` (2,750 B, `RVP-CSR-STATEMENTS`) under the privileged preface's licence statement (`materials/RVP_CSR_RETENTION.md`), through `scripts/retain_statements.py`, one table for the excerpts to come; 19 cache-free tests and nine omissions in PROFILE-CONSISTENCY. No case, capture or credit yet.

## SEMULITH-P4-0333 (leaf P4-SYSTEM.14 a43b-3a) — the CSR-SET case designed: the reference configuration the case's own, all 33 CSRs witnessed

a43b-3a: measured before declaring on 28 of 33: the pinned Sail implements Zicntr under its public configuration (a CLINT device region, one tick per instruction), all five counter values agree, and over 171 guests the variant gains `mm-counters`, `mm-csr-ro-counters` and `c-irq` and loses `mip` readers, so it is per-case data, costing no lapse (`decision_reference-config-per-case.md`). The program is redesigned (136 instructions, 157 steps, M/S/U, all 33 CSRs, `AGREE` as a draft) and the policy review's category row is to be judged. This removes what ZICNTR waited for; raised to the director.

## SEMULITH-AC-0091 (leaf ARTIFACT-CLEANUP.35) — the ninth recurring cleanup through the supported act

.35: at 39 h, on a clean tree, the four acts ran in target/artifact-cleanup/AC0091 (log inside) at `handoff: OK`: 334 candidates planned, 6 captured Cargo incremental outputs (15,766,335 B) strictly selected and removed by the guarded core under a fresh census, residue 0, journal `complete`/`verified`, `--inspect` confirming; 25,436 retained files kept. Re-census against AC0090: 328 unrecorded (1,368,785,623 B), 39 new and 39 gone; they stay for `.29`'s ruled class C. The record is overwritten; `.36` is due after 2026-11-04T21:49Z.

## SEMULITH-P4-0332 (leaf P4-SYSTEM.14 a43b-2e) — the reviews read v5 and xlen-v2 and both are re-credited: the window closed

a43b-2e: the method review's rows name v5 and xlen-v2 (both `satisfied`, 88 authenticated files) and both measure 10 of 10 legs; `CR-GC-M-3` and `CR-D-XLEN-2` re-issue the credits by the same act, `CR-D-XLEN-2` with two limitations fewer than `CR-D-XLEN-1` — the producer's M words no longer describe its evidence; `REQ-GC-M` and `REQ-D-XLEN` `implemented` (46 planned / 2 implemented, 0 drift); both measured records in the dossier, their G-TRACE rows back, G-TRACE green (GS 3 of 10 axes open). The probes re-stated; `derived-status` 37 again. The planned lapse that opens CSR-SET ran a43b-2a … a43b-2e in one day. Containment: four closed records and 12 rows into `archive/P4-SYSTEM-25.md`. Next: a43b-3, CSR-SET.

## SEMULITH-P4-0331 (leaf P4-SYSTEM.14 a43b-2d) — v5 and xlen-v2 captured, exactly once each: traces byte-identical to their predecessors'

a43b-2d: each re-capture ran once on a quiet host behind three guards (a clean tree, no frozen path moved since the declaration commit, the declarations equal to their regeneration) and the retention preflight: baseline and repeat AGREE, the control DIVERGE at its declared step, complete, qualification false. All six traces and six stdout streams are byte-identical to v4's and xlen-v1's; each stderr differs only by the case directory it prints; each measured record differs from its predecessor's only in the manifest, stderr and receipt digests and, for XLEN, the control's declared id and prose. The family holds all 133 files; v5 and xlen-v2 `pending`. The retained-capture rows move with the re-credits (a43b-2e): a row names its capture commit. Next: a43b-2e.

## SEMULITH-XTASK-0075 (leaf XTASK.13 slice b2) — GUEST-GEN's base-mirror and parcel-count arms judge a frozen owner→mirror pair

`scripts/fixtures/guest-gen/base-mirror/` holds the eight guests the mirror governor's predicates need, from both units (7 recorded re-derivations, 3 of them pinned source re-derivations, and a count-only migration); the three base-mirror arms judge it under DEF-GEN's frozen encoding, the governor's seven self-test arms take that encoding (`check_gc_mirror.py --self-test --encoding`, its composition from the encoding's own root), and the five parcel-count arms count the frozen mirror (`derive_gc_parcel_counts.py --encoding --guests`; its self-test's manifest census over its own hand guests). Measured, HEAD's checker over HEAD's tree against the slice's: a damaged live mirror record, an unassemblable rv64i guest and a deleted rv64gc guest no longer refuse through these arms — the first two fail by name (exit 1; the generator's named refusal), the third keeps one miss, the parcel author's cold probe (slice b3). A first before run was invalid: `cargo xtask` fixes its root at build time (knowledge card `an-xtask-binary-judges-the-tree-it-was-built-in.md`). The book's doctrines page explains ruling 5 with the table. None of the paths frozen for a43b-2d moved. `GUEST-GEN --self-test: 400 pass / 0 fail`. Next: a43b-2d.

## SEMULITH-P4-0330 (leaf P4-SYSTEM.14 a43b-2c) — v5 and xlen-v2 declared: the control the case's own, the predeclaration otherwise identical

a43b-2c: `rv64gc-m-forms-v5` and `rv64gc-xlen-forms-v2` declared — each its predecessor's case file with the new id and the control declared (`wrong-quotient`; `truncated-address`), its four prepared inputs re-derived case-independently and byte-identical to v4's / xlen-v1's, its three declarations written from `capture_div.py --declare`; this commit is the declaration commit the captures name. With the id substituted, v5's planned record differs from v4's only in the dependency manifest's digest, xlen-v2's from xlen-v1's only in that digest and the control's id and prose; the literal guard and the case probe's control check (fired RED once) hold on both. The evidence family's fifth re-derivation: 133 files / 80 MiB, 105 present; `evidence/README.md` compressed. `6 case(s), 0 credited, 2 declared`. The manifests' 67 children and the 13 authority views are frozen until the captures. Next: XTASK.13 slice b2, then a43b-2d.

## SEMULITH-P4-0329 (leaf P4-SYSTEM.14 a43b-2b) — the one pinned edit: the control declared per case, CSR-SET's second-method vocabulary, both credits retired

a43b-2b: the case's `control` form gains optional `id` and `statement`, the producer emits them and refuses by name a case declaring neither (no M literal remains in `capture_div.py`; the four retained declarations render to their own bytes); two optional case forms, `second_method` and `adversarial`, judged by the policy review's risk-method leg at any risk by five conditions read from the record (distinct producer versions, recorded pairs whose shared inputs are the declared common inputs, no `shared` pair, adversarial properties of an agreeing capture); the command probe's literal guard (a unique-token control planned verbatim, prose only from the case file or the reviewed neutral set). Found and repaired: probes planning history now plan copies that declare a control, and the method review, which detected `stale` by regenerating, re-checks the declaration route's pins on the capture's own manifest when the producer refuses (v4 and xlen-v1 `stale` at `schema/matched-case.sexp`, not `refused`); knowledge card `a-producer-refusal-hides-staleness-detected-by-regeneration.md`. The lapse: `CR-GC-M-2`, `CR-D-XLEN-1` retired with `credits.sexp`; 48 planned; dossier copies and G-TRACE rows out, G-TRACE open (GS 4 of 10). Probes: DIV-COMMAND 20, DIV-METHOD 22, DIV-POLICY-PROBE 33; eight new seams, each RED; the token-facet inventory 127 with two new token languages. Next: a43b-2c.

## SEMULITH-P4-0328 (leaf P4-SYSTEM.14 a43b-2a) — the lapse window that opens CSR-SET, designed

a43b-2a, documentation only: the control's id and statement become optional fields of the case's `control` form that the producer requires (the four retained declarations cannot gain fields; one schema, not two); CSR-SET's high-risk vocabulary is two optional case forms, `second_method` and `adversarial`, judged for high or critical risk by five conditions read from the measured record (the graph's producers with distinct versions; recorded pairs whose shared inputs are the declared common inputs; no independence credit beyond the pair's assessment; adversarial properties of an agreeing capture); a guard against the literals' return; the order 2b (one pinned edit, both credits retired, 48 / 0) → 2c (v5, xlen-v2 declared, family 89 → 133) → 2d (captured once, traces identical) → 2e (re-credited, 46 / 2) → CSR-SET. The tree record, `decision_producer-debt-paid-before-the-next-case.md` and the unit book's policy page carry it. Containment: eleven closed `.14` records and 33 rows verbatim into `archive/P4-SYSTEM-24.md` (the live tree 129,223 → 93,927 B before the record); this file sharded (`shard-0422.md`, 15 entries; 64,028 → 48,866 B). The main book's task-history list, stuck at part 19, now lists the parts by glob. Next: a43b-2b.

