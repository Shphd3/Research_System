# 从 Toy 到 Phase6：`exp_hierarchical` 的完整故事线、实验意义与当前主线

## 1. 这份文档是干什么的

这份文档不是某一个 phase 的实验报告，而是一份“学习型总说明”。

它要解决五个问题：

1. 我们这条研究主线到底是什么。
2. 我们为什么没有一开始就直接训练一个更大的 Hierarchical MoE。
3. `Phase2` 到 `Phase6` 每个实验具体想证明什么，具体做了什么，最后证明了什么。
4. 为什么我们现在能下某些结论，但还不能下更强的结论。
5. 如果我要花一个小时重新理解整条线，应该怎样把这些实验串成一个连续故事。

这份文档建议的阅读方式是：

- 先看第 2 节和第 3 节，抓住主线。
- 再按顺序看第 4 节到第 9 节，理解每一个阶段。
- 最后看第 14 节到第 19 节，明确“当前最稳的结论是什么”“我们现在到底 reach 到哪里”，以及 `Phase6` 到底新增了什么。

---

## 2. 整条研究主线到底是什么

如果把整条线压缩成一句话，我们真正想回答的问题是：

$$
\text{Flat MoE 在 long-tail 场景下为什么学不好，而 Hierarchical / split-first 架构是否真的更优？}
$$

这个问题又可以拆成三个更小的问题：

1. Flat MoE 的问题是不是先发生在表示层，也就是 router 看到的 hidden state 本身就已经被共享高方差结构“带偏”了。
2. 如果表示层确实有这种 shared head，那么先把 common 和 tail 分开，再让 router 只看 tail，会不会比 flat raw routing 更合理。
3. 如果单层 hierarchical 已经成立，那么 tail 内部是否还值得继续递归拆分。

所以整条主线不是“做一个更大的 MoE”，而是：

$$
\text{shared head} \rightarrow \text{split-first} \rightarrow \text{tail-conditioned routing} \rightarrow \text{recursive hierarchy?}
$$

更具体地说，我们到今天为止一直在试图建立下面这个命题链：

$$
\text{真实模型中存在 shared head}
$$

$$
\Downarrow
$$

$$
\text{把 hidden 先分成 common 和 tail，是有几何意义的}
$$

$$
\Downarrow
$$

$$
\text{router 不该直接看 raw hidden，而应看 tail residual}
$$

$$
\Downarrow
$$

$$
\text{在控制变量后，single-layer hierarchical routing 应该优于 flat raw routing}
$$

$$
\Downarrow
$$

$$
\text{如果 tail 内部还有层次结构，再问 recursive hierarchy 是否成立}
$$

今天这条线已经走到第四步的后半段。也就是说：

- 前三步已经有比较扎实的证据。
- 第四步已经不只是“真实正结果”，而且已经出现了 `LM-relevant specialization` 证据。
- 第五步还没有成立，但它的 primary bottleneck 已经被进一步定位到了 `coarse routing`。

---

## 3. 为什么这条线要分成 Toy、Phase1、Phase2、Phase3、Phase4、Phase5、Phase6

我们没有一开始就直接训练完整 Hierarchical MoE，是因为那样变量太多，无法知道最后看到的现象到底来自哪里。

所以我们采用了“逐层剥离变量”的策略。

### 3.1 Toy 阶段要回答的事情

Toy 阶段不追求真实模型性能，只追求回答“机制是否存在”。

它主要回答四件事：

1. `exp_tail_router`
   - router 会不会被 raw hidden 里的 shared geometry 致盲。
2. `exp_tail_special`
   - 去均值是否足够，还是必须去掉 shared covariance head。
3. `exp_tail_decay`
   - 统一 `weight decay` 会不会系统性压死 tail。
4. `exp_tail_lr`
   - 全局 `learning rate decay` 会不会过早关闭 tail 的学习窗口。

Toy 阶段最后得到的是两个大结论：

$$
\text{问题既来自表示几何，也来自优化动力学}
$$

以及

$$
\text{先 split 再处理 tail，是比 flat 混在一起更合理的方向}
$$

### 3.2 `exp_hierarchical` 要回答的事情

进入 `exp_hierarchical` 以后，我们不再问“机制能不能存在”，而开始问：

$$
\text{这些 toy 机制，能不能迁移到真实大模型 hidden state 和真实 token-level 训练里？}
$$

因此：

- `Phase1` 只审计真实 hidden state 的几何。
- `Phase2` 先用最小 split controller 测结构和优化。
- `Phase3` 再用最小 MoE proxy 测 tail-conditioned router。
- `Phase4` 直接回到真实 block 本体，不再只做 proxy。
- `Phase5` 在真实 block 已经出现正结果后，进一步控制变量，问收益到底来自 split、容量还是 routing，并测试 recursive hierarchy。

这就是为什么这些 phase 看起来很多，但其实是同一条逻辑链的连续分段。

---

## 4. Toy 阶段到底给我们留下了什么

### 4.1 `exp_tail_router`

这个实验最早建立的命题是：

$$
\text{router 失败，可能不是因为 load balance 没做好，而是因为它看到的表示本身就不对。}
$$

它说明 raw hidden 里会有很强的 shared structure，这个结构会让 router 更容易响应 common variation，而不是 rare semantic variation。

这一步给后面留下的最重要问题是：

$$
\text{如果 router 被表示几何带偏，那么我们必须先改表示，再谈 routing。}
$$

### 4.2 `exp_tail_special`

这个实验把“改表示”进一步讲清楚了。它不是简单地说“做个 centering 就好”，而是说明：

$$
\text{raw} \rightarrow \text{centered}
$$

往往不够，真正关键的是：

$$
x_t = (I - V_k V_k^\top)(x-\mu)
$$

其中：

- $\mu$ 是均值。
- $V_k$ 是 centered covariance 的前 $k$ 个主方向。
- $x_t$ 是删掉 shared covariance head 后的 tail residual。

这一步还给出了一个很重要的条件命题：

$$
\text{只有当被删掉的子空间主要承载 shared nuisance，而不是 label-relevant semantics 时，head removal 才会有益。}
$$

也就是说，head removal 从来不是无条件正确的。

### 4.3 `exp_tail_decay`

这个实验说明：

$$
\text{统一 WD 会系统性压低 tail 参数的稳态上限。}
$$

所以 tail 在 flat 结构中吃亏，并不一定是因为表达能力不够，也可能是因为：

$$
\text{common 和 tail 共用同一组正则化条件。}
$$

### 4.4 `exp_tail_lr`

这个实验说明：

$$
\text{全局 LR 衰减会先被 common 驱动，而 tail 还没学够时，学习窗口就已经被关掉。}
$$

因此，toy 阶段最后形成的完整直觉是：

$$
\text{Flat MoE 的失败既有 geometry 通道，也有 optimization 通道。}
$$

不过，到了今天，我们已经把这两个通道的重要性重新排序了：

- 早期我们同时非常关心 `WD` 和 `LR`。
- 现在进入 `Phase5` 以后，我们更清楚地知道：当前真正最重要的是先回答架构本体是否优越。

也就是说，现在最应该优先关注的是：

$$
\text{Hier 这种 split-first 架构本身是否优于 flat。}
$$

而不是先执着于：

$$
\text{WD 或 LR 的最优解耦配方到底是什么。}
$$

---

## 5. `Phase1`：真实 hidden state 中到底有没有 shared head

目的：验证真实 hidden 里是否存在 shared head，以及去掉它后 `tail residual` 是否更可分。

数据：`DCLM + WoS`，协方差池比例 `4:1`。

模型：`Qwen3-8B`。

步骤：在 `post-attention / pre-FFN` 位置，扫描 `layer 5/11/23/35` 和 `rank 4/8/16/32/64`；比较 `raw`、`centered`、`tail_residual`；评估 `probe accuracy / purity / NMI / Sep_trace`。

结论：真实 hidden 里确实有 shared head，单纯去 mean 不够，`tail_residual` 在最佳层稳定更可分。

为什么能得出：两个正式 seed 上都复现，且 `purity / NMI / probe accuracy` 都稳定提升；同时 `layer 35` 的前 `8` 个主方向累计解释方差约为 `0.4069`。

更新作用：强力支持 `H1 [Shared-Head Hypothesis]`。

重点标签：真实 `shared-head` 证据。

对应主要文档：

- [00_research_mainline_and_current_status.md](./00_research_mainline_and_current_status.md)
- [detailed_phase1_metrics_and_root_cause_report.md](../phase1_real_representation_probe/docs/detailed_phase1_metrics_and_root_cause_report.md)
- [report_qwen3_8b_phase1_local.md](../phase1_real_representation_probe/docs/report_qwen3_8b_phase1_local.md)

### 5.1 `Phase1` 想证明什么

`Phase1` 的问题非常基础：

$$
\text{在真实 Qwen hidden state 里，shared head 是否真的存在？}
$$

以及：

$$
\text{如果把这个 shared head 切掉，tail residual 是否更可分？}
$$

### 5.2 `Phase1` 具体做了什么

这一步不训练 backbone，只做表示审计。

具体步骤是：

1. 加载冻结的 `Qwen3-8B`。
2. 选择若干候选层。
3. 在这些层的 `post_attention_layernorm` 位置抓 hidden state。
4. 用 `DCLM + WoS` 的混合数据估计均值和协方差。
5. 对 centered covariance 做特征分解。
6. 构造三种表示：
   - `raw`
   - `centered = h - \mu`
   - `tail_residual = (I - V_k V_k^\top)(h-\mu)`
7. 在 WoS 上比较这些表示的：
   - 线性 probe accuracy
   - cluster purity
   - cluster NMI
   - Fisher-style separability
   - eigenspectrum

### 5.3 `Phase1` 测了哪些指标

第一类指标是谱结构。

如果 centered covariance 的特征值写成：

$$
\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_d \ge 0,
$$

那么前 $k$ 个方向的累计解释方差是：

$$
E_k = \frac{\sum_{i=1}^{k}\lambda_i}{\sum_{j=1}^{d}\lambda_j}.
$$

如果 $E_k$ 在很小的 $k$ 上就很大，就说明 shared variance 很集中，存在明显的低秩 head。

第二类指标是 separability。

对标签 $z$，类间散度和类内散度分别写为：

$$
B_z = \sum_c \pi_c (\mu_c-\mu)(\mu_c-\mu)^\top,
$$

$$
W_z = \sum_c \pi_c \operatorname{Cov}(x \mid z=c).
$$

理论上定义的 Fisher-style separability 是：

$$
\operatorname{Sep}_F(P;z) = \frac{\operatorname{tr}(P B_z P^\top)}{\operatorname{tr}(P W_z P^\top)}.
$$

第三类指标是更直观的 operational metrics：

- probe accuracy
- purity
- NMI

它们回答的问题是：

$$
\text{这份表示是否更容易被简单分类器和聚类结构利用。}
$$

### 5.4 `Phase1` 得到了什么结论

这是目前最稳的一个 phase。

关键结论是：

1. `raw` 和 `centered` 几乎重合。
2. 最优层稳定落在 `layer 35`。
3. 最优 `k` 稳定在 `16~32`。
4. `tail_residual` 的 probe accuracy、purity、NMI 都稳定优于 `raw / centered`。

代表性结果是：

- seed1：`raw acc 0.7522 -> tail_residual acc 0.7690`
- seed2：`raw acc 0.7444 -> tail_residual acc 0.7511`

而且 `layer 35` 的前 `8` 个主方向累计解释方差大约达到 `0.4069`，这说明低秩 shared head 的确存在。

所以 `Phase1` 证明的核心不是“head removal 已经改善了真实语言建模”，而是：

$$
\text{真实 hidden geometry 中确实存在 shared head；tail residual 的几何更利于语义区分。}
$$

