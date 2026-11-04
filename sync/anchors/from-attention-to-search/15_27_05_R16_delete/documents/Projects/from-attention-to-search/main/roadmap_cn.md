派生阅读副本；原件位置：`Projects/from-attention-to-search/main/roadmap_cn.md`。
[精确原始文件](../../../../sources/Projects/from-attention-to-search/main/roadmap_cn.md)；研究修改仍回到原件。

---

# 项目研究路线图

[English](roadmap.md) · [项目入口](../../../../UNAVAILABLE.md) · [全部 Focus](../../../../UNAVAILABLE.md) · [全部 Anchor](../../../../UNAVAILABLE.md) · [研究地图](../../../../UNAVAILABLE.md)

这是一份按问题定位的导航，不另存研究状态或执行队列。Focus 持有研究者判断，Anchor 持有科学设计，Protocol 持有精确执行契约，Summary / Detailed 持有结果与证据。本次整理不激活、暂停、合并或关闭任何既有 Focus。

研究问题的完整层次与子问题作用见 [研究地图](../../../../UNAVAILABLE.md)（[英文入口](../../../../UNAVAILABLE.md)）。[地图数据](../../../../sources/Projects/from-attention-to-search/main/research_map.json)是派生导航，原 Anchor、Focus 与结果记录保留各自权威；离线交互版的生成方法见 [项目入口](../../../../UNAVAILABLE.md)。

## 11月4日当前地图入口

[谱、组合、局部干预与训练效用](../../../../UNAVAILABLE.md)：166个正式问题，85父问题、81子问题。先看七组新增证据，再查完整树。

## 10月31日地图更新

[新增内容与归类核对](../../../../UNAVAILABLE.md)：159个正式问题，84个父问题、75个子问题。七组阅读入口覆盖新增轮次，原问题的优先级与科学判断保持原记录。

## 历史阅读入口（10月22日）：A15_18

本轮小模型关系组织／使用分析归入 **A15_18**。先读 [逐项事实报告](../../../../UNAVAILABLE.md)，再按需打开 [Focus](../../../../UNAVAILABLE.md)、[Anchor](../../../../UNAVAILABLE.md) 和 [Protocol](../../../../UNAVAILABLE.md)。结果审阅与机制判断遵循这些 owner 的既有边界；此入口没有赋予其他问题新的状态或运行授权。

## 按研究线查找

编号用于稳定归属，不表示时间先后、重要性或新的依赖关系。研究线内的父问题、局部子问题及其记录见相应入口；完整清单为 [166 个 owner 的归属登记](../../../../sources/Projects/from-attention-to-search/main/anchor_ownership.json)。

| 研究线 | 问题范围 | Anchor / 实验入口 | 当前正式 owner 数 |
|---|---|---|---:|
| A01 common 算子机制 | 可识别性、真值恢复、梯度共性与反馈共性。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 4 |
| A05 top-1 失败机制 | 早期锁定、抑制、公共偏移与公共 logit 的因果检查。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 7 |
| A06 部分反馈下的功能路由 | 定义 → 状态发现 → 划分保持 → 专家效用及发现 → 真实任务空间。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 6 |
| A07 共同特征干扰与价值 | common/rare 更新干扰；因果专家价值需单独检验。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 7 |
| A09 频率与谱判别 | 特征写入及高增益常见频带与稀有判别的关系。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 2 |
| A10 优化器与学习率机制 | 公共梯度、奇异值集中与 SGD 稳定性。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 3 |
| A11 信息性未来监督 | 直接状态信号、参数传递与跨位置标准头使用。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 7 |
| A12 结构化组合任务 | 单步／两步能力、任务载体有效性、容量与中间状态使用。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 6 |
| A13 MTP 任务属性分解 | 中继必要性、监督位置／内容与普通预测头收益。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 7 |
| A14 条件秩及状态／参数桥接 | 条件功能秩、局部雅可比与有限割线／路径积分映射。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 6 |
| A15 表征几何与功能路由 | 几何、读出、原生使用、实际分发与专家学习分别立证。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 87 |
| A16 负载控制与梯度干扰 | 负载目标的相互作用与同层增量的功能路由。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 5 |
| A17 共享与干扰学习 | 条件规则、呈现次数、局部更新、自然文本几何与保持。 | [Anchor 索引](../../../../UNAVAILABLE.md) · [实验记录](../../../../UNAVAILABLE.md) | 19 |

[A00 基础定义](../../../../UNAVAILABLE.md) 是历史重定向，定义由 A06_00 持有，没有另立当前 Anchor。编号间的空号不创建缺失任务。

## 选择读物

- 已给出具体结果：直接读该实验的 Summary，再按证据需要读 Detailed。
- 已给出问题：在 [Focus 索引](../../../../UNAVAILABLE.md) 找原问题，进入其 Anchor 与协议；没有 Focus 的已登记 owner 仍保留原身份，不因此被激活。
- 只想定位设计或旧编号：读 [Anchor 全索引](../../../../UNAVAILABLE.md)、[归属登记](../../../../sources/Projects/from-attention-to-search/main/anchor_ownership.json) 和 [本次迁移记录](../../../../UNAVAILABLE.md)。
- 查数据、辅助材料或叙述：分别读 [数据登记](../../../../UNAVAILABLE.md)、[支持笔记](../../../../UNAVAILABLE.md) 与 [Stories](../../../../UNAVAILABLE.md)；它们不替代正式 owner。

