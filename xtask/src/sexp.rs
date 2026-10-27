//! The project's S-expression reader in Rust (`XTASK.6` slice `6j`), measured equal to the pinned
//! `scripts/sexp.py` on every `.sexp` file of the corpus and on the pinned reader's own refusal arms.
//!
//! The language is the pinned reader's, no more: nested lists of atoms, an atom an integer (decimal,
//! `0x` hex or `0b` binary, with `_` separators in the prefixed forms, a sign allowed), a quoted string
//! with a CLOSED escape table (`\"` `\\` `\n` `\t` `\r` — a non-ASCII character needs no escape), or a
//! bare symbol; `;` comments run to the end of the line and are recognised in the same pass as strings,
//! so a `;` inside a string is content and a string may span lines. THE READER REFUSES RATHER THAN
//! GUESSES, with the pinned reader's messages: an unterminated list, a stray `)`, an unterminated
//! string or escape and an unknown escape are errors, never best-effort recoveries. Honest limits, each
//! measured not to occur in the corpus: Python's `\d` also reads non-ASCII decimal digits as integers
//! (here only ASCII digits do), and its integers are unbounded (here `i128`).

use std::fs;
use std::path::Path;

/// A refusal, carrying the pinned reader's message.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SexpError(pub String);

impl std::fmt::Display for SexpError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

/// A form: an atom or a list of forms. A symbol and a string are distinct so a writer can round-trip
/// them, as the pinned reader's `Symbol` subclass keeps them apart.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Sexp {
    Int(i128),
    Str(String),
    Symbol(String),
    List(Vec<Sexp>),
}

impl Sexp {
    /// The text of a symbol or string head, as Python's `str` saw both.
    pub fn text(&self) -> Option<&str> {
        match self {
            Sexp::Str(s) | Sexp::Symbol(s) => Some(s),
            _ => None,
        }
    }

    /// Python's `type(x).__name__` for the parsed value.
    fn type_name(&self) -> &'static str {
        match self {
            Sexp::Int(_) => "int",
            Sexp::Str(_) => "str",
            Sexp::Symbol(_) => "Symbol",
            Sexp::List(_) => "list",
        }
    }
}

/// Python's `str.isspace()`.
fn py_space(c: char) -> bool {
    c.is_whitespace() || ('\u{1c}'..='\u{1f}').contains(&c)
}

/// Python's `repr` of a `str` (and of the `Symbol` subclass, which inherits it).
fn py_str_repr(s: &str) -> String {
    let quote = if s.contains('\'') && !s.contains('"') {
        '"'
    } else {
        '\''
    };
    let mut out = String::new();
    out.push(quote);
    for c in s.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if c == quote => {
                out.push('\\');
                out.push(c);
            }
            c if (c as u32) < 0x20 || c as u32 == 0x7f => {
                out.push_str(&format!("\\x{:02x}", c as u32))
            }
            c => out.push(c),
        }
    }
    out.push(quote);
    out
}

/// Python's `repr` of a parsed form (`int`, `str`, `Symbol` — a `str` — or `list`).
#[cfg_attr(not(test), allow(dead_code))] // consumed by the doctrine modules that follow (slice 6k)
pub fn py_repr(form: &Sexp) -> String {
    match form {
        Sexp::Int(n) => n.to_string(),
        Sexp::Str(s) | Sexp::Symbol(s) => py_str_repr(s),
        Sexp::List(items) => format!(
            "[{}]",
            items.iter().map(py_repr).collect::<Vec<_>>().join(", ")
        ),
    }
}

