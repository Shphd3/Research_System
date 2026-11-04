派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/anchor.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/anchor.md)；研究修改仍回到原件。

---

# R16 equal-rank bands and reference-mean control

## 1. Problem Definition
Within the existing spectral-semantic-granularity owner, determine whether layer-dependent native prediction retention differs across sixteen disjoint rank64 bands, and whether the observed ordering depends on restoring the TRAIN reference mean. User explicitly authorized implementation, frozen forward execution and delivery on2026-11-04.
## 2. Physical Priors
PCA variance is not occurrence frequency or semantic granularity. Restoring mean is standard affine PCA reconstruction; omitting it shifts all inputs by the same mean and changes native normalization/operating point. Equal rank does not equal energy.
## 3. Falsifiable Hypotheses
Working assumptions supplied by researcher: earlier/middle computation uses more general patterns; later computation is more complex; leading variance directions reflect more shared pattern variation and remaining directions finer variation. These are unvalidated semantic assumptions. A band/depth preference may be compatible with them; mixed or absent ordering weakens a simple spectral hierarchy.
## 4. Mathematical Model
For each layer, h and mu have1024 coordinates; Q_B is1024x64 with orthonormal columns. Add-mean h_B=mu+(h-mu)Q_B Q_B^T; no-mean g_B=(h-mu)Q_B Q_B^T. Difference is exactly mu before casting. All16 centered components sum to h-mu. All-PC add-mean is h; all-PC no-mean is h-mu, not identity.
## 5. Computational Realization
Same Qwen3-0.6B Base checkpoint/tokenizer,28 layer-specific TRAIN PCA files and175doc/700position natural panel plus37/the auxiliary panel. Each independent single-layer intervention continues native suffix. Target-only and whole-prefix scopes separated. No training or new PCA.
## 6. Minimal Falsification Tests
Equal64 bands separate rank from spectral position. Paired mean ablation separates band-only output from band+reference-mean output, while changing both mean and total vector geometry. Mean-only, zero and full-centered controls characterize the common shift. Old head64/mean/random references are reused. Energy and perturbation retained explicitly.
## 7. Current Evidence
Completed bounded measurement: affine head64 has the highest observed retention at all28layers inbothscopes; target-onlyhead with/withoutmean at1/14/25/28=77.43/17.71%,74.71/40.71%,34.29/12.71%,23.00/4.29%. Other-nonformat finalhead retention increases2.00→5.07%withoutmean while NLLworsens. All737oldheadreplays areexact afterfiveaux-onlybatchrepairs; mainmatrixunchanged. [Summary](summary.md), [Chinese](summary_cn.md), [validation](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/audit/validation.json), [amendments](amendments.md) own evidence. ScientificacceptanceUnknown.
## 8. Claim Boundary And Next Decision
Exploratory exposed English texts only. Prediction retention is not accuracy; failure under native readout does not establish absent information. No energy-matched semantic localization, identified compensation, knowledge erasure or scientific closure. Researcher acceptance Unknown.

AI interpretation only: equalrank weakens the inference that a particular late band replaces the head; mean and decoder geometry contribute. The single unresolved decision is how much of collective960support is rank/energy versus a contextual distinction. No further run is authorized by completion.
