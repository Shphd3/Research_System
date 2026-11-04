派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_02_frequency_complement_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_02_frequency_complement_anchor.md)；研究修改仍回到原件。

---

# Anchor A15_24_02: preserving frequency-related directions while restricting local updates

[中文](15_24_02_frequency_complement_anchor_cn.md) · [Protocol](../../../../../../../../UNAVAILABLE.md) · [Results](../../../../experiments/A15/15_24_frequency_composition_common_path/frequency_complement_20261023/summary.md)

The local question is: **does exact preservation of a matrix's responses to specified input directions require an orthogonal-complement update, and what happens to low-feature prediction under that restriction?** The algebraic condition and predictive effect are separate tests. The researcher authorized bounded analysis and requested reading, explanation, then discussion before updating scientific judgment.

This post-execution reading revision expands explanations without changing the pre-outcome objects, hypothesis, comparisons or budget. Detailed preserves the original design bytes, timestamps and hashes. The Protocol remains byte-frozen.

## 1. Problem definition

Parent [A15_24](../15_24_frequency_composition_common_path_anchor.md) studies learning under feature-frequency dispatch. A feature is a coordinate of the fixed CrossCoder. Low frequency means low activation frequency on the original TRAIN panel; it does not mean rare words, difficult tasks or mastered capabilities.

The earlier direction audit measured geometry of saved parameter displacement. It did not establish predictive function. The researcher's proposal to retain selected directions and update the remainder becomes two local questions: (1) what happens when some previously accumulated displacement along candidate directions is rolled back; (2) what happens when the same proposed optimizer displacement is restricted to the complement, compared with the full displacement and random restrictions? Rollback and prospective-update effects cannot substitute for each other.

Use original T_F, retaining the Base path and two selected experts. No ninth common expert is added. This inherited child neither creates an independent Focus nor expands into general forgetting.

## 2. Physical priors

Exact preservation of a fixed linear map on a fixed input subspace has an algebraic condition. It is not an empirical discovery from loss measurements.

The candidate directions are the first 16 components of the existing centered TRAIN hidden-state PCA. They capture input variation, not a weight SVD; activations are not divided by singular values. Earlier frequency-band contribution analysis motivates examining them but does not qualify them as task-specific high-frequency directions.

A low-feature event can contain many high-frequency features. Shared directions may help its prediction. Retaining their current contribution and prohibiting future changes are distinct claims; the value of the latter requires its own comparison.

## 3. Falsifiable hypothesis

Starting from identical saved parameters, TRAIN batch and AdamW history, a complete displacement restricted to the candidate complement has lower low-feature predictive loss than both the full displacement and a same-rank random-complement displacement when norms are matched. Check both contrasts separately in the two inherited seeds.

Strong rivals are generic reduction in displacement size, an effect shared by arbitrary restrictions, useful shared directions, and a global PCA basis that fails to identify the relevant function. Norm matching, random directions and rollback constrain these rivals without eliminating all of them.

Complement membership is necessary only for the stated objective of **exactly preserving the selected matrix responses**. If the objective is instead tolerable task-loss change, the restriction is one candidate policy; its necessity does not follow from the algebra.

## 4. Mathematical model

### 4.1 Input, expert and loss

Let \(h\in\mathbb R^{1024}\) be the frozen Base final-layer hidden state and \(s>0\) the original fixed TRAIN scale. Each expert sees the full input \(u=h/s\). Fixed routing returns two experts \(\mathcal R(h)\), whose residual computation is

\[
h'=h+\frac{s}{2}\sum_{e\in\mathcal R(h)}
W_{e,\mathrm{down}}\left[\operatorname{SiLU}(W_{e,\mathrm{gate}}u)
\odot(W_{e,\mathrm{up}}u)\right].
\]

