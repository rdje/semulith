# Closed graph-census evidence — LC.4i2a

Owner: `LIVE-CONTAINMENT.4i2a / SEMULITH-LC-0023`.
Contract: `docs/tasks/artifacts/live-containment/inventory-contract.md`.
This is collection evidence; complete semantic graph coverage remains open.

## Immutable source

Revision `28920c6bdace84afaaa68621d4db9ab70060e602` has 1,411 tracked
identities: 1,410 regular blobs and one opaque Gitlink, `vendor/linkedspec`.
The recursive NUL inventory SHA256 is
`aa328d6df30bb2b39d1491c348e88e4a666934f4db51d43d633d9571942351a2`.
Regular source bodies total 15,264,012 bytes. The collector verifies each Git
blob's framed response and object identity, then records its SHA256, byte/LF
counts, mode and path. It never opens the Gitlink implementation.

All 462 source Markdown files are accounted for. They contain 53 literal
`{{#include …}}` candidates, each recorded with its encoded byte offset, exact
marker and digest. All 53 close on their line. These observations include
literal/example text; they are not a claim that every candidate executes or
that transitive expansion has been resolved. The 338 Markdown files outside
registered book source directories remain explicit review inputs. Directory
membership cannot establish whether their content appears through includes.

## Fresh rendered evidence

Seven registered books are built through the documented `mdbook build` CLI
into a fresh repository-volume bundle. The measured proposed LC-0023 working
view contains 120 HTML pages, including print pages, and 3,244 anchor-link
occurrences: 2,006 fragment-only, 1,176 local-path and 62 remote. These are
occurrences, not unique semantic routes. An independent HTML collector and
the existing `unit_books.navigation_findings` reconcile the hyperlink count;
a separate directory traversal reconciles the complete HTML population.
Page identities are checked again after navigation verification.

The collector separately retains 2,076 rendered resource candidates, including
non-anchor `href`, `src`, `srcset`, `action`, `data` and `cite` attributes. They
await route review; the hyperlink verdict does not validate those resources.
Remote links are observed, with identity and availability unclaimed.

The immutable source census and the actual working rendered view are distinct
inputs. The retained result records both the selected source revision and
complete working HEAD/index/member identities before and after the build.
Their equality is required. Explicit `--addition` paths include owned
untracked inputs when collecting a proposal. Later runs rebuild their own
working books; they must not be presented as historical rendered-byte replays.

## Replay and finite qualification

```sh
python3 scripts/collect_containment_graph.py --self-test
python3 -O scripts/collect_containment_graph.py --self-test
python3 scripts/collect_containment_graph.py --revision 28920c6 \
  --output target/live-containment/graph-census/replay-normal
python3 -O scripts/collect_containment_graph.py --revision 28920c6 \
  --output target/live-containment/graph-census/replay-optimized
```

Choose unused output directories. The collector writes only generated evidence
under `target/`; it retains `census.json`, seven build stream pairs and the
rendered bundle. The selected source Git objects and installed Python/mdBook
toolchain must be available. Toolchain execution is a necessary read-only
system dependency; project outputs and child temporary storage stay on volume.
Missing source objects refuse without fetching. Existing output paths refuse
rather than overwriting prior evidence. Exit0 means this bounded collection
completed; exit2 means it could not be qualified. Partial builds are not green.

Twenty-two finite refusal controls run normally and with optimization. Twelve
reuse the immutable-input qualifier's malformed inventory/registry and failed
Git read cases. Ten further cases cover missing/truncated/incorrect/surplus
blob responses, omitted source/include/page/link populations and ambiguous
rendered hyperlinks. Positive controls include UTF-8 byte offsets, incomplete
include candidates, HTML entity decoding and all six resource attributes. They test these named input
contracts, not a universal Markdown parser or final integration coverage.

A copied resource-producer omission returns2 with no success output for the
named resource positive-control failure, normally and with optimization. The
real program and input states remain exact. Three actual public CLI cases also
refuse2/no stdout in both modes: reused output, unavailable source and output
outside `target/`. They preserve the existing evidence bundle and source state.

## Remaining owned work

`.4i2b` reviews reader references, includes, indexes, queries, generated views,
read commands and the source/output relationship. `.4i2c` captures author
overflow candidates from actual public failure output. `.4i2d` reconciles exact
terminals, exclusions, overlaps and full omission coverage. Utility, lifecycle,
derived fields, pressure/debt and checker adoption remain `.4i3–8`.
No capacity, archive, retention or processor-acceptance authority is added.
