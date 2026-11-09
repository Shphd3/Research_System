---
experiment_id: A15_00_03_E01_condition_local_residual_modes
status: completed_pass_conditional_modes_shared_envelope
created: 2026-07-31
approval_date: 2026-07-31
primary_anchor: 15_00_03_condition_local_residual_modes
canonical_protocol: protocol.md
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
resource_profile: local-2xh100
result: summary_cn.md
---

# Protocol 中文伴随版：按 domain/topic 检验 residual projector

## 0. Approval Snapshot

**执行结果（2026-07-31）：** 条件特异 residual 旋转通过，但这些旋转位于高度
共享的 envelope 中。domain \(\Delta O\) 区间稳定为正且远超随机分组，而跨 domain
capture 仍保留同 domain capture 的 95% 以上。见 [summary_cn.md](summary_cn.md)。

已批准的单文档补测进一步显示：跨文档 residual rank-64 overlap 约为 0.30，
而 Haar q95 为 0.094；同一文档不相交 token 半区的 rank-32 overlap 超过
0.51，因此精确局部模式变化不能主要归因于估计噪声。同 domain 只比跨 domain
略高，而跨 domain capture 仍约为同 domain 的 98%。

研究者已授权直接实现与完整运行。唯一问题是：真实 domain/topic 条件下是否出现
“同条件 projector 更一致、跨条件 projector 较不同，但仍可跨条件捕获能量”的
模式。该模式支持条件低维模式；它不证明训练收益。

## 1. Terminology / Definitions

| 指标 | 普通含义 | 计算 | 目的与能回答多少 | 不能证明 |
| --- | --- | --- | --- | --- |
| condition | domain 或其下 area/topic | 标签仅分组，不输入模型 | 给“数据条件”可复现定义 | 标签是模型语义 |
| within overlap | 同一条件两份独立数据学到的方向重合度 | \(\|U_c^{A\top}U_c^B\|_F^2/64\) | estimator 可靠性 + 同条件稳定性 | 功能价值 |
| cross overlap | 不同条件方向重合度 | \(\|U_c^{A\top}U_d^B\|_F^2/64\) | 具体 projector 是否随条件旋转 | 是否仍在共同 envelope |
| cross-capture | 条件 \(c\) 的 basis 捕获条件 \(d\) test residual 能量的比例 | \(\mathrm{tr}(U_c^\top\Sigma_d^{res}U_c)/\mathrm{tr}(\Sigma_d^{res})\) | 方向不同后仍否迁移 | 共同训练收益 |
| capture margin | cross-capture 减 target-specific Haar q95 | fraction | 是否超过随机同维 | 语义因果 |

## 2. Anchor Alignment

主指标是 \(\Delta O=\mathrm{median}(O_{within})-\mathrm{median}(O_{cross})\)；
cross-capture margin 是联合解释的必要指标。只看能量或 overlap 任一个都不足。

## 3. Tested Hypothesis

H1 预测 domain 主分析 \(\Delta O>0\) 且 cross-capture margin \(>0\)；topic 嵌套
复核同向。R0 预测 within≈cross 且都高；R1 预测 within/cross/capture 都低。

## 4. Rival Explanations

标签置换与同大小随机分组排除样本数和文本长度伪影；centered top-64 对照检查
旋转是否 residual 特异；complement-Haar q95 排除任意 residual 方向都可捕获。

## 5. Data / Model / Algorithm / Objective

- 数据：本地 Web of Science Arrow train/validate/test；只输入 `abstract`。
- 固定 128 tokens，文档必须至少 128 tokens；以内容 hash 确定抽样顺序。
- domain：7 类。train 中每类 64 pooled-common、64 fit-A、64 fit-B；validation
  每类 64 估计 target mean；test 每类 64 计算 capture。
- topic：每 domain 按 train/validation/test 最小可用量选前 4 个 area，共 28 个；
  每 topic 的 train A/B、validation mean、test capture 各 32 文档。
- 模型：LB/decommon 40k、80k；12 层；Gate 的直接输入。
- pooled top-64 只由独立、domain-balanced train pool 估计；condition residual
  basis 均先移除该 projector。

## 6. Conditions, Seeds, And Checkpoints

