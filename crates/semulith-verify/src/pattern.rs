//! A regular-expression subset for the schema layer's `pattern` keyword.
//!
//! The tracked schemas use exactly two patterns — `^[A-Za-z][A-Za-z0-9._:/-]*$` and
//! `^[0-9a-f]{64}$` — and the census contract is the same as the Python validator's:
//! **implement what the corpus uses, refuse everything else by name**. A pattern the
//! engine cannot express is [`Refusal`], never a silently weakened match — the soundness
//! property is the refusal, not the coverage (`scripts/validate_records.py` states it for
//! the Python side; this module is the Rust half).
//!
//! Supported constructs:
//!
//! - `^` and `$` anchors (anywhere: like the Python engine, they assert at that point);
//! - literal characters, including escaped punctuation (`\.` `\\` `\/` `\-` …);
//! - character classes `[...]` with ranges (`[a-z]`), negation (`[^...]`), a literal `-`
//!   at either edge, and the escapes `\\` `\]` inside a class;
//! - the quantifiers `*` `+` `?` `{n}` `{n,}` `{n,m}` over the previous atom, greedy with
//!   backtracking.
//!
//! Refused by name: alternation `|`, groups `()` and `(?…)`, backreferences, `.`,
//! lazy quantifiers (`*?`), and escapes outside the supported set.
//!
//! Matching is [`is_match`] — `re.search` semantics (an unanchored pattern may start
//! anywhere), backtracking over `char`s.

/// A pattern the engine does not implement. The reason names the construct — a refusal
/// is the honest answer, a guessed translation is not.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Refusal(pub String);

impl std::fmt::Display for Refusal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "unsupported pattern construct: {}", self.0)
    }
}

#[derive(Clone, Debug)]
enum Atom {
    /// One specific character.
    Literal(char),
    /// A (possibly negated) set of character ranges.
    Class {
        negated: bool,
        ranges: Vec<(char, char)>,
    },
}

#[derive(Clone, Copy, Debug)]
enum Quant {
    /// `*`
    Star,
    /// `+`
    Plus,
    /// `?`
    Opt,
    /// `{n}` or `{n,}` or `{n,m}`
    Rep { min: u32, max: Option<u32> },
}

#[derive(Clone, Copy, Debug)]
enum Anchor {
    /// `^`
    Start,
    /// `$`
    End,
}

#[derive(Clone, Debug)]
enum Piece {
    Anchor(Anchor),
    Atom(Atom, Quant),
}

/// A compiled pattern.
#[derive(Clone, Debug)]
pub struct Pattern {
    pieces: Vec<Piece>,
}

fn is_punctuation(c: char) -> bool {
    matches!(
        c,
        '.' | ','
            | ':'
            | ';'
            | '!'
            | '?'
            | '\''
            | '"'
            | '('
            | ')'
            | '['
            | ']'
            | '{'
            | '}'
            | '<'
            | '>'
            | '|'
            | '\\'
            | '/'
            | '-'
            | '+'
            | '*'
            | '='
            | '_'
            | '@'
            | '#'
            | '$'
            | '%'
            | '^'
            | '&'
            | '~'
            | '`'
    )
}

struct Cursor {
    chars: Vec<char>,
    pos: usize,
}

impl Cursor {
    fn peek(&self) -> Option<char> {
        self.chars.get(self.pos).copied()
    }
    fn bump(&mut self) -> Option<char> {
        let c = self.peek()?;
        self.pos += 1;
        Some(c)
    }
}

