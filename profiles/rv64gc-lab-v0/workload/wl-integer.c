// wl-integer.c — the M workload: 64- and 32-bit multiply, divide and remainder, signed and unsigned,
// through loops the compiler cannot fold; every result goes to a signature slot AND is checked against a
// value derived from the C abstract machine in arbitrary-precision arithmetic (never from any model). A
// failed check returns nonzero -> the shim's HTIF fail. Operands pass through `opaque` so the ELF carries
// the operations the source names (the census of the disassembly is the recorded fact).
#include "wl-common.h"
static __attribute__((noinline)) u64 collatz_steps(u64 n) { u64 s = 0; while (n != 1) { n = (n & 1) ? 3 * n + 1 : n / 2; s++; } return s; }
static __attribute__((noinline)) u64 modpow(u64 b, u64 e, u64 m) { u64 r = 1; b %= m; while (e) { if (e & 1) r = (r * b) % m; b = (b * b) % m; e >>= 1; } return r; }
static __attribute__((noinline)) u32 lcg(u32 x, int rounds) { for (int i = 0; i < rounds; i++) x = x * 1664525u + 1013904223u; return x; }
static __attribute__((noinline)) i64 sdiv_tour(i64 a, i64 b) { return a / b * 1000 + a % b; }
static __attribute__((noinline)) u64 mulhu_tour(u64 a, u64 b) { unsigned __int128 p = (unsigned __int128)a * b; return (u64)(p >> 64) ^ (u64)p; }
static __attribute__((noinline)) i64 mulh_tour(i64 a, i64 b) { __int128 p = (__int128)a * b; return (i64)(p >> 64) + (i64)p; }
static __attribute__((noinline)) u32 w_tour(u32 a, u32 b) { return a / b + a % b + a * b; }
static __attribute__((noinline)) i32 sw_tour(i32 a, i32 b) { return a / b - a % b; }
int main(void) {
    int slot = 0, bad = 0;
    EMIT(collatz_steps(opaque(27)), 111);                                    // 27 reaches 1 in 111 steps
    EMIT(collatz_steps(opaque(97)), 118);
    EMIT(modpow(opaque(3), opaque(200), opaque(1000000007ul)), 136318165ul); // pow(3, 200, 1e9+7)
    EMIT(lcg((u32)opaque(1), (int)opaque(10)), 0xa3a5a0e3u);                 // ten LCG rounds from 1, mod 2^32
    EMIT(sdiv_tour((i64)opaque((u64)-7), (i64)opaque(2)), (u64)(i64)(-3001));   // -7/2 = -3, -7%2 = -1 (C99 truncation)
    EMIT(sdiv_tour((i64)opaque(7), (i64)opaque((u64)-2)), (u64)(i64)(-2999));   // 7/-2 = -3, 7%-2 = 1
    EMIT(mulhu_tour(opaque(0xffffffffffffffffull), opaque(0xffffffffffffffffull)), 0xffffffffffffffffull); // hi ^ lo of (2^64-1)^2
    EMIT(mulh_tour((i64)opaque((u64)-3), (i64)opaque(5)), (u64)(i64)(-16));     // hi(-15) = -1, lo = -15
    EMIT(w_tour((u32)opaque(0x80000000u), (u32)opaque(3)), 0x2aaaaaaau + 2u + 0x80000000u);  // divuw + remuw + mulw, wrapping in 32 bits
    EMIT(sw_tour((i32)opaque((u64)(u32)0x80000000u), (i32)opaque(7)), (u64)(i64)(-306783378 - (-2)));  // INT32_MIN/7 = -306783378, INT32_MIN%7 = -2
    return bad;
}
