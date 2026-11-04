派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/detailed.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/detailed.md)；研究修改仍回到原件。

---

# S08 Detailed result


Across the three readable sources with257 questions each, 6/6 native-SAE/source-pair comparisons meet the frozen both-sides-higher criterion. Passing conditions: ATTN_SAE:Magicoder/GSM8K; ATTN_SAE:Magicoder/MMLU; ATTN_SAE:GSM8K/MMLU; MLPIN_SAE:Magicoder/GSM8K; MLPIN_SAE:Magicoder/MMLU; MLPIN_SAE:GSM8K/MMLU. Other conditions: none. This is dataset-conditioned member similarity, not an identification of domain knowledge or a functional mechanism.

Factual paths: behavior/factor controls describe length, format and literal tokens without answer scoring; representation analysis compares binary supports in the frozen model; functional intervention and training are NOT_RUN. Hook and numerical checks concern measurement quality. Scientific acceptance and closure remain Unknown.

| SAE | pair | A_within | B_within | cross | pooled_difference_95CI | Holm_p | both_sides |
|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder/GSM8K | 0.0351 | 0.0171 | 0.0122 | 0.0139 [0.0129,0.0149] | 0.006 | BOTH_WITHIN_HIGHER |
| ATTN_SAE | Magicoder/MMLU | 0.0351 | 0.0256 | 0.0206 | 0.0098 [0.0086,0.0111] | 0.006 | BOTH_WITHIN_HIGHER |
| ATTN_SAE | GSM8K/MMLU | 0.0171 | 0.0256 | 0.0118 | 0.0096 [0.0084,0.0109] | 0.006 | BOTH_WITHIN_HIGHER |
| MLPIN_SAE | Magicoder/GSM8K | 0.1187 | 0.0968 | 0.0627 | 0.0450 [0.0433,0.0468] | 0.006 | BOTH_WITHIN_HIGHER |
| MLPIN_SAE | Magicoder/MMLU | 0.1187 | 0.0796 | 0.0707 | 0.0284 [0.0268,0.0302] | 0.006 | BOTH_WITHIN_HIGHER |
| MLPIN_SAE | GSM8K/MMLU | 0.0968 | 0.0796 | 0.0620 | 0.0262 [0.0242,0.0282] | 0.006 | BOTH_WITHIN_HIGHER |


A/B order follows the pair column. Each document-pair value averages8 aligned-quantile Jaccards, intersection/union of strictly positive native coordinates. Within A, within B and cross use32,896 distinct pairs each at257 documents/source, not32,896 independent units. Pooled difference is mean(within A,within B)-cross.1,999 document-count bootstrap samples;999 whole-document label permutations; Holm across six main pooled tests. Individual side intervals remain in [full statistics](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/tables/overlap_summary.csv).


## Methods and interpretation of each comparison

Read complete selected Arrow tables and the exact question field; normalized NFKC/casefold/whitespace hashes remove exact repeats, while inference retains internal formatting. MMLU14042rows become13866unique questions;176duplicates. Magicoder75197and GSM8K7473remain unique. Uniform permutation/rejection sampling selects257 questions with>=16tokens/source; MMLU examines359candidates with102short exclusions. Full-population token eligibility was not counted.257is the frozen fast-analysis quota, not a claim of full-corpus inference.

Input the first min(full_length,128)tokens without special tokens, instruction wrappers or answer suffix. Eight positions floor((j+.5)*visible_length/8) are paired by equal quantile index. Main Jaccard averages eight support-set ratios per document pair; it does not pool amplitudes or treat token positions as independent documents.

Frozen official Qwen3-0.6B-Base,28blocks,width1024, FP32CPU2threads,physical8x128. Attention is block27.self_attn.o_proj output before residual addition; MLPIN is actual block27.mlp input after residual/post_attention_layernorm. Each native dictionary is30000/ReLU-Top32; active iff selected z>0. No extra input normalization or decoder-bias subtraction; dictionaries have unrelated IDs. Model body forward avoids unnecessary vocabulary logits. No answer scoring, training, readout fitting or interventions. Source hashes and native loaders are in frozen_plan.json.

