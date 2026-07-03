# 01 公共算子机制闭环总结报告

## 从“公共方向（common direction）”到“机制索引的公共算子（common operator）”

## 摘要

这条线问的是一个很窄的问题：当我们说“混合专家模型”
（mixture-of-experts, MoE）的路由器或专家里有“公共成分”
（common component）时，我们到底在估计什么对象？

我们已经建立的结论：

```text
common 不是一个通用 hidden-state 方向。
common 是一族由机制判据索引的算子。
```

实验显示：

```text
在受控机制中，高方差方向估计（activation PCA）、组均值（group mean）、
梯度交集（gradient intersection）和反馈漂移（feedback drift）会在各自
匹配的判据下胜出。
在真实文本训练审计（real-DCLM）中，路由打分漂移（gate-logit drift）
可以复现 A06 的代理路由坍缩（proxy-route collapse），但简单低秩
gate-logit common 不能解释或救回这个 collapse。
```

下一步不是马上做方法，而是先拆开真实 collapse 的来源：

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

下一步实验必须判断真实 collapse 主要来自 gate-weight drift、hidden-state
drift，还是它们的交互。

阅读路径：第 1-5 节解释机制问题和数学上的不可辨识性；第 6-9 节解释受控
证据、真实负结果和下一步决策；第 10 节和附录提供审计链。

## 术语解释

| 术语 | 中文含义 | 具体对象 / 计算 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 混合专家模型（MoE） | 用路由器把 token 状态分给一个或多个专家的架构。 | 本线中路由器用 hidden state $h$ 和 gate weights $W$ 计算 $z=Wh$。 | common 问题发生在 router 或 expert 反复学习相同结构时。 | MoE routing 本身不能证明专家专业化或有效性。 |
| 公共成分（common component） | 在某个判据下跨 group、token 或训练更新共享的结构。 | 可以是 activation 方向、均值偏移、gradient 方向或 checkpoint drift。 | 本线要回答的就是“哪个对象才应该叫 common”。 | common 不必然有害、可删除或全局唯一。 |
| 公共算子 / 投影算子（common operator/projector $P$） | 用来选择、删除或 replay 候选 common 子空间的线性算子。 | residualization 用 $(I-P)h$；feedback replay 用 $P\Delta h$。 | 它把“common”从直觉变成可测试对象。 | 一个判据下好的 $P$ 不保证在另一个判据下也好。 |
| 残差成分（residual component） | 删除候选 common 后剩下的部分。 | 静态状态中是 $(I-P)h$，drift 中是 $(I-P)\Delta h$。 | 用来判断被删除部分是否承载目标机制。 | residual 不等于 unique，除非判据能证明。 |
| 激活主成分分析（activation PCA） | 寻找 hidden state 中高方差方向的方法。 | hidden-state covariance 的 top eigenvectors。 | 它是“common direction”的自然基线。 | 高方差不等于 shared function 或冗余 gradient。 |
| 梯度交集（gradient intersection） | 寻找跨 group 共享 gradient 方向的方法。 | 删除候选方向后，看 pairwise group-gradient cosine 降低多少。 | 在受控 mismatch regime 中，它估计 optimization common。 | 它不识别真实 feedback drift 或 expert utility。 |
| 反馈漂移（feedback drift） | 训练过程中可能覆盖 routing 的变化。 | hidden drift 是 $\Delta h=h_t-h_0$；logit drift 是 $\Delta z=z_t-z_0$。 | 它连接 common estimation 和 early-training preservation failure。 | aggregate drift 不能单独分离 gate-weight drift 和 hidden-state drift。 |
| 路由打分（gate logit） | top-1 expert 选择前的 router score。 | $z_t=W_t h_t$。 | 真实 DCLM bridge 检查 logit drift 是否复现 route collapse。 | logit 证据本身不说明 hidden state 因果来源。 |
| 代理路由归一化互信息（proxy-route NMI） | proxy label 和 top-1 expert assignment 的一致性。 | NMI 范围是 0 到 1；越高表示 routing 越接近 proxy partition。 | 它是 A06/A01_04 real-DCLM bridge 的 preservation 指标。 | 它不能证明语义专家或语言模型收益。 |
| 解释比例（explain fraction） | 候选 drift 能复现 full collapse 的比例。 | feedback-only replay 的 NMI drop 除以 full NMI drop。 | 判断候选 common 是否足以造成 collapse。 | 如果 random subspace 也高，就不是特异机制证据。 |
| 救回比例（rescue fraction） | 删除候选 drift 后能救回 collapse 的比例。 | 比较 residual-only NMI、full-drift NMI 和 step-0 NMI。 | 判断删除候选部分是否恢复 routing。 | 它不保证训练 loss 不退化，也不证明 expert utility。 |
| 真实 DCLM 桥接审计（real-DCLM bridge） | 在真实文本训练 artifact 上 replay router logits 的审计。 | 使用 DCLM-bin、6-layer Qwen3-MoE toy、raw-center router、seeds 0/1/2、layers 3/4/5、checkpoints 0/5/10。 | 检查受控 feedback 结论能否进入真实训练。 | 它不覆盖所有层、尺度、数据集或干预。 |
| 低秩（low rank） | 用小维子空间解释 common 机制。 | real bridge 先测 rank-1 logit drift，再扫更高 rank。 | 如果低秩成功，就说明简单 projector target 可能成立。 | 高 rank 重构可能不特异，因为 random subspace 也会改善。 |

