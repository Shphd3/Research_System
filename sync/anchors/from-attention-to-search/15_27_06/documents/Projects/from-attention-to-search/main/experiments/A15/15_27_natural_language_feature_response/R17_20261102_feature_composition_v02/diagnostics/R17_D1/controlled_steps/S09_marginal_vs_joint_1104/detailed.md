派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/detailed.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/detailed.md)；研究修改仍回到原件。

---

# S09 Detailed record

## Objects, operations and execution

Reuse the exact frozen official Qwen3-0.6B-Base(28blocks,width1024) native block27SAEs,30000/ReLU-Top32. Attention=o_proj output before residual addition; MLPIN=actual mlp input after residual/post_attention_layernorm. Separate dictionaries, unrelated IDs. This round reads sparse caches only, no model load or forward. Three question-only sources257documents each, original8quantile positions on first min(length,128)tokens; no answers/options. Source Arrow versions/fields remain in S08 data/sources.json; this round binds exact sparse cache/panel hashes.

Within source order SHA256(seed2026110409+'S09'+ID),128discovery/129heldout, all8positions stay together. Within all unordered pairs; cross cyclic offsets1..64,8256unique pairs/group, no self pairs. Position Jaccards are calculated and then averaged; repeated edges/positions are not independent documents.

A computes all discovery probabilities separately by source and quantile, simulates256whole heldout-size independent Bernoulli panels (expected rowcount32, not exact32), and computes actual Jaccards. E[I]=sum p_Ap_Bis exact for independent draws; plugin sum p²has finite probability-estimation bias, and the distinct unbiased discovery intersection U-statistic is reported. Neither is substituted into Jaccard. The exact heldout-count/row32 conditional reference is descriptive, not a discovery forecast. For row32, J=I/64+I²/[64(64-I)]; mean within I is fixed by column counts, higher moments can still alter mean J. Full cross mean I is likewise fixed, while the original balanced cyclic subset can fluctuate. Descriptive intersection distributions use8fixed audit snapshots only.

Curveball trades within source/split/quantile preserve row32and all feature counts; unchanged trades retained.4chains,100burn sweeps,10sweeps between64draws/chain, each sweep ceil(n/2)row-pair proposals. Check every snapshot's unique coordinates/column counts, changed-trade fraction, original-edge retention against sum c²/(n²*32), split-Rhat/ESS. The toy90-state fixed-degree space is an implementation check, not empirical research evidence. Finite diagnostics do not prove perfect mixing.

Discovery picks24IDs by marginal count/document support, all276pairs enter the primary score. Per-document pair product is averaged across8positions. Each source's discovery excess over its own null defines a unit direction; source residual differences define independent frozen contrast weights. Heldout own projections and cross-source residual contrasts test different predictions. Two six-test Holm families,256conditional-null samples,999whole-document bootstrap CIs conditional on fixed discovery weights and estimated null centers. Discovery fitting/selection uncertainty and all null-center uncertainty are not integrated into those CIs; MCSE separate. Nulls can break cross-position document continuity.

Secondary24member-count histograms, discovery-top8exact bit patterns+OTHER, all12discovery-chosen example pairs including adverse/zero results. Exploratory token-conditioned null fixes discovery-top3literal IDs279/315/13orOTHER and keeps original weights. It does not independently match formatting or every lexical item. Between-source excess differences do not impose identical source margins or identify invariant dependence parameters. No semantic labels, classifier/readout fitting, interventions or router utility.

Independent verification covers80unchanged S08files,771document split,200set Jaccards,32audit-snapshot pair vectors,768stratum-margin checks, fixed-intersection identity,24projections and two Holm families. Source counts/marginals, seed/rules and all primary/exploratory results retained. Scientific acceptance/closureUnknown, NuminaMISSING; stop for review.

## A all three means and references

