//! The `CITATION-QUOTES` doctrine's driver, ported from `scripts/check_citation_quotes.sh` (`XTASK.6` slice `6r`),
//! which is now a shim of `cargo xtask check-citation-quotes`.
//!
//! Every quoted phrase a tracked `.sexp` or live `.md` attributes to a pinned section must occur IN that section —
//! `scripts/check_citation_quotes.py`, the pinned Python tool, decides it (the attribution rules and the matching
//! normalization are its docstring's); `check_citations.py` proves a locator EXISTS, this proves the quote under it is
//! THERE. The tool is spawned exactly as the driver spawned it and is not ported; the driver's two inline Python
//! controls (the source-availability probe and the altered-bytes identity control) run verbatim through `python3 -`.
//! HONEST LIMITS, the script's: quotes only, never paraphrase; a quote with no decidable attribution is counted, never
//! judged; PDF pins are counted UNCHECKABLE by name; a clone without the pinned pages prints a NAMED SKIP, never a pass.
//! Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, scratch};

const TOOL: &str = "scripts/check_citation_quotes.py";

/// The availability probe: `check_citations`' own cache route — the fetched working area, else the
/// manifest-verified materials cache. 0 present, 1 absent, 2 cannot be judged. Since `XTASK.11` slice a (ruling 5,
/// `decision_doctrine-controls-refuse-and-freeze.md`) any exception outside the named refusals is a crash the probe
/// cannot judge past — exit 2 — never the exit 1 that means "absent" (a truncated manifest's `DossierError` was read as
/// absence, measured in `XTASK.6` slice 6r).
const AVAILABILITY: &str = r#"import sys
sys.path.insert(0, "scripts")
import check_citations as C
import sexp
try:
    available = C.artifacts_available()
except (C.CitationError, sexp.SexpError, KeyError, OSError) as exc:
    print(exc)
    sys.exit(2)
except Exception as exc:
    print(f"{type(exc).__name__}: {exc}")
    sys.exit(2)
sys.exit(0 if available else 1)
"#;

/// The identity control, verbatim: a page whose bytes differ from its pinned digest must be refused, not judged.
const IDENTITY: &str = r#"import hashlib, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import check_citations as C
import check_citation_quotes as Q
root = Path(sys.argv[1])
(root / "profiles/p").mkdir(parents=True)
(root / "w").mkdir()
original = '<h2>1.1. Alpha</h2><p>The quick brown fox.</p>'
(root / "w/a.html").write_text(original.replace("brown", "black"))
digest = hashlib.sha256(original.encode()).hexdigest()
(root / "profiles/p/sources.sexp").write_text(
    f'(sources (work_dir "w") (source (id "SPEC") (file "a.html") '
    f'(sha256 "{digest}") (bytes {len(original.encode())})))\n')
C.REPO = Q.REPO = root
try:
    Q.corpus_pages()
except C.CitationError as exc:
    print(exc)
    sys.exit(1)
print("accepted altered quote page")
"#;

const SKIP: &str = "CITATION-QUOTES: NAMED SKIP — the pinned pages are absent (neither the fetched working area nor the materials cache); quotes cannot be judged offline. Run scripts/materials.py --fetch.";

/// The tool, spawned as the driver spawned it (`python3 scripts/check_citation_quotes.py …`, stdout and stderr together).
fn tool(repo: &Path, args: &[&str]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg(TOOL)
            .args(args)
            .current_dir(repo),
    )
}

/// `python3 - <args> <<'PY' … PY`: a program on stdin, from the repository root. With `both`, stdout and stderr
/// together as `2>&1` joined them; without, stdout alone, stderr passing through as the shell's did.
fn python_program(repo: &Path, program: &str, args: &[&str], both: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .args(args)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if both {
            Stdio::piped()
        } else {
            Stdio::inherit()
        });
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(program.as_bytes());
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

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the run's exit status must be `expected` and its output must contain `want`.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("CITATION-QUOTES self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{}", captured(out));
            }
        }
    }
}

fn write(path: &Path, text: &str) {
    let _ = fs::write(path, text);
}

