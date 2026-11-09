> **⛔ SUPERSEDED 作为入口 — 不要再把它当作入口。**
> 当前唯一入口：[`continuation.md`](../../../../../../../.research/memory/conversations/0910-sft-matrix-execution/continuation.md)（工作流：SFT 路由表示全矩阵）。
> 本文件是 **2026-09-11 01:30–05:30 这一个时间窗**的盘点索引，作为**历史盘点记录**仍有价值；
> 但它不是当前入口，其 mtime 依据也已随文件改写而漂移。

# 非规范交接索引：2026-09-11 01:30–05:30（北京时间）

本文件是给后续 AI 的文件定位与证据边界索引，不是科学结论、实验
`summary.md`、`detailed.md` 或新的事实来源。不要把文件名、mtime、运行完成标签或
派生分析标签当作科学判决。

## 1. 范围与统计口径

- 时间窗：北京时间 `[2026-09-11 01:30, 05:30)`，等价于 UTC
  `[2026-09-10 17:30, 21:30)`。
- 主检索范围：`/data/250010109/Research_System` 与
  `/data/250010109/MoE_Router` 下普通文件的 filesystem mtime。
- 运维补充范围：`/data/250010109/tools` 中直接相关的 DSH 升级文件；不展开
  `node_modules/` 依赖树。
- 文件系统不提供 birth time，因此仅凭元数据不能严格区分“首次创建”和“已有文件
  更新”。Research_System 的相关目录/文件在顶层或嵌套仓库中均为 untracked，且两个
  仓库在该时间窗均无 commit；这使“本窗新建”的判断可信度较高，但仍不是创建时间证明。

| 范围 | 文件数 | 字节数 | 说明 |
|---|---:|---:|---|
| Research_System | 19 | 1,922,173 | 4 个 Markdown、10 张 PNG、1 个脚本、4 个小型数据/说明文件 |
| MoE_Router | 932 | 32,320,152,270 | 69 个代码/审计/提交入口文件；863 个运行产物 |
| 研究相关合计 | 951 | 32,322,074,443 | 约 30.1 GiB，绝大部分是 checkpoint 与表征分片 |
| tools 主要运维文件 | 4 | 369,099 | DSH 升级说明、包锁与 Web patch；另有 1 个生成的 `node_modules/.package-lock.json` |

## 2. 建议阅读顺序与证据边界

1. 先读 E21 的已授权合同：
   `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/protocol.md`。
   文件状态是 `EXECUTION_AUTHORIZED_BY_RESEARCHER_2026-09-10`，它定义执行与审计顺序，
   但 Protocol 本身不拥有结果。
2. 再读试点资格收据：
   `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/runs/full-20260909T203104Z/dynamic/qualify_receipt.json`。
   其状态是 `PILOT_CHECKS_RECORDED_NOT_SCIENTIFIC_VERDICT`。
3. 核对完整训练/抽取的终端收据：同一 `dynamic/` 目录下的
   `run_dynamic.log` 与 `repair.log`。前者记录首次完成 3 条训练轨迹并生成 252 个分片，
   后者记录补齐后达到 6 条训练轨迹、252 个分片。日志是执行证据，不自动构成机制结论。
4. 再读派生分析：
   `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/audits/dynamic-teacher-20260911/dynamic_analysis.json`。
   其状态明确为 `DERIVED_NOT_SCIENTIFIC_VERDICT`；`analyze.log` 记录 15 个
   条件/种子组合被处理。
5. 面向人的第一阅读入口是
   `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260911/0911_dynamic_structural_teacher/report_cn.md`，
   配图位于相邻 `figures/`。报告中的判读与边界必须按原文保留，不得由后续 AI 加强。
6. 当前设计位置：
   `/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md`。
   它在本窗加入了 E21 派生结果段，但下一决策仍指向已注册的增量学习审计。
7. 与 E21 分开的候选路线是
   `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260911/0911_SAE第二轮方案与小实验/第二轮_SAE诊断与动态监督执行建议_cn.md`。
   同目录 README 明确：只有 AI 候选方案和本地 toy 检查，没有真实大模型结果，也没有启动远程作业。

重要缺口：本次盘点时，E21 实验目录只有 `protocol.md`，没有 `summary.md` 或
`detailed.md`。因此后续 AI 不得把 daily report、Anchor 中的派生段或
`dynamic_analysis.json` 提升成完整的规范证据链；若需要正式结果读取，先查是否后来新增了
这两个文件，并回到执行工作区核对收据与 artifact map。

## 3. Research_System：19 个文件

### 3.1 SAE 第二轮候选包（北京时间 01:43，共 6 个文件，30,471 字节）

目录：`daily_research_reports/0911/0911_SAE第二轮方案与小实验/`

- `第二轮_SAE诊断与动态监督执行建议_cn.md`：19,559 B；候选诊断、辅助 SAE
  复拟合资格试验与需要人类批准的真实训练边界。
- `minimal_geometry_and_sae_checks.py`：7,140 B；本地几何/SAE toy 检查。
- `README.txt`：313 B；明确非大模型结果与运行命令。
- `toy_results/geometry_results.csv`：251 B。
- `toy_results/toy_results.json`：1,926 B。
- `toy_results/toy_arrays.npz`：1,282 B。

### 3.2 E21 Protocol 与 Anchor（2 个文件，22,676 字节）

