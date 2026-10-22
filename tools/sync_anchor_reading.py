#!/usr/bin/env python3
"""Refresh one explicitly profiled, derived Anchor reading copy; never publish Git."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath

from build_reading_bundle import ROOT, build

STATE = '.anchor_sync.json'
PAYLOAD_DIRS = {'raw', 'rawdata', 'raw_data', 'execution', 'runs', 'logs', 'checkpoints', '__pycache__'}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_at(directory: Path) -> dict[str, str]:
    return {p.relative_to(directory).as_posix(): digest(p)
            for p in sorted(directory.rglob('*')) if p.is_file() and p != directory / STATE}


def stable_content(directory: Path) -> str:
    manifest = json.loads((directory / 'manifest.json').read_text())
    for key in ('generated_at', 'source_versions'):
        manifest.pop(key, None)
    content = {'files': {k: v for k, v in files_at(directory).items() if k != 'manifest.json'},
               'manifest': manifest}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()


def component(value: str) -> str:
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', value):
        raise ValueError(f'Unsafe project or Anchor identity: {value!r}')
    return value


def relative_file(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or '\\' in value:
        raise ValueError(f'Unsafe relative path: {value!r}')
    return path.as_posix()


def target_at(root: Path, project: str, anchor: str) -> Path:
    target = root / 'sync' / 'anchors' / component(project) / component(anchor)
    for path in (root / 'sync', root / 'sync/anchors', target.parent, target):
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f'Target must use real directories: {path}')
    if target.exists() and any(p.is_symlink() for p in target.rglob('*')):
        raise ValueError(f'Symlinks are not allowed in the generated target: {target}')
    return target


def profile(root: Path, project: str, anchor: str) -> list[str]:
    config = root / 'sync/anchors/profiles.json'
    if config.is_symlink():
        raise ValueError('The profile configuration must not be a symlink.')
    data = json.loads(config.read_text())
    if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('entries'), list):
        raise ValueError('Expected profiles schema_version 1 and an entries list.')
    entries = [e for e in data['entries'] if isinstance(e, dict)
               and e.get('project') == project and e.get('anchor_id') == anchor]
    if len(entries) != 1:
        raise ValueError('Exactly one matching project/Anchor profile is required.')
    sources = entries[0].get('sources')
    if not isinstance(sources, list) or not sources or not all(isinstance(s, str) for s in sources):
        raise ValueError('The profile must explicitly list Markdown sources.')
    sources = sorted({relative_file(s) for s in sources})
    if any(Path(s).suffix != '.md' or PAYLOAD_DIRS.intersection(Path(s).parts) for s in sources):
        raise ValueError('Only explicit Markdown sources are accepted; payloads stay execution-side.')
    return sources


def verify_existing(target: Path, owner: dict) -> dict | None:
    if not target.exists():
        return None
    state_path = target / STATE
    if not state_path.is_file():
        raise ValueError('Existing target has no sync ownership manifest; refusing overwrite.')
    state = json.loads(state_path.read_text())
    if not isinstance(state, dict) or state.get('schema_version') != 1 or state.get('owner') != owner:
        raise ValueError('Existing target belongs to a different or unknown generated owner.')
    owned = state.get('files')
    if not isinstance(owned, dict) or not owned:
        raise ValueError('Invalid owned-file inventory.')
    for rel, expected in owned.items():
        path = target / relative_file(rel)
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f'Generated file was edited or removed; refusing overwrite: {rel}')
    return state


def sync(root: Path, project: str, anchor: str, check: bool = False) -> Path:
    root = root.resolve()
    target = target_at(root, project, anchor)
    sources = profile(root, project, anchor)
    owner = {'project': project, 'anchor_id': anchor}
    old = verify_existing(target, owner)
    if check and old is None:
        raise ValueError('No generated reading copy exists to check.')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.anchor-reading-', dir=target.parent) as temporary:
        stage = Path(temporary) / 'bundle'
        manifest = build(root, project, stage, sources)
        if any(PAYLOAD_DIRS.intersection(Path(row['path']).parts) for row in manifest['files']):
            raise ValueError('Payload directories cannot be copied into an Anchor reading package.')
        current = stable_content(stage)
        target_at(root, project, anchor)
        # Recheck after building so concurrent manual edits are never overwritten.
        existing = verify_existing(target, owner)
        if (old is None) != (existing is None) or old != existing:
            raise ValueError('Target ownership changed during the build; retry after review.')
        if check:
            if old.get('sources') != sources or old.get('content_sha256') != current:
                raise ValueError('Reading copy is stale: source content or selection changed.')
            return target
        fresh = files_at(stage)
        old_owned = set(existing['files']) if existing else set()
        if existing:
            for path in sorted(target.rglob('*')):
                rel = path.relative_to(target).as_posix()
                if rel == STATE or rel in old_owned:
                    continue
                dest = stage / rel
                if path.is_dir():
                    dest.mkdir(parents=True, exist_ok=True)
                else:
                    if dest.exists():
                        raise ValueError(f'New generated file would overwrite an unrelated file: {rel}')
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, dest)
        state = {'schema_version': 1, 'owner': owner, 'sources': sources,
                 'files': fresh, 'content_sha256': current}
        (stage / STATE).write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        previous = Path(temporary) / 'previous'
        if target.exists():
            target.rename(previous)
        try:
            stage.rename(target)
        except OSError:
            if previous.exists():
                previous.rename(target)
            raise
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--anchor', required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        target = sync(ROOT, args.project, args.anchor, args.check)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Anchor reading sync refused: {exc}\n')
    print(('Current: ' if args.check else 'Synced: ') + str(target))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
