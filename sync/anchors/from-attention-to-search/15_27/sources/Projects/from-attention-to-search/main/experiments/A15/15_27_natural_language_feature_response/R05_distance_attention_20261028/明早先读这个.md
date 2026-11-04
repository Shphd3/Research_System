# 明早先读这个

我们问：哪些 feature（字典中的固定坐标） 真会随远处前文内容而变，是否也在强 Attention 两端共同出现？实际比较是五个距离的相关／无关编辑，以及相近距离的高／中 Attention 配对。结果是 **B 尚无确认的远距候选；A 有部分近距共同激活关联，远距主比较不足**。

**先看实际执行的构造文本。** X写`The gardener watered a living organism with green leaves and roots.`；Y改为`The manager inspected a factory where workers assembled metal parts.`（植物／工厂）。后面保留同样的 `The final report described the plant`。读 `plant`（token ID6008，位置239）；线索结束于95，所以距离为239−95＝144，中间有143个token。CrossCoder f447最后层重构贡献为9.920／0；只改Monday为Tuesday的平均变化为0.077。这里的贡献指重构表征的幅度，不是功能重要性。可是同一家族换一种措辞后，四个版本都是0。[原文与反例](examples_cn.md)

**四张图看什么。**

- [图1](figures/figure1_distance_response.png)：横轴是五个测试距离，纵轴是贡献变化。f447在144处的留出均值为相关0.532、无关0.033、相减0.500个发现RMS（作为固定标尺的均方根）单位；校正q＝0.404，仍属证据不足。平均曲线为正不能替代逐feature复现。
- [图2](figures/figure2_frequency_response.png)：每点一个候选。f447在DCLM命中617/65536＝0.9415%，但远距确认不足。45个候选全部保留；目前无法判定“稳定远响应”偏向哪种频率。
- [图3](figures/figure3_attention_coactivation.png)：纵轴给两端共同命中。CrossCoder高频组在1–32档，高／对照为1.935%／1.515%，差0.420个百分点，校正q＝0.0285；129–160档只差0.044个百分点，未达到预定0.1个百分点。这里比较的是不同token ID；同ID仅4–8篇匹配文档，单列缺项。
- [图4](figures/figure4_crosslayer_contribution.png)：每行一个CrossCoder候选、每列一个真实block。f447最后层平均贡献1.343除以参考RMS609.319＝0.002204。旁边的decoder范数说明层间形状由字典固定，不能解释成信息逐层产生。

**两条认识更新。**

1. 远处编辑能出现大的局部变化，但本轮尚无跨家族稳健名单：SAE20个、CrossCoder25个候选均未达到全部确认条件。措辞、目标词匹配及重复填充仍可解释变化，不能据此宣称长程专属或正确理解。
2. 强Attention与部分近距共同激活有关：CrossCoder高频组及25候选合看均满足近距标准；后者差1.154个百分点。共同局部内容、词性／句法差别和Attention之后的读数仍是竞争解释；这既不能补上B的远距复现，也不证明沿边传递了feature。

**判定：** B＝证据不足；A＝部分支持近距关联，远距确认及同ID比较证据不足。没有发现已验证远距角色，因此频率／层分布仅描述待验证候选。新前向1096/1096，训练、干预、新资源和封存TEST均为0。

**唯一下一步建议，未执行：** 固定`plant`，用独立措辞和非重复填充，验证f447的144-token响应能否复现。先分清具体目标词下的稳健响应，再谈远距组织。

[详细解释](detailed_cn.md) · [逐图读法](figures_cn.md) · [参数与代码附录](appendix_cn.md)
