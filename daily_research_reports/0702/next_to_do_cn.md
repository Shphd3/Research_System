# 0702 Next To Do: Memory Recovery, Minimal Audit, And Learning Update

Date: 2026-07-02.

## 0. 结论

2026-07-02 的核心任务是：先恢复工作记忆，再把 nested learning 接到当前
gating 主线中的一个最小可跑实验，最后用实验结果更新认知。

明天不是直接提出新优化器，也不是做大规模远程训练。明天应当跑一个
bounded audit：先定义公共算子 $P_C$，再用已有 A06_22 / A06_23 证据面
检查 raw $h$ 与去公共后的 $(I-P_C)h$ 在路由间隔、sign flip 和 LM loss
保护指标上的差异。

当天结束时必须产出一个判断：

1. 哪个 $P_C$ 候选最像物理公共算子；
2. 去公共后的 routing 是否值得进入正式 protocol；
3. seminar 中 Adam/SGD、SCALE、谱打平、EMA-Nesterov 哪些只作为学习，
   哪些真正改变当前 gating 下一步。

不更新 graph、root sync、anchor、外部仓库，不 commit，不 push。除非当天
明确决定进入主线状态更新，否则只更新 0702 当日笔记或实验草稿。

## 1. 当前边界

当前主线是：在最高分唯一专家门控中，解释为什么隐藏状态聚类得到的
feature / proxy 到专家分配能初始化成功，但真实 DCLM 训练会在 step 5/10
被擦除。

已经支持：

- 受控均匀特征上，聚类初始化可以建立均匀路由。
- 保持依赖足够大的初始正间隔，而不是门控行向量主动追踪特征中心。
- A06_23 说明第 0 步正间隔不等于训练后一定保持；间隔太薄会跨边界。
- 真实 DCLM 中 proxy routing 能初始化，但 ordinary training 会快速擦除。
- A06_22 说明公共成分是候选机制，但公共投影器定义不稳健。

不能说：

- 公共成分已经是真实根因。
- 去公共成分已经是有效方法。
- 高 route NMI 或均匀负载证明专家有功能价值。
- EMA-Nesterov、SCALE 或任何 optimizer 已经解决当前 MoE routing 问题。

## 2. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 公共特征 | 高频出现、跨上下文复用、对多个预测任务都有贡献的表征方向 | 隐藏状态、梯度或 router update 中被多个条件共享的方向，可由投影器 $P_C$ 近似 | 候选解释：它可能造成路由或更新被高频方向主导 | 当前投影器不等于真实公共算子 |
| 稀有特征 | 低频、语境更具体、组合性更强的表征信息 | 明天先用 A06 real-DCLM proxy label 或 route-position 残差信号操作化 | 当前要保护的是它的路由间隔和更新有效性 | 不自动等于语义复杂度 |
| 路由间隔 | 已选专家相对竞争专家的分数优势 | $\gamma_{f,e}=(w_{a(f)}-w_e)^\top\mu_f$ | 决定特征中心是否仍在原专家一侧 | 不能证明专家有功能价值 |
| sign flip | 路由间隔从正变成非正 | $\gamma_{f,e}(t)\le 0$ 的 pair 比例 | 直接显示是否跨过 top-1 决策边界 | 不能单独说明跨界原因 |
| 高增益方向 | 小幅隐藏状态或参数变化能造成大输出/路由变化的方向 | 奇异值大、梯度投影大、或局部敏感度高的方向 | 可能解释为什么公共方向既有用又危险 | 不能单独证明来自频率 |
| 公共算子 $P_C$ | 把向量投影到公共方向的算子 | mean-common、top hidden-PC、router-row subspace、gradient/update common subspace 等 | 明天实验首先要裁定它是否稳定 | 不同 $P_C$ 不能默认等价 |
| 有效学习率 | 参数实际更新量相对梯度尺度的步长 | Adam 中约为 $\eta/(\sqrt{v}+\epsilon)$ 的坐标级步长 | 用来理解 SGD 为什么难以统一调大学习率 | 不说明更新方向是否正确 |
| EMA-Nesterov | 用过去多步更新的指数滑动平均做外推方向 | $m^{t+1}=\gamma m^t+(1-\gamma)(x^{t+1}-x^t)$ | 解释优化路径平滑，不直接解释 routing margin | 不直接控制公共/稀有方向 |

## 3. 明天总目标

### 必须完成

