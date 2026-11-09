# Purpose Card: E4.2 Zipf Raw-Attention Oracle-MoE

## 1. 总目的

E4.2 要检验：当 synthetic features 呈 Zipf/long-tail 频率分布时，raw-attention Oracle-MoE 的 router 是否还能形成稳定、可用的 feature-to-expert 分配。

## 2. 主线位置

E4 / E4.1 主要检查均匀频率与 shortcut-control。E4.2 把同一套 C0-C7 router 机制放回长尾频率数据，判断 “one-feature-one-expert” 是否只在频率均匀时成立。

## 3. 已知前提

之前 E1/E2 已经显示：低频 feature 容易被背景和高频 feature 淹没。Zipf 数据更接近真实语言里高频/低频结构不均衡的情况，但仍是受控 synthetic trigram。

## 4. 实验目的

在同样的 Oracle-MoE 设置下：

```text
gate_input = raw attention_output
expert_input = original hidden / residual
```

比较 C0-C7 在长尾 feature 分布下的 readback、routing alignment、expert utility 与 boundary geometry。

## 5. 假设与子假设

核心假设：

```text
H4.2: 如果某个 router 机制真的能产生稳健 feature specialization，
它不应只在均匀频率下有效；在 Zipf 数据中也应至少稳定分出高频 feature，
并给低频 feature 留出可诊断的 expert utility 信号。
```

子假设：

- H4.2a: 普通 C0-C6 router 更可能被高频 feature 主导，低频 feature assignment 不稳定。
- H4.2b: C7 oracle-init 若依赖 center 初始化质量，应比自然 router 更能保留低频 feature。
- H4.2c: 若 C7 在 Zipf 下也只分高频、不分低频，说明 one-feature-one-expert 仍受频率和初始化样本量限制。
- H4.2d: 若 readback 高但 utility 不 diagonal，说明模型会做 NTP，但 experts 没有形成频率稳健的功能分化。

## 6. 实验对象

数据：

```text
ABC: [1,2] -> 22, count 10000
DEF: [3,4] -> 23, count 5000
GHI: [6,7] -> 20, count 500
JKL: [8,9] -> 21, count 100
```

模型与 variants 与 E4 保持一致：C0-C7 raw-attention Oracle-MoE。

## 7. 实验范式

训练 C0-C7 全部 variants，5 seeds，10000 steps。训练后做 D0-D7 behavior diagnostic 与 D* boundary audit。

## 8. 预期结果与假设更新

- 若 C7 能在 Zipf 下保持高 readback、高 NMI、utility diagonal：说明 oracle-init 对长尾 feature specialization 有独立价值。
- 若只高频 feature clean，低频 feature 混合：说明频率仍是 specialization pressure 的主导因素。
- 若所有 variants readback 成功但 routing 不 clean：支持 “NTP 不要求 one-feature-one-expert” 的主线判断。

## 9. 能证明什么

E4.2 能证明在受控长尾 synthetic feature 数据中，某个 router 机制是否对频率不均衡有鲁棒性。

## 10. 不能证明什么

它不能证明真实语言语义 routing，也不能证明低频真实语义一定可由 oracle-init 解决。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