这是后面所有结构实验的地基。

---

## 6. `Phase2`：split controller + optimizer decoupling 能不能把几何优势变成训练收益

目的：验证把单层控制器拆成 `common branch + tail branch` 后，是否已经能把 `Phase1` 的几何优势转成训练收益；同时检查 toy 里看起来重要的优化解耦，在真实训练里是不是主矛盾。

数据：`DCLM + WoS` 混合训练数据；同时使用 `next-token LM` 与 `WoS domain` 辅助监督。

模型：冻结 `Qwen3-8B` backbone，只在单层插入一个最小 `split controller`。

步骤：比较 `baseline_ffn`、`split_coupled_optim`、`split_decoupled_optim`；其中 split 形式为

$$
h_c = V_k V_k^\top (h-\mu), \qquad
h_t = (I - V_k V_k^\top)(h-\mu),
$$

并学习

$$
\Delta h = f_c(h_c) + f_t(h_t).
$$

评估 `DCLM PPL / WoS PPL / WoS domain acc / WoS domain NMI / tail_branch_norm`。

结论：`split` 这条结构方向保住了，但 toy 里的强优化解耦配方没有在真实训练里直接复现；`tail branch` 被推大，不等于主指标更好。

为什么能得出：双 seed 长程结果里，`split_coupled_optim` 的 domain 指标优于 baseline，而 `split_decoupled_optim` 虽然把 `tail_branch_norm` 推到更大，却没有带来更好的 `PPL / NMI`。

更新作用：桥接支持 `H2 [Single-Layer Split-First Hypothesis]`，同时削弱“`WD/LR` 解耦是当前主矛盾”这一判断。

重点标签：真实训练里的 `split controller` 桥接验证。

对应主要文档：

- [phase123_understanding_and_failure_analysis.md](../phase123_joint_analysis/docs/phase123_understanding_and_failure_analysis.md)
- [Phase 2 long-run summary](../phase2_split_ffn_decoupling/results/local_1h_len256_summary/phase2_results_mean_std.md)
- [report_local_1h_len256.md](../phase2_split_ffn_decoupling/docs/report_local_1h_len256.md)

### 6.1 `Phase2` 想证明什么

`Phase1` 已经说服我们：tail residual 在几何上更干净。

`Phase2` 接着问：

$$
\text{如果把单层控制器拆成 common branch 和 tail branch，再给 tail 更特殊的 optimizer，是否能在真实训练里获益？}
$$

### 6.2 `Phase2` 具体做了什么

它仍然冻结整个 `Qwen3-8B` backbone，只在单层插一个很小的控制器。

这一步比较三组：

- `baseline_ffn`
- `split_coupled_optim`
- `split_decoupled_optim`

其中 split 的核心是：

$$
h_c = V_k V_k^\top (h-\mu), \qquad
h_t = (I - V_k V_k^\top)(h-\mu)
$$

然后学习：

$$
\Delta h = f_c(h_c) + f_t(h_t),
$$

$$
\tilde h = h + \Delta h.
$$

训练目标是：

$$
L = L_{\mathrm{LM}} + \lambda_{\mathrm{dom}} L_{\mathrm{dom}},
$$

其中：

- $L_{\mathrm{LM}}$ 是 next-token cross-entropy。
- $L_{\mathrm{dom}}$ 是 WoS domain 分类交叉熵。

### 6.3 `Phase2` 最后证明了什么

双 seed 长程结果显示：

- `baseline_ffn`
  - `dclm_ppl = 17.5479 ± 0.3694`
  - `wos_ppl = 9.8634 ± 0.0628`
  - `wos_domain_acc = 0.7511 ± 0.0063`
  - `wos_domain_nmi = 0.5428 ± 0.0056`
- `split_coupled_optim`
  - `dclm_ppl = 17.6052 ± 0.3784`
  - `wos_ppl = 9.9081 ± 0.0639`
  - `wos_domain_acc = 0.7626 ± 0.0075`
  - `wos_domain_nmi = 0.5517 ± 0.0106`
- `split_decoupled_optim`
  - `dclm_ppl = 17.6822 ± 0.3683`
  - `wos_ppl = 9.9102 ± 0.0682`
  - `wos_domain_acc = 0.7475 ± 0.0146`
  - `wos_domain_nmi = 0.5311 ± 0.0253`

同时：

- `split_coupled_optim` 的 `tail_branch_norm` 大约是 `5.19`
- `split_decoupled_optim` 的 `tail_branch_norm` 大约是 `10.99`

也就是说，`split_decoupled_optim` 的 tail 分支确实被“推大了”，但指标没有变好。

所以 `Phase2` 的结论非常关键：

$$
\text{split 这条主线保住了，但 toy 里的强优化解耦配方没有在真实训练里直接复现。}
$$

这告诉我们两件事：

1. `split` 作为结构方向是值得继续的。
2. 真实训练里的问题不能简单归结为“tail 只要更高 LR、更低 WD 就好”。

这也是后来我们逐渐把注意力从 `WD/LR` 重新转回“架构本体”的原因之一。

---

## 7. `Phase3`：把 router 放到 tail residual 上，会不会比 flat raw router 更合理

目的：验证 `tail-conditioned routing` 是否比 `flat raw routing` 更合理，也就是 router 不直接看 raw hidden，而改看 `tail residual` 后，是否会出现更好的 specialization 或更好的主任务方向。

数据：`DCLM + WoS` 混合训练数据，仍带有 `WoS domain` 这一 proxy supervision。

模型：冻结 `Qwen3-8B` backbone，只训练一层最小 `MoE proxy`。

步骤：比较 `flat_raw_uniform`、`tail_router_only`、`tail_router_decoupled_wd`、`tail_router_decoupled_wd_lr`；核心差异是 flat 组使用

$$
u = \sum_i g_i(x) E_i(x),
$$

而 tail router 组使用

$$
u = f_c(h_c) + \sum_i g_i(h_t) E_i(h_t).
$$

评估 `DCLM PPL / WoS PPL / router purity / router NMI`。

结论：`tail-conditioned routing` 已经开始出现弱正信号，但 proxy 证据仍不闭环；强 `WD+LR` 解耦明显最差。

为什么能得出：双 seed 长程结果里，`tail_router_only` 与 `tail_router_decoupled_wd` 在 `WoS PPL / router purity` 上开始出现弱改善，但 `flat_raw_uniform` 仍在部分指标上很强，说明这一步只能给方向性支持，不能当最终证据。

更新作用：弱支持 `H2`，并直接推动研究从 proxy 转向真实 block 本体验证。

重点标签：`tail-conditioned routing` 的 proxy 验证。

对应主要文档：

- [phase123_understanding_and_failure_analysis.md](../phase123_joint_analysis/docs/phase123_understanding_and_failure_analysis.md)
- [Phase 3 long-run summary](../phase3_hierarchical_moe/results/local_1h_len256_summary/phase3_results_mean_std.md)
- [report_local_1h_len256.md](../phase3_hierarchical_moe/docs/report_local_1h_len256.md)

### 7.1 `Phase3` 想证明什么

`Phase2` 只做了 split controller，还没有真正触及 MoE 风格的 routing。

`Phase3` 的问题是：

$$
\text{如果 router 只看 tail residual，而不是直接看 raw hidden，是否会产生更好的 specialization？}
$$

### 7.2 `Phase3` 具体做了什么

仍然冻结 `Qwen3-8B` backbone，只训练一层最小 MoE proxy。

比较四组：

- `flat_raw_uniform`
- `tail_router_only`
- `tail_router_decoupled_wd`
- `tail_router_decoupled_wd_lr`

最关键的结构差异是：

flat 组做的是：

$$
u = \sum_i g_i(x) E_i(x),
$$

也就是 router 和 experts 都看原始 hidden $x$。

tail router 组做的是：

$$
u = f_c(h_c) + \sum_i g_i(h_t) E_i(h_t),
$$

也就是：

- common branch 看 common 分量
- router 只看 tail residual
- tail experts 也只看 tail residual

### 7.3 `Phase3` 最后证明了什么

双 seed 长程结果是：

- `flat_raw_uniform`
  - `dclm_ppl = 17.4472 ± 0.3518`
  - `wos_ppl = 9.8355 ± 0.0685`
  - `router_purity = 0.7818 ± 0.0039`
  - `router_nmi = 0.5820 ± 0.0065`
- `tail_router_decoupled_wd`
  - `dclm_ppl = 17.4585 ± 0.3595`
  - `wos_ppl = 9.7936 ± 0.0664`
  - `router_purity = 0.7840 ± 0.0142`
  - `router_nmi = 0.5808 ± 0.0227`
- `tail_router_only`
  - `dclm_ppl = 17.4755 ± 0.3590`
  - `wos_ppl = 9.7977 ± 0.0748`
  - `router_purity = 0.7826 ± 0.0130`
  - `router_nmi = 0.5768 ± 0.0202`
- `tail_router_decoupled_wd_lr`
  - `dclm_ppl = 17.7727 ± 0.3868`
  - `wos_ppl = 9.9174 ± 0.0403`
  - `router_purity = 0.7656 ± 0.0110`
  - `router_nmi = 0.5447 ± 0.0073`

这说明：

1. `tail_router_only` 和 `tail_router_decoupled_wd` 已经开始出现弱正信号。
2. `WD+LR` 强解耦明显最差。
3. 但 `flat_raw_uniform` 仍然在部分指标上非常强。

所以 `Phase3` 的最合理结论是：

$$
\text{tail-conditioned routing 值得继续，但 proxy 证据还不够闭环。}
$$

换句话说，`Phase3` 不能支持“Hierarchical MoE 已经成立”，它只能支持“这条结构方向值得继续，而且 LR 解耦暂时不该再作为主线”。

---

## 8. 为什么 `Phase2/3` 不够，必须进入 `Phase4`

这一步非常重要，因为它决定了后面整个研究方向为什么会转向“真实 block 本体”。

### 8.1 第一个原因：mixed-gradient problem

在 toy 里，tail 模块近似是 tail-only 接受更新的。

但在真实 `Phase2/3` 中，tail 参数的期望梯度更接近：

$$
\mathbb{E}[g(\theta_t)]
=
q\,\mathbb{E}[\nabla_{\theta_t}L_{\mathrm{LM}}^{\mathrm{common}}]
+
(1-q)\,\mathbb{E}[\nabla_{\theta_t}L_{\mathrm{LM}}^{\mathrm{tail}}]
+
(1-q)\lambda\,\mathbb{E}[\nabla_{\theta_t}L_{\mathrm{aux}}].
$$

意思是：

- tail 模块并不是只在 tail token 上学习
- 它同时承受 common-side LM 梯度、tail-side LM 梯度和辅助目标梯度

所以 `Phase2/3` 的结果很难被解释成“Hierarchical 架构本体到底行不行”。

### 8.2 第二个原因：router objective mismatch

真实 specialization 更接近这个目标：

$$
E^\star = \arg\min_E H(X_{t+1}\mid C,E),
$$

也就是：

$$
\text{最优 expert assignment 应该帮助 next-token prediction。}
$$

但 `Phase3` 的 router 还在优化更像下面的东西：

$$
\operatorname{CE}(r(x), y_{\mathrm{domain}}).
$$

也就是：

$$
\text{domain label supervised router}
$$

这只能算 proxy，不是最终目标。

所以进入 `Phase4` 的逻辑不是“之前都失败了”，而是：

$$
\text{之前的 proxy 已经不够干净，我们必须直接验证 block 架构本体。}
$$

---

## 9. `Phase4`：第一次直接验证真实 block 架构本体

目的：第一次直接验证真实 block 层面的 `split-first hierarchical` 架构，是否优于 `flat raw routing block`；同时把 `LB`、`projector`、`WD-only` 这些边界问题分开看清。

