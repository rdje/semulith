# TOOLBOX.md — the tools-first diagnostic doctrine

⛔ **TOOLS-FIRST.** For ANY unknown — a failure, a crash, a hang, a surprising result, a
"why isn't this working" — reach for a diagnostic tool FIRST. Never eyeball the code and
guess a root cause.

## The rule

- A code change cannot land without **tool-backed WHY + WHERE** and a **measured
  before→after** recorded in its task-tree leaf (see the acceptance checklist in
  `DOCTRINE_ENFORCEMENT.md`).
- If no existing tool shows WHY+WHERE, **build one** — a probe, a tracer, a counter, a
  minimal reproduction harness. The diagnostic tool is a first-class deliverable, kept in
  the repo, not a throwaway.
- **ANTI-SPIN TRIPWIRE:** if you have analyzed for ~2 turns without producing NEW tool
  output that pinpoints WHY+WHERE, STOP — run a tool, build one, or escalate. Never loop
  on analysis.

## The 3-step UNKNOWN protocol (adapt the specific tools to your domain)

1. **WIDEN** — dump the full picture: enumerate all cases/states, the broadest inventory,
   so the failing one is visible in context.
2. **NARROW** — probe the specific failing case for its exact verdict + position/state.
3. **PINPOINT** — a scoped trace that names the exact function/rule/line that fails and why.

The point is to convert "it's broken somewhere" into "line X of function Y rejects input Z
because predicate P is false" before writing a single line of fix.

## This project's toolbox

Every diagnostic here is **tracked**, so a number it produced can be re-derived by the next
reader — that is leg 3 of `docs/CLAIM_VERIFICATION.md`, and an instrument living in a scratch
directory is a "trust me" with extra steps.

The tools live in four family tables under [`docs/toolbox/`](docs/toolbox/) — partitioned at
`LIVE-CONTAINMENT.3` when this file reached 20,478 of its 20,480 bytes. Pick the family that
matches your question:

| Family | Holds |
| --- | --- |
| [governance](docs/toolbox/governance.md) | Repository discipline — the doctrine enforcer, mirrors, routing, history, push, provenance |
| [definition](docs/toolbox/definition.md) | The canonical definition — S-expressions, schemas, fragments, semantics, generators, citations |
| [composition](docs/toolbox/composition.md) | Composition and the board — records, assumptions, composed units, the board, its platform export |
| [execution](docs/toolbox/execution.md) | Execution and evidence — the engines, the guests, coverage, references, bench, materials |

⛔ **A gate that has never been observed RED is not known to work.** Before trusting any check
added here, fire it against a deliberately broken input — the first two project checks
(DELIVERY-PROVENANCE, FIXTURE-FINGERPRINT) were fired against the real corpus (a byte appended
to `docs/GLOSSARY.md`; a byte appended to `examples/synthetic-spec.md`) and each named the
right file and the right reason before being registered.

<!-- Add each new diagnostic as a row in its family table under docs/toolbox/: what question it
answers (WHY / WHERE / how-much) and how to invoke it. The next agent should reach for the
right tool without reading the source. -->
