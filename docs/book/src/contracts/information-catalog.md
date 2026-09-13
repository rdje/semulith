# The information catalog

> **Orientation.** Twenty-four categories of information a processor model may need, `C01`
> through `C24`, each with a representative validation question. It is a **collection
> checklist**, not a feature list: not every target implements every category, and each one
> needs an explicit applicability decision rather than an invented default.
>
> The last section, *Information that must not be conflated*, is the highest-value page in the
> package for anyone who has written an emulator before. Every row is a mistake that produces
> a model which looks right:
>
> - an accurate CPU cannot promise to boot arbitrary board firmware;
> - reproducing an FFT mathematically says nothing about whether DSP machine code executes
>   correctly;
> - host endianness, integer behaviour and floating-point defaults must never define the target
>   by accident;
> - an instruction *absent from the target* may trap, while an instruction *missing from the
>   model* is a model limitation — and reporting the second as the first is an emulator lying
>   to its guest;
> - **architecturally unspecified** has a specification-defined meaning, while **not yet
>   researched** is our own evidence gap.

{{#include ../../../INFORMATION_CATALOG.md}}
