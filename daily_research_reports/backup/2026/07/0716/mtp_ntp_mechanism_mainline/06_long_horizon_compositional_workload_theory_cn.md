# Long-horizon compositional workload：任务属性、credit path 与标准头使用

日期：2026-07-16

状态：AI 理论澄清工作稿；不是研究者判断、正式 story、anchor 或 Protocol。

英文 companion：
[06_long_horizon_compositional_workload_theory.md](06_long_horizon_compositional_workload_theory.md)

## 1. 一句话结论

> **真正可能让 MTP 优于 all-position NTP 的，不是 token 距离本身，而是：
> 早期证据对答案具有不可绕过的反事实作用，多个局部不足证据必须经状态 relay
> 组合，NTP 的稍后 credit path 在给定 learner 与预算下发生衰减、噪声或冲突，
> 同时 MTP 的提前信息梯度能够形成、运输并被标准 next-token 主头因果使用。**

因此，“MTP 必要”不能是仅由数据分布决定的信息论结论。all-position NTP
最终也监督答案 token；MTP 最多在明确的模型、初始化、训练预算和接口下具有
**有限优化优势**。

## 2. 从导师录音得到的问题链

排序依据是因果依赖：前一问未关闭，后一问就不能成为机制结论。

### 第一问：next-one 与 next-two 的因果差异是什么？

导师在 0706 提出“早期信息影响很晚答案”的 long-horizon 直觉，并要求把
next-two 相对 next-one 的优势数学化。0713 科研指导进一步纠正：短任务也能
出现 next-one/next-two 差异，因此必须先解释训练目标的差异，再谈长程 workload。

已有 A11_01 直接结果只支持：

> 在同一个较早隐藏状态上，当预测 horizon 首次覆盖一个 informative target
> 时，MTP 增加一条 NTP 在该状态没有的直接一阶梯度；新增 horizon 是否有用
> 取决于信息包含与方向对齐，而不是 $K$ 的数值本身。

这不是“next-two 总比 next-one 好”。

### 第二问：为什么 formation 不推出标准头 use？

A11_02 已证明受控条件下 direct path 可到达共享参数；但 all-position background
有正有负，seed 973 中正 direct path 被负 background 反转。

A11_03 进一步显示：

- exact source K/V 在所有目标和 seed 下都可完美线性读取 branch；
- informative-MTP 相比 matched shared-aux 没有注册的额外可读性；
- 强标准头 answer-control 增量失败，均值为 `0.01675`，`0/5` 达到 `0.10`。

因此：

```text
direct signal
-> shared-parameter reachability
-> state formation
-> state transport
-> standard-head causal use
-> final task benefit
```

是六个不同 gate。

### 第三问：为什么代码/规划可能更需要这种机制？

0713 导师讨论给出的“决策树、多个局部步骤、深层逻辑、代码比普通文本更
结构化”是**机制直觉**，不是已证明事实。

较精确的候选解释应当是：

- 代码更常出现确定性的 delayed dependence，例如定义—使用、作用域、类型、
  控制流和跨函数契约；
- 正确补全经常需要组合多个单独不足的约束；
- 给定程序状态后，合法未来往往比开放文本更集中，因此 future target 可能是
  较低噪声的状态监督；
- 错误通常是离散且脆弱的，丢失一个早期约束即可改变最终 token。

普通自然语言经常具有更强局部可预测性、更多等价续写和更高条件熵，使远期 token
可能成为 noisy auxiliary target。但证明、规划、长程指代也可以具有与代码相同
的属性；模板代码、样板语法和局部补全也可以完全不需要它们。

所以候选答案是：

> **可能有利于 MTP 的是“确定性的延迟反事实依赖 + 多证据状态组合 +
> 可监督 relay”，而不是 `code` 这个模态标签。**

数据重复、tokenization、exact-match 指标、训练算力或局部模板差异仍是活着的
rival explanation。

### 第四问：如何连接到 MoE？

导师提出“更可拆分的表征最终让不同频率/类型特征进入不同 expert”是项目动机。
当前还缺两座桥：

