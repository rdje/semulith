# My differential comparison says the two models agree — over how many steps?

**Ask, because a comparator that walks only the overlapping prefix will call a truncated run a
pass.** If one model stops early — it trapped, it hit a harness bound, it crashed — the prefix
that both produced can agree perfectly while the *observation* differs completely. The verdict is
green and the evidence is worthless.

## What happened

Two reference models were compared on a program whose last instruction performs a misaligned
load. The comparator printed:

```
AGREE over 2 aligned step(s) (sail-riscv: 3 parsed, spike: 2 parsed)
```

Read it again: **3 parsed and 2 parsed**, and the verdict is `AGREE`. One model had recorded the
misaligned-load trap as a third step; the other had emitted no commit record for a trapping
instruction and simply stopped. The first two steps did match. The thing the experiment existed
to test — *do these two models report this fault the same way?* — was never compared at all.

The comparison was written to return the first differing step and, finding none in the common
prefix, to report agreement. It had no opinion about a prefix being all there was.

## The fix, and the part of it that is not obvious

A length mismatch became a **non-agreeing verdict that has to be explained**:

```
LENGTH MISMATCH after 2 agreeing step(s): sail-riscv produced 3, spike produced 2
  sail-riscv continues at pc=0x0000000080000008 insn=0x40152083; spike stopped.
  The agreeing prefix is NOT a pass. Explain why one model stopped — a trap the other
  reported differently, a harness instruction bound, or a genuine divergence in control
  flow — before recording this run as evidence.
```

It is deliberately **not** an automatic failure-with-a-reason. A length mismatch often *is*
innocent: two harnesses take their instruction bounds from different flags and count different
things. But innocence is for the operator to establish. The comparator's job is to refuse to
decide that on its own, because the wrong default here is silent and green.

Running down the explanation, in this case, produced the actual finding: both models *did* raise
the identical exception with the identical `tval`. They merely record a trapping instruction
differently — one commits it with the trap attached, the other prints a disassembly line and an
exception and commits nothing. That is a **trace-vocabulary difference**, and it belongs in the
adapter, written down, rather than being absorbed by a lenient comparison.

## The general rule

This is `TOOLBOX.md`'s standing rule — *a gate never observed RED is not known to work* — applied
one level up, to the thing doing the comparing:

> **A comparison that has never been seen to diverge is not known to detect divergence.**

So a differential comparator needs RED controls of its own, and they must include the boring
ones: a differing register value, a differing exception *cause*, a differing *tval*, a truncated
trace, and an exception spelling the adapter does not recognise. That last one matters for the
same reason as the first: an unparsed trap is a **dropped** trap, and a dropped trap reads
exactly like agreement. The adapter here raises on an unknown spelling rather than skipping it.

⭐ The project's own gate now enforces the discipline in data: an experiment record claiming
agreement must name the control that was observed failing, or `PROFILE-CONSISTENCY` refuses it.

Related: [[self-test-arms-that-never-ran]], [[re-derivable-vs-cited-evidence]],
[[availability-is-not-identity]].
