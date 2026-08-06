# `Phase 1 / 2 / 3` 理解笔记与失败机理分析

## 1. 主线到底是什么

这轮 `exp_hierarchical` 的主线不是“直接训练一个更大的 MoE”，而是把 toy 里拆出来的三个命题，按最小可验证顺序搬到真实大模型里。

总主线来自 [03_qwen3_8b_experiment_agent_plan.md](/data/250010109/spectral_router/exp_hierarchical/docs/03_qwen3_8b_experiment_agent_plan.md:24)：

1. 表示层是否真的存在会遮蔽 tail 语义的 `shared head`
2. 如果存在，切掉它之后的 `tail residual` 是否更利于语义分发
3. 如果表示层结论成立，把结构和优化也解耦以后，是否能进一步形成真实的专业化

所以三个阶段的关系是：

- `Phase 1`：只验证“几何命题”是否在真实 hidden state 中成立
- `Phase 2`：固定 `Phase 1` 找到的层与 projector，只测试“split 结构 + 优化解耦”能否改善单层控制
- `Phase 3`：在 `Phase 2` 之上，再测试“router 放在 tail residual 上”能否带来更真实的 expert specialization

这三步是嵌套关系：

`Phase 1 -> Phase 2 -> Phase 3`

而不是三套彼此独立的实验。

## 2. 三个 Phase 分别做了什么

### 2.1 Phase 1 做了什么

`Phase 1` 的代码入口是 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:1)。

它做的事情非常克制：

1. 读取冻结的 `Qwen3-8B`
2. 在 `post_attention_layernorm` 位置抓某几层 hidden state
3. 用 `DCLM + WoS` 的混合协方差池估计均值和协方差
4. 对协方差做特征分解，取 top-`k` 主方向
5. 构造三种表示：
   - `raw`
   - `centered = h - \mu`
   - `tail_residual = (I - V_k V_k^\top)(h - \mu)`
6. 在这些表示上做线性 probe 和聚类评估

实现细节：

- 协方差累计在 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:176) 到 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:197)
- `tail_residual` 投影在 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:243) 到 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:246)
- 评估在 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:275) 到 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:302)

这一步没有训练 backbone。  
它只是在问：

> 真实 hidden state 的几何结构里，是否真的存在一个“切掉之后更利于 WoS 领域区分”的共享高方差子空间。

### 2.2 Phase 2 做了什么

`Phase 2` 的代码入口是 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:1)。

它继承 `Phase 1` 的 `best_layer` 和 `best_k`，然后在冻结 backbone 的前提下，只训练一个插入到单层的控制器。

模型有三种：

1. `baseline_ffn`
   - 一个单分支 low-rank adapter
   - 一个 domain 分类头
   - 见 [BaselineController](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:288)
2. `split_coupled_optim`
   - 把表示拆成 `common` 与 `tail`
   - 各自过一个 adapter
   - 但共用统一的优化条件
   - 见 [SplitController](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:315)
3. `split_decoupled_optim`
   - 结构同上
   - 但 `tail_adapter` 与 `domain_head` 用更高 LR、更低 WD
   - 优化器定义在 [make_optimizer](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:459)

`SplitController` 的核心拆分是：

$$
h_c = P_k (h - \mu), \qquad
h_t = (I - P_k)(h - \mu),
$$

其中：

- $h$：这一层抓到的 token hidden state
- $\mu$：混合协方差池估计出来的均值
- $P_k = V_k V_k^\top$：`Phase 1` 估计出的共享主方向投影
- $h_c$：common 分量
- $h_t$：tail residual 分量

然后控制器学的是：

$$
\Delta h = f_c(h_c) + f_t(h_t),
\qquad
\tilde h = h + \Delta h.
$$

代码对应：

- `split_hidden` 在 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:328)
- `forward_hidden` 在 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:335)

训练损失是：

$$
L = L_{\text{LM}} + \lambda_{\text{dom}} L_{\text{dom}},
$$

其中：

- $L_{\text{LM}}$：next-token cross-entropy
- $L_{\text{dom}}$：WoS domain 分类交叉熵
- $\lambda_{\text{dom}}$：domain loss 权重

实际训练逻辑在 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:612) 到 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:641)。

这里有一个很重要的实现事实：

