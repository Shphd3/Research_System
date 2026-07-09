# A11 长程 MTP 语义效率：从一阶速度到有限步闭环

## 0. 执行摘要

**研究问题：** 多词元预测目标（MTP，同一个当前隐藏状态预测多个未来词）是否能比下一词预测目标（NTP，只预测下一个词）更直接、更高效地让当前隐藏状态 $h_T$ 保留未来才显现的变量 $Z$。

**机制解释：**

1. 最小基元是 K=2：第一个未来词共享，第二个未来词一一编码 $Z$。

$$
Y_1=A,\qquad Y_2=S_Z.
$$

2. 第一个有信息未来位置 $\tau$ 是第一个新增 $Z$ 信息的位置；只有 $K\ge\tau$ 时，当前 $h_T$ 才收到直接语义监督。

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
$$

3. 覆盖有信息未来词会给当前状态一个读出有效语义速度；在 K=2 最小模型中：

$$
G_1^{margin}=0,
$$

$$
G_2^{margin}=\frac{\lambda_2}{m^2}\sum_z\|u_z-\bar u\|^2>0.
$$

4. general K 的速度不由 $K$ 大小决定，而由有信息未来位置的中心化输出方向向量和决定。

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j),
$$

$$
G_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

5. 新增有信息 horizon 的增量可能为正，也可能被冲突方向削弱。

$$
G_{K\cup r}-G_K
=\frac1{m^2}\sum_z(2v_z^{(K)\top}a_{r,z}+\|a_{r,z}\|^2).
$$

6. 有限步效率还缺一层优化假设：需要从每步 margin 下界推出 hitting time bound。

$$
M_K(t+1)\ge M_K(t)+\eta g_K-\eta^2B-\epsilon_t.
$$

若

$$
\eta g_K-\eta^2B-\bar\epsilon>0,
$$

则候选结论是：

$$
T_\gamma(K)
\le
\left\lceil
\frac{\gamma-M_K(0)}{\eta g_K-\eta^2B-\bar\epsilon}
\right\rceil.
$$

**主要结果：**

1. 已经证明表示保证：如果 $K$ 覆盖 $Y_\tau=S_Z$ 且 $S_Z$ 一一编码 $Z$，低未来词损失会强迫当前 $h_T$ 含有 $Z$。
2. 已经证明并验证一阶语义速度机制：覆盖有信息 future horizon 会给 $h_T$ 正的读出有效语义速度，非覆盖共享目标在分支折叠点没有这个一阶方向。
3. 已经验证 general K 不是越大越好：新增 horizon 是否有帮助取决于它是否含新语义信息，以及输出方向是否与已有语义方向对齐。
4. 当前还没有证明有限步效率定理：$G_K^{hidden}>0$ 还不能直接推出 $T_\gamma(K)$ 更小。
5. 下一步是 A11_10 理论闭环：验证 velocity persistence、margin-to-recovery calibration、head drift bound、shared / indirect perturbation bound；不是 MoE bridge。

**证据说明：**

1. 对结果 1：
   - 理论公式是互信息表示保证：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon
\quad\Rightarrow\quad
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

   - K=2 最小构造支持 objective-level separation：next-two 直接要求 $h_T$ 预测 $S_Z$，next-one 只需要预测共享 $A$。
   - $\tau=3$ 构造支持 first-informative-horizon：K3 覆盖 $S_Z$，K1/K2 不覆盖。

2. 对结果 2：
   - A11_06 的 no-leakage step-0 守卫通过：$Q(0)=0.25$，$M_Z(0)\approx0$，$E_Z(0)=0$，native H3 为 0。
   - A11_06 的一阶速度结果：K1 的 $G_M^{hidden}=7.28\times10^{-12}$，K2 的 $G_M^{hidden}=-1.16\times10^{-11}$，K3 的 $G_M^{hidden}=0.003816$。
   - A11_07 显示 direct 条件同时提升 $Q$、native H3 和 $M_Z^{ref}$；因此 direct path 不能只用 probe 或 $Q$ 解释。

3. 对结果 3：
   - A11_08 固定 K=4、固定两个有信息 horizon，只改输出方向几何：aligned 的 $G_{hidden}=0.015262$，low/conflict 的 $G_{hidden}=0.000954$，`5/5` seeds 支持 aligned 更大。
   - A11_08b 显示 frozen heads 下 aligned 仍有更大早期 $G_{hidden}^{ref}$，说明该机制不只是 step-0 静态构造；但 trainable heads 会 drift，所以曲线必须记录 current geometry。
   - A11_09 显示 K2 为 0，K3 打开，shared H4 无增量，aligned H4 增强，low/conflict H4 削弱。

