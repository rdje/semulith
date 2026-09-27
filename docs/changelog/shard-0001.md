# CHANGELOG shard — SEMULITH-P0-0031 … SEMULITH-P0-0031

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P0-0031 (leaf P0-PROFILE.10) — the profile was matched on its ISA and not its platform

**What changed.** A challenge to the previous findings turned up a real defect that the first nine
leaves of this tree carried. The matched-profile override configured `base`, `memory.misaligned`
and `extensions` — and **nothing else**. `--print-isa-string` returned `rv64i_zvl32b`, which is
correct, and was read as *"matched"*. It answers a narrower question than that.

Underneath the correct ISA the reference kept its default platform: a core-local interruptor at
`0x0200_0000`, an interrupt generator, machine software/timer/external interrupts all `supported`,
and two IOMemory regions. Established by probe:

```
[5] ld x1, 0x0(x10)      clint[0x…BFF8] -> 0x0000000000000002   x1 <- 0x2
[6] ld x2, 0x0(x10)      clint[0x…BFF8] -> 0x0000000000000003   x2 <- 0x3    # ADVANCING
```

**A guest read a monotonically advancing time source with a plain load — no CSR instruction.**
Four committed claims are refuted by that one measurement: `OB-ENV-VIRTUAL-TIME` ("no time source
is modelled"), `OB-ENV-EVENT-DELIVERY` ("no interrupt controller … no privileged mode"),
`D-MAIN-VS-IO` ("no I/O region is declared"), and `privilege_modes = []` — every trace line in
this repository reads `[M]`, because a hart is always in at least machine mode.

- **Corrected at source, not reworded.** The override now sets `platform.clint.supported = false`,
  the interrupt generator off, all three machine interrupt sources off, and `memory.regions` to
  the single MainMemory region the profile declares. Both probes now raise `load-access-fault`.
- `profile.toml` gains `D-PLATFORM`, corrects `D-MAIN-VS-IO`, and sets `privilege_modes = ["M"]`.
  Decisions 25 → 26, requirements 25 → 26, obligations 33 → 34, checks 66 → 68, differences 4 → 6.
- **The repair is held permanently** by a tracked negative fixture, `guests/guest-no-device.s`,
  which reads CLINT `mtime` and must fault. A device becoming reachable again turns the run red.
- **The three original guests still agree** over 12 / 13 / 3 aligned steps and reproduce
  byte-identically — the repair changed nothing it should not have.

⭐ **Spike is not platform-matched and cannot be**, which is enumerated rather than fixed. Its
interruptor is built in; `--device` only *adds* MMIO plugins; and `-m0x80000000:0x10000` kills its
own reset vector (`trap_instruction_access_fault, epc 0x1000`). `SRC-02` makes that a legitimate
result that **bounds** the claim: any guest touching `0x1000` or `0x0200_0000..0x11ff_ffff`
behaves differently on the two references. The three original guests touch neither — now a
**stated precondition rather than luck**. `guest-no-device` disables its cross-model comparison
for this reason and the runner **prints the skip** rather than applying it silently.

⛔ **The instrument is the lesson.** This is not the `zero-hits` failure — an instrument that could
not see. It is worse and quieter: **an instrument answering a narrower question than the one
asked**. `--print-isa-string` gave one confident string, and the string was true.

**Effect on `G0`.** The verdict stays `incomplete` for the same reason (68 declared checks, 0
implemented). But criterion 3 — *differences enumerated, not assumed absent* — is now met on
evidence rather than on an unexamined configuration, which is a real change in what the gate means.
