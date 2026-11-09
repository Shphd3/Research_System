---
experiment_id: A14_02_E06_reference_jacobian_vs_secant
status: completed_decisive
verdict: h11_finite_displacement_linearization_refuted
canonical_source: summary.md
---

# 决定性结论：E06 参考点 Jacobian 与真实有限 secant

## 直接结果

**H11“单点 Jacobian 可以近似完整训练位移”在 5/5 个有效种子上被决定性
否定。** 与此同时，真实有限 secant 在 5/5 个种子上都通过八维跨 context
迁移和冻结读出功能守卫。

| 对象 | 均值 | 95% 区间 |
| --- | ---: | ---: |
| 参考点 Jacobian 八维外谱尾 | 0.1546 | [0.1123, 0.1892] |
| 参考点 cal 到 test 捕获 | 0.8454 | [0.8108, 0.8877] |
| 真实 secant 八维外谱尾 | 0.0171 | [0.0060, 0.0292] |
| 真实 secant cal 到 test 捕获 | 0.9829 | [0.9708, 0.9940] |
| 参考点像对 secant 的捕获 | 0.2935 | [0.2369, 0.3503] |
| 线性化相对误差 | 1.2595 | [0.9532, 1.5659] |
| 线性化重放 CE 增量 | 0.4797 nat | [0.1259, 0.8872] |
| secant 子空间重放 CE 增量 | 0.00022 nat | [0.00002, 0.00046] |

注册后又使用同一批已保存 checkpoints 做了一个完整位移竞争解释审计：不再把
block 位移投影到八维轨迹空间，而是直接计算完整 \(\Delta\theta\) 的参考点方向
导数。线性化相对误差均值仍为 \(1.2441\)，5/5 seeds 继续否定 H11；八维参数
投影模型在 5/5 seeds 保持功能，CE 平均只增加 \(0.00180\) nat。因此 H11 失败
不是由遗漏少量轨迹空间外参数导致。该审计复用了同一 test split，只用于排除
竞争解释，不计作新的独立确认，也不改变注册 verdict。

![参考点 Jacobian、真实 secant 与线性化误差](figures/reference_jacobian_vs_secant.png)

参考点 H9 本身处于中间区：1/5 达到严格支持门，0/5 达到否定门。因此我们不能
说参考点 Jacobian 完全没有跨 context 共享；可以确定的是，它不能跨越整个训练
位移。

## 最终认识更新

对

\[
\theta(t)=\theta_{\mathrm{ref}}+t\Delta\theta
\]

有精确恒等式

\[
h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}})
=
\int_0^1J_\rho(x;\theta(t))\Delta\theta\,dt.
\]

实验表明：局部方向会沿训练路径发生足够大的旋转，但积分后的真实功能效应仍然
集中在少量跨 context 共享方向中。因此应把理论拆为：

1. **局部版本：**H9-L 加小余项 H11，只适用于确实很小的更新；
2. **有限训练版本：**直接假设或测量 H9-F，即 secant／路径积分像低维。

这保留了“任务复用对应较少功能方向”的核心故事，同时删除了未经证据支持的
“一个 Jacobian 坐标系贯穿完整训练”。
