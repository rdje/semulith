#!/usr/bin/env python3
"""Retain the licensed, source-pinned statements a matched case's properties cite, never the website shell.

A case's normative input is a retained excerpt whose wrapper names the one original page it was copied from, and that page
must be the case's source publication (`review_div_capture.check_retained_input`, `P4-SYSTEM.14` a44-2c). The M and RV64I
excerpts each have their own module (`retain_div_statement.py`, `retain_m_statements.py`, `retain_rv64i_statements.py`). This
is the one table for the cases after them (a43b-3b): an excerpt is a row of `EXCERPTS` — the page and its pin, the licence
evidence and its pin, the statements in source order, the retained path and its pin — and every row goes through the same
bounded pure transformation. Emission reads the acquired pages; verification authenticates only the retained file, without
them. Neither operation is a comparison, capture, property binding, credit or qualification.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys

import experiment_artifacts as A

ROOT = Path(__file__).resolve().parent.parent
PAGES = ".materials/riscv/pinned-v20260120/"
SITE = "https://docs.riscv.org/reference/isa/v20260120/"
PAGE_BYTES = 524288  # the longest pinned page a row names: priv/machine.html, 271,851 B
LICENCE_BYTES = 131072
RETAINED_BYTES = 8192
SPAN_BYTES = 1024
OPENING = "opening:"
PARAGRAPH = b'<div class="paragraph">\n<p>'
PARAGRAPH_END = b"</p>\n</div>"
# The sentence both volumes' prefaces state, line breaks included (materials/RVI_M_RETENTION.md).
LICENCE_STATEMENT = (
    b"Commons Attribution 4.0 International License by the original authors,\n"
    b"and this and future versions of this document will be released under the\n"
    b"same license."
)
# A statement's markup, measured span by span before review: emphasis, code, and the manual's own cross-reference to another
# page of the same publication — kept unmodified, as the licence's reproduction asks. Any other tag or attribute refuses.
OPENING_TAGS = (re.compile(rb"<em>"), re.compile(rb"<code>"),
                re.compile(rb'<a href="[a-z0-9-]+\.html#[A-Za-z0-9_:-]+" class="xref page">'))


@dataclass(frozen=True)
class Page:
    """One pinned page of the acquired snapshot."""
    input_id: str
    file: str
    sha256: str
    label: str  # how the wrapper names it


@dataclass(frozen=True)
class Excerpt:
    input_id: str
    heading: str
    source: Page
    licence: Page
    retained_path: str
    retained_sha256: str
    statements: tuple  # (span name, section), in source order
    scope_note: str


PRIVILEGED_LICENCE = Page("RVP-PRIV-LICENCE", "priv/priv-preface.html",
                          "6e4ba2ab3ea5174ff04881c48df7dfaf9402a0d070a76805535f1c7754645e59",
                          "privileged preface to Version 1.10")
UNPRIVILEGED_LICENCE = Page("RVI-LICENCE", "unpriv/colophon.html",
                            "7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c",
                            "the unprivileged volume's preface")
EXCERPTS = {
    "RVP-CSR-STATEMENTS": Excerpt(
        "RVP-CSR-STATEMENTS", "RVP-CSR §1.1.1: which privilege may access a CSR, and what an attempt without it does",
        Page("RVP-CSR", "priv/priv-csrs.html", "330a17314ef803231955a915748176e5175fc773469f25a8c6b5ae922c9df425",
             "RISC-V Privileged Architecture, §1.1 Control and Status Registers (CSRs)"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html", "0f2d75c5e8fb85505577c62320d035680704d9afeb8aae0e978174edbc63aba6",
        (("norm:Zicsr_higher_priv", "§1.1.1"), ("norm:Zicsr_rw", "§1.1.1"), ("norm:Zicsr_access", "§1.1.1"),
         ("norm:Zicsr_illegal_mode", "§1.1.1"), ("norm:Zicsr_illegal_acc", "§1.1.1")),
        "This excerpt establishes no CSR-SET acceptance."),
    "RVI-ZICNTR-STATEMENTS": Excerpt(
        "RVI-ZICNTR-STATEMENTS", "RVI-ZICNTR §6.1: the counters are read-only CSRs, and what each of the base three counts",
        Page("RVI-ZICNTR", "unpriv/counters.html", "8d619d6ef71d6cd87415342782aa615a0aff121a537342e4497658947f4fa81c",
             "RISC-V Unprivileged Architecture, §6.1 \"Zicntr\" and \"Zihpm\" Extensions for Counters, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-zicntr-statements.html", "ee5bca84e2b9cc3be2c797535adcf701892967687e379c5d4df3738e7e4aad49",
        (("norm:zihpm_op_sz_mode_acc_count", "§6.1"), ("norm:zihpm_op_sz_mode_acc_priv", "§6.1"),
         ("norm:zihpm_op_sz_mode_acc_partition", "§6.1"), ("norm:zicntr_rdcycle_op", "§6.1.1"),
         ("norm:zicntr_rdtime_op", "§6.1.1"), ("norm:zicntr_rdinstret_op", "§6.1.1")),
        "This excerpt establishes no ZICNTR acceptance."),
    "RVP-COUNTEREN-STATEMENTS": Excerpt(
        "RVP-COUNTEREN-STATEMENTS", "RVP-MACHINE §2.1.1.11: what mcounteren gates, and what a read it refuses does",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-counteren-statements.html", "a47ba18329dd6d7d4079f2f37c96619a8cb4347b4e973d37cc80e10ede27890a",
        (("norm:mcounteren_op", "§2.1.1.11"), ("norm:mcounteren_inc_inaccessible", "§2.1.1.11"),
         ("norm:mcounteren_clr_ill_inst_exc", "§2.1.1.11"), ("norm:mcounteren_set_nxt_priv", "§2.1.1.11")),
        "This excerpt establishes no ZICNTR acceptance; the scounteren statement has no anchor to select in its own page, so it is cited, not retained."),
    "RVP-SSTC-STATEMENTS": Excerpt(
        "RVP-SSTC-STATEMENTS", "RVP-SSTC §12.1: why supervisor mode has its own timer, and what the extension adds",
        Page("RVP-SSTC", "priv/sstc.html", "30bea862eee800d485ce34636b2824bf9909a4676b39d2c5734e92fba14216e1",
             "RISC-V Privileged Architecture, §12.1 \"Sstc\" Extension for Supervisor-mode Timer Interrupts, Version 1.0"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-sstc-statements.html", "8032b3fff7e2861adf58a2965f5cca55025242b9ae46f3f034c24677cbf3e7a6",
        (("opening:This extension serves", "§12.1"), ("opening:The extension name is", "§12.1")),
        "This excerpt establishes no SSTC acceptance; the chapter anchors none of its text, so each paragraph is selected by the words it opens with."),
    "RVP-STIMECMP-STATEMENTS": Excerpt(
        "RVP-STIMECMP-STATEMENTS", "RVP-SUPERVISOR §11.1.1.3 and §11.1.1.12: when a supervisor interrupt traps, and what stimecmp makes pending",
        Page("RVP-SUPERVISOR", "priv/supervisor.html", "d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a",
             "RISC-V Privileged Architecture, §11.1 Supervisor-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-stimecmp-statements.html", "7f2362b1cc60afb3281c82e50e244b6dd4b971e13eae25c0aac46e3601d3b6e3",
        (("norm:sie_sip_supervisor_strap", "§11.1.1.3"), ("norm:sie_sip_strap_time_constraint", "§11.1.1.3"),
         ("norm:sip-stip_sie-stie", "§11.1.1.3"), ("norm:stimecmp-stimecmph_sz_acc", "§11.1.1.12"), ("norm:mip_sip-stip_op", "§11.1.1.12")),
        "This excerpt establishes no SSTC acceptance."),
    "RVP-STCE-STATEMENTS": Excerpt(
        "RVP-STCE-STATEMENTS", "RVP-MACHINE §2.1.1.9 and §2.1.1.18: how stimecmp drives STIP, and what menvcfg.STCE gates",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-stce-statements.html", "dd8a425e87b394c6bc655c98724debc3875f690c903685f8a3f84eb504306c15",
        (("norm:mip_stip_stimecmp_acc", "§2.1.1.9"), ("norm:mip_stip_stimecmp_op2", "§2.1.1.9"), ("norm:mip_stip_stimecmp_clr", "§2.1.1.9"),
         ("norm:menvcfg_stce_op1", "§2.1.1.18"), ("norm:menvcfg_stce_op2", "§2.1.1.18")),
        "This excerpt establishes no SSTC acceptance."),
    "RVI-RV32I-STATEMENTS": Excerpt(
        "RVI-RV32I-STATEMENTS", "RVI-RV32I §1.1.2 and §1.1.4 to §1.1.6: what the base's integer, jump and branch forms do, and what a load to x0 still does",
        Page("RVI-RV32I", "unpriv/rv32.html", "3b20e92f067509535f95883832e84b32dbea43a29e1347b7925c374213ad75ec",
             "RISC-V Unprivileged Architecture, §1.1 RV32I Base Integer Instruction Set, Version 2.1"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-rv32i-statements.html", "c476fd879407a93271d504e8cff80bdae93822d8319951b1252485715e0256ef",
        (("norm:imm_always_sex", "§1.1.2"), ("norm:addi_op", "§1.1.4.1"), ("norm:addi_overflow", "§1.1.4.1"), ("norm:slti_sltiu_op", "§1.1.4.1"),
         ("norm:andi_ori_xori_op", "§1.1.4.1"), ("norm:add_op", "§1.1.4.2"), ("norm:sub_op", "§1.1.4.2"), ("norm:add_sub_overflow", "§1.1.4.2"),
         ("norm:slt_sltu_op", "§1.1.4.2"), ("norm:and_or_xor_op", "§1.1.4.2"), ("norm:no_cti_delay_slots", "§1.1.5"), ("norm:jal_target", "§1.1.5.1"),
         ("norm:jal_op", "§1.1.5.1"), ("norm:jalr_target", "§1.1.5.1"), ("norm:jalr_op", "§1.1.5.1"), ("norm:br_target", "§1.1.5.2"),
         ("norm:beq_bne_op", "§1.1.5.2"), ("norm:blt_bltu_op", "§1.1.5.2"), ("norm:bge_bgeu_op", "§1.1.5.2"), ("norm:load_exc_x0", "§1.1.6")),
        "This excerpt establishes no acceptance of any form or of RV32: the profile is RV64, and RV64I §3.1 inherits these statements at XLEN 64."),
    "RVI-RV64I-FORMS-STATEMENTS": Excerpt(
        "RVI-RV64I-FORMS-STATEMENTS", "RVI-RV64I §3.1.2.1 and §3.1.3: AUIPC at 64 bits, and what each load and store width does",
        Page("RVI-RV64I", "unpriv/rv64.html", "6eadb316c2d535ccb87a7a6feb03ff54af6f4b5bbeb5c1a5102a02af81f13abd",
             "RISC-V Unprivileged Architecture, §3.1 RV64I Base Integer Instruction Set, Version 2.1"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-rv64i-forms-statements.html", "f254c3fe90773b67f282984d61498f2f1008ffe214b8bc952baa628189b5d816",
        (("norm:auipc_op_rv64i", "§3.1.2.1"), ("norm:ld_op_rv64i", "§3.1.3"), ("norm:lw_op_rv64i", "§3.1.3"), ("norm:lwu_op", "§3.1.3"),
         ("norm:lh_lhu_lb_lbu_op_rv64i", "§3.1.3"), ("norm:sd_sw_sh_sb_op_rv64i", "§3.1.3")),
        "This excerpt establishes no acceptance of any form; RVI-RV64I-STATEMENTS holds the rest of §3.1.2 for the XLEN case."),
    "RVP-ECALL-STATEMENTS": Excerpt(
        "RVP-ECALL-STATEMENTS", "RVP-MACHINE §2.1.1.8, §2.1.1.14 to §2.1.1.16 and §2.1.3.1: what ECALL and EBREAK raise, what a trap records, and what delegation does",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-ecall-statements.html", "2ee5d450e951ab07758ebc20d46898084adac83acfc9c502965783bdc9b3027b",
        (("norm:medeleg_mideleg_op1", "§2.1.1.8"), ("norm:mepc_op", "§2.1.1.14"), ("norm:mcause_op", "§2.1.1.15"), ("norm:mtval_op", "§2.1.1.16"), ("norm:mtval_other_traps_zero", "§2.1.1.16"), ("norm:ecall_op2", "§2.1.3.1"), ("norm:ebreak_op2", "§2.1.3.1")),
        "This excerpt establishes no acceptance of a trap, or of the laboratory's halting report, which is not one."),
    "RVI-ZICSR-STATEMENTS": Excerpt(
        "RVI-ZICSR-STATEMENTS", "RVI-ZICSR §5.1.1: what each CSR instruction reads and writes, and when it writes nothing",
        Page("RVI-ZICSR", "unpriv/zicsr.html", "0c06e00db7343b293a120e6378a4eee7e4c101a5786a9b661513ceed7dcf047d",
             "RISC-V Unprivileged Architecture, §5.1 \"Zicsr\" Extension for Control and Status Register Instructions, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-zicsr-statements.html", "cb4e86950ad1c41daf2824369ee3a39142dae14df47f33d4fa2facb5b21718d3",
        (("norm:csrrw_op", "§5.1.1"), ("norm:csrrs_op", "§5.1.1"), ("norm:csrrc_op", "§5.1.1"), ("norm:csrrs_csrrc_rs1_x0", "§5.1.1"), ("norm:csrrw_rs1_x0", "§5.1.1"), ("norm:csrrsi_csrrci_uimm_zero", "§5.1.1"), ("norm:csrrwi_rd_x0", "§5.1.1")),
        "This excerpt establishes no acceptance; the immediate forms' own paragraph carries a nested span the tool's markup bound refuses, so it is cited, not retained."),
    "RVI-ZIFENCEI-STATEMENTS": Excerpt(
        "RVI-ZIFENCEI-STATEMENTS", "RVI-ZIFENCEI §4.1: what FENCE.I orders",
        Page("RVI-ZIFENCEI", "unpriv/zifencei.html", "4026de34713f4b898595eb4a17bb58176a0e2905196705a904d3d8fab4432a91",
             "RISC-V Unprivileged Architecture, §4.1 \"Zifencei\" Extension for Instruction-Fetch Fence, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-zifencei-statements.html", "3f1d5189db9a452e9ee5e798eebed1d5e58bd2a62351856bf44e424ed7649616",
        (("norm:fence_i_op", "§4.1"),),
        "This excerpt establishes no acceptance."),
    "RVI-C-STATEMENTS": Excerpt(
        "RVI-C-STATEMENTS", "RVI-C §27.1: where an instruction may start with C present, and what no longer raises an exception",
        Page("RVI-C", "unpriv/c-st-ext.html", "3f7e7d853d6e12e9d44c3d1bb488d1c312179a308d608182fb01db43a49d6aeb",
             "RISC-V Unprivileged Architecture, §27.1 \"C\" Extension for Compressed Instructions, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-c-statements.html", "29d8088d19c6cebcefe3445b3d5574343094c5d0a1edb58a6d665be73c1c5db8",
        (("norm:Zca_align16", "§27.1"), ("norm:Zca_no_misaligned", "§27.1")),
        "This excerpt establishes no acceptance of a compressed form: REQ-GC-C is its own case."),
    "RVI-A-STATEMENTS": Excerpt(
        "RVI-A-STATEMENTS", "RVI-A §12.1.1, §12.1.2 and §12.1.4: what LR and SC do and what ends a reservation, and what a word AMO does with its operands",
        Page("RVI-A", "unpriv/a-st-ext.html", "afbd8def7bdf64287ef51a9cb14dd654fba0f0cfeef63bccdfd47408f5b0dff2",
             "RISC-V Unprivileged Architecture, §12.1 \"A\" Extension for Atomic Instructions, Version 2.1"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-a-statements.html", "897382a40a917d98f563d7ca10525c7ef80392bfbfd6d779e086a0b10ddb9db0",
        (("norm:a_no_aq_rl", "§12.1.1"), ("norm:lr_w_op", "§12.1.2"), ("norm:sc_w_success", "§12.1.2"), ("norm:sc_w_failure", "§12.1.2"), ("norm:sc_reservation_invalidate", "§12.1.2"), ("norm:lr_sc_rv64", "§12.1.2"), ("norm:sc_failure_code", "§12.1.2"), ("norm:sc_intervening_sc_fail", "§12.1.2"), ("norm:constrained_lrsc_compressed_allowed", "§12.1.3"), ("norm:amo_operand_size", "§12.1.4")),
        "This excerpt establishes no acceptance. The misaligned rule, which REQ-D-ATOMIC-MISALIGN owns, is not retained, nor RVP-SUPERVISOR's translation text, which is cited."),
    "RVP-MODES-STATEMENTS": Excerpt(
        "RVP-MODES-STATEMENTS", "RVP-INTRO §Introduction: the privilege levels and what each is for",
        Page("RVP-INTRO", "priv/priv-intro.html", "12c7a31aafbc32fa1f4fab82d60786c65af35f68e648aca7575a05034edf525e",
             "RISC-V Privileged Architecture, Introduction"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-modes-statements.html", "4c105a6e8f0a1b28f79d4dcfc947b08e1a1b60a475b1b10c5dc6b00fac79e349",
        (("norm:always-priv-level", "Introduction"), ("norm:m-level-high-priv-only-mandatory", "Introduction"), ("opening:Each privilege level has a core set", "Introduction"), ("opening:A hart normally runs application code in U-mode", "Introduction")),
        "This excerpt establishes no acceptance of a mode: REQ-D-PRIV-MODES is its own case."),
    "RVP-TRANSLATION-STATEMENTS": Excerpt(
        "RVP-TRANSLATION-STATEMENTS", "RVP-SUPERVISOR §11.1.1.11, §11.1.3.1 and §11.1.4: an unsupported MODE, the A and D schemes, and what Sv39 is",
        Page("RVP-SUPERVISOR", "priv/supervisor.html", "d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a",
             "RISC-V Privileged Architecture, §11.1 Supervisor-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-translation-statements.html", "3e70839ff01d168e0f51a6a093f1090bd33f8b36b4414df3dc8736c2122a81de",
        (("norm:satp-mode_op_unsupported", "§11.1.1.11"), ("opening:Each leaf PTE contains an accessed", "§11.1.3.1"), ("opening:Two schemes to manage the A and D bits are defined:", "§11.1.3.1"), ("opening:The A and D bits are never cleared", "§11.1.3.1"), ("norm:Svadu_disabled_hw_update_falls_back_to_svade", "§11.1.10"), ("norm:Sv39_sxlen", "§11.1.4"), ("norm:Sv39_va_sz", "§11.1.4"), ("norm:Sv39_va_signext", "§11.1.4"), ("norm:Sv39_levels", "§11.1.4"), ("norm:Sv39_leaf_any_level", "§11.1.4"), ("norm:Sv39_page_sizes", "§11.1.4")),
        "This excerpt establishes no acceptance. The walk's numbered steps, a list the tool does not read, are cited and not retained."),
    "RVP-PRIORITY-STATEMENTS": Excerpt(
        "RVP-PRIORITY-STATEMENTS", "RVP-MACHINE §2.1.1.15: the one position the priority table leaves open",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-priority-statements.html", "4f78fa49b581ec31447fa0a1aef0aa4e122317919bb3313bdfd7b4ce61021093",
        (("norm:mcause_exccode_pri2", "§2.1.1.15"),),
        "This excerpt establishes no acceptance. The priority table, which the tool's markup bound does not read, is cited and not retained."),
    "RVI-A-RESERVATION-STATEMENTS": Excerpt(
        "RVI-A-RESERVATION-STATEMENTS", "RVI-A §12.1.2 and §12.1.3: what a reservation may cover, what an SC needs, and misaligned atomics",
        Page("RVI-A", "unpriv/a-st-ext.html", "afbd8def7bdf64287ef51a9cb14dd654fba0f0cfeef63bccdfd47408f5b0dff2",
             "RISC-V Unprivileged Architecture, §12.1 \"A\" Extension for Atomic Instructions, Version 2.1"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-a-reservation-statements.html", "5b92b951ce522b822438991fceb17848be59d8664c6b3405118eb1a1425e0677",
        (("norm:sc_w_success", "§12.1.2"), ("norm:sc_w_failure", "§12.1.2"), ("norm:sc_retire_permission", "§12.1.2"), ("norm:sc_failed_side_effects", "§12.1.2"), ("norm:sc_failed_as_store", "§12.1.2"), ("norm:sc_reservation_invalidate", "§12.1.2"), ("norm:sc_failure_code", "§12.1.2"), ("norm:lr_sc_alignment", "§12.1.2"), ("norm:lr_reservation_set_size", "§12.1.2"), ("norm:sc_pairs_latest_lr", "§12.1.2"), ("norm:sc_success_conditions", "§12.1.2"), ("norm:sc_addr_not_in_reservation_fail", "§12.1.2"), ("norm:amo_alignment", "§12.1.4")),
        "This excerpt establishes no acceptance."),
    "RVI-NAMING-STATEMENTS": Excerpt(
        "RVI-NAMING-STATEMENTS", "RVI-NAMING §36.1: what the letters name, and what G abbreviates",
        Page("RVI-NAMING", "unpriv/naming.html", "4ab3aa0dc9f5626e522eb6849708197f0f014903532a04dbe03dd8bed64abb1d",
             "RISC-V Instruction Set Manual, §36.1 ISA Extension Naming Conventions"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-naming-statements.html", "621ce77e463bd374dd9ac3ac03f87c088cfd2e8df5e6a497946955b3247c0b94",
        (("opening:Standard ISA extensions are given a name", "§36.1"), ("opening:We have also defined an abbreviation", "§36.1")),
        "This excerpt establishes no acceptance of the composition: REQ-D-GC-COMPOSITION is its own case."),
    "RVI-ZC-STATEMENTS": Excerpt(
        "RVI-ZC-STATEMENTS", "RVI-ZC §28.1.2: what C decomposes into, and where Zcf exists",
        Page("RVI-ZC", "unpriv/zc.html", "3bc5a6f600995f96df57ea895f7db1f7fdba5967e7f084ae0be0e7a0d53924b6",
             "RISC-V Instruction Set Manual, §28.1 Zc Extensions for Compressed Instructions"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-zc-statements.html", "2f46aedf9377ba698ab297187b84703f3b5d978d1a09ed71aa311b9bb32a810e",
        (("opening:The Zca extension is added", "§28.1.2"), ("opening:Zcf is the existing set", "§28.1.2"), ("opening:Zcf is only relevant to RV32", "§28.1.2"), ("opening:Zcd is the existing set", "§28.1.2")),
        "This excerpt establishes no acceptance of the closure: REQ-D-EXT-CLOSURE is its own case. The statements of what Zcf and Zcd depend on carry links the tool's markup bound refuses, so they are cited and not retained."),
    "RVI-RVWMO-STATEMENTS": Excerpt(
        "RVI-RVWMO-STATEMENTS", "RVI-RVWMO §17.1: what the memory model is defined over",
        Page("RVI-RVWMO", "unpriv/rvwmo.html", "6126b0e31c33f3ff492308c14f264e9f86ae0d30dfeddaa6f834191c0ab37d91",
             "RISC-V Instruction Set Manual, §17.1 RVWMO Memory Consistency Model, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-rvwmo-statements.html", "41ca6c741dc8e51f2592c2847cb5e74e0ec41528c4e71d7c41ae00c1740f559e",
        (("opening:The RVWMO memory model is defined in terms of", "§17.1"),),
        "This excerpt establishes no acceptance of a memory model, and one hart cannot: REQ-D-RVWMO says what its case leaves out."),
    "RVP-XRET-STATEMENTS": Excerpt(
        "RVP-XRET-STATEMENTS", "RVP-MACHINE §2.1.1.6, §2.1.3.2 and §2.1.3.3: trap returns, WFI, and the bits that intercept them",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-xret-statements.html", "67c69760bc4dffcdf0f2cb10c3b5bc29d7143fb4a746c4b85a6abb375e034ae5",
        (("norm:xret_in_higher_mode", "§2.1.3.2"), ("norm:xret_in_lower_mode", "§2.1.3.2"), ("norm:mstatus_mprv_clr_mret_sret_less_priv", "§2.1.1.6.3"), ("norm:mstatus_tsr_op", "§2.1.1.6.6"), ("norm:mstatus_tw_op", "§2.1.1.6.6"), ("norm:mstatus_tw_always_illegal", "§2.1.1.6.6"), ("norm:wfi_op", "§2.1.3.3"), ("norm:wfi_intr_dis", "§2.1.3.3"), ("norm:wfi_no_intr_pc", "§2.1.3.3")),
        "This excerpt establishes no acceptance. The listings' table and the TVM statement, which the tool's markup bound does not read, are cited and not retained."),
    "RVI-C-FORMS-STATEMENTS": Excerpt(
        "RVI-C-FORMS-STATEMENTS", "RVI-C §27.1.3 to §27.1.7: control transfers, the scaled stack forms, what is reserved, and what a HINT leaves alone",
        Page("RVI-C", "unpriv/c-st-ext.html", "3f7e7d853d6e12e9d44c3d1bb488d1c312179a308d608182fb01db43a49d6aeb",
             "RISC-V Unprivileged Architecture, §27.1 \"C\" Extension for Compressed Instructions, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-c-forms-statements.html", "1680a609cf1a4acaeb5856ecb8c21a59ddd940f15ef4e5776393e98b7fe80332",
        (("norm:c-lwsp_rsv", "§27.1.3.1"), ("norm:c-fld_op", "§27.1.3.2"), ("norm:c-jr_op", "§27.1.4"), ("norm:c-jr_rsv", "§27.1.4"), ("norm:c-jalr_op", "§27.1.4"), ("norm:c-beqz_op", "§27.1.4"), ("norm:c-bnez_op", "§27.1.4"), ("norm:c-addi16sp_op", "§27.1.5.2"), ("norm:c-addi4spn_op", "§27.1.5.2"), ("norm:Zca_illegal", "§27.1.5.4"), ("norm:c-nop_op", "§27.1.5.5"), ("norm:c-ebreak_op", "§27.1.5.6"), ("norm:Zca_hints", "§27.1.7")),
        "This excerpt establishes no acceptance; RVI-C-STATEMENTS keeps §27.1's own two statements."),
    "RVI-F-STATEMENTS": Excerpt(
        "RVI-F-STATEMENTS", "RVI-F §20.1.2 to §20.1.8: reserved rounding modes, the canonical NaN, tininess, what the transfers keep, how conversions clip, and how compares signal",
        Page("RVI-F", "unpriv/f-st-ext.html", "8e42e6ae9b3ab18fcf9c3d4f26a1a251310e3fd08b67368235fb5e9affd32edd",
             "RISC-V Unprivileged Architecture, §20.1 \"F\" Extension for Single-Precision Floating-Point, Version 2.2"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-f-statements.html", "b5098ef80b88e5a3651e524f5dd314bc3977912e61441f9bd3217859f9ce6e33",
        (("norm:roundingmode_rsv", "§20.1.2"), ("norm:F_canonical_NaN", "§20.1.3"), ("norm:ieee_std_tininess", "§20.1.4"), ("norm:fsw_flw_bits_maintained", "§20.1.5"), ("norm:fmin-s_fmax-s_zero_compare", "§20.1.6"), ("norm:fmin-s_fmax-s_one_nan_input", "§20.1.6"), ("norm:fcvt_unrepresentable_nv", "§20.1.7"), ("norm:fcvt_round", "§20.1.7"), ("norm:fsgnj-s_fsgnjn-s_fsgnjx-s_op", "§20.1.7"), ("norm:fmv-x-w_op", "§20.1.7"), ("norm:fmv-w-x_op", "§20.1.7"), ("norm:flt-s_fle-s_signaling", "§20.1.8"), ("norm:feq-s_quiet", "§20.1.8")),
        "This excerpt establishes no acceptance. The accrued-flags and rounding-mode paragraphs carry links the tool's markup bound refuses, and the conversion and classify tables are not statements: each is cited, not retained."),
    "RVI-D-STATEMENTS": Excerpt(
        "RVI-D-STATEMENTS", "RVI-D §21.1.2 to §21.1.7: NaN boxing, what the transfers keep, the two format conversions, and how the double forms read their single counterparts",
        Page("RVI-D", "unpriv/d-st-ext.html", "fe3beb3c4db381063bccf03f5451d0a6184100ac37bb39b4dd1ec726a2befde4",
             "RISC-V Unprivileged Architecture, §21.1 \"D\" Extension for Double-Precision Floating-Point, Version 2.2"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-d-statements.html", "86bad16178d4bcf476687044f0e612fc7c013d31d25cde8d19c1f5966705d9df",
        (("norm:fp_nan-boxing", "§21.1.2"), ("norm:FP_transfer_instrs_narrow_transfer_in", "§21.1.2"), ("norm:FP_nontransfer_instrs_improper_nan-boxed_input", "§21.1.2"), ("norm:fld_fsd_bits_maintained", "§21.1.3"), ("norm:D_computational_instrs", "§21.1.4"), ("norm:fcvt-w-d_fcvt-wu-d_sign_ext", "§21.1.5"), ("norm:fcvt_float_rounding", "§21.1.5"), ("norm:fmv_bits_preserved", "§21.1.5"), ("norm:D_compare_instrs", "§21.1.6"), ("norm:fclass-d_op", "§21.1.7")),
        "This excerpt establishes no acceptance; RVI-F-STATEMENTS holds the rules these forms read as defined analogously."),
}


class RetentionError(ValueError):
    """No partial retained artifact escapes a refused source transformation."""


def require(condition, reason):
    if not condition:
        raise RetentionError(reason)


def pinned(data, limit, digest, name):
    require(type(data) is bytes and 1 <= len(data) <= limit, name + " byte bound/type")
    require(hashlib.sha256(data).hexdigest() == digest, name + " pin differs")


def statement_marks(source: bytes, name: str) -> tuple[bytes, bytes, bytes]:
    """What opens and closes a row's statement, and what opens its quoted bytes.

    A statement is a span by its anchor, as most are. The manual also anchors a whole paragraph, and the Sstc chapter anchors nothing, so `opening:<words>`
    selects the one paragraph that opens with exactly those words. A span is quoted with its own tags; a paragraph is quoted from inside its `<p>`.
    """
    if name.startswith(OPENING):
        words = name[len(OPENING):].encode()
        return PARAGRAPH + words, PARAGRAPH_END, words
    span, anchored = b'<span id="' + name.encode() + b'">', b'<div id="' + name.encode() + b'" class="paragraph">\n<p>'
    if span not in source and anchored in source:
        return anchored, PARAGRAPH_END, b""
    return span, b"</span>", span


def select_span(source: bytes, name: str) -> bytes:
    marker, closing, quoted = statement_marks(source, name)
    start = source.find(marker)
    require(start >= 0, f"{name}: statement is absent")
    require(source.count(marker) == 1, f"{name}: statement is duplicated")
    end = source.find(closing, start + len(marker))
    require(end >= 0, f"{name}: statement is unterminated")
    first = start + len(marker) - len(quoted)
    tagged = closing == b"</span>"
    span = source[first: end + len(closing)] if tagged else source[first: end]
    require(len(span) <= SPAN_BYTES, f"{name}: statement exceeds bound")
    inner = span[len(marker): -len(closing)] if tagged else span
    for tag in re.findall(rb"<[a-zA-Z0-9][^>]*>", inner):
        require(any(shape.fullmatch(tag) for shape in OPENING_TAGS), f"{name} carries unreviewed markup {tag[:40]!r}")
    span.decode("utf-8")
    return span


def retain_statements(excerpt: Excerpt, source: bytes, licence: bytes) -> bytes:
    """Copy the row's exact spans after checking both complete, frozen primary inputs."""
    pinned(source, PAGE_BYTES, excerpt.source.sha256, excerpt.source.input_id)
    pinned(licence, LICENCE_BYTES, excerpt.licence.sha256, "licence evidence")
    require(LICENCE_STATEMENT in licence, "reviewed licence statement is absent")
    spans = [(name, section, select_span(source, name)) for name, section in excerpt.statements]
    header = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Retained {excerpt.source.input_id} statements — v20260120</title>
