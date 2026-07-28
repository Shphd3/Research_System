---
experiment_id: A14_02_E02_frequency_mapping_rank_separation
status: approved
approved_by: researcher
approved_date: 2026-07-26
execution_scope: local_two_gpu_full_then_e03_if_gate
canonical_protocol: protocol.md
---

# Protocol：A14_02_E02 frequency–mapping rank separation

## 0. Approval Snapshot

**批准状态：** `PROTOCOLS_APPROVED`；允许实现、smoke、本地双 H100 full run，
并在 E02 gates 通过后自动继续 E03。  
**目的：**判断已学 common mapping 内，把 target exact frequency 从 $8$ 降到
$1$，是否会使冻结读出 ROOT 功能秩增加超过两个方向。  
**主 anchor：**[A14_02_01](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor_cn.md)。  
**主 prior：**任务方向预算由 mapping 复用更直接决定，不由单 cell raw frequency
单独决定。  
**最强 rival：**LowF 更小秩只是没学会、剂量/边际不匹配、答案头瓶颈或无效
投影。  
**唯一改变：**target cell 的 realized optimizer count，$F=1$ 对 $F=8$。  
**保持固定：**common mapping、总 function dose、逐 alias/entity/answer/context
边际、token/batch/step 数、模型、初始化、optimizer 和评估切片。  
**主指标：**paired difference
$D_s=k_{\mathrm{func},s}^{\mathrm{LowF}}-k_{\mathrm{func},s}^{\mathrm{HighF}}$。  
**Pass：**至少 8 个有效 paired seeds；$\mathbb E[D_s]$ 的单侧 95% upper bound
$\le2$，且至少 80% 有效 pairs 满足 $D_s\le2$。  
**Fail：**全部 hard gates 通过，且单侧 95% lower bound $>2$。  
**Insufficient：**少于 8 个有效 pairs、区间跨 margin，或 capability、rank
validity、replay、matching、test-isolation 任一失败。  
**不能声称：**frequency 永远不影响学习/秩、raw ROOT 或完整参数低秩、自然语言
已验证、H9-F 由 NTP 自动推出。  
**批准决定：**`APPROVED FOR FULL EXECUTION`。

## 1. 术语与指标定义

### 1.1 Exact frequency

对 cell $u=(r,a)$，实际 optimizer 呈现次数为

$$
F_{\mathrm{exact}}(u)
=
\sum_{x\in\mathcal S_{\mathrm{optimizer}}}
\mathbf1\{x\text{ 包含 }u\}.
$$

- **直白含义：**该 alias–entity 精确配对真正进入多少次训练更新。
- **单位：**presentations。
- **判定作用：**确认主 treatment 确实是 $1$ 对 $8$。
- **不能证明：**出现次数等于独立信息量或 context diversity。

### 1.2 Unseen-cell accuracy

unseen-cell 与 frequency target 互斥，并满足 $F_{\mathrm{exact}}=0$。其 alias
$r$ 和 entity $a$ 必须分别在其他 cell 中出现。final accuracy 为

$$
Acc_{\mathrm{unseen}}
=
\frac1{|\mathcal D_{\mathrm{unseen}}|}
\sum_{(r,a,c)}
\mathbf1\{\arg\max_y p_\theta(y\mid r,a,c)=\pi(a)\}.
$$

- **单位：**比例 $[0,1]$。
- **能力门：**$Acc_{\mathrm{unseen}}\ge0.75$。
- **解析：**证明模型能把其他 surfaces 学到的 $\pi(a)$ 用于零曝光 cell；门槛
  已按研究者对小样本、小模型的判断下调并在看结果前冻结。
- **不能证明：**模型内部实现了唯一的 symbolic algorithm。

### 1.3 固定读出 ROOT 功能秩

ROOT 为 final normalization 后、原 language head 前的状态。只在 basis-fit
calibration 上拟合均值 $\mu$ 和 ordered orthogonal basis $U$：

$$
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu).
$$

冻结原输出头，在 rank-selection split 定义

$$
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\left\{
q:
\Delta CE_q\le\epsilon_L,
\quad
\Delta Acc_q\le\epsilon_A
\right\},
$$

其中

$$
\Delta CE_q
=CE(\widetilde h_\rho^{(q)})-CE(h_\rho),
\qquad
\Delta Acc_q
=Acc(h_\rho)-Acc(\widetilde h_\rho^{(q)}),
$$

并冻结

$$
\epsilon_L=0.02\ \mathrm{nat},
\qquad
\epsilon_A=0.01.
$$

- **单位：**ROOT directions。
- **持久规则：**候选 $q$ 及全部更高 rank 均需过阈值。
- **test isolation：**$q$ 在 rank-selection 选择；final test 只验证同一 $q$，
  不得重新选 rank。