数据：`A1/A2/B1` 使用 synthetic small-model 数据；`C1` 使用真实 `DCLM + WoS` block replacement 训练与评测。

模型：`A1/A2/B1` 为 small-model；`C1` 为冻结 `Qwen3-0.6B`，只替换单层 `FFN block`。

步骤：`A1` 用 `oracle split` 测结构本体；`A2` 比较 `with_lb / no_lb`；`B1` 比较 `oracle / PCA / random projector`；`C1` 在真实 `Qwen3-0.6B layer 8` 上比较 `baseline / flat / hier / wd-only`。

结论：`split-first` 在 small-model 上已经明显优于 flat；在真实单层 block 上，`hier_moe_tail_uniform` 已优于 `baseline_ffn` 和 `flat_moe_raw_uniform`；但 `estimated projector` 还没有稳定替代 `oracle split`，`WD-only` 也不是这轮正结果的主要来源。

为什么能得出：`A1` 的 rare-tail PPL 排序支持 `split-first > flat`；`C1` 中

$$
81.5287 < 84.0007 < 85.0412
$$

对应 `hier < baseline < flat`；同时 `B1` gate 失败，且 `hier_moe_tail_wdonly` 与 `hier_moe_tail_uniform` 基本重合。

更新作用：强支持 `H2` 的“真实单层 block 架构优越性”，但不支持“projector 已经闭环”。

重点标签：第一次真实 block-level 正结果。

对应主要文档：

- [revised_hierarchical_moe_experiment_design.md](../phase4_real_hierarchical_moe/docs/revised_hierarchical_moe_experiment_design.md)
- [phase4_experiment_report.md](../phase4_real_hierarchical_moe/docs/phase4_experiment_report.md)
- [phase4_theory_ai_handoff_detailed.md](../phase4_real_hierarchical_moe/docs/phase4_theory_ai_handoff_detailed.md)

`Phase4` 是整条线的第一次关键收束。它不再只做 proxy，而是直接问：

$$
\text{Hierarchical block 本体是否优于 flat raw routing block？}
$$

如果你第一次读这篇文档，`A1/A2/B1/C1` 这些代号其实可以直接翻译成人话：

- `A` 组
  - `small-model / oracle split` 组
  - 用最干净的小模型条件先测“结构本体值不值得做”
- `B` 组
  - `projector replacement` 组
  - 问 estimated projector 能不能替代 oracle split
- `C` 组
  - `real-model main experiment` 组
  - 直接回到真实 `Qwen3-0.6B` 单层 block 上验证主命题

更具体地说：

- `A0`
  - 基础设施 sanity
  - 只检查脚本、指标、参数预算对齐是否正常，不承担科学结论
- `A1`
  - `oracle split` 小模型主实验
  - 在“已知真实 common/tail 切分”的最干净条件下比较 `dense / flat / split / hier`
  - 它回答的是：“split-first 这种结构本体值不值得做？”
- `A2`
  - `load balance` 小模型消融
  - 只问 mild `LB` regularizer 是否必要
- `B1`
  - `estimated projector` 替代实验
  - 把 oracle split 换成 `PCA/random projected`，问 projector 主线是否已经闭环
- `C1`
  - 真实 `Qwen3-0.6B` 单层主实验
  - 在真实 block replacement 上直接比较 `baseline / flat / hier / wd-only`
  - 它回答的是：“真实 block 本体是否已经优于 flat raw block？”

### 9.1 `Phase4` 的五个实验块分别干什么

#### `A0`

基础设施 sanity，不承担科学结论。

#### `A1`

小模型 + oracle split，比较：

- `G0_dense`
- `G1_flat`
- `G2_split_dense`
- `G3_hier_uniform`
- `G4_hier_wdonly`

这里的目标是最小化变量，把“split-first”这件事本身测出来。

#### `A2`

比较 `with_lb` 和 `no_lb`，问 mild load balance regularizer 是否必要。

#### `B1`

问 estimated projector 能不能替代 oracle split。

这里要比较：

- `oracle_hier_*`
- `pca_hier_*`
- `random_projected_hier`

而且 `pca_hier_*` 还要区分：

- `projector_source = dense`
- `projector_source = flat`

#### `C1`

回到真实 `Qwen3-0.6B`，做单层 block replacement。

这一步是 `Phase4` 的真正闭环点。

### 9.2 `A1`：`oracle split` 小模型主实验，最后证明了什么

`A1` 的核心 rare-tail PPL 排序是：

- `G2_split_dense = 30552.3 ± 23197.9`
- `G3_hier_uniform = 31358.6 ± 23652.0`
- `G4_hier_wdonly = 31365.8 ± 22757.6`
- `G0_dense = 31475.7 ± 22931.5`
- `G1_flat = 31995.6 ± 24317.1`

这说明：

$$
\text{split-first 明显优于 flat raw route。}
$$

但也说明：

$$
\text{最强收益首先来自 split，本轮不要夸大 routing。}
$$

因为 `split_dense` 比 `hier` 还略强。

### 9.3 `A2`：small-model `LB` 消融，最后证明了什么

这一步很有意思，因为它推翻了一种先验直觉。

结果显示，在当前小模型设置里：

- `no_lb` 常常不比 `with_lb` 差
- 有时甚至更好

因此 `A2` 的结论不是“LB 一定必要”，而是：

$$
\text{当前 synthetic 设置下，LB 不是主线问题。}
$$

### 9.4 `B1`：`estimated projector` 替代实验，最后证明了什么

`B1` 是 `Phase4` 的一个关键负结果。

理论上，我们希望：

$$
\text{pca\_hier} \approx \text{oracle\_hier} > \text{random\_projected}
$$

但实际 gate 结果是：

- `b1_pass = false`
- 最优 `pca_hier` 没有稳定压过最优 `random_projected`

这说明：

$$
\text{estimated projector 主线在这一轮还没有成立。}
$$

这是一个非常重要的现实约束，因为它意味着：

$$
\text{真实模型里 single-layer hierarchical 的正结果，还不能归功于“我们已经学会了 projector”。}
$$

### 9.5 `C1`：真实 `Qwen3-0.6B` 单层主实验，最后证明了什么

这是 `Phase4` 最重要的正结果。

真实 `Qwen3-0.6B`、单层 `layer 8`、`k=16`、`frozen` 设置下：

- `baseline_ffn`：`WoS rare-token PPL = 84.0007`
- `flat_moe_raw_uniform`：`WoS rare-token PPL = 85.0412`
- `hier_moe_tail_uniform`：`WoS rare-token PPL = 81.5287`

而且：

- `hier_moe_tail_wdonly`
  在 `gamma_ratio = 1.0 / 0.3 / 0.1` 时都与 `hier_moe_tail_uniform` 重合

因此 `Phase4` 最关键的结论是：

$$
\text{在真实模型单层 block 上，hierarchical tail-conditioned block 已经优于 baseline 和 flat raw MoE。}
$$

但它也同时告诉我们：

$$
\text{WD-only 不是这轮正结果的主要来源。}
$$

这正好和你现在的判断一致：现阶段更应该把 `WD` 放在一边，先把“架构是否优越”这个问题讲清楚。

---

## 10. `Phase5`：先控制变量拆清单层收益，再测试 recursive hierarchy

目的：在真实单层 block 上，进一步拆清 `Phase4-C1` 的收益到底来自 `split`、`expert capacity` 还是 `tail-conditioned routing`；并修正旧 router 指标过粗的问题。

数据：真实 `DCLM + WoS` token-level block replacement；`C2` 采用双 seed，`C2.5 / C2.6` 采用三 seed，并保留 `WoS rare-token PPL` 主指标协议。

模型：冻结 `Qwen3-0.6B`，在 `layer 8` 做单层 block replacement，`k=16`，只训练替换块。

步骤：`C2` 比较 `baseline_ffn / flat_moe_raw_uniform / split_dense_tail_uniform / uniform_expert_mixture_tail / hier_moe_tail_uniform`；`C2.5` 进一步做 `2x2` 因子设计，拆开 `router input` 与 `expert input`，并补做 `with_lb / no_lb` 与 `rare-only / signature-token` specialization 指标；`C2.6` 再做 matched-budget split disentanglement，用 `raw_two_branch` 和 `wide_dense` 区分参数量、two-branch 结构和 `x_t` 输入本身。

结论：单层 `combined tail-conditioned block` 在真实主任务上最优；其最稳定的 routed 单因素增益更像是 `expert-tail input`，而不是 `router-only`；但 `split > baseline` 这件事在 matched-budget `C2.6` 里还不能完全排除“纯参数增加”解释，因为 `wide_dense` 已经几乎追平 `split`。同时，`raw_two_branch` 明显差于 `split`，说明如果真的采用 two-branch 结构，给第二分支喂 `x_t` 至少是必要的。`LB` 不是当前 real-model main metric 的关键因子。

为什么能得出：`C2` 中

$$
437.7246 < 455.6466 \approx 455.8094 < 457.6520 < 465.3319
$$

对应 `hier < split-only \approx capacity-only < baseline < flat`；`C2.5` 中

$$
447.1932 \approx 448.6350 \ll 471.7282 \approx 472.3493
$$

对应 `full hier \approx expert-only \ll router-only \approx flat`；`C2.6` 中

$$
465.8115 \approx 465.9182 < 466.1178 \ll 472.4337
$$

对应 `split \approx wide-dense < baseline << raw-two-branch`；同时 `with_lb / no_lb` 在 `WoS rare-token PPL` 上几乎等价。

更新作用：这是当前对 `H2` 最强、也最收束的支持；同时明确收紧 claim 边界，避免把“`router-only` 已成立”说过头。

重点标签：真实单层机制拆解与 claim 边界修正。

对应主要文档：

- [phase5_hierarchical_moe_execution_plan.md](../phase5_recursive_hierarchical_moe/docs/phase5_hierarchical_moe_execution_plan.md)
- [phase5_experiment_report.md](../phase5_recursive_hierarchical_moe/docs/phase5_experiment_report.md)
- [Phase5 summary](../phase5_recursive_hierarchical_moe/results/phase5_full_20260419/summary.md)

`Phase5` 做了两件事：

1. `C2`：对 `Phase4 C1` 的真实正结果做机制拆解。
2. `D1`：在 oracle small-model 中测试 recursive hierarchy。

如果你第一次读这里，`C2 / C2.5 / D1` 也可以直接翻译成人话：

- `C2`
  - 真实单层机制消融主实验
  - 回答“`C1` 的收益到底来自 split、容量，还是 routing”
- `C2.5`
  - 真实单层 `2x2` 因子拆解实验
  - 专门拆开 `router input` 与 `expert input`
  - 同时补做 `with_lb / no_lb` 与更细的 specialization 指标
- `C2.6`
  - 真实单层 matched-budget split disentanglement
  - 专门拆开“额外参数”“two-branch 本身”和 `x_t` 输入本身
- `D1`
  - recursive hierarchy 的 small-model 主实验
  - 回答“如果 tail 内部还有 coarse/fine 结构，递归结构是否真的值得做”

所以简单说：

- `C` = 真实模型单层 block 的主线实验
- `D` = 递归 hierarchical 的前瞻性实验

### 10.1 `C2`：为什么它是这条线里最关键的控制变量实验

`C1` 虽然已经说明 `hier_moe_tail_uniform` 优于 `baseline_ffn` 和 `flat_moe_raw_uniform`，但还无法区分收益到底来自：

1. split
2. 多 expert 容量
3. input-dependent routing

所以 `C2` 专门设计了四组来控制变量。

#### `split_dense_tail_uniform`

它的结构是：

