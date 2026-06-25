# 05 研究线：ordinary top-1 routing 为什么失败

## 裁定

05 线的作用不是提出最终方法，而是解释失败机制：

```text
即使 feature frequency 是 uniform，top-1 gate 仍可能因为 common component、
wrong feature object 或 early lock-in 进入 collapse / merge basin。
```

## 物理先验

router 输入可以写成：

$$
h_f = c + r_f + n
$$

其中：

- $c$ 是不同 feature 共享的 common component；
- $r_f$ 是真正和 feature 相关的 route residual；
- $n$ 是非路由状态或 nuisance；
- gate logit 是 $z_{f,e}=w_e^\top h_f$。

如果 $w_e^\top c$ 或 $w_e^\top n$ 早于 $w_e^\top r_f$ 主导 top-1 选择，
router 就可能先进入错误 basin。之后 early-training feedback 会放大早期偏置。

## 关键证据

```text
A05_03: uniform toy 中 common offset 可以解释 step-0 dominant expert。
A05_04_02: common-logit cancellation 改善 no-position uniform slot routing。
A05_04_03: real DCLM 中 step-0 common margin 不是最大来源，但 centering 仍降低 load；
          到 step 10 common channel 被训练快速放大。
```

核心边界：

```text
toy common-logit causality 不能直接外推为 real-DCLM pure initialization cause。
real DCLM 更像 early-training feedback amplification，而不是 step-0 common
dominance alone。
```

## 与 06 的连接

05 得出的结论是：不要再把问题写成“让 load 均匀”。正确问题是：

```text
怎样找到 route-relevant feature residual，并让 gate 在训练中保持它？
```

这就是 06 线的任务。

## Source Links

```text
Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/
Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/summary.md
Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md
```

## Claim Boundary

可以说：

```text
ordinary top-1 routing 的失败不只是 frequency 问题；common component、错误对象
和 early feedback 都是必须控制的风险。
```

不能说：

```text
common cancellation 是可部署方案；
所有 real-data collapse 都由 step-0 common logit 导致；
expert utility 已经被证明或否定。
```
