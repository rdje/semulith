# `REQ-GC-M` is credited `implemented` on the retained m-forms case, signed by review under delegation

- **Type:** `decision`
- **Date:** `2026-10-26`
- **Status:** `active`
- **Owner / source:** the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md),
  answering the three questions `P4-SYSTEM.14` a42ay put to the director (target/p4-system-14/a42ay/design.md
  "For the director"); continues [`decision_credit-is-a-catalogue-record.md`](decision_credit-is-a-catalogue-record.md)
  and [`decision_ten-legs-satisfied-credit-separate.md`](decision_ten-legs-satisfied-credit-separate.md).
answers: Who signs the first credit record, is one finite case enough for `implemented`, and what does the credit not claim?

## The fact / decision

1. **Authority.** The record `CR-GC-M-1` in `profiles/rv64gc-lab-v0/credits.sexp` carries `authority review`:
   the workflow's review, under the director's delegation of 2026-10-26, cited by this record. It never
   carries `director`, since the director did not sign it.
2. **Sufficiency.** One finite case — `rv64gc-m-forms-v3`, 25 witnesses: the 13 M forms and the 12 Table 1
   cells, one each — whose ten policy legs are measured `satisfied` (`DIV-POLICY: satisfied — 10 of 10 legs`)
   is sufficient for `implemented`, and for nothing more. The derivation defines `implemented` as "every
   effective obligation credited through a current record" (`scripts/requirement_status.py`), and the
   policy defines a credit by its legs (`EVIDENCE_POLICY.md`, "Records, controls and currentness"); both
   hold. The record's `limitations` say what the status does not claim: a finite case, one witness per
   form and per Table 1 cell, the receipt's own words "not all M or CPU acceptance", no claim about the
   CPU's other extensions or about acceptance.
3. **Retention first.** Done before the act: the §11.1.1 statement (a42z, `RVI-M-DIV-STATEMENT`) and the
   other eleven M statements with Table 1 (a42bb, `RVI-M-STATEMENTS`) are retained; the record names both.
4. **The act** (`P4-SYSTEM.14` a42az, one commit): the record; `implementation_status implemented` on
   `REQ-GC-M` in `requirements.sexp`; the GS gate report regenerated; the two model-book chapters that said
   "`REQ-GC-M` keeps deriving `planned`" updated to the derived status. The derivation must report 47
   `planned`, 1 `implemented`, 1 credited, 0 drift.

## Why

- The alternative readings were weaker, not stricter: refusing `implemented` until a wider case exists would
  leave a satisfied ten-leg measurement crediting nothing, which the policy does not ask for; crediting
  more than `implemented` has no status to credit into (the vocabulary is `planned`, `partial`,
  `implemented`, `not-applicable`; `qualification` is a forbidden success word).
- Signing as `review` keeps the authority chain honest and auditable: the delegation record says who
  delegated, when and in what words; the credit says who signed under it.

## How to apply

- A wider M case (more witnesses, or a different reference) supersedes `CR-GC-M-1` by a new record in the
  commit that lands it; the old record is removed there, never repaired (the catalogue decision).
- Any pin movement lapses the credit — the three pins and, through the case's dependency manifest, every
  pinned method input (verified 2026-10-26: `definitions/riscv/m.sexp` moved one byte → `credit CR-GC-M-1 …
  lapsed: manifest input … SHA256 differs`) — the status falls back to `planned`, the gate fails: the act's inputs
  (`measured-experiment.sexp`, `verification.json`, `EVIDENCE_POLICY.md`) are retained bytes and stay so.

## Retirement (2026-10-29, `P4-SYSTEM.14` a44-2b)

`CR-GC-M-1` was retired by removal, as "How to apply" prescribes, in the slice that moved the matched cases'
declarations into data ([`decision_case-declarations-as-data.md`](decision_case-declarations-as-data.md)). That
slice edits inputs the m-forms capture's dependency manifest pins (`scripts/matched_gpr_property.py`,
`scripts/capture_div.py` among them; measured: `credit CR-GC-M-1 lapsed: manifest input scripts/capture_div.py:
SHA256 differs`), and a lapsed record is a finding. In the same commit: `REQ-GC-M` records `planned`
(`REQUIREMENT-STATUS: … 48 planned; 2 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`),
the dossier copy of the case's measured record leaves `references.sexp` and its `G-TRACE` row leaves `gate.sexp`
(an unqualified dossier experiment is a PROFILE-CONSISTENCY finding), the catalogue file leaves with its only
record (RECORD-SCHEMA refuses an empty catalogue; an absent one is no credits, as before a42az), and the record's
text is kept frozen as the qualification probe's fixture (`scripts/fixtures/dossier-qualification/credits.sexp`). The sufficiency and
authority rulings above stand unchanged for the re-credit: the M case re-captured as `v4` under the new manifest
(a44-3, a44-4) is credited by a new record, `CR-GC-M-2` (a44-5), through the same crediting act.
