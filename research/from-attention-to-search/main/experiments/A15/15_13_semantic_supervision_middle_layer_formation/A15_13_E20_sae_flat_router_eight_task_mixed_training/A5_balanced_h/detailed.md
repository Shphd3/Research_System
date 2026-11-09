# A5 balanced h-input training: detailed evidence

[Summary](summary.md) · [Frozen protocol](../protocol.md) · [Submission snapshot](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/protocol_at_submission.md)
Primary Anchor: [last-layer SAE functional routing](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md).
Run: [full-20260908T111248Z](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z); code: [immutable source](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source).

## 0. Direct result and eligibility

All 15 conditions completed 512 updates; all 15 internal-test record sets and 30 comparisons exist. Job pt-j131dsb1 was verified SUCCEEDED; platform last update 2026-09-08 12:09:27 UTC is not an independently recorded finish timestamp. Model training and primary internal evaluation are complete; full external benchmarks are NOT RUN.

Requested AI reading: task-only is best by mean internal-test NLL (0.696579), followed by GMM (0.716802), SAE (0.734016), random (0.735215), dense (0.738619). SAE lacks cross-seed stable superiority over random. Scientific state remains awaiting researcher judgment.

## 1. Terms and condition mapping

C1–C5 are **display aliases introduced for this report**, not an expert-count hyperparameter or a registered C sweep. Routed expert count is fixed at eight. C1: SAE co-activation partition; C2: matched random-feature partition; C3: flat eight-component diagonal GMM control; C4: task-only learned router; C5: dense shared-plus-always-active adapter. Seeds are 17/29/43.

NLL is negative log probability per answer token, in nats/token. Within-seed aggregate = total answer loss / total answer tokens, not average of per-task means. Cross-seed mean uses equal weight; SD has denominator 3−1. Checkpoints, tokens and task rows are not additional independent training seeds.

## 2. Question and approved setup

The linked Anchor asks whether SAE structure provides stable functional benefit beyond matched random and task-learned routing. Protocol A5.6 authorizes the revised architecture; prior old-E20 results are not pooled with this run.

Frozen Qwen3-0.6B-Base, layer 27 MLP pre-input h with width 1024; identical h for teacher, router and experts. Routed arms have shared rank-16 branch plus eight rank-16 experts, Top-1. Dense has shared rank-16 plus one always-active rank-16 branch. All arms activate 65,536 adapter matrix parameters/token. Stored capacity is not matched: routed matrices 294,912 plus router 8,200; dense 65,536. Shared branch and routed expert-bank initialization are paired by seed.

SAE/random/GMM router weights are frozen offline; task-only router weights are trainable. All routed arms use dynamic nonparameter selection bias initialized at zero. Select argmax(z+b), weight by unbiased softmax(z) at the selected expert. Count all nonpadding tokens across the 16 microbatches; update once per effective batch by 0.001 sign(mean(count)−count). No cross-condition aggregation, no auxiliary balancing loss. Evaluation freezes bias.

### Training objectives and regularization by stage

There are two optimization stages and one preceding non-optimization grouping step. Calling all three “SAE regularization” would conflate different objects.

#### SAE feature grouping: no separation loss

Let \(f_{tr}\) and \(a_{tr}\geq 0\) be the identity and activation of the \(r\)-th active SAE feature at position \(t\), with \(r=1,\ldots,32\). A fixed map \(g(f)\in\{1,\ldots,8\}\) assigns retained features to eight groups by spectral clustering of the positive feature co-activation graph. This construction groups features with related co-activation; it does not optimize a differentiable “push different features apart” loss.

The SAE teacher target presented to the offline Router is
\[
s_{tj}=\sum_{r=1}^{32}a_{tr}\,\mathbf 1[g(f_{tr})=j],
\qquad
q_{tj}=\frac{s_{tj}}{\sum_{\ell=1}^{8}s_{t\ell}}.
\]
Thus the SAE grouping changes the target distribution \(q_t\); it is not an added regularizer in subsequent MoE training.

#### Offline fixed-teacher Router fitting

