# Sealed history retrieval

This finite archive terminal preserves the 210 older changelog/development-note shards
sealed at `ff75610`. The director approved the browsing change on 2026-10-08.
Recent history remains in CHANGELOG.md, DEV_NOTES.md and docs/changelog/. This terminal
accepts no new content in its existing object; another seal requires an owned transition.

The tracked descriptor `docs/history/archives.json` owns the source revision, former
paths, member counts, byte/line counts and SHA-256 identities. The content-addressed
object under `docs/history/sealed/` includes every original shard and its SHA manifest.
The project owns retention: these tracked bytes survive ordinary clones, including
shallow clones. Git history, an editor and network access are unnecessary for retrieval.

From the repository root:

```sh
python3 scripts/history_archive.py
python3 scripts/history_archive.py --read docs/changelog/shard-0001.md
bash scripts/check_changelog_shards.sh
```

The reader writes the requested original bytes to stdout. It authenticates the whole
terminal first and never extracts files to disk. A missing or corrupt object, unknown
field, unsafe path, duplicate member or oversized payload fails closed. The freeze gate
also rejects changes to committed descriptors. Restore the exact tracked object/descriptor from a known good commit;
do not rewrite a digest to bless changed history. The freeze gate also checks live and
archived headings together, preserving each entry exactly once and every predecessor
manifest row unchanged. Shard numbering includes retired names.

Ordinary tar tools can also retrieve a member from the object path listed in the
JSON descriptor (`tar -xOf OBJECT_PATH docs/changelog/shard-0001.md`). The checked reader
adds manifest and identity verification. For a filename search, inspect the archived
`docs/changelog/SHARDS.sha256` member. Whole-source reconstruction retains 211 members,
781,740 bytes and 9,639 lines; the immutable compressed object is 284,500 bytes.
