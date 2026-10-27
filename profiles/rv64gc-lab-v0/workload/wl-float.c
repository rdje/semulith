// wl-float.c — the F and D workload with exactly representable operands (dyadic rationals), so every
// IEEE result is exact and derived in gen_workloads.py through binary64/binary32 arithmetic: add, mul, div,
// sqrt, fused multiply-add (exact here, so fma == separate ops — its presence is the census's fact),
// comparisons, conversions both ways, classification through the bit pattern, moves between files.
#include "wl-common.h"
static __attribute__((noinline)) double fma_d(double a, double b, double c) { double r; __asm__("fmadd.d %0, %1, %2, %3" : "=f"(r) : "f"(a), "f"(b), "f"(c)); return r; }  // -fno-builtin would call libm's fma; the instruction is the point
static __attribute__((noinline)) double sqrt_d(double x) { double r; __asm__("fsqrt.d %0, %1" : "=f"(r) : "f"(x)); return r; }
static __attribute__((noinline)) float mul_f(float a, float b) { return a * b; }
static __attribute__((noinline)) u64 bits_d(double x) { u64 r; __builtin_memcpy(&r, &x, 8); return r; }
static __attribute__((noinline)) u64 bits_f(float x) { u32 r; __builtin_memcpy(&r, &x, 4); return r; }
static __attribute__((noinline)) u64 fclass_d(double x) { u64 r; __asm__("fclass.d %0, %1" : "=r"(r) : "f"(x)); return r; }
int main(void) {
    int slot = 0, bad = 0;
    double a = opaque_d(1.5), b = opaque_d(-2.25), c = opaque_d(0.125);
    EMIT(bits_d(fma_d(a, b, c)), 0xc00a000000000000ul);        // 1.5 * -2.25 + 0.125 = -3.25
    EMIT(bits_d(sqrt_d(opaque_d(6.25))), 0x4004000000000000ul);  // sqrt 6.25 = 2.5
    EMIT(bits_d(opaque_d(7.0) / opaque_d(8.0)), 0x3fec000000000000ul);  // 0.875
    EMIT(bits_f(mul_f(opaque_f(3.5f), opaque_f(0.75f))), 0x40280000u);  // 3.5 * 0.75 = 2.625
    EMIT(a < b, 0); EMIT(b < a, 1); EMIT(a == opaque_d(1.5), 1);  // flt.d / feq.d
    EMIT((u64)(i64)opaque_d(-7.75), (u64)(i64)(-7));         // fcvt.l.d truncates toward zero
    EMIT(bits_d((double)(i64)opaque((u64)-13)), 0xc02a000000000000ul);  // fcvt.d.l
    EMIT(fclass_d(opaque_d(-1.0) / opaque_d(0.0)), 1);  // -inf: fclass bit 0
    EMIT(bits_d((double)opaque_f(3.5f)), 0x400c000000000000ul);  // fcvt.d.s
    return bad;
}
