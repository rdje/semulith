//! The `M-VECTORS` doctrine's driver, ported from `scripts/check_m_vectors.sh` (`XTASK.6` slice `6s`), which is now a
//! shim of `cargo xtask check-m-vectors`.
//!
//! The M-extension vector table (`crates/semulith-verify/src/m_vectors/vectors.txt`) must be the generator's output and
//! the generator's reference must obey the chapter — Table 1's zero-divisor and overflow rows, the remainder's sign and
//! bound, the product splits, the word forms' sign extension — judged on an operand set the table does not use. The
//! judge is the driver's inline Python, loading the generator as a module; it runs verbatim through `python3 -`, as the
//! script ran it, and is not ported. The self-test's controls run over COPIES of the generator and a table each copy
//! generated (the `P4-SYSTEM.9` lesson), the script's `sed` mutations as the same first-occurrence replacements. Each
//! self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

const GENERATOR: &str = "scripts/gen_m_vectors.py";
const TABLE: &str = "crates/semulith-verify/src/m_vectors/vectors.txt";

/// The judge, verbatim: `python3 - <generator> <table>` — prints findings, exits 1 on any, 0 when clean.
const JUDGE: &str = r#"import importlib.util, random, sys
from pathlib import Path
gen_path, table = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("gen_m_vectors", gen_path)
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
findings = []
text = G.table()
drift = not table.is_file() or table.read_text() != text
if drift:
    findings.append(f"DRIFT {table}: not the generator's output — regenerate (python3 scripts/gen_m_vectors.py), never edit")
M64 = (1 << 64) - 1
def s(v, n): v &= (1 << n) - 1; return v - (1 << n) if v >> (n - 1) else v
rng = random.Random(0x4D56)                      # an operand set the table does not use
ops = list(G.EDGES) + [rng.getrandbits(64) for _ in range(120)] + [rng.randrange(1, 64) for _ in range(8)]
ops += [(-x) & M64 for x in ops[-8:]]
def R(mn, a, b): return G.reference(mn, a, b)
for a in ops:
    for b in ops[:48]:
        for L, sfx in ((64, ""), (32, "w")):
            ua, ub, sa, sb = a & ((1 << L) - 1), b & ((1 << L) - 1), s(a, L), s(b, L)
            q, r = s(R("div" + sfx, a, b), 64), s(R("rem" + sfx, a, b), 64)
            qu, ru = R("divu" + sfx, a, b), R("remu" + sfx, a, b)
            if L == 32:                          # the word forms sign-extend the 32-bit result
                for v, n in ((q, "div"), (r, "rem")):
                    if v != s(v, 32): findings.append(f"NOT SIGN-EXTENDED {n}w {a:#x} {b:#x}")
                qu, ru = s(qu, 64), s(ru, 64)
                if s(qu, 32) != qu or s(ru, 32) != ru: findings.append(f"NOT SIGN-EXTENDED divuw/remuw {a:#x} {b:#x}")
                qu, ru = qu & 0xFFFF_FFFF, ru & 0xFFFF_FFFF
            if sb == 0:
                if q != -1 or r != sa: findings.append(f"TABLE 1 (zero divisor, signed) {L} {a:#x}: q={q} r={r}")
                if qu != (1 << L) - 1 or ru != ua: findings.append(f"TABLE 1 (zero divisor, unsigned) {L} {a:#x}")
                continue
            if sa == -(1 << (L - 1)) and sb == -1:
                if q != sa or r != 0: findings.append(f"TABLE 1 (overflow) {L}: q={q} r={r}")
            else:
                if sb * q + r != sa: findings.append(f"IDENTITY div/rem {L} {a:#x} {b:#x}: {sb}*{q}+{r} != {sa}")
                if abs(r) >= abs(sb): findings.append(f"REMAINDER TOO LARGE {L} {a:#x} {b:#x}")
                if r and (r < 0) != (sa < 0): findings.append(f"REMAINDER SIGN {L} {a:#x} {b:#x}: r={r}, dividend {sa}")
            if ub * qu + ru != ua or ru >= ub: findings.append(f"IDENTITY divu/remu {L} {a:#x} {b:#x}")
        lo = R("mul", a, b)
        if (R("mulhu", a, b) << 64 | lo) != a * b: findings.append(f"PRODUCT mulhu:mul {a:#x} {b:#x}")
        if s(R("mulh", a, b), 64) * (1 << 64) + lo != s(a, 64) * s(b, 64): findings.append(f"PRODUCT mulh:mul {a:#x} {b:#x}")
        if s(R("mulhsu", a, b), 64) * (1 << 64) + lo != s(a, 64) * b: findings.append(f"PRODUCT mulhsu:mul {a:#x} {b:#x}")
        if s(R("mulw", a, b), 64) != s(s(a, 32) * s(b, 32), 32): findings.append(f"PRODUCT mulw {a:#x} {b:#x}")
for f in findings[:12]:
    print("  " + f)
print(f"M-VECTORS: {'FAIL' if findings else 'ok'} ({text.count(chr(10)) - 7} vectors "
      f"{'DRIFTED from' if drift else 'in sync with'} the generator; "
      f"the reference judged on {len(ops)}x48 operand pairs at both widths; {len(findings)} finding(s))")
sys.exit(1 if findings else 0)
"#;

