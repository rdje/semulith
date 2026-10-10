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

## Exceptional push records and local self-tests

An exceptional push below the commit cadence needs the director's explicit
approval. After that approval, use the recorded act described in `COMMIT.md`:

```bash
scripts/approved_push.sh '<the director’s reason, verbatim>'
```

The act first runs full local CI, then appends and commits the approval in
`docs/push-approvals.md`, then pushes through the boundary. Setting the approval
variable alone does not supply that record. The cadence refusal names this act;
it does not grant approval. The CI recovery exception recorded in
`docs/decisions/decision_ci-recovery-push-approval.md` was fulfilled on `76882c8`
and expired when all three hosted workflows had passed on 2026-10-08. Ordinary
cadence applies afterward.

The three helper tests can be run independently:

```bash
bash scripts/check_push_cadence.sh --self-test
bash scripts/pre_push.sh --self-test
bash scripts/approved_push.sh --self-test
```

Each derives `target/push-selftest/` from its owning repository, including nested
Git/toolchain temporary storage, rather than accepting the caller's temp path.
Successful tests remove their synthetic fixture directories. Their Git pushes
use local throwaway upstreams and stub suites; they neither push this project
nor establish a real full-CI result or exceptional-push authorization. These
helper tests are not registered doctrine arms, so their local totals do not add
to the registered doctrine census.

The approval-act test starts with a literal synthetic prior approval. When its
stub suite fails, the entire ledger must remain byte-for-byte equal to that
baseline, and no commit may be added. Merely finding an entry is insufficient:
that entry might have existed before the failed attempt. A separate successful
case checks that the new approval commit reaches the local synthetic upstream.
