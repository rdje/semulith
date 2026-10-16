# One definition, one book

Each unit owns an mdBook under `docs/models/<unit-id>/`
(`decision_one-definition-one-book`): pinned materials, missing inputs,
modelling choices, reference limits and evidence verdicts. Registration makes
this work reviewable; it does not accept the model.

Registered units:

- **`rv64i-lab-v0`** (kind: processor) — `docs/models/rv64i-lab-v0/`. The scalar
  processor laboratory and its materials-to-model method.
- **`rv64gc-lab-v0`** (kind: processor) — `docs/models/rv64gc-lab-v0/`. The
  Linux-oriented profile, registered with its pinned materials and prospective
  evidence policy. CPU-SYSTEM remains incomplete; registration establishes neither
  processor acceptance nor a Linux boot result. Read its introduction, policy and
  generated gate separately.
- **`dsp56300-lab-v0`** (kind: processor) — `docs/models/dsp56300-lab-v0/`. The
  bounded EXPERIMENTAL DSP subset, compared against its pinned reference; the unit
  that extended the abstraction beyond scalar CPUs (`P3-BREADTH`).
- **`netboard-lab-v0`** (kind: board) — `docs/models/netboard-lab-v0/`. RV64I
  composed with the two devices below, pinning versions; timers and interrupt
  controllers are absent by contract (`P5-BOARD`).
- **`sifive-uart-lab-v0`** (kind: device) — `docs/models/sifive-uart-lab-v0/`.
  The board's serial console and first device dossier.
- **`lan9118-lab-v0`** (kind: device) — `docs/models/lan9118-lab-v0/`. The wired
  NIC dossier, its three indexing levels and guest-readable time sources.

The device/board books adapt the arc: devices have no instruction encodings or
pinned CPU reference models. Their materials fragments state those limits.

## Build and browse the collection

From the repository root, build one book with
`mdbook build docs/models/rv64gc-lab-v0`, or the complete collection with:

```sh
make book
python3 -m http.server --bind 127.0.0.1 --directory docs 8000
```

Open `http://127.0.0.1:8000/book/book/`; a model starts at, for example,
`http://127.0.0.1:8000/models/rv64gc-lab-v0/book/`. Stop the server with Ctrl-C.
Cross-unit links require the shared `docs` root and built destinations.
Sibling rewrites preserve queries, fragments and sources.

```sh
python3 scripts/qualify_book_navigation.py --working-code --require-clean --output target/nav-verified
python3 scripts/qualify_book_toc.py --require-clean --output target/toc-verified
```

Use fresh paths. D77 depth1200 refuses2; immutable navigation replay retains16/1.
Chapter TOCs match SUMMARY hierarchy/labels; page headings/search/resources remain open.

## What the gate establishes

`UNIT-BOOKS` (`scripts/check_unit_books.sh`) reads `materials/units.sexp` through
the shared mapper, checks catalogue IDs/kinds and missing/orphan books, then
builds every book in a fresh `target/` bundle. It checks rendered local hyperlink
paths and HTML fragments, including print. Old output cannot pass; the bundle is
removed. Registered source paths must be relative, on the project volume,
outside symlinks and nested Git repositories.

For example, removing the RV64GC catalogue entry reports
`MODEL-CATALOGUE missing rv64gc-lab-v0`; a link to an absent local page reports
`BOOK-LINK missing-path`. Missing fragments fail separately. Remote availability,
unsupported link syntax and the semantic truth of prose are not established by
this offline check. mdBook can render a missing SUMMARY chapter as a draft: a
successful build alone does not prove chapter completeness or CPU acceptance.

The pre-registration overview and completed partition receipts are preserved in
ordinary history part14; the task-history chapter gives its reading command.
