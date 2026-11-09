# A17_03_E01: Sequential old-sensitive update results

[中文](summary_cn.md) · [Detailed](detailed.md) · [Protocol](protocol.md)

Engineering-complete and actual outputs registered. All six frozen case branches are NO_ORDINARY_FORGETTING;ordinary old CE improved in every case. The run's broad frozen descriptive verdict MIXED_OR_NON_SUPPORTING means the consistent-forgetting-protection criterion was not supported,not mixed forgetting signs. Interpretation below is AI-proposed;scientific mechanism/closure Unknown.

## 1. Purpose

The parent asks what produces shared-learning benefit/interference under finite resources. This round tests a sequential route:after one rule is learned,can avoiding estimated old-task-sensitive parameter directions reduce old deterioration while preserving opposite-rule acquisition? Earlier local transfer does not answer finite sequential retention. Forgetting is not assumed.

## 2. Model

Same three-word lists,different visible FIRST/LAST rules. Start from official Qwen3-0.6B Base;only final Attention o_proj trains. Old2000answers,then each ordinary/protected/random strategy restores the identical old state and learns new2000answers. Match actual per-step norms and presentation order. Plain SGD without momentum enforces parameter-direction constraints;do not pool with earlier AdamW results.

Fit60old-training per-example CE gradients,take16leading uncentered directions and freeze at the old endpoint. Sensitivity is unsigned,not harm. Its complement is not insensitive to every old record. Old deterioration D=L_A(W_final)−L_A(W_A),positive means worse old CE. New gain G=L_B(W_A)−L_B(W_final),positive means new acquisition. Accuracy and correct-versus-other-rule margins are separate readouts.

## 3. Hypothesis

Removing estimated old-sensitive update components may retain useful new learning while reducing forgetting. Rivals:no ordinary forgetting,generic step shrinkage/codimension,non-generalizing sensitivity and fixed-basis drift. Norm matching and equal-rank random restriction control the first generic strategy alternatives. Projection failure cannot prove all new acquisition requires these directions.

## 4. Conclusion

1. Net CE forgetting did not arise in this setting,so the proposed parameter-conflict explanation of forgetting has no observed CE phenomenon to explain. All six ordinary cases acquired new CE gain and further improved old CE. Direction means−0.078888/−0.082602nat per answer. This is not an engineering failure or a universal no-forgetting claim.
2. Effective new CE acquisition remained possible outside these16estimated directions. Protected gains exceeded ordinary in6/6cases,ratios1.1257–1.2600;equal-rank random was nearly ordinary. This is a bounded strategy/existence example,not all-old-insensitivity,functional partition or expert utility. Greater new gain without baseline CE forgetting does not confirm an anti-forgetting mechanism.
3. CE and mean margin gains did not guarantee accuracy retention. In LAST→FIRST,ordinary old accuracy changed+0.417pp versus protected−2.083pp;all three protected seeds lost old accuracy. The policy does not protect every old ability or dominate every metric. Average prediction probability and argmax choice differ.

| Order | New-learning strategy | Old ΔCE↓ | New CE gain↑ | Old Δaccuracy(pp) | New Δaccuracy(pp) |
| --- | --- | ---: | ---: | ---: | ---: |
| FIRST→LAST | ordinary | -0.078888 | 0.120197 | -1.083 | +5.417 |
| FIRST→LAST | protected | -0.087984 | 0.142648 | -1.167 | +4.167 |
| FIRST→LAST | random | -0.078887 | 0.120197 | -1.083 | +5.417 |
| LAST→FIRST | ordinary | -0.082602 | 0.135452 | +0.417 | +4.833 |
| LAST→FIRST | protected | -0.084757 | 0.156123 | -2.083 | +4.000 |
| LAST→FIRST | random | -0.082602 | 0.135452 | +0.417 | +4.833 |


Equal-weight three-seed means;CE in nats/answer,accuracy in percentage points. Negative old delta is further improvement;positive new gain is acquisition. Keep orders separate;only three independent training seeds. Exposed dev,not blind confirmation.

## 5. Analysis

Same old state,batches and norm schedule isolate this direction-restriction policy. Random≈ordinary versus sensitivity-based changes show direction choice matters within this control,but direction fitting/rescaling jointly define the treatment. Extra subspace computation is not FLOPs-matched;no systems or MoE benefit claim.

Fitted energy80.9%–83.6%;first20independent old dev per-example gradient energy coverage51.6%–61.3%,random≈0.00063%–0.00080%. At norm.01,sensitive first-vector ±perturbation old-CE RMS was176.9–528.4times random. This qualifies local old-CE association,not all functions,all dev content or every later sensitivity. Remaining old sensitivities,finite effects and basis drift remain.

Continuity:the old stage itself improved opposite-rule CE≈.266–.314;ordinary opposite training further improved old CE,extending A17 local help. Frequency A17_02 showed larger same-rule marginal CE gains but positive different-rule net CE gains;it did not establish net conflict. Paired-margin follow-up found6declines among18recipient CE helps. This round shows finite sequential meanCE/meanmargin/accuracy can also disagree. Histories,optimizers and panels differ;no pooled effect estimate.

Separate order-new/combination-new ordinary FIRST→LAST old deltas−.081403/−.076372,new gains+.120012/+.120382;LAST→FIRST old−.082220/−.082985,new+.131583/+.139321. Protected FIRST→LAST old−.088342/−.087627,new+.139370/+.145926;LAST→FIRST old−.087017/−.082497,new+.152564/+.159682. Each panel200answers/rule;combined equal weights. All old-training groups actually exposed. Detailed preserves accuracy/margins and exact panel tables.

A concrete discrepancy:seed29protected LAST→FIRST lost14previously correct old answers and recovered5,net−9/400(−2.25pp),while330/400old CE values improved and average old CE fell.080614. This is a prediction-level observation,not aggregation error.

Job pt-ubjfxl7c SUCCEEDED:Smoke960training answers;Full6old+18new trajectories,48000answers/2400steps. Four Smoke/resume/Full workers PASS;22input/426output hashes checked;exact presentation/token audit. Maximum norm mismatch3.73e-7,constraint leakage1.52e-6. Registered44Smoke/114Full saved states in40checkpoint families plus one analysis family. Full final external continuation NOT_CHECKED;Smoke qualifies the same updater only.

AI-proposed update:forgetting is a conditional entry point requiring observed deterioration in the intended metric. One could next explain CE-versus-accuracy direction effects,but no intrinsic incompatibility or expert partition is established. Researcher decides whether this task pair suffices to stop the forgetting route or which measured property warrants a distinguishing next comparison. No new experiment,automatic Focus redirection or closure.