/// `python3 - <args> <<'PY' … PY` from the repository root, stdout and stderr together as `2>&1` joined them.
fn judge(repo: &Path, generator: &Path, table: &Path) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(generator)
        .arg(table)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(JUDGE.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&o.stderr));
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `python3 <gen.py> --out <table> >/dev/null`: a copy of the generator writes its own table.
fn generate(repo: &Path, generator: &Path, table: &Path) {
    let _ = Command::new("python3")
        .arg(generator)
        .arg("--out")
        .arg(table)
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .status();
}

/// `sed 's/PAT/REPL/' src > dst`: the first occurrence on every line, the patterns being literal text.
fn mutate(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        out.push_str(&line.replacen(pattern, replacement, 1));
    }
    let _ = fs::write(dst, out);
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
    /// Every missed arm's report, for a quiet run's refusal (`XTASK.12`).
    misses: Vec<String>,
}

impl Tally {
    /// A missed arm's report: printed at once in a verbose run, kept for a quiet run's refusal (`XTASK.12`).
    fn report(&mut self, report: String) {
        if self.verbose {
            eprintln!("{report}");
        }
        self.misses.push(report);
    }
    /// One arm: the judge's exit status must be `expected` and its output must contain `want`.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report(format!("M-VECTORS self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{}", captured(out)));
        }
    }
}

/// The RED/GREEN controls over copies, never the live files, each judged against a table the copy itself generated.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "mvectors") else {
        eprintln!(
            "M-VECTORS self-test: cannot create a scratch directory under target/doctrine-selftest"
        );
        return false;
    };
    let gen = t.join("gen.py");
    let table = t.join("table.txt");
    let _ = fs::copy(repo.join(GENERATOR), &gen);
    generate(repo, &gen, &table);
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    let (rc, out) = judge(repo, &gen, &table);
    tally.arm(
        "GREEN the generator's own table, its reference obeying the chapter",
        rc,
        0,
        &out,
        "0 finding(s)",
    );
    // `sed -i '0,/^div … 8000000000000000$/s//div … 0/'`: the first line that is the overflow vector, replaced.
    let text = fs::read_to_string(&table).unwrap_or_default();
    let mut edited = String::with_capacity(text.len());
    let mut done = false;
    for line in text.split_inclusive('\n') {
        if !done
            && line.trim_end_matches('\n')
                == "div 8000000000000000 ffffffffffffffff 8000000000000000"
        {
            edited.push_str("div 8000000000000000 ffffffffffffffff 0\n");
            done = true;
        } else {
            edited.push_str(line);
        }
    }
    let _ = fs::write(&table, edited);
    let (rc, out) = judge(repo, &gen, &table);
    tally.arm(
        "RED a hand-edited vector (the overflow quotient) is DRIFT",
        rc,
        1,
        &out,
        "DRIFT",
    );
    generate(repo, &gen, &table);
    let source = repo.join(GENERATOR);
    mutate(
        &source,
        &t.join("floor.py"),
        "    return q if (a < 0) == (b < 0) else -q",
        "    return a // b",
    );
    let (rc, out) = judge(repo, &t.join("floor.py"), &table);
    tally.arm(
        "RED a reference that FLOORS (Python's //) breaks the remainder's sign rule",
        rc,
        1,
        &out,
        "REMAINDER SIGN",
    );
    mutate(
        &source,
        &t.join("zero.py"),
        "        r = -1 if sb == 0 else",
        "        r = 0 if sb == 0 else",
    );
    let (rc, out) = judge(repo, &t.join("zero.py"), &table);
    tally.arm(
        "RED a reference whose zero divisor yields 0 breaks Table 1",
        rc,
        1,
        &out,
        "TABLE 1 (zero divisor, signed)",
    );
    mutate(
        &source,
        &t.join("hsu.py"),
        "        r = (sa * ub) >> 64",
        "        r = (sa * sb) >> 64",
    );
    let (rc, out) = judge(repo, &t.join("hsu.py"), &table);
    tally.arm(
        "RED a reference reading MULHSU's rs2 signed breaks the product split",
        rc,
        1,
        &out,
        "PRODUCT mulhsu:mul",
    );
    mutate(&source, &t.join("noext.py"), "    if word:                                              # \"sign-extend the 32-bit result\"", "    if False:");
    let (rc, out) = judge(repo, &t.join("noext.py"), &table);
    tally.arm(
        "RED a reference that does not sign-extend the word result",
        rc,
        1,
        &out,
        "NOT SIGN-EXTENDED",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "M-VECTORS --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    } else {
        // A quiet run names every missed arm before the caller's refusal line (`XTASK.12`).
        for report in &tally.misses {
            eprintln!("{report}");
        }
    }
    tally.fail == 0
}

/// `cargo xtask check-m-vectors [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Judge FIRST: a finding is a verdict on its own; only a PASS needs the controls' proof.
    // The paths as the script passed them, relative to the root — the DRIFT line prints the table's.
    let (rc, out) = judge(root, Path::new(GENERATOR), Path::new(TABLE));
    let out = captured(&out);
    if rc != 0 {
        eprintln!("{out}");
        return ExitCode::from(1);
    }
    if !self_test(root, false) {
        eprintln!("M-VECTORS: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    println!("{out}");
    ExitCode::SUCCESS
}
