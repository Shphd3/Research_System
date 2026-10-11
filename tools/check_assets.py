#!/usr/bin/env python3
"""Check registered local asset access without loading tensors or downloading data."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import socket
import sys

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = SYSTEM_ROOT / "assets" / "catalog.json"
PAYLOAD_STATUSES = {
    "NOT_VERIFIED", "SOURCE_PRESENT", "SOURCE_FILES_PRESENT", "MODEL_STATE_PRESENT",
    "EMBEDDED_SAE_PRESENT", "ARRAY_FILES_PRESENT", "ADAPTER_STATE_PRESENT",
    "PREPARED_DATA_PRESENT", "METADATA_ONLY", "PAYLOAD_MISSING", "INCOMPLETE",
    "CACHE_DIRECTORY", "PROJECT_ENTRYPOINTS",
}


def check_path(path: Path, expected: str) -> dict:
    """Prove lightweight read/list access; existence alone is insufficient."""
    result = {"path": str(path), "expected": expected}
    try:
        stat = path.stat()  # follows symlinks, including detecting broken targets
        if expected == "file":
            if not path.is_file():
                raise ValueError("expected a regular file")
            with path.open("rb") as stream:
                stream.read(1)
            result.update(status="READABLE_FILE", size_bytes=stat.st_size)
        elif expected == "directory":
            if not path.is_dir():
                raise ValueError("expected a directory")
            if os.access in os.supports_effective_ids:
                traversable = os.access(path, os.X_OK, effective_ids=True)
            elif os.getuid() == os.geteuid():
                traversable = os.access(path, os.X_OK)
            else:
                raise PermissionError("cannot verify traversal for effective UID on this platform")
            if not traversable:
                raise PermissionError("directory is not traversable")
            with os.scandir(path) as entries:
                next(entries, None)
            result.update(status="LISTABLE_DIRECTORY")
        else:
            raise ValueError(f"unsupported path type: {expected}")
        result["ok"] = True
    except FileNotFoundError as error:
        result.update(ok=False, status="NOT_FOUND", error=str(error))
    except PermissionError as error:
        result.update(ok=False, status="PERMISSION_DENIED", error=str(error))
    except (OSError, ValueError) as error:
        result.update(ok=False, status="ACCESS_ERROR", error=str(error))
    return result


def check_location(location: dict) -> dict:
    path = Path(location["path"])
    result = check_path(path, location["expected"])
    result.update(role=location.get("role", "primary"), required=location.get("required", True))
    probes = []
    for probe in location.get("probes", []):
        target = Path(probe["path"])
        if not target.is_absolute():
            target = path / target
        checked = check_path(target, probe.get("expected", "file"))
        checked["required"] = probe.get("required", True)
        probes.append(checked)
    result["probes"] = probes
    result["qualified_access"] = result["ok"] and all(
        probe["ok"] for probe in probes if probe["required"]
    )
    return result


def check_asset(asset: dict) -> dict:
    locations = [check_location(location) for location in asset["locations"]]
    required = [item for item in locations if item["required"]]
    all_required = bool(required) and all(item["qualified_access"] for item in required)
    any_access = any(item["ok"] for item in locations)
    status = "ACCESSIBLE" if all_required else "PARTIAL" if any_access else "UNAVAILABLE"
    payload = asset.get("payload_status", "NOT_VERIFIED")
    metadata_only = payload in {"METADATA_ONLY", "PAYLOAD_MISSING", "INCOMPLETE"}
    return {
        "id": asset["id"], "title_cn": asset["title_cn"], "category": asset["category"],
        "projects": asset.get("projects", []), "access_status": status,
        "payload_status": payload,
        "required_access_passed": all_required,
        "strict_passed": all_required and not metadata_only,
        "loading_or_scientific_eligibility": "NOT_CHECKED",
        "locations": locations,
    }


def load_catalog(path: Path) -> dict:
    catalog = json.loads(path.read_text())
    if catalog.get("schema_version") != 1:
        raise ValueError("unsupported asset catalog schema")
    if not isinstance(catalog.get("assets"), list) or not isinstance(catalog.get("projects"), list):
        raise ValueError("catalog requires projects and assets lists")
    for group in (catalog["projects"], catalog["assets"]):
        ids = [item["id"] for item in group]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate registry identity")
        for item in group:
            if not item.get("locations"):
                raise ValueError(f"{item['id']}: missing locations")
            for location in item["locations"]:
                if not Path(location["path"]).is_absolute():
                    raise ValueError(f"{item['id']}: location must be absolute")
                if location["expected"] not in ("file", "directory"):
                    raise ValueError(f"{item['id']}: invalid location type")
    project_ids = {project["id"] for project in catalog["projects"]}
    for asset in catalog["assets"]:
        if asset.get("payload_status", "NOT_VERIFIED") not in PAYLOAD_STATUSES:
            raise ValueError(f"{asset['id']}: invalid payload_status")
        if not set(asset.get("projects", [])).issubset(project_ids):
            raise ValueError(f"{asset['id']}: unregistered project")
        if not set(asset.get("required_projects", [])).issubset(project_ids):
            raise ValueError(f"{asset['id']}: unregistered required project")
    return catalog


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--asset", action="append", help="Exact asset ID; repeat for dependencies")
    parser.add_argument("--project", action="append", help="Registered project ID")
    parser.add_argument("--category", action="append")
    parser.add_argument("--list", action="store_true", help="List identities without access checks")
    parser.add_argument("--strict", action="store_true", help="Fail if selected required paths/payloads are missing")
    parser.add_argument("--json", action="store_true", help="Print full access report")
    parser.add_argument("--output", type=Path, help="Save a new dated access snapshot; refuse overwrite")
    args = parser.parse_args(argv)
    try:
        if args.list and (args.strict or args.output):
            raise ValueError("--list does not check access; do not combine it with --strict or --output")
        catalog = load_catalog(args.catalog)
        known_assets = {item["id"] for item in catalog["assets"]}
        known_projects = {item["id"] for item in catalog["projects"]}
        if set(args.asset or []) - known_assets:
            raise ValueError("unknown asset ID: " + ", ".join(sorted(set(args.asset) - known_assets)))
        if set(args.project or []) - known_projects:
            raise ValueError("unknown project ID: " + ", ".join(sorted(set(args.project) - known_projects)))
        assets = [item for item in catalog["assets"]
                  if (not args.asset or item["id"] in args.asset)
                  and (not args.project or set(item.get("projects", [])) & set(args.project))
                  and (not args.category or item["category"] in args.category)]
        project_only = bool(args.project) and not args.asset and not args.category
        if not assets and not project_only:
            raise ValueError("selection contains no assets; check IDs/filters")
        if args.list:
            for asset in assets:
                print(f"{asset['id']}\t{asset['category']}\t{asset['title_cn']}")
            if not assets:
                print("No assets are registered for this project; project access was not checked.")
            return 0
        selected_project_ids = set(args.project or [])
        required_project_ids = set(args.project or [])
        for asset in assets:
            selected_project_ids.update(asset.get("projects", []))
            required_project_ids.update(asset.get("required_projects", []))
        selected_project_ids.update(required_project_ids)
        project_results = []
        for project in catalog["projects"]:
            if project["id"] in selected_project_ids:
                checked = check_asset({**project, "category": "project", "payload_status": "PROJECT_ENTRYPOINTS"})
                checked["required_for_selection"] = project["id"] in required_project_ids
                project_results.append(checked)
        report = {
            "schema_version": 1,
            "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "context": {"host": socket.gethostname(), "real_uid": os.getuid(), "effective_uid": os.geteuid()},
            "check_scope": "stat, one-byte file read, directory traversal/list and registered probes; no deserialization, full hashing, GPU, network or download",
            "catalog": str(args.catalog.resolve()),
            "projects": project_results, "assets": [check_asset(asset) for asset in assets],
        }
        failures = [item["id"] for item in report["projects"]
                    if item["required_for_selection"] and not item["strict_passed"]]
        failures += [item["id"] for item in report["assets"] if not item["strict_passed"]]
        report["selected_required_failures"] = failures
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x") as stream:
                json.dump(report, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print("Checked:", report["checked_at_utc"], "; context UID:", report["context"]["effective_uid"])
            for item in report["projects"] + report["assets"]:
                print(f"{item['id']}\t{item['access_status']}\t{item['payload_status']}")
            print("Read access does not certify loadability, identity or scientific eligibility.")
            if failures:
                print("Selected unresolved dependencies:", ", ".join(failures))
        return 1 if args.strict and failures else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Asset check error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
