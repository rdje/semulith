// wl-memory.c — the memory workload: insertion sort of 64 words, a bitwise CRC32 over 256 bytes, a
// byte/half/word/dword store-load tour through a packed struct (little-endian composition), and a
// pointer-chasing linked list in .bss. Expected values derived in gen_workloads.py (arbitrary precision).
#include "wl-common.h"
static u64 words[64]; static u8 pattern[256];
struct __attribute__((packed)) tour { u8 b; u16 h; u32 w; u64 d; };
struct node { struct node *next; u64 v; };
static struct node nodes[16];
static __attribute__((noinline)) void isort(u64 *a, int n) { for (int i = 1; i < n; i++) { u64 k = a[i]; int j = i - 1; while (j >= 0 && a[j] > k) { a[j + 1] = a[j]; j--; } a[j + 1] = k; } }
static __attribute__((noinline)) u32 crc32(const u8 *p, int n) { u32 c = 0xffffffffu; for (int i = 0; i < n; i++) { c ^= p[i]; for (int k = 0; k < 8; k++) c = (c >> 1) ^ ((c & 1) ? 0xedb88320u : 0u); } return c ^ 0xffffffffu; }
static __attribute__((noinline)) u64 tour(struct tour *t, u64 seed) { t->b = (u8)seed; t->h = (u16)(seed >> 8); t->w = (u32)(seed >> 24); t->d = seed * 3; return (u64)t->b + t->h + t->w + t->d; }
static __attribute__((noinline)) u64 chase(struct node *n) { u64 s = 0; while (n) { s = s * 31 + n->v; n = n->next; } return s; }
int main(void) {
    int slot = 0, bad = 0;
    for (int i = 0; i < 64; i++) words[i] = ((u64)i * 2654435761ul ^ ((u64)i << 7)) & 0xffff;
    for (int i = 0; i < 256; i++) pattern[i] = (u8)(i * 37 + 11);
    isort(words, (int)opaque(64));
    u64 chk = 0; for (int i = 0; i < 64; i++) chk += words[i] * (u64)(i + 1);
    EMIT(chk, 90437073ul);
    EMIT(words[0], 0); EMIT(words[63], 64620);
    EMIT(crc32(pattern, (int)opaque(256)), 0x8ed7a350u);
    struct tour t; EMIT(tour(&t, opaque(0x0123456789abcdefull)), 245956588241255954ul);  // b + h + w + d with b = seed&0xff, h = (seed>>8)&0xffff, w = (seed>>24)&0xffffffff, d = 3*seed mod 2^64
    EMIT(*(volatile u8 *)&t.d, 0xcd);   // the dword's low byte: little-endian composition
    for (int i = 0; i < 16; i++) { nodes[i].v = (u64)(i * i + 1); nodes[i].next = (i + 1 < 16) ? &nodes[i + 1] : 0; }
    EMIT(chase(&nodes[(int)opaque(0)]), 3549814510065653880ul);  // fold s = s*31 + (i*i+1) over 16 nodes, mod 2^64
    return bad;
}
