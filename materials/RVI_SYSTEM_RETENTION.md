# Retained ECALL, Zicsr, Zifencei and C statements: source terms and scope

Owner: `P4-SYSTEM.14` a47-1 (2026-11-06); SRC-01 review before retaining a primary-source input. The licence finding and the wrapper's
attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`), and the privileged volume's terms were reviewed at `materials/RVP_CSR_RETENTION.md`; this record adds four excerpts to the same table.

## Why

Batch II-a of `decision_obligations-route.md` credits five requirements, each on its own case. A case's normative input is a retained excerpt whose wrapper names the original page's digest, and that digest must be the case's source publication (`review_div_capture.check_retained_input`, `P4-SYSTEM.14` a44-2c). `REQ-GC-COUNTERS` rests on `RVI-ZICNTR-STATEMENTS`, retained for the ZICNTR case; the other four name pages nothing held.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `priv/machine.html` (RVP-MACHINE, `sources.sexp`) | `b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea` | 271851 |
| `unpriv/zicsr.html` (RVI-ZICSR, `sources.sexp`) | see `scripts/retain_statements.py` | 44903 |
| `unpriv/zifencei.html` (RVI-ZIFENCEI, `sources.sexp`) | see `scripts/retain_statements.py` | 32380 |
| `unpriv/c-st-ext.html` (RVI-C, `sources.sexp`) | see `scripts/retain_statements.py` | 95631 |

Each page pin occurs in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`. That supports retaining the manual text below; it does not establish terms for the served website or its external assets.

## Retention decision

`RVP-ECALL-STATEMENTS`, seven statements: what delegation does (§2.1.1.8); what `mepc`, `mcause` and `mtval` record on a trap (§2.1.1.14 to §2.1.1.16); and what ECALL and EBREAK raise (§2.1.3.1), each anchored on its own paragraph.
`RVI-ZICSR-STATEMENTS`, seven statements of §5.1.1: what CSRRW, CSRRS and CSRRC read and write, and when a form writes nothing.
`RVI-ZIFENCEI-STATEMENTS`, one statement of §4.1: what FENCE.I orders.
`RVI-C-STATEMENTS`, two statements of §27.1: where an instruction may start with C present, and what no longer raises an exception.

The tool's selection did not change. Not retained: the immediate CSR forms' own paragraph, `norm:csrrwi_csrrsi_csrrci_ops`, which carries a nested span the tool's markup bound refuses, so it is cited, not retained; the reserved FENCE.I encodings; and the C forms themselves, which `REQ-GC-C`'s case will name.

Curated inputs under `profiles/rv64gc-lab-v0/retained/`: `rvp-ecall-statements.html`, 3,897 B; `rvi-zicsr-statements.html`, 4,669 B; `rvi-zifencei-statements.html`, 1,622 B; `rvi-c-statements.html`, 1,981 B, each pinned in `scripts/retain_statements.py`.
Regenerate with `python3 scripts/retain_statements.py --emit <id>` using the acquired pages; check the tracked assets without that cache using `--verify`. The excerpts establish no acceptance; each case's declaration, capture, reviews and credit are their own units.
