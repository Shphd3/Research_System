# Continuation Brief: formal representation audit reference

```text
Workstream:     Formal representation audit / methods and data reference
Problem key:    none; bounded explanation and archive
Role:           SECONDARY
Record:         .research/memory/conversations/0914-formal-representation-audit/
Continues from: ../0912-sae-llm训练执行/continuation.md (historical, already SUPERSEDED)
Supersedes:     none; first brief for this named audit reference scope
Updated at:     2026-09-15T14:53:54Z
Status:         CURRENT
Non-canonical:  owns no scientific claim, approval, verdict, or next decision.
```

This is the researcher's selected memory name for this conversation going
forward. Preserve the earlier execution and design conversation records. This
brief does not supersede another conversation's active training or design
continuation.

## A. Environment roots

- Research repository: `/data/250010109/Research_System` — readable.
- Current analysis: `/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis` — readable.
- Natural academic panel: `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/data/natural_panel_v1` — readable.
- Wikipedia data: `/data/250010109/datasets/m2d2_wikipedia_3x3` — readable.
- Academic source archives: `/data/250010109/datasets/m2d2_paired_dev_v1` — readable.

## B. Read list

1. Required: repository `AGENTS.md` and this entire `memory.md`.
2. Required: `daily_research_reports/0915/formal_representation_audit/01_measurement_reference_and_dataset_audit_cn.md` — exact methods, dataset versions, figure selection and reuse boundaries.
3. Required for current two-arm interpretation: `daily_research_reports/0914/docs/analysis2/05_execution_scope_confirmation_v1_cn.md`, `06_semantic_confirmation_v1_report_cn.md`, `07_zero_to_5b_evolution_and_sae_comparison_cn.md`.
4. Required for latest feature display: `daily_research_reports/0914/docs/analysis2/shared_activation_to_19b_cn.md` and its figure manifest.
5. Required for audited identities: analysis `report_assets/formal_representation_audit_20260915/audit_receipt.json` and the relevant dataset manifest listed in the method reference.

Stop if a source necessary for the requested claim is missing; do not infer
its contents from this brief. No formal Anchor/Protocol for a new M2D2
comparison is created by this archive.

## C. Authority and boundaries

- This checkpoint records completed local data/selection audits and reference
  writing. It authorizes no new model extraction, training, intervention or
  remote job.
- A future request may independently authorize further work; resolve that
  scope from the request and its actual owning records.
- Preserve the difference between fixed-panel observations, development
  evidence, untouched confirmation, and causal claims.
- Do not mutate or supervise unrelated training. Do not confuse current
  training source changes with the historical caches used in these figures.

## F. Current state

- DONE: method reference, explicit M2D2 version comparison, source hashes,
  frozen-panel checks, fixed-30 and fixed-150 selection recomputation.
- RETRACTED INTERPRETATION: fixed features were not selected at 0B and are not
  selected by activation duration; feature ID continuity is not semantic
  identity continuity.
- OPEN: new-model M2D2 measurement was not run here; academic data has only
  fit/dev; document identity and pretraining contamination remain unresolved.
- LIMITATION: full-source-row near-duplicate screening of the academic panel
  is verified as builder behavior, not replayed by this audit. Historical
  Wikipedia data was checked for exact token-window duplicates only.
- The legacy execution continuation is historical; no polling or automatic
  resubmission is required to complete this archive task.

## G. Completion contract

Completed when the reference, memory, continuation and audit receipt are
present and links resolve. Future continuation follows the researcher's next
question; this record is not an outstanding execution plan.

## H. Reusable assets

| Asset | Path under current analysis root unless absolute | Use |
|---|---|---|
| Input contract | `config_analysis2_v1.json` | fixed panel, tokenizer, positions and original paired milestones |
| Frozen input | `data/panel_frozen_v1.jsonl`, `data/triplets_frozen_v1.jsonl`, `data/frozen_manifest_v1.json` | exact short-sentence input |
| Original measurement | `semantic_confirmation_v1.py` | relation, sparse overlap, quality, readout definitions |
| Original caches | `runs/confirmation_v1_20260914/full/caches/` | two-arm 0B–5B postprocessing |
| 0B plots | `report_assets/render_zero_to_5b_comparison.py`, `report_assets/zero_to_5b_v1/` | reuse figures and tables |
| Fixed 30 selection | `report_assets/render_shared_domain.py`, `report_assets/shared_domain_v1/` | fit-only retrospective feature cohort |
| Fixed 150 selection | `report_assets/render_shared_19b.py`, `report_assets/shared_domain_19b_v2/` | retained old IDs plus expanded cohort |
| Source audit | `report_assets/audit_formal_representation_sources_20260915.py` | reproduce this archive's identity and selection checks |
| Academic panel | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/data/natural_panel_v1/` | future natural-domain development measurement |
| Historical Wikipedia panel | `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/` | historical window-based replication |

All listed assets were readable and checked at checkpoint. Re-verify hashes
before reuse; do not rebuild a dataset or alter original manifests silently.
