# CHANGELOG shard — SEMULITH-PD-0050 … SEMULITH-PD-0050

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-PD-0050 (leaf PUSH-DISCIPLINE.2) — full CI runs BEFORE the push, at the boundary

- The named full local suite: `make ci` = `check` (CI's rust.yml) + `gate` (CI's
  doctrines.yml) + `bench` + `smoke-bench` + `book` — matching the server workflows and
  consciously exceeding them with the bench and the books; the live three-way smoke is
  excluded with the reason recorded (it needs the untracked, network-acquired reference
  binaries — its standing as not-a-commit-gate). The membership is named in the Makefile
  comment, the hook's output, COMMIT.md, and the green-run record.
- `.githooks/pre-push` now execs `scripts/pre_push.sh`: cadence FIRST (a refused push
  never burns the suite), then `make ci` on BOTH paths (a director-approved push is not an
  unverified one), then the green-run record at `target/push/last-green.txt` (+ `.log`) —
  untracked, on-volume, overwritten per green run; explicitly NOT `.3`'s tracked
  append-only approval record. A red suite refuses, naming the failing leg from make's own
  error line. The cadence number stays in `check_push_cadence.sh` alone.
- Acceptance (d): fired RED by a deliberately broken check — the self-test's broken-suite
  arm refuses and writes NO green record; a red run after a green one does not overwrite
  the last green record; the cadence refusal leaves the suite's marker absent. Self-test
  9/0 in scratch repos with a real bare upstream (the `.1` pattern). On this repository
  the hook refuses cadence-first at 115/300, the suite unburned.
- No new doctrine (the boundary is a hook, not a commit gate — PUSH-CADENCE stays the
  registered one; decision recorded in the leaf). COMMIT.md's Pushing section documents
  the two-question boundary; TOOLBOX.md gains the two rows.
- `make ci` green end to end; `make gate` all green (27 doctrines / 291 arms).
  `PUSH-DISCIPLINE.3` (the approval record) is next.

