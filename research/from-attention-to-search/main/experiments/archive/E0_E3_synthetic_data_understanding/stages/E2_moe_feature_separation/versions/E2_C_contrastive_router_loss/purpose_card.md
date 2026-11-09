# Experiment Card: E2-C Contrastive Router Loss

## 1. Purpose / Main Reason

E2-C 测试一种比 feature-id CE 更弱的监督：不指定哪个 feature 必须进哪个 expert，只让同 feature 的 router representation 更近、不同 feature 更远。

## 2. Mainline Position

它接在 E2-D 后，是 router representation pressure 的诊断支线。它更接近未来从 synthetic 过渡到 weak labels / cluster labels 的设置。

## 3. Known Narrative / Premise

E2-D 说明固定 feature-id CE 可以让 MoE clean specialization。但真实数据中通常没有固定 feature-to-expert label。因此需要测试：只给“同类靠近、异类远离”的 contrastive pressure，是否足以诱导 expert routing clean。

## 4. Experiment Purpose

判断 supervised contrastive loss 是否能让 router representation 形成 feature cluster，并进一步让 top-1 expert choice 形成 one-to-one routing。

## 5. Hypothesis And Sub-Hypotheses

H-C: Contrastive router representation 能形成 feature clusters，并推动 expert routing 更接近 one-to-one。

H-C1: router representation probe / PCA 会显示 feature cluster。

H-C2: 若 cluster-to-expert 边界随之清晰，则 NMI 和 best permutation accuracy 会接近 1。

H-C3: 若 representation cluster 清楚但 routing 仍混合，说明问题在 cluster-to-expert boundary，而不是 representation。

H-C4: LB 可能帮助把 clusters 分配给不同 experts，也可能干扰 feature purity。

## 6. Experiment Object

均匀 all-trigram synthetic data；1-layer Transformer + 4-expert top-1 MoE；projection router representation。

## 7. Experiment Paradigm

Router representation:

$$
r_t = \mathrm{normalize}(W_p h_t)
$$

Router logits:

$$
s_t = W_r r_t + b_r
$$

Auxiliary objective:

$$
L = L_{\text{NTP}} + \alpha L_{\text{LB}} + \lambda L_{\text{supcon}}
$$

## 8. Expected Outcomes And Hypothesis Update Logic

如果 contrastive aux 同时提高 representation cluster 与 routing NMI，则支持 representation clustering pressure 可以改善 routing。

如果 representation cluster 成功但 routing 不 clean，则说明 router head / expert utility 没有把 cluster 转成 expert assignment。

如果 LB 版本更 clean，说明 load pressure 有助于 cluster-to-expert 分配。

## 9. What This Can Prove

它可以检验 weak grouping-style supervision 是否足以改善 synthetic feature routing。

## 10. What This Cannot Prove

它不能证明真实语言 feature clusters 已知；也不能证明 contrastive router 会自然发现语义。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
