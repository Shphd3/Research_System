---
experiment_id: A15_08_07_E01_clinc150_layerwise_conditional_intent_added_accessibility
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_AND_REPORT_DRAFT
experiment_role: robustness_check
primary_anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md
dataset_anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_semantic_conditioned_functional_subspace_anchor.md
created: 2026-08-19
updated: 2026-08-19
---

# Protocol: CLINC150 Layerwise Conditional-Intent Added Accessibility

## 0. Approval Snapshot

| Item | Frozen candidate |
| --- | --- |
| Document status | `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_AND_REPORT_DRAFT` |
| Approval status | A--G were explicitly approved by dxy on 2026-08-19; implementation, smoke, full run, result rendering, canonical result records, and an AI-authored report draft are authorized |
| One uncertainty | On CLINC150, where does matched added accessibility emerge across depth, and at what PCA dimension does each admitted layer retain 80% or 90% of its full-$R_U$ gain? |
| Experiment role | Robustness check of the prior all-layer same-$X$ experiment |
| Treatment | CLINC150 in-scope utterances, with known domain and 15-way intent prediction inside that domain |
| Prior reference | Synthetic taxonomy confirmed blocks 24 and 28 under the registered linear protocol |
| Primary outputs | (1) the complete signed CLINC150 curve $T_\ell$ and positive set $\mathcal L^+_{\mathrm{CLINC}}$; (2) all-layer PCA functional-retention analysis and $r_{G80},r_{G90}$ for admitted layers |
| Changed scientific variable | Dataset and its conditional-fine label system |
| Held fixed | Frozen Qwen3-8B, decision-token site, $X/Z/U/R_U$ objects, TRAIN-only residualization, same-$X$ additive correction family, duplicate-$X$ and mismatch controls, layerwise multiplicity rule, and figure semantics |
| Required figures | Figure 1 reproduces cumulative $X_\ell/Z_\ell$ readability plus per-block $T_\ell$; Figure 2 reports PCA gain-versus-rank with the $G_{80}$ and $G_{90}$ thresholds |
| Stage-1 Pass | At least one eligible CLINC150 block has simultaneous 95% LCB$(T_\ell)>0$ |
| Stage-1 Fail | Every eligible block has simultaneous 95% UCB$(T_\ell)\le0$ |
| Stage-2 Pass | For an admitted layer, a registered PCA rank exceeds both $\eta G_{full}$ and the same-rank Haar q95 with simultaneous 95% LCB $>0$, for $\eta=0.8$ and/or $0.9$ |
| Insufficient | A decisive interval crosses zero; no layer is functionally admitted for Stage 2; or any data/object/control/capability guard fails |
| Cannot claim | Information-theoretic novelty, model understanding, nonlinear novelty, intrinsically low-rank representation, native model use, expert utility, or Router improvement |

This is one ordered experiment with two gates. Stage 1 locates functionally admitted emergence layers. Stage 2 computes PCA and equal-rank random controls for every eligible layer under a frozen all-layer-by-rank family, but assigns formal $G_{80}/G_{90}$ functional-rank conclusions only to Stage-1-admitted layers. Public-parameter bases and Router training remain out of scope.

## 1. Terminology And Definitions

- **Known domain:** evaluation metadata selects one of ten CLINC150 domains; the model does not predict the domain in the primary task.
- **Fine intent:** one of fifteen intent labels inside the known domain.
- **Cumulative accessibility:** a linear head's held-out 15-way accuracy from $X_\ell$ or $Z_\ell$. It describes what is readable by that depth and is not a per-block novelty metric.
- **Matched added accessibility:** the held-out cross-entropy improvement supplied by the correctly paired residual update after subtracting the stronger registered capacity/null control.
- **Emergence layer:** only a block in $\mathcal L^+_{\mathrm{CLINC}}$; a high $Z_\ell$ accuracy, positive point estimate, PCA peak, or visually late rise is not sufficient.
- **Full gain $G_{\ell,full}$:** held-out CE reduction from adding the correctly paired, unrestricted $R_{U,\ell}$ correction to the frozen $X_\ell$ base. It becomes a valid retention reference only when Stage 1 admits that layer.
- **$G_{80}$ and $G_{90}$:** the two target gains $0.8G_{\ell,full}$ and $0.9G_{\ell,full}$, not covariance-energy thresholds.
- **Functional ranks $r_{G80}$ and $r_{G90}$:** the smallest registered PCA ranks that exceed the corresponding target and the equal-rank Haar q95 under simultaneous inference.
- **`NA`:** the functional rank is undefined because the layer's full $R_U$ did not first establish matched added accessibility. `NA` is not a failed rank sweep.
- **`>512`:** full $R_U$ was admitted, but no tested PCA rank through 512 confirmed the requested retention threshold. This is different from `NA`.

