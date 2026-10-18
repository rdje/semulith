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
