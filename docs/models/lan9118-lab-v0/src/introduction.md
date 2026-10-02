# Introduction

`lan9118-lab-v0` is the **Microchip LAN9118** 10/100 Ethernet controller of datasheet
DS00002266B, dossiered as the second device unit — the wired NIC `eth0` of
[`netboard-lab-v0`](../../netboard-lab-v0/src/introduction.md), and the board's window on
the world from v0. Where the UART exercised the device-dossier machinery on the simplest
contract, the NIC is the full-scale case: a real MAC+PHY with four host FIFOs, 24 direct
CSRs, 12 MAC CSRs behind a synchronizer, and 13 PHY registers behind an MII bridge —
52 mirrored requirement/obligation/decision records against the UART's 19.

The NIC is programmed-I/O only — no bus-master DMA — so every device effect reaches the
guest through its own MMIO accesses, exactly the shape the CPU contract's eight
assumptions tolerate. The dossier under `profiles/lan9118-lab-v0/` is the device's
**contract**; no device model exists yet, and nothing here is a probe result.

> **Status: EXPERIMENTAL.** The unit inherits the board's and the processor's status;
> every claim reads as conditional on the CPU's acceptance trajectory.