- DCLM batch 只有 $L_{\text{LM}}$
- WoS batch 才同时有 $L_{\text{LM}} + \lambda_{\text{dom}} L_{\text{dom}}$
- 调度按 `4:1` 混合，见 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:598) 到 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:600)

所以 `Phase 2` 实际在问：

> 如果我们已经知道 tail residual 更干净，那么把这个空间拿来做 split 控制，并给 tail 更特殊的 optimizer，能否在真实语言建模里更好地兼顾 domain 能力和通用能力。

### 2.3 Phase 3 做了什么

`Phase 3` 的代码入口是 [run_phase3_hierarchical_moe.py](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:1)。

它把 `Phase 2` 的 split 进一步变成一个最小 MoE proxy。

对照组是：

1. `flat_raw_uniform`
   - 在原始 hidden 上做 router
   - 每个 expert 是一个 low-rank adapter
   - 见 [FlatMoEController](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:295)
2. `tail_router_only`
   - router 只看 `tail residual`
   - expert 只作用在 tail
   - 见 [TailMoEController](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:324)
3. `tail_router_decoupled_wd`
   - 和上面一样
   - 但 tail experts 的 WD 更弱
4. `tail_router_decoupled_wd_lr`
   - tail experts / router 同时用更弱 WD 与更特殊的 LR 时钟

`TailMoEController` 的核心形式是：

$$
h = \mu + h_c + h_t,
$$

$$
r = \text{Router}(\bar h_t), \qquad
\pi = \text{softmax}(r),
$$

$$
\Delta h = f_c(h_c) + \sum_{e=1}^E \pi_e f_e(h_t),
$$

其中：

- $\bar h_t$：对 sequence 内 token 的 `tail` 做 masked mean pooling
- $E$：expert 数量
- $\pi_e$：第 $e$ 个 expert 的路由概率
- $f_c$：common 分支 adapter
- $f_e$：第 $e$ 个 tail expert

代码对应：

- `split_hidden` 在 [run_phase3_hierarchical_moe.py](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:336)
- tail router 前向在 [run_phase3_hierarchical_moe.py](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:343)

训练损失是：

$$
L = L_{\text{LM}} + \lambda_{\text{router}} L_{\text{router}},
$$

其中：

- $L_{\text{LM}}$：next-token cross-entropy
- $L_{\text{router}}$：用 WoS domain label 监督 router 的交叉熵
- $\lambda_{\text{router}}$：router loss 权重

训练逻辑在 [run_phase3_hierarchical_moe.py](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:617) 到 [run_phase3_hierarchical_moe.py](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:643)。

所以 `Phase 3` 真正问的是：

> 在真实 hidden state 上，如果 router 只看 tail residual，而且专家只在 tail 上分工，是否会比 flat raw router 更专业化。

## 3. 本轮结果总览

为了后续直接交给理论分析，这里先把当前最有说服力的正式结果压缩到一处。当前保留下来的主结果，全部来自已经清理后的正式目录：

- `Phase 1`：`Qwen3-8B` 两个正式 seed
- `Phase 2`：`len=256`、双 seed、长程本地 run
- `Phase 3`：`len=256`、双 seed、长程本地 run

对应主文档分别是：

- [Phase 1 摘要](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/docs/summary.md:1)
- [Phase 2 摘要](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/docs/summary.md:1)
- [Phase 3 摘要](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/docs/summary.md:1)

### 3.1 Phase 1 的正式结果

`Phase 1` 的结论最稳，而且它直接支持后续所有阶段的 projector 选择。

关键事实如下：

1. 两个正式 seed 的最优层都落在 `layer 35`
2. 最优 $k$ 稳定在 `16~32`
3. `raw` 与 `centered` 几乎重合，说明“去均值”不是关键
4. `tail_residual` 在两个正式 seed 上都拿到最优 `probe_accuracy / purity / NMI`

最关键数字如下：

| seed | layer / k | raw acc | centered acc | tail_residual acc | raw purity | tail_residual purity | raw NMI | tail_residual NMI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `qwen3_8b_phase1_local` | `35 / 32` | `0.7522` | `0.7533` | `0.7690` | `0.5000` | `0.5681` | `0.3327` | `0.3975` |
| `qwen3_8b_phase1_seed2` | `35 / 16` | `0.7444` | `0.7400` | `0.7511` | `0.4766` | `0.5725` | `0.3400` | `0.4064` |

