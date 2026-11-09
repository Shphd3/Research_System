# 结果摘要：A15_17_02_E01 精确 17B N8 原生表征可分性审计

主 Anchor：[A15_17_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md)  
冻结 Protocol：[protocol.md](protocol.md)，Amendment A2  
完整证据账本：[detailed.md](detailed.md)  
文档状态：`DRAFT_AWAITING_RESEARCHER_JUDGMENT`  
结果状态／资格：测量 `COMPLETE / ELIGIBLE`；机制判断 `AWAITING_RESEARCHER`

## 一、目的

检验在同一精确 17B 训练坐标上，SAE 相关的第 8 层原生注意力写入集中是否伴随 N8
八个学术来源领域在未参与拟合的记录上更容易被读出。

## 二、假设

预注册主假设预测：全程重构系数 0.1 的 fresh S7，其原生正文均值 N8 测试准确率高于
Dense。最强竞争解释是 SAE 训练历史只改变集中度、尺度或共享方向，并未改善领域区别；
reweighted 1→0.1 与 fresh 0.1 的比较检验这一历史差异，但不把它写成只改变系数的因果
干预。

## 三、分析方法

- 在完全相同的冻结 N8 fit/dev/test 记录和第 8 层原生正文均值上，比较精确 17B
  Dense、fresh S7 0.1 和 reweighted S7 1→0.1。
- 只用 fit 拟合 L2 多类线性读出，用 dev 选择 `C`，在 1,600 条 test 记录上评估；
  对两个预注册差值做 2,000 次按类别分层的配对 bootstrap，并用 97.5% 区间判断方向。
- 报告有效维数、前 16 方向方差占比、类间／类内散度比和五种子 K-means ARI，作为
  结构解释；这些指标不能替代主准确率判据。

## 四、结论

预注册测量判定：

1. `fresh S7 − Dense = +1.4375` 个百分点，但预注册 97.5% 区间为
   `[−0.1250,+2.9375]`，跨过零。因此主方向为 `INSUFFICIENT`：不是已确认提升，也不是
   等效。
2. `reweighted S7 − fresh S7 = −14.9375` 个百分点，97.5% 区间为
   `[−17.5000,−12.5000]`，完全低于零。因此历史对比为
   `REWEIGHTED_LOWER_THAN_FRESH`。
3. reweighted 同时是最集中的条件（`d_eff=7.4958`，Q16 `0.7929`），但 B/W
   (`0.1324`) 和五种子 ARI 均值 (`0.1220`) 最低。这是合格证据，说明在本比较中
   集中度不是 N8 领域可分性的单调代理。

| 预注册规则 | 观察值 | 资格 | 类型化判定 | 证据 |
|---|---|---|---|---|
| fresh−Dense 的 97.5% 区间完全高于零 | `+1.4375` pp；`[−0.1250,+2.9375]` | 合格；同一 1,600 条 test | `INSUFFICIENT` | [配对区间](tables/paired_contrasts.csv) |
| reweighted−fresh 的 97.5% 区间排除零 | `−14.9375` pp；`[−17.5000,−12.5000]` | 合格；同一 1,600 条 test | `REWEIGHTED_LOWER_THAN_FRESH` | [配对区间](tables/paired_contrasts.csv) |

![精确 17B N8 主准确率与预注册区间](figures/n8_17b_separability_primary.png)

读图：左图是三种模型的测试准确率；右图是两个预注册配对差值。fresh 区间跨零，方向
未解决；reweighted 区间完全为负。

### 声称边界

能说：在这些精确检查点和 N8 面板上，fresh S7 没有按预注册规则被确认为高于 Dense；
更集中的 reweighted S7 明显比 fresh 更难读出，且距离式领域组织更弱。  
不能说：系数变化造成了差值、SAE 普遍改善或损害全部语义、语言模型实际使用这些信息、
语言模型质量或训练效率改变，或结果能跨训练种子和任务推广。

### 定稿前需要研究者确认

```text
问题：SAE 相关集中是否增强精确 17B N8 领域可分性？
直接结果：fresh−Dense 方向未解决；reweighted 在更集中的同时显著低于 fresh。
确认了什么：AWAITING_RESEARCHER
削弱或拒绝了什么：AWAITING_RESEARCHER
当前机制及理由：AI 草稿——集中度不是可读性的单调代理；reweighted 历史可能突出非领域或共享方向。
不能声称：系数因果、广义语义、模型实际利用、LM 质量、训练效率或跨种子推广。
唯一下一决策：AWAITING_RESEARCHER；AI 建议区分可逆尺度／条件数变化与领域判别方向丢失。
```

研究者确认或修正上述判断字段前，本摘要保持草稿状态。
