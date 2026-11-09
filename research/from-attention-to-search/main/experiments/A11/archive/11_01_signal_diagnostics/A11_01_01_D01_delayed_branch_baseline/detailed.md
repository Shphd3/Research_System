# Detailed: A11_01 K=2 Branch-Delayed Next-Two

## 0. Quick Recap

Purpose: test whether next-two supervision makes the same prefix hidden state $h_T$ predict the branch-specific second future token $S_B$.

Hypothesis: fixed-next-one can learn the shared next token $A$ while remaining branch-blind; next-two should separate branches because it includes $\operatorname{CE}(q_2(\cdot\mid h_T),S_B)$.

Experiment logic: train the same direct-head causal Transformer under two objectives on balanced deterministic K=2 data, then evaluate single-prefix offset-2 prediction, frozen probe, and branch-swap consistency.

Conclusion: the final 4000-step run supports the mechanism across seeds `971,972,973`.

Evidence: fixed-next-one has offset-2 accuracy 0.000, frozen probe 0.333, branch-swap 0.000; next-two has all three metrics at 1.000.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| branch-blind $h_T$ | Prefix state does not distinguish branches | pairwise branch-state distance is 0; probe is chance | condition | The theorem's lower-bound object | Model as a whole lacks branch information |
| offset-2 single-prefix prediction | Predict $S_B$ from the original $h_T$ | top-1 of $q_2(\cdot\mid h_T)$ | accuracy | Primary mechanism test | Natural-language long-range ability |
| branch-swap | Replace only the early branch token | predicted suffix should switch to new branch | rate | Causal guard | All memorization is impossible |
| identical branch initialization | All `BR_b` embeddings start equal | embedding rows copied at initialization | implementation control | Prevents random identity leakage in fixed-next-one | Robustness without symmetry control |

## 2. Protocol Compliance

| Protocol item | Status | Evidence |
|---|---|---|
| Clean K=2 deterministic data | satisfied | `tables/sample_table.csv` |
| Conditions: fixed-next-one and next-two | satisfied | `tables/per_seed_metrics.csv` |
| Seeds 971, 972, 973 | satisfied | `tables/per_seed_metrics.csv` |
| Primary metric: offset-2 single-prefix accuracy | satisfied | `tables/condition_summary.csv` |
| Guards: frozen probe and branch-swap | satisfied | `tables/condition_summary.csv`, `tables/branch_swap.csv` |
| No broad sweep before K=2 closure | satisfied | only step completion after initial partial convergence |

## 3. Data Construction

The sequence template is:

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01 A_SHARED S_b STOP
```

The evaluation prefix is:

```text
BR_b F00 F01 F02 F03 F04 F05 F06 F07 U00 U01
```

At that prefix:

$$
Y_1=A,\qquad Y_2=S_B.
$$

The first target is shared across branches. The second target is branch-specific and one-to-one with branch id.

## 4. Model And Objective

The model is a one-layer causal Transformer with token embeddings, position embeddings, one causal attention block, and two direct output heads from the final prefix state $h_T$.

The fixed-next-one condition uses:

$$
\mathcal L_{\mathrm{fixed1}}=\operatorname{CE}(q_1(\cdot\mid h_T),A).
$$

The next-two condition uses:

$$
\mathcal L_{\mathrm{next2}}=\operatorname{CE}(q_1(\cdot\mid h_T),A)+\operatorname{CE}(q_2(\cdot\mid h_T),S_B).
$$

Branch embeddings are initialized identically. Under balanced data, this makes fixed-next-one preserve branch symmetry unless the objective provides branch-specific gradients.

## 5. Results

### Final 4000-Step Run

| Condition | Offset-1 accuracy | Offset-2 accuracy | Frozen probe | Branch-swap | Worst-branch probability | Min branch-state distance |
|---|---:|---:|---:|---:|---:|---:|
| fixed-next-one | 1.000 | 0.000 | 0.333 | 0.000 | 0.030 | 0.000 |
| next-two | 1.000 | 1.000 | 1.000 | 1.000 | 0.99999 | 13.986 |

Source: `tables/condition_summary.csv`.

Observation: fixed-next-one learned $A$ but did not expose branch information in $h_T$. Next-two learned $A$, predicted $S_B$, separated branch states, and passed the intervention guard.

Interpretation: the result supports the anchor mechanism that the second-token term supplies branch-relevant pressure on the same prefix state.

### Per-Seed Stability

All three final-run seeds satisfy the pass pattern:

- fixed-next-one: `offset1_accuracy=1.0`, `offset2_single_prefix_accuracy=0.0`, `frozen_probe_accuracy=0.333`, `branch_swap_consistency=0.0`;
- next-two: `offset1_accuracy=1.0`, `offset2_single_prefix_accuracy=1.0`, `frozen_probe_accuracy=1.0`, `branch_swap_consistency=1.0`.

Source: `tables/per_seed_metrics.csv`.

### Initial 1200-Step Check

An initial 1200-step run showed next-two partial convergence on seed `972`: offset-2 accuracy and frozen probe reached 0.667, while the other two seeds reached 1.0. This was treated as insufficient convergence, not as a mechanism failure. The final 4000-step run resolves this instability.

Raw initial run path:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_01_k2_branch_delayed_next_two/a11_01_k2_branch_delayed_next_two_remote_20260706_1704`