- 用 60-90 分钟恢复工作记忆，确保不靠聊天残留推进。
- 写出一个最小实验问题和通过/失败标准。
- 跑一个 bounded audit，优先复用已有 A06_22 snapshot / table，不做大训练。
- 实验后用主指标先读结果：rare/proxy residual margin、matched preserve、
  sign flip、proxy-route NMI、LM loss guard。
- 学习 Adam/SGD gap、SCALE、谱打平、EMA-Nesterov，但只抽取和当前
  common/high-gain routing 问题相关的对象。
- 晚上写 8-10 行认知更新：今天到底学到了什么，下一步是否能进入正式
  anchor / protocol。

### 明天不做

- 不启动 broad feature-existence sweep。
- 不直接写完整长期 protocol；只写最小审批面。
- 不把 optimizer final loss 当成主线证据。
- 不把 EMA-Nesterov 包装成 MoE 方法。
- 不更新 graph 或 root sync。
- 不做没有主指标和保护指标的远程实验。

## 4. 一天安排

### 09:00-10:15 恢复工作记忆

读：

- `PROJECTS.md`
- `sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md`
- `sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md`
- `sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md`
- `daily_research_reports/0701/meeting_brief.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md`

完成物：

- 5 行当前状态复述：
  - 主线；
  - 当前瓶颈；
  - 已支持；
  - 不能 claim；
  - 明天实验的最小决策。

自问：

1. 当前主线到底要保护什么量？
2. 是总 margin 决定判断，还是去公共后的 residual margin 决定判断？
3. A06_22 为什么不能直接支持 common subtraction？

### 10:15-11:15 最小实验审批面

写一个短审批面，不超过 1 页。工作名：

`A06_24_common_operator_residual_routing_smoke_audit`

实验角色：

- root-cause audit；
- 不是 method construction；
- 不是 utility claim。

最小问题：

> 能否定义一个更物理的公共算子 $P_C$，使得基于 $(I-P_C)h$ 的 routing
> 相比 raw $h$ 提高 proxy / rare 分组的 residual margin、降低 sign flip，
> 并且不恶化 LM loss、max load 和 active expert guards？

主指标：

- residual rare/proxy margin；
- sign flip rate；
- matched preserve fraction。

保护指标：

- proxy-route NMI；
- LM loss；
- max load；
- active experts；
- exact gate-input audit；
- projector robustness。

通过标准：

- 至少一个 $P_C$ 候选在 step 5/10 collapse window 中不翻转；
- $(I-P_C)h$ 的 residual margin 高于 raw $h$；
- sign flip 降低；
- LM loss 不出现不可接受回退；
- max load 不变成新的 collapse。

失败标准：

- 不同 $P_C$ 仍像 A06_22 一样给出相反结论；
- margin 改善只来自负载或尺度变化；
- LM loss 明显恶化；
- active experts 或 max load 显示新的路由退化。

11:15 前需要一个明确决定：

- 如果审批面清楚，下午跑 bounded audit。
- 如果审批面不清楚，只跑数据/脚本可用性检查，不解释结果为实验结论。

### 11:15-12:15 实验准备与 smoke check

目标不是正式读结果，而是确认下午能跑。

检查：

- A06_22 表格和 snapshot 是否存在；
- 现有脚本是否能读取 router rows、hidden centers、proxy labels；
- 是否已有 common projector 计算路径；
- 是否能输出 raw $h$ vs $(I-P_C)h$ 的 routing audit table。

完成物：

- 一张 readiness 表：
  - data exists: yes/no；
  - code path exists: yes/no；
  - missing object；
  - fallback plan。

fallback：

- 如果 snapshot 不够，就只用已有 A06_22 tables 做 projector stability
  re-analysis；
- 如果代码路径不够，就不补大工程，只写明缺哪个对象。

### 12:15-13:30 休息与轻整理

只整理上午审批面和 readiness 表。不要扩展实验范围。

午间检查：

- 如果没有明确主指标，下午不跑。
- 如果没有 LM loss / load guard，下午不跑方法比较，只跑可用性检查。

### 13:30-15:45 跑 bounded audit

优先级：

1. 本地或已有结果再分析；
2. 小规模 smoke；
3. 只有本地通过且用户明确同意，才考虑远程提交。

实验条件：

- raw routing on $h$；
- residual routing on $(I-P_C)h$；
- $P_C$ candidates:
  - mean-common guard；
  - top hidden-PC guard；
  - router-row subspace guard；
  - gradient / router-update common subspace as preferred physical candidate,
    if saved objects allow。

必须输出：