Order each source by SHA256('S08'+document ID). Within use all unordered i<j; cross pair A_i with B_(i+offset mod N), offsets1..(N-1)/2. Each group hasN(N-1)/2unique edges; cross has equal degree. Main32896edges/group times8positions=263168token-position comparisons, not independent samples. Explicit graph endpoints and global IDs are saved.

1999independent within-source multinomial document-count bootstraps reweight each original edge by c_i*c_j, retaining all position/pair incidences together. No original self edges are added.999 whole-document label permutations reapply the same pairing rule after relabeling; plus-one p. The null is whole-document representation exchangeability under source labels, not randomized semantic content. Six main one-sided pooled differences use Holm.05; confidence intervals are marginal document-bootstrap intervals and individual sides are retained. Exact per-cell seeds are saved.

Full-token-length bins16/32/48/64/96/128/192/256/512/1024/2048+/infinity take equal counts per source/bin; remove one same-bin document per side if needed for oddN. Stratified permutations preserve bin counts. Fixed32and16causal prefixes control observed context length, not total question length. Fixed16 was added before activation availability due only to11-doc full-length matching for Magicoder/GSM8K; original frozen protocol, plan and panel remain byte-identical.

Same-token controls fix up to3literal token IDs with>=20document coverage/source before responses. Average matching token-position Jaccards within each document pair; leave nonmatching edges missing and report coverage. Document bootstrap only, no conditional permutation claim. This selects a different token/context distribution, so its change from main is not a causal lexical-effect estimate.

The separate amplitude supplement computes raw RMS coordinate difference on positive shared members per aligned position, denominator=shared member count, missing if none, then eligible-position/document-pair averaging. Whole-zL2, hL2, decoder norms and reconstruction error remain separate diagnostics.

## All controls