shared head 存在的最直接证据来自谱结构：

- `layer 35` 前 `8` 个主方向累计解释方差达到 `0.4069`
- `layer 5` 前 `8` 个主方向累计解释方差达到 `0.3295`
- `layer 11` 则明显更平，前 `8` 个方向只有 `0.0561`

因此，`Phase 1` 支持的不是一个模糊直觉，而是一个很具体的结论：

> 在 `Qwen3-8B` 的真实 hidden state 中，确实存在一个低秩、共享、高方差的 head；把它切掉以后，`tail residual` 对 WoS 语义更可分。

### 3.2 Phase 2 的正式结果

`Phase 2` 的问题是：既然 `tail residual` 更干净，那么把单层控制器做成 split 结构，并对 tail 侧做更激进的优化解耦，是否能把几何优势转成训练优势。

长程双 seed 平均结果如下：

| config | dclm_ppl | wos_ppl | wos_domain_acc | wos_domain_nmi |
| --- | --- | --- | --- | --- |
| `baseline_ffn` | `17.5479 ± 0.3694` | `9.8634 ± 0.0628` | `0.7511 ± 0.0063` | `0.5428 ± 0.0056` |
| `split_coupled_optim` | `17.6052 ± 0.3784` | `9.9081 ± 0.0639` | `0.7626 ± 0.0075` | `0.5517 ± 0.0106` |
| `split_decoupled_optim` | `17.6822 ± 0.3683` | `9.9102 ± 0.0682` | `0.7475 ± 0.0146` | `0.5311 ± 0.0253` |

额外观测到的一个关键现象是：

- `split_coupled_optim`
  - `common_branch_norm = 4.7361 ± 0.1452`
  - `tail_branch_norm = 5.1856 ± 0.1389`
- `split_decoupled_optim`
  - `common_branch_norm = 4.6236 ± 0.0465`
  - `tail_branch_norm = 10.9884 ± 0.3638`

这说明：

1. `split` 结构本身没有失效
2. 但“更高 LR + 更低 WD”的 tail-side 强解耦，并没有稳定变成更好的最终指标
3. 相反，它把 tail 分支推得明显更大，却没有带来更好的 `acc / NMI / ppl`

所以 `Phase 2` 的正式结论是：

> `shared head -> split` 这条结构主线还在，但 toy 里那种“LR + WD 同时强解耦”的 optimizer 配方，在真实单层长程训练里没有被支持。

### 3.3 Phase 3 的正式结果

`Phase 3` 的问题是：把 router 放到 `tail residual` 上，是否会形成更真实的 expert specialization。

长程双 seed 平均结果如下：

| config | dclm_ppl | wos_ppl | router_purity | router_nmi |
| --- | --- | --- | --- | --- |
| `flat_raw_uniform` | `17.4472 ± 0.3518` | `9.8355 ± 0.0685` | `0.7818 ± 0.0039` | `0.5820 ± 0.0065` |
| `tail_router_only` | `17.4755 ± 0.3590` | `9.7977 ± 0.0748` | `0.7826 ± 0.0130` | `0.5768 ± 0.0202` |
| `tail_router_decoupled_wd` | `17.4585 ± 0.3595` | `9.7936 ± 0.0664` | `0.7840 ± 0.0142` | `0.5808 ± 0.0227` |
| `tail_router_decoupled_wd_lr` | `17.7727 ± 0.3868` | `9.9174 ± 0.0403` | `0.7656 ± 0.0110` | `0.5447 ± 0.0073` |

这组结果最重要的含义不是“hierarchical 已经成功”，而是三点更细的判断：

1. `tail_router_decoupled_wd` 的 `router_purity` 和 `wos_ppl` 最好，说明 `tail residual + WD-only` 确实开始给出正信号
2. `flat_raw_uniform` 的 `dclm_ppl` 和 `router_nmi` 仍最好，说明它并没有被稳定打穿
3. `tail_router_decoupled_wd_lr` 明显最差，说明把 `LR` 也一起强解耦，在真实设置里反而会坏掉

