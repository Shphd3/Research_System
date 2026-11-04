派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R07_fixed_target_domain_spectrum_20261029/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R07_fixed_target_domain_spectrum_20261029/summary.md)；研究修改仍回到原件。

---

# Fixed-target domain response and spectral location

We asked whether math and biology contexts produce a reproducible difference at the same final token, across rewordings and unseen text families, and where this difference is readable in a fixed natural-text spectrum.

The experiment captured one true 1,024-dimensional block-27 residual-post vector before final model normalization from each of 384 constructed English prefixes. Forty-eight families were split 24/12/12 before inference. Both domains and both wordings share target identity and position within each of two neutral endings. The same frozen Qwen3-0.6B Base, tokenizer and old natural-text PCA are reused. No dictionary reconstruction or CrossCoder analysis is performed.

All four heldout wording/ending cells have positive average paired effects along the discovery-fixed direction, with positive family-bootstrap intervals and BH5 q<.05. The pooled paired difference is 60.64 [46.79,75.29]. All twelve family-averaged differences are positive, but only 41 of 48 individual paired variants are positive. The fixed zero-threshold classification is only 60.42%; the pooled probability of ranking a randomly selected math sample above a biology sample is 70.62%. Neutral endings shift the scores, so average paired generalization does not imply perfect samplewise separation.

The discovery unit mean-difference direction has 58.12% of its squared projection in the first 64 PCs. Its cosine with the heldout mean-difference direction is 0.832. Separately fitted and frozen linear readouts achieve 98.96% in the first 16 PCs, 90.63% in the last 16 and 97.92% in the last 64; the full-dimensional baseline is 98.96%. The head permits easier access at small dimensions, while substantial domain information remains readable in the tail. Mean geometry and classifier accessibility are different measurements.

These observations restrict dependence on particular families and endings within this panel. Shared vocabulary, construction style and imperfectly balanced neutral framing remain alternatives. The labels refer to constructed contexts, not natural clusters or knowledge modules. The old PCA and old natural-document mean differences are prior work, not new results.

All 392 forwards completed. Old-hook, causal-prefix and replay checks are exact; model state is unchanged. No language-model, SAE, CrossCoder or MoE training, new PCA, intervention, task, resource or sealed TEST access occurred. Only the authorized analysis readouts were fitted, with every choice frozen before heldout evaluation. Human scientific acceptance and question closure remain Unknown.

[Chinese figures and examples](../../../../../../../../UNAVAILABLE.md) · [Complete evidence](../../../../../../../../UNAVAILABLE.md).
