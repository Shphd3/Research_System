# 1012 meeting: from shared loss benefits to conditional rule learning

[Chinese reading version](meeting_brief_conditional_mapping_cn.md)

The bounded training and analysis are complete. Round one distinguished correct-answer loss from answer competition. Round two manipulated conditional mappings, but did not qualify old-task acquisition. It therefore cannot determine whether reversal damages an acquired old rule. This brief derives from the [second-round Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary.md); it grants no new scientific authority.

## 1. Purpose

Our root question is when learning new data helps another condition's predictions, when it incurs a learning cost, and which prediction requirements warrant sharing or differentiated treatment.

Round one holds tasks fixed and intervenes on update components. Round two holds content and exposure fixed and changes the conditional answer mapping. The adopted merger is one mapping intervention with diagnostic output readers: the relation hypothesis supplies consistent/reversed labels, while the reuse-versus-conditional-correction hypothesis supplies command and mode comparisons.

## 2. Model

The carrier is the registered Qwen3-0.6B Base. Only its final attention output matrix \(W\), of shape \(1024\times2048\), is trainable. All upstream weights are frozen, so its input \(a(x)\) is fixed for a given input and the projection-output displacement is exactly \(\Delta W a(x)\). Frozen downstream MLP, normalization and head computations remain nonlinear; prediction changes are measured.

Input contains a visible mode, a neutral command and a three-word list. For Red Blue Green:

| Condition | Command 甲 target | Command 乙 target |
|---|---|---|
| Old mode one | Red, FIRST | Green, LAST |
| Consistent new mode two | Red, FIRST | Green, LAST |
| Reversed new mode two | Green, LAST | Red, FIRST |

The new worlds are separate runs with identical prefixes and matched target marginals. Each world's full inputs have consistent labels. Visible mode makes joint satisfaction possible in principle.

Each of three training-order seeds trains the old mode for 240 updates, then branches from its identical old endpoint into 240 consistent and 240 reversed updates. Each update contains 20 valid answer targets; loss is answer-only CE. Joint reversed training adds old supervision and has half the primary new exposure; it is a feasibility witness, not a matched-exposure winner comparison. Equal-norm immediate updates constrain the local update-size rival.

Separate heldout panels contain unseen permutations of familiar unordered triples and entirely unseen unordered triples. Both use familiar vocabulary. Report them separately and then equally combined. Both positions are already supervised in the old mode, so missing-position completion is not tested.

## 3. Hypothesis

Reversing the new command-to-position relation may reduce old correct-versus-opposite answer advantage compared with preserving it. A retention interpretation requires an acquired old conditional mapping.

Rivals include increased candidate-word probability, unequal task difficulty or initial competence, a trainable tensor poorly suited to mode-command learning, different update scales, and different optimization trajectories. Controls constrain parts of these explanations, rather than automatically removing them.

## 4. Conclusion

Smoke job pt-jw3bhrzi and Full job pt-qs6ndgat succeeded on four reserved H100s. All specified training, saved-state registration and independent analysis completed. The descriptive result is insufficient old-mapping acquisition.

Old TEST accuracy rose from 34.75% to 49.75%, but old DEV accuracy by command and panel was only 33%–54%. All three seeds failed the frozen 80% acquisition criterion.

| Old TEST measure, equally pooled seeds and panels | Old endpoint | After consistent | After reversed |
|---|---:|---:|---:|
| Correct-token CE, nat | 1.12044 | 1.03860 | 1.04174 |
| Full-vocabulary accuracy | 49.75% | 49.71% | 49.96% |
| Gold endpoint versus opposite margin, nat | 0.04572 | 0.06428 | 0.05911 |

Reversal gave 0.005165 nat less margin improvement. Its unseen-order and unseen-combination effects were −0.001529 and −0.008802 nat. All seed effects were negative, but the combined magnitude was below the pre-run 0.01 nat descriptive convention. Both branches improved mean old CE and margin. No mean net harm is established, and the failed acquisition premise blocks learned-rule retention claims.

New TEST accuracy remained low: 46.75%→47.21% consistent and 46.25%→48.17% reversed. No branch reached the DEV comparable-skill point. Joint old/new TEST accuracy was 50.21%/47.50%; feasibility remains Unknown, not disproved capacity.

