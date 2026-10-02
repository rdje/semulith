# The platform capability manifest

The document below is the board's **read-only derived export** for a compatibility
checker (`docs/ARCHOGEN_INTEGRATION.md` §3; OWN-06) — generated, never handwritten.
`scripts/gen_platform.py` derives it from the three canonical inputs fingerprinted in
its header (the board definition, the pinned processor's profile dossier, the composed
contract obligations), and the PLATFORM-GEN doctrine re-derives it on every commit and
refuses drift. What you see here is the same file the dossier links to
(`profiles/netboard-lab-v0/platform.sexp`), included — one owner, two readers. Its
contract is `schema/platform.sexp`.

Three properties are worth reading for:

- **Every facility carries an explicit `presence` marker** — `offered`,
  `absent-by-contract`, `limited` — so a checker reads exactly what is on offer, and an
  absence is a declared fact with its evidence edge, never an omission.
- **The dossier pin is verified, not displayed.** The generator re-derives the
  processor's dossier digest from the live dossier and refuses a stale pin — the pin was
  display-only until this leaf measured it.
- **The non-claims are data.** A compatible manifest proves neither OS correctness nor
  manifest-implementation match; test-control capabilities are the platform package's
  declaration, evidenced by the runner's own suites; and no archogen eADL interface
  exists today — archogen is actively developed, so this export is validated by
  derivation freshness, schema conformance and §3 coverage, never by archogen
  acceptance. The real-interface inspection is the `AG-OS` tree's.

```sexp
{{#include ../../../../profiles/netboard-lab-v0/platform.sexp}}
```
