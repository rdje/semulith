# Architecture and canonical definitions

> **Orientation.** The central idea is *one owned executable implementation per semantic rule*.
> Files may be modular and artifacts may be generated, but there is never a second place where
> a behaviour is decided. Decoders, backends, disassemblers, documentation and coverage
> obligations are **derived**; a generated artifact carries the fingerprints of the definition,
> the generator, and the configuration that produced it, and is changed by regeneration rather
> than by editing.
>
> The second idea is that an *independent reference is not a competing authority*. It exists to
> challenge the canonical model, and it keeps its separate provenance precisely so that
> agreement between the two means something. A model that generates its own tests and passes
> them has demonstrated internal consistency and nothing else.
>
> Read the ownership map in §4 alongside [P1](../plan/p1.md): the crate boundary is an
> architectural boundary, not a packaging convenience.

{{#include ../../../ARCHITECTURE.md}}
