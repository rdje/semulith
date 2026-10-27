//! The `STATE-GEN` doctrine's driver, ported from `scripts/check_state_gen.sh` (`XTASK.6` slice `6x`), which is now a
//! shim of `cargo xtask check-state-gen`.
//!
//! The architectural-state modules (`crates/semulith-core/src/state.rs`, `state_rv64gc.rs`) are GENERATED from the
//! units' state descriptors (`profiles/*/state.sexp`) and the arithmetic module by `scripts/gen_state.py`; this check
//! regenerates each pair in memory and refuses the day a module stops byte-matching its descriptor, or the day the
//! generator refuses a descriptor by name (an XLEN disagreement, an unmapped register, a missing census, a shape the
//! RV64 path does not emit, a CSR without its reset, a view of nothing, field resets and legalizations that disagree,
//! a duplicate address). The generator is spawned exactly as the driver spawned it and is not ported; the controls run
//! over scratch copies of the real descriptors with the script's `sed` and Python edits as the same replacements, and
//! its `gc_state` template verbatim. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm
//! total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

use crate::harness::{combined, scratch, Hasher};

const STATE: &str = "profiles/rv64i-lab-v0/state.sexp";
const ARITH: &str = "crates/semulith-core/src/arith.rs";
const OUT: &str = "crates/semulith-core/src/state.rs";
const STATE_GC: &str = "profiles/rv64gc-lab-v0/state.sexp";
const OUT_GC: &str = "crates/semulith-core/src/state_rv64gc.rs";

/// The script's `gc_state` descriptor, verbatim; `{field}` is its one argument (a `(field …)` form or nothing).
const GC_STATE: &str = r#"(state (profile_id "rv64gc-lab-v0") (xlen 64) (note "n")
  (integer_registers (count 32) (width_bits 64) (ids "x0..x31")
    (authority architecture) (source "s")
    (x0 (hardwired_zero true) (authority architecture) (source "s") (statement "x"))
    (named_by_the_isa_chapter (named-register (reg "x1") (role "r")
                               (authority software-convention) (source "s"))))
  (special_registers (register (id "pc") (width_bits 64) (holds "h")
                      (authority architecture) (source "s") (reset "r")
                      (reset_authority laboratory)))
  (privilege_mode (modes m) (modes s) (authority architecture) (source "s")
    (reset (value "m") (authority architecture) (source "s") (statement "x")))
  (fp_registers (count 32) (width_bits 64) (ids "f0..f31")
    (authority architecture) (source "s")
    (reset (value "0") (authority laboratory) (source "s") (statement "x")))
  (csr (id "mstatus") (address 768) (width_bits 64) (authority architecture) (source "s")
    {field}
    (reset (value "0") (authority laboratory) (source "s") (statement "x")))
  (csr (id "sstatus") (address 256) (width_bits 64) (view_of "mstatus")
    (authority architecture) (source "s")
    (reset (value "as mstatus") (authority laboratory) (source "s") (statement "x")))
  (hidden_state_census (question "q") (answer "No") (candidates (checked (candidate "c") (present false) (why "w"))) (candidates (checked (candidate "address-translation caches (TLBs)") (present true) (why "w"))) (candidates (checked (candidate "reservation set (LR/SC)") (present true) (why "w"))) (candidates (checked (candidate "hart wait state (ACTIVE/WAITING)") (present true) (why "w"))) (candidates (checked (candidate "floating-point registers f0-f31 and the fcsr behaviour") (present true) (why "w"))) (consequence "c"))
)
"#;

/// `python3 scripts/gen_state.py <args>` from the root, stdout and stderr together as `2>&1` joined them.
fn generator(repo: &Path, args: &[&str]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg("scripts/gen_state.py")
            .args(args)
            .current_dir(repo),
    )
}

fn check(repo: &Path, state: &str, arith: &str, out: &str) -> (i32, String) {
    generator(
        repo,
        &["--check", "--state", state, "--arith", arith, "--out", out],
    )
}

