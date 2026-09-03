---
experiment_id: A15_11_E01H_qwen_native_router_access_gap_h100
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-29
primary_anchor: A15_11_gradient_consistent_hierarchical_routing
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
scientific_body_frozen_at: 2026-08-29T15:34:00Z
resource_profile: h100-4-reserved
---

# Protocol: Qwen3-30B-A3B Native Router Accessibility Chain

## 0. Approval Snapshot

| Field | Frozen value |
| --- | --- |
| Status | `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN` |
| Authorization | the 2026-08-29 user request delegates readable Anchor/Protocol formalization and autonomous execution, and explicitly requests the reserved 4×H100 allocation; no post-result human judgment is delegated |
| Unique question | where parent-label accessibility is lost along the exact native chain $H\rightarrow Z\rightarrow Q$ |
| Primary task | eight-way parent label on five confirmation blocks |
| Confirmation blocks | 4, 12, 20, 28, 36 |
| Pilot-only block | 44; its exploratory values were visible before freeze and cannot change the line verdict |
| Panels | C4 and C5 reported separately and required to agree; they share semantic atoms and are not called statistically independent replications |
| Primary metric | paired balanced-accuracy gaps and chance-corrected retention through Gate projection and top-8 selection |
| Resource | one reserved worker exposing exactly four H100 GPUs; the six registered layers rotate deterministically over devices by layer offset modulo four |
| Cannot claim | pretraining mechanism, causal native semantic use, expert utility, or language-model loss gain |

All blocks below are confirmed under the delegated execution scope. Any change
to a decision threshold, feature object, confirmation layer, label task, split,
or numeric path creates a successor Protocol.

## 1. Objects And Terms

For registered block $\ell$:

- **Native hidden input $H_\ell$:** the 2048-dimensional final-decision-token
  vector received by the Qwen MoE MLP and Gate.
- **Native Gate logits $Z_\ell$:** the exact bias-free projection
  $Z_\ell=W_{g,\ell}H_\ell\in\mathbb R^{128}$, computed in BF16 on H100.
- **Native sparse route $Q_\ell$:** a 128-dimensional vector with nonzero
  entries only at the native top eight experts; the eight softmax weights are
  renormalized to sum to one as in Qwen3-MoE.
- **Projection loss:** accessibility lost from $H$ to $Z$.
- **Selection loss:** accessibility lost from $Z$ to $Q$.
- **Linear accessibility:** held-out performance of one frozen algorithmic
  family; it is not a claim that the native Router optimizes the label.

The primary label is `parent_id` with eight balanced classes. Global
`child_id` is forbidden as a shared semantic label because the integer is
reused under different parents. Parent-conditional eight-way child probes are
secondary and never alter the primary verdict.

## 2. Anchor Alignment And Hypothesis

E01 fills only the representation-to-Router link in A15_11. A15_09 measured
coarse/fine supervised-space geometry, and A15_10 measured cross-parent fine
readout transfer; neither located information loss through the actual frozen
Gate map and top-8 operation.

The registered hypothesis is a **top-8 selection bottleneck with retained
semantic association**: the 128-dimensional native Gate row space preserves
almost all held-out parent readout available in $H$, while sparse top-8
selection removes a material fraction but remains more parent-associated than
matched label permutations. The rivals are projection mismatch, no material
bottleneck, and a mixed depth-dependent profile.

## 3. Frozen Inputs And Provenance

Activation root:

`/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction`

| Artifact | Required identity |
| --- | --- |
| `c4_activations.npy` | shape `[6,1920,2048]`, float32, SHA-256 `c1748f785e4563689f52cb94951861dbb994d6437f559baeb1a3306e34d43107` |
| `c5_activations.npy` | shape `[6,1920,2048]`, float32, SHA-256 `cf68c95288306386d1b82bed0ca64066af0073873f41aa278da9cd86010a2422` |
| `c4_metadata.jsonl` | SHA-256 `a94a2f59655fd152953f8a2e0086bc69a4f15bb2886a2a15b93eb83fca888ad9` |
| `c5_metadata.jsonl` | SHA-256 `4708b9e655d6152102f9d58f363d947ef4ced1c74658b7078bc0988d01f1bc52` |
| `split_manifest.json` | SHA-256 `e815b6acf13774ed438186bb86ab9233898a7fdfbcb409c7f4b517f2daa25773` |
| `extraction_manifest.json` | SHA-256 `09716a299db3decbd12086799ef90c15ec0ded18d40065b27bbf72bd08cc1282` |

The checkpoint is `/data/share/Qwen3-30B-A3B`. Its `config.json` SHA-256 is
`2850ddb3bf7aecad20b611e2d44f3077fc8193f4827c93beddd4c02ad63c2297`
and its safetensors index SHA-256 is
`df0d481ec595c55a0ba58426d517390c6214a566ec4ff1c8fc4bbce9f57b3c24`.
The run hashes each loaded tensor payload and requires:

