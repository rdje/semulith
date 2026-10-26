//! The `FACT-OWNERSHIP` doctrine (`MODEL-METHOD.7`), ported from `scripts/check_fact_ownership.sh` (`XTASK.6`
//! slice `6h`), which is now a shim of `cargo xtask check-fact-ownership`.
//!
//! "Single source of truth" means one OWNER PER FACT, not one file: the corpus legitimately derives facts
//! into mirrors, and each owner→mirror pair is governed by a doctrine that refuses the day the two drift.
//! `doctrine/fact_ownership.tsv` names, per fact kind, the owning file, the legal mirrors and the governing
//! doctrine. This check verifies the registry HOLDS — exactly one owner per fact kind, owners exist, every
//! mirror names a governor, every governor is a registered project doctrine — and that the corpus's
//! enumerated restatement pairs are all named in it; an ungoverned mirror is how one fact quietly becomes
//! two. The script's inline Python is ported with it: its `glob` patterns are expanded by a reader written
//! here (no new crate) with Python's rules (a `*` never matches a hidden name; a family `dir/` is present
//! when it holds a `.sexp` file at any depth), and its `sorted(set)` listing is printed as Python's `repr`
//! would print it. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total
//! counts; the script's idiom missed its two `armp` arms, so the module's ten restore the honest count.

use std::collections::BTreeMap;
use std::fs;
use std::path::Path;
use std::process::ExitCode;

use crate::harness::{py_splitlines, py_strip, scratch};

