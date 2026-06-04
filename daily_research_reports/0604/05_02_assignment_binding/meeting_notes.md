# Meeting Notes

## Meeting Diagnosis

导师的 Toy claim 是什么：

在 single-feature / uniform / top-1 routing / inhibition 的极简 setting 下，
随机初始化已经给每个 feature 一个 nearest expert。
top-1 会先把该 feature 送到 nearest expert；
inhibition 会把 competing experts 推远；
因此同一 feature 后续会更稳定地进入同一个 expert。
在这个弱定义下，可以形成 feature -> expert 的 route consistency。

我同意什么：

我同意这个 toy claim。
initial lock-in 不是反驳它的理由，反而是它成立的机制。
但这个 claim 只说明 same-feature route consistency，
不说明 non-collapse、feature grouping、或 utility-aligned specialization。

我的 stronger concern 是什么：

如果所有 feature 都进入同一个 expert，也满足“每个 feature 只进一个 expert”的弱定义。
所以我们需要额外区分：
1. 同一 feature 是否稳定；
2. 不同 feature 是否被区分；
3. expert 内多个 feature 是否有结构；
4. route assignment 是否绑定 expert utility。

三个未放松的假设：

1. feature 是否真的是 atomic single feature，还是 slot / B_i / slot+B_i 的组合。
2. feature 分布是否 uniform，还是存在 Zipfian / common feature dominance。
3. 多个 feature 进入同一个 expert 后，它们之间是 arbitrary bucket、slot grouping、B_i grouping，还是 utility-compatible grouping。

## Group Mainline

主线内容更新：

当前主线不是下游 retrieval，而是定义并诊断 feature-level expert specialization。
下一步先做 feature definition + router assignment diagnostic：
把 f=(slot, B_i) 当作 atomic feature，
检查同一 f 是否稳定进入同一个 expert，
同时检查是否出现 expert collapse。

next-to-do：

跑 same-feature routing consistency diagnostic：
- feature definitions: slot, B_i, slot+B_i
- metrics: mean max_e P(route=e|feature), route entropy/load entropy, NMI(route; slot), NMI(route; B_i), NMI(route; slot+B_i)
- interpretation: consistency high + load collapse ≠ specialization

## Personal Research Notes

主线内容更新：

我之前的问题不是 initial lock-in 是否存在；
而是 initial lock-in 产生的是 useful specialization 还是 arbitrary/collapsed assignment。
下次汇报先回答导师 toy question，再声明 stronger concern。

next-to-do：

明早根据今晚 diagnostic 结果，决定下一步：

1. 如果 exact feature 都不稳定：说明当前 router 连弱 toy consistency 都没有复现。
2. 如果 exact feature 稳定但 collapse：说明弱 consistency 成立，但不是 specialization。
3. 如果 exact feature 稳定且非 collapse：继续分析 expert 内 feature grouping 是按 slot、B_i，还是随机。
4. 如果 slot-level route NMI 高且 utility diagonal 也高：才接近 functional specialization。

other：

下次被追问时使用固定句式：
“我先回答老师这个 setting：yes/no。
这个答案依赖 A/B/C。
我原来想问的是放松其中一个假设之后的问题。”