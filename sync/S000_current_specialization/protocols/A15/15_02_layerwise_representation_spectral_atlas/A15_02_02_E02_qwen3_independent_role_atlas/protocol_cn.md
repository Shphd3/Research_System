---
experiment_id: A15_02_02_E02_qwen3_independent_role_atlas
anchor_id: 15_02_02_natural_hierarchy_role_localization
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-02
---

# Protocol：Qwen3-8B 独立 covariance 语义角色图谱

## 0. Approval Snapshot

审批状态：Protocol、实现、smoke 与 full 均已批准。目的：在冻结 Qwen3-8B 中判断同一概念作为父级或子级时是否落在不同 covariance rank。主 Anchor：[A15_02_02](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_02_natural_hierarchy_role_localization_anchor_cn.md)。物理先验：raw head 能量可能由背景方差机械造成；方向选择性必须在逐方向除去背景方差后仍存在。实验类型：冻结表征与指标审计。主指标：按 32 条链配对的父减子 raw/white 频带均值。最小设置：embedding 与全部 36 个 block 输出、128 篇独立 DCLM 文档/65,536 token、原 32 条层级链、四个同位置模板对。全部护栏下存在稳定层-频带效应为 Pass；有效零结果为 Fail；配对、basis、重构或 tail 稳定性失败为 Insufficient。不能证明 Router 效用、组合计算或训练收益。用户于 2026-08-02 明确批准连续执行。

## 1. Terminology / Definitions

| 术语 | 人话含义 | 计算 | 单位 | 判断作用 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| raw 能量 | 语义实际落在某方向的激活量 | $(u_i^\top(h-\mu))^2$ | activation² | 保留真实背景尺度 | 额外语义选择性 |
| white 能量 | 相对该方向平时波动的异常激活 | $a_i^2/\max(\lambda_i,\epsilon)$ | 无量纲 | 去除奇异值优势 | 功能价值或因果 |
| 同概念角色对 | 同一个词分别作为子级、父级 | token ids、绝对位置、长度完全匹配 | 每链每模板一对 | 排除词汇和位置 | 自然话语普遍性 |
| F1--F12 | 等相对秩细频带 | 每带 1/12 方向 | 每方向均值 | 观察谱位置 | 简并区单向量身份 |
| H/M/T | 粗频带 | F1 / F2--F5 / F6--F12 | 每方向均值 | 比较 head 与 non-head | 跨层同语义 |

## 2. Anchor Alignment

决策问题：独立 covariance 与白化后，Qwen3-8B 是否仍存在稳定的语义角色—谱位置关联？决定性反证是只有 raw 差异、白化差异不稳定，或效应依赖模板、链、basis 或 tail floor。结论只属于表征关联。

## 3. Tested Hypothesis

H1：父/子角色在至少一个层 × 频带具有稳定白化差异。描述性子问题是父级是否相对子级更偏 head，以及是否只有最后一层反转。

## 4. Rival Explanations

R0：raw 差异全由 covariance 尺度造成。R1：措辞或目标位置造成。R2：basis 不稳定或极小 tail 特征值造成。R3：孤立层或少数离群链造成深度假象。

## 5. Data / Model / Algorithm / Objective

冻结 `/data/share/Qwen3-8B`，bfloat16、单 H100 推理，不微调。读取 embedding 输出和每个 decoder block 输出的 residual state（层 0--36）。Calibration 为固定 DCLM held-out 中 128 篇不同文档，每篇确定性截取 512 个 Qwen token；禁止完整测试句泄漏。Evaluation 保留原 32 条链，用四种模板构造父/子最小对。每层用 calibration 均值中心化，频谱只离线分解一次。

## 6. Conditions, Seeds, And Checkpoints

必须同时完成 raw/white、四模板、half-split basis、$10^{-6}/10^{-5}/10^{-4}\lambda_1$ 三种 floor、2,000 次链 bootstrap、5,000 次链标签交换和层 0--36 全覆盖。统计单位是 32 条链。固定随机种子：文档 20260802、bootstrap 20260803、permutation 20260804。Half-split 主门定义为归一化 overlap excess $(O-r/d)/(1-r/d)\geq0.25$：H/M/T 至少 35/37 层通过，且第 35、36 层必须通过。

## 7. Primary Metric

每层每方向先算父减子 raw 与 white，再按 F1--F12 和 H/M/T 做每方向均值。报告均值差、配对 log ratio、95% 链 bootstrap 区间、链符号比例、标签交换 $p$ 和同一指标/分辨率族内的 BH-FDR $q$。

稳定效应必须同时满足：bootstrap 区间不含零；$q<0.05$；至少 3/4 模板与总体同号；至少 18/32 链同号；三种 epsilon 结论不变；并在两个相邻层同号复现，或通过单独注册的最后层反转门。

最后层反转要求第 36 层显著、方向与第 35 层及第 1--35 层中位趋势相反，且至少 3/4 模板和 18/32 链支持末层方向；否则不得称为反转。

## 8. Secondary Metrics

逐方向曲线、角色均值、12 带热图、H/M/T 深度轨迹、特征值谱、有效秩、split-half overlap、covariance 重构误差与 token 审计。

## 9. Known Good / Known Bad / Known Confusing Cases

Known good：关系完整出现后，同 token ids、同绝对位置的目标。Known bad：root-vs-leaf 词汇对比、目标后才出现关系。Known confusing：近简并频带内单特征向量可能旋转，因此逐方向曲线只作描述，频带推断是主证据。

## 10. Stage-Level Profiling Plan

S0 固化模型/数据/hash；S1 验证最小对与全层 hook；S2 验证 covariance 重构、能量守恒和 half-split；S3 验证 white 对 epsilon/effective rank 稳定；S4 运行 bootstrap/permutation/模板/链裁定并视觉审计三张图。

## 11. Algorithm Specification

输入：冻结模型、128 篇自然文档、32 条链、四模板对。参数：512 token/文档、12 带、三种 floor、2,000 bootstrap、5,000 permutation。步骤：生成并 hash manifest；在线累计全层 covariance moments；逐层特征分解；提取配对目标状态；计算 raw/white；按链统计；渲染并实际打开 Figures 1--3。Worker 保存大 basis/state；主线只保存完整文本 manifest、小 CSV、审计图和结果记录。

## 12. Success / Failure / Insufficient Evidence

Pass：至少一个层-频带父/子效应通过所有护栏。Fail：工程、数据、basis 均有效但没有稳定效应，或统一映射被层特异符号否定。Insufficient：任何强制门失败。Qwen 内部层特异 Pass 不能恢复 E01 已失败的跨模型普遍命题。

## 13. What This Cannot Claim

不能声称 covariance rank 产生语义、深层执行组合、某频带适合 Router、专家受益或其他模型共享该映射。

## 14. Review Notes And Protocol Changes

用户于 2026-08-02 提供并批准完整设计，授权无需再次等待直接完成。AI 在观察 E02 结果前补充了 FDR、相邻层、模板/链符号、epsilon 和末层反转的精确规则，用于落实用户给出的稳定性要求。

在查看 E02 数据前，half-split 稳定门冻结为 H/M/T 的归一化 overlap excess 至少 0.25，至少 35/37 个表征面通过且第 35、36 层强制通过；该归一化先减去同秩随机子空间的期望 $r/d$，避免对宽频带使用不可能的统一 raw-overlap 阈值。
