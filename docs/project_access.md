# Read a research project from System

[中文](project_access_cn.md)

`Research_System` and repositories under `Projects/` are separate repositories.
A clone of System does not contain `from-attention-to-search`. A relative link is
navigation, not a copy of another repository's files.
The local project's configured upstream is
[`BinaryCheater/from-attention-to-search`](https://github.com/BinaryCheater/from-attention-to-search),
on branch `Xingyu`. Local edits appear upstream only after separately requested
commits and pushes; repository access is still required.

## Full workspace

Start at a named file. Otherwise use `PROJECTS.md` to select a project, its
`main/roadmap.md` to select a workstream, then the Focus/Anchor or Summary needed
for the task. Do not read every record. Project roadmaps own project routing;
System does not maintain a second workstream table.

Run `python tools/check_current_entrypoints.py` to verify tracked entrypoints.
During an authorized edit, `--working-tree` checks present files and reports those
not yet tracked. A successful link check is not scientific approval.

## Legacy paths and frozen identities

For a path from an earlier chat, receipt or unchanged archive, run:

```sh
python tools/research_paths.py daily_research_reports/0930/docs/domain_update_geometry/summary.md
```

`research_locations.json` records old/new paths, original and relocated hashes,
source repository commits and immutable original-byte locations. Navigation-only
rewrites do not amend registered settings, results or approval. Verify a frozen
hash against the original bytes, not a relocated Markdown file with rebased links.
Memory, immutable receipts and historical snapshots are not rewritten as current
state. Never treat the immutable byte archive as another live research source.

## Incomplete workspace or one-repository reader

If the project is unavailable, say which sources could not be read. Do not infer
their contents from the project name, System index or earlier chat. An environment
with access to both repositories can read them separately; otherwise create a
local reading bundle from a complete workspace:

```sh
python tools/build_reading_bundle.py --project from-attention-to-search --output /tmp/research-reading
```

By default, the builder follows the roadmap's current Focus and its explicit
design/experiment owners. With `--source <System-relative-path.md>`, it includes
only the named documents, their available language companions, the project route
and referenced small assets. Repeat `--source` to include another record; links
do not silently expand the document selection. Add `--zip` for one portable archive.
Both output directory and ZIP must be new. Rich Markdown and
formula rendering use the optional `tools/reading_requirements.txt` dependencies
(`python -m pip install -r tools/reading_requirements.txt`). Without them the
builder preserves readable source text; the manifest states the rendering mode.

The bundle contains the project route, selected records, a static HTML
reader, original source copies and a manifest of source versions, hashes and
omitted dependencies. Versions cover all repositories used by the selection.
It includes existing Unknown/draft states as labeled source
content; it neither confirms wording nor approves work. It is local and generated,
not a second place to edit the research. The inventory covers owner fields and
inline links; rich rendering also resolves reference-style Markdown links.
Without the renderer, reference-style links remain literal source text. Other code
paths are not dependencies. History and worker data are not recursively copied.
Section links open the matching heading; unavailable headings are listed and fall
back to the document. Exact Markdown copies retain their original links; use
`index.html` for portable navigation.

Inspect the delivered HTML/Markdown and its manifest before relying on it. Missing
worker data, figures or unavailable historical sources remain visible limitations.
External distribution, collaborator sync and publication keep their own scope.

## Small evidence assets

The default Git policy excludes generated output. A project may explicitly select
small source tables, figures or provenance records in its curated-evidence
manifest. Checks require the exact file, purpose, source and hash; raw runs,
checkpoints and caches remain excluded. A local date figure is not automatically
version controlled. A portable reading bundle carries the selected available
figures with their sources; never promise that ignored files arrive in a clone.