fn parse_atom(c: &mut Cursor) -> Result<Atom, Refusal> {
    match c.bump() {
        Some('[') => {
            let mut negated = false;
            if c.peek() == Some('^') {
                negated = true;
                c.bump();
            }
            let mut ranges = Vec::new();
            let mut first = true;
            loop {
                let lo = match c.bump() {
                    None => return Err(Refusal("an unterminated character class".into())),
                    Some(']') if !first => break,
                    Some('\\') => match c.bump() {
                        Some(']') => ']',
                        Some('\\') => '\\',
                        Some(other) => {
                            return Err(Refusal(format!(
                                "the class escape \\{other} (only \\\\ and \\] are supported)"
                            )));
                        }
                        None => {
                            return Err(Refusal("an unterminated class escape".into()));
                        }
                    },
                    Some(ch) => ch,
                };
                first = false;
                // a range only when '-' sits between two literals and is not the last member
                if c.peek() == Some('-') && c.chars.get(c.pos + 1).is_some_and(|&n| n != ']') {
                    c.bump(); // consume '-'
                    let hi = c
                        .bump()
                        .ok_or_else(|| Refusal("an unterminated character class".into()))?;
                    if hi == '[' || (lo > hi) {
                        return Err(Refusal(format!(
                            "the range {lo}-{hi} (empty or reversed ranges are not supported)"
                        )));
                    }
                    ranges.push((lo, hi));
                } else {
                    ranges.push((lo, lo));
                }
            }
            if ranges.is_empty() {
                return Err(Refusal("an empty character class".into()));
            }
            Ok(Atom::Class { negated, ranges })
        }
        Some('\\') => match c.bump() {
            Some(esc) if is_punctuation(esc) => Ok(Atom::Literal(esc)),
            Some(other) => Err(Refusal(format!(
                "the escape \\{other} (only punctuation escapes are supported)"
            ))),
            None => Err(Refusal("an unterminated escape".into())),
        },
        Some('(') | Some(')') => Err(Refusal(
            "groups (only the supported subset — literals, classes, quantifiers, anchors — \
             is implemented)"
                .into(),
        )),
        Some('.') => Err(Refusal(
            "'.' (only the supported subset — literals, classes, quantifiers, anchors — \
             is implemented)"
                .into(),
        )),
        Some(c) => Ok(Atom::Literal(c)),
        None => Err(Refusal("an unexpected end of pattern".into())),
    }
}

fn parse_quant(c: &mut Cursor) -> Result<Quant, Refusal> {
    match c.peek() {
        Some('*') => {
            c.bump();
            Ok(Quant::Star)
        }
        Some('+') => {
            c.bump();
            Ok(Quant::Plus)
        }
        Some('?') => {
            c.bump();
            Ok(Quant::Opt)
        }
        Some('{') => {
            c.bump();
            let mut min = String::new();
            while matches!(c.peek(), Some(d) if d.is_ascii_digit()) {
                min.push(c.bump().expect("peeked a digit"));
            }
            if min.is_empty() {
                return Err(Refusal("a repetition with no lower bound".into()));
            }
            let min: u32 = min.parse().map_err(|_| {
                Refusal("a repetition bound too large (u32 is the supported range)".into())
            })?;
            match c.bump() {
                Some('}') => Ok(Quant::Rep {
                    min,
                    max: Some(min),
                }),
                Some(',') => {
                    let mut max = String::new();
                    while matches!(c.peek(), Some(d) if d.is_ascii_digit()) {
                        max.push(c.bump().expect("peeked a digit"));
                    }
                    match c.bump() {
                        Some('}') if max.is_empty() => Ok(Quant::Rep { min, max: None }),
                        Some('}') => {
                            let max: u32 = max.parse().map_err(|_| {
                                Refusal(
                                    "a repetition bound too large (u32 is the supported range)"
                                        .into(),
                                )
                            })?;
                            if max < min {
                                return Err(Refusal(format!(
                                    "the repetition {{{min},{max}}} (max < min)"
                                )));
                            }
                            Ok(Quant::Rep {
                                min,
                                max: Some(max),
                            })
                        }
                        _ => Err(Refusal("an unterminated repetition".into())),
                    }
                }
                _ => Err(Refusal("an unterminated repetition".into())),
            }
        }
        _ => Ok(Quant::Rep {
            min: 1,
            max: Some(1),
        }),
    }
}

