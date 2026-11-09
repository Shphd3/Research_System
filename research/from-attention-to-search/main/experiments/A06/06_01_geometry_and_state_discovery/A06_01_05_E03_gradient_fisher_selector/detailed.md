# Detailed Report: A06_01_05_E03 Gradient/Fisher Route-State Selector

## 1. Decision

The experiment supports a bounded gradient-selector method candidate on the
uniform no-position synthetic bridge. Embedding-gradient top1 and
embedding-gradient direction select a route-relevant population and produce
perfect feature routing with positive margins after warmup 40.

The experiment rejects Fisher-only subspace clustering as a finished method:
it improves feature NMI but leaves margin p05 negative.

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Uniform feature | Four features sampled equally | Feature ids 0--3 balanced in calibration/evaluation | probability 0.25 each | Removes frequency skew | Real language semantics |
| Route position | Task-relevant prediction position | Final token of repeated feature slot | sequence index | Positive control for valid hidden-state population | Label-free real route selection |
| Post-hidden gradient | Gradient at router-input hidden states | \(\nabla_{h_{i,p}}\mathcal L_i\) after attention and layer norm | vector | Tests direct MoE state sensitivity | Semantic feature discovery |
| Embedding gradient | Gradient at embedding output | Gradient before attention | vector | Tests causal context sensitivity | Router-ready representation alone |
| Gradient top1 | Hard selector | one token per sample with largest gradient energy | index | Tests route-state localization | Feature separation by itself |
| Gradient direction | Direction classifier | k-means on normalized selected gradients, then average selected hidden states | router rows | Tests whether gradient direction carries feature/class grouping | Margin optimality |
| Fisher subspace | Loss-sensitive geometry | top eigenspace of \(\mathbb E[gg^\top]\) | projection basis | Tests metric reweighting | Positive routing margin |
| Feature NMI | Feature/route agreement | NMI(feature id, routed expert) | 0--1 | Primary separation metric | Expert utility |
| Margin p05 | Lower-tail safety gap | 5th percentile matched logit gap | logit difference | Preservation guard | Global optimum |

## 3. Data And Model

Data construction follows A06_01_05_E01/A06_01_05_E02.

- sequence length: `32`;
- neutral tokens: ids `0--31`;
- feature tokens: ids `32--35`;
- target tokens: ids `36--39`;
- features: `0,1,2,3`, balanced exactly in calibration/evaluation;
- slot starts: `2,10,18`, balanced;
- slot lengths: `1,2,4,8`;
- route position: final token of repeated feature slot;
- objective: cross-entropy at the route position for the feature-specific
  target token.

Model:

- one causal self-attention layer;
- weighted top-1 MoE layer;
- four experts;
- hidden size `64`;
- expert hidden size `128`;
- no explicit position embeddings;
- LM head over synthetic vocabulary.

Training:

- seeds: `0--7`;
- slot lengths: `1,2,4,8`;
- warmup steps: `0,10,40`;
- post-reset checkpoints: `0,10,40,80,160`;
- train batch size: `256`;
- calibration/evaluation samples: `2048`;
- optimizer: AdamW, learning rate `2e-3`, weight decay `1e-4`;
- local run: `2` distributed ranks;
- completed cells: `32/32`;
- training trajectory rows: `5760`.

## 4. Compared Conditions

| Condition | Meaning | Role |
| --- | --- | --- |
| `allpos_centered` | k-means on all centered hidden states | failure baseline |
| `route_centered` | k-means on route-position hidden states | positive control |
| `oracle_centered` | feature-label centers | upper bound |
| `grad_h_topk_centered` | top-1 post-hidden gradient selector | hard route-state selector |
| `grad_h_weighted_centered` | post-hidden gradient-weighted k-means | soft selector |
| `grad_h_direction_centered` | post-hidden gradient-direction clusters | direction classifier |
| `fisher_h_topdim_centered` | post-hidden Fisher eigenspace k-means | metric test |
| `grad_emb_topk_centered` | top-1 embedding-gradient selector | causal-context selector |
| `grad_emb_weighted_centered` | embedding-gradient-weighted k-means | soft causal selector |
| `grad_emb_direction_centered` | embedding-gradient-direction clusters | direction classifier |
| `fisher_emb_topdim_centered` | embedding-gradient Fisher eigenspace k-means | metric test |

