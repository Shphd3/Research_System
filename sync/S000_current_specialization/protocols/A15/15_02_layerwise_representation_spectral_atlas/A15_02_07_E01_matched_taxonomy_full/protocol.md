---
experiment_id: A15_02_07_E01_matched_taxonomy_full
anchor_id: 15_02_07_matched_semantic_complexity
status: APPROVED_FOR_FULL_RUN
canonical_language: en
approved_scope: implementation_and_one_full_run
approved: 2026-08-08
---

# Protocol: Matched Taxonomy 10-Layer Full Run

## 0. Approval Snapshot

- **Question:** under cardinality-matched natural taxonomy tasks, does complex-relative variance of the attention-induced MLP-input increment move to later local parameter ranks with depth, and does its conditionally new linear accessibility do the same?
- **Purpose:** repair the E01 pooling, replay, small-sample, three-layer, H2-headroom, and visualization failures without reusing E01 as eligible evidence.
- **Primary Anchor:** A15_02_07 matched semantic complexity and parameter spectrum.
- **Experiment role:** operationalization and proxy test.
- **Full scope approved:** the 2026-08-08 researcher instruction authorizes the repaired 10-layer TAX full run, analysis, separate TAX figures, and result records.
- **Treatment / control:** complex within-parent 8-leaf discrimination versus simple between-parent 8-parent discrimination with exactly one leaf representing each parent.
- **Changed variable:** whether eight labels cross parent boundaries or remain inside one parent.
- **Held fixed:** 8 classes, one leaf per class, records per leaf and split, prompts, fact schedule, readout token, frozen model, layers, parameter basis, covariance estimator, readout family, bootstrap count, and figure transformation.
- **Primary H1 metric:** sampled late-minus-early change in complex-minus-simple normalized local-rank centroid.
- **Primary H2 metric:** sampled late-minus-early change in complex-minus-simple conditional log-loss gain supplied only by $\Delta n$ after an $n^{old}$ readout is frozen.
- **Pass:** registered point estimate and paired-bootstrap 95% lower bound exceed zero, with all mandatory guards; H1 additionally requires positive DEVELOPMENT direction.
- **Fail:** the paired-bootstrap 95% upper bound is below zero.
- **Insufficient:** guard failure, split reversal, or an interval containing zero.
- **Cannot claim:** shared eigenvector identity, causal MLP use, genuinely equal semantic difficulty, composition, training utility, or routing utility.
- **Full-run limit:** exactly one local two-branch run; TAX is adjudicated independently from COMP.

## 1. Terminology And Definitions

- **Simple TAX task:** classify eight parent labels, with each parent represented by exactly one selected leaf.
- **Complex TAX task:** classify the eight leaves within one parent.
- **Latin-square rotation:** in simple task $r$, parent $p$ is represented by child $(p+r)\bmod8$; across eight tasks every leaf is used exactly once.
- **Old MLP input:** $n^{old}_\ell=RMSNorm_\ell(x_\ell)$.
- **Attention increment:** $\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)$.
- **Local parameter rank:** descending eigenvalue order of $K_\ell=W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}$ inside one layer. Rank equality across layers is order equality, not vector identity.
- **Conditional gain:** confirmation cross-entropy of the frozen old-state readout minus confirmation cross-entropy after adding a linear $\Delta n$ correction, in nats/example.
- **Update readability:** $Disc(\Delta n)=\log8-CE(\Delta n)$, a supporting statistic that does not establish novelty relative to $n^{old}$.

## 2. Anchor Alignment

This experiment adjudicates only the Anchor's TAX branch. H1 tests the parameter-spectrum location of $\Delta n$; H2 tests information newly accessible beyond a frozen old-state readout. The strongest rival is that earlier effects arose from pooled parent centers, tiny probes, cross-hardware cache replay, or old/new saturation rather than semantic refinement.

## 3. Tested Hypotheses

- **H1-TAX:** $R_{\ell}=m_{\ell,complex}-m_{\ell,simple}$ becomes more positive from sampled early to sampled late layers.
- **H2-TAX:** $G_\ell=CIG_{\ell,complex}-CIG_{\ell,simple}$ becomes more positive from sampled early to sampled late layers, where `CIG` is conditional information gain.
- H1 and H2 are separately adjudicated; neither rescues the other.

## 4. Rival Explanations

