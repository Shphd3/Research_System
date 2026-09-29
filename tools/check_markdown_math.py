#!/usr/bin/env python3
"""Check Markdown math source, not rendered appearance or mathematical truth.

Adapted in purpose from memxlife/research-exploration-skill at 0963fe5;
see THIRD_PARTY_NOTICES.md. Default: repository Codex delimiters. Use
--allow-dollar-math only for a separately requested dollar-style reading copy.
Literal code, comments and URLs are excluded; files are never rewritten.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def _blank(match: re.Match[str]) -> str:
    return ''.join('\n' if c == '\n' else ' ' for c in match.group())


def _visible(text: str) -> tuple[list[str], list[str]]:
    text = re.sub(r'<!--.*?-->', _blank, text, flags=re.S)
    errors: list[str] = []
    lines: list[str] = []
    fence: tuple[str, int, int] | None = None
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if m and fence is None:
            fence = (m[1][0], len(m[1]), n)
            lines.append('')
        elif fence is not None:
            if m and m[1][0] == fence[0] and len(m[1]) >= fence[1] and not m[2].strip():
                fence = None
            lines.append('')
        else:
            lines.append(line)
    if fence is not None:
        errors.append(f'line {fence[2]}: unclosed literal code fence')
    visible = '\n'.join(lines)
    visible = re.sub(r'(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)', _blank, visible, flags=re.S)
    visible = re.sub(r'https?://[^\s<>]+', _blank, visible)
    return visible.split('\n'), errors


def _braces(body: str) -> bool:
    depth = 0
    for match in re.finditer(r'(?<!\\)[{}]', body):
        depth += 1 if match.group() == '{' else -1
        if depth < 0:
            return False
    return depth == 0


def check_text(text: str, *, allow_dollar: bool = False) -> list[str]:
    """Return source diagnostics. This is a scoped heuristic, not a TeX parser."""
    lines, errors = _visible(text)
    display: tuple[int, str] | None = None
    body: list[str] = []
    for i, line in enumerate(lines):
        n, stripped = i + 1, line.strip()
        if display:
            if stripped == display[1]:
                if not ''.join(body).strip():
                    errors.append(f'line {display[0]}: empty display math')
                if not _braces('\n'.join(body)):
                    errors.append(f'line {display[0]}: unbalanced display braces')
                if i + 1 < len(lines) and lines[i + 1].strip():
                    errors.append(f'line {n}: display needs a following blank line')
                display, body = None, []
            else:
                if any(d in line for d in (r'\[', r'\]', r'\(', r'\)')):
                    errors.append(f'line {n}: nested or mismatched math delimiter')
                body.append(line)
            continue
        if stripped in (r'\[', '$$'):
            if stripped == '$$' and not allow_dollar:
                errors.append(f'line {n}: dollar display is not the canonical style')
            if i and lines[i - 1].strip():
                errors.append(f'line {n}: display needs a preceding blank line')
            display = (n, r'\]' if stripped == r'\[' else '$$')
            continue
        if re.search(r'\\{2,}[()[\]]', line):
            errors.append(f'line {n}: doubled delimiter backslash')
        # Consume same-line canonical inline expressions before checking leftovers.
        def consume(m: re.Match[str]) -> str:
            value = m[1]
            if not value.strip():
                errors.append(f'line {n}: empty inline math')
            if r'\(' in value or not _braces(value):
                errors.append(f'line {n}: nested inline delimiter or unbalanced braces')
            return ' ' * len(m.group())
        rest = re.sub(r'(?<!\\)\\\((.*?)\\\)', consume, line)
        if any(d in rest for d in (r'\(', r'\)', r'\[', r'\]')):
            errors.append(f'line {n}: unbalanced inline or non-standalone display delimiter')
        # Currency and shell variables are not assumed to be math. Only clear pairs count.
        dollar = re.compile(r'(?<![\\$])\$(?![\d\s$])([^$\n]*?\S)\$(?!\w)')
        if dollar.search(rest) and not allow_dollar:
            errors.append(f'line {n}: dollar inline math is not the canonical style')
        rest = dollar.sub(' ', rest)
        if '$$' in rest:
            errors.append(f'line {n}: display delimiters must stand alone')
        if re.search(r'\\[A-Za-z]+', rest):
            errors.append(f'line {n}: probable raw TeX outside math or literal code')
    if display:
        errors.append(f'line {display[0]}: unclosed display math')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-dollar-math', action='store_true')
    parser.add_argument('files', nargs='+', type=Path)
    args = parser.parse_args()
    failures = 0
    for path in args.files:
        try:
            errors = check_text(path.read_text(encoding='utf-8'), allow_dollar=args.allow_dollar_math)
        except (OSError, UnicodeError) as exc:
            errors = [str(exc)]
        for error in errors:
            print(f'{path}: {error}')
        failures += len(errors)
    print(f'SOURCE {"FAIL" if failures else "PASS"}: {len(args.files)} file(s), '
          f'{failures} issue(s); rendering and mathematical truth NOT checked.')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
