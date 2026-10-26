//! The `REGISTRY-MIRROR` doctrine, ported from `scripts/check_registry_mirror.sh` (`XTASK.6` slice `6i`), which
//! is now a shim of `cargo xtask check-registry-mirror`.
//!
//! The doctrine registry lives in two shell arrays — the universal one in `scripts/check_doctrines.sh`, this
//! project's own in `scripts/check_doctrines.project.sh` — and two documents restate it for humans:
//! `DOCTRINE_ENFORCEMENT.md` and the mdBook chapter `docs/book/src/working/doctrines.md`; the partitioned
//! family files under `docs/doctrines/` restate the project's doctrines only, so their union is judged as a
//! project-scoped mirror. The book is the review surface — the director reads the book, not the code — and a
//! mirror that falls behind under-reports the project's guarantees in the direction that looks fine. Compared:
//! COVERAGE (every registered id has a row in both mirrors), PHANTOM (every id-shaped row is registered),
//! SECTION (a project doctrine is listed under the project heading, a universal one is not), EXECUTABLE
//! (every registered path exists and is executable), COUNT (a sentence `<N> checks run today` states the
//! real universal count, spelled or in digits). It refuses when either driver yields no registry entry.
//! The script's inline Python is ported with it, its three regular expressions matched by hand (no new
//! crate). Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

use crate::harness::{locale_sorted, py_splitlines, py_strip, scratch};