$$
h_{\text{out}} = h_{\text{in}} + E_c(x) + E_t(P_t(x-\mu))
$$

解释：

- 一个 common branch
- 一个 tail branch
- 没有 router

它想证明的是：

$$
\text{如果只做 split，不做 routing，收益有没有？}
$$

#### `uniform_expert_mixture_tail`

它的结构是：

$$
h_{\text{out}} = h_{\text{in}} + E_c(x) + \frac{1}{N}\sum_{i=1}^{N} E_i(P_t(x-\mu))
$$

解释：

- 有多个 tail experts
- 但没有 router
- 直接均匀平均

它想证明的是：

$$
\text{如果只增加 expert 容量，但不给 input-dependent routing，收益有没有？}
$$

#### `hier_moe_tail_uniform`

它的结构是：

$$
h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(P_t(x-\mu)) E_i(P_t(x-\mu))
$$

这就是当前最核心的 hierarchical 单层结构：

- common branch 处理 full hidden
- router 只看 tail residual
- tail experts 也只看 tail residual

它想证明的是：

$$
\text{在控制了 split 和 expert 数量之后，input-dependent routing 是否仍然提供额外增益。}
$$

#### `flat_moe_raw_uniform`

它的结构是：

$$
h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x) E_i(x)
$$

它对应的是更传统、更 flat 的做法：

- router 看 raw hidden
- experts 也看 raw hidden

它是最直接的结构对照。

### 10.2 `C2` 有没有偷偷多给 `hier` 更多专家

没有。

这是 `C2` 最值得信任的地方之一。

在 `C2` 里：

- `flat_moe_raw_uniform`
- `uniform_expert_mixture_tail`
- `hier_moe_tail_uniform`

三者的 tail expert 数量都是 `4`。

因此 `hier` 的收益不能解释成“它只是用了更多专家”。

### 10.3 `C2` 最后证明了什么

双 seed 聚合结果是：

- `hier_moe_tail_uniform`
  - `WoS rare-token PPL = 437.7246 ± 65.3381`
- `split_dense_tail_uniform`
  - `WoS rare-token PPL = 455.6466 ± 71.3311`
- `uniform_expert_mixture_tail`
  - `WoS rare-token PPL = 455.8094 ± 68.2142`
- `baseline_ffn`
  - `WoS rare-token PPL = 457.6520 ± 67.5661`
- `flat_moe_raw_uniform`
  - `WoS rare-token PPL = 465.3319 ± 72.1181`

这一步非常关键，但它的结论边界必须说清。旧 `C2` 第一次在严格控制变量后支持：

$$
\text{combined tail-conditioned routed block}
<
\text{split-only / capacity-only / flat raw}
$$

但旧 `C2` 还**不能**区分：

1. 是 router 改看 `tail residual` 带来的
2. 还是 expert 改看 `tail residual` 带来的
3. 还是两者一起改才成立

因此，旧 `C2` 最安全的说法不是：

$$
\text{router-only 已经成立}
$$

而是：

$$
\text{Hier 的 combined tail-conditioned block 已经优于 split-only、capacity-only 和 flat raw。}
$$

### 10.4 `C2.5`：router input vs expert input disentanglement + specialization metric revision

这一步就是为了修正上面的 claim 边界。

`C2.5` 在真实 `Qwen3-0.6B`、`layer=8`、`k=16`、`frozen`、三 seed 设置下，显式跑了一个 `2x2` 因子设计：

$$
u_t = \sum_i g_i(\text{input}_{\text{router}}) E_i(\text{input}_{\text{expert}})
$$

四个核心 routed 组是：

- `flat_moe_raw_uniform`
  - $g_i(x), E_i(x)$
- `router_tail_expert_raw_uniform`
  - $g_i(P_t(x-\mu)), E_i(x)$
- `router_raw_expert_tail_uniform`
  - $g_i(x), E_i(P_t(x-\mu))$
- `hier_moe_tail_uniform`
  - $g_i(P_t(x-\mu)), E_i(P_t(x-\mu))$

同时还保留：

- `split_dense_tail_uniform`
- `uniform_expert_mixture_tail`
- `baseline_ffn`

并新增了两组 real-model `LB` 对照：

- `flat_moe_raw_no_lb`
- `hier_moe_tail_no_lb`

这一步回答了四个问题。

#### Q1. 仅改 router 输入，是否已经带来收益？

比较：

$$
\text{router\_tail\_expert\_raw\_uniform}
\quad \text{vs} \quad
\text{flat\_moe\_raw\_uniform}
$$

三 seed 结果是：

- rare-token PPL 只改善了 `0.6210`
- `signature_token_purity` 反而下降 `0.0190`
- `doc_purity_rare_only` 也略降

所以当前**不能**说：

$$
\text{router-only change 已经稳定成立。}
$$

#### Q2. 仅改 expert 输入，是否已经带来收益？

比较：

$$
\text{router\_raw\_expert\_tail\_uniform}
\quad \text{vs} \quad
\text{flat\_moe\_raw\_uniform}
$$

三 seed 结果是：

- rare-token PPL 改善 `23.7143`
- `doc_purity_rare_only` 小幅改善
- `signature_token_purity` 基本持平

这说明当前最稳定的单因素增益来源其实是：

$$
\text{expert input} : x \rightarrow P_t(x-\mu)
$$

#### Q3. full hier 是否显著优于两个 partial control？

比较一：

$$
\text{hier\_moe\_tail\_uniform}
\quad \text{vs} \quad
\text{router\_tail\_expert\_raw\_uniform}
$$

full hier 在 rare-token PPL 上明显更好。

比较二：

$$
\text{hier\_moe\_tail\_uniform}
\quad \text{vs} \quad
\text{router\_raw\_expert\_tail\_uniform}
$$

这里 full hier 仍然是主指标最优，但只再改善了 `1.4418` 的 rare-token PPL，而且新的 rare/signature specialization 指标并没有同步更强。

所以现在最准确的说法是：

$$
\text{full hier 在主任务上最好，但其中大部分收益已经可以由 expert-tail input 解释。}
$$

#### Q4. 当前 real-model 中 LB 是否重要？

旧 `C2` 里其实 flat 已经是带 `LB` 的版本。

这次 `C2.5` 又进一步显式比较了：

- `flat_moe_raw_uniform` vs `flat_moe_raw_no_lb`
- `hier_moe_tail_uniform` vs `hier_moe_tail_no_lb`

结果是：

- `LB` 对 `WoS rare-token PPL` 几乎没有影响
- `no_lb` 反而经常给出更高的 `legacy/rare-only/signature` specialization 指标

因此，关于 “flat raw 对照是否已包含 LB” 这个问题，当前答案是：

$$
\text{是的，旧 C2 里 flat 已经带 LB；而 C2.5 又显式补做了 flat/hier 的 no-LB 对照。}
$$

#### 为什么旧 router 指标过粗？

旧 `router_purity / router_nmi` 实际上对应的是：

$$
\text{所有 WoS valid token}
$$

上的 `doc-domain -> expert assignment` 一致性。

这个口径太粗，因为它把：

- 高频 common token
- 真正 rare token
- 更具 domain signature 的 token

全都混在了一起。

所以 `C2.5` 新增了三类更细的指标：

1. `doc_purity_rare_only`
   - 只在 rare token 子集上比较 doc-domain 与 expert
2. `signature_token_purity / nmi`
   - 只在 WoS train 中满足 `count(v) >= 20` 且 `\max_z p(z|v) >= 0.7` 的 signature token 上评估
3. `domain_expert_kl_signature`
   - 测量 pseudo-domain 到 expert 分配的偏离程度

但这一步又带来一个重要新认识：

$$
\text{更强的 specialization proxy 不等于更好的 LM 主任务结果。}
$$

例如：

- `flat_moe_raw_no_lb` 的 `signature_token_purity / nmi / KL` 都明显更高
- 但它的 rare-token PPL 并不更好

也就是说，当前这些 proxy 仍然不是“专家真正帮助 next-token prediction”的完全充分统计量。

最后还要说明一个实现事实：

`expert_wise_rare_token_nll_by_signature_domain` 这张矩阵在本轮三个 seed 上是结构性空的，因为在当前阈值下：

$$
|\text{rare tokens} \cap \text{signature tokens}| = 0
$$

所以结果目录里保留的是显式 `NaN` 占位矩阵，而不是缺文件。

### 10.5 `C2.6`：split gain 是参数效应、two-branch 效应，还是 `tail-residual input` 效应？

`C2.5` 解决的是 routed block 里的 `router input` 与 `expert input`。  
但它没有解决另一个很关键的问题：

$$
\text{split\_dense\_tail\_uniform} > \text{baseline\_ffn}
$$

到底是因为：

1. 只是 block 参数变多了；
2. 还是 because two-branch factorization 本身有效；
3. 还是 because tail branch 吃 `x_t = P_t(x-\mu)` 本身有效。

为了解开这个问题，`C2.6` 在真实 `Qwen3-0.6B`、`layer = 8`、`k = 16`、`frozen`、三 seed 设置下，补做了一个 matched-budget split disentanglement。

四组对照是：

- `baseline_ffn`
  - 单分支 dense，输入 `x`
- `split_dense_tail_uniform`
  - `E_c(x) + E_t(P_t(x-\mu))`
- `raw_two_branch_uniform`
  - `E_c(x) + E_t(x)`
- `baseline_ffn_wide_match_split`
  - 单分支 dense，输入 `x`
  - 但把 `intermediate_size` 调宽到与 `split` 的 block 参数量匹配

其中最关键的预算控制是：

- `baseline_ffn`：`9,437,184` 个 block 可训练参数
- `split_dense_tail_uniform`：`11,796,480`
- `raw_two_branch_uniform`：`11,796,480`
- `baseline_ffn_wide_match_split`：`11,796,480`

这里 `wide_dense` 用的是：

$$
\text{intermediate\_size} = 3840
$$

它和 `split` 的参数预算是精确匹配的，误差为：

$$
0.0\%
$$

所以 `C2.6` 的三个核心比较是：

#### Q1. 仅仅 two-branch + extra params 是否已经有收益？

比较：

$$
\text{raw\_two\_branch\_uniform}
\quad \text{vs} \quad
\text{baseline\_ffn}
$$

三 seed 结果是：

- `raw_two_branch_vs_baseline_rare_ppl_delta = -6.3159`

这里是负数，表示：

$$
\text{raw\_two\_branch\_uniform}
>
\text{baseline\_ffn}
$$

也就是说，在当前真实模型里：

$$
\text{two-branch + extra params 本身不但没有收益，反而更差。}
$$

#### Q2. 仅仅把参数加到和 split 一样多，单分支 dense 能否追平 split？

比较一：

$$
\text{baseline\_ffn\_wide\_match\_split}
\quad \text{vs} \quad
\text{baseline\_ffn}
$$

wide dense 相比 baseline 只改善了很小一截：

- `466.1178 -> 465.9182`

比较二：

$$
\text{baseline\_ffn\_wide\_match\_split}
\quad \text{vs} \quad
\text{split\_dense\_tail\_uniform}
$$

三 seed 结果是：

- `split_vs_wide_dense_rare_ppl_delta = 0.1066`

也就是说：

$$
\text{split\_dense\_tail\_uniform} \approx \text{baseline\_ffn\_wide\_match\_split}
$$

当前数据**不支持**我们说：

$$
\text{split 已经明显超出了 matched-budget 单分支 dense。}
$$

#### Q3. 在参数量和分支结构都匹配后，`x_t` 本身是否仍然有效？

比较：

$$
\text{split\_dense\_tail\_uniform}
\quad \text{vs} \quad
\text{raw\_two\_branch\_uniform}
$$

三 seed 结果是：

- `split_vs_raw_two_branch_rare_ppl_delta = 6.6221`