For block $\ell$, with pre-Attention residual $h_\ell$, Attention write $a_\ell$, and the same post-Attention RMSNorm $N_\ell$,

$$
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell,
$$

$$
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{\mathrm{lin}}[U_\ell\mid X_\ell].
$$

$R_U$ is only the update unexplained by the registered TRAIN-fitted linear family. Its scientific meaning is decided by the held-out branch comparison below.

## 2. Anchor Alignment

The prior all-layer experiment established a bounded synthetic-taxonomy result: blocks 24 and 28 added within-parent child accessibility; other layers were not thereby proved negative. The CLINC150 experiment already completed at blocks 24 and 28 found that neither selected layer's full $R_U$ exceeded its same-$X$ null envelope. Because that experiment did not evaluate all blocks, it cannot identify whether the positive layer moved elsewhere.

This experiment therefore asks one ordered question: **under the same registered layerwise functional definition, where, if anywhere, does added domain-conditioned intent accessibility occur on CLINC150, and how many PCA coordinates retain 80% or 90% of the admitted full-update gain?** Geometry and function remain separate: covariance $r_{80}^{var}/r_{90}^{var}$ are descriptive, while $r_{G80}/r_{G90}$ require held-out functional admission.

## 3. Tested Hypothesis And Strongest Rival

**H-CLINC:** at least one frozen-model block supplies correctly paired $R_U$ information that improves held-out within-domain intent prediction beyond duplicate-$X$ capacity and a same-domain mismatch bank.

**R-CAP:** any apparent improvement comes from giving an underfit $X$ baseline a second correction head, or from generic update geometry unrelated to the current utterance. Under R-CAP, duplicate-$X$ or mismatched $R_U$ performs as well as the correctly paired update.

**H-PCA-FUNC:** for at least one Stage-1-admitted layer, a PCA projection much smaller than width 4096 retains a registered fraction of the full-$R_U$ gain and exceeds equal-rank random projections.

**R-VAR:** PCA only captures large update variance; those directions need not preserve intent-discriminative gain. Under this rival, PCA may explain substantial covariance energy while failing $G_{80}/G_{90}$ or failing to beat Haar.

The layer-location comparison is secondary:

$$
\mathcal L^+_D=
\{\ell:\operatorname{LCB}^{sim}_{0.95}(T^D_\ell)>0\}.
$$

The old reference is $\mathcal L^+_{\mathrm{TAX}}=\{24,28\}$. A different observed set is reported descriptively. A formal cross-dataset profile difference additionally requires a simultaneous interval for the normalized difference to exclude zero; non-confirmation on one dataset alone is not evidence of absence.

## 4. Data Construction And Provenance

Use the already audited CLINC150 in-scope corpus and mapping from the frozen A15_08_06 data contract:

- source commit: `828f8093932c8fe6ca7936c3d2e52903b1c523de`;
- data SHA-256: `36923c3705a59e08fe9c3883d8bc2dd966ef93e22cb78ac41171782a698d56e0`;
- 10 domains, 15 intents per domain;
- 100/20/30 TRAIN/validation/test utterances per intent;
- 15,000/3,000/4,500 rows, 22,500 total;
- all OOS records excluded;
- official test is primary; a collision-excluded sensitivity removes the two previously identified test-involving duplicate rows.

