//! A JSON reader for the evidence machinery — the verify crates carry no dependencies
//! (`P1-LAB.1`), so the reader is ours.
//!
//! The reference contract is `scripts/validate_records.py`: it validates the frozen
//! `examples/*.jsonl` records with Python's `json` module, and this reader must agree with
//! that module's verdicts on the tracked corpus:
//!
//! - duplicate object keys: **last wins** (`json.loads` parity; the corpus has none, and a
//!   reader that refused them would be a different contract, not a stricter one);
//! - numbers: an integer literal becomes [`Json::Int`], anything with a fraction or exponent
//!   becomes [`Json::Float`] — Python's `int`/`float` distinction, kept explicitly because the
//!   schema layer types on it ("integer" accepts only `Int`, "number" accepts both, and a
//!   `Bool` is never an `Int` — in Python `isinstance(True, int)` is true and the validator
//!   has to guard it by hand; here the variants are simply different);
//! - a `Float` that overflows to infinity (e.g. `1e400`) parses as such, matching
//!   `json.loads`; the tracked schemas never accept a float, so this stays a reader fact,
//!   not a validation loophole.
//!
//! A malformed document is a parse [`Error`] that names the line and column — a checker that
//! reads evidence must say *where* the bytes stopped being JSON, never "not valid" alone.

use std::fmt;

/// A parsed JSON document.
#[derive(Clone, Debug, PartialEq)]
pub enum Json {
    /// JSON `null`.
    Null,
    /// JSON `true` / `false` — never an [`Json::Int`], however Python blurs them.
    Bool(bool),
    /// An integer literal (`-?(0|[1-9][0-9]*)`), arbitrary precision within `i128`.
    Int(i128),
    /// A number with a fraction or exponent.
    Float(f64),
    /// A JSON string.
    Str(String),
    /// A JSON array.
    Arr(Vec<Json>),
    /// A JSON object as ordered pairs; lookup is last-wins on duplicate keys.
    Obj(Vec<(String, Json)>),
}

impl Json {
    /// The string value of a `"string"` typed node, else `None`.
    #[must_use]
    pub fn as_str(&self) -> Option<&str> {
        match self {
            Self::Str(s) => Some(s),
            _ => None,
        }
    }

    /// The array value of an `"array"` typed node, else `None`.
    #[must_use]
    pub fn as_arr(&self) -> Option<&[Json]> {
        match self {
            Self::Arr(items) => Some(items),
            _ => None,
        }
    }

    /// The pairs of an `"object"` typed node, else `None`.
    #[must_use]
    pub fn as_obj(&self) -> Option<&[(String, Json)]> {
        match self {
            Self::Obj(pairs) => Some(pairs),
            _ => None,
        }
    }

    /// Last-wins object lookup (Python `json.loads` parity).
    #[must_use]
    pub fn get(&self, key: &str) -> Option<&Json> {
        self.as_obj()
            .and_then(|pairs| pairs.iter().rev().find(|(k, _)| k == key).map(|(_, v)| v))
    }

    /// Whether a `"boolean"` typed node holds `true`.
    #[must_use]
    pub fn as_bool(&self) -> Option<bool> {
        match self {
            Self::Bool(b) => Some(*b),
            _ => None,
        }
    }
}

/// A parse failure with a 1-based line and column.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Error {
    /// 1-based line of the offending byte.
    pub line: usize,
    /// 1-based column of the offending byte.
    pub column: usize,
    /// What the reader expected and what it saw.
    pub message: String,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}:{}: {}", self.line, self.column, self.message)
    }
}

/// Parse a complete JSON document. Trailing content after the top-level value is an error —
/// a record file is one value and nothing else.
pub fn parse(text: &str) -> Result<Json, Error> {
    let mut p = Parser {
        bytes: text.as_bytes(),
        pos: 0,
        line: 1,
        column: 1,
    };
    p.skip_ws();
    let value = p.value()?;
    p.skip_ws();
    if p.pos != p.bytes.len() {
        return Err(p.error("trailing content after the top-level value"));
    }
    Ok(value)
}

struct Parser<'a> {
    bytes: &'a [u8],
    pos: usize,
    line: usize,
    column: usize,
}