/// `int(text.replace("_", ""), base)` on a token the atom patterns accepted.
fn integer(text: &str, base: u32, line: usize, where_: &str) -> Result<Sexp, SexpError> {
    let cleaned: String = text.chars().filter(|&c| c != '_').collect();
    let (negative, digits) = match cleaned.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, cleaned.strip_prefix('+').unwrap_or(&cleaned)),
    };
    let digits = if base == 10 {
        digits
    } else {
        &digits[2..] // the pinned patterns put the 0x/0b prefix right after the sign
    };
    let unreadable = || {
        SexpError(format!(
            "{where_}:{line}: unreadable base-{base} integer ({} characters)",
            text.chars().count()
        ))
    };
    if digits.is_empty() {
        return Err(unreadable());
    }
    let value = i128::from_str_radix(digits, base).map_err(|_| unreadable())?;
    Ok(Sexp::Int(if negative { -value } else { value }))
}

/// The pinned reader's `_atom`: `[+-]?\d+`, `[+-]?0[xX][0-9a-fA-F_]+`, `[+-]?0[bB][01_]+`, else a symbol.
fn atom(text: &str, line: usize, where_: &str) -> Result<Sexp, SexpError> {
    let body = text.strip_prefix(['+', '-']).unwrap_or(text);
    if !body.is_empty() && body.chars().all(|c| c.is_ascii_digit()) {
        return integer(text, 10, line, where_);
    }
    if let Some(hex) = body.strip_prefix("0x").or_else(|| body.strip_prefix("0X")) {
        if !hex.is_empty() && hex.chars().all(|c| c.is_ascii_hexdigit() || c == '_') {
            return integer(text, 16, line, where_);
        }
    }
    if let Some(bin) = body.strip_prefix("0b").or_else(|| body.strip_prefix("0B")) {
        if !bin.is_empty() && bin.chars().all(|c| c == '0' || c == '1' || c == '_') {
            return integer(text, 2, line, where_);
        }
    }
    Ok(Sexp::Symbol(text.to_owned()))
}

/// Parses a whole text into its top-level forms, scanned as one stream (the pinned `parse`).
pub fn parse(text: &str, where_: &str) -> Result<Vec<Sexp>, SexpError> {
    let chars: Vec<char> = text.chars().collect();
    let n = chars.len();
    let mut stack: Vec<Vec<Sexp>> = vec![Vec::new()];
    let mut open_at: Vec<usize> = vec![0];
    let (mut i, mut line) = (0usize, 1usize);
    while i < n {
        let ch = chars[i];
        if ch == '\n' {
            line += 1;
            i += 1;
            continue;
        }
        if py_space(ch) {
            i += 1;
            continue;
        }
        if ch == ';' {
            while i < n && chars[i] != '\n' {
                i += 1;
            }
            continue;
        }
        if ch == '(' {
            stack.push(Vec::new());
            open_at.push(line);
            i += 1;
            continue;
        }
        if ch == ')' {
            if stack.len() == 1 {
                return Err(SexpError(format!(
                    "{where_}:{line}: ')' with no matching '('"
                )));
            }
            let done = stack.pop().unwrap_or_default();
            open_at.pop();
            if let Some(top) = stack.last_mut() {
                top.push(Sexp::List(done));
            }
            i += 1;
            continue;
        }
        if ch == '"' {
            let mut j = i + 1;
            let mut buf = String::new();
            while j < n && chars[j] != '"' {
                let c = chars[j];
                if c == '\\' {
                    if j + 1 >= n {
                        return Err(SexpError(format!(
                            "{where_}:{line}: unterminated escape at end of input"
                        )));
                    }
                    let esc = chars[j + 1];
                    let decoded = match esc {
                        '"' => '"',
                        '\\' => '\\',
                        'n' => '\n',
                        't' => '\t',
                        'r' => '\r',
                        other => {
                            return Err(SexpError(format!(
                                "{where_}:{line}: unknown escape '\\{other}' in string. The reader refuses rather than guessing what it was meant to be; write the character itself, or use one of: \" \\ n r t"
                            )));
                        }
                    };
                    buf.push(decoded);
                    j += 2;
                    continue;
                }
                if c == '\n' {
                    line += 1;
                }
                buf.push(c);
                j += 1;
            }
            if j >= n {
                return Err(SexpError(format!("{where_}:{line}: unterminated string")));
            }
            if let Some(top) = stack.last_mut() {
                top.push(Sexp::Str(buf));
            }
            i = j + 1;
            continue;
        }
        let mut j = i;
        while j < n && !py_space(chars[j]) && !matches!(chars[j], '(' | ')' | '"' | ';') {
            j += 1;
        }
        if j == i {
            return Err(SexpError(format!(
                "{where_}:{line}: cannot read {}",
                py_str_repr(&ch.to_string())
            )));
        }
        let token: String = chars[i..j].iter().collect();
        let value = atom(&token, line, where_)?;
        if let Some(top) = stack.last_mut() {
            top.push(value);
        }
        i = j;
    }
    if stack.len() != 1 {
        return Err(SexpError(format!(
            "{where_}: {} unterminated list(s); the outermost opened on line {}",
            stack.len() - 1,
            open_at.get(1).copied().unwrap_or(0)
        )));
    }
    Ok(stack.pop().unwrap_or_default())
}

