# Summary: A11_14 Natural-Language Semantic Learning Efficiency

Primary anchor: [11_14_natural_language_semantic_learning_efficiency_anchor.md](../../../problem_anchors/11_informative_future_branch_mechanism/11_14_natural_language_semantic_learning_efficiency_anchor.md)
Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Verdict:** insufficient evidence; the full run is valid, but neither method makes the common downstream task adjudicable.

**Direct result:** NTP and K=2 MTP both reach the final 5,000-update budget without attaining $Q_{downstream}\ge0.9$ in any seed. Therefore $T_{0.9}$ and a method-efficiency ordering are not identifiable. MTP has lower $Q$-AUC in 5/5 seeds, but this cannot be promoted to "MTP is worse" because both methods fail the protocol's solvability gate.

**Failure localization:** both methods learn ordinary prompt next-token structure: final non-answer H1 accuracy is `0.921-0.942`, and all five local guards pass. The unresolved term is state-dependent answer behavior. Final counterfactual sensitivity is only `0.238-0.363` for NTP and `0.000-0.375` for MTP. In three MTP seeds the H2 answer remains exactly at chance and produces constant predictions.

**Next action:** do not lengthen training or broaden tasks. Create one decision-weighted all-position follow-up that prevents the single answer position from being diluted by roughly 380 prompt positions while preserving the ordinary LM objective.

## Setup And Primary Metric

The fixed sequence is:

```text
<BOS> cue + 256-word intervening history + request/options
<EOP> <DECIDE> <ANSWER>
```

NTP trains $L_1^{all}$; MTP trains $L_1^{all}+L_2^{all}$. Both are evaluated through the same full-vocabulary H1 argmax at `<DECIDE>`.

$$
Q_{downstream}
=\min\{A_{H1},C_{para}^{model},S_{cf}^{model}\}.
$$

The ten remote tasks use seeds `971-975`, identical paired initializations and minibatches, a two-layer causal Transformer, AdamW, and 5,000 updates.

## Validity

All implementation guards pass:

- 10/10 tasks and 12/12 checkpoints per task;
- identical shared/H2 initialization hashes within every seed;
- identical train/evaluation sample, vocabulary, and batch hashes;
- identical cumulative processed tokens at every paired checkpoint;
- no answer special token in the prompt;
- all values finite;
- train/evaluation split sizes `160/160`.

The remote four-H100 job `pt-xfvrymp5` completed successfully.

## Results

| Seed | NTP final $Q$ | MTP final $Q$ | NTP H1 acc. | MTP H1 acc. | NTP $S_{cf}$ | MTP $S_{cf}$ | MTP H2 acc. |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 971 | 0.3125 | 0.0000 | 0.5938 | 0.5000 | 0.3125 | 0.0000 | 0.5000 |
| 972 | 0.2875 | 0.3750 | 0.6312 | 0.6000 | 0.2875 | 0.3750 | 0.6188 |
| 973 | 0.3625 | 0.3000 | 0.6438 | 0.6250 | 0.3625 | 0.3000 | 0.5000 |
| 974 | 0.2375 | 0.3375 | 0.5688 | 0.6438 | 0.2375 | 0.3375 | 0.6250 |
| 975 | 0.3375 | 0.0000 | 0.6062 | 0.5000 | 0.3375 | 0.0000 | 0.5000 |

The standard full-vocabulary H1 accuracy equals the restricted A/B choice accuracy at the final checkpoint in every run. Thus the failure is not an evaluation artifact in which the model ranks the correct answer among A/B but emits another vocabulary token.

## Central Figure

![A11_14 unweighted learning curves](figures/a11_14_learning_efficiency.png)

**What it tests:** common-H1 semantic recovery, private-H2 versus common-H1 behavior, paired threshold time, and local next-token learning.

**Observed result:** neither curve approaches the 0.9 threshold; threshold bars are final-budget censoring bars, not measured crossing times. Ordinary H1 CE falls sharply and remains similar across methods. H2 improves only in two MTP seeds and does not make the common task reliable.

**Allowed conclusion:** uniform all-position training on this small random-initialized model does not yield an adjudicable semantic-efficiency comparison at the tested budget.

**Not allowed:** MTP is worse than NTP, MTP cannot learn natural-language semantics, or the A11_12 earlier-credit mechanism is false.

## Failure Analysis

Each sequence contains `357-383` model tokens, while the behaviorally decisive answer contributes one position to each horizon average. The optimizer succeeds on the repeated prompt language but the answer gradient is diluted. This is visible in final local H1 accuracy above `0.92` alongside answer accuracy near `0.5-0.64` and low counterfactual sensitivity.

The next experiment should preserve $L_1^{all}$ and $L_2^{all}$, but add an explicit decision loss at the common H1 answer position for both methods and the matched earlier H2 answer loss only for MTP. This is the minimal bridge to a supervised downstream decision; it is not a broader ablation.

## Claim Boundary

**Can claim:** the unweighted all-position small model is not an adjudicable test of semantic learning efficiency; local LM learning succeeds while distant state-conditioned decisions remain weak.

**Cannot claim:** either objective is intrinsically better or worse; more steps would solve the problem; pretrained LLMs behave similarly; decision weighting proves real pretraining efficiency.

