# A credit is a catalogue record that the derivation authenticates, never a flag in a retained receipt

- **Type:** `decision`
- **Date:** `2026-10-23`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42ay, `SEMULITH-P4-0293`; the policy's words in
  `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md` ("Records, controls and currentness": each credited
  disposition links the requirement, effective obligation, owner, tracked runner and structured evidence
  record; "Status and supersession": status is derived and drift-checked from the graph; no typed success
  word substitutes for executed evidence); continues
  [`decision_ten-legs-satisfied-credit-separate.md`](decision_ten-legs-satisfied-credit-separate.md).
answers: How is a requirement credited once a case's measurement satisfies every policy leg, and what keeps that credit honest when the tree moves?

## The fact / decision

1. **The record.** A credited disposition is one `(credit …)` record in the profile catalogue
   `profiles/<profile>/credits.sexp`, validated by `schema/credits.sexp` through RECORD-SCHEMA like the
   requirement and obligation catalogues. It names the requirement, the effective obligations, the case,
   and pins by path, SHA256 and size the measured record, the receipt and the policy document; it names
   the retained sources it rests on, its authority, date, decision record, the number of legs measured
   and its limitations. An absent catalogue is no credits.
2. **The reader.** `scripts/credit_records.py` (unpinned; `records_sexp.py` and `record_catalog.py` are
   pinned children of every declaration and refuse unknown heads, so they do not change) loads the
   catalogue and reports each record `current` or `lapsed`: current only while every pin still describes
   the tree, every input of the case's dependency manifest authenticates, the receipt is a complete
   canonical capture that carries no verdict of its own, and the declaration binds the credited
   requirement and obligations.
3. **The derivation.** `scripts/requirement_status.py` credits a binding only through a current record
   naming its case, requirement and obligation. A receipt whose `qualification` is true is a finding (a
   typed success word), never a credit; a lapsed record, or one naming an unknown case or requirement, is
   a finding. `scripts/review_div_policy.py` reports `credited` from the catalogue and makes a record
   over a measurement that is not `satisfied` a finding. The gate runs both on every commit.
4. **The act is separate.** This unit lands the mechanism with no record in the catalogue: the real tree
   derives `REQ-GC-M` `planned`, 0 credited, 0 records. Writing the first record — and moving the
   recorded `implementation_status` with it, in one commit — is the crediting act, under the ruling the
   director owns (authority; sufficiency of one finite case of 25 witnesses; retention of the §11.1.1 and
   Table 1 spans first).

## Why

- A retained receipt is never replaced (`evidence/README.md`), so the flag it carries can never become
  true honestly; crediting through it would mean rewriting retained bytes.
- A record the derivation re-authenticates on every read gives the policy's currentness rule teeth: a
  moved pin lapses the credit, the status falls back, the recorded status drifts, the gate fails. A
  policy change is a capture, not a note — and not a credit either.
- Keeping the record a catalogue beside the requirements it credits keeps the evidence family's 21 slots
  untouched and keeps the DIV-specific leg review out of the generic derivation: the derivation hashes
  pins; the gate's policy step owns the legs.

## How to apply

- Never set `qualification` true in a receipt; never edit a retained receipt. Credit by adding a record.
- A record's pins are taken from the tree at crediting time (`shasum -a 256`, `wc -c`); `python3 -B
  scripts/credit_records.py --profile <id>` reads them back and says which record is current.
- When a pinned input moves, do not repair the record: capture a new case, measure its legs, and write a
  new record; the old one is removed in the commit that supersedes it, with its history in git.
