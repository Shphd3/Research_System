# Phase6 实验总报告

## 0. 文档定位

这份文档是 `Phase6` 的总报告。它把 `Phase6-A / B / C` 与后续 `no-LB` 补实验放在同一条主线上统一解释，回答三个问题：

1. 当前单层 hier block 是否已经表现出真正的 `LM-relevant specialization`；
2. 如果 expert input 是关键，那么 experts 到底更该看哪一段频带；
3. recursive hierarchy 还没有起来时，主瓶颈到底在什么地方。

如果读者需要更细的单实验细节，可分别阅读：

- `phase6A_report.md`
- `phase6B_report.md`
- `phase6C_report.md`

其中 `no-LB` 结果已经并入上述三份分报告与本总报告，不再单独维护一份独立 follow-up 文档。

## 1. 一页结论

`Phase6` 跑完以后，当前最稳的三条结论是：

1. 单层 `tail-conditioned` block 已经不只是“结构上更好”，而是已经出现了

$$
\text{LM-relevant specialization.}
$$

也就是说，router 选中的 expert 在 token-level NLL 上，确实优于 `second-best / random` 反事实替换。

2. expert 最有用的输入区间不是 `raw / head`，而是更偏 tail 的频带。当前更准确的写法是

$$
\text{the useful expert-input region is tail-oriented.}
$$

这里 `full tail residual` 与 `extreme tail` 都是强候选，但二者的细粒度排序还不够稳定。

3. recursive learned hierarchy 现在最主要的问题不是 fine-local route，而是

$$
\text{coarse routing.}
$$

更具体地说，`R5c \ll R5` 而 `R5d \not< R5` 这一模式，在 `with-LB` 和 `no-LB` 下都成立。

同时，本轮也明确了几条不能写得过满的边界：

- 不能把 `Phase6` 的结果写成“router calibration 已经很好”；
- 不能把 `tail` 与 `extreme` 的排序写成已经钉死；
- 不能把 recursive 线写成“已经准备好直接上真实 recursive Qwen”。

## 2. 共享记号与实验对象

令当前 block 输入 hidden 为：

$$
x \in \mathbb{R}^d.
$$

令 centered hidden 为：

$$
x_c = x - \mu.
$$

若 centered covariance 的前 $k$ 个主方向为 $V_k$，则 tail residual 写为：

$$
x_t = P_t(x-\mu), \qquad P_t = I - V_k V_k^\top.
$$

本报告中最常见的三类 routed block 写法分别是：

$$
\text{flat: } h_{\mathrm{out}} = h_{\mathrm{in}} + E_c(x) + \sum_i g_i(x)E_i(x),
$$

$$
\text{expert-tail: } h_{\mathrm{out}} = h_{\mathrm{in}} + E_c(x) + \sum_i g_i(x)E_i(x_t),
$$

$$
\text{hier: } h_{\mathrm{out}} = h_{\mathrm{in}} + E_c(x) + \sum_i g_i(x_t)E_i(x_t).
$$

若无特别说明，`with-LB` 的 routed 配置都带：

$$
L = L_{\mathrm{LM}} + \beta_{\mathrm{lb}}L_{\mathrm{LB}},
\qquad
\beta_{\mathrm{lb}} = 0.01.
$$

对应的 `no-LB` 补实验则把这一项去掉，训练目标变成：

$$
L = L_{\mathrm{LM}}
$$

或在 recursive family 中更一般地写为：

$$
L = L_{\mathrm{LM}} + \lambda_{\mathrm{aux}}L_{\mathrm{aux}}.
$$

## 3. 为什么要做 Phase6

到 `Phase5` 结束时，我们已经知道：

- `single-layer combined tail-conditioned block` 在真实模型里是正结果；
- 但还不能说当前专家已经出现了真正的功能性 specialization；
- 也不能说 expert 到底该看 `full tail residual`、`extreme tail`，还是别的带宽；
- recursive 线还有一个很强的 oracle upper bound，但 learned 版本没学出来。

因此，`Phase6` 的作用不是重复跑 `Phase5`，而是把主线从：

$$
\text{this block works}
$$

推进到：

$$
\text{why it works, where it works, and where it still fails.}
$$

## 4. Phase6-A：当前单层 hier 是否已经出现 LM-relevant specialization

### 4.1 实验问题

`Phase6-A` 不是看 purity / NMI 这类代理指标，而是直接看：如果把当前 token 强行送到别的 expert，next-token NLL 会不会变差。