The existing official TEST was already viewed for blocks 24 and 28 in A15_08_06. Therefore this run is a **registered robustness profile**, not a pristine new-dataset confirmation. No layer, control, axis, or inference rule may be selected from the remaining layer results.

The primary task fits ten separate 15-way intent heads. Every domain contributes equal weight regardless of utterance count. TRAIN fits all transforms and heads; validation selects ridge penalties; TEST evaluates the frozen all-layer design once.

## 5. Learning Task, Model, And Objects

- Model: frozen local Qwen3-8B, expected 36 blocks and hidden width 4096; implementation must verify both.
- Input wrapper: use the already frozen CLINC150 wrapper and tokenizer from A15_08_06 so the new run changes layer coverage rather than silently changing the dataset realization.
- Decision token: the final non-padding token of the literal `Category:` suffix, with the same occurrence used at every block.
- Blocks: record 1--36. A structurally constant block-1 $X_1$ is marked `STRUCTURALLY_INELIGIBLE`; it is never forced through standardization.
- Saved objects per row and block: $h_\ell,a_\ell,X_\ell,Z_\ell,U_\ell$, native MLP input, sample ID, domain, intent, token ID, and token position.
- Required identities: $U=Z-X$, native MLP input equals $Z$, Attention-write replay equals $a$, repeated-batch determinism, finite values, and exact sample/token ordering.

The base language model is never trained. All readouts are linear ridge models with centered one-hot intent targets.

### 5.1 Mandatory retraining on the new dataset

No learned TAX component and no fitted A15_08_06 coefficient may be reused. From CLINC150 TRAIN, refit from scratch for every eligible layer:

1. $X/U/R_U$ means, scales, and zero-variance masks;
2. the label-free but distribution-dependent affine ridge residualizer $X_\ell\rightarrow U_\ell$;
3. the $X_\ell$ and $Z_\ell$ capability heads;
4. the frozen-$X$ base, true full-$R_U$, duplicate-$X$, and all mismatch correction heads;
5. each layer's PCA basis, covariance spectrum, equal-rank Haar bases, and every rank-specific correction head.

Validation reselects every permitted ridge coefficient on CLINC150. Only the frozen Qwen3-8B parameters, tokenizer, prompt/token definition, mathematical object, rank grid, controls, and analysis rule are inherited. This requirement prevents a TAX-trained residualizer, PCA basis, or classifier from being mistaken for a property of the new task.

## 6. Conditions And Held-Fixed Comparison

For each block and domain, fit a TRAIN-only $X$ base and freeze its logits:

$$
s^0_{\ell,i}=b_{\ell,D_i}(X_{\ell,i}).
$$

Fit equal-budget additive corrections while keeping $s^0$ bit-identical:

$$
s^{true}=s^0+q^{true}(R_U),\qquad
s^{dupX}=s^0+q^{dupX}(X),
$$

$$
s^{mis,b}=s^0+q^{mis,b}(\widetilde R_U^{\,b}),\quad b=1,\ldots,64.
$$

Mismatch maps are one-to-one permutations inside each domain, use every source row once, map no row to itself, and balance source intents within each destination intent. TRAIN, validation, and TEST maps are independently generated from frozen IDs and seeds. Each branch receives the same row count, target, ridge grid, selection budget, and domain weighting; each may select its own validation-optimal penalty.

For the upper figure panel, independently fit matched linear capability heads from $X_\ell$ and $Z_\ell$ and report equal-domain TEST macro accuracy. These heads are descriptive and cannot define emergence.

### 6.1 PCA and low-dimensional conditions

For every eligible layer, center CLINC150 TRAIN $R_{U,\ell}$ and learn one layer-specific PCA basis pooled over the ten domains. Freeze

$$
r\in\{1,2,4,8,16,32,64,128,256,512\}.
$$

At each rank, compare:

1. `pca_head_r`: the first $r$ TRAIN PCA directions;
2. `haar_r_s`: 64 nested equal-rank Haar random subspaces, frozen from TRAIN-side seeds;
3. `full_ru`: unrestricted $R_U$ with the identical base logits, target, ridge grid, weighting, and evaluation code.

