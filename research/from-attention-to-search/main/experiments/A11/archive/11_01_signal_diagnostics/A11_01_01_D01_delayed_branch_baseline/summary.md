# Summary: A11_01 K=2 Branch-Delayed Next-Two

## What We Established

The clean K=2 experiment supports the anchor mechanism. In a deterministic branch-delayed task, fixed-next-one learned the shared next token $A$ but kept the prefix state $h_T$ branch-blind. Next-two learned both $A$ and the branch-specific second token $S_B$, and the same $h_T$ became branch-separable, linearly decodable, and causally sensitive to branch swaps.

This supports the narrow claim that, in the controlled K=2 setting, the second-token loss term gives $h_T$ branch-relevant supervision that next-one at the same position does not give.

It does not prove that multi-token prediction always beats next-token prediction, that next-token prediction cannot learn long-horizon dependencies, that curriculum is superior, or that the same effect transfers to real natural language.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| multi-token prediction | A prefix state predicts more than one future token | here: $h_T$ predicts $Y_1$ and $Y_2$ | objective family | Parent object of the advisor question | Universal improvement |
| next-token prediction | A prefix state predicts only the immediate next token | here: $h_T$ predicts $Y_1$ | objective family | Control objective | Inability to learn long horizon |
| fixed-next-one | Same model architecture, but only offset 1 is trained | active loss $\operatorname{CE}(q_1,A)$ | loss condition | Controls for extra heads/capacity | All next-token behavior |
| next-two | Same $h_T$ predicts offsets 1 and 2 | active loss $\operatorname{CE}(q_1,A)+\operatorname{CE}(q_2,S_B)$ | loss condition | Tests the second-token supervision term | Optimization always succeeds |
| offset2 single-prefix accuracy | Direct prediction of $S_B$ from $h_T$ | top-1 accuracy of $q_2(\cdot\mid h_T)$ | 0 to 1 | Primary metric | Natural-language reasoning |
| frozen probe accuracy | Linear branch readout from frozen $h_T$ | classifier accuracy for $h_T\to B$ | 0 to 1 | Checks representation information | Native head usability |
| branch-swap consistency | Change only the branch token and check suffix prediction | fraction of swaps predicting the new branch suffix | 0 to 1 | Checks causal dependence on early branch | All shortcuts |

## Setup

Data:

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01 A_SHARED S_b STOP
```

The evaluation prefix stops before `A_SHARED`. Therefore $Y_1=A$ is shared across branches, while $Y_2=S_B$ is branch-specific.

Model: one-layer causal Transformer with two direct heads from $h_T$. Branch-token embeddings were initialized identically so that fixed-next-one has no branch-specific symmetry-breaking signal under balanced data.

Seeds: `971,972,973`. Final run: `4000` training steps.

## Main Result

| Condition | Offset-1 accuracy | Offset-2 single-prefix accuracy | Frozen probe accuracy | Branch-swap consistency | Worst-branch offset-2 probability |
|---|---:|---:|---:|---:|---:|
| fixed-next-one | 1.000 | 0.000 | 0.333 | 0.000 | 0.030 |
| next-two | 1.000 | 1.000 | 1.000 | 1.000 | 0.99999 |

Source: `tables/condition_summary.csv`.

Interpretation:

1. Both conditions solved the shared next-token target $A$, so the comparison is not explained by failed basic learning.
2. Fixed-next-one stayed branch-blind: offset-2 accuracy was 0, frozen-probe accuracy was chance for three branches, and branch hidden-state distance was 0.
3. Next-two separated the branch states and made $S_B$ predictable from the same $h_T$: offset-2 accuracy, frozen probe, and branch-swap consistency were all 1.0 across three seeds.

## Boundary

This is an operationalization result, not a new theorem. The theorem already states the objective-level loss gap. The experiment shows that the constructed mechanism can appear in a minimal trainable model when the branch path is not already broken by random initialization.

The result depends on identical branch-token initialization and balanced deterministic data. That is intentional for this first anchor because it isolates objective pressure. A later experiment must remove this symmetry control before claiming robustness.

## Next Decision

Proceed to the next-K planning branch only after documenting this as a closed K=2 support result. The next smallest extension is not curriculum; it is a K>2 branch-controlled suffix test where multiple future tokens share the same early branch cause and local context remains ambiguous.

## Source Artifacts

- Protocol: `protocol.md`
- Detailed record: `detailed.md`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_01_k2_branch_delayed_next_two.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_01_k2_branch_delayed_next_two.json`
- Main result tables: `tables/condition_summary.csv`, `tables/per_seed_metrics.csv`, `tables/branch_swap.csv`
