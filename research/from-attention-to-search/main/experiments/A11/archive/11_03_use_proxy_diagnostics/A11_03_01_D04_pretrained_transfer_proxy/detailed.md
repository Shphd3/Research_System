# A11_15 Pretrained Semantic-Transfer Efficiency: Detailed Evidence

## 0. Result

Status: **insufficient**. The implementation and pairing guards pass, but neither NTP nor K=2 MTP satisfies the held-out $Q\ge0.9$ gate. MTP has higher token-AUC in `2/5` seeds and final $Q$ not lower in `2/5`; this is not a stable efficiency advantage.

## 1. Terminology / Definitions

| Term | Concrete meaning | Formula / computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| common H1 | pretrained model's standard full-vocabulary next-token head after reading `Decision` | vocabulary argmax at $h_{T+1}$ | same downstream interface for both methods | hidden-state causality by itself |
| private H2 | copied full-vocabulary head predicting the answer from prompt-ending $h_T$ | vocabulary argmax of $U_2h_T$ | verifies direct earlier target fitting | common-H1 transfer |
| paraphrase consistency | prediction invariance under unseen wording that preserves state | group consistency fraction | tests semantic rather than wording fit | correct counterfactual use |
| counterfactual sensitivity | answer changes when early state changes and local request stays matched | paired flip fraction | tests state dependence | natural open-ended quality |
| $Q_{eval}$ | weakest required downstream property | $\min\{A_{H1},C_{para},S_{cf}\}$ | primary solvability metric | gradient mechanism |
| token-AUC | normalized area under $Q$ versus processed text tokens | trapezoidal integral | compares the full learning curve | matched compute efficiency |
| local guard | CE/accuracy on eight deterministic non-answer prompt positions | H1 next-token CE/accuracy | detects broad pretrained-language damage | external benchmark retention |

## 2. Data, Model, And Objective

The fixed task contains five persistent-assistant state domains: cost/speed goal, energy, privacy/sharing value, quiet/social preference, and morning/evening availability. Each seed has 160 training and 160 evaluation examples. Training and evaluation use disjoint cue paraphrases while preserving domain, latent state, request, option order, and counterfactual pairing.

The appended suffix is:

```text
... prompt  Decision  A/B
```

Let $T$ be the final prompt position. The losses are:

$$
L_S=\operatorname{CE}(U_1h_T,\texttt{Decision}),
$$

$$
L_I=\operatorname{CE}(U_1h_{T+1},Y),
$$

$$
L_D=\operatorname{CE}(U_2h_T,Y).
$$

NTP uses $L_S+L_I$; MTP uses $L_S+L_I+L_D$. The full Qwen3-0.6B backbone and tied H1/embedding are trainable. H2 is copied from H1 at initialization and receives gradients only in MTP.

Optimization: AdamW, learning rate `1e-5`, weight decay `0.01`, bfloat16, batch size `4`, gradient clipping `1.0`, 300 updates, checkpoints `0,1,2,5,10,20,50,100,200,300`.

## 3. Protocol Compliance And Implementation Audit

- remote four-H100 job `pt-0u9hjxa8`: succeeded;
- ten expected tasks and all ten checkpoints per task complete;
- 100 curve rows, 1,000 per-domain rows, and 10 paired-guard rows;
- model hash, tokenizer hash, selected pretrained-parameter hash, copied-H2 hash, data hashes, and batch hashes pair exactly within each seed;
- processed text-token counts match at every paired checkpoint;
- all values finite; copied H1/H2 answer contrast cosine is exactly one initially;
- prompt answer-token count patterns are label-balanced in train and evaluation;
- sequence length range `364-390`, below the configured `1024` limit.

The first submitted job `pt-jtuq2fmz` stopped after a successful GPU smoke because an inherited guard incorrectly required literal A/B token counts to be equal within every natural-language prompt. Inspection showed every token-count pattern was exactly balanced across A/B labels. The guard was corrected to test label predictiveness of count patterns, and no training objective, data, seed, or decision rule changed.

## 4. Full Paired Results

| Seed | NTP AUC | MTP AUC | NTP final $Q$ | MTP final $Q$ | NTP final H1 | MTP final H1 | MTP final H2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 971 | 0.4933 | 0.5141 | 0.7500 | 0.8250 | 0.8375 | 0.8875 | 0.9000 |
| 972 | 0.4891 | 0.4188 | 0.8750 | 0.8625 | 0.9375 | 0.9188 | 0.9188 |
| 973 | 0.3649 | 0.4217 | 0.8000 | 0.7875 | 0.8750 | 0.8563 | 0.8750 |
| 974 | 0.4402 | 0.2129 | 0.9000 | 0.7500 | 0.9500 | 0.8750 | 0.8938 |
| 975 | 0.3767 | 0.2587 | 0.8000 | 0.8375 | 0.9000 | 0.9063 | 0.9250 |

No row contains a valid $T_{0.9}$ because the criterion requires three consecutive evaluations. Seed 974 NTP reaches `0.9` only at the final checkpoint and therefore does not count as threshold recovery.

## 5. Fit, Transfer, And Private-Head Decomposition

At update 300, both conditions have train $Q=1.0$ in every seed. The pretrained model therefore removes the random model's severe fitting/semantic-prior limitation.

Held-out transfer is materially better than A11_14b but remains incomplete. Mean final values are:

