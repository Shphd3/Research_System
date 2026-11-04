派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/dataset_guide.md)；研究修改仍回到原件。

---

# R01 task: can learned operations be used in composition?

Task semantics are specified operations. The32 Chinese symbols are object names; their ordinary linguistic associations do not define the labels. Each of four F and four G operations is a fixed permutation of32 symbols. A label such as F2 always names the same table.

An atomic prompt requests one operation: “操作 F2。输入：红。答案：”. A composition requests F2 followed by G3. The external target is y=G3(F2(x)). This defines how the answer should change after an operation edit; it does not assume that the network internally performs two table lookups.

## Knowledge and held-out mappings

Atomic training covers all32 inputs of all eight operations:256 rows. Another256 rows change only the wording, for example “输入符号是红。执行操作F2，输出符号：”. They test access across prompt formats, not previously unseen atomic knowledge.

Each of16 operation pairs has fixed20 TRAIN,6 VAL and6 TEST inputs, totaling320/96/96. Inputs are disjoint within each pair. Symbols and operation pairs are seen; TEST holds out pair-input mappings, not entire pairs. VAL supports prespecified selection; TEST is evaluated after the selection is locked.

## Controlled rarity

Every composition trajectory receives46,080 answer targets:1440 updates of32. Balanced exposure gives each pair2880 targets. Skew gives eight pairs5120 each and the other eight640 each, an8:1 ratio. Swap reverses the exposure identity of each pair.

Across distributions, every F and G receives11,520 targets; every input symbol and answer symbol receives1440. Model-independent integer constraints balance the split before model measurements. These marginals remain fixed while the exposure sequence and optimization trajectory change. This is controlled training exposure, not reference-corpus frequency.

A reporting-time data audit found unmatched F–input and G–intermediate joint exposure. Skew versus swap changes74/128 F–input cells and84/128 G–intermediate cells, by up to448 targets per cell. The contrast controls the registered marginals while also changing which component-map entries receive practice; it does not hold all component-computation exposure fixed. This audit narrows interpretation without changing data or criteria.

## What the controls test

P learns the relevant eight tables. C learns different permutations with the same format, answer vocabulary and supervision budget. B is the same untrained Base. A P advantage over both B and C can distinguish relevant-operation preparation from generic training, but cannot by itself establish internal reuse. C may also suffer negative transfer.

U updates the selected original parameters. F freezes the parent and trains an added adapter. J uses the identical adapter while also updating the same original range. Thus F/J compare freezing within the same added structure. A prespecified balanced rank128 capacity check follows rank32 training failure; the primary conditions remain visible.

In result tables a standalone F means Freeze strategy; numbered F0–F3 name first-step task operations. J means Joint updating and U means original-parameter Update.

A positive control feeds the first atomic prediction into a second independent atomic call. It tests whether an explicit external interface can compose the learned maps. Extra calls and intermediate information prevent treating it as a fair single-forward baseline.

## Connection to the hypothesis

Learning help concerns matched-supervision learning curves and held-out predictions. Actual use additionally requires predicted composition changes after changing only an atomic operation, or after replacing a candidate intermediate-symbol carrier from the original atomic parent. The recipient must apply its own second operation to the substituted intermediate. General damage and donor-answer copying do not meet this criterion.

Acquisition, composition and retention guards precede mechanism adjudication. All failed conditions remain reported. Execution completion, task validity, competence and mechanism support are separate facts.

## Provenance and boundary

Frozen dataset SHA256: `a394a65379adeea6f9498ee6ae8768681405d3e88575e2a2c09f820241c1614f`. Data seed20261024; training seeds29/43/71 share this single operation world. Three trajectories are not three independently sampled task worlds.

Full tables and row assignments remain execution-side in `data/dataset.json`, `data/manifest.json` and `data/data_audit.json`. See the [Protocol](protocol.md), [Summary](summary.md) and [Detailed record](detailed.md). External semantics do not establish internal modules, natural-language benefits or an MoE architecture ranking.