| site | A | B | mode | N_A | within_A | within_B | cross | A_minus_cross_lo | B_minus_cross_lo | pooled_minus_cross | pooled_minus_cross_lo | pooled_minus_cross_hi | p_pooled_one_sided | cross_actual_pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | length_matched | 11 | 0.035245 | 0.016378 | 0.006829 | 0.021827 | 0.004165 | 0.018982 | 0.013988 | 0.024113 | 0.001000 | 55 |
| ATTN_SAE | Magicoder | GSM8K | fixed32 | 249 | 0.028491 | 0.016681 | 0.009676 | 0.016888 | 0.004906 | 0.012911 | 0.011225 | 0.014575 | 0.001000 | 30876 |
| ATTN_SAE | Magicoder | GSM8K | fixed16 | 257 | 0.033622 | 0.013091 | 0.010012 | 0.021110 | 0.001486 | 0.013345 | 0.011689 | 0.015133 | 0.001000 | 32896 |
| ATTN_SAE | Magicoder | GSM8K | same_token | 257 | 0.052522 | 0.023681 | 0.013058 | 0.034029 | 0.007781 | 0.025044 | 0.021773 | 0.028822 | nan | 4587 |
| ATTN_SAE | Magicoder | MMLU | length_matched | 59 | 0.035417 | 0.023546 | 0.018960 | 0.013491 | 0.003018 | 0.010521 | 0.008763 | 0.012644 | 0.001000 | 1711 |
| ATTN_SAE | Magicoder | MMLU | fixed32 | 161 | 0.029206 | 0.054011 | 0.018493 | 0.008776 | 0.017648 | 0.023116 | 0.014116 | 0.035825 | 0.001000 | 12880 |
| ATTN_SAE | Magicoder | MMLU | fixed16 | 257 | 0.033622 | 0.033182 | 0.019690 | 0.011753 | 0.006077 | 0.013712 | 0.009939 | 0.019301 | 0.001000 | 32896 |
| ATTN_SAE | Magicoder | MMLU | same_token | 257 | 0.064403 | 0.041122 | 0.024099 | 0.033369 | 0.012223 | 0.028664 | 0.024375 | 0.033504 | nan | 6457 |
| ATTN_SAE | GSM8K | MMLU | length_matched | 121 | 0.017526 | 0.033174 | 0.012440 | 0.003748 | 0.013957 | 0.012910 | 0.009431 | 0.017582 | 0.001000 | 7260 |
| ATTN_SAE | GSM8K | MMLU | fixed32 | 161 | 0.016032 | 0.054011 | 0.009522 | 0.004415 | 0.025918 | 0.025500 | 0.015954 | 0.037989 | 0.001000 | 12880 |
| ATTN_SAE | GSM8K | MMLU | fixed16 | 257 | 0.013091 | 0.033182 | 0.009172 | 0.002359 | 0.016596 | 0.013964 | 0.010066 | 0.019039 | 0.001000 | 32896 |
| ATTN_SAE | GSM8K | MMLU | same_token | 257 | 0.019675 | 0.047413 | 0.015204 | 0.001877 | 0.023393 | 0.018341 | 0.013819 | 0.024579 | nan | 5284 |
| MLPIN_SAE | Magicoder | GSM8K | length_matched | 11 | 0.115964 | 0.102870 | 0.062023 | 0.041962 | 0.033384 | 0.047394 | 0.039790 | 0.055556 | 0.001000 | 55 |
| MLPIN_SAE | Magicoder | GSM8K | fixed32 | 249 | 0.116079 | 0.097801 | 0.065890 | 0.045359 | 0.027907 | 0.041050 | 0.038081 | 0.044231 | 0.001000 | 30876 |
| MLPIN_SAE | Magicoder | GSM8K | fixed16 | 257 | 0.120424 | 0.094315 | 0.061787 | 0.053655 | 0.028828 | 0.045582 | 0.042498 | 0.048534 | 0.001000 | 32896 |
| MLPIN_SAE | Magicoder | GSM8K | same_token | 257 | 0.213164 | 0.153879 | 0.099114 | 0.101724 | 0.047563 | 0.084407 | 0.077263 | 0.092115 | nan | 4587 |
| MLPIN_SAE | Magicoder | MMLU | length_matched | 59 | 0.116656 | 0.074691 | 0.064262 | 0.047124 | 0.006512 | 0.031412 | 0.027735 | 0.035166 | 0.001000 | 1711 |
| MLPIN_SAE | Magicoder | MMLU | fixed32 | 161 | 0.119839 | 0.103416 | 0.074078 | 0.040093 | 0.012671 | 0.037549 | 0.029332 | 0.048526 | 0.001000 | 12880 |
| MLPIN_SAE | Magicoder | MMLU | fixed16 | 257 | 0.120424 | 0.082234 | 0.071220 | 0.044612 | 0.003995 | 0.030109 | 0.025845 | 0.035735 | 0.001000 | 32896 |
| MLPIN_SAE | Magicoder | MMLU | same_token | 257 | 0.214227 | 0.122789 | 0.117402 | 0.086728 | 0.000601 | 0.051107 | 0.045623 | 0.057156 | nan | 6457 |
| MLPIN_SAE | GSM8K | MMLU | length_matched | 121 | 0.097815 | 0.086297 | 0.064823 | 0.029623 | 0.014378 | 0.027233 | 0.022915 | 0.032394 | 0.001000 | 7260 |
| MLPIN_SAE | GSM8K | MMLU | fixed32 | 161 | 0.097955 | 0.103416 | 0.061523 | 0.032081 | 0.023537 | 0.039163 | 0.029377 | 0.052070 | 0.001000 | 12880 |
| MLPIN_SAE | GSM8K | MMLU | fixed16 | 257 | 0.094315 | 0.082234 | 0.058106 | 0.032573 | 0.016976 | 0.030168 | 0.025779 | 0.035367 | 0.001000 | 32896 |
| MLPIN_SAE | GSM8K | MMLU | same_token | 257 | 0.134127 | 0.132462 | 0.092911 | 0.034107 | 0.028765 | 0.040383 | 0.033725 | 0.049058 | nan | 5284 |

## Exact source versions

