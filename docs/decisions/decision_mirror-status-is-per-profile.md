# A mirrored requirement's status belongs to the mirror's profile where that profile derives it

- **Type:** `decision`
- **Date:** `2026-10-29`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43a-3, `SEMULITH-P4-0327`; the workflow's decision under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md), found by the crediting act of
  [`decision_req-d-xlen-credited-implemented.md`](decision_req-d-xlen-credited-implemented.md); RECORD-SCHEMA rule 14
  (MIRROR-DERIVE, `xtask/src/check_requirements.rs`) and `scripts/requirement_status.py`.
answers: Why did crediting REQ-D-XLEN in rv64gc-lab-v0 trip MIRROR DRIFT, and which rule owns a mirrored requirement's implementation status?

## The fact / decision

1. **Two rules met for the first time.** RECORD-SCHEMA rule 14 holds every rv64gc requirement in the base-corpus
   closure to equal rv64i-lab-v0's record on every field but `profile_ids` (`doctrine/fact_ownership.tsv`,
   `base-requirements (rv64gc-lab-v0)`). REQUIREMENT-STATUS derives each policy-declaring profile's
   `implementation_status` from that profile's own evidence and refuses a recorded status that differs from it.
   `REQ-D-XLEN` is the first mirrored requirement a credit moved: rv64gc derives `implemented` (CR-D-XLEN-1), rv64i
   has no case and derives `planned`. Both statuses are right; rule 14 refused the pair (`MIRROR DRIFT
   requirements.sexp [REQ-D-XLEN]: field 'implementation_status' differs from the owner's record`).
2. **The status is the mirror's own where its profile derives it.** Rule 14 now leaves `implementation_status` out of
   the comparison exactly when the mirror's profile directory carries `EVIDENCE_POLICY.md` — the condition under which
   `requirement_status.py` derives and drift-checks that profile (its `selected` profiles). Every other field — the
   statement, kind, forms, sources, applicability, research status, semantics, risk, obligations, dependencies and
   links — is still compared. A mirror whose profile does not derive statuses still may not differ in status.
3. **Measured.** Two new arms, each discriminating: `GREEN a mirror's status its own profile derives` (misses with the
   exemption removed: `80 pass / 1 fail`) and `RED a mirror's status nobody derives` (misses with the exemption made
   unconditional: `80 pass / 1 fail`); `RECORD-SCHEMA --self-test: 81 pass / 0 fail`; the real check `ok`.

## Why

- A status is not the requirement's meaning. The project already says so where meaning is pinned:
  `scripts/matched_gpr_property.py` normalizes `implementation_status` to `planned` before its semantic digest (its
  probe's `test_publishing_derived_status_and_links_does_not_change_semantic_authority`), and the requirement-status
  chapter: "The catalogue's `implementation_status`
  is not carried; it is derived from the evidence graph". A mirror is a derived copy of the owner's *meaning*.
- The alternatives were dishonest or impossible: crediting rv64i's `REQ-D-XLEN` with an rv64gc capture claims evidence
  rv64i does not have; dropping the record from the mirror breaks the closure rule 14 also enforces; keeping rv64gc
  `planned` is drift REQUIREMENT-STATUS refuses. The exemption keeps one owner per fact: meaning — the owner unit;
  status — each deriving profile's evidence.

One definition of the condition: `scripts/requirement_status.py` exposes `derives_statuses(profile_dir)`, which its own
profile selection uses and rule 14 calls (imported, never copied), so the two can never disagree on which profiles
derive their statuses. Considered and not taken: declaring field scope as a facet in the schema kernel — the kernel
(`check_sexp_schema.py`) is pinned by every capture and refuses unknown facets, so it would lapse both credits for a
declaration the predicate already gives.

## How to apply

- Each later credit of a mirrored requirement (the base-corpus closure) needs nothing more; a mirror profile without
  `EVIDENCE_POLICY.md` stays fully byte-equal.
- `implementation_refs` and `evidence_ids` are still compared; widening the exemption to them needs its own measured
  case and arms.
