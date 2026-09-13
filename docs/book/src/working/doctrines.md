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

## The seams, and why they are not a loophole

A neutral check is adapted to a project through `.doctrine/`, never by editing the check:

- **`code_paths.txt`** declares what counts as a code change here. The built-in default was
  measured wrong in both directions over all 125 tracked files — it classified 28 files of
  mdBook prose as code because their path contains `src/`, and it could not see the two
  registries that hold the gates' own ceilings and dispositions, the `.doctrine/` seams, both
  git hooks, and `Cargo.toml`/`Cargo.lock`.
- **`evidence_tokens.txt`** declares this project's instrument signatures. It exists because
  `GAP-CLAIM-CENSUS` prints `git grep … | wc -l` in its own failure hint while
  `TASK-ACCEPTANCE`'s default signature family did not recognise either command — obeying one
  gate produced evidence the other refused.

⛔ Narrowing a gate's scope is precisely the change that can silently disable it, so a seam
edit is only trusted after the outcomes are **fired and observed**: a real code change with no
owning leaf must still be refused, gate data with no owning leaf must now be refused, and prose
alone must pass. A seam that has not been fired is an assertion.

### A seam was the wrong place for three of those fixes

The defects the seams were compensating for are **repaired in the checks themselves**. The
reason is a measurement: with both seam files moved aside, the full enforcer printed
`=== all doctrines green ===` and `rc=0`. Three fixes had silently reverted and nothing said a
word. *A fix whose disappearance is undetectable is not a fix.*

What belongs where is not arbitrary. The anchored `src/`, the three universally
behaviour-governing path families, and the shared census vocabulary are true of **every**
consumer of the template — repairing them in the check is a repair, not a fork. This project's
own gate *data* and *instrument signatures* stay in `.doctrine/`, because a neutral check cannot
know they exist. And both repaired checks were removed from `update_scaffold.sh`'s re-sync list,
so a scaffold update cannot quietly undo them.

`SEAM-INTEGRITY` then guards all of it by asserting **behaviour rather than presence** — every
acceptance box already committed must still be accepted, and the two gates must still agree on
what an instrument is. That last rule is the structural one: the divergence between those two
lists refused honest evidence three times before it was fixed rather than patched.

## Adding one

Write `scripts/check_<name>.sh` — cheap, deterministic, read-only, self-describing, nonzero on
breach. Register it: universal checks in the driver's array, project checks in
`scripts/check_doctrines.project.sh`. Mirror it in `DOCTRINE_ENFORCEMENT.md`. Never hardcode a
project's paths or tool names into a neutral check — that is what the `.doctrine/` seams are
for, and the difference between adopting a portable standard and forking someone's workflow.