所以 `Phase 3` 的正式结论是：

> `tail residual router` 是有希望的，但当前现实证据只支持 `WD-only` 的温和解耦，不支持 toy 里的 `WD + LR` 强解耦全家桶。

### 3.4 当前整条主线到达了什么位置

如果把三个阶段合在一起，当前最稳的结论是：

1. `Phase 1`：通过
   - `shared head` 存在
   - `tail residual` 更可分
2. `Phase 2`：未完全通过
   - `split` 值得保留
   - 但 `LR + WD` 强解耦没有被长程结果支持
3. `Phase 3`：部分通过
   - `tail residual router + WD-only` 有弱正信号
   - 但还不能说 hierarchical 路线已经闭环

因此，本轮现实实验对 toy 主线的真正修正是：

> 现实更支持“温和、选择性、与目标对齐的解耦”，而不支持“把 toy 中有效的每个强化手段原样叠到真实训练里”。

## 4. 各阶段指标到底在测什么

### 4.1 Phase 1 指标

在 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:275) 到 [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:302)，`Phase 1` 用了四个指标：

1. `probe_accuracy`
   - 用 `LogisticRegression` 在 train features 上训练、test features 上预测
   - 测的是“线性可分性”
2. `cluster_nmi`
   - 对 test features 做 `KMeans`
   - 再和真实 WoS domain 算 `normalized_mutual_info`
   - 测的是“无监督聚类与标签的一致性”
3. `cluster_purity`
   - 把聚类结果和真实类做最佳匹配后的纯度
4. `sep_trace`
   - 由 [fisher_trace_ratio](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:87) 定义
   - 即

$$
\mathrm{Sep}_{\mathrm{trace}}
=
\frac{\mathrm{tr}(B)}{\mathrm{tr}(W)},
$$

其中：

- $B$：类间散度矩阵的迹
- $W$：类内散度矩阵的迹

这一步测的是：

> “表示本身几何上是否更适合区分类别。”

不是测语言建模，也不是测真正 MoE specialization。

### 4.2 Phase 2 指标

在 [evaluate_config](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:402) 到 [run_phase2_split_ffn.py](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/scripts/run_phase2_split_ffn.py:456)，`Phase 2` 用了这些指标：

1. `dclm_ppl`
   - DCLM eval 上的 perplexity
   - 测 common/general 侧语言建模是否被破坏
2. `wos_ppl`
   - WoS eval 上的 perplexity
   - 测 domain 侧语言建模效果
3. `wos_domain_acc`
   - domain head 在 WoS test 上的分类准确率
4. `wos_domain_nmi`
   - domain 预测与真实标签的 NMI
5. `common_branch_norm / tail_branch_norm`
   - 两个 adapter 的参数范数
   - 用来观察有没有“tail 支路被推得异常大”

这一阶段的核心不是 purity，而是：

> “split + optimizer 设计，能不能在不损坏 LM 的前提下，把 domain 区分能力做上去。”

### 4.3 Phase 3 指标

在 [evaluate_config](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:414) 到 [run_phase3_hierarchical_moe.py](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:465)，`Phase 3` 用了这些指标：

1. `dclm_ppl`
2. `wos_ppl`
3. `router_purity`
   - 由 [routing_purity](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/scripts/run_phase3_hierarchical_moe.py:287) 定义
   - 真实 domain 与 expert assignment 做最佳置换后的纯度
4. `router_nmi`
   - expert assignment 与 domain label 的 NMI
5. `active_experts`
   - 占比超过 `1%` 的 experts 数
6. `expert_norm_mean`
   - expert 参数范数均值

这一阶段想测的是：

> “专家分工是否真的开始形成。”

但是要注意，这里测的是“对 WoS domain 标签的专业化”，不等于“对真实语言功能分解的专业化”。

## 5. 为什么 toy 里成立，现实里却没有稳定 work

下面是最关键的部分。  
我先给一句总判断：

> toy 里成立的是一个“机制切片”；现实里失败的，不是这个切片本身一定错，而是现实系统同时违反了 toy 背后的多个关键假设。

### 5.1 失效原因一：被删掉的 `shared head` 并不一定纯粹是 nuisance

toy 默认近似是：

