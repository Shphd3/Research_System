# Projects

System owns shared rules and access. Each project owns its research route and
canonical records. Start with a named source; otherwise select a project below.
The project roadmap links its Focus, Anchor and results. Do not maintain a second
workstream/status table here.

## Project Surfaces

| Project | Role | Entry |
|---|---|---|
| ntp-learning-mechanisms | Independent NTP evidence project; its roadmap and owning records hold current research state. | [Research route](Projects/ntp_learning_mechanisms/main/roadmap.md) · [中文](Projects/ntp_learning_mechanisms/main/roadmap_cn.md); [local entry](Projects/ntp_learning_mechanisms/README_cn.md); [runtime-asset registry](Projects/ntp_learning_mechanisms/asset_manifest.json); [cross-machine rules](Projects/ntp_learning_mechanisms/docs/working_cycle_cn.md); [GitHub project](https://github.com/Shphd3/ntp-learning-mechanisms) |
| from-attention-to-search | Default active research project; existing lines keep their own priorities | [Research route](Projects/from-attention-to-search/main/roadmap.md) · [中文](Projects/from-attention-to-search/main/roadmap_cn.md) |
| diffusion-language-models | Incubating research; consult source decisions before execution | [Literature audit](Projects/diffusion-language-models/main/literature/2026-07-17_diffusion_language_model_evidence_audit.md) |
| router-representation-coupling | Independent temporary router-gradient comparison; execution delegated | [Research route](Projects/router-representation-coupling/main/roadmap.md) · [中文](Projects/router-representation-coupling/main/roadmap_cn.md) |
| decommon-router-training | Implementation surface | `Projects/decommon-router-training/` |
| decommon-router-evaluation | Evaluation and engineering qualification | `Projects/decommon-router-evaluation/` |
| kv_cache | Reference; only xyDeng is managed, never push main | `Projects/kv_cache/` |
| academic_writing | Course delivery | `Projects/academic_writing/` |

## Reading And Access

- [Daily reading](daily_research_reports/README_cn.md): meetings and short date indexes.
- [Project access](docs/project_access.md) ([中文](docs/project_access_cn.md)): complete workspace, incomplete checkout and portable reading bundles.
- [Asset registry](assets/README.md) ([中文](assets/README_cn.md)): checkpoint, representation and dataset locations, access snapshots and required-asset checks.
- [Legacy path resolver](tools/research_paths.py): find migrated files from earlier chats and receipts.
- [Earlier project map](docs/archive/project_map_20260926_before_refactor.md): historical context.

A System clone alone does not include independent repositories under `Projects/`.
Run `python tools/check_current_entrypoints.py` in a full checkout. During local
edits use `--working-tree`; report unavailable sources or untracked files honestly.
A navigation check supplies no scientific judgment or execution approval.

The from project uses its existing `Xingyu` branch and the verified
`/data/250010109/MoE_Router/` execution workspace. Inspect the checkout and owning
Protocol before operations; a path is not authorization. Independent projects
remain independently owned. Graph, external sync, commit and push keep their
explicit scope.
