# My id → record map handles duplicates fine — why did the gate stay green on a self-contradicting catalogue?

**It didn't handle them; it hid them.** A dict built as `{r["id"]: r for r in records}`
collapses duplicates last-wins, silently, and every check downstream of the map examines only
the survivor. The catalogue can contradict itself and the gate stays green.

## What happened

Designing the record merge (`SOT-FORMAT.5`), the existing RECORD-SCHEMA gate indexed a
catalogue exactly that way. A probe fed it a scratch `requirements.sexp` with two records
sharing one id and different content (`risk low` vs `risk critical`):

```
$ python3 gate_body.py probe_root
__CHECKED__ 1          # rc=0 — nothing refused a catalogue arguing with itself
```

Both records individually conformed to the schema, so the schema layer had no complaint either.
The contradiction lived entirely in the id collision — and the map erased it before any rule
could see it.

## The rule

**Id uniqueness is a gate rule, never a data-structure accident.** Wherever a population is
keyed by an identifier — records, sources, decisions, fragments — the lookup must *refuse* a
repeated key, naming it, before any cross-check runs on the map. The collapse is not an
implementation convenience; it is a decision about which of two contradictory facts wins, made
without a human and without a log.

The same probe discipline matters: the defect was invisible until duplicates were *written into
a fixture on purpose*. A gate whose RED arms only cover shapes the corpus already has cannot
see what the corpus never does.

## Where this has bitten

- `SOT-FORMAT.5` (2026-09-27): RECORD-SCHEMA rule 8 (UNIQUE-ID) added after the probe above;
  the merge tool re-checks the same precondition because it must stay robust for draft units
  that never passed the gate.
