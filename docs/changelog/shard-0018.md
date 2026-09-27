# CHANGELOG shard — SEMULITH-SF-0041 … SEMULITH-SF-0041

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-SF-0041 (leaf SOT-FORMAT.7) — the reader corrupted every citation it read

**What changed.** `scripts/sexp.py` decoded string escapes by handing the assembled string to
`.encode().decode("unicode_escape")`. That codec is **Latin-1**: it reads each byte as one
character, so the two UTF-8 bytes of `§` came back as `Â§` and an em dash came back as three
characters of noise.

**All 52 specification citations** in `definitions/riscv/rv64i.sem.sexp` were corrupted on read —
every locator committed one leaf earlier as *"52 of 52, every rule cited"*. The claim was true of
the file and false of what any consumer received:

```
raw bytes in file : b'RVI-RV64I \xc2\xa73.1.2.1 \xe2\x80\x94 D-LUI-AUIP'
as the reader sees: 'RVI-RV64I Â§3.1.2.1 â\x80\x94 D-LUI-AUIP'
```

**Why nothing caught it.** The reader that every source of truth in this repository depends on had
**no self-test at all**. Downstream, every instrument asked about structure or behaviour —
`check_semantics.py` asks whether a citation is *present*, and a corrupted string is still present.
None was pointed at **fidelity**, which is a separate property and has to be asserted separately.

**The fix.** Escapes are decoded from a closed five-entry table written in the file, and an escape
outside it is refused rather than guessed — the same soundness stance the module already claimed
for structure. A UTF-8 file needs no escape for non-ASCII at all. The reader now carries 18 arms,
three of them fired RED before the fix:

```
$ python3 scripts/sexp.py --self-test     # BEFORE → 15 pass / 3 fail
$ python3 scripts/sexp.py --self-test     # AFTER  → 18 pass / 0 fail
$ round-trip: each citation verbatim in the file's own bytes → 52 / 52, mojibake 0
```

No tracked file's content changed. The files were always right.

**Direction (director, `2026-09-14`).** Two instructions landed and are now durable records rather
than conversation:

- *Every source of truth is one format* — S-expression, composable, and **extensible to new
  constructs in the same format**. This supersedes the per-file format split in
  `decision_canonical-definition-input`: composition is a merge, and three formats are three merge
  semantics, so under the split a board composing two processors could union their encodings and
  nothing else. New tree `SOT-FORMAT`, 9 leaves.
- *The parser is not written here.* The Rust reader comes from **LinkedSpec**
  (`specs/Lispish.spec` on its Rust backend), added as a **git submodule** pinned to a commit.
  ⛔ I first inferred `pgen` from the capability description — *many backends, Rust among them,
  parses many formats* — and was corrected. The failure mode is general and worth keeping: a
  capability description matches several repositories; only a named artifact identifies one.
  ⛔ **Blocked:** LinkedSpec is preparing its integration document for downstream consumers and it
  is not finished, so `SOT-FORMAT.9` waits for it rather than integrating against internals.

**Also measured, and owned rather than logged.** The mdBook chapter *"Architecture and canonical
definitions"* includes `docs/ARCHITECTURE.md`, which names no format, no `definitions/` directory
and no composition operator — all three introduced over the four preceding commits. The director's
only window into the project shows none of the work. `SOT-FORMAT.8`, at frontier order 2.

**Knowledge.** [`a-parse-without-error-is-not-a-faithful-read`](docs/knowledge/a-parse-without-error-is-not-a-faithful-read.md)
— a parser's error paths are all about structure; it proves nothing about content until a test
compares what it returned with what it read. A test corpus of `foo` and `bar` cannot tell a correct
decoder from a Latin-1 one.

