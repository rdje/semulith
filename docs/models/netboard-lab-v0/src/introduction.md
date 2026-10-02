# Introduction

`netboard-lab-v0` is the project's first **board**: a minimal virtual platform composing
`rv64i-lab-v0` v0 — the EXPERIMENTAL CPU release, whose status the board inherits — with
exactly two devices, the SiFive UART (serial console) and the LAN9118 wired NIC, and
nothing else. Memory, reset and the serial console are present; timers and interrupt
controllers are **absent by contract**, and that is the design's sharpest edge: the CPU
contract excludes every guest-reachable time source and admits no deliverable
asynchronous interrupt, so a CLINT or PLIC would be a composition *rejection*, not a
feature.

The canonical definition is `profiles/netboard-lab-v0/board.sexp`, gated by
`schema/board.sexp` — the first non-processor source-of-truth schema — and it **pins
versions, not names**: the processor by unit id + version + the GATE-REPORT-gated
dossier content digest; each device by its datasheet's material id + revision + sha256.

The board's network device is its window on the world from v0: the LAN9118 is
programmed-I/O, so every device effect reaches the guest through its own MMIO accesses;
receive is recorded-trace replay (deterministic, evidence-grade, re-runnable in a fresh
clone), transmit is a recording sink, and a live host socket stays laboratory play at
the `Environment` boundary, never inside an evidence claim.

> **Status: EXPERIMENTAL.** The board inherits its processor's status; every board claim
> reads as conditional on the CPU's acceptance trajectory, and the composition can never
> outrank its processor.