For the geometric diagnostic, report cumulative PCA variance, $r_{80}^{var}$, $r_{90}^{var}$, entropy effective rank, and frozen TRAIN-projector capture on validation/TEST. These values describe the update cloud and cannot establish functional low rank.

For the functional test, refit a correction head from $R_UP_r$ at every layer and rank. All layer-by-rank fits and plot schemas are frozen before TEST. Stage-1 layer admission controls interpretation rather than deciding which PCA fits are computed, avoiding a post-TEST layer-selection loop.

## 7. Primary Metric And Frozen Analysis

For branch $v$, define per-example held-out gain in nats/example:

$$
g^v_{\ell,i}=CE(s^0_{\ell,i},Y_i)-CE(s^v_{\ell,i},Y_i).
$$

Average utterances equally inside intent, intents equally inside domain, and domains equally overall to obtain $G^v_\ell$. The matched excess is

$$
T_\ell=G^{true}_\ell-
\max\{G^{dupX}_\ell,q_{0.95,b}(G^{mis,b}_\ell)\}.
$$

Use 2,000 paired hierarchical bootstrap draws: resample domains, intents inside domains, and utterances inside intents; reuse the same draw across all blocks and branches. Recompute the mismatch q95 and control maximum inside every draw. Use a max-statistic across every eligible block for two-sided familywise 95% intervals.

Primary verdict:

$$
\mathcal L^+_{\mathrm{CLINC}}
=\{\ell:\operatorname{LCB}^{sim}_{0.95}(T_\ell)>0\}.
$$

### 7.1 $G_{80}/G_{90}$ functional retention

Let $G_{\ell,r}^{PCA}$ be the equal-domain held-out CE gain from the rank-$r$ PCA correction and $G_{\ell,r}^{Haar,s}$ the corresponding gain for random seed $s$. For $\eta\in\{0.8,0.9\}$ define

$$
G_{\eta,\ell}=\eta G_{\ell,full},
$$

$$
D^{(\eta)}_{\ell,r}
=G_{\ell,r}^{PCA}
-\max\left\{
\eta G_{\ell,full},
q_{0.95,s}(G_{\ell,r}^{Haar,s})
\right\}.
$$

The confirmed functional rank is

$$
r_{G\eta,\ell}
=\min\left\{r:
\operatorname{LCB}^{sim}_{0.95}
\bigl(D^{(\eta)}_{\ell,r}\bigr)>0
\right\}.
$$

The simultaneous family contains every eligible layer, registered rank, and both $\eta$ thresholds. The control maximum is recomputed inside each hierarchical bootstrap draw. A projected gain larger than full gain is retained numerically but interpreted as possible projection/refitting regularization, not new information.

Typed output for each layer and threshold:

- `r=<registered rank>`: Stage 1 admitted the layer and that rank passed the threshold plus Haar control;
- `UNCERTAIN`: Stage 1 admitted the layer and a point estimate crossed the target, but the simultaneous interval did not;
- `>512`: Stage 1 admitted the layer, but no registered rank through 512 passed;
- `NA_NO_FULL_ADMISSION`: Stage 1 did not admit full $R_U$, so $0.8G_{full}$ and $0.9G_{full}$ are not valid functional-retention references.

`NA_NO_FULL_ADMISSION` must be explained in the report as follows: the numerator curve may still be plotted descriptively, but asking what fraction of an unadmitted full effect it retains is scientifically undefined. It does not mean PCA was tested and failed, and it cannot be converted to zero rank, infinite rank, or “high rank.”

For the secondary old-versus-new comparison, report

$$
\Delta_\ell=
\frac{T^{\mathrm{CLINC}}_\ell}{\log 15}
-
\frac{T^{\mathrm{TAX}}_\ell}{\log 8}.
$$

Independent hierarchical draws from the two datasets form simultaneous 95% intervals for $\Delta_\ell$. Division by balanced-label entropy makes the scale less sensitive to 15-way versus 8-way prediction, but it does not turn the comparison into a causal dataset intervention.