/// The registry, relative to the repository root.
const TSV: &str = "doctrine/fact_ownership.tsv";
/// The project doctrine slot, whose registered names a governor must be among.
const DRIVER: &str = "scripts/check_doctrines.project.sh";
/// The corpus's actual restatement pairs, `(restater, source)`: the restater restates the source's fact.
/// Each must appear in the registry as a row whose owner matches the source and mirror the restater —
/// enumerated because a completeness claim needs a census. The `platform.sexp` pairs (`P5-BOARD.6`) name
/// today's pinned processor concretely; a second board's leaf extends the census with its own.
const CORPUS_MIRRORS: &[(&str, &str)] = &[
    ("profiles/*/requirements.sexp", "profiles/*/profile.sexp"),
    ("profiles/*/profile.sexp", "profiles/*/state.sexp"),
    (
        "profiles/*/contract-obligations.sexp",
        "profiles/*/requirements.sexp",
    ),
    ("profiles/*/encoding.sexp", "definitions/"),
    ("crates/*/src/state.rs", "profiles/*/state.sexp"),
    ("crates/*/src/definition.rs", "definitions/"),
    ("crates/*/src/definition.rs", "profiles/*/state.sexp"),
    ("profiles/*/platform.sexp", "profiles/*/board.sexp"),
    (
        "profiles/*/platform.sexp",
        "profiles/rv64i-lab-v0/profile.sexp",
    ),
    (
        "profiles/*/platform.sexp",
        "profiles/rv64i-lab-v0/contract-obligations.sexp",
    ),
];

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 the no-duplicated-fact rule is breached, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join(TSV).is_file() {
        eprintln!("FACT-OWNERSHIP: REFUSED — {TSV} is missing; the registry this doctrine judges is gone.");
        return ExitCode::from(2);
    }
    if !self_test(root, false) {
        eprintln!("FACT-OWNERSHIP: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let verdict = check_ownership(root, TSV, CORPUS_MIRRORS);
    if verdict.rc == 2 {
        eprintln!("FACT-OWNERSHIP: REFUSED — the registry could not be judged.");
        for line in &verdict.findings {
            eprintln!("  {line}");
        }
        return ExitCode::from(2);
    }
    if verdict.rc != 0 {
        eprintln!("FACT-OWNERSHIP: the no-duplicated-fact rule is breached.");
        for line in &verdict.findings {
            eprintln!("  {line}");
        }
        eprintln!("  The registry is the authority. Name the owner, or govern the mirror.");
        return ExitCode::from(1);
    }
    println!(
        "FACT-OWNERSHIP: ok ({} fact kind(s): one owner each, every mirror governed)",
        verdict.checked
    );
    ExitCode::SUCCESS
}

/// What the script's `check_ownership` printed and returned: the findings (every line but `__CHECKED__`),
/// the number of rows checked, and its exit code (0 holds, 1 breached, 2 could not judge).
struct Verdict {
    findings: Vec<String>,
    checked: usize,
    rc: i32,
}

impl Verdict {
    /// The findings then `__CHECKED__ N`, one text, as the script's `out` held them.
    fn text(&self) -> String {
        let mut lines = self.findings.clone();
        lines.push(format!("__CHECKED__ {}", self.checked));
        lines.join("\n")
    }
}

/// One registry row: its line number and four cells.
struct Row {
    kind: String,
    owner: String,
    mirror: String,
    governor: String,
}

/// The script's Python, over the registry at `tsv` (a path relative to `root`, or absolute, shown as given),
/// the project doctrine slot, and the corpus pairs.
fn check_ownership(root: &Path, tsv: &str, corpus: &[(&str, &str)]) -> Verdict {
    let refused = |finding: String| Verdict {
        findings: vec![finding],
        checked: 0,
        rc: 2,
    };
    let text = fs::read(root.join(tsv)).map_or_else(
        |_| String::new(),
        |b| String::from_utf8_lossy(&b).into_owned(),
    );
    let mut rows = Vec::new();
    for (i, raw) in py_splitlines(&text).into_iter().enumerate() {
        let line = raw.strip_suffix('\n').unwrap_or(raw);
        if py_strip(line).is_empty() || line.starts_with('#') {
            continue;
        }
        let cells: Vec<&str> = line.split('\t').collect();
        if cells.len() != 4 {
            return refused(format!(
                "BAD ROW {tsv}:{}: expected 4 tab-separated cells, got {}",
                i + 1,
                cells.len()
            ));
        }
        rows.push(Row {
            kind: cells[0].to_owned(),
            owner: cells[1].to_owned(),
            mirror: cells[2].to_owned(),
            governor: cells[3].to_owned(),
        });
    }
    if rows.is_empty() {
        return refused(format!(
            "EMPTY REGISTRY {tsv}: no fact kind is owned by anything — this check cannot judge"
        ));
    }
    let driver = fs::read(root.join(DRIVER)).map_or_else(
        |_| String::new(),
        |b| String::from_utf8_lossy(&b).into_owned(),
    );
    let registered = registered_doctrines(&driver);
    let exists = |path: &str| root.join(path).exists();

    let mut findings = Vec::new();
    let checked = rows.len();
    let mut kinds: BTreeMap<&str, Vec<&Row>> = BTreeMap::new();
    for row in &rows {
        kinds.entry(row.kind.as_str()).or_default().push(row);
        let (kind, owner, mirror, governor) = (&row.kind, &row.owner, &row.mirror, &row.governor);
        if py_strip(owner).is_empty() || owner == "-" {
            findings.push(format!(
                "OWNERLESS {kind}: no owning file — a fact kind nobody owns is a fact nobody may state"
            ));
            continue;
        }
        if !exists(owner) {
            findings.push(format!("MISSING OWNER {kind}: '{owner}' does not exist"));
        }
        if mirror != "-" && governor == "-" {
            findings.push(format!(
                "UNGOVERNED MIRROR {kind}: '{mirror}' restates '{owner}' with no governing doctrine — one fact stated in two, free to drift"
            ));
        }
        if governor != "-" && mirror == "-" {
            findings.push(format!(
                "GOVERNOR WITHOUT MIRROR {kind}: '{governor}' governs nothing — the registry claims a check that has no pair to check"
            ));
        }
        if governor != "-" && !registered.iter().any(|name| name == governor) {
            findings.push(format!(
                "UNREGISTERED GOVERNOR {kind}: '{governor}' is named as a mirror governor but is not a registered project doctrine"
            ));
        }
    }
    for (kind, entries) in &kinds {
        let mut owners: Vec<&str> = entries.iter().map(|row| row.owner.as_str()).collect();
        owners.sort_unstable();
        owners.dedup();
        if owners.len() > 1 {
            findings.push(format!(
                "TWO OWNERS {kind}: {} both claim ownership — exactly one file owns a fact kind",
                py_list(&owners)
            ));
        }
    }

    // the corpus's actual restatement pairs must all be NAMED in the registry
    let mut pairs: Vec<(String, String)> = Vec::new();
    let mut cross: Vec<(&str, &str, Vec<String>, Vec<String>)> = Vec::new();
    for &(restater, source) in corpus {
        let (rs, ss) = (expand(root, restater), expand(root, source));
        if restater.starts_with("profiles/*/") && source.starts_with("profiles/*/") {
            // Same-family patterns pair WITHIN one unit (P3-BREADTH.7): a unit's documents restate that
            // unit's facts; the cross product invented cross-unit pairs the day a second unit landed.
            for r in &rs {
                for s in &ss {
                    if r.split('/').nth(1) == s.split('/').nth(1) {
                        pairs.push((r.clone(), s.clone()));
                    }
                }
            }
        } else {
            cross.push((restater, source, rs, ss));
        }
    }
    for (r, s) in &pairs {
        let named = rows
            .iter()
            .any(|row| matches(s, &row.owner) && matches(r, &row.mirror));
        if !named {
            findings.push(format!(
                "UNREGISTERED MIRROR PAIR: '{r}' restates '{s}' in the corpus but no registry row names this pair — the no-duplicated-fact rule is only as good as the registry's completeness"
            ));
        }
    }
    // Cross-family patterns (crates/ ↔ profiles/, profiles/ ↔ definitions/): the true pairs are not
    // mechanically derivable, so the census runs in the two checkable directions — every registered
    // cross-family row must be LIVE, and every corpus file matching a RESTATER pattern must be registered
    // as a mirror against a source of that family. Owner-side participation is not required.
    for (_, _, rs, ss) in &cross {
        for row in &rows {
            if row.mirror == "-" {
                continue;
            }
            if rs.iter().any(|r| matches(&row.mirror, r))
                && ss.iter().any(|s| matches(&row.owner, s))
            {
                let family = ss.first().is_some_and(|s| s.ends_with('/'));
                if !exists(&row.mirror) || (!family && !exists(&row.owner)) {
                    findings.push(format!(
                        "PHANTOM PAIR {}: the registry names '{}' ← '{}' but the corpus does not carry the pair",
                        row.kind, row.mirror, row.owner
                    ));
                }
            }
        }
        for r in rs {
            let registered_mirror = rows.iter().any(|row| {
                row.mirror != "-"
                    && matches(r, &row.mirror)
                    && ss.iter().any(|s| matches(&row.owner, s))
            });
            if !registered_mirror {
                findings.push(format!(
                    "UNPAIRED RESTATER: '{r}' matches a restatement pattern but no registry row registers it as a mirror — a restatement nobody governs is how one fact becomes two"
                ));
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

/// The doctrine names the project slot registers, as `re.findall(r'^  "([A-Z-]+)\|', driver, re.M)` found them.
fn registered_doctrines(driver: &str) -> Vec<String> {
    driver
        .split('\n')
        .filter_map(|line| {
            let rest = line.strip_prefix("  \"")?;
            let name: String = rest
                .chars()
                .take_while(|c| c.is_ascii_uppercase() || *c == '-')
                .collect();
            (!name.is_empty() && rest[name.len()..].starts_with('|')).then_some(name)
        })
        .collect()
}

/// Symmetric directory-prefix matching: `definitions/` names `definitions/riscv/`, and `definitions/riscv/`
/// answers for `definitions/`.
fn matches(path: &str, pattern: &str) -> bool {
    let p = pattern.trim_end_matches('/');
    let s = path.trim_end_matches('/');
    s == p || s.starts_with(&format!("{p}/")) || p.starts_with(&format!("{s}/"))
}

/// A pattern's corpus files (the script's `expand`): a family `dir/` is present iff it holds a `.sexp` file
/// at any depth; any other pattern is its sorted `glob`.
fn expand(root: &Path, pattern: &str) -> Vec<String> {
    if pattern.ends_with('/') {
        let found = !glob(root, &format!("{pattern}**/*.sexp")).is_empty();
        return if found {
            vec![pattern.to_owned()]
        } else {
            Vec::new()
        };
    }
    let mut found = glob(root, pattern);
    found.sort();
    found
}

/// Python's `glob.glob(pattern, recursive=True)` over `root`, relative paths: a magic segment (`*`, `?`,
/// `[`) lists its directory and never matches a hidden name unless it starts with `.`; `**` is the directory
/// itself and every non-hidden subdirectory beneath it; a literal segment must exist (`lexists`).
fn glob(root: &Path, pattern: &str) -> Vec<String> {
    let mut current: Vec<String> = vec![String::new()];
    for segment in pattern.split('/') {
        let mut next = Vec::new();
        for prefix in &current {
            let dir = if prefix.is_empty() {
                root.to_path_buf()
            } else {
                root.join(prefix)
            };
            let join = |name: &str| {
                if prefix.is_empty() {
                    name.to_owned()
                } else {
                    format!("{prefix}/{name}")
                }
            };
            if segment == "**" {
                next.push(prefix.clone());
                descend(&dir, prefix, &mut next);
            } else if segment.contains(['*', '?', '[']) {
                let Ok(entries) = fs::read_dir(&dir) else {
                    continue;
                };
                let mut names: Vec<String> = entries
                    .flatten()
                    .map(|entry| entry.file_name().to_string_lossy().into_owned())
                    .filter(|name| {
                        (segment.starts_with('.') || !name.starts_with('.'))
                            && fnmatch(segment, name)
                    })
                    .collect();
                names.sort();
                next.extend(names.iter().map(|name| join(name)));
            } else if segment.is_empty() {
                // a trailing `/` (or `//`) names the directory itself, as Python keeps it
                next.push(join(""));
            } else {
                let candidate = join(segment);
                if fs::symlink_metadata(root.join(&candidate)).is_ok() {
                    next.push(candidate);
                }
            }
        }
        current = next;
        if current.is_empty() {
            break;
        }
    }
    current
}

/// Every non-hidden directory beneath `dir`, relative like `prefix`, depth first (the `**` expansion).
fn descend(dir: &Path, prefix: &str, out: &mut Vec<String>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    let mut names: Vec<String> = entries
        .flatten()
        .filter(|entry| entry.path().is_dir())
        .map(|entry| entry.file_name().to_string_lossy().into_owned())
        .filter(|name| !name.starts_with('.'))
        .collect();
    names.sort();
    for name in names {
        let rel = if prefix.is_empty() {
            name.clone()
        } else {
            format!("{prefix}/{name}")
        };
        out.push(rel.clone());
        descend(&dir.join(&name), &rel, out);
    }
}

/// `fnmatch.fnmatchcase`: `*` any run, `?` one character, `[seq]`/`[!seq]` a class with ranges.
fn fnmatch(pattern: &str, name: &str) -> bool {
    fn go(p: &[char], n: &[char]) -> bool {
        match p.first() {
            None => n.is_empty(),
            Some('*') => (0..=n.len()).any(|k| go(&p[1..], &n[k..])),
            Some('?') => !n.is_empty() && go(&p[1..], &n[1..]),
            Some('[') => {
                let Some(close) = p.iter().skip(1).position(|&c| c == ']') else {
                    return !n.is_empty() && n[0] == '[' && go(&p[1..], &n[1..]);
                };
                let class = &p[1..=close];
                let (negate, class) = match class.first() {
                    Some('!') => (true, &class[1..]),
                    _ => (false, class),
                };
                let Some(&c) = n.first() else { return false };
                let mut hit = false;
                let mut i = 0;
                while i < class.len() {
                    if i + 2 < class.len() && class[i + 1] == '-' {
                        hit |= class[i] <= c && c <= class[i + 2];
                        i += 3;
                    } else {
                        hit |= class[i] == c;
                        i += 1;
                    }
                }
                hit != negate && go(&p[close + 2..], &n[1..])
            }
            Some(&c) => !n.is_empty() && n[0] == c && go(&p[1..], &n[1..]),
        }
    }
    let p: Vec<char> = pattern.chars().collect();
    let n: Vec<char> = name.chars().collect();
    go(&p, &n)
}

/// Python's `repr` of a `list[str]`: `['a', 'b']`, double quotes when a string holds `'` and no `"`.
fn py_list(items: &[&str]) -> String {
    let reprs: Vec<String> = items
        .iter()
        .map(|item| {
            let quote = if item.contains('\'') && !item.contains('"') {
                '"'
            } else {
                '\''
            };
            let mut out = String::new();
            out.push(quote);
            for c in item.chars() {
                match c {
                    '\\' => out.push_str("\\\\"),
                    '\n' => out.push_str("\\n"),
                    '\t' => out.push_str("\\t"),
                    '\r' => out.push_str("\\r"),
                    c if c == quote => {
                        out.push('\\');
                        out.push(c);
                    }
                    c => out.push(c),
                }
            }
            out.push(quote);
            out
        })
        .collect();
    format!("[{}]", reprs.join(", "))
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: judging the fixture registry against `pairs` must give `expected` and its text must contain `want`.
    fn arm(
        &mut self,
        root: &Path,
        registry: &str,
        pairs: &[(&str, &str)],
        name: &str,
        expected: i32,
        want: &str,
    ) {
        let verdict = check_ownership(root, registry, pairs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "FACT-OWNERSHIP self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("FACT-OWNERSHIP self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// The ten arms over a scratch registry judged against the real corpus. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let Ok(t) = scratch(root, "target/doctrine-selftest", "fact-ownership") else {
        if verbose {
            eprintln!("FACT-OWNERSHIP self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let registry = t.join("reg.tsv");
    let reg = registry.to_string_lossy().into_owned();
    let write = |text: &str| {
        let _ = fs::write(&registry, text);
    };
    // fixture corpus pair: obligations restate requirements — named in the GREEN fixture registry, omitted
    // from the RED one, so the completeness arm has something to catch. The pair spec globs the REAL corpus,
    // so the GREEN fixture names every unit that carries the catalogues (six since P4-SYSTEM.1).
    let fixture_pairs: &[(&str, &str)] = &[(
        "profiles/*/contract-obligations.sexp",
        "profiles/*/requirements.sexp",
    )];
    write("# fixture registry\n\
configuration\tprofiles/rv64i-lab-v0/profile.sexp\t-\t-\n\
state\tprofiles/rv64i-lab-v0/state.sexp\tprofiles/rv64i-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n\
requirements\tprofiles/rv64i-lab-v0/profile.sexp\tprofiles/rv64i-lab-v0/requirements.sexp\tRECORD-SCHEMA\n\
encodings\tdefinitions/riscv/\tprofiles/rv64i-lab-v0/encoding.sexp\tUNIT-COMPOSITION\n\
obligations\tprofiles/rv64i-lab-v0/requirements.sexp\tprofiles/rv64i-lab-v0/contract-obligations.sexp\tRECORD-SCHEMA\n\
obligations (dsp56300-lab-v0)\tprofiles/dsp56300-lab-v0/requirements.sexp\tprofiles/dsp56300-lab-v0/contract-obligations.sexp\tRECORD-SCHEMA\n\
obligations (sifive-uart-lab-v0)\tprofiles/sifive-uart-lab-v0/requirements.sexp\tprofiles/sifive-uart-lab-v0/contract-obligations.sexp\tRECORD-SCHEMA\n\
obligations (lan9118-lab-v0)\tprofiles/lan9118-lab-v0/requirements.sexp\tprofiles/lan9118-lab-v0/contract-obligations.sexp\tRECORD-SCHEMA\n\
obligations (netboard-lab-v0)\tprofiles/netboard-lab-v0/requirements.sexp\tprofiles/netboard-lab-v0/contract-obligations.sexp\tRECORD-SCHEMA\n\
obligations (rv64gc-lab-v0)\tprofiles/rv64gc-lab-v0/requirements.sexp\tprofiles/rv64gc-lab-v0/contract-obligations.sexp\tRECORD-SCHEMA\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "GREEN a well-formed registry naming every fixture pair",
        0,
        "__CHECKED__ 10",
    );
    write("state\tprofiles/rv64i-lab-v0/state.sexp\tprofiles/rv64i-lab-v0/profile.sexp\tNOT-A-DOCTRINE\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "RED   a governor that is not a registered doctrine",
        1,
        "UNREGISTERED GOVERNOR",
    );
    write("state\tprofiles/rv64i-lab-v0/state.sexp\tprofiles/rv64i-lab-v0/profile.sexp\t-\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "RED   a mirror with no governor — the ungoverned duplication",
        1,
        "UNGOVERNED MIRROR",
    );
    write("state\tprofiles/rv64i-lab-v0/ghost.sexp\t-\t-\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "RED   an owner that does not exist",
        1,
        "MISSING OWNER",
    );
    write("state\tprofiles/rv64i-lab-v0/state.sexp\t-\tRECORD-SCHEMA\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "RED   a governor named over nothing",
        1,
        "GOVERNOR WITHOUT MIRROR",
    );
    write("state\tprofiles/rv64i-lab-v0/state.sexp\t-\t-\nstate\tprofiles/rv64i-lab-v0/profile.sexp\t-\t-\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "RED   one fact kind, two owning files",
        1,
        "TWO OWNERS",
    );
    write("state\tprofiles/rv64i-lab-v0/state.sexp\t-\t-\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "RED   a fixture pair the registry does not name",
        1,
        "UNREGISTERED MIRROR PAIR",
    );
    // the second-unit census (P3-BREADTH.7): same-unit pairing, measured against the real corpus — a
    // cross-product enumeration would invent cross-unit pairs; the pairing must follow the unit capture.
    let same_unit: &[(&str, &str)] = &[("profiles/*/profile.sexp", "profiles/*/state.sexp")];
    write("state (rv64i-lab-v0)\tprofiles/rv64i-lab-v0/state.sexp\tprofiles/rv64i-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n\
state (dsp56300-lab-v0)\tprofiles/dsp56300-lab-v0/state.sexp\tprofiles/dsp56300-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n\
state (sifive-uart-lab-v0)\tprofiles/sifive-uart-lab-v0/state.sexp\tprofiles/sifive-uart-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n\
state (lan9118-lab-v0)\tprofiles/lan9118-lab-v0/state.sexp\tprofiles/lan9118-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n\
state (rv64gc-lab-v0)\tprofiles/rv64gc-lab-v0/state.sexp\tprofiles/rv64gc-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n");
    tally.arm(
        root,
        &reg,
        same_unit,
        "GREEN five units, each pair registered — no cross-unit pair invented",
        0,
        "__CHECKED__ 5",
    );
    write("state (rv64i-lab-v0)\tprofiles/rv64i-lab-v0/state.sexp\tprofiles/rv64i-lab-v0/profile.sexp\tPROFILE-CONSISTENCY\n");
    tally.arm(
        root,
        &reg,
        same_unit,
        "RED   the second unit's same-unit pair must be registered, named",
        1,
        "UNREGISTERED MIRROR PAIR",
    );
    write("bad row without enough cells\n");
    tally.arm(
        root,
        &reg,
        fixture_pairs,
        "REFUSE a malformed registry, never judge it",
        2,
        "BAD ROW",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "FACT-OWNERSHIP --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn python_shapes_are_reproduced() {
        assert!(fnmatch("*.sexp", "a.sexp") && !fnmatch("*.sexp", "a.sexpx") && fnmatch("?", "x"));
        assert!(fnmatch("[a-c]x", "bx") && !fnmatch("[!a-c]x", "bx") && fnmatch("[", "["));
        assert_eq!(py_list(&["b", "a'c"]), "['b', \"a'c\"]");
        assert!(
            matches("definitions/riscv/", "definitions/")
                && matches("definitions/", "definitions/riscv/")
        );
        assert!(!matches("definitions-x", "definitions"));
        assert_eq!(
            registered_doctrines("x\n  \"FOO-BAR|desc|path\"\n  \"bad|\n  \"Baz|\n"),
            vec!["FOO-BAR"]
        );
    }
}
