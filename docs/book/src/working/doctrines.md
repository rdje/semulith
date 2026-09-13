# The doctrine gates

A rule that lives only in a document is a suggestion. Every mechanizable rule here is a script
that exits nonzero, wired into four layers so that non-compliance is expensive rather than
merely discouraged:

| Layer | Mechanism | What it catches |
| --- | --- | --- |
| E1 — discovery | the doctrine documents, reachable from every harness's bootstrap file | "I did not know the rule" |
| E2 — self-check | `scripts/check_doctrines.sh` and each registered check | the rules, executable, runnable by hand |
| E3 — git hook | `.githooks/pre-commit` runs the enforcer | fast local failure |
| E4 — CI | the same enforcer runs server-side | a locally `--no-verify`'d commit |

`make gate` is that command. Thirteen checks run today.

## The universal registry

These ship with the discipline spine and are project-neutral:

| ID | Proves |
| --- | --- |
| `MEMORY-ARCH` | the durable four-layer memory invariants hold |
| `DOCPATH` | no tracked markdown carries a checkout-specific absolute path |
| `TASK-TREE-OWNERSHIP` | every staged code change is owned by a task-tree leaf |
| `TASK-ACCEPTANCE` | that leaf's three hard-gated boxes are ticked and carry tool output **inside each box** |
| `WAIVER-ROUTING` | a leaf saying a gate does not apply names the leaf that owns fixing it |
| `README-STABILITY` | the landing page stays one, under a line cap **and** a byte cap |
| `LIVE-DOC-CURRENCY` | no document reports its own currency — git already carries it |
| `LESSON-PROMOTION` | a new dated lesson reaches the retrievable layer or is explicitly declined |
| `ROUTING-EVIDENCE` | a finding routed to another tree carries what was measured |
| `GAP-CLAIM-CENSUS` | a "nothing checks X" claim records the census it rests on |
| `TABLE-ARITY-RATCHET` | no staged markdown raises the count of table rows whose cells disagree with their header |
| `KNOWLEDGE-MAP` | the derived orientation map is in sync with its sources |
| `PROJECT-SPECIFIC` | this project's own doctrines, below |

## This project's own doctrines

| ID | Proves |
| --- | --- |
| `DELIVERY-PROVENANCE` | every delivered manifest row carries exactly one declared disposition, and the frozen ones still hash to the delivered bytes |
| `FIXTURE-FINGERPRINT` | every record pinning a file's `sha256` still describes the tree |
| `README-ROUTING-CLOSURE` | every destination the landing page routes to is governed, exists, and stays under its ceiling |

Each ships a `--self-test` whose RED arms assert the **reason** as well as the verdict, each was
fired RED before being registered, and each **refuses** — exit 2, not exit 0 — rather than
passing if its own self-test stops discriminating. A check that cannot judge must never report
that the rule holds.

## Two doctrines that are easy to misread

**`WAIVER-ROUTING` does not punish honesty.** A waiver stays legal; it simply has to name the
leaf that owns fixing the gate. An author writing a waiver *is the gate reporting a missing
capability*, which is the highest-signal defect report a gate can receive.

**A line cap is not a size bound.** Measured on a real project running this spine: a file whose
own header called it a "bounded resume pointer" sat at 60 lines — passing, exactly at its cap —
carrying **138,403 bytes**, with one line of 18,816. Line and byte caps are complements, not
redundancy: neither wrapped prose nor very long lines can bypass the budget. Never raise a cap
to fit content.

## Adding one

Write `scripts/check_<name>.sh` — cheap, deterministic, read-only, self-describing, nonzero on
breach. Register it: universal checks in the driver's array, project checks in
`scripts/check_doctrines.project.sh`. Mirror it in `DOCTRINE_ENFORCEMENT.md`. Never hardcode a
project's paths or tool names into a neutral check — that is what the `.doctrine/` seams are
for, and the difference between adopting a portable standard and forking someone's workflow.
