# CHANGELOG shard — SEMILITH-MM-0048 … SEMILITH-MM-0047

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-MM-0048 (leaf MODEL-METHOD.4) — the run-real-code set is acquired, and the PDF question is answered

What the ISA chapters do not own is now pinned: the RISC-V psABI canonical render, the System V
ELF specification, the generic syscall header (the hosted exit convention), and the LLVM
compiler-rt builtins inventory — the last carrying `__muldi3 (di_int a, di_int b); // a * b`,
the soft-multiply intrinsic a no-`M` target calls. Each is digest-pinned in the owning leaf,
cached on-volume under `.materials/run-real-code/`, and re-derivable from the recorded curl
commands; the bytes stay out of git, per the no-redistribution doctrine — the tracked record is
the digest table, not the documents. The startup/runtime contract needed no acquisition: the
harness contract already owns entry state and the ECALL/EBREAK exit convention.

⭐ The PDF question (MODEL-BOOKS.2) is answered **YES**: the specification's PDF rendering carries
the instruction-format tables as selectable text — `pdftotext` extracts 1.96 MB from the
release asset, and the RV32I format-table region yields `funct7 / rs2 / rs1 / funct3` as clean
cells. Encodings can be re-sourced from the primary document. SRC-02 records: the pinned
revision's release PDF was not located in three pages of releases; the chipdoc corpus route was
unavailable here (`$SEMULITH_CHIPDOC_ROOT` unset) — the psABI came from its canonical public
render instead.

## SEMILITH-MM-0047 (leaf MODEL-METHOD.3) — the census sweeps the snapshot, and missing changes its meaning

The coverage census for `rv64i-lab-v0` did what a first pass cannot: it opened the pinned
snapshot and checked. Every covered category's subject matter is present in the pinned pages —
and, the measured surprise, so are the excluded subsystems' chapters (a/d/f/q/v-st-ext, rvwmo,
counters, zicsr, zifencei). `missing` therefore never meant "material absent"; it means the
profile EXCLUDES the subsystem, and all six missing rows now name what would close them: a
profile revision against snapshot chapters (C07/C08/C16), the separate Privileged Architecture
manual (C12/C14/C15), the Debug specification (C18). Device and interconnect categories became
the new `deferred-to-board` disposition — P5-BOARD's to own, with the CPU recording an
environment assumption in their place. Final census: 10 covered, 4 partial, 6 missing with
closers, 3 deferred-to-board, 1 out-of-scope. RECORD-SCHEMA rule 12 (UNRESOLVED MATERIAL) keeps
every named material honest against the catalogue; 33 arms.

