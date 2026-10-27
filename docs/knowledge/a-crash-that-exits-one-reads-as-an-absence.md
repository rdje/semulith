# A probe that exits 1 for "absent" and crashes with exit 1 — which did the gate see?

**An absence, every time: the crash became a NAMED SKIP and the gate turned green.** The availability
probe of `scripts/check_citation_quotes.sh` — nine lines of Python on `python3 -`'s stdin — ends with
`sys.exit(0 if C.artifacts_available() else 1)` inside a `try` whose `except` tuple (`CitationError`,
`SexpError`, `KeyError`, `OSError`) maps a refusal to exit 2. Any other exception propagates, and the
interpreter exits 1 with a traceback on stderr — the same status the driver reads as "the pinned pages
are absent". Measured on 2026-10-27, in the `XTASK.6` slice 6r fixture `manifest-unreadable`: a
`profiles/p/sources.sexp` cut off mid-form made `dossier_sexp.load` raise `dossier_sexp.DossierError` through
`S.read_file`; the traceback went to stderr, the driver printed `CITATION-QUOTES: NAMED SKIP — the
pinned pages are absent …` and exited 0.

## What happened

Slice 6r ported the driver to Rust behind a held shim and measured the port against the bash driver
at HEAD over scratch git repositories, one corpus state each. The state meant to show "availability
REFUSED" (exit 2) showed the NAMED SKIP on both sides — identical bytes in stdout, stderr and exit
status — so the port carries the behaviour faithfully, as a byte-identical port must. The last
traceback line named the exception the probe's tuple does not catch; the collision is in the
script's design, not in either implementation of it. The port did not change the verdict: a port
is measured against the script, and a verdict change is the doctrine owner's decision (an open
question in the `XTASK` leaf).

## Why it matters

A check that cannot judge must say so, never pass — the SEMANTICS doctrine's CITATIONS-arm precedent
the script itself cites. Here the one case the precedent is for (a manifest the reader refuses) is
reported as the benign skip, and nothing downstream distinguishes them but a traceback on a gate
log nobody reads when the gate is green.

## How to apply

- In a probe whose exit code IS the verdict, the interpreter's own failure code must not be a
  verdict: catch `Exception` into the "cannot judge" code, or number the verdicts from 3 so that 1
  stays the interpreter's.
- A fixture state that returns the "wrong" verdict identically on both sides is still a finding —
  read the stderr of a state that surprised you before counting it as identical and moving on.
- When porting a probe, port the collision too and record it; the measurement's contract is the
  script's behaviour, and the fix is a separate, re-measured change.
