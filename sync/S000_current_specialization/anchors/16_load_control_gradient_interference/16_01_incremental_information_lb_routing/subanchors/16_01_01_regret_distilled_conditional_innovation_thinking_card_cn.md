# Thinking Card：效用蒸馏的条件增量 Router

## 我的判断

- **所属研究方向或父问题：** A16_01 可微负载均衡下的层增量路由。
- **具体现象：** 现有 rank-56 Trainable-Innovation 在 20B 两个 seed 上没有可复现的 NLL 优势，而几何可读性通过的方向仍在 expert-choice regret 门失败。
- **机制猜想：** 问题可能不在“增量不存在”，而在监督太间接；若先去掉旧状态可线性预测的增量，再用每个 token 的反事实专家效用直接监督，小分支可能学到 Native Gate 未利用的条件增量。
- **最强替代解释：** 条件残差不含跨文档稳定的专家相对效用，或冻结 expert 的局部效用教师只是短视噪声；任意同维旁路也可能得到同样结果。
- **最不确定的一环：** 冻结 10B 模型上的 expert-choice regret 改善能否迁移到联合训练的 30B NLL。
- **什么证据会改变判断：** 两个 seed 的 held-out 文档上，条件增量分支不能稳定低于 Native、raw-increment 和 Haar-residual 的 expert-choice regret；或通过该门后仍不能改善 30B NLL。
- **当前阻塞的不确定性：** 条件增量是否首先具有可测的专家功能价值。
- **为什么现在需要裁定：** 继续更换公共谱基不能修复现有 E2 失败；应先把训练目标对齐到 expert utility。
- **当前唯一决策：** 是否允许通过两 seed 冻结功能门的条件增量分支进入 10B→30B 联合训练。
- **我依据的材料：** A16_01 20B 阶段结果、三个 E2 no-certificate 结果、0811 公共参数基审计，以及用户在本对话中批准的方案。

## AI 审核

- **唯一未定义对象或隐藏假设：** “专家效用”必须固定为目标 token 局部强制专家后的下一 token loss，不能与长期专家更新效用混写。
- **最小反例或区分实验：** 同一冻结 Native 10B checkpoint、同一功能文档、同一 rank-56 预算下比较 Native、raw-utility、conditional-utility 与 conditional-Haar。
- **需要补充或核验的来源链接：** 父 Anchor、A16_01_E01 证据账本与冻结 E2 数据 manifest。
- **AI 建议：** pursue；先过功能门，再有条件地启动 30B 终点实验。

## 我的确认

- **保留或修改后的判断：** 保留；实现应避免在线八专家反事实开销，并保持 Native Router 存在。
- **是否允许写入正式 anchor：** yes；用户已明确要求据此实现、smoke，并在通过门后提交 30B 训练。
