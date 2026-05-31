# Advisor Report Card

## 0. 60s Version

目的：解释为什么最小 top-1 MoE router 会 collapse。

物理建模 / 假设：top-1 routing 对初始 router geometry 很敏感；早期同 expert 会造成 lock-in 和 starvation。

最小实验：2 orthogonal features、2 experts、linear top-1 router、NTP-style CE。

结论：失败 seed 在 step 0 已 collapse；成功 seed step 0 split 后稳定保持；去掉 router bias 只能把 random split 从 3/10 提高到 6/10。

关键证据：NMI trajectory、selected gate trajectory、counterfactual CE、initial router delta signs。

结论边界：只说明 route-pattern dynamics，不说明 utility-aligned specialization。

下一步：测试 structured router initialization 是否能系统性避免 early lock-in。

## 1. If interrupted, say this

我这次只想请老师判断：
这个最小实验是否足以支持“top-1 specialization 首先受 early router geometry / lock-in 控制”这个机制判断。

## 2. One-sentence Claim

```text
In the minimal 2x2 NTP-style top-1 proxy, route collapse is mainly an early
lock-in and starvation problem, not a late optimization drift problem.
```

## 3. Evidence Table

| observation | interpretation | boundary | next decision |
|---|---|---|---|
| failed seeds collapsed at step 0 | collapse starts before training dynamics | minimal proxy only | test anti-lock-in |
| success seed split stays stable | initial split can be amplified | not utility specialization | structured init |
| no-bias improves 3/10 to 6/10 | shared bias worsens collapse | no-bias not sufficient | compare init/noise/lb |

## 4. Questions For Advisor

1. Is structured router initialization the right next minimal mechanism?
2. Should this mechanism be tested before returning to multi-B slot experiments?
3. Which evidence would be enough to connect route-pattern separation to utility-best expert assignment?
