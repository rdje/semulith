#!/usr/bin/env python3
"""Verify the prepared inputs of every reviewed case through public owners; no execution/qualification."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import types
import unittest
from unittest.mock import patch

import capture_div as Command
import check_sexp_schema as K
import dossier_sexp as D
import experiment_artifacts as A
import matched_gpr_artifacts as F
import matched_gpr_collector as Collector
import matched_gpr_comparison as C
import matched_gpr_image as G
import matched_gpr_property as P
import matched_gpr_source_image as B
import prepare_div_inputs as Prep
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
GUESTS = "profiles/rv64gc-lab-v0/guests"
OVERRIDE = "profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp"
INPUT_BYTES = 65536
FAMILY_FILES = 1101  # fifty cases of 22 slots each and the index: the tenth re-derivation, the window's peak (P4-SYSTEM.14 a49-1)
FAMILY_BYTES = 660 * 1024 * 1024  # fifty cases at most 691,408,896 B with the index
# The three cases the per-case controls read for their own reference configuration (P4-SYSTEM.14 a49-1).
CSR_SET, ZICNTR, SSTC = "rv64gc-csr-set-v3", "rv64gc-zicntr-v3", "rv64gc-sstc-v2"
# Batch II-b, the defined remainder (P4-SYSTEM.14 a48-1).
BATCH_II_B = ("rv64gc-atomics-v1", "rv64gc-c-forms-v1", "rv64gc-f-forms-v1", "rv64gc-d-forms-v1")
# The window that carries fetch faults re-issues the 19 credited cases under new ids (P4-SYSTEM.14 a49-1).
RENEWED = ("rv64gc-m-forms-v7", "rv64gc-xlen-forms-v4", "rv64gc-csr-set-v3", "rv64gc-zicntr-v3", "rv64gc-sstc-v2", "rv64gc-alu-imm-v2", "rv64gc-alu-reg-v2", "rv64gc-lui-auipc-v2", "rv64gc-jalr-lsb-v2", "rv64gc-no-delay-slots-v2", "rv64gc-shamt-v2", "rv64gc-wsuffix-v2", "rv64gc-load-ext-v2", "rv64gc-load-x0-v2", "rv64gc-ecall-ebreak-v2", "rv64gc-csr-access-v2", "rv64gc-counters-v2", "rv64gc-fencei-v2", "rv64gc-ialign-16-v2")
# The seven with a real switch (P4-SYSTEM.14 a50-2).
SWITCHES = ("rv64gc-svade-v1", "rv64gc-atomic-misalign-v1", "rv64gc-fault-priority-v1", "rv64gc-priv-modes-v1", "rv64gc-sv39-v1", "rv64gc-reservation-v1", "rv64gc-sc-deterministic-v1")
# The six `defined` of the last 17 (P4-SYSTEM.14 a51-1).
LAST_DEFINED = ("rv64gc-composition-v1", "rv64gc-ext-closure-v1", "rv64gc-priv-revision-v1", "rv64gc-rvwmo-v1", "rv64gc-priv-insns-v1", "rv64gc-priv-forms-v1")
# The two with a switch of the last 17 (P4-SYSTEM.14 a51-4).
LAST_SWITCHES = ("rv64gc-no-h-v1", "rv64gc-no-pmp-v1")
# The four with no switch of the last 17 (P4-SYSTEM.14 a51-8).
NO_SWITCH = ("rv64gc-endian-v1", "rv64gc-fence-v1", "rv64gc-walk-implicit-v1", "rv64gc-partial-progress-v1")
CASES = (P.CASE_ID, P.M_FORMS_CASE_ID, *BATCH_II_B, *RENEWED, *SWITCHES, *LAST_DEFINED, *LAST_SWITCHES, *NO_SWITCH)  # the 23 superseded directories left the tree at P4-SYSTEM.14 a49-4
OWN_CONFIGURATION = (CSR_SET, ZICNTR, SSTC, "rv64gc-counters-v2", "rv64gc-atomic-misalign-v1", "rv64gc-fault-priority-v1", "rv64gc-reservation-v1", "rv64gc-sc-deterministic-v1", "rv64gc-composition-v1", "rv64gc-priv-insns-v1", "rv64gc-priv-forms-v1")
# The pins this probe states on its own; a test holds them equal to the capture command's table.
PREPARED = {
    P.CASE_ID: {
        "guest.elf": ("guest-image", 4416,
                      "38a327660cb1c699e15694fe98d0467e909726555688074d558768300138e153"),
        "reference-config.json": ("reference-config", 7609,
                                  "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
        "baseline.expected.sexp": ("expectation", 5847,
                                   "87a5b54c50e147017a2dc60d69869d36679067026d7f449d75db6a344199907e"),
        "control.expected.sexp": ("expectation", 5443,
                                  "3f8d591db326a6a83a47921b7743297edc758eb602fa70660b770d37a07c758e"),
    },
    P.M_FORMS_CASE_ID: {
        "guest.elf": ("guest-image", 4440,
                      "208865142e1569636925a5cea6abff6fc4495f317d5d8e79a06e48d3b0f061b1"),
        "reference-config.json": ("reference-config", 7609,
                                  "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
        "baseline.expected.sexp": ("expectation", 7937,
                                   "561b5da3cf87ea4825fca4e1a001a9c7d26321e491d86515c571f47b0019f44f"),
        "control.expected.sexp": ("expectation", 7440,
                                  "ba99e4eca2e784d8389859e35cf04590c180162807311361eef70add589f4ba0"),
    },
}
PREPARED["rv64gc-m-forms-v7"] = {
    "guest.elf": ("guest-image", 4440,
        "208865142e1569636925a5cea6abff6fc4495f317d5d8e79a06e48d3b0f061b1"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 7937,
        "561b5da3cf87ea4825fca4e1a001a9c7d26321e491d86515c571f47b0019f44f"),
    "control.expected.sexp": ("expectation", 7440,
        "ba99e4eca2e784d8389859e35cf04590c180162807311361eef70add589f4ba0"),
}
PREPARED["rv64gc-xlen-forms-v4"] = {
    "guest.elf": ("guest-image", 4408,
        "89228f06141a273369da1607a3130b790b2ae722613f7e6b1edd48e92e57f5e0"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 6548,
        "5322f07f9df97863452a72f4dfb88bba17c3853c781fca6735235aa5947d5ffd"),
    "control.expected.sexp": ("expectation", 6100,
        "010b17f6a1b7bca1633c65d44a5b3c8f1ad8a9fb7d36cd1caa5e778507603510"),
}
PREPARED["rv64gc-csr-set-v3"] = {
    "guest.elf": ("guest-image", 4856,
        "a07daaefb204f47559c60adf8f2942515b6c56e8fdb757aad786c26042d1c7d4"),
    "reference-config.json": ("reference-config", 8748,
        "05746ed66c5f2805afe16c09b072edd373c284b73566a2252b4404f86fd59cea"),
    "baseline.expected.sexp": ("expectation", 34930,
        "92b53fad0ae9903d2a3a8f41941d5c46ab32083183b556bb34d24ef3553cb212"),
    "control.expected.sexp": ("expectation", 33688,
        "a8fb15bdc41fc8cb4d7e0bf4d5650df00a6bedf41d5286e6ab116571e6a01825"),
}
PREPARED["rv64gc-zicntr-v3"] = {
    "guest.elf": ("guest-image", 4960,
        "41f2cbc25ecdd0c5b5dbf8296f1957802a0cecb7e5c7da1d16567f1a04a04090"),
    "reference-config.json": ("reference-config", 8748,
        "05746ed66c5f2805afe16c09b072edd373c284b73566a2252b4404f86fd59cea"),
    "baseline.expected.sexp": ("expectation", 50381,
        "91dac468939659f85b048989d244978963430c745927e8aa4db81531f20d60fb"),
    "control.expected.sexp": ("expectation", 48335,
        "0df59ca83c31079227d425b70a0e5d5666c0a13c500869abdc7a43b03b780c5f"),
}
PREPARED["rv64gc-sstc-v2"] = {
    "guest.elf": ("guest-image", 5080,
        "e4b9a6c82738df70d30e59850a94c10f5e8390ebdd56c05181a74d1d0e491af9"),
    "reference-config.json": ("reference-config", 8748,
        "05746ed66c5f2805afe16c09b072edd373c284b73566a2252b4404f86fd59cea"),
    "baseline.expected.sexp": ("expectation", 53750,
        "05faa0dbaa4654542fde422f40e6bd0f3ef19a346800b00b9a1fc712e74df157"),
    "control.expected.sexp": ("expectation", 51552,
        "2dd7e190cc69431d698fa6d4b3f57e6e28d7e5c309b70208fc0083b76d6bbac6"),
}
PREPARED["rv64gc-alu-imm-v2"] = {
    "guest.elf": ("guest-image", 4384,
        "57b272f57b150c920591f5204da5743e06f5d1ed31f545162aad6405ba2cd9db"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4995,
        "0ac0b935338a6fa6e2aa59a1d4d9e416140212ba0d5dee434d8767124a4be06e"),
    "control.expected.sexp": ("expectation", 4562,
        "762fda139eba49a6e39b3a0b28bd9c07312eb3e7a49d11d858858110205f75e9"),
}
PREPARED["rv64gc-alu-reg-v2"] = {
    "guest.elf": ("guest-image", 4384,
        "69da28692b0480a098c69c4d60f7ad9b9abbbe8c72615c3e191e5d777b820c06"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4279,
        "4538368202c2b80d650a753022c8dc39546f5a300a3911da39b8bb4f0a31f4a0"),
    "control.expected.sexp": ("expectation", 3852,
        "a154b3c901de3111d36dc1246a006397c351d37652e88e72c4f96cb9b6a3c15e"),
}
PREPARED["rv64gc-lui-auipc-v2"] = {
    "guest.elf": ("guest-image", 4352,
        "bbe166bf5ac9f0a76c6f6067ab67beed31f1914b5f368776ee3bd3d004b4b744"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 2992,
        "ac74d4902255b2de8d2d909df0954b346bcb565cbab126cb25fe65fbc5159c8c"),
    "control.expected.sexp": ("expectation", 2616,
        "a3ae72f57e97051ef706611f77a758b558a3c1df7c746f1c703bad978380878b"),
}
PREPARED["rv64gc-jalr-lsb-v2"] = {
    "guest.elf": ("guest-image", 4416,
        "0d830b676e5361da3c94402a01b7e670a72f8f4078f8c11020c2d74a0e69c558"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4333,
        "f402a88a663394093a9768a009b845029bd20035442854c001f1bcc6a7833176"),
    "control.expected.sexp": ("expectation", 3949,
        "e333fffd1df790ffd26ae758ceed71f8fefe89d253234808714edaefc23127b1"),
}
PREPARED["rv64gc-no-delay-slots-v2"] = {
    "guest.elf": ("guest-image", 4424,
        "2fec987f5539f5c9000bce8e341583f6e159d6e8bd6f575de991e4c72afdc379"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4871,
        "4cf28a0d8e26aa668b3698f67b4c011793d5a7efc6469e0c82b7187609c5dc19"),
    "control.expected.sexp": ("expectation", 4425,
        "9d1fbbabda9ea2920106b47c05b78a4a8fa0e94baf601fb54b335f1c3bfc81d7"),
}
PREPARED["rv64gc-shamt-v2"] = {
    "guest.elf": ("guest-image", 4392,
        "1366f75906e44d5fee1f73c8b790d23885c1ad1f6472d7a9f38a67f851fef02a"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 5489,
        "4b3f01ba67f72f6667c47e456a25503845960bbeefdab415ebc213859c5a43d5"),
    "control.expected.sexp": ("expectation", 5049,
        "4af588ed3f48aa80a07b951496bc2d274f4a42c3df6b0308826ca0541a06626d"),
}
PREPARED["rv64gc-wsuffix-v2"] = {
    "guest.elf": ("guest-image", 4376,
        "9988499616f9410bcc274f27252593d605578ecddad4b049239ab355643b5df7"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4726,
        "bf773362eb009abf337e54cb6bc2f350bae2b950caa19d6c272c833ed955cddb"),
    "control.expected.sexp": ("expectation", 4324,
        "e2ecc2831e600059031b9e7bc784e7916ce6ac72dc8bb8a9337dbdec120122eb"),
}
PREPARED["rv64gc-load-ext-v2"] = {
    "guest.elf": ("guest-image", 4440,
        "2f23f23d967dcad3430b910087b3a1689969eac70def5448e994b843fa9d8fde"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 6800,
        "d2f06692dd2ca6dac19265e682aea52a4fdf0da50b0e470287b5244f6f23e7f8"),
    "control.expected.sexp": ("expectation", 6305,
        "da6d28c4ca6cf4ca06560f80396a992f594387bc708648e109a45305bc960a29"),
}
PREPARED["rv64gc-load-x0-v2"] = {
    "guest.elf": ("guest-image", 4448,
        "2b80ee55661ebb6857d76d4475c1589adacf55d1b666e46653bfeb1b920aef7a"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 15026,
        "cd912e422c36c992fed5e12ac3e669b080353d5ffd107ea43abc9a7b18c0d2a3"),
    "control.expected.sexp": ("expectation", 14318,
        "d01ae7f16c7cb2e4b37678123c2eece30330ea57e83ad51bbea1ff0b2ca6a327"),
}
PREPARED["rv64gc-ecall-ebreak-v2"] = {
    "guest.elf": ("guest-image", 4568,
        "88b1230a4c5b406a440c8b95e3b44e08fbc9c2f51efd0b915a642c7adfa8d25b"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 22402,
        "d42b8650cb3b3c1d2743cbcf6f61f0f993cb88f638cd33b2e4813caa17ec209e"),
    "control.expected.sexp": ("expectation", 21391,
        "19242549f01e003a460691b1412bb2870c043768dc278fe15865823e0005d37c"),
}
PREPARED["rv64gc-csr-access-v2"] = {
    "guest.elf": ("guest-image", 4552,
        "d5485858470b7c3f0d2e8a9368c9416b4163ff000b830b11fb941ee99853ceba"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 16479,
        "c7d714f7af6673efe5649d9754d254abf665e18998cce2b68c0db0a6fb4d85c4"),
    "control.expected.sexp": ("expectation", 15685,
        "4d99d2bc734b63da089366c198cfa1a248ede18d8a9728227f831de07fff2587"),
}
PREPARED["rv64gc-counters-v2"] = {
    "guest.elf": ("guest-image", 4560,
        "ff52584f79389225bfc528def5635ba3db7b76499f0ee78fc4a809102e704602"),
    "reference-config.json": ("reference-config", 8748,
        "05746ed66c5f2805afe16c09b072edd373c284b73566a2252b4404f86fd59cea"),
    "baseline.expected.sexp": ("expectation", 15121,
        "62c01e6d239d095ef603f15c1dcd7b2486f67ccc9abddb796726e7681f915a80"),
    "control.expected.sexp": ("expectation", 14297,
        "e840252a625e580dae3eb0a0b9dc3344216bddae4e68153d6fe83b4916120b92"),
}
PREPARED["rv64gc-fencei-v2"] = {
    "guest.elf": ("guest-image", 4384,
        "645e77468a89229cbc88e049725da326be3c525cc9244aded970817d53e1b4fa"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4209,
        "64b542a9a3c7bbd339cfea786b4b4066f2247884126f3ed2e1c49e0acf703bf2"),
    "control.expected.sexp": ("expectation", 3783,
        "605794b243ae788245069b45f3ccfebca1b0dd7085649be638b5a1ae91ad44f5"),
}
PREPARED["rv64gc-ialign-16-v2"] = {
    "guest.elf": ("guest-image", 4360,
        "33b461325bf7fad33f52382213b0528f0e75fba67a701477520afcbd859b709b"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 2884,
        "74310bc471db59ddfd137412043ea8c34768bf386fa9f60462a94cc7198e5d59"),
    "control.expected.sexp": ("expectation", 2527,
        "5b1257b4f5d14fc95104fc922b479b5cc2c9d902c1288faa5716830cc9a399a8"),
}
PREPARED["rv64gc-atomics-v1"] = {
    "guest.elf": ("guest-image", 5280,
        "a152841108b6b539ce542abd2093aa78107c5a0f350f18b46bfe62bd7a7fc588"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 45948,
        "b8e9448e06ac1570cd878d8c48256a0803ae80f7846a623c0831b8b3c5428c73"),
    "control.expected.sexp": ("expectation", 44162,
        "a34c4e9d1ea3eb0bca137787f36e99a12dc3fa500e325db5e0f7f53c90913fa2"),
}
PREPARED["rv64gc-c-forms-v1"] = {
    "guest.elf": ("guest-image", 5032,
        "ed231938317e7689bd597eaf1e2ed739bc40fdbef7afd143b10658bf69f4df3c"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 46782,
        "0333a85c744529a5f54bf80c6efc1754f13626efb40b118aa0716881837a5f61"),
    "control.expected.sexp": ("expectation", 44993,
        "cb9dbdc747a573802702b256ff0b10a1e19c6d850e17a480fefb9f852d11b8b7"),
}
PREPARED["rv64gc-f-forms-v1"] = {
    "guest.elf": ("guest-image", 5552,
        "ded5e6517050e4b02ba472135bd57b83f4a7fe3e28d029c4afedb9481a49d365"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 62048,
        "6c158cfc2b041511ae4dcb82d61d22f9f682ad59fd342c4b8283664e4bb005e0"),
    "control.expected.sexp": ("expectation", 59737,
        "ad1405329c6198c2c49bddfe32fc71c2247126aac250f434f366bb3e2119fc00"),
}
PREPARED["rv64gc-d-forms-v1"] = {
    "guest.elf": ("guest-image", 5632,
        "d820714ee4db5f9fe4e75983fba506c3d81d5a98b99e36b10f4aab548ee493a4"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 63974,
        "11a64ad200c7cf445e3f6632d2d5260859376b8ed0bc3cfd928524ab20c06e55"),
    "control.expected.sexp": ("expectation", 61609,
        "be9d0eafc629e9d9e9554c2ec12862fdfa02faa247b4f74835e5ac846a828757"),
}
PREPARED["rv64gc-svade-v1"] = {
    "guest.elf": ("guest-image", 4816,
        "2d09c17ab89312e22b2de884f1ef4566660fe8fca936f6deb1c8004ebf1183d5"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 26235,
        "97a60887bfe42a288b39809b00b23cfd3a240245f7f472df435f4b12c6f7b74b"),
    "control.expected.sexp": ("expectation", 25116,
        "221f025692c6b9d8160e5d6683561ca587befdf3ee4b17deda5434157d100d57"),
}
PREPARED["rv64gc-atomic-misalign-v1"] = {
    "guest.elf": ("guest-image", 4864,
        "c3e59e94c95f17cd8cc7b7deb40f79ea1708e83501aebceddde0f57f98ef2ee2"),
    "reference-config.json": ("reference-config", 7669,
        "795320f7a2c79910683818942c0ce6d0422f04a5f7550dd136db5800fe951472"),
    "baseline.expected.sexp": ("expectation", 34895,
        "466242a143c549f494d80f6fd2308eee5005fa93bf04a7777bc98ad41ad4030f"),
    "control.expected.sexp": ("expectation", 33490,
        "1921ec87cc197b0733fee937b37e23f233c35a0c3c00c81ad799df1018d3e3c4"),
}
PREPARED["rv64gc-fault-priority-v1"] = {
    "guest.elf": ("guest-image", 5072,
        "03c7e6057bd749dbe1f34e268fbe07c21364eae9c14d1bfc10355d61fd8d6d33"),
    "reference-config.json": ("reference-config", 7669,
        "795320f7a2c79910683818942c0ce6d0422f04a5f7550dd136db5800fe951472"),
    "baseline.expected.sexp": ("expectation", 51258,
        "6263dbf8f4c0a6197999e4ffd5d211aca405f0bde6a7084eb6b909a88fb86663"),
    "control.expected.sexp": ("expectation", 49312,
        "bb136b5381a20952d6e5b365c0d80e30ea9751d0c7f00fdade5594dc731126b2"),
}
PREPARED["rv64gc-priv-modes-v1"] = {
    "guest.elf": ("guest-image", 4680,
        "09b0687414532d8e1e5b87065e73bedf2f5f0d951bd54d019796552649155e62"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 20465,
        "a56b18157bcbbea28ee5d050050bbb3cf58957bbd5e06757083425eb6b4766d9"),
    "control.expected.sexp": ("expectation", 19537,
        "1aef6285148b26f538763063073bda2ad6fbfad86401284e6e2564cd1f5db563"),
}
PREPARED["rv64gc-sv39-v1"] = {
    "guest.elf": ("guest-image", 4848,
        "ee1ee892a452ed0dbaf0f4d80446c5876df7e1c7220c61a5e89966b107d8cbf2"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 26165,
        "7bf44f6a8674ebef780613278e006fd3dcf0909e36290d57917339db93cb7a8d"),
    "control.expected.sexp": ("expectation", 25063,
        "10a209260c197205acbe7f577af1b78e1acaaa6485223346be80473230fca110"),
}
PREPARED["rv64gc-reservation-v1"] = {
    "guest.elf": ("guest-image", 5048,
        "e6f5de4e3ea9e00d4c2aa6ddd1127944f6870d526e7041beb359f0496b161a4a"),
    "reference-config.json": ("reference-config", 7682,
        "e9d98b382f1533e1fb954ce009b306f54260c0063130108d3291c4ec1ffb65ee"),
    "baseline.expected.sexp": ("expectation", 34439,
        "98e67322615aaada21378f83f3ae3fae230dc4730466259495242a041a9d5523"),
    "control.expected.sexp": ("expectation", 32968,
        "d0b11f67e1b81bfe463648f5021cfee0566eebce861ae3f1e2ada1640c29b2fd"),
}
PREPARED["rv64gc-sc-deterministic-v1"] = {
    "guest.elf": ("guest-image", 4928,
        "5c613b81f9e07e632a896fcc13979947d0c1032998c1354432693121a7b9131f"),
    "reference-config.json": ("reference-config", 7682,
        "e9d98b382f1533e1fb954ce009b306f54260c0063130108d3291c4ec1ffb65ee"),
    "baseline.expected.sexp": ("expectation", 29676,
        "ada05dec997bf41bfcea757475042870e07c085e641633a213e3d61397b2bf37"),
    "control.expected.sexp": ("expectation", 28394,
        "d0443cb9520c903f554c64ce46a4733defdc26a9f5a01390ad6335de51dc043c"),
}
PREPARED["rv64gc-composition-v1"] = {
    "guest.elf": ("guest-image", 4488,
        "d77057e80b94b7da188e44ee0b11421e2c7e13da3f4b74f6cee2be7df10064d9"),
    "reference-config.json": ("reference-config", 8748,
        "05746ed66c5f2805afe16c09b072edd373c284b73566a2252b4404f86fd59cea"),
    "baseline.expected.sexp": ("expectation", 7964,
        "592fdab4aa26ad989dd5aaa0eb1fa0ca142f102d7728428aaf18920ed13bb0f8"),
    "control.expected.sexp": ("expectation", 7423,
        "091615d6764e216e9464f94dd381fd835804f4783eb66c09df90efaba008ab16"),
}
PREPARED["rv64gc-ext-closure-v1"] = {
    "guest.elf": ("guest-image", 4568,
        "8232f09dc24845b12ef813cc3dad9b9529914d43c631bdfc55d31614398d98e0"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 12096,
        "4360f8c24040774f653af535b1f8d0b2bbd52c11263aa061b0aa89aee62b168a"),
    "control.expected.sexp": ("expectation", 11400,
        "94c918e65f53eae709b91669334562b9d76dfeb600526eb1a15889085c8bb84b"),
}
PREPARED["rv64gc-priv-revision-v1"] = {
    "guest.elf": ("guest-image", 4480,
        "4d6664434d1b6a17bf324d0f52397687bf3ab4c452a2a5ff75bfe1d0e3f58ea8"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 7020,
        "2963f7a1d53d3dc3e9623cb31e7e9328ee917224fe4d090eec3254b586388025"),
    "control.expected.sexp": ("expectation", 6485,
        "ba254e77397fe0499e1578c29fec55ed41050a041638c939cc3ba4b721d6354f"),
}
PREPARED["rv64gc-rvwmo-v1"] = {
    "guest.elf": ("guest-image", 4456,
        "74e09c06908c1191bdb66d3747f0ab423a6e411ceace680584e2cedd0dd06662"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 6703,
        "fb615729e56e29324d8276265dc6d32909b9f0960c775929dd279b521aa4f5ac"),
    "control.expected.sexp": ("expectation", 6192,
        "c155c73aeaa209a6d99f7f63727bdc0799b9e35fed02c6562fae3dc6a93d8780"),
}
PREPARED["rv64gc-priv-insns-v1"] = {
    "guest.elf": ("guest-image", 4440,
        "25e66194e234aa84da37f1a2c202457bc281adb37928c934870ef929480aaa38"),
    "reference-config.json": ("reference-config", 7610,
        "593c07ad92e7d467144b6b9284d5506a1c0d2fd4deb3584792343b9cd1ee8e5e"),
    "baseline.expected.sexp": ("expectation", 5614,
        "9f8410be220feddf4494650a88d063c800b29ee5be94131bb7c05ff8f63c232e"),
    "control.expected.sexp": ("expectation", 5105,
        "d3dd624ffedbf143eb7f930c4c4b325fe61f98626cf36c97f01094106a95fdf7"),
}
PREPARED["rv64gc-priv-forms-v1"] = {
    "guest.elf": ("guest-image", 5512,
        "c55becbc34b5799d63c68fefc582309ae3860b7fb061d632eb718e95b2c07e0b"),
    "reference-config.json": ("reference-config", 7610,
        "593c07ad92e7d467144b6b9284d5506a1c0d2fd4deb3584792343b9cd1ee8e5e"),
    "baseline.expected.sexp": ("expectation", 61851,
        "7a3d54a4906fa5c73c1436340db36affb646dc9deef79d6899076df100f923d4"),
    "control.expected.sexp": ("expectation", 59472,
        "fcea08045620f2f47c8037b7b75ab3a682dfcb5688427df8e4349149ddf1e081"),
}
PREPARED["rv64gc-no-h-v1"] = {
    "guest.elf": ("guest-image", 4408,
        "04ca2a8c244b321a2a09d0565df288fc76bef12950ca8dd2a9960e6292a50791"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 4450,
        "9edb7928b5cb2697a50640a81f94942ff4a812a493367f64f563da3a5c80a278"),
    "control.expected.sexp": ("expectation", 4050,
        "3260b574a9024338106941db17f477405f5e3f9ac40f8e5f867d255d91f6a9cb"),
}
PREPARED["rv64gc-no-pmp-v1"] = {
    "guest.elf": ("guest-image", 4480,
        "5a52d533c794ed2046c4713ca0fbdda20b42390900f029cf3962bd6423a6cdeb"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 7762,
        "5599f718a9f9fb7e0a91226320cddb48c3b121c1480c4614047129f249881f17"),
    "control.expected.sexp": ("expectation", 7207,
        "f2a58246da5ed823f08b94dee837336491497da6e776dc4cbbd928cb640addea"),
}
PREPARED["rv64gc-endian-v1"] = {
    "guest.elf": ("guest-image", 4488,
        "f9dcaf6a1848c5e517be55413fa95edc43cef45156b676281d4b359424c4b629"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 8683,
        "67d2d7c162c58af41f88f6be8c5866bb67636671c32a5d4cd568b065b1f7886d"),
    "control.expected.sexp": ("expectation", 8117,
        "9afc4cfa97321bce3cccac957cd5d2a2987c1dd573d47feff490a4a29d01b8ce"),
}
PREPARED["rv64gc-fence-v1"] = {
    "guest.elf": ("guest-image", 4488,
        "f06d3accbaa6df6e8c9ed0f52eb00fb9132657d2dd6fc3cc7e76c727556f2102"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 8710,
        "8b626d64a5cb9830fd9405db4fe4dd29fd682f0de4f1d88aaa14818b34190105"),
    "control.expected.sexp": ("expectation", 8152,
        "23dc6b945ea11e445ad5b70fa15e70576ff32673ebf09fb2ce9c8445e43c7799"),
}
PREPARED["rv64gc-walk-implicit-v1"] = {
    "guest.elf": ("guest-image", 4704,
        "f3d5dcdca7523ec3098c45a19715a669326df0a28e03ba5fcc35bd409d2d1676"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 17985,
        "76668445c73f0478800f3444bbe0b4de13331f737f4e67c9fdda0785ff225a0f"),
    "control.expected.sexp": ("expectation", 17079,
        "915e2d17dd9fcc8cc3e1dbef9656e25b18a626fed11eba9bd1e07d0e3610f68f"),
}
PREPARED["rv64gc-partial-progress-v1"] = {
    "guest.elf": ("guest-image", 4896,
        "16e4724d2ce69dfcf4bf7c811b8932d760c67d79e421e3b9e41e175840063100"),
    "reference-config.json": ("reference-config", 7609,
        "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    "baseline.expected.sexp": ("expectation", 31343,
        "b15cd47006d287032096456f9baca6fde6d8aa34f1909cbeefea1a2012309858"),
    "control.expected.sexp": ("expectation", 30022,
        "1ee8f98ec2c7bd5a774030b3ee02dfed9b3af7fb429e53cf6f55661f367e4167"),
}
TOTALS = {P.CASE_ID: 23315, P.M_FORMS_CASE_ID: 27426, "rv64gc-m-forms-v7": 27426, "rv64gc-xlen-forms-v4": 24665, "rv64gc-csr-set-v3": 82222, "rv64gc-zicntr-v3": 112424, "rv64gc-sstc-v2": 119130, "rv64gc-alu-imm-v2": 21550, "rv64gc-alu-reg-v2": 20124, "rv64gc-lui-auipc-v2": 17569, "rv64gc-jalr-lsb-v2": 20307, "rv64gc-no-delay-slots-v2": 21329, "rv64gc-shamt-v2": 22539, "rv64gc-wsuffix-v2": 21035, "rv64gc-load-ext-v2": 25154, "rv64gc-load-x0-v2": 41401, "rv64gc-ecall-ebreak-v2": 55970, "rv64gc-csr-access-v2": 44325, "rv64gc-counters-v2": 42726, "rv64gc-fencei-v2": 19985, "rv64gc-ialign-16-v2": 17380, "rv64gc-atomics-v1": 102999, "rv64gc-c-forms-v1": 104416, "rv64gc-f-forms-v1": 134946, "rv64gc-d-forms-v1": 138824,
          "rv64gc-svade-v1": 63776, "rv64gc-atomic-misalign-v1": 80918, "rv64gc-fault-priority-v1": 113311, "rv64gc-priv-modes-v1": 52291, "rv64gc-sv39-v1": 63685, "rv64gc-reservation-v1": 80137, "rv64gc-sc-deterministic-v1": 70680,
          "rv64gc-composition-v1": 28623, "rv64gc-ext-closure-v1": 35673, "rv64gc-priv-revision-v1": 25594, "rv64gc-rvwmo-v1": 24960, "rv64gc-priv-insns-v1": 22769, "rv64gc-priv-forms-v1": 134445,
          "rv64gc-no-h-v1": 20517, "rv64gc-no-pmp-v1": 27058,
          "rv64gc-endian-v1": 28897, "rv64gc-fence-v1": 28959, "rv64gc-walk-implicit-v1": 47377, "rv64gc-partial-progress-v1": 73870}
BUDGETS = {P.CASE_ID: (27, 54), P.M_FORMS_CASE_ID: (33, 66), "rv64gc-m-forms-v7": (33, 66), "rv64gc-xlen-forms-v4": (25, 50), "rv64gc-csr-set-v3": (157, 314), "rv64gc-zicntr-v3": (292, 584), "rv64gc-sstc-v2": (315, 622), "rv64gc-alu-imm-v2": (19, 38), "rv64gc-alu-reg-v2": (18, 36), "rv64gc-lui-auipc-v2": (10, 20), "rv64gc-jalr-lsb-v2": (16, 32), "rv64gc-no-delay-slots-v2": (21, 42), "rv64gc-shamt-v2": (21, 42), "rv64gc-wsuffix-v2": (17, 34), "rv64gc-load-ext-v2": (32, 64), "rv64gc-load-x0-v2": (68, 136), "rv64gc-ecall-ebreak-v2": (116, 232), "rv64gc-csr-access-v2": (81, 162), "rv64gc-counters-v2": (84, 168), "rv64gc-fencei-v2": (18, 36), "rv64gc-ialign-16-v2": (11, 20), "rv64gc-atomics-v1": (246, 492), "rv64gc-c-forms-v1": (251, 424), "rv64gc-f-forms-v1": (338, 676), "rv64gc-d-forms-v1": (350, 700),
           "rv64gc-svade-v1": (137, 271), "rv64gc-atomic-misalign-v1": (180, 359), "rv64gc-fault-priority-v1": (271, 535), "rv64gc-priv-modes-v1": (109, 217), "rv64gc-sv39-v1": (135, 269), "rv64gc-reservation-v1": (190, 379), "rv64gc-sc-deterministic-v1": (159, 317),
           "rv64gc-composition-v1": (41, 80), "rv64gc-ext-closure-v1": (64, 123), "rv64gc-priv-revision-v1": (36, 71), "rv64gc-rvwmo-v1": (33, 65), "rv64gc-priv-insns-v1": (30, 59), "rv64gc-priv-forms-v1": (345, 689),
           "rv64gc-no-h-v1": (21, 41), "rv64gc-no-pmp-v1": (40, 79),
           "rv64gc-endian-v1": (42, 83), "rv64gc-fence-v1": (41, 81), "rv64gc-walk-implicit-v1": (95, 189), "rv64gc-partial-progress-v1": (163, 325)}


def bounded_bytes(path):
    with path.open("rb") as stream:
        payload = stream.read(INPUT_BYTES + 1)
    if not 1 <= len(payload) <= INPUT_BYTES:
        raise ValueError("prepared input exceeds 1..65536 bytes")
    return payload


def mapped(payload, kind, mapper):
    """Diagnostic-only raw validation followed by the existing single mapper."""
    if type(payload) is not bytes or not 1 <= len(payload) <= INPUT_BYTES:
        raise ValueError("invalid bounded document bytes")
    text = payload.decode("utf-8")
    constructs, operators = K.load_schema(ROOT / "schema" / (kind + ".sexp"))
    issues = K.validate_text(text, constructs, operators, kind)
    if issues:
        raise ValueError(issues[0])
    forms = [form for form in S.parse(text, kind) if form[0] != "comment"]
    if len(forms) != 1 or forms[0][0] != kind:
        raise ValueError("expected exactly one " + kind + " document")
    return mapper(forms[0])


def prefix(case_id):
    return "evidence/" + case_id


def input_record(case_id, name, path=None, digest=None):
    role, _, pinned = PREPARED[case_id][name]
    return dict(id="DIV-" + name, role=role, path=path or prefix(case_id) + "/" + name,
                sha256=pinned if digest is None else digest)


def prepared_bytes(root, case_id):
    check_retention_layout(root)
    result = {}
    for name, (_, size, _) in PREPARED[case_id].items():
        snapshot = A.read_snapshot(root, "input", input_record(case_id, name), max_bytes=INPUT_BYTES)
        if snapshot.pin.disposition != "matched" or len(snapshot.data) != size:
            raise ValueError("prepared artifact pin/size differs: " + name)
        result[name] = snapshot.data
    return result


def retention_limits():
    """Every declared case's finite slots; absent future outputs are permitted."""
    limits = {"README.md": 4096}
    for case_id in CASES:
        for name in PREPARED[case_id]:
            limits[case_id + "/" + name] = INPUT_BYTES
        for run in ("baseline", "repeat", "control"):
            for suffix, bound in (("trace", Collector.TRACE_BYTES),
                                  ("stdout", Collector.STREAM_BYTES),
                                  ("stderr", Collector.STREAM_BYTES),
                                  ("receipt.sexp", F.DOCUMENT_BYTES)):
                limits[case_id + "/" + run + "." + suffix] = bound
        for name in ("case.sexp", "planned-experiment.sexp", "dependencies.sexp", "authorities.sexp",
                     "measured-experiment.sexp", "verification.json"):
            limits[case_id + "/" + name] = INPUT_BYTES
    return limits


