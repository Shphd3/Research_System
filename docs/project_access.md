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
Both output directory and ZIP must be new. The builder uses only the Python
standard library and generates no HTML page or browser interface.

Open `README.md` in a text editor or Markdown reader. It lists the reading order
and package-relative file paths, so clickable links are optional. `documents/`
contains Markdown reading copies with package-relative links and a source note;
`sources/` keeps exact original bytes, including the original links.
`manifest.json` records all selected repositories' versions, both kinds of file
hashes and omitted dependencies. `UNAVAILABLE.md` explains missing, unselected or
out-of-scope sources; unavailable local links lead there instead of silently
pointing outside the package.

Existing Unknown/draft states remain source content; packaging does not confirm
wording or approve work. Edit the owning records, not the reading copies. The
inventory covers owner fields, inline links and single-line reference definitions.
Other code paths remain literal text. History and worker data are not recursively
copied. Heading fragments and TeX formulas are retained; if the reader does not
support them, use headings/file paths and the document's verbal explanation.
The builder does not author missing explanations; apply the shared
[writing rules](report_writing.md) to the requested text.

Check the Markdown and manifest before relying on the bundle. Missing worker data,
figures or historical sources remain explicit limitations. External distribution,
collaborator sync and publication keep their own scope.

## Small evidence assets

The default Git policy excludes generated output. A project may explicitly select
small source tables, figures or provenance records in its curated-evidence
manifest. Checks require the exact file, purpose, source and hash; raw runs,
checkpoints and caches remain excluded. A local date figure is not automatically
version controlled. A portable reading bundle carries the selected available
figures with their sources; never promise that ignored files arrive in a clone.
