# Experiment Card: E2-D Router Supervision Diagnostic

## 1. Purpose / Main Reason

本实验是 E2 的诊断实验。我们已经看到自然 NTP 训练下，MoE 可以读回人工 feature，但不一定形成干净的 one-feature-one-expert 分工。现在直接给 router 人工 feature label，检查模型、expert、router 评估链路是否具备形成 clean specialization 的能力。

## 2. Mainline Position

它接在 E2 / E2.1 / E2.2 / E2-S 之后。此前问题是：hidden representation 中有 feature 信息，但 router 没有自然按 feature identity 切分。E2-D 不研究真实语言可用性，只做 synthetic diagnostic。

## 3. Known Narrative / Premise

已知前提：

- synthetic all-trigram 数据中有真实 feature label：ABC/DEF/GHI/JKL；
- 均匀频率版本中四个 feature 都能稳定 readback；
- 自然 MoE router 的 feature alignment 不等于 clean specialization；
- 如果明确监督 router 仍不能 clean specialization，则需要优先怀疑实现、label 对齐、训练目标或评估位置。

## 4. Experiment Purpose

判断：当 router 获得真实 feature supervision 时，当前 tiny MoE 是否能把 ABC/DEF/GHI/JKL 固定路由到 expert 0/1/2/3，并保持 NTP readback。

## 5. Hypothesis And Sub-Hypotheses

H-D: 给 router 明确 feature label 后，当前 MoE 可以形成 clean feature-expert specialization。

H-D1: router feature CE 会快速下降，fixed-label router accuracy 会接近 1。

H-D2: routing matrix 会接近固定对角：ABC->E0、DEF->E1、GHI->E2、JKL->E3。

H-D3: clean routing 不应破坏 feature readback。

H-D4: 若 dominant expert ablation 造成明显 target probability drop，说明被监督选择的 expert 不只是“被选中”，而是对该 feature prediction 有实际贡献。

## 6. Experiment Object

数据对象：均匀频率 all-trigram synthetic corpus。

模型对象：1-layer causal Transformer + 4-expert top-1 MoE FFN。

监督对象：feature prefix-end 位置的 router logits。

## 7. Experiment Paradigm

训练目标为：

$$
L = L_{\text{NTP}} + \lambda L_{\text{router-feature}}
$$

其中 router auxiliary loss 只作用在真实 feature prefix-end 位置：

$$
L_{\text{router-feature}} =
\frac{1}{|\mathcal{B}_{feat}|}
\sum_{(t,y_f)\in \mathcal{B}_{feat}}
\mathrm{CE}(W_r h_t+b_r,\ y_f)
$$

背景 token 不参与 router supervision。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 `router_aux_lam_1_0` 或 `router_aux_lam_5_0` 达到 fixed-label accuracy 接近 1、NMI 接近 1、routing matrix 接近固定对角，并保持 readback，则说明代码链路正常；自然 E2 不 clean 更可能是 objective / pressure 不足。

如果 router accuracy 高但 ablation 弱，说明 router 可以按 label 分，但 expert competence 未必随之专门化。

如果强监督仍不能形成固定对角，则优先检查实现：位置对齐、feature_id mapping、aux loss 梯度、evaluation routing position。

## 9. What This Can Prove

它可以证明在 controlled synthetic setting 中，当前 MoE/router 实现是否具备被 feature supervision 驱动成 clean specialization 的能力。

## 10. What This Cannot Prove

它不能证明真实语言数据中有可用 feature label；不能证明真实 MoE expert 会自然学习语义分工；也不能说明这种监督策略适用于真实 LLM。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