4. 对结果 4：
   - 现有定理只给 $G_K$ 的一阶下界；还没有证明 velocity persistence、margin-to-recovery calibration、head drift bound 和 shared / indirect perturbation bound。
   - 因此当前不能把一阶速度写成完整有限步训练效率定理。

**结论边界：** 当前只能 claim 受控目标函数机制；不能 claim 自然语言中 MTP 已经优于 NTP，不能 claim NTP 学不到长程变量，不能 claim $K$ 越大越好，不能 claim $Q$ 单独证明 direct supervision，不能 claim MoE 路由保持或专家效用。

**执行动作：** 只推进 A11_10 finite-step semantic efficiency protocol；目标是判定有限步定理所需假设是否 supported / falsified / insufficient evidence。暂不进入 MoE bridge。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 为什么影响判断 | 不能证明什么 |
|---|---|---|---|---|
| 多词元预测目标（MTP） | 同一个当前隐藏状态预测多个未来词 | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ | 判断远处目标是否直接监督当前状态 | $K$ 越大一定越好 |
| 下一词预测目标（NTP） | 当前隐藏状态只预测下一个词 | $L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1)$ | 非覆盖对照 | NTP 不能学习长程变量 |
| 早期语义变量 $Z$ | 前缀中已有、未来才需要的信息 | 受控实验中的分支身份 | 被写入 $h_T$ 的目标变量 | 自然语言全部语义 |
| 当前隐藏状态 $h_T$ | 决策前缀后的模型状态 | $h_z=h_T(Z=z)$ | 直接语义监督作用对象 | 后续所有状态 |
| 第一个有信息未来位置 $\tau$ | 第一个新增 $Z$ 信息的未来偏移 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 决定 $K$ 是否覆盖有效目标 | 真实文本中固定唯一 horizon |
| 有信息 horizon | 未来目标含有关于 $Z$ 的新信息 | $j\in\mathcal I_K$ | 贡献直接语义速度 | 所有未来词都有益 |
| 中心化输出方向 | 去掉共享成分后的 token 输出行 | $u_{j,z}-\bar u_j$ | 决定语义速度方向 | 下游效用 |
| 读出有效语义 margin | $h_T$ 是否沿模型输出头可用方向分开 | $M_K(t)=m^{-1}\sum_z v_z^{ref\top}h_z(t)$ | 有限步定理的 hitting-time 对象 | 自然语言收益 |
| 一阶语义速度 | 当前 loss 对 margin 的瞬时推动 | $G_K^{hidden}=m^{-1}\sum_z v_z^\top(-\nabla_{h_z}L_K)$ | 判断目标函数是否直接推向语义方向 | 多步效率本身 |
| native H3 accuracy | 模型自身第三未来位置预测准确率 | $q_3(\cdot\mid h_T)$ 预测 $S_Z$ 的 top-1 accuracy | 区分模型自身读出与外部 probe | 下游任务价值 |
| 保守恢复分数 $Q$ | 多个可读性检测的最小值 | $Q(t)=\min\{A(t),P(t),S(t)\}$ | 防止 probe-only 假阳性 | direct supervision 来源 |
| hitting time | 指标达到阈值所需步数 | $T_\gamma=\inf\{t:M_K(t)\ge\gamma\}$ | 有限步效率目标 | 全局收敛 |

## 2. 机制解释与建模

### 2.1 K=2 最小基元

K=2 是最小理论基元，因为第 2 个未来目标第一次含有 $Z$：

$$
Y_1=A,\qquad Y_2=S_Z.
$$

定义第 2 位置输出方向：

$$
u_z=u_{S_z}^{(2)},\qquad \bar u=\frac1m\sum_z u_z.
$$

读出 margin：

$$
M_Z^{(2)}(h)=\frac1m\sum_z(u_z-\bar u)^\top h_z.
$$

结论：

$$
G_1^{margin}=0,
$$

$$
G_2^{margin}=\frac{\lambda_2}{m^2}\sum_z\|u_z-\bar u\|^2>0.
$$

这说明 next-two 多出的不是“更多 loss”这个抽象量，而是直接作用在当前 $h_T$ 上的语义方向。

