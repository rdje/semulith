# Introduction

`sifive-uart-lab-v0` is the **SiFive UART** of the FU540-C000 manual's §13, dossiered as
the first *device* unit of the project — the serial console `uart0` of
[`netboard-lab-v0`](../../netboard-lab-v0/src/introduction.md). It is the unit that taught
the dossier machinery its device shape: the same gates that decide a processor dossier
decide this one, with applicability derived from the unit's declared vehicle
(`device-model` / `register-expectations`), never from an exemption.

The dossier under `profiles/sifive-uart-lab-v0/` is the device's **contract**: seven
32-bit registers, two 8-entry FIFOs, the pop-on-read discipline, the watermark level
conditions — and the six measured silences the datasheet never fills, recorded as
requirements of non-commitment rather than papered over. No device model exists yet;
this book is about what the unit is *built from* and how a reader can trust it.

> **Status: EXPERIMENTAL.** The unit inherits the board's and the processor's status;
> every claim reads as conditional on the CPU's acceptance trajectory.