1. MTP 是否真的形成并让标准头使用任务必要的状态；
2. 该状态是否预测 held-out conditional expert utility。

可读性、各向异性、聚类或 route NMI 都不能替代 expert utility。A06 仍然拥有
最终 Router 判据，本轮不设计 Router。

## 3. Long-horizon 的操作定义

### 3.1 建议总定义

给定局部窗口宽度 $w$ 和标准 next-token 主头，一个
**functional long-horizon compositional workload** 是指：

> 存在距离答案超过 $w$ 的早期语义证据；保持答案附近窗口不变而反事实改变该
> 证据会改变正确答案；至少两个单独不足的证据必须经有序状态更新联合决定答案；
> 语义等价改写不改变答案；模型的标准头只有在 relay 被保留时才能完成任务。

这是相对于 $(w,\text{data distribution},\text{learner},\text{interface})$
的定义，不是序列的绝对属性。

### 3.2 七个必须分开的对象

| 对象 | 具体定义或计算 | 逻辑地位 |
| --- | --- | --- |
| token distance | $D=\operatorname{pos}(Y)-\operatorname{pos}(E_0)$ | 只描述几何距离；既不充分，也不是 next-one/next-two 机制的必要条件 |
| local-window insufficiency | 存在 $W_w(x)=W_w(x')$ 但 $Y(x)\neq Y(x')$ 的 collision；等价地局部 Bayes risk 非零 | “非局部”主张的必要条件 |
| delayed counterfactual dependence | 固定其他证据和 local window，$Y(do(E_0=e))\neq Y(do(E_0=e'))$ | “早期证据必要”的必要条件 |
| paraphrase invariance | 对保持潜在语义的变换 $\tau$，$Y(\tau(E_0),E_{1:L})=Y(E_0,E_{1:L})$ | 语义/generalization 主张的必要 guard；一般长距任务本身不必满足 |
| multi-evidence compositional necessity | 每个单一证据都不足，而联合证据确定答案；并且改变任一必要证据可改变答案 | “compositional”主张的必要条件 |
| state transport | 对中间状态/relay 的 matched patch 或 ablation 会改变后续状态或最终正确答案概率 | 标准头利用早期证据的必要机制 |
| standard-head causal use | 干预 intended relay 会改变普通 $q_1$ 的答案 loss/output，且不存在 bypass | “训练信息被普通头使用”的必要条件 |

还需要一个独立的 **informative-horizon condition**。令 $B_t$ 表示排除被研究
证据 $E_j$（或其潜变量 $Z_j$）后的 nuisance context，则要求：

$$
I\!\left(
Z_j;X_{t+k}
\mid B_t,X_{t+1:t+k-1}
\right)>0.
$$

它是“第 $k$ 个 MTP target 在当前状态增加信息特异 direct credit”的必要条件；
它不保证 transport、use 或最终收益。不能在 $Z_j$ 是完整 prefix 的确定函数时
再把完整 $X_{\leq t}$ 放入条件，否则 mutual information 会被定义性地消掉。

## 4. 最小数学模型

### 4.1 任务层

令 $E_0,\ldots,E_L$ 是分散证据，理想语义状态满足：

$$
z_0=\phi(E_0),
\qquad
z_{j+1}=F_j(z_j,E_{j+1}),
\qquad
Y=G(z_L).
$$

模型的 carrier 为：

$$
s_0=\operatorname{encode}_\theta(x_{\mathrm{early}}),
\qquad
s_{j+1}=f_{\theta,j}(s_j,x_j),
\qquad
p_\theta(Y)=q_1(s_L).
$$

若主张 multi-evidence composition，在确定性任务中至少要求：

$$
H(Y\mid W_w,E_i)>0
\quad\text{for every single }E_i,
$$

同时：

$$
H(Y\mid W_w,E_0,\ldots,E_L)=0.
$$

还要有 counterfactual witness：固定其余证据时，至少一个必要 $E_i$ 的变化会
改变 $Y$。

一个候选最小抽象任务是每个样本重新抽取状态更新规则：

$$
z_1=F_{a}(q),
\qquad
Y=G_{b}(z_1),
$$

其中早期证据给出 $a$，中间证据给出 $b$，末端给出 query $q$，答案窗口不包含
$a$ 或 $b$。单独 $(a,q)$ 或 $(b,q)$ 都不足。规则必须跨样本更新或重组，不能
退化为固定 pair/table lookup。

这只是 carrier 的数学形状，不是已批准的数据实现。

### 4.2 明确禁止的 shortcut

- answer token、branch label 或答案 alias 在 intended path 外直接出现；
- 完整双射表删一行后通过“唯一未使用值”消元；
- 最后 $w$ 个 token 单独决定答案；
- 小型固定 pair/table 可由训练集记忆；
- auxiliary head 可以单独完成任务，而普通 $q_1$ 无需 early state；
- generator rejection rule、位置、长度或 token frequency 泄露答案。

### 4.3 all-position NTP 与 MTP

对 token 序列 $X_{1:T}$ 和隐藏状态 $h_t$：

$$
\mathcal L_{\mathrm{NTP}}
=
\mathbb E\sum_{t=1}^{T-1}
\ell\!\left(q_1(h_t),X_{t+1}\right).
$$

$$
\mathcal L_{\mathrm{MTP},K}
=
\mathbb E\sum_{t=1}^{T-1}
\sum_{k=1}^{\min(K,T-t)}
\lambda_k
\ell\!\left(q_k(h_t),X_{t+k}\right).
$$

all-position NTP 在 $t+k-1$ 位置也会看到 $X_{t+k}$。真正差别是：

- MTP 从较早状态 $h_t$ 直接预测 $X_{t+k}$；
- NTP 从较晚状态 $h_{t+k-1}$ 直接预测同一 token；
- 若要让该晚期损失训练较早状态，credit 必须穿过中间状态转移。

### 4.4 两条 credit path

令：

$$
J_{t\rightarrow t+k-1}
=
\frac{\partial h_{t+k-1}}{\partial h_t}.
$$

NTP 对较早状态的 later/indirect credit 是：

$$
g^{\mathrm{NTP}}_{t,k}
=
J_{t\rightarrow t+k-1}^{\top}
\nabla_{h_{t+k-1}}
\ell(q_1(h_{t+k-1}),X_{t+k}).
$$

MTP 的 early/direct credit 是：

$$
g^{\mathrm{MTP}}_{t,k}
=
\nabla_{h_t}
\ell(q_k(h_t),X_{t+k}).
$$

需要比较四件事：

1. **长度：**NTP state path 有 $k-1$ 个 transition；MTP head-to-state path
   在 $h_t$ 处是直接的。
2. **Jacobian 乘积：**若
   $\|J_{t\rightarrow t+k-1}\|$ 收缩，later credit 会衰减；若接近 identity
   或有稳定 residual path，这一优势消失；若放大，还可能反过来。
3. **噪声：**沿任务有用方向 $u$ 可定义：

   $$
   \operatorname{SNR}_u(g)
   =
   \frac{\mathbb E\langle u,g\rangle}
   {\sqrt{\operatorname{Var}(\langle u,g\rangle)+\epsilon}}.
   $$

   远期 target 也可能条件熵更高，使 MTP direct gradient 更 noisy。
4. **冲突：**MTP 的其他 horizon gradient 可能与必要状态或标准头 risk
   负对齐；A11_02 的 seed 973 已给出“direct positive、total negative”的受控
   实例。

对于 $L\gg K$ 的真正长链，MTP 并不会从 $s_0$ 直接预测最终 $Y$。它只能在每个
局部边界提供 lookahead credit。要产生长链优势，多个 direct credits 必须共同
教会一条可运输的 state-update rule；只在第一个位置形成信息仍不够。

## 5. 有边界的理论结果

### Assumptions

1. NTP 与 MTP 使用同一数据、共享 backbone 和普通 $q_1$ 评价接口。
2. 主 NTP loss 的系数保持一致；信息特异结论最终需要 matched shared-aux
   排除 head 数量和 loss 数量。
3. 局部分析点可微；需要一步比较时，标准头风险二阶可微且余项有界。
4. 任务存在由第 3 节定义的 early evidence、joint composition 和 intended
   relay。
5. “更有效”只指给定 learner、初始化、算力/训练 token 预算下的优化或标准头
   loss，不指无约束 Bayes 最优。

### Proposition 1：不存在仅由距离推出的 MTP 信息论必要性

若模型族能表示真实 next-token 条件分布、all-position NTP 达到总体
cross-entropy 的全局最优，并且最终答案 $Y=X_T$ 可由 $X_{<T}$ 识别，则 NTP
在 $T-1$ 的 Bayes-optimal standard head 已能实现最优 $Y$ 风险。此时增加 MTP
目标不能把该 Bayes 风险降得更低。

**证明。**cross-entropy 是严格 proper scoring rule。all-position NTP 的
$T-1$ 项在总体最优处恢复 $P(X_T\mid X_{<T})$；任何额外辅助项都不能优于真实
条件分布在同一 standard-head 评价上的风险。$\square$

所以 MTP 优势只能来自有限容量、有限数据、有限步数、优化路径、正则化或表示
选择，而不能来自“NTP 永远没见过答案”。

### Proposition 2：提前 direct credit 更强的局部充分条件

令 $R_j(s_j)$ 衡量 carrier state 对必要语义状态 $z_j$ 的误差，
$u_j=\nabla_{s_j}R_j$。训练梯度 $g$ 对 carrier 的一阶帮助量为
$\langle u_j,g\rangle$。

假设：

1. informative MTP direct gradient $d_j$ 满足
   $\mathbb E\langle u_j,d_j\rangle\geq\alpha>0$；
2. NTP later-target gradient 范数至多为 $B$；
3. 每个中间 transition Jacobian operator norm 至多为 $\rho<1$；
4. 其他 MTP horizons 对 $u_j$ 的总负对齐绝对值至多为 $c$；
5. 把 state gradient pull back 到共享参数后，direct path 非零且上述正对齐
   不被反转。

则长度为 $k-1$ 的 NTP later credit 有：

$$
\left|
\mathbb E\langle u_j,g^{\mathrm{NTP}}_{j,k}\rangle
\right|
\leq
\|u_j\|B\rho^{k-1}.
$$

若：

$$
\lambda_k\alpha-c
>
\|u_j\|B\rho^{k-1},
$$

则 MTP 新增 credit 在该局部模型中比 NTP 的 later credit 提供更大的
carrier-aligned 驱动力。

**证明。**对 NTP 项使用 Cauchy–Schwarz 和 Jacobian norm 的次乘性；对 MTP
新增项使用假设 1，并减去最坏 background conflict $c$。$\square$

边界：这只证明 formation credit 更强，不证明 $s_j$ 被运输或普通头使用。

### Proposition 3：标准头局部受益条件

令 $R_{\mathrm{std}}(\theta)$ 是普通 $q_1$ 在 carrier 答案上的评价风险；
$G_S$ 是 matched shared-aux 梯度，$G_I$ 是 informative-MTP 梯度，并定义：

$$
\Delta g_{\mathrm{info}}=G_I-G_S.
$$

在同一参数点作局部二阶展开：

$$
R_{\mathrm{std}}(\theta-\eta G_I)
-
R_{\mathrm{std}}(\theta-\eta G_S)
$$

$$
=
-\eta
\left\langle
\nabla R_{\mathrm{std}},
\Delta g_{\mathrm{info}}
\right\rangle
+\frac{\eta^2}{2}
\left(
2G_S^\top H_{\mathrm{std}}\Delta g_{\mathrm{info}}
+
\Delta g_{\mathrm{info}}^\top
H_{\mathrm{std}}
\Delta g_{\mathrm{info}}
\right)
+O(\eta^3).
$$

因此，对充分小的 $\eta$，信息特异 MTP 优势至少要求：

$$
\left\langle
\nabla R_{\mathrm{std}},
\Delta g_{\mathrm{info}}
\right\rangle>0.
$$

有限步长下，这个正一阶项还必须超过曲率代价。若 formation 存在但上式为零，
则不能声称标准头局部受益。

### MTP 与 NTP 等价的反例

令中间 transition 是 identity，$h_{t+k-1}=h_t$，两个 head 绑定为同一线性
readout，且没有其他 background loss。NTP 在较晚位置预测 $X_{t+k}$ 与 MTP
在较早位置预测它产生同一梯度，最多相差 loss 权重；重标学习率后轨迹等价。

所以 token distance 大并不自动产生 credit advantage。

### MTP 更差的冲突反例

令标准头风险：

$$
R_{\mathrm{std}}(\theta)
=\frac12(\theta-1)^2,
$$

NTP gradient 在 $\theta=0$ 为 $-1$。令 auxiliary future loss 为：

$$
L_{\mathrm{aux}}(\theta)
=\frac12(\theta+1)^2,
$$

其 gradient 为 $+1$。当 auxiliary 权重大于主项时，MTP 总更新将 $\theta$
推向负方向，标准头风险上升。future target 存在且有梯度，不代表它与最终
标准头任务一致。

### Formation 不推出 transport/use 的反例

令 $s_0=Z$，因此 auxiliary head 可从 $s_0$ 完美读取 $Z$；但令
$s_1=f(s_0,x_1)=0$，标准头 $q_1(s_1)$ 与 $Z$ 无关。此时 formation 完美，
transport 和 use 都为零。

另一类反例是 final local token 直接编码 $Y$：即使 early state 存在，标准头
也会走 bypass，因此删除 relay 不影响答案。

### 优势消失的条件

MTP 的候选优势会在以下任一情况下消失：

- future target 对必要状态没有条件新增信息；
- local window 或 bypass 已足够完成答案；
- NTP later path 的 Jacobian 近 identity、SNR 高且无冲突；
- MTP direct gradient 只监督 nuisance 或与标准头 risk 正交；
- auxiliary gradients 相互冲突或其高条件熵带来更大噪声；
- early state 形成但没有 transport，或普通头不使用；
- shared-aux/NTP 已饱和，指标没有动态范围；
- 无限容量、无限数据和全局最优使两者达到同一 Bayes risk。

### Claim boundary

上述命题不能推出：

- 一般 Transformer 的 Jacobian 必然收缩；
- 真实代码一定比自然语言更 compositional；
- MTP 在代码 benchmark 上的优势由本机制导致；
- 更大的 $K$、更长 context 或更多 heads 必然更好；
- linear readability 等于 state transport 或 standard-head causal use；
- 更可拆分的表征必然产生有用 MoE experts；
- A12 E04 的失败证明 NTP 或 MTP 无法组合。

## 6. Carrier validation gate

这里的 carrier 是 **data distribution + learner scale + relay interface +
evaluation head**，不是只有一份数据。

阈值尚未冻结；以下只定义计算对象及 pass/fail/insufficient 的语义。

其中 1–4、6、9 主要审计数据/生成规则；5、7、8 必须连同 learner、checkpoint
和标准头接口一起审计。只验证前一组不能宣布 carrier 已经有效。

| Gate | 计算对象 | Pass | Fail | Insufficient |
| --- | --- | --- | --- | --- |
| 1. local window 信息不足 | 对最后 $w$ tokens 建 collision pairs；计算 local-only Bayes/oracle accuracy 与 full-evidence oracle accuracy | 相同 $W_w$ 存在不同答案，local oracle 明显低于 mastery，而 full oracle 可解 | $W_w$ 唯一决定答案，或强 local baseline 已解决 | collision 覆盖不足、oracle 太弱或 $w$ 未冻结 |
| 2. early evidence 反事实必要 | 固定其余 tokens/latent variables，只替换 $E_0$；计算正确答案变化率 | intended pairs 中替换 $E_0$ 稳定改变 $Y$ | $Y$ 不变，或替换同时改变其他因素 | 干预不是 matched，或 ground-truth generator 未审计 |
| 3. paraphrase invariance | 对语义保持变换 $\tau$ 计算 answer consistency，并审计模板/token identity | 语义等价改写保持 $Y$，且表面模板不预测答案 | 改写改变 ground truth，或模板直接泄露 label | paraphrase 的语义等价性无法验证 |
| 4. 多证据组合必要 | joint oracle、每个 single-evidence oracle、evidence deletion/counterfactual | joint 可解；每个单证据不足；破坏任一必要证据可改变答案 | 任一单证据、位置或频率已决定答案 | oracle 不够强，或只测相关性未测必要性 |
| 5. relay 对标准头必要 | 在 capability-matched 模型中，对 intended relay 做 clean/ablate/patch；测普通 $q_1$ answer loss 或 accuracy 变化，并有 self/positive controls | clean 可解；破坏 relay 使标准头显著失败；matched 恢复可救回 | relay ablation 不影响标准头，说明 bypass 或非使用 | 模型本身不会做、patch 无效、controls 失败 |
| 6. 无直接答案 bypass | 枚举 intended path 外字段；做 generator proof、masked-view oracle 与 answer/branch-token 搜索 | 除 intended evidence/relay 外不存在确定答案路径 | answer、branch label、alias、local clue 或 rejection rule 可直接预测 | 生成器约束或 masked oracle 未覆盖所有路径 |
| 7. NTP 至少有可学习尺度 | NTP-only 标准头 learning curve、跨 seed final-window mastery 与 floor/ceiling | 至少一个预定 scale 稳定学会 carrier，且不是瞬时峰值 | 所有 scale 都在 floor 或 seed 不稳定 | 训练预算、seed、实现或阈值不足以判定 |
| 8. matched shared-aux 未饱和 | 在同一标准头指标上测 shared-aux 的 floor/ceiling 距离和 checkpoint 动态范围 | baseline 已有能力但仍留有预注册改善空间 | 已 ceiling，或完全在 floor，无法比较增量 | ceiling/floor 与选点规则未冻结 |
| 9. 非固定表记忆/消元 | held-out rule/map recombination；构造缺失证据后的所有一致 completion | test 需要 unseen recombination；缺失证据至少有两个一致世界给出不同 $Y$ | 训练表 lookup 可解，或像 bijection 一样由唯一未用值完成 | solver 未穷尽 completion，或 split 仍复用固定 pair |

九项是串行 validity gate，不是九个并列成功指标。任一关键 gate `fail` 都阻止
NTP/MTP 目标比较；`insufficient` 也不能当作 pass。

现有证据的判定是：

- A11 的 carrier 有 direct `BR_z` bypass 且 shared-aux/decoding 饱和；
- A12 E04 没有任何 NTP-eligible scale，且 row-removal 被 bijection elimination
  破坏；
- 因而当前不存在已经通过上述 gate 的 carrier。

## 7. Exactly one next decision

> **先冻结 long-horizon/compositional 的操作定义与九项 carrier validity
> test；现有证据不足以直接进入 NTP/MTP Protocol。**

下一步的人类审批入口是
[Thinking Card](07_long_horizon_compositional_workload_thinking_card_cn.md)。
在研究者填写并明确批准前，不创建正式 anchor、Protocol、实现或实验，不更新
graph、sync，不 commit 或 push。

## 8. Source map

- [0706 MTP 录音](../../0706/recordings/mtp.md)
- [0713 科研指导](../../0713/recordings/0713_科研指导_整理稿.md)
- [0713 导师与学长讨论](../../0713/recordings/0713_导师与学长讨论_整理稿.md)
- [A11 current story](../../../../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md)
- [A11_01 inclusion law](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md)
- [A11_02 all-position path decomposition](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md)
- [A11_03 K/V causal use](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)
- [A11_03 source information](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md)
- [A12 E04 carrier failure](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md)