## 1. 动机

专家专业化（specialization）项目反复看到公共成分会支配专业化：

- 公共偏移（common offset）会变成特定专家的路由偏置；
- 公共路由打分（common logit）会导致 top-1 routing collapse；
- 早期训练（early training）会抹掉 step-0 proxy route；
- 公共/稀有梯度重叠（common/rare gradient overlap）会干扰 specialization。

一个自然但危险的捷径是：把隐藏状态最高奇异方向（top hidden-state
singular direction）、批均值（batch mean）、序列均值（sequence mean）或
路由打分对比（route-logit contrast）直接叫做 “the common direction”。这个捷径不安全。
common 可能指 activation 方差、shared prediction function、冗余梯度更新，
也可能指训练 feedback drift。

01 线的目的就是在设计公共分支（common branch）、残差化路由器
（residualized router）或 unique-expert input split 之前，把这个歧义拆开。

## 2. 必须区分的对象

| 名称 | 具体含义 | 常见 estimator | 混淆后的风险 |
|---|---|---|---|
| 激活公共成分（activation common） | 高方差共享 activation 结构 | activation PCA | 会选到高方差 unique 或 nuisance 方向 |
| 功能公共成分（functional common） | shared prediction 需要的成分 | 遮掉 $Ph$ 后的 loss | 可能是有用结构，不能一概删除 |
| 优化公共成分（optimization common） | 造成跨 group 冗余更新的成分 | gradient intersection | 可能在 activation covariance 中不可见 |
| 反馈公共成分（feedback common） | 覆盖 routing 的 checkpoint drift | drift replay/removal | 是动态对象，不一定在 step-0 静态几何中可见 |

这是导师式文档的核心写法：先区分容易混淆的概念，再给干净基线或不可能性，
然后用受控证据和真实证据逐层推进。

## 3. 干净的不可能性结果

令模型输出是 shared branch 和 routed branch 的和：

$$
F_g(h)=S(h)+R_g(h).
$$

对任意 common 成分函数 $\Delta(c)$，定义：

$$
S'(h)=S(h)+\Delta(c),\qquad R'_g(h)=R_g(h)-\Delta(c).
$$

则：

$$
S'(h)+R'_g(h)=S(h)+R_g(h)=F_g(h).
$$

所以只看 $F_g(h)$ 的 loss，不能识别 $\Delta(c)$ 属于 shared branch 还是
routed branch。

这是故事的第一个锚点：加 common branch 不能保证它学到 common，也不能保证
unique experts 不学 common。必须有额外机制判据。

## 4. 机制模型

使用 hidden-state 分解：

$$
h=c+u_g+\epsilon,
$$

其中 $c$ 是共享结构，$u_g$ 是 group-specific 结构，$\epsilon$ 是未建模结构。
候选 operator $P$ 只有相对于判据才有意义。

三个静态判据是：

$$
\operatorname{Var}_g(\mathbb{E}[Ph\mid g])
\quad\text{用于跨 group 稳定性,}
$$

$$
\Delta L_c(P)=L_c((I-P)h)-L_c(h)
\quad\text{用于 shared-prediction 因果性,}
$$

