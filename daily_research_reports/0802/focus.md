# 从频谱画像到频谱专家效用：Router 应学习什么信号？

状态：已完成认识更新；下一项冻结验证尚未建立 Anchor/Protocol。

## 1. 本日唯一回答的问题

**问题：** 已知线性 Router 容易依赖大方差方向、而固定激活频带又没有稳定功能收益后，下一代频谱 Router 应估计什么信号？

**为什么重要：** 这决定下一步是继续按激活谱分组，还是把频谱变成“哪个专家能让当前 token 损失下降更多”的效用估计。

## 2. 认识更新

**一句话回答：** 不应把某个激活频带直接当作专家标签；下一步应检验输入激活、专家权重奇异通道和输出误差信号三者的对齐，能否预测专家的反事实效用。

1. **频带是坐标与学习速度先验，不是功能标签。** 大方差方向更早形成稳定路由，middle/tail 也保留额外几何，但固定 ranks 65--768 没有跨 LB/decommon 稳定预测共同训练兼容性；而且不同层相同谱秩不保证编码相同变量。
2. **Router 与专家是双向共同演化。** selected-only 反馈让先被选中的专家继续获得数据，低方差信号因此更难纠错；已有理论也表明 Router 行与被选专家输入权重会沿相同 token 隐状态方向更新，所以观测到的 Router--expert 几何既可能是能力，也可能只是历史分发留下的耦合。
3. **专家权重谱比激活谱更接近功能坐标，但仍不是效用本身。** 权重 SVD 描述专家能读写并放大的通道；只有再乘上 token 对该通道的激活以及当前输出误差对该通道的需求，才形成可检验的专家效用代理。

**关键关系：** 若专家线性通道 $W_e=U_e\Sigma_eV_e^\top$，token 表征为 $h$，输出损失对专家输出的梯度为 $g$，则一阶效用分数为

$$
S_e(h,g)=-g^\top W_eh=-\sum_k\sigma_{e,k}(u_{e,k}^\top g)(v_{e,k}^\top h).
$$

其中 $v_{e,k}^\top h$ 是输入是否激活该通道，$\sigma_{e,k}$ 是专家通道增益，$u_{e,k}^\top g$ 是当前误差是否需要该输出方向；三者缺一都不能决定专家效用。

## 3. 关键证据表

| 已知结果 | 排除的简单解释 | 仍缺少的决定量 |
| --- | --- | --- |
| tail 稳定路由约需 1938 步，等能后约 615 步 | tail 不是随机噪声，低方差本身会造成学习延迟 | 哪个专家能利用该信号 |
| oracle 覆盖把 M/T 纠错率从 0.500 提到 0.977 | selected-only 反馈会把早期偏置固化 | 未选专家的反事实收益 |
| 固定 M/T/N 未通过兼容性准入 | “产生新划分”不等于“改善专家学习” | 专家特异的功能分数 |
| 权重 SVD 给出专家局部读写通道 | 激活 covariance 不是唯一可用频谱 | 输入×权重×误差的联合对齐 |

**读表结论：** 当前缺口不是更多 PCA 画像，而是把层级/组合信号映射到专家特异的损失收益，并证明该映射超过 Router 历史几何与权重 SVD 单独基线。

**完整证据：** [A15 主线](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_linear_gate_spectral_training_bias/README.md)；[固定频带功能检验](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_02_middle_tail_functional_resolution/A15_02_01_E01_cross_update_compatibility_gate/summary_cn.md)；[学长的 SVD feature 定义](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/017_feature_grained_moe_logic.md)。

## 4. 解释流程图（AI 初稿，研究者修改）

```mermaid
flowchart LR
    A["激活谱揭示层级信息与学习速度"] --> B["固定频带不能稳定预测专家学习收益"]
    B --> C["Router 与专家又会被历史分发共同塑形"]
    C --> D["用专家权重谱定义可读写通道"]
    D --> E["再加入 token 激活与输出误差需求"]
    E --> F["用强制专家损失检验真正效用"]
    F --> G["通过后才训练效用对齐 Router"]
```

## 5. 边界与下一步

- **成立范围：** A15 的控制实验、DCLM 冻结检查，以及学长项目中的 matrix-local SVD 建模共同支持这一问题重构。
- **仍不能说：** 大奇异值方向一定有害、权重 SVD 等于语义、上述一阶分数已经能改善 Router，或小模型规律会自动扩展到 7B--8B。
- **最强未决解释：** 三方对齐分数可能只复现已有 Router/专家共同历史，并不能预测未选专家的反事实损失优势。
- **唯一下一决策：** 在四层概率树 MoE 上，三方频谱效用分数能否比 native logits、激活频带、权重 SVD、Router--expert centroid 和同维随机对照更准确地选择最低损失专家？
- **完成判据：** 在未见组合、独立文档与错误层/置换对照上，显著降低强制专家选择的 held-out top-1 loss regret，并跨三种子和 coarse/fine/composition 变量复现；通过才解锁小模型匹配训练。
- **恢复时第一动作：** 为“Spectral Expert Utility”建立 Anchor，冻结强制专家效用标签、三方分数、五类对照和 pass/fail/insufficient。
