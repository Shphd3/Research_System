# Continuation Brief: 0914 meeting decision and auxiliary-backbone paired pilot

```text
Workstream:     SAE-mediated representation intervention
Problem key:    none; researcher has not confirmed a new canonical key
Role:           PRIMARY
Record:         .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/
Continues from: continuation_analysis2_results_superseded_20260914T103536Z.md
Supersedes:     continuation_analysis2_results_superseded_20260914T103536Z.md
Updated at:     2026-09-14T10:35:36Z
Status:         CURRENT
Non-canonical:  owns no scientific claim, approval, verdict or next decision.
```

## A. Environment roots

- Repository: `/data/250010109/Research_System` (readable).
- Existing training: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining` and `20260913_dense_baseline_pretraining` (readable).
- Analysis: `/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis` (readable).
- Imported/planning root P: repository `daily_research_reports/0914/sae_research_decision_materials/` (readable).
- Execution workspace is not Git. Do not edit live training files or assume current resource availability. A new experiment directory is proposed, not yet created by this task.

## B. Read list — in order

| Source | Why | Required |
|---|---|---|
| `AGENTS.md` | authority and document boundaries | yes |
| P/`00_START_HERE_cn.md`, `01_meeting_decision_audit_cn.md` | source attribution and corrected old-summary claims | yes |
| P/`02_next_step_plan_cn.md` | one candidate experiment, exact gradient/data/budget choices | yes |
| P/`live_source_audit.json` | actual config and source identities | yes |
| `docs/training_reuse_index.md` and actual execution README/sources | reuse before rewriting | yes for implementation |
| `daily_research_reports/0914/meeting/meeting01/0914 SAE model training.md` | original transcribed advisor/senior intent | yes for changing proposal |
| `daily_research_reports/0914/docs/analysis2/06_semantic_confirmation_v1_report_cn.md` and `shared_activation_to_19b_cn.md` | prior results and visualization limits | yes for interpreting prior findings |
| Researcher's future decision card/Protocol | actual adopted design and execution approval | required before new GPU execution; currently absent |

The ZIP proposal, meeting auto-summary and this memory are not canonical approvals. Read the whole accumulating memory when resuming this conversation; current instructions supersede historical next actions, not historical evidence.

## C. Authority and boundaries

Current user scope: import materials, audit meeting, plan next steps and write memory/handoff. No training or new scientific state is authorized by these files. The serial-first candidate follows the transcript but its lambda, budgets and acceptance thresholds are AI recommendations. Do not silently switch to sidecar-first or add AuxK. Do not erase the old training or use its differently configured trajectory as the new matched control.

## E. Action list

| Action | Verify | Pass | Fail |
|---|---|---|---|
| Review decision prompt | source/plan/actual configuration available | produce one concrete decision card | record precise missing item |
| Prepare in-scope implementation proposal | read reuse map and record unique gradient switch | make minimal diff and tests reviewable within current user authorization | do not guess gradient ownership |
| Execute only approved phase | actual researcher scope, envelope, gradient/resume/data gates | bounded Smoke/development with receipts | stop failed phase; no automatic full training |
| Interpret | raw-h paired result, LM cost, SAE diagnostics separated | return bounded comparison to researcher | retain Unknown; no causal upgrading |

## F. Current state

Done: imported originals and verified hashes; original transcript and real code audit; detailed staged plan, decision/execution prompts; memory updated. No new training-source edits or jobs in this planning turn. Pending: adopted problem/design/Protocol and corresponding execution authorization, pilot implementation and fresh natural-text panel. Package's two target papers remain unidentified; feature matching and full downstream suite are not startup prerequisites. Former extraction results through19.136B already exist and need not be rerun.

## G. Completion contract

This requested planning/handoff stage is complete after link/hash checks. The receiving task acts only on its actual user scope and records its own identity. New GPU execution requires a concrete approved scope; no permission follows from forwarding a plan alone. Report real startup evidence and ETA rather than indefinitely supervising unless asked.

## H. Reusable assets

| Asset | Location | Reuse / boundary |
|---|---|---|
| Training engine/model/data/checkpoint | existing SAE execution root, source hashes in P/live_source_audit.json | current six key files match initial run snapshot; clone before edits |
| Real config and parameter counts | SAE `runs/full_50b_bottleneck8_202609121130/` | use actual8-layer config, not obsolete10-layer draft |
| Baseline model export / paired analysis | baseline package; analysis `semantic_confirmation_v1.py` | verify exact pre-MLP export API; reuse inference and probes |
| Frozen360 panel / prior caches | analysis `data/` and `runs/confirmation_v1_20260914/full/` | debug/exploratory, not fresh confirmation |
| Fixed150 figure/caches | analysis `report_assets/shared_domain_19b_v2/` and dated19B report | no new inference needed; selected-slot display only |
| Original package/transcript | P and repository meeting path above | preserved inputs, not authority to run |
| Prompts | P/`03_decision_ai_prompt_cn.md`, `04_execution_ai_prompt_cn.md` | researcher-forwardable local drafts; no external messages sent |