Reversed new CE fell by 0.109310 nat: 0.107779 from list-candidate access and 0.001531 from within-list selection. Its correct endpoint margin changed from −0.005240 to −0.005931. Candidate concentration improved without established conditional reversal.

## 5. Analysis

The logical chain is: root sharing question → distinguish candidate probability from correct selection → intervene on update components → manipulate conditional mapping → qualify old conditional learning → test relation effects and update mechanism → consider an independent shared/separate parameter comparison. The present run stops the acquired-rule interpretation at the qualification step.

The [prior trajectory result](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_03_old_task_sensitive_update/A17_03_E03_trajectory_mechanism/summary.md) remains valid: ordinary/restricted 100-step updates repaired 72/36 old errors, and 24/36 intermediate same-state comparisons showed less old-error margin improvement under restriction. Order and state heterogeneity prevented a uniform whole-trajectory mechanism.

For list probability \(P_3=\sum_{w\in\mathrm{list}}p(w\mid x)\), correct-token CE exactly equals

\[
-\log p(y\mid x)=-\log P_3-\log\frac{p(y\mid x)}{P_3}.
\]

The terms measure list access and correct selection within the list. Compute each per input before averaging. Old acquisition CE fell 1.325015 nat, with 1.276094 from access and 0.048921 from selection. The 96.3% share is arithmetic bookkeeping, not an identified causal percentage. Continuing consistent learning changed old CE by −0.086275+0.004429; reversed learning by −0.085028+0.006319. Access improved while within-list selection slightly worsened.

A post-hoc illustrative old input is mode one, command 甲, list 马 花 猫, target 马. In seed71's reversed branch, p(马) rose 46.001%→47.285% and its CE improved 0.776499→0.748983. The competitor p(猫) rose more, 42.347%→47.471%, and the argmax became incorrect. This selected example explains the distinction; it is not population evidence of net harm.

Supplementary exact algebra also limits the mechanism claim. At the same state and paired new-mode inputs, let \(L_s,L_r\) be consistent/reversed CE, \(s_c=\log p(L_3\mid c)-\log p(L_1\mid c)\), and \(a_2=\mathbb E_L[(s_{乙}-s_{甲})/2]\). Then

\[
L_r-L_s=a_2,\quad G=(L_s+L_r)/2,\quad
g_s=\nabla_WG-\tfrac12\nabla_Wa_2,\quad
g_r=\nabla_WG+\tfrac12\nabla_Wa_2.
\]

Label reversal changes one term's sign, not the entire gradient. \(G\) contains endpoint access and endpoint balance; it is not an internal shared module or pure candidate adaptation. The [same-state identity check](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/paired_loss_identity.json) passed 72 cells with maximum error \(5.59\times10^{-9}\) nat. This checks an identity, not a mechanism.

Component gradient norms, angles and finite interventions remain unmeasured. Small \(a_2\) does not imply a small gradient. If actual increments are \(d_s=-\eta_sg_s,d_r=-\eta_rg_r\), clipping or norm matching gives

\[
d_r-d_s=(\eta_s-\eta_r)\nabla_WG
-\frac{\eta_s+\eta_r}{2}\nabla_Wa_2.
\]

Equal increment norms need not give equal effective scales. Different trained-state losses cannot be substituted into the same-state identity.

AI suggests a bounded DEV-only old-acquisition diagnosis, first on training inputs and then on both unseen panels. If training selection has not formed, evaluate a predeclared finite budget ladder; if training succeeds but heldout selection fails, investigate coverage and generalization. Exposed TEST must not choose future budgets; new confirmation requires a fresh heldout set. This suggestion activates no additional experiment.

The meeting message is: shared loss improvement can coexist with poor rule selection. Round one localized answer competition; round two revealed that the neutral conditional mapping was not yet acquired in this carrier. Establish reliable conditional selection before attributing transfer to reusable rules or recommending separated experts.

Evidence: [registered results](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/results.json) · [Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/detailed.md) · [Focus](/data/250010109/Research_System/Projects/from-attention-to-search/main/focus/focus_conditional_mapping_transfer.md).
