# How do I ask chipdoc to acquire a document — and how do I read the answer?

**File a request in `materials/requests.sexp` — that file is the preferred channel, and the
watcher fires on its change. Read the answer per-request in chipdoc's
`catalog/responses.sexp` — and expect YOUR file to keep saying `open` until YOU flip it:
chipdoc never writes here, so an answered request still reads `open`. That is the protocol,
not silence.** Recorded `2026-10-01` after a session re-derived the filing mechanics from the
channel's operator manual because no durable layer on semulith's side carried them; updated
the same day with the answer path (CHANNEL.md §0.3/§0.5, re-read `2026-10-01`) after the
second incident — chipdoc answered all ten `P5-BOARD.8` requests and semulith, still seeing
`open`, nearly concluded nothing had happened. The manual lives chipdoc-side (`CHANNEL.md`
at the corpus root — the corpus path is deliberately untracked; the untracked
`.semulith-data/chipdoc/README.md` holds it); this card is the semulith-side summary.

## Asking

- **Preferred:** create or edit `materials/requests.sexp` (tracked here) with
  `(request (id "REQ-…") (status open) (wanted "…") (why "…"))` forms. `status open`
  fires; `resolved`/`fulfilled`/`blocked` are ignored. `why` should name the consuming
  leaf so a substitute is judgeable. Commit it — the FSEvents watcher fires on the file
  change, not the commit.
- **Fallback:** an open `(gap …)` in `materials/catalog.sexp` — only when
  `requests.sexp` does not exist, and beware: EVERY open gap is treated as a fetch
  request (a decision-shaped gap is a false positive).
- **Exactly once:** chipdoc suppresses ids it already knows (mirrored in its proposals
  feed or request ledger). A new id always fires; to re-ask after a `blocked`, use a NEW
  id and say what changed (a new route, a new URL).
- **Never write into the chipdoc repository** — the seam is hard: each side's files are
  read-only to the other.

## Reading the answer (the half the second incident closed)

1. **The report, quickest** — `SEMULITH_ROOT=<repo root> python3
   <corpus>/scripts/build_responses.py --report`. One line per request:
   `semulith=open chipdoc=fulfilled|blocked|UNACKNOWLEDGED`. Exit 0 = every open request
   has an answer; 1 = at least one UNACKNOWLEDGED (a channel failure, never normal).
2. **The file** — `<corpus>/catalog/responses.sexp`, re-keyed by OUR ids (never learn
   chipdoc's internal `REQ-0nn`): `(response (id "REQ-…") (status fulfilled|partial|
   blocked) (artifact path (sha256 …) (bytes …)) (evidence "…"))`, generated from
   chipdoc's ledger and drift-checked there.
3. **What each status means here:** `fulfilled` → fetch from the corpus, verify the
   sha256, adopt into `materials/catalog.sexp` (the material record is in
   `catalog/semulith-proposals.sexp`), mark OUR request `resolved`. `blocked` → a
   MEASURED negative (which routes were tried, what each returned) — record it, mark
   OUR request `blocked`, plan around it; it is an answer, not a failure. `partial` →
   judge the substitute, or re-file with a new id naming what is still missing.
4. **Did the last summon even run?** — `<corpus>/.runtime/LAST_RESULT` (written per
   summon, with a desktop notification to the operator): "all semulith requests
   answered", "INCOMPLETE … unacknowledged=[ids]", or "NOT ANSWERED — preflight
   FAILED". A summon that cannot start says so; failure is never silent.

## Measure the channel, don't hope

Run chipdoc's poller read-only (it prints unmirrored open ids; exit 1 = new):

```
SEMULITH_ROOT=<repo root> python3 <corpus>/scripts/poll_semulith_gaps.py
```

The watcher (the sanctioned standing `ChipdocWatcher`) watches both `materials/` files.
If it should have fired and didn't: `launchctl list | grep chipdoc`, then the durable
sentinel `<corpus>/.runtime/PENDING`, then the watcher log — the channel's own
troubleshooting order (a trigger you cannot observe is not a working channel).

## Before filing

Survey what the corpus already holds — the snapshotted feed
(`.semulith-data/chipdoc/catalog/semulith-proposals.sexp`) and its gap records are the
local, offline answer; re-requesting a held document is churn on both sides.
