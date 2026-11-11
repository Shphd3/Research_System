# R04 Protocol：原子集中度正则（A6）与原子共激活分组固定分发（A5）

- 上级：A17_13，接续 R03（`1109-teacher分发训练与2000步分析`）。
- 执行根：`/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/`
- 状态：训练前冻结（2026-11-09）。λ 在冒烟后按下面的规则写入，写入后不再改。
- 研究者授权：`1109-原子集中正则训练与账本分析_Codex执行Prompt.md`；研究者补充要求“只使用 share cluster”，所以训练资源从 4×H100 reserve 改为 share 4×H100 Reserved（`h100-4-reserved-16c256g`）。

## 1. 要回答的不确定性

R03 五臂 2000 步时，总体 NLL 的排序与集中度 $\bar M$ 中位数的排序一致。这个一致可能有两种解释：
1. **集中度是原因**：原子路由越集中，长尾学得越好；
2. **最强的竞争解释**：$\bar M$ 只是“学得好”的副产物（可学习路由学好之后自然更集中），或者 A1 的劣势只来自它的 token 级切分方式，与集中度本身无关。

能把两者分开的比较：
- A6 对 A0：只在 router 上直接优化集中度（不进入表征），检验能不能提高 $\bar M$、能不能改善低频 NLL；
- A5 对 A1：都是固定分发，只把切分单位从 token 换成原子。

## 2. 臂的定义（与 A0 唯一的不同见第 4 节 diff 清单）

**共同部分**：teacher 是 `20261031_dense_order_aligned_moe_baseline` 在 33B token 处的 state，取 block7.norm2 的输出，经 SAE `20261104_moe_gate_input_sae_33b/runs/formal/sae_full_final.pt` 得到 TopK32 编码，共 30000 个原子。每个 micro-batch 在线计算一次，使用 `inference_mode`，两条序列一块。
- 精度沿用 A1 的记录（`data/frozen.pt` 中 `teacher_bf16=True`，当时依据是簇 top-2 一致率 0.9906）。本轮在 DEV 上补测 top-32：单个索引一致率 0.98962，整组 32 个全部相同 0.7059（`evidence/teacher_precision_top32.json`）。单个索引一致率略低于 99%，作为边界记录。
- $p_j$ 用 R03 在 DEV 上冻结的值。$w_j=\min(\log(1/p_j)/\mathrm{median}_j\log(1/p_j),3)$，其中 median 取 7.6513，没有原子被截断到 3。冻结文件 `data/atom_groups.pt`，哈希见 `evidence/atom_groups.json`。

**A6**：路由与 A0 相同。另加
$$\mathcal L_{\text{conc}}=\frac1L\sum_l\frac{\sum_{j\in\mathcal J}w_jH_3(q^{(l)}_j)}{\sum_{j\in\mathcal J}w_j},\quad q^{(l)}_j(e)=\frac{\sum_t z_{t,j}\tilde P^{(l)}_t(e)}{\sum_t z_{t,j}},\quad \tilde P^{(l)}_t=\mathrm{softmax}(W_r^{(l)}\mathrm{sg}(h^{(l)}_t)),\quad H_3(q)=-\tfrac12\log\sum_e q(e)^3$$
其中 $\mathcal J$ 是本 micro-batch 内出现次数 ≥2 的原子。实现方式：在 $W_r$ 的一个分离副本上做 `autograd.grad`，所以梯度只进 $W_r$；各 rank 取平均后，在 DDP 的 CE 梯度同步之后加到 $W_r$ 的梯度上，再做裁剪。这和对 $\mathcal L_{\text{CE}}+\lambda\mathcal L_{\text{conc}}$ 求梯度在数学上等价。

**λ 规则**：冒烟中跑 λ=0 共 50 步，收集 50 步 × 8 层的 $\|\nabla_{W_r}\mathcal L_{\text{CE}}\|$ 与 $\|\nabla_{W_r}\mathcal L_{\text{conc}}\|$，取 λ = 前者中位数 / 后者中位数。λ 写入 `evidence/lambda_frozen.json` 和 `arms/A6.yaml` 后冻结。（初始权重下单 micro-batch 的探针中，CE 范数约 230–700，正则范数约 5–14，所以 λ 预计在 30–50 量级。实际值以冒烟实测为准。）

