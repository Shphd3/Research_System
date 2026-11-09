# S04 执行与证据口径

本轮24条捕获、24条双候选评分完成，模型与SAE全冻结，无训练/筛选/干预。运行耗时117.67秒，CPU2线程，FP32；离线统计和序列求和FP64。新旧结果独立目录，原S02/S03共212个文件哈希不变。[Summary](summary_cn.md)保留目的、假设、分析和有界结论；[协议](protocol_cn.md)及[frozen_plan](frozen_plan.json)在新响应前固定。

## 取样和原生编码

正文/标签/家族完全沿用S03；新后缀一致，末尾冒号ID25，同家族绝对位置一致；旧末尾space-a ID264，不能当同一token下的单词消融。捕获仅包括24条完整可见前缀，没有任何候选答案；随后移除全部hook，才做原生评分。ATTN和MLPIN分别使用原loader，编码与线性+bias→ReLU→Top32实现完全一致；保留preactivation和32/33门限，激活为最终z>0，Top32选入索引另存。原生无hook对照最大差0；候选重复lane最大差0.0。这些是实现检查，不是科学确认。

## 量与分母

z为最终稀疏激活，d为同字典decoder列L2范数，u=z*d。q_raw/q_weighted各在原命名列表内归一化。固定位置保留为0，不按新激活重选；整个列表范数0才不可定义。H1-added旧归一化是本轮从原数组新算的派生值，不冒充S03已报告量。所有列表范数、preactivation、Top32/正值和完整精度见candidate_values。方向零阈值1e-8与旧口径一致。

H2两种参照分别报告：同家族旧差；S03原探索方向。归一化方向直接沿用原selection，原始差探索参照在新响应前仅用旧探索均值固定。计数每候选每split分母3，优先zero_norm→member_inactive→no_reference→same/opposite/zero_difference。原子未激活的q数值仍保存但不算共同成员比例保持。每串和为3；新未双侧激活与零范数的非互斥原始标记也保留。数据独立单位是家族，无显著性或总体结论。

## 原始行为

精确候选和拼接完整ID在data/panel.jsonl，token级logP在results/behavior_raw.jsonl。分数为含句号的完整序列自然对数概率，最大和首选，无长度/先验校正。每候选2token，等长排除本轮长度数量差，但不排除词/标点先验。cat/dog各6条准确率，P/N只偏好，P并非猫狗负例。旧S02使用另一前缀，仅作历史并列。

## 核验与范围

48项候选求和、2304个候选值、72条H2旧新差、96条方向计数、192条支持转换独立复核；旧H2的q与S03原CSV精确重放。所有正文0改动、原候选0重筛、212旧文件保持；最终以verification中实际计数为准。

### ATTN_SAE

新hook重建相对L2误差||h-reconstruction||/||h||的最小/中位/最大=0.351515/0.384022/0.478110；不作跨接口排名。第32与33正值最小差0.000066757，精确边界并列0。

新24条各固定列表零范数数：`{'H1_common': 0, 'H1_added_cat': 9, 'H1_added_dog': 9, 'H2': 0}`。这些列表的不可定义情况都保留在表中，尤其H1新增列表，不能用H2无零范数替代全列表报告。

### MLPIN_SAE

新hook重建相对L2误差||h-reconstruction||/||h||的最小/中位/最大=0.158297/0.186945/0.231346；不作跨接口排名。第32与33正值最小差0.000965595，精确边界并列0。

新24条各固定列表零范数数：`{'H1_common': 0, 'H1_added_cat': 4, 'H1_added_dog': 6, 'H2': 0}`。这些列表的不可定义情况都保留在表中，尤其H1新增列表，不能用H2无零范数替代全列表报告。

## 文件与覆盖

- data：24条旧新前缀/原始标签/所有token与候选、S03原面板/selection、S02原行为分数；全部byte lineage保留。
- cache/new.npz：样本ID，各site__h/z/pre/topk_indices/decoder_norm/cutoff32/33/reconstruction_relative_L2；不含答案位置。
- results：24原生分数及48候选序列、逐家族行为；两SAE全部旧新候选值、72H2配对、96计数、H1四条件模式与192支持转换；全活跃成员原始值。
- 4幅图：每字典一幅固定列表原始/相对热图、一幅旧新H2差值图，来源均是冻结列表及cache，不展示新筛选结果。
- code/evidence：实际脚本、冻结、捕获、核验和输入/输出资产记录；模型/SAE checkpoint不复制。

| 需求 | 状态 | 边界 |
|---|---|---|
| 24正文保持、中性后缀与token | DONE_VALID | 全部完整记录 |
| 两冻结SAE、原候选及全部量 | DONE_VALID | 不跨字典对齐 |
| 原生猫狗评分和P/N偏好 | DONE_EXPLORATORY | 强制二候选 |
| H2旧新方向、指定两原子与失败 | DONE_EXPLORATORY | 成员未激活单列 |
| H1支持变化与正文竞争解释 | DONE_EXPLORATORY | 未测额外信息 |
| 训练/重筛/SVD/干预/新类别 | NOT_RUN_BY_SCOPE | 用户要求止步 |
| 科学接受/下一步 | Unknown | 等待共同审阅 |

无研究假设或Anchor科学状态修改，无commit/push。原协议科学规则未改。小样本、明确词面、整体任务框架与取样token变化、Top32竞争和重建近似仍限制解释。

## 协议与实际执行核对

| 固定项 | 实际 | 资格 |
|---|---|---|
| 24正文及标签保持 | 改动0 | ELIGIBLE |
| 唯一中性后缀 | 精确newline+Description:，24条一致 | ELIGIBLE |
| 原S03列表及方向 | selection字节哈希保持，新筛选0 | ELIGIBLE |
| 原模型/两原SAE | 相同输入哈希、原loader、全冻结 | ELIGIBLE |
| 末尾取样/无未来答案 | token25冒号，仅前缀捕获 | ELIGIBLE |
| 完整候选分数 | 24条、48序列，P/N无正确标签 | ELIGIBLE |
| 旧新H2计数 | 两参照、两split、未激活/零范数分开 | ELIGIBLE |
| H1实际支持 | 全支持交集、全部转换及冻结候选均保留 | ELIGIBLE |
| 六家族可否统计确认 | 无总体推断；只作描述 | BOUNDED |
| 可否验证功能/额外信息 | 本轮未运行相应对照或干预 | NOT_RUN |

原始数据→数值→有界观察的直接链：behavior_raw.jsonl→候选token求和→behavior_pairs.csv→12/12及6/6切换；cache/new.npz和原S03数组→相同列表归一化→H2_old_new_pairs与direction_counts→保持/反向/未激活；原始最终z支持→support_transitions与actual_intersections→H1支持变化。上述来源均在results及evidence保留。正文/后缀/阈值/候选没有运行后修改。
