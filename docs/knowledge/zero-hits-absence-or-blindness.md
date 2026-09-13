# My search returned zero hits — is that absence, or is my instrument blind?

**Find out before you write it down.** A zero from a tool that cannot see the thing you are asking
about is indistinguishable, on screen, from a zero that means the thing is not there. The first is
a non-answer; the second is a finding. They are printed identically.

## What happened

The question was whether two reference models share a floating-point implementation — an `EVD-04`
independence question, where a wrong answer silently inflates the value of every differential
test. The obvious instrument:

```
$ strings -a sail_riscv_sim | grep -ciE 'softfloat|f32_add|f64_mulAdd'
0
$ strings -a spike           | grep -ciE 'softfloat|f32_add|f64_mulAdd'
0
```

Zero for both. Read naively: *neither model uses SoftFloat.* That was one step from being recorded
as a finding in a durable inventory.

A second instrument disagreed, and explained the first:

```
$ nm -a sail_riscv_sim | wc -l      ;  nm -a sail_riscv_sim | grep -ci softfloat
400                                    0
$ nm -a spike          | wc -l      ;  nm -a spike          | grep -ci softfloat
649743                                 495
```

Spike carries **495** softfloat-shaped symbols. The Sail binary carries **400 symbols in total** —
it is a stripped release build, and no symbol-based instrument can answer any question about its
internals. Its zero was never evidence about SoftFloat; it was evidence about the binary's symbol
table.

Reading the source settled it: the Sail model vendors Berkeley SoftFloat too, and 184 of the 199
`.c` files present in both copies are byte-identical. **The naive reading was the exact opposite
of the truth.**

## How to tell the two apart

Every zero needs a companion measurement that establishes the instrument could have seen a hit:

| The zero | The companion that validates it |
| --- | --- |
| `grep -c X file` → 0 | does `grep -c <something-certainly-present> file` return non-zero? |
| `nm \| grep -c X` → 0 | how many symbols are there *at all*? `400` is a stripped binary |
| `find … -name X` → nothing | does the search root exist and contain anything? |
| an API query returns `[]` | did it authenticate, and does it return rows for a known-present case? |
| a test suite reports 0 failures | how many tests *ran*? (see [[self-test-arms-that-never-ran]]) |

The pattern is always the same: **report the denominator next to the numerator.** `0 of 400
symbols` and `0 of 649,743 symbols` are different sentences; `0` and `0` are the same sentence.

## The rule

> A zero from an instrument whose reach you have not measured is not a result. It is a question
> you have not asked yet.

When the denominator turns out to be too small to trust — a stripped binary, an empty search root,
an unauthenticated query — do not weaken the claim to fit the instrument. **Change instrument.**
Here that meant cloning the model's source, at the exact commit its own `--build-info` reports, and
reading it. That cost one shallow clone and turned a false finding into a true one.

Related: [[self-test-arms-that-never-ran]], [[availability-is-not-identity]],
[[a-shorter-trace-is-not-agreement]].