## 5. Full Results

### 5.1 Immediate Routing At Warmup 40

| Method | Feature NMI | Margin p05 | Preserve | Slot-start NMI | Max load |
| --- | ---: | ---: | ---: | ---: | ---: |
| `grad_emb_direction_centered` | 1.000 | 8.801 | 1.000 | 0.001 | 0.250 |
| `grad_emb_topk_centered` | 1.000 | 10.083 | 1.000 | 0.001 | 0.250 |
| `oracle_centered` | 1.000 | 10.083 | 1.000 | 0.001 | 0.250 |
| `route_centered` | 0.996 | 9.456 | 0.992 | 0.001 | 0.258 |
| `grad_h_topk_centered` | 0.990 | 8.794 | 0.981 | 0.005 | 0.266 |
| `grad_h_direction_centered` | 0.988 | 7.634 | 0.980 | 0.004 | 0.266 |
| `grad_h_weighted_centered` | 0.984 | 6.929 | 0.972 | 0.005 | 0.273 |
| `grad_emb_weighted_centered` | 0.976 | 5.983 | 0.957 | 0.007 | 0.289 |
| `fisher_h_topdim_centered` | 0.910 | -2.516 | 0.863 | 0.003 | 0.375 |
| `fisher_emb_topdim_centered` | 0.879 | -4.619 | 0.800 | 0.002 | 0.431 |
| `allpos_centered` | 0.876 | -4.399 | 0.799 | 0.001 | 0.420 |
| `no_reinit` | 0.816 | -3.154 | 0.695 | 0.001 | 0.523 |

### 5.2 Final Routing At Warmup 40

| Method | Feature NMI | Margin p05 | Preserve | Slot-start NMI | Max load |
| --- | ---: | ---: | ---: | ---: | ---: |
| `grad_emb_direction_centered` | 1.000 | 8.040 | 1.000 | 0.001 | 0.250 |
| `grad_emb_topk_centered` | 1.000 | 9.609 | 1.000 | 0.001 | 0.250 |
| `oracle_centered` | 1.000 | 9.290 | 1.000 | 0.001 | 0.250 |
| `route_centered` | 0.996 | 8.844 | 0.984 | 0.001 | 0.258 |
| `grad_h_topk_centered` | 0.992 | 8.298 | 0.977 | 0.001 | 0.266 |
| `grad_h_direction_centered` | 0.992 | 6.582 | 0.969 | 0.001 | 0.266 |
| `fisher_h_topdim_centered` | 0.925 | -2.956 | 0.812 | 0.001 | 0.381 |
| `fisher_emb_topdim_centered` | 0.915 | -3.944 | 0.781 | 0.001 | 0.398 |
| `allpos_centered` | 0.899 | -3.725 | 0.789 | 0.001 | 0.430 |

### 5.3 Slot-Length Robustness At Warmup 40

`grad_emb_topk_centered` has feature NMI `1.000`, positive margin, and preserve
`1.000` for slot lengths `1,2,4,8`.

| Slot length | Feature NMI | Margin p05 | Preserve |
| ---: | ---: | ---: | ---: |
| 1 | 1.000 | 9.359 | 1.000 |
| 2 | 1.000 | 9.885 | 1.000 |
| 4 | 1.000 | 10.425 | 1.000 |
| 8 | 1.000 | 10.665 | 1.000 |

## 6. Visualization Results

### Figure 1: Core NMI And Margin

![Core result](figures/a06_27_core_reinit_nmi_margin.png)

Question answered: which signal form creates immediate feature separation and
positive lower-tail margin?

How to read: left panel shows feature NMI; right panel shows margin p05. The
zero line in the margin panel is the minimum requirement for a positive routing
buffer.

