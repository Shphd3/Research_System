#!/usr/bin/env python3
"""Install thin local skill routes; dry-run unless --apply is supplied.

No authentication, model settings or invocation policy are changed. Existing
directories are moved intact to an explicit backup outside discovery locations.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def route_text(source: Path) -> str:
    text = source.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f'Invalid skill frontmatter: {source}')
    return ('---' + parts[1] + '---\n\n# Canonical Research_System route\n\n'
            f'Read [{source.parent.name}]({source.as_posix()}) before acting.\n'
            'That file and its applicable references own this skill; this entry\n'
            'contains no independent workflow or scientific/run authorization.\n'
            'Resolve relative references from the canonical source directory.\n'
            'If the source is unavailable, report that boundary; do not fall back\n'
            'to an archived skill or infer missing scientific choices.\n')


def install(source_root: Path, destination: Path, backup: Path, apply=False):
    source_root, destination, backup = (p.resolve() for p in (source_root, destination, backup))
    if destination == source_root or destination.is_relative_to(source_root):
        raise ValueError('Destination must be outside the canonical skills tree')
    if backup == destination or backup.is_relative_to(destination):
        raise ValueError('Backup must be outside the discovery destination')
    sources = sorted(source_root.glob('*/SKILL.md'))
    if not sources:
        raise ValueError(f'No canonical skills: {source_root}')
    # Validate every input and replacement before changing any directory.
    plan = []
    for source in sources:
        target = destination / source.parent.name
        body = route_text(source)
        if target.is_symlink():
            raise ValueError(f'Review existing symlink before replacement: {target}')
        current = target / 'SKILL.md'
        if current.is_file() and current.read_text(encoding='utf-8') == body:
            plan.append((source, target, body, 'unchanged'))
            continue
        saved = backup / target.name
        if saved.exists():
            raise ValueError(f'Backup already exists: {saved}')
        plan.append((source, target, body, 'replace' if target.exists() else 'create'))
    for source, target, body, action in plan:
        print(f'{action}: {target.name}')
        if not apply or action == 'unchanged':
            continue
        destination.mkdir(parents=True, exist_ok=True)
        if target.exists():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(backup / target.name))
        target.mkdir()
        (target / 'SKILL.md').write_text(body, encoding='utf-8', newline='\n')
    return [(target.name, action) for _, target, _, action in plan]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skills-root', type=Path, default=ROOT / '.agents/skills')
    p.add_argument('--destination', type=Path, default=Path.home() / '.codex/skills')
    p.add_argument('--backup', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()
    install(a.skills_root, a.destination, a.backup, a.apply)


if __name__ == '__main__':
    main()
