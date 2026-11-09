# Protocol 草案：A06_04_01_E01 上下文条件化专家效用

## 0. 审批快照

**审批状态：** 已批准。用户于 2026-07-21 明确批准实现、自检、smoke 和四张 H100 正式执行；英文 `protocol.md` 为 canonical 执行合同。

**模型合同更新：** 用户于 2026-07-21 禁止下载新 checkpoint，并将首选模型改为严格离线加载的 `/data/share/Qwen3-Coder-30B-A3B-Instruct`。下文若与英文 canonical `protocol.md` 冲突，以英文版为准。

**执行状态：** 已完成。四卡 smoke `pt-11i6h4tv` 与 full `pt-loe1371e` 均成功；注册判定为 `failed`：上下文能力与 \(I_{ctx}\) 通过，但双校准半集身份稳定性和 \(H_a^{REL}\) 失败。正式结果见 [summary.md](summary.md) 与 [detailed.md](detailed.md)。

**目的：** 判断真实代码 MoE 是否存在这样一个最小现象：同一段局部代码和同一组预测目标，在获得“真正相关的跨文件信息”后，某些专家相对其他专家变得更有用，而且原生 Router 没有完全利用这种差异。

**主锚点：** [A06_04_01 Context-Conditioned Expert Utility](../../../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/subanchors/06_04_01_context_conditioned_expert_utility_anchor.md)

**锚点决策问题：** 固定局部前缀和目标 token 后，相关跨文件上下文是否在最后一个 MoE block 产生跨划分稳定的专家效用变化，并留下相对原生 Router 的正损失余量？

**被检验的物理先验：** Router 接收的是上下文化隐藏状态，而不是孤立 token；若专家功能确实依赖条件，相关上下文应改变专家的相对效用。

**核心模型量：** 上下文—专家交互量 \(I_{ctx}\)，并以相关上下文中的绝对专家余量 \(H_a^{rel}\) 作为必要保护条件。

**主要证伪：** 模型本身能利用相关上下文，但相关上下文与等长无关上下文之间不存在稳定的专家相对效用变化，或变化不带来原生 Router 之上的正余量。

**实验角色：** 真实模型上的机制操作化测试；不是 Router 方法构造，也不是训练收益实验。

**主指标：** 留出测试集上的专家×上下文差分中的差分 \(I_{ctx}^{test}\)，单位为每个目标 token 的 nats；同时要求 \(H_a^{rel,test}>0\)。

**最小设置：** 冻结本地 `Qwen3-Coder-30B-A3B-Instruct`；使用 256 个 CrossCodeEval Python 样本；构造相关、局部、等长无关三种上下文；在最后一个 MoE block 中逐一测试全部 128 个路由专家。

**基本配置：** 模型原生每个 token 激活 8 个路由专家且没有共享专家。干预只把 8 个路由槽位中权重最低的一个替换为候选专家，保留原权重、其余 7 个路由专家和总激活数。

**运行条件：** 原生路由；128 个候选专家的等算力单槽替换；相关上下文、局部上下文、等长无关上下文；两个校准半集和一个完全留出测试集。

**通过：** 原生模型确实受益于相关上下文；校准出的优势/劣势专家在两个校准半集稳定；测试集 \(I_{ctx}\ge 0.01\) 且 95% 置信区间下界大于 0；优势专家的相关上下文余量 \(H_a^{rel}\ge 0.01\) 且置信区间下界大于 0。

**失败：** 上下文能力保护条件通过，但专家身份不稳定，或 \(I_{ctx}\) / \(H_a^{rel}\) 没有通过预注册阈值。

**证据不足：** 模型没有利用给定的相关上下文；数据配对、数值不变量或 128 专家全量评估失败；四卡分片缺失；基础设施中断。

**不能声称：** 不能声称 unfiltered 仓库代码普遍存在 headroom，不能声称 learned Router 有效，不能声称 rare 学得更快、common 保持，不能声称冲突隔离或 1M 长上下文利用已经得到改善。

