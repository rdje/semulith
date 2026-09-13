# What is claimed, and what is not

This page exists because the difference between *"we built an emulator"* and *"this exact
profile behaves as this exact specification revision permits, and here is the evidence"* is the
entire value of the project. Getting that difference wrong once costs more than every feature
gained by overstating it.

## Claimed today

Nothing about a processor.

At the time of writing this repository contains a reviewed **plan**, the **normative rules**
that plan will be executed under, starter **data contracts**, and the **enforcement machinery**
that makes those rules mechanical. The Rust workspace holds a placeholder crate.

## Not claimed

| Not claimed | Why it matters |
| --- | --- |
| An implemented CPU or DSP | No instruction semantics have been written. |
| A conformance result | No gate has been run. Gate status is `passed`, `failed`, or `incomplete`; nothing here is any of them yet. |
| An accepted processor profile | A profile is a *versioned* selection with attached evidence. None exists. |
| Validated reference access | Sail, Spike, ACT4, SoftFloat and TestFloat are **candidates**. None has been acquired, built, configured, or smoke-tested for this project. |
| Working schema validation *in this repository* | The delivered package reports schema checks run with Python `jsonschema` elsewhere. They are cited, not re-derivable here; rule `RUST-01` makes the re-derivation a Rust deliverable. |
| The name | *Semulith* is proposed. No crate, repository, domain, or trademark has been reserved or cleared. |

## The rules that keep it that way

Three of the project's normative rules exist specifically to stop this page from quietly
becoming false:

- **`SRC-03`** — never fabricate source hashes, test results, tool availability, namespace
  availability, or accepted gate status.
- **`EVD-01`** — finite testing, including deterministic differential testing, establishes
  *tested evidence* and is never labelled universal proof.
- **`AI-03`** — AI review and agreement are criticism and workflow aids, not independent
  conformance evidence.

And one mechanical habit: a gate that reports `incomplete` is never rewritten as `passed`
because the missing infrastructure is "coming". No *when available* clause turns an incomplete
gate into a pass.

## Reporting fidelity separately

When there are results, "supports architecture X" will not be among them. Fidelity is reported
per axis — instruction semantics, system modes, platform coverage, concurrency, timing,
implementation compatibility, and evidence — because a model can be excellent on one and absent
on another, and a single headline hides exactly that.
