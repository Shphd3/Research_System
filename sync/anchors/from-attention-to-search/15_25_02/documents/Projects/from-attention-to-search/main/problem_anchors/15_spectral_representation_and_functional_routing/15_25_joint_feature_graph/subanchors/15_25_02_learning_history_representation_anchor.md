派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_02_learning_history_representation_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_02_learning_history_representation_anchor.md)；研究修改仍回到原件。

---

# A15_25_02: How does learning history change conditional-rule representations, and which directions matter for answering?

## 1. Problem Definition

The research question is: **How does learning history change conditional-rule representations, and which directions matter most for answering the task?** The researcher fixed this question and authorized the Anchor, Protocol and complete frozen analysis on 2026-10-23. This child of [A15_25](../../../../../../../../UNAVAILABLE.md) examines whether inspectable representation components have a local functional role. The separate A17 experiment supplies saved models and data; its design and scientific decisions remain with A17.

Task A uses a visible mode: command 甲 selects the first word and 乙 the last. Task B reverses that command mapping under another visible mode. For example, with 黄 红 鸟, mode one plus 甲 requires 黄, whereas mode two plus 甲 requires 鸟. Four states are compared: original Base; acquired A; A followed only by B; A followed by mixed A+B. The last state did not learn A+B from Base. Only the final block's attention Q/K/V/O matrices changed. All earlier computations should therefore agree for the same input.

The uncertainty is whether changes that distinguish successful joint answering can be localized to task-relevant directions rather than generic displacement or frequently active components. Support retains a bounded candidate decomposition for further research; comparable random-control effects weaken it; invalid replay, poor dictionary coverage or unresolved uncertainty restrict the corresponding inference. No question closure is automatic.

## 2. Physical Priors

One mathematical assumption is used: saved CrossCoder normalization and decoder weights define additive contributions in the original residual coordinates. Preserving the reconstruction error makes a selective edit well defined even when reconstruction is imperfect. A shared CrossCoder activation vector spans fourteen selected layers; it is not fourteen independent feature inventories.

The AI operational hypothesis is that some learning-related changes influence answering more strongly than equal-size nonspecific changes. The strongest rival is generic output/format displacement. Feature occurrence frequency alone does not establish importance, semantic identity or transferable computation.

## 3. Falsifiable Hypotheses

H1: feature directions selected using discovery examples produce larger correct-versus-alternative margin damage under attenuation than frequency/decoder-norm matched, perturbation-norm equalized random features on separate evaluation groups. H2: a low-rank subspace of mixed-minus-sequential residual changes shifts the sequential state's old-task answers toward the mixed state more than an equal-rank, equal-perturbation-norm random subspace. H2 can hold even if the fixed CrossCoder fails to resolve the change.

Effects only in reconstruction, comparable random effects, or effects without task specificity do not identify a rule mechanism. Transfer between learning states on identical inputs tests localization of a state difference; it is not cross-task or cross-dataset reuse.

## 4. Mathematical Model

Let \(h_m(x)\in\mathbb R^{1024}\) be the last block's residual before final normalization for model state \(m\) and input \(x\). The frozen output function is \(g\). The answer margin is \(M=g(h)_y-g(h)_a\), where \(y\) is the correct word and \(a\) is the opposite list endpoint. Accuracy over the full vocabulary, negative log likelihood and first/last/other probability accompany this margin.

For shared CrossCoder activations \(z\), last-layer decoder \(D\), saved scale \(s\), mean \(\mu\), bias \(b\), and actual residual error \(e\),

\[
h=\mu+s(b+zD)+e,\qquad h'=h+s(z'-z)D.
\]

This edit leaves \(e\) intact. Discovery importance is the mean positive first-order margin contribution \(\max(0,z_f s D_f^\top\nabla_h M)\). It proposes candidates; measured finite interventions adjudicate their importance. Decoder directions need not be orthogonal.

For paired state change \(\Delta=h_{mixed}-h_{sequential}\), fit right singular vectors \(V_k\) on discovery rows only and evaluate \(h'=h_{sequential}+\Delta V_kV_k^\top\). This is a projection of an observed difference, not a learned new model. Geometry and intervention support separate claims.

## 5. Computational Realization

Reuse the exact FP32 A17 model loader and the fourteen residual-post hooks, saved normalization and fixed-threshold encoder from the existing CrossCoder analysis. Adapt the paired input, feature ranking and interventions. There is no optimizer, parameter update, dictionary training or new training data generation.

The [Protocol](../../../../experiments/A15/15_25_02_learning_history_representation/20261023/protocol.md) binds all four checkpoints, 1,600 existing old/reversed DEV examples, deterministic unordered-word-group discovery/evaluation separation, control construction and compute ceiling. DEV was already exposed in A17, so the new split limits analysis selection leakage but is not fresh confirmation. Unchanged layers, native replay, no-op and full-vector replacement are explicit checks. Native behavior and raw geometry remain usable separately from dictionary qualification.

## 6. Minimal Falsification Tests

Three primary contrasts are fixed: half attenuation of the mixed state's 32 old-task candidates on old examples; half attenuation of its 32 new-task candidates on new examples; rank-16 mixed-to-sequential transfer on old examples. Each is compared with eight matched random controls. Use paired unordered-group means and 5,000 bootstrap resamples with two-sided 98.333% intervals. A strictly positive interval supports that local contrast; a nonpositive upper bound weakens it; an interval spanning zero is insufficient. These are delegated operational thresholds, not physical constants.

Reconstruction preserves at least 80% of centered variation and changes full-vocabulary accuracy by at most five percentage points to qualify a state for strong dictionary-decomposition claims. Failure leaves residual-preserving interventions measurable but bounds their interpretation to the chosen dictionary directions. A native/cached maximum margin error above 0.001 or a nonzero no-op invalidates dependent interventions.

## 7. Current Evidence

Before this analysis, the source A17 seed-29 endpoints report old/new accuracy of 0%/100% after B-only continuation and 99.625%/99.75% after mixed continuation. These are inherited behavior observations, not results of this Anchor. The newly registered paired geometry and interventions are **NOT RUN** at design freeze. Both continuations have 1,200 updates, but B exposure differs: 24,000 B answers versus 12,000 A plus 12,000 B answers. A causal effect of curriculum alone is not identified.


**Execution evidence added 2026-10-23.** Four-state extraction and all 253 intervention conditions are complete. Discovery-fixed rank-16 raw difference transfer yields 80.88% old evaluation accuracy versus 0.12% for equal-rank/equal-perturbation random controls, with new accuracy 98.28%. CrossCoder half-attenuation excess margin damage is 1.130 and 1.427 logits, but all four whole-reconstruction gates fail and candidate coefficient transfer does not recover old answers. These are local observations from one seed and exposed DEV; researcher mechanism judgment remains Unknown. [Complete facts, intervals and boundaries](../../../../experiments/A15/15_25_02_learning_history_representation/20261023/summary.md).

## 8. Claim Boundary And Next Decision

Scope is one task family, one selected training seed, fixed endpoints and local final-residual interventions. Earlier shared computations, final task sensitivity and CrossCoder recurrence are distinct objects. Frequency describes this analysis sample; pretraining frequency, long/short-range organization, general reusable skills and parameter separation remain untested.

The next researcher-owned decision is whether the controlled evidence identifies a sufficiently specific candidate direction set to motivate a later experiment. That judgment remains **Unknown** until the researcher reviews the results. Execution completion does not close the question.