**审批决策：** 按冻结测量执行；不扩展 Router 方法或训练实验。

## 1. 术语 / 定义

| 术语 | 直白定义 | 具体对象或计算 | 单位 / 公式 | 为什么重要 | 不能证明什么 |
| --- | --- | --- | --- | --- | --- |
| 共享模型 | 所有输入使用并更新同一组稠密参数 | 普通 dense FFN；本实验不以它为主比较对象 | 不适用 | 给后续“选择性共享”提供边界 | 本测量不比较训练收益 |
| 上下文配对 | 同一局部代码和目标，只改变前置跨文件信息 | `REL`、`LOCAL`、`NUIS` 三个 prompt 共享相同 `prompt` 与 `groundtruth` | 一组三个样本 | 消除目标 token 和局部前缀差异 | 不能消除所有数据集选择偏差 |
| `REL` | 检索到的候选相关上下文 | CrossCodeEval 非 oracle retrieval 给出的 `crossfile_context.text` 加原始 in-file prompt | token 序列 | 表示真实检索器提供的跨文件证据 | 每段检索片段都真正相关或被模型正确使用 |
| `LOCAL` | 只有局部上下文 | 仅原始 in-file prompt | token 序列 | 检查跨文件信息是否必要 | 与 `REL` 长度匹配 |
| `NUIS` | 等长但无关的跨文件上下文 | 来自另一仓库的 context，按模型 tokenizer 截断到与 `REL` 完全相同 token 数，再接同一 in-file prompt | token 序列 | 排除长度、绝对位置和“多给文本”解释 | 绝对不存在偶然语义重合 |
| 上下文化路由状态 | Router 真正接收的 token 表征 | 最后一层、与目标预测位置对齐的 \(h_{i,t,26}^{c}\) | 2048 维向量 | 明确路由对象不是孤立 token | 整个样本只有一个路由决定 |
| 原生路由 | 不修改模型的 top-8 路由 | 模型原始 gate 输出和专家集合 | target NLL | 真实基线 | 原生选择最优 |
| 单槽替换 | 等算力专家干预 | 用候选专家替换最低权重路由槽位；候选已激活时该位置 no-op | target NLL | 只改变专家身份，不改变激活专家数 | 可部署 Router |
| 专家余量 \(H_e^c\) | 候选专家相对原生路由能减少多少损失 | \(L_{native}^c-L_e^{swap,c}\) | nats / target token | 判断原生 Router 是否漏掉有用专家 | 该专家可由输入预测 |
| 上下文效用位移 \(\delta_e\) | 相关上下文比无关上下文更偏好专家 \(e\) 的程度 | \(H_e^{rel}-H_e^{nuis}\) | nats / target token | 选择上下文优势/劣势专家 | 自身不排除校准过拟合 |
| 主交互量 \(I_{ctx}\) | 两个专家的相对排序是否因相关上下文而改变 | \((H_a^{rel}-H_b^{rel})-(H_a^{nuis}-H_b^{nuis})\) | nats / target token | 区分一般 context gain 与专家特异效应 | learned Router 捕获能力 |
| 路由重叠 | 两种上下文使用相同专家的概率性相似度 | \(O=\sum_e q(e\mid c_1)q(e\mid c_2)\)，再对对齐位置取均值 | \([0,1]\) | 辅助解释路由是否响应上下文 | 共享是有益还是有害 |

## 2. 与锚点对齐

**决策问题：** 是否存在与真实跨文件证据绑定的、留出集可重复的专家函数差异？

**物理先验：** 同一目标 token 的隐藏状态会随可用上下文改变；若专家函数有条件性，专家相对效用也应改变。

**核心模型量：** \(I_{ctx}^{test}\)；\(H_a^{rel,test}\) 是绝对 headroom 保护条件。

**证伪：** native context gain 存在，而专家×上下文交互和绝对 headroom 不存在。

