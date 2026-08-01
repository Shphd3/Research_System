# 功能目标相同时，输入方差不均会让线性 Gate 先学会大方差方向吗？

状态：已形成受控因果认识更新；真实 DCLM 联合训练因负载守卫失败而证据不足。

## 1. 本日唯一回答的问题

**问题：** 当不同谱方向承载同等强度的专家区分目标、输入总能量也保持一致时，输入在不同方向上的方差不相等（covariance 各向异性）本身是否会让线性 Gate 更早学会高方差方向？

**为什么重要：** 这决定现有 Router 的 head 偏好是否存在一个可独立验证的训练速度来源，而不只是 head 输入能量更大或 tail 根本学不会。

## 2. 认识更新

**一句话回答：** 会；在固定表征、匹配专家目标和不带动量与权重衰减的随机梯度下降（SGD）下，大方差方向不是 Gate 的功能目标，却会缩短达到同等学习进度所需的更新次数；在本次注册谱比下，学习时间比近似遵循输入方差比的倒数。

这里把输入方向按方差由高到低称为 head、middle、tail，并用“达到一半目标所需的更新次数”比较学习速度：每个频带都以自己的同等强度目标为基准，次数越少表示学得越快。平谱时三者都约需 141 步；中等非平谱时约为 56、111、223 步；强非平谱时约为 29、114、457 步。把强非平谱白化后，三者又都回到约 141 步。

这排除了三个主要误解：总能量已匹配，因此不是整体学习率变大；平谱随机旋转没有产生同量级顺序，因此不是任意方向巧合；只给 tail 目标时它最终也能学会，因此慢不等于不可表达。认识应更新为：**奇异谱给线性 Gate 一个有限时间的学习速度偏置，使 head 先进入 Router；它不推出最终只看 head。**

## 3. 关键证据图

![非平谱分离学习时间，白化后重新重合](../../Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_E03_S_controlled_spectral_learning_dynamics/figures/e03_s_crossing_times.png)

**读图结论：** 同一条件内三条曲线的纵向距离表示学习同等比例目标所需更新次数的差异；平谱时重合，4:2:1 约形成 1:2:4，16:4:1 约形成 1:4:16，而白化后重新重合。这直接支持输入方差谱是受控系统中的速度来源。

**完整证据：** [E03-S 结果摘要](../../Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_E03_S_controlled_spectral_learning_dynamics/summary.md)；[完整证据记录](../../Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_E03_S_controlled_spectral_learning_dynamics/detailed.md)。

## 4. 解释流程图

```mermaid
flowchart LR
  A["先把各方向的专家目标强度和输入总能量匹配"] --> B["只改变输入谱是否平坦"]
  B --> C["方差越大的方向达到同等拟合所需更新越少"]
  C --> D["谱差越大，head 到 tail 的时间差越大"]
  D --> E["白化后时间差消失，只给 tail 目标时最终也能学会"]
  E --> F["认识更新：奇异谱造成有限时间 head-first 偏置，而非 head-only 能力"]
```

## 5. 边界与下一步

- **成立范围：** 固定高斯表征、固定谱基底、各方向强度匹配的软专家分数目标、线性 Gate、无正则随机梯度下降；8 个随机种子与 2,048 个平谱随机旋转对照全部通过。
- **仍不能说：** 真实 DCLM 中的 head alignment 一定由该机制产生、AdamW 保留同一排序、专家共同训练会继续强化它、middle/tail 没有功能，或频谱分发提高验证损失/FLOP。
- **最强未决解释：** 真实训练中专家优势谱与上游基底同时变化；本次 [E03-R](../../Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_E03_R_real_early_spectral_learning_dynamics/summary.md) 的三个 seeds 到 step100 时，都出现某一层连续 20 步约 99% 的 token 流向同一个专家，因而无法区分谱动力学、专家反馈与路由塌缩。
- **唯一下一决策：** 是否批准一个仍不使用负载均衡辅助损失（`lambda_lb=0`）、但重新冻结非梯度负载稳定规则的 E03-R 新 Protocol。
- **完成判据：** 新 Protocol 必须先在三个随机种子上越过本次失败窗口，同时不触发“任一专家份额 $>0.8$”或“至少四个专家完全不接收 token”的守卫，再进入 2B-token 轨迹；科学判据继续要求至少两个随机种子的形成时间超过随机方向对照，且不能由基底漂移单独解释。
- **恢复时第一动作：** 审核 E03-R 的 `insufficient_load_guard` 结果记录，先决定是否值得修订负载稳定条件；现有轨迹在首个注册训练检查点前停止，若获批准必须从初始化重跑。
