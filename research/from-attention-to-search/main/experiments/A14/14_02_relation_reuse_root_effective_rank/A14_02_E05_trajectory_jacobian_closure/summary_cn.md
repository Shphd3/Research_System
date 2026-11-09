---
experiment_id: A14_02_E05_trajectory_jacobian_closure
status: completed_refuted
verdict: eight_dimensional_trajectory_closure_refuted
canonical_source: summary.md
---

# 结论：E05 训练轨迹与 Jacobian 闭包

## 直接结果

**“实际八维参数轨迹会落入 endpoint Jacobian 的八维 ROOT 像”在 4/5 个
有效种子上被否定。** 但被否定的不是低维性本身：

- 实际 block 参数有限位移的八维捕获为 \(0.9975\)；
- 只保留这八维参数位移，CE 平均只变化 \(0.00026\) nat，accuracy 不变；
- 该 block 的精确 ROOT 有限效应八维外谱尾仅为 \(0.0132\)，跨 context 捕获
  为 \(0.9868\)；
- endpoint Jacobian 像却平均只捕获精确效应的 \(0.3672\)；
- 用 endpoint 像投影精确效应后，CE 平均增加 \(0.2212\) nat。

![参数轨迹、endpoint Jacobian 与功能闭包](figures/trajectory_closure.png)

## 认识更新

模型确实以少量参数方向学成，学到的有限 ROOT 变化也确实位于少量跨 context
共享方向中；但是这组有限效应方向不能由训练终点的单点 Jacobian 识别。

因此不能把

\[
J_\rho(x;\theta_T)\Delta\theta
\]

当作

\[
h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}})
\]

的可靠替代。下一步只需判断：问题来自参考点本身没有共享像，还是来自完整位移
超出局部线性化范围。

