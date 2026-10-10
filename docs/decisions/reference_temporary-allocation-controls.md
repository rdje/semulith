# Repository-volume temporary allocation controls

- Type: `reference`
- Owner: `LIVE-CONTAINMENT.4d`, `SEMULITH-LC-0007`, 2026-10-10
- answers: How are temporary paths and fixture cleanup checked without making a foreign write?

The f699474 source census finds12 unqualified shell allocations (ten in scripts,
two in executable task artifacts) and two unqualified Python self-test allocators.
The materials self-test's individual mkdtemp fixtures also lack cleanup. Repair
these sites with repository-derived templates/parents and one scoped materials
fixture lifetime. The driver, hook, repaired entrypoints and push boundary export
repository-derived TMPDIR for delegated tools. Failed root lookups and the newly
qualified allocation results refuse before those paths are used. Synth creates
its scratch parent, checks allocation failure and retains an exit cleanup trap.

`python3 scripts/probe_temporary_locality.py` exposes these modes:

| Mode | What is actually exercised |
| --- | --- |
| `--mode shell` | Every tracked shell/hook mktemp call expression, including stdout helpers and task artifacts:56sites at this capture. A shim refuses unqualified/outside-target templates before executing the OS tool. Successful allocations are checked on-volume and deleted exactly. Acquisition, update and push workflows are not executed. |
| `--mode python` | Actual materials and dump-comparator self-tests under an allocator guard. Missing/outside-target parents refuse before allocation; every allocated directory must be gone afterwards. Both self-tests run successfully after repair. |
| `--mode children` | Actual environment-setting blocks from14entrypoints, with unset and foreign inherited defaults:28child checks. The push block runs in function scope, as in its real entrypoint. |
| `--mode parent` | Synth's actual parent/allocation block in a fresh repository-local fixture. The f699474 block fails without a parent; the repaired block allocates successfully. |
| `--mode bare-shell`, `bare-python`, `residue`, `unconstrained-child` | Deliberately unqualified allocators, a leaking qualified fixture and an unconstrained child. Each fails for its named reason; only this invocation's proven fixture directories are cleaned. |

`--revision f699474` replays predecessor source read-only. Shell44/56 and Python0/2
were observed RED; current56/56 and2/2 pass. The first narrow extractor counted
only command substitutions (16sites); the complete extractor includes direct
stdout helper calls and the expanded census includes all tracked executable task
artifacts. The gate uses the complete population. This is a direct-allocation and
child-default control, not a proof about every operating-system write. Existing
project caches and evidence retention keep their separate contracts.

The host interpreter and mktemp are required, read-only toolchain dependencies.
Their executable locations are resolved at runtime; no project cache/store is
placed beside them. The shim rejects foreign paths before allocation. Legacy or
shared directories are not deleted on inferred ownership.

The source-repair guard SEAM-INTEGRITY runs ten new permanent arms: the four
positive modes, four negative modes, an optimized-interpreter refusal and the
published acceptance probe. All19arms discriminate; earlier nine remain intact.
The first shim used asserts; a mock allocator confirmed optimization removed its
guard. Explicit checks now remain active under optimization and check the parent
device before allocation. No real allocator ran in the bypass reproduction.

That acceptance probe exposed a separate stale fixture: its custom token
WIDGET-COVERAGE already matched the default verdict family introduced by
`d8c2337` (`git log -S`/blame of the signature declaration). CTRL-4b therefore
returned GREEN without the custom declaration: published probes9pass/1fail.
Use `widget_evidence_ok`, which requires its declared seam:10pass/0fail.
Production acceptance vocabulary is unchanged. The complete published probe now
runs under SEAM-INTEGRITY so later vocabulary expansion cannot silently invalidate
its discriminating input. Reporting also correctly calls this the current tracked
acceptance corpus; it does not claim to compare each box with its historical commit.
