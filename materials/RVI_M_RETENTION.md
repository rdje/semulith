# Retained DIV statement: source terms and scope

Owner: `P4-SYSTEM.14` a42z; SRC-01 review before retaining a primary-source input.

## Finding and root cause

The `RVI-PINNED-V20260120` catalogue record said served pages carry only a
copyright footer and no CC-BY statement. That snapshot-wide absence claim was
introduced in `3afd2757de464f499b3e3d25a7c35b70de662b17`. Its cited evidence was
the website footer. It did not account for the manual prefaces: the pinned
unprivileged colophon contains a CC-BY4.0 statement in its preface to Version2.2,
covering that manual and future versions. The privileged preface contains a
corresponding statement for its own volume. These are counterexamples inside
the same snapshot, rather than terms inferred from another publication's PDF.

The defect is the scope of the catalogue's evidence: a footer cannot establish
the absence of a licence statement elsewhere in a multi-page publication. The
history establishes where the claim entered; it does not establish which other
pages the original investigator read. Correct the live claim and retain history.

## Reviewed source identities

| Input | SHA256 | Bytes |
| --- | --- | --- |
| Snapshot SHA256SUMS | `f77463370c2fe52513a9803917c30b717f6169f2164d0c848b85c2fcd817530b` | 6229 |
| `unpriv/m-st-ext.html` | `85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716` | 35588 |
| `unpriv/colophon.html` | `7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c` | 112487 |

The two page pins occur in that manifest. The cache is the existing public
materials route, `.materials/riscv/pinned-v20260120/`; no other repository is
modified. The unprivileged licence-evidence page is the
[same publication's colophon](https://docs.riscv.org/reference/isa/v20260120/unpriv/colophon.html).
Its historical preface explicitly extends the stated licence to future manual
versions. This supports retaining the manual text identified below; it does not
establish terms for the entire served website or the external diagram assets.

## Retention decision

Retain only the exact `norm:div_divu_op` span from
[M Version2.0 §11.1.2](https://docs.riscv.org/reference/isa/v20260120/unpriv/m-st-ext.html).
It supplies the signed/unsigned XLEN division and rounding-toward-zero statement
needed by the finite `-7 / 2 = -3` witness. It supplies no other M acceptance.

The quoted manual text is CC-BY4.0. The new wrapper retains the copyright notice, identifies RISC-V
International and the original manual authors, links the source and licence,
records both original page digests and the extraction tool, states the omissions
and preserves the selected span's bytes. This implements the licence's
[reproduction and attribution conditions, §§2(a),3(a)](https://creativecommons.org/licenses/by/4.0/legalcode.en).
The project adds no endorsement claim or restrictions to the licensed text.
Website navigation, scripts, styles, diagrams and footer are omitted. The
wrapper is project-authored; the retained manual statement keeps its own terms.

Curated input: `profiles/rv64gc-lab-v0/retained/div-statement.html`,1576B,
SHA256 `bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58`.
Its fingerprint differs from the original page, deliberately. Regenerate with
`python3 scripts/retain_div_statement.py --emit` using the acquired source pages;
check the tracked asset without that cache using `--verify`. The pure emitter
checks both complete input pins, selects one exact span and adds a deterministic
wrapper. The verifier uses the existing anchored snapshot reader.

This is a scoped redistribution decision for one licensed statement. The full
HTML snapshot remains untracked; the other specification artifacts' terms and
profile release questions remain open. No reference binary is redistributed.

## Integration frontier

P4-SYSTEM.14 a42aa adopts the retained excerpt in
`rv64gc-signed-div-truncation-v2`, under `RVI-M-DIV-STATEMENT` with its own path
and digest. Current source authority keeps `RVI-M` and the original publication
digest. The binding refuses substitution in either direction. The reviewed
population includes the extraction producer; composition controls authenticate
the actual tracked excerpt without an acquired materials cache. The source text,
wrapper and licence decision above are unchanged by this integration.

Canonical capture, the full retention family and policy qualification remain
pending. This finite source/artifact binding changes no requirement status.

## Second scoped retention: the other eleven statements and Table 1 (a42bb)

`P4-SYSTEM.14` a42bb, 2026-10-23. The m-forms case (`rv64gc-m-forms-v3`) predeclares 25 properties:
thirteen forms and twelve Table 1 cells. Its expectations cite §11.1.1, §11.1.2 and Table 1, but only
the DIV/DIVU statement above was retained; a credit resting on the other statements would rest on
cited, unretained text. The same pinned page and licence evidence support retaining, in one new
attributed wrapper, the eleven other normative spans and Table 1:

| Span (`<span id=…>`) | Section | Bytes |
| --- | --- | --- |
| `norm:mul_op` | §11.1.1 | 179 |
| `norm:mulh_mulhu_mulhsu_op` | §11.1.1 | 267 |
| `norm:mulw_op` | §11.1.1 | 210 |
| `norm:rem_remu_op` | §11.1.2 | 110 |
| `norm:rem_result_sign` | §11.1.2 | 109 |
| `norm:divw_divuw_op` | §11.1.2 | 286 |
| `norm:remw_remuw_op` | §11.1.2 | 146 |
| `norm:remw_remuw_result_sign` | §11.1.2 | 145 |
| `norm:div_by_zero` | §11.1.2 | 84 |
| `norm:rem_by_zero` | §11.1.2 | 89 |
| `norm:signed_div_overflow` | §11.1.2 | 231 |
| `<table id="divby0">` (Table 1, with its caption) | §11.1.2 | 1,698 |

The quoted text is the same CC-BY 4.0 manual text as the DIV statement, under the same licence
evidence (the unprivileged preface whose statement covers future versions); the wrapper carries the
same attribution, links, both original page digests and the transformation's name, and states the
omissions. Only static markup is retained: `<code>` inside the spans; table structure, `<p>`, `<br>`,
`<em>`, `<sup>`, and `class`/`id`/`style` attributes where every style is a column width. Anything
else refuses. The DIV/DIVU span is not repeated.

Curated input: `profiles/rv64gc-lab-v0/retained/m-statements.html`, identity `RVI-M-STATEMENTS`
(bytes and SHA256 in `scripts/retain_m_statements.py`, `RETAINED_SHA`). Regenerate with
`python3 scripts/retain_m_statements.py --emit` from the acquired pages; check the tracked asset
without them using `--verify`. The emitter reads the source and licence pins from
`scripts/retain_div_statement.py`, their one owner, which does not change: it is a pinned input of
the retained case. The new file is not one of the case's 64 pinned inputs, so retaining it
invalidates nothing; a crediting record cites it by identity. This remains a scoped redistribution
decision for these statements and this table; the full snapshot stays untracked and the other
specification artifacts' terms remain open.
