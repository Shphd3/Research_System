# A06_03_01_E02 实验总结：specialist/generalist 路由释放

## 结论

训练得到的 specialists 在释放 router 后仍保持显著任务优势，但它们的
route margin 增长略小于负载匹配的 generalists。仅训练 router 的 SGD 在第
50 步得到：

\[
D_m(50)=-0.00324,
\qquad
95\%\ \mathrm{CI}=[-0.00413,-0.00245].
\]

同时，generalist 减 specialist 的任务损失差为 0.9125 nats/task-token，
95% 置信区间为 \([0.8905,0.9438]\)。

这说明“专家身份效用差”不会单调变成“已正确路由的置信度增长”，但不说明
路由坍塌。两个条件的 route NMI 始终为 1，margin 都在增长，而且 specialist
更快消除了相对自身 expert floor 的路由剩余误差。

## 术语解释

| 术语 | 具体含义 | 计算 | 当前作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| specialist | 只接受一个上下文任务训练的专家 | correct expert-only exposure | 有唯一功能身份 | 自然语言语义专家 |
| generalist | 四个任务更新次数完全相同的专家 | balanced shuffled exposure | 负载匹配控制 | 专家无用 |
| 反事实功能差 | assigned expert 相对最佳 competitor 的 loss 优势 | \(G_f^{cf}=\min_{b\ne f}(L_{f,b}^{cf}-L_{f,f}^{cf})\) | 测 expert 身份价值 | 应增加多少 margin |
| 路由间隔 | assigned expert 相对最近 competitor 的 score lead | \(m_f=s_f-\max_{b\ne f}s_b\) | 测当前路由置信度 | expert 是否有用 |
| 路由剩余误差 | native loss 高于 forced assigned-expert floor 的部分 | \(E_f=L_f^{native}-L_{f,f}^{cf}\) | 分离 routing 与 expert function | 系统吞吐收益 |

## 精确设置

- 四个等频序列级任务；开头 instruction \(f\) 决定后续目标
  \((c+f)\bmod4\)。
- 序列长 33，含 16 组 content/output；全部 32 个 next-token positions
  进入 LM loss。
- 一层 causal attention、一层 residual + LayerNorm、四个 MLP experts、
  weighted top-1 router；无 learned positional embedding。
- 先进行 200 步 expert-only exposure，得到 specialists 或 balanced
  generalists；再从完全相同的 router 和 representation 状态释放 50 步。
- 主条件：router-only SGD，learning rate \(10^{-4}\)。
- 迁移条件：router-only AdamW 与 joint AdamW；release optimizer 均从空状态开始。
- 正式证据：32 seeds、128 个 task-seed 配对单元、远程 4 卡完整运行。

## 核心结果

| 第 50 步指标 | Specialist | Generalist | 配对结论 |
| --- | ---: | ---: | ---: |
| 初始反事实功能差 | 8.8947 | -0.0042 | specialist 有唯一功能 |
| SGD margin growth | 0.10031 | 0.10337 | \(D_m=-0.00324\) |
| SGD native task loss | 0.6441 | 1.5576 | specialist 低 0.9125 |
| SGD normalized routing excess | 0.7612 | 0.8513 | specialist 比例下降更快 |
| 最低 route NMI | 1.0000 | 1.0000 | 路由身份未破坏 |

预注册的操作化 H3 得到支持：specialist 的任务价值保持，但 margin growth
更小。机制解释必须收紧：当前 useful expert 从一开始就是 top-1，margin 更新
只改变已选 expert 的 probability；反事实功能差比较的是“换成另一个 expert”
会怎样。两者不是同一个干预，所以不应期待单调关系。

## 优化器迁移

| 条件 | 第 50 步 \(D_m\) | 95% CI | 结论 |
| --- | ---: | ---: | --- |
| router-only SGD | -0.00324 | \([-0.00413,-0.00245]\) | 可靠为负 |
| router-only AdamW | -0.04668 | \([-0.05474,-0.03562]\) | 同号、尺度更大 |
| joint AdamW | 0.00013 | \([-0.00465,0.00770]\) | 无法区分 |

joint AdamW 使两个条件的 task loss 都接近零，因此 margin contrast 回到无法
区分。它只能作为迁移结果，不能覆盖冻结 experts/representation 的主因果比较。

## 核心图

![margin growth contrast](figures/margin_growth_contrast.png)

阴影为按 seed 聚类的 95% 置信区间。SGD 与 router-only AdamW 的
specialist-minus-generalist contrast 可靠为负；joint AdamW 最终跨零。

![task value and routing efficiency](figures/task_loss_and_routing_efficiency.png)

左图说明 specialist 始终保持明显更低的任务损失；右图说明它虽然 margin
增长较小，却消除了更大比例的自身 routing excess。因此不能把较小 margin
growth 写成任务学习更差。

![pressure and realized movement](figures/pressure_actual_movement.png)

generalist 的初始 pressure 中位数为 146.99，specialist 为 121.94；第一步
实际 margin movement 分别为 0.002175 和 0.002148。较高 residual pressure
对应稍大的置信度更新，但不能告诉 router 哪个未选 expert 最好。

## 假设更新

| 假设 | 裁定 |
| --- | --- |
| specialist 保持任务价值 | 支持 |
| specialist 获得更大 margin growth | 证伪 |
| 负 \(D_m\) 表示 specialization collapse | 证伪；NMI 为 1，margin 都增长 |
| router-only AdamW 保持对比符号 | 支持 |
| joint training 保持非零对比 | 证据不足 |

## 边界与下一决策

当前只证明：在受控上下文任务和正确 top-1 起点下，ordinary weighted top-1
能够保持 supplied route；expert identity utility 与正确路由的 confidence
growth 不是同一量。

不能推出：自然语言语义 specialization、无先验发现、错误路由纠正、真实下游
收益，或新 gating 已经必要。

**下一唯一决策：** 固定 learned specialists，把 function-matched expert 的
初始 score rank 控制为 2 或 4，在 full-sequence LM loss 下检验 weighted
top-1 是否能找到它。主指标改为纠正时间与累计任务后悔值，而不是从正确路由
出发的 margin growth。

