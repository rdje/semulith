# CHANGELOG shard — _(2026-09-14)_ … _(2026-09-14)_

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-14)_ — availability is not identity, and a budget can be wrong in your favour

- ⛔ **The package manager had a formula called `sail`. It deploys WordPress sites to
  DigitalOcean.** An exact name collision with the Sail ISA specification language: the lookup
  succeeded, the version was current, the licence was real, and the referent was wrong. Had the
  check been `brew info sail >/dev/null && echo available`, the dossier would carry a sentence
  that is false, sourced and reproducible. Identity needs a field only the real thing can
  produce — here `--build-info`, which prints an upstream release, a git sha and the compiler.
  Promoted: [`docs/knowledge/availability-is-not-identity.md`](docs/knowledge/availability-is-not-identity.md).
- The roadmap priced reference acquisition as the first activity whose cost was *not obviously
  bounded*, assuming an OCaml/opam build of Sail. Release 0.14 ships a native binary for this
  host's architecture, so Sail was the **cheapest** candidate, not the dearest. Three models
  obtained in one leaf. The estimate was wrong; the reasoning behind it ("acquisition is work
  with observable outcomes") was right and is untouched.
- ⛔ **The Sail model will not tell you what configuration it ran with.**
  `--print-default-config` ignores `--config-override` — byte-identical dumps. `EVIDENCE_AND_GATES`
  §5 wants the *effective* configuration, so it is recorded as (default) + (tracked override)
  with the merge explicitly labelled **ours**. The model's one self-description is
  `--print-isa-string`, which is why `rv64i_zvl32b` is pinned and re-derived.
- Having three binaries is not having three opinions. The gate now refuses a candidate whose
  `lineage` field is missing, because an unasked independence question reads exactly like an
  answered one.

