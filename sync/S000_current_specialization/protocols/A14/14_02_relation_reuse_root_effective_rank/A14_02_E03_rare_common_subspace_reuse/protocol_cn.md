---
experiment_id: A14_02_E03_rare_common_subspace_reuse
status: approved_conditional
approved_by: researcher
approved_date: 2026-07-26
execution_scope: run_only_after_e02_capability_rank_common_space_gates
canonical_protocol: protocol.md
---

# Protocol：A14_02_E03 rare–common subspace reuse

## 0. Approval Snapshot

**批准状态：**`PROTOCOLS_APPROVED`，但只有 E02 capability、rank-validity 与
common-space stability gates 通过后执行。  
**目的：**判断一次调用已学 common mapping 的 rare 暴露，是否产生 common 与
历史 residual 之外、幅度非小且冻结读出功能上必要的新方向。  
**主 anchor：**[A14_02_02](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor_cn.md)。  
**主 prior：**rare 的任务有效更新大部分复用 common/old directions；几何 outside
不自动等于功能新方向。  
**最强 rival：**rare 确实需要新方向，或 outside 只是 AdamW、common-space 估计、
参数 gauge、随机删除损害造成的假象。  
**唯一改变：**同一个 batch-size-1 slot 中放 rare target 或 matched common
control；其余起点状态和字段固定。  
**主因果指标：**$\Delta CE_{\mathrm{drop-new}}$。  
**Pass（reuse）：**至少 8 个 causal-valid seeds；rare 有可测增益，但新分量小，
或删除新分量的单侧 95% upper bound $\le0.02$ nat，同时 base/random guards 通过。  
**Fail（new direction required）：**至少 8 个 causal-valid seeds；
$\rho_{\mathrm{new}}$ 稳定非小，$\Delta CE_{\mathrm{drop-new}}$ 的单侧 95% lower
bound $>0.02$ nat，超过等范数 random deletion，且 base 保持。  
**Insufficient：**rare full branch 没有稳定可测功能增益、少于 8 seeds、E02 gate
失败、common/old space 不稳、或功能结果混合。  
**不能声称：**所有 rare facts 都复用、参数坐标新颖等于语义新颖、自然语言或
多层 LLM 已验证、H9-F 由 NTP 自动推出。  
**批准决定：**`APPROVED, CONDITIONAL ON E02 GATES`。

## 1. 术语与指标定义

### 1.1 Target-attributable finite parameter effect

rare/control 从完全相同的 $\theta_{\mathrm{ref}}$ 与 AdamW state 各走一个实际
step：

$$
v_r
=
\theta_T^{\mathrm{rare}}
-
\theta_T^{\mathrm{ctrl}}.
$$

- **直白含义：**把一个 common control 换成 rare target 后，实际 optimizer
  终点改变了多少。
- **单位：**注册非输出头参数坐标中的 Euclidean vector。
- **判定作用：**所有 common/outside/new 分解的对象。
- **不能证明：**它等于 rare 样本的 per-example gradient；gradient 另行记录。

### 1.2 Common、outside、old 与 new 分量

令 $P_c$ 为 leave-target-out common step-contrast space 的正交投影，
$P_{\mathrm{old}}$ 为 $G_c^\perp$ 内历史 residual update space 的投影：

$$
v_\parallel=P_cv_r,
\qquad
v_\perp=(I-P_c)v_r,
$$

$$
v_{\mathrm{old}}=P_{\mathrm{old}}v_\perp,
\qquad
v_{\mathrm{new}}=(I-P_c-P_{\mathrm{old}})v_r.
$$

$G_c$ 用 32 个 common contrasts 拟合并用另 32 个验证；$R_{\mathrm{old}}$ 来自
E02 终点前最后 64 个实际 batch updates 在 $G_c^\perp$ 中的 95% energy basis。

### 1.3 Outside 与 new energy fractions

$$
\rho_\perp
=
\frac{\|v_\perp\|_2^2}
{\max(\|v_r\|_2^2,\varepsilon)},
$$

$$
\rho_{\mathrm{new}}
=
\frac{\|v_{\mathrm{new}}\|_2^2}
{\max(\|v_r\|_2^2,\varepsilon)},
$$

$$
\nu_{\mathrm{new}}
=
\frac{\|v_{\mathrm{new}}\|_2^2}
{\max(\|v_\perp\|_2^2,\varepsilon)}.
$$

- **单位：**无量纲 energy fraction。
- **作用：**$\rho_\perp$ 判断 outside 总量；$\rho_{\mathrm{new}}$ 判断相对完整
  effect 的新量；$\nu_{\mathrm{new}}$ 只描述 outside 内部的新颖度。
- **非小门：**

$$
\rho_{\mathrm{new}}
\ge
\max(0.05,Q_{0.95}(\rho_{\mathrm{new}}^{\mathrm{common-null}})).
$$

- **不能证明：**参数几何新颖就是任务或语义新颖。

### 1.4 Rare functional gain

在预注册 rare-cell/new-context eval 上：

