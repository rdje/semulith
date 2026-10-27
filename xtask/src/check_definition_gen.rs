//! The `DEF-GEN` doctrine's driver, ported from `scripts/check_definition_gen.sh` (`XTASK.6` slice `6an`), which is now a
//! shim of `cargo xtask check-definition-gen`.
//!
//! `crates/semulith-core/src/definition.rs` and `definition_rv64gc.rs` are GENERATED from the units' canonical definitions
//! by `scripts/gen_definition.py`; the check regenerates each in memory (`--check`) and refuses the day it stops
//! byte-matching the committed file. The generator, the C-expansion probe (`scripts/probe_c_expansions.py`), the C-engine
//! probe (`scripts/probe_c_engine.py`) and the controls' four inline Python programs (the fence mutator over the pinned
//! `sexp`/`records_sexp`, the ghost instruction, the fieldless operand, the reversed decode rows) are spawned as the
//! script spawned them; nothing of them is ported. The controls run over scratch copies of the real fragments and over
//! staged rv64gc compositions written as the script's heredocs wrote them, the `sed`/`grep -v` edits as the same
//! literal replacements and line drops. Each self-test arm is one `tally.arm(` call — the needle loops keep their one
//! call each, as the script's did — the idiom the `DERIVED-COUNTS` arm total counts.

use std::ffi::OsStr;
use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, on_path, scratch, Hasher};

const ENCODING: &str = "profiles/rv64i-lab-v0/encoding.sexp";
const STATE: &str = "profiles/rv64i-lab-v0/state.sexp";
const OUT: &str = "crates/semulith-core/src/definition.rs";
// P4-SYSTEM.2 slice h (the route flip): the census's rv64gc owner→mirror pair.
const ENCODING_GC: &str = "profiles/rv64gc-lab-v0/encoding.sexp";
const STATE_GC: &str = "profiles/rv64gc-lab-v0/state.sexp";
const OUT_GC: &str = "crates/semulith-core/src/definition_rv64gc.rs";

/// `MUTATE_FENCE`, verbatim: `python3 - <replacement> <out>` — the one `tlb-invalidate` effect of the real
/// `system.sem.sexp` replaced, the document re-rendered through the pinned `records_sexp`.
const MUTATE_FENCE: &str = r####"import sys
from pathlib import Path
sys.path.insert(0, 'scripts')
import sexp as S
import records_sexp as R
forms = S.read_file(Path('definitions/riscv/system.sem.sexp'))
replacement = S.parse(sys.argv[1])[0]
matches = 0
def replace(form):
    global matches
    if not isinstance(form, list):
        return form
    if form and form[0] == 'tlb-invalidate':
        matches += 1
        return replacement
    return [replace(child) for child in form]
mutated = [replace(form) for form in forms]
assert matches == 1, 'fence mutation must replace exactly one effect'
Path(sys.argv[2]).write_text(R.render_forms(mutated))
"####;
/// The ghost instruction `zzz9` beside `add`, verbatim: `python3 - <rv64i.sexp>`.
const GHOST_INSN: &str = r####"import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
add = '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))'
assert add in text
ghost = add.replace('(name add)', '(name zzz9)')
open(path, "w", encoding="utf-8").write(text.replace(add, add + "\n  " + ghost))
"####;
/// The operand `rs9` that names no field, verbatim: `python3 - <rv64i.sexp>`.
const FIELDLESS_OPERAND: &str = r####"import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
add = '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))'
assert add in text
open(path, "w", encoding="utf-8").write(
    text.replace(add, add.replace("(operands rd rs1 rs2)", "(operands rd rs1 rs2 rs9)")))
"####;
/// The `INSNS` rows reversed, verbatim: `python3 - <c-definition.rs>`.
const REVERSE_ROWS: &str = r####"import re, sys
from pathlib import Path
p = Path(sys.argv[1]); text = p.read_text()
begin = text.index('pub static INSNS: &[InsnDef] = &[\n') + len('pub static INSNS: &[InsnDef] = &[\n')
end = text.index('\n];', begin)
rows = re.split(r'(?=^    InsnDef \{)', text[begin:end], flags=re.M)
p.write_text(text[:begin] + ''.join(reversed([row for row in rows if row])) + text[end:])
"####;

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `python3 scripts/gen_definition.py <args…> 2>&1` from the repository root, captured with its exit status.
fn generator(repo: &Path, args: &[&OsStr]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg("scripts/gen_definition.py")
            .args(args)
            .current_dir(repo),
    )
}

/// `python3 scripts/<probe> <args…> 2>&1` from the repository root, captured with its exit status.
fn probe(repo: &Path, script: &str, args: &[&OsStr]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg(script)
            .args(args)
            .current_dir(repo),
    )
}

