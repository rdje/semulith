# Closed task-trees — the completed-tree register

The `docs/TASK_TREE.md` index holds one row per OPEN tree; a tree whose Metadata status
becomes `done` moves its row here, verbatim, in the commit that closes it (the index's
registered pressure control: "completed trees leave the index" — `LIVE-CONTAINMENT.1`). A
reopened tree moves back. Each row keeps the outcome summary it closed with; the tree file
under [`tasks/`](tasks/) stays the authority. FRONTIER-SYNC gates this register like the
index: every tree has exactly one row, a row's status and leaf counts are re-derived from the
tree, and an open tree here — or a completed one there — is a breach.

<!-- ANCHOR: closed -->
| Tree | Status | Outcome | Owner |
| --- | --- | --- | --- |
| [`SEMULITH-TREES`](tasks/SEMULITH-TREES.md) | `done` | — (4/4 leaves complete) | repo-local |
| [`P0-PROFILE`](tasks/P0-PROFILE.md) | `done` (reopened once, for `.10` — a measured defect the first nine leaves carried) | — (10/10 leaves complete) | repo-local |
| [`P1-LAB`](tasks/P1-LAB.md) | `done` (reopened once, for `.13` — the `.11` allocation figures had to be proven, not reported) | — (13/13 leaves complete; gate G1 RUN, verdict `incomplete` — criterion 6 routed to the P2-SCALAR tree) | repo-local |
| [`P2-SCALAR`](tasks/P2-SCALAR.md) | `done` | — (9/9 leaves complete; the CPU-LAB report reads `incomplete` with G-CONTRACT/G-OBLIGATIONS named — the release decision is the EXPERIMENTAL release of the versioned artifact, `decision_release-rv64i-lab-v0`) | repo-local |
| [`DSP-REVIEW`](tasks/DSP-REVIEW.md) | `done` | — (8/8 leaves complete; six findings routed to P3-BREADTH's first leaf, each with its ROUTING EVIDENCE — none reproduces on the scalar profile) | repo-local |
| [`P3-BREADTH`](tasks/P3-BREADTH.md) | `done` | — (8/8 leaves complete; gate `BREADTH` RUN `2026-10-01`, verdict **`passed`** — the capability report published at `docs/BREADTH-REPORT.md`) | repo-local |
| [`MODEL-COMPOSE`](tasks/MODEL-COMPOSE.md) | `done` | — (6/6 leaves complete; a composition is a verdict, a discharge, and a materializable unit) | repo-local |
| [`MODEL-METHOD`](tasks/MODEL-METHOD.md) | `done` (reopened once, for the per-kind chapter) | — (19/19 leaves complete; the demand chapter landed and is a LIVE chapter `2026-10-01`) | repo-local |
| [`MODEL-BOOKS`](tasks/MODEL-BOOKS.md) | `done` | — (8/8 leaves complete; the per-unit book structure, the five-chapter arc, and the `UNIT-BOOKS` gate — every registered unit has a book that builds) | repo-local |
| [`SOT-FORMAT`](tasks/SOT-FORMAT.md) | `done` | — (10/10 leaves complete; the `SOURCE-FORMAT` gate registered, the format split cannot return) | repo-local |
| [`PUSH-DISCIPLINE`](tasks/PUSH-DISCIPLINE.md) | `done` | — (3/3 leaves complete; the cadence, the named suite at the boundary, and the append-only approval record gated by `PUSH-RECORD`) | repo-local |
| [`DOC-SHARDING`](tasks/DOC-SHARDING.md) | `done` | — (2/2 leaves complete; both append heads shard into `docs/changelog/` under one frozen manifest) | repo-local |
| [`PORT-WEB`](tasks/PORT-WEB.md) | `done` | — (1/1 leaves complete; the crate skeleton builds for `wasm32-unknown-unknown` from its first slice, gated by `PORT-WEB`) | repo-local |
| [`UPSTREAM-TRACK`](tasks/UPSTREAM-TRACK.md) | `done` | — (4/4 leaves complete; age and exposure derived by command, `blocks` gated, the tree closed) | repo-local |
| [`BOOK-APPARATUS`](tasks/BOOK-APPARATUS.md) | `done` | — (2/2 leaves complete; the index landed generated + gated by `BOOK-INDEX`, and the first reading-experience audit pass revised 13 of the 29 main-line chapters — the yield was factual drift) | repo-local |
| [`MEMORY-POINTER`](tasks/MEMORY-POINTER.md) | `done` | — (1/1 leaves complete; MEMORY.md is the §6 next-action pointer per the director's `2026-10-02` ruling — 34/7,031 → 29/1,865) | repo-local |
| [`MCU-DOCS`](tasks/MCU-DOCS.md) | `done` | — (2/2 leaves complete; the twelve answers reconciled same-day — twelve MCU documents adopted and digest-verified into `.materials/mcu/`) | repo-local |
| [`PREFIX-DISCIPLINE`](tasks/PREFIX-DISCIPLINE.md) | `done` | — (1/1 leaves complete; the SEMULITH- prefix pinned in `commit-msg`, watched behaviourally by `COMMIT-PREFIX` #29 — history keeps both spellings, immutably) | repo-local |
| [`ROADMAP-V3`](tasks/ROADMAP-V3.md) | `done` | — (3/3 leaves complete; consumed by the v0.4 revision at P1 first slice) | repo-local |
| [`MIRROR-DRIFT`](tasks/MIRROR-DRIFT.md) | `done` (reopened once, for `.4` — a mirror class the first three leaves did not cover) | — (4/4 leaves complete) | repo-local |
| [`SEMULITH-PKG`](tasks/SEMULITH-PKG.md) | `done` | — (9/9 leaves complete) | repo-local |
| [`BOOTSTRAP`](tasks/BOOTSTRAP.md) | `done` | — | repo-local |
<!-- ANCHOR_END: closed -->