/// Reads a file as `Path.read_text()` did — UTF-8, universal newlines — and parses it with the path as
/// the error location. An unreadable or non-UTF-8 file is a refusal naming it.
pub fn read_file(path: &Path) -> Result<Vec<Sexp>, SexpError> {
    let shown = path.to_string_lossy().into_owned();
    let bytes = fs::read(path).map_err(|e| {
        // `[Errno 2] No such file or directory: 'path'`, as Python's OSError printed it
        let text = e.to_string();
        let reason = text.split(" (os error").next().unwrap_or(&text).to_owned();
        match e.raw_os_error() {
            Some(code) => SexpError(format!("[Errno {code}] {reason}: {}", py_str_repr(&shown))),
            None => SexpError(format!("{reason}: {}", py_str_repr(&shown))),
        }
    })?;
    let text = String::from_utf8(bytes).map_err(|e| {
        // Python's UnicodeDecodeError, for the three shapes a UTF-8 decoder reports
        let at = e.utf8_error().valid_up_to();
        let byte = e.as_bytes()[at];
        let total = e.as_bytes().len();
        match e.utf8_error().error_len() {
            // a sequence cut off by the end of the file: Python names the whole remainder when it is
            // more than one byte, the lone lead byte otherwise
            None if total - at > 1 => SexpError(format!(
                "'utf-8' codec can't decode bytes in position {at}-{}: unexpected end of data",
                total - 1
            )),
            None => SexpError(format!("'utf-8' codec can't decode byte 0x{byte:02x} in position {at}: unexpected end of data")),
            Some(_) if (0x80..0xC0).contains(&byte) || !(0x80..0xF5).contains(&byte) || byte == 0xC0 || byte == 0xC1 => {
                SexpError(format!("'utf-8' codec can't decode byte 0x{byte:02x} in position {at}: invalid start byte"))
            }
            Some(_) => SexpError(format!("'utf-8' codec can't decode byte 0x{byte:02x} in position {at}: invalid continuation byte")),
        }
    })?;
    let text = text.replace("\r\n", "\n").replace('\r', "\n");
    parse(&text, &shown)
}

/// The head of a form: the symbol (or string) its list begins with (the pinned `head`).
pub fn head(form: &Sexp, where_: &str) -> Result<String, SexpError> {
    match form {
        Sexp::List(items) => match items.first() {
            Some(first) if first.text().is_some() => {
                Ok(first.text().unwrap_or_default().to_owned())
            }
            Some(first) => Err(SexpError(format!(
                "{where_}: expected a list beginning with a symbol, got list beginning with {}",
                first.type_name()
            ))),
            None => Err(SexpError(format!(
                "{where_}: expected a list beginning with a symbol, got empty list"
            ))),
        },
        other => Err(SexpError(format!(
            "{where_}: expected a list beginning with a symbol, got {}",
            other.type_name()
        ))),
    }
}

