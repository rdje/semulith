# SYN16 synthetic fixture specification

Version: 1. This is an invented fixture for illustrating data contracts; it represents no physical processor.

## A1 — Addition

Inputs `a` and `b` are unsigned 16-bit values. The result is `(a + b) modulo 65536`, also an unsigned 16-bit value. There are no status flags, exceptions, memory effects, or time claims. The host's overflow behavior has no bearing on this definition.

Boundary examples for future checks: `0 + 0 -> 0`; `65535 + 1 -> 0`; `32767 + 1 -> 32768`. These are mathematically derived expected values, not observations from an implementation.

## E1 — Input contract

The fixture environment supplies `a` and `b` in the inclusive range 0 through 65535. Input outside this range is a malformed fixture and must be rejected by the harness before invoking the arithmetic operation. It is not a guest architectural exception.
