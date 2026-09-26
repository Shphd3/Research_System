#!/usr/bin/env python3
"""Check local Skill metadata and links after Skill edits; not a research gate.

Requires PyYAML (also used by skill-creator's validator). Run from any cwd:
    python tools/check_skills.py
Use --skills-root for an isolated fixture or another checkout, --json for data.
This checks local structure, not model behavior or scientific authorization.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required; run in the skill-creator Python environment.")


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^]\n]*\]\((<[^>\n]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")


def prose_lines(text: str):
    """Exclude literal examples from link validation."""
    fence = None
    for line in text.splitlines():
        match = re.match(r"\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield line


def validate(skills_root: Path) -> dict:
    errors, entries, seen = [], [], {}
    links_checked = 0
    directories = sorted(p for p in skills_root.iterdir() if p.is_dir()) if skills_root.is_dir() else []
    if not directories:
        errors.append(f"No skill directories: {skills_root}")
    for folder in directories:
        source = folder / "SKILL.md"
        if not source.is_file():
            errors.append(f"Missing entrypoint: {source}")
            continue
        text = source.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        if not match:
            errors.append(f"Invalid frontmatter: {source}")
            continue
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML: {source}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"Frontmatter must be a mapping: {source}")
            continue
        name, description = data.get("name"), data.get("description")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"Invalid skill name: {source}")
        else:
            if name != folder.name:
                errors.append(f"Name/folder mismatch: {source}: {name}")
            if name in seen:
                errors.append(f"Duplicate skill name {name}: {source}, {seen[name]}")
            seen[name] = str(source)
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"Invalid description: {source}")
        if isinstance(description, str) and (description.startswith("[TODO:") or "<" in description or ">" in description):
            errors.append(f"Unfinished/invalid description: {source}")
        documents = sorted(folder.rglob("*.md"))
        for document in documents:
            for line in prose_lines(document.read_text(encoding="utf-8")):
                if re.fullmatch(r"\s*\[TODO:[^\n]*\]\s*", line):
                    errors.append(f"Unfinished instruction: {document}")
                for match_link in LINK.finditer(line):
                    target = match_link.group(1).strip("<>")
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    path = (document.parent / unquote(parsed.path)).resolve()
                    links_checked += 1
                    if not path.exists():
                        errors.append(f"Missing local link: {document}: {target}")
        entries.append({"name": name, "entry_bytes": source.stat().st_size,
                        "markdown_bytes": sum(p.stat().st_size for p in documents)})
    return {"skills": entries, "local_links_checked": links_checked, "errors": errors,
            "scope": "Structural checks only; not a model or scientific verdict"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, default=ROOT / ".agents/skills")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.skills_root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for error in result["errors"]:
            print(f"FAIL {error}")
        print(f"Checked {len(result['skills'])} skills and {result['local_links_checked']} local links; "
              f"{len(result['errors'])} issue(s).")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
