# Provenance and frozen records

Supplied material arrives under `docs/provenance/<package>/`, verbatim, with a `DELIVERY.md`
recording what arrived, when, and with which fingerprints. Nothing there is maintained against
the live tree — the live tree is maintained against the task-trees.

## Why a delivered manifest is not a live check

The v0.2 planning package arrived with a root-level `MANIFEST.sha256` listing 25 files. It
verified cleanly on arrival — and two of its rows named `README.md` and `ROADMAP.md`, the two
files this repository exists to change.

A manifest at the repository root invites `shasum -a 256 -c` while containing rows whose failure
is already scheduled. Its only stable outcome would be failure, and **a check whose failure is
expected trains its reader to skip it** — after which it silently stops covering the rows that
were still meaningful.

## The three dispositions

Every manifest row is given exactly one, as **data** in the package's `dispositions.tsv`:

| Disposition | Meaning | Gated |
| --- | --- | --- |
| `frozen-in-place` | still at the delivered path with the delivered bytes | re-hashed every commit |
| `relocated` | identical bytes, moved; the row's path is the delivery path | re-hashed every commit |
| `live` | this repository owns it now; drift is expected | existence only |

There is no fourth, unstated category. An undeclared manifest row, or a disposition naming a
path the manifest never listed, is a breach — that asymmetry is precisely how a row would
otherwise leave coverage without anyone deciding it should.

The counts are **derived on every run**, not written down here: one derived source beats N
synchronized copies.

## Inputs that are not in the repository

`DESIGN_INPUTS.json` fingerprints three documents supplied to the package's author and not
reproduced here — roadmap v0.1, its review, and archogen's revision 2.0. Those hashes are
unverifiable from this repository alone, and that is **stated rather than implied**: the schema
field they use is `file_name`, not `path`, specifically so the `FIXTURE-FINGERPRINT` gate does
not treat an unverifiable hash as a checked one.

## Results that were produced elsewhere

`PACKAGE_CHECKS.md` reports schema validation with Python `jsonschema` 4.26.0 in an environment
this one is not. Those results are **cited, not re-derivable here**. Rule `RUST-01` makes the
re-derivation a Rust deliverable, and the P1 checker lane owns it.

Cite it, label it, do not count it. A claim with a named gap is usable; a claim with a hidden
gap is the defect.