```json
{
  "Magicoder": {
    "asset": "hf_prepared_ise_uiuc_magicoder_oss_instruct_75_k",
    "repo": "ise-uiuc/Magicoder-OSS-Instruct-75K",
    "revision": "5f839b1f368a76b161028bb9edff055db34022b2",
    "field": "problem",
    "split": "train",
    "file": "/data/share/109_cache_dir/hf_data/datasets/ise-uiuc___magicoder-oss-instruct-75_k/default/0.0.0/5f839b1f368a76b161028bb9edff055db34022b2/magicoder-oss-instruct-75_k-train.arrow",
    "sha256": "d4724bb2a38cb74105dc9034f08117fa60e9de82286a0e6ae32f30b4a3970611"
  },
  "GSM8K": {
    "asset": "hf_prepared_gsm8k",
    "repo": "gsm8k",
    "revision": "e53f048856ff4f594e959d75785d2c2d37b678ee",
    "field": "question",
    "split": "train",
    "file": "/data/share/109_cache_dir/hf_data/datasets/gsm8k/main/0.0.0/e53f048856ff4f594e959d75785d2c2d37b678ee/gsm8k-train.arrow",
    "sha256": "6146bca074f4c6c5e07de7e96cc968adab3833dbdafeda21830f27558eea3d9b"
  },
  "MMLU": {
    "asset": "hf_prepared_cais_mmlu",
    "repo": "cais/mmlu",
    "revision": "c30699e8356da336a370243923dbaf21066bb9fe",
    "field": "question",
    "split": "test",
    "file": "/data/share/109_cache_dir/hf_data/datasets/cais___mmlu/all/0.0.0/c30699e8356da336a370243923dbaf21066bb9fe/mmlu-test.arrow",
    "sha256": "58769d67ced092719390e496f1d4bbf8b99c43b77bba39d054b9a09aecb63cab"
  }
}
```

| dataset | N | median_full_tokens | min_full_tokens | max_full_tokens | median_visible_tokens | truncated | code_fence | with_newline | with_question_mark |
|---|---|---|---|---|---|---|---|---|---|
| Magicoder | 257 | 252.000000 | 62 | 793 | 128.000000 | 248 | 158 | 257 | 9 |
| GSM8K | 257 | 56.000000 | 28 | 168 | 56.000000 | 4 | 0 | 0 | 249 |
| MMLU | 257 | 50.000000 | 16 | 613 | 50.000000 | 50 | 0 | 27 | 179 |

## Native dictionary quality

| site | dataset | N | positions_per_doc | active_min | active_max | active_mean | z_L2_mean | z_L2_doc_SD | h_L2_mean | relative_reconstruction_error_mean | relative_reconstruction_error_p95 | decoder_norm_min | decoder_norm_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | 257 | 8 | 32 | 32 | 32.000000 | 38.945469 | 4.912744 | 66.669350 | 0.535184 | 0.637810 | 0.999999 | 1.000001 |
| ATTN_SAE | GSM8K | 257 | 8 | 32 | 32 | 32.000000 | 50.016098 | 8.426587 | 98.497192 | 0.705962 | 0.818755 | 0.999999 | 1.000001 |
| ATTN_SAE | MMLU | 257 | 8 | 32 | 32 | 32.000000 | 52.429012 | 7.733827 | 81.478737 | 0.455528 | 0.603645 | 0.999999 | 1.000001 |
| MLPIN_SAE | Magicoder | 257 | 8 | 32 | 32 | 32.000000 | 87.849968 | 5.517982 | 110.716728 | 0.312248 | 0.431924 | 0.999999 | 1.000001 |
| MLPIN_SAE | GSM8K | 257 | 8 | 32 | 32 | 32.000000 | 119.931221 | 25.402987 | 148.492889 | 0.401202 | 0.521990 | 0.999999 | 1.000001 |
| MLPIN_SAE | MMLU | 257 | 8 | 32 | 32 | 32.000000 | 86.108810 | 9.080378 | 114.101753 | 0.281253 | 0.443278 | 0.999999 | 1.000001 |

## Separate shared-member amplitude

| site | A | B | within_A | within_B | cross | pooled_minus_cross |
|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | 5.916856 | 9.218238 | 11.070833 | -3.503286 |
| ATTN_SAE | Magicoder | MMLU | 5.916856 | 10.275075 | 10.538594 | -2.442629 |
| ATTN_SAE | GSM8K | MMLU | 9.218238 | 10.275075 | 16.251305 | -6.504649 |
| MLPIN_SAE | Magicoder | GSM8K | 13.780904 | 27.680134 | 37.648341 | -16.917822 |
| MLPIN_SAE | Magicoder | MMLU | 13.780904 | 17.141076 | 20.144026 | -4.683036 |
| MLPIN_SAE | GSM8K | MMLU | 27.680134 | 17.141076 | 36.533608 | -14.123003 |

