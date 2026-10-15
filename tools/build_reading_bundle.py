#!/usr/bin/env python3
"""Build a local, bounded Markdown reading copy. Source documents remain the research owners."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import zipfile
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from research_paths import ROOT, local_links, link_path, relocated, relocations, link_matches, reference_matches

CORE = {'anchor', 'protocol', 'summary', 'detailed', 'execution_record'}
ASSETS = {'.png', '.jpg', '.jpeg', '.svg', '.csv', '.tsv', '.json', '.pdf'}
MAX_BYTES = 2 * 1024 * 1024


def role(path: Path) -> str:
    stem = path.stem.removesuffix('_cn')
    return 'anchor' if stem.endswith('_anchor') else stem


def companion(path: Path) -> Path:
    return path.with_name(path.stem.removesuffix('_cn') + ('' if path.stem.endswith('_cn') else '_cn') + path.suffix)


def repo_version(repo: Path) -> dict:
    def git(*args):
        try:
            result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
        except OSError:
            return None
        return result.stdout.strip() if result.returncode == 0 else None
    status = git('status', '--porcelain')
    return {'path': str(repo), 'head': git('rev-parse', 'HEAD'),
            'working_tree_dirty': None if status is None else bool(status)}


def permitted(path: Path, root: Path) -> bool:
    # Resolving symlinks prevents a local-looking link from copying worker/private data.
    return path.is_relative_to(root) and path.resolve().is_relative_to(root.resolve()) and not any(
        part in {'.git', '.research', 'runs', 'logs', 'checkpoints', '__pycache__'}
        for part in path.relative_to(root).parts)


def source_bytes(path: Path, snapshots: dict[Path, bytes]) -> bytes:
    if path not in snapshots:
        snapshots[path] = path.read_bytes()
    return snapshots[path]


def owner_paths(text: str, source: Path, root: Path):
    """Explicit fields may be System-relative, document-relative or legacy paths."""
    for values in re.findall(r'^(?:anchor|protocol):[ \t]*(.+)$', text, re.M):
        for value in values.split(';'):
            value = value.strip().strip('`\"\'')
            legacy = re.match(r'^(?:\.\./)+(Projects/.*)$', value)
            if legacy:
                value = legacy[1]
            path, _ = link_path(value, source, root)
            if path is not None:
                yield path


def select_documents(root: Path, project: Path, requested: list[str],
                     snapshots: dict[Path, bytes] | None = None) -> list[Path]:
    snapshots = {} if snapshots is None else snapshots
    mapping = relocations(root)
    route = project / 'main/roadmap.md'
    if not route.is_file():
        raise ValueError(f'Project roadmap unavailable: {route}')
    if requested:
        seeds = [relocated(Path(os.path.abspath(root / value)), mapping, root) for value in requested]
    else:
        focus = next((path for match, path, _ in local_links(source_bytes(route, snapshots).decode(), route, root)
                      if re.fullmatch(r'\[current focus\]\(\s*', match['prefix'], re.I)), None)
        if focus is None:
            raise ValueError('No Current Focus link; provide --source for the intended record.')
        seeds = [relocated(focus, mapping, root)]
    selected = {route}
    for seed in seeds:
        if not seed.is_file() or not permitted(seed, root) or seed.suffix != '.md':
            raise ValueError(f'Unavailable or unsupported source: {seed}')
        selected.add(seed)
        if requested:
            continue  # Explicit selection is bounded; links cannot widen it silently.
        text = source_bytes(seed, snapshots).decode()
        owners = [relocated(path, mapping, root) for path in owner_paths(text, seed, root)]
        protocol_parents = {p.parent for p in owners if role(p) == 'protocol'}
        for _, path, _ in local_links(text, seed, root):
            path = relocated(path, mapping, root)
            # problem_key is an identity, not a filesystem naming convention.
            # Explicit protocols bound the experiment families; otherwise direct
            # result links are the only available owners. Never recurse into history.
            if role(path) in CORE and (not protocol_parents or path.parent in protocol_parents or path in owners):
                owners.append(path)
        for owner in owners:
            if not owner.is_file() or not permitted(owner, root) or owner.suffix != '.md':
                continue  # Build records missing/unselected owner fields in its inventory.
            selected.add(owner)
            if role(owner) in CORE:
                selected.update(p for p in owner.parent.glob('*.md') if p.stem.removesuffix('_cn') in CORE)
    selected |= {companion(p) for p in list(selected) if companion(p).is_file()}
    if len(selected) > 64:
        raise ValueError('Selection exceeds 64 documents; choose a narrower --source.')
    for path in selected:
        if not permitted(path, root) or path.stat().st_size > MAX_BYTES:
            raise ValueError(f'Unsafe or oversized document: {path}')
        source_bytes(path, snapshots)
    order = {'summary': 1, 'anchor': 2, 'protocol': 3, 'detailed': 4, 'execution_record': 5, 'roadmap': 6}
    primary = {p for seed in seeds for p in (seed, companion(seed))} if requested else selected
    return sorted(selected, key=lambda p: (p not in primary, 0 if p.name.startswith('focus_') else order.get(role(p), 7),
                                          not p.stem.endswith('_cn'), str(p)))


def reading_copy(text: str, resolve_link) -> str:
    """Change only link destinations; keep prose, code and formula bodies intact."""
    edits = []
    for match in [*link_matches(text), *reference_matches(text)]:
        target = match['target'].strip('<>')
        resolved = resolve_link(target)
        # Images from the web remain clickable sources, not automatic downloads.
        if match['prefix'].startswith('![') and re.match(r'^(?:https?:)?//', target):
            edits.append((match.begin, match.begin + 1, ''))
        if resolved != target:
            edits.append((match.destination_start, match.destination_end, resolved))
    for begin, end, replacement in sorted(edits, reverse=True):
        text = text[:begin] + replacement + text[end:]
    return text


def build(root: Path, project_name: str, output: Path, requested: list[str], make_zip: bool = False) -> dict:
    root = root.resolve()
    project = root / 'Projects' / project_name
    if Path(project_name).name != project_name or project_name in {'.', '..'} or not project.resolve().is_relative_to(root / 'Projects'):
        raise ValueError('Project must name one child of Projects/.')
    output = output.resolve()
    archive_path = Path(str(output) + '.zip')
    if output.exists() or (make_zip and archive_path.exists()):
        raise ValueError(f'Output already exists; use a new directory: {output}')
    snapshots = {}
    docs = select_documents(root, project, requested, snapshots)
    if any(p.is_relative_to(output) or output.is_relative_to(p.parent) for p in docs):
        raise ValueError('Place generated output outside source folders, e.g. /tmp/research-reading.')
    mapping = relocations(root)
    contents = {path: snapshots[path].decode() for path in docs}
    selected, omissions, assets = set(docs), [], set()
    seen_omissions = set()

    def omit(source, target, reason, kind='link'):
        key = (source, str(target), reason, kind)
        if key not in seen_omissions:
            seen_omissions.add(key)
            omissions.append({'source': source.relative_to(root).as_posix(), 'target': str(target),
                              'reason': reason, 'kind': kind})

    def reason_for(target):
        if not permitted(target, root):
            return 'outside allowed source workspace'
        if not target.is_file():
            return 'source unavailable'
        if target in selected:
            return None
        if target.suffix.lower() in ASSETS and target.stat().st_size <= MAX_BYTES:
            assets.add(target)
            source_bytes(target, snapshots)
            return None
        return 'outside selected documents or asset/size limit'

    copies = {p: output / 'documents' / p.relative_to(root) for p in docs}

    def resolver(source, url):
        target, fragment = link_path(url, source, root)
        if target is None:
            return url  # External links and local heading fragments keep their meaning.
        target = relocated(target, mapping, root)
        reason = reason_for(target)
        if reason:
            omit(source, target, reason)
            dest, fragment = output / 'UNAVAILABLE.md', ''
        else:
            dest = copies[target] if target in selected else output / 'sources' / target.relative_to(root)
            # Editor line suffixes are not portable Markdown filename syntax.
            fragment = re.sub(r'^:\d+(?::\d+)?', '', fragment)
        relative = os.path.relpath(dest, copies[source].parent).replace(os.sep, '/')
        return quote(relative, safe='/') + fragment

    transformed = {}
    for path in docs:
        original = contents[path]
        for owner in owner_paths(original, path, root):
            owner = relocated(owner, mapping, root)
            reason = reason_for(owner)
            if reason:
                omit(path, owner, reason, 'owner field')
        transformed[path] = reading_copy(original, lambda url, source=path: resolver(source, url))

    files = []
    output.mkdir(parents=True)
    for path in sorted(selected | assets):
        relative = path.relative_to(root).as_posix()
        dest = output / 'sources' / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = snapshots[path]
        dest.write_bytes(data)
        row = {'path': relative, 'copy': 'sources/' + relative,
               'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
               'role': 'document' if path in selected else 'referenced asset'}
        if path in selected:
            reading = copies[path]
            reading.parent.mkdir(parents=True, exist_ok=True)
            exact = quote(os.path.relpath(dest, reading.parent).replace(os.sep, '/'), safe='/')
            prefix = f'派生阅读副本；原件位置：`{relative}`。\n[精确原始文件]({exact})；研究修改仍回到原件。\n\n---\n\n'
            reading.write_text(prefix + transformed[path])
            row['reading_copy'] = reading.relative_to(output).as_posix()
            row['reading_sha256'] = hashlib.sha256(reading.read_bytes()).hexdigest()
        files.append(row)
    source_repos = {root, project}
    for path in selected | assets:
        if path.is_relative_to(root / 'Projects'):
            source_repos.add(root / 'Projects' / path.relative_to(root / 'Projects').parts[0])
    manifest = {'generated_at': datetime.now(timezone.utc).isoformat(), 'project': project_name,
                'scope': 'Explicit sources and language companions; project route included' if requested else 'Default Focus and its direct owner records',
                'authority': 'Derived reading copy; source states and researcher decisions are unchanged.',
                'source_versions': [repo_version(repo) for repo in sorted(source_repos)],
                'format': 'Markdown; Python standard library only',
                'files': files, 'omitted_links': omissions,
                'limitations': [
                    'No recursive history or raw worker data is copied.',
                    'Owner fields, inline links and single-line reference definitions are inventoried. Other literal code paths remain source text.',
                    'Heading fragments are retained; support depends on the reader. Search headings or open the listed file path if needed.',
                    'Exact originals in sources/ retain original links. Use documents/ for rebased portable links.',
                    'Formulas retain original TeX. The bundle does not rewrite explanations or prove scientific correctness.',
                    'Inline remote images become source links. Reference-style remote images and raw HTML remain original source syntax; no browser is required.'
                ]}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    unavailable = ['# 未包含的来源\n',
                   '此表区分未选入、无法取得或超出工作区/资产范围的引用；不代表这些来源都已失效。\n']
    for row in omissions:
        unavailable.append(f"- 来源：`{row['source']}`；目标：`{row['target']}`；原因：{row['reason']}。\n")
    if not omissions:
        unavailable.append('所检查范围没有未包含的来源。\n')
    (output / 'UNAVAILABLE.md').write_text('\n'.join(unavailable))
    index = ['# 研究阅读包\n', '指定来源\n' if requested else '默认研究路线\n',
             '直接用文本编辑器或 Markdown 阅读器打开文件，无需网页、浏览器服务或额外 Python 依赖。原有 Unknown、草稿和判断边界保持原样。\n',
             '按下列顺序阅读；链接无法打开时，使用旁边的包内路径。章节跳转不可用时按标题搜索。\n']
    for i, path in enumerate(docs, 1):
        title = next((line[2:].strip() for line in contents[path].splitlines() if line.startswith('# ')), path.name)
        title = title.replace('[', r'\[').replace(']', r'\]')
        rel = copies[path].relative_to(output).as_posix()
        index.append(f'{i}. [{title}]({quote(rel, safe="/")}) — `{rel}`\n')
    index += ['\n## 来源与范围\n',
              f'包含 {len(docs)} 份文档及 {len(assets)} 个引用资产；{len(omissions)} 条未包含引用见 [UNAVAILABLE.md](UNAVAILABLE.md)。\n',
              '原始字节副本在 `sources/`；可移植阅读副本在 `documents/`，只调整链接并添加来源说明。版本与两类文件哈希见 [manifest.json](manifest.json)。\n',
              '正文说明、结果和限制以所选原件为准；此工具不补写缺失解释，不确认科学判断。编辑研究请回到拥有该文件的仓库。\n']
    (output / 'README.md').write_text('\n'.join(index))
    if make_zip:
        with zipfile.ZipFile(archive_path, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(output.rglob('*')):
                if path.is_file():
                    archive.write(path, path.relative_to(output.parent))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='from-attention-to-search')
    parser.add_argument('--source', action='append', default=[], help='Exact System-relative or absolute Markdown source plus its language companion; repeat for more')
    parser.add_argument('--output', type=Path, required=True, help='New directory, e.g. /tmp/research-reading')
    parser.add_argument('--zip', action='store_true', help='Also create a portable ZIP beside the directory')
    args = parser.parse_args()
    try:
        result = build(ROOT, args.project, args.output, args.source, args.zip)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Reading bundle not built: {exc}\n')
    print(f"Built {len(result['files'])} source files; {len(result['omitted_links'])} omitted links. Open {args.output / 'README.md'}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
