# SFT 矩阵审计入口：给审计 AI 的资料清单与攻击面

日期：2026-09-10。性质：**派生导航视图，不是证据本体**。本文只说明"该读什么、读了能核什么、该攻哪里"，不含新的科学结论，也不改变任何 canonical 记录。所有数字以被指向的产物为准。

用途：把下文的「审计 AI 开场指令」整段复制给审计方，本文其余部分作为其阅读地图。

执行根：`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`
运行根：`<执行根>/runs/full-20260909T203104Z/`（下文相对路径均以此为基准）

---

## 一、必须首先交给审计 AI 的四条边界

否则审计会以"证据不足即否定一切"或"文件存在即通过"两种方式失效。

1. **研究者科学边界（逐字，AI 不得代为解除）**：
   > "这批模型适合观察'预训练模型局部微调中的结构变化'。固定八簇不能证明自然类别何时诞生，也不能替代语义解释。**审计末尾采集仍未齐全，尚不能交完整表征结论。**"
2. **不得作为证据的来源**：对话 memory（`.research/memory/conversations/**`，非 canonical）、文件名/运行标签/状态名（`COMPLETE`、`RENDERED_NOT_SCIENTIFIC_VERDICT`、`COMPUTED_NOT_SCIENTIFIC_VERDICT` 都只是完成度，不是科学判决）、期望中的模式。
3. **审计者不得做什么**：不得修改 `fm/**`（改动会作废全部 42 条 `run_identity.json` 与教师目标清单）；不得提交/推送/改 Graph/外部同步；不得干涉其他用户的作业；不得输出凭证。
4. **重跑是允许的，且被鼓励**：只读重算是审计的核心手段。`postprocess/` 下的探针可原样重跑，产物写入 `analysis/` 之外不影响身份。

---

## 二、阅读顺序（五层，由结论反推到身份）

顺序不能反：先拿到**待审断言清单**，再逐条找它的来源，否则会被海量产物淹没。

### L1 待审结论面（先读，建立 claim list）

| 文件 | 审计者从中提取什么 |
|---|---|
| `Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_matrix_training_dynamics_cn.md` | 主结论：剧烈变化在路由侧、集中在训练前 1/8 内完成；五通道表、9 行时间表、14 条件 NLL 端点表 |
| `Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_matrix_full_analysis_cn.md` | 全维分析四段式读面；§5 含研究者边界原句 |
| `daily_research_reports/0909/docs/0909_组会逐句校订稿_含原文对照.md` | 导师提问的原文语境（09:05 / 09:35 / 10:36 / 14:52）——判断"我们回答的是不是被问的问题" |

要求审计者：把这两份文档里**每一个量化陈述**抄成一张表，标出它引用的产物路径；引用不到产物的，直接标为不可核。

### L2 数字溯源（canonical 产物，逐条对表）