## Limits and numerical audit

Formatting, topic, task/source and lexical choices co-vary; controls cannot uniquely identify domain knowledge. Near duplicates, pretraining exposure and incomplete MMLU stems remain. Native Top32competition is a measurement constraint, not a semantic finding. Reconstruction and one-model/one-layer/prefix sampling limit claims. Weak length matching and intervals crossing0are insufficient, not evidence of no difference. No-op and fixed32prefix equivalence,200independent Python-set checks,90saved-edge mean replays, graph degrees and six Holm adjustments are audited in evidence/independent_verification.json. Full texts and exact token positions in data/panel.jsonl, native sparse coordinates in cache/activations.npz, deterministic unselected examples in tables/deterministic_examples.jsonl. Scientific acceptance Unknown.

Source/topic mixture: Magicoder programming questions (python139/257 as programming-language metadata), GSM8K grade-school math stories, MMLU mixed subjects (professional_law36/257,moral_scenarios30/257), uniformly sampled by question rather than subject-balanced. Dataset identity is not a fine semantic class.

## Bounded recognition update and posthoc descriptive counterexamples


Recognition update: the overlap subprediction generalizes from constructed families to these three natural question sources. Both-side95% intervals remain positive in the four limited controls; none removes the observed association. This does not test semantic parent/child recruitment or adjudicate H2. Group means do not describe every document:57/257 MMLU documents have lower same-source neighbor means than cross-Magicoder means in MLPIN;48/257 GSM8K documents do so against Magicoder in Attention. A posthoc descriptive counterexample is MMLU:test:row6874, text: 'Statement 1| The softmax function is commonly used in mutliclass logistic regression. Statement 2| The temperature of a nonuniform softmax distribution affects its entropy.'. Its within-MMLU mean=0.071092, cross-Magicoder=0.086829. These are dependent descriptive points, not new confirmatory tests. Same-token MLPIN MMLU-minus-cross-Magicoder is only.005388[.000601,.011027], closer to the boundary than main.008862. Control subsets/token distributions differ; their change from main is not a causal effect estimate.
| site | pair | dataset | N | negative_documents | zero_documents | min_advantage | median_advantage |
|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder/GSM8K | Magicoder | 257 | 0 | 0 | 0.003836 | 0.021865 |
| ATTN_SAE | Magicoder/GSM8K | GSM8K | 257 | 48 | 0 | -0.008484 | 0.005147 |
| ATTN_SAE | Magicoder/MMLU | Magicoder | 257 | 0 | 0 | 0.003483 | 0.013272 |
| ATTN_SAE | Magicoder/MMLU | MMLU | 257 | 32 | 0 | -0.007512 | 0.002211 |
| ATTN_SAE | GSM8K/MMLU | GSM8K | 257 | 37 | 0 | -0.009199 | 0.005114 |
| ATTN_SAE | GSM8K/MMLU | MMLU | 257 | 0 | 0 | 0.002435 | 0.010754 |
| MLPIN_SAE | Magicoder/GSM8K | Magicoder | 257 | 0 | 0 | 0.012105 | 0.057365 |
| MLPIN_SAE | Magicoder/GSM8K | GSM8K | 257 | 2 | 0 | -0.012561 | 0.035947 |
| MLPIN_SAE | Magicoder/MMLU | Magicoder | 257 | 0 | 0 | 0.019018 | 0.048364 |
| MLPIN_SAE | Magicoder/MMLU | MMLU | 257 | 57 | 0 | -0.015738 | 0.008748 |
| MLPIN_SAE | GSM8K/MMLU | GSM8K | 257 | 1 | 0 | -0.001421 | 0.036533 |
| MLPIN_SAE | GSM8K/MMLU | MMLU | 257 | 29 | 0 | -0.024747 | 0.017546 |
