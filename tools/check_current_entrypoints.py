#!/usr/bin/env python3
"""Check System -> project -> research entrypoints, without assigning scientific state."""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
from research_paths import ROOT, local_links


def tracked_paths(repo: Path) -> set[Path]:
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=repo, capture_output=True, check=True)
    return {repo / raw.decode() for raw in result.stdout.split(b'\0') if raw}


def current_entrypoints(text: str) -> list[str]:
    """Read explicit Markdown paths; code examples are not implicit entrypoints."""
    from research_paths import link_matches
    return [m['target'].strip('<>') for m in link_matches(text)]


def inspect(root: Path = ROOT, working_tree: bool = False) -> tuple[list[str], list[str], int]:
    catalog = root / 'PROJECTS.md'
    if not catalog.is_file():
        return ['MISSING PROJECTS.md'], [], 0
    sources, projects = [catalog], set()
    for _, path, _ in local_links(catalog.read_text(), catalog, root):
        for base in ('Projects', 'research'):
            if path.is_relative_to(root / base):
                projects.add(root / base / path.relative_to(root / base).parts[0])
        if path.is_relative_to(root / 'Projects') or path.is_relative_to(root / 'research'):
            if path.name in {'roadmap.md', 'roadmap_cn.md'} and path.is_file():
                sources.append(path)
                companion = path.with_name('roadmap.md' if path.name.endswith('_cn.md') else 'roadmap_cn.md')
                if companion.is_file() and companion not in sources:
                    sources.append(companion)
    sources = list(dict.fromkeys(sources))
    failures, pending, checked, tracked = [], [], set(), set()
    for repo in [root, *sorted(p for p in projects if (p / '.git').exists())]:
        try:
            tracked |= tracked_paths(repo)
        except (OSError, subprocess.CalledProcessError):
            failures.append(f'TRACKING_UNAVAILABLE {repo}: Git metadata could not be read')
    for source in sources:
        for _, path, _ in local_links(source.read_text(), source, root):
            if path in checked:
                continue
            checked.add(path)
            try:
                name = path.relative_to(root).as_posix()
            except ValueError:
                failures.append(f'OUTSIDE_WORKSPACE {path}')
                continue
            if not path.exists():
                failures.append(f'MISSING {name}')
            elif path.is_file() and path not in tracked:
                (pending if working_tree else failures).append(f'UNTRACKED {name}')
            if name.startswith('daily_research_reports/') and path.name.startswith('focus_'):
                failures.append(f'DAILY_FOCUS {name}: current questions belong to the project')
    if len(sources) == 1:
        failures.append('NO_PROJECT_ROUTE: no available project roadmap was loaded')
    # Projects opt into the explicit ownership contract in their own AGENTS.
    # Once adopted, deleting the registry must fail rather than disable checking.
    from check_anchor_organization import inspect as inspect_organization
    for project in sorted(projects):
        rules = project / 'AGENTS.md'
        if rules.is_file() and 'anchor_ownership.json' in rules.read_text():
            organization_issues, _ = inspect_organization(project)
            failures.extend(f'ORGANIZATION {project.name}: {issue}' for issue in organization_issues)
    return failures, pending, len(checked)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--working-tree', action='store_true', help='Accept present new files and report their tracking state')
    args = parser.parse_args()
    failures, pending, count = inspect(working_tree=args.working_tree)
    for item in failures:
        print(item)
    if pending:
        print(f'Pending tracking: {len(pending)} present entrypoints (not committed/tracked evidence).')
    print(f'Checked {count} System/project entrypoints; {len(failures)} issue(s).')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
