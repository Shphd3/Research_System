# Purpose Card: E4.1 Raw-Attention Shortcut-Controlled Oracle-MoE

## 1. 总目的

E4.1 要回答：如果 E4 中某些 router 设计看起来形成了 one-feature-one-expert，这种分配到底是按完整上下文关系在分，还是只是在利用 token / target shortcut。

## 2. 主线位置

E4 已经把模型切到标准 Oracle-MoE 设置：

```text
gate_input = attention_output
expert_input = original hidden / residual
```

E4.1 接在 E4 之后，是对 E4 结论的必要控制实验。没有 E4.1，不能把 unique-uniform 上的 expert assignment 解释成 relation-level feature routing。

## 3. 已知前提

在 `unique_uniform` 中，人工 feature、prefix-end token、target token 和 attention source token 基本绑定：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

因此，如果 router 把 ABC/DEF/GHI/JKL 分给不同 expert，它可能是在按完整 feature 分，也可能只是在按 `2/4/7/9` 或 `22/23/20/21` 这些表面 token 分。

## 4. 实验目的

构造三个 shortcut-control 数据集，打破 feature 与单个 token 因素之间的一一对应，检验 C0-C7 router 是否仍然形成稳定、可用的 feature-aligned functional specialization。

## 5. 假设与子假设

核心假设：

```text
H4.1: 如果某个 router design 真正在用上下文关系分 expert，
那么在 shared prefix-end、shared target、crossed-factorial 控制数据上，
它仍应保持 feature assignment、boundary alignment、expert utility、readback 四者一致。
```

子假设：

- H4.1a: 若 shared prefix-end 后 routing alignment 明显下降，说明 E4 的分配依赖 prefix-end token shortcut。
- H4.1b: 若 shared target 后同 target features 被分到相似 experts，说明 router 依赖 target token shortcut。
- H4.1c: 若 crossed-factorial 后仍能 one-feature-one-expert，并且 forced-routing utility diagonal，才支持 relation-level routing。
- H4.1d: 若 C7 oracle-init 只在 unique-uniform 成功，在 crossed-factorial 失败，说明 oracle center 初始化学到的是当前数据几何，不是一般关系抽象。

## 6. 实验对象

沿用 E4 的 C0-C7 router variants：

```text
C0 standard linear
C1 fixed parameter-center
C2 trainable center + repulsion
C3 inhibition
C4 center + inhibition
C5 clean linear inhibition
C6 clean center inhibition
C7a-e Dingyi-style oracle-init family
```

所有 variants 使用 raw `attention_output` 做 router 输入。

## 7. 实验范式

在三个控制数据上重新 full run：

| dataset | 构造目的 |
|---|---|
| `shared_b_uniform` | 共享 prefix-end token，破坏 “末尾 token = feature” 的捷径 |
| `shared_target_uniform` | 共享 target token，破坏 “target = feature” 的捷径 |
| `crossed_factorial_uniform` | 交叉 first token / prefix-end token / target，检验完整关系分配 |

每个训练完成后做 D0-D7 router behavior diagnostic 和 D* boundary direction audit。

## 8. 预期结果与假设更新

- 若 C7 在三个控制数据上仍保持高 readback、高 feature-expert alignment、utility diagonal：增强 “oracle-init 可以诱导功能性 feature specialization” 的结论。
- 若 C7 在 `unique_uniform` 成功但在 shared / crossed 控制上失败：说明 unique 结果主要由 shortcut geometry 支撑。
- 若 C5/C6 只提升 selected-best rate，但不提升 feature boundary：说明 inhibition 提供功能排他性，但不是 relation-level routing。
- 若所有 variants 在 crossed-factorial 上 readback 成功但 routing 不 clean：说明 NTP 任务仍可由非 one-feature-one-expert 路径完成。

## 9. 能证明什么

E4.1 能判断 E4 的 routing 结果是否经得起 shortcut-control，特别是能否区分 token-level shortcut 与 context-relation-level routing。

## 10. 不能证明什么

即使 E4.1 成功，也不能证明真实语言语义 routing；它只支持 controlled synthetic trigram setting 下的机制结论。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
