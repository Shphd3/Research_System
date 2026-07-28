# Protocol：A12_02 一步标准下一词元干扰

## 0. Approval Snapshot

**批准状态：** 用户在 2026-07-12 明确要求执行第一个实验，因此本最小协议获准运行。
**目的：** 判断一阶梯度干扰能否定量解释 Next-2 的局部标准损失代价。
**主 Anchor：** `../../../problem_anchors/12_structured_compositional_mtp_workload/12_02_one_step_ntp_interference_anchor_cn.md`。
**唯一问题：** $-\eta\lambda\langle g_N,g_A\rangle$ 是否预测配对的一步标准损失差？
**实验角色：** 根因审计。
**主指标：** 两个最小有效步长下，$\Delta_{obs}$ 对 $\Delta_{pred}$ 的过原点回归斜率。
**最小设置：** $M=8$ 精确置换组合数据、单层因果 Transformer、NTP burn-in、配对克隆更新。
**配置：** 5 个 seed；每 seed 32 个固定 audit batch；相对参数步长 $10^{-5},3\times10^{-5},10^{-4}$；float64 审计。
**通过：** 小步长斜率在 $[0.8,1.2]$、Pearson 相关不低于 $0.95$、符号一致率不低于 $0.90$、中位归一化残差不高于 $0.20$，且所有守卫通过。
**失败：** 有效小步长下相关低于 $0.5$ 或符号一致率低于 $0.70$，且守卫有效。
**证据不足：** 其余中间结果、少于 80% 行数值可分辨，或配对/数据/恢复守卫失败。
**不能声称：** 完整训练因果、容量尺度、课程收益、自然语言迁移或普遍 MTP 优势。
**批准决策：** 只运行本根因审计；后续 anchors 由结果门控。

## 1. 术语解释

| 术语 | 中文含义 | 具体计算 | 单位/公式 | 为什么重要 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| $L_N$ | 两条件共享的标准自回归目标 | 格式 CE 加下一状态答案 CE | nat | 公平 NTP 比较 | 最终任务质量 |
| $L_A$ | Next-2 独有未来目标 | 从决策状态直接预测答案 | nat | 新增监督 | 下游使用 |
| 相对步长 | 更新范数相对参数范数 | $\|\delta\theta\|/\|\theta\|$ | 无量纲 | 控制局部区间 | 优化器动力学 |
| $\Delta_{pred}$ | 一阶预测差 | $-\eta\lambda\langle g_N,g_A\rangle$ | nat | 机制预测 | 曲率 |
| $\Delta_{obs}$ | 实测配对差 | $L_N(\theta_M')-L_N(\theta_N')$ | nat | 局部因果观察 | 长期收敛 |

## 2. Anchor Alignment

物理先验、核心模型项、证伪条件与 claim boundary 均与 A12_02 anchor 完全一致。

## 3. Tested Hypothesis

两个最小且数值可分辨的更新尺度上，跨批次与 seed 满足：

$$
\Delta_{obs}=\Delta_{pred}+O(\eta^2).
$$

## 4. Rival Explanations

曲率主导、标准监督不一致、批次或参数未配对、随机辅助头、浮点精度不足。

## 5. Data / Model / Algorithm / Objective

- 数据：`D_model8`，六张等长置换表，输入 155 个原子词元，目标为 `<FMT_u> <E_y>`；
- 训练 8192 条，审计 1024 条；
- 模型：单层因果 Transformer，隐藏维 64，4 个头，MLP 宽度 256；
- $L_N=L_{format}(h_T)+L_{answer}(h_{T+1})$；
- 预期的 $L_A=L_{answer}^{direct}(h_T)$ 使用标准答案反嵌入行在决策状态直接读出；
- NTP-only AdamW burn-in；正式审计使用 float64 配对 SGD 扰动，不使用优化器状态。

## 6. Conditions, Seeds, And Checkpoints

只比较同一 checkpoint、同一 batch 下的 NTP-only 与联合 Next-2 一步更新。Seeds 为 `971--975`；每 seed 首个验证答案准确率达到 `0.70` 的 checkpoint 进入审计，否则 step 600 并判定校准守卫失败。

## 7. Primary Metric

$$
\widehat\beta=\frac{\sum_i\Delta_{pred,i}\Delta_{obs,i}}{\sum_i\Delta_{pred,i}^2}.
$$

主指标同时受相关、符号、残差与数据守卫保护；只看梯度余弦不能通过。

## 8. Secondary Metrics

Pearson 相关、符号一致率、归一化绝对残差、梯度余弦、曲率缩放、验证准确率和格式翻转梯度选择性。

## 9. Known Good / Known Bad / Known Confusing Cases

- 已知正例：用 $g_N$ 替代 $g_A$；
- 已知反例：跨 batch 打乱辅助梯度；
- 易混淆：$\Delta_{pred}$ 近零的行，仅按预注册 float64 分辨率排除并报告比例。

## 10. Stage-Level Profiling Plan

依次审计数据、burn-in、梯度配对与有限差分；任何硬守卫失败均不得更新 claim。

## 11. Algorithm Specification

计算 $g_N,g_A$；按 $g_N$ 范数换算实际 $\eta$；克隆两份参数执行 NTP 与联合更新；在同一 batch 重算 $L_N$；恢复并记录预测、实测和哈希。

## 12. Success / Failure / Insufficient Evidence

严格应用第 0 节阈值，不在结果出现后修改。

## 13. What This Cannot Claim

不能判断低秩竞争、尺度依赖、课程学习、跨位置保持、自然语言迁移或最终 MTP 性能。

## 14. Review Notes And Protocol Changes

执行前已将标准目标修正为同时包含格式和下一位置答案损失，避免早期草案中 NTP 没有答案监督的不公平比较。实际 runner 直接复用了 tied standard unembedding，而没有实例化一个单独复制并冻结的辅助头；因此结果边界进一步收窄为“共享读出下的辅助目标”。该合规偏差不改变“证据不足”判定，结果出现后未修改阈值。
