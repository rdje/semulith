# A loader that builds the review's records moved every mutation count of the property probe — why, and what shape keeps them?

**Two copies of one module are two classes.** `scripts/probe_matched_gpr_property.py` applies one mutation to the
text of `scripts/matched_gpr_property.py` and executes the result as a separate module (`exec` into a fresh
`types.ModuleType`). Every frozen dataclass in that copy — `ReviewedPropertyCase`, `PropertyAuthority`,
`ReviewedProperty` — is a new class object. A dataclass's generated `__eq__` compares fields only when
`other.__class__ is self.__class__`; otherwise it returns `NotImplemented` and the comparison is `False`. A case
declaration loader (`scripts/matched_gpr_case.py`, `P4-SYSTEM.14` a44-2b) that built those records from the
*original* module would hand the mutated copy records of the other class, so `selected.authority == case.authority`
fails in every arm — not just the arm the mutation targets — and all 35 measured loss counts shift together.

## The shape that keeps them

- **The loader returns neutral data; the consumer maps it.** `matched_gpr_case.read_case` returns a dictionary of the
  schema's fields with tuples for the repeated forms and imports no record type; `matched_gpr_property.reviewed_case`
  maps it onto its own classes, so a mutated copy maps onto the copy's classes. Measured after the switch: every one of
  the 35 arms lost exactly what it lost before (target/p4-system-14/a44-2b/property-arms.txt). It also removes the
  import cycle a record-building loader would need (loader → property module → loader).
- **Keep a pure function pure by passing what the caller already holds.** The binder `bind_source_property` opened no
  file and its probe asserts that under patched `open`; reading the declaration inside it would break that. A caller
  that selected the case passes it (`case=`), and only the id-only path reads the declaration.
- **A traced I/O window is a contract too.** The producer review traces `Path.open` while the authority review runs and
  requires exactly the 13 current views; a declaration read inside that window is "unreviewed". Resolve the case
  before the window and pass it in — whether a given pathlib method routes through `Path.open` is the interpreter's
  business ([`a-count-of-pathlib-calls-tests-the-interpreter.md`](a-count-of-pathlib-calls-tests-the-interpreter.md)).

## How to catch it

Before moving a constructor out of a module that a probe mutates by `exec`, grep the probe for `exec(` /
`module_from_spec` and run its full mutation table, not just its green arm: a green arm passes either way; only the
loss counts show the class split.

Evidence: target/p4-system-14/a44-2b (equality-before-removal.txt, property-arms.txt, green-1 and green-2 runs);
`docs/tasks/P4-SYSTEM.md` `.14` a44-2b; `decision_case-declarations-as-data.md`, Addendum.