| site | A | B | comparison | real_J | real_CI_lo | real_CI_hi | discovery_Bernoulli_J | real_minus_Bernoulli | heldout_fixed32_margin_J | real_minus_fixed32_margin |
|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | within_A | 0.035707 | 0.033468 | 0.038309 | 0.037457 | -0.001750 | 0.034054 | 0.001653 |
| ATTN_SAE | Magicoder | GSM8K | within_B | 0.017482 | 0.016263 | 0.018747 | 0.020486 | -0.003004 | 0.017342 | 0.000139 |
| ATTN_SAE | Magicoder | GSM8K | cross | 0.012468 | 0.011609 | 0.013428 | 0.011863 | 0.000605 | 0.012401 | 0.000067 |
| ATTN_SAE | Magicoder | GSM8K | pooled_gap | 0.014126 | 0.012725 | 0.015598 | 0.017108 | -0.002982 | 0.013297 | 0.000829 |
| ATTN_SAE | Magicoder | MMLU | within_A | 0.035707 | 0.033468 | 0.038309 | 0.037457 | -0.001750 | 0.034054 | 0.001653 |
| ATTN_SAE | Magicoder | MMLU | within_B | 0.026412 | 0.023358 | 0.030711 | 0.027848 | -0.001436 | 0.024380 | 0.002032 |
| ATTN_SAE | Magicoder | MMLU | cross | 0.020494 | 0.020062 | 0.020962 | 0.020806 | -0.000312 | 0.020456 | 0.000038 |
| ATTN_SAE | Magicoder | MMLU | pooled_gap | 0.010565 | 0.008896 | 0.012869 | 0.011846 | -0.001281 | 0.008760 | 0.001805 |
| ATTN_SAE | GSM8K | MMLU | within_A | 0.017482 | 0.016263 | 0.018747 | 0.020486 | -0.003004 | 0.017342 | 0.000139 |
| ATTN_SAE | GSM8K | MMLU | within_B | 0.026412 | 0.023358 | 0.030711 | 0.027848 | -0.001436 | 0.024380 | 0.002032 |
| ATTN_SAE | GSM8K | MMLU | cross | 0.012047 | 0.011212 | 0.012958 | 0.011521 | 0.000526 | 0.012016 | 0.000031 |
| ATTN_SAE | GSM8K | MMLU | pooled_gap | 0.009900 | 0.008126 | 0.012198 | 0.012646 | -0.002746 | 0.008845 | 0.001055 |
| MLPIN_SAE | Magicoder | GSM8K | within_A | 0.119809 | 0.116053 | 0.123955 | 0.119551 | 0.000258 | 0.117224 | 0.002585 |
| MLPIN_SAE | Magicoder | GSM8K | within_B | 0.098103 | 0.095286 | 0.100882 | 0.099485 | -0.001383 | 0.097680 | 0.000422 |
| MLPIN_SAE | Magicoder | GSM8K | cross | 0.062319 | 0.060568 | 0.063950 | 0.063178 | -0.000859 | 0.062212 | 0.000107 |
| MLPIN_SAE | Magicoder | GSM8K | pooled_gap | 0.046637 | 0.044233 | 0.049093 | 0.046341 | 0.000296 | 0.045240 | 0.001396 |
| MLPIN_SAE | Magicoder | MMLU | within_A | 0.119809 | 0.116053 | 0.123955 | 0.119551 | 0.000258 | 0.117224 | 0.002585 |
| MLPIN_SAE | Magicoder | MMLU | within_B | 0.079965 | 0.076133 | 0.084679 | 0.081924 | -0.001959 | 0.077960 | 0.002005 |
| MLPIN_SAE | Magicoder | MMLU | cross | 0.070354 | 0.068269 | 0.072429 | 0.070937 | -0.000582 | 0.070260 | 0.000094 |
| MLPIN_SAE | Magicoder | MMLU | pooled_gap | 0.029533 | 0.027126 | 0.032378 | 0.029801 | -0.000268 | 0.027332 | 0.002201 |
| MLPIN_SAE | GSM8K | MMLU | within_A | 0.098103 | 0.095286 | 0.100882 | 0.099485 | -0.001383 | 0.097680 | 0.000422 |
| MLPIN_SAE | GSM8K | MMLU | within_B | 0.079965 | 0.076133 | 0.084679 | 0.081924 | -0.001959 | 0.077960 | 0.002005 |
| MLPIN_SAE | GSM8K | MMLU | cross | 0.062726 | 0.060686 | 0.064973 | 0.061205 | 0.001520 | 0.062612 | 0.000114 |
| MLPIN_SAE | GSM8K | MMLU | pooled_gap | 0.026308 | 0.023444 | 0.029783 | 0.029499 | -0.003191 | 0.025209 | 0.001100 |

## A intersection identity

