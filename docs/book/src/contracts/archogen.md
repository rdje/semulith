# archogen and eADL

> **Orientation.** archogen generates specific-purpose operating systems from **eADL**, its
> source of truth. Semulith provides modelled processors and, after their validation, the
> platforms those OSes run and are tested on.
>
> The boundary is the whole content of this chapter, and it is an *ownership* boundary rather
> than a repository or language one:
>
> - **eADL** describes hardware and OS functionality, required and offered behaviour, workload,
>   and constraints. It contains **no implementation**.
> - **archogen's engine** owns algorithms, provider selection, lowering, code generation, and
>   simulator composition.
> - **Semulith** owns executable CPU and device behaviour, exposed through versioned APIs.
>
> Missing model behaviour is therefore an unsupported *engine realization* — never a reason to
> put implementation into eADL. And Semulith does not grow a second eADL parser, matcher,
> scheduler, or OS generator; it consumes archogen's checked realization plan through a
> versioned adapter.
>
> Two honesty constraints survive the integration. Generated tests from eADL cannot detect an
> incorrect eADL interpretation **shared** by the OS and test generators. And if the hosted
> playground reuses Semulith device transitions, their agreement is shared-model evidence, not
> an independent hardware comparison — Semulith does not become an independent oracle merely by
> being a separate project.

{{#include ../../../ARCHOGEN_INTEGRATION.md}}
