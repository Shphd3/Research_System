# Results: topic relation, template mismatch and shared-parameter interference

[Protocol](protocol.md) · [Detailed evidence](detailed.md) · [Chinese reading surface](summary_cn.md) · [结果文件摘要清单](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/result_artifact_manifest.json)

Execution COMPLETE. Registered training prediction NOT SUPPORTED at its preset magnitude; format trend and dynamic bridge INSUFFICIENT. This requested AI analysis does not promote researcher-owned scientific state.

## 1. Purpose

Test whether topic relation or meaning-preserving prompt-template mismatch predicts the cost of sharing a fixed adaptation budget, and whether actual cross-task updates support that explanation.

## 2. Hypothesis

Related topics may be more compatible with sharing. The strongest rival is that template-mixture mismatch increases shared excess loss for fixed question content. SAE prediction is a downstream question, not measured here.

## 3. Analysis method

- Freeze S7 and adapt the last down projection with LoRA. Compare shared rank16 against two topic-routed rank8 branches at65,536 total parameters, with matched Solo, random grouping and capacity controls. Six subjects, six fixed pairs, five balanced views forming three mismatch levels, three seeds;640 physical trajectories each run128 updates before one-time CONFIRM access.
- At fixed S16 states8/64/128, apply rollback-only source updates with copied Adam moments and full/half learning rates. Evaluate independent READOUT self/cross effects and a zero-new-gradient momentum control; step64 is primary.
- Use5,000 synchronized subject-family bootstrap draws with fixed subjects/seeds. Report initial gradient geometry and transfer separately. Additional uniform-letter/accuracy checks are posthoc descriptive analyses; no SAE predictor was extracted or fitted.

## 4. Conclusion

| Registered quantity | Estimate [interval] | Verdict |
| --- | --- | --- |
| Γ: FAR minus NEAR isolation gain | +0.001631 [-0.000521, +0.003821] (95%) | Upper bound below preset0.01 |
| FAR shared16 minus isolated2×8 | -0.003145 [-0.006031, -0.000276] (95%) | Shared16 has lower loss; all three seeds agree |
| Ω: mismatch0→0.5 increment | +0.002618 [-0.002145, +0.007699] (97.5%) | Insufficient |
| Ω: mismatch0.5→1 increment | +0.001776 [-0.003354, +0.006920] (97.5%) | Insufficient/seed-unstable |

Sources: [主检验表](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/analysis/primary_training.csv), [六格共享代价表](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/analysis/semantic_format_six_cells.csv). The small positive Γ reflects a larger shared advantage for NEAR; it is not an isolation benefit for FAR. Mean NEAR shared-minus-Solo losses are−0.004761,−0.002143,−0.000367 across the three levels. FAR descriptive family intervals cross zero at every level. These do not establish universally harmful sharing.

**Clarification: shared gain differs from isolation gain.** Shared gain is matched-Solo minus shared loss. A researcher-requested posthoc paired-family readout gives NEAR0.002424 [−0.000068,0.004882], FAR0.000340 [−0.002076,0.002858], and NEAR−FAR0.002084 [−0.000057,0.004170] (descriptive95% intervals). All three seed contrasts are positive, but the interval still slightly crosses zero. This is directional evidence of greater shared gain for NEAR, not established negative transfer for FAR. It neither replaces registered Γ nor changes its0.01 threshold. [Supplementary readout](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/supplementary/shared_gain_clarification.json).

Initial M=0.053339 [0.046282,0.059684], with positive halves and subject-group contrasts, but its lower bound misses the registered0.05 threshold. Initial transfer J is positive at both scales (0.005130 and0.002777), yet cannot rescue the chain. At step64/full LR, K=0.000115 [−0.002419,0.002578]; incremental help relative to zero new gradient is−0.001107 [−0.002811,0.000588]. Full/half self-improvement gates fail. Sources: [起点方向](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/analysis/geometry.json), [起点迁移](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/analysis/transfer.json), [动态诊断](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/analysis/dynamic.json).

Capacity remains relevant: FAR D8−D16=0.003318 [0.001090,0.005599]; at equal total parameters, S32−D16=−0.004134 [−0.007503,−0.000680], both98.333% intervals. Topic isolation is not established as the better allocation; active-rank/optimization distinctions remain. Source: [容量对照](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/analysis/capacity.csv).

**Posthoc task-quality boundary:** all registered Solo loss-headroom gates pass, but S16 CONFIRM accuracy is24.44% [23.38%,25.52%]. All seven conditions score about24.28%–24.68%, with intervals covering25%; their mean NLLs1.422–1.438, including each95% lower bound, exceed the analytical uniform-letter reference ln4=1.386294. This does not establish content learning. Answer-format/probability calibration is a compatible explanation, not a directly measured decomposition. This check changes no registered threshold, endpoint or verdict. Source: [均匀字母基线对照](/data/250010109/MoE_Router/experiments/20260925_human_semantic_updates/full_v1/supplementary/uniform_letter_reference.csv).

**SAE remains untested.** No activation-distribution or predictive evidence was collected. Source inspection shows the frozen SAE observes last-block attention output, upstream of the adapted down projection; for a fixed input, this LoRA training cannot change that SAE input. Static prediction across examples remains possible but unmeasured.

Bounded meeting conclusion: this checkpoint/task/budget did not establish the registered semantic-distance or format-mismatch interference law; geometry did not establish the training mechanism, and content competence remains unestablished relative to a trivial reference. It therefore supplies no evidence yet for SAE-based parameter partitioning. This is not a universal no-interference claim.

**One AI-proposed next decision:** qualify a task/base-adaptation setting that demonstrably learns question content and generalizes beyond the uniform-letter reference before testing SAE prediction. If it still mainly reflects answer-format adaptation, stop using this carrier for semantic interference. No new experiment was submitted.

Completion:640 trajectories,270 dynamic snapshots,61 initial states and640 final evaluations; five jobs SUCCEEDED. Approximately25.3 minutes to training endpoints and27.5 minutes through analysis from submission;7.47 allocated GPU hours from platform start/end timestamps. Independent-rater agreement remains unmeasured;16 CONFIRM families per subject limit precision. No figures generated.
