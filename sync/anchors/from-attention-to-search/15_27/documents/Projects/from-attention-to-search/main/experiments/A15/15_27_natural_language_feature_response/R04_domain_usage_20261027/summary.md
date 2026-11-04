派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/summary.md)；研究修改仍回到原件。

---

# R04: domain-referenced feature usage and context response

We ask whether existing features show reproducible shared, mathematics-biased or biology-biased usage, and whether the same coordinates respond to domain edits at identical target tokens. This implements the 1027 discussion's suggestion to define a relationship before measuring feature properties. It is a preliminary domain-referenced analysis.

The primary readout is the native E16 SAE on block27 MLP input. The separate CrossCoder analysis uses A22's native fourteen-layer shared z and its block27 reconstruction contribution. Both received identical texts and selected candidates independently. The completed run used 120 real documents, 72 constructed prefixes, 256 DCLM reference windows and eight checks: **456/512** new sequence forwards. No model or dictionary was trained. Replay and visible-prefix checks passed.

Each dictionary selected 32 shared and 32 biased candidates, with 16 biased toward each domain. All 32 biased directions recurred in heldout documents; all 32 shared candidates occurred in both domains. Shared/biased heldout balanced accuracy was **95%/100% for SAE** and **92.5%/97.5% for CrossCoder**. The corresponding matched-random means were 75.875%/73.5% and 85.625%/95.625%; some CrossCoder random sets reached 100%. The token bag baseline reached 95%. All four selection-pipeline permutation tests had BH q=0.000999, but these results establish finite-panel label readability, not pure semantics, uniqueness or functional use. A zero-error bootstrap interval of [1,1] does not imply perfect population accuracy.

Shared/math-biased/bio-biased median DCLM reference rates were 32.7278%/0.1701%/0.0397% for SAE and 58.1451%/0.3777%/0.1640% for CrossCoder. These are finite-reference rates. Shared-candidate selection already favors widespread use, so this ordering does not identify a formation mechanism.

**Fixed-target group confirmation remains insufficient.** SAE shared/biased q values were 0.375/0.375; CrossCoder values were 0.21875/0.125. The CrossCoder biased group had E=0.0324655 and a positive bootstrap interval [0.0082731,0.0605451], but its exact six-family sign-flip p was 0.0625. The preregistered combined criterion was not met. In a real illustration, CC f12314 at the identical `method` token changed shared z from 0 to 0.0348436, giving native final-layer contribution 0 to 19.3588. At the `example` target, the same feature was zero in all six versions.

Specific sources, subgenres, terminology, compensating neutral preambles, word sense and unequal edit sizes remain competing explanations. No natural cluster, frequency causality, physical range, functional importance or architecture-quality conclusion follows. Researcher mechanism judgment and question closure remain Unknown. See the [figures](../../../../../../../../UNAVAILABLE.md), [worked examples](../../../../../../../../UNAVAILABLE.md), [detailed record](../../../../../../../../UNAVAILABLE.md) and [appendix](../../../../../../../../UNAVAILABLE.md).
