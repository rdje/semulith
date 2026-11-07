#!/usr/bin/env python3
"""Policy-leg measurement controls on synthetic retained cases; measurement only, no credit."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "scripts" / "sexp.py").is_file())
MUTATION = None
# Each seam replaces one load-bearing predicate in a copied module; its test must then fail.
SEAMS = {
    "credit-pending": ('    missing = [leg.id for leg in legs if leg.disposition != "satisfied"]\n', '    missing = []\n'),
    "trust-receipt": ('    if receipt.get("qualification") is True and missing:\n', '    if False:\n'),
    "infer-feature": ('    feature = [FEATURE_DISPOSITIONS.get(ob) for ob in obligation_ids]\n',
                      '    feature = [FEATURE_DISPOSITIONS.get(ob, "none applies (inferred)") for ob in obligation_ids]\n'),
    "any-control": ('    at_witness = diff.get("step_n") == witness_step and observed == {witness_register}\n',
                    '    at_witness = True\n'),
    "coverage-optional": ('    _leg(legs, "form-coverage", vacuous or (bool(required) and predeclared == required),\n',
                          '    _leg(legs, "form-coverage", vacuous or bool(required),\n'),
    "trace-optional": ('    _leg(legs, "statement-trace", traced, trace_measured)\n', '    _leg(legs, "statement-trace", True, trace_measured)\n'),
    "state-vacuous": ('    vacuous = requirement["kind"] in ("state", "configuration", "memory") and not required\n', '    vacuous = not required\n'),
    "configuration-vacuous": ('    vacuous = requirement["kind"] in ("state", "configuration", "memory") and not required\n', '    vacuous = requirement["kind"] in ("state", "memory") and not required\n'),
    "memory-vacuous": ('    vacuous = requirement["kind"] in ("state", "configuration", "memory") and not required\n', '    vacuous = requirement["kind"] in ("state", "configuration") and not required\n'),
    # a46-4: a form that writes no GPR is predeclared by a later read, one seam per condition.
    "silent-any-form": ('    silent = {f for f in required if not any(s["writes"] for s in steps.values() if mnemonic(s) == f)}\n', '    silent = set(required)\n'),
    "silent-any-cell": ('if cells.get(pid) == "form:" + f and any(mnemonic(steps[m]) == f for m in steps if m < n)})', 'if any(mnemonic(steps[m]) == f for m in steps if m < n)})'),
    "silent-any-order": ('if cells.get(pid) == "form:" + f and any(mnemonic(steps[m]) == f for m in steps if m < n)})', 'if cells.get(pid) == "form:" + f and any(mnemonic(steps[m]) == f for m in steps)})'),
    "boundary-tag": ('BOUNDARY_MARKERS = ("Table", "(boundary")\n', 'BOUNDARY_MARKERS = ("Table",)\n'),
    "lock-stale": ('    stale = method.get("disposition") == "stale"\n', '    stale = False\n'),
    "first-property": ('    witness_step, witness_register = witnesses[named[0]]\n',
                       '    witness_step, witness_register = next(iter(witnesses.values()))\n'),
    "credit-any": ('    credited_now = any(c["disposition"] == "current" for c in naming)\n',
                   '    credited_now = bool(naming)\n'),
    # a43b-2b: the five conditions of the risk-method leg (P4-SYSTEM.14 a43b-2a, D2), one seam each.
    "both-forms": ('    c1 = second is not None and adversarial is not None and kind in SECOND_METHODS\n', '    c1 = True\n'),
    "distinct-versions": ('    c2 = len(ids) >= 2 and all(i in producers for i in ids) and len(versions) == len(ids)\n',
                          '    c2 = True\n'),
    "recorded-common": ('    c3 = bool(joined) and len(found) == len(joined) and bool(common) and shared == common\n',
                        '    c3 = True\n'),
    "shared-pair": ('    c4 = bool(found) and "shared" not in ancestry and bool(derived)\n', '    c4 = True\n'),
    "adversarial-executed": ('    c5 = bool(props) and set(props) <= set(witnesses) and baseline == "AGREE"\n', '    c5 = True\n'),
    # a43b-3g: the category row of the matched comparison, one seam per judgement.
    "category-row": ('    row, row_measured = _category_row(root, case_dir, profile_dir, case_id, requirement["source_semantics"], expectation_path,\n'
                     '                                      producers, declared_steps, requirement["id"], named[0])\n', '    row, row_measured = True, ""\n'),
    "source-specific-absent": ("""        if declared is None:\n            return False, f"; category {category}: {unreadable or f'no disposition declared for {requirement_id}'}"\n""", """        if declared is None:\n            return True, ""\n"""),
    "implementation-disposition": ("""        if declared is not None:\n            held, measured = _disposition_row(declared,""", """        if False:\n            held, measured = _disposition_row(declared,"""),
    "source-specific-kind": ('    if row["kind"] != "case":\n', '    if False:\n'),
    "source-specific-control": ('    if row["control_property"] != control_property:\n', '    if False:\n'),
    "walk-absent": ('    if not record_path.is_file():\n        return False, "no retained page-table comparison"\n', '    if not record_path.is_file():\n        return True, ""\n'),
    "walk-guest": ('("the guest", _one(record, "guest_sha256") == _digest(_bounded_bytes(case_dir / "guest.elf"))),\n            ("the case\'s configuration", _one(record, "case_config_sha256") == _digest(_bounded_bytes(case_dir / "reference-config.json")))', '("the guest", True),\n            ("the case\'s configuration", _one(record, "case_config_sha256") == _digest(_bounded_bytes(case_dir / "reference-config.json")))'),
    "walk-trace": ('("the reference\'s trace", _one(record, "reference_trace_sha256") == _digest(reference))', '("the reference\'s trace", True)'),
    "walk-compare": ('        return Walk.compare(reference.decode("utf-8"), engine.decode("utf-8"))\n', '        return True, ""\n'),
    "selection-recorded": ('        selection = bool(str(semantics.get("detail") or "").strip())\n', '        selection = True\n'),
    "unknown-category": ('    return False, f"; category {category}: no row measured for it here"\n', '    return True, ""\n'),
    "effect-case": ('("its case", _one(record, "case_id") == case_id)', '("its case", True)'),
    "effect-guest": ('("the guest", _one(record, "guest_sha256") == _digest(_bounded_bytes(case_dir / "guest.elf")))', '("the guest", True)'),
    "effect-config": ('("the case\'s configuration", _one(record, "case_config_sha256") == case_config)', '("the case\'s configuration", True)'),
    "effect-binary": ('("the reference producer\'s binary", reference is not None and f"sha256:{_one(record, \'binary_sha256\')}" == str(_one(reference, "version")))',
                      '("the reference producer\'s binary", True)'),
    "effect-differs": ('("a different configuration", alternative != case_config)', '("a different configuration", True)'),
    "effect-override": ('(named, alternative == _digest(declared)),', '(named, True),'),
    "effect-declared-refused": ('        return False, f"the case\'s declared alternative refuses: {refused}"\n', '        declared, named = b"", "nothing"\n'),
    "effect-trace": ('("its trace", _one(record, "trace_sha256") == _digest(trace) and _one(record, "trace_bytes") == len(trace))', '("its trace", True)'),
    "effect-diverges": ('    if result.verdict != "DIVERGE" or difference is None:\n',
                        '    if difference is None:\n        return True, "observed effect"\n    if False:\n'),
    "effect-at-witness": ('    if difference.step_n not in declared_steps:\n', '    if False:\n'),
}
MUTATION_TESTS = {
    "credit-pending": "test_undeclared_boundary_rows_keep_the_case_pending",
    "trust-receipt": "test_receipt_claiming_qualification_is_a_finding",
    "infer-feature": "test_undeclared_feature_disposition_is_pending",
    "any-control": "test_control_diverging_elsewhere_is_pending",
    "coverage-optional": "test_partial_form_coverage_is_pending",
    "lock-stale": "test_stale_method_is_invalidated_not_blocked",
    "first-property": "test_control_leg_reads_the_property_the_control_run_names",
    "credit-any": "test_lapsed_credit_is_a_finding_and_credits_nothing",
    "trace-optional": "test_a_requirement_with_no_statement_trace_stays_pending",
    "state-vacuous": "test_state_requirement_without_forms_is_vacuous_but_explicit",
    "configuration-vacuous": "test_a_configuration_requirement_naming_no_form_is_vacuous_too",
    "memory-vacuous": "test_a_memory_requirement_naming_no_form_is_vacuous_too",
    "silent-any-form": "test_a_form_that_writes_a_gpr_gets_no_later_read",
    "silent-any-cell": "test_a_silent_form_no_cell_names_stays_pending",
    "silent-any-order": "test_a_silent_form_read_before_its_step_stays_pending",
    "boundary-tag": "test_boundary_tag_marks_a_directed_row",
    "both-forms": "test_second_method_names_one_of_the_policy_methods",
    "distinct-versions": "test_second_method_producers_have_distinct_versions_at_any_risk",
    "recorded-common": "test_second_method_common_inputs_are_the_recorded_shared_inputs",
    "shared-pair": "test_second_method_never_rests_on_a_pair_recorded_as_shared",
    "adversarial-executed": "test_adversarial_case_names_declared_properties_of_an_agreeing_capture",
    "category-row": "test_implementation_defined_without_a_retained_effect_is_pending",
    "selection-recorded": "test_implementation_defined_with_no_recorded_selection_is_pending",
    "unknown-category": "test_a_category_with_no_branch_is_pending_and_named",
    "source-specific-absent": "test_source_specific_with_no_disposition_is_pending",
    "implementation-disposition": "test_implementation_defined_with_a_disposition_is_read_by_it",
    "source-specific-kind": "test_source_specific_closing_through_a_record_is_pending_on_a_case",
    "source-specific-control": "test_source_specific_naming_another_control_is_pending",
    "walk-absent": "test_a_disposition_asking_for_walks_with_none_retained_is_pending",
    "walk-guest": "test_a_walk_record_of_another_guest_is_pending",
    "walk-trace": "test_a_walk_trace_that_moved_is_pending",
    "walk-compare": "test_a_walk_comparison_that_does_not_hold_is_pending",
    "effect-case": "test_a_retained_effect_for_another_case_is_pending",
    "effect-guest": "test_a_retained_effect_of_another_guest_is_pending",
    "effect-config": "test_a_retained_effect_of_another_case_configuration_is_pending",
    "effect-binary": "test_a_retained_effect_of_another_binary_is_pending",
    "effect-differs": "test_a_retained_effect_with_no_configuration_of_its_own_is_pending",
    "effect-override": "test_a_retained_effect_under_another_configuration_is_pending",
    "effect-declared-refused": "test_a_case_whose_declared_alternative_refuses_is_pending",
    "effect-trace": "test_a_retained_effect_whose_trace_moved_is_pending",
    "effect-diverges": "test_a_retained_effect_that_agrees_is_pending",
    "effect-at-witness": "test_a_retained_effect_differing_at_no_declared_step_is_pending",
}
XLEN_CASE_ID = "rv64gc-xlen-forms-v4"  # the XLEN case's reviewed capture: xlen-v1 (a43a-2f), xlen-v2 (a43b-2e), xlen-v3 (a43e-5), xlen-v4 (a49-3)
CSR_CASE_ID = "rv64gc-csr-set-v3"  # the first implementation-defined case (a43b-3g), re-captured as v2 (a43e-5) and v3 (a49-3)
ZICNTR_CASE_ID = "rv64gc-zicntr-v3"  # the second, on the same configuration (a43c-5), re-captured as v2 (a43e-5) and v3 (a49-3)
SSTC_CASE_ID = "rv64gc-sstc-v2"  # the third, and the first with a delivered interrupt (a43e-5), re-captured as v2 (a49-3)
# G-OBLIGATIONS' Batches I, II-a and II-b, re-issued or credited at a49-3: the requirement each case binds, and the forms that write no GPR, so a later read predeclares them.
BATCH_I = {"rv64gc-alu-imm-v2": ("REQ-D-ALU-IMM", "OB-ALU-IMM", "low"), "rv64gc-alu-reg-v2": ("REQ-D-ALU-REG", "OB-ALU-REG", "low"), "rv64gc-lui-auipc-v2": ("REQ-D-LUI-AUIPC", "OB-LUI-AUIPC", "medium"), "rv64gc-jalr-lsb-v2": ("REQ-D-JALR-LSB", "OB-JALR-LSB", "medium"), "rv64gc-no-delay-slots-v2": ("REQ-D-NO-DELAY-SLOTS", "OB-NO-DELAY-SLOTS", "low"), "rv64gc-shamt-v2": ("REQ-D-SHAMT", "OB-SHAMT", "high"), "rv64gc-wsuffix-v2": ("REQ-D-WSUFFIX", "OB-WSUFFIX", "high"), "rv64gc-load-ext-v2": ("REQ-D-LOAD-EXT", "OB-LOAD-EXT", "high"), "rv64gc-load-x0-v2": ("REQ-D-LOAD-X0", "OB-LOAD-X0", "high"), "rv64gc-ecall-ebreak-v2": ("REQ-D-ECALL-EBREAK", "OB-GC-ECALL-EBREAK-V3", "high"), "rv64gc-csr-access-v2": ("REQ-GC-CSR-ACCESS", "OB-GC-CSR-ACCESS", "high"), "rv64gc-counters-v2": ("REQ-GC-COUNTERS", "OB-GC-COUNTERS", "medium"), "rv64gc-fencei-v2": ("REQ-GC-FENCEI", "OB-GC-FENCEI", "low"), "rv64gc-ialign-16-v2": ("REQ-D-IALIGN-16", "OB-IALIGN-16", "medium"), "rv64gc-atomics-v1": ("REQ-GC-ATOMICS", "OB-GC-ATOMICS", "high"), "rv64gc-c-forms-v1": ("REQ-GC-C", "OB-GC-C", "medium"), "rv64gc-f-forms-v1": ("REQ-GC-F", "OB-GC-F", "high"), "rv64gc-d-forms-v1": ("REQ-GC-D", "OB-GC-D", "high")}
# The seven with a switch, credited at a50-4: each binds its requirement and reads its first difference from the retained effect.
SWITCHES = {"rv64gc-svade-v1": ("REQ-D-SVADE", "OB-SVADE", "medium", "its declared alternative", "step 93 (csrrs x22, scause, x0): Sail {}, expectations {'x22': 13}"), "rv64gc-atomic-misalign-v1": ("REQ-D-ATOMIC-MISALIGN", "OB-ATOMIC-MISALIGN", "medium", "its declared alternative", "step 24 (csrrs x30, mcause, x0): Sail {'x30': 4}, expectations {'x30': 5}"), "rv64gc-fault-priority-v1": ("REQ-D-FAULT-PRIORITY", "OB-GC-FAULT-PRIORITY-V2", "medium", "its declared alternative", "step 159 (csrrs x22, scause, x0): Sail {'x22': 13}, expectations {'x22': 4}"), "rv64gc-priv-modes-v1": ("REQ-D-PRIV-MODES", "OB-PRIV-MODES", "high", "its declared alternative", "step 5 (csrrs x5, misa, x0): Sail {'x5': 9223372036855828781}, expectations {'x5': 9223372036856090925}"), "rv64gc-sv39-v1": ("REQ-D-SV39", "OB-SV39", "high", "its declared alternative", "step 17 (csrrs x5, satp, x0): Sail {'x5': 10376293541462147075}, expectations {'x5': 0}"), "rv64gc-reservation-v1": ("REQ-D-RESERVATION", "OB-GC-RESERVATION-V2", "medium", "the profile override", "step 23 (sc.w x15, x6, (x3)): Sail {'x15': 0}, expectations {'x15': 1}"), "rv64gc-sc-deterministic-v1": ("REQ-D-SC-DETERMINISTIC", "OB-GC-SC-DETERMINISTIC-V2", "medium", "the profile override", "step 21 (sc.w x15, x6, (x3)): Sail {'x15': 0}, expectations {'x15': 1}")}
# The six `defined` of the last 17, credited at a51-3.
LAST_DEFINED = {"rv64gc-composition-v1": ("REQ-D-GC-COMPOSITION", "OB-GC-COMPOSITION", "low"), "rv64gc-ext-closure-v1": ("REQ-D-EXT-CLOSURE", "OB-EXT-CLOSURE", "medium"), "rv64gc-priv-revision-v1": ("REQ-D-PRIV-REVISION", "OB-PRIV-REVISION", "low"), "rv64gc-rvwmo-v1": ("REQ-D-RVWMO", "OB-RVWMO", "medium"), "rv64gc-priv-insns-v1": ("REQ-D-PRIV-INSNS", "OB-PRIV-INSNS", "medium"), "rv64gc-priv-forms-v1": ("REQ-GC-PRIV-INSNS", "OB-GC-PRIV-INSNS-V3", "high")}
# The two with a switch of the last 17, credited at a51-6.
LAST_SWITCHES = {"rv64gc-no-h-v1": ("REQ-D-NO-H", "OB-NO-H", "low", "its declared alternative", "step 5 (csrrs x5, misa, x0): Sail {'x5': 9223372036856091053}, expectations {'x5': 9223372036856090925}"), "rv64gc-no-pmp-v1": ("REQ-D-NO-PMP", "OB-NO-PMP", "low", "its declared alternative", "step 22 (ld x7, x1, 0): Sail {}, expectations {'x7': 66}")}
# The four with no switch of the last 17, credited at a51-10: each row reads a declared disposition in place of an effect.
NO_SWITCH = {"rv64gc-endian-v1": ("REQ-D-ENDIAN", "OB-ENDIAN", "medium", "DS-ENDIAN", "byte-0"), "rv64gc-fence-v1": ("REQ-D-FENCE", "OB-FENCE", "medium", "DS-FENCE", "fence-fm-reserved"), "rv64gc-walk-implicit-v1": ("REQ-D-WALK-IMPLICIT", "OB-WALK-IMPLICIT", "high", "DS-WALK-IMPLICIT", "walk-three"), "rv64gc-partial-progress-v1": ("REQ-GC-PARTIAL-PROGRESS", "OB-GC-PARTIAL-PROGRESS", "high", "DS-PARTIAL-PROGRESS", "load-rd-kept")}
READ_AFTER = {"rv64gc-no-delay-slots-v2": ["beq", "bge", "bgeu", "blt", "bltu", "bne"], "rv64gc-load-ext-v2": ["sb", "sd", "sh", "sw"], "rv64gc-load-x0-v2": ["lb", "lbu", "ld", "lh", "lhu", "lw", "lwu"], "rv64gc-ecall-ebreak-v2": ["ebreak", "ecall"], "rv64gc-fencei-v2": ["fence.i"], "rv64gc-c-forms-v1": ["c.beqz", "c.bnez", "c.ebreak", "c.fld", "c.fldsp", "c.fsd", "c.fsdsp", "c.j", "c.jr", "c.nop", "c.sd", "c.sdsp", "c.sw", "c.swsp"], "rv64gc-f-forms-v1": ["fadd.s", "fcvt.s.l", "fcvt.s.lu", "fcvt.s.w", "fcvt.s.wu", "fdiv.s", "flw", "fmadd.s", "fmax.s", "fmin.s", "fmsub.s", "fmul.s", "fmv.w.x", "fnmadd.s", "fnmsub.s", "fsgnj.s", "fsgnjn.s", "fsgnjx.s", "fsqrt.s", "fsub.s", "fsw"], "rv64gc-d-forms-v1": ["fadd.d", "fcvt.d.l", "fcvt.d.lu", "fcvt.d.s", "fcvt.d.w", "fcvt.d.wu", "fcvt.s.d", "fdiv.d", "fld", "fmadd.d", "fmax.d", "fmin.d", "fmsub.d", "fmul.d", "fmv.d.x", "fnmadd.d", "fnmsub.d", "fsd", "fsgnj.d", "fsgnjn.d", "fsgnjx.d", "fsqrt.d", "fsub.d"], "rv64gc-priv-insns-v1": ["mret", "sfence.vma", "sret", "wfi"], "rv64gc-priv-forms-v1": ["mret", "sfence.vma", "sret", "wfi"]}
OVERRIDE = "profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp"
BINARY = "b" * 64
METHOD = dict(disposition="satisfied", capture_binding="matched", record_disposition="valid",
              charged_read_bytes=1, record_sha256="a", planned_sha256="b")
STALE = dict(METHOD, disposition="stale", capture_binding=None, record_disposition=None,
             reason="evidence/cx/dependencies.sexp: pinned bytes differ")


def moved_inputs(root: Path, case_id: str) -> list[str]:
    """Pinned inputs whose current bytes differ from the case's manifest — read independently of the method."""
    sys.path.insert(0, str(root / "scripts"))
    import sexp as S
    forms = S.parse((root / "evidence" / case_id / "dependencies.sexp").read_text())
    manifest = next(f for f in forms if isinstance(f, list) and f and str(f[0]) == "dependencies")
    moved = []
    for item in S.children(manifest, "input"):
        path, pin = str(S.children(item, "path")[0][1]), str(S.children(item, "sha256")[0][1])
        target = root / path
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != pin:
            moved.append(path)
    return moved


def load_module(workdir: Path):
    """Import the module under test from a copy, with the chosen seam applied."""
    src = (HERE / "review_div_policy.py").read_text()
    if MUTATION:
        old, new = SEAMS[MUTATION]
        assert src.count(old) == 1, MUTATION
        src = src.replace(old, new, 1)
    target = workdir / "scripts"; target.mkdir(exist_ok=True)
    for name in ("records_sexp.py", "sexp.py", "record_catalog.py", "check_sexp_schema.py", "credit_records.py", "statement_trace.py"):
        shutil.copy(ROOT / "scripts" / name, target / name)
    (workdir / "schema").mkdir(exist_ok=True)
    shutil.copy(ROOT / "schema" / "credits.sexp", workdir / "schema" / "credits.sexp")
    shutil.copy(ROOT / "schema" / "statement-trace.sexp", workdir / "schema" / "statement-trace.sexp")
    (target / "review_div_policy.py").write_text(src)
    spec = importlib.util.spec_from_file_location("review_div_policy_under_test", target / "review_div_policy.py")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def fixture(root: Path, *, obligation="OB-GC-M", kind="instruction", insns=("div", "rem"), risk="medium", declare_boundaries=False,
            steps=None, expected_reads_reference=False, repeat=True, control="DIVERGE", control_step=0,
            control_register="x7", qualification=False, stale_policy=False, witness_source="SRC §1",
            control_property="p0", versions=("v", "v"), pairs=(), declaration=None, category="defined", detail="d",
            silent_forms=(), witness_step=0):
    """One synthetic retained case under profile fx-v0; every knob breaks exactly one leg.

    `pairs` adds recorded producer pairs (left, right, shared input ids, assessment) and `declaration` writes the
    case's `case.sexp` (its second method and adversarial case, a43b-2b); by default the case declares neither."""
    profile = root / "profiles" / "fx-v0"; profile.mkdir(parents=True)
    obs = " ".join(f'(insns "{i}")' for i in insns)
    (profile / "requirements.sexp").write_text(
        f'(requirement (id "REQ-X") (profile_ids "fx-v0") (kind {kind}) (statement "s") {obs} '
        f'(source_refs (source_id "SRC") (locator "1")) (applicability included) (research_status resolved) '
        f'(implementation_status planned) (source_semantics (category {category}) (detail "{detail}")) (risk {risk}) '
        f'(obligation_ids "{obligation}"))\n')
    (profile / "contract-obligations.sexp").write_text(
        f'(obligation (id "{obligation}") (contract_id "fx-env") (contract_version "1") (profile_ids "fx-v0") '
        f'(direction cpu-guarantee) (statement "s") (authority architecture) (source_refs (source_id "SRC") (locator "1")) '
        f'(parameters) (required_checks "c1"))\n')
    policy = b"# policy\n"; (profile / "EVIDENCE_POLICY.md").write_bytes(policy)
    declared = ["p0"] + ([f"p{n}" for n, _, s in (steps or [(0, "", witness_source), (1, "", "SRC §1 (Table 1)"), (2, "", "SRC §1 (Table 1)")]) if "Table" in s or "(boundary" in s] if declare_boundaries else [])
    (profile / "statement-trace.sexp").write_text('(trace (requirement_id "REQ-X") (clause (text "s")' + "".join(f' (properties "{p}")' for p in declared) + '))\n')
    case = root / "evidence" / "cx"; case.mkdir(parents=True)
    steps = steps or [(0, "div x7, x5, x6", witness_source), (1, "rem x8, x5, x6", "SRC §1 (Table 1)"),
                      (2, "div x9, x5, x0", "SRC §1 (Table 1)")]
    (case / "baseline.expected.sexp").write_text(
        '(expectations (program "p.s") (entry "0x0") (instructions 3) (fetches 6)\n' + "".join(
            f'  (step (n {n}) (insn "{insn}") ' + ('(writes)' if insn.split()[0] in silent_forms else f'(writes (write (reg "x7") (value "0x{n + 1:x}")))')
            + f' (derivation "d") (source "{source}"))\n'
            for n, insn, source in steps) + ')\n')
    props = [f'(property (id "p0") (requirement_id "REQ-X") (obligation_ids "{obligation}") (observation_kinds "gpr-change") '
             f'(statement "s") (gpr_witness (step_n {witness_step}) (register "x7")))']
    if declare_boundaries:
        props += [f'(property (id "p{n}") (requirement_id "REQ-X") (obligation_ids "{obligation}") (observation_kinds "gpr-change") '
                  f'(statement "s") (gpr_witness (step_n {n}) (register "x7")))' for n, _, s in steps if "Table" in s or "(boundary" in s]
    expected_inputs = '(input_ids "guest-source") (input_ids "expectation")' + (
        ' (input_ids "reference-config")' if expected_reads_reference else "")
    control_run = (f'(control_run (id "c0") (run_id "control") (baseline_id "baseline") (mutation_input_ids "mutant-expectation") '
                   f'(property_ids "{control_property}") (expected_verdict "DIVERGE") (observed_verdict "{control}") (reason "r"))')
    (case / "planned-experiment.sexp").write_text(
        '(experiment (id "cx") (program "p.s") (instructions 3) (models "m") (verdict "AGREE") (reproduced "r") (control "c")\n'
        '  (verification (format_version "matched-gpr-v1") (comparison_rule "rule-v1") (limitations "l")\n    '
        + "\n    ".join(props) + '\n    ' + control_run + '\n'
        '    (input (id "guest-source") (role "guest-source") (path "profiles/fx-v0/guests/p.s") (sha256 "0"))\n'
        '    (input (id "collector") (role "collector") (path "scripts/c.py") (sha256 "0"))\n'
        '    (input (id "reference-config") (role "reference-config") (path "evidence/cx/ref.json") (sha256 "0"))\n'
        '    (input (id "reference-identity") (role "reference-identity") (path "profiles/fx-v0/retained/id.sexp") (sha256 "0"))\n'
        '    (input (id "expectation") (role "expectation") (path "evidence/cx/baseline.expected.sexp") (sha256 "0"))\n'
        '    (input (id "mutant-expectation") (role "expectation") (path "evidence/cx/control.expected.sexp") (sha256 "0"))\n'
        f'    (producer (id "reference") (role "reference") (version "{versions[0]}") (candidate_id "m") (input_ids "guest-source") '
        '(input_ids "reference-config") (input_ids "reference-identity"))\n'
        f'    (producer (id "expected") (role "expected") (version "{versions[1]}") {expected_inputs})'
        + "".join(f'\n    (producer_pair (id "{left}-{right}") (left "{left}") (right "{right}") (subsystem "gpr-change") '
                  f'(assessment "{assessment}") ' + " ".join(f'(shared_input_ids "{i}")' for i in shared)
                  + ' (evidence "e") (consequence "c"))' for left, right, shared, assessment in pairs) + '))\n')
    if declaration is not None:
        (case / "case.sexp").write_text(declaration)
    runs = [dict(run_kind="baseline", comparison=dict(verdict="AGREE", gpr_difference=None))]
    if repeat:
        runs.append(dict(run_kind="repeat", comparison=dict(verdict="AGREE", gpr_difference=None)))
    diff = None if control != "DIVERGE" else dict(step_n=control_step, observed=[[control_register, 1]], expected=[[control_register, 2]])
    runs.append(dict(run_kind="control", comparison=dict(verdict=control, gpr_difference=diff)))
    (case / "verification.json").write_text(json.dumps(dict(
        case_id="cx", profile_id="fx-v0", qualification=qualification, evaluation="pending", disposition="pending",
        limitations=["l"], comparison=dict(runs=runs))))
    pin = hashlib.sha256(policy).hexdigest() if not stale_policy else "0" * 64
    (case / "dependencies.sexp").write_text(
        f'(dependencies (format_version "v") (input (id "d1") (role "dependency") (path "profiles/fx-v0/EVIDENCE_POLICY.md") (sha256 "{pin}")))\n')
    (case / "measured-experiment.sexp").write_text('(experiment (id "cx") (program "p.s") (measured yes))\n')
    return case


def retain_effect(root: Path, case: Path, *, differ_at=0, **pins):
    """The case's retained configuration effect: its guest and configuration, the raw trace and a record pinning them.

    `differ_at` is the step the trace first differs at (None: it agrees), and each of `pins` replaces one record field.
    The alternative must be the profile override, so the fixture root carries the one the tool renders."""
    sys.path.insert(0, str(HERE))
    import measure_config_effect as Effect
    (root / "schema").mkdir(exist_ok=True)
    shutil.copy(ROOT / "schema" / "override.sexp", root / "schema" / "override.sexp")
    (root / OVERRIDE).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / OVERRIDE, root / OVERRIDE)
    (case / "guest.elf").write_bytes(b"guest")
    (case / "reference-config.json").write_bytes(b'{"own": true}\n')
    rows = []
    for n in range(3):
        rows.append(f"[{n}] [M]: 0x{0x80000000 + 4 * n:016X} (0x00000013) nop")
        if n != differ_at:
            rows.append(f"x7 <- 0x{n + 1:016X}")
    trace = ("\n".join(rows) + "\n").encode()
    digest = lambda data: hashlib.sha256(data).hexdigest()
    fields = dict(case_id="cx", binary_sha256=BINARY, guest_sha256=digest(b"guest"), case_config_sha256=digest(b'{"own": true}\n'),
                  alternative_config_sha256=digest(Effect.profile_config(root)), trace_sha256=digest(trace))
    fields.update(pins)
    reference = root / "profiles" / "fx-v0" / "reference"
    reference.mkdir(exist_ok=True)
    (reference / "cx.effect.trace").write_bytes(trace)
    (reference / "cx.effect.sexp").write_text("(config_effect " + " ".join(f'({k} "{v}")' for k, v in fields.items())
                                              + f" (instructions 3) (trace_bytes {len(trace)}))\n")


def credit(root: Path, *, case_id="cx", requirement="REQ-X", obligation="OB-GC-M", measured_sha=None, complete=True):
    """A credit record for the fixture case, every pin taken from the fixture's own bytes (a42ay)."""
    receipt = root / "evidence" / case_id / "verification.json"
    body = json.loads(receipt.read_text()); body["complete_canonical_capture"] = complete; receipt.write_text(json.dumps(body))
    def pin(rel):
        data = (root / rel).read_bytes()
        return f'(pin (path "{rel}") (sha256 "{measured_sha if measured_sha and rel.endswith("measured-experiment.sexp") else hashlib.sha256(data).hexdigest()}") (byte_size {len(data)}))'
    (root / "profiles" / "fx-v0" / "credits.sexp").write_text(
        f'(credit (id "CR-{case_id}") (profile_ids "fx-v0") (requirement_id "{requirement}") (obligation_ids "{obligation}") (case_id "{case_id}")\n'
        f'  (measured {pin(f"evidence/{case_id}/measured-experiment.sexp")}) (receipt {pin(f"evidence/{case_id}/verification.json")})\n'
        f'  (policy {pin("profiles/fx-v0/EVIDENCE_POLICY.md")}) (retained_sources "SRC") (authority director) (date "2026-10-23")\n'
        f'  (decision "decision_fixture.md") (legs 10) (limitations "fixture"))\n')


class PolicyTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target" / "tmp"; base.mkdir(parents=True, exist_ok=True)
        self._tmp = TemporaryDirectory(dir=str(base)); self.root = Path(self._tmp.name)
        self.M = load_module(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def measure(self, method=METHOD, case="cx"):
        return self.M.measure_policy(self.root, method=dict(method), case_id=case)

    def legs(self, table):
        return {leg["id"]: leg["disposition"] for leg in table["legs"]}

    def test_every_leg_satisfied_grants_no_credit(self):
        fixture(self.root, declare_boundaries=True)
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"], t["findings"], t["credited"]), ("satisfied", [], [], False))
        self.assertEqual(set(self.legs(t).values()), {"satisfied"})
        self.assertEqual(t["coverage"], dict(required=["div", "rem"], exercised=["div", "rem"], predeclared=["div", "rem"]))

    def test_undeclared_boundary_rows_keep_the_case_pending(self):
        fixture(self.root, insns=("div",))
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["boundary-fixtures"]))
        self.assertEqual(t["boundary"], dict(present=[1, 2], predeclared=[]))
        self.assertFalse(t["credited"])

    def test_boundary_tag_marks_a_directed_row(self):
        """A `(boundary: …)` tag marks a directed row as a table citation does (the XLEN guest's ten, a43a-2f)."""
        steps = [(0, "div x7, x5, x6", "SRC §1"), (1, "div x8, x5, x6", "SRC §1 (boundary: bit 63)"),
                 (2, "div x9, x5, x0", "SRC §1 (boundary: the wrap at 2^63)")]
        fixture(self.root, insns=("div",), steps=steps)
        t = self.measure()
        self.assertEqual((t["missing"], t["boundary"]), (["boundary-fixtures"], dict(present=[1, 2], predeclared=[])))
        self.tearDown(); self.setUp()
        fixture(self.root, insns=("div",), steps=steps, declare_boundaries=True)
        t = self.measure()
        self.assertEqual((t["disposition"], t["boundary"]), ("satisfied", dict(present=[1, 2], predeclared=[1, 2])))

    def test_the_property_bound_is_the_tools_own(self):
        """The rehearsal found this review still refusing above 64 after the tools moved to 96 (a49-1): one bound, held equal."""
        bound = re.search(r"^MAX_PROPERTIES = (\d+)", (ROOT / "scripts" / "matched_gpr_relations.py").read_text(), re.M)
        self.assertEqual(self.M.MAX_PROPERTIES, int(bound[1]))

    def test_a_requirement_with_no_statement_trace_stays_pending(self):
        """A case that covers every form and agrees on every step can still leave a clause unread (a49-1)."""
        fixture(self.root, declare_boundaries=True)
        (self.root / "profiles" / "fx-v0" / "statement-trace.sexp").unlink()
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["statement-trace"]))
        self.assertIn("REQ-X has no statement trace", self.legs_text(t, "statement-trace"))

    def test_state_requirement_without_forms_is_vacuous_but_explicit(self):
        """A state requirement names no form (REQ-D-XLEN): satisfied, and the leg says why; another kind naming none stays pending."""
        fixture(self.root, kind="state", insns=(), declare_boundaries=True)
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"], t["coverage"]),
                         ("satisfied", [], dict(required=[], exercised=[], predeclared=[])))
        self.assertIn("coverage is vacuous, its 3 predeclared witnesses", self.legs_text(t, "form-coverage"))
        self.tearDown(); self.setUp()
        fixture(self.root, insns=(), declare_boundaries=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["form-coverage"]); self.assertIn("0 of 0 forms predeclared", self.legs_text(t, "form-coverage"))

    def test_a_configuration_requirement_naming_no_form_is_vacuous_too(self):
        """REQ-D-IALIGN-16 says where an instruction may start, and names no form: its witnesses are its coverage (a47-3)."""
        fixture(self.root, kind="configuration", insns=(), declare_boundaries=True)
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("satisfied", []))
        self.assertIn("a configuration requirement names no form: coverage is vacuous, its 3 predeclared witnesses", self.legs_text(t, "form-coverage"))

    def test_a_memory_requirement_naming_no_form_is_vacuous_too(self):
        """REQ-D-IALIGN-16 says where an instruction may start, and names no form: its witnesses are its coverage (a47-3)."""
        fixture(self.root, kind="memory", insns=(), declare_boundaries=True)
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("satisfied", []))
        self.assertIn("a memory requirement names no form: coverage is vacuous, its 3 predeclared witnesses", self.legs_text(t, "form-coverage"))

    def silent(self, *, cell="form:sb", steps=None, witness=1, insns=("sb",), silent_forms=("sb",)):
        """A store writes no GPR, so its witness is the read that observes it (P4-SYSTEM.14 a46-4)."""
        fixture(self.root, insns=insns, silent_forms=silent_forms, witness_step=witness, control_step=witness,
                steps=steps or [(0, "sb x7, 0, x1", "SRC §1"), (1, "lbu x8, x1, 0", "SRC §1 (boundary: the read)")],
                declaration=f'(case (property (id "p0") (cell "{cell}")))\n')
        table = self.measure()
        return table, self.legs_text(table, "form-coverage")

    def test_a_form_that_writes_no_gpr_is_predeclared_by_the_read_after_it(self):
        table, text = self.silent()
        self.assertEqual((table["disposition"], table["missing"]), ("satisfied", []))
        self.assertIn("1 of 1 forms predeclared ['sb']", text)
        self.assertIn("writing no GPR, read after their own step: ['sb']", text)

    def test_a_silent_form_read_before_its_step_stays_pending(self):
        table, text = self.silent(witness=0, steps=[(0, "lbu x8, x1, 0", "SRC §1 (boundary: the read)"), (1, "sb x7, 0, x1", "SRC §1")])
        self.assertEqual((table["disposition"], table["missing"]), ("pending", ["form-coverage"]))
        self.assertIn("0 of 1 forms predeclared []", text)

    def test_a_silent_form_no_cell_names_stays_pending(self):
        table, text = self.silent(cell="form:lbu")
        self.assertEqual((table["disposition"], table["missing"]), ("pending", ["form-coverage"]))
        self.assertIn("0 of 1 forms predeclared []", text)

    def test_a_form_that_writes_a_gpr_gets_no_later_read(self):
        """DIV writes rd, so it has a change to witness at its own step, and a later read stands in for nothing."""
        table, text = self.silent(cell="form:div", insns=("div",), silent_forms=(),
                                  steps=[(0, "div x7, x5, x6", "SRC §1"), (1, "add x8, x7, x0", "SRC §1 (boundary: the read)")])
        self.assertEqual((table["disposition"], table["missing"]), ("pending", ["form-coverage"]))
        self.assertIn("0 of 1 forms predeclared []", text)

    def test_partial_form_coverage_is_pending(self):
        fixture(self.root, insns=("div", "rem", "mul"), declare_boundaries=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["form-coverage"]); self.assertIn("2 of 3 forms predeclared", self.legs_text(t, "form-coverage"))

    def legs_text(self, table, leg_id):
        return next(leg["measured"] for leg in table["legs"] if leg["id"] == leg_id)

    def test_expectation_step_without_source_is_pending(self):
        fixture(self.root, declare_boundaries=True,
                steps=[(0, "div x7, x5, x6", "SRC §1"), (1, "rem x8, x5, x6", ""), (2, "div x9, x5, x0", "SRC §1 (Table 1)")])
        self.assertIn("source-located-expectations", self.measure()["missing"])

    def test_witness_not_citing_requirement_source_is_pending(self):
        fixture(self.root, declare_boundaries=True, witness_source="OTHER §9")
        self.assertEqual(self.measure()["missing"], ["source-located-expectations"])

    def test_expected_producer_reading_reference_inputs_is_pending(self):
        fixture(self.root, declare_boundaries=True, expected_reads_reference=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["source-located-expectations"]); self.assertIn("reads reference inputs", self.legs_text(t, "source-located-expectations"))

    def test_missing_repeat_run_is_pending(self):
        fixture(self.root, declare_boundaries=True, repeat=False)
        self.assertEqual(self.measure()["missing"], ["repeated-execution"])

    def test_agreeing_control_is_pending(self):
        fixture(self.root, declare_boundaries=True, control="AGREE")
        self.assertEqual(self.measure()["missing"], ["discriminating-control"])

    def test_control_diverging_elsewhere_is_pending(self):
        fixture(self.root, declare_boundaries=True, control_step=1, control_register="x8")
        t = self.measure()
        self.assertEqual(t["missing"], ["discriminating-control"]); self.assertIn("witness step 0 x7", self.legs_text(t, "discriminating-control"))

    def test_control_leg_reads_the_property_the_control_run_names(self):
        """The control changes p1's value (step 1, x7): named, the leg is satisfied; the first property is not it."""
        fixture(self.root, declare_boundaries=True, control_step=1, control_property="p1")
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("satisfied", []))
        self.assertIn("witness step 1 x7", self.legs_text(t, "discriminating-control"))
        self.tearDown(); self.setUp()
        fixture(self.root, declare_boundaries=True, control_step=1, control_property="p0")
        self.assertEqual(self.measure()["missing"], ["discriminating-control"])
        self.tearDown(); self.setUp()
        case = fixture(self.root, declare_boundaries=True, control_property="absent")
        with self.assertRaises(self.M.Refused): self.measure()
        planned = case / "planned-experiment.sexp"
        sibling = '(control_run (id "c1") (run_id "control") (property_ids "p0") (expected_verdict "DIVERGE") (observed_verdict "DIVERGE") (reason "r"))\n    '
        planned.write_text(planned.read_text().replace('(control_run (id "c0")', sibling + '(control_run (id "c0")', 1))
        with self.assertRaises(self.M.Refused): self.measure()

    def test_current_credit_reports_credited_over_a_satisfied_measurement(self):
        """`credited` is the credit record's word, not the measurement's (a42ay)."""
        fixture(self.root, declare_boundaries=True); credit(self.root)
        table = self.measure()
        self.assertEqual((table["disposition"], table["credited"], table["credit_ids"], table["findings"]),
                         ("satisfied", True, ["CR-cx"], []))
        self.assertEqual(self.M.summary(table), (0, "DIV-POLICY: satisfied — 11 of 11 legs satisfied; credited by CR-cx"))

    def test_credit_over_a_pending_measurement_is_a_finding(self):
        fixture(self.root); credit(self.root)
        table = self.measure()
        self.assertEqual((table["disposition"], table["credited"]), ("pending", True))
        self.assertTrue(any("while its measurement is pending" in f for f in table["findings"]), table["findings"])
        self.assertEqual(self.M.summary(table)[0], 1)

    def test_lapsed_credit_is_a_finding_and_credits_nothing(self):
        fixture(self.root, declare_boundaries=True); credit(self.root, measured_sha="0" * 64)
        table = self.measure()
        self.assertEqual((table["disposition"], table["credited"]), ("satisfied", False))
        self.assertTrue(any("lapsed" in f and "measured pin" in f for f in table["findings"]), table["findings"])
        self.assertIn("no qualification credit", self.M.summary(table)[1])

    def test_receipt_claiming_qualification_is_a_finding(self):
        fixture(self.root, qualification=True)
        t = self.measure()
        self.assertEqual(t["disposition"], "pending"); self.assertEqual(len(t["findings"]), 1)
        self.assertIn("claims qualification", t["findings"][0]); self.assertEqual(self.M.summary(t)[0], 1)
        self.assertFalse(t["credited"])

    def test_unsatisfied_method_is_blocked(self):
        fixture(self.root, declare_boundaries=True)
        for disposition in ("refused", "unavailable", "unsupported"):
            t = self.measure(method=dict(METHOD, disposition=disposition, capture_binding=None))
            self.assertEqual((t["disposition"], self.M.summary(t)[0], t["invalidated_by"]), ("blocked", 1, None), disposition)
            self.assertIn("matched-reference-comparison", t["missing"]); self.assertIn("currentness", t["missing"])
            self.assertIn("legs measured but blocked", t["findings"][0])

    def test_stale_method_is_invalidated_not_blocked(self):
        fixture(self.root, declare_boundaries=True)
        t = self.measure(method=STALE)
        self.assertEqual((t["disposition"], t["findings"], t["credited"]), ("invalidated", [], False))
        self.assertEqual(t["missing"], ["matched-reference-comparison", "currentness"])
        self.assertEqual(t["invalidated_by"], STALE["reason"]); self.assertEqual(t["method"]["reason"], STALE["reason"])
        code, line = self.M.summary(t)
        self.assertEqual(code, 0); self.assertIn("DIV-POLICY: invalidated — 9 of 11", line)
        self.assertIn("invalidated by evidence/cx/dependencies.sexp", line); self.assertIn("no qualification credit", line)

    def test_qualification_over_invalidated_method_is_a_finding(self):
        fixture(self.root, declare_boundaries=True, qualification=True)
        t = self.measure(method=STALE)
        self.assertEqual((t["disposition"], len(t["findings"]), t["credited"]), ("invalidated", 1, False))
        self.assertIn("claims qualification", t["findings"][0]); self.assertEqual(self.M.summary(t)[0], 1)

    def second(self, *, risk="high", kind="independent-exact-expectation", versions=("sail-v", "author-v"),
               assessment="not-examined", shared=("guest-source", "dependency-manifest"),
               common=("guest-source", "dependency-manifest"), adversarial=("p0",)):
        """A CSR-SET-shaped declaration (a43b-2a, D2) on a fixture whose other legs are satisfied: the record's
        reference and expected producers, their recorded pair and shared inputs, an adversarial witness. Every
        knob breaks exactly one condition. Returns the risk-method leg and the table."""
        declaration = (f'(case (second_method (kind "{kind}") (producer_ids "expected") (producer_ids "reference") '
                       + " ".join(f'(common_input_ids "{i}")' for i in common)
                       + ' (independently_derived "the expected values derived from the pinned chapter, no reference '
                       'output among the inputs"))\n  (adversarial ' + " ".join(f'(property_ids "{i}")' for i in adversarial)
                       + ' (failure_mode "a forbidden CSR write commits its destination")))\n')
        fixture(self.root, declare_boundaries=True, risk=risk, versions=versions,
                pairs=(("reference", "expected", shared, assessment),), declaration=declaration)
        t = self.measure()
        return next(leg for leg in t["legs"] if leg["id"] == "risk-method"), t

    def test_second_method_satisfies_high_risk_when_all_five_conditions_hold(self):
        leg, t = self.second()
        self.assertEqual((leg["disposition"], t["disposition"], t["credited"]), ("satisfied", "satisfied", False), leg)
        self.assertIn("ancestry ['not-examined']: no independence credit", leg["measured"])
        self.assertIn("adversarial ['p0']", leg["measured"])

    def test_second_method_names_one_of_the_policy_methods(self):
        leg, t = self.second(kind="two-wrappers")
        self.assertEqual((leg["disposition"], t["missing"]), ("pending", ["risk-method"]), leg)
        self.assertIn("(1)", leg["measured"])

    def test_second_method_producers_have_distinct_versions_at_any_risk(self):
        """Two wrappers around one producer share a version; a low-risk declaration is judged, never ignored."""
        measured = []
        for risk in ("high", "low"):
            leg, t = self.second(risk=risk, versions=("v", "v"))
            measured.append((risk, leg["disposition"], t["missing"], "(2)" in leg["measured"]))
            self.tearDown(); self.setUp()
        self.assertEqual(measured, [("high", "pending", ["risk-method"], True), ("low", "pending", ["risk-method"], True)])

    def test_second_method_common_inputs_are_the_recorded_shared_inputs(self):
        leg, t = self.second(common=("guest-source",))
        self.assertEqual((leg["disposition"], t["missing"]), ("pending", ["risk-method"]), leg)
        self.assertIn("(3) common inputs ['guest-source'] are not the recorded pairs' shared inputs", leg["measured"])

    def test_second_method_never_rests_on_a_pair_recorded_as_shared(self):
        leg, t = self.second(assessment="shared")
        self.assertEqual((leg["disposition"], t["missing"]), ("pending", ["risk-method"]), leg)
        self.assertIn("(4) ancestry ['shared']", leg["measured"])

    def test_adversarial_case_names_declared_properties_of_an_agreeing_capture(self):
        leg, t = self.second(adversarial=("p0", "p9"))
        self.assertEqual((leg["disposition"], t["missing"]), ("pending", ["risk-method"]), leg)
        self.assertIn("(5) adversarial properties ['p0', 'p9']", leg["measured"])

    def implementation_defined(self, *, differ_at=0, detail="the selection", effect=True, insns=("div", "rem"), boundaries=True, **pins):
        """A case on its own configuration; every other leg satisfied. Returns the matched comparison's text and the table."""
        case = fixture(self.root, declare_boundaries=boundaries, category="implementation-defined", detail=detail,
                       versions=(f"sha256:{BINARY}", "author-v"), insns=insns)
        if effect:
            retain_effect(self.root, case, differ_at=differ_at, **pins)
        t = self.measure()
        return self.legs_text(t, "matched-reference-comparison"), t

    def test_a_defined_requirements_comparison_reads_as_it_always_has(self):
        fixture(self.root, declare_boundaries=True)
        t = self.measure()
        self.assertEqual(self.legs_text(t, "matched-reference-comparison"),
                         "method satisfied; baseline AGREE; rule rule-v1; vocabulary ['gpr-change']")

    def test_implementation_defined_with_an_observed_effect_is_satisfied(self):
        text, t = self.implementation_defined()
        self.assertEqual((t["disposition"], t["missing"], t["category"], t["credited"]), ("satisfied", [], "implementation-defined", False))
        self.assertIn("selection recorded; observed effect under the profile override: step 0 (div x7, x5, x6): Sail {}", text)

    def declared_alternative(self, switches=' (extension_off "Svade")'):
        """A case on the profile override that declares what selects otherwise: the record pins that rendering, not the override."""
        sys.path.insert(0, str(HERE))
        import measure_config_effect as Effect
        case = fixture(self.root, declare_boundaries=True, category="implementation-defined", detail="the selection",
                       versions=(f"sha256:{BINARY}", "author-v"), insns=("div", "rem"))
        retain_effect(self.root, case)
        shutil.copy(ROOT / "schema" / "alternative.sexp", self.root / "schema" / "alternative.sexp")
        path = self.root / Effect.Prep.alternative_path("cx")
        path.write_text(f'(alternative (case_id "cx") (reason "Selects otherwise."){switches})\n')
        return Effect, case, path

    def test_a_case_with_a_declared_alternative_is_read_against_it(self):
        Effect, case, path = self.declared_alternative()
        record = self.root / "profiles" / "fx-v0" / "reference" / "cx.effect.sexp"
        rendered = Effect.alternative_config(self.root, "cx")[0]
        before = hashlib.sha256(Effect.profile_config(self.root)).hexdigest()
        record.write_text(record.read_text().replace(before, hashlib.sha256(rendered).hexdigest()))
        t = self.measure()
        text = self.legs_text(t, "matched-reference-comparison")
        self.assertEqual((t["disposition"], t["missing"]), ("satisfied", []), text)
        self.assertIn("selection recorded; observed effect under its declared alternative: step 0 (div x7, x5, x6): Sail {}", text)

    def test_a_retained_effect_of_the_override_when_the_case_declares_otherwise_is_pending(self):
        self.declared_alternative()
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["matched-reference-comparison"]))
        self.assertIn("does not pin its declared alternative", self.legs_text(t, "matched-reference-comparison"))

    def test_a_case_whose_declared_alternative_refuses_is_pending(self):
        self.declared_alternative(' (extension_off "NotAnExtension")')
        t = self.measure()
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["matched-reference-comparison"]))
        self.assertIn("declared alternative refuses: alternative names unknown extension", self.legs_text(t, "matched-reference-comparison"))

    def test_implementation_defined_without_a_retained_effect_is_pending(self):
        """The policy: "A configuration file without an observed effect" is insufficient by itself."""
        text, t = self.implementation_defined(effect=False)
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["matched-reference-comparison"]))
        self.assertIn("no retained configuration effect", text)

    def test_implementation_defined_with_no_recorded_selection_is_pending(self):
        text, t = self.implementation_defined(detail=" ")
        self.assertEqual(t["missing"], ["matched-reference-comparison"]); self.assertIn("selection unrecorded", text)

    def source_specific(self, *, disposition=True, kind="case", control="p0", walks=False, walk_files=None, category="source-specific"):
        """A case whose requirement closes by a declared disposition: every other leg satisfied. Returns the comparison's text and the table."""
        case = fixture(self.root, declare_boundaries=True, category=category, detail="the source's own category",
                       versions=(f"sha256:{BINARY}", "author-v"))
        shutil.copy(ROOT / "schema" / "dispositions.sexp", self.root / "schema" / "dispositions.sexp")
        if disposition:
            extra = f' (control_property "{control}")' if kind == "case" else ""
            extra += " (walk_record yes)" if walks else ""
            (self.root / "profiles" / "fx-v0" / "dispositions.sexp").write_text(
                f'(disposition (id "DS-X") (requirement_id "REQ-X") (kind {kind}) (source_id "SRC") (source_locator "§1") '
                f'(argument "The reference has one behaviour.") (controls "the case\'s control"){extra})\n')
        if walk_files is not None:
            sys.path.insert(0, str(HERE))
            import measure_walk_trace as Walk
            record, trace, lab = Walk.walk_paths(self.root, "cx")
            record = self.root / "profiles" / "fx-v0" / "reference" / record.name
            record.parent.mkdir(parents=True, exist_ok=True)
            reference, engine = walk_files
            (case / "guest.elf").write_bytes(b"guest"); (case / "reference-config.json").write_bytes(b'{"own": true}\n')
            record.with_name("cx.walk.trace").write_text(reference); record.with_name("cx.walk.lab").write_text(engine)
            digest = lambda data: hashlib.sha256(data).hexdigest()
            record.write_text(f'(walk_trace (case_id "cx") (binary_sha256 "{BINARY}") (guest_sha256 "{digest((case / "guest.elf").read_bytes())}") '
                              f'(case_config_sha256 "{digest((case / "reference-config.json").read_bytes())}") (instructions 2) '
                              f'(reference_trace_sha256 "{digest(reference.encode())}") (engine_trace_sha256 "{digest(engine.encode())}"))\n')
        t = self.measure()
        return self.legs_text(t, "matched-reference-comparison"), t

    WALK = "PTW: Start, vpn=0x400, access_type=R, privilege=S\nmem[R,0x0000000080003000] -> 0x0000000020001001\nPTW: Step, level=2, pte=0x20001001, pte_addr=0x80003000\nPTW: Success, final_ppn=0x80007, level=2\n"
    OURS = "ptw[0x0000000080003000] -> 0x0000000020001001\n"

    def test_source_specific_with_its_disposition_is_satisfied(self):
        text, t = self.source_specific()
        self.assertEqual((t["disposition"], t["missing"], t["category"]), ("satisfied", [], "source-specific"), text)
        self.assertIn("category source-specific: disposition DS-X declared, its control p0", text)

    def test_implementation_defined_with_a_disposition_is_read_by_it(self):
        """The policy's "alternative disposition": the reference offers no switch, and the category stays what the source says."""
        text, t = self.source_specific(category="implementation-defined")
        self.assertEqual((t["disposition"], t["missing"], t["category"]), ("satisfied", [], "implementation-defined"), text)
        self.assertIn("selection recorded; disposition DS-X declared, its control p0", text)

    def test_implementation_defined_with_a_disposition_naming_another_control_is_pending(self):
        text, t = self.source_specific(category="implementation-defined", control="p9")
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("names the control p9, and this case's is p0", text)

    def test_source_specific_with_no_disposition_is_pending(self):
        text, t = self.source_specific(disposition=False)
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["matched-reference-comparison"]), text)
        self.assertIn("no disposition declared for REQ-X", text)

    def test_source_specific_closing_through_a_record_is_pending_on_a_case(self):
        text, t = self.source_specific(kind="record")
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("closes through a record, not a case", text)

    def test_source_specific_naming_another_control_is_pending(self):
        text, t = self.source_specific(control="p9")
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("names the control p9, and this case's is p0", text)

    def test_a_disposition_asking_for_walks_with_none_retained_is_pending(self):
        text, t = self.source_specific(walks=True)
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("no retained page-table comparison", text)

    def test_a_retained_walk_comparison_that_holds_is_satisfied(self):
        text, t = self.source_specific(walks=True, walk_files=(self.WALK, self.OURS))
        self.assertEqual((t["disposition"], t["missing"]), ("satisfied", []), text)
        self.assertIn("1 distinct PTEs read on both with the same values", text)

    def test_a_walk_record_of_another_guest_is_pending(self):
        text, t = self.source_specific(walks=True, walk_files=(self.WALK, self.OURS))
        record = self.root / "profiles" / "fx-v0" / "reference" / "cx.walk.sexp"
        record.write_text(re.sub(r'\(guest_sha256 "[0-9a-f]{64}"\)', f'(guest_sha256 "{"e" * 64}")', record.read_text()))
        t = self.measure(); text = self.legs_text(t, "matched-reference-comparison")
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("does not pin the guest", text)

    def test_a_walk_trace_that_moved_is_pending(self):
        self.source_specific(walks=True, walk_files=(self.WALK, self.OURS))
        (self.root / "profiles" / "fx-v0" / "reference" / "cx.walk.trace").write_text(self.WALK + "\n")
        t = self.measure(); text = self.legs_text(t, "matched-reference-comparison")
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("does not pin the reference's trace", text)

    def test_a_walk_comparison_that_does_not_hold_is_pending(self):
        text, t = self.source_specific(walks=True, walk_files=(self.WALK, "ptw[0x0000000080003000] -> 0x0000000000000001\n"))
        self.assertEqual(t["missing"], ["matched-reference-comparison"], text)
        self.assertIn("different PTEs", text)

    def test_a_category_with_no_branch_is_pending_and_named(self):
        fixture(self.root, declare_boundaries=True, category="unspecified")
        t = self.measure()
        self.assertEqual(t["missing"], ["matched-reference-comparison"])
        self.assertIn("category unspecified: no row measured for it here", self.legs_text(t, "matched-reference-comparison"))

    def effect_pending(self, needle, **pins):
        text, t = self.implementation_defined(**pins)
        self.assertEqual((t["disposition"], t["missing"]), ("pending", ["matched-reference-comparison"]), text)
        self.assertIn(needle, text)

    def test_a_retained_effect_for_another_case_is_pending(self):
        self.effect_pending("does not pin its case", case_id="other-v1")

    def test_a_retained_effect_of_another_guest_is_pending(self):
        self.effect_pending("does not pin the guest", guest_sha256="0" * 64)

    def test_a_retained_effect_of_another_case_configuration_is_pending(self):
        self.effect_pending("does not pin the case's configuration", case_config_sha256="0" * 64)

    def test_a_retained_effect_of_another_binary_is_pending(self):
        self.effect_pending("does not pin the reference producer's binary", binary_sha256="0" * 64)

    def test_a_retained_effect_with_no_configuration_of_its_own_is_pending(self):
        own = hashlib.sha256(b'{"own": true}\n').hexdigest()
        self.effect_pending("does not pin a different configuration", alternative_config_sha256=own)

    def test_a_retained_effect_under_another_configuration_is_pending(self):
        self.effect_pending("does not pin the profile override", alternative_config_sha256="0" * 64)

    def test_a_retained_effect_whose_trace_moved_is_pending(self):
        self.effect_pending("does not pin its trace", trace_sha256="0" * 64)

    def test_a_retained_effect_that_agrees_is_pending(self):
        self.effect_pending("reads AGREE: no observed effect", differ_at=None)

    def test_a_retained_effect_differing_at_no_declared_step_is_pending(self):
        """Only p0 (step 0) is declared here, so the case misses the boundary leg too; the comparison's own text names the step."""
        text, t = self.implementation_defined(differ_at=1, insns=("div",), boundaries=False)
        self.assertIn("matched-reference-comparison", t["missing"])
        self.assertIn("first differs at step 1, no declared property's", text)

    def test_a_retained_effect_with_no_trace_or_a_malformed_record_refuses(self):
        case = fixture(self.root, declare_boundaries=True, category="implementation-defined", detail="the selection",
                       versions=(f"sha256:{BINARY}", "author-v"))
        retain_effect(self.root, case)
        reference = self.root / "profiles" / "fx-v0" / "reference"
        data = (reference / "cx.effect.trace").read_bytes()
        (reference / "cx.effect.trace").unlink()
        with self.assertRaises(self.M.Refused): self.measure()
        (reference / "cx.effect.trace").write_bytes(data)
        (reference / "cx.effect.sexp").write_text("(other)\n")
        with self.assertRaises(self.M.Refused): self.measure()

    def test_high_risk_requires_a_second_method(self):
        fixture(self.root, declare_boundaries=True, risk="high")
        t = self.measure()
        self.assertEqual(t["missing"], ["risk-method"]); self.assertIn("second method", self.legs_text(t, "risk-method"))

    def test_undeclared_feature_disposition_is_pending(self):
        fixture(self.root, obligation="OB-Y", declare_boundaries=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["feature-rules"]); self.assertIn("undeclared", self.legs_text(t, "feature-rules"))

    def test_changed_policy_breaks_currentness(self):
        fixture(self.root, declare_boundaries=True, stale_policy=True)
        t = self.measure()
        self.assertEqual(t["missing"], ["currentness"]); self.assertIn("changed since the pin", self.legs_text(t, "currentness"))

    def test_oversize_declaration_refuses(self):
        case = fixture(self.root, declare_boundaries=True)
        planned = case / "planned-experiment.sexp"
        planned.write_text(planned.read_text() + '(comment "' + "x" * 65536 + '")\n')
        with self.assertRaises(self.M.Refused): self.measure()

    def test_unknown_case_refuses(self):
        fixture(self.root)
        with self.assertRaises(self.M.Refused): self.measure(case="absent")

    def test_cli_json_and_exit_codes(self):
        fixture(self.root)
        method = self.root / "method.json"; method.write_text(json.dumps(METHOD))
        from contextlib import redirect_stdout, redirect_stderr
        from io import StringIO
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.M.main(["--root", str(self.root), "--case", "cx", "--method-json", str(method), "--json"])
        table = json.loads(out.getvalue())
        self.assertEqual((code, table["disposition"], table["credited"]), (0, "pending", False)); self.assertIn("DIV-POLICY: pending", err.getvalue())
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(self.M.main(["--root", str(self.root), "--case", "absent", "--method-json", str(method)]), 2)

    def test_output_is_deterministic_and_bounded(self):
        fixture(self.root, declare_boundaries=True)
        first, second = self.measure(), self.measure()
        self.assertEqual(first, second); self.assertLessEqual(len(json.dumps(first).encode()), 65536)

    def test_real_tree_measures_as_its_manifest_predicts(self):
        """Every reviewed capture, measured by the live consumer in the one `--every-retained` run PROFILE-CONSISTENCY
        makes (a43a-2f), and again by the module under test from the same method results. The prediction comes from
        each case's manifest and the live credit catalogue, never from the tree's history: current pins, every leg
        satisfied — credited when a record names the case; a moved method pin, invalidated with the two method legs
        missing — and a record that names the case lapses and is its one finding (a42ay), exit 1. Since the planned
        lapse that opens CSR-SET (P4-SYSTEM.14 a43b-2b) no record names v4 or the XLEN case: invalidated, exit 0."""
        import subprocess
        done = subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / "review_div_policy.py"), "--every-retained", "--json"],
                              capture_output=True, text=True, cwd=str(ROOT))
        tables = json.loads(done.stdout)
        self.assertEqual([t["case_id"] for t in tables], [self.M.CASE_ID, XLEN_CASE_ID, CSR_CASE_ID, ZICNTR_CASE_ID, SSTC_CASE_ID, *BATCH_I, *SWITCHES, *LAST_DEFINED, *LAST_SWITCHES, *NO_SWITCH])
        moved = {t["case_id"]: moved_inputs(ROOT, t["case_id"]) for t in tables}
        catalogue = ROOT / "profiles" / "rv64gc-lab-v0" / "credits.sexp"
        forms = self.M.S.parse(catalogue.read_text()) if catalogue.is_file() else []
        naming = {t["case_id"]: [str(self.M._one(f, "id")) for f in forms if isinstance(f, list) and f and str(f[0]) == "credit"
                                 and str(self.M._one(f, "case_id")) == t["case_id"]] for t in tables}
        self.assertEqual(done.returncode, 1 if any(moved[c] and naming[c] for c in moved) else 0, done.stderr)
        self.assertEqual(done.stderr.splitlines(), [f"{t['case_id']}: {self.M.summary(t)[1]}" for t in tables])
        for live in tables:
            self.assertEqual(self.M.measure_policy(ROOT, method=live["method"], case_id=live["case_id"]), live)
        for t in tables:
            with self.subTest(case=t["case_id"]):
                ids = naming[t["case_id"]]
                self.assertEqual(t["credit_ids"], ids)
                if moved[t["case_id"]]:
                    # A moved pinned input invalidates the measurement and, through credit_records.authenticate's walk
                    # of the same manifest, lapses any record naming the case: its one finding, exit 1.
                    self.assertEqual((t["disposition"], t["missing"], t["credited"]),
                                     ("invalidated", ["matched-reference-comparison", "currentness"], False))
                    self.assertEqual(sum(1 for leg in t["legs"] if leg["disposition"] == "satisfied"), 9)
                    self.assertEqual(t["method"]["disposition"], "stale"); self.assertTrue(t["invalidated_by"], t["method"])
                    self.assertEqual([f.split(" names this case but lapsed: ")[0] for f in t["findings"]],
                                     ["credit " + i for i in ids])
                    self.assertEqual(self.M.summary(t)[0], 1 if ids else 0)
                else:
                    self.assertEqual((t["disposition"], t["missing"], t["findings"], t["credited"]),
                                     ("satisfied", [], [], bool(ids)))
                    self.assertEqual(sum(1 for leg in t["legs"] if leg["disposition"] == "satisfied"), 11)
                    self.assertIsNone(t["invalidated_by"])
                    self.assertEqual(self.M.summary(t), (0, "DIV-POLICY: satisfied — 11 of 11 legs satisfied; " + (
                        "credited by " + ", ".join(ids) if ids else "no qualification credit")))
        table, xlen, csr, zicntr, sstc, *batch = tables
        no_switch = batch[-len(NO_SWITCH):]; batch = batch[:-len(NO_SWITCH)]
        for t in no_switch:
            requirement, obligation, risk, disposition, control = NO_SWITCH[t["case_id"]]
            self.assertEqual((t["requirement_id"], t["obligation_ids"][0], t["risk"], t["category"]), (requirement, obligation, risk, "implementation-defined"), t["case_id"])
            self.assertIn(f"selection recorded; disposition {disposition} declared, its control {control}", self.legs_text(t, "matched-reference-comparison"), t["case_id"])
            self.assertNotIn("observed effect", self.legs_text(t, "matched-reference-comparison"), t["case_id"])
            declared = {str(self.M._one(p, "id")) for p in self.M.S.children(self.M.S.children(self.M._one_form(
                ROOT / "evidence" / t["case_id"] / "planned-experiment.sexp", "experiment"), "verification")[0], "property")}
            named_ids = {word.strip() for group in re.findall(r"\(([^()]*)\)", self.M.FEATURE_DISPOSITIONS[obligation])
                         for word in re.split(r"[,;]", group) if re.fullmatch(r"[a-z][a-z0-9.]*(-[a-z0-9.]+)+", word.strip())}
            self.assertTrue(named_ids, t["case_id"]); self.assertEqual(named_ids - declared, set(), t["case_id"])
        split = len(BATCH_I) + len(SWITCHES)
        switches = batch[len(BATCH_I):split] + batch[split + len(LAST_DEFINED):]; batch = batch[:len(BATCH_I)] + batch[split:split + len(LAST_DEFINED)]
        for t in switches:
            requirement, obligation, risk, named, first = {**SWITCHES, **LAST_SWITCHES}[t["case_id"]]
            self.assertEqual((t["requirement_id"], t["obligation_ids"][0], t["risk"], t["category"]), (requirement, obligation, risk, "implementation-defined"), t["case_id"])
            self.assertIn(f"selection recorded; observed effect under {named}: {first}", self.legs_text(t, "matched-reference-comparison"), t["case_id"])
            declared = {str(self.M._one(p, "id")) for p in self.M.S.children(self.M.S.children(self.M._one_form(
                ROOT / "evidence" / t["case_id"] / "planned-experiment.sexp", "experiment"), "verification")[0], "property")}
            named_ids = {word.strip() for group in re.findall(r"\(([^()]*)\)", self.M.FEATURE_DISPOSITIONS[obligation])
                         for word in re.split(r"[,;]", group) if re.fullmatch(r"[a-z][a-z0-9.]*(-[a-z0-9.]+)+", word.strip())}
            self.assertTrue(named_ids, t["case_id"]); self.assertEqual(named_ids - declared, set(), t["case_id"])
        for t in batch:
            self.assertEqual((t["requirement_id"], t["obligation_ids"][0], t["risk"], t["category"]), (*{**BATCH_I, **LAST_DEFINED}[t["case_id"]], "defined"), t["case_id"])
            self.assertEqual(t["coverage"]["required"], t["coverage"]["predeclared"], t["case_id"])
            quiet = READ_AFTER.get(t["case_id"])
            self.assertEqual(f"writing no GPR, read after their own step: {quiet}" in self.legs_text(t, "form-coverage"), bool(quiet), t["case_id"])
            # Each property a disposition names in its lists is one the case declares (a47-3).
            declared = {str(self.M._one(p, "id")) for p in self.M.S.children(self.M.S.children(self.M._one_form(
                ROOT / "evidence" / t["case_id"] / "planned-experiment.sexp", "experiment"), "verification")[0], "property")}
            named = {word.strip() for group in re.findall(r"\(([^()]*)\)", self.M.FEATURE_DISPOSITIONS[t["obligation_ids"][0]])
                     for word in re.split(r"[,;]", group) if re.fullmatch(r"[a-z][a-z0-9.]*(-[a-z0-9.]+)+", word.strip())}
            self.assertEqual(named - declared, set(), t["case_id"])
        rows = [20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32]
        self.assertEqual(table["boundary"], dict(present=rows, predeclared=rows))
        forms = ["div", "divu", "divuw", "divw", "mul", "mulh", "mulhsu", "mulhu", "mulw", "rem", "remu", "remuw", "remw"]
        self.assertEqual((table["coverage"]["predeclared"], table["coverage"]["exercised"], table["coverage"]["required"]),
                         (forms, forms, forms))
        self.assertEqual((table["requirement_id"], table["obligation_ids"], table["category"], table["risk"]),
                         ("REQ-GC-M", ["OB-GC-M"], "defined", "medium"))
        boundaries = [1, 5, 6, 7, 8, 9, 10, 13, 16, 24]
        self.assertEqual(xlen["boundary"], dict(present=boundaries, predeclared=boundaries))
        self.assertEqual(xlen["coverage"], dict(required=[], exercised=[], predeclared=[]))
        self.assertIn("coverage is vacuous, its 17 predeclared witnesses", self.legs_text(xlen, "form-coverage"))
        self.assertTrue(self.legs_text(xlen, "feature-rules").startswith("OB-XLEN: none applies: "))
        self.assertEqual((xlen["requirement_id"], xlen["obligation_ids"], xlen["category"], xlen["risk"]),
                         ("REQ-D-XLEN", ["OB-XLEN"], "defined", "low"))
        self.assertEqual((csr["requirement_id"], csr["obligation_ids"], csr["category"], csr["risk"]),
                         ("REQ-D-CSR-SET", ["OB-CSR-SET"], "implementation-defined", "high"))
        self.assertIn("selection recorded; observed effect under the profile override: step 34 (csrrs x20, mcycle, x0): Sail {}, "
                      "expectations {'x20': 34}", self.legs_text(csr, "matched-reference-comparison"))
        self.assertIn("coverage is vacuous, its 53 predeclared witnesses", self.legs_text(csr, "form-coverage"))
        self.assertIn("independent-exact-expectation", self.legs_text(csr, "risk-method"))
        self.assertIn("step 130 registers ['x28']", self.legs_text(csr, "discriminating-control"))
        # The feature disposition names properties; each is one this case declares.
        declared = {str(self.M._one(p, "id")) for p in self.M.S.children(self.M.S.children(self.M._one_form(
            ROOT / "evidence" / CSR_CASE_ID / "planned-experiment.sexp", "experiment"), "verification")[0], "property")}
        words = {word.strip("(),.;:") for word in self.M.FEATURE_DISPOSITIONS["OB-CSR-SET"].split()}
        cited = {word for word in words if word.startswith(("s-", "u-", "refused-", "alias-", "csr-", "mhartid-", "fs-"))}
        self.assertEqual(len(cited), 20, sorted(cited))
        self.assertEqual(cited - declared, set())
        self.assertEqual((zicntr["requirement_id"], zicntr["obligation_ids"], zicntr["category"], zicntr["risk"]),
                         ("REQ-D-ZICNTR", ["OB-ZICNTR"], "implementation-defined", "high"))
        self.assertIn("selection recorded; observed effect under the profile override: step 6 (rdcycle x5): Sail {}, "
                      "expectations {'x5': 6}", self.legs_text(zicntr, "matched-reference-comparison"))
        self.assertIn("coverage is vacuous, its 44 predeclared witnesses", self.legs_text(zicntr, "form-coverage"))
        self.assertIn("independent-exact-expectation", self.legs_text(zicntr, "risk-method"))
        self.assertIn("step 109 registers ['x21']", self.legs_text(zicntr, "discriminating-control"))
        declared = {str(self.M._one(p, "id")) for p in self.M.S.children(self.M.S.children(self.M._one_form(
            ROOT / "evidence" / ZICNTR_CASE_ID / "planned-experiment.sexp", "experiment"), "verification")[0], "property")}
        words = {word.strip("(),.;:") for word in self.M.FEATURE_DISPOSITIONS["OB-ZICNTR"].split()}
        cited = {word for word in words if word.startswith(("s-", "u-", "m-", "ro-", "alias-", "instret-", "cycle-", "trap-"))}
        self.assertEqual(len(cited), 26, sorted(cited))
        self.assertEqual(cited - declared, set())
        self.assertEqual((sstc["requirement_id"], sstc["obligation_ids"], sstc["category"], sstc["risk"]),
                         ("REQ-D-SSTC", ["OB-SSTC"], "implementation-defined", "high"))
        self.assertIn("selection recorded; observed effect under the profile override: step 8 (rdtime x5): Sail {}, "
                      "expectations {'x5': 8}", self.legs_text(sstc, "matched-reference-comparison"))
        self.assertIn("coverage is vacuous, its 39 predeclared witnesses", self.legs_text(sstc, "form-coverage"))
        self.assertIn("independent-exact-expectation", self.legs_text(sstc, "risk-method"))
        self.assertIn("step 172 registers ['x11']", self.legs_text(sstc, "discriminating-control"))
        # The rule asks for delivery boundaries and suppression cases: the disposition names every property, so none goes unread.
        declared = {str(self.M._one(p, "id")) for p in self.M.S.children(self.M.S.children(self.M._one_form(
            ROOT / "evidence" / SSTC_CASE_ID / "planned-experiment.sexp", "experiment"), "verification")[0], "property")}
        words = {word.strip("(),.;:") for word in self.M.FEATURE_DISPOSITIONS["OB-SSTC"].split()}
        cited = {word for word in words if word.startswith(("s-", "u-", "m-", "not-", "pending-", "suppressed-", "stce-", "delivered-",
                                                            "delivery-", "scheduled-", "undelegated-"))}
        self.assertEqual((len(declared), cited), (39, declared))


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    if MUTATION:
        suite = unittest.defaultTestLoader.loadTestsFromName(MUTATION_TESTS[MUTATION], PolicyTests)
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(PolicyTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"DIV-POLICY-PROBE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; measurement only, no qualification credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
