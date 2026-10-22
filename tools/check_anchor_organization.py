#!/usr/bin/env python3
"""Check registered project ownership and placement, without judging research state.

The project registry is ``main/anchor_ownership.json``. Paths in that registry
are relative to the project root. Historical snapshots are outside the current
owner scan; a topic-key directory is not an exemption for a live Anchor.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = ROOT / "Projects/from-attention-to-search"
HISTORY_PARTS = {"archive", "archives", "backup", "snapshots", ".git", ".local"}
LINE_ID = re.compile(r"A\d{2,}\Z")
ANCHOR_ID = re.compile(r"\d{2,}(?:_\d{2,})*\Z")
FORMAL_RECORD = re.compile(r"(?:protocol(?:[_-].*)?|summary|detailed|execution_record)(?:_cn)?\.md\Z", re.I)


def historical(path: Path, base: Path) -> bool:
    return bool(set(path.relative_to(base).parts) & HISTORY_PARTS)


def is_anchor(path: Path) -> bool:
    """Find named designs and historical numbered designs with explicit identity."""
    if re.fullmatch(r"(?:.*_)?anchor(?:_cn)?\.md", path.name, re.I):
        return True
    # Legacy files such as 07.md carry an identity in their front matter.
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        front = text.split("\n---", 1)[0]
        return bool(re.search(r"^anchor_id\s*:", front, re.M))
    return False


def inspect(project_root: Path = DEFAULT_PROJECT) -> tuple[list[str], dict[str, int]]:
    project = project_root.resolve()
    registry = project / "main/anchor_ownership.json"
    issues: list[str] = []
    counts = {"lines": 0, "anchors": 0, "anchor_files": 0, "experiment_records": 0}
    if not registry.is_file():
        return [f"MISSING_REGISTRY {registry}"], counts
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"INVALID_REGISTRY {registry}: {exc}"], counts
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return [f"INVALID_SCHEMA {registry}: expected schema_version 1"], counts

    def rows(name: str) -> list[dict]:
        value = data.get(name, [])
        if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
            issues.append(f"INVALID_SCHEMA {name}: expected a list of objects")
            return []
        return value

    def location(value: object, label: str, kind: str | None = None) -> Path | None:
        if not isinstance(value, str) or not value:
            issues.append(f"INVALID_PATH {label}: expected a project-relative path")
            return None
        raw = Path(value)
        path = (project / raw).resolve()
        if raw.is_absolute() or ".." in raw.parts or not path.is_relative_to(project):
            issues.append(f"OUTSIDE_PROJECT {label}: {value}")
            return None
        if kind == "file" and not path.is_file():
            issues.append(f"MISSING_FILE {label}: {value}")
        elif kind == "directory" and not path.is_dir():
            issues.append(f"MISSING_DIRECTORY {label}: {value}")
        elif kind is None and not path.exists():
            issues.append(f"MISSING_PATH {label}: {value}")
        return path

    def inside(path: Path, base: Path | None) -> bool:
        return base is not None and path.is_relative_to(base)

    line_rows = rows("lines")
    anchor_rows = rows("anchors")
    support_rows = rows("support_records")
    legacy_rows = rows("legacy_experiments")
    counts.update(lines=len(line_rows), anchors=len(anchor_rows))
    lines: dict[str, dict] = {}
    for row in line_rows:
        line = row.get("id")
        if not isinstance(line, str) or not LINE_ID.fullmatch(line):
            issues.append(f"INVALID_LINE_ID {line!r}")
            continue
        if line in lines:
            issues.append(f"DUPLICATE_LINE_ID {line}")
            continue
        layout = row.get("layout")
        if layout not in {"parent_subanchor", "registered_flat"}:
            issues.append(f"INVALID_LAYOUT {line}: {layout!r}")
        anchor_root = location(row.get("anchor_root"), f"{line}.anchor_root", "directory")
        experiment_root = location(row.get("experiment_root"), f"{line}.experiment_root", "directory")
        if anchor_root and not inside(anchor_root, project / "main/problem_anchors"):
            issues.append(f"MISPLACED_LINE {line}: anchor_root must be under main/problem_anchors")
        if experiment_root and (
            experiment_root.parent != project / "main/experiments"
            or not re.fullmatch(re.escape(line) + r"(?:_.+)?", experiment_root.name)
        ):
            issues.append(f"UNNUMBERED_EXPERIMENT_LINE {line}: {row.get('experiment_root')}")
        if row.get("index") is not None:
            location(row["index"], f"{line}.index", "file")
        lines[line] = {**row, "anchor_root_path": anchor_root, "experiment_root_path": experiment_root}

    for identifier, number in Counter(row.get("id") for row in anchor_rows).items():
        if number > 1:
            issues.append(f"DUPLICATE_ANCHOR_ID {identifier}: {number} owners")
    anchors: dict[str, dict] = {}
    registered_files: dict[Path, str] = {}
    experiment_owners: dict[Path, str] = {}
    for row in anchor_rows:
        identifier, line = row.get("id"), row.get("line")
        if not isinstance(identifier, str) or not ANCHOR_ID.fullmatch(identifier):
            issues.append(f"INVALID_ANCHOR_ID {identifier!r}")
            continue
        if line not in lines:
            issues.append(f"UNKNOWN_LINE {identifier}: {line!r}")
            continue
        if identifier.split("_")[0] != line[1:]:
            issues.append(f"WRONG_LINE_ID {identifier}: registered under {line}")
        owner = lines[line]
        path = location(row.get("path"), f"{identifier}.path", "file")
        companions = row.get("companions", [])
        experiment_roots = row.get("experiment_roots", [])
        if not isinstance(companions, list) or not isinstance(experiment_roots, list):
            issues.append(f"INVALID_SCHEMA {identifier}: companions and experiment_roots must be lists")
            continue
        paths = [path, *(location(value, f"{identifier}.companion", "file") for value in companions)]
        for candidate in paths:
            if candidate is None:
                continue
            if not inside(candidate, owner["anchor_root_path"]):
                issues.append(f"MISPLACED_ANCHOR {identifier}: {candidate.relative_to(project)}")
            if historical(candidate, project):
                issues.append(f"HISTORICAL_CANONICAL_OWNER {identifier}: {candidate.relative_to(project)}")
            if candidate in registered_files:
                issues.append(f"DUPLICATE_ANCHOR_PATH {candidate.relative_to(project)}: {registered_files[candidate]}, {identifier}")
            registered_files[candidate] = identifier
        for value in experiment_roots:
            exp = location(value, f"{identifier}.experiment_root", "directory")
            if exp is None:
                continue
            if not inside(exp, owner["experiment_root_path"]) or exp == owner["experiment_root_path"]:
                issues.append(f"MISPLACED_EXPERIMENT {identifier}: {value}")
            if exp in experiment_owners and experiment_owners[exp] != identifier:
                issues.append(f"DUPLICATE_EXPERIMENT_OWNER {value}: {experiment_owners[exp]}, {identifier}")
            experiment_owners[exp] = identifier
        anchors[identifier] = {**row, "path_object": path}

    for identifier, row in anchors.items():
        parent_id = row.get("parent_id")
        parent = anchors.get(parent_id) if isinstance(parent_id, str) else None
        if parent_id is not None and (
            parent is None or parent_id == identifier or parent.get("line") != row["line"]
            or not identifier.startswith(parent_id + "_")
        ):
            issues.append(f"INVALID_PARENT {identifier}: {parent_id!r}")
        line, path = lines[row["line"]], row["path_object"]
        if path is None or line.get("layout") != "parent_subanchor":
            continue
        if not path.name.startswith(identifier + "_"):
            issues.append(f"UNNUMBERED_ANCHOR_FILE {identifier}: {path.relative_to(project)}")
        if parent_id is None:
            if (path.parent.parent != line["anchor_root_path"]
                    or not path.parent.name.startswith(identifier + "_")):
                issues.append(f"MISPLACED_PARENT {identifier}: {path.relative_to(project)}")
        elif parent and parent["path_object"]:
            expected = parent["path_object"].parent / "subanchors"
            if path.parent != expected:
                issues.append(f"MISPLACED_CHILD {identifier}: expected {expected.relative_to(project)}")

    for row in support_rows:
        location(row.get("path"), "support_record")
        if not row.get("reason"):
            issues.append(f"MISSING_SUPPORT_REASON {row.get('path')}")
    legacy: list[Path] = []
    for row in legacy_rows:
        path = location(row.get("path"), "legacy_experiment")
        owner_ids = row.get("owner_ids", [])
        if not isinstance(owner_ids, list) or not owner_ids or any(owner not in anchors for owner in owner_ids):
            issues.append(f"INVALID_LEGACY_OWNER {row.get('path')}: {owner_ids!r}")
        if not row.get("reason"):
            issues.append(f"MISSING_LEGACY_REASON {row.get('path')}")
        if path:
            if not inside(path, project / "main/experiments"):
                issues.append(f"MISPLACED_LEGACY_EXPERIMENT {row.get('path')}")
            legacy.append(path)

    anchor_tree = project / "main/problem_anchors"
    if anchor_tree.is_dir():
        for path in sorted(anchor_tree.rglob("*.md")):
            if historical(path, anchor_tree):
                continue
            try:
                formal = is_anchor(path)
            except (OSError, UnicodeError) as exc:
                issues.append(f"UNREADABLE_ANCHOR {path.relative_to(project)}: {exc}")
                continue
            if formal:
                counts["anchor_files"] += 1
                if path.resolve() not in registered_files:
                    issues.append(f"ORPHAN_ANCHOR {path.relative_to(project)}: no numbered registry owner")
    experiment_tree = project / "main/experiments"
    if experiment_tree.is_dir():
        for path in sorted(experiment_tree.rglob("*.md")):
            if historical(path, experiment_tree) or not FORMAL_RECORD.fullmatch(path.name):
                continue
            counts["experiment_records"] += 1
            matches = [(base, owner) for base, owner in experiment_owners.items() if path.is_relative_to(base)]
            if not matches and not any(path == base or path.is_relative_to(base) for base in legacy):
                issues.append(f"ORPHAN_EXPERIMENT {path.relative_to(project)}: no registered Anchor owner")
            # Nested roots can refine the same owner; different owners cannot overlap.
            if len({owner for _, owner in matches}) > 1:
                issues.append(f"AMBIGUOUS_EXPERIMENT {path.relative_to(project)}: {sorted({owner for _, owner in matches})}")
    map_path = project / "main/research_map.json"
    if map_path.is_file():
        issues.extend(inspect_reading_map(project, map_path, data))
    return sorted(set(issues)), counts


def inspect_reading_map(project: Path, path: Path, registry: dict) -> list[str]:
    """Keep the derived reading view aligned without evaluating its claims."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("anchors"), list):
            return ["INVALID_READING_MAP expected an anchors list"]
        rows = data["anchors"]
        if any(not isinstance(row, dict) for row in rows):
            return ["INVALID_READING_MAP expected Anchor objects"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"INVALID_READING_MAP {exc}"]
    issues: list[str] = []
    owners = {row["id"]: row for row in registry["anchors"] if isinstance(row.get("id"), str)}
    identifiers = [row.get("id") for row in rows]
    if any(not isinstance(identifier, str) for identifier in identifiers):
        return ["INVALID_READING_MAP expected string Anchor IDs"]
    for identifier, n in Counter(identifiers).items():
        if n > 1:
            issues.append(f"DUPLICATE_MAP_ANCHOR {identifier}")
    for identifier in sorted(set(owners) - set(identifiers)):
        issues.append(f"MISSING_MAP_ANCHOR {identifier}")
    for row in rows:
        identifier = row["id"]
        owner = owners.get(identifier)
        if owner is None:
            issues.append(f"UNKNOWN_MAP_ANCHOR {identifier}")
            continue
        if row.get("line") != owner.get("line") or row.get("parent_id") != owner.get("parent_id"):
            issues.append(f"WRONG_MAP_OWNER {identifier}")
        if row.get("source") != owner.get("path"):
            issues.append(f"WRONG_MAP_SOURCE {identifier}")
            continue
        source = project / owner["path"]
        if source.is_file() and row.get("source_sha256") != hashlib.sha256(source.read_bytes()).hexdigest():
            issues.append(f"STALE_MAP_SOURCE {identifier}: refresh the derived explanation against its Anchor")
        for field in ("title_cn", "question_cn", "why_cn", "approach_cn", "role_for_parent_cn", "evidence_state_cn", "boundary_cn"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                issues.append(f"EMPTY_MAP_EXPLANATION {identifier}.{field}")
        for field in ("evidence_sources", "related_results"):
            references = row.get(field, [])
            if not isinstance(references, list):
                issues.append(f"INVALID_MAP_REFERENCES {identifier}.{field}")
                continue
            for reference in references:
                if not isinstance(reference, str):
                    issues.append(f"INVALID_MAP_REFERENCE {identifier}.{field}")
                    continue
                target = (project / reference).resolve()
                if not target.is_relative_to(project) or not target.is_file():
                    issues.append(f"MISSING_MAP_REFERENCE {identifier}: {reference}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT,
                        help="Project repository root (default: from-attention-to-search)")
    args = parser.parse_args()
    issues, counts = inspect(args.project_root)
    for issue in issues:
        print(issue)
    print(f"Checked {counts['lines']} lines, {counts['anchors']} registered Anchors, "
          f"{counts['anchor_files']} current Anchor files and {counts['experiment_records']} "
          f"experiment records; {len(issues)} issue(s). Scientific state was not evaluated.")
    return bool(issues)


if __name__ == "__main__":
    raise SystemExit(main())