**边界：** 这是 CrossCodeEval Python、本地 Qwen3-Coder-30B-A3B-Instruct、最后一个 MoE block 上的局部结论；不直接关闭完整 A06_04 parent。

## 3. 被检验假设

对于相同的 in-file prompt 和 groundtruth，`REL` 会使某个候选专家 \(a\) 相对专家 \(b\) 更有用；该排序由校准集确定，在独立仓库组成的测试集仍保持，并且把最低权重槽位换成 \(a\) 能真实降低 `REL` 的目标损失。

## 4. 竞争解释

1. **目标 token 解释：** 专家只按待预测 token 分工。配对设计让三种条件的目标完全相同。
2. **局部语法解释：** 专家只按最后几枚局部 token 分工。三种条件共享同一 in-file prompt。
3. **长度 / 位置解释：** 更长 prompt 改变了隐藏状态和路由。`NUIS` 与 `REL` 精确匹配跨文件 token 数。
4. **一般上下文收益：** 相关 context 对所有专家同样有帮助。\(I_{ctx}\) 通过专家间差分消去共同变化。
5. **校准极值过拟合：** 从 128 个专家中挑最大值会产生假阳性。专家身份必须在两个校准半集稳定，并只在 untouched test 上判定。
6. **算力差异：** 干预多算了专家。单槽替换保持每 token 的 8 个路由专家不变。
7. **仅路由变化、无功能变化：** route overlap 下降不代表有用。它只能作为副指标，最终由 NLL headroom 和 \(I_{ctx}\) 决定。

## 5. 数据 / 模型 / 算法 / 目标

### 5.1 数据

- 数据源：CrossCodeEval GitHub revision `40c68d2b7ca2a8eae95d901ac80e6a540a84a53d`。
- 数据文件：archive Git blob `d838b2795a5b314fb7580c652c4df98f4c61d2c9` 中的非 oracle retrieval 文件 `python/line_completion_rg1_unixcoder_cosine_sim.jsonl`。不使用会借助 reference completion 检索的 `line_completion_oracle_*` 文件，避免目标泄漏式的检索上界被误当成真实 workload。
- 使用字段：`prompt`、`groundtruth`、`metadata.task_id`、`metadata.repository`、`crossfile_context.text`。
- 固定样本数：256。计算 `SHA256(repository + "|60401")` 的首字节并对 4 取模：余数 `0` 分入 `cal-A`，`1` 分入 `cal-B`，`2/3` 分入 `test`；再在每个池内按完整 `SHA256(task_id + "|60401")` 排序并分别取 64、64、128 个有效样本。同一 repository 不得跨 split。禁止按 native loss、路由、专家余量或模型正确性筛选。
- 仅允许的完整性排除：`groundtruth` 为空；相关 context 为空；groundtruth 经模型 tokenizer 后超过 128 tokens；没有同 split、不同 repository 且足够长的 nuisance donor；按冻结截断规则仍无法形成不超过 4096 tokens 的样本。任一 split 样本不足目标数量即判为证据不足，不临时放宽规则。

### 5.2 Prompt 构造

基础模型不使用聊天模板。分隔符沿用 CrossCodeEval `crossfile_context.text` 中的注释格式。

1. `REL = relevant_crossfile_context + in_file_prompt`。
2. `LOCAL = in_file_prompt`。
3. `NUIS = matched_irrelevant_crossfile_context + in_file_prompt`。
4. `NUIS` donor 必须来自同一 split 的不同 repository；按 task hash 顺序向后扫描并选择第一个足够长的 donor，再截断为与 `REL` cross-file 部分完全相同的 tokenizer token 数。若扫描一圈没有合法 donor，该样本按已注册完整性规则排除。
5. 4096-token 预算：groundtruth 最多 128；in-file prompt 保留最靠近补全点的最后 2304；cross-file context 按检索顺序保留最前 1536；固定分隔符占剩余预算。三条件共享完全相同的 in-file 和 target tokenization。

### 5.3 模型

