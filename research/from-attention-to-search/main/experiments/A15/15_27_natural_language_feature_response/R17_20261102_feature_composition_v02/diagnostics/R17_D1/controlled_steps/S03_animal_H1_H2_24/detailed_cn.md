# S03 执行、读法与核验

数据、筛选与止步规则见[冻结协议](protocol_cn.md)和[frozen_plan](frozen_plan.json)。H1/H2原命题及旧结果未修改；本轮直接用户指令是执行授权来源，运行完成不代表科学接受。

探索完成2026-11-03T12:07:53.844658+00:00；候选冻结2026-11-03T12:08:11.921935+00:00；保留完成2026-11-03T12:08:59.935083+00:00。CPU推理分别26.34/27.91秒，FP32两线程，固定物理4×192；每阶段额外一次无hook对照，最大差为0。没有生成答案或LM-head行为重测。

输入模型权重SHA `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`；与S02一致。原生loader、SAE权重哈希和hook见两个capture收据。

## ATTN_SAE

重建相对L2误差定义||h-decoder(z)||2/||h||2，24条中最小／中位／最大=0.334739/0.406187/0.492346。这是该hook单点的近似误差，不作跨接口质量排名。

decoder范数范围0.999999046至1.000000834；最小Top32第32与33值差0.004713297，边界精确并列0。原生激活都是32个，不是人为阈值筛成32。新成员可能来自Top32竞争；完整preactivation也保存。

[全部24条全文与全部活跃ID/数值](ATTN_SAE/casebook_cn.md) · [全部候选值](results/ATTN_SAE/candidate_values.csv) · [成员转换](results/ATTN_SAE/transitions.csv) · [H2同支持配对](results/ATTN_SAE/H2_pairs.csv)。

## MLPIN_SAE

重建相对L2误差定义||h-decoder(z)||2/||h||2，24条中最小／中位／最大=0.171619/0.207678/0.251560。这是该hook单点的近似误差，不作跨接口质量排名。

decoder范数范围0.999998927至1.000001073；最小Top32第32与33值差0.000723362，边界精确并列0。原生激活都是32个，不是人为阈值筛成32。新成员可能来自Top32竞争；完整preactivation也保存。

[全部24条全文与全部活跃ID/数值](MLPIN_SAE/casebook_cn.md) · [全部候选值](results/MLPIN_SAE/candidate_values.csv) · [成员转换](results/MLPIN_SAE/transitions.csv) · [H2同支持配对](results/MLPIN_SAE/H2_pairs.csv)。

## 完成范围与原始记录

| 接口 | 共同候选 | 猫新增 | 狗新增 | H2候选 | 全支持相同/6 | 列表支持相同/6 |
| --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | 6 | 6 | 6 | 6 | 0 | 6 |
| MLPIN_SAE | 6 | 6 | 6 | 6 | 0 | 6 |

保留旧S01/S02文件140个，哈希全部相同。24条输入token重放，72条转换计数、72条H2差值、1152个候选加权数值独立复核通过。数据标签、目标token与位置、候选门控和编码规则均通过；这些是实现有效性，不是原H1/H2的科学确认。

data为24条加旧12条及原分数；cache的两个NPZ含ID、h、最终z、完整preactivation、32/33阈值、decoder范数和重建误差；results含共同/新增/消失逐原子事件、探索排序、固定候选四条件值、归一化、全部失败与分组覆盖；figures含两接口各3幅。code保留实际脚本；evidence保存冻结、捕获、检查和交付收据。归一化是候选向量内的计算；总幅度及原始值始终可取回。

## 覆盖台账

| 项目 | 状态 | 边界 |
|---|---|---|
| 数据和旧结果保留 | DONE_VALID | 24条，旧12条不变 |
| 两套原生SAE与位置 | DONE_VALID | 冻结，CPU，无后续token |
| H1共同/新增/强度与检查 | DONE_EXPLORATORY | 6家族，未测额外信息 |
| H2比例/同支持/方向与检查 | DONE_EXPLORATORY | 未测额外预测信息 |
| 图、完整例、失败例、核验 | DONE_VALID | 仅当前受控数据 |
| H3/H4/训练/probe/干预 | NOT_RUN_BY_SCOPE | 用户要求停止 |
| 科学接受、下一步决定 | Unknown | 等待共同审阅 |
