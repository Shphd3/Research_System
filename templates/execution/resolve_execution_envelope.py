#!/usr/bin/env python3
"""Resolve one execution profile and image from docs/execution_envelope.md."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
ENVELOPE = ROOT / "docs/execution_envelope.md"
REGISTRY_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def fail(message: str) -> None:
    raise SystemExit(message)


def registry() -> dict:
    if not ENVELOPE.is_file():
        fail(f"missing execution envelope: {ENVELOPE}")
    match = REGISTRY_RE.search(ENVELOPE.read_text(encoding="utf-8"))
    if match is None:
        fail("execution envelope has no parseable registry block")

    top: dict[str, str] = {}
    fields: dict[str, dict[str, str]] = {}
    entities: dict[str, dict[str, dict[str, str]]] = {}
    section = entity = None
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            section = entity = None
            if stripped.endswith(":"):
                section = stripped[:-1]
                fields.setdefault(section, {})
                entities.setdefault(section, {})
            elif ":" in stripped:
                key, value = stripped.split(":", 1)
                top[key.strip()] = value.strip().strip("\"'")
            continue
        if section is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip().strip("\"'")
        value = value.strip().strip("\"'")
        if indent == 2 and not value:
            entity = key
            entities[section].setdefault(entity, {})
        elif indent == 2:
            fields[section][key] = value
        elif indent == 4 and entity is not None:
            entities[section].setdefault(entity, {})[key] = value
    return {"top": top, "fields": fields, "entities": entities}


def resolve(profile_arg: str | None, image_arg: str | None) -> dict[str, str]:
    data = registry()
    top = data["top"]
    entities = data["entities"]
    profiles = {**entities.get("profiles", {}), **entities.get("legacy_profiles", {})}
    images = {**entities.get("images", {}), **entities.get("legacy_images", {})}
    profile_key = profile_arg or top.get("default_profile")
    image_key = image_arg or top.get("default_image")
    if not profile_key or profile_key not in profiles:
        fail(f"unknown or missing profile key: {profile_key}")
    if not image_key or image_key not in images:
        fail(f"unknown or missing image key: {image_key}")
    profile = profiles[profile_key]
    image = images[image_key]
    if profile.get("status") == "deferred":
        fail(f"profile is deferred and unavailable: {profile_key}")
    if image.get("status") in {"deferred", "prohibited_for_new_runs"}:
        fail(f"image is unavailable for new submissions: {image_key}")
    submission = data["fields"].get("submission", {})
    return {
        "resource_profile": profile_key,
        "profile_status": profile.get("status", ""),
        "execution_surface": profile.get("surface", ""),
        "workspace": profile.get("workspace", ""),
        "aec2": profile.get("aec2", ""),
        "worker_spec": profile.get("worker_spec", ""),
        "worker_nodes": profile.get("worker_nodes", "1"),
        "worker_processes": profile.get("worker_processes", ""),
        "gpus": profile.get("gpus", ""),
        "quota_type": profile.get("quota_type", ""),
        "priority": profile.get("priority", ""),
        "storage_mount": profile.get("storage_mount", ""),
        "gpu_used": profile.get("gpu_used", ""),
        "image_id": image_key,
        "image_status": image.get("status", ""),
        "image_url": image.get("url", ""),
        "image_interpreter": image.get("interpreter", ""),
        "image_torch": image.get("torch", ""),
        "image_cuda": image.get("cuda", ""),
        "image_activation": image.get("activation", ""),
        "submission_entry_point": submission.get("entry_point", ""),
        "envelope": ENVELOPE.relative_to(ROOT).as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile")
    parser.add_argument("--image")
    parser.add_argument("--format", choices=("json", "shell"), default="json")
    args = parser.parse_args()
    result = resolve(args.profile, args.image)
    if args.format == "shell":
        for key, value in result.items():
            print(f"{key.upper()}={json.dumps(str(value))}")
    else:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
