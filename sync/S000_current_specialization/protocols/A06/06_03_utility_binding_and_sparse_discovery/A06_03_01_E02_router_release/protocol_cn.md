# 实验协议：A06_03_01_E02 Specialist/Generalist Router Release

## 0. 审核摘要

**状态：** 依据持续研究目标，于 2026-07-10 批准执行。

**目的：** 在 representation 与 router 初始状态完全相同的条件下，判断 expert specialization value 是否产生更有利于任务的多步 weighted-top-1 route dynamics。

**主 anchor：** `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/subanchors/06_03_01_trainable_expert_utility_binding_anchor.md`

**唯一问题：** 用 specialists 替换 generalists 后，释放 router 是否产生更大的 assigned-margin growth，同时保持更低 native task loss？

**主指标：** router-only SGD 在 step 50 的

$$
D_m(50)
=
\operatorname{median}_{f,seed}
\left[\Delta m_f^{spec}(50)-\Delta m_f^{gen}(50)\right].
$$

**通过 value-aligned transmission：** $D_m(50)$ 的 seed-clustered 95% CI 下界大于 0，specialist native task loss 更低，所有 guard 通过。

**支持 transmission misalignment：** specialist task-loss advantage 的 CI 下界大于 0，但 $D_m(50)$ 的 CI 上界不大于 0。

**证据不足：** A06_03_01_E01 exposure 未复现、non-expert state 不同、初始 route 不同、少于 32 seeds、loss 发散或 finite-step closure 失败。

**不能声称：** 自然语言 semantic routing、from-scratch discovery、真实 downstream gain，或新 gate 已经必要/最优。

## 1. 术语解释

| 术语 | 具体含义 | 计算 | 为什么重要 | 不能证明什么 |
| --- | --- | --- | --- | --- |
| specialist start | 只在指定 context task 上训练的 experts | A06_03_01_E01 correct expert-only checkpoint | positive utility 起点 | 自然语义 |
| generalist start | 从所有 tasks 获得等量更新的 experts | A06_03_01_E01 shuffled checkpoint | load-matched control | experts 无用 |
| router release | 取消 forced assignment，只训练 native weighted-top-1 router | optimizer steps | utility-to-route handoff | from-scratch discovery |
| margin growth | assigned expert 最小 score lead 的变化 | $m_f(t)-m_f(0)$ | route strength | task value |
| routing excess loss | native loss 超过 forced expert floor 的部分 | $E_f=L_f^{native}-L_{f,f}^{cf}$ | 隔离 routing inefficiency | 总任务难度 |
| normalized excess | 初始 routing excess 的剩余比例 | $R_f(t)=E_f(t)/E_f(0)$ | 训练效率 | 系统效率 |

## 2. 核心设置

- 完全复用 A06_03_01_E01 的四种 context-defined modular tasks、33-token sequence、全位置 LM loss、一层 causal Transformer、known-good instruction state 与四个 MLP experts。
- 先确定性重建 200-step specialist/generalist expert-only checkpoints。
- release 前必须复现：specialist median gap >5；generalist absolute median gap <0.5；route NMI=1；non-expert state max error $\le10^{-7}$。
- primary：冻结 experts 与 representation，只训练 router；SGD LR $10^{-4}$。
- optimizer transfer：router-only AdamW，LR 0.001。
- realism transfer：joint AdamW；router/expert LR 0.001，representation LR 0.0005。
- release 50 steps；checkpoints 0、1、2、5、10、20、50；32 seeds。

## 3. 假设与对照

| 假设 | 判定 |
| --- | --- |
| H1 specialists 保持 task value | final $L^{gen}-L^{spec}$ 的 95% CI 下界 >0 |
| H2 specialists 获得更强 route growth | $D_m(50)$ 的 95% CI 下界 >0 |
| H3 当前 gate 未按 value 校准 | H1 通过且 $D_m(50)$ CI 上界 $\le0$ |
| H4 optimizer transfer | SGD 与 router-only AdamW 的 $D_m$ 同号 |
| H5 joint transfer | joint AdamW 保留同一 qualitative route/task relation |

## 4. 训练效率

因为 specialist/generalist 的 expert-function floor 不同，不能直接把绝对 loss 收敛速度当作 routing efficiency。对每个 task 使用自己的 forced floor：

$$
R_f(t)
=
\frac{L_f^{native}(t)-L_{f,f}^{cf}(t)}
{L_f^{native}(0)-L_{f,f}^{cf}(0)}.
$$

报告 median $R_f(t)$、normalized-excess curve 面积以及首次 $R_f\le0.1$ 的 checkpoint。

## 5. 结果图约定

1. **margin-growth contrast：** 横轴 release step，纵轴 paired specialist-minus-generalist margin growth。
2. **native task loss 与 normalized routing excess：** 同时看 task value 和 router optimization efficiency。
3. **utility、pressure 与 actual movement：** 检查 A06_03_01_E01 一步 mismatch 是否延续到真实更新。

## 6. 边界与下一步

若 specialists 保持 task value 但没有更强 route growth，下一方法 anchor 才可瞄准 relative-utility transmission；若 ordinary weighted top-1 已产生 value-aligned co-stability，则继续进入更少 oracle、更加 grounded 的上下文任务。joint 结果不能覆盖 router-only 主因果结论。

所有 release 优化器均从空优化器状态开始，不继承 expert exposure 阶段的 AdamW 动量。