For SAE, random-feature and GMM conditions only, the linear Router predicts
\(p_t=\operatorname{softmax}(Wh_t+c)\) and minimizes
\[
\mathcal L_{\mathrm{Router}}
=\frac{1}{|V|}\sum_{t\in V}D_{KL}(q_t\Vert p_t)
+\frac{\lambda_W}{2}\lVert W\rVert_F^2.
\]
\(V\) is the set of covered answer-prediction positions. The first term has coefficient `1`. The second term is ridge regularization of the Router weight matrix \(W\) only; it shrinks \(W\) to control the linear readout and does **not** separate SAE features. The bias \(c\) is not penalized. \(lambda_W\) was selected on development KL from `{0, 1e-5, 1e-4, 1e-3}` independently for each condition and seed:

| Condition | Seed 17 \(\lambda_W\) | Seed 29 \(\lambda_W\) | Seed 43 \(\lambda_W\) | Teacher target |
|---|---:|---:|---:|---|
| SAE feature groups | 0 | 0 | 0.001 | normalized SAE activation mass per spectral group, \(q_t\) above |
| matched random-feature groups | 0.001 | 0.00001 | 0.001 | same construction after frequency-matched group-label shuffling |
| flat diagonal GMM | 0.0001 | 0 | 0.00001 | one-hot mixture-component assignment |
| task-only learned Router | N/A | N/A | N/A | no offline teacher fit |
| dense shared adapter | N/A | N/A | N/A | no Router |

Evidence: frozen [Router objective](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/teacher.py), [fitting and validation selection](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/router.py), [feature grouping](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/graph.py), and the retained [Router selection records](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/routers).

#### MoE adapter/expert training

For every condition \(C\), the 512-update differentiated objective is the same answer-token cross entropy:
\[
\mathcal L_C
=1\cdot\mathcal L_{\mathrm{answer\ CE}}+0\cdot R_C
=-\frac{1}{N_{\mathrm{answer}}}\sum_{t\in\mathrm{answer}}
\log p_{\theta_C}(y_t\mid x,y_{<t}).
\]
Hence each condition has task-loss coefficient `1`, no explicit \(R_C\), and regularization-loss coefficient `0`. Each eligible answer token has normalized weight \(1/N_{\mathrm{answer}}\) inside the complete effective batch. Prompt/padding tokens do not enter the loss, although nonpadding prompt tokens enter balancing counts.

| Condition | Explicit regularizer in \(\mathcal L_C\) | AdamW decoupled weight decay | Router during this stage | Count-based balance bias |
|---|---|---|---|---|
| SAE feature groups | none; coefficient 0 | 0.01 on shared/expert adapter parameters | frozen | update rate 0.001 |
| matched random-feature groups | none; coefficient 0 | 0.01 on shared/expert adapter parameters | frozen | update rate 0.001 |
| flat diagonal GMM | none; coefficient 0 | 0.01 on shared/expert adapter parameters | frozen | update rate 0.001 |
| task-only learned Router | none; coefficient 0 | 0.01 on shared/expert parameters; 0 on Router | trainable from answer loss | update rate 0.001 |
| dense shared adapter | none; coefficient 0 | 0.01 on all shared/active adapter parameters | absent | N/A |

AdamW weight decay is an optimizer-level, decoupled shrinkage, not an additive term in the recorded `train_nll`. For a decayed parameter \(\theta\) its contribution has the form \(\theta\leftarrow(1-0.01\eta_t)\theta\) at learning rate \(\eta_t\), in addition to the adaptive gradient update. The balancing bias obeys
\[
b_i^{(u+1)}=b_i^{(u)}+0.001\,\operatorname{sign}(\bar c^{(u)}-c_i^{(u)}),
\]
where \(c_i^{(u)}\) counts all nonpadding tokens assigned to expert \(i\) in update \(u\). This is outside autograd and is not a loss or a feature-separation regularizer.

Frozen-code evidence: [answer-token loss and backward normalization](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/train.py), [optimizer parameter groups](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/train.py), [frozen coefficients](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/config.py), and [bias update](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/source/model.py).

AdamW, expert LR 2e−4, task-router LR 5e−4, 26-update warmup and cosine schedule, gradient clipping 1.0, microbatch 8 × accumulation 16 = 128 records/update, 512 updates. Fixed final checkpoint, no test-based checkpoint selection. All checkpoints 0/128/256/384/512, recovery state, optimizer, bias and full sample schedules retained.