### 2.2 $\tau=m$ 覆盖律

若前 $m-1$ 个未来目标不含 $Z$：

$$
I(Z;Y_j\mid Y_{<j})=0,\qquad j<m,
$$

且第 $m$ 个未来目标为：

$$
Y_m=S_Z,
$$

则 $K<m$ 时没有直接语义速度，$K\ge m$ 时语义速度打开。这是 first-informative-horizon law。

### 2.3 general K 向量和机制

多个有信息未来位置的贡献由向量和决定：

$$
a_{j,z}=\lambda_j(u_{j,z}-\bar u_j),
$$

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}a_{j,z}.
$$

一阶速度是：

$$
G_K=\frac1{m^2}\sum_z\|v_z^{(K)}\|^2.
$$

新增有信息 horizon 的增量是：

$$
G_{K\cup r}-G_K
=\frac1{m^2}\sum_z(2v_z^{(K)\top}a_{r,z}+\|a_{r,z}\|^2).
$$

因此，新增共享未来词没有直接语义增量；新增 aligned informative horizon 增强；新增 low/conflict informative horizon 可能削弱。结论不是“更大的 K 更好”。

### 2.4 有限步效率候选命题

有限步效率需要每步 margin 增长下界：

$$
M_K(t+1)\ge M_K(t)+\eta g_K-\eta^2B-\epsilon_t.
$$

若：

$$
\eta g_K-\eta^2B-\bar\epsilon>0,
$$

则：

$$
T_\gamma(K)
\le
\left\lceil
\frac{\gamma-M_K(0)}{\eta g_K-\eta^2B-\bar\epsilon}
\right\rceil.
$$

这里 $g_K$ 不是已经免费得到的常数；它需要 velocity persistence 证明或实验下界。$\epsilon_t$ 也不是零；全位置训练中的 shared / indirect loss 必须作为扰动界定。

## 3. 主要结果

### 结果 1：A11 已经证明受控表示保证。

如果 $K$ 覆盖 $Y_\tau=S_Z$，且 $S_Z$ 一一编码 $Z$，低 $Y_\tau$ loss 会推出 $h_T$ 含有 $Z$。

**证据说明：**

- 理论公式：$\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon\Rightarrow I(h_T;Z)\ge H(Z)-\varepsilon$。
- K=2 和 $\tau=3$ 受控构造都支持：覆盖有信息 horizon 后，当前 $h_T$ 受到直接语义约束。

**边界：** 表示保证不说明训练更快。

### 结果 2：A11 已经证明并验证一阶语义速度机制。

在分支折叠、固定输出方向的一阶模型中，覆盖有信息 horizon 给 $h_T$ 正的读出有效语义速度；非覆盖共享目标没有该一阶方向。

**证据说明：**

- 理论公式：K=2 时 $G_1^{margin}=0$，$G_2^{margin}=\frac{\lambda_2}{m^2}\sum_z\|u_z-\bar u\|^2>0$。
- A11_06 在 $\tau=3$ 中验证：K3 的 $G_M^{hidden}=0.003816$，K1/K2 近 0。
- A11_07 进一步显示 direct 条件 native H3 和 $M_Z^{ref}$ 强，indirect-only 条件即使 $Q$ 非平凡，也没有同样的 native direct prediction。

**边界：** 一阶速度不是有限步效率定理。

### 结果 3：A11 已经验证 general K 不是越大越好。

general K 的一阶速度由有信息 horizon 的中心化输出方向向量和决定；新增 horizon 可能增强，也可能削弱。

**证据说明：**

- A11_08：同样 K=4、同样两个有信息 horizon 下，aligned 的 $G_{hidden}=0.015262$，low/conflict 的 $G_{hidden}=0.000954$。
- A11_08b：frozen heads 下 aligned 仍有更高早期 $G_{hidden}^{ref}$，说明方向机制不是单纯 step-0 artifact。
- A11_09：K2 近 0，K3 打开，shared H4 无增量，aligned H4 增强，low/conflict H4 削弱。

**边界：** 这不证明自然语言 future token 方向天然对齐。

### 结果 4：A11 当前还没有证明有限步效率定理。

当前不能从 $G_K^{hidden}>0$ 直接推出 $T_\gamma(K)$ 更小。

**证据说明：**

