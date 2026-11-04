派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/hypothesis_update.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/hypothesis_update.md)；研究修改仍回到原件。

---

# Recognition update and one next hypothesis

[中文](hypothesis_update_cn.md) · [AI interpretation](ai_interpretation.md) · [Facts](observations.md)

Status: AI_PROPOSAL. This develops an explanation without closing A15_26 or adding training to the current round.

## Two recognition updates

Specify the contexts in which an acquired capability is callable. Across three symbolic parents, the original256 atomic mappings and96 two-call compositions all score100%, while alternative wordings of the same mappings fail. Two-call100% is expected implementation calibration; the behavioral observation is instability of the same mappings across contexts. Training fit, local answers and availability for composition are distinct qualifications.

Global component deficits and local composition failures can coexist. Order discount acquisition misses the95% threshold, yet fixed matched cases can answer every independent component correctly and still miss the full order. Keep all four pairing cells and the original48-case denominator; model-success subsets cannot create a newly qualified population.

## One falsifiable next hypothesis: context coverage is an intervenable bottleneck

Candidate explanation: component training produces context-dependent behavior, and a changed invocation or sequencing context prevents reliable use in one forward pass. Prompt-specific lookup, independently learned whole-composition mappings and an unresolved sequencing interface remain rivals; arithmetic weakness also matters for orders.

AI suggestion: hold operation mappings, target labels, total exposure, model update range and optimization budget fixed. Compare repeated atomic supervision in the original context with equal exposure distributed across invocation contexts. Lock held-out atomic contexts and untaught compositions; give no new composition labels, true intermediates or extra inference calls. Assess atomic context qualification before the composition contrast.

If atomic context transfer improves but composition does not, an invocation-coverage explanation is weakened and binding/interface hypotheses gain priority. If both improve, the intervention has bounded utility, while internal reuse still needs causal evidence. If atomic qualification is not achieved, the composition mechanism remains unadjudicated.

The current round has consumed its permitted qualification revision and does not add this training comparison. Concurrent R01 has an independent rule-revision/interchange contract; its outcomes remain separate. The researcher's next decision and mechanism acceptance are Unknown.
