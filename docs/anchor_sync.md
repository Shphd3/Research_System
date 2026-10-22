# Anchor reading sync after research guidance

[中文](anchor_sync_cn.md) · [Published reading index](../sync/anchors/README.md)

The researcher requested a standing workflow: after delivering a substantive
Anchor guidance or revision round, refresh a bounded reading copy in
Research_System. A reader with access only to this repository should be able
to read the question, design, necessary evidence and dataset identity.

## Trigger and destination

Run this step after completing the owning sources for the round and before
reporting delivery complete. An Anchor can still be draft or pending researcher
review. Guidance completion does not mean question closure or scientific approval.
Plain conversation without a formal source does not require inventing an Anchor.

Use one stable folder per existing owner:

```text
sync/anchors/<project>/<anchor_id>/
  README.md        reading order
  documents/       reading copies with portable links
  sources/         exact source bytes and selected small metadata
  manifest.json    source versions, hashes and omitted dependencies
  UNAVAILABLE.md   sources not selected, unavailable or execution-side
```

The project retains the editable scientific sources. The System folder is a
read-only generated view. Preserve existing IDs, language authority, draft and
Unknown states, result eligibility and recorded approval. Copying grants no
experiment authority. Parent/child relationships stay with the source registry.

## Maintain a bounded profile

[profiles.json](../sync/anchors/profiles.json) lists each destination's explicit
source files. Include the named Anchor and available language companion, an
applicable Focus, the necessary round's Protocol/Summary/Detailed, and a dataset
guide with small provenance metadata when relevant. Select exact rounds; a newer
round does not erase earlier evidence. Do not recursively export the project,
all linked histories, raw JSONL, checkpoints, activation arrays or execution logs.

A new registered sync profile creates navigation rather than a new research
question. Add its entry to the bilingual `sync/anchors/README` index; reuse that
entry on later rounds, with Git recording earlier versions. Retain only material relevant to the delivered guidance. Existing
`sync/S000_current_specialization/` and date-specific handoffs keep their roles;
this directory supplies stable owner-based access.

## Refresh and verify

The wrapper reuses the established `build_reading_bundle.py` source-selection,
link-rebasing and provenance logic:

```sh
python tools/sync_anchor_reading.py --project from-attention-to-search --anchor 17_04
python tools/sync_anchor_reading.py --project from-attention-to-search --anchor 17_04 --check
```

Generate a candidate in a temporary directory, verify its scope and source hashes,
then refresh only the generated destination's owned files. Refuse to overwrite
manual changes or an unowned destination. Never edit a reading copy to repair
research meaning; update the owning source and regenerate it. Source absence
remains recorded; do not imply that a worker path became a GitHub download.

Check source and reading-copy hashes, local portable links, preserved states and
Git payload scope. An unchanged source does not need another snapshot merely
because time passed. `--check` works in a complete workspace; a System-only
reader uses the saved manifest and copies without requiring the original project.

This standing request authorizes in-scope reading synchronization. Commit/push
follow an existing applicable authorization; otherwise report the local copy as
not yet published. Never say a local file is visible on GitHub before publishing
and verifying it. The present A17_04 update has explicit commit/push authorization.

## Event-based and periodic use

The default trigger is a completed guidance round. A separately requested
periodic task may check freshness and refresh registered profiles when sources
are accessible. A schedule does not create access to a missing project or permit
new experiments. No periodic automation is established by this document.
