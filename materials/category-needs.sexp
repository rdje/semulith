;; category-needs.sexp — the category-needs catalogue (MODEL-METHOD.2). One
;; (category-need …) per docs/INFORMATION_CATALOG.md category per unit; validate with
;;   python3 scripts/check_sexp_schema.py category-needs.sexp schema/category-needs.sexp
;; Dispositions are honest about ABSENT vs NEVER-NEEDED: `missing` (a reason is owed) means
;; the unit requires the category and the catalogue lacks the material; `out-of-scope` means
;; the unit never owed it. This file is the first honest pass — MODEL-METHOD.3 revises every
;; disposition it can evidence better.

(category-need (category "C01") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C02") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C03") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C04") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C05") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C06") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C07") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition missing) (reason "F and D are excluded from this profile; the numerics material that would supply C07 is therefore absent from the catalogue. Reopen with the first F/D unit."))
(category-need (category "C08") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition missing) (reason "V is excluded from this profile; the vector material is absent. Reopen with the first vector unit."))
(category-need (category "C09") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition partial) (reason "In-order, single-hart, one-operation-at-a-time is declared (no interlock or forwarding questions arise); packet/issue-group semantics are absent by construction.") (material "RVI-PINNED-V20260120"))
(category-need (category "C10") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C11") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C12") (layer system) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition missing) (reason "Translation is excluded (no MMU, no S/U modes); the translation material is absent. Reopen with the first translated unit."))
(category-need (category "C13") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition partial) (reason "Code visibility is decided as a laboratory policy (re-fetch every instruction); the Zifencei maintenance questions are absent from this profile by exclusion.") (material "RVI-PINNED-V20260120"))
(category-need (category "C14") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition partial) (reason "Only requested traps (ECALL/EBREAK) exist; interrupt sources, nesting and delivery are all excluded with no privilege modes.") (material "RVI-PINNED-V20260120"))
(category-need (category "C15") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition missing) (reason "Privilege modes beyond M are not modelled; the system-programming material is absent. Reopen with the first privileged unit."))
(category-need (category "C16") (layer system) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition missing) (reason "One hart, no atomics: the memory-consistency and multicore material is absent. Reopen with MC-MULTICORE."))
(category-need (category "C17") (layer board) (kind "datasheet") (unit "rv64i-lab-v0") (disposition out-of-scope) (reason "Reset and time are the harness's concern in this laboratory (the CPU/environment contract owns them); no board exists to supply them."))
(category-need (category "C18") (layer system) (kind "debug-spec") (unit "rv64i-lab-v0") (disposition missing) (reason "No debug entry, trace, or counters exist in this profile (Zicntr/Zihpm excluded); the debug material is absent."))
(category-need (category "C19") (layer board) (kind "datasheet") (unit "rv64i-lab-v0") (disposition out-of-scope) (reason "The laboratory declares exactly one main-memory region and no devices; platform and device documentation is the board's, and no board is modelled."))
(category-need (category "C20") (layer board) (kind "abi-spec") (unit "rv64i-lab-v0") (disposition out-of-scope) (reason "ABI, loader and system-call conventions belong to the environment the board provides; this unit models the processor only."))
(category-need (category "C21") (layer board) (kind "datasheet") (unit "rv64i-lab-v0") (disposition out-of-scope) (reason "External input and co-simulation scheduling are the harness/board's boundary; the processor unit does not own them."))
(category-need (category "C22") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C23") (layer processor) (kind "isa-manual") (unit "rv64i-lab-v0") (disposition covered) (material "RVI-PINNED-V20260120"))
(category-need (category "C24") (layer processor) (kind "model-contract") (unit "rv64i-lab-v0") (disposition partial) (reason "The observation contract declares determinism, replay-relevant state and stop reasons; snapshot/versioning policy is declared for P1, not yet built."))
