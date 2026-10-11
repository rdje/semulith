# Exact-token facets preserve the pattern search contract

- **Type:** `decision`
- **Date:** `2026-10-11`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a27, `SEMULITH-P4-0218`; schema kernel and a26 digest reproducer
answers: Why do exact-token facets use strict end anchors while generic patterns remain searches?

## The fact / decision

The schema kernel deliberately uses regex search. Its `$` end anchor also accepts
one terminal newline: a26 reproduced a 64-hex SHA256 plus newline passing the
reference schema. Inventory24 project schemas:91 patterned fields;83 old token
facets in13 files admit that boundary, while eight new artifact facets already
refuse it. Five complete-document regressions reproduce the admission too.

Repair the83 declarations to strict `\Z` ends (escape the backslash in the
S-expression string). Preserve their complete source bytes otherwise and leave
the generic kernel unchanged. Do not globally replace search with fullmatch:
a declared unanchored `needle` pattern must still accept `hayneedlehay`.
All current project patterns describe whole tokens; any future different pattern
contract needs a reviewed example rather than being silently skipped.

`probe_schema_token_facets.py` exercises every field with named valid tokens,
newline/other boundary refusals and five real complete documents through the
public kernel. Normal/optimized controls and loose-end, ignored-pattern and
fullmatch mutations discriminate. RECORD-SCHEMA runs them before judging records.
These are grammar controls, not artifact authentication, execution or qualification.
Canonical bytes, mappings, fixed seals/caps and CPU status remain unchanged.
