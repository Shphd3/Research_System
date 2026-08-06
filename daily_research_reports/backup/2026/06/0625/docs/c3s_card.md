Phenomenon:
嵌套特征 A→AB→ABC→ABCD 中，common 特征先学且反复出现，tail 特征后学。

Mechanism guess:
common 梯度重复出现，形成高增益 common 子空间 C；tail 更新如果与 C 对齐，会获得更大一级损失下降，因此被吸入 C，造成 feature interference。

Key variables:
C, P_C, u_t, α_t, δ(t), tail accuracy, common accuracy。

Causal relation:
common frequency ↑ → common gradient repetition ↑ → singular concentration ↑ → tail update α_t ↑ → tail recovery ↓。

Observable metric:
δ(t), α_t, top-k feature mass, effective rank, common accuracy, tail accuracy。

Alternative explanation:
tail 数据不足；模型容量不足；C3S 有效只是 loss reweight，不是 projection；common 子空间不稳定。

Decision:
若 δ(t) 小、α_t 高、C3S 降低 α_t 且提升 tail，同时 common 保持，则 pursue。
若 α_t 不高或 δ(t) 大，则 revise / park。