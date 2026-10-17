# Closed qualification history

Transition under `LIVE-CONTAINMENT.4i2b5b1h / SEMULITH-LC-0041`.

Authority: the director's standing session instruction, “do whatever you see fit
regarding the task history or archive”, with signoff and production quality required.
This finite selection implements that delegation; it grants no blanket overflow sink.

Source `968bc0109682628609ae6b83bc7bf42b01fc9b2c` supplies four completed,
source-pinned qualification records (481,178 bytes): book-index consumer,
graph/query census, include/navigation readers and orientation indexes. Their
closed captures cover LC0023/28/32–39. They are historical measurements, not the
current inventory contract or a maintained product specification. The inventory
contract and live retention-verifier inputs remain ordinary Markdown.

The complete pre-transition `docs/book/src/working/task-trees.md` is also retained
as an unexpanded source snapshot. Its current native successor stays live.
These five originals total 497,850 bytes. Collection ordering and every original
byte, Git mode and identity are preserved; no result is summarized away.

From the repository root:

```sh
python3 scripts/qualification_history_archive.py
python3 scripts/qualification_history_archive.py --list
python3 scripts/qualification_history_archive.py --read docs/tasks/artifacts/live-containment/include-readers.md
python3 scripts/qualification_history_archive.py --read docs/book/src/working/task-trees.md
python3 scripts/qualification_history_preservation.py
python3 scripts/probe_qualification_history.py
```

The reader authenticates the descriptor, object, manifest, all originals and
four navigation pages before printing an original. README mode/size/coverage
are checked; the publishing guard freezes its content in both views. It uses the standard library and this project's
shared archive codecs, without Git, network or filesystem extraction. Ordinary
and shallow clones containing the transition retain the tracked object. Replaying
the historical qualifications still requires their declared sources/producers;
archiving their Markdown does not add a toolchain or raw-output retention promise.

`descriptor.json` names the exact capture, five logical originals, source counts,
content-addressed object, canonical manifest and original heading aliases. The
`original_path` field names historical members rather than live file pins. The
original artifact paths become navigation pages; the book snapshot has no stub.
Public tar also retrieves originals: `tar -xOf OBJECT_PATH LOGICAL_PATH`, using
the object path in the descriptor. The checked reader additionally verifies all
metadata, identities, modes, canonical encoding, bounded decompression and views.

This terminal is immutable. Missing/corrupt inputs, unsafe or unknown members,
changed descriptors/navigation and excess metadata fail closed. Restore exact
committed bytes; changing a digest to bless changed history is refused by the
publishing guard. Corrections belong in new records. Another capture requires
its own owned authority and transition. Existing capacities remain fixed.

Reproduce the captured serialization without writing or extracting files:

```sh
python3 - <<'PY'
import gzip,io,json,sys
sys.path.insert(0,'scripts')
import qualification_history_archive as A
row,originals=A.load_terminal(A.PROJECT)
manifest={'schema_version':1,'kind':'qualification-history-source',
          'source':row['source'],'source_tree_sha256':row['source_tree_sha256'],
          'members':row['members']}
encoded=(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
raw=A.T.canonical_tar([*originals.items(),(A.MANIFEST,encoded)])
buffer=io.BytesIO()
with gzip.GzipFile(fileobj=buffer,mode='wb',filename='',mtime=0,compresslevel=9) as stream:
    stream.write(raw)
A.require(A.digest(buffer.getvalue())==row['sha256'],'serialization differs')
print(row['sha256'])
PY
```
