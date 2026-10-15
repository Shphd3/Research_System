# Continuation: completed A22 CrossCoder analysis

Record:1012-全层 Qwen3 CrossCoder训练; thread01a13046-9276-7d13-9af9-a2bda6aa9e5b. Updated:2026-10-13T15:46:17.249648+00:00; CURRENT in this record only. Codex /root (Codex desktop; exact model unknown). Non-canonical, no new execution or scientific approval.

## Objective and scope

Transfer the completed frozen-model dictionary for later shared-feature analysis. This user request authorizes a memory checkpoint and handoff, not a new remote analysis job. Visible roots: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder; Base=/data/share/Qwen3-0.6B-Base. Protect frozen training artifacts and other conversation records; place new analysis in a fresh execution analysis directory.

## Read list

Read the [complete report](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/final_training_20261013T115447Z/report.md) for seven figures and measured limits, [exact bindings](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/handoff_20261013T154617Z/bindings.json) for checkpoint/data identities and loading pointers, and [actual configuration](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/configuration.json) plus [input contract](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/input_contract.json). Follow [asset lookup](/data/250010109/Research_System/assets/README.md) and refresh strict access in the receiving environment. Reuse extraction_a16.py,batchtopk_a18.py,metrics.py under exec/crosscoder for exact definitions.

## Current work and reusable assets

A22/pt-2639gg8p completed999997440unique paired positions/exposures,244140updates including1000ancestorupdates. Frozen Qwen3-0.6B Base;14one-based blocks2,4,...28,H1024,F16384. Final and0.5B immutable resumable checkpoints registered;Base unchangedPASS. FullVAL L0254.539,zero-hit1.770%,FVE.864722-.999333;block28fixed-panelCEdelta+.305962nats. Scientific/measurement approvalUnknown.

Reuse FastBatchTopKCrossCoder; builder/load reference crosscoder/train_a22.py:328. Restore full crosscoder weights/buffers and normalization for inference, not Adam training. Same-position inputs; fixedTRAINmean/RMS normalization;eval/no_grad/use_threshold=True; saved inverse transform. Threshold.051281. Actual methodReLU+globalBatchTopK,k256average,L1=0,unsquaredmeanhiddenL2+AuxK/32;BF16Base/GEMMs,FP32master/loss. Do not rerun trainer or fitVALscales/thresholds.

## Next action and completion

Receiving user controls scope. AI proposal: per-feature layer profile -> reconstruction-utility checks -> independent text evidence -> shared-contribution aggregation, with feature-matched0.5B/final stability. Figure5aggregates all features and has not classified shared features. Return methods,evidence,limits; missing essential assets block dependent work. No new analysis experiments executed here. New costly remote work needs an explicit scope/budget; no resubmission/extension,scientific state edit,commit orpush from this brief.

DCLMfileholdout has unknown original-document/near-duplicate independence. FVE is whole-window SSEratio vsfixedTRAINmean; otherpapers use differentreductions. TRAINinactivity differs fromVALzero-hit. Acausal codes and highest-site absoluteoverwrites are not causal evidence; single frozenBasecannotshowpretrainingemergence. A23/A24are separateobjects whose live statewasnotrefreshedhere. [Chinese companion](continuation_cn.md).
