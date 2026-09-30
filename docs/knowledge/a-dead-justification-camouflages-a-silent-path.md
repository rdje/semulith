# A comment explains why a silent skip is safe — can I trust it?

**No — re-measure its premise.** A justifying comment is a claim about the code as of the day it
was written. The definition can change under it; the comment stays; and what it camouflages turns
from a justified exception into a live silent path that review keeps skating over, because the
sentence reads like someone already checked.

## What happened

`P3-BREADTH.2`'s hook audit (`2026-10-01`) censused the generation pipeline for silent escape
hatches and found one in `exec.rs`'s operand extraction: an operand naming no field was
`continue`d past, justified by a comment — "FENCE's `fm`/`pred`/`succ` are declared operands
without field ranges". That premise was TRUE when written and FALSE at audit time:
`P2-SCALAR.1` had given all three field ranges (`definitions/riscv/rv64i.sexp:36-38`), so the
arm was unreachable for real data and the comment was dead weight in four places (the runtime,
the generator's emitted docstring, two test sites). The arm was still live for any FUTURE
unfielded operand — exactly the "guessed translation" `docs/ARCHITECTURE.md` §2 forbids.

The fix moved the invariant to where the contract says it lives: the GENERATOR now refuses an
operand that names no field (rc 2, naming instruction and operand), the runtime arm is a loud
`ModelError` instead of a skip, and the test ratchet lost its dead whitelist.

## Re-verify

```
bash scripts/check_definition_gen.sh   # its self-test's RED arm feeds an unfielded operand
                                       # and demands the named refusal
grep -rn "names no field" scripts/gen_definition.py crates/semulith-core/src/exec.rs
```

## The method, generalized

To census for silent escape hatches, don't read comments — enumerate the SHAPES silence takes:
default/catch-all arms that produce output or skip (`_ =>`, `let-else { continue }`), Python
`except:` bodies, `unwrap_or` on parsed definition data, lookups that fall back to identity.
Then for each hit, re-measure the justification's premise against TODAY's data. The hits whose
comments are still true are the designed seams; the rest are defects.