| 断言类别 | 唯一来源 | 审计者应核 |
|---|---|---|
| 14 条件训练/留出 NLL、t0 值 | `analysis/points.json` | t0 是否真的唯一（dev 2.79651 / test 2.83464）；14/14 是否都下降；端点数是否与表一致 |
| 方向位移 \(D\)、关系变化 \(R\)、\(S\) | `analysis/metrics.csv`、`analysis/contrasts.csv` | 39 对照 × 21 时刻的规模、配对定义、是否把单个区间不跨零当成发现 |
| 路由负载、原生 argmax 与实际路由的不一致 | `analysis/routing.csv` | 负载标准差 0.2372→0.3010；不一致率的定义（逐记录 vs 按来源加权是两个不同统计量，须看作者用哪个） |
| 教师覆盖 | `analysis/teacher_coverage_metrics.csv` | high28 在 dev/test 面板的覆盖量（34/1480、36/1481）；`MISSING_SOURCE_SUPPORT` 不等于效果为零 |
| 长度敏感性 | `analysis/length_sensitivity.csv` | 主结论是否对长度分层稳健 |
| 变化时点（损失/几何/路由/读出四通道） | `analysis/postprocess/change_timing.json` | 各通道最大单区间降幅/跳变是否与稿中一致 |
| 逐记录专家改选（76.77%） | `analysis/postprocess/routing_churn.json` | 端点值、逐条件范围 0.5133–0.9446、F/U 分解 |
| 图族产物 | `analysis/postprocess/figures_manifest.json`、`analysis/postprocess/fig0*/` | 图是否只声明为派生视图 |
| 公共 PCA 轴 | `analysis/global_axis_limits.json` | 这是全图公共轴的唯一权威来源，不得用各图自算轴 |
| 离线十配置（G8） | `offline_hierarchy/`（`receipt.json`、`identity.json`、`strict_recheck.csv`、`matched_control.csv`、`path_evidence.json`、`explanation_cn.md`） | 深度未增加也是有效结果；匹配控制的符号约定 `right_minus_left_* = high − leaf` |
| 计算回执 | `analysis/compute_receipt.json` | 42×21×2=1764 分片、39 对照、640 s 级；状态名是完成度非判决 |

### L3 可重跑脚本（让审计者自己算，而不是相信 JSON）

- `postprocess/probe_change_timing.py` → 复现四通道 × 21 检查点
- `postprocess/probe_routing_churn.py --workers 6` → 复现逐记录改选（读分片 npz 单成员，约 13 ms/条）
- `postprocess/figures/fig01…fig07*.py`、`common.py` → 复核图与数表一致
- `postprocess/parallel_analyze.py`（分析引擎，`compute_receipt.json` 记录其 `engine_sha256`）
- `postprocess/{axis_limits.py, panel_metadata.py}` → 轴与面板元数据口径

### L4 身份与完整性链（判"这批产物到底是不是这次跑的"）

`run_identity.json`（`source_hashes` 覆盖 `fm/**/*.py`）、`prepare_receipt.json`、`read_receipt.json`、`analysis/inputs.json`、`analysis/verify_training_corrected.json`、`full_submission_receipt.json`、`acp/`。

要求审计者：独立重算一次 `source_hashes` 并与 `run_identity.json` 比对，不要接受"文件存在"作为通过。

### L5 偏离与已知缺陷（审计火力最该集中处）

| 事项 | 记录位置 | 审计者要判 |
|---|---|---|
| `fm/verify.py` 侧车命名缺陷（期望 `update_SSSS.pt.json`，实际写 `update_SSSS.json`） | `postprocess/correct_verify.py` | 冻结不就地修是对的，还是应该重跑？修正是否改变了原始语义 |
| `fm/report.py` 覆盖表缺陷 | `postprocess/splice_coverage.py` | 拼接后的表是否只有显示层修正 |
| 分析引擎换成轨迹并行 | `postprocess/parallel_analyze.py` + `engine_sha256` | 是否改变了数学与产物 schema（声称未变） |
| 跨主机产物（容器 ↔ pod） | memory 与 `compute_receipt.json` 旁证 | **不得称为逐位相同**；实测数值等价量级 1e-16 |
| 聚类读出的显示对齐陷阱 | `analysis/clusters/<label>/<step>_h.npz` 的 `development` / `transition_from_previous` | 直接读 `transition_from_previous` 会误报大量流动，必须先做匈牙利重匹配 |

### L6 运行前合同（逐项判定，而不是重读一遍）

- `sft_audit_matrix_v2.json`：14 条件 × 3 种子、42 任务、39 个 G1–G6 对照定义、882 点、十离线配置 —— **要求审计者拿它与实际产物逐项对齐，缺失项与额外项都要报**
- `sft_audit_agent_handoff_cn.md`：9 行最低交付标准表 + 7 组预期问答 + 回审顺序
- `sft_representation_audit_plan_cn.md`：v2 主计划（科学定义所在）
- `sae_hierarchy_offline_extension_cn.md`：十配置离线附件

