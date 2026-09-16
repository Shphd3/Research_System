# Continuation Brief: completed SAE checkpoint analyses awaiting researcher review

```text
Workstream:     SAE-mediated representation evolution
Problem key:    none (bounded exploratory checkpoint analysis)
Role:           PRIMARY
Record:         .research/memory/conversations/0912-sae-llm训练执行/
Continues from: ../0912-梳理-sae-动态形成预训练方案/continuation_sol_handoff_superseded_20260914T024357Z.md
Supersedes:     continuation_pre_analysis1_completion_superseded_20260914T004614Z.md
Updated at:     2026-09-14T00:46:14Z
Status:         SUPERSEDED by ../0912-梳理-sae-动态形成预训练方案/continuation.md
Non-canonical:  points at evidence and derived reports; owns no claim,
                approval, verdict, or next decision.
```

## A. Environment roots

| Root | Path | Readable here? |
| --- | --- | --- |
| Research records | `/data/250010109/Research_System` | yes |
| SAE execution workspace | `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining` | yes; not Git |
| Frozen DCLM view | `/data/250010109/training_data_views/dclm_pair_v1` | yes |
| Qwen tokenizer/reference | `/data/share/Qwen3-0.6B-Base` | yes |

Execution outputs and checkpoints are preserved under the execution workspace.
Do not move raw outputs into the research repository and do not edit a run
directory that may be owned by a scheduler process.

## B. Read list — in order; stop if a required item is absent

| # | Path | Answers which question | Required? |
| --- | --- | --- | --- |
| 1 | `/data/250010109/Research_System/AGENTS.md` | What authority and evidence boundaries apply? | yes |
| 2 | This record's complete `memory.md` | What was approved, run, preserved, and left open? | yes |
| 3 | `daily_research_reports/0914/docs/analysis1/08_complete_experiment_report_cn.md` | What data, metrics, results, deviations and claim boundary comprise the completed analysis? | yes |
| 4 | `daily_research_reports/0914/docs/analysis1/05_execution_record.md` and `06_execution_certificate.md` | Did the semantic job and its final Smoke complete operationally? | yes |
| 5 | `daily_research_reports/0914/docs/analysis1/tables/first_stage_source_manifest.json` and `semantic_result_source_manifest.json` | Which copied tables/figures trace to which machine results? | yes |
| 6 | Execution `runs/checkpoint_audit_2x5090_0p5_1_3_5_10b_20260913T125500Z/full/audit_receipt.json` | Did the 115M-token fixed-heldout audit complete? | yes |
| 7 | Execution `analysis_runs/analysis1_20260913/full/analysis_receipt.json` | Did the 864-sentence semantic analysis complete? | yes |

No formal Anchor or Anchor-aligned Protocol owns this question. Do not infer
one from the plan, report, filenames, machine receipts, or this brief.

## C. Authority and boundaries

- Completed scope: read-only analysis of 0.5B/1B/3B/5B/10B checkpoints and a
  frozen unmatched Qwen3-0.6B Base endpoint. Both jobs performed zero optimizer
  updates and left training/checkpoints unchanged.
- Scientific eligibility: `BOUNDED_EXPLORATORY_ONLY`. The candidate semantic
  panel was programmatically constructed, has repeated template families, and
  was not researcher reviewed. A matched native-baseline comparison was not run.
- May report: measured SAE health, fixed-panel geometry/readout changes, and
  period-specific reader mismatch, with the stated denominators and caveats.
- May not claim: abstract semantic formation, monotonic emergence, stable
  cross-checkpoint semantic atoms, SAE causal benefit/harm, or generalization
  across seeds/models/natural text.
- Not approved: no new training, rerun, matched comparison, panel replacement,
  feature intervention, publication, commit, or push follows from this brief.
- Human-owned decision still open: whether to accept this bounded reading and
  whether to rebuild the semantic panel before further comparison.

## F. Current state

- DONE: fixed-heldout audit job `pt-p5mlwlqn` is `SUCCEEDED`; its full receipt
  is `PASS`, with 56,146 identical sequences and 114,987,008 token positions
  per checkpoint.
- DONE: semantic job `pt-lok5c11y` is `SUCCEEDED`; its receipt is `PASS`, with
  864 samples, 216 facts, five checkpoint caches, one Qwen cache and nine
  cross-reader caches. No optimizer update occurred.
- DONE: the complete technical reading surface is
  `daily_research_reports/0914/docs/analysis1/08_complete_experiment_report_cn.md`.
- MATERIAL LIMITATIONS: strong character-TFIDF control, templates reused across
  splits, no human adjudication, no matched no-SAE baseline, one training seed,
  no readout CI, and several planned controls marked `NOT_RUN`.
- RETRACTED/PROHIBITED INTERPRETATIONS: Smoke or `PASS` is not a scientific
  verdict; Qwen is not a matched baseline; same feature IDs do not establish
  semantic identity across checkpoints; PCA/t-SNE clusters are descriptive.
- No analysis job needs monitoring or resubmission. Existing training jobs are
  outside this completed analysis handoff and must not be stopped or duplicated.

## G. Completion contract

- This reporting task is complete when report 08, both source manifests,
  appended memory and this single CURRENT continuation pass consistency checks.
- A future scientific conclusion requires researcher review and an owning
  Anchor/Protocol; these cannot be reconstructed from this non-canonical record.
- Stop and ask the researcher before changing the panel, launching a matched
  comparison, modifying the architecture/objective, or starting any GPU work.
- Never trade a reduced or template-leaking analysis for a `COMPLETE` scientific
  label.

## H. Reusable assets — reuse before rewriting

| Asset | Path | Reuse for | Verified? |
| --- | --- | --- | --- |
| Complete report | `daily_research_reports/0914/docs/analysis1/08_complete_experiment_report_cn.md` | first reading and method definitions | yes |
| Four-part analyses | sibling `03_checkpoint_audit_four_panel_report_cn.md` and `07_semantic_evolution_four_part_report_cn.md` | concise result presentation | yes |
| Local evidence manifests | sibling `tables/first_stage_source_manifest.json` and `tables/semantic_result_source_manifest.json` | copied artifact lineage | yes |
| Frozen candidate panel | execution `analysis_assets/semantic_panel_v1.jsonl` plus `.manifest.json` | exact rerender or audit only | yes; unreviewed |
| Panel builder | execution `dense_sae/analysis/build_semantic_panel.py` | inspect how the panel was generated | yes |
| Analysis sources | execution `dense_sae/analysis/checkpoint_audit.py` and `semantic_evolution.py` | metric implementation audit | yes |
| Machine results | execution fixed-heldout `full/` and semantic `analysis_runs/analysis1_20260913/full/` | authoritative raw outputs | yes; receipts PASS |
| Final source snapshot | execution `analysis_runs/analysis1_20260913/source_snapshot/analysis1_source_20260913T164000Z.tar.gz` | exact semantic-run code provenance | yes; SHA-256 `cab649ea6e83d3d61a5d186e02b8271950fdab6dfdb7e8fadd26031e56981285` |
| Report renderer | sibling `code/render_semantic_evolution_report.py` | regenerate curated semantic figures/tables from existing caches | yes |
| Continuation template | `/data/250010109/Research_System/templates/research_process/continuation_brief_template.md` | future continuation rewrites | yes |

Assets are implementation aids and provenance pointers, not scientific verdicts.
