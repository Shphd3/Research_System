# S09: marginal overlap explanation and replicated joint structure are different findings

A: source/position marginal frequencies reproduce most of the S08-style overlap gap. B: direct coactivation statistics still exceed exact row32/column-count nulls and replicate across the internal heldout split. Overlap alone is not sufficient evidence for combinations. No semantic, functional or router mechanism is inferred.

The factual paths are: behavior/factor controls inspect metadata and token strata without answer scoring; representation analysis separates binary overlap from coactivation; functional intervention, classifier fitting and model training are NOT_RUN. Scientific acceptance/closure Unknown; stop for researcher review after delivery.

Original771documents and8positions are unchanged; each source has128discovery/129heldout documents. Discovery Bernoulli references reproduce 99.4%–127.7%of the pooled gap but only constrain expected rowcount32, with observed10–64/12–60counts and probability-estimation error. Exact heldout-margin/row32 nulls reproduce 82.9%–97.0%; these are descriptive ratios, not causal explained fractions or discovery-only forecasts. 5/6conditional document intervals for the remaining Jaccard gap span0.

| SAE | pair | real_gap | discovery_frequency_gap | fixed32_margin_gap | fixed32_ratio | remaining_gap_CI |
|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder/GSM8K | 0.014126 | 0.017108 | 0.013297 | 94.1% | [-0.000572,0.002301] |
| ATTN_SAE | Magicoder/MMLU | 0.010565 | 0.011846 | 0.008760 | 82.9% | [0.000136,0.004108] |
| ATTN_SAE | GSM8K/MMLU | 0.009900 | 0.012646 | 0.008845 | 89.3% | [-0.000719,0.003353] |
| MLPIN_SAE | Magicoder/GSM8K | 0.046637 | 0.046341 | 0.045240 | 97.0% | [-0.001008,0.003852] |
| MLPIN_SAE | Magicoder/MMLU | 0.029533 | 0.029801 | 0.027332 | 92.5% | [-0.000206,0.005047] |
| MLPIN_SAE | GSM8K/MMLU | 0.026308 | 0.029499 | 0.025209 | 95.8% | [-0.001765,0.004574] |


![A overlap and marginal references](figures/01_overlap_vs_frequency.png)

Each native dictionary uses24discovery-frequency-selected coordinates and all276pairs. Mean binary pair products over8positions/document are centered by each source's own exact-margin null. Discovery residual directions and between-source contrast directions are frozen before heldout coactivation. Own-source6/6and between-source6/6heldout contrasts pass the registered positive-direction/document-CI/mixing/conditional-null criteria; Holm separately within the two six-test families, all adjusted p=.023346. Minimum raw conditional p=1/257from256null samples; no higher p-resolution claim.

| site | dataset | heldout_real_projection | heldout_null_projection | heldout_excess | doc_CI_lo | doc_CI_hi | Holm_p |
|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | 0.186106 | 0.097805 | 0.088301 | 0.064902 | 0.110268 | 0.023346 |
| ATTN_SAE | GSM8K | 0.216684 | 0.090062 | 0.126622 | 0.099632 | 0.155953 | 0.023346 |
| ATTN_SAE | MMLU | 0.077154 | 0.027513 | 0.049641 | 0.036945 | 0.062883 | 0.023346 |
| MLPIN_SAE | Magicoder | 0.383465 | -0.074431 | 0.457896 | 0.431771 | 0.483500 | 0.023346 |
| MLPIN_SAE | GSM8K | 0.368308 | 0.053087 | 0.315221 | 0.275806 | 0.354469 | 0.023346 |
| MLPIN_SAE | MMLU | 0.171067 | -0.240288 | 0.411355 | 0.399029 | 0.424048 | 0.023346 |


| site | A | B | heldout_A_excess | heldout_B_excess | heldout_difference | doc_CI_lo | doc_CI_hi | Holm_p |
|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | 0.049623 | -0.098536 | 0.148159 | 0.120497 | 0.176919 | 0.023346 |
| ATTN_SAE | Magicoder | MMLU | 0.065604 | -0.008821 | 0.074425 | 0.055799 | 0.095029 | 0.023346 |
| ATTN_SAE | GSM8K | MMLU | 0.114482 | -0.016618 | 0.131101 | 0.102118 | 0.160289 | 0.023346 |
| MLPIN_SAE | Magicoder | GSM8K | 0.315661 | -0.085220 | 0.400881 | 0.355508 | 0.447682 | 0.023346 |
| MLPIN_SAE | Magicoder | MMLU | 0.236749 | -0.141447 | 0.378195 | 0.347057 | 0.413916 | 0.023346 |
| MLPIN_SAE | GSM8K | MMLU | 0.067408 | -0.243117 | 0.310525 | 0.263189 | 0.356736 | 0.023346 |


![B coactivation null and heldout](figures/02_joint_null_and_holdout.png)

The ordinate is pair-coactivation excess projected on unit-length discovery weights, not Jaccard, accuracy or semantic intensity. Discovery points are fitted, not validation; gray bands are algorithmic null ranges, not additional documents. The conditional intervals hold discovery weights and the estimated null center fixed; discovery-selection/probability-estimation and all null-center uncertainties are not integrated. MCSE is separate.

Example ATTN GSM8K #17625/#14773: discovery real.214844vs null.129898; heldout221/1032positions=.214147vs null.115708,94/129coactive documents. Concrete text/token/native magnitudes in tables/concrete_pair_cases.jsonl. A contrary selected MLPIN pair #20989/#24338 in GSM8K changes from below null in discovery (2/1024vs.003948) to above null in heldout (12/1032vs.003138). Aggregate replication does not imply every pair replicates; all selected pairs and all276components are retained.

All checked rows remain32unique coordinates and all feature counts are exact. Primary heldout nulls propose4,617,600row trades/site,>99.999%change; maximum scalar Rhat=1.0276, minimum ESS=129.9. Some coordinates are forced:1032/99072ATTN active edges and1677/99072MLPIN edges. Four chains,100burn sweeps,10sweeps between64samples each; finite-time diagnostics rather than asymptotic theory establish bounded numerical adequacy. See [Curveball construction/proof](https://doi.org/10.1103/PhysRevE.91.042812); unchanged trades are retained.

Token-stratified exploratory nulls remain positive but52/89strata have<8rows, and only three literal token IDs plus OTHER are constrained. S08 described formatting and did not independently match it; neither does this round. Length medians252/56/50, code fences158/257vs0vs0, question/source/topic/near-duplicate differences remain. A between-source residual contrast conditions on each source's own margins; it is not a comparison after imposing identical margins on both sources, and attainable dependence still varies with support. Nulls break document continuity across positions. This is a new internal split on already-exposed S08 documents, not external fresh confirmation. Numina remains unavailable. No feature concepts or router efficacy are assigned.

[Detailed](detailed.md), [Protocol](protocol.md), [Reproduce](reproduce.md). Wait for review; no automatic follow-up.
