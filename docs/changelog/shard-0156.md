# DEV_NOTES shard — _(2026-10-02)_ … _(2026-10-02)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-02)_ — a device dossier reuses the machinery by declaration, and a datasheet's silences are requirements (P5-BOARD.2)

The first device unit (`sifive-uart-lab-v0`) taught the dossier machinery its third shape
(after generated-definition and sibling-crate): `vehicle (route device-model) (comparison
register-expectations)`. The load-bearing design choices:

**Applicability is derived, never exempted.** The instruction-shaped gates
(EXTRACTION, EXERCISE-COVERAGE, INTERACTION-MATRIX) read the `vehicle` declaration and
derive what applies: the device answers the legs it honestly can (every state element a
reset — the FIFOs' resets are recorded as *"unspecified", sourced to the measured silence*,
which satisfies the contract without inventing behaviour; every obligation a POS+NEG pair)
and the rest is n/a *by declaration* — with contradiction = RED in both directions (an
`encoding.sexp` or a `guests/` corpus beside the declaration refuses). Anti-drift by
construction: the day P5-BOARD.5's probes land, the gate refuses until taught the device
exercise leg.

**A datasheet's silence is a record, not an oversight.** Six of the nineteen requirements
are `unspecified`-category non-commitments — the sharpest found in execution: §13.8's
watermark bits carry a strict-inequality RAISED and a strict-inequality CLEARED condition
each, and the manual never says whether the bit is a pure level of FIFO occupancy or holds
between the two. The `==` boundary and every pre-first-condition value (including the
X-marked resets) are undetermined (`REQ-D-UART-WM-MODE`), so the expectation documents pin
a watermark bit only when its raised condition holds under *every* reading. The first
draft asserted "level conditions" — the dossier's own expected-results discipline caught
it before it ossified, exactly the failure EVD-05 exists to prevent.

**Naming is contract-shaped.** A private `REQ-U-` id prefix (for the unspecified records)
collided with RECORD-SCHEMA's mechanical `D-X` → `REQ-D-X` decision→requirement mapping —
the mapping is the contract, the prefix was convention. The records are now named by their
`source_semantics` category in prose and carry the house id shape; one fact, three
surfaces (requirement, obligation, decision), one wording, mechanically mirrored.

Validation: all dossier documents schema-validate; the three profile-glob gates decide the
device by declaration; every edited check's self-test green (17/9/14/41/7/14/10 arms, 0
fail); `make gate` all doctrines green; the mdBook builds and its index stays byte-exact.

