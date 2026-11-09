# Anchor: representation mean, frequent features and expert selection

Version2026-10-19 v1.0. Faithful English companion to the received [Chinese design](15_23_mean_component_frequency_routing_anchor_cn.md); original seven sections retained, with no added scientific choice. Execution approval is recorded separately.

## 1. Purpose

The overall goal is effective expert specialization under explicit parameter and computation budgets. This round asks whether frequent features principally contribute the current-layer representation mean, whether long-run group-response differences partly explain raw routing concentration, and how subtracting that average changes input assignment. This is frozen statistical analysis and routing intervention, without new expert training or capacity claims. Experts retain the complete original input; centering only affects routing information.

## 2. Existing observations and gaps

The frozen candidate list hasfour frequency bands, each split into two relation subgroups. Earlier review raw routing left5/8 slots empty and gave the lowest band0% of positions. Ratio calibration left2/8 empty and gave it12.43%; low-feature macro receipt rose from0 to72.22%, a different denominator from position share. These facts do not yet identify true representation means or learning benefits. Group-size imbalance and unstable/singleton groups remain visible.

## 3. Intuition, hypotheses and rivals

H1: frequent-band average decoded contribution has a large signed projection onto the true representation mean. Report bias, residual and all bands. H2: with fixed lists and inputs, subtracting TRAIN mean group scores weakens persistent winners and changes low-feature receipt. This concerns routing baselines, not learning. Rivals include group size, coactivation, data distribution, within-band competition and shifted frozen-encoder inputs.

## 4. Three distinct operations

Representation centering subtracts the hidden-state TRAIN mean; score centering subtracts each band's/subgroup's average contribution; ratio calibration divides contribution by its average. They change encoder input, score baseline and score scale respectively. None is equivalent to deleting frequent atoms or a first singular direction.

## 5. Route

Freeze TRAIN definitions and lists; decompose the true mean; compare raw/ratio/subtractive scores with fixed encodings; perform reliable true-input re-encoding if possible; inspect actual receipt and text; then propose one next learning decision without starting it.

## 6. Interpretation branches

Strong mean correspondence plus changed receipt supports mean baselines as one source, not optimal learning. Strong correspondence without receipt improvement is insufficient to explain routing; inspect competition/coactivation. Weak correspondence with score changes supports a score-baseline explanation, not removal of common representations. Ratio benefit without subtractive benefit separates their hypotheses. Large re-encoding changes with degraded reconstruction are confounded by mismatch. Uniformer load without better target receipt does not establish useful specialization.

## 7. Delivery

A one-page Chinese report and a detailed record give the question, smallest supporting numbers, rivals and one proposed next decision; formulas, configuration, tables and limitations remain traceable. Keep explanations outside figures and do not join static routing evidence to historical learning results as a verified causal chain.
