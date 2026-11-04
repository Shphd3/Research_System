# 按 Anchor 阅读项目材料

[English](README.md) · [同步规则](../../docs/anchor_sync_cn.md) · [来源配置](profiles.json)

这些只读副本让你和agent只访问Research_System，也能读到已选项目的正式研究材料。
科学内容回原项目修改，再刷新这里；来源版本与哈希由每包的manifest.json记录。

| 项目／问题 | 讲什么 | 阅读入口 |
|---|---|---|
| from-attention-to-search／A17_04 | 列表首末条件映射：顺序反转后旧准确率降到0%，混合监督两种规则可兼顾；含R02设计、事实与数据说明 | [完整阅读包](from-attention-to-search/17_04/README.md) · [简短导览](../../assets/a17_list_rule_mapping_cn.md) |
| from-attention-to-search／A15_24_01 | common 梯度裁剪改变 AdamW 更新；四模型配对未支持稳定低频收益，含数据身份与数值边界 | [完整阅读包](from-attention-to-search/15_24_01/README.md) |
| from-attention-to-search／A15_24 | 频率评分与特征组合：原学习结果、组会依据及待确认子问题；组合分析已有记录，更新相容性假设未测试 | [问题与候选阅读包](from-attention-to-search/15_24/README.md) |
| from-attention-to-search／A17_04 R05 | 165任务、89正式端点；原轮/R2事实、资格失败与缺证、独立AI解释及交付清单；科学接受Unknown | [R05阅读包](from-attention-to-search/17_04_R05/README.md) |

这里只同步指定记录与必要的小型元数据。原始数据、模型与缓存仍在资产登记的执行存储。

- [A15_25_02：学习经历与任务重要方向](from-attention-to-search/15_25_02/README.md)：本地阅读副本；已暴露 DEV 探索证据，字典整体重建资格未通过。

- [A15_24_02：频率相关方向保持与补空间局部更新](from-attention-to-search/15_24_02/README.md)：Anchor、冻结 Protocol 和24项测试事实；已暴露 DEV，科学判断待阅读与讨论。

- [A10_03：Router 数值误差与一次有限学习更新](from-attention-to-search/10_03/README.md)：AI 草案、源码审查与60行合成校准；真实回放 NOT RUN，仅本地同步。

- [A15_24_03：参数影响与特征频率](from-attention-to-search/15_24_03/README.md)：40项完成，匹配与跨模型证据不足；待研究者检查实现与结果。

- [A15_26：低频组合对已有计算的帮助与复用](from-attention-to-search/15_26/README.md)：独立父Anchor讨论稿；机制检验待确认，NOT RUN，仅本地阅读同步。

- [A17_04 R06: fixed-new-exposure functional protection](from-attention-to-search/17_04_R06/README.md) — bounded continuation; original owner preserved; local reading copy.

- [A15_25_03：同token共同候选与上下文计算的功能依赖](from-attention-to-search/15_25_03/README.md)：只读资产与设计；DRAFT_NOT_EXECUTABLE，干预NOT RUN；待明确继续指令。

- [A15_27：自然语言feature关系](from-attention-to-search/15_27/README.md)：R03同token共激活分析完成，子图组织与部分远处编辑响应有界成立；同频成簇、长短程分工及R02双线索整合未决。保留R01/R02；仅本地派生阅读副本。 离线decoder/谱补测已加入：固定组方向相似性未确立；语义可分性缺配对缓存，未运行。 R04两域实验停在最后层编码对象不匹配，未运行，0/512。

- [A15_28：句内feature延续与旧图关联](from-attention-to-search/15_28/README.md)：双语设计与当前资产核查；H1/H2 NOT RUN；仅本地阅读同步。

- [A15_27_01: fixed-target domain response and spectral location](from-attention-to-search/15_27_01/README.md) — bounded R07; real target vectors and heldout readout, scientific acceptance/closure Unknown.

- [A15_27_02：域内与混合主要子空间](from-attention-to-search/15_27_02/README.md)：R07续接的固定文本探索性结果，科学接受Unknown。

- [A15_27_03：CrossCoder领域均值差分解](from-attention-to-search/15_27_03/README.md)：R09重建、频率／家族与受控距离结果，含A–D图和全字典方向背景。探索性证据，科学接受Unknown；本地阅读副本。

- [A15_27_04：全字典领域成员整体分析](from-attention-to-search/15_27_04/README.md)：R10数学433/生物527，五项缓存统计；纯换目标词及独立谱缺失，新增前向0，科研接受Unknown。

- [A15_27_05 · 谱位置与语义粒度](from-attention-to-search/15_27_05/README.md)：1031 R12有界结果；旧H探索性、来源覆盖不足及科研接受Unknown保留。

- [A15_29：谱分层路由渐进监督与全层级监督](from-attention-to-search/15_29/README.md) — 固定 P/F 对照；记录实际资格与提交状态，科研结论待定。

- [15_27_05_01 — Dense checkpoint dynamics](from-attention-to-search/15_27_05_01/README.md):2026-11-01,independent Dense0.5B–33B evidence;local reading copy,scientific acceptance Unknown.


- Feature组合四路线：[A15_27_06 共同成员与额外细节响应](from-attention-to-search/15_27_06/README.md) · [A15_27_07 固定成员上的相对强弱](from-attention-to-search/15_27_07/README.md) · [A15_27_08 跨频率来源优势](from-attention-to-search/15_27_08/README.md) · [A15_27_09 罕见配置与内容对应](from-attention-to-search/15_27_09/README.md)；本地阅读副本，修订版留出已暴露，科学接受Unknown。

- [R16 delete-head64 / keep960](from-attention-to-search/15_27_05_R16_delete/README.md): bounded arrival-round reading copy under the existing scientific owner.

- [S08 dataset support overlap](from-attention-to-search/15_27_06_S08/README.md): bounded arrival-round reading copy under the existing scientific owner.

- [R16等维谱段与参考均值对照](from-attention-to-search/15_27_05_R16_equal64/README.md)：原15_27_05主anchor的本轮有界阅读副本，含当前结果与必要旧R16／删除对照；这是阅读导航，不是新科研问题。

- [A15_27_10：近远物品事实行为](from-attention-to-search/15_27_10/README.md)：本轮行为前置关卡，含完整原文、逐家族数据、操作门槛与不确定性；无SAE／训练／干预，科学接受Unknown，仅本地阅读副本。

- [15_27_11: remote target / nearby competitor composition](from-attention-to-search/15_27_11/README.md): R19 factual results and raw-case reading; scientific acceptance Unknown; no training/intervention.
