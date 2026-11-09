---
experiment_id: A14_02_E04_shared_jacobian_path_image
status: completed_supported
verdict: supported_registered_local_h9
canonical_source: summary.md
---

# 结论：E04 共享 Jacobian / 路径像

## 直接结果

**注册的局部 H9 在 5/5 个有效种子上得到支持。** 对只用 calibration
样本估计的八维任务梯度参数空间 \(G_m\)：

- held-out ROOT Jacobian 的八维外谱尾均值为 \(0.0393\)，bootstrap 95%
  区间为 \([0.0259,0.0500]\)；
- calibration 子空间对 test Jacobian 能量的捕获均值为 \(0.9607\)，
  95% 区间为 \([0.9500,0.9741]\)。

因此，在训练完成点附近，同一个已学任务映射面对不同 nuisance contexts 时，
确实复用了少量 ROOT 方向：

\[
J_\rho(x;\theta_T)G_m
\approx
B_mA_x,
\qquad
\dim\operatorname{Col}(B_m)\le8.
\]

![held-out Jacobian 谱尾与跨 context 迁移](figures/jacobian_tail_and_transfer.png)

## 最重要的对照

| 探针 | 八维外谱尾 | cal 到 test 捕获 | 含义 |
| --- | ---: | ---: | --- |
| 训练后任务 \(G_m\) | 0.0393 | 0.9607 | 局部 H9 通过 |
| 同维随机 \(G\) | 0.2206 | 0.7794 | 不是任意参数方向都会共享 |
| 初始化点任务 \(G_m\) | 0.1421 | 0.8577 | 训练显著强化了共享像 |

输出头可见部分只占 Jacobian 能量的 \(0.3617\)，但输出头零空间部分同样低尾，
所以结果不只是答案类别瓶颈。

## 不能越界

把完整 final ROOT 强行投影到这个局部像后，CE 平均增加 \(0.6367\) nat。这不
否定 H9，因为 H9 只描述选定参数方向的无穷小 ROOT 作用，并不包含 base ROOT、
其他参数块或整个训练过程的有限位移。

**认识更新：**“不同 contexts 共享局部方向”已经得到直接支持；“这组局部方向
就是完整训练所使用的有限功能路径”仍需单独验证。

