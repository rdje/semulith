# Finite P4 task-history seal — approved and implemented

- Type: `decision` (review retained below; director approval2026-10-10)
- Owner: `LIVE-CONTAINMENT.4` slice (b), `SEMULITH-LC-0005`
- Capture: `47cb4365b6b0ec38b76ac7863e3ad39eb82e3b1c`
- Decision needed: retain original historical narratives through a verified,
  tracked archive, with bounded navigation stubs at their existing Markdown paths.

The task family at the capture is89 files/3,145,153 B against3,145,728 B:575 B
of room. These are retained historical snapshots, growing with completed work.
The active P4 task still carries its full18-node graph and current evidence leaf.
A new ordinary slice would exhaust the aggregate; sharding alone does not remove
that scaling term. No existing ceiling is raised by this proposal.

## Director approval and implementation — 2026-10-10

The director authorized the task-history/archive decision and required signoff
quality. `LIVE-CONTAINMENT.4c` / `SEMULITH-LC-0006` implements this exact finite
capture. The original proposal below records the review boundary, including its
then-pending authorization; those historical statements do not describe now.

`docs/task-history/descriptor.json` and its immutable tracked object preserve all
12 originals and the exact manifest. The object is byte-identical to the reviewed
prototype.12 navigation pages total7,040B and retain all eight incoming anchors;
the five original consumer bodies need no seal-related rewrite. The task family
releases1,137,663B. TASK-HISTORY runs strict whole-terminal/retrieval/navigation
and predecessor checks unconditionally, with46 controls. Metadata and expansion
are bounded; unknown, unsafe, duplicate, corrupt or missing data refuses before
stdout. Project-owned retention works without Git history/network/extraction.
The three-file terminal has a387,317B ceiling (375,029object+8,192descriptor+
4,096front door), leaving all existing ceilings unchanged. Future seals require
their own owned finite transition. See `docs/task-history/README.md`.

The recipe below now retrieves each authenticated original through the checked
reader before repeating the reviewed serialization. It remains runnable after
migration; the archive does not depend on this recipe or the former live bodies.

## Concrete recommendation

Seal exactly the12 original files in the manifest below: the base P4 archive and
parts2–12, through closed .13. Keep the active tree, other task archives and
feature/model books directly readable. Preserve all original bytes in one immutable,
content-addressed object under a separately governed `docs/task-history/` finite
terminal; the existing three-file changelog terminal stays unchanged.

Replace these12 live historical narratives only after approval and a verified
migration with12 bounded navigation stubs at the same paths. The prototype stubs
total6,830 B and preserve the eight currently referenced anchors. They explain the
new read route rather than pretending to contain the old narrative. The task
family would shrink by1,137,873 B. Compression is storage, not authority to delete
unique evidence: every original remains retrievable by its logical filename.

The browsing change is specific: following an old link reaches a navigation
pointer; reading the full historical narrative uses the checked reader or ordinary
tar instead of opening the original Markdown body. This requires the director's
direction. It grants no CPU acceptance, requirement status or release credit.

## Verified prototype

- All12 working sources equal their captured Git blobs and SHA256/byte/line pins.
- Original source:1,144,703 B/15,055 lines. Manifest:2,418 B,
  SHA256 `63c450410ee2e1ca339d57970abf39214e49b7259ea6cd18b7c425718d0b6e89`.
- Thirteen archive members (12 originals plus manifest),1,147,121 B total source.
  USTAR:1,167,360 B; gzip:375,029 B, SHA256
  `892f5c98fb8567392fea2b0a615baab3bd2aa4a38768517e0f3c7b418887242d`.
- Two independent serializations are byte-identical. Every original was retrieved
  through both Python and `tar -xOf` and compared byte-for-byte.
- Four actual controls refuse outer corruption, a changed payload with unchanged
  manifest, an extra member, and an escaping/unknown logical read.
- Prototype and proposed stubs:
  `target/live-containment/task-history-review/`. No live archive was removed,
  replaced or edited. This is a retention/retrieval proof, not a production gate.

Example of the already-executed tool-neutral retrieval:

```sh
tar -xOf target/live-containment/task-history-review/892f5c98fb8567392fea2b0a615baab3bd2aa4a38768517e0f3c7b418887242d.tar.gz docs/tasks/archive/P4-SYSTEM-12.md
```

## Consumers and preservation

The tracked, project-owned text census found81 path/link records:54 inside the
capture and27 outside, across five external files. This is a reference census,
not81 distinct semantic dependencies. No literal book include consumes these files;
no maintained script, hook, registry or build names them as an input. The task-
acceptance gate explicitly excludes `docs/tasks/archive/` from live leaf checks.
The proposed migration must rerun this census against the then-current tree.

