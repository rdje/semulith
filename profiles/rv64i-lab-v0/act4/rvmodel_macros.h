/* rvmodel_macros.h — the rv64i-lab-v0 DUT macros for the ACT4 campaign
 * (P2-SCALAR.5 strand 2).
 *
 * The macro NAMES are the suite's interface (tests/env/check_defines.h @ the
 * pinned e2216915 refuses the build without them); the definitions are this
 * laboratory's own. Two measured facts shape the file:
 *
 *   1. SIGNATURE-mode builds (the only mode this campaign runs) forcibly
 *      include tests/env/sail_macros.h AFTER this header, which #undefs and
 *      redefines RVMODEL_DATA_SECTION, RVMODEL_HALT_PASS/FAIL,
 *      RVMODEL_IO_WRITE_STR, RVMODEL_INTERRUPT_LATENCY,
 *      RVMODEL_TIMER_INT_SOON_DELAY and the SET/CLR interrupt macros to their
 *      HTIF/Sail forms. The definitions below therefore stand for honesty and
 *      for any future non-signature build — in the campaign's own ELFs the
 *      sail_macros.h forms are the ones emitted.
 *   2. The laboratory declares NO devices and NO interrupt sources
 *      (D-PLATFORM). The interrupt macros exist only because check_defines.h
 *      requires the names; no I-suite test executes them (measured: the
 *      interrupt machinery compiles out without STANDARD_SM_SUPPORTED). Their
 *      target address is 0x80000000 by the suite's own convention — a store
 *      there would corrupt the test image, so any execution is a loud,
 *      detectable failure rather than a silent one.
 *
 * The termination/console convention is HTIF: a 32-bit store of 1 (pass) or 3
 * (fail) to `tohost`, and console bytes as store pairs (low word the byte,
 * high word device 1 / command 1). The campaign harness watches the store
 * trace for exactly these crossings; it never reads target memory.
 *
 * SPDX-License-Identifier: MIT OR Apache-2.0
 */

#ifndef _RVMODEL_MACROS_H
#define _RVMODEL_MACROS_H

/* The tohost/fromhost doublewords, placed by RVMODEL_DATA_SECTION at the end of
 * the signature region. */
#define RVMODEL_DATA_SECTION \
        .pushsection .tohost,"aw",@progbits;                 \
        .balign 8; .global tohost; tohost: .dword 0;         \
        .balign 8; .global fromhost; fromhost: .dword 0;     \
        .popsection

/* No boot work: the laboratory's reset state IS the declared entry state
 * (D-ENTRY-STATE), and with no Zicsr there is no CSR initialization to do.
 * RVMODEL_BOOT_TO_MMODE defined blank bypasses the suite's default CSR setup,
 * exactly as the suite intends for targets without machine-mode CSRs. */
#define RVMODEL_BOOT
#define RVMODEL_BOOT_TO_MMODE

/* Termination: HTIF. 1 = pass, 3 = fail; the store loop repeats the verdict
 * until the harness's step budget stops the run. */
#define RVMODEL_HALT_PASS  \
  li x1, 1                ;\
  la t0, tohost           ;\
  write_tohost_pass:      ;\
    sw x1, 0(t0)          ;\
    sw x0, 4(t0)          ;\
    j write_tohost_pass   ;\

#define RVMODEL_HALT_FAIL  \
  li x1, 3                ;\
  la t0, tohost           ;\
  write_tohost_fail:      ;\
    sw x1, 0(t0)          ;\
    sw x0, 4(t0)          ;\
    j write_tohost_fail   ;\

/* Console: one HTIF store pair per byte (low word the byte, high word
 * device 1 / command 1). */
#define RVMODEL_IO_INIT(_R1, _R2, _R3)
#define RVMODEL_IO_WRITE_STR(_R1, _R2, _R3, _STR_PTR) \
1:                          ;\
  lbu _R1, 0(_STR_PTR)      ;\
  beqz _R1, 3f              ;\
  la _R2, tohost            ;\
  sw _R1, 0(_R2)            ;\
  li _R1, 0x01010000        ;\
  sw _R1, 4(_R2)            ;\
  addi _STR_PTR, _STR_PTR, 1;\
  j 1b                      ;\
3:

/* Required names only — see fact (2) above. Never executed by the I suite. */
#define RVMODEL_INTERRUPT_LATENCY 10
#define RVMODEL_TIMER_INT_SOON_DELAY 5000
#define RVMODEL_SET_MEXT_INT(_R1, _R2) \
  li _R1, 1                           ;\
  li _R2, 0x80000000                  ;\
  sw _R1, 0(_R2)                      ;
#define RVMODEL_CLR_MEXT_INT(_R1, _R2) \
  li _R2, 0x80000000                  ;\
  sw zero, 0(_R2)                     ;
#define RVMODEL_SET_MSW_INT(_R1, _R2)  \
  li _R1, 1                           ;\
  li _R2, 0x80000000                  ;\
  sw _R1, 0(_R2)                      ;
#define RVMODEL_CLR_MSW_INT(_R1, _R2)  \
  li _R2, 0x80000000                  ;\
  sw zero, 0(_R2)                     ;

#endif /* _RVMODEL_MACROS_H */
