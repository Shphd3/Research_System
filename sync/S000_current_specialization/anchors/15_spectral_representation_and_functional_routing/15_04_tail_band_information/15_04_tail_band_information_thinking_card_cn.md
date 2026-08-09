---
thinking_card_id: 15_04_tail_band_information
status: researcher_direction_confirmed_minimal_geometry_only
human_language: zh
formalization_authorized: confirmed
execution_authorized: false
---

# Thinking Card：共同参数秩后移是否落入跨层共享 tail

> 研究者 2026-08-09 确认：A15_04 是当前 close-out gate，但只允许一次现有固定样本集合上的最小几何检验。几何通过后才区分近零响应汇与功能通道；当前不批准删除 tail、下游任务、Router 或执行。

## 我的判断

- **当前判断：**A15_02_07 不支持复杂目标特异的参数秩后移或条件新增线性信息；保留现象是简单与复杂目标共有的逐层后移。
- **已有证据：**参数 tail 的跨层方向重合已经测过，而且比 head 更强；无需重复检验参数对齐。
- **当前缺口：**尚不知道晚层语义方差是否进入那个跨层共享 tail，还是任意等维随机空间都能捕获相似结构。
- **最强竞争解释：**tail 是共享的近零响应汇，或语义表示足够分布式，导致随机空间也可读；二者都不能推出功能。
- **会改变判断的证据：**同一语义协方差在真实共享 tail 中出现比随机、head 和 middle 更强的晚层增量；否则停止共享-tail 解释。
- **当前唯一决策：**把这一个比较写成可审核 Protocol；不扩大数据和任务。

## 术语解释

- **固定样本集合（bank）：**实验前冻结且不按结果更换的一组文本；本轮是 A15_02_06 的 512 条样本。
- **互斥层组（fold）：**把层分成互不重叠的两组；一组只构造共享空间，另一组只检验，再交换角色。
- **子图（panel）：**一张大图中的一幅小图；正式文档下文只写“子图”。
- **近零响应汇（near-null sink）：**参数增益接近零而不是 activation 接近零；信息可能存在并可读，但本层 MLP 对它反应很小。

## AI 审核

- **最小实验：**保持模型、activation 和数据不变，只把测量投影换成真实共享 tail、该层 local tail、等维随机、共享 head、共享 middle。
- **主指标：**真实共享 tail 的超随机捕获量之“晚层减早层”；它只裁定几何，不裁定功能。
- **功能边界：**只有几何 Pass 后，才可另立 counterfactual：从 $\Delta n_\ell$ 删除共享-tail 分量，并与等能量控制比较即时 MLP 响应和同一批题目的目标损失。

## 我的确认

- **保留后的判断：**先连接“参数 tail 共享”与“语义共同后移”这两项已有观察；不能连接时关闭 tail 功能化路线。
- **授权边界：**允许完善 Anchor 和起草不可执行 Protocol；不批准实现、smoke 或 full run。
