# Preserve live append-history predecessors

- **Type:** `decision`
- **Date:** `2026-10-11`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a23–a25, `SEMULITH-P4-0214`–`0216`
answers: How are older live history entries preserved through sharding, and can restored working bytes conceal a staged edit?

## The measured defect

A23 caught an overbroad replacement changing two older receipt counts before its
commit landed. The manual predecessor inverse stopped that commit and restored
the originals. A25 reproduces both edits from5de7c27 in an owned fixture: the old
partition judge reports240 frozen rows and rc0. It authenticates shards/manifests
and checks heading uniqueness, but does not compare old live entry bodies.

## The contract

SHARD-FREEZE now also invokes history_predecessor.py. It reads a closed HEAD and
index inventory through Git, then immutable blob IDs. A failed Git read refuses;
only absence from a successful inventory establishes absence. Working reads stay
on the project volume, outside symlinks/nested Git boundaries. Each snapshot is
bounded to8MiB/1024 paths; Git sizes are checked before payload reads, and working reads use
at most one extra sentinel byte to detect overflow. Temporary snapshots live under
target/history-predecessor and are removed, without creating another Git repository.

The pure history_entries module owns the shared splitter, wrapper, ceiling reader
and exception; the published sharder re-exports the same names. For each old head,
its preamble stays exact. Current entries followed by new shards in reverse numeric
creation order must end in every complete predecessor entry, with exact bytes and
order. New whole entries may precede them, including corrections. New shards must
have the published name/wrapper, registered digest and declared head. Missing,
changed, duplicated or reordered old records refuse; no old claim is silently edited.

Both the staged and working head views undergo this proof. The complete staged
manifest, shards and sealed inputs also run through the existing partition judge
in a disposable snapshot. Restoring working bytes cannot conceal a staged history
edit. The existing working-corpus archive/freeze checks and31 controls remain intact.
This is preservation and authentication; neither establishes that old prose is true.

## Verification and limits

38 controls pass normally and optimized. Five independent omissions lose17/1/2/2/1
assertions in both modes: predecessor, order, staged partition, Git errors and shard
wrapper. Public-sharder integration passes. The actual a24 transition reconstructs
both entire sources from f40ece2; two retained count edits and one moved receipt edit
with an updated digest still refuse. The real production guard reads97 complete
predecessor entries in each of the two-head index/working views at d8083a9.

An initial fixture omitted its allocated scratch parent (three errors); correct the
fixture before accepting results. The actual-transition instrument also assumed the
old notes count was in shard0239; inspect the committed source, test that count in
its retained head and separately mutate a real moved rc field. No production history
was changed by either failed instrument. Earlier archives, seals and caps remain exact.

Final review also reproduced an import-time Git read outside refusal handling.
Extract six shared definitions/constants unchanged; all remaining sharder definition
ASTs stay exact. A fresh-process no-Git import control now passes. Sharder output,
public aliases and the actual partition inverse remain unchanged.