也就是说：

$$
\text{split\_dense\_tail\_uniform}
<
\text{raw\_two\_branch\_uniform}
$$

这一步非常重要，因为它说明：

$$
\text{如果你真的要用 two-branch 结构，那么给第二分支喂 } x_t \text{ 是有价值的。}
$$

换句话说，`x_t` 的作用现在更像是：

$$
\text{把原本有害的 raw two-branch，拉回到可用区域。}
$$

而不是已经强到足以在当前 setting 下明显压过 matched-budget wide dense。

#### `C2.6` 的最终修正结论

`C2.6` 之后，对 `split > baseline` 最合理的归因应该修正为：

1. 当前真实模型里，`split > baseline` **还不能完全排除纯参数增加解释**，因为 `baseline_ffn_wide_match_split` 已经几乎追平了 `split_dense_tail_uniform`。
2. 当前真实模型里，`two-branch factorization` **本身并没有表现出独立收益**，因为 `raw_two_branch_uniform` 反而比 baseline 更差。
3. 当前真实模型里，`x_t` **在 two-branch 结构中是有价值的**，因为它能稳定改善 `raw_two_branch_uniform`。
4. 因此更准确的说法不是：

$$
\text{split-alone 已经作为结构本体明确胜过 matched-budget dense}
$$

而是：

$$
\text{within two-branch models, } x_t \text{ is important; but split-alone gain over baseline has not yet ruled out a parameter-matching explanation.}
$$

---

## 11. `Phase5-D1`：recursive hierarchy 为什么还没有成立

目的：验证如果 tail 内部确实还存在 `coarse / fine` hierarchy，那么 recursive factorization / routing 是否还能进一步改善更细粒度 rare tail。

数据：带有显式 `coarse / fine` 潜变量结构的 synthetic small-model 数据；关键生成参数是 `rho1` 与 `rho2`。

模型：递归 small-model 家族 `R0-R6`，包含 dense、flat、一级 split、一级 hier、递归 split、递归 hier 与 oracle upper bound。

步骤：比较 `R0-R6` 在 `rare-fine-tail PPL` 上的表现，并用 `R6_oracle_recursive_router_upper_bound` 提供“router 完全学对时”的结构上界。

结论：`recursive factorization` 可能有一点潜力，但 `learned recursive hierarchy` 还没有成立；当前更像是 recursive router 没学出来，而不是递归结构在原理上没价值。

为什么能得出：最佳组合附近，

$$
R6_{\text{oracle}} \ll R2, R3, R4, R5,
$$

而且 gate 明确给出 `recursive_positive = false`、`recursive_factorization_positive = true`，说明 oracle 上界很强，但 learned recursive 结果还没有追上。

更新作用：只给 `H3 [Recursive-Tail Hypothesis]` 提供“结构可能有潜力”的部分支持，不支持“recursive learned hierarchy 已成立”。

重点标签：recursive 上界强、学习闭环未达成。

### 11.1 `D1` 想证明什么

当 `C2` 已经支持“单层 hierarchical routing 有价值”之后，下一个自然问题是：

$$
\text{如果 tail 内部还有层次结构，recursive learned hierarchy 是否更好？}
$$

### 11.2 `D1` 里的 `R0-R6` 是什么

这里的 `R` 代表 `recursive` 这一条小模型线。

- `R0_dense_ffn`
  - 普通 dense baseline
- `R1_flat_raw_moe`
  - flat raw MoE
- `R2_level1_split_dense`
  - 一级 split，不做 routing
- `R3_level1_hier_moe`
  - 一级 hierarchical MoE
- `R4_recursive_split_dense`
  - 递归 split，但不做 learned routing
- `R5_recursive_hier_moe`
  - 完整二级 learned hierarchical MoE
- `R6_oracle_recursive_router_upper_bound`
  - 直接使用真实 coarse/fine 标签做 oracle routing 的上界组

### 11.3 `Oracle` 在实验里到底起什么作用

`Oracle` 在这条线上有两种意义。

第一种是 `oracle split`：

$$
x = [x_c; x_{t1}; x_{t2}]
$$

也就是直接知道 common、一级 tail、二级 tail 的真实坐标切分，不需要再估计 projector。

它的作用是：

$$
\text{去掉 projector 估计误差，只看结构本体值不值得做。}
$$

第二种是 `oracle router upper bound`，也就是 `R6`。

这里 router 不是自己学，而是直接喂真实 coarse/fine 标签。它的作用是：

$$
\text{告诉我们：如果 router 完全学对了，理论上最好能到哪里。}
$$

所以 Oracle 的科学作用非常明确：

- 去掉 projector 误差
- 去掉 router 学习误差
- 把“结构不行”和“没学出来”区分开

### 11.4 `rho1=0.2, rho2=0.1` 是什么

这两个不是优化超参数，而是 small-model 数据生成过程里的生成参数。

`D1` 的 token 生成可以理解成：

$$
p(x_{t+1}\mid x_t,z_1,z_2)
=
(1-\rho_1-\rho_2)T_{\mathrm{common}}
+
\rho_1 T^{\mathrm{coarse}}_{z_1}
+
\rho_2 T^{\mathrm{fine}}_{z_1,z_2}
$$

其中：

- $\rho_1$ 控制 coarse tail 结构的触发概率
- $\rho_2$ 控制 fine tail 结构的触发概率

因此：

- $\rho_1$ 越大，一级 tail 结构越强
- $\rho_2$ 越大，二级细粒度结构越强

`rho1=0.2, rho2=0.1` 之所以重要，是因为这组设置下 fine-level 结构已经足够强，递归结构才最有机会被看见。

### 11.5 `D1` 最后证明了什么

最佳组合附近的结果是：

- `R2_level1_split_dense`：`rare-fine-tail PPL = 8832.0`
- `R4_recursive_split_dense`：`rare-fine-tail PPL = 8941.5`
- `R3_level1_hier_moe`：`rare-fine-tail PPL = 8995.2`
- `R5_recursive_hier_moe`：`rare-fine-tail PPL = 9205.1`
- `R6_oracle_recursive_router_upper_bound`：`rare-fine-tail PPL = 1040.4`

gate 文件给出的结论是：

- `recursive_positive = false`
- `recursive_factorization_positive = true`

这意味着：

1. learned recursive hierarchy 还没有打赢一级 hierarchy。
2. recursive factorization 本身可能有一点潜力。
3. Oracle 上界非常强，说明真正的瓶颈更像是：

$$
\text{recursive router 没学出来}
$$

而不是：

$$
\text{recursive structure 在原理上没价值。}
$$

---

## 12. 低秩投影到底是怎么实现的

你反复关心“低秩投影到底是不是一个训练出来的低秩模块”，这里把它完整说清楚。

在 `Phase4/5` 的真实模型实验中，这个 projector 不是训练出来的 adapter，而是一个由数据估计出来的固定线性算子。

具体步骤是：

1. 在选定层收集 hidden states。
2. 估计均值：

$$
\mu = \mathbb{E}[x]
$$

3. 估计 centered covariance：

$$
\Sigma = \mathbb{E}[(x-\mu)(x-\mu)^\top]
$$

4. 对 $\Sigma$ 做特征分解，取前 $k$ 个特征向量组成 $V_k$。
5. 定义 tail projector：

$$
P_t = I - V_k V_k^\top
$$

6. 前向时对每个 hidden 做：

$$
\text{centered} = x - \mu
$$

$$
\text{common} = (x-\mu)V_kV_k^\top
$$

$$
x_t = (x-\mu) - \text{common}
$$

所以更准确地说，这个“低秩投影”并不是在学一个 low-rank block，而是在：

$$
\text{删掉一个 rank-}k\text{ 的 shared covariance head 子空间。}
$$

这一步在真实模型里是数据驱动估计的，在 `D1` 里甚至更干净，因为 `D1` 直接用 oracle 坐标切分，连估计误差都没有。

---

## 13. 现在最稳的数理逻辑链是什么

如果把 `Phase2-5` 压成当前最能 defend 的逻辑链，我会这样写。

### 第一步：真实几何已经成立

`Phase1` 支持：

$$
\text{shared head exists in real hidden states}
$$

以及：

$$
\text{tail residual is more separable than raw hidden}
$$

### 第二步：split 结构成立，但强优化解耦没有成立

`Phase2` 支持：

$$
\text{split is promising}
$$

但不支持：

$$
\text{the toy optimizer recipe transfers directly to real training}
$$

### 第三步：tail-conditioned routing 有弱正信号

`Phase3` 支持：

$$
\text{routing on tail residual is more promising than routing on raw hidden}
$$

但这一步还不足以闭环。

### 第四步：真实 block 本体已经给出正结果

`Phase4-C1` 支持：

$$
\text{hierarchical tail-conditioned block} > \text{baseline FFN and flat raw MoE block}
$$

### 第五步：控制变量后，single-layer combined tail-conditioned block 的优势成立，但 router-only 很弱，split-alone 也还没有完全排除参数解释

`Phase5-C2` 和 `C2.5` 合起来支持：

$$
\text{hier gain is not only split}
$$

也支持：

$$
\text{hier gain is not only more expert capacity}
$$

但 `C2.5` 进一步说明：

$$
\text{the main gain is closer to expert-tail input than to router-only input}
$$

因此当前最稳的结论更准确地写成：

$$
\text{single-layer split-first combined tail-conditioned block has real structural advantage}
$$

但 `C2.6` 又进一步说明：

$$
\text{split-alone gain over baseline is still almost matched by a wide dense control}
$$

以及：

$$
\text{raw two-branch is bad, and } x_t \text{ mainly rescues that branch structure}
$$

所以今天最稳的说法不是：

$$
\text{every split effect is already a pure structure effect}
$$

而是：

$$
\text{combined tail-conditioned block is solid; within two-branch models, } x_t \text{ matters; but split-alone still needs tighter evidence against a matched-budget dense explanation.}
$$

### 第六步：recursive learned hierarchy 尚未成立

`Phase5-D1` 说明：

$$
\text{recursive factorization may help, but learned recursive routing is not established yet}
$$

所以，今天最稳的主线不是：

$$
\text{recursive learned hierarchy has already won}
$$

而是：

$$
\text{split-first} \rightarrow \text{single-layer tail-conditioned routing}
$$

这条线已经有比较扎实的真实证据。

---

## 14. 我们现在到底能下什么结论，不能下什么结论

### 14.1 现在能下的结论

1. 真实大模型 hidden state 中确实存在 shared head。
2. `tail residual` 的几何确实更适合语义区分。
3. 在真实单层 routed family 里，`combined tail-conditioned block` 已经稳定优于 `flat raw MoE`，并在 `WoS rare-token PPL` 上达到当前最好结果。
4. `Phase6-A / D1` 已经说明：当前单层 hier 的收益不只是 proxy 指标更好，而是已经出现了 `LM-relevant specialization`。也就是说，被 router 选中的 expert 在 `middle / rare` token 上确实优于 second-best / random 替代 expert，而且这条结论对 `no-LB` 稳健。
5. 在 routed 控制组里，`expert-tail input` 是当前最稳定的单因素增益来源；`router-only` 改成看 `x_t` 目前仍然很弱。
6. `Phase6-B / D2` 进一步说明：expert 最该看的不是 `raw` 或 `head`，而是更 `tail-oriented` 的 band。当前 `full tail residual` 与 `extreme tail` 都明显优于 `raw / head`，而且这条“大结论”对 `no-LB` 稳健；真正仍未定死的只是 `tail` 与 `extreme` 的精细排序。
7. 在 non-routing matched-budget 控制组里，`split_dense_tail_uniform ≈ baseline_ffn_wide_match_split > baseline_ffn`，所以 `split-alone` 还没有明确打赢 matched-budget wide dense。
8. 在 two-branch 结构内部，`x_t` 是必要的，因为 `split_dense_tail_uniform << raw_two_branch_uniform`。
9. `LB` 不是当前真实单层 block 主指标的关键因子，因为 `with_lb / no_lb` 在主 PPL 上几乎等价。
10. `Phase6-C / D3` 说明 recursive learned hierarchy 的 primary bottleneck 在 `coarse routing`，而不是 `fine-local routing`。同时 teacher-aided CE 还能继续缩小 gap，说明训练信号本身也是第二层瓶颈；这条诊断对 `no-LB` 也稳健。

