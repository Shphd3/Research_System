# A06_03_02_E01 Protocol：Learned Specialist 的 Rank-Mediated Correction

## 0. 审批摘要

**状态：** 依据持续研究目标，于 2026-07-10 批准执行。

**唯一问题：** learned specialists、representation、score ladder 和 load 都受控
时，weighted top-1 能否像 utility-bearing soft mixture 一样，从初始 rank 2 或
4 找回 useful expert？

**主统计量：** rank-4 top-1 相对相同初态 soft mixture 的配对删失纠正时间差：

$$
D_{corr}=\operatorname{median}_{f,seed}
\left[\widetilde T_{corr}^{top1,rank4}
-\widetilde T_{corr}^{soft,rank4}\right].
$$

**支持 sparse discovery bottleneck：** $D_{corr}$ 超过 5 步且聚类 CI 下界为
正，同时 top-1 的 normalized cumulative regret 更大。

**支持无实质 bottleneck：** 两个 rank-4 条件纠正率均至少 0.90，$D_{corr}$ 的
CI 上界不超过 5，regret gap 的 CI 上界不超过 0.05。

## 1. 术语解释

| 术语 | 具体含义 | 计算 | 当前作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| useful expert | correct exposure 后 forced task loss 最低的 specialist | $u(f)=f$ | 功能 target | 自然语义 |
| initial rank | useful expert 的初始 score 排名 | 1、2、4 | 控制搜索距离 | 真实出现频率 |
| sustained correction | useful expert 连续 5 步保持 top-1 | route accuracy $\ge0.95$ | 排除瞬时 crossing | 永久收敛 |
| capped correction time | 未在 300 步纠正时记作 301 | $\widetilde T_{corr}$ | 纳入删失单元 | 完整生存模型 |
| normalized cumulative regret | 相对初始 routing excess 的时间平均剩余误差 | $NR$ | 训练效率共同证据 | wall-clock 效率 |
| forward utility coverage | 哪些 expert outputs 进入 loss | top-1 为 1 个，soft 为 4 个 | 机制干预 | 等 compute |

## 2. 精确设置

- 复用 A06_03_01_E01/A06_03_01_E02 的四类上下文 modular task。
- 序列长 33，全部 32 个 next-token positions 进入 LM loss。
- 一层 causal attention、residual + LayerNorm、四个 MLP experts；无 learned
  positional embedding，不加入 position 或 route labels。
- 先进行 200 步 expert-only exposure，重建 specialists/generalists。
- correction 阶段冻结 experts 与 representation，只训练 router。
- optimizer：full-batch SGD，learning rate 0.001，无 momentum/weight decay。
- correction horizon 300，逐步评估；持续窗口 5。
- 正式 32 seeds；smoke 使用 2 seeds、完整 exposure、50 步 correction。

## 3. Rank 构造

所有条件共享 score ladder：

$$
[0.75,0.25,-0.25,-0.75].
$$

只 permutation expert identity，使 useful expert 位于 rank 1、2 或 4。其余 experts
按循环顺序排列，因此 rank 2/4 的初始 selected wrong expert 相同，且每个 expert
初始 top-1 load 完全平衡。由 task centers $C$ 和目标 score matrix $S$ 解：

$$
W^\top=C^+S.
$$

必须通过：train/test useful-rank accuracy $\ge0.999$、p05 adjacent gap $\ge0.40$、
load spread 0、train construction-center score error $\le5\times10^{-4}$、
top-1/soft 初态差 $\le10^{-7}$。

held-out centers 不要求逐值复现 train target matrix；test validity 直接由 held-out
useful-rank accuracy 与 p05 adjacent gap 保护，以免把采样漂移误判为条件不一致。

## 4. 条件

| Expert state | Forward | Rank | 作用 |
| --- | --- | ---: | --- |
| specialist | weighted top-1 | 1/2/4 | correct guard、短搜索、强 stress |
| specialist | soft mixture | 1/2/4 | matched utility-coverage controls |
| generalist | weighted top-1 | 4 | 无唯一功能 target 的几何 guard |
| generalist | soft mixture | 4 | soft specificity guard |

## 5. 指标与判定

定义 held-out routing excess：

$$
E_f(t)=L_f^{native}(t)-L_{f,u}^{cf}.
$$

归一化累计 regret：

$$
NR_f(T)=\frac1{T+1}\sum_{t=0}^T
\frac{[E_f(t)]_+}{\max([E_f(0)]_+,10^{-12})}.
$$

报告 capped sustained correction time、horizon correction rate、$NR$、useful
expert probability/rank、majority selected identity、boundary-change count、native
task/all-position loss、router gradient/update norm。

判定：

- **H1 rank-mediated：** top-1 rank4-rank2 capped time 超过 5，且 $NR$ 差为正；
  两者 CI 下界均为正。
- **H2 utility coverage：** rank-4 top1-soft capped time 超过 5，且 $NR$ 差为正；
  两者 CI 下界均为正。
- **H3 no material bottleneck：** 两边 correction rate $\ge0.90$，时间差 CI 上界
  $\le5$，regret gap CI 上界 $\le0.05$。
- 时间与 regret 不一致时，结论为 mixed，不强行归类。

## 6. 有效性与边界

specialist utility gap 中位数必须大于 5；generalist absolute gap 小于 0.5；32
seeds、rank/load/state guards、finite trajectory 必须全部通过。soft rank-4
correction rate 若低于 0.90，说明正对照或 horizon 不充分，主结论无效。

本实验不能证明 label-free discovery、自然语言 semantic expert、production
sparse-compute speedup 或 soft routing 是最终方法。soft mixture 激活四条功能路径，
只用于判断未选 expert utility 是否需要进入 forward feedback。

## 7. 下一决策

若 weighted top-1 明显受 rank 限制且 soft control 同时改善 correction time 与
normalized regret，下一步才设计 sampled candidate 或 occasional-soft feedback。
若 top-1 与 soft 相当，则移除 oracle rank construction，直接进入 random-init、
更少 oracle 的 grounded context task。
