# 摘要：A15_17_01_E03 系数切换前后激活复用审计

主 Anchor：`15_17_01_sae_shared_direction_reuse_anchor.md`  
冻结 Protocol：[protocol.md](protocol.md)  
完整证据：[detailed.md](detailed.md)  
结果状态：`PASS`；对于预注册的 checkpoint 对比，结果 `ELIGIBLE`。机制判断：`AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`。

## 1. Purpose

检查重构系数切换之后观察到的原生有效维数下降，是否同时伴随着同一固定
192 个样本上的 Top-32 SAE 原子复用增加。

## 2. Hypothesis

如果“共享原子复用”是低维化的必要伴随现象，那么 17B、
`lambda_rec=0.1` 的后期 checkpoint 应该比 15B、`lambda_rec=1.0` 的前期
checkpoint 具有更高的跨样本原子使用分布余弦相似度，同时原生有效维数更低。
竞争解释是：低维来自 decoder 方向共线、系数协方差或一般训练历史漂移，
不需要同 ID 原子复用增加。

## 3. Analysis Method

- 在相同的 192 个 N8 样本、每个样本 256 个有效 token、第 7 层原生
  Attention 输出位置和原生 Top-32 encoder 输出上，对比精确 15B
  `lambda_rec=1.0` 与精确 17B `lambda_rec=0.1` checkpoint。
- 对每个样本构造归一化原子使用频率向量，计算样本间平均余弦；以
  `post - pre` 为主指标，做 2,000 次配对样本 bootstrap，seed 为 `20260922`。
- 计算同面板原生 Attention 写入的中心化参与比有效维数，并核验加载、对齐、
  有限值、Top-32、重复前向、CPU/GPU、一致性、只读性和 artifact 完整性。

## 4. Conclusion

**预注册结论：`PRE_HIGHER_REUSE`。** 测量结果有效，但“后期低维且同 ID
复用增加”的必要条件没有出现。

1. **这一次没有观察到“低维 + 同 ID 复用增加”的组合。** 15B 的复用指标为
   `0.647618`，17B 为 `0.625302`；`post - pre = -0.022316`，配对样本
   bootstrap 95% 区间为 `[-0.035251, -0.008884]`，完全低于 0。与此同时，
   原生有效维数从 `15.674361` 降至 `8.418492`，下降 `7.255869`，即
   `46.29%`。因此注册规则选择 `PRE_HIGHER_REUSE`，而不是
   `POST_HIGHER_REUSE_AND_LOWER_DIMENSION`。

   **关键图：** [直觉与观测对比](figures/intuition_vs_observation.png)。

   **读图方式：** 右侧显示复用差值位于 0 以下，但有效维数仍然下降，说明两
   个变化方向相反。

   该图不能证明系数降低因果地导致了其中任何一个变化。

2. **工程和数值证据链完整。** 四个 RTX5090 worker 全部通过；每个模型有
   192 个样本、49,152 个有效 token，0 个排除。原生 Top-32 与 top-128 前缀
   的非 tie 不一致数为 0；重复前向的 pooled write 漂移为 0；CPU/GPU 数值、
   模型只读性、artifact 检查和独立 post-run 审计全部通过。

   **关键图：** [复用与原生几何曲线](figures/reuse_history_contrast.png)。

   **读图方式：** 左图区间完全在 0 左侧；中、右图只是集中性描述，不能当作
   额外的独立显著性检验。

### Claim Boundary

可以说：在这组固定样本和这两个 checkpoint 上，后期模型的原生有效维数更低，
但模型内同 ID 原子使用分布的相似度更低。这削弱了“低维化伴随共享原子复用
增加”这一具体解释。

不能说：`lambda_rec` 的孤立因果效应、语义质量、下游 utility、训练 seed 的
普适性、跨模型 feature ID 对齐，或激活复用是低维化的唯一机制。

### Next Step Analysis

**决策：`AI 建议`——不要再把“同 ID 原子复用增加”作为这条训练历史对比中
低维化的默认解释；下一步应在同一对 checkpoint 上检查 decoder 方向几何或
系数协方差。**

理由是：有效维数下降了 46.29%，但主复用指标显著下降，当前必要条件失败，
因此 decoder 几何和系数协方差竞争解释仍然存在。

未解决不确定性：两个端点还同时跨越了训练阶段、microbatch、梯度累积、
CE chunk、optimizer/RNG 历史；bootstrap 只覆盖 192 个样本的抽样不确定性，
不覆盖训练 seed 或因果不确定性。

完成标准：在同一面板上分解 decoder 几何、系数协方差和 residual 对原生有效维数
下降的贡献，并确认它们是否独立于同 ID 复用。如果要声称系数的因果效应，则应
另行设计只改变系数、保持训练条件匹配的 fork。

停止或转向条件：不能根据本结果升级为系数的因果解释；若核心问题仍是
`lambda_rec` 的因果作用，应转向严格匹配的消融。

恢复动作：先阅读 [detailed.md](detailed.md) 的完整证据链，并由研究者确认机制
判断，再更新 Anchor 和 Focus。
