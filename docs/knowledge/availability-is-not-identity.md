# The package manager has a formula with the right name — is it the right software?

**Not necessarily, and the name is the weakest possible evidence that it is.** Establishing that
*something called X exists and installs* is a different question from establishing that *it is
the X you meant*. Rule `SRC-03` is usually read as "don't record a URL as availability"; the
sharper form is **availability is not identity**, and a package manager is where the two come
apart most convincingly, because everything looks right.

## What happened

`P0-PROFILE.5` needed the Sail ISA specification language — the RISC-V reference formal model.
The host package manager has a formula called `sail`, bottled, current, and one command away:

```
$ brew info --formula sail
==> sail: stable 0.10.9 (bottled)
CLI toolkit to provision and deploy WordPress applications to DigitalOcean
https://sailed.io
License: GPL-3.0-only
```

It is a WordPress deployment tool. Nothing about the lookup *failed*: the formula existed, the
name matched exactly, the version was recent, the licence was real. Only the second line says so,
and only if you read it instead of the exit code.

Had the shape of the check been `brew info sail >/dev/null && echo available`, the dossier would
have recorded **"Sail: available via the host package manager"** — a sentence that is false,
sourced, and reproducible.

## The general shape

The failure mode is that the *query* succeeds while the *referent* is wrong. It recurs wherever a
short name is a namespace:

- a package registry (`pip install sail`, `npm i sail`, `cargo add sail`) — name collisions are
  first-come, not curated;
- a repository that has moved — `riscv-non-isa/riscv-arch-test` answered `301`, not `404`, and
  `curl -L` would have followed it silently to a different owner;
- a binary earlier on `PATH` than the one you meant;
- a container tag that was re-pointed.

## What to do instead

Check identity with a field that only the real thing can produce, and record *that*:

| Weak (availability) | Strong (identity) |
| --- | --- |
| the formula/package exists | its description, homepage and licence |
| `--version` prints something | `--build-info`: upstream release, git sha, compiler, vendored library versions |
| the URL returns `200` | the **final** URL after redirects, recorded when it differs |
| the binary runs | it answers a question only the right tool can answer |

For the reference models in this repository the identity field is
`sail_riscv_sim --build-info`, which prints `Sail RISC-V release 0.14; git 29e6158; Sail 0.20.2
(opam-v2.5.1); AppleClang 21.0.0…` — an upstream release, a commit, and the toolchain that built
it. That string cannot be produced by a WordPress deployer.

⭐ And write the failed attempt down. `profiles/rv64i-lab-v0/references.toml` carries an
`[[attempt]]` record for this collision with its `consequence`, so the next reader does not
rediscover it — `SRC-02` makes an honest "this route is wrong" a result, not an embarrassment.

Related: [[re-derivable-vs-cited-evidence]], [[self-test-arms-that-never-ran]].
