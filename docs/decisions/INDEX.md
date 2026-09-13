# Decision & Fact Records — Index (memory layer C)

Durable, cross-cutting facts and decisions live here, one record per file (ADR-style). Every
record must be listed below (the MEMORY-ARCH doctrine check enforces it). New record: copy
`TEMPLATE.md` → `<type>_<short-kebab-slug>.md`, fill it in, and add its row.

| Record | Type | One-line hook |
| --- | --- | --- |
| [`decision_claim-verification-adopted.md`](decision_claim-verification-adopted.md) | `decision` | "checked" means re-derived, falsified and durable; a missing leg is named, never omitted |
| [`decision_delivery-provenance-is-frozen.md`](decision_delivery-provenance-is-frozen.md) | `decision` | a delivered manifest records what arrived; its live rows are declared, not silently drifting |
| [`decision_public-repository-no-confidential-content.md`](decision_public-repository-no-confidential-content.md) | `project` | the repo is public and carries nothing confidential, so evidence is recorded unredacted |
