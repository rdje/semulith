# CHANGELOG shard — SEMILITH-AC-0051 … SEMILITH-MM-0050

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-AC-0051 (leaf ARTIFACT-CLEANUP.2) — the sanctioned watcher is a ruling, not a false positive

The director ruled CHIPDOC's ChipdocWatcher ("it will stay there — do not worry about it from
now on"), and the ruling is now data: `doctrine/sanctioned_processes.tsv` carries the
executable substring, the ruling, and its date, and `check_no_background_jobs.sh` exempts
matching processes from both census arms — with the detection itself untouched, because the
census's whole design is that a list of things you thought of cannot see the thing you did not.
An agent proposes a row; only the director's ruling lands one. Verified both directions: the
live check prints `handoff: OK` with the watcher running, and the control probe (row absent)
flags the same process again. Tracked-content gates are unaffected.

## SEMILITH-MM-0050 (leaf MODEL-METHOD.6) — no coding without the source of truth, and MODEL-METHOD closes

The director's rule is a gate now. The unit registry gains `(requires …)` — the categories a
unit's scope declares — and `SCOPE-COVERAGE` (19th doctrine, 7 arms) refuses the day a required
category is `missing` or has no census row, fired RED before registration on a scratch unit whose
required category was absent. A unit with an undeclared scope refuses too: code may not start
against a scope never declared. `rv64i-lab-v0` declares its 14 in-scope categories, and the
verdict reads `1 unit(s) may code — every required category covered` — P1-LAB's precondition is a
verdict, composed with EXTRACTION (coverage says the facts are OWNED; extraction says they are
EXTRACTABLE). **`MODEL-METHOD` closes at 13/13**: the method in prose, the census, the
acquisitions, and the coding gate all landed; every P1 precondition is mechanical.

