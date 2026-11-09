---
experiment_id: A15_02_E04_qwen3_post_o_proj_semantic_atlas
anchor_id: 15_02_layerwise_representation_spectral_atlas
status: COMPLETED_DEPTH_PASS_SPECTRAL_FAIL
canonical_language: en
companion_language: zh
approved: 2026-08-06
completed: 2026-08-06
---

# Protocol: Qwen3-8B Post-o_proj Full-Attention Semantic Variance Atlas

## 0. Approval Snapshot

- Researcher authorization: the 2026-08-06 instruction explicitly approves implementation, smoke, an eight-5090 full run, analysis, a self-contained 0806 report, and an 0807 knowledge update.
- A--G audit blocks: `CONFIRMED`; cross-block consistency: `PASS`.
- Git commit, push, graph editing, external sync, model training, and Router construction are outside scope.

## 1. Question And Claim Boundary

In frozen Qwen3-8B, after `o_proj` has mixed all attention heads but before residual addition, does the full attention branch \(g_\ell=W_Oa_\ell\) retain the late-layer increase in fine-versus-coarse semantic discriminability found before `o_proj`, and where does this signal lie in the post-`o_proj` natural-text covariance spectrum?

This is a frozen representation audit. It cannot establish causal semantic computation, compositionality, Router utility, expert compatibility, or training benefit.

## 2. Representation Object

For every decoder block, capture the direct output of `self_attn.o_proj`:

\[g_\ell=W_{O,\ell}a_\ell\in\mathbb R^{4096}.\]

It is the cross-head-mixed attention branch output. It is not a set of 32 architectural heads, the residual sum, the post-attention RMSNorm state, the MLP input, or the block output. All 36 blocks are analyzed; block 36 is reported separately.

## 3. Data And Provenance

- Model: local `/data/share/Qwen3-8B`, frozen, bfloat16 forward.
- Semantic cube: exactly the previously audited 512 texts, comprising 8 coarse domains, 8 fine concepts per domain, 4 templates, and 2 fact bundles. Template 1--2 are design and 3--4 confirmation.
- Readout: the shared final `Classification:` colon token at the already-audited position.
- Covariance calibration: the same 128 independent DCLM documents and 65,536 tokens; two fixed halves of 32,768 tokens.
- No text, label, split, readout, calibration token, or seed may be changed after inspecting post-`o_proj` results.

## 4. Metrics

For granularity \(s\in\{coarse,fine\}\), let \(B_{\ell,s}\) be between-class covariance and \(W_{\ell,s}\) be within-class/template covariance. Full-state discriminability is

\[D_{\ell,s}=\frac{\operatorname{tr}(B_{\ell,s})}{\operatorname{tr}(W_{\ell,s})+\epsilon},\qquad R_\ell=\log\frac{D_{\ell,fine}}{D_{\ell,coarse}}.\]

The primary depth statistic is

\[T_{post}=\operatorname{median}_{\ell=25:35}R_\ell-\operatorname{median}_{\ell=1:12}R_\ell.\]

Natural-text covariance is decomposed into 16 equal-rank bands of 256 directions: F1=head, F2--F8=middle, F9--F16=tail. Each band reports actual between-class variance \(b\), background-normalized variance \(q\), discriminability \(j=B/W\), and relative actual-variance enrichment \(e\).

## 5. Hypotheses And Rivals

- H1 depth: \(T_{post}>0\) with hierarchical-bootstrap lower bound above zero, 4/4 template contrasts positive, and 8/8 leave-one-parent contrasts positive.
- H2 actual-energy location: F1 has the largest per-direction \(b\) for both granularities in at least half of blocks 1--35.
- H3 fixed non-head specificity: any claimed middle/tail enrichment must exceed equal-dimensional random directions and survive design/confirmation, both calibration halves, nuisance residualization, and three eigenvalue floors.
- Strongest rival: pre-`o_proj` semantic concentration is rotated or diluted by \(W_O\), so post-`o_proj` depth or fixed-band structure does not persist; apparent tail effects may be calibration-basis or tiny-eigenvalue artifacts.