| site | comparison | analytic_discovery_plugin_E_intersection | discovery_unbiased_E_intersection | MC_Bernoulli_mean_intersection | real_heldout_intersection | fixed32_null_mean_intersection | fixed32_null_intersection_range | real_J_linear_I_over64 | real_J_curvature | null_J_curvature_mean | full_cross_real_J | full_cross_null_J |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | within_Magicoder | 2.285522 | 2.051550 | 2.285406 | 2.080245 | 2.080245 | 0.000000 | 0.032504 | 0.003203 | 0.001550 | nan | nan |
| ATTN_SAE | within_GSM8K | 1.277649 | 1.035741 | 1.277881 | 1.076490 | 1.076490 | 0.000000 | 0.016820 | 0.000662 | 0.000522 | nan | nan |
| ATTN_SAE | within_MMLU | 1.715714 | 1.477255 | 1.715194 | 1.512536 | 1.512536 | 0.000000 | 0.023633 | 0.002779 | 0.000746 | nan | nan |
| ATTN_SAE | Magicoder/GSM8K | 0.740791 | 0.740791 | 0.741330 | 0.777647 | 0.775616 | 0.007025 | 0.012151 | 0.000317 | 0.000282 | 0.012435 | 0.012402 |
| ATTN_SAE | Magicoder/MMLU | 1.288101 | 1.288101 | 1.287259 | 1.278192 | 1.277729 | 0.005950 | 0.019972 | 0.000523 | 0.000492 | 0.020485 | 0.020455 |
| ATTN_SAE | GSM8K/MMLU | 0.719322 | 0.719322 | 0.719914 | 0.751438 | 0.751862 | 0.006480 | 0.011741 | 0.000306 | 0.000268 | 0.012055 | 0.012016 |
| MLPIN_SAE | within_Magicoder | 6.756134 | 6.557363 | 6.752419 | 6.636234 | 6.636234 | 0.000000 | 0.103691 | 0.016118 | 0.013533 | nan | nan |
| MLPIN_SAE | within_GSM8K | 5.733582 | 5.526759 | 5.734544 | 5.653358 | 5.653358 | 0.000000 | 0.088334 | 0.009769 | 0.009347 | nan | nan |
| MLPIN_SAE | within_MMLU | 4.796555 | 4.582354 | 4.798862 | 4.577580 | 4.577580 | 0.000000 | 0.071525 | 0.008441 | 0.006436 | nan | nan |
| MLPIN_SAE | Magicoder/GSM8K | 3.765572 | 3.765572 | 3.765533 | 3.714950 | 3.712700 | 0.011825 | 0.058046 | 0.004273 | 0.004201 | 0.062277 | 0.062209 |
| MLPIN_SAE | Magicoder/MMLU | 4.193459 | 4.193459 | 4.193485 | 4.151814 | 4.156009 | 0.017518 | 0.064872 | 0.005482 | 0.005322 | 0.070433 | 0.070262 |
| MLPIN_SAE | GSM8K/MMLU | 3.649780 | 3.649780 | 3.655132 | 3.730802 | 3.730937 | 0.014323 | 0.058294 | 0.004432 | 0.004316 | 0.062727 | 0.062614 |

## B own-source primary/exploratory

| site | dataset | mode | heldout_real_projection | heldout_null_projection | heldout_excess | doc_CI_lo | doc_CI_hi | p_null | Holm_p | mixing_pass | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | position | 0.186106 | 0.097805 | 0.088301 | 0.064902 | 0.110268 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | position | 0.216684 | 0.090062 | 0.126622 | 0.099632 | 0.155953 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | MMLU | position | 0.077154 | 0.027513 | 0.049641 | 0.036945 | 0.062883 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | position_token3 | 0.186106 | 0.102254 | 0.083852 | 0.061037 | 0.105257 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | position_token3 | 0.216684 | 0.092557 | 0.124128 | 0.097466 | 0.153167 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | MMLU | position_token3 | 0.077154 | 0.032407 | 0.044748 | 0.033044 | 0.057352 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | position | 0.383465 | -0.074431 | 0.457896 | 0.431771 | 0.483500 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | position | 0.368308 | 0.053087 | 0.315221 | 0.275806 | 0.354469 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | MMLU | position | 0.171067 | -0.240288 | 0.411355 | 0.399029 | 0.424048 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | position_token3 | 0.383465 | -0.053158 | 0.436623 | 0.410488 | 0.463270 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | position_token3 | 0.368308 | 0.083922 | 0.284386 | 0.246002 | 0.322759 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | MMLU | position_token3 | 0.171067 | -0.207783 | 0.378851 | 0.366457 | 0.390974 | 0.003891 | nan | True | SUPPORTED_STATISTIC |

## B source contrasts

