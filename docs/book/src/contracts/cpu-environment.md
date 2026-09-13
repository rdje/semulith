# The CPU/environment contract

> **Orientation.** A CPU is never validated in the abstract — it is validated *under stated
> assumptions about what memory and devices will do*. This contract is what makes that
> conditional explicit instead of accidental.
>
> It has its own ID, version, requirement catalog, parameters, legal-event rules, and tests.
> Scalar configuration fields cannot express all of it: ordering, temporal rules, and
> relationships *between* responses have to be enumerable named requirements too, or the
> interesting failures have nowhere to be written down.
>
> Every entry names its authority — processor specification, chosen implementation parameter,
> platform specification, or explicitly synthetic laboratory policy. **Laboratory policy cannot
> override an architectural requirement**, and labelling which is which is what stops a
> convenient test harness decision from quietly becoming a claimed processor behaviour.
>
> §5 is the board's obligation: for every CPU assumption, name the guarantee that satisfies it,
> or reject the composition. That check is the reason the CPU-first ordering survives contact
> with integration bugs.

{{#include ../../../CPU_ENVIRONMENT.md}}