## 6. Visualization Results

No central figure is needed for the main reading path. The decisive evidence is tabular and fully specified by the primary metric plus two guards.

Plot contract if a figure is later added:

- question answered: whether next-two separates branch states while fixed-next-one remains branch-blind;
- metric: offset-2 accuracy, frozen probe, branch-swap, and hidden-state pairwise distance;
- allowed conclusion: controlled K=2 operational support;
- limitation: no natural-language or curriculum claim.

## 7. Failure Decomposition

The result blocks the main rival explanations for this first anchor:

| Rival explanation | Evidence against it | Remaining uncertainty |
|---|---|---|
| More heads/capacity caused success | both conditions used the same direct-head architecture | architecture family remains narrow |
| Native offset-2 head artifact | frozen probe is 1.0 for next-two and chance for fixed-next-one | probe is deterministic and minimal |
| Local context leakage | branch-swap consistency is 1.0 only for next-two | harder noisy contexts not tested |
| Fixed-next-one failed basic learning | fixed-next-one offset-1 accuracy is 1.0 | only this controlled objective tested |

## 8. Artifact Map

Code workspace:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:

`active/synthetic_data_understanding/scripts/run_a11_01_k2_branch_delayed_next_two.py`

Config:

`active/synthetic_data_understanding/configs/a11_01_k2_branch_delayed_next_two.json`

Optional ACP submitter:

`active/synthetic_data_understanding/scripts/submit_a11_01_k2_branch_delayed_next_two_4gpu.sh`

Final result dir:

`active/synthetic_data_understanding/results/a11_01_k2_branch_delayed_next_two/a11_01_k2_branch_delayed_next_two_remote_20260706_1708`

Curated mainline tables:

- `tables/condition_summary.csv`
- `tables/per_seed_metrics.csv`
- `tables/branch_probabilities.csv`
- `tables/branch_swap.csv`
- `tables/training_history.csv`
- `tables/sample_table.csv`

Run command:

```bash
python active/synthetic_data_understanding/scripts/run_a11_01_k2_branch_delayed_next_two.py \
  --config active/synthetic_data_understanding/configs/a11_01_k2_branch_delayed_next_two.json \
  --run-name a11_01_k2_branch_delayed_next_two_remote_20260706_1708 \
  --device cuda
```

Job id: none. The final run executed directly in the current remote container. The visible runtime hardware had 2 H100 GPUs; a dry-run 4-GPU ACP submitter was created but not submitted.

## 9. Claim Boundary

Can claim:

In this controlled K=2 distribution and direct-head model, next-two supplies branch-relevant supervision that makes $h_T$ predict $S_B$, while fixed-next-one can solve the shared next token with branch-blind $h_T$.

Cannot claim:

MTP always beats NTP; NTP cannot learn long-horizon dependencies; curriculum is better than full-horizon; this synthetic result transfers to real natural language; optimization will always succeed without the symmetry control.

## 10. Next Decision

Update the anchor as supported for the clean K=2 mechanism, then move to the smallest next-K extension: K>2 branch-controlled suffixes where multiple future tokens share the same early branch cause. The next experiment should remove or weaken one control at a time, starting with longer branch-specific suffixes before noisy filler or curriculum.
