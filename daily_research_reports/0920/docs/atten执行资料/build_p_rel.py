#!/usr/bin/env python3
"""Generate the proposed controlled relation panel. No external dependencies.
This creates an audit dataset, NOT evidence about a language model.
Python >= 3.10. Usage: python build_p_rel.py --output data/P_rel_v1
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import re

TEMPLATES: dict[str, list[str]] = {
    "horizontal": [
        "{A} is to the left of {B}.",
        "{B} is to the right of {A}.",
        "To the left of {B} is {A}.",
        "To the right of {A} is {B}.",
        "The item on the left of {B} is {A}.",
        "The item on the right of {A} is {B}.",
        "{B} has {A} on its left.",
        "{A} has {B} on its right.",
    ],
    "vertical": [
        "{A} is above {B}.",
        "{B} is below {A}.",
        "Above {B} is {A}.",
        "Below {A} is {B}.",
        "The item higher than {B} is {A}.",
        "The item lower than {A} is {B}.",
        "{B} has {A} above it.",
        "{A} has {B} below it.",
    ],
    "sequence": [
        "{A} comes before {B}.",
        "{B} comes after {A}.",
        "Before {B} comes {A}.",
        "After {A} comes {B}.",
        "{A} precedes {B} in the sequence.",
        "{B} follows {A} in the sequence.",
        "{B} has {A} earlier in the sequence.",
        "{A} has {B} later in the sequence.",
    ],
    "containment": [
        "{A} is inside {B}.",
        "{B} contains {A}.",
        "Inside {B} is {A}.",
        "Surrounding {A} is {B}.",
        "{A} is contained within {B}.",
        "{B} has {A} inside it.",
        "{B} encloses {A}.",
        "{A} is enclosed by {B}.",
    ],
}


def split_name(entity_bucket: str, template_bucket: str) -> str:
    table = {
        ("fit", "fit"): "fit",
        ("fit", "dev"): "dev_template",
        ("dev", "fit"): "dev_entity",
        ("dev", "dev"): "dev_joint",
        ("fit", "test"): "test_template",
        ("test", "fit"): "test_entity",
        ("test", "test"): "test_joint",
    }
    return table.get((entity_bucket, template_bucket), "reserved")


def build(output: Path, seed: int) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    # Refuse silent overwrites: versioned artifacts must remain immutable.
    if any(output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {output}")
    rng = random.Random(seed)
    entity_numbers = list(range(1, 401))
    rng.shuffle(entity_numbers)
    rows: list[dict] = []
    for pair_idx in range(200):
        # Reference order is independent of the truth value and number magnitude.
        e1 = f"box {entity_numbers[2 * pair_idx]:04d}"
        e2 = f"box {entity_numbers[2 * pair_idx + 1]:04d}"
        entity_bucket = "fit" if pair_idx < 120 else "dev" if pair_idx < 160 else "test"
        prefix = f"Objects in reference order: {e1}; {e2}. "
        for family_idx, (family, templates) in enumerate(TEMPLATES.items()):
            for t_idx, template in enumerate(templates):
                template_bucket = "fit" if t_idx < 4 else "dev" if t_idx < 6 else "test"
                for direction in (0, 1):
                    # 0: first reference entity bears R to second; 1: reverse.
                    A, B = (e1, e2) if direction == 0 else (e2, e1)
                    body = template.format(A=A, B=B)
                    text = prefix + body
                    sample_id = f"P_rel_v1.p{pair_idx:03d}.{family}.t{t_idx}.y{direction}"
                    rows.append({
                        "sample_id": sample_id,
                        "dataset": "P_rel_v1",
                        "text": text,
                        "body_start_char": len(prefix),
                        "split": split_name(entity_bucket, template_bucket),
                        "entity_bucket": entity_bucket,
                        "template_bucket": template_bucket,
                        "source_group_id": f"pair_{pair_idx:03d}",
                        "semantic_state_id": f"pair_{pair_idx:03d}.{family}.y{direction}",
                        "contrast_pair_id": f"pair_{pair_idx:03d}.{family}.t{t_idx}",
                        "template_id": f"{family}.t{t_idx}",
                        "family": family,
                        "family_label": family_idx,
                        "direction_label": direction,
                        "joint_label": family_idx * 2 + direction,
                        "reference_entities": [e1, e2],
                        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    })
    assert len(rows) == 12800
    assert len({r["sample_id"] for r in rows}) == len(rows)
    assert len({r["text"] for r in rows}) == len(rows)
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        groups[r["contrast_pair_id"]].append(r)
    # The two opposite meanings in a contrast pair have the same word multiset.
    for pair in groups.values():
        assert len(pair) == 2
        assert {r["direction_label"] for r in pair} == {0, 1}
        wordsets = [Counter(re.findall(r"\w+|[^\w\s]", r["text"].lower())) for r in pair]
        assert wordsets[0] == wordsets[1]
    entity_sets = {
        bucket: {e for r in rows if r["entity_bucket"] == bucket for e in r["reference_entities"]}
        for bucket in ("fit", "dev", "test")
    }
    assert not entity_sets["fit"] & entity_sets["dev"]
    assert not entity_sets["fit"] & entity_sets["test"]
    assert not entity_sets["dev"] & entity_sets["test"]
    counts = dict(sorted(Counter(r["split"] for r in rows).items()))
    expected = {"fit": 3840, "dev_template": 1920, "dev_entity": 1280,
                "dev_joint": 640, "test_template": 1920, "test_entity": 1280,
                "test_joint": 640, "reserved": 1280}
    assert counts == dict(sorted(expected.items()))
    for split in counts:
        selected = [r for r in rows if r["split"] == split]
        with (output / f"{split}.jsonl").open("w", encoding="utf-8") as f:
            for row in selected:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    (output / "templates.json").write_text(json.dumps(TEMPLATES, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {"dataset": "P_rel_v1", "seed": seed, "n_records": len(rows),
                "counts": counts, "automatic_checks_passed": True,
                "human_language_review": "required_before_model_evaluation",
                "model_tokenizer_length_check": "not_run",
                "meaning": {"horizontal": "left_of", "vertical": "above",
                            "sequence": "before", "containment": "inside"}}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260920)
    args = parser.parse_args()
    print(json.dumps(build(args.output, args.seed), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