/// Compile a pattern. Any construct outside the supported subset is a [`Refusal`].
pub fn compile(pattern: &str) -> Result<Pattern, Refusal> {
    let mut c = Cursor {
        chars: pattern.chars().collect(),
        pos: 0,
    };
    let mut pieces = Vec::new();
    while let Some(ch) = c.peek() {
        match ch {
            '^' => {
                c.bump();
                pieces.push(Piece::Anchor(Anchor::Start));
            }
            '$' => {
                c.bump();
                pieces.push(Piece::Anchor(Anchor::End));
            }
            '|' => return Err(Refusal("alternation (…|…)".into())),
            _ => {
                let atom = parse_atom(&mut c)?;
                let quant = parse_quant(&mut c)?;
                // a lazy quantifier is a different engine contract — refuse, never approximate
                if c.peek() == Some('?')
                    && !matches!(
                        quant,
                        Quant::Rep {
                            min: 1,
                            max: Some(1)
                        }
                    )
                {
                    return Err(Refusal("lazy quantifiers (*? +? ?? {n,m}?)".into()));
                }
                pieces.push(Piece::Atom(atom, quant));
            }
        }
    }
    Ok(Pattern { pieces })
}

impl Atom {
    fn matches(&self, ch: char) -> bool {
        match self {
            Self::Literal(want) => *want == ch,
            Self::Class { negated, ranges } => {
                let inside = ranges.iter().any(|&(lo, hi)| (lo..=hi).contains(&ch));
                inside != *negated
            }
        }
    }
}

impl Pattern {
    /// Whether the pattern matches anywhere in `text` (Python `re.search` semantics).
    #[must_use]
    pub fn is_match(&self, text: &str) -> bool {
        let chars: Vec<char> = text.chars().collect();
        // a leading ^ anchors the whole match at position 0
        let anchored = matches!(self.pieces.first(), Some(Piece::Anchor(Anchor::Start)));
        if anchored {
            return self.match_from(&chars, 0);
        }
        (0..=chars.len()).any(|start| self.match_from(&chars, start))
    }

    fn match_from(&self, chars: &[char], start: usize) -> bool {
        match_pieces(&self.pieces, chars, start)
    }
}

fn quant_bounds(quant: Quant) -> (u32, Option<u32>) {
    match quant {
        Quant::Star => (0, None),
        Quant::Plus => (1, None),
        Quant::Opt => (0, Some(1)),
        Quant::Rep { min, max } => (min, max),
    }
}

/// Backtracking matcher: try to consume `pieces` starting at `pos`; for atoms with a
/// repetition, try the longest first so greedy semantics hold.
fn match_pieces(pieces: &[Piece], chars: &[char], pos: usize) -> bool {
    let Some((piece, rest)) = pieces.split_first() else {
        return true;
    };
    match piece {
        Piece::Anchor(Anchor::Start) => pos == 0 && match_pieces(rest, chars, pos),
        Piece::Anchor(Anchor::End) => pos == chars.len() && match_pieces(rest, chars, pos),
        Piece::Atom(atom, quant) => {
            let (min, max) = quant_bounds(*quant);
            let mut taken = 0u32;
            let mut at = pos;
            let limit = max.map_or(chars.len() - pos, |m| (m as usize).min(chars.len() - pos));
            while taken < limit as u32 && at < chars.len() && atom.matches(chars[at]) {
                taken += 1;
                at += 1;
            }
            // greedy: longest first, backtracking down to the minimum
            let mut try_taken = taken;
            loop {
                if try_taken >= min && match_pieces(rest, chars, pos + try_taken as usize) {
                    return true;
                }
                if try_taken == 0 {
                    return false;
                }
                try_taken -= 1;
            }
        }
    }
}

/// Compile and search in one call — the schema validator's shape.
pub fn is_match(pattern: &str, text: &str) -> Result<bool, Refusal> {
    Ok(compile(pattern)?.is_match(text))
}

#[cfg(test)]
mod tests;