/// The RED/GREEN controls over a synthetic artifact (numbered sections, a descendant, the two measured renderings, a
/// possessive) — never the cache.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "citquotes") else {
        eprintln!("CITATION-QUOTES self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("pages"));
    write(
        &t.join("pages/SPEC.html"),
        "<h2>1.1. Alpha</h2><p>The quick brown fox jumps over the lazy dog; the fox&#8217;s tail is long.</p>\n<h3>1.1.1. Alpha detail</h3><p>Stores the address (<code>'pc'</code>+4) into rd. Range 7&#8212;&#8203;5 bits.</p>\n<h2>1.2. Beta</h2><p>Implementations shall ignore writes to these bits.</p>\n",
    );
    write(&t.join("pages/PDFDOC.pdf"), "");
    let pages = t.join("pages").display().to_string();
    let judge = |name: &str, ext: &str, text: &str| -> (i32, String) {
        let file = t.join(format!("{name}.{ext}"));
        write(&file, &format!("{text}\n"));
        tool(repo, &["--pages", &pages, &file.display().to_string()])
    };
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let (rc, out) = judge(
        "green",
        "sexp",
        "(doc (statement \"The rule: 'the quick brown fox jumps' (SPEC §1.1).\"))",
    );
    tally.arm(
        "GREEN an R1 quote that is in its cited section passes",
        rc,
        0,
        &out,
        "1 attributed quote(s) judged (R1 1",
    );
    let (rc, out) = judge("sub", "sexp", "(doc (statement \"'Stores the address (pc+4) into rd' (SPEC §1.1), and 'Range 7-5 bits' (SPEC §1.1.1).\"))");
    tally.arm("GREEN a section includes its descendants; code-literal quotes, zero-width space and dashes fold", rc, 0, &out, "2 attributed quote(s) judged (R1 2");
    let (rc, out) = judge(
        "miss",
        "sexp",
        "(doc (statement \"'shall ignore writes to these bits' (SPEC §1.1)\"))",
    );
    tally.arm(
        "RED a quote under the wrong section is refused, naming where it is",
        rc,
        1,
        &out,
        "is not in SPEC §1.1 — found in §1.2",
    );
    let (rc, out) = judge(
        "nowhere",
        "sexp",
        "(doc (statement \"'a sentence the page never says' (SPEC §1.1)\"))",
    );
    tally.arm(
        "RED a quote the artifact never says is refused as such",
        rc,
        1,
        &out,
        "found nowhere in the cited artifact",
    );
    let (rc, out) = judge(
        "unresolved",
        "sexp",
        "(doc (statement \"'the quick brown fox' (SPEC §9.9)\"))",
    );
    tally.arm(
        "RED a quote under a section the artifact lacks is UNRESOLVED",
        rc,
        1,
        &out,
        "UNRESOLVED",
    );
    let (rc, out) = judge(
        "order",
        "sexp",
        "(doc (statement \"'lazy dog … quick brown' (SPEC §1.1)\"))",
    );
    tally.arm(
        "RED ellipsis pieces out of order are refused",
        rc,
        1,
        &out,
        "is not in SPEC §1.1",
    );
    let (rc, out) = judge(
        "inorder",
        "sexp",
        "(doc (statement \"'quick brown … [it] … lazy dog' (SPEC §1.1)\"))",
    );
    tally.arm(
        "GREEN ellipsis and editorial-bracket pieces in order pass",
        rc,
        0,
        &out,
        "0 finding(s)",
    );
    let (rc, out) = judge(
        "r2",
        "sexp",
        "(doc (rule (source \"SPEC §1.1 — 'shall ignore writes to these bits'\")))",
    );
    tally.arm(
        "RED an R2 quote in a (source …) is judged under its leading locator",
        rc,
        1,
        &out,
        "[R2]",
    );
    let (rc, out) = judge("r3", "sexp", "(expectations (step (n 0) (derivation \"x — 'shall ignore writes to these bits'\") (source \"SPEC §1.1\")))");
    tally.arm(
        "RED an R3 derivation quote is judged under its step's source",
        rc,
        1,
        &out,
        "[R3]",
    );
    let (rc, out) = judge("r4", "sexp", "(doc (statement \"Per SPEC §1.2 the rule holds: 'implementations shall ignore' — always.\"))");
    tally.arm(
        "GREEN an R4 quote in a single-locator string is judged and passes",
        rc,
        0,
        &out,
        "(R1 0, R2 0, R3 0, R4 1)",
    );
    let (rc, out) = judge(
        "multi",
        "sexp",
        "(doc (statement \"SPEC §1.1 or SPEC §1.2: 'never in the page at all' — no adjacency.\"))",
    );
    tally.arm(
        "GREEN a quote beside two locators is counted, never judged",
        rc,
        0,
        &out,
        "1 unattributed",
    );
    let (rc, out) = judge(
        "possessive",
        "sexp",
        "(doc (statement \"'the fox's nose is long' (SPEC §1.1)\"))",
    );
    tally.arm(
        "RED a possessive stays inside the phrase (the whole quote is judged)",
        rc,
        1,
        &out,
        "'the fox's nose is long'",
    );
    let (rc, out) = judge(
        "pdf",
        "sexp",
        "(doc (statement \"'anything at all in a manual' (PDFDOC §2)\"))",
    );
    tally.arm(
        "GREEN a quote under a PDF pin is counted UNCHECKABLE by name",
        rc,
        0,
        &out,
        "PDFDOC ×1",
    );
    // ── Markdown (CITATION-ACCURACY.2): the two adjacency shapes; code, prose-distance and wraps ──
    let (rc, out) = judge(
        "md-r1",
        "md",
        "The rule: \"the quick brown fox jumps\" (SPEC §1.1).",
    );
    tally.arm(
        "GREEN an MD-R1 quote followed by its locator passes",
        rc,
        0,
        &out,
        "(MD-R1 1, MD-R5 0)",
    );
    let (rc, out) = judge(
        "md-r1-wrong",
        "md",
        "It says \"Implementations shall ignore writes\" (SPEC §1.1).",
    );
    tally.arm(
        "RED an MD-R1 quote under the wrong section is refused, naming where it is",
        rc,
        1,
        &out,
        "is not in SPEC §1.1 — found in §1.2",
    );
    let (rc, out) = judge(
        "md-r5",
        "md",
        "SPEC §1.1's \"the lazy dog\" is the sentence's end.",
    );
    tally.arm(
        "GREEN an MD-R5 possessive locator before its quote passes",
        rc,
        0,
        &out,
        "(MD-R1 0, MD-R5 1)",
    );
    let (rc, out) = judge(
        "md-r5-wrong",
        "md",
        "SPEC §1.2's \"quick brown fox\" is elsewhere.",
    );
    tally.arm(
        "RED an MD-R5 quote under the wrong section is refused",
        rc,
        1,
        &out,
        "found in §1.1",
    );
    let (rc, out) = judge(
        "md-code",
        "md",
        "A code span: `\"never in the page at all\"` (SPEC §1.1) is not a quotation.",
    );
    tally.arm(
        "GREEN a quote inside a code span is not judged",
        rc,
        0,
        &out,
        "0 attributed quote(s) judged (MD-R1 0, MD-R5 0)",
    );
    let (rc, out) = judge("md-prose", "md", "SPEC §1.1 describes the fox. The laboratory calls the outcome \"nothing retired\" in its own words.");
    tally.arm(
        "GREEN a quote in a one-locator paragraph is counted, never judged",
        rc,
        0,
        &out,
        "1 counted (a locator near, no adjacency)",
    );
    let (rc, out) = judge(
        "md-wrap",
        "md",
        "As written, \"the quick brown\nfox jumps\" (SPEC §1.1) wraps a line.",
    );
    tally.arm(
        "GREEN a quoted phrase that wraps a line stays one phrase",
        rc,
        0,
        &out,
        "(MD-R1 1, MD-R5 0); 0 finding(s)",
    );
    let (rc, out) = tool(repo, &["--bogus"]);
    tally.arm(
        "RED an unknown invocation is refused, not judged",
        rc,
        2,
        &out,
        "Usage:",
    );
    let (rc, out) = python_program(
        repo,
        IDENTITY,
        &[&t.join("identity").display().to_string()],
        true,
    );
    tally.arm(
        "RED the default quote corpus refuses altered source bytes",
        rc,
        1,
        &out,
        "sha256",
    );
    // XTASK.11 slice a (ruling 5): the availability probe's own exits, with its call patched — an unexpected
    // exception refuses (2); only a recognised absence is the named skip's 1.
    let patched = |body: &str| {
        format!(
            "import sys\nsys.path.insert(0, \"scripts\")\nimport check_citations as C\ndef _patched():\n{body}\nC.artifacts_available = _patched\n{AVAILABILITY}"
        )
    };
    let (rc, out) = python_program(
        repo,
        &patched("    raise ValueError(\"a foreign failure\")"),
        &[],
        true,
    );
    tally.arm(
        "RED an unexpected exception in the availability probe refuses, never reads as absent",
        rc,
        2,
        &out,
        "ValueError: a foreign failure",
    );
    let (rc, out) = python_program(repo, &patched("    return False"), &[], true);
    tally.arm(
        "GREEN a recognised absence is the availability probe's exit 1, the named skip",
        rc,
        1,
        &out,
        "",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "CITATION-QUOTES --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-citation-quotes [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Re-run the controls before judging: a check that no longer discriminates must refuse, not pass.
    if !self_test(root, false) {
        eprintln!("CITATION-QUOTES: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    // The cache route: neither the fetched working area nor the materials cache → a NAMED SKIP, never a pass.
    let (rc, out) = python_program(root, AVAILABILITY, &[], false);
    if rc == 1 {
        println!("{SKIP}");
        return ExitCode::SUCCESS;
    }
    if rc != 0 {
        eprintln!(
            "CITATION-QUOTES: REFUSED — source availability cannot be judged: {}",
            captured(&out)
        );
        return ExitCode::from(2);
    }
    let (rc, out) = tool(root, &[]);
    let out = captured(&out);
    if rc != 0 {
        eprintln!("{out}");
        if rc == 2 {
            eprintln!("CITATION-QUOTES: REFUSED — source evidence cannot be judged.");
            return ExitCode::from(2);
        }
        eprintln!("CITATION-QUOTES: FAIL — a quoted phrase is not in the section its locator names. Re-cite it (the finding names where the phrase is) — never loosen the match.");
        return ExitCode::from(u8::try_from(rc).unwrap_or(1));
    }
    println!("{}", out.rsplit('\n').next().unwrap_or(""));
    ExitCode::SUCCESS
}
