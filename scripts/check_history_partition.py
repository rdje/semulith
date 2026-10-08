#!/usr/bin/env python3
"""Judge the logical live/archived history partition; invoked by SHARD-FREEZE."""
import hashlib, re, sys, pathlib
from history_archive import ArchiveRefused, load_archives

# Arguments: previous archive index (or empty), root, live directory/manifest,
# previous live manifest (or empty), then the independent live heads.
previous_index = pathlib.Path(sys.argv[1]) if sys.argv[1] else None
root = pathlib.Path(sys.argv[2])
shard_rel, manifest_rel, prev_path = sys.argv[3:6]
heads = [root / h for h in sys.argv[6:]]
shard_dir = root / shard_rel
manifest = root / manifest_rel
findings = []


ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>\S+)$")
ENTRY = re.compile(r"^## (.+)$", re.M)

shards = sorted(shard_dir.glob("*.md")) if shard_dir.is_dir() else []
try:
    archive_records, archived = load_archives(root, previous_index)
except (ArchiveRefused, OSError) as exc:
    print(f"ARCHIVE REFUSED {exc}")
    print("__CHECKED__ 0")
    sys.exit(1)

rows: list[tuple[str, str, int]] = []           # (digest, path, lineno)
if manifest.is_file():
    for n, line in enumerate(manifest.read_text().splitlines(), 1):
        if not line.strip():
            continue
        m = ROW.match(line)
        if not m:
            findings.append(f"MALFORMED  {manifest_rel}:{n}: not a sha256sum row — "
                            f"'{line}' — the manifest is data, not prose")
            continue
        rows.append((m.group("digest"), m.group("path"), n))

if not shards and not rows and not archived:
    print(f"NO SHARDS  {shard_rel} holds no shard and {manifest_rel} no rows — "
          f"a freeze check with nothing frozen cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

for rel, (sha, blob) in archived.items():
    if any(path == rel for _, path, _ in rows) or (root / rel).exists():
        findings.append(f"DUPLICATE ARCHIVED PATH {rel}: logical history must exist exactly once")

# 1. COVERAGE ----------------------------------------------------------------------
by_path = {}
for digest, rel, n in rows:
    by_path.setdefault(rel, []).append((digest, n))
for rel, dups in sorted(by_path.items()):
    if len(dups) > 1:
        findings.append(f"DUPLICATE ROW {manifest_rel}: '{rel}' is manifested "
                        f"{len(dups)} times (lines {[n for _, n in dups]})")
for p in shards:
    rel = p.relative_to(root).as_posix()
    if rel not in by_path:
        findings.append(f"UNMANIFESTED {rel}: a shard with no manifest row is frozen by nobody")
for rel, entries in sorted(by_path.items()):
    p = root / rel
    if not p.is_file():
        findings.append(f"MISSING     {rel}: manifested but does not exist")
    elif p.parent != shard_dir:
        findings.append(f"NOT A SHARD {rel}: the manifest may only freeze *.md files directly "
                        f"under {shard_rel}/ — {rel} escapes the partition")
    elif p not in shards:
        findings.append(f"NOT A SHARD {rel}: manifested but is not a *.md shard")

# 2. FROZEN ------------------------------------------------------------------------
for digest, rel, n in rows:
    p = root / rel
    if p.is_file() and p.parent == shard_dir:
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != digest:
            findings.append(f"THAWED      {rel}: the shard changed after the shard event — "
                            f"manifest {digest[:12]}…, file {actual[:12]}… "
                            f"(manifest line {n}). Entries in a shard are never edited")

# 3. APPEND-ONLY -------------------------------------------------------------------
if prev_path:
    prev = pathlib.Path(prev_path)
    if prev.is_file():
        current = {rel: sha for rel, (sha, _) in archived.items()}
        for digest, rel, n in rows:
            current[rel] = digest
        for line in prev.read_text().splitlines():
            m = ROW.match(line)
            if not m:
                continue
            rel, digest = m.group("path"), m.group("digest")
            if rel not in current:
                findings.append(f"REMOVED ROW {rel}: a manifest row committed at HEAD is gone — "
                                f"the manifest only grows, history is never rewritten")
            elif current[rel] != digest:
                findings.append(f"MODIFIED ROW {rel}: the manifest row changed after being "
                                f"committed — frozen means frozen, including the manifest")

# 4. UNIQUE ------------------------------------------------------------------------
seen: dict[str, str] = {}
for label, (_, blob) in archived.items():
    for eid in ENTRY.findall(blob.decode('utf-8')):
        if eid in seen:
            findings.append(f"DUPLICATED ENTRY '{eid}': archived history repeats {seen[eid]} and {label}")
        else:
            seen[eid] = label
for label, path in [(h.name, h) for h in heads] + [(p.name, p) for p in shards]:
    if not path.is_file():
        continue
    for eid in ENTRY.findall(path.read_text()):
        if eid in seen:
            findings.append(f"DUPLICATED ENTRY '{eid}': appears in both {seen[eid]} and "
                            f"{label} — the partition must hold every entry exactly once")
        else:
            seen[eid] = label

for f in findings:
    print(f)
print(f"__CHECKED__ {len(rows) + len(archived)}")
sys.exit(1 if findings else 0)
