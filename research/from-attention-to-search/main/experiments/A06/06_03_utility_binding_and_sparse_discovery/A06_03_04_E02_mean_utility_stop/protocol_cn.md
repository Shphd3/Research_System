# A06_03_04_E02 Utility-Certified Audition Stop：实验协议

**唯一问题：** 能否利用 audition 已计算出的 incumbent/challenger 输出，在不知道
feature label 和 useful expert ID 时，判断何时安全切回 top-1？

固定复用 A06_03_04_E01 rank-4 specialists，冻结表示和专家，Router-only SGD `0.001`，
full-LM，总 horizon 800 步。最多连续 audition 到第 600 步；停止后全部使用 top-1。

对当前路由到 incumbent \(e\) 的位置，利用同一次 pair forward 比较 challenger \(c\)
和 incumbent 的强制路径 loss：

\[
U_{e,c}=\operatorname{EMA}[\ell(E_c(h))-\ell(E_e(h))].
\]

EMA decay 为 `0.9`。所有 12 个有向 expert pair 均被观测、最小 \(U_{e,c}>0\)
连续 9 步、且全位置 route assignment 连续 9 步变化不超过 1% 时停止。该规则读取
LM 训练已有 target/loss，不读取 task mask 或 feature label。

对照：固定 audition 600 步；真实 route correction 的 oracle stop；只看 score gap
大于 `1.0` 的 score-only stop；all-position utility stop；只看 task positions 的
oracle utility stop；generalist false-certificate guard。

主判据：utility-all 的纠正和保持至少 `90%`，premature stop 不超过 `5%`，中位
audition saving 至少 `30%`，generalist 触发低于 `10%`。若 all-position 失败而
task-position oracle 通过，说明停止证书还缺少语义位置信用。

边界：不能证明 joint training、预训练 LLM、可扩展 per-token state、MTP re-trigger
或系统吞吐。
