# 学会遗忘与router：既有长尾问题的子分析

隶属现有问题1，不新增独立研究问题；接续1111-学会遗忘的四张图。AI分析；研究者判断Unknown。

## 2026-11-10T18:24:41.737729+00:00｜A–F完成补记

1. 假设：MoE多学会内容可能对应router集中；两架构共同遗忘可能有共享来源；后期干扰可能是估计噪声；A5可能改变expert条件谱。
2. 先验→模型→计算：分发筛选表征方向→掌握率/集中相关、共享损失变化、跨份梯度T与协方差谱→A控制频率与Dense已有掌握率；B沿R04账本；E复用旧8批次、经用户明确批准扩展独立DEV并比较32与扩展8；F八层norm2、DEV定义低频方向、EVAL测量，共同A0表征和打乱标签控制。
3. 跑前预测：完全沿/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/protocol_cn.md、protocol_E_cn.md、protocol_F_cn.md的冻结读法。支持→保留为几何或局部证据，干预由研究者决定；不支持→报告反例，不改指标；不足→记录缺失或噪声，不补训。此条是完成补记，不重写跑前预测。
4. 结果：A的0.5/1/10B频段相关中位数0.0222/0.0627/0.0429；B的3B→5B共同显著遗忘3169个，Jaccard0.7502、随机11.424倍、变化相关0.8004。E的10B扩展32版均0/120负对，唯一跨时点候选未确认；扩展8也改变负率，不能单独归因序列数。F原始秩顺序0/8，条件/全局秩与低频放大的联合顺序：各自2/8、共同A0为0/8。第7层A5自身低频内部方差放大1.0027，关于全局均值二阶矩1.0234。C早Dense存档缺失；A0新增真实200步前向。表和图：/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/results；速报：/data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup/明早速报_追加_cn.md。
5. 研究者决定：Unknown。只用本地MIG/CPU；未训练、未更新参数、未提交资源、未commit/push；旧实验与旧交付只读。
6. 链条位置：学习现象→相关与局部梯度/条件谱诊断；尚未建立谱变化导致训练收益的干预链。

已strict核验资产：representation_learn_forget_followup_early_positions_20261111；dataset_learn_forget_extended_DEV_20261111；analysis_learn_forget_followup_gradient_sketches_20261111；representation_learn_forget_followup_FFN_inputs_20261111；analysis_learn_forget_followup_spectra_20261111；analysis_learn_forget_followup_tables_20261111。GPU占用墙钟与首次中断Unknown见/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/results/execution_cost.csv，不冒充CUDA kernel时长。

今日认识更新：逐feature集中未显示强学习对应；共同遗忘可在两架构量到；后期负梯度符号对抽样敏感；分发改变条件谱，但A5最低秩和明显低频方差放大的完整解释未获支持。

## 2026-11-11T00:06:45.211059+00:00｜组会前补图：有效秩的时间轨迹

1. 假设：原生专家相对于全体输入的有效方向较少，这一结构可能在早期已经形成；竞争解释是只有较晚 checkpoint 才出现。
2. 先验→模型→计算：固定任务 F 的 262144 个 DEV 位置→按各模型各层硬 Top2 分组、分别扣均值→每专家熵有效秩除以同层全局秩，比较前四层与后四层随训练的比值；Dense 仅算全局秩。用既有配对损失做差，另对原 3169 个共同遗忘 feature 的固定代表窗口做关键词粗分。
3. 跑前预测：两个层段 500/1000 步均低于 0.90 且已测后续至 10B 不高于 0.95，就保留早期形成并保持的读法；否则仅保留满足判据的层段或报告不支持。冻结读法见 /data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup2/protocol_cn.md。
4. 结果：四项及 11/11 检查点完成。500 步原生 0.745/0.812、10B 0.790/0.853；A5 2000 步 0.856/0.840、约 1B 0.854/0.842。关键词粗分命中 421/3169，模板类 347504 个去重正激活支持位置。原表、图、输入身份和分位口径见 /data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup2/组会前速报_cn.md；执行回执 /data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup2/evidence。资产 analysis_learn_forget_followup2_20261111 strict 通过。
5. 研究者决定：Unknown；本地 MIG 和 CPU，只读前向与统计，无参数更新。
6. 链条位置：学习现象与表征几何；还不能以秩比解释 A5 的训练收益。

今日认识更新：原生专家输入相对全局的秩缩减在最早已测 500 步就存在，到 10B 仍在；绝对秩却增加。A5 续训时秩比几乎不变，NLL 领先缩小但在约 1B 仍为正。网页模板关键词命中的是共同遗忘特征中的一部分。
