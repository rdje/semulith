# A board on the accepted processor needs a processor contract that admits devices, so the netboard re-bases onto rv64gc version 1

- **Type:** `decision`
- **Date:** `2026-11-10`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.13`'s design brief, `SEMULITH-P5-0020`; the engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Can a board compose the accepted rv64gc-lab-v0 version 0, and if not, what must change first and which board carries it?

## What was measured

Each processor's effective contract, read with the project's own reader (`records_sexp` and `effective_contract.contract_measure`); re-derive from the repository root:

```sh
python3 -B -c '
import sys; from pathlib import Path; sys.path.insert(0, "scripts")
import records_sexp as R, effective_contract as E
for u in ("rv64i-lab-v0", "rv64gc-lab-v0"):
    d = Path("profiles") / u; obs = R.load(d / "contract-obligations.sexp"); by = {o["id"]: o for o in obs}
    ids = sorted({ob for ob, _ in E.contract_measure(d, obs)[0]})
    print(u, len(ids), [i for i in ids if by[i]["direction"] != "cpu-guarantee"])'
```


| Processor | Effective obligations | Environment assumptions |
| --- | --- | --- |
| `rv64i-lab-v0` | 36 | 8 |
| `rv64gc-lab-v0` | 57 | 10 |

`netboard-lab-v0` composes the scalar contract: 36 of its catalogue's obligations are `rv64i-lab-env-v0`'s, and 71 are its two devices'. Its UART and NIC are polled MMIO devices with no bus-master DMA, and it declares timers and interrupt controllers absent by contract.

Against that board, `rv64gc-lab-v0`'s ten assumptions read:

| Assumption | A polled, DMA-free MMIO board | Why |
| --- | --- | --- |
| `OB-GC-ENV-DATA-ACCESS` | **contradicts it** | "The laboratory physical map contains only executable, little-endian main memory, with no MMIO or side-effecting reads." |
| `OB-GC-ENV-INTERRUPT-SOURCES-V2` | holds for a polled board; **contradicts** any board with timers or interrupt controllers | "The laboratory supplies no external interrupt source: MSIP, MTIP and MEIP read zero" and "No new latch, platform controller, injected pending event or host timer is introduced." |
| `OB-GC-ENV-VIRTUAL-TIME` | holds if the board's time is the hart's step count | time and `mcycle` advance by one at every step boundary, and no host time reaches the guest |
| `OB-GC-ENV-RESERVATION-EVENTS` | holds without DMA | one hart and no other agent writing memory |
| the other six | none contradicts it, on reading | addressing, fetch supply, ordering, event positions, reset and translation inputs; read, not exercised against a device model, so the window's brief re-reads each against the device-region version |

## The decision

1. **Version 0 is a closed-laboratory processor.** Its acceptance is real and stays: it says what the CPU does with main memory, its own timer comparator and no outside agent. No board with a device composes it. `BOARD-VERDICT` would reject one by name, and it should.
2. **A board needs a processor contract version that admits device regions.** That version supersedes `OB-GC-ENV-DATA-ACCESS` with one that declares MMIO regions: their access widths, side-effecting reads, and no instruction fetch from them. ROADMAP P5's timers and interrupt controllers need a further supersession of `OB-GC-ENV-INTERRUPT-SOURCES-V2` that names MTIP and MEIP sources. Each is a change to `rv64gc-lab-v0`'s dossier, so it rides in a new version with its own release decision: `P4-SYSTEM.20`, the next pinned window, carries the first. Whether the interrupt sources come in the same version is that window's design brief to measure.
3. **The netboard re-bases; no second board.** Once version 1 admits device regions, `netboard-lab-v0` composes it: its devices, map and generated artifacts carry over, its 36 scalar obligations become rv64gc's effective ones, and its three `satisfies` edges re-target. A second board would double the generators, books and verdicts to keep a board on a processor whose role is the scalar laboratory. The scalar composition verdict stays readable in history.
4. **Until then nothing changes.** The netboard's verdict against `rv64i-lab-v0` stays mechanically valid, as a contract-design result, and its claims stay conditional on that experimental processor.

## What this does not settle

- Which interrupt controller and timer device the board gets. ROADMAP P5 names timers and interrupt controllers; P6's firmware decides what it needs of them.
- Whether `OB-GC-ENV-VIRTUAL-TIME` survives a board timer unchanged. A device timer that counts steps keeps it; one that counts anything else supersedes it.

## How to apply

- `P4-SYSTEM.20`'s brief measures the device-region supersession with the rest of the window, and the window's list names it.
- `P5-BOARD.13` waits on that version's release decision, then re-bases the netboard and re-runs `BOARD-VERDICT`, `BOARD-GEN` and `PLATFORM-GEN`.
- A board leaf that composes a processor reads that processor's environment assumptions first, with the command above.
