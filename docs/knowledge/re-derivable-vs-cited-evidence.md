# A document reports a check that passed elsewhere — may this project rely on it?

**Answer: cite it, label it, and do not count it.** A result produced in an environment this
repository cannot reproduce is a *cited* claim. It may inform a decision; it may not discharge
an obligation, appear as a gate's passing input, or be summarised as "checked".

## Evidence

`docs/provenance/planning-package-v0.2/PACKAGE_CHECKS.md` reports schema validation with
Python `jsonschema` 4.26.0 and the counts it produced. In this repository:

```
$ python3 --version
Python 3.14.7
$ python3 -c "import jsonschema"
ModuleNotFoundError: No module named 'jsonschema'
```

So the leg-1 question ("does it reproduce, by command, from the source?") currently has no
answer here, and the honest report is *cited, not re-derivable in this repository*.

## How to convert a citation into evidence

Build the producer inside the repository and track it. Here, rule `RUST-01` makes that a Rust
deliverable rather than a Python dependency, and the P1 checker lane owns it — the schemas
must be validated by something this project builds, runs, and versions.

Until then the gap is *named*: `EVD-08` requires reports to carry their limitations, and
`SRC-03` forbids presenting an unrun check as a run one. A claim with a named gap is usable;
a claim with a hidden gap is the defect.

## The general rule

Three different questions, and only the first is about the number being right:

1. **re-derive** — does one command in this tree reproduce it?
2. **falsify** — what would make it false, and is there an oracle we did not build?
3. **durability** — is the producer tracked, and does anything fail when it goes stale?

An imported result answers none of them. It inherits its author's answers, which do not
travel with the file.