## 6. Controls And Comparisons

The post-`o_proj` result is compared descriptively, using identical definitions, with cached pre-`o_proj` full-attention and block-residual results. The existing MLP-input full-state metrics are included only where definitions match. Numeric differences between sites are not attributed causally to `o_proj`, residual addition, or normalization.

## 7. Validity Gates

1. Hook all 36 `o_proj` outputs and verify shape `[batch, sequence, 4096]`.
2. Verify module output equals direct `F.linear(o_proj_input, weight, bias)` within relative error \(<10^{-6}\).
3. Verify deterministic replay, complete 512-record semantic coverage, and 65,536-token calibration coverage.
4. Verify covariance reconstruction, trace/energy conservation, FP32 Gram against direct FP64, and basis orthogonality.
5. Verify H/M/T calibration-half stability and eigenvalue-floor robustness.
6. Use 2,000 hierarchical paired bootstraps and the frozen random-subspace null.
7. Stop and report `insufficient_<guard>` if any mandatory gate fails; do not relax controls or filter concepts/layers.

## 8. Decision Rules

- `depth_pass_spectral_pass`: H1, H2, H3 and all guards pass.
- `depth_pass_spectral_fail`: H1 and H2 pass, but no fixed non-head band passes H3.
- `depth_fail_spectral_pass`: H1 fails but H2/H3 pass.
- `joint_fail`: all guards pass but both registered scientific clauses fail.
- `insufficient_<guard>`: a validity gate fails.

Block 36 never enters the early/late primary statistic and is interpreted separately.

## 9. Required Artifacts And Figure Contracts

- Full CSVs: depth discriminability, 16-band metrics, bootstrap comparisons, covariance spectrum, basis stability, energy conservation, template and leave-one-parent controls, floor sensitivity, random-subspace null, and cross-site comparison.
- Figure 0: post-`o_proj` covariance spectrum; axes are normalized rank and background variance.
- Figure 1: post-`o_proj` depth trajectory plus pre/post/residual comparison; the ordinate is \(R\) or \(D\), not loss.
- Figure 2: layer×16-band heatmaps for \(b,q,j\) and fine/coarse log ratios.
- Figure 3: decisive layer×band discriminability and H/M/T depth trajectories.
- Every central figure must be opened and visually audited for axes, colorbar, layer 35/36 visibility, and claim boundary.

## 10. Execution Contract

- Surface: SCO ACP, one node, profile `5090-8-spot`.
- Frozen tuple: workspace `share-space`; cluster `computing-cluster-5090-01g`; worker spec `n12lp.nn.i10a.8`; one worker; spot; normal priority; 8 GPUs/processes.
- Run order: local contract tests -> ACP smoke -> full extraction -> analysis -> visual audit -> evidence records.
- Worker code and raw outputs remain under the active worker surface; only curated tables, figures, manifests, and records enter the research mainline.

## 11. Confirmation Ledger

| Block | State | Frozen decision |
| --- | --- | --- |
| A question/boundary | CONFIRMED | exact post-`o_proj` branch; frozen representation claim only |
| B data/provenance | CONFIRMED | identical 512 semantic texts and 65,536-token calibration |
| C task/supervision | CONFIRMED | frozen coarse/fine representation audit |
| D model/object | CONFIRMED | Qwen3-8B, 36 exact `o_proj` outputs |
| E objective/optimization | CONFIRMED | no model training; fixed analysis |
| F evidence/decision | CONFIRMED | \(T_{post}\), 16 bands, random and split guards |
| G execution | CONFIRMED | implementation, smoke, full, analysis, 0806 report, 0807 focus; one 8×5090 spot node |

## 12. Execution Closure

The formal 8×5090 ACP job `om-5y1d8uf1` completed successfully with zero retries. All hard guards passed. The typed verdict is `depth_pass_spectral_fail`: the depth and actual-variance head-dominance clauses pass; middle relative enrichment passes its local controls, tail stability fails, and therefore the registered joint spectral clause fails. Results are recorded in [summary.md](summary.md) and [detailed.md](detailed.md).
