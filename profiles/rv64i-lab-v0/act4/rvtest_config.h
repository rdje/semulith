/* rvtest_config.h — the rv64i-lab-v0 DUT configuration for the ACT4 campaign
 * (P2-SCALAR.5 strand 2).
 *
 * The upstream framework generates this file from a UDB YAML description of the
 * DUT. This laboratory writes the minimal honest set by hand: exactly what the
 * pinned env headers (tests/env @ e2216915) read in VALUE contexts, and nothing
 * else. Every macro left UNDEFINED here is a measured absence, not an oversight:
 *
 *   - STANDARD_SM_SUPPORTED / S_SUPPORTED / U_SUPPORTED / F_SUPPORTED / …
 *     stay undefined: the trap handlers, the T-SBI machinery and every CSR path
 *     compile out (measured by grep over the pinned headers; the I-suite bodies
 *     carry no CSR or fence.i instruction outside compiled-out guards — the
 *     laboratory profile declares M-mode only and no Zicsr).
 *   - UDB_NUM_PMP_ENTRIES stays undefined: `#if UDB_NUM_PMP_ENTRIES > 0`
 *     evaluates false (check_defines.h) — the profile has no PMP.
 *   - ZICNTR_SUPPORTED stays undefined: no time CSR to emulate
 *     (derived_config.h) — the profile declares no counter at all.
 *
 * SPDX-License-Identifier: MIT OR Apache-2.0
 */

#ifndef RVTEST_CONFIG_H
#define RVTEST_CONFIG_H

#define UDB_MXLEN 64

#endif /* RVTEST_CONFIG_H */