[系统 PROJECTS.md](../../../../UNAVAILABLE.md) 只选择项目；本路线图负责项目内导航。科研结论和下一决定留在所属 Focus / Anchor，不能从列表顺序或目录存在推断。

## A15_26：低频组合复用

[独立父Anchor](../../../../UNAVAILABLE.md)持有核心问题。[R01符号实验事实](../../../../UNAVAILABLE.md)已完整交付，组成跨问法与组合资格失败；[并行订单V2](../../../../UNAVAILABLE.md)另持有自己的实验。两轮结果不混合，机制接受与问题关闭Unknown。


## A15_25_03：同token的C→R功能依赖

[Focus](../../../../UNAVAILABLE.md) · [Anchor](../../../../UNAVAILABLE.md)。研究者本轮明确的新子问题，R01已执行数据资格关卡并因支持样本不足停止；模型前向与干预NOT RUN；不改变A17或旧频率分析结论。


## A15_27：自然语言响应及后继领域子问题

[Focus](../../../../UNAVAILABLE.md) · [父Anchor](../../../../UNAVAILABLE.md) · [R06结果](../../../../UNAVAILABLE.md)。父正文当前聚焦固定词含义响应。R01—R05保留在原轮次；R04已完成456/512次前向，旧预检的NOT RUN不是当前执行状态。

R07、R08、R09、R10/R11分别由四个子Anchor持有；[完整范围与当前证据](../../../../UNAVAILABLE.md)逐项说明。最新[R11 A02](../../../../UNAVAILABLE.md)完成450篇新文档、462次前向，整体三域复核未建立。运行完成与科学接受分开。

## A15_28：句内feature延续与旧图关联

[Focus](../../../../UNAVAILABLE.md) · [Anchor](../../../../UNAVAILABLE.md) · [先读这一页](../../../../UNAVAILABLE.md)。独立问题。两字典H1与CrossCoder H2已有结果；SAE H2接口受阻。匹配范围内同坐标延续有界成立，旧图关联未通过完整背景控制。A15_27仍持有自己的问题。

## A15_27_02：域内与混合主要子空间

[Focus](../../../../UNAVAILABLE.md) · [Anchor](../../../../UNAVAILABLE.md) · [R08结果](../../../../UNAVAILABLE.md)。用户激活的R07探索性续接，固定384文本与三真实接口；域内/混合子空间、中心差、方差分解及UMAP辅助。全部适用统计完成，秩不足保留NA；科学接受Unknown，已停止自动扩展。


## A15_27_03：领域均值差的 CrossCoder 分解

[Anchor](../../../../UNAVAILABLE.md) · [R09 结果](../../../../UNAVAILABLE.md) · [A–D 补充](../../../../UNAVAILABLE.md)。约定的主分解、频率与家族分析、3,842 次距离前向和纯缓存补充全部完成。全字典原留出残差比为 0.5368／0.7214；36 名候选复现激活使用偏向。重建、频率、decoder 朝向与构造距离响应分别解释。原留出已经暴露，科学接受与闭合为 Unknown；完成后停止自动扩展。


## 10月31日完整新增问题导航

[七组新增工作及14个新owner](../../../../UNAVAILABLE.md)覆盖A15_24—28的后继轮次，包括A15_27_04的R10/R11 A02和已执行的A15_28。旧段落中的未运行状态按其日期保留；当前事实请从该入口进入原结果。


## A15_27_04: domain members and three-domain replication

[Atlas and latest replication](../../../../UNAVAILABLE.md) · [R11 A02](../../../../UNAVAILABLE.md). 完整字典筛选、频率与谱分析、第三域及新来源复核各有明确边界；不是领域专属或MoE收益的证明。


## A15_27_06–09: Feature组合与自然语言对应

[R17 四路线结果](../../../../UNAVAILABLE.md)。384条材料与600自然文档；冻结模型和字典，科学接受Unknown。

[A15_27_06 共同成员与额外细节响应](../../../../UNAVAILABLE.md) · [A15_27_07 固定成员上的相对强弱](../../../../UNAVAILABLE.md) · [A15_27_08 跨频率来源优势](../../../../UNAVAILABLE.md) · [A15_27_09 罕见配置与内容对应](../../../../UNAVAILABLE.md)


## R17_D1：双SAE四假设修正重测（2026-11-03）

[完整结果](../../../../UNAVAILABLE.md)。两SAE各H1–H4、独立CC、288新主面板及48附表、600自然文档、原生与位置诊断已完成；原结果保留。无答案细化仍受选择／读出／字典与H4覆盖限制。科学接受Unknown，无后续自动执行。