| Block | Module index / tensor key | Payload SHA-256 |
| ---: | --- | --- |
| 4 | `3 / model.layers.3.mlp.gate.weight` | `dc4f558c07513e45629e33936f7b01aa02cbed9fb45f5abec488d1948bdb31e3` |
| 12 | `11 / model.layers.11.mlp.gate.weight` | `80a517bd484ce86f2ecfaab14b9b939a89e4451146efb7eb0f68c1d579a49ff6` |
| 20 | `19 / model.layers.19.mlp.gate.weight` | `29c28f809e9293c29f03e293f311c14420204024521579ece0186175cb73560c` |
| 28 | `27 / model.layers.27.mlp.gate.weight` | `a37ac22bf3c84eb066ac71f95096918c843b7c3c0580d02bdcb65a78212ecbe9` |
| 36 | `35 / model.layers.35.mlp.gate.weight` | `68bb7a65e9195508084ecae20b3ed7613ccbdcca1a9272cf5842bbd1e5fd8a46` |
| 44 | `43 / model.layers.43.mlp.gate.weight` | `5e23d4b713cf5b19d4e681c36b465c494d589a2d1dd5f5e5e9d9f3fde8648d33` |

Each tensor must be BF16 with shape `[128,2048]`. The block labels are
one-based; using `model.layers.{block}` is a fatal off-by-one error.

Each panel contains 30 complete `template_family_id` blocks, each spanning all
eight parents, eight children per parent, and hence 64 rows. The existing A/B
halves contain 15 disjoint complete families and are never regenerated.

## 4. Native Numeric Construction

For each panel/layer, one H100 device computes

```text
h = cached float32 values cast back to torch.bfloat16
w = frozen gate tensor in torch.bfloat16
z = F.linear(h, w)                         # BF16 native output
p = softmax(z, dtype=torch.float32)
values, indices = topk(p, 8)
values = values / sum(values over top8)
q = scatter(values at indices into 128-vector)
```

FP32 $H W_g^\top$ and its top-8 route are sensitivity objects only. The run
reports exact-set agreement, Jaccard overlap, and the eighth-minus-ninth logit
gap. BF16/FP32 disagreement is expected near ties; there is no 99.9% exact-set
guard. If BF16 and FP32 reverse the registered qualitative line verdict, E01
is `Insufficient`.

## 5. Held-Out Probe Contract

For each of $H,Z,Q$, perform A-to-B and B-to-A cross-fitting. Training-only
coordinate means center both train and held-out features; coordinatewise scale
normalization is forbidden. Fit multinomial L2 logistic regression with
`lbfgs`, intercept, `max_iter=5000`, `tol=1e-8`, and
$C\in\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}$.

Select $C$ within the training half using five deterministic folds of complete
template families, three families per validation fold. Minimize mean held-out
negative log likelihood and break ties toward smaller $C$. The same algorithm,
rows, labels, folds, and scorer apply to all three feature objects. A or B test
labels never choose preprocessing, $C$, retries, representation, or layer.

The combined out-of-fold ledger gives every example exactly one prediction.
Report held-out negative log likelihood, balanced accuracy, per-class recall,
selected $C$, convergence, coefficients, and prediction probabilities. Any
nonconvergence or row mismatch remains visible and makes that cell ineligible.

## 6. Primary Metrics

For $K=8$ and balanced accuracy `BA`, define

$$
D_{proj}=BA(H)-BA(Z),\qquad
D_{select}=BA(Z)-BA(Q),\qquad
D_{total}=BA(H)-BA(Q),
$$

and, only when $BA(H)>1/K$,

$$
R_Z=\frac{BA(Z)-1/K}{BA(H)-1/K},
\qquad
R_Q=\frac{BA(Q)-1/K}{BA(H)-1/K}.
$$

These chance-corrected retention scores are empirical and unclipped. NLL gaps
are reported as a calibration guard and cannot replace the BA verdict after
results are visible.

Native route association uses the actual top-8 weights:

$$
p(e\mid y)=\frac1{n_y}\sum_{i:y_i=y}Q_{ie},
\qquad
I_Q(Y;E)=\sum_{y,e}p(y)p(e\mid y)\log\frac{p(e\mid y)}{p(e)}.
$$

Report $I_Q/H(Y)$, top-1 adjusted mutual information, expert-load entropy,
effective expert count, and conditional load profiles. These are associations,
not expert utility.

## 7. Uncertainty And Null

Use 10,000 paired bootstrap draws with root seed `151101`. The independence
unit is one complete template family; each draw resamples 30 families and uses
the identical indices for $H,Z,Q$, all layers, and both paired gaps. C4 and C5
are bootstrapped separately.

