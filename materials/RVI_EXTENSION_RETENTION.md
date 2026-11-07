# Retained A, C, F and D statements: source terms and scope

Owner: `P4-SYSTEM.14` a48-1 (2026-11-06); SRC-01 review before retaining a primary-source input. The licence finding and the wrapper's
attribution scheme are the M retention's (`materials/RVI_M_RETENTION.md`); this record adds four excerpts to the same table.

## Why

Batch II-b of `decision_obligations-route.md` credits four requirements, each on its own case. A case's normative input is a retained excerpt whose wrapper names the original page's digest, and that digest must be the case's source publication.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `unpriv/a-st-ext.html` (RVI-A, `sources.sexp`) | `afbd8def7bdf64287ef51a9cb14dd654fba0f0cfeef63bccdfd47408f5b0dff2` | 56889 |
| `unpriv/c-st-ext.html` (RVI-C, `sources.sexp`) | `3f7e7d853d6e12e9d44c3d1bb488d1c312179a308d608182fb01db43a49d6aeb` | 95631 |
| `unpriv/f-st-ext.html` (RVI-F, `sources.sexp`) | `8e42e6ae9b3ab18fcf9c3d4f26a1a251310e3fd08b67368235fb5e9affd32edd` | 70860 |
| `unpriv/d-st-ext.html` (RVI-D, `sources.sexp`) | `fe3beb3c4db381063bccf03f5451d0a6184100ac37bb39b4dd1ec726a2befde4` | 40001 |

Each page pin occurs in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`. That supports retaining the manual text below; it does not establish terms for the served website or its external assets.

## Retention decision

`RVI-A-STATEMENTS`, ten statements: LR and SC, what ends a reservation, a word AMO's operands, and that compressed forms are allowed in a constrained loop.
`RVI-C-FORMS-STATEMENTS`, thirteen statements: control transfers, the scaled stack forms, what is reserved, and what a HINT leaves alone.
`RVI-F-STATEMENTS`, thirteen statements: reserved rounding modes, the canonical NaN, tininess, what the transfers keep, how conversions clip, and how compares signal.
`RVI-D-STATEMENTS`, ten statements: NaN boxing, what the transfers keep, the two format conversions, and how the double forms read their single counterparts.

The tool's selection did not change. Not retained: the accrued-flags and rounding-mode paragraphs of §20.1.2, which carry links the tool's markup bound refuses; the conversion and classify tables, which are not statements; the misaligned atomic rule, which `REQ-D-ATOMIC-MISALIGN` owns; and RVP-SUPERVISOR's translation text. Each is cited, not retained.

Curated inputs under `profiles/rv64gc-lab-v0/retained/`: `rvi-a-statements.html`, 4,452 B; `rvi-c-forms-statements.html`, 6,346 B; `rvi-f-statements.html`, 6,368 B; `rvi-d-statements.html`, 4,708 B, each pinned in `scripts/retain_statements.py`.
Regenerate with `python3 scripts/retain_statements.py --emit <id>` using the acquired pages; check the tracked assets without that cache using `--verify`. The excerpts establish no acceptance; each case's declaration, capture, reviews and credit are their own units.

## The seven's four excerpts (`P4-SYSTEM.14` a50-2, 2026-11-06)

### Why

The seven requirements of `decision_seven-with-a-switch.md` each need a case, and a case's normative input is a retained excerpt whose wrapper names the original page's digest.

### Reviewed source identities

Each page's pin is in `scripts/retain_statements.py` and `profiles/rv64gc-lab-v0/sources.sexp`, and occurs in the snapshot manifest; the cache is the existing materials route, `.materials/riscv/pinned-v20260120/`: `priv/priv-intro.html` (RVP-INTRO), `priv/supervisor.html` (RVP-SUPERVISOR), `priv/machine.html` (RVP-MACHINE) and `unpriv/a-st-ext.html` (RVI-A). That supports retaining the manual text below; it does not establish terms for anything else on those pages.

### Retention decision

`RVP-MODES-STATEMENTS`, four statements: the privilege levels and what each is for.
`RVP-TRANSLATION-STATEMENTS`, eleven statements: an unsupported MODE, the A and D schemes, and what Sv39 is.
`RVP-PRIORITY-STATEMENTS`, one statement: the one position the priority table leaves open.
`RVI-A-RESERVATION-STATEMENTS`, thirteen statements: what a reservation may cover, what an SC needs, and misaligned atomics.

The tool's selection did not change. Not retained: the priority table itself and the opening sentence that points at it, which carry a link the tool's markup bound refuses; and the walk's numbered steps, including the misaligned-superpage step and the Svade step, which are list items the tool does not read. Each is cited by its section and not quoted.

Curated inputs under `profiles/rv64gc-lab-v0/retained/`: `rvp-modes-statements.html`, 3,173 B; `rvp-translation-statements.html`, 4,099 B; `rvp-priority-statements.html`, 1,743 B; `rvi-a-reservation-statements.html`, 5,467 B. Regenerate with `python3 scripts/retain_statements.py --emit <id>` using the acquired pages; check the tracked assets without that cache using `--verify`. The excerpts establish no acceptance.

## The six `defined` cases of the last 17 (`P4-SYSTEM.14` a51-1, 2026-11-07)

### Reviewed source identities

Each page's pin is in `scripts/retain_statements.py` and `profiles/rv64gc-lab-v0/sources.sexp`, and occurs in the snapshot manifest; the cache is the existing materials route.

### Retention decision

`RVI-NAMING-STATEMENTS`, two statements: what the letters name, and what G abbreviates.
`RVI-ZC-STATEMENTS`, four statements: what C decomposes into, and where Zcf exists.
`RVI-RVWMO-STATEMENTS`, one statement: what the memory model is defined over.
`RVP-XRET-STATEMENTS`, nine statements: trap returns, WFI, and the bits that intercept them.

The tool's selection did not change. Not retained: the privileged listings' table and the TVM statement, which the tool's markup bound does not read; the statements of what Zcf and Zcd depend on, which carry links the bound refuses; and SFENCE.VMA's, because a case retains one publication and `rv64gc-priv-forms-v1`'s is the Machine-Level chapter. All are cited.

Curated inputs under `profiles/rv64gc-lab-v0/retained/`: `rvi-naming-statements.html`, 2,310 B; `rvi-zc-statements.html`, 2,438 B; `rvi-rvwmo-statements.html`, 1,852 B; `rvp-xret-statements.html`, 4,367 B.