| Rival | Registered separator |
| --- | --- |
| parent pooling versus one child inflates variance | one leaf per class in both conditions; equal 8-way estimator |
| arbitrary leaf selection drives simple tasks | eight Latin-square rotations use every leaf once |
| tiny high-dimensional logistic probe | 80 TRAIN examples per task and deterministic dual ridge readout |
| old/new headroom masquerades as new information | freeze old readout, then fit only a $\Delta n$ logit correction |
| external cache mismatch | same-run repeated first batch and direct hook-site identity; no old attention cache |
| three points imply a trend | ten fixed layers and registered sampled early/late statistic |
| smoothing creates the result | exact arrays determine metrics; 129-rank smoothing is display-only |

## 5. Data Construction And Provenance

- Source facts: verified A15_02 taxonomy with 8 parents, 8 leaves per parent, and 6 label-free fact atoms per leaf.
- Generated data: `taxonomy_full.json`, SHA-256 `ce91dbbd3c5071e17beeccf0d86a280dc8a3e48e0fdbf2178868da45eea18af4`.
- Total records: 1,920 = 64 leaves × 30 expressions.
- Per leaf: 10 TRAIN, 10 DEVELOPMENT, 10 CONFIRMATION.
- Splits use disjoint five-template families. Each expression selects three of six facts through a deterministic split-specific schedule.
- Every prompt is label-free and ends at the common `Classification:` readout.
- There are eight simple rotation tasks and eight complex parent tasks. Every task has 8 classes and 10 records per class per split.
- Confirmation truth is unavailable to data construction, standardization, ridge selection, or stopping.

## 6. Learning Task And Permitted Supervision

Qwen3-8B is frozen. H1 uses confirmation class centers only. H2 permits class labels on TRAIN for fitting and DEVELOPMENT for ridge selection; CONFIRMATION labels are used once for registered reporting. The prediction unit is one 8-way task-specific class label. Tasks are equally weighted.

## 7. Model, Layers, And Parameter Basis

- Model: local frozen `/data/share/Qwen3-8B`; bfloat16 SDPA forward.
- Layers: 1, 5, 9, 13, 17, 21, 25, 29, 33, 36.
- Early sample: 1, 5, 9. Late sample: 25, 29, 33. Layer 36 is displayed as a boundary and excluded from the primary early/late statistic.
- Representation: exact $\Delta n$ at the final prompt token.
- Parameter operator: native $K_\ell$; ten verified A15_02_06 basis files with hashes recorded in worker preflight.
- Basis vectors are used only as an orthonormal coordinate; individual directions are not matched across layers.

## 8. Fixed-Capacity Readout Objective

Let $Y_c$ be centered one-hot TRAIN targets. After TRAIN-only feature standardization, the base readout solves

$$
\min_W\frac1N\lVert Y_c-X_{old}W\rVert_F^2+\lambda\lVert W\rVert_F^2.
$$

After $W$ is selected on DEVELOPMENT and frozen, the increment solves

$$
\min_U\frac1N\lVert Y_c-L_{base}-X_{\Delta n}U\rVert_F^2+\lambda_\Delta\lVert U\rVert_F^2.
$$

The augmented logits are $L_{base}+X_{\Delta n}U$. The frozen grid is
$\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}$; ties choose larger regularization. Balanced classes make the centered target's intercept zero. Dual closed-form ridge is used; no iterative convergence or checkpoint choice exists.

The primary H2 quantity is

$$
CIG_{\ell,d}=CE^{conf}_{base}-CE^{conf}_{augmented}.
$$

`Disc($\Delta n$)` uses a separate ridge readout on $\Delta n$ and is supporting only.

## 9. Conditions, Seeds, And Independence

- Conditions: simple and complex, separately measured at ten layers.
- Independent bootstrap unit: the eight matched task indices; layers and parameter directions are not replicates.
- Paired bootstrap: 2,000 resamples, seed 2711 for H1 and 2712 for H2.
- All records, directions, tasks, and layers are retained; no outlier deletion or post-hoc task filtering is permitted.

## 10. Primary Metrics And Frozen Analysis

For task $q$, class center $\mu_{qk}$, and $K=8$:

$$
b^{(q)}_{\ell,d,i}=\frac1{K-1}\sum_{k=1}^K(\mu_{qk,i}-\bar\mu_{q,i})^2,
\qquad b_{\ell,d,i}=\frac18\sum_q b^{(q)}_{\ell,d,i}.
$$

Normalize $\pi_{\ell,d,i}=b_{\ell,d,i}/\sum_jb_{\ell,d,j}$ and define

$$
m_{\ell,d}=\sum_i\pi_{\ell,d,i}\frac{i-0.5}{4096},\qquad
R_\ell=m_{\ell,complex}-m_{\ell,simple}.
$$

The H1 primary statistic is

$$
T_{rank}=median_{\ell\in\{25,29,33\}}R_\ell-median_{\ell\in\{1,5,9\}}R_\ell.
$$