- checkpoint：本地 `/data/share/Qwen3-Coder-30B-A3B-Instruct`；必须使用 `local_files_only=True`、`HF_HUB_OFFLINE=1` 和 `TRANSFORMERS_OFFLINE=1`。
- fingerprint：见英文 canonical `protocol.md` 中 config、weight index 与 tokenizer 的 SHA256。
- dtype：BF16；`eval()`；dropout 关闭；batch=1；不生成文本，只做 teacher-forced scoring。
- 架构事实：本地 config 与实际 module tree 共同验证 48 层全部为 MoE、128 routed experts、top-8 routed activation、无 shared expert。
- 预注册主层：最后一个实际 MoE block，zero-based `layer=47`。本实验失败不能外推到全部层。

### 5.4 干预算法

对 teacher-forced 序列，目标 token \(y_j\) 由前一位置的 logit 预测。因此只在位置 `target_start-1` 到 `target_end-2` 的 layer-26 MoE 路由上执行干预；context token 和其他层保持 native。

对每个候选专家 \(e\in\{0,\ldots,127\}\)：

1. 记录 native top-8 expert IDs 和 weights。
2. 找到最低 weight 的 routed slot。
3. 若 \(e\) 尚未激活，用 \(e\) 替换该 slot，保持原 weight，不重新归一化。
4. 若 \(e\) 已在 top-8，该位置保持 native，记为 no-op。
5. 其他七个 routed slots 和所有非目标预测位置不变；该模型没有 shared expert。
6. 计算 groundtruth 全部目标 token 的平均 NLL。

### 5.5 目标函数

本实验不训练模型。唯一任务量是 teacher-forced target negative log-likelihood：

\[
L_i^c(e)=-\frac{1}{|y_i|}\sum_j\log p_e(y_{i,j}\mid x_i^c,y_{i,<j}).
\]

## 6. 条件、随机性与检查点

无训练 seed、无 checkpoint。数据排序 seed 固定为 `60401`，paired bootstrap seed 固定为 `60402`，重采样次数固定为 `10000`。

| 项目 | 对应锚点条款 | 模型量 / 竞争解释 | 为什么需要 | 主/副证据 | 通过 | 失败 | 证据不足 | 产物 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Native `REL` vs `NUIS` | 模型能利用相关 context | context-capability guard | 没有它就无法解释专家条件性 | 必要保护 | \(L_{native}^{NUIS}-L_{native}^{REL}>0\) 且 CI 下界 >0 | 不作为机制失败 | CI 不通过 | `tables/context_capability.csv` |
| 128-expert matched slot swap | 功能 headroom | \(H_e^c\)、\(I_{ctx}\) | 决定专家功能而非路由外观 | 主证据 | 主阈值全部通过 | 主阈值失败 | 分片缺失 | `tables/expert_context_utility.csv` |
| `cal-A` / `cal-B` identity check | split stability | 极值过拟合 | 防止 128 选 1 假阳性 | 必要保护 | \(a\) 双半集 top-8、\(b\) 双半集 bottom-8 | 身份不稳定 | 某 split 样本不足 | `tables/calibration_stability.csv` |
| `LOCAL` condition | 跨文件必要性 | local-only rival | 给出方向性边界 | 副证据 | `REL` 方向一致 | 不改变主判定 | 长度不可比 | `tables/local_only_guard.csv` |
| Native replay / formal no-op | 实现正确性 | 数值与 hook 错误 | 确保 swap 没有暗改模型 | 必要保护 | NLL 差绝对值 \(\le 2\times10^{-4}\) nats/token | 不作为科学失败 | 判定证据不足 | `tables/invariance_checks.csv` |
| 路由重叠与 top-8 Jaccard | Router 是否响应 context | route-overlap diagnostic | 连接选择性共享直觉 | 副证据 | 仅解释 | 不单独判定 | router logits 缺失 | `tables/route_overlap.csv` |
| 选中专家对的梯度审计 | would-be training signal | \(g_e^c=\nabla_{\theta_e}L^c\) | 回答“同一目标在不同 context 下会怎样训练 expert” | 副证据 | 报告 cosine / norm | 不单独判定 | 显存或 hook 失败不影响主判定 | `tables/gradient_diagnostic.csv` |

