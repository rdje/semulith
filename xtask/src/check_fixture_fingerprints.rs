//! The `FIXTURE-FINGERPRINT` doctrine, ported from `scripts/check_fixture_fingerprints.sh` (`XTASK.6` slice
//! `6g`), which is now a shim of `cargo xtask check-fixture-fingerprints`.
//!
//! A data record that pins a file's SHA-256 makes a claim about the working tree that nothing re-derives by
//! itself (`docs/CLAIM_VERIFICATION.md` §5B: a constant that is a function of the repository is DERIVED or
//! GATED, never carried). The rule: in every tracked JSON/JSONL record, an object carrying BOTH `path` and
//! `sha256` names a file that exists, resolved against the record's own directory, whose content hashes to
//! that value. Not covered, deliberately: `docs/provenance/**` (`DELIVERY-PROVENANCE` knows row dispositions),
//! `vendor/` and `.app-data/` (other projects' trees, one of which once crashed the scan), `.git` and `target`.
//!
//! The script's inline Python is ported with it. JSON is read by a parser written here (no new crate) that
//! reports a malformed record with Python's `json` messages and positions, so an `UNPARSEABLE` finding reads
//! as before; hashing goes through `sha256sum` or `shasum -a 256` as `DELIVERY-PROVENANCE` does (the script
//! used Python's `hashlib`; the port refuses when neither hasher is on `PATH`). Each self-test arm is one
//! `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

use crate::harness::{py_splitlines, py_strip, scratch, Hasher};

/// Top-level directories the scan never enters, relative to the root (the script's `EXCLUDE`).
const EXCLUDE: &[&str] = &["docs/provenance", ".git", "target", "vendor", ".app-data"];

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 a record pins a fingerprint that no longer describes the tree, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    let Some(hasher) = Hasher::find() else {
        // A skip is never a pass: with no hasher this check cannot judge anything.
        eprintln!("FIXTURE-FINGERPRINT: REFUSED — no sha256sum or shasum on PATH; this check cannot judge.");
        return ExitCode::from(2);
    };
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, &hasher, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, &hasher, false) {
        eprintln!(
            "FIXTURE-FINGERPRINT: REFUSED — the check does not discriminate (self-test failed)."
        );
        return ExitCode::from(2);
    }
    let (findings, checked) = scan_tree(root, &hasher);
    if !findings.is_empty() {
        eprintln!(
            "FIXTURE-FINGERPRINT: a record pins a fingerprint that no longer describes the tree."
        );
        for finding in &findings {
            for line in finding.split('\n') {
                eprintln!("  {line}");
            }
        }
        eprintln!("  Re-derive the pin from the file, or fix the file — never edit the pin to silence this.");
        return ExitCode::from(1);
    }
    println!("FIXTURE-FINGERPRINT: ok ({checked} pinned fingerprint(s) re-derived)");
    ExitCode::SUCCESS
}

/// Every `.json`/`.jsonl` record under `root` (the script's `scan_tree`): the findings, in the order the
/// script printed them, and the number of pins checked.
fn scan_tree(root: &Path, hasher: &Hasher) -> (Vec<String>, usize) {
    let mut findings = Vec::new();
    let mut checked = 0;
    walk(root, root, hasher, &mut findings, &mut checked);
    (findings, checked)
}

