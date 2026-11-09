# Experiment Card: E2-B Prototype / Center Gating

## 1. Purpose / Main Reason

E2-D 已经证明：如果直接给 router feature-id CE，当前 MoE 可以形成 clean specialization。E2-B 进一步问：如果把 expert router 改成 prototype/center 形式，是否更自然地接近 feature clustering。

## 2. Mainline Position

本实验属于 E2 router 改造支线，不并入 spectral 或 H-MoE。它接在 E2-D 后，用来检查 router inductive bias，而不是检查代码是否能工作。

## 3. Known Narrative / Premise

普通 linear router 在自然 NTP 下没有稳定 one-feature-one-expert。显式 feature supervision 可以做到 clean specialization。因此下一步要测试：改变 router geometry 是否能减少对强 feature-id CE 的依赖。

## 4. Experiment Purpose

判断 cosine prototype gating 是否比 ordinary linear router 更容易形成 ABC/DEF/GHI/JKL 到 experts 的一对一分工。

## 5. Hypothesis And Sub-Hypotheses

H-B: Prototype / center gating 会更贴近聚类式 specialization，因此在相同 NTP setting 下比普通 linear router 更接近 one-to-one routing。

H-B1: 无 aux 的 prototype router 若优于普通 no-LB，说明 center inductive bias 有自然帮助。

H-B2: 加 prototype CE 后若固定对角成功，说明 prototype router 可被 feature signal 驱动成 clean specialization。

H-B3: 若 LB 降低 fixed-label accuracy 或 ablation drop，说明 LB 会干扰 feature-pure center assignment。

## 6. Experiment Object

均匀 all-trigram synthetic data；1-layer Transformer + 4-expert top-1 MoE；prototype router。

## 7. Experiment Paradigm

每个 expert 有可学习 center $c_e$，router 使用 cosine similarity：

$$
s_{t,e} = \tau \cdot \cos(h_t, c_e)
$$

top-1 expert 为：

$$
e_t = \arg\max_e s_{t,e}
$$

有 aux 的版本使用固定 feature-to-expert mapping。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 no-aux prototype 已明显强于 ordinary linear router，则支持 prototype gating 自身更适合 feature clustering。

如果只有 aux prototype 成功，则说明 center gating 可被监督成 clean specialization，但自然 NTP 仍不给足压力。

如果 aux prototype 也失败，则需要重新检查 prototype implementation 或 feature position。

## 9. What This Can Prove

它可以检验 center-style router 是否改善 controlled synthetic feature routing。

## 10. What This Cannot Prove

它不能证明真实语言语义天然是 prototype cluster；也不能证明真实 MoE 会自然形成语义专家。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
