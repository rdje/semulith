# Include guard integration — LC.4i2b3b2

Owner: LIVE-CONTAINMENT.4i2b3b2 / SEMULITH-LC-0030.
Source: aacaee98b02292bfcee8f139fad28530bcfe4e95.
D65 and D68 fixed by the verified integration; normal COMMIT closes the work unit.
LC0029 component/replay: docs/tasks/artifacts/live-containment/include-source-validator.md.

## Retained complete closed book receipts

Each complete span below preserves its original bytes and source route. Earlier
ordinary task archives and sealed history remain byte/mode exact. Current generic
whole-entry/byte-count explanations and commands remain in the book. This retention
grants no new archive seal, capacity, processor or adoption authority.

<!-- LC0030 history-window -->
````text
Completed development notes move as whole entries into authenticated history
shards; their contents are retained, not summarized away. P4.13 c22a moved seven
older entries from a 47,462-byte live head, leaving thirteen entries / 31,228 bytes
before the new receipt. Removing only that new receipt and navigation footer,
then concatenating the live prefix and archived suffix, reconstructs the original
bytes and entry order exactly. The owning task records source/suffix SHA256 and
lengths. The frozen manifest gains one row; earlier rows and sealed history remain
unchanged. The 48 KiB live ceiling stays fixed, and the book retains the worked
feature examples independently of the session notes.

The complete P4.13 c26a/c28a book receipts remain in ordinary archive14;
read them through the commands below. Current partition rules remain above.

