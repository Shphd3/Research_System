# A11_14b 决策加权语义效率实验协议

保持 A11_14 的任务、数据划分、模型、优化器、batch 顺序、token 预算和共同 H1 指标不变。唯一修改是：两种方法都增加权重为 `1.0` 的 H1 决策 loss，MTP 再增加对应的更早 H2 决策 loss，同时保留原来的全位置 loss。

$$
L_{NTP}^{dw}=L_1^{all}+L_I,
$$

$$
L_{MTP}^{dw}=L_1^{all}+L_2^{all}+L_I+L_D.
$$

训练 2,000 步，seeds `971-975`，远程四卡。每个 checkpoint 同时评估 train 与 held-out paraphrase：

$$
Q_{split}=\min\{A_{H1}^{split},C_{para}^{split},S_{cf}^{split}\}.
$$

只有 evaluation $T_{0.9}$ 与 token-AUC 在至少 `4/5` seed 同时支持 MTP，并且 local H1 守卫全部通过，才支持窄化的决策加权语义效率优势。若 train 会而 eval 不会，结论是同义迁移不足；若 train 也不会，则结论是模型拟合不足。

