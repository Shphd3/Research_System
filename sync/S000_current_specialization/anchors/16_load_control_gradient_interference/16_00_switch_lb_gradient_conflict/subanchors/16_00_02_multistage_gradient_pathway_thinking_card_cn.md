# Thinking Card：Centering 是否在训练早中晚阶段减少负载控制的梯度冲突？

状态：`HUMAN_CONFIRMED`；记录研究者在 2026-08-09 明确给出的判断与执行要求。

- **父方向：** 在选择新的负载控制器之前，先解释负载控制是否减慢了有效的 Router 与专家学习。
- **现象：** Vanilla-Full 与 Centered-Full 使用相同的 Switch 负载均衡系数，却形成了明显不同的硬专家使用状态。
- **机制判断：** 减去 running center 可能同时减少语言模型目标与负载均衡目标在 Router 上游路径中的冲突、减少同一专家内不同文档更新的冲突，并降低 LB 更新对独立文本预测的即时代价。
- **最强竞争解释：** Centering 可能只是改变 token 分配或起到正则作用；原始梯度更同向不保证 held-out 学习更快，而且专家参数没有直接的 LB 梯度。
- **改变判断的证据：** 在 Vanilla 与 Centered 的早期、中期、后期 checkpoint 上，保持 seed 和完整状态配对，同时测 Router 上游表征梯度、Gate 梯度、专家 LM 更新冲突、精确 AdamW 影子一步 NLL 与硬负载。
- **数据判断：** 文档级与领域级专家更新测量使用本地 `river-martin` Web of Science 标注摘要，并保留未触碰的数据划分。
- **当前下一决策：** 先执行多阶段梯度路径审计，再决定是否启动 dynamic expert bias 的长期训练对比。
