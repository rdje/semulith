# My schema validates every file it was designed from — why does it refuse the real corpus?

**Read the whole corpus before designing the grammar, and when the corpus writes a shape your
language cannot state, extend the language — never bend the corpus.** A grammar designed from a
sample fits the sample. The real corpus always contains the shapes the tidy design assumed away,
and each one is a fork: declare it honestly, or discover at migration time that "extensible by
data" was true only for the shapes the designer happened to have in mind.

## What happened

`SOT-FORMAT.1` built a schema language whose construct grammar is uniform `(name value)` field
pairs — designed from `schema/schema.sexp` and four small files, where it fit. `SOT-FORMAT.2`
then took the language to the real corpus and found three positional mini-languages the record
grammar cannot state, all in files already committed and consumed:

- fragment encodings: `(fixed (31 25 0x0) (14 12 0x0) …)` — positional integer triples;
- `(operands rd rs1 rs2)` — a bare-symbol list, empty for `ecall`;
- the semantics effect bodies: a 32-head expression language, `(add (reg rs1) (reg rs2))`, where
  the arguments are expressions, not fields.

Refusing the corpus was not an option — these files are generated from pinned upstream tables and
read by working tools. Ignoring the shapes was worse: "extensible" would have meant "typo-tolerant"
for exactly the constructs the tree exists to validate. The alternative that respects the corpus
and the doctrine at once: ONE new declaration kind, `(operator (name SYM) (fixed N) | (variadic)
[(min N)] [(arg SPEC)])`, parsed by the same kernel meta-level as `(construct …)` and `(field …)`.
Adding a construct or an operator is now data; a *fifth* kind would change the kernel — the same
boundary a database draws between adding a table and adding a column type, named in advance so
nobody discovers it as a surprise.

Re-derived:

```
$ python3 scripts/check_sexp_schema.py definitions/riscv/rv64i.sexp schema/fragment.sexp
  check_sexp_schema: ok — definitions/riscv/rv64i.sexp conforms to fragment.sexp
$ python3 scripts/check_sexp_schema.py definitions/riscv/rv64i.sem.sexp schema/semantics.sexp
  check_sexp_schema: ok — definitions/riscv/rv64i.sem.sexp conforms to semantics.sexp
$ python3 scripts/check_sexp_schema.py --self-test | tail -1
  check_sexp_schema --self-test: 31 pass / 0 fail        (16 -> 31; 15 operator arms)
```

⭐ **The uniform-pair grammar was not wrong by accident — it was wrong by sampling.** `.1`'s own
record says a first design "assumed a tidy uniform `(name value)` pair grammar; reading the real
corpus before building refused it" — for `schema.sexp`'s own declarations. The same sampling
trap one level down — designing from the files `.1` had already read — produced a grammar that
fit every file consulted and still could not state the corpus. The fix is procedural, not
intellectual: enumerate the population FIRST, then design. (`SOT-FORMAT.3`/`.4` convert the
records and the TOML/JSON configuration — the enumeration step happens there before any schema
is written for them.)
