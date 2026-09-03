# A16_01：可微负载均衡下的层增量信息路由


## 1. Problem Definition

A16 研究 MoE 如何在维持稀疏专家可用负载的同时，不减慢语言模型学习。A16_00 已说明可微负载均衡目标的作用随训练阶段变化，但没有选出有用的 Router 表征；A15 则说明固定 covariance band 可以改变分发，却没有获得功能坐标证书。因此本父 Anchor 测试的是实际路由干预，而不是再次指定频带。

对第 $\ell$ 层，令 $n_\ell^{old}$ 为 attention 写入加入前的归一化 token 状态，$n_\ell^{new}$ 为 attention 后实际对 Router 可见的归一化状态，$u_\ell=n_\ell^{new}-n_\ell^{old}$ 为**同层可见增量**。**增量分支**是在保留原生完整状态 Gate 的同时，从 $u_\ell$ 计算低秩残差 logits。

唯一决策问题是：**在四层 MoE 初始化、DCLM 顺序、真正可微的 Switch 负载均衡、优化器和 30B-token 终点完全配对时，显式增量分支是否改善 held-out next-token NLL；当独立认证的冻结方向存在时，它的收益是否超过同维 Haar 随机方向？**

注册两种实现。Trainable-Innovation 是工程版，端到端学习低秩投影；Certified-Innovation 是科学版，只有冻结方向先通过表示证书和专家效用证书才可启动。Native-LB 与 Haar-Innovation-LB 分别控制普通训练和额外低秩容量。本 Anchor 不判断认证语义目标是否普遍，也不把任何终点差异全部归因于负载均衡。

## 2. Physical Priors

1. 零输出初始化的残差分支可以在不删除信息、不改变 step-0 路由函数的情况下引入候选输入；若 no-op 恒等式失败，该先验不成立。
2. 若实际增量包含在完整状态中难以被 Gate 隔离的专家选择信息，专用低秩路径可能降低有限训练预算下的优化难度；若两个 seed 的工程版都不改善 30B NLL，该先验不获支持。
3. 只有在不看终点 NLL 所选方向超过同维、同启动状态、同计算的随机方向时，才能把收益归因于方向身份；否则额外容量、正则化或稳定旁路仍是最强解释。

## 3. Falsifiable Hypotheses

- **H1，工程效用：** $u_\ell$ 上可训练低秩分支在两个配对 seed 中都改善 30B held-out NLL。
- **H2，认证方向身份：** 同一冻结方向通过 E1 表示准入和 E2 专家效用准入后，Certified-Innovation 在两个 seed 中都优于 Native-LB 与 Haar-Innovation。
- **最强竞争解释：** 完整 attention 后状态已经含有全部可用信息；任何表面收益来自额外参数、延迟启用、正则化、负载变化或随机低维条件，而不是认证方向身份。

Engineering Pass 只支持 H1，不支持 H2。Scientific Pass 必须满足 H2，不能由 H1 推出。完整有效运行不满足对应两 seed 规则为 Fail；若到 10B 仍没有两 seed 的共同 E1+E2 证书，科学比较记为 `INSUFFICIENT_NO_CERTIFICATE`；已预提交的 Certified/Haar 任务保持休眠的 Native 行为到 30B，不得解释为科学条件。

## 4. Mathematical Model

实际同层对象为

$$
n_\ell^{old}=N_\ell(h_\ell),\qquad
n_\ell^{new}=N_\ell(h_\ell+a_\ell),\qquad
u_\ell=n_\ell^{new}-n_\ell^{old}.
$$

Native-LB 使用 $g_\ell^{native}=W_\ell n_\ell^{new}$。工程版使用可训练 rank-$k$ 分解：

$$
g_\ell^{eng}=W_\ell n_\ell^{new}+B_\ell A_\ell^\top\operatorname{RMS}(u_\ell),
$$

其中 $A_\ell\in\mathbb R^{d\times k}$、$B_\ell\in\mathbb R^{E\times k}$，启用时 $B_\ell=0$。科学版使用冻结方向和冻结 TRAIN 统计量：

$$
g_\ell^{cert}=W_\ell n_\ell^{new}+C_\ell P_\ell^\top S_\ell^{-1}(u_\ell-\mu_\ell),
$$

其中 $P_\ell^\top P_\ell=I$，启用时 $C_\ell=0$。Haar 只把 $P_\ell$ 替换为固定同秩 Haar frame，其余完全匹配 Certified。

所有条件优化

$$
L=L_{LM}+0.01\sum_{\ell=1}^{4}L_{LB,\ell},\qquad
L_{LB,\ell}=8\sum_e\overline p_{\ell,e}f_{\ell,e},
$$