impl<'a> Parser<'a> {
    fn error(&self, message: &str) -> Error {
        Error {
            line: self.line,
            column: self.column,
            message: message.to_string(),
        }
    }

    fn bump(&mut self) -> Option<u8> {
        let b = *self.bytes.get(self.pos)?;
        self.pos += 1;
        if b == b'\n' {
            self.line += 1;
            self.column = 1;
        } else {
            self.column += 1;
        }
        Some(b)
    }

    fn peek(&self) -> Option<u8> {
        self.bytes.get(self.pos).copied()
    }

    fn skip_ws(&mut self) {
        while matches!(self.peek(), Some(b' ' | b'\t' | b'\n' | b'\r')) {
            self.bump();
        }
    }

    fn expect(&mut self, b: u8) -> Result<(), Error> {
        match self.peek() {
            Some(got) if got == b => {
                self.bump();
                Ok(())
            }
            _ => Err(self.error(&format!("expected '{}'", b as char))),
        }
    }

    fn value(&mut self) -> Result<Json, Error> {
        match self.peek() {
            Some(b'{') => self.object(),
            Some(b'[') => self.array(),
            Some(b'"') => Ok(Json::Str(self.string()?)),
            Some(b't') => self.literal("true", Json::Bool(true)),
            Some(b'f') => self.literal("false", Json::Bool(false)),
            Some(b'n') => self.literal("null", Json::Null),
            Some(b'-' | b'0'..=b'9') => self.number(),
            Some(_) => Err(self.error("unexpected character")),
            None => Err(self.error("unexpected end of input")),
        }
    }

    fn literal(&mut self, word: &str, value: Json) -> Result<Json, Error> {
        for &b in word.as_bytes() {
            match self.peek() {
                Some(got) if got == b => {
                    self.bump();
                }
                _ => {
                    return Err(self.error(&format!("invalid literal, expected '{word}'")));
                }
            }
        }
        Ok(value)
    }

    fn object(&mut self) -> Result<Json, Error> {
        self.expect(b'{')?;
        let mut pairs = Vec::new();
        self.skip_ws();
        if self.peek() == Some(b'}') {
            self.bump();
            return Ok(Json::Obj(pairs));
        }
        loop {
            self.skip_ws();
            if self.peek() != Some(b'"') {
                return Err(self.error("expected an object key (a string)"));
            }
            let key = self.string()?;
            self.skip_ws();
            self.expect(b':')?;
            self.skip_ws();
            let value = self.value()?;
            pairs.push((key, value));
            self.skip_ws();
            match self.bump() {
                Some(b',') => continue,
                Some(b'}') => break,
                _ => return Err(self.error("expected ',' or '}' in an object")),
            }
        }
        Ok(Json::Obj(pairs))
    }

    fn array(&mut self) -> Result<Json, Error> {
        self.expect(b'[')?;
        let mut items = Vec::new();
        self.skip_ws();
        if self.peek() == Some(b']') {
            self.bump();
            return Ok(Json::Arr(items));
        }
        loop {
            self.skip_ws();
            items.push(self.value()?);
            self.skip_ws();
            match self.bump() {
                Some(b',') => continue,
                Some(b']') => break,
                _ => return Err(self.error("expected ',' or ']' in an array")),
            }
        }
        Ok(Json::Arr(items))
    }