- step 0 / 5 / 10 的 residual margin；
- matched preserve fraction；
- sign flip rate；
- proxy-route NMI；
- max load；
- active experts；
- LM loss guard；
- projector robustness table。

时间上限：

- 15:45 必须停止扩展；
- 即使结果不完整，也进入 first read。

### 15:45-16:45 第一遍读结果

按顺序读：

1. 实验是否有效：数据、条件、guard 是否齐。
2. 主指标是否移动：residual margin 和 sign flip。
3. 是否有代价：LM loss、max load、active experts。
4. 是否稳定：不同 $P_C$ 是否仍翻转。

只允许三种判断：

- supported for next protocol；
- weakened / operator still unstable；
- insufficient evidence because setup invalid or guards missing。

禁止写：

- common subtraction works；
- semantic expert exists；
- utility improved。

### 16:45-17:45 学习 Adam/SGD gap 与 SCALE

读：

- `daily_research_reports/0701/docs/design_problem_understanding_revised.md`
- Adam/SGD gap paper 的摘要、核心实验和结论表；
- SCALE paper 的 optimizer component 和 output-head normalization 部分。

只抽取四个对象：

- 有效学习率；
- 输出层 token 类别梯度不均；
- 谱方向或坐标方向的尺度不均；
- 它们是否能解释 routing margin 消耗。

完成物：

| 学习材料 | 直接控制对象 | 能否接当前 $P_C$ / margin 问题 | 不能 claim |
|---|---|---|---|
| Adam/SGD gap |  |  |  |
| SCALE |  |  |  |

### 19:30-20:15 学习谱打平与 EMA-Nesterov

目标是更新认知，不进入方法设计。

必须会讲：

- 一维稳定条件：$0<\eta<2/\lambda$。
- 多维稳定上界：$\eta<2/\lambda_{\max}$。
- 谱打平可能扩大稳定学习率，但不保证 rare routing margin 改善。
- EMA-Nesterov 平滑的是外推路径，不直接定义 common/rare 子空间。

完成物：

- 4 句解释：谱打平控制什么、EMA-Nesterov 控制什么、它们和 gating 主线
  的关系、为什么不能直接作为 claim。

### 20:15-21:15 当日认知更新

写当天最终笔记段落，建议文件：

`daily_research_reports/0702/modeling_choices_to_confirm_cn.md`

如果当天决定只保留在对话中，也至少写 8-10 行总结：

- 今天跑了什么；
- 最重要主指标是什么；
- $P_C$ 是否稳定；
- raw $h$ vs $(I-P_C)h$ 是否改变 residual margin；
- sign flip 是否下降；
- LM loss / load guard 是否安全；
- Adam/SGD 和 SCALE 给了什么启发；
- EMA-Nesterov 是否仍只作为理论学习；
- 明天之后是否应写正式 anchor / protocol；
- 需要用户确认的 3 个建模选择。

## 5. 明天的判断规则

### 推进

只有当结果能改变以下至少一项时推进：

- 当前假设：公共/高增益方向是否压低稀有特征路由间隔；
- claim boundary：common 是否仍只是候选机制；
- next decision：公共算子和稀有特征如何操作化。

### 暂停

如果一个方法只改善 optimizer loss，但没有说明控制了哪个机制对象，则暂停进入主线。

如果 $P_C$ 仍然翻转，则暂停 common subtraction 方法 claim，回到 common
operator 定义。

### 只作为理论学习

EMA-Nesterov 默认只作为理论学习，除非能提出可测诊断：

- 外推轨迹低频化是否减少 route margin sign flip；
- 轨迹平滑是否改变 common-band update mass；
- 这种改变是否不伤害 LM loss。

没有这些诊断前，不把 EMA-Nesterov 写进当前 gating anchor。

## 6. 明天结束时的最低交付标准

必须回答：

1. 明天是否完成了工作记忆恢复？
2. 最小实验问题是什么？
3. 实验是否真的跑了，还是只完成 readiness check？
4. $P_C$ 候选中哪个最稳定？
5. raw $h$ vs $(I-P_C)h$ 的 residual margin 有没有改变？
6. sign flip 有没有下降？
7. LM loss、max load、active experts 是否安全？
8. Adam/SGD gap 的近因是什么？
9. SCALE 直接控制了什么对象？
10. 谱打平和 EMA-Nesterov 是否改变当前 gating next decision？
11. 写正式 protocol 前还缺哪 3 个建模确认？

如果第 2-7 个问题不能回答，明天不进入正式 anchor / protocol。

