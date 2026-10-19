# Sealed history retrieval

Two finite immutable segments retain368 older CH/DEV shards. The first210 were
sealed at ff75610 on2026-10-08. LC0049 adds exactly158 closed shards from
a5bf45798255bca41d73f284bfe6987f48fc351f under the standing archive delegation.
Recent history stays in CHANGELOG.md, DEV_NOTES.md and new docs/changelog/ shards.
Existing objects and descriptors are immutable; another seal needs a new owned,
reviewed finite transition. The capacity authority is LC0049-CAPACITY in
`docs/tasks/artifacts/live-containment/task-claims.md`.

`docs/history/archives.json` pins each source revision, former names, source/member
counts, byte/line counts and SHA256 identities. Each content-addressed object under
`docs/history/sealed/` retains its original shards and source manifest. The
project owns retention through tracked bytes: ordinary/shallow clones need no
Git history, network access or extraction to recover the originals.

From the repository root:

```sh
python3 scripts/history_archive.py
python3 scripts/history_archive.py --read docs/changelog/shard-0001.md
python3 scripts/history_archive.py --read docs/changelog/shard-0366.md
bash scripts/check_changelog_shards.sh
```

The first command authenticates2 objects/368 shards. Read writes one original to
stdout after authenticating the whole terminal. Missing/corrupt objects, unknown
fields, unsafe names, duplicate/extra/missing members or oversized payloads refuse.
The freeze gate preserves committed descriptors and the complete live/archived
partition: every logical shard/entry appears once, prior manifest rows retain
identity, and retired shard numbers are never reused. Restore exact committed
objects/descriptors after corruption; never repin a changed source to bless it.

Ordinary tar also retrieves a member without extracting it to disk:

```sh
tar -xOf docs/history/sealed/89ad7214ebbf637cc48dc4468f3d43fb7d0f2eb08a43fa5c4ab42118ba8df2b5.tar.gz docs/changelog/shard-0366.md
```

The checked reader adds full identity, manifest and bounded-expansion checks.
Manifest snapshots have the same former logical filename at distinct capture
boundaries; retrieve each metadata snapshot with tar from its named segment.

| Segment | Original members incl. manifest | Source bytes | LF | Fixed object bytes |
| --- | --- | --- | --- | --- |
| ff75610 | 211 | 781740 | 9639 | 284500 |
| a5bf4579 | 159 | 782755 | 11200 | 276917 |

The finite terminal has exactly4 files. Its581897B ceiling is the two fixed
objects561417B plus the existing16384B index and4096B front-door bounds. All
reader resource limits and ordinary-history/head ceilings stay fixed. These
counts authorize this exact captured population only. The source proof checks
complete reconstruction separately from semantic closure, live dimensions and
unretained residue; no retired source bytes are unretained.
