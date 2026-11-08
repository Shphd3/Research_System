# 长短程认识更新：成员更替不等于事实差异衰减

## 给导师的10秒讲法

物品事实离答案更远时，SAE成员会换，但事实差异没有平均变弱；这个任务窗口里，成员更替不能直接叫作信息丢失。

## 给导师的30秒讲法

我们重算12个留出家族，并补了填充和位置对照。16到128token，Attention平均换掉7.2个成员，MLP换4.1个，但相对事实差异约为近距1.08和1.20倍。换填充、固定事实位置后也没出现平均衰减。多数换入成员此前已有阈值下响应；这个局部观察不等于一般长上下文或因果记忆结论。

## 主图与读法

![距离、成员与事实差异](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/figures/main_distance.png)

左图是仍共同使用的成员数，右图是A/B差的范数相对整体码尺度，再与近距作比。共同成员变少、事实差异幅度仍在可以同时发生。固定六成员方向cos约0.94/0.96不能替代完整码；完整事实差方向约0.60/0.73，幅度与方向必须分开说。

## 必须保留的反例与边界

F11保留较多成员仍有轻微差异减弱；F19的Attention约0.79倍、MLP约1.89倍，回答均正确。反转填充还使近距F28一条失败，分差−0.0848；不能按距离单调解释成功率。原主任务完整候选仍三距12/12，物品词单独评分64为11/12。SAE重构真实A/B差的误差接近1，所以码范数不是模型事实信息量。d=p−e−1也使事实位置/回答位置/距离不能完全独立。


模板相关性敏感性也需保留：按六个模板均值和64种符号互换，Attention的H2原始p=0.03125、Holm p=0.1875，转为证据不足；MLP亦不足。家族主判定按原协议保持，但不能把该保持结论称为跨独立模板确认。

## 唯一值得继续追问的问题（AI建议）

这些随距离重组但未平均衰减的事实差异，哪些真正被答案读取？

本轮不设计或运行相应干预/训练；待共同审阅。[完整结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/summary_cn.md) · [四组全文与反例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/casebook_cn.md) · [所有原始数据/方法/代码](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/artifacts_cn.md)。