Observed result: embedding-gradient top1 and embedding-gradient direction reach
NMI `1.000` and positive margin at warmup 40. Fisher improves NMI but remains
below zero margin.

Take-home: use embedding-gradient top1/direction as the next method candidate;
do not use Fisher-only clustering as the method.

Limitation: the figure is synthetic and does not establish real-DCLM transfer.

### Figure 2: Signal Role Share

![Signal role share](figures/a06_27_gradient_signal_role_share_w40.png)

Question answered: where does the selector signal live?

How to read: bars show the fraction of nonnegative gradient/Fisher signal mass
on route, slot, and target positions. Route is a subset of slot, so the bars do
not sum to one.

Observed result: post-hidden gradients are exactly route-local. Embedding
gradients place most mass on route/slot positions and zero on the target token.

Take-home: the method works by selecting the route-relevant population. This is
a valid selector result, not semantic evidence.

Limitation: in this synthetic setup the loss is evaluated at a known route
position, so post-hidden gradient locality is partly built into the objective.

## 7. Mechanism Interpretation

The evidence separates three signal forms.

1. Gradient magnitude selects route-relevant states. Post-hidden gradient is
   route-local by construction in this pointwise loss, while embedding
   gradient also highlights the causal slot region.
2. Gradient direction carries feature/class information strongly enough to
   produce router rows with perfect feature NMI and positive margins after
   warmup.
3. Fisher subspace is an incomplete metric change. It increases NMI over
   all-position clustering but does not thicken the lower-tail margin.

Therefore the next method should not be "Fisher metric only." It should be a
gradient-selected route-state initialization method, with margin-thickening
guards.

## 8. Claim Boundary

Supported:

- label-free task-gradient signals can identify a route-relevant hidden-state
  population on the uniform no-position bridge;
- embedding-gradient top1/direction are stronger candidates than Fisher-only
  subspace clustering;
- positive margin and preserve can be achieved without feature labels in this
  synthetic setting.

Not supported:

- semantic experts;
- real-DCLM transfer;
- common/rare routing;
- expert utility;
- attention context equals rare feature;
- Fisher-only routing as a solved method.

## 9. Next Decisions

Decision 1: promote embedding-gradient top1/direction to the next method
candidate, not Fisher-only clustering.

Decision 2: test a margin-thickened gradient selector: selected states from
embedding-gradient top1/direction, router row construction from hidden centers,
and preservation guards such as row scaling, row projection, or refresh.

Decision 3: add a harder objective-locality guard. Use a loss setting where
the supervised signal is less trivially localized, or compute gradients at an
earlier layer, to test whether the selector remains valid beyond this
pointwise route-position loss.

Decision 4: after the uniform bridge is stable, move to a nonuniform
common/rare bridge and judge rare-feature NMI, rare margin p05, and
common-vs-rare separation.

## 10. Artifact Map

- Runner:
  `scripts/run_a06_27_gradient_fisher_route_state_selector.py`
- Protocol:
  `protocol.md`
- Chinese protocol companion:
  `protocol_cn.md`
- Summary JSON:
  `summary.json`
- Full run log:
  `logs/local/a06_27_gradient_fisher_full_local2gpu_20260705.log`
- Main tables:
  `tables/condition_aggregate_reinit.csv`,
  `tables/condition_aggregate_final.csv`,
  `tables/condition_trajectory_aggregate.csv`,
  `tables/selector_diagnostics_aggregate.csv`,
  `tables/training_trajectory.csv`
- Main figures:
  `figures/a06_27_core_reinit_nmi_margin.png`,
  `figures/a06_27_gradient_signal_role_share_w40.png`

Reproduction command:

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --standalone --nproc_per_node=2 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E03_gradient_fisher_selector/scripts/run_a06_27_gradient_fisher_route_state_selector.py \
  --run-stage full \
  --run-name a06_27_gradient_fisher_full_local2gpu_20260705 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E03_gradient_fisher_selector
```
