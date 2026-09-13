# Two tracked files are byte-identical — which one is canonical, and what proves it?

**Answer: the artifact that enumerates the delivery decides, not the file names.** Look, in
order, for (1) a delivery manifest or index that lists one of the paths, (2) inbound
references from other tracked files, (3) the path a downstream contract already binds to.
The unlisted, unreferenced copy is the accident; delete it and keep the named one.

## Evidence

Measured while ingesting planning package v0.2 (`SEMULITH-PKG.1`):

```
$ diff docs/ARCHOGEN_INTEGRATION.md docs/SEMULITH_ARCHOGEN_INTEGRATION.md ; echo rc=$?
rc=0                                   # byte-identical: 97 lines, 11997 bytes each
$ grep -rn 'SEMULITH_ARCHOGEN_INTEGRATION' . | grep -v '^./.git/'
                                       # (no output — referenced by nothing)
$ grep -c ARCHOGEN docs/provenance/planning-package-v0.2/MANIFEST.sha256
1                                      # the manifest names docs/ARCHOGEN_INTEGRATION.md only
```

`ROADMAP.md` §3 and `README.md` both route readers to `docs/ARCHOGEN_INTEGRATION.md`, so
three independent signals agree.

## Why it matters beyond tidiness

Rule `OWN-01` says each semantic rule has **one** owned implementation. Two copies of a
contract document is that failure in its cheapest form: both pass every gate, both read
correctly, and they diverge on the first edit — after which two readers hold different
contracts and neither knows it. Byte-identity is exactly the state in which the defect is
free to fix; it never gets cheaper than this.

## The trap

Do not settle it by "the more specific name looks more official". `SEMULITH_ARCHOGEN_INTEGRATION.md`
reads as the more deliberate of the two and was the wrong one. Name aesthetics are not
provenance.