| External consumer | Records | Disposition |
| --- | --- | --- |
| `docs/book/src/plan/p4/contract-v2.md` | 2 | Existing paths lead to disclosed retrieval stubs. |
| `docs/book/src/working/task-trees.md` | 6 | Keep historical measurements; preserve destination paths. |
| `docs/changelog/shard-0221.md` | 1 | Immutable history: preserve bytes; its old path resolves to a stub. |
| `docs/tasks/P4-SYSTEM.md` | 16 | Keep active graph and paths; preserve requested section anchors. |
| `profiles/rv64gc-lab-v0/ENVIRONMENT.md` | 2 | Preserve source bytes/dossier identity; profile-progress anchor remains addressable. |

These consumers need no body rewrite when their paths/anchors are retained.
Current anchor obligations: part8 `profile-progress`; part11 `commits`,
`verification`; part12 `acceptance`, `changelog`, `commits`, `designs`,
`verification`. Each is backed by an original heading. Archived cross-links keep
their logical paths; retrieval of a different original uses the same reader.

## Migration contract after direction

Own one atomic transition under .4. Authenticate the exact sources again before
replacing any body; a changed source pauses that transition for review. Track the
object and strict immutable descriptor, plus a bounded retrieval front door, in
`docs/task-history/`. Register exactly that finite terminal with fixed measured
object identity, bounded metadata/navigation, and no permission for ordinary
appends or future seals. Do not expand the existing changelog terminal's contract.

The checked reader must work without Git/network/extraction, authenticate the
whole object and exact member census, enforce bounded decompression and safe
relative names, and refuse unknown/duplicate/missing members, malformed metadata,
changed source identities and unsafe reads. Freeze the captured descriptor/object;
restore exact committed bytes on corruption, never bless a replacement digest.
Retention is project-owned: the tracked object survives ordinary/shallow clones.

Generate and verify the bounded stubs with their original paths and required
anchors. Prove full original-source reconstruction, complete consumer resolution,
no include/build loss and unchanged active task graph. Re-derive all affected
size/count/link projections; run fail-closed controls and doctrine/books before
committing the atomic migration. Full containment-doctrine adoption remains .4
work; this finite transition cannot become an unrestricted overflow sink.

## Why direction is required

The read-only source guide is
`/Volumes/SSD/Documents/github/fsmgen/docs/LIVE_DOCUMENT_SIZE_CONTAINMENT_ADOPTION_GUIDE.md`,
Stop conditions: **“a lifecycle choice would change what users can directly browse”.**
Its Phase2 also requires utility/consumer classification, lossless retrieval and an
atomic migration. The2026-10-08 approval covered210 changelog shards only; it does
not authorize these task narratives. The guide was re-read in full for this review.

Alternative: keep direct narrative browsing and choose a different bounded
history lifecycle before resuming ordinary task growth. A larger cap is not a
solution demonstrated by these measurements. Until direction arrives, original
files remain intact; the completed registration is committed and independently
resumable. The next CPU work remains .14 structured experiments/policy/status/
mirror reconciliation after containment.

## Exact capture manifest

The JSON block is the exact2,418-byte manifest member, including its final newline.
It records historical identities, not a claim about mutable current state.

