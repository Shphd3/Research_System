# A11_19 Bridge-Token-Conditioned Transport: Detailed Record

## 1. Decision Question

Does the negative one-position transport found in A11_18 remain negative when only the intervening teacher-forced token changes, or is the cross-position semantic kernel conditioned on that token?

## 2. Model And Operational Definition

For bridge token $b$,

$$
U_b=v_1^\top J_{T+1}^{(b)}J_T^\top d_T,
$$

and its normalized shared-parameter estimate is

$$
\widehat U_b
=-
\frac{\langle\nabla M_{1,T+1}^{(b)},g_D^S\rangle}
{\|\nabla M_{1,T+1}^{(b)}\|\|g_D^S\|}.
$$

The primary statistic is trapezoidal AUC of $\widehat U_b$ over updates `20-200`. Positive values mean that, on average after burn-in, descending the extra H2 loss locally raises the standard H1 semantic margin at the next position.

## 3. Fixed Setup

- model and trajectories: the five Qwen3-0.6B NTP trajectories used by A11_18;
- seeds: `971, 972, 973, 974, 975`;
- checkpoints: `0, 20, 100, 200, 300` updates;
- diagnostic data: seen examples;
- fixed source update: shared-parameter gradient of the extra H2 loss at $h_T$;
- fixed target readout: standard H1 semantic margin at $h_{T+1}$;
- changed variable: one teacher-forced bridge token only.

| Bridge | Token ID | Intended role |
|---|---:|---|
| `Decision` | 40425 | original transition |
| `Answer` | 21806 | answer-format transition |
| `Therefore` | 15277 | discourse continuation |
| `:` | 25 | punctuation transition |

Alternative bridges were not used to train separate trajectories. This isolates diagnostic state-transition geometry but does not estimate adaptation to those bridges.

## 4. Complete Primary Table

| Seed | `Decision` AUC | `Answer` AUC | `Therefore` AUC | `:` AUC |
|---:|---:|---:|---:|---:|
| 971 | -0.0436 | -0.1139 | +0.0495 | +0.2091 |
| 972 | -0.0366 | -0.0718 | +0.0146 | +0.1953 |
| 973 | -0.1126 | -0.2008 | -0.0139 | -0.0172 |
| 974 | -0.1481 | -0.1953 | +0.0409 | +0.0736 |
| 975 | -0.1828 | -0.1858 | +0.0091 | +0.1669 |
| Positive seeds | 0/5 | 0/5 | 4/5 | 4/5 |

Final normalized usefulness at update 300 is negative in all five seeds for `Decision` and `Answer`, and positive in all five for `Therefore` and `:`.

## 5. Guard Audit

The exact restore hashes, curve completeness, and original-bridge reproduction all pass. The maximum shared-checkpoint deviation from A11_18 for `Decision` is `4.2036e-05`, below the `0.02` tolerance.

The preregistered derivative guard required central-difference sign agreement for all four cells within at least four seeds. It passed in only seeds 971-973. The three mismatches are:

| Seed | Bridge | Predicted finite change | Central finite change | Normalized $\widehat U_b$ |
|---:|---|---:|---:|---:|
| 974 | `Decision` | -0.000002 | +0.000329 | -0.000074 |
| 974 | `Therefore` | +0.000119 | -0.001432 | +0.001360 |
| 975 | `Therefore` | +0.001675 | -0.000373 | +0.018837 |

These failures invalidate the formal preregistered verdict. They do not indicate a restore bug or a mismatch in the reproduced A11_18 curve. They show that a sign-only finite-difference guard is unstable when the predicted local change is close to zero.

## 6. Visualization Results

### Central Figure

![Bridge-conditioned transport](figures/a11_19_bridge_token_conditioned_transport.png)

- **Question:** does bridge identity change post-burn-in cross-position usefulness?
- **Data:** five seeds, fixed NTP checkpoints, four diagnostic bridge tokens.
- **Reading:** left is the seed mean at each checkpoint; right counts seeds with positive `20-200` AUC.
- **Observed:** `Decision` and `Answer` become increasingly negative, whereas `Therefore` and `:` are mostly positive.
- **Take-home:** the one-position kernel is not a function of distance alone; it depends materially on the intervening token-conditioned state transition.
- **Limitation:** four bridges, one position, one pretrained model, and diagnostic teacher forcing only.

## 7. Hypothesis Assessment

- **Robust position bottleneck:** descriptively weakened, because two alternatives have positive AUC in `4/5` seeds.
- **Token-conditioned transport:** descriptively supported by the primary trajectories, but not formally supported under the preregistered all-cell derivative guard.
- **Formal experiment status:** insufficient.

The correct scientific reading is therefore two-level: the strict adjudication remains insufficient; the measured trajectory pattern is large, reproducible, and directly relevant to theory construction.

## 8. Claim Boundary

This experiment supports adding the bridge-conditioned transition $J_{T+1}^{(b)}$ to the local theory. It does not establish an all-token law, a long-generation law, a finite downstream gain, or an MTP-over-NTP result on natural tasks.

## 9. Artifact Map

- job: `pt-n84fwtq8`;
- run: `a11_19_bridge_token_conditioned_transport_4gpu_20260711_031500`;
- raw result directory: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_19_bridge_token_conditioned_transport/a11_19_bridge_token_conditioned_transport_4gpu_20260711_031500`;
- canonical table: `tables/bridge_summary.csv`;
- decision record: `hypothesis_decision.json`;
- figure: `figures/a11_19_bridge_token_conditioned_transport.png`;
- config: `configs/a11_19_bridge_token_conditioned_transport.json`;
- runner: `scripts/run_a11_19_bridge_token_conditioned_transport.py`;
- analyzer: `scripts/analyze_a11_19_bridge_token_conditioned_transport.py`;
- submitter: `scripts/submit_a11_19_bridge_token_conditioned_transport_4gpu.sh`.