### 14.2 现在不能下的结论

1. “estimated projector 已经稳定可替代 oracle split”
2. “WD-only 一定是当前真实收益的主要来源”
3. “recursive learned hierarchy 已经优于一级 hierarchical”
4. “router-only 改成看 tail residual 就已经稳定成立”
5. “更高的 purity / NMI 就等于更好的 LM 主任务收益”
6. “split > baseline 已经完全排除了纯参数增加解释”
7. “two-branch factorization 本身已经在真实模型里稳定有益”
8. “middle tail 已经唯一确定为 expert 最优频带”
9. “fine-local routing 是当前 recursive gap 的主瓶颈”
10. “我们已经完成了最终完整方法”

这些话现在都还不能说，不是因为主线错了，而是因为证据还没有走到那一步。

---

## 15. 我们现在 reach 到哪里

如果要用一句最准确的话总结当前进度，我会写：

$$
\text{我们已经从 toy 机制验证，推进到了真实模型中 single-layer hierarchical architecture 的正结果，并且已经证明它具有对 no-LB 稳健的 LM-relevant specialization；但 projector 替代、router calibration 与 learned recursive hierarchy 仍未闭环。}
$$

如果再压缩一点，就是：

$$
\text{当前真正成立的是：single-layer combined tail-conditioned routed block 的优越性，以及它已经出现了功能性的 expert specialization。}
$$

而不是：

$$
\text{整个最终递归体系已经完全成立。}
$$

---

## 16. 现在最值得记住的主线

如果你只记一件事，请记住下面这条线：

1. `Phase1` 证明真实 hidden state 里有 shared head。
2. `Phase2` 和 `Phase3` 说明 split 和 tail-conditioned routing 值得继续，但 proxy 还不够干净。
3. `Phase4` 第一次证明真实 block 本体已经优于 flat。
4. `Phase5-C2` 先证明这种优越性不只是 split，也不只是容量。
5. `Phase5-C2.5` 再进一步说明：在 routed family 里，主要稳定增益来源更像是 `expert-tail input`，而不是 `router-only`。
6. `Phase5-C2.6` 又说明：在 non-routing matched-budget family 里，`split-alone` 还没有明确打赢 matched-budget wide dense，但 `x_t` 能明显修正 raw two-branch。
7. `Phase6-A` 把这条线从“结构上更好”推进到“已经出现 LM-relevant specialization”。
8. `Phase6-D1` 进一步说明：这条 `LM-relevant specialization` 结论对 `no-LB` 也是稳健的。
9. `Phase6-B / D2` 进一步说明 expert 最该看的不是 `raw/head`，而是 `tail-oriented` band，其中 `full tail residual` 与 `extreme tail` 当前最强，但精细排序仍会轻微变化。
10. `Phase6-C / D3` 则把递归主线的 primary bottleneck 稳健地定位到 `coarse routing`。

所以今天最稳、最适合继续推进的主线是：

$$
\text{真实模型中的 split-first, single-layer combined tail-conditioned routed block}
$$

并且这条线现在已经不只是结构优势，而是：

$$
\text{single-layer LM-relevant specialization}
$$

这是我们当前真正已经 reach 到的位置。

---

## 17. 如果接下来要继续学习，最好的问题是什么

读完这篇文档以后，最值得继续追问的不是“下一步再跑什么”，而是：

1. 为什么 `Phase4-C1` 和 `Phase5-C2` 已经是正结果，但 `B1` 的 projector 主线还没成立。
2. 为什么 `router_raw_expert_tail_uniform` 已经几乎追上 `hier_moe_tail_uniform`，而 `router_tail_expert_raw_uniform` 仍然很弱。
3. 为什么 `Phase6-A` 中 token-level `G_cf` 已经是正的，但 `route margin` 与 `G_cf` 的相关性仍然这么弱。
4. 为什么 `Phase6-B` 里 `full tail residual` 与 `extreme tail` 几乎打平，而 `middle` 反而不是唯一最优。
5. 为什么 `R6` 的 Oracle 上界这么强，而 `R5` 的 learned recursive hierarchy 却没有跟上，并且为什么 `R5c` 明显强于 `R5d`。

如果这五个问题被真正讲清楚，我们对整条主线的理解就会非常扎实。

---

## 18. 汇报可直接引用的重点实验摘要

如果汇报里只能放最重要的几个实验，我建议优先讲下面五个。它们基本覆盖了“为什么值得做、已经走到哪一步、还卡在哪儿”这三件事。

### 18.1 `Phase1`：真实表征审计

这是整条线的地基实验。它要回答的不是“Hier 方法已经在真实语言建模里赢了没有”，而是更基础的问题：

$$
\text{真实 hidden 里到底有没有一个 shared high-variance head？}
$$

以及：

$$
\text{如果把这个 shared head 去掉，tail residual 是否更适合 long-tail 语义区分？}
$$

实验做法是：在冻结的 `Qwen3-8B` 上，选取 `post-attention / pre-FFN` 位置的 hidden state，扫描 `layer 5/11/23/35` 与 `rank 4/8/16/32/64`，用 `DCLM + WoS` 的混合数据估计协方差，然后比较 `raw`、`centered`、`tail_residual` 三种表示在 `probe accuracy / purity / NMI / Sep_trace` 上的表现。

它最重要的结果是两点。第一，`layer 35` 的前 `8` 个主方向累计解释方差约为 `0.4069`，说明真实 hidden 里确实存在低秩 shared head。第二，在两个正式 seed 上，`tail_residual` 的 `probe accuracy / purity / NMI` 都稳定优于 `raw / centered`，而 `raw` 和 `centered` 几乎重合。这说明“单纯去 mean 不够”，真正有用的是把 shared covariance head 删掉，得到更干净的 `tail residual`。

这一步在汇报里最好这样讲：`Phase1` 不是方法胜利，而是**命题的几何前提成立**。如果这一层不成立，后面所有 `split-first / tail-conditioned` 结构都没有根据；而现在这层是成立的。

### 18.2 `Phase4-C1`：真实单层 block 的第一次正结果

这是第一条真正能落在真实模型上的强证据。它回答的是：

$$
\text{在真实 Qwen block 上，single-layer hierarchical block 本体是否已经优于 baseline 和 flat raw MoE？}
$$

实验设置是：冻结 `Qwen3-0.6B`，只替换 `layer 8` 的一个 `FFN block`，用真实 `DCLM + WoS` 数据训练，比较 `baseline_ffn`、`flat_moe_raw_uniform` 和 `hier_moe_tail_uniform`。这里的 `hier` 指的是：

$$
h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(P_t(x-\mu)) E_i(P_t(x-\mu)).
$$

最关键的结果是 `WoS rare-token PPL`：

- `baseline_ffn = 84.0007`
- `flat_moe_raw_uniform = 85.0412`
- `hier_moe_tail_uniform = 81.5287`

也就是说，在真实单层 block 上，`hier` 已经同时优于 `baseline` 和 `flat raw MoE`。而且这一轮里 `wd-only` 版本和 `uniform` 版本几乎重合，说明当前主收益不是来自 `WD` 技巧，而是来自结构本体。

这一步在汇报里最好这样讲：**到 `C1` 为止，研究已经从 toy / proxy 进入了“真实 block 本体正结果”阶段。** 这也是整条主线第一次真正闭环的地方。

### 18.3 `Phase5-C2`：真实单层机制消融，证明收益不只是 split，也不只是容量

`C1` 虽然已经给了正结果，但还不能回答收益到底来自什么。`C2` 的作用，就是把下面三件事拆开：

1. 只做 `split` 有没有收益  
2. 只增加 `expert capacity` 有没有收益  
3. `input-dependent routing` 是否还提供额外价值

所以 `C2` 设计了几个关键对照：

- `split_dense_tail_uniform`
  - 只做 `common/tail` 分支拆分，不做 routing
- `uniform_expert_mixture_tail`
  - 有多个 tail expert，但直接均匀平均，不做 input-dependent routing
- `flat_moe_raw_uniform`
  - router 和 experts 都看 raw hidden
- `hier_moe_tail_uniform`
  - router 和 experts 都看 `tail residual`

双 seed 聚合结果里，`WoS rare-token PPL` 排序是：

- `hier_moe_tail_uniform = 437.7246 ± 65.3381`
- `split_dense_tail_uniform = 455.6466 ± 71.3311`
- `uniform_expert_mixture_tail = 455.8094 ± 68.2142`
- `baseline_ffn = 457.6520 ± 67.5661`
- `flat_moe_raw_uniform = 465.3319 ± 72.1181`

这个结果非常关键。它说明 `hier` 的收益不能解释成“只做 split 就够了”，因为 `hier < split-only`；也不能解释成“只是多了几个 expert”，因为 `hier < capacity-only`；更不能解释成“flat raw MoE 其实也一样好”，因为 `flat` 反而最差。

但 `C2` 仍然有边界：它证明的是

$$
\text{combined tail-conditioned block}
$$

已经优于 `split-only / capacity-only / flat`，却还不能区分到底是 `router 看 x_t` 带来的，还是 `expert 看 x_t` 带来的。

### 18.4 `Phase5-C2.5`：把 router input 和 expert input 拆开之后，发现主增益更像来自 `expert-tail input`

这是当前最容易被误读、但也最重要的修正实验。它的核心问题是：

$$
\text{C2 里的收益，到底是 router 看 tail residual 带来的，还是 expert 看 tail residual 带来的？}
$$

所以 `C2.5` 做了一个真实模型上的 `2x2` 因子设计：

- `flat_moe_raw_uniform`
  - \(g_i(x), E_i(x)\)
- `router_tail_expert_raw_uniform`
  - \(g_i(x_t), E_i(x)\)
- `router_raw_expert_tail_uniform`
  - \(g_i(x), E_i(x_t)\)
- `hier_moe_tail_uniform`
  - \(g_i(x_t), E_i(x_t)\)

三 seed 聚合结果里，`WoS rare-token PPL` 是：

- `hier_moe_tail_uniform = 447.1932 ± 49.0255`
- `router_raw_expert_tail_uniform = 448.6350 ± 48.5303`
- `router_tail_expert_raw_uniform = 471.7282 ± 52.2785`
- `flat_moe_raw_uniform = 472.3493 ± 52.4237`

这个结果给了一个很明确的新认识。  
只改 router 输入，也就是 `g_i(x) -> g_i(x_t)`，几乎不带来主指标改善；  
只改 expert 输入，也就是 `E_i(x) -> E_i(x_t)`，却能带来非常大的 rare-token PPL 改善；  
full hier 仍然是最好，但它相比 `expert-only` 只再提升了大约 `1.44` 的 rare-token PPL。

所以现在最准确的讲法不是“router-only 已经成立”，而是：

$$
\text{single-layer combined tail-conditioned block is best,}
$$

但其中大部分收益更像是

$$
\text{expert input} : x \rightarrow x_t
$$

而不是

$$
\text{router-only} : x \rightarrow x_t.
$$

这一步在汇报里非常重要，因为它帮助我们把 claim 边界收紧，避免把 `tail-conditioned routing` 夸大成已经完全成立的主因。

