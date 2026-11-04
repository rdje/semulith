# Retained Zicntr and mcounteren statements: source terms and scope

Owner: `P4-SYSTEM.14` a43c-1 (2026-11-04); SRC-01 review before retaining a primary-source input. The licence finding and the wrapper's
attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`), and the privileged volume's terms were reviewed at
`materials/RVP_CSR_RETENTION.md`; this record adds two excerpts to the same table.

## Why

The ZICNTR case (REQ-D-ZICNTR, `implementation-defined`, high; `decision_reference-config-per-case.md`) binds its properties to one publication: a
case's normative input is a retained excerpt whose wrapper names the original page's digest, and that digest must be the case's source publication
(`review_div_capture.check_retained_input`, `P4-SYSTEM.14` a44-2c). The requirement names one source, RVI-ZICNTR §6.1, so that page is the normative input. What the
case's refused reads rest on is in another: `mcounteren`'s gate, RVP-MACHINE §2.1.1.11. It is retained beside it, and the credit names both.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `unpriv/counters.html` (RVI-ZICNTR, `sources.sexp`) | `8d619d6ef71d6cd87415342782aa615a0aff121a537342e4497658947f4fa81c` | 40747 |
| `priv/machine.html` (RVP-MACHINE, `sources.sexp`) | `b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea` | 271851 |
| `unpriv/colophon.html` (the unprivileged volume's licence evidence) | `7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c` | 112487 |
| `priv/priv-preface.html` (the privileged volume's licence evidence) | `6e4ba2ab3ea5174ff04881c48df7dfaf9402a0d070a76805535f1c7754645e59` | 54715 |

Each page pin occurs in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`. That supports retaining the manual
text below; it does not establish terms for the served website or its external assets. `priv/machine.html` is the longest page a row names, so the tool's page bound
moved from 262,144 B to 524,288 B; the tool is pinned by no case.

## Retention decision

`RVI-ZICNTR-STATEMENTS`, six statements in source order: of §6.1, that the counters are accessible via unprivileged read-only CSRs and divided between the two extensions; of
§6.1.1, what RDCYCLE, RDTIME and RDINSTRET read. `RVP-COUNTEREN-STATEMENTS`, four statements of §2.1.1.11: what `mcounteren` controls, that the counters keep incrementing
when not accessible, and the refused and the permitted read.

Not retained: the XLEN=32 forms and the RDTIME hart-synchronization sentence, which no witness of this one-hart RV64 case cites; Zihpm's statements, which the profile does not
select; and `scounteren`'s, because its page carries no anchor for it, and the extractor selects by anchor rather than by a span it would have to invent. `scounteren` is cited
(RVP-SUPERVISOR §11.1.1.5) and not retained, and the credit will say so.

Curated inputs: `profiles/rv64gc-lab-v0/retained/rvi-zicntr-statements.html`, 3,094 B, SHA256 `ee5bca84e2b9cc3be2c797535adcf701892967687e379c5d4df3738e7e4aad49`;
`profiles/rv64gc-lab-v0/retained/rvp-counteren-statements.html`, 2,806 B, SHA256 `a47ba18329dd6d7d4079f2f37c96619a8cb4347b4e973d37cc80e10ede27890a`.
Regenerate with `python3 scripts/retain_statements.py --emit <id>` using the acquired pages; check the tracked assets without that cache using `--verify`; the controls are
`scripts/probe_statement_retention.py` (19 tests, nine guard omissions in PROFILE-CONSISTENCY). The excerpts establish no ZICNTR acceptance; the case's declaration, capture, reviews
and credit are later units.