The whole P4.13 c29b1 append-history receipt is retained in
[archive 13](#read-task-history).

P4.14 a42l1 retains four completed workflow designs and three whole book
receipt spans in ordinary part19. Complete source inverses preserve each byte;
active a42/a42l and current explanations stay live. Read the records below.

````
<!-- LC0030 end history-window -->

<!-- LC0030 task-and-dev -->
````text
The complete c29e1/c33c task and DEV partition receipts are retained in
ordinary part19. They include source identities and all inverse/control
measurements. Earlier archives remain immutable.

````
<!-- LC0030 end task-and-dev -->

<!-- LC0030 book-and-dev -->
````text
Ordinary part19 retains the complete c30b/c33d book and DEV partition
receipts, including source identities and measured inverses. Current
feature explanations and examples remain in their chapters.

````
<!-- LC0030 end book-and-dev -->

<!-- LC0030 byte-measurement -->
````text
Size claims use encoded file bytes. At the c29d1 diagnostic, the index generator
reported 23,612 "bytes" for a file containing 24,064 bytes: it had counted Python
characters, which omit UTF-8's extra bytes for non-ASCII text. The generator now
reports the written file's `stat().st_size`. Its output bytes and 40 indexed terms
are unchanged, and `--check` still succeeds quietly. The byte-count assertion
fails on the old message and passes after the reporting-only correction.
Containment and inverse proofs measure actual bytes throughout; a character
count cannot establish available space under a byte cap.


````
<!-- LC0030 end byte-measurement -->

## Integration contract and boundaries

The public `python3 scripts/unit_books.py CORPUS_ROOT` and
`bash scripts/check_unit_books.sh` force the owned validator before links for
every project/unit build, including scratch configurations. The injected
command/root derive from the current repository; caller command, ordering,
renderer and optional overrides cannot silently disable the check. Seven
default book.toml files declare mandatory HTML source checking before links.
Unit configs use `../../../scripts/book_includes.py`; the main config uses
`../../scripts/book_includes.py`. Persisted paths remain relative.

book_includes.py is the transport authority: one exact
`BOOK-INCLUDES: checked N chapters / M include edges` line witnesses success.
Missing/ambiguous success, unavailable/invalid protocol metadata and a named
source processor launch/JSON failure refuse2. `BOOK-INCLUDES: REFUSED — `
preserves source refusal2 across mdbook's101 status;
`BOOK-INCLUDES: DEFECT — ` identifies source defect1. Ordinary malformed TOML
remains build-defect1. The source/selector/stdout/unchanged-book contract from
LC0029 is retained. Navigation, remote availability, chapter completeness,
prose truth, full graph/lifecycle adoption and processor acceptance remain
separate claims.

Public installed mdbook0.5.4: twelve controlled builds per mode show that a
supports rejection or missing Python script without explicit renderers can
leave build0. Explicit HTML renderers force JSON invocation; missing script,
component exits1/2 and bad JSON stop101. This is an observed integration
contract, not a native tool defect. Read-only operating-system/toolchain
executables (Python, Bash, Git and mdbook on PATH) are necessary external
inputs; all project-owned copies, outputs, temporary files and evidence stay
under repository-derived target paths. Historical replay requires the named
local Git objects and current public toolchain; unavailable objects refuse
without fetching. No historical toolchain/output retention is promised.
Gitlinks remain unmaterialized and opaque; no other repository is written.

## Reproduction and measured results

The tracked producer `scripts/qualify_include_guard.py` owns all eight modes.
Use fresh target directories. On an uncommitted reproduction, declare every
owned untracked input with `--addition PATH`; committed inputs need none.
Commands below execute both modes and retain raw streams, complete physical/
index/mode inventories, reports, output identities and typed results.

```sh
for mode in protocol original public faults books omissions concurrency original-concurrency; do
  python3 scripts/qualify_include_guard.py --mode "$mode" \
    --output "target/live-containment/include-integration-replay/$mode"
  python3 -O scripts/qualify_include_guard.py --mode "$mode" \
    --output "target/live-containment/include-integration-replay/$mode-O"
done
```

- Original immutable aacaee98: seven cases × CLI/shell × normal/O =28
  evaluations, all0;24 are bad missing-file/absent-anchor/duplicate-anchor
  cases, four are valid selected-anchor controls. Copied regular bytes/modes
  remain exact; no Git init/fetch or submodule implementation access.
- Repaired public matrix: eleven cases × two interfaces × two modes =44:
  the same24 defects return1,16 invalid-UTF8/symlink inputs refuse2, four
  valid cases remain0. Both project and unit books are exercised.
- Actual source faults: chapter/include × read/change × CLI/shell × two
  modes =16 refusal2, each with exactly one injection. Restore the fixture
  before each interface; failed self-tests cannot stand in for injected faults.
- Default book mode: seven books,93 complete chapters,49 include edges;
  all344 output files and every complete expanded book object match an
  independent pass-through build. The default leg does not override source-check
  command/order/renderer. Normal/O full raw/expanded objects, input reports and
  output populations agree. Validating unchanged inputs adds no rendered bytes.
- Three actual guard omissions per mode fail1; removing before-links ordering,
  HTML renderer or processor from copied actual default configuration refuses2
  against independently captured pre-expansion inputs. Syntax/import failures
  are not accepted as guard discrimination.
- D68: the old fresh/removal probe compared the complete shared bundle directory
  across a build. Eight concurrent shell invocations can see peers allocate or
  remove their own healthy bundles. The published immutable runs reproduce15
  failures/one pass across16 shells; an earlier run failed all16. This variation
  is scheduling, not a source-verdict change. The repaired probe records only
  its own real allocated directory, asserts its removal, and retains fresh-output
  assertions. Both published eight-way runs pass all16 shells. This is finite
  concurrency evidence; absence of scheduling coverage would refuse qualification.
- All old23 unit/26 navigation/22 component methods remain. The stale-success
  mock supplies a source witness to keep isolating missing fresh output; D68
  scopes cleanup observation to its invocation. Seven integration methods give
  52 aggregate methods normal/O. Six new static source controls make22 shell
  arms; actual `check_derived_counts.sh --list` re-derives1571 project arms.
- Legacy tracked qualify_book_includes.py replay still re-emits the exact80700B
  LC0028 ledger in both modes: SHA256
  b4be9b9a4d1896f8439b94f2bf0b820b3d98f3a6758d805668407c960cc3cda5.

Initial integration fixture failures modified models.md while that probe's
SUMMARY selected intro.md. Actual chapter capture isolated the mistake; fixtures
were corrected before verification. The immutable original U gives51 methods/
13 failures/eight errors with those corrected controls; the repaired code passes.
The final seventh method additionally qualifies unavailable/invalid metadata.
Initial concurrent failures were traced to D68, logged/owned and repaired;
serialized green runs alone were not accepted as the solution.

## Whole source inverse

Four complete spans above retain2180B before replacement. The retained proposal
is15806B; final source teaching yields15882B from the original16897B. Reverse
the teaching seams in reverse order, authenticate that whole retained proposal,
then replace mapped spans in descending proposed offset with their authenticated
payloads. Require the exact original length/digest and immutable source equality.
Missing/changed payload, replacement or final-source bytes must fail. No current
heading/example is removed. Whole CH/DEV suffixes use the published sharder and
combined predecessor/index guards; old106 entries/order and all earlier
archives/seals remain byte/mode exact. Main book family524281→523499B: main
config+137, doctrine+96, task teaching/retention−1015. The six unit configs add840B
outside this family. No ceiling, health, archive or milestone authority changes.

```json
{
  "source": "docs/book/src/working/task-trees.md",
  "source_commit": "aacaee98b02292bfcee8f139fad28530bcfe4e95",
  "source_bytes": 16897,
  "source_sha256": "3dd9d8e07ced05dea99c4e41c58b0d244751e0d4fe92b596ebe6aae24412b6d1",
  "proposed_bytes": 15806,
  "proposed_sha256": "6da155238dc72fae0e82d99da6b26a6de21484a1009121894261a9fd8e91679f",
  "book_delta": -1091,
  "spans": [
    {
      "label": "history-window",
      "source_offset": 5707,
      "payload_bytes": 1173,
      "payload_sha256": "8dbb2200125ef8da1fa061d8f9f59a72afb73d7bdfb243fec56b46591be460b3",
      "replacement": "Completed development notes move as whole entries into authenticated history\nshards. Remove the new live receipt/footer and concatenate the retained live\nprefix and archived suffix to reconstruct the original bytes and entry order.\nThe manifest gains rows; earlier rows and sealed history remain immutable.\nThe 48 KiB ceiling stays fixed; current worked feature examples stay in the book.\nComplete c22a/c26a/c28a/c29b1/a42l1 receipts and source inverses are retained:\n\n```sh\ncat docs/tasks/artifacts/live-containment/include-source-integration.md\n```\n\n",
      "proposed_offset": 5707
    },
    {
      "label": "task-and-dev",
      "source_offset": 9051,
      "payload_bytes": 194,
      "payload_sha256": "093e7033f8840c7b976d682922cf495d459631bc10f6842d4f2b7db898ff536a",
      "replacement": "Read the complete c29e1/c33c receipts in the retained record above.\nEarlier archives remain immutable.\n\n",
      "proposed_offset": 8430
    },
    {
      "label": "book-and-dev",
      "source_offset": 9310,
      "payload_bytes": 200,
      "payload_sha256": "a5467d7d82e1092c59ceb6795b953b53d8d1b3d0798bde4a167d7924d9252ef5",
      "replacement": "The retained record preserves the complete c30b/c33d receipt and source route.\nCurrent feature explanations and examples remain in their chapters.\n\n",
      "proposed_offset": 8599
    },
    {
      "label": "byte-measurement",
      "source_offset": 9553,
      "payload_bytes": 613,
      "payload_sha256": "f32065d42ae93e607bcf3828ee8059c5e927429b4c9895302348623d39ed157b",
      "replacement": "Measure `len(text.encode(\"utf-8\"))` or the written file's `stat().st_size`,\nnot character count: `\"\u00e9\"` is one character but two UTF-8 bytes.\nLimits, available-space calculations and inverses use actual bytes.\nThe retained record above includes the complete c29d1 diagnostic receipt.\n\n",
      "proposed_offset": 8790
    }
  ],
  "teaching_seams": [
    {
      "path": "docs/book/src/working/task-trees.md",
      "old": "D65: missing/duplicate includes pass UNIT-BOOKS; repair before signoff.",
      "new": "D65 repair: UNIT-BOOKS rejects missing/ambiguous includes before expansion."
    },
    {
      "path": "docs/book/src/working/task-trees.md",
      "old": "**Include source validation (component).**",
      "new": "**Include source validation.**"
    },
    {
      "path": "docs/book/src/working/task-trees.md",
      "old": "From the repository root, qualify controls and opt into the project-book check:\n\n```sh\npython3 scripts/probe_book_includes.py\npython3 -O scripts/probe_book_includes.py\nMDBOOK_PREPROCESSOR__SOURCE_CHECK__COMMAND='python3 ../../scripts/book_includes.py' \\\nMDBOOK_PREPROCESSOR__SOURCE_CHECK__BEFORE='[\"links\"]' \\\nmdbook build docs/book\n```\n\nDefault UNIT-BOOKS still needs LC0030 integration; D65 remains open.",
      "new": "All seven books validate before links by default. UNIT-BOOKS forces validation\neven for scratch configurations, requires an execution witness and preserves\nsource refusal2. Missing files/anchors and duplicate anchors fail1. From root:\n\n```sh\npython3 scripts/probe_book_includes.py\npython3 -O scripts/probe_book_includes.py\nbash scripts/check_unit_books.sh\nmake book\n```\n\nReplay public/default qualification:\n\n```sh\ncat docs/tasks/artifacts/live-containment/include-source-integration.md\n```"
    }
  ],
  "final_proposed_bytes": 15882,
  "final_proposed_sha256": "2d7341092bf7dfda4d8ce710d69dafb547042cc7564948a65d3a65f42f57babf",
  "final_book_delta": -1015
}
```

## Qualified code/configuration identities

```json
[
  {
    "path": "scripts/unit_books.py",
    "bytes": 10884,
    "sha256": "4a30f679d32f86e83dc6a92dd5fca4dd3fa42fa444d3974b89ef59826927acdb",
    "mode": "0o644"
  },
  {
    "path": "scripts/book_includes.py",
    "bytes": 13638,
    "sha256": "9a5f1153379b86bbed6bfe93abe80abcecf80fce08daa8eab8c9ede54cbeb154",
    "mode": "0o644"
  },
  {
    "path": "scripts/probe_unit_books.py",
    "bytes": 17133,
    "sha256": "836cfebf5ccf708b24e9b868bcb3453bb7cbc5e5f1de2009dbf3ac30dcdbe132",
    "mode": "0o644"
  },
  {
    "path": "scripts/probe_book_includes.py",
    "bytes": 15079,
    "sha256": "86d760c3cc8aa4408d0aa17bc8232f9f086d225a7d59855a67c4e37edb6d7ce2",
    "mode": "0o644"
  },
  {
    "path": "scripts/check_unit_books.sh",
    "bytes": 7976,
    "sha256": "a03a58746f76b0528f549fff236a1e18a02e19932a7207850a0298dd5b0435e5",
    "mode": "0o755"
  },
  {
    "path": "scripts/qualify_include_guard.py",
    "bytes": 23007,
    "sha256": "1242bd019a7a975c53bd2cd23dfdfacc42cf91d1a2c8d7975e2e29f845560f1e",
    "mode": "0o644"
  },
  {
    "path": "scripts/check_doctrines.project.sh",
    "bytes": 14912,
    "sha256": "5355fe8810b8eb0007afc574c2af2c2ceb71d72efbfdff5acf57b7f9f2b369de",
    "mode": "0o755"
  },
  {
    "path": "docs/book/book.toml",
    "bytes": 575,
    "sha256": "fc170c2572571723c8ffa9214ea88cbc304f2d03d00c5ee7c03ff8862396229b",
    "mode": "0o644"
  },
  {
    "path": "docs/models/rv64i-lab-v0/book.toml",
    "bytes": 621,
    "sha256": "49bd7843706002593a8668fe03cd50f15da3363d8fb69e34748d1e77caecefa8",
    "mode": "0o644"
  },
  {
    "path": "docs/models/dsp56300-lab-v0/book.toml",
    "bytes": 661,
    "sha256": "a55803a07d011df196b95bc86ac540a72bf6a98402fe784aedfead2cf07817cf",
    "mode": "0o644"
  },
  {
    "path": "docs/models/netboard-lab-v0/book.toml",
    "bytes": 640,
    "sha256": "39797d121f73d5a2e43d292bde8ed3e60f371261520fa7d02f7827275311aa7b",
    "mode": "0o644"
  },
  {
    "path": "docs/models/sifive-uart-lab-v0/book.toml",
    "bytes": 636,
    "sha256": "d9c7361ac2f3c47a80e286c92fd925f4e4b558f016437c212904d84a6531c458",
    "mode": "0o644"
  },
  {
    "path": "docs/models/lan9118-lab-v0/book.toml",
    "bytes": 648,
    "sha256": "4745e4ff072a2b8b747d4c34dec9cf5e7b11dc16205742047fcc99bd66e5432b",
    "mode": "0o644"
  },
  {
    "path": "docs/models/rv64gc-lab-v0/book.toml",
    "bytes": 601,
    "sha256": "19b89cbdf392aa078ff84ed6f2143468448c1ae2abc60f374d30ceb1d6c91848",
    "mode": "0o644"
  }
]
```

## Actual qualification result/input identities

These generated files are disposable evidence at the named invocation boundary;
the tracked recipes reproduce them. The complete before/after inventories match
for all1434 immutable members plus the two declared additions. Subsequent owned
publication notes/history moves are checked separately before commit. These pins
do not promise byte-stable absolute diagnostic paths between relocated runs.

```json
[
  {
    "path": "target/live-containment/include-source-integration/published-protocol/result.json",
    "bytes": 2828,
    "sha256": "f542718bba3a22275310abbc74415881f4864a6051d5cd8925e206159d27446d"
  },
  {
    "path": "target/live-containment/include-source-integration/published-protocol/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-protocol-O/result.json",
    "bytes": 2831,
    "sha256": "1d1d61a601f672ffad1170bac822665abef6ae856271a92a9e033268bf7e0f4d"
  },
  {
    "path": "target/live-containment/include-source-integration/published-protocol-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original/result.json",
    "bytes": 2189,
    "sha256": "a671355f35c252785ceccfdee1d1fff503bdb8d32e631b74992a3a743fcbcc70"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original-O/result.json",
    "bytes": 2192,
    "sha256": "b35f37ae5a00c9f4569751434087285556990c8968f732be0e5b6470d22f77e9"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-public/result.json",
    "bytes": 3320,
    "sha256": "be626f67d673b1f50992f3172ebf6f315c0d134a5cfc9d5ecd1dfdffb90ac9b3"
  },
  {
    "path": "target/live-containment/include-source-integration/published-public/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-public-O/result.json",
    "bytes": 3323,
    "sha256": "c84f992ac4f5db82f2957446d38fcb8cdec5704ef339ab4c3159adf3b103a08a"
  },
  {
    "path": "target/live-containment/include-source-integration/published-public-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-faults/result.json",
    "bytes": 1124,
    "sha256": "3fde60a5da008b58d37d7e65e856550ccb380db01b2c7c918aeddff162e19e66"
  },
  {
    "path": "target/live-containment/include-source-integration/published-faults/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-faults-O/result.json",
    "bytes": 1127,
    "sha256": "8a993c045d3f5dd73e086e88dd34f5c62ce2f6a977fb39b6e8d2770c93101d1c"
  },
  {
    "path": "target/live-containment/include-source-integration/published-faults-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-books/result.json",
    "bytes": 352,
    "sha256": "e2ec7f0bf75d3dde20841d454a4f968c203d184a6bbda84604165b3fefe17637"
  },
  {
    "path": "target/live-containment/include-source-integration/published-books/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-books-O/result.json",
    "bytes": 355,
    "sha256": "26daa2f706f7756ee080ea0c65aa2ea8c4db25ecb53512c1bfb7ffb5eaf014b7"
  },
  {
    "path": "target/live-containment/include-source-integration/published-books-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-omissions/result.json",
    "bytes": 1306,
    "sha256": "43d33f85b81767e095df13d40b4bfbd6a4ffd8dd577d50ded1239f6b6ed33f8e"
  },
  {
    "path": "target/live-containment/include-source-integration/published-omissions/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-omissions-O/result.json",
    "bytes": 1309,
    "sha256": "96320ea01d21ec0b9915b4691f4c008b0b3f20ded56c340e1d8bbcd5eecc5ac7"
  },
  {
    "path": "target/live-containment/include-source-integration/published-omissions-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-concurrency/result.json",
    "bytes": 1811,
    "sha256": "c19fb9e3436570444b8b4e127258ebf867a855dd20be52cef361ab904bb594a6"
  },
  {
    "path": "target/live-containment/include-source-integration/published-concurrency/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-concurrency-O/result.json",
    "bytes": 1814,
    "sha256": "4eb900634dc0fba155ec19e906d1bf8a6672f58432cc6151229d49a4754602bd"
  },
  {
    "path": "target/live-containment/include-source-integration/published-concurrency-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original-concurrency/result.json",
    "bytes": 1844,
    "sha256": "bdeedea3c618af7f004c365aaac1021431ffbe9acbe553fa5aeff6e990864f76"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original-concurrency/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original-concurrency-O/result.json",
    "bytes": 1847,
    "sha256": "b53b2bd326d8dffe6ec61920985f6d3d2b4ee36f7b06bd53a6ea3068b8a63d01"
  },
  {
    "path": "target/live-containment/include-source-integration/published-original-concurrency-O/working-before.json",
    "bytes": 260167,
    "sha256": "fd9d15bc1f9e4ddd5e236056864a3dac889518521fb26a35a59e6071409d3ab4"
  }
]
```

## Historical calibration-count correction — D70

Five LC0027/28/29 receipts in LIVE-CONTAINMENT.md called the scaffold subset
24 tests. Their actual --only-scaffold logs report5; the protected source
contains five Scaffold methods. The full public suite adds19 Census methods
(11 declared plus eight generated ps/lsof failure methods), yielding24.
Those original subset invocations qualify five per mode; historical bytes
are preserved with this explicit correction. LC0030 reruns both commands
normal/O: subset5/0 and full24/0. Reproduce from the repository root:

```sh
python3 scripts/probe_handoff_census.py --only-scaffold
python3 -O scripts/probe_handoff_census.py --only-scaffold
python3 scripts/probe_handoff_census.py
python3 -O scripts/probe_handoff_census.py
```

## Chapter contents assessment — LC0040

Owner: LIVE-CONTAINMENT.4i2b5b1. Source718bbd9/1466 identities;107 SUMMARY,
configuration and chapter pins. All93 chapters/seven parts match independent
plain-label SUMMARY hierarchy, paths, numbering and labels in complete protocol
metadata and both generated forms:14 TOCs. All344 outputs are capture-exact
normal/O. Three supported SUMMARY controls remove/rename/unnest a chapter;
each native build succeeds0 and fails the original complete contract1. These
are configuration controls, not mdBook defects. All330 other outputs and
runtime page headings/search/resources remain open; no browser/adoption or
processor acceptance claim. Original source copies/modes/index stay exact.

Every TOC row remains.107 source pins reconstruct from authenticated Git indices;
330 exclusions retain membership/order by baseline indices. The344-file baseline
uses retained LC0038 plus exact removals/replacements.
Generated protocol bodies and omission manifests retain canonical fingerprints;
raw diagnostics are replay outputs, not an archival promise. Missing Git
objects/pinned producers refuse without fetching. Normal/O inverse and six
refusal controls pass; old book teaching stays byte-exact.
XZ uses preset6, explicit8MiB dictionary,64MiB XZ memory limit and524288-byte
metadata/reconstruction bounds. Existing capacities and published prefix stay fixed.

```json
{"encoding":"lzma6/xz/base64 canonical UTF-8 JSON; source and manifest indices","metadata_bytes":250018,"metadata_sha256":"742f449b7fd7de38d5cec015b5c360732508d621bd4ad82ebfad0c8d251934dc","compressed_bytes":13968,"compressed_sha256":"357e92945364c99b6fb29df94d1951b654af64106fc4449633841627fb50cd86","metadata_xz_base64":"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","complete":{"canonical_bytes":292570,"canonical_sha256":"14c0bc4ad827bbae157e0694bf7740de1f52fbf383f7c3bf28b47e9ac4ee7ca1"},"producer":{"sha256":"1cfd53789ad2311587813cc30957b1a5c17f64e9bf80f3e7444849bf06500917","mode":420,"bytes":26674},"inventory_producer":{"sha256":"7e4c32464c940b4c457c7a45f7d5090988864422c8c98c45598afd63fd1fff77","mode":420,"bytes":16283},"project_source":"718bbd953bf6fd119a6a822de47d7eda75519f05","project_source_members":1466,"published_prefix":{"bytes":24876,"sha256":"9272e92c62f5bddde8c21e3bbc326fd8fea81eee26eca7f5c37253b37acedb19"}}
```

Decode the complete metadata through the pinned tracked producer:

```python
from pathlib import Path
import json,re,sys
sys.path.insert(0,'scripts')
import qualify_book_toc as Q
text=Path('docs/tasks/artifacts/live-containment/include-source-integration.md').read_text()
phase=text.split('## Chapter contents assessment — LC0040\n',1)[1]
f=json.loads(re.search(r'^```json\n(.*?)\n```$',phase,re.M|re.S)[1])
v=Q.decode_capture(f)
print(len(v['normal']['inputs']),len(v['normal']['observations']),len(v['optimized_overrides']))
```
