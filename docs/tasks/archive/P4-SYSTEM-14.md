# P4-SYSTEM ordinary history — part14

Owner: P4-SYSTEM.14 a24 / SEMULITH-P4-0215. Source: `f40ece2b8ae978ebcfa27d71f976eb6414cec196`.

This ordinary Markdown part is outside the closed12-file task-history seal.
The old overview below is historical: its unregistered RV64GC claim was stale
after47cb436; the live overview now follows the registry. Retain it as evidence,
not as a current project claim. No earlier archive or fixed ceiling changes.

## Inverse map

```json
[
  {
    "source": "docs/book/src/models.md",
    "source_bytes": 2621,
    "source_sha256": "caffacb9f80803145f4d2094f04ab4d303ed370c6454df28e499a7c1125c5e86",
    "payload": "model-overview",
    "offset": 0,
    "length": 2621
  },
  {
    "source": "docs/book/src/working/task-trees.md",
    "source_bytes": 18581,
    "source_sha256": "b8f320b4e52d8d8b1257abf9933fd2b2e15fa66764da940e80eb01f3fce4ac55",
    "payload": "completed-book-receipts",
    "offset": 4284,
    "length": 1956,
    "live_replacement": "The complete P4.13 c26a/c28a book receipts remain in ordinary archive14;\nread them through the commands below. Current partition rules remain above.\n\n",
    "new_guide_line": "cat docs/tasks/archive/P4-SYSTEM-14.md\n"
  }
]
```

<!-- BEGIN model-overview bytes=2621 sha256=caffacb9f80803145f4d2094f04ab4d303ed370c6454df28e499a7c1125c5e86 -->
# One definition, one book

Every modelled unit has its own mdBook beside this one, under `docs/models/<unit-id>/` —
the `decision_one-definition-one-book` rule: the unit of modelling is the unit of
documentation. A unit's book is where a reviewer reads **how that unit went from pinned
documents to a running model**: its complete materials bill (generated from the pinned
dossier, gated so a digest cannot rot), what the materials do not contain, the method, the
references and what their agreement is worth, and the evidence with the honest gate
verdict.

Today five units exist:

- **`rv64i-lab-v0`** (kind: processor) — `docs/models/rv64i-lab-v0/`. Build it with
  `mdbook build docs/models/rv64i-lab-v0`, or build every book with `make book`.
- **`dsp56300-lab-v0`** (kind: processor) — `docs/models/dsp56300-lab-v0/`. The bounded,
  EXPERIMENTAL DSP56300 subset: a sibling-crate model, checkpoint-compared against the
  pinned reference — and the unit that pushed the public abstraction past its
  scalar-CPU assumptions (`P3-BREADTH`).
- **`netboard-lab-v0`** (kind: board) — `docs/models/netboard-lab-v0/`. The first board:
  `rv64i-lab-v0` composed with the two devices below, pinning versions not names —
  timers and interrupt controllers absent *by contract* (`P5-BOARD`).
- **`sifive-uart-lab-v0`** (kind: device) — `docs/models/sifive-uart-lab-v0/`. The
  board's serial console: the first device dossier, the one that taught the machinery
  its `device-model` shape.
- **`lan9118-lab-v0`** (kind: device) — `docs/models/lan9118-lab-v0/`. The board's wired
  NIC: the full-scale device dossier — 52 mirrored records, three indexing levels, and
  the guest-readable time sources recorded as composition data.

The device and board books adapt the arc honestly: no encoding or reference chapters'
worth of fiction — a device has no instruction encodings and pins no reference models,
and the fragments say so by declaration.

A sixth directory, `profiles/rv64gc-lab-v0/`, exists at the **resolution stage**
(`P4-SYSTEM.1`): the Linux-capable profile's selection is exact and citable, but its
definition pipeline has not started — it is deliberately unregistered, and a book
arrives with its registration day.

The wiring is a gate, not a habit: the `UNIT-BOOKS` doctrine
(`scripts/check_unit_books.sh`) enumerates the registered units from
`materials/units.sexp` — the one registration place — and fails the commit if a unit lacks
its book, if a book does not build, or if a book under `docs/models/` belongs to no
registered unit. Adding a profile without its book fails the gate.
<!-- END model-overview -->

<!-- BEGIN completed-book-receipts bytes=1956 sha256=8ea84ea70fe8b83cd22315025ec463abb388e94490ec913c64ad703b0dac5a29 -->
P4.13 c26a applies the same discipline to the task tree itself. At 123,960 bytes,
the live tree had 7,112 bytes of room under its fixed 131,072-byte part ceiling.
Six completed spans totaled 81,532 bytes; archive 8 already held 59,436, so those
payloads could not fit there. [Archive 9](#read-task-history)
retains all six payloads in source order with individual byte lengths and SHA256
markers, including older log rows in their original context. It is 83,418 bytes
with wrappers; the live partition is 45,205 bytes before the new receipt.

The verification extracts each marked payload, removes only new live routing,
ownership and receipt text, and reconstructs the committed source from 5eaef2a:
123,960 bytes, SHA256
`efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac`.
Earlier archive parts and all retained source segments are byte-exact. The
frontier, census and next action stay live; feature examples remain in their
book chapters. Neither the task-family nor per-part cap grows, and this move
adds no CPU-contract credit.

P4.13 c28a repeats the whole-entry proof for development notes. Source `5daa7bb`
holds 23 entries/47,951 bytes, only 1,201 bytes below the fixed 49,152-byte cap.
The published sharder targets 30,000 bytes: sixteen entries remain in 29,706
bytes; seven oldest entries move as an exact 18,245-byte suffix into shard 0225
(18,478 bytes including its wrapper). Remove only the new receipt/navigation
footer and concatenate the retained prefix and archived suffix to reconstruct
the source, SHA256
`6d0ccb9383365685023d20543138f1e47735360257fe1fb9fe9560e91ecb70c3`.
The earlier manifest rows and sealed history stay byte-exact, and no bound grows.
At that checkpoint the next evidence question was the public Sail override's
contained-versus-crossing AMO granule behavior. C28b subsequently qualified it;
the [memory chapter](../plan/p4/contract-memory.md) retains that result and its
wrong-granule control.



<!-- END completed-book-receipts -->