/// Every direct child list whose head is `name` (the pinned `children`).
#[cfg_attr(not(test), allow(dead_code))] // consumed by the doctrine modules that follow (slice 6k)
pub fn children<'a>(form: &'a Sexp, name: &str) -> Result<Vec<&'a Sexp>, SexpError> {
    let Sexp::List(items) = form else {
        return Err(SexpError(format!("expected a list, got {}", py_repr(form))));
    };
    Ok(items
        .iter()
        .filter(|c| matches!(c, Sexp::List(l) if l.first().and_then(Sexp::text) == Some(name)))
        .collect())
}

/// The single value of `(name value)`, refusing absence and duplication alike (the pinned `field`).
#[cfg_attr(not(test), allow(dead_code))] // consumed by the doctrine modules that follow (slice 6k)
pub fn field<'a>(form: &'a Sexp, name: &str, where_: &str) -> Result<&'a Sexp, SexpError> {
    let found = children(form, name)?;
    if found.len() != 1 {
        return Err(SexpError(format!(
            "{where_}: expected exactly one ({name} …), found {}",
            found.len()
        )));
    }
    match found[0] {
        Sexp::List(items) if items.len() == 2 => Ok(&items[1]),
        other => Err(SexpError(format!(
            "{where_}: ({name} …) must carry exactly one value, got {}",
            py_repr(other)
        ))),
    }
}

/// A canonical rendering for measurement: symbols bare, strings quoted with the closed escape table,
/// integers decimal, lists parenthesised and space-separated, one top-level form per line.
#[cfg_attr(not(test), allow(dead_code))] // consumed by the doctrine modules that follow (slice 6k)
pub fn dump(forms: &[Sexp]) -> String {
    fn one(form: &Sexp, out: &mut String) {
        match form {
            Sexp::Int(n) => out.push_str(&n.to_string()),
            Sexp::Symbol(s) => out.push_str(s),
            Sexp::Str(s) => {
                out.push('"');
                for c in s.chars() {
                    match c {
                        '\\' => out.push_str("\\\\"),
                        '"' => out.push_str("\\\""),
                        '\n' => out.push_str("\\n"),
                        '\t' => out.push_str("\\t"),
                        '\r' => out.push_str("\\r"),
                        c => out.push(c),
                    }
                }
                out.push('"');
            }
            Sexp::List(items) => {
                out.push('(');
                for (i, item) in items.iter().enumerate() {
                    if i > 0 {
                        out.push(' ');
                    }
                    one(item, out);
                }
                out.push(')');
            }
        }
    }
    let mut out = String::new();
    for (i, form) in forms.iter().enumerate() {
        if i > 0 {
            out.push('\n');
        }
        one(form, &mut out);
    }
    out
}

/// `cargo xtask sexp <file.sexp>`: parse and report, for checking a file by hand — the pinned `scripts/sexp.py`
/// command line, answered by this reader (`ok: N top-level form(s); heads: …` on stdout, `REFUSED: …` on
/// stderr with exit 1, usage with exit 2). The pinned reader stays the authority for Python consumers.
pub fn run(args: &[String]) -> std::process::ExitCode {
    let [path] = args else {
        eprintln!(
            "usage: cargo xtask sexp <file.sexp>   # parse and report, for checking a file by hand"
        );
        return std::process::ExitCode::from(2);
    };
    let forms = match read_file(Path::new(path)) {
        Ok(forms) => forms,
        Err(error) => {
            eprintln!("REFUSED: {error}");
            return std::process::ExitCode::from(1);
        }
    };
    let mut heads: Vec<String> = Vec::new();
    for form in forms.iter().filter(|f| matches!(f, Sexp::List(_))) {
        match head(form, path) {
            Ok(h) => {
                if !heads.contains(&h) {
                    heads.push(h);
                }
            }
            Err(error) => {
                eprintln!("REFUSED: {error}");
                return std::process::ExitCode::from(1);
            }
        }
    }
    heads.sort();
    println!(
        "ok: {} top-level form(s); heads: {}",
        forms.len(),
        heads.join(", ")
    );
    std::process::ExitCode::SUCCESS
}

#[cfg(test)]
mod tests {
    use super::*;

