# Experiment Card: E2-H H-MoE Hierarchical Routing Side Branch

## 1. Purpose / Main Reason

本支线检验一个更强的 MoE 直觉：如果数据本身有两层结构，层级 MoE 是否会自然把高层结构交给 root router，把低层结构交给 leaf/path experts，并且比 Flat-MoE 更稳定地读回人工结构。

## 2. Mainline Position

E1-E2.2 已经说明：普通 Flat-MoE 可以读回 synthetic feature，但不会稳定形成 one-feature-one-expert 分工。本支线不并入主线，只作为 H-MoE 架构假设的独立测试。

## 3. Known Narrative / Premise

已知前提：

- synthetic NTP 可以构造可控人工序列特征；
- dense Transformer 能读回这些特征；
- Flat-MoE 的 router 不一定按人工 feature identity 切分 expert。

因此更精确的问题是：显式给 router 分层结构之后，是否会更容易出现“高层事件 / 低层短语”的路由分工。

## 4. Experiment Purpose

从数据构建开始，完整检查：

1. 数据是否真的有 L1 phrase 与 L2 event 两层结构；
2. dense NTP 是否能读回 L1/L2；
3. Flat-MoE 与 H-MoE 是否都能读回；
4. H-MoE 的 root / path routing 是否比 Flat-MoE 更贴近 planted hierarchy。

## 5. Hypothesis And Sub-Hypotheses

核心假设 H-HMoE：

```text
在含有复用短语和组合事件的 synthetic corpus 中，H-MoE 会比 Flat-MoE 更稳定地形成层级路由：root 对齐 L2 event family，leaf/path 对齐 L1 phrase 或 role。
```

细化假设：

- H1: dense 模型能读回 L1 phrase 和 L2 event，说明任务本身可学。
- H2: H-MoE 的 L1/L2 readback 不低于 Flat-MoE，说明分层架构没有牺牲基本预测能力。
- H3: H-MoE root 与 L2 family 的对应关系应强于 Flat expert 与 L2 family 的对应关系。
- H4: H-MoE leaf/path 与 L1 phrase 或 role 的对应关系应稳定出现。

竞争解释 H0：

```text
H-MoE 和 Flat-MoE 都只是学会 next-token readback；router 不会因为数据有层级结构就自然形成稳定层级分工。
```

## 6. Experiment Object

数据对象是两层 synthetic sequence：

- L1: 2-token phrase，例如 `E1=[1,2]`, `A1=[17,18]`, `O1=[25,26]`。
- L2: event = entity phrase + action phrase + object phrase，例如 `F1_E1_A1_O1=[1,2,17,18,25,26]`。

模型对象：

- dense Transformer；
- Flat-MoE，8 experts；
- H-MoE，4 root groups，每组 2 leaf experts，总共 8 leaf experts。

## 7. Experiment Paradigm

所有模型都训练 next-token prediction。评估不只看 loss，而是看：

- L1 readback：给 phrase 第一个 token，预测第二个 token；
- L2 readback：给 entity+action prefix，预测正确 object 起始 token；
- routing alignment：expert/root/path 与人工 L1/L2 标签是否对应。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 H-MoE readback 接近 dense/Flat，且 root 明显对齐 L2 family、path 明显对齐 L1 phrase，则支持 H-MoE 能自然暴露层级结构。

如果三类模型都能 readback，但 H-MoE routing 不比 Flat 更稳定，则说明当前 objective 下“可学层级结构”不等于“自然层级专家分工”。

如果 dense 都不能 readback，则说明数据或任务构造失败，不能解释 MoE。

## 9. What This Can Prove

它可以检验 controlled synthetic hierarchy 下，H-MoE 是否比 Flat-MoE 更容易形成与人工层级标签一致的路由结构。

## 10. What This Cannot Prove

它不能证明真实 LLM 的专家有自然语义层级，也不能证明 H-MoE 在真实语言任务中优于 Flat-MoE。

## 11. Result

见 `summary.md`。

## 12. Conclusion

见 `summary.md`。

## 13. Next Step

见 `summary.md`。

