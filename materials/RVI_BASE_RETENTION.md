# Retained RV32I and RV64I base statements: source terms and scope

Owner: `P4-SYSTEM.14` a46-1 (2026-11-06); SRC-01 review before retaining a primary-source input. The licence finding and the wrapper's
attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`), and the unprivileged volume's terms were reviewed there; this record adds two excerpts to the same table.

## Why

Batch I of `decision_obligations-route.md` credits nine base requirements, each on its own case. A case's normative input is a retained excerpt whose wrapper names the original page's digest, and that digest must be the case's source publication (`review_div_capture.check_retained_input`, `P4-SYSTEM.14` a44-2c).
Five of the nine name RVI-RV32I (`REQ-D-ALU-IMM`, `REQ-D-ALU-REG`, `REQ-D-JALR-LSB`, `REQ-D-NO-DELAY-SLOTS`, `REQ-D-LOAD-X0`), and RV64I §3.1 inherits those statements at XLEN 64. Two name RV64I statements `RVI-RV64I-STATEMENTS` does not hold (`REQ-D-LUI-AUIPC`, `REQ-D-LOAD-EXT`). `REQ-D-SHAMT` and `REQ-D-WSUFFIX` rest on that older excerpt, which already holds them.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `unpriv/rv32.html` (RVI-RV32I, `sources.sexp`) | `3b20e92f067509535f95883832e84b32dbea43a29e1347b7925c374213ad75ec` | 107630 |
| `unpriv/rv64.html` (RVI-RV64I, `sources.sexp`) | `6eadb316c2d535ccb87a7a6feb03ff54af6f4b5bbeb5c1a5102a02af81f13abd` | 49246 |
| `unpriv/colophon.html` (the unprivileged volume's licence evidence) | `7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c` | 112487 |

Each page pin occurs in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`. That supports retaining the manual text below; it does not establish terms for the served website or its external assets.

## Retention decision

`RVI-RV32I-STATEMENTS`, twenty statements in source order: that immediates are sign-extended (§1.1.2); what ADDI, SLTI, SLTIU, ANDI, ORI and XORI do, and that overflow is ignored (§1.1.4.1); what ADD, SUB, SLT, SLTU, AND, OR and XOR do (§1.1.4.2); that control transfers have no delay slots (§1.1.5); how JAL and JALR form a target and a link (§1.1.5.1); how a branch forms its target and when each takes it (§1.1.5.2); and that a load to `x0` still raises its exceptions (§1.1.6).
`RVI-RV64I-FORMS-STATEMENTS`, six statements: AUIPC at 64 bits (§3.1.2.1), and what each load and store width does (§3.1.3).

The tool's selection did not change: each is a `norm:` span, quoted unmodified under the same markup allowlist and byte bound.

Not retained: the misaligned-access, fence, ecall and hint statements of §1.1.6 to §1.1.8, which later batches name as they need them, and `norm:slliw_srliw_sraiw_imm5_rsv`, because a reserved encoding is not witnessed here.

Curated inputs: `profiles/rv64gc-lab-v0/retained/rvi-rv32i-statements.html`, 6,428 B, SHA256 `c476fd879407a93271d504e8cff80bdae93822d8319951b1252485715e0256ef`;
`profiles/rv64gc-lab-v0/retained/rvi-rv64i-forms-statements.html`, 2,993 B, SHA256 `f254c3fe90773b67f282984d61498f2f1008ffe214b8bc952baa628189b5d816`.
Regenerate with `python3 scripts/retain_statements.py --emit <id>` using the acquired pages; check the tracked assets without that cache using `--verify`; the controls are
`scripts/probe_statement_retention.py` (21 tests, nine guard omissions in PROFILE-CONSISTENCY). The excerpts establish no acceptance; each case's declaration, capture, reviews and credit are later units.