    fn one(text: &str) -> Sexp {
        let forms = parse(text, "<arm>").expect("parses");
        assert_eq!(forms.len(), 1);
        forms.into_iter().next().expect("one form")
    }

    fn refuses(text: &str, needle: &str) {
        let err = parse(text, "<arm>").expect_err("must refuse");
        assert!(err.0.contains(needle), "{err}");
    }

    /// The pinned reader's own self-test arms, re-asserted here.
    #[test]
    fn the_pinned_readers_arms_hold() {
        assert_eq!(
            field(
                &one("(sem (source \"RVI-RV64I \u{a7}3.1.2.1 \u{2014} D-LUI\"))"),
                "source",
                ""
            )
            .ok(),
            Some(&Sexp::Str(
                "RVI-RV64I \u{a7}3.1.2.1 \u{2014} D-LUI".to_owned()
            ))
        );
        assert_eq!(
            field(&one(r#"(x (s "a\nb"))"#), "s", "").ok(),
            Some(&Sexp::Str("a\nb".to_owned()))
        );
        assert_eq!(
            field(&one(r#"(x (s "a\tb"))"#), "s", "").ok(),
            Some(&Sexp::Str("a\tb".to_owned()))
        );
        assert_eq!(
            field(&one(r#"(x (s "a\"b"))"#), "s", "").ok(),
            Some(&Sexp::Str("a\"b".to_owned()))
        );
        assert_eq!(
            field(&one(r#"(x (s "a\\b"))"#), "s", "").ok(),
            Some(&Sexp::Str("a\\b".to_owned()))
        );
        refuses(r#"(x (s "a\qb"))"#, "unknown escape");
        refuses("(x (s \"a\\", "unterminated");
        assert_eq!(
            field(&one("(x (s \"a;b\"))"), "s", "").ok(),
            Some(&Sexp::Str("a;b".to_owned()))
        );
        assert_eq!(
            field(&one("(x (s \"a\nb\"))"), "s", "").ok(),
            Some(&Sexp::Str("a\nb".to_owned()))
        );
        assert_eq!(
            field(&one("(x (s \"v\"))   ; trailing"), "s", "").ok(),
            Some(&Sexp::Str("v".to_owned()))
        );
        refuses("(x (s \"a))", "unterminated string");
        refuses("(x))", "no matching");
        refuses("(a\n (b\n  (c", "unterminated list");
        assert_eq!(
            parse("(a\n (b\n  (c", "<arm>").err().map(|e| e.0),
            Some("<arm>: 3 unterminated list(s); the outermost opened on line 1".to_owned())
        );
        let Sexp::List(n) = one("(n 12 0x1f 0b101 -3 +0X_F 0b1_0)") else {
            panic!()
        };
        assert_eq!(
            &n[1..],
            &[
                Sexp::Int(12),
                Sexp::Int(31),
                Sexp::Int(5),
                Sexp::Int(-3),
                Sexp::Int(15),
                Sexp::Int(2)
            ]
        );
        let Sexp::List(x) = one("(x sym \"sym\")") else {
            panic!()
        };
        assert!(
            matches!(&x[1], Sexp::Symbol(s) if s == "sym")
                && matches!(&x[2], Sexp::Str(s) if s == "sym")
        );
        assert!(field(&one("(x (s \"a\") (s \"b\"))"), "s", "<arm>")
            .unwrap_err()
            .0
            .contains("found 2"));
        assert!(field(&one("(x (s \"a\" \"b\"))"), "s", "<arm>")
            .unwrap_err()
            .0
            .contains("exactly one value"));
        assert_eq!(
            head(&Sexp::Int(3), "w").unwrap_err().0,
            "w: expected a list beginning with a symbol, got int"
        );
        assert_eq!(
            head(&Sexp::List(vec![]), "w").unwrap_err().0,
            "w: expected a list beginning with a symbol, got empty list"
        );
        assert_eq!(
            children(&Sexp::Str("it's".to_owned()), "a").unwrap_err().0,
            "expected a list, got \"it's\""
        );
        assert_eq!(
            dump(
                &one("(a \"q\\\"\\n\" 0x10 -2 (b))")
                    .clone()
                    .into_iter_single()
            ),
            "(a \"q\\\"\\n\" 16 -2 (b))"
        );
    }

    /// Every `.sexp` file of the corpus reads as the pinned `scripts/sexp.py` reads it: one canonical dump
    /// from each reader over the whole corpus, byte-identical. An absent comparator is a failure, not a skip.
    #[test]
    fn the_corpus_reads_as_the_pinned_reader_reads_it() {
        use std::io::Write as _;
        use std::process::{Command, Stdio};
        let root = std::env::var("XT0016_ROOT")
            .map(std::path::PathBuf::from)
            .unwrap_or_else(|_| {
                Path::new(env!("CARGO_MANIFEST_DIR"))
                    .parent()
                    .expect("the workspace root")
                    .to_path_buf()
            });
        let listed = Command::new("git")
            .args(["ls-files", "-z", "*.sexp"])
            .current_dir(&root)
            .output()
            .expect("git ls-files");
        assert!(listed.status.success(), "git ls-files failed");
        let files: Vec<String> = String::from_utf8_lossy(&listed.stdout)
            .split('\0')
            .filter(|s| !s.is_empty())
            .map(str::to_owned)
            .collect();
        assert!(
            files.len() >= 300,
            "the corpus census found only {} files",
            files.len()
        );
        let pydump = concat!(
            "import sys, pathlib\nsys.path.insert(0, 'scripts'); sys.dont_write_bytecode = True\nimport sexp\n",
            "def d(x):\n    if isinstance(x, list): return '(' + ' '.join(map(d, x)) + ')'\n",
            "    if isinstance(x, sexp.Symbol): return str(x)\n",
            "    if isinstance(x, str): return '\"' + x.replace('\\\\','\\\\\\\\').replace('\"','\\\\\"').replace('\\n','\\\\n').replace('\\t','\\\\t').replace('\\r','\\\\r') + '\"'\n",
            "    return str(x)\n",
            "for p in sys.stdin.read().split('\\0'):\n    if not p: continue\n    print('== ' + p)\n",
            "    try: print('\\n'.join(d(f) for f in sexp.read_file(pathlib.Path(p))))\n",
            "    except sexp.SexpError as e: print('REFUSED: ' + str(e))\n",
        );
        let mut child = Command::new("python3")
            .args(["-I", "-c", pydump])
            .current_dir(&root)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .expect("python3 is the comparator");
        child
            .stdin
            .take()
            .expect("stdin")
            .write_all(files.join("\0").as_bytes())
            .expect("file list");
        let output = child.wait_with_output().expect("python3 finished");
        assert!(
            output.status.success(),
            "the pinned reader's dump failed: {}",
            String::from_utf8_lossy(&output.stderr)
        );
        let mut ours = String::new();
        for file in &files {
            ours.push_str("== ");
            ours.push_str(file);
            ours.push('\n');
            match read_file(&root.join(file)) {
                Ok(forms) => {
                    ours.push_str(&dump(&forms));
                    ours.push('\n');
                }
                Err(error) => {
                    ours.push_str("REFUSED: ");
                    ours.push_str(&error.0);
                    ours.push('\n');
                }
            }
        }
        let theirs = String::from_utf8_lossy(&output.stdout);
        if theirs != ours {
            let first = theirs
                .lines()
                .zip(ours.lines())
                .position(|(a, b)| a != b)
                .unwrap_or(0);
            panic!("the readers disagree ({} files); first differing line {}:\n pinned: {}\n   ours: {}", files.len(), first + 1,
                   theirs.lines().nth(first).unwrap_or(""), ours.lines().nth(first).unwrap_or(""));
        }
    }

    trait Single {
        fn into_iter_single(self) -> Vec<Sexp>;
    }
    impl Single for Sexp {
        fn into_iter_single(self) -> Vec<Sexp> {
            vec![self]
        }
    }
}