<!-- capture-manifest -->
```json
{
  "capture": "47cb4365b6b0ec38b76ac7863e3ad39eb82e3b1c",
  "kind": "task-history-review",
  "members": [
    {
      "bytes": 130981,
      "lines": 1913,
      "path": "docs/tasks/archive/P4-SYSTEM.md",
      "sha256": "9db47e0cd10192a7cc0d3924f9040800a0b955d3df45af4ab03ef467edc7613f"
    },
    {
      "bytes": 130753,
      "lines": 1409,
      "path": "docs/tasks/archive/P4-SYSTEM-2.md",
      "sha256": "b0f56d0f2fa83039612aeb1783e8ae6703ccc66bab1c8ddaaa6305afe6721a86"
    },
    {
      "bytes": 122822,
      "lines": 1511,
      "path": "docs/tasks/archive/P4-SYSTEM-3.md",
      "sha256": "e12f28829dfba58efd39a49343c1b8e89940749465e0a99ff35cfef400f0d4e6"
    },
    {
      "bytes": 55878,
      "lines": 843,
      "path": "docs/tasks/archive/P4-SYSTEM-4.md",
      "sha256": "4b90b92aa5359c7df69e816bfa3d35c13f2e0fd8726726e495e701ea1f27668a"
    },
    {
      "bytes": 63976,
      "lines": 801,
      "path": "docs/tasks/archive/P4-SYSTEM-5.md",
      "sha256": "c4f2a2ae013ac7f2f13f5508ed41d789d2d0dd82eb3957ebf2c24a9e0b87515e"
    },
    {
      "bytes": 127941,
      "lines": 1386,
      "path": "docs/tasks/archive/P4-SYSTEM-6.md",
      "sha256": "e289fa311bc5e9977dab62194c4773da03f7b62f734f88dea0a6f21fbb160e98"
    },
    {
      "bytes": 125771,
      "lines": 1792,
      "path": "docs/tasks/archive/P4-SYSTEM-7.md",
      "sha256": "ad336894f530fabc121b19e7b8b9ed68c62d01d32f5c89bbd714dc0a9deb3892"
    },
    {
      "bytes": 59436,
      "lines": 868,
      "path": "docs/tasks/archive/P4-SYSTEM-8.md",
      "sha256": "68fd32cfc36e8c341bcd0a251da3854e5e229d93a014e3f72c7687c9788e7375"
    },
    {
      "bytes": 83418,
      "lines": 1147,
      "path": "docs/tasks/archive/P4-SYSTEM-9.md",
      "sha256": "ad15045fe1549a1c0dc7b6950042ae68d2207dbe61943fcb989e046cb50ecb4e"
    },
    {
      "bytes": 81004,
      "lines": 1124,
      "path": "docs/tasks/archive/P4-SYSTEM-10.md",
      "sha256": "5e0f7eccbdd1f85707c66259ff78cb624b0b966894b97a2de074f4d73d9df310"
    },
    {
      "bytes": 84762,
      "lines": 1174,
      "path": "docs/tasks/archive/P4-SYSTEM-11.md",
      "sha256": "ee6d39437ea5a5ee5d3ea981665b486e3db29f68987f00faea04da9296ad8302"
    },
    {
      "bytes": 77961,
      "lines": 1087,
      "path": "docs/tasks/archive/P4-SYSTEM-12.md",
      "sha256": "c37126b4351abd7c78f119f223d3fbe78701bebc11c2d1df71f0ac3f4301b575"
    }
  ],
  "schema_version": 1
}
```

## Reproduce the review before migration

The originals are retained in the seal. The following checked recipe rebuilds the
exact artifact from this manifest on the repository volume (Python3.14.7,
zlib1.2.12). It needs neither a donor repository nor the previous scratch files.
USTAR members follow manifest order, then the manifest; mode0644 and all other
metadata zero/empty. Gzip level9/mtime0 has no source filename.

```python
from pathlib import Path
import gzip, hashlib, io, json, subprocess, sys, tarfile
p = Path("docs/decisions/decision_task-history-seal-review.md")
text = p.read_text()
manifest = text.split("<!-- capture-manifest -->\n```json\n", 1)[1].split("```", 1)[0].encode()
assert len(manifest) == 2418
assert hashlib.sha256(manifest).hexdigest() == "63c450410ee2e1ca339d57970abf39214e49b7259ea6cd18b7c425718d0b6e89"
items = []
for row in json.loads(manifest)["members"]:
    data = subprocess.check_output([sys.executable, "scripts/task_history_archive.py", "--read", row["path"]])
    assert len(data) == row["bytes"] and data.count(b"\n") == row["lines"]
    assert hashlib.sha256(data).hexdigest() == row["sha256"]
    items.append((row["path"], data))
items.append(("docs/history/task-history-manifest.json", manifest))
buffer = io.BytesIO()
with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
    for name, data in items:
        member = tarfile.TarInfo(name)
        member.size, member.mode, member.mtime = len(data), 0o644, 0
        member.uid = member.gid = 0
        member.uname = member.gname = ""
        archive.addfile(member, io.BytesIO(data))
blob = gzip.compress(buffer.getvalue(), compresslevel=9, mtime=0)
assert len(blob) == 375029
assert hashlib.sha256(blob).hexdigest() == "892f5c98fb8567392fea2b0a615baab3bd2aa4a38768517e0f3c7b418887242d"
output = Path("target/live-containment/task-history-review/reproduced.tar.gz")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_bytes(blob)
```

Verification: prototype/reproduction/consumer/negative controls/focused9 and
seven books rc=0, recorded by `SEMULITH-LC-0005`.
The review above was committed before direction; the dated approval now authorizes
the implemented finite migration. Full containment adoption remains open.