## 3. Protocol conformance and limitations

| Item | Expected / actual | Audit / boundary |
|---|---|---|
| Matrix | five arms × three seeds × 512 | all 15 training receipts, final hashes and checkpoint paths verified |
| Evaluation | 8,481 paired test records | identical record IDs, sources and token denominators; saved NPZ hashes match |
| Training/base identity | frozen approved implementation | training/evaluation identities match; frozen run manifest reverified |
| Curves | 0/128/256/384/512 | all full development checkpoints present |
| Frozen base | no base training | training receipts assert base frozen; runtime qualification is separately retained |
| Interventions | SAE/GMM, three seeds | six paired intervention effects retained in 30-comparison aggregate |
| Aggregation | token-weighted within seed | recomputed from raw arrays in float64; agrees with saved float32 aggregate within 1e−6 |
| Inference | per-seed bootstrap, no pooled seed inference | seed 43 reversal is retained, not averaged away |
| C labels | no variable-C experiment | report aliases only; user wording interpreted as conditions |
| Formal outcome label | protocol has overlapping failure/insufficient wording | label remains unresolved; data support no stable positive claim |
| Full external benchmark | separate standardized evaluation | NOT RUN; smoke only; no new evaluation job submitted by this reporting task |

No training exclusions or missing conditions were introduced. Report statistics, smoothing, SD bars and timing extrapolation are post-hoc descriptive displays, not changes to the primary decision rule.

## 4. All seed-level results

| Condition | Seed | Train last32 | Development | Test |
|---|---|---|---|---|
| C1 sae | 17 | 0.737050 | 0.743851 | 0.734041 |
| C1 sae | 29 | 0.733011 | 0.744124 | 0.734529 |
| C1 sae | 43 | 0.745825 | 0.743015 | 0.733478 |
| C2 random_features | 17 | 0.740690 | 0.747346 | 0.737502 |
| C2 random_features | 29 | 0.736713 | 0.748206 | 0.738148 |
| C2 random_features | 43 | 0.742854 | 0.740332 | 0.729997 |
| C3 gmm | 17 | 0.717120 | 0.724064 | 0.714462 |
| C3 gmm | 29 | 0.717274 | 0.728501 | 0.718874 |
| C3 gmm | 43 | 0.728811 | 0.726770 | 0.717070 |
| C4 task_only | 17 | 0.698973 | 0.707986 | 0.697479 |
| C4 task_only | 29 | 0.694711 | 0.706730 | 0.696181 |
| C4 task_only | 43 | 0.708573 | 0.706202 | 0.696076 |
| C5 dense_shared_r16 | 17 | 0.742138 | 0.748679 | 0.738796 |
| C5 dense_shared_r16 | 29 | 0.738226 | 0.749307 | 0.739445 |
| C5 dense_shared_r16 | 43 | 0.749881 | 0.747444 | 0.737617 |

Source: [all seeds](tables/all_seeds.csv). Training loss is the last-32-update token-weighted objective on changing minibatches; development/test are fixed evaluation sets. Comparisons between these columns are not a formal generalization-gap estimator.

## 5. Condition means

| Condition | Train last 32 steps mean ± SD | Final development mean ± SD | Final test mean ± SD |
|---|---|---|---|
| C1 sae | 0.738629 ± 0.006551 | 0.743663 ± 0.000578 | 0.734016 ± 0.000526 |
| C2 random_features | 0.740085 ± 0.003115 | 0.745295 ± 0.004319 | 0.735215 ± 0.004531 |
| C3 gmm | 0.721069 ± 0.006706 | 0.726445 ± 0.002236 | 0.716802 ± 0.002218 |
| C4 task_only | 0.700752 ± 0.007100 | 0.706973 ± 0.000916 | 0.696579 ± 0.000782 |
| C5 dense_shared_r16 | 0.743415 ± 0.005932 | 0.748476 ± 0.000948 | 0.738619 ± 0.000927 |

[Download means and SD](tables/condition_means.csv). The small SAE–random mean advantage is about 0.001200 nats/token; its sign does not hold in all seeds.

## 6. Primary paired comparisons

Positive comparator-minus-SAE favors SAE. Intervals resample records within source **inside each seed**, 2,000 draws; they do not quantify uncertainty over training seeds.