/// One directory of the script's `os.walk`: its records in name order, then its subdirectories in listing
/// order, never entering `.git` or `target` and never following a link to a directory.
fn walk(root: &Path, dir: &Path, hasher: &Hasher, findings: &mut Vec<String>, checked: &mut usize) {
    if dir != root {
        let rel = relative(root, dir);
        if EXCLUDE
            .iter()
            .any(|e| rel == *e || rel.starts_with(&format!("{e}/")))
        {
            return; // the script pruned these subtrees by their root-relative path
        }
    }
    let Ok(entries) = fs::read_dir(dir) else {
        return; // os.walk ignores a directory it cannot list
    };
    let mut directories = Vec::new();
    let mut files = Vec::new();
    for entry in entries.flatten() {
        let name = entry.file_name().to_string_lossy().into_owned();
        let path = entry.path();
        // os.walk sorts an entry by `is_dir()`, which follows links; a link to a directory is listed but,
        // without followlinks, never walked.
        let is_dir = fs::metadata(&path).is_ok_and(|meta| meta.is_dir());
        if is_dir {
            let link = entry.file_type().is_ok_and(|kind| kind.is_symlink());
            if !link && name != ".git" && name != "target" {
                directories.push(path);
            }
        } else {
            files.push((name, path));
        }
    }
    files.sort_by(|a, b| a.0.cmp(&b.0));
    for (name, path) in files {
        if !(name.ends_with(".json") || name.ends_with(".jsonl")) {
            continue;
        }
        let shown = relative(root, &path);
        let Ok(bytes) = fs::read(&path) else {
            continue; // the script would have crashed here; nothing to judge in an unreadable record
        };
        let text = String::from_utf8_lossy(&bytes);
        let parent = path.parent().unwrap_or(root);
        for (lineno, outcome) in records(&text, name.ends_with(".jsonl")) {
            let record = match outcome {
                Ok(record) => record,
                Err(error) => {
                    // the script named an unparseable record by its full path (`fp`), the others by
                    // their root-relative one (`shown`)
                    let full = path.display();
                    findings.push(if name.ends_with(".jsonl") {
                        format!("UNPARSEABLE {full}:{lineno} — {error}")
                    } else {
                        format!("UNPARSEABLE {full} — {error}")
                    });
                    continue;
                }
            };
            let mut found = Vec::new();
            pins(&record, &mut found);
            for (pin, want) in found {
                *checked += 1;
                let where_ = format!("{shown}:{lineno}");
                if want.chars().count() != 64
                    || !want
                        .chars()
                        .all(|c| c.is_ascii_digit() || ('a'..='f').contains(&c))
                {
                    findings.push(format!(
                        "MALFORMED {where_} — sha256 '{want}' is not 64 lowercase hex"
                    ));
                    continue;
                }
                let target = parent.join(&pin);
                if !fs::metadata(&target).is_ok_and(|meta| meta.is_file()) {
                    findings.push(format!(
                        "MISSING   {where_} — pins '{pin}', which does not exist"
                    ));
                    continue;
                }
                let got = hasher.digest(&target);
                if got != want {
                    findings.push(format!(
                        "DRIFTED   {where_} — '{pin}'\n    pinned  {want}\n    current {got}"
                    ));
                }
            }
        }
    }
    for path in directories {
        walk(root, &path, hasher, findings, checked);
    }
}

/// The records of one file with their line numbers: each non-blank line of a `.jsonl`, or the whole text as
/// line 1 (the script's `records`).
fn records(text: &str, jsonl: bool) -> Vec<(usize, Result<Json, String>)> {
    if jsonl {
        py_splitlines(text)
            .into_iter()
            .enumerate()
            .filter_map(|(i, line)| {
                let line = py_strip(line);
                (!line.is_empty()).then(|| (i + 1, parse(line)))
            })
            .collect()
    } else {
        vec![(1, parse(text))]
    }
}

/// Every object carrying BOTH `path` and `sha256` as strings, anywhere in the structure, in the order
/// Python's `dict.values()` and `list` iteration reached them.
fn pins(value: &Json, out: &mut Vec<(String, String)>) {
    match value {
        Json::Object(pairs) => {
            if let (Some(Json::Str(path)), Some(Json::Str(sha))) =
                (lookup(pairs, "path"), lookup(pairs, "sha256"))
            {
                out.push((path.clone(), sha.clone()));
            }
            for (_, item) in pairs {
                pins(item, out);
            }
        }
        Json::Array(items) => {
            for item in items {
                pins(item, out);
            }
        }
        _ => {}
    }
}

/// A member by key; the pairs hold one entry per key (the last value, at the first position), as a `dict`.
fn lookup<'a>(pairs: &'a [(String, Json)], key: &str) -> Option<&'a Json> {
    pairs.iter().find(|(k, _)| k == key).map(|(_, v)| v)
}

