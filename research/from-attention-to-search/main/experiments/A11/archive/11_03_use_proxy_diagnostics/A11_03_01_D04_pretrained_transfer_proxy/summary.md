# A11_15 Pretrained Semantic-Transfer Efficiency: Summary

## What We Established

The paired four-GPU run is valid, but it does **not** establish a K=2 MTP semantic-learning efficiency advantage. Both methods fit every training paraphrase, yet neither reaches the held-out semantic threshold in any seed. MTP learns its private H2 answer head, but that gain does not reliably improve the common H1 downstream behavior.

**Decision:** insufficient evidence for semantic-efficiency ordering. The next experiment should audit shared-parameter gradient transmission, not tune another loss weight or expand K.

## Terminology / Definitions

The task presents an early user state, inserts a long distractor span, and asks for a later A/B decision whose correct answer depends on that state. Training uses cue paraphrases `0,1`; evaluation uses unseen paraphrases `2,3`.

For the standard next-token head H1:

$$
A_{H1}=\frac{1}{N}\sum_i \mathbf 1[\arg\max_v p_1(v\mid X_i)=Y_i].
$$

Paraphrase consistency $C_{para}$ is the fraction of same-state paraphrase groups receiving the same H1 answer. Counterfactual sensitivity $S_{cf}$ is the fraction of paired examples for which changing only the early state flips the H1 answer. The primary score is:

$$
Q_{eval}=\min\{A_{H1},C_{para},S_{cf}\}.
$$

This minimum prevents high answer accuracy from hiding failure to preserve meaning across paraphrases or respond to state interventions. It cannot by itself identify which gradient path caused a prediction.

Threshold time $T_{0.9}$ is the earliest processed-token count whose checkpoint begins three consecutive evaluations with $Q_{eval}\ge0.9$. Token-AUC is the trapezoidal area under $Q_{eval}$ versus processed tokens, normalized by the token interval.

## Setup

- model: pretrained `Qwen3-0.6B-Base`, full-model bfloat16 fine-tuning;
- fixed A11_13 256-word task, 160 train and 160 held-out examples per seed;
- NTP: $L_S+L_I$; K=2 MTP: $L_S+L_I+L_D$;
- $L_I$ is the common H1 answer loss after the shared `Decision` token; $L_D$ predicts the same answer one position earlier through H2;
- 300 updates, batch size 4, AdamW `1e-5`, seeds `971-975`;
- paired examples, text tokens, update count, initialization, batch schedule, and pretrained checkpoint;
- remote job `pt-0u9hjxa8`, 10/10 tasks complete.

This is response-position fine-tuning. It is not pure all-position MTP pretraining and does not match FLOPs.

## Primary Evidence

| Metric | NTP | K=2 MTP | Decision |
|---|---:|---:|---|
| evaluation threshold reached | 0/5 | 0/5 | efficiency not adjudicable |
| final train $Q$ | 1.000 in 5/5 | 1.000 in 5/5 | both fit seen wording |
| mean final evaluation $Q$ | 0.825 | 0.8125 | no reliable MTP gain |
| final evaluation $Q$ range | 0.750-0.900 | 0.750-0.8625 | counterfactual transfer remains incomplete |
| MTP token-AUC higher | - | 2/5 | not supported |
| MTP final $Q$ not lower | - | 2/5 | not supported |
| mean final common-H1 accuracy | 0.900 | 0.8888 | no common-head advantage |
| mean final private-H2 accuracy | 0.000 | 0.9025 | MTP directly fits H2 |
| local-language guard pass | - | 0/5 | both drift; MTP exceeds its step-0 CE limit in every seed |

The limiting component is usually $S_{cf}$: its mean final value is `0.825` for NTP and `0.8125` for MTP. At the domain level, the morning/evening availability state is hardest (`0.6687` NTP, `0.6125` MTP), while three domains are near or at one.

## Visualization Results

### Plot Contract

**Question:** does pretrained K=2 MTP reach the common-H1 held-out semantic criterion earlier than NTP?  
**How to read:** solid curves are evaluation $Q$; dashed curves are train $Q$; the upper-right panel separates common H1 from private H2; the lower-right panel is non-answer next-token cross-entropy.  
**Allowed conclusion:** identify train fit, held-out transfer, private-head absorption, and local-language cost.  
**Limitation:** unreached threshold bars show the final budget, not a measured threshold time.

![A11_15 pretrained semantic-transfer curves](figures/a11_15_pretrained_semantic_transfer_efficiency.png)

Both train curves reach one. Evaluation improves late but remains below the sustained threshold. MTP H2 reaches roughly the same final accuracy as the common H1, while common-H1 $Q$ does not improve over NTP. This directly rules out interpreting H2 fitting as downstream semantic efficiency.

## Hypothesis Decisions

| Hypothesis | Result | Decision |
|---|---|---|
| pretrained held-out solvability | 0/5 threshold reach for both | insufficient |
| earlier-credit efficiency | AUC and final-$Q$ wins only 2/5 | not supported |
| common-head transmission | H2 improves to 0.9025 mean without H1 advantage | weakened |
| local pretrained guard | 0/5 | failed |

## Claim Boundary And Next Decision

We can say that pretrained semantics substantially improves held-out transfer over the random model, but this response-position K=2 objective does not yield a reliable common-H1 efficiency advantage. We cannot say that MTP is worse in general, because the run never crossed the preregistered solvability gate and is not a pretraining comparison.

The next minimal decision is whether the extra H2 loss has positive shared-parameter directional usefulness for the held-out common-H1 semantic margin. If that transmission is absent or signed inconsistently, private H2 fitting is the expected outcome and a stronger MTP claim must require an explicit coupling condition.