以及

$$
\Delta C(P)=
\mathbb{E}_{g\neq g'}\cos(G_g,G_{g'})
-
\mathbb{E}_{g\neq g'}\cos(G_g^r(P),G_{g'}^r(P))
$$

用于梯度冗余性，其中：

$$
G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g].
$$

动态判据是 feedback replay/removal。若 $\Delta h=h_t-h_0$，
$P_{\mathrm{fb}}$ 只有在 replay $P_{\mathrm{fb}}\Delta h$ 能复现 collapse、
remove 后能 rescue routing 时才是相关 feedback common。

## 5. 命题与证明

### 命题 1：激活公共成分（activation common）和梯度公共成分（gradient common）可以分离

令 $a,b$ 正交归一。令 $z_a,z_b$ 是不相关、单位方差的标量，且
$\epsilon$ 是方差小于两个信号项的各向同性噪声。定义：

$$
h=s_a a z_a+s_b b z_b+\epsilon,\qquad s_b^2>s_a^2.
$$

此时 activation covariance 在 $b$ 方向的 eigenvalue 大于 $a$ 方向，所以
activation PCA 的 top direction 是 $b$。

现在假设 group gradients 共享 input direction $a$：

$$
G_g=q_ga^\top+E_g,
$$

其中扰动 $E_g$ 不包含比 $a$ 项更强的共享 right-singular direction。那么共享
gradient right direction 是 $a$。因为 $a\perp b$，activation PCA 和
gradient intersection 可以选择不同 projector。因此 activation variance 不是
optimization common 的充分定义。

### 命题 2：真实路由打分漂移（gate-logit drift）混合了三种机制

gate logit 为 $z_t=W_th_t$：

$$
z_t-z_0=W_th_t-W_0h_0.
$$

加减项后：

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

所以 aggregate logit-drift 实验不能单独判断 collapse 来自 gate-weight
drift、hidden-state drift，还是 interaction。

## 6. 受控证据

受控实验按层推进故事。

**A01_01：可识别性。** 在已知 $P_c^*$ 的 synthetic hidden states 中，
四类 estimator 在不同 regime 中胜出：

```text
criterion_winner_diversity = 4
```

这削弱了 single-estimator theory。

**A01_03：optimization common。** 在 activation-gradient mismatch regimes
中，gradient intersection 在 gradient-overlap reduction 上胜过 activation
PCA：

```text
n_passed_mismatch_regimes = 4 / 4
```

这支持 gradient intersection 作为当前 optimization-common estimator。

**A01_04 controlled feedback bridge。** 在 feedback regimes 中，
feedback-only replay 复现 proxy-route collapse，feedback removal rescue
routing：

```text
n_passed_main_feedback_regimes = 2 / 2
controls_ok = true
```

这说明 feedback-common collapse 是有效的受控机制。

## 7. 真实证据与负结果

真实 DCLM 有界桥接审计（bounded bridge）复用了 A06 raw-center proxy setup，
并捕获 seeds 0/1/2、layers 3/4/5、checkpoints 0/5/10 的 gate logits。

full logit drift 复现了 A06 collapse：

```text
step0 NMI = 0.7549
step5 full NMI = 0.0410
step10 full NMI = 0.0131
```

但低秩 feedback-logit bridge 失败：

```text
pass = false
mean_explain_valid = 0.4230
mean_rescue_valid = 0.1625
mean_random_explain_valid = 0.3355
```

提高 rank 可以重构更多 collapse，但 random subspaces 也变好。因此高 rank
重构不是低秩 common 机制的特异证据。

## 8. 调和与修正理论

受控结果和真实结果并不矛盾。

受控实验说明：

```text
如果相关 common 机制被隔离，对应 estimator 可以找到或 replay 它。
```

真实 gate-logit 实验说明：

```text
真实 DCLM 中，aggregate gate-logit collapse 不能由一个简单 rank-1
logit-common direction 解释。
```

修正后的工作理论是：

```text
common 必须按机制和层/状态角色索引。
真实 preservation failure 很可能混合 gate-weight drift、hidden-state drift
和 expert-feedback effects。
```

因此 residualized MoE 方法仍然过早。我们还不知道真实应该 residualize 哪一项。

## 9. 下一步实验

下一步应计算三个 replay state 下的 route NMI：

