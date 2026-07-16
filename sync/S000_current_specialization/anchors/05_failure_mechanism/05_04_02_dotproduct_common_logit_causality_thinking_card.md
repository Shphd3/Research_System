# Thinking Card — 05_04_02 Dot-Product Common-Logit Causality Anchor

> Migrated from [05_04_02_dotproduct_common_logit_causality_anchor.md](05_04_02_dotproduct_common_logit_causality_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

父问题：为什么普通 sparse top-1 MoE router 不能稳定形成 feature-to-expert specialization？

当前子问题：dot-product router 的 collapse 是否由 common-logit dominance 的时序和因果作用驱动？

核心结论：common logit 在 step 0 已经强于 slot margin，step 10 前继续放大，并且 common-logit cancellation 显著提高 slot-level specialization。

最小测试：审计 common logit 的 step-0/early timing、slot-init basin、common-logit cancellation 和 common-source ablation。

当前边界：只研究 no-position uniform slot toy setting；不声称真实 LM、multi-B 或 expert computation causality。

下一步决策：设计 label-free anti-common / anti-lockin router，并保留 B-source audit 作为边界条件。
