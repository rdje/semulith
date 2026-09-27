# My exhaustive reduced-width test fails on signed operations — is the primitive wrong?

**Probably not — the test is comparing at the wrong width.** Reducing the verification width
works differently for unsigned-bitwise operations than for signed ones, and the difference is
exactly where a naive exhaustive check lies to you.

## The rule

Bitwise and logical operations are **width-transparent on the low bits**: `and`, `or`, `xor`,
logical shifts, unsigned comparison, wrapping add/sub — the low *n* bits of the wide result
depend only on the low *n* bits of the inputs. For these, comparing `primitive(x, y) as u8`
against an 8-bit reference for all 65,536 `(x, y)` pairs is sound.

Signed operations are **width-sensitive**: the result depends on the sign bit, and the sign
bit lives at a different position at each width. `0x80 < 0` is **true** asked at width 8
(0x80 is -128 there) and **false** asked at width 64 of the same zero-extended byte (128 is
positive there). The low byte of a wide signed comparison does **not** equal the narrow
signed comparison of the low bytes.

## What happened here

`P1-LAB.2`'s 8-bit exhaustive sweep of `semulith-core`'s arithmetic primitives compared the
`u64` `slt` against an `i8` reference directly: `slt(x, y)` vs `(x as i8) < (y as i8)`. It
failed immediately — the primitive correctly treats `0x80` as +128 (its bit 63 is 0), the
reference treated it as -128. Same for `sar`: the reference replicated bit 7, the wide
primitive replicates bit 63.

The fix is not to weaken the test; it is to **embed the narrow signed view at the target
width before asking the wide primitive**: sign-extend each 8-bit input to 64 bits, then
compare against the sign-extended narrow reference. Logical ops stay width-transparent and
need no embedding.

```
let xs = (x as i8 as i64) as u64;              // the 8-bit signed view at XLEN
assert_eq!(slt(xs, ys), u64::from((x as i8) < (y as i8)));
```

## How to decide, per operation

| Operation class | Reduced-width check |
| --- | --- |
| add, sub, and, or, xor, shl, shr, sltu | compare the low byte against the narrow reference — width-transparent |
| slt, sar, and every operation whose contract names "signed" | sign-extend the narrow inputs to the target width first, then compare in full |