$$
h = h_{\mathrm{shared}} + h_{\mathrm{tail}},
\qquad
y \perp h_{\mathrm{shared}} \mid h_{\mathrm{tail}},
$$

也就是：

- hidden state $h$ 可以拆成 shared 部分和 tail 部分
- 只要知道 $h_{\mathrm{tail}}$，标签 $y$ 和 $h_{\mathrm{shared}}$ 条件独立

在这个前提下，删掉 shared head 不会丢掉任务关键信息。

但真实模型更像：

$$
h = U a(x) + V b(x) + \varepsilon,
$$

其中：

- $x$：输入文本
- $U a(x)$：top-eigenspace 上的共享大方差分量
- $V b(x)$：残差子空间中的 tail 分量
- $\varepsilon$：剩余噪声

现实里并不保证：

$$
I(y; a(x) \mid b(x)) = 0.
$$

这里：

- $I(\cdot;\cdot\mid\cdot)$：条件互信息
- $y$：我们关心的标签，可能是 domain、next token 或 latent expert

如果

$$
I(y; a(x) \mid b(x)) > 0,
$$

那就说明 top 主方向里也含有有效语义。  
此时投影到 $U^\perp$ 会直接损失可用信号。

更直观一点，如果真实语义向量 $s$ 与被删掉子空间 $H_k$ 的夹角不是 $90^\circ$，那么删掉后保留下来的语义能量只有：

$$
\|P_{H_k^\perp}s\|^2
=
\|s\|^2 \sin^2 \theta,
$$

其中：

- $P_{H_k^\perp}$：投影到被删子空间正交补
- $\theta$：$s$ 与 $H_k$ 的主夹角

也就是说，只要 $\theta$ 不大，删 head 就会伤到语义本身。  
这可以解释：

- `Phase 1` 线性 probe 受益
- 但 `Phase 2/3` 的 generative 指标并不总是一起变好

因为 probe 看的是“区分几何”，而 LM 需要的是“预测有效信息”。

### 5.2 失效原因二：`Phase 1` 的“更可分”不等于 `Phase 2/3` 的“更可训练”

`Phase 1` 是在**文档级 pooled 表示**上测线性可分性：

$$
\bar h = \frac{1}{T}\sum_{t=1}^{T} h_t,
$$

其中：

- $h_t$：第 $t$ 个 token 的 hidden state
- $T$：文档长度
- $\bar h$：文档均值表示

均值池化会降低噪声方差。若 token 级噪声近似独立，

$$
\mathrm{Var}(\bar h) \approx \frac{1}{T}\mathrm{Var}(h_t).
$$

所以文档级 probe 更容易看到稳定 domain 结构。

但 `Phase 2/3` 的控制器是在**token 级 forward hook**上工作，训练时优化的是 token-level next-token loss。  
这意味着：

- `Phase 1` 证明的是“平均意义上的几何更干净”
- `Phase 2/3` 需要的是“每个 token 的局部状态都足够稳定地可利用”

这两者不是一回事。

因此，`Phase 1` 成功而 `Phase 2/3` 不完全成功，并不矛盾。  
它更像是在说：

> 几何线索存在，但还没有被当前这版单层控制器稳定地转成 token-level 训练收益。

### 5.3 失效原因三：辅助监督与 LM 目标可能梯度不对齐

`Phase 2` 和 `Phase 3` 的总损失都长这样：

$$
L = L_{\mathrm{LM}} + \lambda L_{\mathrm{aux}}.
$$

其中：

- `Phase 2` 里 $L_{\mathrm{aux}} = L_{\mathrm{dom}}$
- `Phase 3` 里 $L_{\mathrm{aux}} = L_{\mathrm{router}}$

设参数为 $\theta$，则总梯度为：

$$
\nabla_\theta L
=
\nabla_\theta L_{\mathrm{LM}}
+
\lambda \nabla_\theta L_{\mathrm{aux}}.
$$

如果两个梯度方向不一致，即

$$
\cos\angle\big(\nabla_\theta L_{\mathrm{LM}}, \nabla_\theta L_{\mathrm{aux}}\big) < 0,
$$

那就会出现：

- domain/router 指标在提升
- 但 language modeling 指标在受损

或者相反：

- 为了保住 LM
- 系统会自动压制 tail-side 的辅助分工