fn emit(repo: &Path, state: &str, arith: &str, out: &str) -> (i32, String) {
    generator(repo, &["--state", state, "--arith", arith, "--out", out])
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `sed 's/PAT/REPL/' src > dst`: the first occurrence on every line, the pattern being literal text.
fn sed_literal(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let out: String = text
        .split_inclusive('\n')
        .map(|line| line.replacen(pattern, replacement, 1))
        .collect();
    let _ = fs::write(dst, out);
}

/// `t.replace(a, b, 1)` on a file, as the script's Python did.
fn replace_first(path: &Path, from: &str, to: &str) {
    if let Ok(text) = fs::read_to_string(path) {
        let _ = fs::write(path, text.replacen(from, to, 1));
    }
}

/// `text.rstrip()[:-1] + form + ")\n"`: a form appended inside the descriptor's closing paren.
fn append_form(src: &Path, dst: &Path, form: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let body = text.trim_end();
    let body = &body[..body.len().saturating_sub(1)];
    let _ = fs::write(dst, format!("{body}{form})\n"));
}

/// The script's census remover: the balanced `(hidden_state_census …)` form cut out of the descriptor.
fn remove_census(src: &Path, dst: &Path) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let Some(start) = text.find("(hidden_state_census") else {
        return;
    };
    let mut depth = 0i32;
    for (i, c) in text[start..].char_indices() {
        match c {
            '(' => depth += 1,
            ')' => {
                depth -= 1;
                if depth == 0 {
                    let end = start + i + 1;
                    let _ = fs::write(dst, format!("{}{}", &text[..start], &text[end..]));
                    return;
                }
            }
            _ => {}
        }
    }
}

fn hand_edit(path: &Path, line: &str) {
    let mut text = fs::read(path).unwrap_or_default();
    text.extend_from_slice(line.as_bytes());
    let _ = fs::write(path, text);
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the run's exit status must be `expected` and its output must contain `want` — or, with an empty
    /// `want`, there must be no output at all.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if want.is_empty() {
            if rc == expected && out.is_empty() {
                self.pass += 1;
                return;
            }
            self.fail += 1;
            if self.verbose {
                eprintln!("STATE-GEN self-test MISS: {name} — expected rc={expected} and no output, got rc={rc}\n{out}");
            }
            return;
        }
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("STATE-GEN self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}");
            }
        }
    }
}

