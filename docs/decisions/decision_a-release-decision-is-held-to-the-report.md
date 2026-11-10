# A release decision is of one unit, one version and one dossier, and `accepted` never exceeds the report

- **Type:** `decision`
- **Date:** `2026-11-10`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.18` slice c1, `SEMULITH-P4-0397`; the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: What makes a recorded release decision stand, when does it stop standing, and who records one?

## What was measured

Before this unit a `decision` row in `gate.sexp` needed only a tracked file. With the other nine axes green, any tracked record turned `G-RELEASE` green and the verdict `passed`. "Accepted only on passed" was a sentence in a task leaf, and nothing tied a decision to the bytes it accepted.

## The decision

1. **The record states one form.** A release decision is a record in `docs/decisions/` with one form in a fenced `lisp` block:

   ```text
   (release (unit "<unit>") (version "<version>") (outcome "accepted") (dossier-sha256 "<digest>"))
   ```

   The record lives outside the dossier, so pinning the dossier's digest is not a fixed point.
2. **The report verifies it at every commit.** The unit and the version must be the profile's, and the digest must be the dossier's today. When the dossier moves, the decision stops standing and `G-RELEASE` reads `incomplete` until a decision is recorded for the new bytes. That is intended: a release is of exact bytes.
3. **`accepted` never exceeds the report.** It stands only while every other axis is green, a verified record of a native x86_64 host is in the manifest ([`decision_hosted-run-is-a-record.md`](decision_hosted-run-is-a-record.md)), and the manifest declares at least one capability limit. Limits are `(limit (statement "…"))` forms in `gate.sexp`, and the report lists them. `experimental` may be recorded over open axes.
4. **Who records it.** `ROADMAP.md` says of gate `CPU-SYSTEM`: "It does not require a new user permission ceremony." `docs/EVIDENCE_AND_GATES.md` §7 says a release decision "is recorded by the designated project maintainer or delegated release procedure after machine-generated results". So the workflow records it, as a local commit, under the director's rulings of 2026-11-06 and 2026-11-07. Publishing it is a push, and a push below the cadence stays the director's to approve.
5. **The act is separate.** This unit lands the mechanism with no decision in the tree. Slice c2 is the act.

## The rehearsal

On a clone of the tree, with the real dossier of `rv64gc-lab-v0`:

| Step | The report reads |
| --- | --- |
| before | `incomplete`, 1 of 10 axes open |
| a decision pinned to another digest | `incomplete`: the decision is of another dossier |
| the decision pinned to the dossier's digest, one limit declared | `passed` |
| one comment added to `gate.sexp` afterwards | `incomplete`: the decision is of another dossier |

## What this does not settle

- `profile.sexp` says `(status "development")`, and 88 retained evidence files name that file, so it cannot move outside a pinned window. The decision record says what the artifact is; that field does not.
- The scalar unit's report reads its decision as prose. `P4-SYSTEM.19` owns that unit's records.

## How to apply

- To record a decision: add the row and the limits to `gate.sexp`, read the digest the report prints under "The versioned artifact", write the record with it, and regenerate. The record is outside the dossier, so writing it does not move the digest.
- After any dossier change the decision no longer stands. Record a new one for the new version, or let the gate read `incomplete`.