/// `python3 - <args…> <<'PY'`: a program on stdin from the repository root; its own output passes through when the
/// self-test is the command, is silenced when the script ran its controls `>/dev/null 2>&1`. True on exit 0.
fn python_program(repo: &Path, program: &str, args: &[&OsStr], verbose: bool) -> bool {
    let through = || {
        if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        }
    };
    let mut command = Command::new("python3");
    command
        .arg("-")
        .args(args)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(through())
        .stderr(through());
    let Ok(mut child) = command.spawn() else {
        return false;
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(program.as_bytes());
    }
    child.wait().is_ok_and(|s| s.success())
}

/// `sed 's/PAT/REPL/' src > dst`: the first occurrence on every line, the patterns being literal text.
fn sed_first(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        out.push_str(&line.replacen(pattern, replacement, 1));
    }
    let _ = fs::write(dst, out);
}

/// `sed 's/PAT/REPL/g' src > dst`: every occurrence, the patterns being literal text.
fn sed_all(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let _ = fs::write(dst, text.replace(pattern, replacement));
}

/// `grep -v 'NEEDLE' path > tmp && mv tmp path`: the lines carrying the needle dropped.
fn drop_lines(path: &Path, needle: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let kept: String = text
        .split_inclusive('\n')
        .filter(|line| !line.contains(needle))
        .collect();
    let _ = fs::write(path, kept);
}

/// `grep -qF NEEDLE path; rc=$?`: 0 when a line carries the needle, 1 when none does, 2 when the file cannot be read.
fn carries(path: &Path, needle: &str) -> i32 {
    match fs::read_to_string(path) {
        Ok(text) => i32::from(!text.contains(needle)),
        Err(_) => 2,
    }
}

/// `printf '…' >> path`: the text appended.
fn append(path: &Path, text: &str) {
    if let Ok(mut file) = fs::OpenOptions::new().append(true).create(true).open(path) {
        let _ = file.write_all(text.as_bytes());
    }
}

/// `cp -r src dst` with `dst` absent: the tree copied.
fn copy_dir(src: &Path, dst: &Path) {
    let _ = fs::create_dir_all(dst);
    let Ok(entries) = fs::read_dir(src) else {
        return;
    };
    for entry in entries.flatten() {
        let from = entry.path();
        let to = dst.join(entry.file_name());
        if from.is_dir() {
            copy_dir(&from, &to);
        } else {
            let _ = fs::copy(&from, &to);
        }
    }
}

/// `cp definitions/riscv/*.sexp <dst>/`: every `.sexp` file of the real fragment directory.
fn copy_sexp_files(src: &Path, dst: &Path) {
    let Ok(entries) = fs::read_dir(src) else {
        return;
    };
    for entry in entries.flatten() {
        let from = entry.path();
        if from.is_file() && from.extension().is_some_and(|e| e == "sexp") {
            let _ = fs::copy(&from, dst.join(entry.file_name()));
        }
    }
}

/// A staged rv64gc composition as the script's heredocs wrote it: the three fixed extension forms, an optional extra
/// line of extensions, the status and slot.
fn gc_encoding(extra: Option<&str>, slot: &str) -> String {
    let mut text = String::from(
        "(encoding (profile \"rv64gc-lab-v0\") (ilen 32)\n  (compose (base \"riscv/rv64i\")\n    (extensions \"riscv/zicsr\") (extensions \"riscv/zicntr\") (extensions \"riscv/system\")\n",
    );
    if let Some(extra) = extra {
        text.push_str("    ");
        text.push_str(extra);
        text.push('\n');
    }
    text.push_str(&format!(
        "    (status partial) {slot})\n  (fragment-root \"definitions\"))\n"
    ));
    text
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the exit status must be `expected` and the output must contain `want` — or, for an empty `want`, be
    /// empty.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if want.is_empty() {
            if rc == expected && out.is_empty() {
                self.pass += 1;
                return;
            }
            self.fail += 1;
            if self.verbose {
                eprintln!("DEF-GEN self-test MISS: {name} — expected rc={expected} and no output, got rc={rc}\n{out}");
            }
            return;
        }
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("DEF-GEN self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}");
            }
        }
    }
}