- **不能证明：**严格矩阵秩、非线性内在维度、所有中间计算维度。

### 1.4 主非劣效量

$$
D_s
=
k_{\mathrm{func},s}^{\mathrm{LowF}}
-k_{\mathrm{func},s}^{\mathrm{HighF}}.
$$

- **单位：**directions。
- **方向：**$D_s>0$ 表示 LowF 需要更多方向。
- **主边界：**$\tau=2$。
- **统计量：**paired bootstrap 的单侧 95% upper/lower bounds，10,000 次，
  seed `20260726`。

### 1.5 Common-space stability

用 32 个 leave-target-out common AdamW step contrasts 拟合 $G_c$，并在另 32 个
probe contrasts $V_{\mathrm{test}}$ 上计算

$$
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}.
$$

- **单位：**energy fraction。
- **E03 门：**LowF 至少 8 个 seeds 满足 $C_{\mathrm{common}}\ge0.80$。
- **不能证明：**该参数空间是唯一或坐标不变的模型机制。

## 2. Anchor Alignment

本实验是 root-cause/operationalization test。它只裁定 frequency non-inferiority，
不把 E01 的 lookup-$K$ 三点趋势升级成新的主因果结论。

## 3. Tested Hypothesis

$$
H_{\mathrm{reuse}}:\mathbb E[D_s]\le2,
\qquad
H_{\mathrm{frequency}}:\mathbb E[D_s]>2.
$$

## 4. Rival Explanations

1. LowF 未学会；由 target-new-context 与 unseen-cell gates 排除。
2. 总剂量或边际不同；由整数 count/context audit 排除。
3. 输出头吸收缺失信息；输出头在 replay 中冻结。
4. 低 rank 只是任意投影；由 shuffle 与 matched-rank random subspace 排除。
5. test 选择 rank；由三分 split 与 hash audit 排除。

## 5. Data、模型、目标与算法

### 5.1 Common task

$$
p(y\mid r,a,c)=\mathbf1\{y=\pi(a)\},
$$

$r\in\{0,\ldots,15\}$，$a\in\mathbb Z_{17}$，$\pi$ 为每个 seed 前冻结的随机
bijection，$c$ 不改变答案。

### 5.2 Cell split

$$
\mathcal T_s
=\{(r,(4r+j+o_s)\bmod17):j=0,\ldots,3\},
$$

$$
\mathcal U_s^{cal}
=\{(r,(4r+j+o_s)\bmod17):j=4,\ldots,7\},
$$

$$
\mathcal U_s^{test}
=\{(r,(4r+j+o_s)\bmod17):j=8,\ldots,11\}.
$$

三者两两互斥；每个 alias 剩余五个 cells 是 donors。

### 5.3 Count matching

冻结 donor baseline $B=19196$。LowF target count 为 $1$，HighF 为 $8$。
HighF 从非 target、非 unseen donors 移走整数表 $X$：

$$
X_{r,a}\ge0,
\qquad
\sum_aX_{r,a}=28,
\qquad
\sum_rX_{r,a}=7t_a,
$$

其中 $t_a$ 是 entity $a$ 出现在 target 集中的次数。由此两个条件都具有
$1,535,744$ 次 optimizer presentations 和 5,999 个 batch-size-256 updates。
训练 context 由 alias 与 seed 固定，因此逐 alias count 相同自动保证 context
边际相同；评估 contexts 使用互斥 offsets。

### 5.4 模型与训练

- causal Transformer：2 layers、1 head、width 64、FF width 128；
- full-position NTP cross-entropy；
- AdamW，learning rate 0.002，weight decay 0，gradient clip 1；
- 每个条件对冻结 materialized stream 做一次 deterministic shuffle 和完整遍历；
- fixed final checkpoint，不用 confirmation test 选 checkpoint；
- paired seeds $0,\ldots,9$；两张 H100 各跑一个固定 shard。

## 6. Conditions、Seeds 与 Checkpoint

| 条件 | target $F$ | 作用 | 主/次 | 必须通过 |
|---|---:|---|---|---|
| Common-LowF | 1 | 主 treatment | 主 | capability、rank validity、common-space |
| Common-HighF-Duplicate | 8 | 主 control；新增七次为 exact duplicate | 主 | capability、rank validity |

`Common-HighF-Diverse` 不进入 full protocol：E01 已裁定 diversity rival，且本
实验两个主条件都必须直接通过同一 unseen/new-context gate。lookup-$K$ 曲线复用
E01 作为次级历史证据，不新增一个与 frequency verdict 并列的主问题。

## 7. Primary Metric

主判定只使用 $D_s$ 及其 paired one-sided interval。单独列出
$k_{\mathrm{func}}^{\mathrm{fix}}$ 是物理测量；不以 raw ROOT effective rank 或
参数 rank 代替主结论。

