# Protocol: A06_01_05_E02 MPI Uniform Feature Router

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

## Result Status

This protocol has been executed. It is kept as the reproducibility and
decision-contract record for the completed full run
`a06_26_mpi_full_local2gpu_20260703`.

## Decision Question

Does MPI-style dynamic expert-spectral routing produce stable uniform
feature-to-expert separation on the no-position slot bridge, without using
label-known route-position centers?

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| MPI | One power iteration from router row through expert weights | \(\tilde r_e=r_eW_eW_e^\top\) | Vector in hidden space | Implements the paper's spectral-router mechanism | Full paper setting |
| Retraction | Normalizing the MPI row to fixed scale | \(\hat r_e=C'N^{-1/2}\tilde r_e/\|\tilde r_e\|\) | Router row | Separates scale control from feature awareness | Feature specialization |
| Feature NMI | Agreement between feature id and route expert | NMI(feature, route) | 0--1 | Primary decision metric | Expert utility |
| Margin p05 | Lower-tail matched route margin | 5th percentile of matched expert score minus competitor | Logit difference | Detects whether assignment is stable | Loss optimality |
| Slot-start NMI | Position shortcut guard | NMI(slot_start, route) | 0--1 | Excludes slot-position leakage | All nuisance effects |

## Paper Method Adaptation

The Redesign MoE router paper describes a router row update where each router
row is multiplied by its expert weight operator and then retracted to a fixed
norm before computing logits. The official arXiv HTML exposes the code-shaped
hint with `R`, `wg`, normalization, and a scale factor \(C=C'N^{-1/2}\). The
public TorchTitan patch exposes the same core operation as router row times
expert first-layer transpose times expert first-layer matrix.

This bridge uses a GLU-free expert FFN. Therefore the input-side expert matrix
\(W_e\) is the first linear projection transposed into input space. The tested
row is:

\[
\tilde r_e = r_eW_eW_e^\top,\qquad
\hat r_e=\frac{C'}{\sqrt{N}}\frac{\tilde r_e}{\|\tilde r_e\|_2}.
\]

This is a mechanism-faithful bridge, not a claim of exact architecture-level
reproduction of the paper's large-model experiments.

Sources:

- paper: <https://arxiv.org/abs/2606.12397>
- code:
  <https://github.com/ericshwu/Router-with-Manifold-Power-Iteration/blob/main/torchtitan-patches/ttp/models/aoe4.py>

## Data Construction

The dataset is the same uniform no-position slot bridge used by A06_01_05_E01.

- sequence length: `32`;
- neutral tokens: ids `0--31`;
- feature tokens: ids `32--35`;
- target tokens: ids `36--39`;
- features: `0,1,2,3`, balanced exactly at `0.25` each in calibration and eval;
- slot starts: `2,10,18`, balanced;
- slot lengths: `1,2,4,8`;
- input construction: neutral background, repeated feature token in the slot,
  and the target token immediately after the slot;
- audited route position: final token of the repeated feature slot;
- objective: cross-entropy at the route position for the feature-specific
  target token.

No explicit position embeddings are used.

## Model And Training

- architecture: one causal self-attention layer, one top-1 MoE layer, LM head;
- hidden size: `64`;
- attention heads: `4`;
- experts: `4`;
- expert hidden size: `128`;
- optimizer: AdamW;
- learning rate: `2e-3`;
- weight decay: `1e-4`;
- gradient clipping: `1.0`;
- train steps: `160`;
- train batch size: `256`;
- calibration samples: `2048`;
- eval samples: `2048`;
- eval batch size: `512`;
- checkpoints: `0,10,40,80,160`;
- seeds: `0--7`;
- local GPUs: `2`.

## Conditions

| Condition | Meaning | Role |
| --- | --- | --- |
| `vanilla` | Standard trainable router | Baseline |
| `retract_c1` | Row normalization and \(C'=1\) without MPI | Retraction ablation |
| `mpi_c1` | MPI with \(C'=1\) | Paper-style spectral router |
| `mpi_c2` | MPI with \(C'=2\) | Scale sweep |
| `mpi_c4` | MPI with \(C'=4\) | Scale sweep |
| `mpi_c8` | MPI with \(C'=8\) | Scale sweep |
| `static_svd_init` | Static initial router rows from expert top singular directions | Static spectral baseline |
| `route_centered_init` | K-means on route-position hidden states | Positive control |
| `oracle_centered_init` | Feature-label centers | Upper bound |

## Primary Decision Rule

MPI is promoted as a method candidate only if the best `mpi_c*` condition:

1. reaches route-centered feature NMI within `0.05`;
2. has positive margin p05;
3. keeps max load near balanced usage;
4. keeps slot-start NMI near zero.

If MPI improves over vanilla by at least `0.05` feature NMI but fails the
route-centered and margin tests, it is recorded as a useful spectral baseline,
not a solved specialization method.

## Commands

Smoke run:

```bash
CUDA_VISIBLE_DEVICES=0 python Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E02_manifold_power_iteration/scripts/run_a06_26_mpi_uniform_feature_router.py \
  --run-stage smoke \
  --run-name a06_26_mpi_smoke_local \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E02_manifold_power_iteration
```

Full run:

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --standalone --nproc_per_node=2 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E02_manifold_power_iteration/scripts/run_a06_26_mpi_uniform_feature_router.py \
  --run-stage full \
  --run-name a06_26_mpi_full_local2gpu_20260703 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E02_manifold_power_iteration
```

Log:
`logs/local/a06_26_mpi_full_local2gpu_20260703.log`

## Expected Artifacts

- runner:
  `scripts/run_a06_26_mpi_uniform_feature_router.py`;
- summary JSON:
  `summary.json`;
- tables:
  `tables/data_audit.csv`,
  `tables/training_trajectory.csv`,
  `tables/condition_aggregate_final.csv`,
  `tables/diagnostics_aggregate.csv`;
- figures:
  `figures/final_feature_nmi_by_method.png`,
  `figures/final_margin_p05_by_method.png`,
  `figures/feature_nmi_trajectory_by_method.png`,
  `figures/router_svd_alignment_by_method.png`;
- report:
  `summary.md` and `detailed.md`.
