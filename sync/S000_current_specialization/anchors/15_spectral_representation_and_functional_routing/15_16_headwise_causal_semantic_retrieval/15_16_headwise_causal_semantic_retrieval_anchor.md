# A15.16 — Headwise causal semantic retrieval audit

```text
problem_key: A15.headwise_causal_semantic_retrieval_audit
conversation_owner: codex-thread:01a0679c-7ee2-71f3-91b5-f4df234571db
ownership_status: CLAIMED
status: PHASE1_FULL_RUN_COMPLETE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
```

## 1. Problem Definition

The parent A15 line asks which representation can support a semantic Router and where conditional expert computation should be placed. Existing evidence shows that current-token label readability and expert utility are not interchangeable: block 9 is descriptively highly readable, yet a two-layer functional comparison did not establish a stable block-9 advantage.

This Anchor asks a smaller upstream question. In frozen Qwen3-0.6B-Base, do the query-conditioned context vectors returned by individual attention query heads contain reproducibly unequal amounts of real M2D2 parent and within-parent child information? Phase 1 determines whether a head-resolved follow-up is warranted. It does not test causal use, sparse retrieval, KV-cache compression, expert utility, or language-model gain.

## 2. Physical Priors

Different attention query heads can weight the same causal history differently. Qwen3-0.6B has 16 query heads and eight shared Key/Value groups, so two query heads can share stored Key/Value tensors while still returning different vectors through different queries and attention weights. If semantic retrieval is functionally heterogeneous at this anatomical resolution, identical-capacity readouts should expose stable head-to-head differences on held-out windows. If information is diffuse, the apparent best head should not survive a search-corrected null and untouched confirmation.

## 3. Falsifiable Hypotheses

**Primary hypothesis.** At least one of the two registered gold-label tasks has a layer whose between-head readability spread is larger than a window-label permutation null after correcting for the search over all 28 layers, and the development-selected top four heads retain a positive advantage on confirmation.

**Strongest rival.** All query-head outputs carry similar or negligible label information; selecting the largest of 448 layer-head scores creates an unstable apparent specialist.

The relation between coarse and conditional-fine head profiles is measured, not assumed. The two profiles may overlap completely even if both tasks show genuine head heterogeneity.

## 4. Mathematical Model

For block $\ell$, query head $h$, and current prediction position $t$, the audited vector is the head output immediately before the attention output projection:

$$
r_{\ell,h,t}=\sum_{j\leq t}\alpha_{\ell,h,tj}V_{\ell,g(h),j}\in\mathbb{R}^{128},
$$

where $g(h)$ is the shared Key/Value group of query head $h$. An affine three-class probe is fitted independently for each $(\ell,h)$. Conditional-child probes receive the true parent only to select one of three parent-specific affine heads; each head still reads the complete 128-dimensional $r_{\ell,h,t}$.

For held-out task cross-entropy $\mathrm{CE}_{\ell,h}$ in nats, define readable information gain

$$
G_{\ell,h}=\log 3-\mathrm{CE}_{\ell,h},
$$

and within-layer head spread

$$
S_\ell=Q_{0.90}(G_{\ell,1:16})-Q_{0.10}(G_{\ell,1:16}).
$$

$G$ measures accessibility to the registered affine readout; $S$ measures inequality across heads. Neither quantity establishes native or causal use.

## 5. Computational Realization

- Freeze the exact Qwen3-0.6B-Base and M2D2 `3×3` identities used by the prior layerwise audit.
- Capture the input to each block's attention output projection, verify shape `[batch, token, 16, 128]`, and use positions 63--254 only.
- Fit four independent probe seeds. Each of the four approved RTX 5090 SPOT GPUs runs one seed over all 28 layers and 16 query heads.
- Development selects one layer and its top four heads per task. Confirmation is opened only after that selection file and its hash are written.

## 6. Minimal Falsification Tests

The decisive comparison is real head spread against 2,000 window-level label permutations. Development uses the maximum spread across all 28 layers in each permutation, protecting the layer search. Confirmation tests only the frozen development layer. A task passes only if both permutation gates pass and a 2,000-replicate window bootstrap gives a strictly positive lower 95% bound for the development-selected top four heads versus the other 12 on confirmation.

`PASS` means at least one task has reproducible query-head heterogeneity. `FAIL` means neither task passes while all qualification checks pass. `INSUFFICIENT` means tensor identity, causality, model/data identity, null construction, checkpoint reload, or confirmation sealing fails.

## 7. Current Evidence

The prior MLP-input audit descriptively selected block 9 for both gold tasks but failed one registered shuffled-label qualification edge and found no coarse-before-fine depth gap. The later block-1/block-9 LoRA comparison did not show a stable relation between static readability and expert utility. Controlled retrieval evidence also shows that feature alignment alone need not preserve sparse attention output quality. These results motivate a head-resolved accessibility audit but do not predict its outcome.

Phase 1 completed in one eligible four-seed run. Both tasks selected block 20 and query heads `[4,5,13,7]` on development. Their confirmation top-four-minus-rest gains were positive—parent `0.300311 [0.293544,0.306483]` nat and conditional child `0.354685 [0.347546,0.362285]`—but both real head spreads were below their registered development and confirmation permutation thresholds. The typed verdict is `NO_REPRODUCIBLE_HEAD_HETEROGENEITY`.

The descriptive coarse and conditional-fine head profiles were almost identical: mean layerwise Spearman correlation `0.971534`, complete top-four overlap in 21/28 layers, and block-20 overlap `4/4`. This supports a shared readability ranking, not separate coarse-head and fine-head roles. The complete evidence and null limitation are recorded in the [Summary](/Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/summary.md).

## 8. Claim Boundary And Next Decision

A stable descriptive head ranking exists, but the registered Phase-1 gate does not qualify label-specific head heterogeneity, and the two semantic granularities favor the same heads. No causal head, useful KV selector, expert insertion point, or task-improving module is established.

The sole next decision is: after the researcher reviews the completed Phase-1 four-part result, decide whether to authorize a separately frozen Phase-2 design comparing current-token state, causal history mean, actual attention retrieval, and minimal intervention. No Phase-2 design or execution begins before that review.
