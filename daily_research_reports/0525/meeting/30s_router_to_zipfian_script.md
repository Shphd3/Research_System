# 30s Group Meeting Script - Router Specialization To Zipfian

Source sync:

```text
Projects/from-attention-to-search/XingyuD/sync/0524_router_feature_specialization/report.md
Projects/from-attention-to-search/XingyuD/sync/0525_zipfian_hierarchical/report.md
```

## 30s Script

我这两天主要在检查 top-1 sparse MoE router 到底有没有形成有功能意义的 expert specialization。0524 的 uniform AB/CB 结果显示：corrected selected-gate sparse router 可以学会任务，semantic initialization 或 semantic refresh 也能制造早期语义 routing，但训练后这条语义 route 会衰减；更关键的是，routing heatmap 上的语义结构没有稳定转化成 ablation-based functional expert。因此当前结论是：semantic separability 不是 functional specialization 的充分条件，问题更像 route assignment、expert utility 和 NTP objective 没有对齐。

基于这个结论，我下一步转到 Zipfian hierarchical-sense synthetic setup，不是无端换数据集，而是为了测试更接近语言分布的 token frequency skew 是否会放大这种 route-function mismatch。这个数据里同一个 token $b_i$ 有 common meaning 和 context-conditioned senses：`r b_i` 是 neutral/common，`A b_i`、`C b_i` 是不同上下文 sense。H0529a 的目的就是比较 uniform flat 和 Zipfian flat，看 Zipfian 是否削弱 tail context-sense functional specialization；H0530a 再比较 flat Zipfian 和 hierarchical common/sense MoE，看显式 common/sense 分解是否能改善 route-function alignment。主指标仍然是 ablation-based $S_{\mathrm{sense}}$ 和 route-function alignment，不用 routing heatmap 单独下结论。

## One-Sentence Transition

0524 证明了“看起来 semantic 的 route 不等于 functional expert”，所以 0525 的 Zipfian 实验是在问：真实语言式的频率不均衡会不会进一步诱导 flat router 走 token/common/frequency shortcut，以及 hierarchy 是否能把 common meaning 和 context-conditioned sense function 分开。

## Zipfian Experiment Purpose And Links

### H0529a Zipfian Frequency Shortcut

Purpose:

```text
判断 token-Zipfian frequency 是否会削弱 flat top-1 selected-gate sparse MoE 的 tail context-sense functional specialization。
```

Key decision metric:

```text
tail bucket ablation-based S_sense and tail route-function alignment
```

Links:

```text
Purpose card:
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/purpose_card.md

Closure:
Projects/from-attention-to-search/main/hypotheses/H0529a_zipfian_frequency_shortcut/hypothesis_closure.md

Summary:
Projects/from-attention-to-search/main/experiments/H0529a_zipfian_frequency_shortcut/summary.md
```

### H0530a Hierarchical Common/Sense MoE

Purpose:

```text
判断 two-level common/sense Hierarchical MoE 是否比 flat Zipfian top-1 sparse MoE 更能形成 tail context-sense functional specialization。
```

Key decision metric:

```text
tail S_sense, tail route-function alignment, and uniform-eval tail CE
```

Links:

```text
Purpose card:
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/purpose_card.md

Closure:
Projects/from-attention-to-search/main/hypotheses/H0530a_hierarchical_common_sense_moe/hypothesis_closure.md

Summary:
Projects/from-attention-to-search/main/experiments/H0530a_hierarchical_common_sense_moe/summary.md
```

## Claim Boundary For Meeting

可以说：

```text
uniform setup 已经把问题从 semantic separability 收紧到 route-function alignment。
Zipfian setup 是为了测试 token-frequency skew 是否放大这个 mismatch。
Hierarchy comparison 是为了测试 common/sense decomposition 是否能改善 functional expert utility。
```

不要说：

```text
Zipfian 一定更真实所以一定更好。
Hierarchy 是已经确认的修复方向。
routing heatmap 的语义结构就是 expert specialization。
```
