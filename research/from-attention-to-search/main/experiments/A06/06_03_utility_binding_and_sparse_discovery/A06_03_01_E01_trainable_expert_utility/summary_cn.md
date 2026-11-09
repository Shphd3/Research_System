# A06_03_01_E01 实验总结：上下文任务上的可训练专家功能绑定

## 结果摘要

**结论：** 正确的路由条件暴露能够在受控上下文 next-token 任务上形成可泛化的任务特定 expert function；这个结果不需要表征漂移，并且在表征共同训练时仍成立。但反事实功能差越大，不代表 weighted top-1 router 收到的同方向 raw gradient 越强。

主结果来自 32 seeds、128 个 task-seed 单元：

- 正确 expert-only 暴露：128/128 的 \(G_f^{cf}>0\)；中位 gap 为 8.895。
- 打乱 expert-only 暴露：中位 gap 为 -0.004，专家基本可互换。
- 正确减打乱的配对中位差为 8.892 nats/task-token，95% CI 为 \([8.694,9.142]\)。
- 相对功能绑定从第 10 步开始持续为正。
- 两个条件的 native route NMI 都是 1.0，因此 route purity 本身不能证明 expert utility。

## 数据与方法

序列开头给出四种等频 instruction 之一；instruction \(f\) 决定后续 content \(c\) 应预测 output \((c+f)\bmod4\)。每条序列包含 16 组 content/output pairs，共 33 tokens，全部 32 个 next-token positions 进入 LM loss。

主比较冻结 representation 和 router，只训练四个相同初始化的 MLP experts：

- 正确暴露：task \(f\) 始终进入 expert \(f\)；
- 平衡打乱：task-expert mapping 循环变化，使每个 expert 从每个 task 获得完全相同的更新次数。

测试集使用不同 content 顺序。评估时固定所有非 expert 组件，逐个强制 expert，计算：

\[
G_f^{cf}
=
\min_{b\ne f}
\left[L_{f,b}^{cf}-L_{f,f}^{cf}\right].
\]

## 核心证据

![功能差轨迹](figures/utility_gap_trajectory.png)

正确 expert-only 和 correct joint 均从第 10 步开始持续脱离打乱控制；说明稳定的 task-expert identity，而不是 load/count，制造了 expert function。

![反事实 expert loss matrix](figures/counterfactual_loss_matrices.png)

正确暴露得到约 0.002 的对角 loss 和 9.4--9.8 的非对角 loss，形成 specialists；打乱暴露的所有 experts 都在 0.082--0.087 左右，形成近似 generalists。

![utility 与 router pressure](figures/utility_router_pressure.png)

正确 specialist 的 task-gradient pressure 中位数为 121.94，打乱 generalist 为 146.99。配对差为 -23.44，95% CI 为 \([-26.82,-20.98]\)；正确条件仅在 1/128 单元更大。因此 H3 被证伪。

机制原因是两种指标测量不同对象。\(G_f^{cf}\) 比较不同 experts 的完整反事实功能；weighted top-1 update 只使用当前 selected expert 的 benefit：

\[
\Delta w_j
=
\frac{\eta}{\tau}
p_r(\mathbf 1[j=r]-p_j)B_rh.
\]

它没有直接比较未选 experts 的自身功能。更大的 residual loss 可以产生更大的 raw pressure，因此 pressure magnitude 不能直接作为 specialization utility 的 proxy。

## 假设更新

| 假设 | 裁定 |
| --- | --- |
| 正确暴露形成测试集功能绑定 | 支持 |
| 功能绑定必须依赖 representation drift | 证伪；冻结表征时仍成立 |
| 更大 utility gap 会产生更强 router pressure | 证伪 |
| route purity 足以证明 specialization | 证伪；两边 NMI 都是 1 |

## 边界与下一步

当前只证明受控 context-defined task 中的 expert utility formation，不能推广到自然语言语义、无标签 discovery、真实 downstream benefit 或 sparse-compute efficiency。

下一 anchor 应采用两阶段 handoff：分别从 specialist 与 generalist experts 出发，保持相同正确 router，然后释放 router，检验 route identity、counterfactual utility 和 native task loss 是否共同稳定。raw pressure magnitude 不再作为主 utility 指标。