/// The universal registry, relative to the repository root.
const UNIVERSAL: &str = "scripts/check_doctrines.sh";
/// The project registry.
const PROJECT: &str = "scripts/check_doctrines.project.sh";
/// The two documents that restate the whole registry.
const MIRRORS: &[&str] = &[
    "DOCTRINE_ENFORCEMENT.md",
    "docs/book/src/working/doctrines.md",
];
/// The partitioned long-form rows' union (`LIVE-CONTAINMENT.3`), a project-scoped mirror the check writes.
const UNION: &str = "target/registry-mirror/docs-doctrines-union.md";
/// The spelled counts the COUNT sentence may use, by value.
const WORDS: [&str; 26] = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "twentyone",
    "twentytwo",
    "twentythree",
    "twentyfour",
    "twentyfive",
];

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 a document no longer mirrors the registry, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join(UNIVERSAL).is_file() {
        println!("REGISTRY-MIRROR: ok (no driver yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("REGISTRY-MIRROR: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let mut mirrors: Vec<(String, bool)> =
        MIRRORS.iter().map(|m| ((*m).to_owned(), false)).collect();
    if root.join("docs/doctrines").is_dir() {
        // The partitioned long-form rows: their UNION is a project-scoped mirror, so a doctrine registered
        // without its long-form row — in any family — is NOT MIRRORED. Written as the script's `cat` wrote it:
        // the family files in the shell's collation order.
        let mut names: Vec<String> = fs::read_dir(root.join("docs/doctrines"))
            .map(|entries| {
                entries
                    .flatten()
                    .map(|entry| entry.file_name().to_string_lossy().into_owned())
                    .filter(|name| name.ends_with(".md") && !name.starts_with('.'))
                    .collect()
            })
            .unwrap_or_default();
        names = locale_sorted(names);
        let mut union = Vec::new();
        for name in &names {
            if let Ok(bytes) = fs::read(root.join("docs/doctrines").join(name)) {
                union.extend_from_slice(&bytes);
            }
        }
        let path = root.join(UNION);
        if let Some(parent) = path.parent() {
            let _ = fs::create_dir_all(parent);
        }
        let _ = fs::write(&path, union);
        mirrors.push((path.to_string_lossy().into_owned(), true));
    }
    let verdict = check_mirror(root, UNIVERSAL, PROJECT, &mirrors);
    if verdict.rc == 2 {
        eprintln!("REGISTRY-MIRROR: REFUSED — the registry could not be read, so its mirrors cannot be judged.");
        for line in &verdict.findings {
            eprintln!("  {line}");
        }
        return ExitCode::from(2);
    }
    if verdict.rc != 0 {
        eprintln!("REGISTRY-MIRROR: a doctrine document no longer mirrors the enforcer registry.");
        for line in &verdict.findings {
            eprintln!("  {line}");
        }
        eprintln!("  The REGISTRY is authoritative. Add the row — never drop a registration to match a document.");
        return ExitCode::from(1);
    }
    println!(
        "REGISTRY-MIRROR: ok ({} document(s) mirror the registry)",
        verdict.checked
    );
    ExitCode::SUCCESS
}

/// What the script's `check_mirror` printed and returned.
struct Verdict {
    findings: Vec<String>,
    checked: usize,
    rc: i32,
}

impl Verdict {
    fn text(&self) -> String {
        let mut lines = self.findings.clone();
        lines.push(format!("__CHECKED__ {}", self.checked));
        lines.join("\n")
    }
}

/// The last path component, as `pathlib.Path(...).name`.
fn basename(path: &str) -> &str {
    path.trim_end_matches('/')
        .rsplit('/')
        .next()
        .unwrap_or(path)
}

/// The script's Python over the two registries and the mirrors (`(path as given, project-scoped)`).
fn check_mirror(
    root: &Path,
    universal_path: &str,
    project_path: &str,
    mirrors: &[(String, bool)],
) -> Verdict {
    let universal = registry(&root.join(universal_path));
    let project = registry(&root.join(project_path));
    if universal.is_empty() || project.is_empty() {
        return Verdict {
            findings: vec![format!(
                "NO REGISTRY universal={} project={} — the registry format changed; this check cannot judge",
                universal.len(),
                project.len()
            )],
            checked: 0,
            rc: 2,
        };
    }
    let mut registered = universal.clone();
    registered.extend(project.iter().map(|(k, v)| (k.clone(), v.clone())));
    let mut findings = Vec::new();

    // 4. EXECUTABLE
    for (did, rel) in &registered {
        let p = root.join(rel);
        match fs::metadata(&p) {
            Ok(meta) if meta.is_file() => {
                if !executable(&meta) {
                    findings.push(format!(
                        "NOT EXECUTABLE {did}: {rel} is registered but not executable"
                    ));
                }
            }
            _ => findings.push(format!(
                "NO CHECK   {did}: registry names {rel}, which does not exist"
            )),
        }
    }

    let mut checked = 0;
    for (mirror, project_scoped) in mirrors {
        let name = basename(mirror);
        let path = root.join(mirror);
        if !path.is_file() {
            findings.push(format!("NO MIRROR  {mirror} does not exist"));
            continue;
        }
        checked += 1;
        let text = fs::read(&path).map_or_else(
            |_| String::new(),
            |b| String::from_utf8_lossy(&b).into_owned(),
        );
        let lines = py_splitlines(&text);
        // which lines sit under a heading that announces the PROJECT's own doctrines
        let mut listed: BTreeMap<String, bool> = BTreeMap::new();
        let mut flag = false;
        for line in &lines {
            if line.starts_with('#') {
                flag = project_heading(line);
            }
            if let Some(id) = row_id(line) {
                listed.insert(id, flag);
            }
        }
        // 1. COVERAGE
        let expected = if *project_scoped {
            &project
        } else {
            &registered
        };
        for did in expected.keys() {
            if !listed.contains_key(did) {
                findings.push(format!(
                    "NOT MIRRORED {name}: '{did}' is registered and has no row — the document under-reports what this repository enforces"
                ));
            }
        }
        // 2. PHANTOM
        for did in listed.keys() {
            if !registered.contains_key(did) {
                findings.push(format!(
                    "PHANTOM    {name}: '{did}' has a row but is registered nowhere"
                ));
            }
        }
        // 3. SECTION
        for (did, under_project) in &listed {
            if project.contains_key(did) && !under_project {
                findings.push(format!(
                    "WRONG SECTION {name}: '{did}' is a project doctrine listed outside the project section"
                ));
            }
            if universal.contains_key(did) && !project.contains_key(did) && *under_project {
                findings.push(format!(
                    "WRONG SECTION {name}: '{did}' is universal but listed under the project section"
                ));
            }
        }
        // 5. COUNT
        for raw in count_sentences(&text) {
            let got = if raw.chars().all(|c| c.is_ascii_digit()) {
                raw.parse::<usize>().ok()
            } else {
                WORDS.iter().position(|w| *w == raw.to_lowercase())
            };
            match got {
                None => findings.push(format!(
                    "UNREADABLE COUNT {name}: '{raw} checks run today' is not a number"
                )),
                Some(n) if n != universal.len() => findings.push(format!(
                    "COUNT DRIFT {name}: '{raw} checks run today' — {} are registered in {}",
                    universal.len(),
                    basename(universal_path)
                )),
                Some(_) => {}
            }
        }
    }
    let rc = i32::from(!findings.is_empty());
    Verdict {
        findings,
        checked,
        rc,
    }
}

/// A registry file's `id → path` entries: on each non-comment line, the first quoted
/// `"ID|what it proves|path/to/check.sh"` triple (`ENTRY.search`), later lines overriding earlier ids.
fn registry(path: &Path) -> BTreeMap<String, String> {
    let mut out = BTreeMap::new();
    if !path.is_file() {
        return out;
    }
    let text = fs::read(path).map_or_else(
        |_| String::new(),
        |b| String::from_utf8_lossy(&b).into_owned(),
    );
    for line in py_splitlines(&text) {
        if py_strip(line).starts_with('#') {
            continue;
        }
        if let Some((id, check)) = entry(line) {
            out.insert(id, check);
        }
    }
    out
}

/// `[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*` at the start of `s`: the id and its length in bytes.
fn doctrine_id(s: &str) -> Option<&str> {
    let bytes = s.as_bytes();
    if !bytes.first().is_some_and(u8::is_ascii_uppercase) {
        return None;
    }
    let alnum = |b: &u8| b.is_ascii_uppercase() || b.is_ascii_digit();
    let mut end = 1;
    while bytes.get(end).is_some_and(alnum) {
        end += 1;
    }
    while bytes.get(end) == Some(&b'-') && bytes.get(end + 1).is_some_and(alnum) {
        end += 1;
        while bytes.get(end).is_some_and(alnum) {
            end += 1;
        }
    }
    Some(&s[..end])
}

/// The first `"ID|proves|path.sh"` triple in a line, as the script's `ENTRY` regular expression found it.
fn entry(line: &str) -> Option<(String, String)> {
    for (at, _) in line.match_indices('"') {
        let rest = &line[at + 1..];
        let Some(id) = doctrine_id(rest) else {
            continue;
        };
        let Some(rest) = rest[id.len()..].strip_prefix('|') else {
            continue;
        };
        let proves_end = rest.find(['"', '|']);
        let Some(rest) = proves_end.and_then(|e| rest[e..].strip_prefix('|')) else {
            continue;
        };
        let Some(path_end) = rest.find(['"', '|']) else {
            continue;
        };
        let check = &rest[..path_end];
        if rest[path_end..].starts_with('"') && check.ends_with(".sh") {
            return Some((id.to_owned(), check.to_owned()));
        }
    }
    None
}

/// The id of a table row `| `ID` | …` (the script's `ROW.match`), if the line is one.
fn row_id(line: &str) -> Option<String> {
    let rest = line.strip_prefix('|')?;
    let rest = rest.trim_start_matches(py_space).strip_prefix('`')?;
    let id = doctrine_id(rest)?;
    let rest = rest[id.len()..].strip_prefix('`')?;
    rest.trim_start_matches(py_space)
        .starts_with('|')
        .then(|| id.to_owned())
}

/// Python's `\s` for `str` patterns.
fn py_space(c: char) -> bool {
    c.is_whitespace() || ('\u{1c}'..='\u{1f}').contains(&c)
}

/// Python's `\w` for `str` patterns: alphanumeric or underscore.
fn py_word(c: char) -> bool {
    c.is_alphanumeric() || c == '_'
}

/// Whether a heading announces the project's own doctrines (`project'?s? own doctrine`, case-insensitive).
fn project_heading(line: &str) -> bool {
    let lower = line.to_lowercase();
    lower.match_indices("project").any(|(at, word)| {
        let mut rest = &lower[at + word.len()..];
        if let Some(r) = rest.strip_prefix('\'') {
            rest = r;
        }
        if let Some(r) = rest.strip_prefix('s') {
            rest = r;
        }
        rest.starts_with(" own doctrine")
    })
}

/// Every `<N> checks run today` sentence's `<N>` (the script's `NUM.finditer`, case-insensitive, `\b` on both
/// sides): an ASCII-letter word or a digit run at a word boundary, then the three words.
fn count_sentences(text: &str) -> Vec<String> {
    let chars: Vec<char> = text.chars().collect();
    let mut found = Vec::new();
    let mut i = 0;
    while i < chars.len() {
        let boundary = i == 0 || !py_word(chars[i - 1]);
        let c = chars[i];
        if boundary && (c.is_ascii_alphabetic() || c.is_ascii_digit()) {
            let digits = c.is_ascii_digit();
            let mut end = i;
            while end < chars.len()
                && if digits {
                    chars[end].is_ascii_digit()
                } else {
                    chars[end].is_ascii_alphabetic()
                }
            {
                end += 1;
            }
            let raw: String = chars[i..end].iter().collect();
            let mut at = end;
            let mut ok = true;
            for word in ["checks", "run", "today"] {
                let start = at;
                while at < chars.len() && py_space(chars[at]) {
                    at += 1;
                }
                if at == start {
                    ok = false;
                    break;
                }
                let taken: String = chars[at..].iter().take(word.len()).collect();
                if taken.to_lowercase() != word {
                    ok = false;
                    break;
                }
                at += word.len();
            }
            if ok && (at >= chars.len() || !py_word(chars[at])) {
                found.push(raw);
                i = at;
                continue;
            }
        }
        i += 1;
    }
    found
}

/// Whether a file's mode lets someone execute it (`st_mode & 0o111`).
#[cfg(unix)]
fn executable(meta: &fs::Metadata) -> bool {
    use std::os::unix::fs::PermissionsExt as _;
    meta.permissions().mode() & 0o111 != 0
}

/// Without Unix modes (the wasm32 build of the workspace) a regular file is taken as executable.
#[cfg(not(unix))]
fn executable(_: &fs::Metadata) -> bool {
    true
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally<'a> {
    root: &'a Path,
    universal: &'a str,
    project: &'a str,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: judging the fixture registries against `mirror` must give `expected` and contain `want`.
    fn arm(&mut self, mirror: &(String, bool), name: &str, expected: i32, want: &str) {
        let verdict = check_mirror(
            self.root,
            self.universal,
            self.project,
            std::slice::from_ref(mirror),
        );
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "REGISTRY-MIRROR self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("REGISTRY-MIRROR self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// Makes a scratch file executable (the script's `chmod +x`); a no-op without Unix modes.
fn set_executable(path: &Path, on: bool) {
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt as _;
        if let Ok(meta) = fs::metadata(path) {
            let mode = meta.permissions().mode();
            let mode = if on { mode | 0o111 } else { mode & !0o111 };
            let _ = fs::set_permissions(path, fs::Permissions::from_mode(mode));
        }
    }
    #[cfg(not(unix))]
    {
        let _ = (path, on);
    }
}

/// The thirteen arms over scratch registries and mirrors. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(root, "target/doctrine-selftest", "registry-mirror") else {
        if verbose {
            eprintln!("REGISTRY-MIRROR self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let td = t.to_string_lossy().into_owned();
    let (a, b) = (t.join("a.sh"), t.join("b.sh"));
    let touch_exec = |path: &PathBuf| {
        let _ = fs::write(path, "");
        set_executable(path, true);
    };
    touch_exec(&a);
    touch_exec(&b);
    let u = format!("{td}/u.sh");
    let p = format!("{td}/p.sh");
    let mut tally = Tally {
        root,
        universal: &u,
        project: &p,
        pass: 0,
        fail: 0,
        verbose,
    };
    let drivers = || {
        let _ = fs::write(
            &u,
            format!("# \"ID|what it proves|relative/path/to/check.sh\"   <- format doc, must NOT count\nDOCTRINES=(\n  \"ALPHA|proves alpha|{td}/a.sh\"\n)\n"),
        );
        let _ = fs::write(
            &p,
            format!("PROJECT_DOCTRINES=(\n  \"BETA|proves beta|{td}/b.sh\"\n)\n"),
        );
    };
    let m_path = format!("{td}/M.md");
    let mirror = |body: &str| {
        let _ = fs::write(&m_path, format!("{body}\n"));
    };
    let m: (String, bool) = (m_path.clone(), false);
    let good = "## Registry\n\n| ID | Proves |\n| --- | --- |\n| `ALPHA` | alpha |\n\n### This project's own doctrines\n\n| ID | Proves |\n| --- | --- |\n| `BETA` | beta |\n\nOne checks run today.";
    drivers();
    mirror(good);
    tally.arm(&m, "GREEN both mirrored", 0, "__CHECKED__ 1");
    let without_beta: Vec<&str> = good.lines().filter(|l| !l.contains("`BETA`")).collect();
    mirror(&without_beta.join("\n"));
    tally.arm(&m, "RED   a registered id has no row", 1, "NOT MIRRORED");
    mirror(&format!("{good}\n| `GAMMA` | unregistered |"));
    tally.arm(&m, "RED   a row nothing registers", 1, "PHANTOM");
    mirror(&good.replace("\nOne checks", "\nSeven checks"));
    tally.arm(&m, "RED   the count sentence drifts", 1, "COUNT DRIFT");
    mirror(&good.replace("\nOne checks", "\nUmpteen checks"));
    tally.arm(&m, "RED   the count is not a number", 1, "UNREADABLE COUNT");
    mirror("## Registry\n\n| ID | Proves |\n| --- | --- |\n| `ALPHA` | alpha |\n| `BETA` | beta |\n\nOne checks run today.");
    tally.arm(
        &m,
        "RED   project doctrine outside its section",
        1,
        "WRONG SECTION",
    );
    mirror("### This project's own doctrines\n\n| ID | Proves |\n| --- | --- |\n| `ALPHA` | alpha |\n| `BETA` | beta |\n\nOne checks run today.");
    tally.arm(
        &m,
        "RED   universal doctrine inside the project section",
        1,
        "WRONG SECTION",
    );
    drivers();
    set_executable(&b, false);
    mirror(good);
    tally.arm(
        &m,
        "RED   a registered check is not executable",
        1,
        "NOT EXECUTABLE",
    );
    set_executable(&b, true);
    let _ = fs::remove_file(&b);
    mirror(good);
    tally.arm(&m, "RED   a registered check does not exist", 1, "NO CHECK");
    touch_exec(&b);
    let _ = fs::remove_file(&m_path);
    tally.arm(&m, "RED   the mirror file is missing", 1, "NO MIRROR");
    mirror(good);
    let _ = fs::write(&u, "DOCTRINES=(\n)\n");
    tally.arm(
        &m,
        "REFUSE the registry parses to nothing",
        2,
        "NO REGISTRY",
    );
    // The project-scoped mirror (LIVE-CONTAINMENT.3): the partitioned family union restates the project's
    // doctrines only — it is judged against the project registry, never the universal.
    drivers();
    let f_path = format!("{td}/F.md");
    let f: (String, bool) = (f_path.clone(), true);
    let _ = fs::write(&f_path, "# family\n\n## This project's own doctrines — f\n\n| ID | Proves |\n| --- | --- |\n| `BETA` | b |\n");
    tally.arm(
        &f,
        "GREEN a project-scoped mirror needs no universal row",
        0,
        "__CHECKED__ 1",
    );
    let _ = fs::write(
        &f_path,
        "# family\n\n## This project's own doctrines — f\n\n| ID | Proves |\n| --- | --- |\n",
    );
    tally.arm(
        &f,
        "RED   the family union lost a project doctrine",
        1,
        "NOT MIRRORED",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "REGISTRY-MIRROR --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_three_patterns_are_matched_as_python_matched_them() {
        assert_eq!(
            entry("  DOCTRINES+=(\"KNOWLEDGE-MAP|the derived map|knowledge-map/scripts/check_knowledge_map.sh\")"),
            Some(("KNOWLEDGE-MAP".to_owned(), "knowledge-map/scripts/check_knowledge_map.sh".to_owned()))
        );
        assert_eq!(
            entry("  \"lower|x|a.sh\" \"A1-B2|p|q.sh\""),
            Some(("A1-B2".to_owned(), "q.sh".to_owned()))
        );
        assert_eq!(entry("\"A-|p|q.sh\""), None);
        assert_eq!(entry("\"A|p|q.py\""), None);
        assert_eq!(row_id("|  `FOO-BAR`  | x |"), Some("FOO-BAR".to_owned()));
        assert_eq!(row_id("| `foo` | x |"), None);
        assert_eq!(row_id("| `FOO`x | x |"), None);
        assert!(
            project_heading("### This project's own doctrines (x)")
                && project_heading("## projects own doctrine")
        );
        assert!(!project_heading("## project doctrines"));
        assert_eq!(count_sentences("Thirteen checks run today. 7 CHECKS RUN TODAY; xthree checks run today; 4 checks run todays"), vec!["Thirteen", "7", "xthree"]);
        assert_eq!(WORDS.iter().position(|w| *w == "thirteen"), Some(13));
    }
}
