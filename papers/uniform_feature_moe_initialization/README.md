# Uniform Feature MoE Initialization Paper Workspace

Working title:

```text
Uniform Feature Routing in Top-1 MoE: A Center-Initialization Baseline
```

Goal:

```text
Write a first self-contained paper draft for the simplest uniform-feature
case: uniform feature frequency, approximately uniform feature geometry, and a
center-initialized top-1 router.
```

Current files:

| File | Role |
|---|---|
| `latex/paper.tex` | first ICLR-style LaTeX draft |
| `latex/references.bib` | minimal bibliography and placeholders |
| `experiment_plan.md` | experiment plan requested by the 2026-07-03 meeting |
| `template/SOURCE.md` | template source record |
| `template/iclr2026.zip` | official ICLR 2026 template zip |
| `template/iclr2026_official/` | unzipped official template |

Claim boundary:

```text
This draft is a controlled-case write-up. It can argue that route-position
center initialization gives a clean and margin-protected baseline in the
uniform synthetic setting. It cannot claim real-language semantic experts,
nonuniform Zipf robustness, common/rare utility, or a deployed MoE method.
```

Main source artifacts:

```text
daily_research_reports/0703/recordings/0703meeting.md
daily_research_reports/0703/resources/theoretical_analysis.md
daily_research_reports/0703/a06_25_warmup_spectral_router_reinit/meeting_brief.md
Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_24_synthetic_common_rare_transformer_moe/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_25_warmup_spectral_router_reinit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_26_mpi_uniform_feature_router/summary.md
```
