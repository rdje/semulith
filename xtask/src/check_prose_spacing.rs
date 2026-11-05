//! The `PROSE-SPACING` doctrine's driver (`P4-SYSTEM.14` a43e-c1): no word and number run together in the prose of a book.
//!
//! The founding measurement: 534 lost spaces across 37 tracked documents (`All114effective`, `its102/114`,
//! `Nine principals,27 boundaries`). Each read wrong in the surface the director reviews, and every gate stayed green.
//! Prose only: a fence, an indented block, a code span, a link
//! target, an HTML tag, a URL and a path are not prose. An identifier that really does end in a number is named in
//! `doctrine/prose_identifiers.txt`, so reviewing an exception means reading one short file.
//!
//! HONEST LIMIT: it judges the spacing around numbers and nothing else; it says nothing about whether a number is right.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

use crate::harness::combined;

const IDENTIFIERS: &str = "doctrine/prose_identifiers.txt";
const ROOTS: [&str; 10] = [
    "docs/book/src/",
    "docs/models/",
    "profiles/",
    "docs/toolbox/",
    "docs/doctrines/",
    "README.md",
    "LIVE_STATUS.md",
    "ROADMAP.md",
    "RULES.md",
    "TOOLBOX.md",
];

/// `name` a token equal to it, `name#` the name then digits then any letters.
struct Identifiers {
    exact: Vec<String>,
    families: Vec<String>,
}

impl Identifiers {
    fn parse(text: &str) -> Self {
        let (mut exact, mut families) = (Vec::new(), Vec::new());
        for line in text.lines() {
            let line = line.split(" #").next().unwrap_or("").trim();
            if line.is_empty() || line.starts_with('#') {
                continue;
            }
            match line.strip_suffix('#') {
                Some(family) => families.push(family.to_string()),
                None => exact.push(line.to_string()),
            }
        }
        Self { exact, families }
    }

    fn allows(&self, token: &str) -> bool {
        self.exact.iter().any(|name| name == token)
            || self.families.iter().any(|family| {
                token.strip_prefix(family.as_str()).is_some_and(|rest| {
                    rest.starts_with(|c: char| c.is_ascii_digit())
                        && rest.chars().all(|c| c.is_ascii_alphanumeric())
                })
            })
    }
}

fn word_char(c: char) -> bool {
    c.is_alphanumeric() || c == '_'
}

/// A glued token's reason, when `token` is a word and a number run together.
fn glued(token: &str) -> bool {
    let letters = token
        .chars()
        .take_while(|c| c.is_ascii_alphabetic())
        .count();
    let digits = token.chars().take_while(|c| c.is_ascii_digit()).count();
    if letters >= 2 {
        return token[letters..].starts_with(|c: char| c.is_ascii_digit());
    }
    if digits > 0 {
        let rest = &token[digits..];
        let unit = matches!(
            rest,
            "st" | "nd"
                | "rd"
                | "th"
                | "px"
                | "ns"
                | "us"
                | "ms"
                | "KiB"
                | "MiB"
                | "GiB"
                | "B"
                | "D"
        );
        return !unit && rest.chars().take_while(|c| c.is_ascii_lowercase()).count() >= 3;
    }
    false
}

/// Cut what is not prose out of one line: code spans, link targets, HTML tags, URLs and paths.
fn prose_segments(line: &str) -> Vec<String> {
    let mut out = String::new();
    let mut chars = line.char_indices().peekable();
    while let Some((at, c)) = chars.next() {
        let rest = &line[at..];
        let close = match c {
            '`' => rest[1..].find('`').map(|n| n + 2),
            '<' => rest[1..].find('>').map(|n| n + 2),
            ']' if rest.starts_with("](") => rest.find(')').map(|n| n + 1),
            _ => None,
        };
        if let Some(length) = close {
            out.push(' ');
            while chars.peek().is_some_and(|(next, _)| *next < at + length) {
                chars.next();
            }
            continue;
        }
        out.push(c);
    }
    out.split_whitespace().map(str::to_string).collect()
}

