# Thinking Card — A07_04 Common / Rare Gradient Conflict Splitting Anchor

> Migrated from [07_04_common_rare_gradient_conflict_splitting_anchor.md](07_04_common_rare_gradient_conflict_splitting_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

父问题：expert partition 是否有功能价值，而不只是 load 更均匀。
当前子问题：高频 feature 与稀有 feature 在同一 expert 中梯度相冲时，routing 能否减少共享并降低 rare loss。
当前判断：neural proxy 中测到了梯度冲突，但 centered split 只弱改善，不能 claim MoE 功能价值。
关键证据：8 seeds；centered split 相比 random top-1 的 $\Delta\mathcal{C}=0.0271$，rare loss 改善 `0.0632`，但 dense rare loss 更低。
最危险边界：dense baseline 是反例边界；route conflict 降低不等于 rare learning 已解决。
下一步决策：先修正 proxy/router，再决定是否重跑 A07_04。

Question:
When a high-frequency feature $C$ and a rare feature $R$ have conflicting gradients inside shared experts, does top-1 MoE routing reduce their expert overlap enough to reduce rare-feature loss?

Physical prior:
If $C$ is much more frequent than $R$ and their per-expert gradients conflict, updates dominated by $C$ can raise $L_R$ unless routing separates them.

Core model:
For feature $f\in\{C,R\}$ and expert $e$, use routing probability $q_{f,e}=P(E=e\mid F=f)$ and per-expert gradient $g_{f,e}$.

Model term being tested:
Routing-weighted gradient conflict $\mathcal{C}_{C,R}$ as the mediator between expert sharing and rare loss.

Primary metric:
Conflict reduction $\Delta\mathcal{C}_{C,R}=\mathcal{C}_{C,R}^{\mathrm{baseline}}-\mathcal{C}_{C,R}^{\mathrm{candidate}}$, with rare-loss improvement as a required guard.

Falsifier:
No negative $C/R$ gradient conflict, no shared expert overlap, nonpositive $\Delta\mathcal{C}_{C,R}$, or positive conflict reduction without rare-loss improvement.

Can claim:
The neural proxy can measure common/rare gradient conflict, and centered routing weakly reduces it versus random top-1 in this run.

Cannot claim:
General semantic expert specialization, real-corpus transfer, or that load balance / route purity alone proves functional specialization.

Next decision:
Revise the proxy or router before using A07_04 as support evidence.