## 7. 主指标

校准阶段先计算

\[
H_e^c=\mathbb{E}_{cal}[L^c(native)-L^c(e)],\qquad
\delta_e=H_e^{REL}-H_e^{NUIS}.
\]

只用 `cal-A + cal-B` 选择

\[
(a,b)=\arg\max_{e\ne e'}(\delta_e-\delta_{e'}),
\quad H_a^{REL,cal}>0.
\]

然后冻结 \((a,b)\)，在 test 计算

\[
I_{ctx}^{test}
=(H_a^{REL,test}-H_b^{REL,test})
-(H_a^{NUIS,test}-H_b^{NUIS,test}).
\]

**单位：** nats / target token。

**为什么它主导决策：** 它要求“专家间差异”随相关 context 改变，能够消去所有专家共同获得的一般上下文收益。仅有 route flip、hidden-state 距离或单个 expert loss 差都不能完成这个区分。

**假阳性代价：** 会错误授权后续 learned Router 方法，因此采用独立 test、双校准半集稳定性、matched nuisance、绝对 headroom 和 0.01 nats/token 实际阈值的保守联合规则。

**假阴性边界：** 单一 Python benchmark 和最后一层可能漏掉其他层/语言中的效应；所以失败只否定该注册表面，不否定所有上下文路由。

## 8. 副指标

1. native context gain：\(G_{ctx}=L_{native}^{NUIS}-L_{native}^{REL}\)。
2. relevant absolute headroom：\(H_a^{REL,test}\)。
3. 128 维 utility-vector 的 `REL`/`NUIS` Spearman correlation。
4. full-gate route overlap \(\sum_e q_e^{REL}q_e^{NUIS}\) 和 native top-8 Jaccard。
5. 候选专家 native inclusion rate，解释 no-op 比例。
6. 选中 \(a,b\) 的最后一层 expert-parameter gradient cosine、norm ratio 和按 expert 分配的 gradient mass。
7. 上下文化隐藏状态位移 \(\|h^{REL}-h^{NUIS}\|_2\)；它只说明 representation 改变，不能作为成功标准。

## 9. 已知好例 / 坏例 / 易混淆例

**已知好例：** `REL` 应比 `NUIS` 或 `LOCAL` 降低 native target NLL；否则 workload-model pairing 不具备本实验所需的上下文能力。

**已知坏例：** route overlap 明显下降但 \(I_{ctx}\) 和 \(H_a^{REL}\) 为零。这只说明 Router 对 context 敏感，不说明选择正确。

**易混淆例：**

- \(I_{ctx}>0\) 但 \(H_a^{REL}\le0\)：相对排序变化来自某个专家变差，没有原生 Router headroom，判失败。
- \(H_a^{REL}>0\) 但 \(I_{ctx}\le0\)：存在一般 expert headroom，但没有证据说明它由相关 context 条件化，不通过本 sub-anchor。
- `REL` 优于 `LOCAL` 但不优于等长 `NUIS`：不能排除长度/位置效应，判证据不足。
- gradient 明显不同但 loss utility 不同不稳定：训练信号诊断不能替代功能结论。

## 10. 分阶段执行与四卡合同

### 10.1 执行位置