/// Every lost space in one word of prose: `All114effective`, or `principals,27`.
fn word_findings(word: &str, identifiers: &Identifiers, into: &mut Vec<String>) {
    if word.contains("://")
        || (word.contains('/')
            && word.contains('.')
            && !word.contains(char::is_whitespace)
            && word.matches('/').count() >= 2)
    {
        return;
    }
    let mut start = None;
    let chars: Vec<(usize, char)> = word.char_indices().collect();
    for (index, (at, c)) in chars.iter().enumerate() {
        let inside = c.is_ascii_alphanumeric();
        if inside && start.is_none() {
            start = Some(*at);
        }
        let last = index + 1 == chars.len();
        if let (Some(from), true) = (start, !inside || last) {
            let to = if inside { *at + c.len_utf8() } else { *at };
            let token = &word[from..to];
            let before = word[..from].chars().next_back();
            let after = word[to..].chars().next();
            let attached = before.is_some_and(|b| {
                matches!(b, '#' | '=' | '+' | '*' | '@' | '\\' | '.' | '_' | '$') || word_char(b)
            }) || after.is_some_and(|a| word_char(a) || a == '_');
            let hex = token.starts_with("0x");
            let dotted = after == Some('.')
                && word[to + 1..].starts_with(|n: char| n.is_ascii_alphanumeric());
            if !attached && !hex && !dotted && glued(token) && !identifiers.allows(token) {
                into.push(token.to_string());
            }
            start = None;
        }
    }
    // A code span is cut out of the line, so a number glued to its closing mark starts a word here.
    if word.starts_with([',', ';', ':']) && word[1..].starts_with(|c: char| c.is_ascii_digit()) {
        into.push(word.to_string());
    }
    let bytes = word.as_bytes();
    for at in 3..bytes.len().saturating_sub(1) {
        let mark = bytes[at];
        if matches!(mark, b',' | b';' | b':')
            && bytes[at + 1].is_ascii_digit()
            && bytes[at - 3..at].iter().all(u8::is_ascii_lowercase)
        {
            let number: String = word[at + 1..]
                .chars()
                .take_while(|c| c.is_ascii_digit() || matches!(c, ',' | '/'))
                .collect();
            let tail = &word[at + 1 + number.len()..];
            if tail.is_empty() || tail.starts_with(|c: char| !c.is_ascii_alphanumeric()) {
                into.push(word[..at + 1 + number.len()].to_string());
            }
        }
    }
}

/// `(line, token)` for each lost space in one markdown document's prose.
fn findings(text: &str, identifiers: &Identifiers) -> Vec<(usize, String)> {
    let (mut out, mut fenced) = (Vec::new(), false);
    for (index, line) in text.lines().enumerate() {
        if line.trim_start().starts_with("```") {
            fenced = !fenced;
            continue;
        }
        if fenced || line.starts_with("    ") || line.starts_with('\t') {
            continue;
        }
        let mut tokens = Vec::new();
        for word in prose_segments(line) {
            word_findings(&word, identifiers, &mut tokens);
        }
        out.extend(tokens.into_iter().map(|token| (index + 1, token)));
    }
    out
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: judging `text` finds exactly `want`.
    fn arm(&mut self, name: &str, text: &str, want: &[&str]) {
        let identifiers = Identifiers::parse("rv#\nsha#\nARM64\nFE00FF\n");
        let got: Vec<String> = findings(text, &identifiers)
            .into_iter()
            .map(|(_, token)| token)
            .collect();
        if got == want {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("PROSE-SPACING self-test MISS: {name}: expected {want:?}, got {got:?}");
            }
        }
    }
}