def check_retention_layout(root):
    """Census known quiescent paths only; do not descend into unknown directories."""
    limits = retention_limits()
    directory = root / "evidence"
    device = root.stat().st_dev
    for folder in (directory, *(directory / case_id for case_id in CASES)):
        info = folder.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_dev != device:
            raise ValueError("retention directory type/volume differs")
    declared = {"README.md", *CASES}
    names = set()
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.name not in declared:
                raise ValueError("undeclared retained family member")
            names.add(entry.name)
    if names != declared:
        raise ValueError("incomplete retained family layout")
    members = [directory / "README.md"]
    for case_id in CASES:
        with os.scandir(directory / case_id) as entries:
            for entry in entries:
                if case_id + "/" + entry.name not in limits:
                    raise ValueError("undeclared retained case member")
                members.append(directory / case_id / entry.name)
    total = 0
    for path in members:
        info = path.lstat()
        relative = path.relative_to(directory).as_posix()
        if (not stat.S_ISREG(info.st_mode) or info.st_dev != device
                or not 0 <= info.st_size <= limits[relative]):
            raise ValueError("retained member type/volume/role bound differs")
        total += info.st_size
    if len(members) > FAMILY_FILES or total > FAMILY_BYTES:
        raise ValueError("retention family exceeds its declared envelope")
    return tuple(path.relative_to(directory).as_posix() for path in members), total


