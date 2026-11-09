# Summary: A11_14b Decision-Weighted Semantic Efficiency

Primary anchor: [11_14b_decision_weighted_semantic_efficiency_anchor.md](../../../problem_anchors/11_informative_future_branch_mechanism/11_14b_decision_weighted_semantic_efficiency_anchor.md)
Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Verdict:** insufficient for held-out semantic efficiency, with a clear train-to-paraphrase transfer failure.

**What changed:** both methods retain their all-position objectives and receive the same order-one H1 answer loss. MTP additionally receives the matched earlier H2 answer loss. This repairs the answer-position dilution seen in A11_14.

**Direct result:** train fitting becomes strong, but held-out paraphrase recovery remains weak. Final train $Q$ is `0.80-1.00` for NTP and `0.90-1.00` for MTP. Final evaluation $Q$ is only `0.30-0.35` for NTP and `0.2375-0.4375` for MTP. Neither condition reaches evaluation $Q\ge0.9$ in any seed, so evaluation $T_{0.9}$ remains unidentifiable.

**Method comparison boundary:** MTP has higher evaluation AUC in 2/5 seeds and higher final evaluation $Q$ in 2/5. It fits train $Q$ at least as well as NTP in 4/5 seeds, and its private H2 answer accuracy reaches `0.575-0.688`, but this does not yield a seed-consistent common-H1 transfer advantage.

**What we do next:** stop tuning the random-initialized small model. The next bridge should use a pretrained small language model whose lexical and paraphrase geometry already connects unseen phrasings.

## Objective

$$
L_{NTP}^{dw}=L_1^{all}+L_I,
$$

$$
L_{MTP}^{dw}=L_1^{all}+L_2^{all}+L_I+L_D.
$$

$L_I$ is the standard H1 answer loss at `<DECIDE>` for both methods; $L_D$ is MTP's earlier H2 answer loss at `<EOP>`.

## Key Results

| Seed | NTP train $Q$ | MTP train $Q$ | NTP eval $Q$ | MTP eval $Q$ | NTP eval AUC | MTP eval AUC |
|---:|---:|---:|---:|---:|---:|---:|
| 971 | 0.800 | 0.900 | 0.3000 | 0.2875 | 0.2725 | 0.2309 |
| 972 | 0.900 | 1.000 | 0.3500 | 0.2875 | 0.2738 | 0.2434 |
| 973 | 1.000 | 1.000 | 0.3375 | 0.4375 | 0.3266 | 0.3355 |
| 974 | 1.000 | 0.900 | 0.3000 | 0.2375 | 0.3033 | 0.2821 |
| 975 | 0.925 | 1.000 | 0.3250 | 0.3625 | 0.2998 | 0.3165 |

All five local H1 guards pass. Final non-answer H1 accuracy is `0.908-0.917` for NTP and `0.919-0.924` for MTP. The failure is not local forgetting.

## Central Figure

![A11_14b decision-weighted learning curves](figures/a11_14b_decision_weighted_learning_efficiency.png)

**How to read:** dashed curves are train $Q$ and solid curves are held-out paraphrase $Q$. Both train curves rise toward or above 0.9, while evaluation curves remain near 0.3. The H2 panel shows that MTP trains its private direct head, but common H1 transfer stays inconsistent.

**Allowed conclusion:** explicit decision weighting repairs fitting but does not make a random-initialized two-layer model a valid semantic-generalization test.

**Not allowed:** MTP is worse, MTP's earlier path is absent, or decision weighting proves a natural-language benefit.

## Claim Boundary

**Can claim:** the current bottleneck is held-out paraphrase transfer, not task construction, answer dilution, implementation, or local LM learning. A random-initialized two-layer model can fit the training phrasings but does not ground unseen phrasings into the same semantic state reliably.

**Cannot claim:** NTP or MTP has a natural-language efficiency advantage; a larger random model would solve the issue; pretrained language models will preserve the same ordering.