## 8. Secondary Metrics 与守卫

对任意评估切片 $\mathcal D$，

$$
Acc(\mathcal D)
=\frac{1}{|\mathcal D|}\sum_{(x,y)\in\mathcal D}
\mathbf1\{\arg\max p_\theta(\cdot\mid x)=y\},
$$

$$
CE(\mathcal D)
=-\frac{1}{|\mathcal D|}\sum_{(x,y)\in\mathcal D}
\log p_\theta(y\mid x).
$$

target/new-context 门为 $Acc\ge0.95$、$CE\le0.10$ nat；unseen-cell 门为
$Acc\ge0.75$。accuracy 单位是比例，CE 单位是 nat；二者证明行为能力，不证明
内部实现方式。

对 calibration 已选择并冻结的 rank，

$$
\Delta CE_q^{\mathrm{test}}=CE_q^{\mathrm{test}}-CE_{\mathrm{full}}^{\mathrm{test}},
\qquad
\Delta Acc_q^{\mathrm{test}}=Acc_{\mathrm{full}}^{\mathrm{test}}-Acc_q^{\mathrm{test}}.
$$

final-test 门为 $\Delta CE\le0.02$ nat、$\Delta Acc\le0.01$；它只验证 rank
迁移，不在 final test 重新选 rank。

full-rank identity replay 为

$$
E_{\mathrm{identity}}=|CE_{q=d}-CE_{\mathrm{full}}|\le10^{-5}\ \mathrm{nat}.
$$

ROOT shuffle 为

$$
\Delta CE_{\mathrm{shuffle}}=CE(h_{\rho,\sigma(i)},y_i)-CE(h_{\rho,i},y_i),
\qquad
\Delta Acc_{\mathrm{shuffle}}=Acc_{\mathrm{full}}-Acc_{\mathrm{shuffle}},
$$

并要求 CE 增加至少 $0.10$ nat 或 accuracy 下降至少 $0.10$。这两个守卫验证
ROOT 干预面有效，但不证明所选子空间唯一。

对每个 selected-rank Haar 随机基 $Q_j$，

$$
\widetilde h_j^{(q)}=\mu+Q_{j,q}Q_{j,q}^\top(h-\mu).
$$

32 个随机子空间中通过同一 CE/accuracy 门的数量必须为 0；它验证任务特异性，
不证明对所有非线性子空间的全局最优。

对 centered ROOT 的奇异值能量 $\lambda_i=\sigma_i^2$，

$$
p_i=\frac{\lambda_i}{\sum_j\lambda_j},
\qquad
r_{\mathrm{eff}}=\exp\left(-\sum_i p_i\log p_i\right).
$$

raw ROOT entropy effective rank 只作 H12 几何描述，不能替代冻结头功能秩。
$C_{\mathrm{common}}$ 已在 1.5 定义，只决定 E03 是否有资格执行。

## 9. Known Good / Bad / Confusing

- good：full-rank replay 精确恢复；
- bad：ROOT shuffle 明显破坏答案；
- confusing：模型 task accuracy 高但 unseen-cell 低，功能秩不得解释为复用。

## 10. Stage Profiling

| 阶段 | 问题 | 通过条件 | 产物 |
|---|---|---|---|
| generator | count、split、边际是否严格匹配 | 全部 exact | generator_audit.json |
| smoke | hooks、checkpoint、三分 replay 是否有效 | 全部 schema/gates 可计算 | smoke/ |
| full training | final checkpoint 是否具备能力 | capability gates | jobs/* |
| rank | calibration 选择、test 只验证 | replay guards | replay_curves.csv |
| merge | 非劣效是否成立 | 预注册规则 | decision.json |

## 11. Execution Contract

原始 checkpoints、logs、probe vectors 留在 runnable workspace；mainline 只接收
protocol、summary、detailed、小表格和中心图。任何 implementation bug 修复必须
先保留原输出并版本化，不能根据 confirmation test 改阈值。

## 12. Success / Failure / Insufficient

按 Approval Snapshot 原样执行。E02 verdict 与 E03 execution gate 分开：即使
非劣效主 verdict 为 fail，只要 capability、rank validity 与 common-space
stability 全过，E03 仍可执行以解释机制；任一 gate 失败则 E03 parked。

## 13. What This Cannot Claim

见 Approval Snapshot；特别不能把 E01 $K$ 趋势与 E02 frequency 非劣效合并成
“mapping 数量普适决定秩”的因果定律。

## 14. Review Notes And Protocol Changes

- 2026-07-26：研究者批准 unseen-cell 精确定义，并因小样本/小模型将 final
  accuracy 门从候选 0.90 下调为 0.75；其他定义与阈值批准。
- 2026-07-26：研究者批准本地双卡 full run，以及 gates 后自动继续 E03。