/// A path relative to the root, as `os.path.relpath` showed it.
fn relative(root: &Path, path: &Path) -> String {
    path.strip_prefix(root)
        .unwrap_or(path)
        .to_string_lossy()
        .into_owned()
}

/// What the scan needs of a JSON document: its shape, with strings kept.
#[derive(Debug)]
enum Json {
    Object(Vec<(String, Json)>),
    Array(Vec<Json>),
    Str(String),
    Other,
}

/// Parses a document as Python's `json.loads` would, or returns its `JSONDecodeError` message.
fn parse(text: &str) -> Result<Json, String> {
    let chars: Vec<char> = text.chars().collect();
    if chars.first() == Some(&'\u{feff}') {
        return Err(position(
            "Unexpected UTF-8 BOM (decode using utf-8-sig)",
            &chars,
            0,
        ));
    }
    let mut parser = Parser {
        chars: &chars,
        at: 0,
        depth: 0,
    };
    parser.skip_space();
    let value = parser.value()?;
    parser.skip_space();
    if parser.at != chars.len() {
        return Err(position("Extra data", &chars, parser.at));
    }
    Ok(value)
}

/// `msg: line L column C (char P)`, the positions Python's `JSONDecodeError` derives from a character offset.
fn position(msg: &str, chars: &[char], at: usize) -> String {
    let before = &chars[..at.min(chars.len())];
    let lineno = before.iter().filter(|&&c| c == '\n').count() + 1;
    let colno = match before.iter().rposition(|&c| c == '\n') {
        Some(newline) => at - newline,
        None => at + 1,
    };
    format!("{msg}: line {lineno} column {colno} (char {at})")
}

/// A recursive-descent reader over characters, following `json.scanner`'s pure-Python decoder.
struct Parser<'a> {
    chars: &'a [char],
    at: usize,
    depth: usize,
}