批准后在远程执行面新建独立 workspace：

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a06_04_context_utility
```

原始数据、模型缓存、逐样本 parquet、日志和完整 runs 留在远程 `/data`；Research_System mainline 只接收小型表、主图、`summary.md` 和 `detailed.md`。

### 10.2 ACP 资源

```text
WORKSPACE_NAME=share-space
CLUSTER_NAME=share-cluster
WORKER_SPEC=n6ls.iu.i40.4
GPU_COUNT=4
QUOTA_TYPE=spot
IMAGE_URL=registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-private-lite:container1-20260523142552
MOUNT_SPEC=01995892-d478-76d8-aec7-13fd8284477e:/data
MODEL_PATH=/data/share/Qwen3-Coder-30B-A3B-Instruct
```

checkpoint 已在 `/data/share` 完整存在，禁止重新下载。SCO CLI 已升级到 2.0.0 / registry release `20260630`，`share-space` 与 `share-cluster` 的只读查询恢复，四卡 spec `n6ls.iu.i40.4` 已验证存在。

### 10.3 阶段表

| 阶段 | 局部问题 | 输入证据 | 通过 / 失败 / 不清楚 | 调试产物 | 交接 |
| --- | --- | --- | --- | --- | --- |
| Preflight | 模型、数据、四卡和 hook 环境是否可用 | revision、`nvidia-smi`、SCO、磁盘 | 四卡可见、revision 一致、依赖可导入 | `logs/preflight.log` | 失败即停 |
| Smoke | 单槽替换是否精确且产物 schema 完整 | 8 样本、专家 `[0,16,32,48]`、三条件 | finite loss；no-op tolerance 通过；四 shard 可合并 | `runs/smoke/` | 通过才 full |
| Full scoring | 128 专家是否全部完成 | 256 样本、三条件 | 四卡按样本分片，每个样本评估全部 128 experts；无缺失 | `runs/full/shard_*.jsonl` | merge |
| Frozen selection | 校准专家对是否稳定 | cal-A / cal-B | 双半集 top/bottom-8 规则 | `tables/calibration_stability.csv` | 冻结 \((a,b)\) |
| Held-out decision | 主交互和绝对 headroom 是否通过 | untouched test | 按第 12 节裁定 | `tables/primary_metrics.json` | result record |
| Gradient audit | would-be update 是否随 context 改变 | 固定 test 子集 32 样本、冻结 \((a,b)\) | 只报告，不改变主判定 | `tables/gradient_diagnostic.csv` | detailed |

## 11. 算法规格

**输入：** 固定模型 revision、CrossCodeEval 固定 archive、256-sample manifest、三种 prompt、候选 expert IDs `0..63`。

**参数：** `layer=26`、`max_seq_len=4096`、`target_cap=128`、`infile_cap=2304`、`crossfile_cap=1536`、data seed `60401`、bootstrap seed `60402`、10000 bootstrap replicates。

**中间量：** native gate scores、top-8 IDs/weights、target mask、candidate-swap loss、\(H_e^c\)、\(\delta_e\)、\((a,b)\)、\(I_{ctx}\)、route overlap、gradient diagnostic。

**步骤：**

1. 下载并校验固定模型/data revisions，写 immutable manifest。
2. 构造 256 个 context-paired 样本和 repository-grouped splits。
3. native forward，记录 loss、router probabilities、top-8、hidden states 和长度。
4. 运行 smoke；任何数值不变量失败立即停止。
5. 四张卡按确定性样本序号分片；每张卡持有一个模型副本，并对其样本的 `REL/NUIS/LOCAL` 完成全部 128 个专家的 exact slot-swap scoring。最后一层缓存避免四张卡重复跑同一样本的 Transformer 主干。
6. 合并前验证 `(task_id, condition, expert_id)` 笛卡尔积完整。
7. 仅用 cal-A/cal-B 计算稳定性并冻结 \((a,b)\)。
8. 在 test 计算 \(I_{ctx}\)、\(H_a^{REL}\) 和 paired-bootstrap CI。
9. 对固定 32 test 样本执行 selected-pair gradient audit；不更新参数。
10. 生成一个主表和至多两张主图；原始逐样本结果留远程。

**输出：** `sample_manifest.jsonl`、`expert_condition_losses.parquet`、`context_capability.csv`、`calibration_stability.csv`、`primary_metrics.json`、`route_overlap.csv`、`gradient_diagnostic.csv`、`context_expert_interaction.png`、`headroom_and_overlap.png`。

**失败原因标签：** `model_context_incapable`、`data_pair_invalid`、`no_op_mismatch`、`missing_expert_shard`、`nonfinite_loss`、`unstable_identity`、`no_context_interaction`、`no_absolute_headroom`、`infrastructure_failure`。

## 12. 成功 / 失败 / 证据不足

### 成功

必须同时满足：

1. \(G_{ctx}\) 的 95% paired-bootstrap CI 下界 \(>0\)；
2. \(a\) 在 cal-A 和 cal-B 都位于 \(\delta\) top-8，\(b\) 都位于 bottom-8；
3. \(I_{ctx}^{test}\ge0.01\) nats/token 且 CI 下界 \(>0\)；
4. \(H_a^{REL,test}\ge0.01\) nats/token 且 CI 下界 \(>0\)；
5. no-op、全量 128 experts、三条件和四分片完整性全部通过。

允许结论仅为：

> 在注册的真实跨文件代码补全表面上，同一目标的相关上下文会改变最后一层路由专家的相对功能效用，并存在原生 Router 未完全利用的留出损失余量。

### 失败

上下文能力保护条件通过，但稳定性、\(I_{ctx}\) 或 \(H_a^{REL}\) 任一科学条款不通过。允许结论仅为：

> 在注册模型、数据、层和干预下，没有检测到足以支持 context-conditioned expert headroom 的证据。

### 证据不足

上下文能力、数据配对、数值不变量、全量分片或基础设施任一保护条件不成立。不得把它写成“专家效用不存在”。

## 13. 本实验不能声称什么

- CrossCodeEval 是静态分析筛出的跨文件依赖任务；不能代表 unfiltered repository-code 分布。
- 只测最后一个 MoE block；不能否定或证明其他层。
- 模型被冻结；不能说明 rare 学得更快、common 保持或训练冲突减少。
- 单槽 oracle swap 不是可部署 Router。
- \(I_{ctx}>0\) 不能赋予专家自然语言语义。
- route overlap、hidden-state dispersion 和 gradient difference 都只能辅助解释，不能代替 loss utility。
- 不测 1M token；只能作为“长上下文检索信息是否可能需要条件化路由”的前置机制证据。

## 14. 审阅记录与协议变更

- **2026-07-20，AI 草案：** 将用户提出的“同一 token / 不同上下文”改写为更严格的“同一 in-file prefix 和同一 groundtruth，仅改变相关 evidence”。原因是不同 target 会让梯度差异成为必然现象，无法证明 context-conditioned routing。
- **2026-07-20，AI 草案：** 选择等长不同仓库 context 作为主负对照，`LOCAL` 只作方向性保护；这样主指标不受 prompt 长度和目标绝对位置直接混淆。
- **2026-07-20，AI 草案：** 用 native top-k 中最低权重槽位的 matched swap 代替“强迫所有 token 只走一个 expert”，避免改变 active compute 和制造严重分布外干预。
- **2026-07-21，用户批准：** 批准数据规模 256、最后一层 `26`、0.01 nats/token 实际阈值、四卡规格和上述 claim boundary，并要求开始执行和自检。
- **2026-07-21，实现细化：** 四卡由 expert-ID 分片改为样本分片；所有卡仍评估全部 128 个候选。原因是最后一层精确缓存可避免 Transformer 主干重复前向。该变化不改变 prompt、干预、损失或统计量，并增加 cached replay 对 literal patched full forward 的等价性检查。
- **2026-07-21，模型合同更新：** 改用本地 Qwen3-Coder，结构变为 128 experts/top-8/layer 47；GPT-OSS 仅在注册的 4096-token OOM 后作为独立实验备用。Qwen 峰值显存自检通过，因此未切换。
- **2026-07-21，执行闭环：** 纠正 BF16 residual 加法顺序后，快速重放、完整前向和 formal no-op 的 logits/NLL 最大误差均为 0。四卡 full 完成 256 样本、三条件、全部 128 experts；最终因专家身份不稳定和绝对正 headroom 不通过而判失败，不是证据不足。
