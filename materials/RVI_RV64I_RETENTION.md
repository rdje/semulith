# Retained RVI-RV64I statements: source terms and scope

Owner: `P4-SYSTEM.14` a43a-2a (2026-10-29); SRC-01 review before retaining a primary-source input. The licence
finding and the wrapper's attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`); this record
adds one more scoped retention from the same publication.

## Why

The XLEN case (REQ-D-XLEN: "XLEN = 64. The integer registers and the supported user address space are 64 bits.",
RVI-RV64I §3.1.1, `defined`, low; `decision_state-capture-plan.md` item 1) binds its properties to the one source
its requirement names. A case's normative input is a retained excerpt whose wrapper names the original page's
digest, and that digest must be the case's source publication (`review_div_capture.check_retained_input`,
`P4-SYSTEM.14` a44-2c) — so the XLEN case needs RVI-RV64I's statements retained the way the M case's were.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `unpriv/rv64.html` (RVI-RV64I, `sources.sexp`) | `6eadb316c2d535ccb87a7a6feb03ff54af6f4b5bbeb5c1a5102a02af81f13abd` | 49246 |
| `unpriv/colophon.html` (the licence evidence) | `7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c` | 112487 |

Both page pins occur in the snapshot manifest; the cache is the existing materials route,
`.materials/riscv/pinned-v20260120/`.

## Retention decision

Retain exactly ten statements of RV64I Version 2.1 §3.1, in source order: `norm:rv64i_xreg_sz` (§3.1.1, the 64-bit
registers and address space), `norm:rv64_w_sex` (§3.1.2), `norm:addiw_op`, `norm:addiw_overflow`,
`norm:slliw_srliw_sraiw_op`, `norm:lui_op_rv64i` (§3.1.2.1), `norm:addw_subw_op`, `norm:addw_subw_overflow`,
`norm:sll_srl_sra_sh_amt_rv64i` and `norm:sllw_srlw_sraw_op` (§3.1.2.2) — the statements the XLEN program's witnesses
rest on (`profiles/rv64gc-lab-v0/guests/xlen-forms.s`, a43a-1). Not retained: the load/store and AUIPC statements
and the reserved-encoding statement, which no witness cites.

The spans' markup was measured before review: `<em>` five times and one `<a href="rv32.html#gprs" class="xref
page">` — the manual's own cross-reference to the RV32I register-state section of the same publication. Each span
is kept unmodified (the licence's reproduction condition), so the extractor accepts exactly those shapes and
refuses any other tag or attribute; the retained link is relative and does not resolve beside the excerpt, which
the wrapper's source link makes good.

Curated input: `profiles/rv64gc-lab-v0/retained/rv64i-statements.html`, 4,163 B, SHA256
`5c93941804b6bab707d3c0345529fc918b10a953d72bc82d5735bcf78788f2a5`, input id `RVI-RV64I-STATEMENTS`. Regenerate with
`python3 scripts/retain_rv64i_statements.py --emit` using the acquired pages; check the tracked asset without that
cache using `--verify`; the controls are `scripts/probe_rv64i_statement_retention.py` (17 tests, seven guard
omissions in PROFILE-CONSISTENCY). The excerpt establishes no XLEN acceptance; the case's declaration, capture,
reviews and credit are later units.