- 北京时间 02:14：`.../A15_13_E21_dynamic_structural_teacher/protocol.md`，8,750 B。
- 北京时间 05:04：`.../subanchors/15_13_11_structural_routing_incremental_learning_anchor.md`，13,926 B。

二者都位于嵌套仓库 `Projects/from-attention-to-search`，当前为 untracked；本窗无 commit。

### 3.3 动态结构教师阅读包（北京时间 02:13–05:04，共 11 个文件，1,869,026 字节）

目录：`daily_research_reports/0911/0911_dynamic_structural_teacher/`

- `report_cn.md`：25,233 B，北京时间 05:04。
- `figures/`：10 张 PNG，合计 1,843,793 B。
  - 第一轮读出：`F1_relation_appendix.png`、`F1_relation_meeting.png`、
    `F2_pointcloud_meeting.png`、`F3_structure_meeting.png`、
    `F5_cluster_shape_meeting.png`、`F6_noise_meeting.png`。
  - 第二轮结果：`R1_relation_drift.png`、`R2_structure.png`、
    `R3_membership_vs_noise.png`、`R4_task_effect.png`。

这 10 个日期目录阅读副本已逐一与 MoE_Router 审计目录中的源图做 `cmp`，全部字节一致。
报告提到的 F4 Sankey 不在本窗的日期目录 10 图中，不应虚构或补链。

## 4. MoE_Router：932 个文件

共同根目录：
`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix`

### 4.1 代码与审计入口（69 个文件，2,274,569 字节）

| 子树 | 文件数 | 字节数 | 内容 |
|---|---:|---:|---|
| `dynamic/` | 18 | 114,721 | 8 个 Python 源文件、4 个 shell 入口、6 个 `pyc` |
| `audits/task_u-cluster-evolution-20260911/` | 15 | 1,234,799 | 6 张 F 图、作图脚本、PCA/K-means/GMM 缓存 |
| `audits/dynamic-teacher-20260911/` | 7 | 924,437 | 派生 JSON、2 个日志、4 张 R 图 |
| `data/.../dynamic/` | 29 | 612 | 多次 submit 返回文本；路径重复嵌套，属于操作痕迹 |

`dynamic/` 的主要源文件：

- `smoke_cpu.py`：CPU smoke。
- `qualify_dynamic.py`：刷新、主模型不变与梯度隔离资格检查。
- `dyn_teacher.py`：SAE/GMM 动态教师实现。
- `train_dynamic.py`：训练循环及结构梯度隔离断言。
- `extract_dynamic.py`：指定更新步的表征抽取。
- `analyze_dynamic.py`：轨迹、关系与配对分析。
- `round2_figures.py`：R1–R4 作图。
- `run_dynamic.sh`、`repair_dynamic.sh`：首次运行与缺失轨迹修复。
- `submit_dynamic.sh`、`submit_repair.sh`：reserved 4xH100 提交入口。

### 4.2 大体积运行产物（863 个文件，32,317,877,701 字节）

根目录：`runs/full-20260909T203104Z/`

| 子树 | 文件数 | 字节数 | 扩展名分解 |
|---|---:|---:|---|
| `dynamic/` | 359 | 13,551,608,722 | 148 `.pt`、182 `.json`、7 `.jsonl`、19 `.log`、1 `.txt`、2 无后缀 |
| `dynamic_representations/` | 504 | 18,766,268,979 | 252 `.npz` + 252 `.json` |

表征面板覆盖 6 个动态条件/种子轨迹，每条 21 个更新点，每点 development/test 两个
split，即 \(6\times21\times2=252\) 个 NPZ 分片及 252 个配套 JSON。不要把这些原始产物
复制进 Research_System；按执行工作区原位读取。

运行日志边界：`run_dynamic.log` 末尾记录 `full finished trained=3 shards=252`；
`repair.log` 末尾记录 `repair trained=6` 和 `repair finished shards=252`。这只说明修复流程
补齐了目标轨迹/分片，科学资格仍由 Protocol、收据、派生状态与未来 Summary/Detailed
共同约束。

## 5. 同窗运维文件（与科学材料分开）

北京时间 01:33–01:43 的 DSH 0.1.5 升级相关文件：

- `/data/250010109/tools/UPGRADE-DSH-0.1.5.md`：4,775 B。
- `/data/250010109/tools/deepseek-harness/package.json`：66 B。
- `/data/250010109/tools/deepseek-harness/package-lock.json`：343,093 B。
- `/data/250010109/tools/dsh_web_patches.py`：21,165 B。

`node_modules/.package-lock.json`（310,454 B）是生成的安装内部文件，仅计作环境痕迹，
不作为交接阅读材料。运维升级材料不得与 E21 科学证据混读。

## 6. 可复现检索

```bash
find /data/250010109/Research_System -xdev -type f \
  -newermt '2026-09-10 17:30:00 UTC' \
  ! -newermt '2026-09-10 21:30:00 UTC' \
  -printf '%T@\t%s\t%p\n' | sort -n

find /data/250010109/MoE_Router -xdev -type f \
  -newermt '2026-09-10 17:30:00 UTC' \
  ! -newermt '2026-09-10 21:30:00 UTC' \
  -printf '%T@\t%s\t%p\n' | sort -n
```

mtime 是可变属性。若后续文件被改写，上述命令的结果会漂移；需要重做盘点时，应以新的
执行时刻重新生成清单，而不是把本索引当不可变 manifest。