核心反事实指标写为：

$$
G_{\mathrm{cf}}(e')
=
\mathbb{E}\left[
\ell\big(y, f_{e'}(c)\big)
-
\ell\big(y, f_{e^\star}(c)\big)
\right].
$$

若

$$
G_{\mathrm{cf}}(e') > 0,
$$

则说明当前 router 选中的 expert 对当前 token 的确更合适。

### 4.2 with-LB 主结果

`Phase6-A` 的 gate 为：

```json
{
  "a_pass": true,
  "conclusion_text": "hier middle G_second=0.0489, hier rare G_second=0.0604; A-pass=True."
}
```

关键数值如下：

- `flat_moe_raw_uniform`
  - `wos_middle: G(second) = -0.0020`
  - `wos_rare: G(second) = -0.0026`
- `router_raw_expert_tail_uniform`
  - `wos_middle: G(second) = 0.0441`
  - `wos_rare: G(second) = 0.0567`
- `hier_moe_tail_uniform`
  - `wos_middle: G(second) = 0.0489`
  - `wos_rare: G(second) = 0.0604`

而且这个方向与真实主指标同向：`hier / expert-tail` 的 `WoS rare-token PPL` 都优于 `flat`。

### 4.3 这一步到底证明了什么

`Phase6-A` 支持的是：

$$
\text{single-layer tail-conditioned block already exhibits LM-relevant specialization.}
$$

它不支持的则是：

- “router-only 已经完全成立”；
- “router 分数越尖锐，收益就一定越大”。

原因是：`route margin` 与 `G_{\mathrm{cf}}` 的相关性仍然很弱，所以当前能说的是“选对 expert 有用”，还不能说“router calibration 已经成熟”。

## 5. Phase6-B：experts 更该看哪一段频带

### 5.1 实验问题

`Phase6-B` 固定 router 看 raw hidden，只改变 expert 输入 band，比较：

- `raw`
- `head`
- `middle`
- `extreme tail`
- `full tail residual`

因此，这一步回答的是：

$$
\text{如果 expert input 才是关键，那 experts 最值得学习哪一段频带？}
$$

### 5.2 with-LB 主结果

`Phase6-B` 的 gate 为：

```json
{
  "best_config_by_middle_frequency_token_ppl": "router_raw_expert_extreme_uniform",
  "best_config_by_wos_rare_token_ppl": "router_raw_expert_tail_uniform"
}
```

聚合主结果如下：

- `router_raw_expert_tail_uniform`
  - `WoS rare-token PPL = 80.0392`
  - `middle-token PPL = 59.9559`
- `router_raw_expert_extreme_uniform`
  - `WoS rare-token PPL = 80.0758`
  - `middle-token PPL = 59.9433`
- `router_raw_expert_middle_uniform`
  - `WoS rare-token PPL = 81.0415`
- `router_raw_expert_head_uniform`
  - `WoS rare-token PPL = 83.1055`
- `router_raw_expert_raw_uniform`
  - `WoS rare-token PPL = 83.6789`
- `baseline_ffn`
  - `WoS rare-token PPL = 83.6731`

### 5.3 这一步到底证明了什么

这一步支持的不是：

$$
\text{middle is uniquely best.}
$$

而是：

$$
\text{the useful expert-input region is tail-oriented.}
$$

更细地说：

- `full tail residual` 更偏向优化主指标 `WoS rare-token PPL`；
- `extreme tail` 更偏向优化 `middle-token PPL`；
- `raw / head` 明显不够好。

所以当前最稳的 claim 是：

$$
\text{experts should look at a tail-oriented band, not raw/head-dominated input.}
$$

## 6. Phase6-C：recursive 线为什么还没起来

### 6.1 实验问题

`Phase6-C` 继续留在 synthetic recursive small-model family，不直接上真实 recursive Qwen，而是拆解：

$$
R6_{\mathrm{oracle}} \gg R5_{\mathrm{learned}}
$$

到底意味着什么。

这里：

- `R5`：learned coarse + learned fine
- `R6`：oracle coarse + oracle fine
- `R5c`：oracle coarse + learned fine
- `R5d`：learned coarse + oracle fine local

### 6.2 with-LB 主结果

关键数值如下：

- `R5 = 8775.19`
- `R5c = 2951.38`
- `R5d = 9121.51`
- `R6 = 1057.94`

对应 gate 为：

```json
{
  "r5c_improvement_vs_r5": 5823.8124,
  "r5d_improvement_vs_r5": -346.3190,
  "conclusion_text": "Coarse routing is the primary recursive bottleneck."
}
```

### 6.3 这一步到底证明了什么

最关键的模式是：

$$
R5c \ll R5,\qquad R5d \not< R5.
$$

这说明：

- 只要 coarse routing 正确，系统立刻大幅改善；
- 只修 fine-local routing，并不能救回整体系统。

因此 `Phase6-C` 最稳的结论是：

$$
\text{coarse routing is the primary recursive bottleneck.}
$$

同时，因为 `R5c` 与 `R6` 之间仍有明显剩余 gap，当前也不能把问题简单写成“只要 coarse 对了就完全够了”。剩余 gap 里仍然包含 fine routing / training signal / support 问题。

## 7. no-LB 补实验：哪些结论不依赖 LB

`Phase6-D1 / D2 / D3` 的作用不是重写主线，而是检查 `Phase6-A / B / C` 的结论对 `LB` 是否稳健。

### 7.1 D1：A-noLB

关键结果：

- `flat_moe_raw_no_lb`
  - `wos_middle: G(second) = 0.0041`
  - `wos_rare: G(second) = 0.0082`
- `hier_moe_tail_no_lb`
  - `wos_middle: G(second) = 0.0356`
  - `wos_rare: G(second) = 0.0439`
- `router_raw_expert_tail_no_lb`
  - `wos_middle: G(second) = 0.0679`
  - `wos_rare: G(second) = 0.0829`

因此：

$$
\text{LM-relevant specialization is robust to removing LB.}
$$

而且 `no-LB` 下更强的组其实变成了 `router_raw_expert_tail_no_lb`。

### 7.2 D2：B-noLB

关键结果：

- `router_raw_expert_extreme_no_lb`
  - `WoS rare-token PPL = 80.2372`
  - `middle-token PPL = 60.2245`
- `router_raw_expert_tail_no_lb`
  - `WoS rare-token PPL = 80.2819`
  - `middle-token PPL = 60.2561`
- `raw / head / baseline` 仍明显更差

因此：

$$
\text{tail-oriented band remains robust without LB.}
$$

但 `tail` 与 `extreme` 的细粒度排序并不稳定，所以当前不能把某一者写成唯一正确答案。

### 7.3 D3：C-noLB

关键结果：

- `R5 = 9269.80`
- `R5c = 2995.38`
- `R5d = 9445.16`
- `R6 = 1130.28`

因此仍有：

$$
R5c \ll R5,\qquad R5d \not< R5.
$$

所以：

$$
\text{coarse routing is the primary recursive bottleneck}
$$

这条诊断同样不依赖 `LB`。

## 8. 现在最稳的结论，和还不能写太满的地方

### 8.1 现在最稳的三条结论

补完 `with-LB + no-LB` 以后，当前最稳的三条结论是：

1. 

$$
\text{single-layer tail-conditioned block already exhibits LM-relevant specialization;}
$$

2.

$$
\text{the useful expert-input region is tail-oriented;}
$$

3.

$$
\text{coarse routing is the primary recursive bottleneck.}
$$

### 8.2 仍然不能写得太满的地方

当前仍需要保守写法的地方有三处：

1. `tail` 与 `extreme` 的细排序还不稳定；
2. `route margin` 与 `G_{\mathrm{cf}}` 的弱相关问题还在；
3. recursive 线还不能直接升级到真实 recursive Qwen。

所以当前最合理的主线写法不是：

$$
\text{everything about hierarchical routing is already solved.}
$$

而是：

$$
\text{single-layer tail-conditioned routing has become a real, LM-relevant result,}
$$

同时：

$$
\text{recursive hierarchy still mainly fails at coarse routing.}
$$

## 9. 对总主线的意义

`Phase6` 之后，整条主线已经可以从：

$$
\text{shared head exists} \rightarrow \text{split-first block works}
$$

进一步收束到：

$$
\text{shared head exists}
\rightarrow
\text{single-layer tail-conditioned block works}
\rightarrow
\text{this block already exhibits LM-relevant specialization.}
$$

并且，当前最值得继续推进的方向也更清楚了：

- 单层线：继续细化 `full tail residual / extreme tail` 的 expert-input 设计；
- 递归线：优先修 coarse routing，而不是先修 fine-local route；
- `LB`：保留为可选训练配方，但不再视为这条主线成立所必需的核心条件。
