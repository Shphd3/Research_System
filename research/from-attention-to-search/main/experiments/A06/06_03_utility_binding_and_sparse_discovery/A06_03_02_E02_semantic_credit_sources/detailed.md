# A06_03_02_E02 Semantic-Credit Source Decomposition: Detailed Record

## Decision

H3, the dual-bottleneck hypothesis, is supported. Full-LM background positions
systematically oppose useful-route correction, while selected-only top-1 still
fails in most rank-2 cells and every rank-4 cell after background removal.

## Protocol Compliance

| Contract | Measured evidence | Status |
| --- | --- | --- |
| 32 seeds, four tasks | 32 seeds, 128 cells/condition | pass |
| Learned specialist advantage | median `8.894682` | pass |
| Installed useful rank | minimum accuracy `1.0` | pass |
| Adjacent score separation | minimum p05 `0.472443` | pass |
| Balanced initial load | maximum spread `0` | pass |
| Gradient source closure | maximum relative error `3.2983e-7` | pass |
| Half-task scale identity | maximum relative error `0.0` | pass |
| Soft positive control | rank 2 and rank 4 both `128/128` | pass |
| Remote full run | ACP `pt-t897a1ag`, `SUCCEEDED` | pass |

## Data And Model

For task \(f\in\{0,1,2,3\}\) and content \(c\), each sequence starts with the task
token and alternates content token \(c\) with transformed token
\((c+f)\bmod 4\). Each sequence has 33 tokens. Its 32 next-token targets split
exactly into 16 transformed task targets and 16 content/background targets.
Content orders are balanced and disjoint between train and test.

The model contains one causal self-attention layer, residual connection,
LayerNorm, and four MLP experts. No learned position embedding is used. Experts
first receive 200 route-conditioned exposure updates. During A06_03_02_E02 correction,
all non-router parameters are frozen.

## Mathematical Audit

With internally averaged task and background losses,

\[
g_{full}=\tfrac12g_{task}+\tfrac12g_{background}.
\]

The measured maximum relative closure error is `3.2983e-7`. The half-task
gradient equals \(0.5g_{task}\) with zero measured relative error. Therefore the
causal difference between full and task-only branches is not an implementation
or normalization artifact.

For task center \(\mu_f\), useful expert \(u\), and selected expert \(r\),

\[
m_{u,r}=(w_u-w_r)^\top\mu_f,
\qquad
P_q=-\langle g_u^q-g_r^q,\mu_f\rangle.
\]

At rank 2, task pressure has median `2.610600`, with 5th/95th percentiles
`-0.905057/8.443366` and positive fraction `0.835938`. Background pressure has
median `-9.081992`, 5th/95th percentiles `-11.622051/-7.380539`, and positive
fraction `0`. Full pressure has median `-3.328575` and is positive in only
`0.023438` of cells. Rank 4 has the same sign pattern.

## Complete Condition Results

| Condition | Correction | Median capped time | Median normalized regret | Median final task loss | Median final useful probability |
| --- | ---: | ---: | ---: | ---: | ---: |
| rank-2 full top-1 | 0.0000 | 301 | 1.0133 | 6.3844 | 0.2188 |
| rank-2 task top-1 | 0.3281 | 301 | 0.9915 | 5.7087 | 0.3037 |
| rank-2 half-task top-1 | 0.1484 | 301 | 0.9947 | 5.9308 | 0.3004 |
| rank-2 background top-1 | 0.0000 | 301 | 1.1398 | 7.9097 | 0.0769 |
| rank-2 task soft | 1.0000 | 19 | 0.1149 | 0.0566 | 0.6508 |
| rank-4 full top-1 | 0.0000 | 301 | 1.0132 | 6.3817 | 0.0877 |
| rank-4 task top-1 | 0.0000 | 301 | 0.9917 | 6.1095 | 0.1077 |
| rank-4 half-task top-1 | 0.0000 | 301 | 0.9948 | 6.1617 | 0.1078 |
| rank-4 background top-1 | 0.0000 | 301 | 1.1401 | 7.9107 | 0.0396 |
| rank-4 task soft | 1.0000 | 69 | 0.1961 | 0.0744 | 0.6189 |

The median capped-time difference between full and task-only rank-2 branches is
zero because more than half of task-only cells remain censored at step 301.
Correction-rate improvement is therefore the decisive source effect; relying
only on median time would hide the `42/128` recovered cells.

## Visualization Results

### Initial Source Pressure

![Initial source pressure](figures/initial_source_pressure.png)

- Question: which position source initially raises or lowers useful margin?
- Aggregation: median over 32 seeds and four tasks at installed rank 2.
- Reading: values above zero favor useful expert crossing.
- Result: task is positive; background is larger and negative; full is negative.
- Limitation: this is local pressure, not a finite-time crossing guarantee.

### Causal Branch Trajectories

![Causal branch trajectories](figures/source_branch_trajectories.png)

- Question: does removing background or exposing expert utility resolve the basin?
- Aggregation: checkpoint-wise median over 128 rank-2 cells.
- Result: task masking produces only a small probability increase; soft utility
  coverage produces decisive probability growth and regret removal.
- Limitation: soft uses all four experts and is not a compute-matched method.

## Failure Decomposition

The result requires a rank-dependent dual-bottleneck model:

\[
\Delta m_{u,r}
\approx \eta\left(P_{semantic}+P_{background}
+P_{coverage}\right).
\]

\(P_{background}<0\) explains why full top-1 moves away from the useful expert.
Removing it exposes \(P_{semantic}>0\), which is enough for some rank-2 cells but
not for the larger rank-4 barrier. Soft routing adds utility-bearing feedback
from the unselected useful expert, making the crossing reliable. This equation
is a mechanism decomposition; the separate terms are intervention-defined and
are not yet available without oracle masks or additional expert evaluation.

## Claim Boundary

Supported: both position-source credit and candidate utility coverage causally
matter in this controlled learned-specialist system.

Not supported: natural-language semantic masks, MTP-derived routing credit,
semantic expert identity in a pretrained LLM, top-2 sufficiency, or efficiency
per activated FLOP.

## Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`
- Protocol: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_02_E02_semantic_credit_sources/protocol.md`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_41_semantic_credit_source_decomposition.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_41_semantic_credit_source_decomposition.json`
- Submitter: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_41_semantic_credit_source_decomposition_4gpu_acp.sh`
- Raw result: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_41_semantic_credit_source_decomposition/a06_41_full_4gpu_20260711_01/`
- Curated tables: `tables/condition_summary.csv`, `tables/paired_comparisons.csv`, `tables/decision_summary.json`
- Curated figures: `figures/initial_source_pressure.png`, `figures/source_branch_trajectories.png`
- ACP job: `pt-t897a1ag`

Reproduction:

```bash
A0641_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_a06_41_semantic_credit_source_decomposition_4gpu_acp.sh
```
