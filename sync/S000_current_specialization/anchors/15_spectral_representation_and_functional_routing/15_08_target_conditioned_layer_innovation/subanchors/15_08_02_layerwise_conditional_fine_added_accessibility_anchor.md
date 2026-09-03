---
anchor_id: 15_08_02_layerwise_conditional_fine_added_accessibility
status: COMPLETED_PASS_LAYERS_24_28
canonical_language: en
chinese_companion: 15_08_02_layerwise_conditional_fine_added_accessibility_anchor_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
parent_line: 15_spectral_representation_and_functional_routing
execution_authority: APPROVED_AND_COMPLETED_FULL_FROZEN_ALL_LAYER_RUN
created: 2026-08-16
updated: 2026-08-16
---

# A15_08_02 Layerwise Conditional-Fine Added Accessibility

Parent definition: [A15_08 Target-Conditioned Layer Innovation](../15_08_target_conditioned_layer_innovation_anchor.md). Chinese companion: [Anchor](15_08_02_layerwise_conditional_fine_added_accessibility_anchor_cn.md). Draft execution contract: [E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_02_E01_layerwise_conditional_fine_added_accessibility/protocol.md).

## 1. Problem Definition

The final research program asks whether layer-local new information can be isolated in a low-dimensional space useful for later dispatch. This child Anchor owns only the prerequisite functional question:

> Across the eligible blocks of frozen Qwen3-8B, which same-token normalized attention transitions add held-out within-parent child accessibility beyond an identical old-state branch and target-independent equal-budget controls?

The target is **conditional-fine** classification: parent identity is known and the readout predicts one of eight children inside that parent. The prediction unit is one frozen decision-token occurrence. Added accessibility means held-out cross-entropy reduction under the registered linear readout family; it does not mean Shannon-information creation, knowledge storage, native model use, or Router utility.

The scientific population is every block in forward order; there is no preselected single-block smoke or best-layer screen. Block 25 contributes prior evidence that the extraction and metric can be made eligible on another target, not a prediction for this taxonomy. Block 1 is recorded but becomes structurally ineligible if its old state is constant at the frozen decision token; blocks 2--36 are the expected eligible set.

## 2. Physical Priors

1. **Exact same-layer subtraction.** At one token, block, and post-attention RMSNorm, the no-write state and actual state share one coordinate, so their difference is physically defined.
2. **Same-$X$ branch isolation.** Freezing one base logit vector from the same $X_\ell$ for every branch makes the true and control comparisons differ only in the added correction input.
3. **Function precedes compression.** A covariance spectrum, PCA direction, public basis, or cluster can describe update geometry but cannot establish that the update adds target accessibility. Low-rank analysis is admissible only after this Anchor passes.

## 3. Falsifiable Hypotheses

**H-CF — layer-local conditional-fine added accessibility.** At least one eligible block has a positive simultaneous lower bound for target-aligned residual-update gain beyond both duplicate-$X$ correction capacity and target-independent, same-budget residual-update mismatch banks. `AI_PROPOSAL`: use 64 mismatch banks, their q95, and familywise 95% simultaneous intervals to instantiate this judgment.

**Strongest rival R-CAP — correction capacity without new target-aligned input.** The second branch improves because the old-only readout is underfit or because any same-dimensional correction has extra capacity. R-CAP predicts that duplicate $X$ or sample-mismatched updates improve as much as the true update.

Other rivals are expression/template leakage, parent imbalance, an incapable target task, structurally constant old states, invalid tensor identity, and layer-dependent old-state headroom. Raw positive gain alone is compatible with all of these and is not a Pass.

The deeper-representation and low-rank hypotheses motivate the experiment but are not jointly adjudicated here. This Anchor does not require monotonic depth growth and registers no low-rank verdict.

## 4. Mathematical Model

At the frozen decision token in block $\ell$, let $h_\ell$ be the input residual, $a_\ell$ the attention write after output projection, and $N_\ell$ the same post-attention RMSNorm. Define