/// The RED/GREEN controls over a surgical copy of the real unit and staged rv64gc compositions. Quiet unless `verbose`
/// (the script ran it `>/dev/null 2>&1` before the real judgement). A fence mutation that does not apply ends the
/// controls at once, as the script's `|| return 1` did.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "defgen") else {
        if verbose {
            eprintln!(
                "DEF-GEN self-test: cannot create a scratch directory under target/doctrine-selftest"
            );
        }
        return false;
    };
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    // The generator resolves fragments as <encoding's parent^3>/<fragment-root>, so the surgical unit mirrors the real
    // layout: tmp/profiles/<unit>/encoding.sexp composes tmp/definitions/riscv/*. The state descriptor is fingerprinted,
    // not read — the real one answers.
    let enc = t.join("profiles/rv64i-lab-v0/encoding.sexp");
    let riscv = t.join("definitions/riscv");
    let _ = fs::create_dir_all(t.join("profiles/rv64i-lab-v0"));
    let _ = fs::create_dir_all(&riscv);
    let real_riscv = repo.join("definitions/riscv");
    let _ = fs::copy(repo.join(ENCODING), &enc);
    let _ = fs::copy(real_riscv.join("rv64i.sexp"), riscv.join("rv64i.sexp"));
    let _ = fs::copy(
        real_riscv.join("rv64i.sem.sexp"),
        riscv.join("rv64i.sem.sexp"),
    );
    let definition = t.join("definition.rs");
    let state = OsStr::new(STATE);
    // `GEN`: the surgical unit's encoding, the real state, the scratch module, then the caller's flags.
    let gen = |check: bool| {
        let mut args = vec![
            OsStr::new("--encoding"),
            enc.as_os_str(),
            OsStr::new("--state"),
            state,
            OsStr::new("--out"),
            definition.as_os_str(),
        ];
        if check {
            args.push(OsStr::new("--check"));
        }
        generator(repo, &args)
    };
    // GREEN: the generator emits a module from the real definition.
    let (rc, out) = gen(false);
    tally.arm(
        "GREEN the generator emits a module from the real definition",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    // GREEN: the drift check passes on a faithful regeneration.
    let (rc, out) = gen(true);
    tally.arm(
        "GREEN a faithful regeneration is judged in sync",
        rc,
        0,
        captured(&out),
        "",
    );
    // RED: a hand-edit of the generated module is detected, named, and refused.
    append(&definition, "\n// hand edit\n");
    let (rc, out) = gen(true);
    tally.arm(
        "RED a hand-edited module is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "DRIFT",
    );
    // RED: a unit with an instruction length this generator cannot emit is refused by name.
    sed_first(&repo.join(ENCODING), &enc, "(ilen 32)", "(ilen 64)");
    let (rc, out) = gen(true);
    tally.arm(
        "RED an unsupported instruction length is refused by name",
        rc,
        2,
        captured(&out),
        "ilen 64",
    );
    let _ = fs::copy(repo.join(ENCODING), &enc);
    // RED: a unit other than the laboratory profile is refused by name.
    sed_first(
        &repo.join(ENCODING),
        &enc,
        "(profile \"rv64i-lab-v0\")",
        "(profile \"rv64i-other-v0\")",
    );
    let (rc, out) = gen(true);
    tally.arm(
        "RED another unit is refused by name",
        rc,
        2,
        captured(&out),
        "rv64i-other-v0",
    );
    let _ = fs::copy(repo.join(ENCODING), &enc);
    // RED: an instruction the semantics do not cover is refused, naming the instruction.
    let rv64i = riscv.join("rv64i.sexp");
    python_program(repo, GHOST_INSN, &[rv64i.as_os_str()], verbose);
    let (rc, out) = gen(true);
    tally.arm(
        "RED an encoding instruction without semantics is refused, naming it",
        rc,
        2,
        captured(&out),
        "zzz9",
    );
    let _ = fs::copy(real_riscv.join("rv64i.sexp"), &rv64i);
    // RED: a semantics rule referencing an operand the encoding does not provide is refused.
    let rv64i_sem = riscv.join("rv64i.sem.sexp");
    sed_first(
        &real_riscv.join("rv64i.sem.sexp"),
        &rv64i_sem,
        "(add (reg rs1) (reg rs2))",
        "(add (reg rs1) (reg rs3))",
    );
    let (rc, out) = gen(true);
    tally.arm(
        "RED an undeclared operand reference is refused, naming it",
        rc,
        2,
        captured(&out),
        "'rs3'",
    );
    let _ = fs::copy(real_riscv.join("rv64i.sem.sexp"), &rv64i_sem);
    // RED: an instruction declaring an operand that names no field is refused, naming it — extraction for it would be
    // silent, and silence is the guessed translation ARCHITECTURE §2 forbids (P3-BREADTH.2).
    python_program(repo, FIELDLESS_OPERAND, &[rv64i.as_os_str()], verbose);
    let (rc, out) = gen(true);
    tally.arm(
        "RED an operand naming no field is refused, naming it",
        rc,
        2,
        captured(&out),
        "rs9",
    );
    let _ = fs::copy(real_riscv.join("rv64i.sexp"), &rv64i);
    // RED: a fragment whose semantics document is missing is refused, naming the pairing.
    let _ = fs::remove_file(&rv64i_sem);
    let (rc, out) = gen(true);
    tally.arm(
        "RED a fragment without its semantics document is refused",
        rc,
        2,
        captured(&out),
        "no semantics document",
    );

    // ---- the rv64gc branch (P4-SYSTEM.2 slice d) -------------------------------------------------
    // (the previous arm removed the rv64i sem file; restore it before the rv64gc setup)
    let _ = fs::copy(real_riscv.join("rv64i.sem.sexp"), &rv64i_sem);
    // GREEN: the staged rv64gc composition emits the extended module — three separate (extensions …) forms (the shape
    // the dropped-form regression hid), the pseudo rows landing as PSEUDOS metadata, and the privileged operator
    // variants in the Sem enum.
    let gc_enc = t.join("gc/profiles/rv64gc-lab-v0/encoding.sexp");
    let gc_riscv = t.join("gc/definitions/riscv");
    let _ = fs::create_dir_all(t.join("gc/profiles/rv64gc-lab-v0"));
    let _ = fs::create_dir_all(t.join("gc/definitions"));
    copy_dir(&riscv, &gc_riscv);
    for f in ["zicsr", "zicntr", "system"] {
        let _ = fs::copy(
            real_riscv.join(format!("{f}.sexp")),
            gc_riscv.join(format!("{f}.sexp")),
        );
        let _ = fs::copy(
            real_riscv.join(format!("{f}.sem.sexp")),
            gc_riscv.join(format!("{f}.sem.sexp")),
        );
    }
    const SLOT_M: &str = "(slot (id m) (requires \"riscv/m\"))";
    let _ = fs::write(&gc_enc, gc_encoding(None, SLOT_M));
    // The staged composition's generator run: `--encoding <gc> --state STATE --out <out>`.
    let gen_gc = |out: &Path| {
        generator(
            repo,
            &[
                OsStr::new("--encoding"),
                gc_enc.as_os_str(),
                OsStr::new("--state"),
                state,
                OsStr::new("--out"),
                out.as_os_str(),
            ],
        )
    };
    let gc_system_sem = gc_riscv.join("system.sem.sexp");
    let real_system_sem = real_riscv.join("system.sem.sexp");
    // `MUTATE_FENCE <replacement> <out> || return 1`
    let mutate_fence = |replacement: &str| {
        python_program(
            repo,
            MUTATE_FENCE,
            &[OsStr::new(replacement), gc_system_sem.as_os_str()],
            verbose,
        )
    };
    let gc_definition = t.join("gc-definition.rs");
    let (rc, out) = gen_gc(&gc_definition);
    tally.arm(
        "GREEN the rv64gc composition emits the extended module",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    if !mutate_fence("(tlb-invalidate (reg rs1) (reg rs2))") {
        return false;
    }
    let (rc, out) = gen_gc(&t.join("gc-obsolete-fence.rs"));
    tally.arm(
        "RED the obsolete value-only fence arity is refused",
        rc,
        2,
        captured(&out),
        "takes 4 argument(s), got 2",
    );
    let _ = fs::copy(&real_system_sem, &gc_system_sem);
    for needle in ["TrapDeliver", "CsrRead", "Xret", "static PSEUDOS"] {
        let rc = carries(&gc_definition, needle);
        tally.arm(
            &format!("GREEN the emitted module carries {needle}"),
            rc,
            0,
            "",
            "",
        );
    }
    // RED: a privileged operator in an RV64I rule is refused, named — the rv64i module's byte surface is frozen, so the
    // refusal is the honest verdict there. Rewrite the fence rule to query (mode) in the rv64i surgical copy (a fresh
    // encoding copy: the earlier arms mutated the first).
    let _ = fs::copy(repo.join(ENCODING), &enc);
    sed_first(
        &rv64i_sem,
        &rv64i_sem,
        "(effect (nop))",
        "(effect (if (eq (mode) (lit 3)) (nop) (nop)))",
    );
    let (rc, out) = gen(false);
    tally.arm(
        "RED a privileged operator in a base rule is refused where not lowered",
        rc,
        2,
        captured(&out),
        "does not lower",
    );

    // ---- the A-extension operator surface (P4-SYSTEM.4 slice b) ------------------------------
    // The A variants emit exactly when the composition composes riscv/a: the tracked rv64gc module (the slot still
    // declared) keeps its byte surface, and the composition WITH the fragment proves the lowering — the same discipline
    // as the privileged operators off the rv64i module.
    let _ = fs::copy(real_riscv.join("a.sexp"), gc_riscv.join("a.sexp"));
    let _ = fs::copy(real_riscv.join("a.sem.sexp"), gc_riscv.join("a.sem.sexp"));
    let _ = fs::write(
        &gc_enc,
        gc_encoding(Some("(extensions \"riscv/a\")"), SLOT_M),
    );
    let gc_a = t.join("gc-a-definition.rs");
    let (rc, out) = gen_gc(&gc_a);
    tally.arm(
        "GREEN the rv64gc+A composition emits the A-operator module",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    for needle in ["LoadReserved", "StoreConditional", "Amo(u64"] {
        let rc = carries(&gc_a, needle);
        tally.arm(
            &format!("GREEN the emitted module carries {needle}"),
            rc,
            0,
            "",
            "",
        );
    }
    // RED: an amo operation literal the composition does not encode is refused, named — the closed set is derived from
    // the composed encodings' own funct5 fixed bits, never typed.
    sed_first(
        &real_riscv.join("a.sem.sexp"),
        &gc_riscv.join("a.sem.sexp"),
        "(amo (lit 0) (lit 32)",
        "(amo (lit 3) (lit 32)",
    );
    let (rc, out) = gen_gc(&gc_a);
    tally.arm(
        "RED an amo op outside the closed Zaamo nine is refused, naming it",
        rc,
        2,
        captured(&out),
        "not one of the closed Zaamo nine",
    );
    let _ = fs::copy(real_riscv.join("a.sem.sexp"), gc_riscv.join("a.sem.sexp"));
    // RED: an A operator where the composition does not compose riscv/a is refused, named — the variants emit WITH the
    // fragment; a module carrying them without it would not compile against its evaluator.
    drop_lines(&gc_enc, "extensions \"riscv/a\"");
    if !mutate_fence("(set (reg rs1) (store-conditional (lit 32) (reg rs1) (reg rs2)))") {
        return false;
    }
    let (rc, out) = gen_gc(&gc_a);
    tally.arm(
        "RED an A operator without riscv/a composed is refused, named",
        rc,
        2,
        captured(&out),
        "does not compose riscv/a",
    );
    let _ = fs::copy(&real_system_sem, &gc_system_sem);

    // ---- the floating-point operator surface (P4-SYSTEM.7 slice c3) --------------------------
    // The F variants emit exactly when the composition composes riscv/f — the A discipline: the tracked rv64gc module
    // keeps its byte surface until the F bind (slice c6), and the staged composition WITH the fragment proves the
    // lowering.
    let _ = fs::copy(real_riscv.join("f.sexp"), gc_riscv.join("f.sexp"));
    let _ = fs::copy(real_riscv.join("f.sem.sexp"), gc_riscv.join("f.sem.sexp"));
    let _ = fs::write(
        &gc_enc,
        gc_encoding(Some("(extensions \"riscv/f\")"), SLOT_M),
    );
    let gc_f = t.join("gc-f-definition.rs");
    let (rc, out) = gen_gc(&gc_f);
    tally.arm(
        "GREEN the rv64gc+F composition emits the floating-point module",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    for needle in [
        "FReg(&'static str)",
        "Rounding(&'static Sem)",
        "FMadd(u8",
        "FToI(u8, u8, bool",
        "Sem::FUnbox(",
    ] {
        let rc = carries(&gc_f, needle);
        tally.arm(
            &format!("GREEN the emitted module carries {needle}"),
            rc,
            0,
            "",
            "",
        );
    }
    // RED: an FP rule whose encoding carries rm but which never resolves it is refused — check_semantics.check_fp,
    // re-derived by the generator that emits the table.
    sed_first(
        &real_riscv.join("f.sem.sexp"),
        &gc_riscv.join("f.sem.sexp"),
        "(fadd 32 (rounding (field rm))",
        "(fadd 32 (lit 0)",
    );
    let (rc, out) = gen_gc(&gc_f);
    tally.arm(
        "RED an FP rule that never resolves its rm is refused, naming it",
        rc,
        2,
        captured(&out),
        "never resolves it through (rounding (field rm))",
    );
    let _ = fs::copy(real_riscv.join("f.sem.sexp"), gc_riscv.join("f.sem.sexp"));
    // RED: an FP operator where the composition does not compose riscv/f is refused, named.
    drop_lines(&gc_enc, "extensions \"riscv/f\"");
    if !mutate_fence("(set (reg rs1) (fclass 32 (reg rs2)))") {
        return false;
    }
    let (rc, out) = gen_gc(&gc_f);
    tally.arm(
        "RED an FP operator without riscv/f composed is refused, named",
        rc,
        2,
        captured(&out),
        "does not compose riscv/f",
    );
    let _ = fs::copy(&real_system_sem, &gc_system_sem);

    // ---- the D format conversion (P4-SYSTEM.7 slice d2) ---------------------------------------
    // FToF emits exactly when the composition composes riscv/d (the D bind, slice d5); the staged composition WITH F
    // and D proves the lowering of all 32 D rules.
    let _ = fs::copy(real_riscv.join("d.sexp"), gc_riscv.join("d.sexp"));
    let _ = fs::copy(real_riscv.join("d.sem.sexp"), gc_riscv.join("d.sem.sexp"));
    let _ = fs::write(
        &gc_enc,
        gc_encoding(
            Some("(extensions \"riscv/f\") (extensions \"riscv/d\")"),
            SLOT_M,
        ),
    );
    let gc_d = t.join("gc-d-definition.rs");
    let (rc, out) = gen_gc(&gc_d);
    tally.arm(
        "GREEN the rv64gc+F+D composition emits the double-precision module",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    for needle in [
        "FToF(u8, u8, &'static Sem, &'static Sem)",
        "Sem::FToF(",
        "\"fcvt.d.s\"",
    ] {
        let rc = carries(&gc_d, needle);
        tally.arm(
            &format!("GREEN the emitted module carries {needle}"),
            rc,
            0,
            "",
            "",
        );
    }
    // RED: the format conversion where the composition does not compose riscv/d is refused. F stays composed: the
    // refusal is D's own, not the F surface's.
    sed_first(
        &gc_enc,
        &gc_enc,
        "(extensions \"riscv/f\") (extensions \"riscv/d\")",
        "(extensions \"riscv/f\")",
    );
    let rc = carries(&gc_enc, "extensions \"riscv/f\"");
    tally.arm(
        "GREEN the no-D composition still composes riscv/f",
        rc,
        0,
        "",
        "",
    );
    if !mutate_fence("(set (reg rs1) (f2f 32 64 (reg rs1) (reg rs2)))") {
        return false;
    }
    let (rc, out) = gen_gc(&gc_d);
    tally.arm(
        "RED the format conversion without riscv/d composed is refused, named",
        rc,
        2,
        captured(&out),
        "does not compose riscv/d",
    );
    let _ = fs::copy(&real_system_sem, &gc_system_sem);

    // ---- the M operators (P4-SYSTEM.11 slice a) ------------------------------------------------
    // The eight variants emit exactly when the composition composes riscv/m (the M bind, slice b); the staged
    // composition WITH M proves the lowering of all 13 M rules.
    let _ = fs::copy(real_riscv.join("m.sexp"), gc_riscv.join("m.sexp"));
    let _ = fs::copy(real_riscv.join("m.sem.sexp"), gc_riscv.join("m.sem.sexp"));
    let _ = fs::write(
        &gc_enc,
        gc_encoding(
            Some("(extensions \"riscv/m\")"),
            "(slot (id c) (requires \"riscv/c\"))",
        ),
    );
    let gc_m = t.join("gc-m-definition.rs");
    let (rc, out) = gen_gc(&gc_m);
    tally.arm(
        "GREEN the rv64gc+M composition emits the multiply/divide module",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    for needle in [
        "Mul(&'static Sem, &'static Sem)",
        "Sem::DivU(",
        "Sem::MulHsu(",
        "\"remuw\"",
    ] {
        let rc = carries(&gc_m, needle);
        tally.arm(
            &format!("GREEN the emitted module carries {needle}"),
            rc,
            0,
            "",
            "",
        );
    }
    // RED: an unguarded division is refused by the generator too (the semantics checker's domain rule, re-derived where
    // the executable table is emitted).
    sed_first(
        &real_riscv.join("m.sem.sexp"),
        &gc_riscv.join("m.sem.sexp"),
        "(set (reg rd) (div (reg rs1) (reg rs2)))",
        "(set (reg rd) (div (reg rs1) (reg rs1)))",
    );
    let (rc, out) = gen_gc(&gc_m);
    tally.arm(
        "RED a division its guard does not cover is refused, naming its divisor",
        rc,
        2,
        captured(&out),
        "(div … (reg rs1)) is reached where its divisor may be zero",
    );
    let _ = fs::copy(real_riscv.join("m.sem.sexp"), gc_riscv.join("m.sem.sexp"));
    // RED: an M operator where the composition does not compose riscv/m is refused, named.
    sed_first(&gc_enc, &gc_enc, "    (extensions \"riscv/m\")", "");
    let rc = carries(&gc_enc, "extensions \"riscv/m\"");
    tally.arm(
        "GREEN the no-M composition composes no riscv/m",
        rc,
        1,
        "",
        "",
    );
    if !mutate_fence("(set (reg rs1) (mul (reg rs1) (reg rs2)))") {
        return false;
    }
    let (rc, out) = gen_gc(&gc_m);
    tally.arm(
        "RED an M operator without riscv/m composed is refused, named",
        rc,
        2,
        captured(&out),
        "does not compose riscv/m",
    );
    let _ = fs::copy(&real_system_sem, &gc_system_sem);

    // ---- C expansions (P4-SYSTEM.12 slice b) -------------------------------------------------
    // C lowering is proved on a disposable composition, independent of the live binding, including compiled Rust
    // decoding and independent operand/immediate-limit expectations.
    copy_sexp_files(&real_riscv, &gc_riscv);
    sed_first(
        &repo.join(ENCODING_GC),
        &gc_enc,
        "(slot (id c) (requires \"riscv/c\"))",
        "(extensions \"riscv/c\")",
    );
    let c_definition = t.join("c-definition.rs");
    let cgen = || {
        generator(
            repo,
            &[
                OsStr::new("--encoding"),
                gc_enc.as_os_str(),
                OsStr::new("--state"),
                OsStr::new(STATE_GC),
                OsStr::new("--out"),
                c_definition.as_os_str(),
            ],
        )
    };
    let cprobe = || {
        probe(
            repo,
            "scripts/probe_c_expansions.py",
            &[gc_enc.as_os_str(), c_definition.as_os_str()],
        )
    };
    let (rc, out) = cgen();
    tally.arm(
        "GREEN the full composition with C emits expansion metadata",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    let (rc, out) = cprobe();
    // `[ "$rc" -ne 0 ] || printf '%s\n' "$out"`: the probe's report on stdout when it passes.
    if rc == 0 && verbose {
        println!("{}", captured(&out));
    }
    tally.arm(
        "GREEN C's spec-side mappings and compiled specialization decoder",
        rc,
        0,
        captured(&out),
        "compiled decoder 8/8",
    );
    python_program(repo, REVERSE_ROWS, &[c_definition.as_os_str()], verbose);
    let (rc, out) = cprobe();
    tally.arm(
        "RED reversing specificity makes the compiled decoder fail",
        rc,
        1,
        captured(&out),
        "specialization_decode",
    );
    // RED: the mapper's spec-side expectation catches a plausible but wrong compact-register offset. Generation itself
    // succeeds: this tests correctness beyond shape/arity checks.
    sed_all(
        &real_riscv.join("c.sem.sexp"),
        &gc_riscv.join("c.sem.sexp"),
        "(field rd_p) (lit 8)",
        "(field rd_p) (lit 9)",
    );
    let (rc, out) = cgen();
    tally.arm(
        "GREEN a well-formed wrong C mapping still generates",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    let (rc, out) = cprobe();
    tally.arm(
        "RED a wrong compact-register mapping is caught independently",
        rc,
        1,
        captured(&out),
        "c.addi4spn: rd=16, expected 15",
    );
    let _ = fs::copy(real_riscv.join("c.sem.sexp"), gc_riscv.join("c.sem.sexp"));
    // RED: exact operand binding is re-judged at generation, not trusted from SEMANTICS.
    sed_first(
        &real_riscv.join("c.sem.sexp"),
        &gc_riscv.join("c.sem.sexp"),
        "(operand (name rd) (value (lit 0))) (operand (name jimm20)",
        "(operand (name jimm20)",
    );
    let (rc, out) = cgen();
    tally.arm(
        "RED an unbound base operand is refused by generation",
        rc,
        2,
        captured(&out),
        "c.j: binds",
    );
    let _ = fs::copy(real_riscv.join("c.sem.sexp"), gc_riscv.join("c.sem.sexp"));

    // P4-SYSTEM.12 c2: compile the TRACKED evaluator on the temporary C composition. Each RED arm requires a behavioral
    // test failure, never a compile/tool failure.
    let (rc, out) = probe(repo, "scripts/probe_c_engine.py", &[]);
    tally.arm(
        "GREEN C's exact parcel and expansion execution",
        rc,
        0,
        captured(&out),
        "18 passed; 0 failed",
    );
    let (rc, out) = probe(
        repo,
        "scripts/probe_c_engine.py",
        &[
            OsStr::new("--mutation"),
            OsStr::new("erase-expansion-widths"),
        ],
    );
    tally.arm(
        "RED losing a mapped immediate's width changes execution",
        rc,
        1,
        captured(&out),
        "c_engine::signed_immediates_keep_their_mapped_widths ... FAILED",
    );
    let (rc, out) = probe(
        repo,
        "scripts/probe_c_engine.py",
        &[OsStr::new("--mutation"), OsStr::new("word-parcel-read")],
    );
    tally.arm(
        "RED a word read crosses the first parcel's region",
        rc,
        1,
        captured(&out),
        "c_engine::mixed_lengths_at_two_mod_four_and_exact_region_end ... FAILED",
    );
    let (rc, out) = probe(
        repo,
        "scripts/probe_c_engine.py",
        &[OsStr::new("--mutation"), OsStr::new("short-ilen")],
    );
    tally.arm(
        "RED a wider prefix needs every ILEN parcel",
        rc,
        1,
        captured(&out),
        "c_engine::unsupported_long_prefix_keeps_all_ilen_bits ... FAILED",
    );

    // The slice-(h) census arms: the gate's judging loop covers the rv64gc owner→mirror pair — pinned against the REAL
    // pair, not a synthetic one.
    let (rc, out) = generator(
        repo,
        &[
            OsStr::new("--check"),
            OsStr::new("--encoding"),
            OsStr::new(ENCODING_GC),
            OsStr::new("--state"),
            OsStr::new(STATE_GC),
            OsStr::new("--out"),
            OsStr::new(OUT_GC),
        ],
    );
    tally.arm(
        "GREEN the census's rv64gc pair is in sync",
        rc,
        0,
        captured(&out),
        "",
    );
    let gc_module = t.join("gc-module.rs");
    let _ = fs::copy(repo.join(OUT_GC), &gc_module);
    append(&gc_module, "\n// hand edit\n");
    let (rc, out) = generator(
        repo,
        &[
            OsStr::new("--check"),
            OsStr::new("--encoding"),
            OsStr::new(ENCODING_GC),
            OsStr::new("--state"),
            OsStr::new(STATE_GC),
            OsStr::new("--out"),
            gc_module.as_os_str(),
        ],
    );
    tally.arm(
        "RED the census's rv64gc pair catches a hand edit",
        rc,
        1,
        captured(&out),
        "DRIFT",
    );

    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "DEF-GEN --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `judge_pair <encoding> <state> <module>`: the owner→mirror census for one pair — the generator's `--check`, its
/// output and the verdict on stderr when it refuses or finds drift, the `ok` line with the encoding's digest otherwise.
fn judge_pair(root: &Path, encoding: &str, state: &str, module: &str) -> Result<(), ExitCode> {
    let (rc, out) = generator(
        root,
        &[
            OsStr::new("--check"),
            OsStr::new("--encoding"),
            OsStr::new(encoding),
            OsStr::new("--state"),
            OsStr::new(state),
            OsStr::new("--out"),
            OsStr::new(module),
        ],
    );
    let out = captured(&out);
    if rc == 2 {
        eprintln!("{out}");
        eprintln!("DEF-GEN: REFUSED — the canonical definition could not be judged.");
        return Err(ExitCode::from(2));
    }
    if rc != 0 {
        eprintln!("{out}");
        eprintln!("DEF-GEN: FAIL — {module} is out of sync with the canonical definition. Regenerate — never edit:\n  python3 scripts/gen_definition.py");
        return Err(ExitCode::from(1));
    }
    // `sha256sum "$1" | cut -d' ' -f1`, its first sixteen characters.
    let sha = Hasher::find()
        .map(|h| h.digest(&root.join(encoding)))
        .unwrap_or_default();
    let short: String = sha.chars().take(16).collect();
    println!("DEF-GEN: ok ({module} matches the canonical definition, encoding sha256 {short})");
    Ok(())
}

/// `cargo xtask check-definition-gen [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!("DEF-GEN: REFUSED — python3 is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Re-run the controls before judging: a check that no longer discriminates must refuse, not pass.
    if !self_test(root, false) {
        eprintln!("DEF-GEN: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    if !root.join(ENCODING).is_file() {
        println!("DEF-GEN: ok (no encoding composition yet)");
        return ExitCode::SUCCESS;
    }
    // The owner→mirror census: every tracked encoding composition (+ its state descriptor) and its generated module.
    if let Err(code) = judge_pair(root, ENCODING, STATE, OUT) {
        return code;
    }
    if let Err(code) = judge_pair(root, ENCODING_GC, STATE_GC, OUT_GC) {
        return code;
    }
    ExitCode::SUCCESS
}
