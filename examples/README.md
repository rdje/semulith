# Synthetic data examples — v0.2

These records illustrate the starter schemas. They describe a self-defined 16-bit arithmetic fixture, not RISC-V or a real DSP. No model implementation or test execution is claimed. Evidence is deliberately `planned` and contains no invented passing result or binary hash.

- `synthetic-spec.md` is the local authority for this fixture only.
- `sources.json` pins its actual file hash.
- `requirements.jsonl`, `evidence.jsonl`, and `contract-obligations.jsonl` validate one record at a time against their matching schemas.
- `fixture-context.json` declares the example profile, obligation IDs, and check IDs so their purpose is reviewable. It is fixture context, not a completed global catalog schema.

The production P1 graph checker must additionally validate identities, scope, dependencies, implementation ownership, artifact hashes, freshness, policy, and completed evidence. A passing schema check does not supply those checks. Completed proof evidence must name the actual checked proposition, checker, assumptions, and bounds; a `passed` record without completed-run artifacts is invalid even at the schema level.