这可以解释 `Phase 2` 里的现象：

- `split_coupled_optim` 拿到了更好的 `WoS domain acc / NMI`
- 但 `baseline_ffn` 却保住了更好的 `ppl`

这不是简单的“谁更强”，而更像是在说：

> 当前 auxiliary objective 和 LM objective 之间还存在明显张力。

### 5.4 失效原因四：toy 里的 tail 梯度是“干净稀疏”，现实里的 tail 梯度是“稀疏且高噪声”

toy 里 tail 稀有，但信号结构很干净。  
真实训练里，tail 分支的更新不只是少，而且更噪。

设 tail 参数为 $\theta_t$，其更新近似写成：

$$
\theta_{t+1}
=
(1 - \eta_t \gamma_t)\theta_t
- \eta_t g_t,
$$

其中：

- $\eta_t$：学习率
- $\gamma_t$：等效 weight decay
- $g_t$：随机梯度

若 tail 只在概率 $p \ll 1$ 的 batch 上收到有效梯度，而这些梯度本身又带大噪声协方差 $\Sigma_{\xi}$，那么低 WD、高 LR 会把稳态方差抬高。  
粗略地，某一维上的稳态尺度满足：

$$
\mathbb{E}\|\theta\|^2
\propto
\frac{\eta^2 p \, \mathrm{tr}(\Sigma_{\xi})}{\eta \gamma}
=
\frac{\eta p \, \mathrm{tr}(\Sigma_{\xi})}{\gamma}.
$$

这说明：

- 增大学习率 $\eta$
- 降低权重衰减 $\gamma$

会在低信噪比场景里快速放大 tail 参数方差。

这和 `Phase 2` 的观测是对得上的：

- `split_decoupled_optim` 的 `tail_branch_norm` 明显大于 coupled
- 但指标并没有更好

说明 tail 并不是“死了”，而更像是“被推过头了”。

### 5.5 失效原因五：当前真实实验的控制器容量太小，近似误差可能主导结果

`Phase 2/3` 训练的都不是完整 backbone，而是单层 low-rank controller。

若理想修正映射是 $\Delta W^\star$，而我们只能用秩不超过 $r$ 的更新：

$$
\Delta W = BA,
\qquad
\mathrm{rank}(\Delta W) \le r,
$$

那么只要

$$
\|\Delta W^\star - \Delta W\|_F
$$

还很大，真实任务上的误差就可能被“函数近似能力不足”主导，而不是被表示几何本身主导。

更具体地说，当前设置同时有几个强约束：

- 只改一层
- 只在 `post-attention / pre-FFN` 注入
- adapter rank 很小
- backbone 完全冻结

所以真实系统很可能处于这样一种状态：

> `Phase 1` 找到了一个好几何，但 `Phase 2/3` 这套小模块还没有足够表达能力去把这份几何优势吃满。

### 5.6 失效原因六：`Phase 3` 的 router supervision 和真实 specialization 目标并不完全等价

`Phase 3` 的 router loss 是：

$$
L_{\mathrm{router}}
=
\mathrm{CE}(r(x), y_{\mathrm{domain}}),
$$

其中：

- $r(x)$：router logits
- $y_{\mathrm{domain}}$：WoS 的人工 domain 标签

但真实的 expert specialization 更像是在学习某个潜在功能划分 $z^\star$，而不是简单复制 WoS domain 标签。  
如果真实最优 expert assignment 是 $z^\star$，而非 $y_{\mathrm{domain}}$，那么最大化：

$$
I(E; y_{\mathrm{domain}})
$$

并不等于最大化：

$$
I(E; z^\star).
$$

这里：

- $E$：expert assignment 随机变量
- $I(\cdot;\cdot)$：互信息

这就会导致一种很微妙的情况：

- `router_purity / NMI` 相对 domain 标签很好
- 但语言建模未必更好

或者反过来：

- 一个更利于 LM 的 routing
- 未必更对齐人工 domain 标签

所以 `Phase 3` 现在的评价标准，本质上仍然是一个 supervised proxy，不是最终的 specialization 真值。

### 5.7 失效原因七：toy 研究的是“有限训练窗口里的 starvation”，而长程实验会让 coupled 方案追上来

toy 里的核心命题之一是：