| 条件 | 为什么测 | 能回答多少 | 产物 |
| --- | --- | --- | --- |
| 7 domains | 主条件结构 | 粗领域模式 | domain pair table |
| 28 topics | 嵌套复核 | 细 topic 方向 | topic pair table |
| permuted labels ×256 | 标签特异性 | gap 是否超置换 | null table |
| matched random groups ×64 | 样本组合 rival | 非标签分组基线 | null table |
| complement-Haar ×256 | capture 随机方向 | 能量迁移是否非随机 | capture null |
| centered top-64 | 谱位置对照 | residual 是否更条件化 | band contrast |

随机种子为 20260731；层、checkpoint 和 source-target pair 都不是独立种子。

## 7. Primary Metric

\[
O(c,d)=\frac{\|U_c^{A\top}U_d^B\|_F^2}{64},\quad
\Delta O=\operatorname{median}_cO(c,c)-
\operatorname{median}_{c\ne d}O(c,d).
\]

以 200 次文档/basis bootstrap 重估 projector，再以 2000 次 domain-block
bootstrap 汇总 \(\Delta O\)。domain 模型级下界
\(>0\) 且高于置换 q95，回答“具体 residual projector 随条件变化”；它不能说明
这些变化仍可迁移，因此必须同时看 capture margin。

## 8. Secondary Metrics

cross-capture、within-capture、cross/within capture ratio、centered-top overlap、
逐层热图、40k/80k 变化、LB/decommon 描述性差异，以及 topic-within-domain
与 topic-cross-domain 分解。

### 8.1 已批准的文档级机制补测

研究者于 2026-07-31 明确批准使用已有激活做更严格的文档级检查。对每篇
`domain_a` 与 `domain_b` 文档，先减去该文档自己的 token 均值，再移除由独立
样本估计的 pooled top-64，最后只用该文档的 128 个 token 拟合 rank-64
residual projector。以完全相同数量和配对规则比较同 domain 与跨 domain 文档：

\[
O_{s,t}=\frac{\|U_s^\top U_t\|_F^2}{64}.
\]

对同一文档对，同时报告 source basis 捕获 target residual 方差的绝对比例，以及
相对 target 自身最优 rank-64 capture 的保留率；per-document centered top-64
作为 common 对照。该补测区分“精确方向稳定”和“具体方向变化但仍位于共享
方差包络”。它只细化机制，不替换原先注册的 condition-level 主指标。

## 9. Known Good / Known Bad / Known Confusing Cases

- 同一矩阵 overlap 必须为 1；独立 Haar-64 的 q95 应接近既有约 0.09。
- within 高、cross 低但 capture 不过随机，只支持隔离条件方向，不支持 envelope。
- within≈cross 都高支持全局共享 residual，不是测量失败。
- topic 标签与领域词汇相关，不得写成模型内部语义因果。

## 10. Stage-Level Profiling Plan

S0 冻结标签/token manifest；S1 actual-input/no-op smoke；S2 四 endpoint 激活；
S3 domain overlap/capture；S4 topic 复核和 null；S5 bootstrap/verdict/figures。

## 11. Runtime And Resource Contract

本地 2×H100 并行：GPU0 跑 LB，GPU1 跑 decommon。原始激活和 cache 留在 worker
surface；主线只接收表、图、summary/detailed。任何 guard 失败均停止对应 endpoint。

## 12. Pass / Fail / Insufficient

- **Pass conditional-modes：** domain \(\Delta O\) bootstrap 下界 \(>0\)、超过标签
  置换 q95，cross-capture margin 下界 \(>0\)；topic 方向同向。
- **Fail global-shared：** within 与 cross 精确接近且都远高于随机。
- **Fail label-specificity：** 真实 gap 不超过置换/随机组。
- **Insufficient：** within overlap 接近 Haar、CI 过宽、对象 replay 或样本合同失败。

## 13. Output Contract

输出 domain/topic pair CSV、模型级表、null 表；主图为 within/cross overlap 与
cross-capture 双面板；summary/detailed；以及按 Focus 五段规则、以实验名命名的
中文认识更新，不创建新的 `focus.md`。

## 14. Claim Boundary And Next Decision

只回答条件分层表征几何，不回答专家兼容性或训练收益。独立 2B 匹配实验已经
得到“路由改变、NLL 无收益”；几何 Pass 不等于训练 Pass。