| Metric | NTP | K=2 MTP |
|---|---:|---:|
| $A_{H1}$ | 0.9000 | 0.8888 |
| $C_{para}$ | 0.8950 | 0.8925 |
| $S_{cf}$ | 0.8250 | 0.8125 |
| $Q_{eval}$ | 0.8250 | 0.8125 |
| H2 native accuracy | 0.0000 | 0.9025 |

MTP successfully trains the direct H2 interface, but the standard H1 curve is not better. This is evidence for **private-head fitting without reliable common-head transmission**. It does not prove that the hidden state lacks semantic information; it shows that H2 accuracy alone cannot be used as the downstream efficiency claim.

## 6. Domain And Failure Decomposition

Final mean common-H1 evaluation accuracy:

| Domain | NTP | K=2 MTP |
|---|---:|---:|
| morning/evening availability | 0.6687 | 0.6125 |
| cost/speed goal | 0.8500 | 0.8313 |
| quiet/social preference | 1.0000 | 1.0000 |
| energy state | 0.9812 | 1.0000 |
| privacy/sharing value | 1.0000 | 1.0000 |

The task is not uniformly difficult. The availability domain accounts for most residual error, followed by cost/speed. Because the aggregate $Q$ also requires counterfactual flips, apparently high H1 accuracy is not enough to pass.

## 7. Local Pretrained-Language Guard

Mean local CE changes from `2.0659` at step 0 to `2.3737` for NTP and `2.6095` for MTP. MTP's final/initial CE ratios are `1.164, 1.175, 1.210, 1.659, 1.117`, so all five violate the preregistered `10%` step-0 tolerance. Relative MTP-vs-NTP CE and accuracy guards pass only `3/5` seeds.

This indicates that narrow response-position full-model fine-tuning alters local next-token behavior. It is not evidence of general catastrophic forgetting because the probe contains only eight fixed positions per prompt and no external LM benchmark.

## 8. Visualization Results

### Plot Contract

**Question:** does the earlier H2 answer loss produce a faster common-H1 held-out semantic curve without local-language degradation?  
**Data source:** aggregated `curve_metrics.csv`, five paired seeds.  
**Axes:** updates on x; $Q$, accuracy, right-censored token budget, or local CE on y. Shading is the observed seed range.  
**Allowed conclusion:** training fit, held-out ordering, H1/H2 separation, and local probe drift.  
**Limitation:** the lower-left bars use the final token budget when threshold is unreached.

![A11_15 pretrained semantic-transfer curves](figures/a11_15_pretrained_semantic_transfer_efficiency.png)

The dashed train curves reach one, but the solid evaluation curves remain below the sustained threshold. NTP has the higher mean evaluation curve after roughly 100 updates; seed variation is wide. The upper-right panel shows the decisive mismatch: MTP H2 becomes accurate, while common H1 does not gain a stable advantage. The lower-right panel shows greater mean local CE drift for MTP.

## 9. Hypothesis Audit

| Hypothesis | Observation | Decision |
|---|---|---|
| H1 pretrained solvability | neither method reaches sustained $Q\ge0.9$ in any seed | insufficient |
| H1b non-ceiling | both start at $Q=0$ | passed; no ceiling |
| H2 earlier-credit efficiency | MTP AUC higher 2/5, final $Q$ not lower 2/5 | not supported |
| H3 common-head transmission | MTP H2 mean 0.9025, common H1 mean 0.8888 versus NTP 0.9000 | weakened |
| H4 local guard | 0/5 full guard pass | failed |

## 10. Interpretation And Claim Boundary

**Observation:** pretraining enables complete train fit and substantially better unseen-paraphrase transfer than the random model.  
**Interpretation:** pretrained semantic geometry is useful, but a copied private H2 objective can absorb its own target without reliably improving the common H1 decision path.  
**Claim:** this response-position fine-tuning experiment does not support a K=2 MTP common-H1 learning-efficiency advantage.  
**Boundary:** it does not compare pure NTP/MTP pretraining, matched FLOPs, larger models, open-ended generation, or external benchmarks, and it does not prove that MTP is generally harmful.

## 11. Artifact Map

Canonical evidence:

- [summary](summary.md)
- [paired efficiency](tables/paired_efficiency.csv)
- [trajectory summary](tables/trajectory_summary.csv)
- [hypothesis decision](hypothesis_decision.json)
- [central figure](figures/a11_15_pretrained_semantic_transfer_efficiency.png)

Raw result:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
results/a11_15_pretrained_semantic_transfer_efficiency/
a11_15_pretrained_semantic_transfer_efficiency_4gpu_20260710_181900
```

Logs:

```text
.../logs/acp/a11_15_pretrained_semantic_transfer_efficiency_4gpu_20260710_181900
```

Code and configuration:

```text
configs/a11_15_pretrained_semantic_transfer_efficiency.json
scripts/run_a11_15_pretrained_semantic_transfer_efficiency.py
scripts/analyze_a11_14_natural_language_semantic_learning_efficiency.py
scripts/submit_a11_15_pretrained_semantic_transfer_efficiency_4gpu.sh
```

Remote job: `pt-0u9hjxa8`.  
Model file SHA-256: `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`.  
Tokenizer SHA-256: `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`.

## 12. Next Decision

Create A11_16 as a pretrained shared-parameter transmission audit. At fixed checkpoints, measure whether the extra H2 loss gradient through the shared backbone has positive directional usefulness for the held-out common-H1 semantic margin, and verify the first-order prediction with an actual small shared-parameter step. This distinguishes missing transmission from private-head absorption and signed interference without changing the task, K, or model.