class CaseInputTests(unittest.TestCase):
    """One reviewed case's four prepared inputs; subclassed once per case."""

    CASE_ID = None

    @classmethod
    def setUpClass(cls):
        if cls.CASE_ID is None:
            raise unittest.SkipTest("abstract per-case test class")

    def setUp(self):
        self.case = P.reviewed_case(self.CASE_ID)
        self.payloads = prepared_bytes(ROOT, self.CASE_ID)
        self.source = bounded_bytes(ROOT / GUESTS / self.case.program)
        self.baseline = self.payloads["baseline.expected.sexp"]
        self.control = self.payloads["control.expected.sexp"]
        self.step = self.case.control().witness.step_n
        self.register = self.case.control().witness.register
        base = ROOT / "target/prepared-div-input-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)

    def source_finding(self, expectation):
        return C.compare_source_expectation(
            source=self.source, baseline_expectation=expectation,
            instructions=self.case.instructions, program=self.case.program,
            witness=self.case.control().witness)

    def fixture_record(self, name, payload, *, repin=False):
        path = self.temporary / name
        path.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest() if repin else None
        return input_record(self.CASE_ID, name, path.relative_to(ROOT).as_posix(), digest)

    def test_actual_four_pins_and_sizes(self):
        self.assertEqual(len(self.payloads), 4)
        self.assertEqual(sum(map(len, self.payloads.values())), TOTALS[self.CASE_ID])
        for name, (_, size, digest) in PREPARED[self.CASE_ID].items():
            self.assertEqual(len(self.payloads[name]), size)
            self.assertEqual(hashlib.sha256(self.payloads[name]).hexdigest(), digest)

    def test_pins_equal_the_capture_commands_table(self):
        rows = Command.prepared_inputs(self.CASE_ID)
        self.assertEqual(len(rows), 5)
        for role, _, path, size, digest in rows[:4]:
            name = path.rsplit("/", 1)[1]
            self.assertEqual(path, prefix(self.CASE_ID) + "/" + name)
            self.assertEqual((role, size, digest), PREPARED[self.CASE_ID][name])
        self.assertEqual(rows[4], Command.IDENTITY_ROW)  # the profile's identity, shared by every case
        with self.assertRaises(Command.AuthorityError):
            Command.prepared_inputs("rv64gc-unpinned")

    def test_baseline_is_the_complete_canonical_copy(self):
        canonical = GUESTS + "/" + Path(self.case.program).stem + ".expected.sexp"
        self.assertEqual(self.baseline, bounded_bytes(ROOT / canonical))
        document = mapped(self.baseline, "expectations", D.expectations_to_doc)
        instructions, fetches = BUDGETS[self.CASE_ID]
        self.assertEqual((document["program"], document["instructions"], document["fetches"]),
                         (self.case.program, instructions, fetches))
        self.assertEqual([step["n"] for step in document["step"]], list(range(instructions)))

    def test_complete_image_matches_public_reconstruction(self):
        image = self.payloads["guest.elf"]
        built = G.build_guest_image(self.source, program=self.case.program, entry=0x80000000)
        self.assertEqual(image, built.image)
        result = B.check_source_image(self.source, image, program=self.case.program, entry=0x80000000)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(result.facts.image_sha256, PREPARED[self.CASE_ID]["guest.elf"][2])

    def test_all_source_values_and_the_control_value_match(self):
        result = self.source_finding(self.baseline)
        self.assertEqual(result.disposition, "matched", result.reason)
        self.assertEqual(len(result.facts.derivation.steps), self.case.instructions)
        self.assertEqual(result.facts.witness_value, self.case.control().expected_value)
        for item in self.case.properties:
            writes = dict(result.facts.derivation.steps[item.witness.step_n].writes)
            self.assertEqual(writes.get(int(item.witness.register[1:])), item.expected_value, item.property_id)

    def test_control_is_exactly_one_typed_wrong_value(self):
        base = mapped(self.baseline, "expectations", D.expectations_to_doc)
        changed = mapped(self.control, "expectations", D.expectations_to_doc)
        self.assertEqual(changed["step"][self.step]["writes"][self.register], f"0x{self.case.control_value:016x}")
        restored = deepcopy(changed)
        restored["step"][self.step]["writes"][self.register] = base["step"][self.step]["writes"][self.register]
        self.assertEqual(restored, base)
        expected = R.render_forms([[S.Symbol("comment"), Prep.control_note(self.case)],
                                   D.expectations_to_form(changed)]).encode("utf-8")
        self.assertEqual(expected, self.control)
        result = self.source_finding(self.control)
        self.assertEqual(result.disposition, "failed")
        self.assertEqual(result.difference.step_n, self.step)
        self.assertEqual(result.difference.observed, ((self.register, self.case.control().expected_value),))
        self.assertEqual(result.difference.expected, ((self.register, self.case.control_value),))

    def test_config_is_exact_public_materialization(self):
        canonical = mapped(bounded_bytes(ROOT / OVERRIDE), "override", D.override_to_doc)
        if self.CASE_ID in OWN_CONFIGURATION:  # the overlay's own controls are scripts/probe_reference_overlay.py
            overlay = mapped(bounded_bytes(ROOT / Prep.overlay_path(self.CASE_ID)), "overlay", Prep.overlay_to_doc)
            canonical = Prep.apply_overlay(canonical, overlay)
        payload = self.payloads["reference-config.json"]
        self.assertEqual(payload, (json.dumps(canonical, indent=2) + "\n").encode("utf-8"))
        self.assertEqual(json.loads(payload), canonical)
        changed = deepcopy(canonical)
        changed["base"]["writable_misa"] = True
        self.assertNotEqual(changed, json.loads(payload))

    def test_curation_tool_reproduces_the_retained_bytes(self):
        items = Prep.curate(ROOT, self.case)
        self.assertEqual([item.name for item in items], list(PREPARED[self.CASE_ID]))
        for item in items:
            self.assertEqual(item.payload, self.payloads[item.name], item.name)
            self.assertEqual((item.role, item.byte_size, item.sha256), PREPARED[self.CASE_ID][item.name])
        self.assertEqual([row["retained"] for row in Prep.verify(ROOT, self.case)], ["equal"] * 4)

    def test_changed_artifacts_are_not_accepted_under_the_original_pins(self):
        for name, payload in self.payloads.items():
            with self.subTest(name=name):
                record = self.fixture_record(name, payload + b"\n")
                result = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
                self.assertEqual(result.pin.disposition, "mismatch")

    def test_missing_artifacts_are_unavailable(self):
        for name in PREPARED[self.CASE_ID]:
            record = input_record(self.CASE_ID, name, (self.temporary / name).relative_to(ROOT).as_posix())
            self.assertEqual(A.read_snapshot(ROOT, "input", record,
                                            max_bytes=INPUT_BYTES).pin.disposition, "unavailable")

    def test_repinning_a_changed_image_does_not_restore_correspondence(self):
        payload = self.payloads["guest.elf"]
        for changed in (bytes([payload[0] ^ 1]) + payload[1:], payload[:-1] + bytes([payload[-1] ^ 1])):
            record = self.fixture_record("guest.elf", changed, repin=True)
            snapshot = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
            self.assertEqual(snapshot.pin.disposition, "matched")
            result = B.check_source_image(self.source, snapshot.data, program=self.case.program,
                                          entry=0x80000000)
            self.assertEqual(result.disposition, "refused")

    def test_additional_control_change_is_detected_by_the_source_author(self):
        changed = mapped(self.control, "expectations", D.expectations_to_doc)
        changed["step"][1]["writes"]["x6"] = "0x0000000000000003"
        result = self.source_finding(R.render_forms([D.expectations_to_form(changed)]).encode())
        self.assertEqual(result.disposition, "failed")
        self.assertEqual(result.difference.step_n, 1)

    def test_matching_pin_cannot_exceed_the_prepared_input_bound(self):
        record = self.fixture_record("guest.elf", b"x" * (INPUT_BYTES + 1), repin=True)
        result = A.read_snapshot(ROOT, "input", record, max_bytes=INPUT_BYTES)
        self.assertEqual(result.pin.disposition, "refused")

    def test_supplied_byte_findings_launch_no_process_or_artifact_read(self):
        with patch.object(subprocess, "Popen", side_effect=AssertionError("process launched")), \
                patch.object(A, "read_snapshot", side_effect=AssertionError("artifact read")):
            self.assertEqual(self.source_finding(self.baseline).disposition, "matched")
            result = B.check_source_image(self.source, self.payloads["guest.elf"],
                                          program=self.case.program, entry=0x80000000)
            self.assertEqual(result.disposition, "matched")

    def test_package_copy_needs_no_binary_or_materials(self):
        for case_id in CASES:
            for name in PREPARED[case_id]:
                path = self.temporary / prefix(case_id) / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(bounded_bytes(ROOT / prefix(case_id) / name))
        (self.temporary / "evidence/README.md").write_bytes(bounded_bytes(ROOT / "evidence/README.md"))
        self.assertFalse((self.temporary / "target/refs").exists())
        self.assertFalse((self.temporary / ".materials").exists())
        self.assertEqual(prepared_bytes(self.temporary, self.CASE_ID), self.payloads)