$$
\Delta CE_{\mathrm{gain}}
=
CE(\theta_T^{\mathrm{ctrl}})
-CE(\theta_T^{\mathrm{rare}}).
$$

- **单位：**nat。
- **causal-valid 门：**$\Delta CE_{\mathrm{gain}}\ge0.02$ nat。
- **解释：**rare step 相比 control 确实改善了 rare task；若没有，无法判断某个
  新分量是否是该功能增益所必需。

### 1.5 Exact endpoint drop-new

$$
\theta_T^{\mathrm{drop-new}}
=
\theta_T^{\mathrm{rare}}-v_{\mathrm{new}}
=
\theta_T^{\mathrm{ctrl}}+v_\parallel+v_{\mathrm{old}}.
$$

构造后不继续训练，直接完整前向：

$$
\Delta h_{\mathrm{new}}^{\mathrm{exact}}(x)
=
h_\rho(x;\theta_T^{\mathrm{rare}})
-h_\rho(x;\theta_T^{\mathrm{drop-new}}).
$$

- **解析：**这是两个完整参数 endpoint 的 exact finite difference。
- **不能使用：**$J_\rho(\theta_\star)v_{\mathrm{new}}$；E06 已表明单点 Jacobian
  不能代表该类有限效应。

### 1.6 主因果指标

冻结同一个 reference output head：

$$
\Delta CE_{\mathrm{drop-new}}
=
CE(\theta_T^{\mathrm{drop-new}})
-CE(\theta_T^{\mathrm{rare}}).
$$

- **单位：**nat。
- **方向：**正值表示删除新分量损害 rare task。
- **功能边界：**$0.02$ nat。
- **为何最重要：**它直接测试“新分量是否被任务使用”；参数范数不能替代它。

### 1.7 Random-removal specificity 与 base preservation

对 16 个与 $v_{\mathrm{new}}$ 等范数、且位于 keep-space 正交补中的 Haar random
directions $z_j$：

$$
\Delta CE_{\mathrm{random},j}
=
CE(\theta_T^{\mathrm{rare}}-z_j)
-CE(\theta_T^{\mathrm{rare}}),
$$

$$
\Delta CE_{\mathrm{specific}}
=
\Delta CE_{\mathrm{drop-new}}
-Q_{0.95}(\Delta CE_{\mathrm{random}}).
$$

新方向必要要求 $\Delta CE_{\mathrm{specific}}>0$。在 base/common slice 上：

$$
\Delta CE_{\mathrm{base}}
=
CE_{\mathrm{base}}(\theta_T^{\mathrm{drop-new}})
-CE_{\mathrm{base}}(\theta_T^{\mathrm{rare}}),
$$

并要求 $|\Delta CE_{\mathrm{base}}|\le0.02$ nat。

### 1.8 Common-space、重构与辅助诊断

前置 common-space 指标为

$$
C_{\mathrm{common}}
=\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}.
$$

- **单位：**held-out update energy fraction。
- **门槛：**至少 8 个 E02-valid seeds 达到 $0.80$，才允许把 rare 分量称为
  `outside-common`。
- **不能证明：**通过该门也不等于 common space 对任务功能充分。

分解重构误差为

$$
E_{\mathrm{recon}}
=\frac{\|v_r-v_\parallel-v_{\mathrm{old}}-v_{\mathrm{new}}\|_2}
{\max(\|v_r\|_2,\varepsilon)}
\le10^{-6}.
$$

它只检查数值分解是否闭合。令
$g_r=g^{\mathrm{rare}}-g^{\mathrm{ctrl}}$ 为注册参数上的 gradient contrast，
则 common-space 对齐为

$$
c_{\mathrm{grad}}
=\frac{\|P_cg_r\|_2}{\max(\|g_r\|_2,\varepsilon)},
\qquad
c_{\mathrm{step}}
=\frac{\|P_cv_r\|_2}{\max(\|v_r\|_2,\varepsilon)}.
$$

二者是无量纲 subspace cosine；差异用于诊断 AdamW preconditioning，不能证明
这些方向被任务功能使用。

exact drop-new 的 accuracy 下降为

$$
\Delta Acc_{\mathrm{drop-new}}
=Acc(\theta_T^{\mathrm{rare}})-Acc(\theta_T^{\mathrm{drop-new}}).
$$

定义正确类 logit margin

$$
m_\theta(x,y)=z_y(x;\theta)-\max_{y'\ne y}z_{y'}(x;\theta),
$$

则 margin 下降为

$$
\Delta m_{\mathrm{drop-new}}
=\mathbb E[m_{\theta_T^{\mathrm{rare}}}(X,Y)
-m_{\theta_T^{\mathrm{drop-new}}}(X,Y)].
$$

accuracy drop 单位是比例，margin drop 单位是 logit；二者只解释 CE 变化，
不能替代注册的主 CE 判定。

## 2. Anchor Alignment

本实验是 mechanism/causal-intervention audit，服务 H9-F/T6-F 的 finite endpoint
story；不测试 H9-L，也不恢复 H11。