| Seed | Comparator minus SAE | Difference | 95% within-seed record-bootstrap interval |
|---|---|---|---|
| 17 | random_features minus sae | 0.003461 | [0.003114, 0.003806] |
| 17 | gmm minus sae | -0.019579 | [-0.020271, -0.018870] |
| 17 | task_only minus sae | -0.036562 | [-0.037454, -0.035714] |
| 29 | random_features minus sae | 0.003618 | [0.003292, 0.003944] |
| 29 | gmm minus sae | -0.015655 | [-0.016341, -0.015004] |
| 29 | task_only minus sae | -0.038349 | [-0.039310, -0.037415] |
| 43 | random_features minus sae | -0.003481 | [-0.003873, -0.003122] |
| 43 | gmm minus sae | -0.016407 | [-0.016985, -0.015837] |
| 43 | task_only minus sae | -0.037402 | [-0.038347, -0.036507] |

Source: [primary contrasts](tables/primary_contrasts.csv) and [original pairwise aggregate](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/results/aggregate.json). Seed 43's random−SAE interval is [−0.003873, −0.003122]; the reversal is not just an interval crossing zero.

The protocol maps nonpositive random contrast to NO_STABLE_STRUCTURE_GAIN but also maps seed reversal to INSUFFICIENT. The original implementation's ordered branch would use NO_STABLE_STRUCTURE_GAIN; the Anchor emphasizes insufficient evidence on reversal. Preserve this naming conflict for the researcher; do not edit frozen criteria after observing results. The common substantive reading is no demonstrated stable SAE superiority.

## 7. Internal per-task means across three seeds

| Task | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|
| mmlu | 0.680939 | 0.721751 | 0.632551 | 0.610583 | 0.720708 |
| mmlu_pro | 1.277971 | 1.323650 | 1.194406 | 1.149022 | 1.339917 |
| bbh | 1.320626 | 1.240303 | 1.220139 | 1.132606 | 1.375335 |
| gsm8k | 0.699784 | 0.701413 | 0.656156 | 0.593205 | 0.704021 |
| math | 0.729617 | 0.730554 | 0.725883 | 0.724463 | 0.732867 |
| gpqa | 0.784696 | 0.799438 | 0.753504 | 0.756510 | 0.807368 |
| humaneval | 0.838384 | 0.839931 | 0.809288 | 0.790758 | 0.861529 |
| mbpp | 1.079171 | 1.078597 | 1.053043 | 1.053725 | 1.083001 |

These are internal per-task NLL values, **not official benchmark accuracy**. [All per-task seed values](tables/per_task_all_seeds.csv) and [means with sample SD](tables/per_task_means.csv) are retained. Overall NLL is token-weighted and must not be reconstructed by equally averaging these eight columns.

## 8. Important figures

![Loss curves](figures/loss_curves.png)

Purpose: compare optimization and fixed-development loss, with the same parameter budget per token. Left uses non-overlapping 32-step token-weighted windows; right uses all 8,480 development records at five fixed checkpoints. Line = seed mean, band = one sample SD. Sources: [training windows](tables/train_window32.csv), [development curve](tables/dev_curve.csv). C4 is consistently lower; mean curves alone cannot establish the C1–C2 cross-seed claim.

![Test values](figures/test_nll.png)

Purpose: expose each independent training seed rather than hide reversal behind means. Dots are final test values; black bars are mean ± sample SD, not bootstrap intervals. Source: [all seeds](tables/all_seeds.csv). This supports a bounded comparative-loss reading, not generated-answer capability.

## 9. Route-intervention evidence

Within-position expert-selection shuffling while retaining the registered coefficient increases answer loss in all three seeds: SAE +0.022518 to +0.023130; GMM +0.035090 to +0.037799 nats/token. All six within-seed paired intervals exclude zero. Sources: `left_intervention` in SAE/GMM-versus-dense entries of [aggregate](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/results/aggregate.json).

This establishes sensitivity to this trained routing assignment under this intervention. It does not show semantic correctness or that SAE assignment is better than GMM/task-only. Larger intervention damage alone is not a better-method ranking.

## 10. Benchmark runtime: evidence and proposed budget

Current frozen runtime is HF causal bfloat16, batch size one, shared task prompts/tokenizer/stopping/scorers and no chat wrapper. Actual ACP single-record-per-suite smoke timings were:

