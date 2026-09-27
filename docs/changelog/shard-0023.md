# CHANGELOG shard — SEMULITH-MM-0043 … SEMULITH-MM-0043

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0043 (leaf MODEL-METHOD.12) — a citation that is present is not a citation that resolves

**The challenge.** An external investigation reported that this profile's pinned source does not
exist: `riscv/riscv-isa-manual` has no `2026-01-20` tag (the tags jump `01-17` → `01-21`), its
January release PDFs number **RV32I §2 and RV64I §4**, and the `§1.1` / `§3.1` numbering used by all
52 semantic citations is what you get only when `Introduction` is unnumbered front matter rather
than Chapter 1 — which no build it checked does. Conclusion: the pin matches no public build.

**Re-derived from the primary artifact before defending or conceding.** Every observation in the
report is true. The conclusion is not, and the difference is one word: **publication**.

```
github.com/riscv/riscv-isa-manual   numbers Introduction as Chapter 1  -> RV32I §2,    RV64I §4
docs.riscv.org  (pinned here)       Introduction is front matter       -> RV32I §1.1,  RV64I §3.1
```

`docs.riscv.org` is the RISC-V **Ratified Specifications Library**, a different publication of the
same specification, and it applies exactly the numbering rule the report deduced. Verified end to
end:

```
$ curl …/reference/isa/v20260120/unpriv/{intro,rv32,rv64}.html   -> HTTP 200 ×3
  and byte-identical to the pinned copies AND to the digests committed in sources.toml
$ python3 scripts/check_citations.py
  52 of 52 instruction citations resolve in the pinned artifact
```

⭐ **The investigation was not sloppy — it was under-informed by me.** What I had published was the
bare string `v20260120` with no publication attached, and given only that, searching the source
repository is the *reasonable* first move. The report even reconstructed the numbering rule that
explains the discrepancy; it lacked only the fact that some publication applies it.

**The real defect, which the challenge exposed and which was not the pin.** Nothing could have
settled this mechanically. `check_semantics.py` asks whether a rule *carries* a citation, and a
citation pointing nowhere still carries. `scripts/check_citations.py` now resolves every locator
against the pinned bytes — 10 self-test arms, and it **refuses rather than passing** when the
artifacts are absent, which matters because they are untracked and need the network:

```
$ mv target/sources/riscv-v20260120 … && python3 scripts/check_citations.py ; echo $?
REFUSED: the pinned artifacts are not present at target/sources/riscv-v20260120 … exit=1
```

`sources.toml` now names its publication **and the one it is not**, because the next person to
check this will start where the last one did.

**The interim substitution is declined**, recorded as `GAP-RISCV-JAN-2026-PDF`. Adopting the
January PDFs would turn 52 resolving citations into 52 unresolvable ones — a strictly worse
position reached by acquiring *more* material. They may be catalogued later under their own ids;
acquiring a document and repointing a pin are two decisions and only the first is cheap.

**Also measured:** the docs.riscv.org rendering carries only `Copyright © RISC-V International®` —
**no CC-BY statement**, unlike the GitHub PDF. So `OQ-4` (redistribution terms) stays open for the
rendering, and the pinned HTML is still read, never redistributed.

**Knowledge.** [`a-version-string-is-not-an-identity`](docs/knowledge/a-version-string-is-not-an-identity.md)
— a version names a point in time within one publication; across publications it identifies
nothing, and section numbers are exactly the part that will not survive the crossing.