/// The RED/GREEN controls over scratch copies of the real descriptor and arithmetic module, then the script's own
/// rv64gc descriptor template through every refusal the generator names.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "stategen") else {
        eprintln!(
            "STATE-GEN self-test: cannot create a scratch directory under target/doctrine-selftest"
        );
        return false;
    };
    let _ = fs::copy(repo.join(STATE), t.join("state.sexp"));
    let _ = fs::copy(repo.join(ARITH), t.join("arith.rs"));
    let p = |rel: &str| t.join(rel).display().to_string();
    let (state, arith, out) = (p("state.sexp"), p("arith.rs"), p("state.rs"));
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let (rc, o) = emit(repo, &state, &arith, &out);
    tally.arm(
        "GREEN the generator emits a module from the real descriptor",
        rc,
        0,
        captured(&o),
        "wrote",
    );
    let (rc, o) = check(repo, &state, &arith, &out);
    tally.arm(
        "GREEN a faithful regeneration is judged in sync",
        rc,
        0,
        captured(&o),
        "",
    );
    hand_edit(&t.join("state.rs"), "\n// hand edit\n");
    let (rc, o) = check(repo, &state, &arith, &out);
    tally.arm(
        "RED a hand-edited module is refused, naming DRIFT",
        rc,
        1,
        captured(&o),
        "DRIFT",
    );
    for d in ["badxlen", "mepc", "nocensus"] {
        let _ = fs::create_dir_all(t.join(d));
    }
    sed_literal(
        &t.join("state.sexp"),
        &t.join("badxlen/state.sexp"),
        "(xlen 64)",
        "(xlen 32)",
    );
    let (rc, o) = check(repo, &p("badxlen/state.sexp"), &arith, &out);
    tally.arm(
        "RED a descriptor/arithmetic XLEN disagreement is refused, naming both",
        rc,
        2,
        captured(&o),
        "xlen mismatch",
    );
    sed_literal(
        &t.join("state.sexp"),
        &t.join("mepc/state.sexp"),
        "(id \"pc\")",
        "(id \"mepc\")",
    );
    let (rc, o) = check(repo, &p("mepc/state.sexp"), &arith, &out);
    tally.arm(
        "RED an unmapped special register is refused by name",
        rc,
        2,
        captured(&o),
        "'mepc'",
    );
    remove_census(&t.join("state.sexp"), &t.join("nocensus/state.sexp"));
    let (rc, o) = check(repo, &p("nocensus/state.sexp"), &arith, &out);
    tally.arm(
        "RED a descriptor without its SEM-08 census is refused, naming it",
        rc,
        2,
        captured(&o),
        "hidden_state_census",
    );
    for d in ["family", "spaces", "stack", "noxlen"] {
        let _ = fs::create_dir_all(t.join(d));
    }
    append_form(&t.join("state.sexp"), &t.join("family/state.sexp"), " (register_family (id \"acc\") (count 2) (width_bits 56) (ids \"a, b\") (authority architecture) (source \"DSP56300FM §3.4.1\"))");
    append_form(&t.join("state.sexp"), &t.join("spaces/state.sexp"), " (memory_spaces (space (id \"x\") (word_bits 24) (authority architecture) (source \"DSP56300FM §3.1\")))");
    append_form(&t.join("state.sexp"), &t.join("stack/state.sexp"), " (hardware_stack (levels 16) (width_bits 48) (indexing \"SP pre-increments; slot 0 unwritable\") (stale_slots_observable true) (authority architecture) (source \"DSP56300FM §5.4.3\"))");
    let (rc, o) = check(repo, &p("family/state.sexp"), &arith, &out);
    tally.arm(
        "RED a declared register_family is refused by name (F1)",
        rc,
        2,
        captured(&o),
        "register_family declared",
    );
    let (rc, o) = check(repo, &p("spaces/state.sexp"), &arith, &out);
    tally.arm(
        "RED a declared memory_spaces is refused by name (F3)",
        rc,
        2,
        captured(&o),
        "memory_spaces declared",
    );
    let (rc, o) = check(repo, &p("stack/state.sexp"), &arith, &out);
    tally.arm(
        "RED a declared hardware_stack is refused by name",
        rc,
        2,
        captured(&o),
        "hardware_stack declared",
    );
    sed_literal(
        &t.join("state.sexp"),
        &t.join("noxlen/state.sexp"),
        " (xlen 64)",
        "",
    );
    let (rc, o) = check(repo, &p("noxlen/state.sexp"), &arith, &out);
    tally.arm(
        "RED a descriptor without xlen is refused, naming the binding",
        rc,
        2,
        captured(&o),
        "no xlen",
    );
    // The script's rv64gc descriptor template, its one argument a `(field …)` form inside `mstatus`.
    let _ = fs::create_dir_all(t.join("gc"));
    let gc_state = |field: &str| {
        let _ = fs::write(t.join("gc/state.sexp"), GC_STATE.replace("{field}", field));
    };
    let (gstate, gout) = (p("gc/state.sexp"), p("gc/state.rs"));
    const HEADER: &str = "(state (profile_id \"rv64gc-lab-v0\") (xlen 64) (note \"n\")";
    gc_state("");
    let (rc, o) = emit(repo, &gstate, &arith, &gout);
    tally.arm(
        "GREEN the rv64gc descriptor emits a module (mode + CSR storage + field tables)",
        rc,
        0,
        captured(&o),
        "wrote",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "GREEN the rv64gc regeneration is judged in sync",
        rc,
        0,
        captured(&o),
        "",
    );
    gc_state("");
    replace_first(&t.join("gc/state.sexp"), HEADER, &format!("{HEADER} (register_family (id \"f\") (count 8) (width_bits 32) (ids \"f0..f7\") (authority architecture) (source \"s\"))"));
    let (rc, o) = emit(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED the rv64gc path refuses register_family, named",
        rc,
        2,
        captured(&o),
        "register_family declared",
    );
    gc_state("");
    replace_first(&t.join("gc/state.sexp"), HEADER, &format!("{HEADER} (memory_spaces (space (id \"io\") (word_bits 64) (authority architecture) (source \"s\")))"));
    let (rc, o) = emit(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED the rv64gc path refuses memory_spaces, named",
        rc,
        2,
        captured(&o),
        "memory_spaces declared",
    );
    gc_state("");
    replace_first(&t.join("gc/state.sexp"), HEADER, &format!("{HEADER} (hardware_stack (levels 2) (width_bits 64) (indexing \"x\") (stale_slots_observable false) (authority laboratory) (source \"s\"))"));
    let (rc, o) = emit(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED the rv64gc path refuses hardware_stack, named",
        rc,
        2,
        captured(&o),
        "hardware_stack declared",
    );
    gc_state("");
    replace_first(
        &t.join("gc/state.sexp"),
        "(candidate \"address-translation caches (TLBs)\") (present true)",
        "(candidate \"address-translation caches (TLBs)\") (present false)",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a census silent on the translation cache is refused, named",
        rc,
        2,
        captured(&o),
        "does not declare a present translation-cache",
    );
    gc_state("");
    replace_first(
        &t.join("gc/state.sexp"),
        "(candidate \"reservation set (LR/SC)\") (present true)",
        "(candidate \"reservation set (LR/SC)\") (present false)",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a census silent on the reservation is refused, named",
        rc,
        2,
        captured(&o),
        "does not declare a present reservation",
    );
    gc_state("");
    replace_first(
        &t.join("gc/state.sexp"),
        "(candidate \"hart wait state (ACTIVE/WAITING)\") (present true)",
        "(candidate \"hart wait state (ACTIVE/WAITING)\") (present false)",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a census silent on the wait state is refused, named",
        rc,
        2,
        captured(&o),
        "does not declare a present wait-state",
    );
    gc_state("");
    replace_first(
        &t.join("gc/state.sexp"),
        "(candidate \"floating-point registers f0-f31 and the fcsr behaviour\") (present true)",
        "(candidate \"floating-point registers f0-f31 and the fcsr behaviour\") (present false)",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a census silent on the FP file is refused, named",
        rc,
        2,
        captured(&o),
        "does not declare a present fp-file",
    );
    // The census's real rv64gc pair, by the paths the script passed (relative to the root).
    let (rc, o) = check(repo, STATE_GC, ARITH, OUT_GC);
    tally.arm(
        "GREEN the census's rv64gc pair is in sync",
        rc,
        0,
        captured(&o),
        "",
    );
    let _ = fs::copy(repo.join(OUT_GC), t.join("gc-module.rs"));
    hand_edit(&t.join("gc-module.rs"), "\n// hand edit\n");
    let (rc, o) = check(repo, STATE_GC, ARITH, &p("gc-module.rs"));
    tally.arm(
        "RED the census's rv64gc pair catches a hand edit",
        rc,
        1,
        captured(&o),
        "DRIFT",
    );
    // As the script: the next edit lands on the descriptor the FP arm left behind.
    replace_first(&t.join("gc/state.sexp"), "(reset (value \"0\") (authority laboratory) (source \"s\") (statement \"x\")))\n  (csr (id \"sstatus\")", ")\n  (csr (id \"sstatus\")");
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a csr without a reset is refused, named",
        rc,
        2,
        captured(&o),
        "expected exactly one (reset",
    );
    gc_state("");
    sed_literal(
        &t.join("gc/state.sexp"),
        &t.join("gc/state.sexp"),
        "(view_of \"mstatus\")",
        "(view_of \"nostatus\")",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a view of an undeclared csr is refused by name",
        rc,
        2,
        captured(&o),
        "a view of nothing",
    );
    gc_state("(field (id \"all\") (bit_hi 63) (bit_lo 0) (discipline warl) (legalize (any)) (reset \"1\") (reset_authority laboratory) (authority architecture) (source \"s\"))");
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED field resets disagreeing with the csr-level reset are refused",
        rc,
        2,
        captured(&o),
        "one reset, one value",
    );
    gc_state("(field (id \"all\") (bit_hi 63) (bit_lo 0) (discipline warl) (reset \"0\") (reset_authority laboratory) (authority architecture) (source \"s\"))");
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a WARL field without a (legalize …) is refused",
        rc,
        2,
        captured(&o),
        "without a",
    );
    gc_state("(field (id \"all\") (bit_hi 63) (bit_lo 0) (discipline wpri) (legalize (any)) (reset \"0\") (reset_authority laboratory) (authority architecture) (source \"s\"))");
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a WPRI field carrying a legalize is refused",
        rc,
        2,
        captured(&o),
        "WPRI field carries no",
    );
    gc_state("(field (id \"all\") (bit_hi 63) (bit_lo 0) (discipline warl) (legalize (read-only 2)) (reset \"0\") (reset_authority laboratory) (authority architecture) (source \"s\"))");
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a read-only constant disagreeing with the field's reset is refused",
        rc,
        2,
        captured(&o),
        "one constant, stated once",
    );
    gc_state("");
    sed_literal(
        &t.join("gc/state.sexp"),
        &t.join("gc/state.sexp"),
        "(address 256)",
        "(address 768)",
    );
    let (rc, o) = check(repo, &gstate, &arith, &gout);
    tally.arm(
        "RED a duplicate csr address is refused",
        rc,
        2,
        captured(&o),
        "duplicate csr address",
    );
    let _ = fs::create_dir_all(t.join("gcwrong"));
    append_form(&t.join("state.sexp"), &t.join("gcwrong/state.sexp"), " (csr (id \"mstatus\") (address 768) (width_bits 64) (authority architecture) (source \"s\") (reset (value \"0\") (authority laboratory) (source \"s\") (statement \"x\")))");
    let (rc, o) = check(repo, &p("gcwrong/state.sexp"), &arith, &out);
    tally.arm(
        "RED a csr declared under rv64i-lab-v0 is refused, named",
        rc,
        2,
        captured(&o),
        "csr / privilege_mode declared under rv64i-lab-v0",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "STATE-GEN --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `judge_pair <descriptor> <module>`: the generator's `--check` over the pair; a failure prints its output and the
/// FAIL line and ends the run; a pass prints the descriptor's digest prefix.
fn judge_pair(root: &Path, state: &str, module: &str) -> Result<(), ExitCode> {
    let (rc, out) = check(root, state, ARITH, module);
    if rc != 0 {
        eprintln!("{}", captured(&out));
        eprintln!("STATE-GEN: FAIL — {module} is out of sync with {state}. Regenerate — never edit:\n  python3 scripts/gen_state.py");
        return Err(ExitCode::from(1));
    }
    let sha = Hasher::find()
        .map(|h| h.digest(&root.join(state)))
        .unwrap_or_default();
    let prefix: String = sha.chars().take(16).collect();
    println!("STATE-GEN: ok ({module} matches {state}, sha256 {prefix})");
    Ok(())
}

/// `cargo xtask check-state-gen [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("STATE-GEN: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    if !root.join(STATE).is_file() {
        println!("STATE-GEN: ok (no state descriptor yet)");
        return ExitCode::SUCCESS;
    }
    if let Err(code) = judge_pair(root, STATE, OUT) {
        return code;
    }
    if let Err(code) = judge_pair(root, STATE_GC, OUT_GC) {
        return code;
    }
    ExitCode::SUCCESS
}
