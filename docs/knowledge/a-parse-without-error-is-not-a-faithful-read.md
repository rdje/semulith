# My reader parsed the file without error — can I trust the strings it handed back?

**Not until something has compared them to the file.** A parser has two jobs: decide the structure,
and reproduce the content. Every error message it can print is about the first job. A reader that
silently rewrites the bytes inside a string is, from the outside, indistinguishable from a correct
one — it returns a structure, no exception, and every downstream check passes.

## What happened

This project's canonical-definition reader decoded escape sequences by collecting them raw and
handing the finished string to a codec:

```python
stack[-1].append("".join(buf).encode().decode("unicode_escape"))
```

`unicode_escape` is **Latin-1**. It interprets each byte as one character. A `§` in a UTF-8 file is
the two bytes `C2 A7`, so it comes back as two characters, `Â§`. An em dash `—` is three bytes and
comes back as three characters of noise.

The file on disk was always correct. The reader corrupted it on the way in:

```
raw bytes in file : b'RVI-RV64I \xc2\xa73.1.2.1 \xe2\x80\x94 D-LUI-AUIP'
as the reader sees: 'RVI-RV64I Â§3.1.2.1 â\x80\x94 D-LUI-AUIP'
```

**All 52 specification citations** in the semantics fragment were affected — every one of them,
because a citation to a specification names a section, and a section marker is `§`. The commit
that introduced them had been verified as *"52 of 52, every rule cited"*, and that claim was true:
the citations were present, complete and correct **in the file**. Nothing had ever compared the
string the reader produced against the string the file contained.

## Why no check caught it

Each downstream check asked a question the corruption did not affect:

| The check | What it asked | Why the corruption passed |
| --- | --- | --- |
| the reader's own error paths | is the structure well-formed? | it was |
| `check_semantics.py` | does every instruction cite a source? | it did — a corrupted string is still non-empty |
| the guest smoke suite | do the models agree? | citations are never executed |
| the fragment generator | does it reproduce byte-for-byte? | it writes, it does not read back |

Every instrument was pointed at structure or at behaviour. **None was pointed at fidelity**, and
fidelity is a separate property that has to be asserted separately.

## The test that finds it, in one line

The content a reader returns must be findable, verbatim, in the bytes it read:

```python
assert reader_output in path.read_text()      # for every string literal
```

That single assertion would have failed on day one. Generalised: for any reader, writer, codec or
transport, **assert a round-trip on content that is not plain ASCII** — accented letters, `§`, `—`,
`µ`, `→`, CJK, an emoji. A test corpus made only of `foo` and `bar` cannot distinguish a correct
decoder from a Latin-1 one, and most hand-written test corpora are made of `foo` and `bar`.

## The rule

> A parser proves it understood the shape. It proves nothing about the content until a test
> compares what it returned with what it read.

Two smaller rules fall out of it, and both are worth keeping:

- **Decode escapes with a table you wrote, not with a codec you borrowed.** A closed table of five
  escapes — `\" \\ \n \t \r` — cannot reinterpret bytes it was not asked about, and an escape
  outside the table is refused instead of guessed. The borrowed codec was chosen because it was one
  line; the one line was the defect.
- **A file format that is UTF-8 needs no escape for non-ASCII at all.** Write the `§`.

And the reader that had this defect had **no self-test** — 150 lines of parsing on which every
source of truth in the repository depends, with zero arms. It now has 18. See
[[self-test-arms-that-never-ran]] for the sibling failure, where the arms existed and did not run.

Related: [[self-test-arms-that-never-ran]], [[zero-hits-absence-or-blindness]].
