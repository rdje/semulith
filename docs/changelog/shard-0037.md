# CHANGELOG shard — SEMULITH-UT-0052 … SEMULITH-UT-0052

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-UT-0052 (leaf UPSTREAM-TRACK.2) — `verified` must carry the re-run that earned it

The tracker already refused a `verified` with no pin. It now refuses the next hole too: a
`verified` whose event names a pin but captures no `(repro …)` output **inside the subtree** —
the pin retires upstream's changelog claim, but only the captured run retires ours. Four new
self-test arms (pin-without-repro, artifact missing, artifact escaping the subtree, pin+artifact
accepted); `16 pass / 0 fail`.

⛔ **Fired RED on the real tracker before any artifact existed** — the strengthened gate refused
LS-001's just-committed `verified` ("captures no (repro …) re-run output", rc=1). Then the
evidence landed and every state became earned, not asserted:

- **LS-001 → `verified`** — the reproduction re-ran and was captured into the subtree itself:
  `evidence/verified-a8d34c845.txt`, `8 matched / 0 differed`. A maintainer copying the issue
  directory out now carries the proof with it.
- **LS-003 → `verified`** — the three first-consumer papercuts are remedied in the guide at the
  adopted pin, and each remedy was *exercised* during the pin update (workspace exclusion,
  prerequisite chain, maintained wrapper), transcript captured — exit statuses, not banners,
  per the guide's own warning.
- **LS-002 → `acknowledged`** — upstream took ownership by name: the LS-001 fix commit records
  "LS-002 and related kind/strict requirements remain .83.1 owned". No re-run owed; the design
  question is theirs until it ships.

