# A08 Preserved Specialization Presentation Brief

## 核心结论

08 的目标是构造一种新的 MoE gating/training 方法：它能在 real data 上初始化 specialization，并在 early training 中保存这个 specialization。这里的 specialization 重新定义为三层：初始化 route identity、early-training preservation、以及后续 functional utility。

当前不是说方法已经成功，而是已经把 05/06/07 和导师主线组织成一条十轮可证伪路线。

## 一句话主线

```text
稳定奇异方向可以作为 gate-forward 方向；
但 CE 会继续放大这些方向并覆盖路由；
所以我们要设计 singular-converged gating + anti-feedback training，
先保存 real-DCLM proxy partition，再测试 utility。
```

## 为什么需要 08

05 说明 common / early feedback 会影响 top-1 routing。

06 说明 real-DCLM proxy partition 可以在 step 0 初始化，但普通训练到 step 5/10 会擦掉。

07 说明 controlled nested surface 上，控制 tail update 进入 common subspace 的比例能改善 tail loss。

所以 08 的问题是：

```text
能不能把 07 的 update-space control 和导师的 singular direction intuition，
用于解决 06 的 real-DCLM preservation failure？
```

## 新定义

| 层级 | 含义 | 主指标 |
|---|---|---|
| Initialization specialization | step 0 route identity 成立 | proxy-route NMI |
| Preserved specialization | early training 后 route identity 仍在 | proxy_route_NMI@step5/10 |
| Functional specialization | preserved route 有功能价值 | tail loss / alpha_tail / fixed-route ablation |

## 十轮路线

1. A08_01：定义 singular direction convergence。
2. A08_02：测试 converged direction 能否变成 gate row。
3. A08_03：测试 common/residual split reservoir。
4. A08_04：测试 residual reservoir 能否循环抽取新方向。
5. A08_05：在 real DCLM 上审计 singular convergence。
6. A08_06：定义 real initialization specialization。
7. A08_07：分解 early training 为什么擦掉 proxy partition。
8. A08_08：在 controlled data 上测试 singular-converged gating 方法。
9. A08_09：在 real DCLM 上测试 preservation。
10. A08_10：测试 preserved partition 是否有 functional utility。

## 首批实验

首批执行 A08_01 到 A08_04，属于 synthetic / mechanism batch。

它们回答：

```text
方向稳定 -> gate forward -> split reservoir -> iterative direction discovery
```

通过后才进入 real-DCLM。

## 当前边界

可以说：

```text
08 已经形成从导师机制到 real-data preserved specialization 的研究路线。
```

不能说：

```text
方法已经解决 real-DCLM preservation；
route 已经有 utility；
真实语义 experts 已经存在。
```

## 下一步

执行四卡 batch：

```text
A08_01 -> A08_02 -> A08_03 -> A08_04
```

如果四卡通过，进入：

```text
A08_05 real-DCLM singular convergence audit
```
