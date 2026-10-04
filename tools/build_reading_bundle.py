#!/usr/bin/env python3
"""Build a local, bounded reading copy. Source documents remain the research owners."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import zipfile
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote

from research_paths import ROOT, local_links, link_path, relocated, relocations

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


def render_markdown(text: str, document_id: str = '', resolve_link=None) -> tuple[str, str]:
    try:
        import mistune
    except ImportError:
        return '<pre>' + html.escape(text) + '</pre>', 'escaped Markdown source'
    math = []
    # Code is left literal. Math tokens are protected from Markdown escape processing.
    pattern = re.compile(r'(^ {0,3}(?:`{3,}|~{3,})[^\n]*\n.*?^ {0,3}(?:`{3,}|~{3,})[^\n]*$|`+[^`\n]*`+)|'
                         r'(\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<!\\)\$[^$\n]+(?<!\\)\$)', re.S | re.M)
    try:
        from latex2mathml.converter import convert
    except ImportError:
        convert = None
    def protect(match):
        if match[1]:
            return match[0]
        token = match[2]
        display = token.startswith((r'\[', '$$'))
        trim = 1 if token.startswith('$') and not display else 2
        body = token[trim:-trim]
        rendered = '<code class="math-source">' + html.escape(token) + '</code>'
        if convert:
            try:
                rendered = convert(body, display='block' if display else 'inline')
            except Exception:
                pass  # Preserve exact TeX on unsupported syntax, never silently drop a formula.
        marker = f'READINGBUNDLEMATH{len(math):06d}TOKEN'
        math.append((marker, rendered, token))
        return marker
    protected = pattern.sub(protect, text)
    class ReaderRenderer(mistune.HTMLRenderer):
        def __init__(self):
            super().__init__(escape=True)
            self.headings = {}

        def heading(self, text, level, **attrs):
            title = text
            for marker, _, token in math:
                title = title.replace(marker, token)
            title = html.unescape(re.sub(r'<[^>]+>', '', title)).lower()
            slug = re.sub(r'[^\w\s-]', '', title)
            slug = re.sub(r'\s', '-', slug)
            count = self.headings.get(slug, 0)
            self.headings[slug] = count + 1
            slug += f'-{count}' if count else ''
            ident = document_id + '--' + slug if document_id else slug
            return f'<h{level} id="{html.escape(ident, quote=True)}">{text}</h{level}>\n'

        def link(self, text, url, title=None):
            if resolve_link:
                url, reason = resolve_link(url)
                if reason:
                    text = '[未包含：' + text + ']'
            return super().link(text, url, title)

        def image(self, text, url, title=None):
            if re.match(r'^(?:https?:)?//', url):
                return '<span class="muted">[远程图片：请查阅原始文件]</span>'
            if resolve_link:
                url, reason = resolve_link(url)
                if reason:
                    return super().link('[未包含图片：' + text + ']', url, title)
            return super().image(text, url, title)

    result = mistune.create_markdown(renderer=ReaderRenderer(), plugins=['table'])(protected)
    # An offline reading copy must not fetch remote images on opening.
    result = re.sub(r'<img\b[^>]*src="(?:https?:)?//[^>]*>',
                    '<span class="muted">[远程图片：请查阅原始文件]</span>', result)
    for marker, rendered, _ in math:
        result = result.replace(marker, rendered)
    return result, 'Markdown + MathML with TeX fallback' if convert else 'Markdown + literal TeX'


CSS = '''
:root{color-scheme:light;--ink:#182d3b;--muted:#546577;--accent:#166861;--line:#dce5e7}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#f5f7f7;font:16px/1.8 system-ui,sans-serif}
a{color:var(--accent);text-underline-offset:3px}header{padding:2rem 5vw;background:#173c42;color:white}
header h1{font-size:1.8rem;margin:0}header p{margin:.5rem 0;max-width:80ch}header a{color:#d4f4e9}
.layout{display:grid;grid-template-columns:290px minmax(0,1fr);gap:2rem;max-width:1500px;margin:auto;padding:2rem}
nav{position:sticky;top:1rem;height:calc(100vh - 2rem);overflow:auto;padding:.5rem}nav a{display:block;padding:.4rem 0;line-height:1.5;font-size:.9rem}
input{width:100%;padding:.7rem;border:1px solid var(--line);border-radius:5px;font:inherit}label{font-weight:600}
main{min-width:0}article,aside{background:white;border:1px solid var(--line);border-radius:8px;margin-bottom:1.4rem;padding:1.5rem 2rem;overflow-wrap:anywhere}
article>details>summary{cursor:pointer;font-size:1.2rem;font-weight:650}article .provenance{font-size:.8rem;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:.7rem}
h1,h2,h3{line-height:1.4}article h1{font-size:1.6rem}article h2{font-size:1.3rem}article h3{font-size:1.1rem}
pre{overflow:auto;white-space:pre-wrap;background:#f3f6f6;padding:1rem;font-size:.84rem}code{font-size:.88em}table{display:block;overflow:auto;border-collapse:collapse;font-size:.9rem}
th,td{padding:.5rem .7rem;border:1px solid var(--line);text-align:left}th{background:#eef4f3}img{max-width:100%;height:auto}
math[display=block]{overflow:auto;padding:1rem 0}details{margin:.7rem 0}summary{cursor:pointer}li{margin:.25rem 0}.muted{color:var(--muted)}[hidden]{display:none!important}
@media(max-width:850px){.layout{display:block;padding:1rem}nav{position:static;height:auto;max-height:18rem;margin-bottom:1rem}article,aside{padding:1rem}header{padding:1.5rem}}
@media print{nav,header input{display:none}.layout{display:block}article{break-inside:auto;border:0;padding:0}body{background:white}}
'''
JS = '''
const query=document.getElementById('search');
query.addEventListener('input',()=>{const q=query.value.toLowerCase();document.querySelectorAll('article').forEach(a=>{a.hidden=!a.textContent.toLowerCase().includes(q);const d=a.querySelector('details');d.open=!!q||d.dataset.initial==='open'});document.querySelectorAll('nav a[data-doc]').forEach(a=>{a.hidden=document.getElementById(a.dataset.doc).hidden})});
function reveal(id){const target=document.getElementById(decodeURIComponent(id));if(!target)return;const a=target.closest('article');if(a){a.hidden=false;const d=a.querySelector('details');if(d)d.open=true;document.querySelectorAll('nav a[data-doc]').forEach(link=>{if(link.dataset.doc===a.id)link.hidden=false})}target.scrollIntoView()}
window.addEventListener('hashchange',()=>reveal(location.hash.slice(1)));
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>reveal(a.getAttribute('href').slice(1))));
if(location.hash)reveal(location.hash.slice(1));
'''


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
    ids = {path: f'doc-{index}' for index, path in enumerate(docs)}
    seen_omissions, fragment_targets = set(), []

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

    def resolver(source, url):
        if url.startswith('#'):
            target, fragment = source, url
        else:
            target, fragment = link_path(url, source, root)
            if target is None:
                return url, None
            target = relocated(target, mapping, root)
        reason = reason_for(target)
        if reason:
            omit(source, target, reason)
            return '#omissions', reason
        section = unquote(fragment.partition('#')[2])
        if target in selected:
            result = '#' + ids[target]
            if section:
                result += '--' + section
                fragment_targets.append((source, target, section, result))
            return result, None
        result = quote('sources/' + target.relative_to(root).as_posix())
        return result + ('#' + quote(section, safe='=/?:-') if section else ''), None

    links, rendered_docs, modes = [], {}, set()
    for path in docs:
        original = contents[path]
        # Metadata paths remain literal source text but their availability is audited.
        for owner in owner_paths(original, path, root):
            owner = relocated(owner, mapping, root)
            reason = reason_for(owner)
            if reason:
                omit(path, owner, reason, 'owner field')
        # Also retain the inline inventory when the optional renderer is absent.
        for match, _, _ in local_links(original, path, root):
            resolver(path, match['target'])
        rendered, mode = render_markdown(original, ids[path], lambda url, source=path: resolver(source, url))
        rendered = re.sub(r'<h1 id="([^"]*)">.*?</h1>\n?', r'<span id="\1"></span>', rendered, count=1, flags=re.S)
        rendered_docs[path] = rendered
        modes.add(mode)

    available_ids = {value for rendered in rendered_docs.values() for value in re.findall(r' id="([^"]+)"', rendered)}
    replacements = {}
    for source, target, section, url in fragment_targets:
        if url[1:] not in available_ids:
            omit(source, str(target) + '#' + section, 'section unavailable; opens document')
            replacements[html.escape(url, quote=True)] = '#' + ids[target]
    articles = []
    for path in docs:
        rendered = rendered_docs[path]
        for old, new in replacements.items():
            rendered = rendered.replace('href="' + old + '"', 'href="' + new + '"')
        original = contents[path]
        title = next((line[2:].strip() for line in original.splitlines() if line.startswith('# ')), path.name)
        label = ('中文伴随稿 · ' if path.stem.endswith('_cn') else '原文 · ') + title
        links.append(f'<a href="#{ids[path]}" data-doc="{ids[path]}">{html.escape(label)}</a>')
        raw = 'sources/' + path.relative_to(root).as_posix()
        open_first = (path.stem.endswith('_cn') or not companion(path).is_file()) and (
            (requested and role(path) != 'roadmap') or path.name.startswith('focus_') or role(path) == 'summary')
        state = 'open' if open_first else 'closed'
        articles.append(f'<article id="{ids[path]}"><details data-initial="{state}" {"open" if open_first else ""}>'
                        f'<summary>{html.escape(label)}</summary><p class="provenance">{html.escape(str(path.relative_to(root)))} · '
                        f'<a href="{quote(raw)}">原始文件</a></p>{rendered}</details></article>')
    # Page, original copies and hashes all use the same bytes captured above.
    files = []
    output.mkdir(parents=True)
    for path in sorted(selected | assets):
        relative = path.relative_to(root).as_posix()
        dest = output / 'sources' / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = snapshots[path]
        dest.write_bytes(data)
        files.append({'path': relative, 'copy': 'sources/' + relative, 'sha256': hashlib.sha256(data).hexdigest(),
                      'bytes': len(data), 'role': 'document' if path in selected else 'referenced asset'})
    source_repos = {root, project}
    for path in selected | assets:
        if path.is_relative_to(root / 'Projects'):
            source_repos.add(root / 'Projects' / path.relative_to(root / 'Projects').parts[0])
    manifest = {'generated_at': datetime.now(timezone.utc).isoformat(), 'project': project_name,
                'scope': 'Explicit sources and language companions; project route included' if requested else 'Default Focus and its direct owner records',
                'authority': 'Derived reading copy; source states and researcher decisions are unchanged.',
                'source_versions': [repo_version(repo) for repo in sorted(source_repos)], 'rendering': sorted(modes),
                'files': files, 'omitted_links': omissions,
                'limitations': ['No recursive history or raw worker data is copied.',
                               'Owner fields and inline links are inventoried; rendered reference-style links are also resolved. Other literal code paths remain source text.',
                               'Section links use document-scoped heading IDs. Unavailable sections open the document and are listed.',
                               'Original Markdown copies preserve exact bytes, including their original absolute links; use index.html for portable navigation.',
                               'Unsupported formulas retain literal TeX; source checks do not prove typesetting correctness.']}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    missing_rows = ''.join('<li><code>' + html.escape(row['source']) + '</code> → <code>' + html.escape(row['target']) + '</code> — ' + html.escape(row['reason']) + '</li>' for row in omissions)
    page = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>研究阅读包 · ' + html.escape(project_name) + '</title><style>' + CSS + '</style>'
            '<header><h1>研究阅读包</h1><p>' + ('指定来源' if requested else '默认研究路线') + '</p>'
            '<p>由原件生成的离线阅读副本。原有 Unknown、草稿和判断边界保持原样。</p>'
            '<a href="manifest.json">来源与范围清单</a></header><div class="layout"><nav><label for="search">搜索本包内容</label>'
            '<input id="search" type="search" placeholder="关键词 / 术语 / 状态"><p class="muted">' + str(len(docs)) + ' 份原文；含语言伴随稿</p>'
            + ''.join(links) + '<a href="#omissions">未包含的链接与阅读限制</a></nav><main>'
            '<aside>' + ('本包按指定来源组织，文档日期和状态以原文为准。' if requested else '先读项目导航和当前 Focus，再按需要查阅具体记录。') +
            '公式不支持时保留 TeX 原文；完整来源路径和版本见清单。'
            '未包含 ' + str(len(omissions)) + ' 条链接；这不是所有历史资料的完整副本。</aside>'
            + ''.join(articles) + '<aside id="omissions"><h2>未包含的链接与阅读限制</h2><p>'
            + html.escape(' '.join(manifest['limitations'])) + '</p><details><summary>展开未包含链接 (' + str(len(omissions)) + ')</summary><ul>'
            + missing_rows + '</ul></details></aside></main></div><script>' + JS + '</script></html>')
    (output / 'index.html').write_text(page)
    (output / 'README.md').write_text('# Research reading bundle\n\nOpen index.html offline. Exact source copies are in sources/.\n'
                                     'Manifest records selection, versions, hashes and omissions. Edit the owning repositories, not this copy.\n')
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
    print(f"Built {len(result['files'])} source files; {len(result['omitted_links'])} omitted links. Open {args.output / 'index.html'}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