<body>
<h1>{excerpt.heading}</h1>
<p>Copyright © RISC-V International.
Manual text by RISC-V International and the original RISC-V ISA manual authors.
The quoted statements are licensed under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
Semulith adds this wrapper and retains only the named statements; all surrounding
text, diagrams and website assets are omitted. Each quoted span is unmodified.
No endorsement is implied.</p>
<p>Source: <a href="{SITE}{excerpt.source.file}">RISC-V Ratified Specifications Library,
v20260120, {excerpt.source.label}</a>.<br>
Original page SHA256: <code>{excerpt.source.sha256}</code>.<br>
Licence evidence: <a href="{SITE}{excerpt.licence.file}">{excerpt.licence.label}</a>,
whose statement also covers future manual versions.<br>
Licence-evidence page SHA256: <code>{excerpt.licence.sha256}</code>.<br>
Transformation: <code>scripts/retain_statements.py</code>.
{excerpt.scope_note}</p>
""".encode("utf-8")
    body = b"".join(f'<h2>{section}: <code>{name}</code></h2>\n<blockquote><p>'.encode("utf-8") + span
                    + b"</p></blockquote>\n" for name, section, span in spans)
    retained = header + body + b"</body></html>\n"
    require(len(retained) <= RETAINED_BYTES, "retained artifact exceeds bound")
    return retained


def read_pin(root, *, path, digest, limit, input_id):
    return A.read_snapshot(root, "input", dict(id=input_id, path=path, sha256=digest), max_bytes=limit)


def verify_retained(excerpt: Excerpt, root=ROOT):
    """Authenticate the curated input alone; no acquired source/cache access."""
    return read_pin(root, path=excerpt.retained_path, digest=excerpt.retained_sha256, limit=RETAINED_BYTES,
                    input_id=excerpt.input_id).pin


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--emit", metavar="INPUT_ID", choices=sorted(EXCERPTS),
                         help="print one retained artifact from the acquired pages")
    actions.add_argument("--verify", action="store_true", help="authenticate every tracked excerpt without the acquired pages")
    args = parser.parse_args(argv)
    if args.verify:
        worst = 0
        for excerpt in EXCERPTS.values():
            pin = verify_retained(excerpt)
            print(json.dumps(dict(id=excerpt.input_id, disposition=pin.disposition, reason=pin.reason, path=pin.path,
                                  byte_size=pin.byte_size, sha256=pin.sha256)))
            worst = max(worst, 0 if pin.disposition == "matched" else 2 if pin.disposition == "unavailable" else 1)
        return worst
    excerpt = EXCERPTS[args.emit]
    inputs = []
    for page, limit in ((excerpt.source, PAGE_BYTES), (excerpt.licence, LICENCE_BYTES)):
        snapshot = read_pin(ROOT, path=PAGES + page.file, digest=page.sha256, limit=limit, input_id=page.input_id)
        if snapshot.pin.disposition != "matched":
            print(json.dumps(dict(disposition=snapshot.pin.disposition, reason=snapshot.pin.reason)), file=sys.stderr)
            return 2 if snapshot.pin.disposition == "unavailable" else 1
        inputs.append(snapshot.data)
    try:
        output = retain_statements(excerpt, *inputs)
    except (RetentionError, UnicodeError) as exc:
        print(json.dumps(dict(disposition="refused", reason=str(exc))), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
