#!/usr/bin/env python3
"""Preserve expectation text while changing only its direct fetch-count field.

The canonical parser validates the stream; token spans keep strings, comments,
whitespace and every other field byte-for-byte. Shared by the author and governor.
"""
from __future__ import annotations

import sexp as S

# Strings and comments are indivisible tokens: a textual "(fetches ...)" there
# must never become a field. The canonical parser validates the complete stream.
TOKENS = S.TOKENS


def with_fetches(text, value):
    """Insert/replace exactly one direct field, preserving every other byte."""
    if type(value) is not int or value < 0:
        raise S.SexpError('fetch count must be a nonnegative integer')
    forms = S.parse(text)
    records = [f for f in forms if isinstance(f, list) and f and f[0] == 'expectations']
    if len(records) != 1:
        raise S.SexpError('mirror needs exactly one expectations form')
    record = records[0]
    S.field(record, 'instructions')
    if S.children(record, 'fetches'):
        S.field(record, 'fetches')  # refuse duplicate/malformed fields before surgery
    stack, fields = [], {}
    for token in TOKENS.finditer(text):
        word = token[0]
        if word.startswith(';'):
            continue
        if word == '(':
            stack.append([token.start(), None])
        elif word == ')':
            start, head = stack.pop()
            if len(stack) == 1 and stack[0][1] == 'expectations' and head in ('instructions', 'fetches'):
                fields[head] = (start, token.end())
        elif stack and stack[-1][1] is None:
            stack[-1][1] = word
    if 'instructions' not in fields:
        raise S.SexpError('cannot locate the canonical direct instructions field')
    replacement = f'(fetches {value})'
    if 'fetches' in fields:
        start, end = fields['fetches']
        return text[:start] + replacement + text[end:]
    _, end = fields['instructions']
    return text[:end] + ' ' + replacement + text[end:]

