# The cleanup planner refused the whole of `target/` over 4460 scratch files — whose names were they?

**Mine: the XTASK.8 controls' record of probe invocations, keyed by argv with U+001F between words and
U+001E for `/`.** `scripts/artifact_cleanup.py --plan` walks `target/` and passes every entry through its
path contract (`relative()`: UTF-8, no byte below 0x20, no 0x7F, no backslash, under 4096 bytes, no `..`);
one name it cannot represent refuses the whole plan with `unsafe relative path`, and the recurring cleanup
cannot run until the name is gone. A key encoding chosen for one tool's lookup table became a path that
another tool, with its own correct contract, must refuse — and the control script that wrote the names
never removed them.

## What happened

On 2026-10-27 the fifth recurring cleanup (`ARTIFACT-CLEANUP.28`, AC0085) ran its plan act first, as
always, and the act refused after a 73 s walk: `{"disposition": "refused", "reason": "unsafe relative
path"}`. A census of `target/` for names with control characters, backslashes or over-length found 4460
entries, all under `target/xtask/xt0017` — but my first census grouped them by a three-component prefix and
printed one example, `shadow/record/`, and I archived and removed those 4 files (the `control_shadow.sh`
record) and re-ran: refused again, 86 s. The second census listed the population per directory: 4456 files
in `rest/rec12` and `rest/rec24` (2228 each), the two parallel prefetch runs of XTASK.8 slice c (2026-10-27
03:38 and 03:44), each named `<argv with U+001F/U+001E>.out` or `.rc`. The commit gate's own prefetch (the
same key shape) writes under the check's scratch and removes it before its summary; the measurement copies
did not. Both populations were archived whole (`shadow-record.tar` 4 entries, `rest.tar` 4459 entries, each
count checked against the files before anything was removed) and removed; the census then found 0 such
names and the acts ran.

## How to catch it, and what to do

- **A key is not a file name.** A lookup table that must live on disk gets names from a hash or an index
  (`sha256(key)[:16]`, `0001`…), never from the key's bytes; the key itself lives inside the record.
  Control characters in names are legal to the filesystem and hostile to every other tool's path contract.
- **Scratch a control writes under `target/` is the control's to remove.** The gate's version cleans up;
  a development copy must do the same or write under `TMPDIR` (`mktemp -d`), where a census of `target/`
  never sees it.
- **A partial profile is not a profile — again.** A census grouped for display is not a census for action: act on
  the listed population (every directory, its count), never on a group's one example.
- **A census that refuses one entry refuses the tree.** That is the planner's correct contract today
  (nothing it cannot name may be planned), but a refusal that names the offending path, or quarantines
  it as "unrepresentable" and plans the rest, would have turned a blocked recurrence into a listed item.
  Recorded in the `.28` result as an open design item for the ARTIFACT-CLEANUP tree, not changed here.

Evidence: target/artifact-cleanup/AC0085-run-1-refused.log; the census (`os.walk` over `target/`, bytes
< 0x20 / 0x7F / `\` / > 4096) in the leaf's result; `scripts/artifact_cleanup.py` `relative()` and its
call at the walk (`name = relative(path + "/" + entry.name)`); `docs/tasks/ARTIFACT-CLEANUP.md` `.28`.
