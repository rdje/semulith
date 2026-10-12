#!/usr/bin/env python3
"""Owned documentation paths shared by the book and include validators."""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import re

PROJECT = Path(__file__).resolve().parent.parent


class BookRefused(ValueError):
    """Unsafe metadata or an input that cannot supply a book verdict."""


def owned_root(root: Path) -> Path:
    root = root.resolve()
    if not root.is_dir() or not root.is_relative_to(PROJECT):
        raise BookRefused('corpus root must be inside this project')
    if root.stat().st_dev != PROJECT.stat().st_dev:
        raise BookRefused('corpus root is on another volume')
    parent = root
    while parent != PROJECT:
        marker = parent / '.git'
        if marker.exists() or marker.is_symlink():
            raise BookRefused('corpus root crosses another Git boundary')
        parent = parent.parent
    return root


def book_path(root: Path, value: str) -> Path:
    """A source book must be a canonical relative path in this corpus's models."""
    clean = value.rstrip('/')
    parts = clean.split('/')
    if (not clean or '\\' in clean or any(ord(c) < 32 for c in clean) or
            re.match(r'^[A-Za-z]:', clean) or PurePosixPath(clean).is_absolute() or
            any(p in {'', '.', '..', '.git'} for p in parts) or
            len(parts) < 3 or parts[:2] != ['docs', 'models']):
        raise BookRefused('UNSAFE BOOK PATH ' + value)
    return source_path(root, clean)


def source_path(root: Path, relative: str) -> Path:
    """Check every existing component before reading/building an owned input."""
    cursor = root
    for part in PurePosixPath(relative).parts:
        cursor = cursor / part
        marker = cursor / '.git'
        if cursor.is_symlink() or marker.exists() or marker.is_symlink():
            raise BookRefused('UNSAFE BOOK PATH symlink/Git boundary: ' + relative)
        if cursor.exists() and cursor.stat().st_dev != root.stat().st_dev:
            raise BookRefused('UNSAFE BOOK PATH another volume: ' + relative)
    return cursor