fn self_test(verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    tally.arm(
        "RED   a word, a number and a word run together",
        "All114effective checks are realized.",
        &["All114effective"],
    );
    tally.arm(
        "RED   a word and a ratio",
        "with its102/114 checkpoint",
        &["its102"],
    );
    tally.arm(
        "RED   a number and the word after it",
        "and 80malformed rows",
        &["80malformed"],
    );
    tally.arm(
        "RED   a number with separators",
        "the1,536architectural cases",
        &["the1", "536architectural"],
    );
    tally.arm(
        "RED   a number after a comma with no space",
        "Nine principals,27 boundaries",
        &["principals,27"],
    );
    tally.arm(
        "RED   a number after a colon with no space",
        "policy:64 children",
        &["policy:64"],
    );
    tally.arm(
        "RED   prose beside a code span is still judged",
        "`rv64gc` adds144 cases",
        &["adds144"],
    );
    tally.arm(
        "RED   a number glued to a code span's closing mark",
        "`--self-test`;50 controls",
        &[";50"],
    );
    tally.arm(
        "GREEN a number inside a code span",
        "the forms (`:2`, `::10`)",
        &[],
    );
    tally.arm(
        "GREEN a spaced number",
        "All 114 effective checks, 27 boundaries: 64 children.",
        &[],
    );
    tally.arm("GREEN a code span", "the `All114effective` spelling", &[]);
    tally.arm("GREEN a fence", "```\nAll114effective\n```\n", &[]);
    tally.arm("GREEN an indented block", "    All114effective\n", &[]);
    tally.arm(
        "GREEN a link target",
        "[the page](plan/contract114.md)",
        &[],
    );
    tally.arm(
        "GREEN a URL",
        "see https://example.org/all114effective",
        &[],
    );
    tally.arm("GREEN a named family", "rv64gc and sha256 and rv32", &[]);
    tally.arm("GREEN a named identifier", "ARM64 and FE00FF", &[]);
    tally.arm("GREEN a hexadecimal value", "the word 0xdeadbeef", &[]);
    tally.arm("GREEN an ordinal and a unit", "the 3rd of 64KiB", &[]);
    tally.arm("GREEN a section locator", "§2.1.1.8 and x5, x86-64", &[]);
    let (pass, fail) = (tally.pass, tally.fail);
    println!("PROSE-SPACING --self-test: {pass} pass / {fail} fail");
    fail == 0
}

fn real(repo: &Path) -> Result<(usize, Vec<String>), String> {
    let identifiers =
        fs::read_to_string(repo.join(IDENTIFIERS)).map_err(|e| format!("{IDENTIFIERS}: {e}"))?;
    let identifiers = Identifiers::parse(&identifiers);
    let (rc, listed) = combined(
        Command::new("git")
            .args(["ls-files", "*.md"])
            .current_dir(repo),
    );
    if rc != 0 {
        return Err(format!("git ls-files rc={rc}"));
    }
    let (mut judged, mut breaches) = (0, Vec::new());
    for path in listed
        .lines()
        .filter(|p| ROOTS.iter().any(|r| p.starts_with(r)))
    {
        judged += 1;
        let text = fs::read_to_string(repo.join(path)).map_err(|e| format!("{path}: {e}"))?;
        for (line, token) in findings(&text, &identifiers) {
            breaches.push(format!("{path}:{line}: {token}"));
        }
    }
    Ok((judged, breaches))
}

/// `cargo xtask check-prose-spacing [--self-test]`: 0 clean, 1 a lost space, 2 refused.
pub fn run(repo: &Path, args: &[String]) -> ExitCode {
    let verbose = args.iter().any(|a| a == "--self-test");
    if !self_test(verbose) {
        eprintln!("PROSE-SPACING: REFUSED: the self-test no longer discriminates");
        return ExitCode::from(2);
    }
    if verbose {
        return ExitCode::SUCCESS;
    }
    match real(repo) {
        Err(reason) => {
            eprintln!("PROSE-SPACING: REFUSED: {reason}");
            ExitCode::from(2)
        }
        Ok((judged, breaches)) if breaches.is_empty() => {
            println!("PROSE-SPACING: ok ({judged} document(s), no word and number run together in their prose)");
            ExitCode::SUCCESS
        }
        Ok((_, breaches)) => {
            for breach in &breaches {
                eprintln!("{breach}");
            }
            eprintln!("PROSE-SPACING: {} lost space(s): separate the word from the number, or name a real identifier in {IDENTIFIERS}", breaches.len());
            ExitCode::from(1)
        }
    }
}
