# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; planning package v0.2
  is the design input, `ROADMAP.md` is the plan. No CPU code exists yet.
- **Active trees:** `MODEL-METHOD` (1 of 6) and `MODEL-BOOKS` (0 of 6).
- **Frontier leaf:** `MODEL-METHOD.2` — the materials requirement schema and catalogue.
- **Next action:** `MODEL-METHOD.2`. `docs/INFORMATION_CATALOG.md` states *what must be known* to
  model a processor in 24 categories (C01–C24) plus DSP questions in §5. Nothing states **which
  material supplies each**, nor which are supplied by **nothing**. Build the record type binding
  category → material → disposition (`covered` / `missing` / `not-applicable` **with reason**),
  as JSON Lines under a JSON Schema so `RECORD-SCHEMA` and the tracked validator apply. Then `.3`
  censuses `rv64i-lab-v0`, `.4` acquires what is missing and reachable (including: does the
  specification **PDF** carry the encoding tables as text?), `.5` writes the method in prose, and
  `.6` mechanizes *no coding without the source of truth*.
- **Format decision (mine, recorded in the tree):** JSON Lines + JSON Schema, not S-expressions —
  the data is records, not trees, and the repo already gates JSONL. S-expressions are parked for
  the canonical *executable semantics* in `P1-LAB`, with a stated trigger.
- **Just closed:** `P0-PROFILE` 10/10. Gate `G0` run, verdict **`incomplete`** (68 declared
  checks, 0 implemented — the deliverable, not a failure). ⛔ Reopened for `.10` after a measured
  defect the first nine leaves carried: the profile was matched on its **instruction set and not
  its platform**, so the reference kept a core-local interruptor a guest could read `mtime` from
  with a plain load. Corrected at source; held by the negative fixture `guest-no-device.s`.
  Spike's platform is **not** matchable and that is enumerated (`DIFF-PLATFORM-SPIKE`).
- **Then:** `P1-LAB.1` — the crate skeleton; where the 68 declared checks acquire fixtures.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-MM-0033 (leaf MODEL-METHOD.1)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
