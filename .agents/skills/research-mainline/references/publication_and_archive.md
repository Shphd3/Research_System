# Publication And Archive

Use this reference only for an explicitly requested root Anchor publication or
for archive maintenance.

## Root Anchor Mirror

Project-local Anchors remain canonical. When the user explicitly requests the
root mirror, publish and verify it with:

```text
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py --check
```

The publisher keeps internal links relative and rewrites links leaving the
Anchor tree to repository-root absolute paths. Never hand-edit the generated
mirror; update its source and republish.

Publication must preserve the exact source claim, boundary, next decision, and
artifact links. It does not authorize external collaborator sync, handoff,
commit, or push.

## External Handoff

Route an explicitly requested external package to `research-communication`
handoff mode. It may include only approved Anchors, Protocols, Summary,
Detailed, referenced curated figures or tables, and a short index. Exclude raw
logs, checkpoints, datasets, full result directories, caches, private notes,
unrelated Anchors, and unrequested code.

## Archive

Archive superseded or support-only experiments instead of deleting them. Keep
a short index with the archived folder, reason, and reopening condition. An
archive move must preserve evidence links and cannot change the registered
scientific meaning.

## Stop Conditions

Stop if the target is dirty in a way that would overwrite unrelated work, the
publication scope is not explicit, a source is unconfirmed, or link validation
fails. Completion requires a clean generated check or an audited archive index;
commit and push remain separate explicit actions.
