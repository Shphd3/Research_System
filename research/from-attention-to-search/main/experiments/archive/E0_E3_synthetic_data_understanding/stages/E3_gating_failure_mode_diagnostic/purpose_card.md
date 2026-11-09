# Experiment Card: E3 Gating Failure Mode Diagnostic

## 1. Purpose / Main Reason

E3 的目的不是继续证明 MoE 是否能 one-feature-one-expert，而是解释一个已经稳定出现的现象：

```text
feature representation 在 hidden space 中可分，
但 natural top-1 router 没有自然按 ABC/DEF/GHI/JKL 干净分 expert。
```

## 2. Mainline Position

E2 系列已经形成当前主线判断：

```text
representation separability != router specialization
```

E2-D 进一步说明：如果给 router 明确的 feature label supervision，当前模型和代码链路可以形成 clean specialization。因此 E3 要诊断的是 natural NTP objective 下缺少什么压力，或者 router 实际按什么变量路由。

## 3. Known Narrative / Premise

已知前提：

- synthetic trigram data 可以被 dense / MoE 读回；
- feature identity 可以从 router input hidden state 中线性读出；
- router boundary 与 feature-difference direction 弱对齐；
- supervised router auxiliary loss 可以让 router 达到 clean feature specialization；
- 因此 failure 更可能来自 objective、shortcut、expert utility、shared path 或 training dynamics，而不是模型完全不能分。

## 4. Experiment Purpose

E3 要把 gating failure mode 拆开，回答：

```text
router choice 是由 feature_id、token shortcut、target token、difficulty/scale、
hidden geometry、expert utility、shared path，还是 early routing history 解释？
```

## 5. Hypothesis And Sub-Hypotheses

H3: Natural top-1 router 不 clean，不是因为 feature 不可分，而是因为 NTP loss 下 clean feature partition 不是必要解。

H3a: Router 可能使用 token / target shortcut，而不是完整 context relation。

H3b: Router 可能按 hidden norm、CE difficulty、target margin 或 confidence 分。

H3c: 多个 experts 都能完成同一 feature prediction，因此没有独占 expert 的压力。

H3d: Attention/residual/LM head/shared path 已经承担主要 prediction，MoE path 不是唯一必要路径。

H3e: 早期随机 routing 与 expert co-adaptation 可能锁定最终分工。

## 6. Experiment Object

对象是 4-feature uniform synthetic trigram NTP，模型是 1-layer causal Transformer + 4-expert top-1 MoE FFN。

核心数据包括：

- unique feature dataset；
- shared prefix-end token dataset；
- shared target dataset；
- crossed factorial dataset。

## 7. Experiment Paradigm

用同一模型和训练参数，在多个控制数据集上比较：

- natural no-LB router；
- LB router；
- supervised router upper bound。

再用 predictor decomposition、training dynamics trace、component ablation 和 forced-routing utility 来归因 failure mode。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 supervised router 在所有数据中 clean，而 natural router 不 clean，则支持 objective insufficiency。

如果 shared-target 中同 target features route 相似，则支持 target-token shortcut。

如果 predictor 中 difficulty/norm 强，则支持 confidence/scale routing。

如果多个 experts forced-routing utility 接近，则支持 expert utility degeneracy。

如果 zero MoE output 影响小而 attention/shared path ablation 影响大，则支持 shared-path bypass。

如果 early checkpoint route 与 final route 高一致，则支持 early routing lock-in。

## 9. What This Can Prove

E3 可以在 controlled synthetic setting 中诊断 natural top-1 router 不 clean 的主要 failure mode。

## 10. What This Cannot Prove

E3 不能证明真实语言中的 MoE expert 语义分工；不能说明真实 LLM 应该使用 supervised feature labels；也不能直接证明某种新 routing architecture 在真实任务上有效。

## 11. Result

Full run 已完成。Supervised router 在所有控制数据集上达到 clean specialization，`NMI = 1.000`、`ARI = 1.000`，且 readback probability 约 `0.996-0.997`。

Natural no-LB / LB router 也能完成 readback，但只形成 partial feature-expert alignment：NMI 约 `0.556-0.724`。Feature identity 可以从 hidden state 中线性读出，但 learned router choice 更像由 router projection / hidden geometry 解释，而不是由人工 feature label 直接解释。

## 12. Conclusion

E3 支持 H3：natural NTP objective 下，clean feature partition 不是必要解。主要 failure mode 是 objective insufficiency + expert utility degeneracy；不是模型容量不够，也不是代码链路无法 clean routing。

## 13. Next Step

下一步应测试 specialization pressure，而不是继续重复普通 MoE full run。重点是让 one-feature-one-expert 在 loss 或 utility 上变得更必要。
