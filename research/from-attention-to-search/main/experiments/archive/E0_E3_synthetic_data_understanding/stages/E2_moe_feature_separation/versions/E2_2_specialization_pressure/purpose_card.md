# Experiment Card: E2.2 Specialization Pressure Test

## 1. Purpose / Main Reason

E2.2 的目的，是在不修改 router objective 的前提下，检验 MoE 没有形成 clean one-feature-one-expert 的原因。

E2/E2.1 已经显示：feature identity 在 router input 中仍可分，但 router boundary 没有强按 feature-difference direction 切分；多个 expert 也能支持同一 feature prediction。因此 E2.2 要问：如果增加分工压力，MoE 会不会被迫更 feature-aligned？

## 2. Mainline Position

E2.2 位于：

```text
E2 MoE feature alignment
-> E2.1 router input geometry
-> E2.2 specialization pressure
```

它决定下一步应该继续追求 one-feature-one-expert，还是转向理解 shared path / expert sharing。

## 3. Known Narrative / Premise

已知前提：

- E2 证明 MoE 有 feature-expert alignment，但不是严格一一对应；
- E2.1 证明 router input 没有 representation collapse；
- 当前 router 不强按 PCA / feature-difference direction 切；
- 不改 router objective 时，分工只能来自数据、容量、任务 loss 和训练动力学。

## 4. Experiment Purpose

E2.2 要回答：

```text
如果降低 expert 容量或增加 feature 数量，MoE 是否会出现更强 feature-aligned specialization？
```

## 5. Hypothesis And Sub-Hypotheses

H2.2a：如果 expert capacity 是主要原因，降低 `ffn_dim` 会提高 feature-expert alignment。

H2.2b：如果 feature 数量压力是主要原因，增加 feature count 会提高 routing specialization。

H2.2c：如果共享路径足够强，压力不会带来更干净 routing；模型可能继续通过 attention/residual/LM head 或共享 expert capacity 完成 readback。

## 6. Experiment Object

三组条件：

| Condition | Feature count | ffn_dim | Source |
|---|---:|---:|---|
| baseline | 4 | 128 | E2 completed run |
| bottleneck | 4 | 16 | new run |
| pressure | 16 | 16 | new run |

所有条件使用 top-1 MoE、NTP、no-LB / LB 对照，不修改 router objective。

## 7. Experiment Paradigm

比较：

- NMI / ARI；
- readback probability；
- dominant expert ablation drop；
- routing entropy；
- dominant expert fraction；
- expert load imbalance。

## 8. Expected Outcomes And Hypothesis Update Logic

如果压力提高 NMI/ARI 和 ablation drop，说明 specialization 需要容量或任务压力。

如果 readback 仍高但 ablation drop 下降，说明模型学会任务但没有依赖 expert path，shared path 可能吸收了 feature prediction。

如果 feature count 增加后 routing 仍不更 feature-aligned，说明 one-feature-one-expert 不是当前 NTP objective 的自然解。

## 9. What This Can Prove

E2.2 可以判断降低 expert 容量和增加 feature 数量是否会推动 controlled synthetic MoE 更 feature-aligned。

## 10. What This Cannot Prove

它不能证明真实 LLM expert 的语义分工，也不能说明所有 MoE 都无法 specialization。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