---

## 三、审计者应主动攻击的八个点

按"若被推翻则主结论受损"排序。前两个是真正可能翻盘的。

1. **t0 的专家输出严格为 0**（42/42 分片 `max|E| = max|shared| = 0`）。所以"76.77% 的记录在 u512 落到与 t0 不同的专家"比较的是**一次空转的分配**与一次有效分配。审计者必须判断：这是否足以推翻"训练中路由发生剧烈变化"这一表述？（我方口径：它使该数字不能读成"功能上的改换门庭"，但不否定"分配被整体重掷"。）
2. **独立性零假设 0.8040 是事后自推导，不是预注册判据**。要求审计者重算 `1 − Σ_k p_k(t0)·p_k(t512)`，检查边缘分布取法是否正确，以及"实测/期望 = 0.955 ⇒ t0 归属无预测力"是真结论还是边缘分布形状的必然结果。
3. **匈牙利重匹配给出的是下界**：真实合并可被匹配吸收。要求审计者独立复核"F 条件在全部 20 个区间流动恒为 0.0000"是否确为 h 逐位不变的互证，而非对齐伪影。
4. **多重比较**：39 对照 × 21 时刻。任何一个区间不跨零都不构成发现；要求审计者检查稿中是否有此类越界表述。
5. **CI95 只覆盖记录抽样，不含种子间训练方差**（种子间在 u512 约 0.14 nats）。方法排序类结论是否被过度声明。
6. **覆盖不足**：high28 在主面板只覆盖 34/1480（dev）与 36/1481（test），且 `weights(source, keep)` 在缺支持时返回缺失。任何 high28 结论是否越过了这个支持量。
7. **训练端点的跨种子差距混有各自批次组成差异**，不能称作纯粹的训练随机性方差；单步损失尖峰不得当作退化事件。
8. **结构梯度只更新 router**：梯度隔离的实际顺序是"保存其他参数梯度 → 注入结构梯度 → 断言未变"（`fm/training.py:116–122`）。审计者应核验实现与注册决定一致，且结构梯度未通过共同裁剪系数即时影响 attention。

---

## 四、可直接复制的「审计 AI 开场指令」

> 你是本实验的独立审计方。你的任务是**反驳**，不是复述。
>
> 工作根目录：`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`，运行根 `<根>/runs/full-20260909T203104Z/`。
>
> 先读 `Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_audit_postrun_brief_cn.md`（本文件），按它的五层顺序取证。然后：
> 1. 把 `sft_matrix_training_dynamics_cn.md` 与 `sft_matrix_full_analysis_cn.md` 中每一句量化陈述抄成断言表，逐条指向产物路径；指向不到的标为不可核。
> 2. 对每条断言，**自己从 L2 产物重算一次**，不要采信 JSON 中的汇总值本身。
> 3. 至少重跑 `postprocess/probe_change_timing.py` 与 `postprocess/probe_routing_churn.py --workers 6`，并检查它是否正确处理了显示对齐陷阱（必须先做匈牙利重匹配）。
> 4. 逐项核对 `sft_audit_matrix_v2.json` 与实际产物的一致性，缺失与多余都报。
> 5. 对本文第三节列出的八个攻击点各给一个明确判定：成立 / 不成立 / 证据不足。证据不足时给出补齐所需的最小测量。
>
> 硬约束：不得修改 `fm/**`（会作废全部 42 条 run_identity 与教师目标清单）；不得提交、推送、改 Graph 或外部同步；不得干涉其他用户的作业；不得输出任何凭证。只读重算与在 `postprocess/` 之外新建只读探针是允许的。
>
> 不得把文件名、运行状态名、或期望中的模式当作证据。`Unknown` 是合法结论。不得代研究者解除其科学边界。
>
> 输出：一张断言—证据—判定表；一份"翻盘风险排序"；一份最小补齐清单。
