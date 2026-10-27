// wl-calls.c — the call workload: Ackermann(2, 3) by the textbook recursion, a recursive Fibonacci, a
// function-pointer dispatch table driven by a loop (an indirect jalr per round), and a deep call chain
// spilling registers. Expected values derived in gen_workloads.py.
#include "wl-common.h"
static __attribute__((noinline)) u64 ack(u64 m, u64 n) { if (m == 0) return n + 1; if (n == 0) return ack(m - 1, 1); return ack(m - 1, ack(m, n - 1)); }
static __attribute__((noinline)) u64 fib(u64 n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
static __attribute__((noinline)) u64 f_add(u64 x) { return x + 7; }
static __attribute__((noinline)) u64 f_mul(u64 x) { return x * 3; }
static __attribute__((noinline)) u64 f_xor(u64 x) { return x ^ 0x55; }
static __attribute__((noinline)) u64 f_shr(u64 x) { return x >> 1; }
static u64 (*const table[4])(u64) = { f_add, f_mul, f_xor, f_shr };
static __attribute__((noinline)) u64 chain(u64 a, u64 b, u64 c, u64 d, u64 e, u64 f, u64 g, u64 h, u64 i) { return a + 2*b + 3*c + 4*d + 5*e + 6*f + 7*g + 8*h + 9*i; }
int main(void) {
    int slot = 0, bad = 0;
    EMIT(ack(opaque(2), opaque(3)), 9);
    EMIT(fib(opaque(15)), 610);
    u64 x = opaque(100), d = 0; for (int i = 0; i < 12; i++) { x = table[i & 3](x); d = d * 131 + x; }
    EMIT(d, 5985972586309034701ul);
    EMIT(chain(opaque(1), opaque(2), opaque(3), opaque(4), opaque(5), opaque(6), opaque(7), opaque(8), opaque(9)), 285);
    return bad;
}
