<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/sifive-uart-lab-v0/profile.sexp`  `a44a7ddbff330cdec752e2541f95b2288e4bf4c333878c910a7d25be4695f401`
     `profiles/sifive-uart-lab-v0/state.sexp`  `60206ed9b8b95accd5102ab303dacfcd2e1e0e90449768ce4a2bc4be1574c071`
     `profiles/sifive-uart-lab-v0/requirements.sexp`  `110876c5e3190c3ff2bdc7526ad05f4e33fcd7f3152d28b90285ce1e29cfb4d3`
     `profiles/sifive-uart-lab-v0/contract-obligations.sexp`  `2042125eee217e78c065f408247ba6cfdd29f0c19ebc8bb85e5492e43222d96f`
     `profiles/sifive-uart-lab-v0/sources.sexp`  `f723943561eba48d768d48be6e668b4998274e8d97f89b4315479bce1cc4a016`
     Generator: `scripts/gen_model_book.py` (sha256 `2f062f639b366734683fc5121779bd446fef1ac3c66b7766326deb9f92b855a2`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 19 decisions, 7 declared scope registers |
| `state.sexp` | the device-state census, including the hidden-state census | 7 registers, 2 FIFO families, hidden state: The two FIFOs' contents and occupancies, and nothing else. Every other hardware state the chapter implies is invisible at the MMIO boundary: the register map exposes no counter, shift register, sampler or pin-latch readout, and the board's backends (recorded input on RX, host console on TX) move whole bytes, so wire timing can never become an MMIO observation. |
| `requirements.sexp` | the predeclared requirements, one per decision (RECORD-SCHEMA cross-checks the statements verbatim) | 19 requirements |
| `contract-obligations.sexp` | the device contract (`sifive-uart-v0`): every obligation with positive AND negative checks | 19 obligations, 38 declared checks |
| `expectations/` | the EVD-05 register-read corpus: datasheet-derived expectations recorded before any model exists | 3 documents, 17 expected steps |

This unit declares `(route device-model)`: it carries no `encoding.sexp` (a device has no instruction encodings), no `guests/` corpus (the expectations are the corpus) and no `interactions.sexp` (INTERACTION-MATRIX derives the route from the declaration — the matrix attaches with the probe corpus, P5-BOARD.5). The absences are the shape, not gaps.
