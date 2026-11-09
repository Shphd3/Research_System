# Result Summary: H0522 Router Factor Audit Seq32

### Observation

四卡 ACP job `pt-xceqs84c` 已完成 Stage 1-5，四个 seed 为 `20260521, 20260522, 20260523, 20260524`。

最重要指标是 `factor -> expert_id` 的解释力，主要看 normalized mutual information，即某个 factor 和 expert id 的对应关系有多强。Stage 1/2 中，旧 H0521b checkpoint 的 `source_position` 和 `token_id` 最强：`source_position` 的平均 NMI 为 0.1205，router-logit \(R^2\) 为 0.3540；`token_id` 的平均 NMI 为 0.0861，router-logit \(R^2\) 为 0.3263。`rule_label` 平均 NMI 只有 0.0138。

### Interpretation

这说明 H0521b 中的 expert bucket 不是 clean rule/function bucket。它更像由 source position、token id 和 mixed hidden state 共同决定。

Stage 5 中，factor-disentangled synthetic task 的 eval accuracy 为 1.0，但 `rule_label` 并没有稳定强于 identity：`rule_label` 平均 NMI 为 0.0175，`first_identity` 为 0.0272，`second_identity` 为 0.3047，`target_id` 为 0.5070。这个结果进一步削弱了“普通 top-1 MoE 自然按 rule/function 分 expert”的解释。

### Limitation

Stage 5 当前构造仍然暴露了 target/second-token shortcut，因此它不能证明 router 一定不会学 rule/function。它只能说明：在这一版可学习的 seq_len=32 解耦任务中，ordinary MoE 更容易把 routing 对齐到 target/second-token shortcut，而不是稳定 rule/function。

### Key Figures

![Stage 1 factor NMI](figures/stage1_factor_nmi_by_seed.png)

Stage 1 显示 source-position 和 token-id 对 expert id 的解释力高于 rule/class。

![Stage 2 component flip rate](figures/stage2_component_flip_rate_by_seed.png)

Stage 2 显示移除 position / token-id component 更容易翻转 expert。

![Stage 5 disentangled NMI](figures/stage5_disentangled_nmi_by_seed.png)

Stage 5 显示 rule/function 没有稳定胜过 identity；target/second-token shortcut 更强。

### Claim Update

Result:

```text
ordinary no-load-balance top-1 MoE can solve the seq_len=32 synthetic tasks,
but its expert id is not a stable rule/function index.
```

Interpretation:

```text
router behavior is better described as position/token-id/target-shortcut
modulated mixed routing.
```

Claim boundary:

```text
This does not prove MoE routing is useless; it only rejects using this ordinary
top-1 expert id as a clean Reverse Index signal in the current setup.
```

### Decision

下一步不要直接做 Reverse Index alignment。先做 anti-shortcut synthetic：同时平衡 identity、position、target，让 rule/function 成为唯一真正可泛化因素，再看 `NMI(rule, expert_id) - NMI(identity/position/target, expert_id)` 是否跨 seed 稳定为正。
