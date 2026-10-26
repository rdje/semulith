/* rvtest_config.h — the rv64gc-lab-v0 DUT configuration for the ACT4 campaign
 * (P4-SYSTEM.15 slice a, after P2-SCALAR.5 strand 2 for rv64i).
 *
 * The same minimal set as rv64i's, on purpose: the pinned RV64I suite (tests/rv64i/I) is
 * what runs here, from reset in M-mode, and its bodies carry no CSR, fence.i or
 * floating-point instruction outside compiled-out guards. The GC profile's S/U modes,
 * Zicsr, Zicntr, F/D and C are not exercised by this suite and are therefore not
 * declared to its framework — an undeclared feature compiles its machinery out; it
 * does not claim its absence from the model. The M/A/F/D/C suites are their own
 * acquisition and their own DUT configuration (a later slice).
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