$$
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell.
$$

Using TRAIN-only grouped cross-fitting, fit the linear conditional mean and define

$$
R_{U,\ell}=U_\ell-\widehat m^U_\ell(X_\ell).
$$

For parent $p$, fit an old-state base readout $b_{\ell,p}$ and freeze its logits:

$$
s^0_{\ell,i}=b_{\ell,p(i)}(X_{\ell,i}).
$$

All added branches reuse exactly $s^0_{\ell,i}$. The true branch is

$$
s^{true}_{\ell,i}=s^0_{\ell,i}+q^{true}_{\ell,p(i)}(R_{U,\ell,i}),
$$

the staged capacity control is

$$
s^{dupX}_{\ell,i}=s^0_{\ell,i}+q^{dupX}_{\ell,p(i)}(X_{\ell,i}),
$$

and mismatch bank $b$ is

$$
s^{mis,b}_{\ell,i}=s^0_{\ell,i}+q^{mis,b}_{\ell,p(i)}(\widetilde R^{,b}_{U,\ell,i}),
$$

where $\widetilde R^{,b}_{U}$ is formed by a balanced sample-level reassignment inside each parent. It is not a fixed child-label renaming and contains no confirmation information. The duplicate-$X$ branch, the mismatch-bank construction, and the conservative maximum below are `AI_PROPOSAL` controls introduced to make the researcher's same-$X$ requirement falsifiable.

For branch $v$, define equal-parent held-out gain

$$
G^v_\ell=
\mathbb E_{conf}\left[
CE(s^0_\ell,Y)-CE(s^v_\ell,Y)
\right]
\quad\text{nats/example}.
$$

The conservative layerwise matched excess is

$$
T_\ell=G^{true}_\ell-
\max\left\{G^{dupX}_\ell,
q_{0.95,b}(G^{mis,b}_\ell)\right\}.
$$

The primary scientific output is the simultaneous-positive layer set

$$
\mathcal L^+=\left\{\ell:\operatorname{LCB}^{sim}_{0.95}(T_\ell)>0\right\}.
$$

Every eligible layer remains in the signed curve whether its estimate is positive, zero, or negative.

## 5. Computational Realization

1. Freeze local Qwen3-8B, tokenizer, prompt schema, final `Classification:` decision-token occurrence, conditional-fine taxonomy, and parent-specific eight-way ridge family.
2. Reuse the existing balanced TAX TRAIN/DEVELOPMENT expressions for all-layer fitting. `AI_PROPOSAL`: before scientific adjudication, generate and hash a new 640-example CONFIRMATION bank with 8 parents, 8 children per parent, and 10 expression/content families per child, all disjoint from TRAIN and DEVELOPMENT.
3. Fit residualizers and readouts with TRAIN only; use DEVELOPMENT only for the frozen ridge grid and diagnostics; open the new CONFIRMATION labels exactly once after every layer, control map, plot rule, and interval rule is frozen.
4. `AI_PROPOSAL`: give the true, duplicate-$X$, and each of 64 mismatch corrections the same input width, training rows, parent weighting, regularization grid, and selection budget. Each branch may choose its own DEVELOPMENT-optimal ridge value so controls are not artificially weakened.
5. After one explicit full-run approval, model-independent known cases and identity preflight run first; if they pass, the same execution directly extracts blocks 1--36 and fits eligible blocks 2--36 in forward order. The researcher explicitly waived a separate single-layer smoke on 2026-08-16.
6. `AI_PROPOSAL`: the primary figure has x=1--36, marks block 1 as NA if structurally ineligible, plots signed $T_\ell$ with simultaneous 95% intervals and a zero line, and highlights $\mathcal L^+$ without filtering the other layers.
7. No PCA, covariance eigensystem, public basis, clustering, minimal-rank retrieval, Router training, or expert evaluation is performed under this Anchor.

## 6. Minimal Falsification Tests

Subject to capability, data, identity, leakage, and record guards:

