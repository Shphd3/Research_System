# Protocol: A17_03_E03 trajectory state/operator audit

## 0. Approval Snapshot

APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FINITE_FULL_ANALYSIS. User: “请你先完成第一轮任务”. Scientific mechanism/closure Unknown. Root-cause audit; no second-round new datasets/training authorized here. Active Focus: /data/250010109/Research_System/Projects/from-attention-to-search/main/focus/focus_old_task_sensitive_update_cn.md

## 1. Terminology

full=d; out=v; out_norm=v*s/||v||. State history is ordinary or protected. Initially wrong/correct subsets are fixed from the original old endpoint, never selected by intervention outcomes.

## 2. Anchor Alignment

Primary Anchor: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/subanchors/17_03_02_trajectory_mechanism_anchor.md. Inherited unknown: intermediate effects on old-error repair; no change to frozen E01/E02 evidence.

## 3. Tested Hypothesis

Immediate restriction may reduce old-error margin improvement/repair. Test within-state operator contrast, then state/history interaction. A null/opposite effect is scientifically admissible.

## 4. Rivals

Accumulated state, source/downstream gradient changes, answer-pool adaptation, strongest competitors, finite rounding. State contrasts do not isolate gradient versus downstream response.

## 5. Data and Provenance

Registered list_rules_v1 train4000/dev800. dev has400 pairs,200 per unseen-order/combination panel. Test stays closed. Next batch uses original new_order[20*t:20*(t+1)] at saved t. Input IDs and exact paths are in config and strict input_access.json.

## 6. Task and Supervision

Visible FIRST/LAST rule, three distinct words, answer prefix; correct next answer token only. No old-data training, oracle feature targets, SAE or experts.

## 7. Model and Freeze

Exact registered Qwen3-0.6B Base; FP32 native eval SDPA; only model.layers.27.self_attn.o_proj.weight[1024,2048] changes. All other parameter bytes and version counts remain fixed.

## 8. Update Construction

Recompute gradient of mean20-answer CE, micro5. s=0.01*min(original ordinary next-step raw gradient norm,1). d=-s*g/||g||. Delete original Q component without resizing; normalize remaining component separately. No momentum/decay/cumulative trajectory. Three loss gradients are recomputed only for decomposition qualification.

## 9. Conditions

Seeds29/43/71 x two orders x histories ordinary/protected x states1/16/50 =36; three directions x scale1 =108 Full cells. Smoke four seed29 step16 state/history cases x3 =12 cells,20 pairs; four independent replay cells. Saved trajectory recap includes1/16/50/100.

## 10. Primary Analysis

Freeze original old wrong/correct groups. Per case/state/history/panel report out_norm-full old pair margin and full-competitor margin changes on originally wrong group, repaired count, and initially correct losses. Separately report deletion full-out and amplification out-out_norm. Contrast ordinary/protected histories. Equal seed weights; orders separate and equal combined; panel separately and equal combined. Lists/batches are not independent seeds. Descriptive signs only; no p-values, new significance threshold, winner/state selection or blind-confirmation claims. Unqualified/missing cells remain explicit and block dependent contrasts.

## 11. Secondary Metrics and Guards

CE, pool logmass, conditional20 CE, pair-access/selection, b/h, full argmax and competitor identity. Baseline replay error<2e-5; loss split<2e-5; gradient split relative<2e-4; actual-step rounding<1e-2; out/out_norm leakage<2e-3. Exact W/source20 restoration and no-op; frozen bytes/versions and independent-process exact replay. Numerical guards do not define scientific significance.

## 12. Known Cases

Known-good: same-state restore and complete readouts. Known-bad: different batches across histories at the same t, changing Q, test access. Confusing-valid: CE improves while argmax loses; a group margin improves without a one-step repair.

## 13. Stage Contracts

Preflight binds input IDs/files and frozen code/config/contracts. Four-H100 reserved Smoke12 cells and independent replay4; FAIL blocks Full. Separate authorized four-H100 reserved Full108 after gate PASS. Audit all cells and original trajectory, register actual outputs, complete bilingual Summary/Detailed. Timeout7200s each, no fallback profile. No unbounded sweep; no additional short training branches in this contract.

## 14. Artifacts and Provenance

Execution root /data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism; unique run /data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z. Preserve source/config/freeze, strict input access, mounted pod logs, job/image/resource receipt, per-state baseline/source diagnostics, per-cell readouts and manifests, progress, worker checks, trajectory/within-state/cross-history summaries. No new trained checkpoints. Hash sources, data, selected checkpoints/manifests, subspaces and matched original readouts.

## 15. Support, Non-support, Insufficient

Qualified within-state loss of repair/margin benefit supports only a local candidate. Effects absent/opposite/heterogeneous weaken that operator explanation. No argmax flips can be insufficient for repair causality while finite margin effects remain reportable. Source ineffective or numerical failure is ineligible, not hypothesis refutation. Whole-trajectory mechanism may remain Unknown after engineering completion.

## 16. Cannot Claim

No complete100-step mediation, expert advantage, rule algorithm, universal compatibility/incompatibility, natural-language transfer or capacity necessity. Paired-output algebra is not independent mechanism evidence.

## 17. Authorization and Freeze

Question/design scope adopted by explicit completion request and prior pasted round-one plan. A-G inherit verified data/task/model and user-selected three-way analysis; exact grid/numerical guards are delegated engineering choices grounded in E01/E02. Freeze snapshots before GPU execution; after start append receipts/amendments, never silently change the scientific body.


### Completion receipt / 完成回执

2026-10-11: Smoke pt-c1i5f9pl qualified12 cells and4 exact external replays. Full pt-8aoyrzuw completed108/108, independent3888 aggregate and86400 record checks passed. No retry/skip/new training. [Summary](summary_cn.md) and [Detailed](detailed_cn.md) own bounded interpretation; mechanism/closure Unknown.
