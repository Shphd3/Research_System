# Thinking Card — A09_01 常见高增益带 / 稀有判别 Anchor

> Migrated from [09_01_common_band_rare_discrimination_anchor_cn.md](09_01_common_band_rare_discrimination_anchor_cn.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** common 特征容易形成高增益方向；rare 信息可能存在，但预测时仍被 common 方向压住。

**Mechanism guess:** 高增益带贡献很多分数，但不一定贡献正确判别；rare 剩余带分数更小，却可能更能区分正确目标和干扰项。

**Key variables:** 高增益带、剩余带、正确目标、common 干扰项、rare 损失、MoE 分开。

**Causal relation:** common 高增益带大但判别弱 -> 分数竞争放大 common 干扰项 -> rare 正确目标被压低；有效 MoE 分开应减少这个错配。

**Observable metric:** 错配差：高增益带的分数占比减去高增益带的判别占比。

**Rival Explanations:** rare 损失改善可能来自容量、随机分开、负载变化或正则化，而不是 common/rare 机制。

**Decision:** 只有当 MoE 分开同时降低错配差并改善 rare 损失，才继续作为机制；否则暂放方法，只保留诊断。