| Suite | Full records | Single-record smoke seconds | Naive GPU-hours/model |
|---|---|---|---|
| bbh | 6511 | 13.23 | 23.94 |
| gpqa | 448 | 20.36 | 2.53 |
| gsm8k | 1319 | 8.04 | 2.94 |
| mbpp | 500 | 5.44 | 0.76 |
| math | 5000 | 8.66 | 12.02 |
| mmlu | 14042 | 2.96 | 11.54 |
| mmlu_pro | 12032 | 8.08 | 27.02 |

Naively multiplying each timing by its dataset size gives **80.75 GPU-hours/model**, excluding official EvalPlus. At Base + 15 trained checkpoints and ideal four-GPU utilization this becomes **323 wall-hours**, about 13.5 days. This is a **risk illustration, not an ETA or confidence bound**: one record per suite is not representative, repeated setup overhead can inflate it, and long output tails can increase actual time. Do not provision a full run from this extrapolation.

### AI proposal: time-boxed qualification and screening

1. **20–30 minutes throughput pilot**, not a new capability claim. Measure prefill and generation separately across fixed prompt/output-length strata; test one common candidate batch 4/8/16 on Base and all five adapter types. Preserve the architecture hooks and verify frozen bias, padding handling, likelihood and generation/scoring parity against batch one. Record actual tokens/sec, memory and timeouts.
2. **2–4 hours target on four H100 for first screening**, contingent on pilot throughput. Use Base plus all five conditions at the prechosen seed 17; no best-seed selection. Fix approximately 128 stratified records per task family (~1,024/model, six models) before examining any capability scores. Use identical sample IDs for every model, preserve published shots and generation caps, and cache model-independent prompts/requests. The subset is a screening result, not an official/full benchmark score.
3. **Re-estimate before full confirmation.** Only if the pilot measures 4–8× end-to-end throughput improvement would the naive all-16-model budget scale to roughly 40–81 wall-hours (plus EvalPlus), still not a guaranteed finish time. Do not promise same-day full coverage. Decide whether all seeds/all tasks are scientifically needed after the fixed screen; any reduced scope must be explicit.

Use independent one-GPU workers and length-aware task shards; merge by stable record ID, with coverage/duplicate guards. Do not average shard scores blindly. Evaluate Base once per frozen contract; cache responses only within exact checkpoint/config/data identities, never share generated outputs across arms.

The harness supports batching and request caching ([official documentation](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/interface.md)); actual gains and numerical parity with this custom adapter are **not measured**. Increasing batch size changes the currently frozen batch-one manifest, so it requires an explicit execution-only amendment and qualification for all models. No silently shortened generation, changed few-shot count, alternate backend, or bypassed Python hooks. External execution still requires approval; this task only proposes the plan.

The screen addresses whether lower teacher-forced answer loss transfers to generated-answer correctness. If it does not, do not claim a capability benefit. If projected screening exceeds four hours, return the scope/time tradeoff before proceeding; do not keep extending the job in the background.

## 11. Evidence and artifact map

- [Run manifest](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/manifest.json): frozen source/config/data identities and resume command.
- [Report verification](/data/250010109/MoE_Router/reports/a5_20260908/verification.json): 15 final checkpoint and NPZ hashes; pairing, counts, curves and aggregation checks.
- [Reproduction script](/data/250010109/MoE_Router/reports/a5_20260908/build_report.py): read-only report derivation outside the frozen source tree.
- [Submission receipt](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/submission_receipt.json): job identity.
- [Qualification](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/qualification/receipt.json): actual-image training and benchmark smoke evidence.
- [Tables](tables/condition_means.csv) and [raw run results](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/results/aggregate.json): direct result sources.
- Frozen raw inputs, schedules, all training records, checkpoints and original evaluation NPZs remain under the run; no old E20 file is overwritten.

## 12. State and next decision

Numerical observations are verified. Mechanism explanation and Focus/Anchor scientific transition remain human-owned and unmodified. AI recommends qualifying the bounded benchmark screen above, not launching the full matrix immediately. Partial screening cannot replace full benchmarks or cross-seed confirmation. The existing Focus still describes older execution state; this report does not silently rewrite that human-owned surface.
