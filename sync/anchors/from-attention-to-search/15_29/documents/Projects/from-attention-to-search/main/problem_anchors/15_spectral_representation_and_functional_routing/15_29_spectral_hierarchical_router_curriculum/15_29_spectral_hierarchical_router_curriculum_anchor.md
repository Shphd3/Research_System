派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor.md`。
[精确原始文件](../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor.md)；研究修改仍回到原件。

---

# A15_29: Does progressive spectral routing supervision help a fixed MoE?

## 1. Problem Definition

The researcher fixed this question on2026-10-31: does enabling head-, middle-, then tail-band conditional routing supervision improve learning relative to using the same full hierarchy from the beginning? P is progressive; F is full throughout. Each starts from the same ordinary8-layer MoE random initial state and trains to50B valid prediction tokens. Their sole active treatment is the two deeper supervision coefficients' token schedule. The plain ordinary MoE is a reference; P versus F isolates this particular curriculum within one seed, not all teacher benefits.

## 2. Physical Priors

A frozen33B Dense teacher supplies contextual FFN inputs. Centered covariance orders variance, not activation frequency or semantic coarseness. Whether its artificial binary partitions aid routing is an empirical hypothesis. Independent subspace stability does not imply stable clustering. The1031 spectral interpretation analysis did not establish a universal coarse-to-fine semantic spectrum.

## 3. Falsifiable Hypotheses

P may benefit by delaying deeper constraints; the rival is that early access to the same deeper information is equally good or better. A P advantage in matched validation-loss trajectories is descriptive support for this one curriculum; equal or worse P weakens it. Collapsed/unstable targets, unmatched exposures or failed recovery make the treatment comparison insufficient. Cross-seed robustness and natural semantic hierarchy remain untested.

## 4. Mathematical Model

At layer i and position t, teacher FFN input h is the actual learned post-norm2 vector. A estimates mean and covariance; descending eigenvectors divide1024 coordinates at128 and512, with only documented nearby-gap adjustment allowed. A fixed whole-band RMS normalizes each projection; neither token unit normalization nor inverse-eigenvalue whitening is used. Weighted binary clustering produces two head groups, four middle groups and eight tail leaves. Conditional probabilities are softmax of negative squared distance divided by a calibration-only temperature. All node fits use weighted-median initialization followed by exactly one nearest-center reassignment and weighted centroid update; the root seed is the first head-band PC and child seeds are fixed original-hidden-coordinate directions. Child fits retain all positions with soft parent weights. Leaf index is4a+2b+c; parents are exact leaf sums.

Teacher leaf q and student raw pre-bias8-way softmax p define three conditional terms:

\[
D_H=\mathrm{KL}(q_a\Vert p_a),\quad
D_M=\sum_a q_a\mathrm{KL}(q_{b|a}\Vert p_{b|a}),\quad
D_T=\sum_{a,b}q_{ab}\mathrm{KL}(q_{c|ab}\Vert p_{c|ab}).
\]

The chain rule gives \(D_H+D_M+D_T=\mathrm{KL}(q_{abc}\Vert p_{abc})\), avoiding repeated parent constraints. The objective is

\[
L=L_{LM}+\lambda(N)(D_H+\gamma_M(N)D_M+\gamma_T(N)D_T),
\]

averaged over valid positions and eight layers. N is completed valid training tokens before the update. Supervision recomputes router logits from stop-gradient student FFN input; it directly updates router weights only. LM backpropagation still trains backbone, experts and routers. The frozen teacher and tree receive no gradients. Loss-free bias affects only selected experts, never these supervised probabilities.

## 5. Computational Realization

Both groups reuse the corrected baseline model, packed DCLM stream, reference-rank sample/mask order, optimizer, constant-after-warmup LR and exact save milestones. The student has507988992 parameters,8layers,hidden1024,eight independent1536-wide experts/layer,top2,no shared expert. Final V5 calibration A/B/C5 contains262144/262144/16384 positions in disjoint physical documents and complete original2048-token contexts. A fits production coordinates/tree; B independently refits; C checks probability and document support. B relabeling uses only tree-preserving swaps selected on A, not C. Online teacher generation uses the same causal input as each student microbatch; no50B cache is materialized.

## 6. Minimal Falsification Tests

Before full runs, require numerical KL chain equality, router-only auxiliary gradients, unchanged zero-weight LM path, exact2/4/8rank masks, teacher prefix causality, independent target checks, finite GPU updates, no dropped assignments, virtual-clock phase boundaries and two separate true-process-restart comparisons. Engineering thresholds and their limits are in Protocol. Full P/F compare validation loss at the same token checkpoints; sign of P-minus-F is a within-seed descriptive readout, not a statistical cross-seed claim. Missing paired validation remains missing, without substituting training loss.

## 7. Current Evidence

The exact teacher checkpoint hash, CPU load and prefix causality were checked. Calibration contexts were frozen and CPU contract checks passed. Target fitting and GPU execution status belongs to Detailed and execution receipts; no P/F training result is established. Actual2xRTX5090 hardware access passed in om-t99qfhv3. V5 all8 offline target gates passed on fresh C5. The replacement2GPUjob om-to4cwwnz passed actual GPUcausality/gradient/target replay checks and is completing throughput and P/F true-process-restart qualification. V1–V4 failures remain recorded. The shared8GPU formal serialization mechanism is still unverified. The1031 analysis remains a motivation with its original negative/insufficient boundaries, not evidence for this method.

## 8. Claim Boundary And Next Decision

This tests a fixed artificial spectral curriculum, not natural semantic hierarchy, adaptive convergence detection or general seed robustness. Researcher authorization covers implementation, offline fitting,2xRTX5090spot smoke, and smoke-pass-gated sequential8xRTX5090spot50B jobs, preserving the ordinary baseline. The next operational decision is whether all actual engineering gates and the8GPU shared resource cap are verified; only then submit both jobs. The later scientific judgment remains with the researcher after paired results.

[Protocol](../../../experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/protocol.md) · [Detailed](../../../experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/detailed.md) · [Baseline](../../../../../../../UNAVAILABLE.md) · [1031 spectral analysis](../../../../../../../UNAVAILABLE.md)