Typed cross-dataset reading:

- `PROFILE_DIFFERENCE_SUPPORTED`: at least one simultaneous interval for $\Delta_\ell$ excludes zero;
- `SAME_CONFIRMED_PATTERN`: CLINC confirms exactly blocks 24 and 28 and no $\Delta_\ell$ interval excludes zero;
- `PROFILE_SHIFT_INSUFFICIENT`: confirmed sets differ but no $\Delta_\ell$ interval excludes zero;
- `NO_CLINC_LAYER_CONFIRMED`: $\mathcal L^+_{\mathrm{CLINC}}=\varnothing$; this is a scientific Fail only if every simultaneous UCB is non-positive, otherwise it is Insufficient.

## 8. Required Figures And Tables

### Figure 1: exact reproduction of the prior conclusion figure

Two vertically aligned panels with a shared x-axis of Transformer blocks 1--36:

1. **Upper panel:** equal-domain TEST intent accuracy (%) for $X_\ell$ and $Z_\ell$. This is cumulative linear readability.
2. **Lower panel:** signed $T_\ell$ in nats/example with simultaneous 95% intervals and a zero line. Highlight only newly confirmed CLINC layers; mark prior TAX blocks 24/28 with a separate hollow reference symbol.

The caption must say: cumulative readability can rise even when few or no individual blocks have confirmed added accessibility.

### Figure 2: PCA functional-retention and $G_{80}/G_{90}$

This composite figure has the same scientific meaning as the earlier rank-retention result figure while remaining valid when the new emergence set is unknown in advance:

1. **All-layer overview:** two heatmaps over Transformer block (rows) and registered PCA rank (columns), one for $D^{(0.8)}_{\ell,r}$ and one for $D^{(0.9)}_{\ell,r}$. Stage-1-admitted layers are outlined. This panel proves that all layers and ranks were evaluated rather than selected after TEST.
2. **Admitted-layer curves:** for every layer in $\mathcal L^+_{\mathrm{CLINC}}$, plot rank on the x-axis and held-out CE gain in nats/example on the y-axis. Show PCA, 64 Haar curves/band, full-$R_U$, $G_{80}=0.8G_{full}$, and $G_{90}=0.9G_{full}$.
3. **No-admission fallback:** if $\mathcal L^+_{\mathrm{CLINC}}=\varnothing$, the figure still renders the all-layer heatmaps and the pre-registered reference blocks 24/28 descriptively, with a visible `FULL R_U NOT ADMITTED; G80/G90 = NA` label. No layer is chosen by its point estimate.

Figure 2 must print one typed result per eligible layer: `r=<value>`, `UNCERTAIN`, `>512`, or `NA_NO_FULL_ADMISSION`, separately for 80% and 90%.

Required tables:

- all-layer $X/Z$ capability and eligibility;
- $G^{true}$, $G^{dupX}$, mismatch q95, $T$, pointwise and simultaneous intervals;
- official-test and collision-excluded sensitivity;
- covariance $r_{80}^{var}/r_{90}^{var}$ and TEST projector-capture diagnostics;
- all-layer/rank $G^{PCA}$, Haar q95, $G_{80}$, $G_{90}$, $D^{(0.8)}$, $D^{(0.9)}$, and typed functional-rank outputs;
- old-versus-new normalized layer-profile difference and typed verdict (table; not one of the two required primary figures);
- object identities, residualizer audit, selection freeze, and artifact manifest.

## 9. Guards, Stages, And Stop Rules

