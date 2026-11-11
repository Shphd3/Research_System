# R04实现与分析补充（Codex接管，训练首次启动前）

本补充保留原冻结Protocol，不改变A6/A5目标、预算、λ规则、数据或P1–P4预测。当前share pt-nmcuobkl排队，尚无训练更新。

1. 修复逐位置脚本的A2随机score分支，采用与训练评估相同的seed/序列/rank映射，并启用确定性计算；保留Claude旧A1产物，重新生成，旧差异真实最大值见执行根evidence/A1_prior_position_precision.json。
2. 修复A6 total_loss日志漏正则，补充concentration raw/weighted的token/update TensorBoard标签；实际正则梯度算法与目标不变。
3. 冒烟恢复由正常10+10退出改为完整10步保存后的真实外部SIGKILL进程树，再恢复到20；记录外部kill及逐步一致性。
4. A6/A5在训练时同一次评估中直接捕获逐位置fp16损失、uint8 Top2与原FP64总体NLL，避免bf16权重快照重算与训练评估不一致；每250步bf16快照及完整存档策略不变。
5. 位置账本保留原n≥50、配对SE、BH q<.05与0.01nat阈值；净遗忘对从此前多个checkpoint选最低值这一选择作Bonferroni，再跨原子BH。位置之间相关未被配对SE消除，结果为描述性。
6. 现有A0缺部分250步存档，A4/A1-deep只存1000/2000；不补训、不编造。保留相邻可用区间，另补所有臂共同1000→2000区间用于比较。
7. 固定score仍有变化的load bias，P4的近零翻转是待检验预测，不将χ强设0；按实际硬Top2集合计算。

实际代码、输入访问与三项审计位于执行根evidence/。研究者判断Unknown。
