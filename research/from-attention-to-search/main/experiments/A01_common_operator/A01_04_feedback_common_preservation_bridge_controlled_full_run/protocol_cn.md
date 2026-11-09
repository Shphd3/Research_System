# Protocol CN: A01_04 Feedback Common Preservation Bridge Controlled Full Run

## 0. Approval Snapshot

Approval status：用户在 active goal 中要求执行 full run。

Purpose：在受控环境中测试 feedback-common drift 是否能解释并拯救 proxy-route NMI collapse。

Primary anchor：`01_04_feedback_common_preservation_bridge_anchor.md`。

Decision question：

```text
Does estimated feedback common explain step-0 to step-5/10 proxy-route NMI collapse?
```

Physical prior：

```text
preservation failure 可以是动态过程：
step-0 proxy geometry 有效，但 early training drift 会覆盖它。
```

Core model：

\[
\Delta h=P_{\mathrm{fb}}\Delta h+(I-P_{\mathrm{fb}})\Delta h
\]

Primary metric：

```text
proxy_nmi_drop_explained_by_feedback_common
```

含义：只 replay \(P_{\mathrm{fb}}\Delta h\) 能解释多少 full drift 造成的 NMI drop。

Basic setup：构造 step-0 可路由的 proxy hidden states，然后加入 common feedback drift、residual drift、nuisance drift，比较：

```text
step0
full_drift
feedback_only
residual_only
random_feedback_only
random_residual_only
```

Conditions：

```text
common_feedback
mixed_feedback_residual
residual_drift_control
nuisance_drift_control
weak_feedback
```

Pass：

```text
feedback regimes 中，feedback-only replay 能解释大部分 NMI drop；
residual-only replay 能 rescue 大部分 NMI；
random controls 不能达到同样效果。
```

Fail：

```text
full drift 会 collapse，但 feedback replay/removal 不能解释或拯救。
```

Insufficient：

```text
step0 proxy routing 不强；
full drift 不造成 collapse；
或者 NMI drop denominator 太小。
```

Cannot claim：

```text
不能 claim real-DCLM feedback causality；
不能 claim real preservation rescue；
不能 claim MoE utility。
```

关键边界：

```text
本地 `A06_01_04_E03/E04` 目前只有 trajectory metrics、summary、figures、logs，
没有可 replay/remove 的 hidden-state drift tensor。
所以真实 DCLM 版 01_04 需要先恢复或重跑 hidden/checkpoint artifact。
```
