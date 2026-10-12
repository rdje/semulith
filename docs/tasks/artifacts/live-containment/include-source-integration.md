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
