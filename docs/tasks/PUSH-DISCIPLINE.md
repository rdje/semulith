# PUSH-DISCIPLINE: how work leaves this machine

## Metadata

- Tree ID: `PUSH-DISCIPLINE`
- Status: `active`
- Roadmap lane: cross-cutting; the discipline spine's outward boundary
- Gate: contributes `PUSH-CADENCE` — a push happens on cadence, or with the director's approval
- Depends on: nothing; the hooks are already installed (`core.hooksPath=.githooks`)
- Unlocks: a durable answer to "may this leave the machine, and who said so"
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Push is the one act in this project that is **outward-facing and irreversible in effect** — bytes
reach a server, and a server may keep, cache or index them whatever happens locally afterwards.
Make it a governed act rather than a judgement call.

Director instruction, `2026-09-14`: *"Set the push cadence to every 300 commits. Exceptional push
happen from time to time, but they shall require my approval."*

⛔ Measured before writing a line: `COMMIT.md` — the normative commit workflow — **says nothing
about pushing at all** (`grep -i push COMMIT.md` → 0 hits), and no `pre-push` hook exists. The
policy did not exist to be broken; it did not exist at all.

## Non-Goals

- Not a mirror of the commit workflow. Committing is routine and local; pushing is neither.
- Not an attempt to make the cadence unenforceable-by-hand. A human with `git push --no-verify` can
  always proceed; the gate exists so that doing so is **deliberate and visible**, never accidental
  and never something an agent does on its own reading of the situation.
- Not a release process. Tagging, versioning and publication are separate and not in scope here.

## Acceptance Criteria

1. The cadence is **one number in one place**, and any document restating it is checked against
   that place rather than trusted.
2. A push below cadence is **refused by a hook**, with the refusal naming exactly what makes it
   permissible — approval — and how to supply it.
3. An approved push records **who approved it and for what reason**, so the exception is auditable
   after the fact rather than indistinguishable from a routine push.
4. The instrument states the current distance honestly when there is no upstream, no network, or a
   detached HEAD — refusing rather than guessing.

## Task Tree

- ID: `PUSH-DISCIPLINE.1` — **the cadence, mechanized at the push boundary**
  Status: `done`
  Goal: a `pre-push` hook and a tracked instrument. Below cadence and without approval, the push is
  refused; the refusal explains the two ways forward.
  Acceptance: cadence is 300 and lives in exactly one place; `COMMIT.md` states it and a self-test
  arm proves the two agree; the hook refuses a below-cadence push and permits an approved one;
  ≥ 8 arms fired RED before the hook is trusted; the instrument refuses on no-upstream and on
  detached HEAD rather than reporting a number it cannot know.
  Verification: `11 pass / 0 fail`, 3 fired RED first; the gate refuses on this repository at 45 of
  300 and names both ways forward.
  Commit: `SEMULITH-PD-0046`

