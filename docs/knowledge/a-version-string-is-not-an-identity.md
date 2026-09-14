# Someone says my pinned source does not exist — is my pin wrong, or are we reading different publications?

**Check which publication each of you searched before you touch the pin.** The same specification
is often published more than once — a source repository, a release PDF, a rendered documentation
site — and the renderings disagree about things that look canonical, section numbers above all. A
version string names a point in time. It does not name *which* publication you took it from, and
without that half it identifies nothing.

## What happened

This project pinned `v20260120` of the RISC-V unprivileged specification and derived 52 instruction
semantics from it, each citing a section: `RVI-RV64I §3.1.2.1`, `RVI-RV32I §1.1.4`, and so on.

An external investigation reported, carefully and with evidence:

- there is no `2026-01-20` release of `riscv/riscv-isa-manual` — the tags jump `01-17` → `01-21`;
- the January release PDFs number **RV32I §2 and RV64I §4**;
- the `§1.1` / `§3.1` numbering is what you get only if "Introduction" is unnumbered front matter
  rather than Chapter 1 — and every build they checked numbers it as Chapter 1;
- therefore the pin "uses a numbering no public build produces".

Every one of those observations was **true**. The conclusion was wrong. The pin is not a GitHub
tag at all — it is a version segment of a *different publication*, `docs.riscv.org`, the RISC-V
Ratified Specifications Library, which renders "Introduction" as unnumbered front matter exactly
as the report deduced, and therefore numbers RV32I `§1.1` and RV64I `§3.1`.

Re-derived, end to end:

```
$ curl -sI https://docs.riscv.org/reference/isa/v20260120/unpriv/rv64.html   -> HTTP 200
$ sha256 live == sha256 pinned == sha256 in sources.toml                     -> identical, all 3 files
$ python3 scripts/check_citations.py
  52 of 52 instruction citations resolve in the pinned artifact
```

⭐ **The investigation was not sloppy — it was under-informed by me.** What I had published was the
bare string `v20260120`, with no publication attached. Given only that, searching the source
repository is the *reasonable* first move. The report even reconstructed the exact numbering rule
that explains the discrepancy; it lacked only the fact that some publication applies that rule.

## Why it survived so long

Nothing could have settled it mechanically. The project's semantics checker asks whether each rule
**carries** a citation — and a citation that points nowhere still carries. The question "does
`§3.1.2.1` exist in the document we pinned?" had no instrument, so it could only be answered by a
person going and looking, which is exactly the kind of question that gets answered by assertion
instead. See [[a-parse-without-error-is-not-a-faithful-read]] for the same shape one layer down:
presence checked, fidelity not.

## What to do about it

| Record | Not this | But this |
| --- | --- | --- |
| the source | `revision = "v20260120"` | publication **and** revision, plus the publication it is *not* |
| the locator | "§3.1.2.1" | a locator plus an instrument that resolves it against the pinned bytes |
| the artifact | a URL | a URL, a digest, and a re-fetch that compares the two |

And keep the **negative** field. `sources.toml` now carries a `not_this_publication` line naming
`github.com/riscv/riscv-isa-manual` and the reason it differs, because the next person to check
this will start where the last one did, and a record that only says what a thing *is* leaves the
most likely wrong turn unmarked.

## The rule

> A version identifies a point in time within one publication. Cross-publication, it identifies
> nothing — and section numbers are exactly the part that will not survive the crossing.

When a claim of yours is challenged from outside: **re-derive it from the primary artifact before
defending it and before conceding it.** Here the challenge was refuted in four commands — but had
the digests disagreed, the same four commands would have proved the challenger right, which is what
makes running them first the honest move rather than a defensive one.

Related: [[availability-is-not-identity]], [[a-parse-without-error-is-not-a-faithful-read]],
[[re-derivable-vs-cited-evidence]].
