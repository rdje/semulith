# Explicit obligation-catalog parts preserve frozen records

- **Type:** `decision`
- **Date:** `2026-10-09`
- **Status:** `active`
- **Owner / source:** P4-SYSTEM.13 c2, measured catalog capacity and reader controls

## The fact / decision

Obligation catalogs may use explicit `(include-obligations (path "…"))` forms.
Paths are canonical repository-root-relative POSIX paths, expanded in place by
`scripts/record_catalog.py`; record mapping delegates to that one owner.

## Why

The GC catalog reached 63,014 of its fixed 65,536-byte authored-part bound before
five complete boundary assumptions. Its frozen v0/v1 records cannot be rewritten.
Moving their contiguous bytes into two parts reproduces the entire old stream
exactly (SHA-256
3981180e99dcc0a35155f0955d5f0979cf9793de36627af91dbcac5458926f6c),
leaves each authored part under the same bound and adds only include
directives to aggregate storage. No duplicate flattened source is maintained.

The consumer census identified raw readers in freeze checking, record conversion,
Rust declaration tests and gate-report scratch fixtures; dictionary consumers
already use the record loader. All these paths now share expansion. The census
also reproduced rejection of schema-valid top-level annotations by the record
loader; reserved comment forms now stay out of its record mapping.

## How to apply

Keep obligation records one per line for the existing frozen-line hash contract.
Place parts beside the unit catalog with an `.obligations.sexp` suffix; the dossier
gate routes that suffix to the obligation schema. Includes belong only to obligation
catalogs. Every included source is schema validated with its own origin before
the existing cross-record rules judge the expanded catalog.

Missing files, cycles, repeated parts, malformed directives, noncanonical paths,
non-obligation part forms and resolved paths escaping the selected root refuse.
Only parsed top-level directives expand; literal strings and comments do not.
Include-only lines merge their newline with a part's final newline. Preserve
the expanded stream byte-for-byte when partitioning existing records and verify
all mappings, order, version membership and frozen pins. Do not raise any cap.

Use `record_catalog.text(path, root=...)` for expansion, `records_sexp.load` for
mapping, and `source_texts` plus the schema owner's `validate_text` for original
source validation. Scratch mutation controls flatten through the owner so they
cannot accidentally read live parts. The permanent probe exercises 31 controls;
its disabled-expansion mutant must fail. This format change grants no new
behavioral evidence or contract credit.