> 统一 WD / LR 会让 tail 在有限训练预算内学不起来。

这本质上是一个**有限时长动力学命题**，不是说 coupled 在无穷长时间下一定更差。

如果记某个方案在训练步数 $T$ 下的性能为 $M(T)$，那么 toy 更关心的是有限窗口：

$$
M_{\mathrm{decoupled}}(T) - M_{\mathrm{coupled}}(T)
\quad \text{在中等 } T \text{ 下是否显著为正。}
$$

而不是

$$
\lim_{T \to \infty} M_{\mathrm{decoupled}}(T)
>
\lim_{T \to \infty} M_{\mathrm{coupled}}(T).
$$

这也能解释为什么：

- 小规模或短程时 decoupled 有正信号
- 拉长训练后 coupled 追了上来，甚至反超

这未必说明 toy 错了。  
更可能说明：

> 现实中的这套单层 proxy，已经给了 coupled 足够多的时间去弥补早期 starvation。

但与此同时，这也暴露出另一个问题：

> 如果一个方法只在很短的 transient 里有效，却不能稳定转成更好的终态，那它在真实系统里的工程价值就会下降。

## 6. 怎样理解那些“不符合直觉”的结果

### 6.1 为什么 `Phase 1` 明明是正结论，`Phase 2` 却没有稳定赢

最容易误解的地方就在这里。  
这两者并不冲突，因为它们回答的问题不同：

- `Phase 1`：几何上有没有更干净的子空间
- `Phase 2`：当前这版单层 split controller，能不能把这份几何优势稳定变成训练收益

`Phase 1` 的成功说明：

- 主线不是空想
- `shared head` 确实存在

`Phase 2` 的犹豫说明：

- 几何优势不自动等于优化优势
- 当前控制器与损失设计还不足以稳定吃到这份优势

### 6.2 为什么 `WD-only` 在 `Phase 3` 里比 `WD+LR` 更靠谱

这恰恰是最值得学习的结果之一。  
它说明 toy 里“tail 需要更持久 LR”这个命题，在现实系统里并不是可以直接照搬的。

更可能的现实情况是：

- 低 WD 先帮助 rare experts 不被过度压缩
- 但再叠加强 LR，会让 noisy tail gradients 被放大得过头

于是 `WD-only` 成为一个比较稳的折中点：

- 既保留 tail
- 又不至于把 tail 学成高方差不稳定分支

### 6.3 为什么 `flat_raw_uniform` 还会在某些指标上更强

这通常意味着 raw hidden 里仍然保留了大量“对当前监督任务直接有用”的 coarse 信息。

也就是说，raw hidden 可能同时包含两种东西：

1. 会干扰专业化的 shared nuisance
2. 对当前 domain 预测或 LM 又确实有帮助的 coarse 语义

当前的 projector 还没把这两者完全分开，所以 raw baseline 还能靠“粗但全”的特征吃到一部分优势。

## 7. 我对当前主线的判断

如果只看这轮真实实验，我会把主线更新成下面这个版本：

1. `Phase 1` 已经证明：
   - “shared head 存在”这件事是真的
2. `Phase 2` 说明：
   - split 结构值得继续
   - 但当前这版 optimizer 解耦策略过于理想化
3. `Phase 3` 说明：
   - tail residual router 是有希望的
   - 但最稳的版本更像是 `WD-only`，而不是 toy 里的强解耦全家桶

所以真正被现实修正掉的，不是“解耦”主线本身，而是它的**强版本**：

> 现实更支持“温和、选择性、与目标对齐的解耦”，而不支持“把 toy 里验证过的每个强化手段都原样叠上去”。

## 8. 接下来最值得做什么

从理论和实现两个角度看，下一步最值得做的是：

1. 保留 `tail residual router`
2. 暂时只保留 `WD-only decoupling`
3. 重做 `Phase 3` 的目标函数，而不是先继续放大算力

最关键的改动方向是：

- 降低当前 supervised domain label 对 router 的强绑定
- 让 router 目标更贴近“对 LM 有帮助的 specialization”
- 检查多层、而不是单层 projector / controller

一句话概括：

> toy 证明了“为什么解耦可能有效”，真实实验告诉我们“什么样的解耦方式太理想化了”。
