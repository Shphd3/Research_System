# Layout and naming

Use for placement or authorized reorganization. The project owns research;
System owns shared process and access; daily folders own dated communication.

## Stable project layout

```text
Projects/<project>/main/
  roadmap.md                         project workstreams and reading route
  focus/focus_<problem>.md            stable question and researcher decision
  problem_anchors/<line>/<question>/  sole design and any settled-question report
  experiments/<line>/<question>/<experiment>/
    protocol.md
    summary.md / summary_cn.md
    detailed.md
    figures/                         selected evidence with provenance
  stories/<line>/                    requested stage/line synthesis
  research_notes/<topic>/<date>/      supporting notes and historical packages
  parking_lot/README.md
```

Preserve existing numbered line/Anchor identities and experiment conventions.
A stable topic key may name a previously unnumbered storage family; it does not
activate a question or infer a scientific dependency. Supporting notes never
replace a formal owner. Do not invent new Anchors to fill a directory.

A Focus keeps its problem_key and project path across meetings, dates and model
switches. Move an existing Focus only as part of authorized reorganization, with
old/new paths recorded. A translation is a companion, not another question.
Retained legacy records do not become current merely by appearing in an index.

## Daily reading

```text
daily_research_reports/MMDD/
  README.md / README_cn.md            short index into project owners
  meeting_report/                     requested speaking core and Q&A
  figures/                           date-local reading copies
    SOURCES.md
```

Meeting records and short progress notes may remain on the date surface. Do not
create a new Focus, Anchor, Protocol or complete result ledger there. Historical
backup snapshots retain their original meaning; they are not a placement template.
Keep one primary speaking entry when a meeting is requested, and label older
versions as history. No formal document is needed for a routine short answer.

## Anchors, experiments and stories

Names describe stable questions or comparisons, not temporary runtime state.
Keep independent parent questions as siblings. `subanchors/` is for a local
clause, rival, repair or robustness question that inherits its parent's decision;
a prerequisite relationship alone does not make one question a child.

Keep experiment settings and full evidence with the experiment, and the current
scientific design with its Anchor. An Anchor fulfills `design.md`; do not create
both. Stories use the existing numbered subject filenames and aligned language
companions. Their index names the reading scope rather than creating a new verdict.

## Evidence and delivery assets

The experiment keeps its selected evidence figures and source tables. A dated
report displaying a figure keeps a date-local reading copy with a relative link.
Record source path, purpose and SHA256 in `figures/SOURCES.md`; refresh reading
copies when the source changes. A labeled schematic is not measured evidence.

Generated figures and tables are excluded from Git by default. Select only small,
necessary evidence in the project's curated-evidence manifest; payload checks
verify the exact paths, sources, sizes and hashes. A local image is not guaranteed
in a clone. For a portable reading bundle, carry selected available assets and
list missing dependencies. Never copy raw runs, caches, datasets or checkpoints
into the research mainline. See [project access](../../../../docs/project_access.md).

## Migration completion

Move the sole current source; rebase live references and remove its old path.
Preserve original bytes/hashes for frozen identity and record relocation separately
from amendments. Do not rewrite memory, immutable receipts or historical snapshots
as current state; provide the old-path resolver instead. Preserve legacy science
and language roles rather than manufacturing translations or confirmations.

Check both repository indexes, new file discoverability, links and evidence
identity. Distinguish inherited missing sources from migration regressions. Verify
root-to-project and project-only reading. Graph and external publication remain
separately scoped; no question closes or gains approval through migration.