The product is elementwise. A frozen RMS norm and output head yield next-token probabilities; \(\ell=-\log p(y\mid h')\) uses the actual target \(y\), in nat, lower is better. The full Transformer is not rerun.

Only the low-list expert E0 up matrix \(W\in\mathbb R^{1024\times1024}\) may change temporarily. All other matrices, head, inputs, routes and scale are fixed. E0's low-frequency list does not imply its input contains only low-frequency information.

### 4.2 What preservation constrains

The columns of \(V\in\mathbb R^{1024\times16}\) are unit orthogonal directions from the existing TRAIN PCA, with \(V^\top V=I\) and \(P=VV^\top\). Each column of \(WV\) is the matrix response to a unit input direction. It is neither an activation frequency nor a loss contribution.

For a displacement \(U\), exact preservation is equivalent to

\[
(W+U)V=WV
\quad\Longleftrightarrow\quad UV=0
\quad\Longleftrightarrow\quad U=U(I-P).
\]

Subtracting gives the first equivalence. If \(UV=0\), then \(UP=UVV^\top=0\), hence \(U=U(I-P)\). Conversely, \((I-P)V=0\). Thus every row of \(U\) is orthogonal to the column space of \(V\); an arbitrary oblique complement alone does not ensure this null action.

The allowed displacement space has dimension \(1024\times1008=1{,}032{,}192\). No existing forward component is deleted:

\[
W_*=W_*P+W_*(I-P),\qquad W_{\mathrm{new}}=W_*+U(I-P).
\]

Here \(W_*\) is the saved step-168 matrix. Both terms remain in the forward pass. A mixed input \(u=Pu+(I-P)u\) can still change through its complement component, and downstream predictions may change.

### 4.3 Two interventions

With initialization \(W_{\mathrm{init}}\), define net historical displacement \(D=W_*-W_{\mathrm{init}}\). Rollback uses

\[
W_{\mathrm{rollback}}=W_*-aDP,\qquad a\in\{0.25,0.5\}.
\]

This removes part of the accumulated displacement, not all of \(W_*P\). A saved same-rank random basis \(Q\) supplies \(DQQ^\top\), rescaled to the same actual edit norm, distinguishing direction choice from generic perturbation.

The update test constructs full AdamW displacement \(U\) from the same saved state, then compares \(U\), \(U(I-P)\), and \(U(I-QQ^\top)\). Each complement also has a version rescaled to \(\lVert U\rVert_F\), the square root of the sum of squared matrix entries. Both natural and matched norms are retained.

Projecting the raw gradient alone is generally different: AdamW uses previous first/second moments, coordinatewise scaling and weight decay. A separate gradient-only projection diagnostic tests whether its eventual displacement satisfies \(UV=0\).

### 4.4 Primary metric

B1 denotes the original TRAIN low-frequency band. For feature \(j\), let \(S_j\) contain DEV positions where it is active and E0 is routed. Let \(J=\{j:|S_j|>0\}\) over B1. The primary metric is

\[
L_{\mathrm{low},E0}=\frac{1}{|J|}\sum_{j\in J}\frac{1}{|S_j|}\sum_{i\in S_j}\ell_i.
\]

Average within each supported feature, then equally across features. Positions can contribute to several features and are not independent experimental replicates. Unsupported IDs are NA, not zero. Full-DEV low/high macros and overall NLL are secondary readouts, not replacements.

## 5. Computational implementation

Use original T_F seeds 11/22, their initialization and full step-168 saved states, and existing TRAIN basis, groups and routes. In each saved TRAIN order, select the first 512 E0-hit positions; microbatch 64; sum next-token cross entropy divided by 512. Restore AdamW history and terminal learning rate \(3\times10^{-5}\); clip only the eligible matrix to norm 1.

Construct one ordinary proposal and one gradient-only diagnostic proposal per seed. Each starts independently from the original state. Restore parameters after every intervention. Accepted continuation steps are zero; no new trained checkpoint is saved.

All primary forwards and gradients use FP32 with TF32 off. Projection uses FP64 before FP32 application. Small contrasts must not be combined with historical BF16 loss as a direct replay. Evaluate all DEV; only E0-hit positions need recomputation for edits, while invariant positions reuse their baseline. Protocol fixes exact counts, resources, asset identities and failure gates.

## 6. Minimal falsification test

The prespecified local sign pattern requires matched PCA-complement primary loss minus full-update loss, and minus matched random-complement loss, each below \(-10^{-6}\) nat in both seeds. This is a descriptive numerical floor, not significance, practical noninferiority or scientific acceptance. Report every condition against the original model too, so a smaller increase is not relabeled absolute learning gain.

Required checks cover exact per-position no-op NLL, original model/optimizer identity, frozen tensors, projection residual, actual edit norms, finiteness and complete coverage. Preserve and mark failed conditions INVALID. Report high-feature and overall loss without inventing scientific acceptance bounds.

## 7. Current evidence

The previous [saved-weight audit](../../../../research_notes/frequency_routing_input_update_direction_20261023.md) found 15.16% / 15.33% of all gate/up net displacement in the first 16 input PCs, versus 1.49% / 1.48% in saved random directions. This is geometry, not predictive utility.

This round's factual evidence is in [Summary](../../../../experiments/A15/15_24_frequency_composition_common_path/frequency_complement_20261023/summary.md) and [Detailed](../../../../../../../../UNAVAILABLE.md). Execution is complete; numerical checks pass; evidence is exploratory on exposed DEV. The question remains open and researcher scientific judgment remains Unknown. This section does not adjudicate mechanism support.

## 8. Claim boundary and next decision

Scope is one matrix of one expert, two saved seeds, one scratch batch per seed, a fixed global input basis and previously exposed DEV. High/low independent tasks have not been separated, nor is the basis qualified as task-specific. Results do not establish long-training benefit, frequency causation, general forgetting or reproduction of an advisor algorithm.

Follow the requested sequence: researcher reading, stepwise explanation, then discussion of understanding. The scientific next decision is Unknown; completion neither closes the question nor authorizes additional training or a new architecture.