$$
z_{\mathrm{gate}}=z_0+(W_t-W_0)h_0,
$$

$$
z_{\mathrm{hidden}}=z_0+W_0(h_t-h_0),
$$

$$
z_{\mathrm{interaction}}=z_0+(W_t-W_0)(h_t-h_0).
$$

决策规则：

| 主导 collapse 项 | 解释 | 下一步 |
|---|---|---|
| $(W_t-W_0)h_0$ | gate weights 偏离 proxy partition | gate-update 或 router-loss intervention |
| $W_0(h_t-h_0)$ | hidden states 被训练 feedback 推走 | hidden feedback-common estimator |
| interaction / cancellation | collapse 是耦合机制，不是简单 projector | 先建更细 feedback model |

## 10. 来源图谱和审计表

这个 closure 不引入新测量。它只是把已经记录的 A01 证据整理成一条机制故事。

### 10.1 来源图谱

| 对象 | 来源 |
|---|---|
| 路线文档 | `../route_document.md` |
| 中文路线文档 | `../route_document_cn.md` |
| A01_01 可识别性 | `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md`；`../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/detailed.md` |
| A01_03 activation/gradient mismatch | `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md`；`../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/detailed.md` |
| A01_04 受控 feedback bridge | `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/summary.md`；`../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/detailed.md` |
| A01_04 real-DCLM logit bridge | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/summary.md`；`../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/detailed.md` |

### 10.2 实验逻辑链

| 步骤 | 问题 | 证据 | 解锁的决策 |
|---|---|---|---|
| A01_01 | common 是单一 estimator，还是由判据决定？ | 四类 estimator 在不同受控 regime 中胜出。 | 把 common 看成机制索引的对象。 |
| A01_03 | activation 和 gradient 判据冲突时，谁更能估计 optimization common？ | gradient intersection 在四个 mismatch regime 中全胜。 | optimization-common audit 使用 gradient intersection，同时保留 activation PCA 作为 rival。 |
| A01_04 controlled | feedback common 能否在受控 router 中被因果 replay/remove？ | feedback-only replay 造成 proxy route collapse；residual-only removal 救回 routing。 | feedback-common 是有效受控机制。 |
| A01_04 real-DCLM | 简单低秩 gate-logit common 能否解释真实 A06 collapse？ | full logit drift 复现 collapse，但 rank-1 explain/rescue 失败，random control 接近。 | 方法构造前，先拆 gate-weight、hidden-state 和 interaction。 |

### 10.3 实测结果

| 实验 | 主指标 | 实测结果 | 它决定什么 | 它不能决定什么 |
|---|---|---:|---|---|
| A01_01 | `criterion_winner_diversity`：胜出主判据的非随机 estimator family 数量。 | 4 | controlled regime 中不支持 universal common estimator。 | real-DCLM common、层选择或 utility。 |
| A01_03 | `gradient_overlap_reduction_advantage`：$\Delta C(P_{\mathrm{grad}})-\Delta C(P_{\mathrm{act}})$。 | 4 / 4 mismatch regimes pass。 | controlled mismatch setting 中，optimization-common 更适合用 gradient intersection 估计。 | 真实 feedback 因果性或 preservation rescue。 |
| A01_04 controlled | `proxy_nmi_drop_explained_by_feedback_common`：feedback-only drift 复现 full proxy-route NMI drop 的比例。 | 2 / 2 main feedback regimes pass；controls ok。 | feedback replay/removal 是有效受控 preservation 机制。 | real-DCLM hidden drift 或 loss-neutral intervention。 |
| A01_04 real-DCLM | real bridge pass rule：rank-1 explain/rescue 必须特异地解释并救回 full collapse。 | `pass=false`；mean explain 0.4230；mean rescue 0.1625。 | 低秩 gate-logit common 不足以作为主要真实解释。 | hidden-state drift 和 gate-weight drift 谁主导。 |

### 10.4 证明 / 假设 / 经验命题账本

| 陈述 | 类型 | 状态 | 边界 |
|---|---|---|---|
| 只看 shared+routed sum 的 loss，不能唯一分配一个 function component 属于 shared branch 还是 routed branch。 | Section 3 的代数证明。 | 支持。 | 这是不可辨识性结果，不等于 common branch 永远没用。 |
| activation PCA 和 gradient common 可以选择正交 projector。 | 命题 1 的构造性证明。 | 支持；A01_03 提供受控证据。 | 依赖命题中写明的 covariance 和 gradient 结构。 |
| aggregate gate-logit drift 混合 gate-weight drift、hidden-state drift 和 interaction。 | 命题 2 的代数分解。 | 支持。 | 不说明真实 run 中哪一项主导。 |
| feedback common 可以覆盖 routing。 | 受控经验命题。 | A01_04 controlled 支持。 | 尚未证明 real-DCLM hidden-state drift。 |
| 低秩 real gate-logit common 解释 A06 collapse。 | 经验命题。 | 被 A01_04 real-DCLM 削弱。 | 高 rank reconstruction 不特异，因为 random subspace 也会改善。 |
| real hidden-state feedback common 解释 A06 collapse。 | 开放经验命题。 | 未解决。 | 需要下一步 gate-weight / hidden-state decomposition。 |
| 现在应构造 residualized MoE 或 common branch。 | 方法提案。 | 暂不支持作为 mainline 下一步。 | 分离真实 drift source 后可以重新评估。 |

## 11. 主张边界

可以 claim：

- controlled common estimation 是机制条件化的；
- gradient intersection 是当前 controlled optimization-common estimator；
- feedback replay/removal 是有效受控 preservation 机制；
- real gate-logit drift 可以复现 A06 collapse；
- 低秩 gate-logit common 不足以作为主要真实解释。

不能 claim：

- real hidden-state feedback common 已被识别；
- gate-weight drift 和 hidden-state drift 已经分离；
- common branch 或 residualized MoE 会改善语言模型 loss 或 rare-token
  utility；
- 单个 layer-global common projector 足够；
- proxy-route NMI 能证明语义专家效用。

当前工作假设：

```text
真实 preservation failure 是耦合的 training-feedback 问题。
下一步有效动作是 decomposition，不是 method construction。
```

## 附录：数据 / 模型 / 参数 / 脚本

| 实验 | 数据 / 模型 / 目标 | 参数和 checkpoint | runner 与结果路径 | 主指标 |
|---|---|---|---|---|
| A01_01 | 已知 $P_c^*$ 的 synthetic hidden states；判据测试 subspace recovery、shared-loss sensitivity 和 gradient-overlap reduction。 | dim 16；common rank 2；unique rank 2；6 groups；600 samples/group；seeds 0-9。 | `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/scripts/run_common_operator_full_run.py`；结果目录 `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/`；config `tables/run_config.json`。 | `criterion_winner_diversity` |
| A01_03 | synthetic activation/gradient mismatch states；目标是区分 activation variance 和 optimization redundancy。 | dim 32；common/functional/unique/nuisance ranks 2；6 groups；500 samples/group；seeds 0-19。 | `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/scripts/run_gradient_vs_activation_full_run.py`；结果目录 `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/`；config `tables/run_config.json`。 | `gradient_overlap_reduction_advantage` |
| A01_04 controlled | synthetic proxy router + feedback/residual drift；目标是测试 proxy-route collapse 的 replay/removal 因果性。 | dim 32；8 experts；600 samples/group；feedback rank 1；seeds 0-19。 | `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/scripts/run_feedback_bridge_controlled_full_run.py`；结果目录 `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/`；config `tables/run_config.json`。 | `proxy_nmi_drop_explained_by_feedback_common` |
| A01_04 real-DCLM | DCLM-bin 真实文本设置；6-layer Qwen3-MoE toy；raw-center router；从 next-token training 中恢复 gate-logit artifacts。 | seeds 0/1/2；layers 3/4/5；checkpoints 0/5/10；65,536 eval tokens/layer；lr 0.0003；batch 2。 | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/scripts/run_real_dclm_feedback_logit_bridge.py`；rank sweep `scripts/reanalyze_real_feedback_logit_artifacts.py`；结果目录 `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/`。 | real bridge pass rule |

关键真实 DCLM artifact：

| Artifact | Path |
|---|---|
| source manifest | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/config/source_manifest.json` |
| run config | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/config/run_config.json` |
| per-cell bridge scores | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_scores.csv` |
| bridge summary JSON | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_summary.json` |
| rank sweep | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_rank_sweep_summary.csv` |
