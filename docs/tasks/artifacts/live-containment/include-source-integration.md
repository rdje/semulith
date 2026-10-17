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

## Heading navigation assessment — LC0042

Owner: LIVE-CONTAINMENT.4i2b5b2 / SEMULITH-LC-0042.
Immutable source1226311fcbef388d92c65fdf596f39a4e06d78cb:1477 identities,
1476 regular files and one opaque Gitlink. This phase preserves the entire
published46333B integration record above, including its LC0040 capture.

### Boundary and independent contracts

Fresh public mdBook builds cover seven books/344 generated files. All107
SUMMARY/configuration/chapter pins and all120 HTML roles are retained:93
chapters, six first-chapter index aliases and seven each print/toc/404 pages.
Independent Python HTML parsing and executed WebKit DOM serialization reconcile
1406 source/runtime headings and589 actual navigation entries: levels, IDs,
unique targets, complete labels/inline markup, list nesting, title, current
chapter and the navigation's active parent. Every page/heading/navigation row
and baseline generated-file identity is retained, not sampled.

An observational script is injected only while serving the copied generated
bundle from127.0.0.1; no original output file changes. The adapter awaits load
and a delayed JavaScript witness before serializing the DOM. Native engine
exit0 alone is insufficient: script-omitted and blank witnesses also exit0 but
fail the independent execution contract. The positive delayed-JS and actual
HTTP-loopback witnesses pass. Unexpected stderr, JS errors, navigation failure,
timeout or renderer termination refuse qualification. Each owned native process
is waited/reaped; the loopback server is shut down and joined.

Actual engine: OS WebKit22625.1.29.11.28, macOS27.0.1 build26A434, public
WKWebView with WKWebsiteDataStore.nonPersistent. Swift6.4/driver1.168.6 compiles
the owned adapter with Swift6 strict mode and warnings as errors, rc=0/empty
compile diagnostics. Compiler/module/temp/output data stay below the owned
target directory. Installed SDK/framework/compiler are required external
read-only OS dependencies; their public headers define the API. No personal
browser profile, external Git implementation or Gitlink internals are used.

### Results and root cause

Normal and optimized runs complete with identical page contracts:119 correct,
one wrong. D78 priority1: authored project index.html marks introduction.html
and index.html active simultaneously. Its title/body are Index. The public
generated toc script's unconditional root-index first-link fallback fires even
when an explicit Index chapter link matches. This is a current-page ambiguity,
not a browser/JavaScript failure. Immediate next owner is LC0043, recorded in
the task root before assessment publication.

Three actual copied-producer omissions discriminate: skip heading insertion,
omit h2 from the selector, and omit inline-label copying. Each native launch
completes0 but the independent complete heading contract fails1. The fourth
cause control removes the public index fallback: authored Index becomes correct
while a previously correct unit-book index alias becomes wrong. A repair must
preserve all six aliases. Neither removing the fallback alone nor accepting
engine exit0 is sufficient. No production generated bundle was edited.

```sh
python3 scripts/qualify_book_headings.py --output target/heading-replay
python3 scripts/qualify_book_headings.py --verify-record
python3 -O scripts/qualify_book_headings.py --self-test
```

Use a fresh output. Capture0 means completed measurement; --require-clean
returns1 for this immutable source's D78. Unjudgeable input returns named
BOOK-HEADINGS refusal2. Record queries authenticate and reconstruct the whole
retained normal/optimized metadata and source/book references. Nine damaged
outer/inner frames refuse normally and with optimization, including consistent
re-hashed source, membership, type and trailing-compression corruptions.

### Retention and limits of the claim

The bounded XZ/base64 frame below retains complete input/page/header/navigation
rows, checks, source tree, toolchain, calibration, actual omission results,
all344 baseline generated identities and exact old/new book teaching seams.
Source pins reference the immutable1477-member Git census; baseline manifest
deltas authenticate and expand the whole LC0040 predecessor catalogue. The
optimized view uses exact metadata replacements over the normal view; inverse
checks compare both whole expanded views with the actual raw capture. Record
replay requires those Git objects and pinned producers, with lazy fetch disabled;
it does not claim a no-Git query or reproduce browser execution from metadata.

Raw DOM/stdout/stderr/ordered HTTP streams and omitted-bundle file tables remain
generated diagnostics. Their identities and complete per-path request counts
are retained, not the raw streams or every alternate bundle byte. Earlier Chrome
and Edge calibration diagnostics, including headless display/graphics warnings,
are preserved in the owned calibration directory and task log; they are not
silently accepted as WebKit qualification. WebKit is required; Chrome/Edge were
read-only calibration tools. Chromium ancestry is not an independent engine oracle.

Click/scroll behavior, layout/visual output, search, full resource loading and
the other224 generated non-HTML files remain unqualified. Successful requests
are observations, not resource completeness. This finite assessment grants no
full semantic-graph, containment-adoption or CPU/MCU/DSP/board acceptance claim.
Existing task/book/family/part limits and earlier sealed terminals stay fixed.
promotion: declined; finite evidence and D78 ownership live here and in the task.

### Complete authenticated capture

```json
{"compressed_bytes":55308,"compressed_sha256":"231014304dac7dd48f36912cddaa90b6c9a6fe4e88c0c608e2c5e6a4955c24f5","encoding":"xz6/base64 canonical UTF-8 JSON","metadata_bytes":1436304,"metadata_sha256":"7cf06b996a371a43a64e51c75da1c09de4feae7d93246e8d0d86d12bc78a0d6c","metadata_xz_base64":"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","native_producer":{"bytes":4686,"mode":420,"sha256":"6ebec7e777778898eeb9d5a1aa05fde29fba535301a17e99a7f4e7b25a68221a"},"producer":{"bytes":54522,"mode":420,"sha256":"b2a584a05cb7754fba2244ff9af8b25d30240bfb0488e74d2c2c83fe2f6904d2"},"schema_version":1}
```