**Pass — `CONDITIONAL_FINE_ADDED_ACCESSIBILITY_FOUND`.** $\mathcal L^+$ is nonempty. Pass is layer-local: only members of $\mathcal L^+$ are admitted to a later low-rank study.

**Fail — `NO_REGISTERED_LAYER_EXCEEDS_MATCHED_CONTROLS`.** Every eligible layer has a simultaneous 95% upper bound for $T_\ell$ at or below zero. This closes the current linear residual-update definition for this taxonomy and model; it does not prove the absence of nonlinear or model-native information.

**Insufficient.** No layer passes but at least one decisive interval crosses zero; or any task-capability, branch-identity, data-independence, control-validity, extraction, or provenance guard fails.

Preflight has no scientific verdict. Any failed data, identity, known-case, fit, or control guard stops the all-layer run before confirmation; otherwise only the complete all-layer confirmation evaluation assigns Pass, Fail, or Insufficient.

## 7. Current Evidence

1. [A15_02_05](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) found reproducible conditional-fine residual structure but no stable fine-specific local-rank relocation beyond coarse structure. Geometry did not answer conditional novelty.
2. [A15_02_07 TAX](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md) found update readability without a strict same-$X$ conditional-gain gate. It motivates reusing the taxonomy, not inheriting a positive verdict.
3. [A15_07](../../15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md) proposed low-rank conditional-fine discriminant directions but was parked unrun because a functional novelty gate had to come first.
4. [A15_08_E04](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md) established eligible local added accessibility at block 25 for a controlled two-hop target and found that rank two retained only 33.24% of full point gain. It validates the measurement discipline, not this taxonomy hypothesis.
5. [A15_08_01_E02](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/summary.md) showed why a favorable depth interaction cannot replace signed absolute gain: the remote two-hop absolute gain declined. This successor therefore plots direct layerwise matched excess.

6. [A15_08_02_E01](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_02_E01_layerwise_conditional_fine_added_accessibility/summary.md) completed the frozen all-block confirmation run on 2026-08-16. Block 1 was structurally ineligible because the old state was constant at the registered decision token; blocks 2--36 entered one simultaneous correction. The registered verdict is `CONDITIONAL_FINE_ADDED_ACCESSIBILITY_FOUND`, with

$$
\mathcal L^+=\{24,28\}.
$$

Block 24 has $T_{24}=0.1087$ with simultaneous 95% interval $[0.0526,0.1649]$; block 28 has $T_{28}=0.0653$ with $[0.0239,0.1067]$. Block 25 has a positive point estimate $T_{25}=0.0693$ but its interval $[-0.0073,0.1460]$ crosses zero and is not admitted. Capability, identical-base-logit, 64-bank mismatch, tensor-identity, and reconstruction guards all passed.

## 8. Claim Boundary And Next Decision

The strongest possible claim is limited to one frozen model, one conditional-fine taxonomy, one decision-token occurrence, one same-layer normalized attention transition, and one registered linear readout family: a named set of layers adds held-out child accessibility beyond the identical old-state base and the registered target-independent equal-budget controls.

Even a Pass cannot establish monotonic deep improvement, representation low rank, a shared cross-layer space, semantic clustering, native MLP use, expert specialization, Router utility, causal necessity, or natural-language generality. Those require independent follow-ups.

**Exactly one next decision:** whether blocks 24 and 28, together with the subsequently confirmed rank-256 functional-retention spaces, should enter a separately frozen intervention or Router-utility experiment. This Anchor does not authorize that follow-up.

**Completion criterion: satisfied.** The frozen Protocol, all-layer tables, simultaneous intervals, primary figures, receipts, and artifact manifest are archived under [A15_08_02_E01](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_02_E01_layerwise_conditional_fine_added_accessibility).

**Resume action:** no rerun is required. Only blocks 24 and 28 may receive task-related interpretation under this experiment; block 25 remains unresolved and geometry alone cannot promote it to added conditional-fine information.
