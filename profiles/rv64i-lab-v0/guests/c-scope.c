// c-scope.c — the first COMPILED freestanding guest of rv64i-lab-v0
// (P2-SCALAR.5, strand 1; G1 criterion 6; decision_c-guest-routing-and-toolchain).
//
// Compiled by the pinned toolchain (scripts/build_c_guest.sh: clang 21.1.8
// -march=rv64i -mabi=lp64 — the backend may emit only RV64I — linked by ld.lld
// 21.1.8) and retired under first-divergence comparison against sail-riscv AND
// spike by scripts/run_semulith_smoke.py.
//
// The guest is SELF-CHECKING: every expected value below is a constant derived
// from the C abstract machine and the RV64I rules the source lowers to — never
// from any model's output. A failed check routes to fail(code): any runner that
// mis-executes diverges from the other two at exactly that check, which is what
// makes three-way agreement on the success path the evidence.
//
// Scope deliberately toured: 64-bit ALU with wrap, 32-bit (*W) arithmetic, every
// load/store width with little-endian composition, branches and a counted loop,
// real function calls (argument registers, stack spills), and variable shifts
// through the full 6-bit register-shamt range (a 32-bit shift by >= 32 is UB in C,
// so the *W shamt boundary stays with bound-shiftw's assembly — see the comment
// at section 6). ⚠️ What the COMPILER does with this tour is the measured fact,
// not the source's intention: at -O1 clang constant-folds fib/sum6/pick, so the
// ELF contains no switch jump table and fewer calls than the source tours
// (measured by disassembly, P2-SCALAR.5 strand 3 — the evidence covers what the
// ELF contains). The jump-table idiom this guest was meant to exercise is pinned
// for real by dir-chase's measured load→jalr sequence. There is NO
// multiplication or division anywhere — M is not in this profile, and -nostdlib
// means a libgcc helper call would link-fail rather than slip one in.

typedef unsigned long u64;
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;

// emit materializes v in a register as its own observable step (the observation
// vocabulary is register writes; a result left only in memory would prove
// nothing — the P2-SCALAR.1 lesson).
static __attribute__((noinline)) void emit(u64 v) { __asm__ volatile("" : "+r"(v)); }

static __attribute__((noreturn)) void halt(u64 code) {
  emit(code);
  __asm__ volatile("ebreak");
  __builtin_unreachable();
}

static __attribute__((noinline, noreturn)) void fail(u64 code) {
  halt((u64)0xFA11 << 48 | code);
}

#define CHECK(cond, code)  \
  do {                     \
    if (!(cond))           \
      fail(code);          \
  } while (0)

static u64 buf[8]; // .bss: zero on every runner by the ELF contract

static __attribute__((noinline)) u64 fib(u64 n) {
  u64 a = 0, b = 1;
  for (u64 i = 0; i < n; i++) {
    u64 t = a + b;
    a = b;
    b = t;
  }
  return a;
}

// Six integer arguments force the calling convention's argument registers; the
// additions keep the body on the ALU alone.
static __attribute__((noinline)) u64 sum6(u64 a, u64 b, u64 c, u64 d, u64 e,
                                          u64 f) {
  return a + b + c + d + e + f;
}

static u64 pick(u64 which) {
  switch (which & 3) {
  case 0:
    return 10;
  case 1:
    return 100;
  case 2:
    return 1000;
  default:
    return 10000;
  }
}

void c_main(void) {
  // 1. 64-bit ALU, both wrap directions (D-ALU-REG/D-ALU-IMM: overflow is
  // ignored, the result wraps modulo 2^64).
  u64 max = 0x7FFFFFFFFFFFFFFFUL;
  u64 min = max + 1;
  CHECK(min == 0x8000000000000000UL, 0x0101);
  CHECK(min - 1 == max, 0x0102);
  CHECK(max + max == 0xFFFFFFFFFFFFFFFEUL, 0x0103);

  // 2. 32-bit arithmetic: the *W forms — low-32 compute, sign-extended retire.
  u32 w = 0x7FFFFFFFU + 1U;
  CHECK(w == 0x80000000U, 0x0201);
  CHECK((u64)(u32)(0U - 1U) == 0xFFFFFFFFUL, 0x0202);
  {
    int neg = (int)w; // bit 31 set: negative when read signed
    CHECK(neg < 0, 0x0203);
  }

  // 3. Every load/store width, little-endian composition (bound-alias's lanes,
  // through compiled code this time).
  u8 *p = (u8 *)buf;
  for (u64 i = 0; i < 8; i++)
    p[i] = (u8)(0x41 + i); // "ABCDEFGH" in memory order
  CHECK(p[0] == 0x41 && p[7] == 0x48, 0x0301);
  CHECK(*(u16 *)(p + 0) == 0x4241, 0x0302);         // lh/lhu lane composition
  CHECK(*(u32 *)(p + 0) == 0x44434241U, 0x0303);    // lw/lwu
  CHECK(buf[0] == 0x4847464544434241UL, 0x0304);    // ld
  *(u16 *)(p + 8) = 0x5A59;                         // sh into the next dword
  CHECK(p[8] == 0x59 && p[9] == 0x5A, 0x0305);
  *(u32 *)(p + 12) = 0x01020304U;                   // sw crossing the lane
  CHECK(p[12] == 0x04 && p[15] == 0x01, 0x0306);
  buf[2] = 0x1122334455667788UL;                    // sd
  CHECK(p[16] == 0x88 && p[23] == 0x11, 0x0307);

  // 4. Branches and a counted loop: sum 1..64.
  u64 sum = 0;
  for (u64 i = 1; i <= 64; i++)
    sum += i;
  CHECK(sum == 2080, 0x0401);

  // 5. Real calls: argument registers, a stack frame, and an indirect jump.
  CHECK(fib(20) == 6765, 0x0501);
  CHECK(sum6(1, 2, 4, 8, 16, 32) == 63, 0x0502);
  CHECK(pick(1) + pick(2) + pick(3) + pick(4) == 11110, 0x0503);

  // 6. Variable shifts: the 6-bit register-shamt range on u64 (RV64 reads 6
  // bits), and a full-width *W shift on u32. NB: a 32-bit shift by >= 32 is UB
  // IN C — the ISA's 5-bit *W shamt boundary is NOT expressible through the C
  // abstract machine (it is pinned in assembly by bound-shiftw instead; the
  // first draft of this guest tried, and clang exploited the UB to delete the
  // entire rest of the program — caught by the self-check as fail 0x0501).
  u64 one = 1;
  u64 by = 63;
  CHECK(one << by == 0x8000000000000000UL, 0x0601);
  CHECK((one << 33) == 0x200000000UL, 0x0602);
  {
    u32 w32 = 1;
    u32 amt = 31; // the widest *W-left-shift C allows
    CHECK((w32 << amt) == 0x80000000U, 0x0603);
    int neg = -16;
    CHECK((neg >> 2) == -4, 0x0604); // arithmetic right shift, sign fills
  }

  // Success: the signature retires into registers as the closing visible steps.
  emit(0xC0FFEE0000000001UL);
  emit(sum);
  emit(fib(20));
  emit(buf[0]);
  halt(0x600DC0DE600DC0DEUL);
}

// The entry point: naked, so no stack is touched before sp is valid. The
// laboratory's MainMemory is [0x80000000, +0x80000000) on every runner; the
// stack starts 1 MiB above the image base, far above this program's image.
__attribute__((naked, used)) void _start(void) {
  __asm__ volatile("li sp, 0x80100000\n"
                   "j c_main\n");
}
