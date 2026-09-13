# Planning package checks — v0.2

Date: 2026-09-13. These checks apply to this documentation/schema package. No CPU, DSP, board, OS execution, or conformance gate has been run or passed.

| Check | Result |
|---|---|
| JSON Schema Draft 2020-12 schemas, checked with Python jsonschema 4.26.0 | All 3 schemas valid |
| Synthetic requirement/evidence/contract records | All 5 records validate against their matching schemas |
| Negative schema controls | All 6 rejected: missing source, invalid research status, passing evidence without completion data, malformed fingerprint, passing proof without proof metadata, invalid contract direction |
| Synthetic source fingerprint | Matches the included source file |
| Example profile/requirement/evidence/obligation links | Checked for the supplied records; all evidence remains planned |
| Information catalog | All C01–C24 retained |
| Review disposition | All M1–M19 addressed |
| Local Markdown links and code fences | Links resolve; fence pairs balanced |
| archogen integration review | Compared against supplied revision 2.0 §§3–6, 12–15 and F13–F16/F19/F22/F23/F29/F30 |

The production graph checker, artifact-freshness analysis, source interpretation validation, Rust implementation, and acceptance automation remain future work. The limited fixture-link checks above are not a general dependency graph implementation. The source ledger contains research candidates, not acquired reference builds.

`MANIFEST.sha256` records exact package file contents except itself. `DESIGN_INPUTS.json` records the actual local fingerprints of the supplied design inputs for provenance; those input documents are not reproduced in the archive.
