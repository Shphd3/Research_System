# A06_03_04_E03 Tail-Safe Utility Certificate：实验协议

**唯一问题：** lower-tail pairwise expert utility 能否消除均值证书的 premature
stop，同时保留计算节省？

完全复用 A06_03_04_E02：rank-4 specialists、冻结表示和专家、Router-only SGD `0.001`、
full-LM、最多 600 步 continuous audition、总 800 步、32 seeds、四任务。只改变
逐 token utility 的聚合函数：

\[
D_{e,c}(h)=\ell(E_c(h))-\ell(E_e(h)).
\]

条件包括 fixed600、oracle route、mean reproduction、q25、q10、lower-CVaR10、
task-position q10 oracle，以及 generalist q10/CVaR guards。每个有向 pair 的统计量
使用 decay `0.9` EMA；12 个 pair 全部为正连续 9 个稳定步骤才停止。

非 oracle tail rule 通过要求：纠正和保持至少 `90%`、premature stop 不超过
`5%`、中位 audition saving 至少 `30%`、generalist trigger 低于 `10%`。

每步记录所有有向 pair 的 mean/q25/q10/CVaR10 最小值，并保存 stop 邻域的 pair
统计和 token count。只有 tail statistic 在 mean 已转正而 unsafe tail 尚未消失时
仍保持非正，才能支持尾部机制。

边界：通过不能证明 joint training、预训练 LLM、many-expert 可扩展统计或系统吞吐。
