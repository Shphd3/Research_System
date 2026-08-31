# Thinking Card：粗—细判别空间复用的跨层变化

- **父研究方向：**A15 表征空间几何与功能路由。
- **现象：**已有组会问题只知道粗类与父类条件细类方向的直接关系尚未测量，也不知道该关系是否随模型层深变化。
- **当前机制判断：**Unknown。候选包括 shared coarse space、fine residual space 和 layer-dependent geometry；本轮不预先选择其中一个。
- **最强竞争解释：**逐层差异可能只是 Fisher 空间估计不稳定、模板表达或有限样本造成，而不是稳定的深度结构。
- **最不确定点：**mathematics / physics 的细类空间在每一层复用多少八父类粗空间，以及六层轨迹能否在 C4/C5 间复现。
- **会改变判断的证据：**在冻结 Qwen3-30B-A3B、固定 Block 4/12/20/28/36/44、固定 C4/C5、固定两目标父类和统一估计器下，逐层 raw/corrected overlap、随机 null、复现参照和 principal angles 的完整轨迹。
- **当前阻塞未知：**粗—细判别几何是深度稳定、单调变化、阶段变化还是非单调变化。
- **为什么现在需要：**任何 shared coarse、fine residual 或 layer-dependent Router 假设都会把这一未测几何当作架构前提。
- **当前下一决策：**完成冻结的真实表征 audit 后，只选择一个最值得进行因果验证的架构问题，不直接训练 Router。
- **已知来源：**0826 组会记录、已通过的合成估计器校准、C4/C5 冻结文本面板。
