# Retained RVP-CSR statements: source terms and scope

Owner: `P4-SYSTEM.14` a43b-3b (2026-11-03); SRC-01 review before retaining a primary-source input. The licence
finding and the wrapper's attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`), which already recorded the
privileged volume's own statement; this record adds the first retention from that volume.

## Why

The CSR-SET case (REQ-D-CSR-SET, `implementation-defined`, high; `decision_reference-config-per-case.md`) binds its properties to one
publication: a case's normative input is a retained excerpt whose wrapper names the original page's digest, and that digest must be
the case's source publication (`review_div_capture.check_retained_input`, `P4-SYSTEM.14` a44-2c). Of the six sources the requirement
names, RVP-CSR is the one that states what the case's refused accesses rest on: which privilege may access a CSR, and what an
attempt without it, or a write to a read-only one, does.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `priv/priv-csrs.html` (RVP-CSR, `sources.sexp`) | `330a17314ef803231955a915748176e5175fc773469f25a8c6b5ae922c9df425` | 140884 |
| `priv/priv-preface.html` (the licence evidence) | `6e4ba2ab3ea5174ff04881c48df7dfaf9402a0d070a76805535f1c7754645e59` | 54715 |

Both page pins occur in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`. The
preface to Version 1.10 states the licence for that volume and its future versions, in the same words the unprivileged preface
uses ("released under a Creative Commons Attribution 4.0 International License by the original authors, and this and future versions
of this document will be released under the same license"). That supports retaining the manual text below; it does not establish terms for
the served website or its external assets.

## Retention decision

Retain exactly five statements of §1.1.1, in source order: `norm:Zicsr_higher_priv` (a CSR is accessible at all higher levels),
`norm:Zicsr_rw` (csr[11:10] and read-only), `norm:Zicsr_access` (csr[9:8], the lowest level that can access it),
`norm:Zicsr_illegal_mode` and `norm:Zicsr_illegal_acc` (the two refusals) — the statements the case's legal and refused accesses
rest on. Not retained: the field-specification statements of §1.1.3 (WPRI, WLRL, WARL), which belong to the privilege leaf and which no
witness cites, and the CSR listing tables of §1.1.2, whose selection the requirement's own statement records.

The spans' markup was measured before review: `<code>` five times and one `<a href="hypervisor.html#sec:hcauses" class="xref page">`,
the manual's own cross-reference to the trap-cause table of the same publication. Each span is kept unmodified (the licence's
reproduction condition), so the extractor accepts exactly those shapes and refuses any other tag or attribute; the retained link is
relative and does not resolve beside the excerpt, which the wrapper's source link makes good.

Curated input: `profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html`, 2,750 B, SHA256 `0f2d75c5e8fb85505577c62320d035680704d9afeb8aae0e978174edbc63aba6`, input id `RVP-CSR-STATEMENTS`.
Regenerate with `python3 scripts/retain_statements.py --emit RVP-CSR-STATEMENTS` using the acquired pages; check the tracked asset without
that cache using `--verify`; the controls are `scripts/probe_statement_retention.py` (19 tests, nine guard omissions in
PROFILE-CONSISTENCY). The excerpt establishes no CSR-SET acceptance; the case's declaration, capture, reviews and credit are later units.
