# A17 E03 supplement: paired-rule answer margin

[中文](summary_cn.md) · [Detailed](detailed.md) · [Protocol](protocol.md)

Engineering completion verified; registered descriptive verdict `DESCRIPTIVE_HETEROGENEOUS_OR_INSUFFICIENT`. Scientific interpretation below is an AI-proposed bounded reading, awaiting researcher adjudication; no question closure.

## Purpose

The parent asks what benefits and interference shared learning produces under finite parameters, data and compute, and which effects may require differentiated processing. This round checks one link: does observed cross-rule loss help also improve the correct answer relative to the other rule's answer? It narrows the meaning of help without deciding model sharing versus separation.

## Model

The same three-word list receives a visible FIRST or LAST instruction. The exact saved Qwen3-0.6B Base state is held fixed; only a saved actual layer27 Attention o_proj increment is applied, then restored. Read the complete FP32 model before/after on independent paired development lists. No LM or SAE training occurred.

For each list, m_FIRST is log p(first|FIRST) minus log p(last|FIRST); m_LAST reverses the candidates under LAST. Their sum S measures how the two prompts separate relative first/last preference. A positive recipient Δm is a local relative-answer improvement, not automatically a top1 improvement. Log probability differences equal logit differences. All losses/margins use natural logarithms.

## Hypothesis

The candidate inference is that lower recipient loss means better relative choice under its rule. The frozen operational test requires source-effective, recipient-helping updates to improve recipient pair margin consistently in the primary slice. Rivals: answer-pool mass increases without relative choice improving; common positional bias changes both prompts; beating the other-rule answer still fails against the middle word or full vocabulary. Report both directional margins, S, CE, list/full accuracy and conditional20 CE; S cannot substitute for recipient improvement.

## Conclusion

1. The inference from loss help to consistent pair-margin transfer needs narrowing. In the primary early-state slice, all18 updates improved independent own-rule CE and recipient CE, but12 improved recipient pair margin and6 worsened it. The frozen consistency criterion is not met. These observed counterexamples refute the every-helpful-update inference in the primary set; consistent transfer was not established. They preserve observed loss help and do not negate every form of rule-selection ability.
2. Average effects contain more than a uniform answer-pool lift. Both direction averages are positive, and S increased in18/18 conditions, mean+0.003115. Conditional20 CE decreased on average in both directions (17/18 individual conditions improved). Pure uniform pool lift and identical additive positional bias across prompts cannot alone produce positive S. This does not identify an internal rule algorithm or show that each recipient improves.
3. This round excludes an overstrong interpretation without locating common or differentiated functions. Effects are small and dependent on source direction/batch/state. Accuracy changes averaged −0.370 percentage points for FIRST→LAST and +0.556 for LAST→FIRST; there is no consistent bidirectional accuracy gain. These are exposed-dev local interventions across three training seeds, not blind confirmation, natural-text transfer or expert necessity.

| Source → recipient | ΔCE↓ | Δpair margin↑ | Improved/worsened | Δaccuracy (pp) |
| --- | ---: | ---: | ---: | ---: |
| FIRST → LAST | -0.002282 | 0.000545 | 4/9 · 5/9 | -0.370 |
| LAST → FIRST | -0.002436 | 0.000940 | 8/9 · 1/9 | +0.556 |


Each row averages three training seeds equally and three previously heldout source batches per seed; all use update16, saved eta0.01, multiplier1, and the same60 paired lists. Negative ΔCE means less loss; positive Δmargin means better correct-versus-other-rule preference. Improved/worsened counts refer to nine source updates, not nine independent training replications.

## Analysis

Why this comparison: each update starts from the same saved state and is compared with no update on the same lists, independent of source content groups. It identifies the specified update's local prediction consequence. Correct-answer loss checks probability gain; pair margin checks gain relative to the other-rule answer. A uniform answer-pool lift can change the former but not the latter, separating that rival. Positive means, consistent batch effects and accuracy gains answer different questions and cannot substitute for one another.

Completion: job pt-hz9kc697 succeeded on four H100 reserved. Smoke8/8 conditions and Full280/280 conditions at seven unique states passed; all frozen input330 and payload642 hashes matched. Independent arithmetic replay of280 endpoint files and seven baselines differed by at most1.43e-14; deterministic no-op drift was0. The Base initial state is deduplicated, not three seeds. Full outputs are registered as `representation_a17_paired_rule_margin_20261010t141041z` with current strict access evidence.

A concrete counterexample is seed29, FIRST source batch2: recipient LAST CE fell0.710992090→0.709480082 while its pair margin fell0.993702888→0.992825667; accuracy stayed47/60. The model increased correct-answer probability without improving its advantage over the competing FIRST answer. This answers the proposed falsifier directly.

The exact CE decomposition is ΔCE=Δconditional20CE−Δlog(pool probability). FIRST→LAST averages are−0.002282=−0.001379−0.000903; LAST→FIRST averages are−0.002436=−0.001464−0.000972. Thus answer-pool mass and within-pool prediction both changed. This is a probability-accounting identity, not a causal mediation decomposition. Conditional20 improvement can coexist with worse first/last preference because the other18 candidate words also affect the conditional normalizer.

Novelty panels differ. Nominal order-new versus combination-new FIRST→LAST mean Δmargin is+0.001721 versus−0.000043; LAST→FIRST is−0.001119 versus+0.001969. The60-list merge weights20 order-new and40 combination-new pairs. Actual exposure reclassification yields 8/10/6 seen-group-unseen-order pairs and52/50/54 unseen-group pairs for seeds29/43/71, respectively; the small actual seen-group panel cannot support a broad generalization comparison. Detailed preserves both definitions and all separate/combined values.

Sensitivity, not primary rescue: Base had6/6 source-effective/helping/margin-improving updates; update100 had7 margin-improving,5 margin-worsening,4 without resolved recipient help and2 ineffective sources. No new measurement was run to obtain these summaries; all derive from frozen endpoints. The knowledge update is a narrower meaning of shared help, together with local conditional-preference evidence; no common/differentiated function was identified. AI suggestion: first decide whether this bounded answer suffices to stop supplementary readouts. Further mechanism work needs a researcher-selected unresolved rival whose answer changes a judgment, not merely another available metric. The next scientific question, mechanism and architecture decision remain Unknown; no new run is authorized.
