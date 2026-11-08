派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/protocol_cn.md)；研究修改仍回到原件。

---

# R01 冻结逐checkpoint行为检查协议

本轮执行授权来自当前研究者“设计并执行、先核查可行性”的明确请求；资产、工程与现有资源预算检查通过后执行。科学接受Unknown。原生Dense与普通MoE，参数与负载偏置冻结，无训练。

先审计全部真实状态并核验哈希、计数、严格加载。24正式内容家族，六模板，物品／颜色／目的地各8家族；另6工程家族。主前缀1152token，真实间隔16/256/1024，占2048上下文的0.78/12.5/50%。主条件保持答案位置、问题、候选和填充token库存，A/B只替换关键事实；事实绝对位置和填充顺序仍是混杂。每个距离含A/B、无证据和错误实体事实；后两者没有正确标签。另做1024间隔的填充顺序反转与1408前缀绝对位置对照。每个正式状态384提示，smoke每模型96提示，全部文本在首轮模型分数前冻结。

完整候选为前导空格＋词语＋句号，分数为逐token自然对数条件概率之和。保留逐token、首token、去句号和长度平均分。配对候选token数相同。两侧都严格选对才记家族成功，平分失败；另报逐提示准确率、正确分差、偏好变化和无效证据偏好。以24家族为主要单位，95%Wilson区间，10000次家族配对bootstrap，六模板聚类敏感性；不能把改写当完全独立样本。全部内容、模板、退化点保留。60/80/90%首次采样跨越与下一已测点保持只是AI描述性敏感性，不是研究者确认的通用学会标准，也不插值出现时刻。近程也弱时，不能辨认距离特有学习差距。

先在Dense33B与Baseline33B核验原生CE和完整候选计分、前缀一致、有限值、冻结与截断。BF16事先工程容差为CE和分数差<0.03nat、前缀隐藏状态最大差<0.15；行为分数不决定是否保留任务。使用当前容器H100MIG3g.40gb，不申请新作业；FP32参数，CUDA BF16 autocast、FP32logsoftmax、关闭TF32，8提示×2候选批次。预计完整阶段≤3600秒才推进，正式阶段硬上限3600秒；缺失、损坏、部分结果全部保留，失败不替换权重或改测试。

报告支持、不支持和不足分支，保留训练进度不匹配状态，再做真实同token比较。Dense281431040总／激活参数，MoE507988992总、281496576常规激活；训练顺序仅核实一致至22.018691584B。因此结果是两条实际轨迹的行为描述，不给出干扰或专家机制归因。交付全部状态与原文／位置／分数、曲线与区间、脚本／配置／成本及中文事实报告。后续状态选择为AI建议，不训练SAE、CrossCoder、router或底模。完整A–G范围审计与冻结／修订约束见英文主协议。


## Amendment A01 — runtime estimator correction

After smoke and before full scores: the initial estimator scaled checkpoint load/SHA overhead by the fourfold prompt ratio. Corrected to one load per state plus fourfold score time, using actual14Dense/23Baseline composition. Estimate4579.790s→1394.601s; ceiling remains3600s. Texts, scoring, tolerances and state selection unchanged. Original receipt retained; [amendment](../../../../../../../../UNAVAILABLE.md). Implementation correction under the current execution request, no scientific criterion change.


## Amendment A02 — post-hoc numerical verification

After primary results were visible, recheck every main prompt with absolute BF16 correct-minus-other margin<0.06nat plus paired fact inFP32, fixed in code before launch;300s ceiling on existing resource. Original texts, thresholds and BF16 primary unchanged. Report all flips separately; never call the subset a fullFP32trajectory. [Scope and exposure record](../../../../../../../../UNAVAILABLE.md). Current user requested complete behavior and anomaly checking; no training or new remote resource.
