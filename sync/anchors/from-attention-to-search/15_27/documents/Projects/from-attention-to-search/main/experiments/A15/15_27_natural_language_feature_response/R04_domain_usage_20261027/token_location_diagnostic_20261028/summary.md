派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/summary.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/summary.md)；研究修改仍回到原件。

---

# Exploratory diagnosis: where does domain-related feature activity appear?

We compare the original32domain-biased candidates in heldout documents, earlier controlled-prefix positions and the original generic final target. No candidate reselection, fitting, model forward, attention or new task occurred.

The old four probes, matched random references, DCLM rates and target tests were rechecked against the unchanged R04 zip and saved data. Document labels remain readable (SAE shared/biased95%/100%;CC92.5%/97.5%), but CCbiased random sets average95.625% and can reach100%. No original fixed-target group passes the combined confirmation criterion (CCbiasedq=.125).

All32candidates occur in40heldout documents. Earlier controlled prefixes cover24SAE/26CCcandidates; final targets cover4/5. Among the28SAE/27CCtarget-silent candidates,21in each dictionary activate earlier in the domain-clue sentence. The remaining7SAE/6CCare absent from the entire controlled text. These observations retain both position selection and text/content/format mismatch explanations. They do not identify exclusive causes, pure semantics, information transfer or functional importance.

The fixed heatmap displays8oldcandidates per dictionary in old F08counterexample/F09CCexample/F11SAEexample;all32enter coverage tables. CCf12630 at protein/with has final-layer native contribution35.10/42.87,but0atmethod. Ordinary-token activity can still depend on earlier terminology. Old document examples for absent candidates include formula variables/digits,which the controlled prose lacks. Many earlier activations have only one supporting family.

Suggested next step,not run:independent paraphrases with fixed candidate IDs and predefined readings near a term and at a subsequent identical ordinary token. The entire new diagnosis is exploratory. [Chinese one-page explanation](summary_cn.md),[detailed evidence](../../../../../../../../../UNAVAILABLE.md),[heatmap](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/figures/token_feature_heatmap.png).
