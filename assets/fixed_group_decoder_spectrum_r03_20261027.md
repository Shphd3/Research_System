# R03 fixed-group decoder/spectrum offline assets

Actually saved outputs are `analysis_fixed_group_decoder_geometry_spectrum_r03_20261027` and `representation_qwen3_layer27_reference_pca_r03_20261027`. The former holds fixed-group cosine/matched nulls and spectral/panel alignment; the latter stores reference mean/covariance/basis and512decoder directions/projections. Payloads remain execution-side. [Summary](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/summary.md).

Inputs reuse original R03 groups/frequency/z, A22 and the matching-hook raw h in `representation_crosscoder_relation_learning_20261015t164000z`. Historical raw-cache Base hashes were not independently recorded, so PCA retains BOUNDED_SOURCE_CHAIN_MATCH despite verified cache bytes/hook/producer chain. Source files differ from structural VAL, but dictionary training saw the TRAIN sources and document/near-duplicate independence is Unknown.

New forwards0,cumulative1500/1500;model/dictionary training0,new clustering0,classifier fits0,PCAstatistical fits1. Semantic discrimination is NOT RUN because qualified labels and matching raw h are not paired. [Fresh strict access](checks/20261027_fixed_group_decoder_spectrum_outputs.json) is not scientific eligibility. [Appendix](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/appendix.md).

Execution root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement`.