Use 1,000 label-null draws with root seed `151102`. Within every held-out
template family independently permute the eight parent labels as complete
parent blocks, preserving its 8×8 balance. Apply one draw identically to every
layer and feature object. A max statistic across the five confirmation layers
controls the scan. Conditional-fine nulls permute eight children only within
the same `(template_family,parent)` block.

The null is applied to frozen out-of-fold predictions and native $Q$ loads; it
does not retrain a probe and is not described as training-set uncertainty.

## 8. Confirmation Verdict

Block 44 is always rendered as `PILOT_NOT_BLIND`. Only Blocks 4/12/20/28/36
enter the following line verdict.

At one block/panel:

- **projection preserved** if the paired bootstrap lower 95% bound of $R_Z$
  is at least `0.90` and the upper 95% bound of $D_{proj}$ is at most `0.05`;
- **material selection loss** if the lower 95% bound of $D_{select}$ is at
  least `0.10`;
- **retained route association** if $I_Q/H(Y)$ exceeds the max-layer 97.5th
  percentile of the matched label null;
- **near-total sparse retention** if the lower 95% bound of $R_Q$ is at least
  `0.90`.

The line verdict is:

- `TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION` if at least four of
  five confirmation blocks satisfy projection preserved, material selection
  loss, and retained route association in both C4 and C5;
- `GATE_PROJECTION_BOTTLENECK` if at least four of five have a lower 95% bound
  of $D_{proj}\ge0.10$ in both panels;
- `NO_MATERIAL_ACCESS_BOTTLENECK` if at least four of five satisfy projection
  preserved and near-total sparse retention in both panels;
- `MIXED_OR_NOT_ESTABLISHED` otherwise;
- `Insufficient` if hidden accessibility does not exceed its matched
  max-layer null, a required cell is invalid, input identity fails, or BF16
  and FP32 produce different line verdicts.

Thresholds are practical effect thresholds, not population constants.
Conditional-fine results, Block 44, NLL, AMI, load entropy, or plots cannot
rescue or reverse the primary verdict.

## 9. Stages And Required Artifacts

| Stage | Operation | Stop rule | Required artifact |
| --- | --- | --- | --- |
| 0 | hash inputs, map one-based blocks to zero-based Gate tensors, and audit the exact reserved 4×H100 environment | any mismatch stops | `preflight.json` |
| 1 | synthetic numeric unit tests and label-blind BF16/FP32 route reconstruction smoke | no scientific metric may be opened; any identity failure stops | `smoke_receipt.json`, test log |
| 2 | construct $H,Z,Q$ and all cross-fitted parent predictions | missing/nonconverged cells retained, never replaced | feature manifests, `predictions.parquet` or CSV |
| 3 | paired bootstrap, label null, fine diagnostic, and frozen verdict | exact counts/formulas required | `results.json`, `layer_metrics.csv`, null ledger |
| 4 | render and audit | every figure contract and artifact hash required | `figures/`, `completion_audit.json` |

Required figures are: (1) a layerwise $BA(H),BA(Z),BA(Q)$ ladder with paired
uncertainty for C4/C5; (2) projection and selection gap panels; and (3) a
native top-8 parent-by-expert load heat map at all six layers. Every figure
must state its question, metric, unit, source, allowed conclusion, and limit.

## 10. Claim Boundary And Stop Rule

E01 can locate a loss of supervised parent-label accessibility at the native
linear Gate projection or sparse top-8 interface and can establish a bounded
route-label association. It cannot say that semantic routing improves Qwen
loss, that routed experts are functionally appropriate, that pretraining used
the A15_11 gradient mechanism, or that a replacement Router will help.

The experiment stops after the frozen matrix and verdict. No result-dependent
layer selection, regularization extension, alternative label grouping, PCA,
Fisher overlap, UMAP, or X-MoE collapse score is allowed as a rescue.

## 11. Confirmation, Freeze, And Resource Isolation Ledger

All scientific blocks, immutable inputs, metrics, thresholds, confirmation
layers, and claim boundaries are identical to the original E01 scientific
design. Before any scientific result was generated, the shared E01 file and
worker surface were concurrently rewritten by another task to a contradictory
8×RTX-5090 SPOT contract. To preserve that external edit while obeying this
task's explicit reserved 4×H100 instruction, this collision-safe successor
freezes only the execution resource and provenance under a new experiment ID.
It uses workspace `share-space`, AEC2 cluster `share-cluster`, worker spec
`n6ls.iu.i40.4`, one node, normal priority, reserved quota, and exactly four
visible H100 devices. Layers rotate deterministically over those devices.

No scientific result was inspected before this isolation. Any non-H100
device, non-reserved quota, different GPU count, input mismatch, or automatic
fallback must fail closed. The resource correction does not alter the
estimand, analysis, verdict rule, or claim boundary.
