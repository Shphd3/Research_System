# researcher judgment record Handwrite Draft

This is rough user thinking for AI audit. It is not a final anchor, protocol,
or experiment plan. Fill only the researcher judgment record. Do not hand-write the full
0-8 anchor here.

## User Control

**Preserve:**

**Do not silently change:**

**Unclear / risky:**

**Candidate priors:**

## 0. researcher judgment record

**Phenomenon:**

在合成数据实验中，使用all hidden states的数据进行无监督聚类，我们在多数seeds找到了features的中心，但是少数还是因为背景hidden states发生了混淆。因此需要构建更好的方法，来找到features所在（目前想到了SAE，不知道是否还有没有其他的工具能够确定中心的），并且构造出proxy vector用来初始化gating row vectors. 进而，更可能达到初始化的时候分开，早期训练也能跳出collapse basin的目的。

**Mechanism guess:**

1. 虽然features高频出现，但是背景hidden states均匀分布，导致距离聚类混淆
可证伪：通过聚类指标看减去均值的hidden states是否形成明显的簇，背景hidden states分到哪

2. 两类features之间的中心距离过近，从而导致两类features混淆。
可证伪：每个features都分得很远，聚类不在同一类

3. 由于common分量导致即使分到不同簇，还是会优化到一起。
可证伪：没有common分量，能够保持聚类甚至可以分出features聚类

**Key variables:**

最少需要哪些变量？
1. 是否减去common分量
2. SAE的

**Causal relation:**

暂不理解

**Observable metric:**

哪个数能看到这个关系？

**Alternative explanation:**

还有什么 rival explanation？

**Decision:**

看到什么结果后，我会 pursue / revise / park？
