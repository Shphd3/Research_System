"""Resolve research links and recorded relocations without changing source authority."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LOCATIONS = ROOT / "docs/research_locations.json"
LINK_START = re.compile(r"!?\[(?:\\.|[^\]\n])*\]\(")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


@dataclass(frozen=True)
class LinkMatch:
    text: str
    begin: int
    finish: int
    destination_start: int
    destination_end: int

    def start(self):
        return self.begin

    def end(self):
        return self.finish

    def __getitem__(self, key):
        if key == 0:
            return self.text[self.begin:self.finish]
        return {'prefix': self.text[self.begin:self.destination_start],
                'target': self.text[self.destination_start:self.destination_end],
                'end': self.text[self.destination_end:self.finish]}[key]


def inline_matches(text: str):
    """Keep offsets, balanced destinations, angle brackets and optional titles."""
    for start in LINK_START.finditer(text):
        i = start.end()
        while i < len(text) and text[i] in ' \t':
            i += 1
        dest_start = i
        if i < len(text) and text[i] == '<':
            i += 1
            while i < len(text) and text[i] not in '>\n':
                i += 2 if text[i] == '\\' else 1
            if i == len(text) or text[i] != '>':
                continue
            i += 1
        else:
            depth = 0
            while i < len(text) and text[i] not in ' \t\n':
                if text[i] == '\\':
                    i += 2
                    continue
                if text[i] == '(':
                    depth += 1
                elif text[i] == ')':
                    if depth == 0:
                        break
                    depth -= 1
                i += 1
            if depth:
                continue
        dest_end = i
        while i < len(text) and text[i] in ' \t':
            i += 1
        if i < len(text) and text[i] in '\"\'(':
            closing = ')' if text[i] == '(' else text[i]
            i += 1
            while i < len(text) and text[i] not in (closing, '\n'):
                i += 2 if text[i] == '\\' else 1
            if i >= len(text) or text[i] != closing:
                continue
            i += 1
            while i < len(text) and text[i] in ' \t':
                i += 1
        if i < len(text) and text[i] == ')':
            yield LinkMatch(text, start.start(), i + 1, dest_start, dest_end)


def masked_prose(text: str) -> str:
    """Preserve offsets/newlines while hiding code and math from link scanners."""
    masked = list(text)
    spans = []
    fence_start = None
    offset = 0
    for line in text.splitlines(keepends=True):
        fence = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            mark = fence[1]
            if fence_start is None:
                fence_start = (offset, mark[0], len(mark))
            elif mark[0] == fence_start[1] and len(mark) >= fence_start[2]:
                spans.append((fence_start[0], offset + len(line)))
                fence_start = None
        offset += len(line)
    if fence_start is not None:
        spans.append((fence_start[0], len(text)))
    for start, end in spans:
        masked[start:end] = ['\n' if c == '\n' else ' ' for c in text[start:end]]
    remaining = ''.join(masked)
    pattern = re.compile(r'(`+)([^`]*?)\1|\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<!\\)\$[^$\n]+(?<!\\)\$', re.S)
    for match in pattern.finditer(remaining):
        masked[match.start():match.end()] = ['\n' if c == '\n' else ' ' for c in match[0]]
    return ''.join(masked)


def link_matches(text: str):
    """Ignore code and math: bracket/parenthesis expressions are not file links."""
    for match in inline_matches(masked_prose(text)):
        yield LinkMatch(text, match.begin, match.finish, match.destination_start, match.destination_end)


def reference_matches(text: str):
    """Single-line reference definitions; leave labels and titles unchanged."""
    pattern = re.compile(r'^ {0,3}\[(?:\\.|[^\]\\\n])+\]:[ \t]*(?P<target><[^>\n]+>|(?:\\.|[^\s])+)', re.M)
    for match in pattern.finditer(masked_prose(text)):
        yield LinkMatch(text, match.start(), match.end(), match.start('target'), match.end('target'))


def relocations(root: Path = ROOT) -> dict[str, str]:
    path = root / "docs/research_locations.json"
    if not path.is_file():
        return {}
    return {row["old"]: row["new"] for row in json.loads(path.read_text())["files"]}


def link_path(target: str, source: Path, root: Path = ROOT) -> tuple[Path | None, str]:
    """Read a local Markdown target; keep fragments and URL-encoded filenames."""
    target = target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")]
    else:
        target = re.split(r'\s+[\"\']', target, maxsplit=1)[0]
    if not target or target.startswith("#") or SCHEME.match(target) or target.startswith("//"):
        return None, ""
    path, sep, fragment = target.partition("#")
    path = re.sub(r'\\([!\"#$%&\'()*+,./:;<=>?@\[\]\\^_`{|}~-])', r'\1', unquote(path))
    if not path:
        return None, ""
    line_suffix = re.search(r':\d+(?::\d+)?$', path)
    suffix = ''
    if line_suffix:
        suffix = line_suffix[0]
        path = path[:line_suffix.start()]
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = (root if path.startswith(('Projects/', '.agents/')) else source.parent) / candidate
    return Path(os.path.abspath(candidate)), suffix + sep + fragment


def relocated(path: Path, mapping: dict[str, str], root: Path = ROOT) -> Path:
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError:
        return path
    # A previously relocated reading file may later be archived again.
    # Follow its recorded destinations without rewriting historical entries.
    visited = set()
    while relative in mapping and mapping[relative] != relative:
        if relative in visited:
            raise ValueError(f"Cyclic research relocation: {relative}")
        visited.add(relative)
        relative = mapping[relative]
    return root / relative


def local_links(text: str, source: Path, root: Path = ROOT):
    for match in link_matches(text):
        path, fragment = link_path(match["target"], source, root)
        if path is not None:
            yield match, path, fragment


def rebase_links(text: str, old: Path, new: Path, mapping: dict[str, str], root: Path = ROOT) -> str:
    def replace(match):
        path, fragment = link_path(match["target"], old, root)
        if path is None:
            return match[0]
        dest = relocated(path, mapping, root)
        # A relative worker path must not change meaning when its document moves.
        if not dest.is_relative_to(root):
            if old.parent == new.parent:
                return match[0]
            relative = str(dest) + fragment
        else:
            relative = os.path.relpath(dest, new.parent).replace(os.sep, "/") + fragment
        if any(c in relative for c in " ()"):
            relative = "<" + relative + ">"
        return match["prefix"] + relative + match["end"]

    result, end = [], 0
    for match in link_matches(text):
        result.extend([text[end:match.start()], replace(match)])
        end = match.end()
    result.append(text[end:])
    return ''.join(result)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Old or current path, absolute or relative to Research_System")
    args = parser.parse_args()
    path = Path(args.path)
    if not path.is_absolute():
        path = ROOT / path
    result = relocated(Path(os.path.abspath(path)), relocations())
    print(result)
    return 0 if result.exists() else 1


if __name__ == "__main__":
    raise SystemExit(main())
