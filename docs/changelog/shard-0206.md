# DEV_NOTES shard — _(2026-10-05)_ … _(2026-10-05)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-05)_ — the counters started moving, and a view that masked them appeared (P4-SYSTEM.5 slice a)

Execution of the `.5` brief's checkpoint (a) measured:

- **The `.2` zeros were right for the wrong reason.** mm-counters read 0 at
  every cell because nothing moved — and nothing could have SHOWN a move: the
  architectural CSR read computes a view's exposed mask from the view's declared
  fields, and a field-LESS view masks to zero. The counter views would have read
  0 forever, statements notwithstanding ("a read-only shadow of mcycle"). The
  first timekeeping test caught it (cycle read 0 where the storage held 2,
  rc=1), and the root fix is the statement's own meaning: a view declaring no
  fields is a full-width shadow of its owner (promotion: declined — the
  durability is the machinery: the suite and the corpus re-run it in make
  check).
- **"One tick per step boundary" has exactly one honest reading.** The runner
  executes a count of steps; a tick at every non-Failed outcome makes time at
  executed step k equal k — main flow, handler flow, trapping `.word` steps all
  alike. That is what makes mm-counters' re-derivation mechanical (0/1/2/25/51
  at steps 0/1/2/25/51) and the determinism proof trivial (the domain is a pure
  function of the step index by construction, not by argument).
- **instret's genuine count was already in the engine's vocabulary.** The
  trap-END discipline's `frame.trapped` flag IS "the instruction did not
  complete" — a delivered trap, a faulting fetch, a reserved decode. Retired is
  its negation; no new state was needed, and the trap cells in mm-counters
  (gated reads at 13/39) needed no re-derivation because a trap is not a read.

## _(2026-10-05)_ — the experiment that graded its own policy (P4-SYSTEM.4 slice f; the leaf closes)

Execution of the `.4` brief's checkpoint (f) measured:

- **"AccessFault" is a family, not a number.** Decision 6's reasoning — "the
  override declares AccessFault for the atomic kinds, so uniform cause 7 makes
  the cells AGREE" — measured FALSE the first time `a-lrsc-fault` ran under
  Sail: a misaligned LR came back cause 5, and the exception table says why
  ("load and load-reserved instructions generate load exceptions"). The offered
  choice is misaligned (4/6) OR access-fault (5/7), and within access-fault the
  cause follows the access kind. The bind-day uniform-7 was not a legal option
  for LR at all — and the matched experiment is what caught it, exactly the job
  it exists for. The policy is now kind-matched (LR → 5, SC/AMO → 7) everywhere
  the policy is written down: the engine arm, the schema contract, the state
  document, and the decision record with its verbatim mirrors (promotion:
  declined — the durability is the machinery: the a-lrsc-fault guest and the
  comparator re-run it).
- **A declared policy and a platform extern can honestly disagree.** The width
  cell was the leaf's flagged watch item from slice (c) onward, and it measured
  exactly as flagged: Sail's reservation externs take physaddrbits and no width,
  so `sc.d` after `lr.w` matches and stores; the laboratory's declared
  width-equal policy fails with code 1. Both are legal under §12.1.2's latitude
  — the spec's must-fails key on the reservation SET and implementations may
  fail any unconstrained sequence. The verdict is a named divergence, not a
  defect on either side, and the divergence's downstream is consequential (the
  re-converging recovery pair is the corpus's own consistency proof).
- **The flip condition outlived its slice.** The fetch leg's A exclusion,
  written at slice (a) with the M precedent's shape, flipped on its own the
  moment the census declared the A forms — 87 == 87 the day of the bind, no edit
  needed. A check written against the future state it will judge is the
  difference between a mechanism and a to-do list.

## _(2026-10-05)_ — the bind that fit in one commit, and the formatter that graded the manifest (P4-SYSTEM.4 slice e)

Execution of the `.4` brief's checkpoint (e) — the atomic bind — measured:

- **The flip mechanism is load-tested by construction.** The pieces the earlier
  slices staged each landed once: the slot became an extension; the census dual
  edit (schema + `_SCOPE_LISTS` + the scope block + the PARTS family) read 87;
  the fetch leg's slice-(a) exclusion flipped ON ITS OWN the moment the census
  declared the A forms (87 == 87, rv64i unchanged) — the flip condition written
  six days earlier did exactly what it was written to do. The evaluator arms
  ported byte-identically from the scratch proof, so the tracked engine is the
  proven one, and the 88/88 corpus plus the 16/16 cell proof re-ran against the
  tracked build with the same tallies (promotion: declined — the durability is
  the machinery: the gates judge the bound unit on every commit from here).
- **rustfmt is a generator constraint, not a style preference.** The manifest's
  five-fragment list tripped rustfmt's vertical array layout where the
  four-fragment one had stayed inline — measured: 79 chars inline-clean, 90
  broken. A generator that emits code a formatter would rewrite produces drift
  on every regeneration; the emission now decides the layout by construction
  (the 80-char cutoff), and `cargo fmt --check` inside `make check` is the gate
  that arms it.
- **The identity proof is the bind's spine.** 76 pre-bind guests, both CLIs,
  the parent worktree against the post-bind build: 3,468 == 3,468 trace lines,
  `cmp` clean. Additive extensions are supposed to leave the old corpus alone —
  but "supposed to" is a hope and 3,468 lines is a measurement.

## _(2026-10-05)_ — the corpus grades its author four times before it grades the engine once (P4-SYSTEM.4 slice d)

Execution of the `.4` brief's checkpoint (d) measured:

- **A derivation tool that never applies its writes derives a fiction.** The
  spec-side stepper computed every register write into the expectation and
  mutated nothing — so the next instruction read zeros, and the first run
  "completed" every guest in 5-6 steps. Caught at the first `sw`: the step after
  it left the program. The READS-AND-WRITES contract is what makes the fix
  correct by construction: execute reads the pre-instruction file throughout,
  the writes land after the whole effect (promotion: declined — the corpus
  itself re-runs the rule at the bind).
- **The comparison rule is part of the corpus's vocabulary, not a detail.** The
  runner observes register CHANGES, so a register written its own value is no
  observation — the `.3` "x8-already-zero" rule. Eleven of twelve guests failed
  the first run on exactly this (the aq/rl cells' repeated 41s, the handlers'
  repeated CSR reads). The expectations now derive only observable changes.
- **"Reserved" must be checked against the decode table, not remembered.**
  funct5 0x02 is LR's OWN — my "reserved AMO funct5" `.word` decoded as
  `lr.w x6, (x1)` and executed, reading the handler's first word through a
  register the mtvec setup had consumed (the observed `0x342025f3` named it).
  The genuinely reserved 0x05 replaced it; the census that matters is the closed
  set {0x00,0x01,0x04,0x08,0x0C,0x10,0x14,0x18,0x1C} plus LR 0x02 and SC 0x03.
- **A data PA is an allocation, and allocations collide.** The sv39 guest's data
  leaf pointed at base+0x1000 — the ROOT TABLE's page. Cell 3's own store
  overwrote root[0] with 17, turning it into a leaf with R=0, and every later
  walk faulted on schedule. The fix is the honest one (move the data to
  base+0x4000), and the failure mode is now a named audit step: a guest's data
  addresses and its page-table addresses live in one map.