### 18.5 `Phase5-D1`：recursive hierarchy 的上界很强，但 learned recursive 还没学出来

这是当前主线的前瞻实验，不是已经成立的最终结果。它回答的是：

$$
\text{如果 tail 内部还有 coarse/fine hierarchy，recursive factorization / routing 值不值得做？}
$$

`D1` 在 synthetic small-model 上比较了：

- 一级 split / 一级 hier
- 递归 split / 递归 hier
- 以及一个 `oracle_recursive_router_upper_bound`

最佳组合附近的 `rare-fine-tail PPL` 是：

- `R2_level1_split_dense = 8832.0`
- `R4_recursive_split_dense = 8941.5`
- `R3_level1_hier_moe = 8995.2`
- `R5_recursive_hier_moe = 9205.1`
- `R6_oracle_recursive_router_upper_bound = 1040.4`

这里最重要的不是谁是第一，而是结构关系。`R6` 的 oracle 上界极强，说明如果 coarse/fine 路由学对了，递归结构的潜在收益是很大的；但 `R5` 的 learned recursive hierarchy 还远远没有追上这个上界，而且连一级结构都没有稳定打赢。

所以 `D1` 在汇报里要讲成：

- `recursive factorization` 可能有潜力
- `oracle upper bound` 很强
- 但 `learned recursive routing` 目前还没有成立

这一步的价值，不是宣布“递归已经成功”，而是明确指出：**真正的瓶颈更像是 recursive router 没学出来，而不是结构在原理上没价值。**

### 18.6 如果汇报时间只够讲三件事，应该讲什么

如果你的汇报时间非常紧，我建议最少讲下面三件事：

1. `Phase1`
   - 讲清真实 hidden 里确实有 `shared head`，`tail residual` 的几何更干净
2. `Phase4-C1`
   - 讲清真实单层 block 上，`hier` 已经第一次优于 `baseline` 和 `flat`
3. `Phase5-C2 + C2.5`
   - 讲清当前最稳的结论不是“router-only 已经成立”，而是“single-layer combined tail-conditioned block 成立，其中大头收益更像来自 expert-tail input”

如果还能再多讲一个实验，就补 `Phase5-D1`，用来说明我们为什么还不能把“recursive learned hierarchy 已经成立”写进结论。

### 18.7 可直接加入总报告的主结论表述

下面这段可以直接放进总报告的“阶段性结论”部分：

> 现阶段最稳定的结论是：在真实 `Qwen3-0.6B` 单层 block replacement 设置下，`split-first` 的 `combined tail-conditioned routed block` 已经稳定优于 `baseline FFN` 与 `flat raw MoE`。其中，`tail residual` 的几何优势在真实 hidden 中确实存在，并且已经转化为了真实语言建模收益；但这种收益的最稳定来源，目前更像是让 tail-side experts 处理 `x_t = P_t(x-\mu)`，而不是单独把 router 输入从 `x` 改成 `x_t`。进一步地，matched-budget 对照说明：`split-alone` 还没有明确打赢 matched-budget wide dense，因此当前还不能把全部收益都归因为“split 结构本体”；不过，如果采用 two-branch 结构，那么让第二分支看 `x_t` 是必要的，因为 raw two-branch 会明显退化。综合而言，我们已经在真实模型中建立了单层 `combined tail-conditioned routed block` 的有效性，但 projector 替代、router-only 几何路由、以及 learned recursive hierarchy 仍未闭环。

如果需要再短一版，可以用下面这段：

> 当前研究已经从 toy / proxy 推进到真实模型单层 block 的正结果：`combined tail-conditioned routed block` 在主任务上优于 `baseline` 和 `flat raw MoE`。当前最可靠的增益来自 `expert-tail input`，而不是 `router-only`；`split-alone` 仍需更强证据来排除 matched-budget dense 解释；recursive hierarchy 目前只有 oracle 上界强，learned 版本尚未成立。

## 19. `Phase6`：定义 LM-relevant specialization，收束 expert-input band，并定位 recursive bottleneck

`Phase6` 的意义在于，它把我们从“结构上看起来 work”推进到了“为什么 work、该往哪一段输入学、递归为什么没起来”。

### 19.1 `Phase6-A`：当前单层 hier 已经出现 LM-relevant specialization

这是 `Phase6` 最重要的新结论。它第一次用 token-level 反事实 gap 直接回答：

$$
\text{被 router 选中的 expert，是否真的比替代 expert 更能降低 next-token loss？}
$$

答案是肯定的。

在 `wos_middle` 上：

- `flat_moe_raw_uniform` 的 `G(second) ≈ -0.0020`
- `hier_moe_tail_uniform` 的 `G(second) = 0.0489`
- `router_raw_expert_tail_uniform` 的 `G(second) = 0.0441`

在 `wos_rare` 上：

- `flat_moe_raw_uniform` 的 `G(second) ≈ -0.0026`
- `hier_moe_tail_uniform` 的 `G(second) = 0.0604`
- `router_raw_expert_tail_uniform` 的 `G(second) = 0.0567`

这一步极其关键，因为它让我们可以把主线从：

$$
\text{single-layer combined tail-conditioned block works}
$$

升级为：

$$
\text{single-layer combined tail-conditioned block already exhibits LM-relevant specialization.}
$$

但它也保留了一个边界：`route margin` 与 `G_cf` 的相关性仍然很弱，所以当前能说的是“选对 expert 有用”，还不能说“router calibration 已经很好”。

### 19.2 `Phase6-B`：不是 middle 唯一最优，而是 tail-oriented band 最有价值

`Phase6-B` 的初始问题是：

$$
\text{experts 最该学的，到底是 head、middle、extreme tail，还是 full tail residual？}
$$

结果比最初的 “middle tail” 假设更细。

如果看主指标 `WoS rare-token PPL`：

- `router_raw_expert_tail_uniform = 80.0392`
- `router_raw_expert_extreme_uniform = 80.0758`
- `router_raw_expert_middle_uniform = 81.0415`
- `router_raw_expert_head_uniform = 83.1055`
- `baseline_ffn = 83.6731`
- `router_raw_expert_raw_uniform = 83.6789`

如果看 `middle-frequency token PPL`：

- `extreme = 59.9433`
- `tail = 59.9559`
- `middle = 60.5447`

所以最准确的结论不是：

$$
\text{middle uniquely dominates}
$$

而是：

$$
\text{the useful expert-input region is tail-oriented.}
$$

其中：

- `full tail residual` 略偏向优化 `rare-token` 主指标
- `extreme tail` 略偏向优化 `middle-token` 指标

这一步把导师式的 “middle tail” 直觉，收束成了一个更 defendable 的结论：**真正值得押注的不是 raw/head，而是 tail-oriented band；至于是 full tail 还是更 extreme 的 tail，还要在下一轮继续细化。**

### 19.3 `Phase6-C`：recursive gap 的 primary bottleneck 在 coarse routing

这是 `Phase5-D1` 的真正后续。它回答：

$$
R6_{\mathrm{oracle}} \gg R5_{\mathrm{learned}}
$$

到底意味着什么。

关键结果是：

- `R5 = 8775.19`
- `R5c = 2951.38`
- `R5d = 9121.51`
- `R5e = 8417.96`
- `R5f = 7255.76`
- `R6 = 1057.94`

其中最重要的结构关系是：

$$
R5c \ll R5,\qquad R5d \not< R5.
$$

这说明：

1. `coarse routing` 是 primary bottleneck；
2. 只修 `fine-local routing` 并不能救回来；
3. `teacher-aided CE` 还能继续缩小 gap，所以训练信号也是第二层问题；
4. 但即便如此，距离 `R6` 还有很大差距，因此当前绝不能把 recursive learned hierarchy 讲成已经成立。

### 19.4 `Phase6` 对整个主线到底新增了什么

如果压成一句话，`Phase6` 的新增价值是：

$$
\text{它把“单层 hierarchical 结构成立”推进成了“单层 hierarchical 结构已经具有功能性的 expert specialization”。}
$$

并且同时告诉我们：

1. expert 输入应该看 `tail-oriented band`，不是 `raw/head`
2. recursive 方向如果还要继续，先修 `coarse routing`，不要先修 `fine-local routing`

### 19.5 `Phase6 no-LB`：哪些结论对去掉 `LB` 仍然稳健

在补做完 `Phase6-D1 / D2 / D3` 之后，我们现在可以把 `Phase6` 的结论进一步分成两层：

第一层：对 `no-LB` 稳健的结构结论  
第二层：仍然会随着 `LB` 改变的精细排序

#### 19.5.1 `Phase6-A` 的主结论对 `no-LB` 稳健

在 `no-LB` 下，

$$
\text{hier\_moe\_tail\_no\_lb}
$$

仍然满足：

$$
G_{\mathrm{second}}^{\mathrm{wos\_middle}} = 0.0356 > 0,
\qquad
G_{\mathrm{second}}^{\mathrm{wos\_rare}} = 0.0439 > 0.
$$

而且

$$
\text{router\_raw\_expert\_tail\_no\_lb}
$$

更强：

$$
G_{\mathrm{second}}^{\mathrm{wos\_middle}} = 0.0679,
\qquad
G_{\mathrm{second}}^{\mathrm{wos\_rare}} = 0.0829.
$$

所以 `LM-relevant specialization` 这条结论，不是靠 mild `LB` 才成立的。

#### 19.5.2 `Phase6-B` 的大结论对 `no-LB` 也稳健，但细排序不稳

`with-LB` 下：

$$
\text{rare-token 最优} = \text{tail},
\qquad
\text{middle-token 最优} = \text{extreme}.
$$

`no-LB` 下：

$$
\text{rare-token 最优} = \text{extreme},
\qquad
\text{middle-token 最优} = \text{extreme}.
$$

但无论有无 `LB`，稳定事实都没有变：

$$
\text{extreme / tail / middle} \ll \text{head / raw / baseline}.
$$

所以我们现在能稳稳写下来的，不是：

$$
\text{full tail residual 一定严格优于 extreme tail}
$$

而是：

$$
\text{useful expert-input region is tail-oriented.}
$$

#### 19.5.3 `Phase6-C` 的递归诊断对 `no-LB` 也稳健

`no-LB` 下仍然有：

$$
R5c \ll R5,\qquad R5d \not< R5.
$$

因此：

$$
\text{coarse routing is the primary recursive bottleneck}
$$

不是一个依赖 `LB` 的偶然现象，而是当前递归线的稳定诊断。

#### 19.5.4 `Phase6 no-LB` 之后，主线到底修正成什么

这轮补实验最重要的意义是：它把我们对 `LB` 的定位进一步收窄了。

现在最合理的口径是：

$$
\text{LB 不是主线理论成立的必要条件。}
$$

更具体地说：

1. 单层 `LM-relevant specialization` 不依赖 `LB`
2. `tail-oriented expert-input region` 不依赖 `LB`
3. `coarse routing bottleneck` 也不依赖 `LB`

真正仍然不稳定的，只是这些 finer-grained 的 ranking：

1. `tail` 与 `extreme` 谁是唯一最优
2. `router calibration` 是否已经够好

所以当前最稳的主线，已经可以写成：

$$
\text{split-first} \rightarrow \text{single-layer tail-conditioned routing} \rightarrow \text{LM-relevant specialization}
$$

并把 `no-LB geometry routing` 作为概念默认口径；mild `LB` 现在更像是可选训练配方，而不是理论成立所必须依赖的组件。

所以到 `Phase6` 为止，最稳、最适合继续推进的主线已经可以写成：

$$
\text{shared head} \rightarrow \text{split-first} \rightarrow \text{single-layer tail-conditioned routing} \rightarrow \text{LM-relevant specialization}
$$

而递归部分目前仍然只是：

