# Research layout and reading refactor — 2026-10-02

[中文](research_refactor_20261002_cn.md) · [Checks](research_refactor_20261002_validation.json)

The authorized refactor is complete for the starting September snapshot and its
registered historical Focuses. System now owns shared rules and project access;
the research project owns questions, designs and evidence; daily folders retain
meetings, short updates and reading indexes. Scientific states are unchanged.

## Read and work

Start at a named source. Otherwise use [PROJECTS](../PROJECTS.md), then the
[project roadmap](../Projects/from-attention-to-search/main/roadmap.md). Read the
Focus for the question and pending decision; follow its Anchor, Protocol and
Summary/Detailed only as needed. The roadmap does not duplicate results.

465 files were relocated: 443 into the independent project and 22 into daily
meeting locations. This includes formal designs/results, registered Focuses,
reference source code and supporting notes. Legacy question identities, duplicate
historical Focus versions and original language roles were preserved rather than
silently consolidated. [The manifest](research_locations.json) records each move
and original-byte archive. Earlier paths resolve through `tools/research_paths.py`.

Reports follow [shared writing guidance](report_writing.md): short, direct
sentences; consistent terms; defined objects; explicit assumptions and boundaries.
Final reports use the explanatory structure needed by the research rather than
an eleven-heading template. Anchor and Summary retain their owning contracts.
This adopts clear-language principles, not a claim of STE100 compliance.

Markdown remains the editable source. The [local reading bundle](project_access.md)
adds search, foldable detail, formulas and figures. The supplied example contains
14 source documents and 22 referenced assets. It lists 132 omitted links, mostly
other research lines and worker sources. No service or network is needed to read
it. Packaging drafts preserves their pending status.

## Verification and limits

- All 465 original hashes and destinations verified; relocated bodies differ only
  in navigation or recorded paths. A separate comparison checked 1,428 existing
  canonical Markdown records and 1,133 protected historical/memory/sync/Graph files.
- 56 System/project entrypoints, 14 skills with 71 local links, 34 unit tests and
  all 65 selected evidence identities passed. Rich rendering was also tested.
- No introduced unresolved inline link remained in the changed scope. 174
  inherited unavailable references remain recorded in the local audit archive.
- Math-source checks found no added diagnostic. Existing historical source
  diagnostics were retained; this is not a mathematical proof or blanket rendering
  certification. Desktop/mobile navigation and sampled formulas/figures were inspected.
- `AGENTS.md` is 7,299 bytes versus 7,301 before; README and PROJECTS were shortened.
  The web project prompt is unchanged. Both repositories passed whitespace checks
  allowing retained Markdown hard breaks.

Changes remain local and uncommitted; 30 entrypoints await tracking. The project
is still an independent checkout. Commit/push, execution and external sync were
not performed. Concurrent October 2 candidate drafts were left untouched and are
outside this migration snapshot. No claim of independent reader comprehension or
new scientific approval follows from these checks.
