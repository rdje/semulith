# Schemas and fixtures

`schemas/` holds three JSON Schema (draft 2020-12) starters, and `examples/` holds fixtures
that exercise them. Both are **starting data contracts**, not an implemented evidence system.

## The three record types

| Schema | Record | The field that carries the weight |
| --- | --- | --- |
| `requirement.schema.json` | one source-linked obligation | `source_semantics` — the *original architecture's* category (`defined`, `implementation-defined`, `unspecified`, `undefined`, `reserved`, `unpredictable`, …), kept separate from `research_status` and `implementation_status` |
| `evidence.schema.json` | one evidence result | `producer.independence` — a classification (`unknown`, `shared-definition`, `partly-independent`, `independently-derived`), a scope, and a justification |
| `contract-obligation.schema.json` | one CPU/environment assumption or guarantee | `authority` — `architecture`, `implementation-profile`, `platform`, or `laboratory` |

Three separate status axes on a requirement is not bureaucracy. *Is this relevant to the
profile?*, *do we understand it?* and *have we implemented it?* are independent questions, and
a single "status" field forces two of them to be guessed.

## What the schemas actually enforce

Shape, and two conditional rules worth knowing:

- an evidence record with `status: passed` or `failed` must carry `procedure`, `tool_versions`,
  `result_summary`, **and at least one input and one artifact** — a passing result with no
  completed-run data is invalid at the schema level;
- a `passed` record whose `method` is `checked-proof` must additionally carry `proof`, naming
  the proposition, the checker, the assumptions, and the bounds.

## What they do not enforce

Everything that matters most. Identifier references, profile consistency, graph integrity,
artifact existence and hashes, evidence freshness, and gate policy are the **P1 checker's**
job. A syntactically valid JSON file is not an accepted CPU claim, and `schemas/` cannot make
it one.

## The one claim this repository can currently re-derive

The delivered package reports schema validation performed with Python `jsonschema` 4.26.0 in
its author's environment. That environment is not this one, so those results are **cited, not
re-derivable here** — and rule `RUST-01` makes the re-derivation a Rust deliverable rather than
a Python dependency.

What *is* re-derived, on every commit, is the fixture's own fingerprint claim: the
`FIXTURE-FINGERPRINT` gate re-hashes every record that pins a file's `sha256` and fails if it
no longer describes the tree.
