派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/protocol_cn.md)；研究修改仍回到原件。

---

# R20协议：距离与回答位置组合

## 授权与冻结

当前用户明确授权完整重算、必要补充实验与交付，不中途等待确认。冻结时间2026-11-04T15:21:58.891249+08:00（UTC2026-11-04T07:21:58.891223+00:00）。问题由用户确认，以下阈值/计算细节为AI在授权内固定的操作口径，不冒充普适标准或研究者科学接受。机制判断Unknown。不训练，不干预，不研究竞争答错。

## 数据、模型与识别

复用R19主144条，24族各两事实×三距离；原12留出为主要单位但已暴露，12发现仅探索。两个原生SAE各30000/Top32：第28层Attention投影输出、实际MLP输入，ID不跨字典相认。原prefix320，p319，e302/254/190，d=p−e−1排除两端。当前模型/SAE/reference资产strict通过，原件哈希保护。

新前向228条件：反转填充72、同token长度办公填充72、固定e190的近/中距48、六模板覆盖族position IDs统一+64的36；固定e远距24条复用。前两者固定e/p/token数，固定e组p207/255/319；位置索引组不改可见文本/位置。三变量仍不能完全分离。四smoke并入正式结果不重跑，六旧校准另列；共234条评分前向和一次无操作校验。CPU2线程/FP32/SDPA/物理2×328，每阶段1800秒，不升级GPU/云资源；单条原子保存，可从已有条目续跑。

## 主要量与判定

全部12留出保留，事实先在族内平均，不按六成员或答题好坏筛选。主比较16→128。H1平均共同成员/32≥.90；H2完整30000维截断码中，相对事实差异比保持[.8,1.25]；H3相对差异至少降20%。令delta=z_A−z_B，s=||delta||/sqrt((||z_A||²+||z_B||²)/2)，x=log(s128/s16)。幅度与delta方向cos独立报告。两字典×三假设共六p做Holm；8192整族bootstrap；精确2^12符号互换，假设位置误差对称。等效p取两边界单侧p的最大值，H3检验−x−log1.25；模板六均值/64符号敏感性另列。H1区间下界≥.9/H2比值区间全在[.8,1.25]/H3比值上界<.8，同时校正p≤.05且N≥8才支持。H1上界<.9、H2全在范围外、H3下界>.8分别未支持；其他不足。增大也是合法观察，不改口径找退化。方向相似不代替幅度不变。

## 完整分析与频率机会

三个距离对分别保留成员ID/频率/原始与相对强度，共同/换入/换出、全码与共同成员范数/方向。平方坐标改变分解为共同改变+换入+换出，不是隐藏能量或输出因果贡献。旧六ID固定、缺失为实际零，旧严格子样本只复核，不替代全族。保存h离线再编码核对Top32，截断前ReLU仅作阈值敏感性；看排名25–32、激活/阈值≤1.25、换入之前的未截断响应，避免把掉出Top32当作真实消失。

频率复用独立D1参考300文档/38400位置，count≥20且doc≥5；Attention35/70、MLP33/62，零和不足单列。列组字典基数、左端可换出数、旧排名四档匹配的换出期待；换入在非左端成员里按参考频率无放回抽512次，固定实际换入数。另用发现主任务出现次数+32×参考概率作任务机会敏感性，不用留出拟合。期待零只报告未校准，不算无穷富集。这些为描述性机会模型，不增设主要检验。

## 案例、可靠性与交付

规则先固定：四个不重复留出族，依次取两字典平均共同成员最多、最少、剩余中平均相对事实差异log比最小、与总体中位趋势反号且幅度最大的族。若无反号，取字典分歧最大并说明没有反号；平手按ID。仅为展示，不用案例作统计确认。两事实三距离全文/评分/频率/全部成员保留。F23低频成员零和F28物品词/句号不同结果作为已知混淆校验。新增对照无论支持与否都保存；资源缺口只阻塞依赖部分。

阶段：构造/冻结→旧缓存重算→4新+6旧smoke→其余224新前向→预定统计/对照→三审计/案例/图/双语Summary与Detailed→实际资产登记/核验/本地阅读同步→停止。旧文件保护、原生编码/无操作/候选前缀校验、逐token分数与实际距离独立复算。主要结果、探索与新增前向分别标记。交付主图、全审计图、10秒/30秒讲法及唯一一个AI建议的后续问题；科学接受与后续执行待共同审阅。

## 原版和变更

英文[完整协议](protocol.md)拥有逐项设置，与本中文说明一致。冻结后不改科学正文；变更必须追加时间、前后值、原因、已见数据、影响、权限和证据资格，保留原版本。不因结果不显著而换定义或模板。

## Amendment A1: configuration metadata qualification / 配置元数据说明

Recorded 2026-11-04T15:52:39.313753+08:00 (UTC 2026-11-04T07:52:39.268527+00:00), after all control outputs were visible. The frozen config reused R19and retains three unused R19provenance fields: prefix_count292,new_prefixes96,panel_sha256ofR19. Actual execution used panel_rows372,new_forward_rows228,the literal panel and IDlists; none of those legacy fields controls scoring or statistics. Original config/protocol bytes remain preserved. effective_config.jsonnow scopes the inherited fields and records actual372conditions,192new texts,36same-textposition-index variants and current dataSHA. This is metadata qualification only: no text/token,split,forward,member,metric,threshold,test or result changed. Scientific eligibility is unchanged. The current user authorized the complete audit and correction; no additional experiment is implied.

已见全部结果后发现复制配置残留旧R19的292/96及旧panel哈希字段，它们没有参与R20抽样/评分/统计。实际使用的新字段是372/228和真实ID表。保留原冻结文件；effective_config.json把旧字段放入继承命名空间，给出当前哈希和192新文本+36同文位置索引条件。仅澄清元数据，不改任何科学输入/结果。
