# How does semulith ask chipdoc for a document, and know it was heard?

**File a `(request …)` in `materials/requests.sexp` with `(status open)` — the preferred,
false-positive-free channel.** chipdoc's watcher (FSEvents, persistent) fires on the
change, summons its acquisition agent, and mirrors the id as resolved when fulfilled.
The fallback — an open `(gap …)` in `materials/catalog.sexp` — also fires, but EVERY open
gap fires, including review-decision gaps, so it is noisier.

## The contract (adopted from chipdoc's `CHANNEL.md`, 2026-09-30, copied here per Policy 12)

Direction A (semulith → chipdoc), in order of preference:

1. **`materials/requests.sexp`** — the poller prefers it whenever it exists; only genuine
   acquisition requests fire. Shape: `(request (id "REQ-X") (status open) (wanted "…")
   (why "…"))`. `resolved`/`fulfilled`/`blocked` are ignored. Fires on: create the file,
   add a request, or reopen a `status`.
2. **An open `(gap …)` in `materials/catalog.sexp`** — the fallback; fires on any open
   gap whose id chipdoc does not already know.
3. **Operator relay** — the manual escape hatch (a chipdoc-side ledger entry or a
   `CHIPDOC_REQUEST_BRIEF=…` direct summon).

**Exactly once:** chipdoc suppresses any id it already knows (present in its proposals
feed or its own ledger), so a fulfilled request stops firing; a NEW id always fires.
**Nothing else fires**: editing a task leaf, DEV_NOTES, the book, the roadmap, or any
prose file — the poller reads only those two files.

**What fulfillment looks like:** the document lands in chipdoc's corpus with a
`SHA256SUMS`, the proposals feed mirrors the id as a resolved gap, `SEMULITH.md` notes
the batch. Semulith then adopts through the seam (catalogue + cache, digest verified).
It is event-driven, not polling; a durable `.runtime/PENDING` sentinel means a missed
notification cannot become silence.
**The answer path, updated `2026-10-01`:** answers also arrive PER-REQUEST, re-keyed by
our ids, in chipdoc's `catalog/responses.sexp` (and `build_responses.py --report`) —
and our own `requests.sexp` keeps saying `open` until WE flip it, because chipdoc never
writes here. That gap caused the second incident (answered 5/5, seen as 10× `open`).
The full ask→answer loop lives in [`the-chipdoc-request-channel.md`](the-chipdoc-request-channel.md);
this card keeps the channel's measured history.

## Measured here

- `2026-09-29`: the poller read only TOP-LEVEL `(gap …)` forms and this catalogue nests
  its gaps inside the `(materials …)` form — the channel was deaf to our gaps until the
  chipdoc-side fix (`6bfabf2`). The fix was measured heard (`MODEL-METHOD.17`).
- `2026-09-30`: two gaps filed in `materials/catalog.sexp` (DSP56300, ADI SHARC) — the
  watcher fired at 19:42:33, hung the first run on a missing provider setting (the
  incident CHANNEL.md §7 exists for), and both documents plus seven more DSP families
  landed in the corpus the same day (`SEMULITH.md`'s 2026-09-30 batch). The channel is
  two-way, measured end-to-end.

## Troubleshooting order when "filed and nothing happened"

(1) `status` is `open` and the id is new (not already known); (2) the watcher runs
(`launchctl list | grep chipdoc`); (3) `SEMULITH_ROOT` points at this checkout; (4) the
durable sentinel `.runtime/PENDING` and the watcher log; (5) the agent's preflight
(`PI_PROVIDER`/`PI_MODEL` set, auth ready) — without the provider variable the agent
used to hang a full hour and look like no trigger (the 2026-09-30 incident).

## answers

- Which file do I write to ask chipdoc for a document? `materials/requests.sexp`
  (preferred) with `(status open)`; fallback: an open gap in `materials/catalog.sexp`.
- When does a request fire? On create/add/reopen, only if the id is new and the status
  is open. `resolved`/`fulfilled`/`blocked` never fire.
- How do I know it was heard? `catalog/responses.sexp` re-keys the answer by our id
  (`build_responses.py --report`); `.runtime/LAST_RESULT` records the last summon's
  outcome; the proposals feed mirrors the id as resolved; our own file flips when WE
  flip it.
- If it did not fire, where do I look? Status/id-newness → watcher running →
  SEMULITH_ROOT → the sentinel and watcher log → the agent's provider/auth preflight.