- A11_06 / A11_08 / A11_09 主要支持一阶或早期 velocity 机制。
- A11_08b 已显示 trainable output heads 会漂移。
- A11_07 已显示 all-position indirect transfer 可以让 $Q$ 非平凡，因此 shared / indirect loss 不能被忽略。

**边界：** 有限步定理必须先补齐可检验优化假设。

## 4. A11_10 最小协议

A11_10 不测试“再证明 K3 更强”。它只测试有限步定理需要的四个假设。

| 假设 | 指标表达式 | 测什么 | 为什么必要 | 支持 | falsify | insufficient evidence |
|---|---|---|---|---|---|---|
| velocity persistence | $G_K^{ref}(t)=m^{-1}\sum_z v_z^{ref\top}(-\nabla_{h_z}L_K)$ | 语义速度是否在早期窗口保持正下界 | 提供 $g_K$ | $G_K^{ref}(t)>0$ in `4/5` seeds | 阈值前变 0 或负 | 梯度噪声或 step-0 饱和 |
| margin-to-recovery calibration | $M_K(t)\ge\gamma\Rightarrow H3(t)\ge0.9$ 或 $Q(t)\ge0.9$ | margin 是否预测 native recovery | 把 margin hitting time 转成语义恢复 | margin 阈值领先或同步 recovery | margin 与 recovery 脱钩 | 两者都不跨阈值 |
| head drift bound | $c_u(t)=\frac{\sum_z v_z^{ref\top}v_z^{cur}(t)}{(\sum_z\|v_z^{ref}\|^2)^{1/2}(\sum_z\|v_z^{cur}(t)\|^2)^{1/2}+\epsilon}$ | reference direction 是否仍有效 | 防止输出头漂移破坏定理方向 | $c_u(t)$ 保持正相关 | $c_u(t)$ 过零或翻转 | 需要 current-geometry theorem |
| shared / indirect perturbation bound | $P_{non-direct}(t)=m^{-1}\sum_z v_z^{ref\top}(-\nabla_{h_z}L_{non-direct})$ | 非直接 loss 是否可界定 | 全位置训练不能忽略 indirect path | 负向扰动有下界且净增量正 | perturbation 大于 direct term | 梯度分解不可用 |

协议条件只包含：decision-only frozen-head theorem-window 条件、最小 trainable-head drift audit、clean $\tau=3$ all-position perturbation audit。无 K 大扫参、无 loss-weight sweep、无 architecture sweep、无 MoE bridge。

## 5. 执行动作

下一步只做：

```text
daily_research_reports/0710/mtp_long_horizon_semantic_efficiency_theory_closure/protocols/A11_10_finite_step_semantic_efficiency_protocol.md
```

完成标准不是“曲线更好看”，而是把四个有限步定理假设分别判定为 supported / falsified / insufficient evidence。

## 6. 来源索引

**当前 0710 包：**

- `daily_research_reports/0710/mtp_long_horizon_semantic_efficiency_theory_closure/story_cn.md`
- `daily_research_reports/0710/mtp_long_horizon_semantic_efficiency_theory_closure/anchors/11_10_finite_step_semantic_efficiency_anchor.md`
- `daily_research_reports/0710/mtp_long_horizon_semantic_efficiency_theory_closure/protocols/A11_10_finite_step_semantic_efficiency_protocol.md`

**读取的 sync source：**

- `sync/S000_current_specialization/stories/11_long_horizon_mtp_objective/story_cn.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_06_readout_effective_margin_efficiency_anchor.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_07_no_leakage_all_position_efficiency_anchor.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_08_general_k_readout_margin_dynamics_anchor.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_08b_output_geometry_dynamics_audit_anchor.md`
- `sync/S000_current_specialization/anchors/11_long_horizon_mtp_objective/11_09_next_k_inclusion_law_anchor.md`

## 7. 两句导师汇报版本

A11 现在已经证明并验证：MTP 的受控优势不是“预测更多 token”，而是当 $K$ 覆盖第一个含 $Z$ 的未来位置时，当前 $h_T$ 获得直接读出有效语义速度；general K 的速度由有信息 horizon 的中心化输出方向向量和决定，所以不是 $K$ 越大越好。

当前唯一缺口是有限步效率：还没有证明 $G_K^{hidden}>0$ 必然推出更小 $T_\gamma$；下一步 A11_10 只验证 velocity persistence、margin-to-recovery calibration、head drift 和 shared / indirect perturbation bound，不进入 MoE bridge。