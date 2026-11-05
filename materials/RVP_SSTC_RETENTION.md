# Retained Sstc, stimecmp and STCE statements: source terms and scope

Owner: `P4-SYSTEM.14` a43d-2 (2026-11-05); SRC-01 review before retaining a primary-source input. The licence finding and the wrapper's
attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`), and the privileged volume's terms were reviewed at
`materials/RVP_CSR_RETENTION.md`; this record adds three excerpts to the same table.

## Why

The SSTC case (REQ-D-SSTC, `implementation-defined`, high; `decision_reference-config-per-case.md`) binds its properties to one publication: a case's normative input is
a retained excerpt whose wrapper names the original page's digest, and that digest must be the case's source publication (`review_div_capture.check_retained_input`,
`P4-SYSTEM.14` a44-2c). The requirement names one source, RVP-SSTC §12.1, so that page is the normative input. What the case's witnesses rest on is in two others: what makes
the interrupt pending and when it traps, RVP-SUPERVISOR §11.1.1.3 and §11.1.1.12, and what `menvcfg.STCE` gates, RVP-MACHINE §2.1.1.9 and §2.1.1.18. They are retained beside it, and the credit names all three.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `priv/sstc.html` (RVP-SSTC, `sources.sexp`) | `30bea862eee800d485ce34636b2824bf9909a4676b39d2c5734e92fba14216e1` | 27429 |
| `priv/supervisor.html` (RVP-SUPERVISOR, `sources.sexp`) | `d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a` | 186455 |
| `priv/machine.html` (RVP-MACHINE, `sources.sexp`) | `b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea` | 271851 |
| `priv/priv-preface.html` (the privileged volume's licence evidence) | `6e4ba2ab3ea5174ff04881c48df7dfaf9402a0d070a76805535f1c7754645e59` | 54715 |

Each page pin occurs in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`. That supports retaining the manual
text below; it does not establish terms for the served website or its external assets.

## Retention decision

`RVP-SSTC-STATEMENTS`, two paragraphs of §12.1 in source order: why supervisor mode has its own timer, and that the extension adds `stimecmp` and `STCE`.
`RVP-STIMECMP-STATEMENTS`, five statements: of §11.1.1.3, when an interrupt traps to S, when those conditions are evaluated, and what `sip.STIP` and `sie.STIE` are; of §11.1.1.12, that `stimecmp` is 64-bit, and when the interrupt
becomes pending. `RVP-STCE-STATEMENTS`, five statements: of §2.1.1.9, that STIP is read-only and reflects the timer signal, which a write above `time` clears; of §2.1.1.18, that the extension adds `STCE`, and what it enables and refuses.

**The tool gained two selection shapes, and why.** The Sstc chapter anchors none of its text, so `opening:<words>` selects the one paragraph opening with exactly those words, and three of the supervisor statements are whole
paragraphs carrying the anchor on their `<div>`, not a span. Each is quoted from inside its `<p>`, unmodified, under the same markup allowlist and byte bound, and a shared opening refuses. The older excerpts' bytes did not move (`--emit` against each retained file, `cmp` silent).

Not retained: the hypervisor's `vstimecmp` and `henvcfg` statements, and `stimecmph`'s RV32 form, none of which this one-hart RV64 case can reach, though `norm:stimecmp-stimecmph_sz_acc` carries the latter in its one sentence; `mtime` and `mtimecmp`, which the laboratory does not declare.

Curated inputs: `profiles/rv64gc-lab-v0/retained/rvp-sstc-statements.html`, 2,926 B, SHA256 `8032b3fff7e2861adf58a2965f5cca55025242b9ae46f3f034c24677cbf3e7a6`;
`profiles/rv64gc-lab-v0/retained/rvp-stimecmp-statements.html`, 4,315 B, SHA256 `7f2362b1cc60afb3281c82e50e244b6dd4b971e13eae25c0aac46e3601d3b6e3`;
`profiles/rv64gc-lab-v0/retained/rvp-stce-statements.html`, 3,101 B, SHA256 `dd8a425e87b394c6bc655c98724debc3875f690c903685f8a3f84eb504306c15`.
Regenerate with `python3 scripts/retain_statements.py --emit <id>` using the acquired pages; check the tracked assets without that cache using `--verify`; the controls are
`scripts/probe_statement_retention.py` (21 tests, nine guard omissions in PROFILE-CONSISTENCY). The excerpts establish no SSTC acceptance; the case's declaration, capture, reviews
and credit are later units.