- ID: `PUSH-DISCIPLINE.2` — **full CI runs on the wrong side of the push boundary**
  Status: `done` (`2026-09-29`)
  Goal: Policy 16 says full CI runs **before** a push and selected checks for ordinary commits.

  GAP CENSUS, measured `2026-09-14` — the claim is not "nothing checks this", because something
  does; it is that the check sits **after** the act it is supposed to authorise:

  ```
  $ ls .github/workflows/            ->  doctrines.yml  rust.yml
  $ grep -A3 '^on:' .github/workflows/doctrines.yml
    on:
      push:                          <- runs AFTER the bytes have reached the server
      pull_request:
  $ grep -oE 'check_[a-z_]+\.sh' .githooks/pre-push   ->  check_push_cadence.sh   (cadence only)
  $ grep -nE '^(ci|check):' Makefile                   ->  20:check:              (no `ci:` target)
  ```

  So the full suite runs *on* push, server-side, and locally there is a `check` target but no `ci`
  one. A red CI run after a push tells you what you already shipped. ⚠️ And the pre-push hook this
  tree just added is the natural place to fix it, which is why it is the next leaf rather than a
  separate tree.
  Acceptance: a push runs the full local suite or is refused; the suite that runs is **named**, not
  implied; a green run is recorded with what it covered and when, so the next push can say what was
  verified rather than assume; fired RED by a deliberately broken check.
  Design (recorded before code, `2026-09-29`):
  - **The named suite** is `make ci` = `check` + `gate` + `bench` + `smoke-bench` +
    `book` — the server CI's content (`rust.yml` = check; `doctrines.yml` = gate) plus the
    browser bench and both books, all local, deterministic, no network. EXCLUDED, with the
    reason recorded: the live three-way smoke (`run_semulith_smoke.py`) needs the
    untracked, network-acquired reference binaries under `target/refs/` — the same
    not-a-commit-gate standing it already has. The membership is NAMED in the Makefile
    comment, the hook's output, COMMIT.md, and the green-run record.
  - **The hook**: `.githooks/pre-push` execs a new tracked instrument,
    `scripts/pre_push.sh`, which (1) runs the cadence gate FIRST (a refused push never
    burns the suite), (2) runs `make ci` on BOTH paths (cadence push and
    director-approved push alike), naming the failing leg on refusal, and (3) writes the
    green-run record. The cadence number stays in `check_push_cadence.sh` alone.
  - **The green-run record** lives at `target/push/last-green.txt` (+ `last-green.log`):
    untracked, on-volume, overwritten per green run — it answers "what did the last green
    pre-push run cover, and when" without git archaeology, and it is NOT the tracked
    append-only approval record (that is `.3`'s artifact, a different thing).
  - **No new doctrine.** The boundary behavior is a hook, not a commit gate;
    PUSH-CADENCE stays the registered doctrine. `pre_push.sh` carries its own
    `--self-test` (scratch repos with a stub Makefile; the cadence leg exercised through
    a real bare upstream, the `.1` pattern) — the deliberately-broken-check RED is one of
    its arms, recorded in the verification log.
  - **RED demonstration (acceptance d):** the self-test's broken-suite arm (a scratch
    `ci` target that fails) → refusal naming the failing leg, and NO green record
    written; plus the never-burns-the-suite arm (cadence refusal leaves the suite's
    marker absent).
  Result: met, `2026-09-29`. **The full local suite runs at the pre-push boundary, on both
  paths, before any bytes leave.** The suite is NAMED: `make ci` = `check` (CI's rust.yml)
  + `gate` (CI's doctrines.yml) + `bench` + `smoke-bench` + `book` — matching the server
  workflows and consciously exceeding them with the bench and the books; the live
  three-way smoke is excluded with the reason recorded (it needs the untracked,
  network-acquired reference binaries — the not-a-commit-gate standing it already has).
  `.githooks/pre-push` now execs `scripts/pre_push.sh`: (1) the cadence gate FIRST (a
  refused push never burns the suite — measured: the cadence refusal leaves the stub
  suite's marker and the record absent), (2) `make ci` on both paths (cadence push and
  director-approved alike), a red suite refusing with the failing leg NAMED from make's
  own error line and the log pointed at, (3) the green-run record at
  `target/push/last-green.txt` (+ `.log`) — untracked, on-volume, overwritten per green
  run, answering "what did the last green run cover and when" without git archaeology;
  explicitly NOT `.3`'s tracked append-only approval record. The cadence number stays in
  `check_push_cadence.sh` alone; COMMIT.md's Pushing section documents the two-question
  boundary. Acceptance (d): fired RED by a deliberately broken check — the self-test's
  broken-suite arm (a scratch `ci` target that fails) refuses, names the leg, and writes
  NO green record; and a red run after a green one does NOT overwrite the last green
  record. Self-test 9/0 in scratch repos with a real bare upstream (the `.1` pattern).
  No new doctrine: the boundary is a hook, not a commit gate — PUSH-CADENCE stays the
  registered doctrine; recorded here per the leaf's own design. One authoring defect,
  mine: `local record_dir=… log="$record_dir/…"` in one declaration tripped `set -u`
  (the second assignment reads the first before it exists) — 3/6 became 9/0 after the
  split. Exercised on this repository: the hook refuses cadence-first at 115/300, both
  routes named, the suite unburned.
  Lessons: `promotion: declined (the set -u ordering slip is fixed in the script; the record's shape is documented in it)`.

- ID: `PUSH-DISCIPLINE.3` — **the approval record**
  Status: `pending`
  Goal: an exceptional push leaves a durable trace — who approved, when, why, and what range of
  commits it covered — so "exceptional" can be audited rather than asserted.
  Acceptance: the record is tracked, append-only, and written by the same act that permits the push,
  never afterwards from memory.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `PUSH-DISCIPLINE.3` | `pending` | the audit trail is only worth building once exceptions can actually occur — and the boundary now runs the suite on both paths (`.2`), so an exception is a real, recorded act |

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| `2026-09-14` | Cadence is 300 commits since the last push | director instruction |
| `2026-09-14` | An exceptional push requires the director's approval, supplied explicitly | director instruction; the hook cannot judge whether an exception is warranted, and neither can an agent |
| `2026-09-14` | The gate refuses rather than warns | a warning at an outward-facing boundary is a warning that gets read after the bytes have left |
| `2026-09-14` | The cadence number lives in the instrument; documents that restate it are checked | the same no-duplicated-fact rule the canonical definition uses |

## Open Questions

- Should the cadence count **commits** or **leaves completed**? Commits today, because that is what
  the director said and what git can count without interpretation.
- ⚠️ 45 commits currently exist only on this disk, and cadence 300 means they stay there for a long
  while. That is the director's deliberate call, made with the exposure stated. Recorded here so it
  is a decision on the record rather than an oversight nobody revisits.

## Blockers

- None.

## Acceptance Checklist (leaf `PUSH-DISCIPLINE.2`)

- [x] **REPRODUCE / ISSUE** — the gap census the leaf already carried, re-measured at the
  pre-leaf state: the workflows run `on: push` (server-side, after the bytes), the pre-push
  hook ran cadence only, and no `ci` target existed:

  ```
  $ git show HEAD~0:Makefile | grep -c '^ci:'   # before this leaf's Makefile edit
  0
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: Policy 16's pre-push half was never wired;
  WHERE, measured at the pre-leaf state:

  ```
  $ git show HEAD~0:.githooks/pre-push | grep -c 'check_push_cadence'   -> 1 (cadence only)
  $ git show HEAD~0:Makefile | grep -c '^ci:'                           -> 0 (no ci target)
  $ grep -c '^on:' .github/workflows/rust.yml .github/workflows/doctrines.yml  -> 1, 1 (on push)
  ```

  The suite membership decision: match the server workflows (`rust.yml` = check,
  `doctrines.yml` = gate) and consciously exceed them (`bench`, `smoke-bench`, `book` —
  all local, deterministic, no network); exclude the live three-way smoke (it needs the
  untracked, network-acquired reference binaries — the standing it already has).

- [x] **FIX** — the `ci` target (membership named in the Makefile comment);
  `scripts/pre_push.sh` (cadence first → the named suite on both paths → the green
  record at `target/push/last-green.txt`, refusal naming the failing leg from make's own
  error line); `.githooks/pre-push` execs it; COMMIT.md's Pushing section documents the
  two-question boundary; TOOLBOX.md gains the two rows. The cadence number never moved
  from `check_push_cadence.sh`.

- [x] **ADDRESSED (verified)** — the self-test, incl. acceptance (d)'s deliberately
  broken check, and the suite itself:

  ```
  $ bash scripts/pre_push.sh --self-test
  PRE-PUSH self-test: 9 pass / 0 fail
    (RED the cadence refusal comes FIRST — never burns the suite;
     RED approved + deliberately broken suite → refusal names the leg, no record;
     RED a red run after a green one does NOT overwrite the last green record;
     GREEN approved + green suite → permitted, the record names commit + membership)
  $ make ci
  ci: all legs green (check, gate, bench, smoke-bench, book)
  $ printf '' | bash .githooks/pre-push          # the hook's real path, this repository
  PUSH-CADENCE: REFUSED — 115 commits since the last push; … rc=1   (the suite unburned)
  ```

- [x] **NO REGRESSION** — no push was attempted at any point; committing is unaffected
  (this commit passed the pre-commit enforcer); the cadence self-test unchanged:

  ```
  $ bash scripts/check_push_cadence.sh --self-test -> PUSH-CADENCE --self-test: 11 pass / 0 fail
  $ make gate
  === all doctrines green ===          (27 doctrines / 291 self-test arms, re-derived)
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (PUSH-DISCIPLINE 2/3), `LIVE_STATUS.md`,
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.3`), this tree,
  COMMIT.md, TOOLBOX.md, the Makefile.

## Acceptance Checklist (leaf `PUSH-DISCIPLINE.1`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: nowhere, and that is the finding. Measured
  before writing anything:

  ```
  $ grep -ci push COMMIT.md          ->  0     the normative commit workflow never mentions pushing
  $ ls .githooks/                    ->  commit-msg  pre-commit     (no pre-push)
  $ git rev-list --count origin/main..HEAD  ->  45
  ```

  WHY it matters: a commit is local and reversible, a push is not. 45 commits of work had exactly
  one governance rule between them and a server — a human remembering. ⛔ And the specific failure
  to guard against is an **agent** deciding on its own that a given push is surely fine, which is
  the reading any assistant asked to "finish up" would naturally reach.

- [x] **ADDRESSED (verified)** — leg 2. `scripts/check_push_cadence.sh` holds the number (300) and
  `.githooks/pre-push` refuses below it. On this repository right now:

  ```
  $ bash scripts/check_push_cadence.sh --status ; echo $?
  PUSH-CADENCE: REFUSED — 45 commits since the last push; the cadence is 300, so this push is
  EXCEPTIONAL and needs the director's approval.
    Two ways forward, and only two:
      1. Wait. The cadence is 300 commits; this is 45.
      2. Ask the director. … SEMULITH_PUSH_APPROVED='<the director's reason>' git push
    ⛔ An agent may not supply this on its own judgement. The exception is the
       director's to grant; the variable only carries it.
  1
  ```

  11 arms, and the ones that matter are RED — each runs in a throwaway repository with a real
  upstream, because a gate about distance-from-upstream cannot be tested without one:

  ```
  ok  RED   1 commit ahead is still below cadence          ok  RED   an EMPTY approval is not an approval
  ok  RED   the refusal names BOTH ways forward            ok  RED   a detached HEAD refuses rather than reporting a distance
  ok  RED   the refusal names the approval variable        ok  RED   a branch with no upstream refuses rather than guessing
  ok  RED   the refusal forbids an agent supplying approval itself
  ok  GREEN an approved push is permitted                  ok  GREEN the approval RECORDS the reason given
  ok  GREEN COMMIT.md states the same cadence (300) as this script
  PUSH-CADENCE --self-test: 11 pass / 0 fail
  ```

  ⛔ Three of those arms were **fired RED first and failed**: two because the refusal message
  wrapped across a newline so a literal match missed it, and one because `COMMIT.md` did not yet
  state the cadence. The last is the no-duplicated-fact arm doing its job before the fact existed.

  ⛔ The instrument refuses on `DETACHED`, `NO-UPSTREAM` and `NOT-A-REPO` rather than printing a
  distance it cannot know — "0 commits ahead" for a detached HEAD is a lie that *permits* a push.

- [x] **NO REGRESSION** — leg 3. The hook is new and touches only `git push`, which this project
  has never run. Committing is unaffected — this commit passed the pre-commit enforcer:

  ```
  $ bash scripts/check_doctrines.sh   ->  all doctrines green
  ```

- [x] **LOCKSTEP** — `COMMIT.md` gains the `Pushing` section it never had, stating the cadence and
  the approval route; `TOOLBOX.md` gains the instrument row;
  [`decision_push-cadence`](../decisions/decision_push-cadence.md) records the policy, the reason a
  push is governed differently, and **the accepted exposure** — 45 commits on one disk, on the
  record as a decision rather than an oversight.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-29` | `PUSH-DISCIPLINE.2` | the gap census re-measured at HEAD | `ci:` target absent from the Makefile; the workflows run `on: push`; the hook ran cadence only |
| `2026-09-29` | `PUSH-DISCIPLINE.2` | `scripts/pre_push.sh --self-test` (scratch repos, a real bare upstream, a stub Makefile) | 9 pass / 0 fail — incl. acceptance (d)'s deliberately broken check (the refusal names the leg, no green record written) and the never-burns-the-suite arm |
| `2026-09-29` | `PUSH-DISCIPLINE.2` | `make ci` | all legs green: check, gate (27 doctrines), bench, smoke-bench (44 arms), book (both books) |
| `2026-09-29` | `PUSH-DISCIPLINE.2` | the hook's real path on this repository (direct invocation, no push) | cadence-first refusal at 115/300, both routes named, the suite never ran |
| `2026-09-29` | `PUSH-DISCIPLINE.2` | `check_push_cadence.sh --self-test`; `make gate` | 11/0 (unchanged); all doctrines green |
| `2026-09-14` | `PUSH-DISCIPLINE.1` | does any push policy exist today? | `grep -ci push COMMIT.md` → 0; no `pre-push` hook |
| `2026-09-14` | `PUSH-DISCIPLINE.1` | `--self-test`, first run | `8 pass / 3 fail` — 2 wrapped messages, 1 undocumented cadence |
| `2026-09-14` | `PUSH-DISCIPLINE.1` | `--self-test`, after the fixes | `11 pass / 0 fail` |
| `2026-09-14` | `PUSH-DISCIPLINE.1` | the gate on this repository | REFUSED at 45 of 300, `exit=1`, both routes named |
| `2026-09-14` | `PUSH-DISCIPLINE.1` | detached HEAD / no upstream | refuses; never prints a distance it cannot know |
| `2026-09-14` | `PUSH-DISCIPLINE.1` | `COMMIT.md` cadence vs the script's | 300 == 300, checked by the script itself |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `PUSH-DISCIPLINE.2` | `SEMULITH-PD-0050 (leaf PUSH-DISCIPLINE.2): …` | the named full local suite (`make ci`) runs at the pre-push boundary on both paths, cadence-first; the green-run record at `target/push/last-green.txt`; fired RED by a deliberately broken check (self-test 9/0); no new doctrine (a hook, not a commit gate) |
| `PUSH-DISCIPLINE.1` | `SEMULITH-PD-0046 (leaf PUSH-DISCIPLINE.1): the push boundary gets a gate that refuses` | 11 arms, 3 fired RED first; 45 of 300 |

## Changelog

- `2026-09-14`: Created on a director instruction setting the push cadence. Measured first: the
  repository had no push policy and no `pre-push` hook, so this is a gap being closed rather than a
  rule being tightened.
- `2026-09-29`: Leaf `.2` done: the named full local suite (`make ci` = check + gate + bench +
  smoke-bench + book — the server workflows' content plus the bench and the books; the live
  smoke excluded with its reason) runs at the pre-push boundary on BOTH paths, cadence-first;
  a red suite refuses naming the failing leg; a green one leaves `target/push/last-green.txt`.
  Fired RED by a deliberately broken check (self-test 9/0). COMMIT.md's Pushing section now
  documents the two-question boundary.
