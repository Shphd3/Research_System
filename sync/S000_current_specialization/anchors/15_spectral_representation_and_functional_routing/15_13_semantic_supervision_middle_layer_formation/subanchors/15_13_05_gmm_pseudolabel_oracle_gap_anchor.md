# A15_13_05: Can Diagonal-GMM Pseudo Labels Close the Causal-Router Oracle Gap?


## 1. Problem Definition

The decision question is whether unsupervised hierarchical labels fitted to frozen final-layer whole-window representations can train a block-14 causal Router that approaches unit-coefficient gold-path Oracle behavior while preserving task performance, and whether gradient-free load-balancing bias reduces the remaining gap. The test has two linked surfaces: the established M2D2-Wikipedia `3×3` causal-language-modeling workload and an eight-task answer-only continuation mixture. It does not test full-model pretraining, online label discovery, hidden-state formation in the frozen base, or uncontaminated benchmark generalization.

## 2. Physical Priors

Final-layer whole-window representations contain domain-related distribution structure. A diagonal-covariance Gaussian mixture can use direction, norm, and coordinate-wise variance without seeing semantic truth. If this structure identifies functionally related examples, frozen assignments should improve conditional expert learning beyond a frequency-matched random partition. Hard pseudo paths with unit expert coefficient separate label quality from online route prediction and probability attenuation.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts that diagonal-GMM supervision reduces the learned-to-Oracle gap in final negative log-likelihood and loss-curve area without lowering the registered task score, and that matching-expert deletion or substitution is more damaging. The strongest rival predicts increased route-label agreement or parameter separation without better likelihood, task score, or selective expert utility. A second hypothesis predicts that gradient-free load bias helps only when it reduces the same task and functional gaps, not merely route entropy.

## 4. Mathematical Model

For answer tokens or M2D2 target tokens $j\in\mathcal T$, the task objective is

$$
L_{\mathrm{task}}=-\frac{1}{|\mathcal T|}\sum_{j\in\mathcal T}\log p(x_j\mid x_{<j}).
$$

The causal Router at block 14 reads only the state available at the current prediction position. Learned routes use a top-one index and the learned route probability as expert coefficient. Hard pseudo and gold Oracle paths use their frozen label index and coefficient one while training a detached-shadow diagnostic Router.

For a learned condition $m$ and matched Oracle $o$, the final-loss gap is $G_{\mathrm{NLL}}=L_m-L_o$. Learning-efficiency gap is the ratio of answer tokens required to reach the task-only loss at 75% of its budget. Expert function is the increase in task NLL after deleting the chosen expert or substituting an eligible wrong expert. Route agreement and parameter geometry are explanatory only.

## 5. Computational Realization

The base is frozen Qwen3-0.6B-Base with its language head frozen. Rank-eight shared, coarse, and fine LoRA residuals are added only to zero-indexed block 14 `down_proj`; one token activates total rank 24. Flat routing activates one rank-24 expert. A train-only rank-64 principal-component basis is fitted to frozen final-layer whole-window means. The primary labeler fits a three-component diagonal Gaussian mixture, then child mixtures inside its coarse assignments, using 20 deterministic restarts, at most 100 iterations, and train likelihood alone for restart selection. M2D2 uses three children per parent. The eight-source mixture uses eight total leaves by assigning three children to each of the two largest train-only coarse clusters and two to the smallest, a deterministic rule that never reads source truth.

M2D2 hierarchical training has exactly two stages of 144 optimizer updates: stage one trains shared LoRA, coarse experts, and coarse Router; stage two freezes the coarse Router, keeps coarse experts trainable, and trains shared LoRA, fine experts, and fine Router. No coarse-row-space subtraction is used. The benchmark mixture uses the exact eight registered task sources and answer-only cross entropy; because official evaluation items may appear in training, its task scores are explicitly internal capability diagnostics.

## 6. Minimal Falsification Tests

Evidence is eligible only after every registered condition and both seeds have finite final checkpoints, one immutable manifest, identical evaluators, per-item task predictions, complete fixed-development curves, route arrays, full-batch load statistics, expert interventions, and parameter geometry. Verdict A requires the hard diagonal-GMM method to reduce the learned-to-Oracle final-NLL and curve-area gaps versus ordinary diagonal-GMM learning in both seeds, preserve or improve the two-seed benchmark macro average versus matched task-only, and move at least one selective expert-intervention effect toward Oracle. Verdict B applies when semantic routing is learned but those task gates fail. Verdict C applies when evidence is incomplete or ineligible. Load balancing is effective only if its on-minus-off comparison improves task evidence in both seeds.

## 7. Current Evidence

E08 established a small M2D2 gold-path Oracle value with a worst-control NLL advantage of `0.001506 [0.001396, 0.001618]` nats per target token and positive child interventions. E07 learned more semantic routes but was worse than task-only by `0.001054` NLL per token. E09's direction-plus-radius pseudo-label hierarchy beat newly trained simple baselines but remained `0.000903` worse than the matched staged task-only hierarchy. The saved secondary diagonal-GMM labels had higher confirmation normalized mutual information than the trained direction-plus-radius labels (`0.524` versus `0.444`), but they used only five library initializations and were not trained as the primary method; therefore they do not answer this anchor.

## 8. Claim Boundary And Next Decision

This experiment can establish only whether the frozen-label, one-layer, frozen-base realization closes part of the registered Oracle gap while retaining internal task performance. It cannot establish semantic reasoning rather than topical/source regularity, benchmark generalization, optimal expert placement, full-model benefit, or causation from parameter geometry. The one next decision is to accept verdict A, B, or C from the unified frozen-checkpoint evaluation; no condition may be pruned or retuned after observing an intermediate result.
