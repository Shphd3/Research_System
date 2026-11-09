# A11_15 预训练语义迁移效率实验协议

保持 A11_13 的 256-word 任务、`0,1 -> 2,3` 同义表达 split 和共同 H1 指标不变，使用 `Qwen3-0.6B-Base`。

NTP 训练共享格式 loss 与共同 H1 答案 loss：

$$
L_{NTP}^{pt}=L_S+L_I.
$$

MTP 再增加从 prompt 最后状态提前预测同一 A/B 的 H2 loss：

$$
L_{MTP}^{pt}=L_S+L_I+L_D.
$$

训练 300 步，batch size 4，AdamW `1e-5`，seeds `971-975`，远程四卡。每个 checkpoint 评估 train/eval $Q$、共同 H1、私有 H2、同义一致、反事实敏感和预训练局部 token CE/accuracy。

第一门槛是 evaluation 可解；只有至少一种方法在 `4/5` seed 连续三次达到 $Q\ge0.9$，才比较 MTP/NTP 的 $T_{0.9}$ 与 token-AUC。如果两种方法在至少 `4/5` seed 的 step 0 已有 $Q\ge0.9$，则报告“任务可解但受天花板限制”，不判定训练效率。该实验是决策位置微调，不代表纯预训练 MTP 效率。