其中 $\overline p$ 是平均 softmax 概率，$f$ 是 stop-gradient 的 hard top-1 token 比例。唯一主观测量是文档配对的 30B 终点差 $\Delta NLL(A-B)=NLL_A-NLL_B$，单位 nat/token，负值表示 $A$ 更好。它衡量固定 token 预算下的预测质量，不能证明专家专业化是唯一中介。

## 5. Computational Realization

使用已验证的四层、hidden size 768、八稀疏专家加一共享专家、top-1 DCLM MoE。Native-LB 和 Trainable-Innovation-LB 在 seed 17/29 中分别共享 step-0 状态，从头训练到 30B。工程版 rank 固定为 56，这是注册的八父类、每父类八 child 构造所支持的最大判别秩；该端到端因子只是工程对象，不能称为语义方向。

在 Native 的 2B、5B、10B checkpoint 上应用冻结的[层增量信息方法](/daily_research_reports/backup/2026/08/0810/docs/layerwise_incremental_information_routing/README.md)。E1 要求由 TRAIN/DEVELOPMENT 构造的 rank-56 方向相对旧状态提供 held-out conditional-fine 可读增益，并超过同秩 Haar 与父类内标签置乱；E2 冻结模型、专家和方向，要求 held-out 选专家遗憾低于 old-only 与同秩 Haar。两个 seed 首次至少一个共同层同时通过的里程碑记为 $t^*$；秩在 confirmation 前固定，不能根据终点结果选择。

全部八个任务从配对 step-0 状态启动。Certified 与 Haar 带有休眠的零输出分支；启用前，它们的模型参数、优化器状态、数据游标和 Router 行为必须与 Native 逐项一致。在 $t^*$，配对休眠任务在不改变已有模型和优化器状态的情况下加载冻结 Certified/Haar frame，激活零输出 head，并继续到相同的 30B 总 token 终点。若 10B 仍没有 $t^*$，两者保持休眠到 30B，科学比较记为 insufficient。在线推理只使用当前样本的 $u_\ell$；匹配双差分只用于离线学方向，绝不是 Router 输入。

## 6. Minimal Falsification Tests

决定证据只有一个终点 NLL 指标，但给出两个 typed comparison：

1. **工程版：** 30B 的 Trainable-Innovation 减 Native。
2. **科学身份：** 30B 的 Certified 减 Haar，并由 Certified 减 Native 保护。

Pass 要求每个 seed 点估计都为负，且各自文档配对 95% 区间都在零以下。科学结果还要求存在合格 $t^*$，并且 Certified/Haar 启动状态精确匹配。完整有效比较不满足规则为 Fail；LB 回传缺失、step-0 或启动状态不配对、数据顺序分叉、增量重构失败、checkpoint 缺失或终点评估不完整为 Insufficient。

硬守卫检查 $n^{new}=n^{old}+u$、零输出 no-op、每层有限非零 LB-only Gate 梯度、分支梯度可达、checkpoint 精确恢复、token hash 配对，以及 Certified/Haar 的秩、参数与 FLOPs 匹配。负载、路由熵、分支 logit 范数、route flip 与 NLL/FLOP 只解释结果，不能挽救失败的主比较。

## 7. Current Evidence

终点比较仍为 `NOT RUN`，但执行已经开始。修正版不可变实现通过了四个 arm 各自的 8×5090 smoke 合同：可微 LB 到达每层 native Gate，预期的 innovation 与上游路径获得梯度，冻结 frame 不获得梯度；各 arm 保持 step-0 与数据身份一致，checkpoint 和证书状态可精确恢复。八个 30B 作业已全部提交，并在注册的十分钟启动审计中保持 RUNNING、零重试、LM+LB 数值有限且 TensorBoard 可用。这些只属于执行有效性事实；当前还没有里程碑 E1+E2 证书，也没有结果证明同层低秩增量改善 NLL。

## 8. Claim Boundary And Next Decision

即使 Engineering Pass，也只能支持在当前四层、两 seed、30B、LB 控制设置中，可训练增量分支具有实用价值；不能证明学得投影表示语义新增。Scientific Pass 还可说明预先准入的方向在该设置中超过匹配随机方向，但不能证明普遍语义层级、尺度迁移或专家专业化是唯一中介。

唯一下一决策是保持配对训练到注册的 2B 里程碑，并执行冻结的“两 seed 共同 E1+E2”准入流程。完整 anchor 的完成仍要求八个数值合格的 30B 终点；Certified/Haar 只有存在 $t^*$ 时才获得科学终点裁定。恢复动作是审计两个 Native 的首个完整 2B checkpoint，按注册规则生成共同证书 artifact，或让休眠分支持续到下一注册里程碑；不允许根据结果修改架构或阈值。
