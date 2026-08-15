# 15_06_02 Router--Expert Specialization Thinking Card

研究者已确认的判断（2026-08-10）：

- 父问题：在线 Local/Relay 频谱 Router 的训练损失差异，是否对应真正的 Router 功能与专家专业化差异。
- 当前现象：五个具有可微负载均衡损失的 seed-17 训练臂已经保存 2B、5B、10B checkpoint，但终点 NLL 不能说明专家是否学得不同、Router 是否选对专家。
- 机制猜想：如果 covariance H/M/T 身份有功能价值，HMT 应比同维随机匹配控制更早形成非互换专家，并让 Router 分数更准确地排序专家反事实效用。
- 最强竞争解释：稳定低维瓶颈本身即可造成参数或输出差异；专家看起来不同，但 Router 没有利用这些差异，或一个专家对所有 token 都普遍更好。
- 会改变判断的证据：在同一文档、同一 token、同一 checkpoint 的配对反事实中，HMT 相对 matched-random 同时降低专家选择遗憾并提高 Router 分数与专家效用的一致性；参数子空间、同输入输出和替换代价形成一致证据链。
- 不能声称：单 seed 冻结审计不能证明专业化导致总体 NLL、不能证明 H/M/T 的普遍语义，也不能评估 PCGrad 的训练收益。
- 当前决策：批准五臂、seed 17、2B/5B/10B 的冻结 Router--Expert 功能与专业化审计；不测梯度冲突和系统负载。
