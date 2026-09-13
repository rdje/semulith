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
- **Active tree:** `MODEL-BOOKS` (0 of 6 leaves), now unblocked.
- **Frontier leaf:** `MODEL-BOOKS.1` — the book structure and the complete materials bill.
- **Next action:** `MODEL-BOOKS.1`. One mdBook per processor model at `docs/models/<profile-id>/`:
  the complete materials list (every specification artifact, encoding table, reference model and
  internal contract, pinned by exact identity, GENERATED from `sources.toml`/`references.toml` so
  a digest cannot rot) and the methodology that turned those documents into the model. Prose
  first; tables only where a list is the honest form.
- **Just closed:** `P0-PROFILE` 10/10. Gate `G0` run, verdict **`incomplete`** (68 declared
  checks, 0 implemented — the deliverable, not a failure). ⛔ Reopened for `.10` after a measured
  defect the first nine leaves carried: the profile was matched on its **instruction set and not
  its platform**, so the reference kept a core-local interruptor a guest could read `mtime` from
  with a plain load. Corrected at source; held by the negative fixture `guest-no-device.s`.
  Spike's platform is **not** matchable and that is enumerated (`DIFF-PLATFORM-SPIKE`).
- **Then:** `P1-LAB.1` — the crate skeleton; where the 68 declared checks acquire fixtures.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0031 (leaf P0-PROFILE.10)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