    fn string(&mut self) -> Result<String, Error> {
        self.expect(b'"')?;
        let mut out = String::new();
        loop {
            match self.bump() {
                None => return Err(self.error("unterminated string")),
                Some(b'"') => return Ok(out),
                Some(b'\\') => match self.bump() {
                    Some(b'"') => out.push('"'),
                    Some(b'\\') => out.push('\\'),
                    Some(b'/') => out.push('/'),
                    Some(b'b') => out.push('\u{0008}'),
                    Some(b'f') => out.push('\u{000C}'),
                    Some(b'n') => out.push('\n'),
                    Some(b'r') => out.push('\r'),
                    Some(b't') => out.push('\t'),
                    Some(b'u') => {
                        let hi = self.hex4()?;
                        let ch = if (0xD800..0xDC00).contains(&hi) {
                            // a high surrogate must pair with a following \uXXXX low surrogate
                            if self.bump() != Some(b'\\') || self.bump() != Some(b'u') {
                                return Err(self.error("lone high surrogate in a string escape"));
                            }
                            let lo = self.hex4()?;
                            if !(0xDC00..0xE000).contains(&lo) {
                                return Err(self.error("invalid low surrogate in a string escape"));
                            }
                            let cp = 0x10000 + ((hi - 0xD800) << 10) + (lo - 0xDC00);
                            char::from_u32(cp).ok_or_else(|| {
                                self.error("surrogate pair outside the Unicode range")
                            })?
                        } else if (0xDC00..0xE000).contains(&hi) {
                            return Err(self.error("lone low surrogate in a string escape"));
                        } else {
                            char::from_u32(hi).ok_or_else(|| {
                                self.error("escape sequence outside the Unicode range")
                            })?
                        };
                        out.push(ch);
                    }
                    _ => return Err(self.error("invalid escape sequence in a string")),
                },
                Some(b) if b < 0x20 => {
                    return Err(self.error("unescaped control character in a string"));
                }
                Some(b) => {
                    // Collect the rest of this UTF-8 sequence (the input is `&str`, so the
                    // bytes of one scalar arrive contiguously and validly).
                    let width =
                        utf8_width(b).ok_or_else(|| self.error("invalid UTF-8 in a string"))?;
                    let start = self.pos - 1;
                    let end = start + width;
                    if end > self.bytes.len() {
                        return Err(self.error("truncated UTF-8 in a string"));
                    }
                    let s = std::str::from_utf8(&self.bytes[start..end])
                        .map_err(|_| self.error("invalid UTF-8 in a string"))?;
                    out.push_str(s);
                    for _ in 1..width {
                        self.bump();
                    }
                }
            }
        }
    }

    fn hex4(&mut self) -> Result<u32, Error> {
        let mut v = 0u32;
        for _ in 0..4 {
            let b = self
                .bump()
                .ok_or_else(|| self.error("truncated \\u escape"))?;
            let d = (b as char)
                .to_digit(16)
                .ok_or_else(|| self.error("non-hex digit in a \\u escape"))?;
            v = v * 16 + d;
        }
        Ok(v)
    }

    fn number(&mut self) -> Result<Json, Error> {
        let start = self.pos;
        if self.peek() == Some(b'-') {
            self.bump();
        }
        match self.peek() {
            Some(b'0') => {
                self.bump();
                if matches!(self.peek(), Some(b'0'..=b'9')) {
                    return Err(self.error("invalid number: leading zeros are not allowed"));
                }
            }
            Some(b'1'..=b'9') => {
                while matches!(self.peek(), Some(b'0'..=b'9')) {
                    self.bump();
                }
            }
            _ => return Err(self.error("invalid number: expected a digit")),
        }
        let mut is_float = false;
        if self.peek() == Some(b'.') {
            is_float = true;
            self.bump();
            if !matches!(self.peek(), Some(b'0'..=b'9')) {
                return Err(self.error("invalid number: expected a digit after '.'"));
            }
            while matches!(self.peek(), Some(b'0'..=b'9')) {
                self.bump();
            }
        }
        if matches!(self.peek(), Some(b'e' | b'E')) {
            is_float = true;
            self.bump();
            if matches!(self.peek(), Some(b'+' | b'-')) {
                self.bump();
            }
            if !matches!(self.peek(), Some(b'0'..=b'9')) {
                return Err(self.error("invalid number: expected a digit in the exponent"));
            }
            while matches!(self.peek(), Some(b'0'..=b'9')) {
                self.bump();
            }
        }
        let literal = std::str::from_utf8(&self.bytes[start..self.pos])
            .map_err(|_| self.error("invalid UTF-8 in a number"))?;
        if is_float {
            literal
                .parse::<f64>()
                .map(Json::Float)
                .map_err(|_| self.error("number out of range"))
        } else {
            match literal.parse::<i128>() {
                Ok(v) => Ok(Json::Int(v)),
                Err(_) => Err(self.error("integer literal out of i128 range")),
            }
        }
    }
}

fn utf8_width(first: u8) -> Option<usize> {
    match first {
        0x00..=0x7F => Some(1),
        0xC2..=0xDF => Some(2),
        0xE0..=0xEF => Some(3),
        0xF0..=0xF4 => Some(4),
        _ => None,
    }
}

#[cfg(test)]
mod tests;
