# DEV_NOTES shard — _(2026-10-11)_ … _(2026-10-11)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-11)_ — fail closed on unavailable handoff census (P4-SYSTEM.14 a42i)

D47: actual sandbox denies ps spawn with EPERM, but the parent handoff script
suppresses stderr, ignores failed capture and judges its empty process snapshot
as green. Host-view ps/lsof both rc=0 with empty stderr. Director authorizes
stopping idle Kimi; subsequent absence is recorded, no new sanctioned exemption.
The defect concerns inability to judge process state, not an unproved CPU result.

Capture each host tool's exit/status, separate stderr and nonempty stdout before
using its snapshot. Any failed command, reported stderr, or empty/whitespace-only
output returns2 without handoff OK. Retain original lsof-before-ps ordering and
every successful parser/classifier/ancestry/advisory/sanctioned rule; no lexical
process-name detector or extra exemptions. Owned mktemp stderr file is on the
repository volume, mode/creation owned by mktemp, EXIT cleanup and HUP/INT/TERM handlers. Normal/refusal
and TERM cleanup paths are verified. No claim of SIGKILL cleanup or detection
of silent host restrictions, other-uid jobs, or processes invisible to published
handle/command rules. Full host visibility remains the signoff requirement.

Old fixed40-line help stops before Usage/exit contract. Extract the complete
comment header and reject surplus arguments under the published single-option
syntax. These are narrow existing CLI-contract repairs. User-facing book explains
0/1/2, host visibility, read-only handles, advisories/authority and synthetic CI.
Current teaching revised within the fixed aggregate cap; historical crash-recovery
receipt remains byte-exact. README/make help reflect the same gate command.

New bounded stdlib probe executes actual Bash copies with controlled ps/lsof
subprocess responses in disposable repo-volume fixtures. It copies the real
sanctioned registry verbatim; worker IDs are synthetic records and are never
signaled by tests. Read-only handle outside repository cwd, command-named checkout,
advisory/all, existing exemption/unsanctioned other process and usage are exercised.
Tool failures retain valid partial stdout; status0+stderr and empty/whitespace
snapshots still refuse. Every exit checks owned stderr residue. TERM uses an
explicit checkpoint/release handshake, not a scheduling window; collect child
completion before disposing fixtures. Existing exemption cannot cover another
process. No real editor is closed by these tests.

19 positives pass normal/O; committed parent loses11 assertions with zero errors.
Independent omitted status/stderr/empty/TERM guards lose2/2/4/1 normal/O, no errors.
Actual restricted new census rc=2 names ps exit126 and leaves no stderr file;
unrestricted actual rc=0. No green verdict is inferred from restricted visibility.
Makefile gate adds the exact normal/O synthetic commands; the existing doctrine
CI job invokes make gate. Actual host census remains outside commit/CI gates;
39 doctrines/1439 arms unchanged. No redundant Rust/fullCI or outward push.

Verified whole source/task/README/Makefile/workflow/book inverses normal/O;
make -n gate resolves the enforcer plus exact tested normal/O commands, all other
suite legs/CI setup unchanged. Focused12/sharder12/seven books/3212 fresh+actual
links, complete normal/print teaching and literal --all host example rc=0.
History100/scope1367 bytes/modes/Gitlinks exact normal/O; actual old/moved/
published receipt+updated-digest edits jointly refuse. Whole DEV3180B/one entry
moves to0270 (3413B/51171112f2da43ec469733f22f3d887da1c786e94729eb17656cbe587580cf6d),
CH647B/one to0271 (884B/c96521afd6916316f9ca2f0936cd96c04f5c0759b5d44d371d43ab0591728819);
63live+210sealed273logical. Book proposal first exceeded36B remaining family
room; bounded rewrite lands +24B, with earlier receipt untouched. Render probe
initially compared straight apostrophe with actual smart apostrophe; normalize
that observed formatting only, then verify every teaching word normal/O.
EOF instrument first assumed per-line, then last-line warnings; both refused.
Actual byte/line census shows one Git warning at the first blank of each EOF
run (0270:51;0271:15). Match those exact outputs with whole moved bytes proved.
First commit hook refuses SEAM-INTEGRITY:56/57 isolated shell allocations.
Actual new allocation is on-volume; evaluator binds ROOT but not REPO_ROOT.
Add that existing script binding to the fixture root only; all allocator/path/
volume predicates remain byte-exact.57/57 normal/O and SEAM19/0 pass; omitted
or misdirected binding returns56/57 at handoff site70 before nonproject writes,
normal/O. Bare allocation still refuses. Whole instrument inverse exact outside
one binding. No first-attempt commit; update14-file proof/stage and retry hooks.
Final hooks/hash/mode/brief0/host-census postconditions next.
Artifact cleanup became due during this slice: finish/commit before pivot, then
own recurring cleanup ahead of ordinary-part guard assessment/remaining adequacy.
promotion: declined — existing fail-closed/tool-first/handoff rules govern;
no new policy, sanctioned entry, archive authority or qualification credit.

