# How do I ask chipdoc to acquire a document?

**File a request in `materials/requests.sexp` — that file is the preferred channel, and the
watcher fires on its change.** Recorded `2026-10-01` after a session re-derived the filing
mechanics from the channel's operator manual because no durable layer on semulith's side
carried them. The manual itself lives chipdoc-side (`CHANNEL.md` at the corpus root — the
corpus path is deliberately untracked; the untracked `.semulith-data/chipdoc/README.md`
holds it); this card is the semulith-side summary so the next session never has to.

## The rule

- **Preferred:** create or edit `materials/requests.sexp` (tracked here) with
  `(request (id "REQ-…") (status open) (wanted "…") (why "…"))` forms. `status open`
  fires; `resolved`/`fulfilled`/`blocked` are ignored. `why` should name the consuming
  leaf so a substitute is judgeable. Commit it — the FSEvents watcher fires on the file
  change, not the commit.
- **Fallback:** an open `(gap …)` in `materials/catalog.sexp` — only when
  `requests.sexp` does not exist, and beware: EVERY open gap is treated as a fetch
  request (a decision-shaped gap is a false positive).
- **Exactly once:** chipdoc suppresses ids it already knows (mirrored in its proposals
  feed or request ledger). A new id always fires. Fulfilment arrives chipdoc-side
  (its ledger + feed); semulith adopts the material into `materials/catalog.sexp` and
  fetches it into `.materials/`, then marks the request resolved.
- **Never write into the chipdoc repository** — the seam is hard: each side's files are
  read-only to the other.

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