The H2 primary statistic replaces $R_\ell$ with
$G_\ell=CIG_{\ell,complex}-CIG_{\ell,simple}$.

H1 passes only if confirmation $T_{rank}>0$, paired-bootstrap lower 95% bound $>0$, and DEVELOPMENT $T_{rank}>0$. H2 passes only if confirmation $T_{CIG}>0$ and its paired-bootstrap lower bound $>0$. Upper bound below zero is Fail; otherwise Insufficient.

## 11. Mandatory Guards And Figures

1. Exact same-run attention replay on the repeated first batch.
2. Direct `o_proj` site relative error below $10^{-5}$ at layers 1, 21, and 36.
3. $\Delta n$ projection reconstruction relative error below $10^{-4}$ at every layer.
4. Dataset/task/split counts exactly match Section 5.
5. Mean augmented `Disc` across ten layers exceeds 0.1 nats/example in both conditions.
6. All curves are finite/nonnegative and normalized masses sum to one.
7. Required TAX figure: ten rows ordered shallow to deep; raw left, normalized right; exact thin lines plus centered 129-rank linear-domain mean before `log10`.
8. Required H1/H2 TAX metric figure and full machine tables.

Smoothing affects display only. Raw $b_i$, normalized $\pi_i$, centroids, bootstrap values, and verdicts use unsmoothed arrays.

## 12. Known Cases

- A single-direction synthetic class difference must peak in that direction.
- Identical centers must refuse normalization.
- Zero $\Delta n$ must give exactly zero conditional gain.
- Multiplying raw variance by a positive constant must preserve normalized centroid.
- Constant curves must remain constant under the 129-rank smoother.

## 13. Stage Contract

| Stage | Operation | Required evidence | Stop rule |
| --- | --- | --- | --- |
| Preflight | verify Protocol/data/basis hashes, two H100s, schema | `preflight.json` | any mismatch stops |
| Tests | data balance, covariance, ridge no-op, smoothing | `unit_tests.log` | any failure stops |
| Extract | one frozen forward over all 1,920 texts, ten hooks | layer tensors and manifest | replay/site/projection failure marks guard insufficient |
| H1 | split-specific class centers, paired task bootstrap | exact curves and H1 table | no filtering |
| H2 | base ridge, frozen base, increment ridge, delta-only support | task/layer readout ledger | confirmation never used for selection |
| Render | TAX-only ten-layer curves and metrics | PNG/PDF plus figure contract | rendered artifacts must be opened and audited |
| Finalize | typed outcome and artifact manifest | result JSON | no automatic publication or Git action |

## 14. Output And Provenance Contract

Worker code and raw outputs live under
`XingyuD/MoE_Routing_Experiments/active/a15_01_10_e02_e03_tax_comp_10layer_full/`.
Canonical Protocol/results/figures live in this E02 directory. The run records Protocol, data, basis, code, environment, tensor, table, and figure hashes. Existing dirty files are preserved. No sync, graph edit, commit, or push is authorized.

## 15. Typed Outcomes

- `joint_pass`: H1 and H2 pass all registered rules.
- `h1_only`: H1 passes and H2 fails.
- `h2_only`: H2 passes and H1 fails.
- `joint_fail`: both upper confidence bounds are below zero.
- `insufficient_mixed`: at least one interval crosses zero or H1 split direction fails.
- `insufficient_guard`: any mandatory guard fails; H1/H2 cannot be claimed.

## 16. Claim Boundary

This experiment can establish only a TAX-specific association between depth, local parameter-rank allocation of $\Delta n$, and fixed linear conditional accessibility. It cannot establish composition, causal MLP use, semantic-difficulty equality, learned storage location, shared cross-layer directions, or downstream utility.

## 17. Confirmation And Freeze Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question/boundary | CONFIRMED | approved Anchor and 2026-08-08 full-run instruction |
| B data/provenance | CONFIRMED | researcher-required cardinality repair plus verified taxonomy source |
| C task/supervision | CONFIRMED | 8-way matched labels and untouched confirmation |
| D model/architecture | CONFIRMED | frozen Qwen3-8B, requested ten layers, verified bases |
| E objective | CONFIRMED | delegated smoke repair; conditional ridge removes headroom and convergence failures |
| F comparison/evidence | CONFIRMED | registered H1/H2, bootstrap, separate TAX figures |
| G execution | CONFIRMED | explicit implementation and full-run authorization; two local H100s |

Cross-block consistency: `PASS`. This file is frozen before the first E02 model forward. Any outcome-changing change requires a new append-only amendment and explicit eligibility statement.