impl Parser<'_> {
    fn peek(&self) -> Option<char> {
        self.chars.get(self.at).copied()
    }

    fn skip_space(&mut self) {
        while matches!(self.peek(), Some(' ' | '\t' | '\n' | '\r')) {
            self.at += 1;
        }
    }

    fn err(&self, msg: &str, at: usize) -> String {
        position(msg, self.chars, at)
    }

    fn starts_with(&self, word: &str) -> bool {
        word.chars()
            .enumerate()
            .all(|(i, c)| self.chars.get(self.at + i) == Some(&c))
    }

    fn value(&mut self) -> Result<Json, String> {
        match self.peek() {
            Some('"') => {
                self.at += 1;
                self.string().map(Json::Str)
            }
            Some('{') => {
                self.at += 1;
                self.object()
            }
            Some('[') => {
                self.at += 1;
                self.array()
            }
            Some('n') if self.starts_with("null") => {
                self.at += 4;
                Ok(Json::Other)
            }
            Some('t') if self.starts_with("true") => {
                self.at += 4;
                Ok(Json::Other)
            }
            Some('f') if self.starts_with("false") => {
                self.at += 5;
                Ok(Json::Other)
            }
            Some('N') if self.starts_with("NaN") => {
                self.at += 3;
                Ok(Json::Other)
            }
            Some('I') if self.starts_with("Infinity") => {
                self.at += 8;
                Ok(Json::Other)
            }
            Some('-') if self.starts_with("-Infinity") => {
                self.at += 9;
                Ok(Json::Other)
            }
            Some(c) if c == '-' || c.is_ascii_digit() => self.number(),
            _ => Err(self.err("Expecting value", self.at)),
        }
    }

    /// `(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?`, as far as it matches; a bare `-` is no value.
    fn number(&mut self) -> Result<Json, String> {
        let start = self.at;
        let mut at = self.at;
        if self.chars.get(at) == Some(&'-') {
            at += 1;
        }
        match self.chars.get(at) {
            Some('0') => at += 1,
            Some(c) if c.is_ascii_digit() => {
                while self.chars.get(at).is_some_and(char::is_ascii_digit) {
                    at += 1;
                }
            }
            _ => return Err(self.err("Expecting value", start)),
        }
        if self.chars.get(at) == Some(&'.')
            && self.chars.get(at + 1).is_some_and(char::is_ascii_digit)
        {
            at += 1;
            while self.chars.get(at).is_some_and(char::is_ascii_digit) {
                at += 1;
            }
        }
        if matches!(self.chars.get(at), Some('e' | 'E')) {
            let mut e = at + 1;
            if matches!(self.chars.get(e), Some('+' | '-')) {
                e += 1;
            }
            if self.chars.get(e).is_some_and(char::is_ascii_digit) {
                while self.chars.get(e).is_some_and(char::is_ascii_digit) {
                    e += 1;
                }
                at = e;
            }
        }
        self.at = at;
        Ok(Json::Other)
    }

    /// The string whose opening quote was just consumed, decoded as `json.decoder.py_scanstring` does.
    fn string(&mut self) -> Result<String, String> {
        let begin = self.at - 1;
        let mut out = String::new();
        loop {
            let Some(c) = self.peek() else {
                return Err(self.err("Unterminated string starting at", begin));
            };
            match c {
                '"' => {
                    self.at += 1;
                    return Ok(out);
                }
                '\\' => {
                    let Some(escape) = self.chars.get(self.at + 1).copied() else {
                        return Err(self.err("Unterminated string starting at", begin));
                    };
                    match escape {
                        '"' => out.push('"'),
                        '\\' => out.push('\\'),
                        '/' => out.push('/'),
                        'b' => out.push('\u{08}'),
                        'f' => out.push('\u{0c}'),
                        'n' => out.push('\n'),
                        'r' => out.push('\r'),
                        't' => out.push('\t'),
                        'u' => {
                            let first = self.hex4(self.at + 2)?;
                            self.at += 6;
                            let code = if (0xd800..0xdc00).contains(&first)
                                && self.chars.get(self.at) == Some(&'\\')
                                && self.chars.get(self.at + 1) == Some(&'u')
                            {
                                match self.hex4(self.at + 2) {
                                    Ok(second) if (0xdc00..0xe000).contains(&second) => {
                                        self.at += 6;
                                        0x10000 + (((first - 0xd800) << 10) | (second - 0xdc00))
                                    }
                                    _ => first,
                                }
                            } else {
                                first
                            };
                            out.push(char::from_u32(code).unwrap_or('\u{fffd}'));
                            continue;
                        }
                        _ => return Err(self.err("Invalid \\escape", self.at)),
                    }
                    self.at += 2;
                }
                c if (c as u32) < 0x20 => {
                    return Err(self.err("Invalid control character at", self.at));
                }
                c => {
                    out.push(c);
                    self.at += 1;
                }
            }
        }
    }

    /// Four hex digits at `at`, or Python's `Invalid \uXXXX escape` naming the escape's position.
    fn hex4(&self, at: usize) -> Result<u32, String> {
        let digits: Option<String> = (0..4)
            .map(|i| {
                self.chars
                    .get(at + i)
                    .copied()
                    .filter(char::is_ascii_hexdigit)
            })
            .collect();
        digits
            .and_then(|d| u32::from_str_radix(&d, 16).ok())
            .ok_or_else(|| self.err("Invalid \\uXXXX escape", at - 1))
    }

    fn object(&mut self) -> Result<Json, String> {
        self.descend()?;
        let mut pairs: Vec<(String, Json)> = Vec::new();
        self.skip_space();
        if self.peek() == Some('}') {
            self.at += 1;
            self.depth -= 1;
            return Ok(Json::Object(pairs));
        }
        loop {
            if self.peek() != Some('"') {
                return Err(self.err("Expecting property name enclosed in double quotes", self.at));
            }
            self.at += 1;
            let key = self.string()?;
            self.skip_space();
            if self.peek() != Some(':') {
                return Err(self.err("Expecting ':' delimiter", self.at));
            }
            self.at += 1;
            self.skip_space();
            let value = self.value()?;
            match pairs.iter_mut().find(|(k, _)| *k == key) {
                Some(slot) => slot.1 = value,
                None => pairs.push((key, value)),
            }
            self.skip_space();
            match self.peek() {
                Some('}') => {
                    self.at += 1;
                    self.depth -= 1;
                    return Ok(Json::Object(pairs));
                }
                Some(',') => {
                    self.at += 1;
                    let comma = self.at - 1;
                    self.skip_space();
                    if self.peek() == Some('}') {
                        return Err(self.err("Illegal trailing comma before end of object", comma));
                    }
                }
                _ => return Err(self.err("Expecting ',' delimiter", self.at)),
            }
        }
    }

    fn array(&mut self) -> Result<Json, String> {
        self.descend()?;
        let mut items = Vec::new();
        self.skip_space();
        if self.peek() == Some(']') {
            self.at += 1;
            self.depth -= 1;
            return Ok(Json::Array(items));
        }
        loop {
            items.push(self.value()?);
            self.skip_space();
            match self.peek() {
                Some(']') => {
                    self.at += 1;
                    self.depth -= 1;
                    return Ok(Json::Array(items));
                }
                Some(',') => {
                    self.at += 1;
                    let comma = self.at - 1;
                    self.skip_space();
                    if self.peek() == Some(']') {
                        return Err(self.err("Illegal trailing comma before end of array", comma));
                    }
                }
                _ => return Err(self.err("Expecting ',' delimiter", self.at)),
            }
        }
    }

    /// Python's decoder recurses and dies at its recursion limit on a deep document (the `vendor` story);
    /// this reader stops at the same order of depth with a message instead of a crash.
    fn descend(&mut self) -> Result<(), String> {
        self.depth += 1;
        if self.depth > 900 {
            return Err(
                "maximum recursion depth exceeded while decoding a JSON document".to_owned(),
            );
        }
        Ok(())
    }
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: scanning the fixture tree must give `expected` (0 no finding, 1 a finding) and its text (the
    /// findings, then `__CHECKED__ N`) must contain `want`.
    fn arm(&mut self, tree: &Path, hasher: &Hasher, name: &str, expected: i32, want: &str) {
        let (findings, checked) = scan_tree(tree, hasher);
        let rc = i32::from(!findings.is_empty());
        let mut out = findings;
        out.push(format!("__CHECKED__ {checked}"));
        let out = out.join("\n");
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("FIXTURE-FINGERPRINT self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("FIXTURE-FINGERPRINT self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// The seven arms over a scratch tree. Returns whether every arm held.
fn self_test(root: &Path, hasher: &Hasher, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let Ok(t) = scratch(root, "target/doctrine-selftest", "fixture-fingerprint") else {
        if verbose {
            eprintln!("FIXTURE-FINGERPRINT self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let fix = t.join("fix");
    let spec: PathBuf = fix.join("spec.md");
    let ledger = fix.join("sources.json");
    let write_ledger = |sha: &str| {
        let _ = fs::write(
            &ledger,
            format!(
                "{{\"sources\":[{{\"id\":\"S\",\"path\":\"spec.md\",\"sha256\":\"{sha}\"}}]}}\n"
            ),
        );
    };
    if fs::create_dir_all(&fix).is_err() || fs::write(&spec, "payload\n").is_err() {
        if verbose {
            eprintln!("FIXTURE-FINGERPRINT self-test: cannot build the fixture tree");
        }
        let _ = fs::remove_dir_all(&t);
        return false;
    }
    let h = hasher.digest(&spec);
    write_ledger(&h);
    tally.arm(&t, hasher, "GREEN pinned hash matches", 0, "__CHECKED__ 1");
    let _ = fs::write(&spec, "tampered\n");
    tally.arm(&t, hasher, "RED   pinned file changed", 1, "DRIFTED");
    let _ = fs::write(&spec, "payload\n");
    write_ledger(&h[..h.len().min(63)]);
    tally.arm(&t, hasher, "RED   malformed hash length", 1, "MALFORMED");
    write_ledger(&"0".repeat(64));
    tally.arm(&t, hasher, "RED   wrong hash, well-formed", 1, "DRIFTED");
    write_ledger(&h);
    let _ = fs::rename(&spec, fix.join("gone.md"));
    tally.arm(&t, hasher, "RED   pinned file absent", 1, "MISSING");
    let _ = fs::rename(fix.join("gone.md"), &spec);
    let _ = fs::write(&ledger, "{\"sources\":[{\"id\":\"S\"");
    tally.arm(&t, hasher, "RED   unparseable record", 1, "UNPARSEABLE");
    let _ = fs::remove_file(&ledger);
    tally.arm(&t, hasher, "GREEN nothing pinned", 0, "__CHECKED__ 0");
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "FIXTURE-FINGERPRINT --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The parser's messages are Python's `json.loads` messages, position included.
    #[test]
    fn malformed_documents_read_as_python_reports_them() {
        let cases = [
            (
                "{\"sources\":[{\"id\":\"S\"",
                "Expecting ',' delimiter: line 1 column 22 (char 21)",
            ),
            ("", "Expecting value: line 1 column 1 (char 0)"),
            ("   ", "Expecting value: line 1 column 4 (char 3)"),
            (
                "{",
                "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)",
            ),
            ("[1,2", "Expecting ',' delimiter: line 1 column 5 (char 4)"),
            (
                "{\"a\":1,}",
                "Illegal trailing comma before end of object: line 1 column 7 (char 6)",
            ),
            (
                "{\"a\" 1}",
                "Expecting ':' delimiter: line 1 column 6 (char 5)",
            ),
            (
                "\"abc",
                "Unterminated string starting at: line 1 column 1 (char 0)",
            ),
            (
                "{\"a\":\"\u{01}\"}",
                "Invalid control character at: line 1 column 7 (char 6)",
            ),
            (
                "{\"a\":\"\\q\"}",
                "Invalid \\escape: line 1 column 7 (char 6)",
            ),
            ("{\"a\":1} x", "Extra data: line 1 column 9 (char 8)"),
            ("nul", "Expecting value: line 1 column 1 (char 0)"),
            ("[1 2]", "Expecting ',' delimiter: line 1 column 4 (char 3)"),
            (
                "{\"a\":1",
                "Expecting ',' delimiter: line 1 column 7 (char 6)",
            ),
            ("{\"a\":", "Expecting value: line 1 column 6 (char 5)"),
            ("-", "Expecting value: line 1 column 1 (char 0)"),
            ("1.", "Extra data: line 1 column 2 (char 1)"),
            ("[", "Expecting value: line 1 column 2 (char 1)"),
            ("{\"a\":1}}", "Extra data: line 1 column 8 (char 7)"),
            (
                "\"\\u12\"",
                "Invalid \\uXXXX escape: line 1 column 3 (char 2)",
            ),
            (
                "{\"a\":1,\"b\"}",
                "Expecting ':' delimiter: line 1 column 11 (char 10)",
            ),
            (
                "{\n \"a\": [1,\n  2 3]}",
                "Expecting ',' delimiter: line 3 column 5 (char 16)",
            ),
        ];
        for (text, want) in cases {
            assert_eq!(parse(text).err().as_deref(), Some(want), "{text:?}");
        }
    }

    /// Well-formed documents parse, pins are found as Python's `dict` iteration found them, the last
    /// duplicate key wins at the first key's position.
    #[test]
    fn pins_follow_python_dict_semantics() {
        let doc = "{\"path\":\"a\",\"sha256\":\"x\",\"path\":\"b\",\"items\":[{\"sha256\":\"y\",\"path\":\"c\"},{\"path\":1,\"sha256\":\"z\"}],\"n\":-1.5e+3,\"t\":true,\"u\":null,\"i\":Infinity}";
        let mut found = Vec::new();
        pins(&parse(doc).expect("well-formed"), &mut found);
        assert_eq!(
            found,
            vec![
                ("b".to_owned(), "x".to_owned()),
                ("c".to_owned(), "y".to_owned())
            ]
        );
        assert_eq!(
            py_splitlines("a\nb\r\nc\rd\u{2028}e"),
            vec!["a", "b", "c", "d", "e"]
        );
        assert_eq!(py_strip(" \u{1c}x\t"), "x");
    }
}
