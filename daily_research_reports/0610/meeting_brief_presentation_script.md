# Presentation Script for Meeting Brief

## 0. Opening

这次我想汇报的是两个 anchor 合起来后的主结论：在无 position embedding、feature 均匀的最小 setting 里，为什么 sparse top-1 MoE 还是不能自然形成 slot-to-expert specialization。

我们后续统一使用 dot-product router。之前 cosine similarity 和 dot-product 的现象一致，但这轮所有机制判断都以 dot-product 为 source of truth。

---

## 1. Setup

实验数据是一个最小 moving-block task。每条 sequence 只有一个连续三元组：

```text
SLOT_s B_CONST Y_s
```

这个 block 会在 sequence 里移动，position embedding 被去掉。loss 和 routing metric 都只在 `B_CONST` 位置计算。任务是在 `B_CONST` 位置根据前面的 `SLOT_s` 预测对应的 `Y_s`。

所以这个 setting 的目的很简单：slot 是真正决定 target 的 feature；如果 router 能形成 feature-to-expert specialization，它应该按 slot 形成稳定分发。

---

## 2. Conclusion 1

第一个结论是：collapse 不是因为 slot 信息缺失，也不是因为 slot-specialization 不可达。

baseline 在没有 position embedding、block 移动的条件下仍然 collapse。模型 accuracy 是 1.0，但 mean max_load 是 0.969，mean slot_NMI 只有 0.080。

同时，slot probe 显示 `h_B` 中 slot 信息可以被线性解码，held-out-position accuracy 是 1.0。

另外，slot-aware initialization 可以形成高 NMI 的 slot-level specialization，mean slot_NMI 是 0.980，accuracy 还是 1.0。

所以这里我们排除了三个一阶解释：不是模型没学会任务，不是 hidden state 没有 slot 信息，也不是 slot-specialization 本身不可实现。

---

## 3. Conclusion 2

第二个结论是：在 dot-product router 下，common component 对 router logit 的贡献是确定可分解的，而且它在训练早期就主导 routing decision。

我们把 routed hidden state 分解成：

```text
h = c + r_slot + u_position + residual
```

因为 router 是 dot-product，所以 score 可以精确分解成：

```text
w_e^T h = w_e^T c + w_e^T r_slot + w_e^T u_position + w_e^T residual
```

这不是数值 artifact。reconstruction error 的 mean 是 1.073e-7，max 是 5.849e-7。

结果显示，2238 / 2560 个 cells 是 common-dominant。更关键的是，step 0 的 common margin 已经是 0.2993，而 slot margin 只有 0.0523；step 0 的 common argmax 对 final dominant expert 的预测率是 0.844。到 step 10，common margin 增长到 1.7087，预测率变成 0.969。

所以 common-logit 不是 collapse 之后才出现的结果，它在早期 lock-in 之前就已经是一个强机制候选。

---

## 4. Conclusion 3

第三个结论是：减去 common-logit 可以显著提高 slot-level specialization，并保持 accuracy=1.0。

baseline 的 slot_NMI 是 0.080，max_load 是 0.969，accuracy 是 1.0。

如果只在 early window，也就是 step 0 到 10，做 common-logit cancellation，slot_NMI 提高到 0.896，max_load 降到 0.434，accuracy 仍然是 1.0。

如果从 step 0 到 final 都做 cancellation，slot_NMI 是 0.963，max_load 是 0.309，accuracy 仍然是 1.0。

这说明 common-logit 不只是一个 diagnostic pattern。至少在这个 controlled dot-product setting 里，它对 random-init collapse 有 intervention-relevant causal role。

---

## 5. Current Interpretation

现在我的理解是：feature 信息其实在 hidden state 里，但 router 的早期打分坐标系被 common 方向劫持了。

具体说，`w_e^T c` 会给不同 expert 产生不同的 effective bias。random initialization 下，某个 expert 对 common component 的 score 更高，于是 early top-1 routing 会把多个 slot 分到这个 expert。由于 sparse top-1 训练只更新被选中的 expert 和相应 routing path，这个早期优势会被稳定下来，最后形成 collapse。

slot-init 和 common-cancel 的作用，是把模型从 common-collapse basin 推向 slot-specialization basin。

---

## 6. Basin and Source

slot-init 的成功也不是很神秘。插值实验显示，从 random init 往 slot-aligned init 移动时，final NMI 会从 collapse 逐渐进入 specialization。alpha=0 时 NMI 是 0.080；alpha=0.2 是第一个超过 0.90 的测试点，NMI 是 0.930。

source audit 方面，B_CONST 和 B-position representation 是 leading source candidate。route_at_slot 和 varied-B 都能降低 common margin。但 varied-B 没有恢复 slot_NMI，所以 common source 还没有完全识别。

---

## 7. Boundaries

这里的边界是：这个结论只覆盖 minimal synthetic no-position moving-block task，dot-product sparse top-1 router，以及固定 B_CONST 的主 setting。

我们还不能 claim common source 已经完全识别，也不能 claim common-cancellation 是一个可部署方法，更不能 claim 结果直接推广到真实 LM 或者专家计算已经因果 slot-specialized。

---

## 8. Next Decision

下一步我认为应该从机制诊断转到一个最小 label-free intervention：设计一个 anti-common / anti-lockin 的 dot-product sparse top-1 router，在不使用 slot label 或 slot-centroid initialization 的情况下，控制 early common-logit bias，看 random-init training 是否能进入高 slot_NMI 的 specialization basin。

成功标准应该是：slot_NMI 显著提高，accuracy 保持接近 1.0，max_load 作为 secondary metric 下降。失败标准是：只改善 load balance 但 slot_NMI 不提高，或者 accuracy 掉下去。