class RetainedCaseInputTests(CaseInputTests):
    CASE_ID = P.CASE_ID


class MFormsCaseInputTests(CaseInputTests):
    CASE_ID = P.M_FORMS_CASE_ID


class CsrSetCaseInputTests(CaseInputTests):
    """The first case with its own reference configuration: the pins hold through the overlay."""
    CASE_ID = CSR_SET


class ZicntrCaseInputTests(CaseInputTests):
    """The ZICNTR case: its own overlay, and the same rendered configuration as CSR-SET's."""
    CASE_ID = ZICNTR


class SstcCaseInputTests(CaseInputTests):
    """The SSTC case: its own overlay, CSR-SET's rendered configuration, and boundaries that fetch nothing."""
    CASE_ID = SSTC


class FamilyTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/prepared-div-input-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)

    def test_raw_schema_precedes_mapping(self):
        with patch.object(D, "expectations_to_doc", side_effect=AssertionError("mapper reached")):
            with self.assertRaises(ValueError):
                mapped(b"(expectations (unknown true))", "expectations", D.expectations_to_doc)

    def test_index_and_declared_retention_envelopes_fit(self):
        index = bounded_bytes(ROOT / "evidence/README.md")
        self.assertLessEqual(len(index), 4096)
        self.assertLessEqual(len(index.splitlines()), 80)
        self.assertEqual((Collector.TRACE_BYTES, Collector.STREAM_BYTES, F.DOCUMENT_BYTES),
                         (4 * 1024 * 1024, INPUT_BYTES, INPUT_BYTES))
        limits = retention_limits()
        # The envelope is the ceiling, set once for every batch (a46-2): the declared cases must fit it, and each case is still exactly its slots.
        self.assertEqual(len(limits), 1 + 22 * len(CASES))
        self.assertLessEqual(len(limits), FAMILY_FILES)
        self.assertEqual(sum(limits.values()), 4096 + 13828096 * len(CASES))
        self.assertLess(sum(limits.values()), FAMILY_BYTES)
        self.assertLessEqual(max(Collector.TRACE_BYTES, Collector.STREAM_BYTES,
                                 F.DOCUMENT_BYTES, INPUT_BYTES), 4 * 1024 * 1024)
        members, total = check_retention_layout(ROOT)
        self.assertEqual(len(members), 1 + 44 * 22)  # the 38 current, the two the tools name, and the four since their captures (a51-9)
        self.assertEqual(set(P.reviewed_case_ids()), set(CASES))

    def test_every_retired_case_reads_back_from_history(self):
        """The page lists what left the tree and history holds it (decision_superseded-cases-retired.md); a copy without that history cannot judge it."""
        def git(*args):
            return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if shallow != "false":
            self.skipTest("no full history to read back from")
        page = (ROOT / "docs/models/rv64gc-lab-v0/src/retired-cases.md").read_text()
        cases = re.findall(r"^\| `(rv64gc-[a-z0-9-]+)` \| `REQ-[A-Z0-9-]+` \| `(rv64gc-[a-z0-9-]+)` \| ([0-9,]+) \| `([0-9a-f]{8})` \| `([0-9a-f]{40})` \| `([0-9a-f]{64})` \|$", page, re.M)
        self.assertEqual(len(cases), 25)
        for case, holder, size, commit, tree, measured in cases:
            with self.subTest(case=case):
                self.assertFalse((ROOT / "evidence" / case).exists())
                self.assertTrue((ROOT / "evidence" / holder / "case.sexp").is_file())
                self.assertEqual(git("rev-parse", f"{commit}:evidence/{case}").decode().strip(), tree)
                listing = git("ls-tree", "-r", "-l", tree).decode().splitlines()
                self.assertEqual((len(listing), sum(int(line.split()[3]) for line in listing)), (22, int(size.replace(",", ""))))
                self.assertEqual(hashlib.sha256(git("show", f"{commit}:evidence/{case}/measured-experiment.sexp")).hexdigest(), measured)
        files = re.findall(r"^\| `(profiles/[^`]+)` \| ([0-9,]+) \| `([0-9a-f]{8})` \| `([0-9a-f]{64})` \|$", page, re.M)
        self.assertEqual(len(files), 16)
        for path, size, commit, digest in files:
            with self.subTest(path=path):
                self.assertFalse((ROOT / path).exists())
                data = git("show", f"{commit}:{path}")
                self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (int(size.replace(",", "")), digest))

    def test_undeclared_linked_and_oversized_members_refuse(self):
        for change in ("sibling", "unknown", "stream", "metadata", "link", "missing-case"):
            with self.subTest(change=change), TemporaryDirectory(dir=self.temporary) as directory:
                root = Path(directory)
                (root / "evidence").mkdir()
                (root / "evidence/README.md").write_text("bounded fixture index\n")
                for case_id in CASES:
                    folder = root / "evidence" / case_id
                    folder.mkdir()
                    for name in PREPARED[case_id]:
                        (folder / name).write_bytes(bounded_bytes(ROOT / prefix(case_id) / name))
                folder = root / "evidence" / CASES[0]
                if change == "sibling":
                    (root / "evidence/undeclared-case").mkdir()
                elif change == "unknown":
                    (folder / "unknown").mkdir()
                elif change == "stream":
                    (folder / "baseline.stdout").write_bytes(b"x" * (Collector.STREAM_BYTES + 1))
                elif change == "metadata":
                    (folder / "authorities.sexp").write_bytes(b"x" * (INPUT_BYTES + 1))
                elif change == "link":
                    (folder / "baseline.trace").symlink_to("missing")
                else:
                    for name in PREPARED[CASES[1]]:
                        (root / "evidence" / CASES[1] / name).unlink()
                    (root / "evidence" / CASES[1]).rmdir()
                with self.assertRaises((ValueError, FileNotFoundError)):
                    prepared_bytes(root, CASES[0])

    def test_write_is_exclusive_and_refuses_an_existing_file(self):
        case = P.reviewed_case(P.M_FORMS_CASE_ID)
        items = Prep.curate(ROOT, case)
        root = self.temporary / "fresh"
        root.mkdir()
        with patch.object(Prep, "curate", return_value=items):
            rows = Prep.write(root, case)
            self.assertEqual([row["name"] for row in rows], list(PREPARED[case.case_id]))
            for item in items:
                self.assertEqual((root / "evidence" / case.case_id / item.name).read_bytes(), item.payload)
            with self.assertRaises(Prep.CurationRefused):
                Prep.write(root, case)
            partial = self.temporary / "partial"
            (partial / "evidence" / case.case_id).mkdir(parents=True)
            (partial / "evidence" / case.case_id / "control.expected.sexp").write_bytes(b"older")
            with self.assertRaises(Prep.CurationRefused):
                Prep.write(partial, case)
            self.assertEqual(sorted(p.name for p in (partial / "evidence" / case.case_id).iterdir()),
                             ["control.expected.sexp"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=["actual-layout"])
    args = parser.parse_args()
    classes = (RetainedCaseInputTests, MFormsCaseInputTests, CsrSetCaseInputTests, ZicntrCaseInputTests, SstcCaseInputTests, FamilyTests)
    if args.mutation:
        before = "    check_retention_layout(root)\n    result = {}\n"
        source = Path(__file__).read_text()
        if source.count(before) != 1:
            raise RuntimeError("prepared-input layout mutation seam count changed")
        module = types.ModuleType("mutated_prepared_div_inputs")
        module.__file__ = __file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, "    result = {}\n", 1), __file__, "exec"),
             module.__dict__)
        classes = (module.RetainedCaseInputTests, module.MFormsCaseInputTests, module.CsrSetCaseInputTests, module.ZicntrCaseInputTests, module.SstcCaseInputTests, module.FamilyTests)
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls) for cls in classes)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"DIV-CAPTURE-INPUTS: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; prepared artifacts of every reviewed case, no reference process or capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
