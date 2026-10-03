<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/lan9118-lab-v0/profile.sexp`  `dab007291ac812efc71c500e774cdf823240f296e86636cc49f76429c0adb288`
     `profiles/lan9118-lab-v0/state.sexp`  `e7b9c2b04155bc2fff6ff4e16fd78f45021e072ed64146d6c495eb460e1a40e2`
     `profiles/lan9118-lab-v0/requirements.sexp`  `705c93d1c6676beb5d0322d69590a11a794f543f416b5feaedba28494642f781`
     `profiles/lan9118-lab-v0/contract-obligations.sexp`  `5525c294ee520283a31b82c43a381173ef2482a93991f99d79811fab6cb04beb`
     `profiles/lan9118-lab-v0/sources.sexp`  `eee2e26aac26903c0beec6ae72232bca49b7d79998fa2e01de12a6f244b4479b`
     Generator: `scripts/gen_model_book.py` (sha256 `2f062f639b366734683fc5121779bd446fef1ac3c66b7766326deb9f92b855a2`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 52 decisions, 28 declared scope registers |
| `state.sexp` | the device-state census, including the hidden-state census | 49 registers, 4 FIFO families, hidden state: The four FIFOs' contents and occupancies, the TX command-parser state, and the counter values the composition freezes — and nothing else. Every other hardware state the datasheet implies is either register-carried (the synchronizer busy bits, the dump/fast-forward self-clearing bits) or invisible at the MMIO boundary: the MIL FIFOs are 'not visible to the host processor' by the datasheet's own words, and the wire-domain machines (PHY link training, auto-negotiation, the analog front end) surface only through PHY register bits whose scene the replay backend declares (REQ-D-NIC-PHY-LINK). |
| `requirements.sexp` | the predeclared requirements, one per decision (RECORD-SCHEMA cross-checks the statements verbatim) | 52 requirements |
| `contract-obligations.sexp` | the device contract (`lan9118-v0`): every obligation with positive AND negative checks | 52 obligations, 104 declared checks |
| `expectations/` | the EVD-05 register-read corpus: datasheet-derived expectations recorded before any model exists | 3 documents, 27 expected steps |

This unit declares `(route device-model)`: it carries no `encoding.sexp` (a device has no instruction encodings), no `guests/` corpus (the expectations are the corpus) and no `interactions.sexp` (INTERACTION-MATRIX derives the route from the declaration — the matrix attaches with the probe corpus, P5-BOARD.5). The absences are the shape, not gaps.