| Stage | Goal | Required operation | Output | Stop rule |
| --- | --- | --- | --- | --- |
| Data preflight | preserve the frozen CLINC task | verify hashes, 10-by-15 mapping, split counts, OOS exclusion, duplicate audit, prompt/token identity | data receipt | any mismatch stops before model forward |
| Object smoke | verify the measured transition | one small batch at blocks 1, 24, 28, 36; check all tensor identities and determinism | smoke receipt | any systematic identity failure stops scale-up |
| All-layer extraction | obtain comparable objects | one deterministic pass recording blocks 1--36 | extraction manifest | missing block/row/token or nonfinite values stops fitting |
| TRAIN/validation freeze | fit without TEST selection | retrain all CLINC residualizers and heads; fit every layer's PCA/Haar/rank heads; freeze 64 mismatch maps, penalties, seeds, and both figure schemas | selection-freeze receipt | TEST remains sealed until complete |
| TEST evaluation | locate emergence and measure functional retention | evaluate every eligible layer and rank once; run the all-layer and layer-by-rank simultaneous bootstrap families | exact arrays and tables | no post-TEST layer/rank/control/axis change |
| Render | reproduce the two conclusion meanings | render Figure 1 (layerwise emergence) and Figure 2 (PCA $G_{80}/G_{90}$ retention) only from frozen tables | PNG/PDF plus render receipt | figures cannot change verdict logic |

Implementation, smoke, full extraction, TEST evaluation, and publication require separate explicit approval scopes. A smoke can validate only data and tensor identities; it cannot produce a scientific verdict.

**AI_PROPOSAL for execution review:** reuse the verified single-node `8×5090` profile from A15_08_06; write raw runs under `/data/250010109/MoE_Router/experiments/20260819_a15_08_07_e01_clinc150_layerwise_added_accessibility_and_pca/` and canonical `summary.md`, `detailed.md`, figures, and tables beside this Protocol. This resource/path choice remains non-executable until explicitly confirmed.

## 10. Known Cases And Interpretation Guards

- **Known good:** a synthetic correction carrying intent labels must yield positive matched excess.
- **Known bad:** independently permuted labels and fully mismatched updates must not pass.
- **Known confusing:** $Z_\ell$ accuracy can be high while $T_\ell$ is zero; this is cumulative accessibility without confirmed local addition.
- **Known confusing:** PCA can cross the numerical $0.8G_{full}$ line when full $R_U$ was not admitted. The curve is then descriptive and both formal functional ranks remain `NA_NO_FULL_ADMISSION`.
- **Known confusing:** an admitted full gain with no passing registered PCA rank is `>512` or `UNCERTAIN`, not `NA`.
- **Headroom guard:** report old-only CE at every block; late layers with nearly exhausted CE headroom may be inconclusive rather than negative.
- **Prior selected-layer evidence:** blocks 24/28 on CLINC were already viewed and failed full-$R_U$ admission. They remain in the all-layer family but cannot be described as newly discovered negatives.

## 11. Success, Failure, And Claim Boundary

- **Pass — `CLINC_LAYER_LOCAL_ACCESSIBILITY_FOUND`:** $\mathcal L^+_{\mathrm{CLINC}}$ is nonempty. Claim only the named blocks and registered linear family.
- **Fail — `NO_REGISTERED_CLINC_LAYER_EXCEEDS_MATCHED_CONTROLS`:** every eligible block's simultaneous 95% UCB is non-positive and all guards pass.
- **Insufficient:** no positive layer but at least one decisive interval crosses zero, or any capability, identity, leakage, null, or provenance guard fails.

For every Stage-1-admitted layer, Stage 2 separately returns:

- `PCA_G80_G90_CONFIRMED` when both $r_{G80}$ and $r_{G90}$ exist;
- `PCA_G80_ONLY_CONFIRMED` when only the 80% threshold passes;
- `PCA_RETENTION_NOT_REACHED` when full gain is admitted but the frozen grid does not confirm a threshold;
- `PCA_RETENTION_UNCERTAIN` when the relevant interval crosses the registered boundary.

For every non-admitted layer, the only eligible Stage-2 functional verdict is `NA_NO_FULL_ADMISSION`. Geometric PCA ranks may still be reported, but cannot rescue functional admission.

The result report must lead with exactly two knowledge statements:

