/* wl-link.ld — the workload linker script (P4-SYSTEM.15 slice f). The ACT4 DUT's link.ld places the
 * framework's text before its data and reserves the stack by a location-counter bump that ld.lld does
 * not honour for the output section that follows; a compiled workload's code and stack must not share
 * bytes, so this script lays out: entry shim, code, rodata, data (the signature region), the HTIF
 * mailbox on its own 64-byte line, bss, then a fixed stack top at 1 MiB — all inside the laboratory's
 * MainMemory region [0x80000000, 0x80000000 + 2 GiB). */
RAM_ORIGIN = 0x80000000;
RAM_LENGTH = 0x80000000;
OUTPUT_ARCH( "riscv" )
ENTRY(rvtest_entry_point)
MEMORY { ram (rwx) : ORIGIN = RAM_ORIGIN, LENGTH = RAM_LENGTH }
SECTIONS
{
  .text.init RAM_ORIGIN : { *(.text.init) } > ram
  .text . : { *(.text) *(.text.*) } > ram
  .rodata ALIGN(16) : { *(.rodata) *(.rodata.*) *(.srodata) *(.srodata.*) } > ram
  .data ALIGN(16) : { *(.data) *(.data.*) *(.sdata) *(.sdata.*) } > ram
  .tohost ALIGN(64) : { *(.tohost) } > ram
  .bss ALIGN(16) : { __bss_start = .; *(.bss) *(.bss.*) *(.sbss) *(.sbss.*) *(COMMON) . = ALIGN(16); __bss_end = .; } > ram
  _end = .;
  __stack_top = RAM_ORIGIN + 0x100000;
  ASSERT(_end <= __stack_top - 0x10000, "the workload's image reaches into its own stack")
}
