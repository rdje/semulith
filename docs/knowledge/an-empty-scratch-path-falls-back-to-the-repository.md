# My self-test could not create its scratch directory — what does the rest of it do?

**Whatever its commands do in the caller's directory, unless the self-test stops.** A shell
self-test that writes `t="$(mktemp -d …)"` and never checks the result carries on with `t=""`.
Most commands then aim at `/…` and fail harmlessly, but two forms fall back to where the check
runs, which is the real repository: `git -C "$t"` (git documents that `-C ""` leaves the
directory unchanged) and `cd "$t"` (bash treats `cd ""` as no move).

## What happened

On 2026-10-24, while measuring the bash `PUSH-RECORD` driver before its port (`XTASK.6` slice
`6e`), a failure-injection run made `target/doctrine-selftest` unwritable to observe the
"self-test cannot run" refusal. The driver's self-test builds a scratch git repository with
`git -C "$t" init`, `config user.email t@t`, `config user.name t`, `add -A` and
`commit -m base`. With `t=""` every one of those ran against the real repository: the local
config gained a `[user]` section (`t <t@t>`), the two modified task-tree files were staged, and
`git commit` started the real pre-commit gate. Nothing announced it: the main run had sent the
self-test's output to `/dev/null`.

It was stopped about ten minutes in, before the gate finished: the process tree was killed
(children included), and the state was restored and verified:

- no commit was made (`git log -1` still `922a1dbd`); no `.git/index.lock` was left;
- the `[user]` section was the last in `.git/config`, so git had appended it; it was removed,
  and the identity is again the global one every recent commit carries;
- the index was unstaged back to clean (`git diff --cached --quiet`); `.git/hooks` untouched.

## How to catch it, and what to do

- **Before firing a failure-injection probe, read the code path the failure drives.** The
  probe was reasonable for the four drivers measured before it; for this one it handed an
  empty path to `git -C`.
- **Guard every scratch allocation:** `t="$(…)" || return 1; [ -n "$t" ] && [ -d "$t" ] || return 1`.
  The Rust doctrine modules (`xtask/src/harness.rs`, `scratch`) return an error and the
  self-test stops before any command runs.
- **Look for the two fallback forms:** `grep -nE 'git -C "\$t"|cd "\$t"'` across the drivers
  whose scratch assignment is unguarded. On 2026-10-24 that found `check_push_record.sh`
  (ported in `6e`), `check_seam_integrity.sh` (`cd "$t" && git init -q . && git add leaf.md`)
  and `check_contract_freeze.sh` (`cd "$t" && judge "$t"`).

Evidence: `docs/tasks/XTASK.md` (slice `6e`, the defect owned mid-slice); target/xtask/xt0009.

## The same class through a link (2026-10-26)

A fixture directory may hold a **link into the real tree** (`check_requirements.sh` links `$t/schema` to
the real `schema/` so fixtures validate against the real schemas). A path through that link is a real
path: `rm -f "$t/schema/credits.sexp"` in a new self-test arm deleted the tracked `schema/credits.sexp`.
The token-facet probe's closed inventory caught it (`24 != 25`); the culprit was isolated by running each
suspect alone and checking the file after each, and the file came back from git. Before writing into or
removing under any fixture subpath, read how the fixture was built: `grep -n "ln -s" <driver>`.

## Guarded at the source (2026-10-26, `XTASK.6` slice `6f`)

The form was the scaffold's, not two drivers': `grep -lF 't="$(SELFTEST_TMP)"' scripts/*.sh` found 32
bash drivers, every allocation unchecked. Each now reads
`t="$(SELFTEST_TMP)" && [ -n "$t" ] && [ -d "$t" ] || { echo "<DOCTRINE> self-test: cannot create a scratch
directory under target/doctrine-selftest" >&2; return 1; }` — the Rust modules' wording — so with the
directory unwritable the `--self-test` run names the cause and the main run refuses before the first
fixture command. The scan widened to the link form (`grep -nE 'git -C "\$t"|cd "\$t"|ln -s'`) found 14
fallback-form lines in 6 drivers, none reachable past the guard; measured with the directory at mode 500
and `.git/config`, HEAD, the index and `schema/` verified unchanged. A new driver copies the guarded line,
not the bare one. Evidence: `docs/tasks/XTASK.md` slice `6f`; target/xtask/xt0010.
