派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/literature_context.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/literature_context.md)；研究修改仍回到原件。

---

# Literature context for the interpretation

[中文](literature_context_cn.md)

Lake and Baroni (2018) separate successful near-distribution generalization from systematic combination of learned primitives in the SCAN recurrent-model setting. This motivates checking the context in which an operation is callable, alongside its training fit. It does not establish the cause of any Qwen failure here, and no numerical result is transferred between tasks. [Primary paper](https://proceedings.mlr.press/v80/lake18a.html).

Geiger et al. (2021) test alignments between neural states and explicit causal-model variables using interchange interventions. The useful methodological constraint here is to predict the recipient-specific counterfactual answer and test controls, instead of interpreting any performance drop as intermediate computation. No verified alignment is assumed by the order task specification. [Primary paper](https://arxiv.org/abs/2106.02997).

These sources were checked during this run. They contextualize the bounded interpretation; this round's measurements, eligibility and frozen comparison rules remain owned by its Protocol, Summary and Detailed records.