## 3. Tested Hypothesis

**Reuse:** causal-valid rare effect 主要落在 common/old space，或 novel component
删除后功能保持。  
**Necessary-new rival:** rare effect 有稳定非小的 novel component，且 exact
drop-new 特异地删除 rare gain。

## 4. Rival Explanations

1. AdamW 使 gradient 与 update 不同：同时记录两者，分解实际 step effect；
2. $G_c$ 估计不足：32/32 split capture gate；
3. 旧 residual 被误称为新：显式 $R_{\mathrm{old}}$；
4. 任意参数删除都会伤害：equal-norm random removal；
5. 删除损坏基础模型：base-preservation；
6. 多步非线性分叉：主时间尺度固定为一个 step。

## 5. Data、模型与单步算法

- 只复用通过 E02 gates 的 Common-LowF seed；
- reference 为 E02 fixed final checkpoint 与 optimizer state；
- rare cell 从 E02 的零训练曝光集合按 seed 预注册选择；E03 eval contexts 与
  E02 confirmation contexts 互斥；
- control 使用同一 entity 与答案 $\pi(a)$，选择历史高频 donor alias；rare 与
  control exposure context 相同；
- 两支各做一个 batch-size-1 full-position NTP AdamW step；
- language head 在 step 前冻结，且所有 endpoints 用同一 reference head；
- 非输出头 trainable parameters 构成注册参数向量；
- paired seeds 继承 E02，目标至少 8 个 causal-valid seeds。

## 6. Conditions、Seeds 与 Checkpoints

| 对象 | 改变 | 固定 | 作用 |
|---|---|---|---|
| rare branch | rare cell | ref、optimizer、entity、answer、context | treatment |
| control branch | common donor cell | 同上 | counterfactual |
| drop-new endpoint | 删除 $v_{\mathrm{new}}$ | rare/control base 与 frozen head | 主干预 |
| random drop | 等范数随机方向 | norm、head、eval | 破坏守卫 |

## 7. Primary Metric

$\Delta CE_{\mathrm{drop-new}}$ 决定功能必要性；必须在
$\Delta CE_{\mathrm{gain}}$、$\rho_{\mathrm{new}}$、specificity 和 base guards
之后解释。

## 8. Secondary Metrics

$\rho_\perp$、$\rho_{\mathrm{new}}$、$\nu_{\mathrm{new}}$、common-null、
gradient cosine、actual-step cosine、accuracy drop、logit-margin drop、
$\Delta CE_{\mathrm{specific}}$、$\Delta CE_{\mathrm{base}}$。

## 9. Known Good / Bad / Confusing

- good：$v_r=v_\parallel+v_{\mathrm{old}}+v_{\mathrm{new}}$ 数值重构误差
  $\le10^{-6}$ relative；
- bad：故意删除完整 $v_r$ 应回到 control endpoint；
- confusing：$\nu_{\mathrm{new}}\approx1$ 但 $\rho_\perp$ 极小，不能称为新方向。

## 10. Stage Profiling

| 阶段 | 问题 | 通过条件 | 产物 |
|---|---|---|---|
| E02 gate | 是否允许 E03 | 三类 gate 全过 | e02_gate.json |
| branch audit | 起点与单变量是否匹配 | hash/count exact | branch_audit.json |
| spaces | common/old 是否稳定 | capture/null gates | subspace_metrics.csv |
| endpoint | 分解与重构是否精确 | error $\le10^{-6}$ | endpoint_audit.json |
| function | new 是否必要 | 预注册 CE rules | seed_summary.csv |

## 11. Algorithm Specification

1. 加载 E02 model/optimizer state，冻结 output head。
2. 用 target-free common counterfactual steps 构造 $G_c$，用 E02 最后 64 个
   historical updates 构造 $R_{\mathrm{old}}$。
3. 从同一起点执行 rare/control 各一步，记录 per-example gradients 与 actual
   AdamW endpoints。
4. 分解 $v_r$，构造 exact drop-new 与 16 个 random-drop endpoints。
5. 用同一 frozen head 在 rare eval 与 base eval 上完整前向。
6. 按 frozen rules merge，不根据 final data 改 rank/threshold。

## 12. Success / Failure / Insufficient

按 Approval Snapshot 执行。若至少 8 个 E02-valid seeds 但 fewer than 8 的
$\Delta CE_{\mathrm{gain}}\ge0.02$，记录为 `no_stable_measurable_rare_gain`，归入
功能必要性 `insufficient`；这本身说明注册单步 rare 暴露没有稳定可测增益，
但不能强行升级为 common-only sufficiency。

## 13. What This Cannot Claim

参数分解依赖注册坐标；exact endpoint 干预给出该干预下的因果效应，但不提供
唯一的非线性归因分解，也不能推广到完整训练路径或自然语言事实。

## 14. Review Notes And Protocol Changes

- 2026-07-26：研究者批准 exact endpoint drop-new、单 AdamW step 主尺度、
  frozen reference head、leave-target-out spaces 和 E02 gate 后自动执行。