1. **Emergence location:** list $\mathcal L^+_{\mathrm{CLINC}}$ and explain whether the old blocks 24/28 replicate, disappear, or coexist with new admitted blocks.
2. **PCA functional retention:** for each admitted layer report $G_{full}$, $G_{80}$, $G_{90}$, $r_{G80}$, and $r_{G90}$; if no layer is admitted, state that both functional ranks are `NA` because there is no validated full effect to retain.

Stage-1 Pass alone does not establish low-dimensionality. Stage-2 Pass establishes only PCA-family functional compressibility at the named layer, rank, task, and linear readout; it does not establish intrinsically low-rank representation, model-native use, or routing utility. Even a different layer profile does not prove that natural language alone caused the shift, because the old and new tasks also differ in labels, class count, wording, and sample distribution.

## 12. A--G Review Ledger

| Block | Decision | State |
| --- | --- | --- |
| A | ordered CLINC question: recover emergence layers, then test PCA $G_{80}/G_{90}$ retention without promoting geometry to function | `CONFIRMED` |
| B | audited CLINC150 in-scope data, official splits, collision sensitivity, reused-TEST boundary | `CONFIRMED` |
| C | known-domain 15-way intent task and permitted supervision | `CONFIRMED` |
| D | frozen Qwen3-8B, existing CLINC prompt/token, all blocks, exact $X/Z/U/R_U$ objects | `CONFIRMED` |
| E | retrain all learned $R_U$-related components on CLINC TRAIN; matched full/PCA/Haar fitting | `CONFIRMED` |
| F | $T_\ell$ emergence plus jointly corrected $G_{80}/G_{90}$ functional-rank rules and exactly two primary figures | `CONFIRMED` |
| G | staged preflight/smoke/all-layer-by-rank run, artifacts, and separate approval scopes | `CONFIRMED` |

Cross-block consistency: `PASS_APPROVED_FOR_EXECUTION`.

Promotion requires explicit confirmation of A--G. Design confirmation does not authorize execution. After confirmation, the same file is promoted; no competing plan file is created.

## 13. Execution Receipt — 2026-08-19

This section records the approved execution without changing the frozen scientific design above.

| Stage | ACP job | Outcome | Claim eligibility |
| --- | --- | --- | --- |
| Object smoke | `pt-fb5eki0n` | SUCCEEDED; 160 rows, blocks 2--36, all identity guards passed | engineering only |
| TRAIN/validation extraction | `pt-hspr6s63` | SUCCEEDED; 18,000 rows, 35 eligible layers | eligible |
| Residual/PCA fit | `pt-smj8d3rq` | SUCCEEDED; all 35 layers passed | eligible |
| Selection and freeze | `pt-m55ktxr6` | SUCCEEDED; 350 functional tasks, 350 nonlinear diagnostics, 64 mismatch and 64 Haar controls | registered analyses eligible; nonlinear outputs diagnostic only |
| TEST confirmation | `pt-3o8ipsox` | SUCCEEDED; 4,500 rows, 35 layers | eligible robustness profile |

- TEST gate receipt hash: `0dbeb2d44710f6cd2040350817edf2f062881ff91500606c5b6dea6bebb4eadb`.
- Registered verdict: `FAIL_ALL_LAYERS_NONPOSITIVE`; admitted layer set is empty.
- Registered Stage-2 result: all layers are `NA_NO_FULL_ADMISSION` for both $r_{G80}$ and $r_{G90}$.
- Deviations affecting the primary verdict: none. Block 1 was handled exactly as the registered `STRUCTURALLY_INELIGIBLE` case.
- Post-hoc diagnostics: nonlinear-$X$ and supervised reduced-rank outputs are diagnostic and cannot alter the registered verdict.
- Canonical result records: [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_07_E01_clinc150_layerwise_conditional_intent_added_accessibility/summary.md), [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_07_E01_clinc150_layerwise_conditional_intent_added_accessibility/detailed.md), and [evidence/layerwise_result.json](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_07_E01_clinc150_layerwise_conditional_intent_added_accessibility/evidence/layerwise_result.json).
- Interpretation status: `AI_DRAFT_AWAITING_DXY_JUDGMENT`.