**A5**：在 DEV 上构建原子共激活图，边权 $W_{jk}=\#\{t:j,k\in A_t\}/\sqrt{n_jn_k}$；$n_j\ge20$ 的原子有 29999 个。对归一化拉普拉斯做谱聚类，取前 8 个特征向量（lobpcg），按行归一化后做 k-means（种子 2026110902）。然后移动边界原子 4964 次，使各组 DEV token 质量都落在均值的 ±20% 内（实际为 0.80–1.05）。分数 $s_{t,e}=\sum_{j\in G_e}w_jz_{t,j}$，选择 $S=\mathrm{Top2}(s+b)$，权重固定为各 0.5，8 层共用同一组分数，load bias 照常更新。

## 3. 预登记数值（EVAL，b=0）

| 臂 | $\bar M$ 中位数 | bin0 | bin1 | bin2 | bin9 |
|---|---|---|---|---|---|
| A1（token k-means） | 0.6969 | 0.660 | 0.675 | 0.703 | 0.675 |
| A5（原子谱聚类） | 1.3375 | 1.353 | 1.340 | 1.407 | 0.887 |

全部频段的数值见 `evidence/atom_groups.json` 的 `preregistered_b0_concentration`。

## 4. 与 A0 的 diff 清单

1. `routing_mode`：A6 为 `native_conc`（路由与 native 相同，另加 $\mathcal L_{\text{conc}}$）；A5 为 `fixed_scores` + `score_source=atom_groups`。
2. 存储：完整恢复存档每 250 步一份，只保留最近 2 个，旧的在新存档写完并算出哈希后删除，删除写入 `deletion_receipts.jsonl`；第 2000 步额外存一份完整 milestone；每 250 步另存 bf16 权重快照到 `runs/<arm>/weights/`。
3. 新增日志字段：每步的 `conc_*`、CE 与正则两部分的梯度范数及其比值；TensorBoard 的 `conc/*`。
4. A6 在 λ=0 冒烟时额外检查前 50 步 loss 与 A0 原始记录（`original_first200.json`）在 1e-6 内一致。
5. 不变的部分：模型结构、初始化、seed、数据顺序、batch、优化器、lr 调度、bf16/TF32、grad clip、load bias 规则、评估集。DDP 不使用自定义 comm hook；NCCL 超时 30 分钟，打开异步错误处理；评估和存档前后都有 barrier。

## 5. 预测与判定（训练前写死）

| 编号 | 预测 | 支持 | 削弱 |
|---|---|---|---|
| P1 | A6 在 2000 步的 $\bar M$ 中位数高于 A0，低频段更明显 | 成立 | 不成立：正则没有改变路由 |
| P2 | A6 在 bin0–2 的 NLL 低于 A0，且总体 NLL 不比 A0 差超过 0.01 | 成立 | 低频没有改善，或总体明显变差 |
| P3 | A5 的 $\bar M$ 高于 A1，NLL 也低于 A1 | 两项都成立 | 两项都不成立：原子切分不优于 token 切分 |
| P4 | 可学习路由的臂中，遗忘集中在高翻转率分位；固定路由臂翻转率约为 0，遗忘更少 | 成立 | 遗忘与翻转率无关 |

单种子，只有 2000 步。若差异小于相邻检查点之间的波动（250 步间隔下同一臂 NLL 的变化量），判为“不足”。

**各结果的下一步（AI 建议，研究者决定为 Unknown）**：
- P1 和 P2 都支持 → 做多种子复验，并检查是否存在循环风险（换一套原子定义来测 $\bar M$）；
- P1 支持而 P2 不支持 → 说明集中度可以被优化，但不带来学习收益，应弱化“集中度是原因”的解释；
- P1 不支持 → 先检查 λ 和梯度比，判断是正则太弱还是 load bias 抵消了它。

## 6. 资源

share 4×H100 一个任务，按冒烟 → A6 2000 → A5 2000 的顺序运行。任务内自动重试 3 次，每次间隔 30 秒。分析在本地 MIG 上做。
