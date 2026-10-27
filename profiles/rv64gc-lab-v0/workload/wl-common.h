// wl-common.h — shared by the rv64gc workloads (P4-SYSTEM.15 slice f): the signature region the start
// shim exports, an opaque barrier so the compiler must emit the operations the source names (the value
// is the compiler's fact; the barrier keeps it from being the compiler's constant), and the EMIT check.
typedef unsigned long u64; typedef long i64; typedef unsigned int u32; typedef int i32;
typedef unsigned short u16; typedef unsigned char u8;
extern volatile u64 wl_signature[64];
static inline u64 opaque(u64 v) { __asm__ volatile("" : "+r"(v)); return v; }
static inline double opaque_d(double v) { __asm__ volatile("" : "+f"(v)); return v; }
static inline float opaque_f(float v) { __asm__ volatile("" : "+f"(v)); return v; }
#define EMIT(v, want) do { u64 _v = (u64)(v); wl_signature[slot++] = _v; if (_v != (u64)(want)) bad++; } while (0)
