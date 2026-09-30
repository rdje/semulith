/* link.ld — the rv64i-lab-v0 link map for the ACT4 campaign (P2-SCALAR.5
 * strand 2). The section LAYOUT is the suite's contract (tests/env expects
 * .text.init first, the stack symbols, and .text.rvmodel last so the
 * variable-size model code cannot shift the data/signature addresses); the
 * VALUES are this laboratory's declared memory map: one MainMemory region,
 * base 0x80000000, size 2 GiB — identical to the matched sail override
 * (reference/sail-rv64i-lab-v0.override.sexp), so the same ELF runs on all
 * three models.
 *
 * SPDX-License-Identifier: MIT OR Apache-2.0
 */

RAM_ORIGIN = 0x80000000;
RAM_LENGTH = 0x80000000;
TEST_BASE  = RAM_ORIGIN;
NUM_HARTS  = 1;
STACK_SIZE = 0x20000;

OUTPUT_ARCH( "riscv" )
ENTRY(rvtest_entry_point)

MEMORY
{
  ram (rwx) : ORIGIN = RAM_ORIGIN, LENGTH = RAM_LENGTH
}

PROVIDE(__stack_size = STACK_SIZE);
PROVIDE(__num_harts = NUM_HARTS);

SECTIONS
{
  ASSERT(TEST_BASE >= ORIGIN(ram) && TEST_BASE < ORIGIN(ram) + LENGTH(ram),
         "TEST_BASE is outside the laboratory's MainMemory region")

  .text.init   TEST_BASE : { *(.text.init) } > ram
  .text.rvtest . : { *(.text.rvtest) *(.text.rvtest.*) } > ram

  . = ALIGN(0x4000);
  .rodata . : { *(.rodata) *(.rodata.*) *(.srodata) *(.srodata.*) } > ram
  .data   . : { *(.data) *(.data.*) *(.sdata) *(.sdata.*) } > ram

  . = ALIGN(16);
  .bss . : {
    __bss_start = .;
    *(.sbss) *(.sbss.*) *(.bss) *(.bss.*) *(COMMON)
    . = ALIGN(16);
    __bss_end = .;
  } > ram

  . = ALIGN(16);
  __stack_bottom = .;
  . += __stack_size * __num_harts;
  __stack_top = .;

  . = ALIGN(0x1000);
  .text.rvmodel . : { *(.text.rvmodel) *(.text.rvmodel.*) *(.text) *(.text.*) } > ram

  . = ALIGN(0x1000);
  _end = .;

  ASSERT(_end <= ORIGIN(ram) + LENGTH(ram),
         "ACT ELF exceeds the laboratory's MainMemory region")
}