$$
\text{oracle headroom exists, but learned recursive hierarchy is not closed yet.}
$$

---

## 20. 组会应该怎么讲：把故事线压成一条主线

如果把整个项目压成一条最清楚的故事线，我建议按下面四步来讲：

### 20.1 第一步：先证明问题本身成立

我们最开始不是直接去做 hierarchical MoE，而是先问：

$$
\text{真实 hidden 中，到底有没有一个 shared head，使得 raw hidden 不适合直接做 tail learning？}
$$

`Phase1` 给出的答案是：有。

所以故事线的起点不是 “我想做 MoE”，而是：

$$
\text{真实 hidden 的几何已经告诉我们，应该先 split common / tail。}
$$

### 20.2 第二步：再证明单层真实 block 确实 work

`Phase4-C1` 和 `Phase5-C2 / C2.5 / C2.6` 一起把这个命题压清楚了：

1. 真实单层 `combined tail-conditioned block` 已经优于 `baseline` 和 `flat raw MoE`
2. 这个收益不只是 split，也不只是容量
3. 当前最稳定的 routed 单因素增益更像是

$$
E_i(x) \rightarrow E_i(x_t)
$$

而不是

$$
g_i(x) \rightarrow g_i(x_t)
$$

所以到 `Phase5` 为止，故事线已经不是“hier 可能有点用”，而是：

$$
\text{single-layer combined tail-conditioned block 在真实模型里已经成立。}
$$

### 20.3 第三步：再把“结构成立”推进成“功能成立”

`Phase6-A` 是这一轮真正的关键增量，因为它第一次直接问：

$$
\text{被 router 选中的 expert，是否真的比替代 expert 更能降低当前 token 的 next-token loss？}
$$

答案是肯定的。

因此主线被进一步推进成：

$$
\text{single-layer combined tail-conditioned block already exhibits LM-relevant specialization.}
$$

这比“purity 更高”“NMI 更高”都更硬，因为它直接落在 token-level NLL 上。

### 20.4 第四步：最后说明后面的路该怎么走

`Phase6-B / C` 和后续 `D1 / D2 / D3` 解决的是“下一步往哪儿推”。

- `Phase6-B / D2` 告诉我们：expert 真正该看的不是 `raw/head`，而是 `tail-oriented band`，而且这条结构结论对 `no-LB` 稳健
- `Phase6-C / D3` 告诉我们：recursive 如果还要继续，先修 `coarse routing`，不要先修 `fine-local routing`

所以现在最清楚的一句话主线是：

$$
\text{shared head} \rightarrow \text{split-first} \rightarrow \text{single-layer combined tail-conditioned routing} \rightarrow \text{LM-relevant specialization}
$$

而不是：

$$
\text{recursive learned hierarchy has already succeeded.}
$$

---

## 21. 现在最真实的问题到底在哪里

到 `Phase6` 为止，我们已经不再卡在“有没有正结果”，而是卡在更细的三个点上。

### 21.1 问题一：router 几何仍然不够好

`Phase6-A` 已经说明：

$$
G_{\mathrm{cf}} > 0
$$

成立，也就是当前 expert selection 已经有功能性价值。  
但同时 `route margin` 与 `G_cf` 的相关性仍然很弱。

这说明两件事同时成立：

1. router 选中的 expert 的确更好
2. 但 router 自己对“什么时候真的选对了”还不够敏感

所以当前真正没想清楚的不是 “selection 有没有用”，而是：

$$
\text{为什么 selection 已经有用，但 router 几何仍然和真实 expert advantage 对不齐？}
$$

### 21.2 问题二：tail-oriented 已成立，但 band 还没最终定死

`Phase6-B` 已经排除了 `raw/head`，但还没有在

$$
\text{full tail residual} \quad vs \quad \text{extreme tail}
$$

之间给出完全终局的答案。

现在最准确的状态是：

- `with-LB` 下，`full tail` 在 `rare-token PPL` 上最好
- `no-LB` 下，`extreme tail` 在 `rare-token PPL` 上轻微反超
- 二者都明显优于 `raw/head`

所以现在可以 defend 的是：

$$
\text{tail-oriented band is the right family}
$$

但还不能说：

$$
\text{one exact band has already uniquely won.}
$$

### 21.3 问题三：recursive 的第一瓶颈已经定位，但学习闭环还没做出来

`Phase6-C` 已经让 `R6 \gg R5` 不再只是一个模糊现象，而是更具体地变成了：

$$
R5c \ll R5,\qquad R5d \not< R5.
$$

也就是说，当前 recursive gap 的第一瓶颈已经定位到了 `coarse routing`。

但问题在于：  
**知道 primary bottleneck 在哪，不等于已经知道怎么把它学出来。**

所以递归主线现在真正的问题是：

$$
\text{如何让 learned coarse router 更逼近 oracle coarse routing？}
$$

---

## 22. 下一步最合理的规划

如果接下来继续推进，我建议把顺序定成下面三步。

### 22.1 第一步：把 no-LB geometry routing 当成新的默认概念口径

现在已经可以确认，下面三条主结论都对 `no-LB` 稳健：

1. 单层已经出现 `LM-relevant specialization`
2. expert 最该看的输入是 `tail-oriented band`
3. recursive 的 primary bottleneck 在 `coarse routing`

因此下一步最合理的理论口径，不再是 “with-LB 才成立”，而应改成：

$$
\text{no-LB geometry routing as the conceptual default.}
$$

这不等于 `LB` 以后完全无关，而是：

$$
\text{LB is not required for the key structural conclusions.}
$$

### 22.2 第二步：继续研究 router 几何如何对齐 token-level expert advantage

在单层主线上，下一步更值得推进的不是继续扫更多 proxy，而是直接研究：

$$
\Delta_i(t) = \ell_{\setminus i}(t) - \ell_i(t)
$$

或更广义的 token-level expert advantage，看看是否能把 router 学得更接近真实有效的选择边界。

也就是说，下一步该问的是：

$$
\text{how to align routing geometry with token-level expert advantage?}
$$

### 22.3 第三步：继续细化 tail band，再谈更强的可学习 routing 几何

`Phase6-B / D2` 现在已经把 band 问题进一步收窄成：

$$
\text{tail-oriented family is right, but tail vs extreme is still open.}
$$

因此更值得推进的不是继续比较 `raw/head`，而是：

1. 连续化 / 可学习 band 设计
2. 解释为什么 `tail` 与 `extreme` 会随 `LB` 轻微换位
3. 直接比较哪一种 band 更对齐 token-level expert advantage

### 22.4 第四步：recursive 先修 coarse router，再谈真实模型递归

`Phase6-C / D3` 已经说明，下一步如果还要碰 recursive，不应该先去修 `fine-local routing`，而应按：

1. `coarse router`
2. `teacher-aided coarse/fine supervision`
3. 只有在 small-model 缩小 `R6-R5` gap 之后，再考虑真实 recursive Qwen

所以现在最不该做的事情是：

$$
\text{直接跳到真实 recursive Qwen，假设它会自己学出来。}
$$

---

## 23. 当前武器库：固定认识与实验证据

下面这些是现在最值得反复使用的“固定认识 + 证据”。

### 23.1 `shared head` 真实存在

证据：`Phase1` 中 `layer 35` 的 top-8 explained variance 约为 `0.4069`，且 `tail_residual` 的 `probe / purity / NMI` 在两个正式 seed 上都稳定优于 `raw / centered`。

因此可以稳定使用的结论是：

$$
\text{真实 hidden state 中确实存在 low-rank shared head.}
$$

### 23.2 单层真实 block 上，combined tail-conditioned block 已经成立

证据：`Phase4-C1` 中

$$
81.5287 < 84.0007 < 85.0412
$$

即 `hier_moe_tail_uniform` 在 `WoS rare-token PPL` 上同时优于 `baseline_ffn` 和 `flat_moe_raw_uniform`。

因此可以稳定使用的结论是：

$$
\text{single-layer combined tail-conditioned block already beats baseline and flat raw MoE in real models.}
$$

### 23.3 routed family 里，主增益更像来自 expert-tail input

证据：`Phase5-C2.5` 中

$$
448.6350 \ll 471.7282 \approx 472.3493
$$

即 `router_raw_expert_tail_uniform` 明显强于 `router_tail_expert_raw_uniform` 与 `flat`。

因此可以稳定使用的结论是：

$$
\text{the most reliable single routed gain currently comes from } E_i(x)\rightarrow E_i(x_t).
$$

### 23.4 当前单层 hier 已经出现 LM-relevant specialization，而且这点对 no-LB 稳健

证据：`Phase6-A` 中

$$
G_{\mathrm{second}}^{\mathrm{middle}} = 0.0489,\qquad
G_{\mathrm{second}}^{\mathrm{rare}} = 0.0604
$$

而 `Phase6-D1` 中 `hier / expert-tail` 在 `no-LB` 下仍然明显强于 `flat`。

因此可以稳定使用的结论是：

$$
\text{current single-layer hier already exhibits LM-relevant specialization.}
$$

### 23.5 expert 真正该看的是 tail-oriented band，而且这点对 no-LB 稳健

证据：`Phase6-B` 中 `tail / extreme` 在 `WoS rare-token PPL` 与 `middle-token PPL` 上都明显优于 `raw / head / baseline`；`Phase6-D2` 则说明这条“大结论”在去掉 `LB` 后仍然成立。

因此可以稳定使用的结论是：

$$
\text{the useful expert-input region is tail-oriented rather than raw/head-oriented.}
$$

### 23.6 recursive 的第一瓶颈已经定位到 coarse routing，而且这点对 no-LB 稳健

证据：`Phase6-C` 中

$$
R5c = 2951.38 \ll 8775.19 = R5,\qquad
R5d = 9121.51 \not< R5.
$$

因此可以稳定使用的结论是：

$$
\text{coarse routing is the primary recursive bottleneck.}
$$

而 `Phase6-D3` 在 `no-LB` 下仍然保持同样的结构关系。

---

## 24. 组会里最短的一分钟讲法

如果只用一分钟，我建议按下面这个模板来讲：

> 我主要在探究这样一个问题：真实模型里，为什么 `split-first` 的单层 hierarchical block 会比 `flat raw MoE` 更好，以及它到底是不是已经出现了真正有用的 expert specialization。  
> 为此，我先做了 `Phase1` 去证明真实 hidden 里确实存在 `shared head`；然后在 `Phase4/5` 做真实单层 block replacement，证明 `combined tail-conditioned block` 已经优于 `baseline` 和 `flat raw MoE`；最后在 `Phase6-A/B/C` 又分别做了反事实 expert gap、band intervention 和 recursive oracle-gap bridge。  
> 我观察到三个关键现象：第一，当前单层 `hier` 的 `G_cf(second)` 在 `middle / rare` token 上稳定为正，说明它已经出现了 `LM-relevant specialization`；第二，expert 真正该看的不是 `raw/head`，而是 `tail-oriented band`；第三，recursive gap 的第一瓶颈在 `coarse routing`。  
> 这说明当前最稳的结论是：真实模型中的 single-layer combined tail-conditioned block 不只是结构上更好，而且已经出现了功能性的 expert specialization；并且这个方向对 no-LB 也是稳健的。  
> 但我目前还没有完全想清楚的一点是，为什么 `G_cf` 已经为正，而 router 的 `route margin` 与真实 expert advantage 的相关性仍然很弱；另外，`full tail` 和 `extreme tail` 为什么会在 with-LB / no-LB 下轻微换位。这会直接影响后续如何继续推进几何路由，以及 recursive 里的 coarse router 该怎么学。  
> 下一步我准备把 no-LB geometry routing 作为默认概念口径，继续研究如何让 router 几何更对齐 token-level expert advantage，并在 recursive 上优先修 coarse routing。