| site | A | B | mode | heldout_A_excess | heldout_B_excess | heldout_difference | doc_CI_lo | doc_CI_hi | p_null | Holm_p | mixing_pass | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | position | 0.049623 | -0.098536 | 0.148159 | 0.120497 | 0.176919 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | MMLU | position | 0.065604 | -0.008821 | 0.074425 | 0.055799 | 0.095029 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | MMLU | position | 0.114482 | -0.016618 | 0.131101 | 0.102118 | 0.160289 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | GSM8K | position_token3 | 0.047050 | -0.096692 | 0.143742 | 0.116514 | 0.172176 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | MMLU | position_token3 | 0.062442 | -0.008735 | 0.071177 | 0.052980 | 0.091847 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | MMLU | position_token3 | 0.112102 | -0.015034 | 0.127136 | 0.098364 | 0.156005 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | GSM8K | position | 0.315661 | -0.085220 | 0.400881 | 0.355508 | 0.447682 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | MMLU | position | 0.236749 | -0.141447 | 0.378195 | 0.347057 | 0.413916 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | MMLU | position | 0.067408 | -0.243117 | 0.310525 | 0.263189 | 0.356736 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | GSM8K | position_token3 | 0.306558 | -0.074816 | 0.381374 | 0.335781 | 0.428185 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | MMLU | position_token3 | 0.233239 | -0.135879 | 0.369119 | 0.338627 | 0.402540 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | MMLU | position_token3 | 0.060298 | -0.221665 | 0.281962 | 0.235467 | 0.328211 | 0.003891 | nan | True | SUPPORTED_STATISTIC |

## Actual constraints

| site | mode | split | rows_per_source | per_snapshot_strata | checked_snapshots | max_column_error | row_degree | changed_trade_fraction | proposals | moved_edges | mean_abs_retention_error | lowN_strata | total_strata | locked_feature_edges | total_edges |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | position | heldout | 129 | 24 | 6144 | 0 | 32 | 0.999998 | 4617600 | 140577616 | 0.000224 | 0 | 24 | 1032.000000 | 99072 |
| ATTN_SAE | position_token3 | heldout | 129 | 89 | 22784 | 0 | 32 | 0.999993 | 4626480 | 139972208 | 0.002349 | 52 | 89 | 1511.000000 | 99072 |
| MLPIN_SAE | position | heldout | 129 | 24 | 6144 | 0 | 32 | 0.999998 | 4617600 | 121811576 | 0.000321 | 0 | 24 | 1677.000000 | 99072 |
| MLPIN_SAE | position_token3 | heldout | 129 | 89 | 22784 | 0 | 32 | 0.999993 | 4626480 | 120114102 | 0.002084 | 52 | 89 | 3245.000000 | 99072 |

## Recognition and remaining uncertainty

 #17625/#14773: discovery real.214844vs null.129898; heldout221/1032positions=.214147vs null.115708,94/129coactive documents. Concrete text/token/native magnitudes in tables/concrete_pair_cases.jsonl. A contrary selected MLPIN pair #20989/#24338 in GSM8K changes from below null in discovery (2/1024vs.003948) to above null in heldout (12/1032vs.003138). Aggregate replication does not imply every pair replicates; all selected pairs and all276components are retained.

All checked rows remain32unique coordinates and all feature counts are exact. Primary heldout nulls propose4,617,600row trades/site,>99.999%change; maximum scalar Rhat=1.0276, minimum ESS=129.9. Some coordinates are forced:1032/99072ATTN active edges and1677/99072MLPIN edges. Four chains,100burn sweeps,10sweeps between64samples each; finite-time diagnostics rather than asymptotic theory establish bounded numerical adequacy. See [Curveball construction/proof](https://doi.org/10.1103/PhysRevE.91.042812); unchanged trades are retained.

Token-stratified exploratory nulls remain positive but52/89strata have<8rows, and only three literal token IDs plus OTHER are constrained. S08 described formatting and did not independently match it; neither does this round. Length medians252/56/50, code fences158/257vs0vs0, question/source/topic/near-duplicate differences remain. A between-source residual contrast conditions on each source's own margins; it is not a comparison after imposing identical margins on both sources, and attainable dependence still varies with support. Nulls break document continuity across positions. This is a new internal split on already-exposed S08 documents, not external fresh confirmation. Numina remains unavailable. No feature concepts or router efficacy are assigned.

[Detailed](detailed.md), [Protocol](protocol.md), [Reproduce](reproduce.md). Wait for review; no automatic follow-up.
