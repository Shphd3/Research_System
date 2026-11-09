# SFT 路由表示全矩阵 v2 · 训练后分析与收尾计划（新增文档）

- 生成时间：2026-09-10T05:15Z
- 执行根：`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`
- 运行根：`runs/full-20260909T203104Z/`（identity 冻结于 2026-09-09T22:22:15Z）
- **文档定位（重要）**：本文件是**新增**计划，不是替换。
  - 原始设计/执行计划：`sft_representation_audit_plan_cn.md`（未改动）
  - 剩余工作清单（旧）：`sft_audit_remaining_work_cn.md`（未改动）
  - 交付与验收口径：`sft_audit_agent_handoff_cn.md`（未改动）
  - 身份与资产边界：`sft_audit_sources_cn.md`、`sft_audit_matrix_v2.json`（未改动）
  - 本文件只描述**集群跑完之后**要做什么、当前已确认到什么程度、以及给审计者的检查清单。
- 处理 agent：DeepSeek via Claude（harness: Claude Code；model: deepseek-flash）。非 canonical：科学判决仍由 researcher 拥有。

---

## 0. 一句话状态

**集群段已全部完成并经独立清点复核**（42/42 轨迹、882/882 检查点、1764/1764 分片，身份失配 0）；作业最终显示 `FAILED` **不是训练或提取失败**，而是完成验证器在"分析尚未运行（按设计在本地跑）"时以退出码 1 结束的连锁结果。剩余工作全部是**本机 CPU**：`analyze → render → 深 verify（含修正器）→ finalize → 证据索引与交付`。

---

## 1. 完成度核验（独立清点，不依赖作业状态字段）

核验方式：直接遍历共享存储上的产物并逐条校验其记录的 `identity['source']` 是否等于 live `source_hashes()`，而不是读作业的 state 字段。

| 对象 | 期望 | 实际 | 状态 |
|---|---|---|---|
| `conditions/*/training.json` | 42（14 条件 × 3 种子） | 42，全部 `TRAINING_COMPLETE_NOT_SCIENTIFIC_VERDICT` 且 identity 匹配，失败 0 | ✅ |
| 检查点 `checkpoints/update_SSSS.pt` + 同名 `.json` sidecar | 882（42 × 21） | 882 + 882 | ✅ |
| `recovery.pt` + `recovery.json` | 42 | 42 | ✅ |
| `sample_schedule.pt` + `parameter_contract.json` | 42 | 42 | ✅ |
| `representations/<cond>__seed<S>/update_SSSS/{development,test}.npz` + sidecar | 1764（42×21×2） | 1764，identity 失配 0 | ✅ |
| live `source_hashes()` == 冻结的 `run_identity.json` 源 | True | True | ✅ |
| 离线 G8（本机）`offline_hierarchy` | COMPLETE | `OFFLINE_COMPUTED_WITH_TYPED_INSUFFICIENCY_NOT_SCIENTIFIC_VERDICT`；40 views、2523 cluster 状态、1200 matched rows、345 图 | ✅ |
| 本机测试套件 | 43 | 43 通过（需 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`） | ✅ |

检查点更新位置（21 个，矩阵合同 `checkpoint_updates`）：`0,1,4,8,16,32,64,96,128,160,192,224,256,288,320,352,384,416,448,480,512`。

**至此为止，没有任何证据表明训练/提取存在缺失或身份漂移。** 唯一"红字"是下一节的验证器缺陷。

---

## 2. 作业终态 `FAILED` 的归因（唯一的"未完成"表象）

### 2.1 时间线（作业 `pt-uwfk144u`，`a15-sft-matrix-full-20260909T203104Z-r2`）

```
22:49Z  qualify      PASS（skip 复用，含 36 更新资格门）
23:00Z  train-all    4×H100，42 条轨迹 × 512 更新
01:38Z  （训练完成，42/42 training.json COMPLETE）
01:38Z  extract-all  1764 分片
04:48Z  （提取完成）
04:48Z  verify --fast 运行
04:51Z  verify 退出码 1 → 脚本终止 → 作业 state=FAILED
```

### 2.2 缺陷本体：`fm/verify.py` 的 sidecar 命名错误（已确认）

- `fm/verify.py:44-47` 期望的文件名：
  `checkpoints/update_SSSS.pt.json`、`recovery.pt.json`
- `fm/training.py:checkpoint_save` 实际写出的文件名（`path.with_suffix('.json')`）：
  `checkpoints/update_SSSS.json`、`recovery.json`
- 后果：每条轨迹被判 22 个"缺失" → 训练部分 `found = 42 − 924 = −882` → `training.status = PARTIAL` → `overall != COMPLETE` → `fm/cli.py:cmd_verify` 执行 `sys.exit(1)`（这是**设计内**的行为：非 COMPLETE 必须非零退出），外层 `timeout … bash fm_full.sh` 因此以非零结束，作业被判 FAILED。

**这是完成度计量口径的错误，不是产物缺失。** 第 1 节的独立清点已经用真实命名重新数过：882/882、42/42 全部在位。

### 2.3 为什么不在 `fm/` 里修（红线）

`source_hashes()` 覆盖 `fm/**/*.py`（以及 `matrix.json`、`runtime.sh`、`vendor_provenance.json`、`acp_full.sh`、`fm/offline_legacy/*.json`、`README.md`）。每一个检查点、每一个分片、每个 `training.json`、以及 TargetStore 清单都内嵌了生成时的 `source_hashes()`。**改任何一个 fm 源文件 = 全部 42 条轨迹 + 1764 个分片的来源记录当场作废**，且必须同批重建 target manifest 并重新冻结（历史教训：资格轮 r7 正是因为改了 fm 代码而使 target manifest 失效）。

因此处置方式是固定的：**在 `fm/` 之外写独立后处理器**，不改动 live 代码，并在 `evidence_index.md` 中记录"验证器偏差 + 本后处理器的修正口径"。

### 2.4 修正器要做什么（与 `report.py` 覆盖率拼接同属"fm 外后处理"）

1. 按真实文件名重新清点训练产物（42 条 `training.json`、882 `.pt`+`.json`、42 组 recovery/schedule/contract），逐条校验 `identity['source']`；
2. 输出一份 `analysis/verify_training_corrected.json`（或 draft 目录下同名文件），字段与 `fm verify` 的训练段兼容，附 `method` 与 `boundary` 说明；
3. 覆盖 `fm/report.py` 中已知未生效的覆盖率表拼接问题：直接从 `analysis/teacher_coverage_metrics.csv` 拼表（同样在 `fm/` 之外完成）；
4. 所有修正产物都标注 `NOT_SCIENTIFIC_VERDICT`，不得改写任何原始 receipt。

### 2.5 已实现的 fm 外后处理器（本轮已完成并验证）

新增目录 `postprocess/`（位于执行根，**不在 `fm/` 内**；`source_hashes()` 只覆盖 fm/**/*.py 与列名的少量文件，新增此目录不改变任何已记录身份）：

| 脚本 | 作用 | 用法 | 当前状态 |
|---|---|---|---|
| `postprocess/correct_verify.py` | 按真实 sidecar 命名重数训练段并复核身份/摘要 | `python3 postprocess/correct_verify.py --run runs/full-20260909T203104Z [--fast]` | **已运行，exit=0**，receipt `analysis/verify_training_corrected.json`：42/42 轨迹、882/882 `.pt`、882/882 sidecar、0 缺失、0 身份失配、`source_hashes_live_matches_recorded=true`、分片 1764/1764；`--fast` 跳过 46 GB 摘要复算（复算版待 L1 完成后跑，避免与 analyze 抢 I/O） |
| `postprocess/splice_coverage.py` | 由 `analysis/teacher_coverage_metrics.csv` 拼读者向覆盖率表；若 `result_draft/evidence_index.md` 存在则追加指针 | `python3 postprocess/splice_coverage.py --run runs/full-20260909T203104Z` | **已实现并用合成 CSV 验证**（多表、种子均值、`MISSING` 处理、JSON+Markdown 双输出）；待 L1 产出 CSV 后正式运行 |
| `postprocess/run_analyze_guard.sh` | 分析进程的自动重启 guard（最多 5 次，flock 防重） | 见 L1 状态条 | 运行中 |

三者都不修改任何原始产物、不改 `fm/`、不产出科学裁决。

---

## 3. 剩余工作链（全部本地 CPU；集群不再需要）

> 均已确认是纯 CPU 路径：`fm/analysis.py`、`fm/render.py`、`fm/verify.py`、`fm/offline.py` 无 torch/cuda 导入（`fm/core.py` 导入 torch，故本机仍建议带 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`）。

### L1 `fm analyze` —— 全维指标/自助法/PCA/聚类/对比

```bash
cd /data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
  python3 -m fm analyze --run runs/full-20260909T203104Z
```

- **状态：已于 2026-09-10T05:07Z 在本机后台启动；被外部静默杀掉两次后，现由 tmux 专用服务器 + 自动重启 guard 托管**。日志 `runs/full-20260909T203104Z/analysis_local.log`。
  - 第一次运行 05:07Z 起动、05:32Z 通过输入认证、05:56Z 在第 3 条轨迹的 update 160 处被静默杀死（日志 0 字节、无 traceback ⇒ 外部 SIGKILL/SIGTERM，非代码异常）。
  - 复跑前先隔离进程树：`tmux -L fm_matrix new-session -d -s guard 'bash postprocess/run_analyze_guard.sh'`。**必须用独立 socket 的 tmux server**（默认 socket 上是 harness 自己的 `deepseek-harness-web`，其会话重启可能连带清理）。
  - `postprocess/run_analyze_guard.sh`：监视 `python3 -m fm analyze` 是否存在；若退出且 `analysis/compute_receipt.json` 未出现，则自动重启（最多 5 次，flock 防重复）。已有进程在跑时它只等待，不打断。
  - **注意**：`tmux kill-session` 不会杀掉 pane 里 `exec` 的 python（它会变成 PPID=1 的孤儿继续写同一批产物）。清理时必须显式 `kill <python_pid>`，否则会出现两个进程同时写同一 run root 的危险重叠。
- 先做全量输入认证：对 1764 个分片逐个校验 `sha256` + `identity['source']` + `panel_sha256`，任何一项不符即 `ValueError('analysis input changed')`；通过后写 `analysis/inputs.json`。
- 产物（写进 `runs/full-20260909T203104Z/analysis/`）：
  `inputs.json`、`metrics.csv`、`length_sensitivity.csv`、`routing.csv`、`clusters.json`、`teacher_coverage_metrics.csv`、`bootstrap/<traj>/<step>_<split>.npz`（2000 draws）、`clusters/<traj>/<step>_<obj>.npz`、`projections/*.npz`+`projections.json`、`contrasts.csv`（39 对比 × 4 指标 × 21 更新 × 2 划分）、`points.json`、`compute_receipt.json`。
- 进度观测：`analysis/progress.json` 每完成一个 (轨迹, 更新) 写一次，共 42×21=882 次；该文件是唯一的进度刻度。
- 失败处理：`compute()` 无断点续算，中途异常需整段重跑；若报 `analysis input changed`，说明输入侧被外部改动，**先查因，不要改 fm 去迁就**。
- ETA（2026-09-10T06:30Z 实测）：输入认证段要哈希 1764 个分片共 **123 GB**（`du -sh representations`），实测 **≈200 MB/s** ⇒ 认证段约 **10–25 min**（首次运行实测 05:07Z→05:32Z 完成认证）。compute 段首次运行实测：**24 分钟完成 2.5 条轨迹 ⇒ 约 10 min/轨迹 ⇒ 全量约 7 h**（单进程，192 核未并行；随机器负载波动，以 `analysis/progress.json` 实测校准）。
- **完成后自检**：`analysis/compute_receipt.json` 存在即计算结束；训练段完成度另见 `analysis/verify_training_corrected.json`（见 2.4 与 L3）。

### L2 `fm render` —— G0–G7 图廊与对比图

```bash
python3 -m fm render --run runs/full-20260909T203104Z
```

- 依赖 L1 产物存在；产出图廊 + 对比图。判定：渲染完成且 receipt 状态非科学裁决。

### L3 深 `verify` + 训练段修正器

```bash
python3 -m fm verify --run runs/full-20260909T203104Z --lenient   # 取回 JSON 报告，训练段仍会是 PARTIAL
python3 <fm 之外的修正器> --run runs/full-20260909T203104Z        # 按真实 sidecar 命名重数训练产物
```

- 判定：修正后训练段 `found == expected`（42 / 882），且 `run_identity_ok = true`、分片段 1764/1764。
- 边界：修正器只改"清点口径"，不改任何原始文件。

### L4 `fm finalize`（结果草稿）+ 覆盖率表拼接

```bash
python3 -m fm finalize --run runs/full-20260909T203104Z
```

- 产出唯一结果草稿：`summary_draft.md` / `summary_cn.md` / `detailed_draft.md` / `evidence_index.md` / `ai_read_guide_cn.md` / `mentor_question_evaluation_cn.md` / `verify_receipt.json` / `receipt.json`（`DRAFT_NOT_CANONICAL`、`scientific_judgment = PENDING_RESEARCHER`）。
- 覆盖率表由 fm 外后处理器拼接（见 2.4）。
- 判定：`receipt.json` 明确 `PENDING_RESEARCHER`；**任何科学结论必须由 researcher 确认后才可写入 canonical Summary。**

### L5 交付给 researcher（读面顺序）

1. `summary_draft.md`（+ `summary_cn.md`）：Purpose / Hypothesis / Analysis method / Conclusion 四段；
2. `contrasts.csv` 里 6 组（G1–G6）共 39 个对比的效应量与 CI95（**注意：`R` 指标无 bootstrap，只有固定 panel 点值**）；
3. `routing.csv`（每 source 的实际计数、平均原生概率、`native_actual_disagreement`）与 `clusters.json`；
4. `mentor_question_evaluation_cn.md`（对导师问题的可答/不可答边界）。

### L6 收尾（不自动执行）

commit / push / Graph 更新 / 外部同步：**默认不做**，需 researcher 明确指示。memory checkpoint 见 `.research/memory/conversations/0910-sft-matrix-execution/memory.md`。

---

## 4. 训练集 NLL 诊断（已算出，供交叉核对；**不是** panel NLL）

来源：42 条 `conditions/*/training.json` 的 `history`。每条历史里的 `train_nll` 是该更新**当步被调度的那批记录**上的平均 NLL（token 加权），**不是**固定评测集——这是训练诊断，不是科学结论。

### 4.1 数字

| 量 | F 家族（冻结注意力） | U 家族（开放最后注意力） |
|---|---|---|
| t0（update 1，42 条共同） | 0.864 | 0.864 |
| update 512 端点（种子 17，单条） | 0.577–0.583 | 0.545–0.546 |
| update 512（3 种子均值） | ≈0.64 | ≈0.61 |
| 末 20 步均值（种子 17） | 0.685–0.692 | 0.651–0.652 |
| 相对 t0 的下降 | 25.2–25.9% | 29.2–29.4% |

- **U 家族系统性低于 F 家族约 0.035 nats**（同种子、同调度，匹配比较成立）。这是训练集上唯一的大效应。
- **教师臂（sae_a / sae_b / gmm_a / gmm_b / high28_a / high28_b / task）在同一种子、同一注意力档内几乎不可分**：512 处差异 ≲0.003 nats。
- **种子间离散 ~0.14 nats，远大于教师臂效应**（例：task_f 在 512 处三条种子分别 0.581 / 0.627 / 0.719）。任何教师臂结论都必须经过 panel + bootstrap CI，不能靠单条轨迹端点。
- 非单调：`nll@128 → nll@256` 在多数条件下**略升**（F 0.733→0.736，U 0.678→0.700）。这是逐步记录集变化 + 噪声造成的表观现象，趋势只能看窗口均值/EMA。
- 结构项（`scheme a/b`）：权重从 0.01 线性降到 0.001（512 步累计 2.816）；`structural_loss` u1 0.181 → u256 0.091 → u512 0.090（sae_b_u 种子 17）；结构梯度范数 0.0258 → 0.0011。
- 路由器漂移：`parameter_delta_norms.router` 在 512 处 1.14（sae_b_u 种子 17）；U 臂 `attention` 漂移 2.34，**F 臂 attention 漂移恒为 0.0（确证冻结）**。
- 负载观测（`balance` 字段，训练集内）：`max_vio` u1 1.467 → u512 3.090；`native_actual_disagreement` 0.0 → 0.3125。即训练中路由持续向少数专家集中，且与原生 argmax 的分歧增大——这是**观察**，其科学读法应取 L1 的 `routing.csv`（分 source）与 `clusters.json`，不要从单条历史下结论。

### 4.2 正确读法（避免误读）

- 单步 NLL 的抖动标度：末 100 次更新的**步间比值标准差 ≈ 0.09–0.12**。因此单步 +35–40% 的上升只是 ~3σ 噪声，**不能当事件读**。重算显示最大单步上升（36.6–40.5%）散布在不同更新上（例：task_f 种子 17 出现在 update 463，0.620→0.838），不存在"聚集在 261/356/447/462"的稳定模式。
- 决定性 NLL 对比一律取 L1 的固定 panel（development 1480 条 / test 1481 条）+ bootstrap 95% CI，训练历史曲线只用于"有没有在学、有没有发散"的诊断。

---

## 5. 本轮已解析的两个机制疑点（审计时请核对结论）

### 5.1 update 1 的 `task_router_gradient_norm` 位精确为 0.0（全部 42 条）——**不是 bug**

- 现象：42 条轨迹在 update 1 全部为位精确 `0.0`，update 2 起为 3.2e-6 量级，update 512 为 0.009–0.060。
- 机制（已由代码闭合）：`fm/legacy/model.py:11` 中 `Bank` 的上投影 `b` 零初始化 → t0 时每个专家输出**恒为 0** → `delta = shared + coefficient·experts` 对 `coefficient` 的偏导在 t0 恒为 0 → 任务损失对 router 参数无梯度。
- 佐证：纯任务臂 `task_f` / `task_u` 在 update 1 的 `parameter_delta_norms.router = 0.0`（router 完全没动）；结构臂 `sae_b_u` 的 update 1 只有结构项贡献（`clip_groups.router = 0.025808 == structural_gradient_norm`）。
- 结论：任务驱动的 router 训练实质**从 update 2 开始**；update 1 由结构先验独占（该步结构权重取最大值 0.01）。解读早期路由动态时必须记住这一点。

### 5.2 单步尖峰与噪声标度

见 4.2：步间比值 std ≈ 0.09–0.12，单步 40% 上升属噪声；此前"尖峰聚集在固定更新"的说法**不可复现，已撤回**。

---

## 6. 审计清单（逐条可执行，供 researcher 的 agent 使用）

| # | 检查项 | 命令/位置 | 通过标准 |
|---|---|---|---|
| A1 | 源身份未漂移 | 比较 live `source_hashes()` 与 `runs/full-20260909T203104Z/run_identity.json` 的 `source` | 完全相等（当前 = True） |
| A2 | 轨迹齐全 | `ls conditions/*/training.json` | 42 个，状态 `TRAINING_COMPLETE_NOT_SCIENTIFIC_VERDICT`，无 `failure.json` |
| A3 | 检查点齐全 | 数 `checkpoints/update_*.pt` 与 `.json` | 各 882 |
| A4 | 分片齐全 + 身份 | 逐分片比对 sidecar 的 `identity['source']` 与 `identity['panel_sha256']` | 1764/1764，失配 0 |
| A5 | 恢复与合同文件 | `recovery.pt(.json)`、`sample_schedule.pt`、`parameter_contract.json` | 42 组齐备，schedule 的 sha256 与 baseline 一致 |
| A6 | 验证器缺陷复现 | `fm/verify.py:44-47` vs `fm/training.py:checkpoint_save` | 确认 `.pt.json`/`recovery.pt.json` 与实际 `.json` 命名不符 |
| A7 | 关键数字交叉核对 | 见 §4.1：t0=0.864；种子 17 端点 F 0.577–0.583 / U 0.545–0.546；结构权重 0.01→0.001 | 与本文一致 |
| A8 | 梯度隔离 | `fm/training.py:116-122`（capture → 断言非 router 参数逐位不变 → 才 apply 结构梯度）；F 臂 `attention` 旋钮 `delta=0.0` 且 `gradient_norms` 里根本无 `attention` 键 | 结构梯度只进 router；F 臂注意力确未被更新 |
| A9 | 参数组裁剪独立 | `fm/network.py` 的 `parameter_groups()` + `clip_groups()` | 三组各自裁剪，无跨条件 all-reduce |
| A10 | 资格回执 | `runs/full-20260909T203104Z/qualification/receipt.json` | `PASS`，36 更新，离散字段精确、浮点字段在噪声底限内 |
| A11 | 测试 | `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python3 -m pytest -q` | 43 通过 |
| A12 | 作业终态解释 | `full_launch.log` 尾部 + `pt-uwfk144u` 状态 | 训练/提取完成 → verify 退出码 1 → FAILED，与 §2 一致 |

---

## 7. 最小上下文审计 Prompt（可直接粘贴给审计 agent）

> 你是审计 agent。目标：在**最少上下文**下验证一个已完成的 42 轨迹 SFT 路由表示矩阵实验的产物真实性与身份链，不做科学解释。
>
> 工作目录：`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`，运行根 `runs/full-20260909T203104Z/`。本机跑 Python 需 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`。
>
> 只做以下 7 件事，每件给出"通过/不通过 + 你实际看到的数字"：
> 1. 读 `fm/core.py` 的 `source_hashes()`，现场计算该哈希，与 `runs/full-20260909T203104Z/run_identity.json` 里的冻结值逐字符比对。
> 2. 数 `runs/full-20260909T203104Z/conditions/*/training.json`：期望 42 个；逐个检查 `status` 与 `identity['source']`；报告任何不一致。
> 3. 数 `conditions/*/checkpoints/update_*.pt` 与同名 `.json`：各期望 882；再数 `representations/**/*.npz` 与其 sidecar：期望 1764，且 sidecar 的 `sha256` 与文件实算值一致、`identity['source']` 与第 1 步哈希一致。
> 4. 打开 `fm/verify.py` 第 40–60 行与 `fm/training.py` 的 `checkpoint_save`，判断二者对 sidecar 文件名的期望是否一致；解释 `found = -882` 从何而来。**不要修改任何 fm 文件**（改任何 fm 源文件都会作废全部产物身份）。
> 5. 抽查 3 条轨迹的 `training.json`：报告 update 1 的 `train_nll`（应为 0.864）、512 的 `train_nll`（F 家族 0.577–0.583、U 家族 0.545–0.546，种子 17）、`structural_weight` 首末（0.01 → 0.001）、以及 `task_router_gradient_norm` 在 update 1 是否为位精确 0.0。
> 6. 检查 `fm/training.py` 中结构梯度的注入顺序：结构梯度是否在"断言非 router 参数梯度逐位不变"之后才被加入；F 臂（冻结注意力）的 `parameter_delta_norms.attention` 是否为 0.0。
> 7. 跑 `pytest -q`（43 项）并报告结果。
>
> 输出格式：一个 7 行表（检查项 / 期望 / 实测 / 结论），外加"任何你认为像 bug 但不在上面 7 项内"的观察，每条注明你看到的原始证据。不要给出科学结论。

---

## 8. 未决与需要 researcher 拥有的判断

1. **教师臂的可判性**：训练集 NLL 上六种教师臂几乎不可分，且种子离散（~0.14）远大于臂间差（≲0.003）。是否"以 panel NLL + 表示几何（D/S/R）为主要裁决面、承认训练损失不是裁决面"，属研究判断。
2. **U 家族领先的含义**：U 比 F 低 ~0.035 nats 是训练集上的匹配比较；它是否对应"表示更可读"或"任务更强"，必须等 panel NLL 与 D/S/R 对比的 CI，不可由训练损失外推。
3. **路由集中现象**（`max_vio` 1.47→3.09、`native_actual_disagreement`→0.31）是观察，不是结论；它在各教师臂之间是否有差异、与结构先验的关系，属机制问题。
4. **`R` 指标无 bootstrap**（`analysis.py` 中固定 panel 点值），凡涉及 R 的对比不得声称有 CI。
5. **固定 K=8 的聚类是探索性显示**（代码内已标注 `FIXED_K8_EXPLORATORY`、对齐仅用于展示），不能当作"类别自然出生/消失"的证据。
6. 最终 claim boundary、whether-to-claim 与下一步决策由 researcher 确认后方可写入 canonical Summary。

---

## 9. 参考路径索引

| 用途 | 路径 |
|---|---|
| 执行根（代码/合同） | `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`（`fm/`、`matrix.json`、`runtime.sh`、`acp_full.sh`） |
| 运行根（证据） | `runs/full-20260909T203104Z/`：`run_identity.json`、`full_submission_receipt.json`、`qualification_submission_receipt.json`、`full_launch.log`、`conditions/`、`representations/`、`analysis/`（L1 产物） |
| 完成验证器（有缺陷，冻结） | `fm/verify.py:44-47`；真实命名来源 `fm/training.py:checkpoint_save` |
| 结构梯度与参数组 | `fm/training.py:89-135`；`fm/network.py`（`parameter_groups`/`clip_groups`） |
| 零梯度机制依据 | `fm/legacy/model.py:7-22`（`Bank.b` 零初始化）、`fm/legacy/model.py:83-110`（`coefficient` 路径）、`fm/legacy/train.py:94-123`（`lr_factor`/`_norm`） |
| 分析入口（CPU） | `fm/analysis.py`（输入认证 `validated_shard`、`compute`） |
| 测试 | `tests/test_pipeline.py`（43 项） |
| 非 canonical 会话记录 | `.research/memory/conversations/0910-sft-matrix-execution/memory.md` |

---

## 10. 交接 Prompt（主目标一致性检测 + 后续规划）

> 与 §7 的分工：§7 审计**产物真伪与身份链**；§10 审计**方向是否跑偏**并规划后续。两者可分别交给不同 agent。

```text
# 角色与任务
你是新对话的主 agent。先判定"我们已完成/计划要做的事"与"研究主目标"是否同一件事，
再给出后续路线。禁止用聊天历史、文件名、作业状态、或本 prompt 的措辞当证据——
一切判定必须落到 canonical 源并引用其具体位置。

# 第 0 步（只读；先不要写文件、不要改任何东西）
按顺序读：
0.1 治理：/data/250010109/Research_System/AGENTS.md 与 CLAUDE.md；
    仓库技能在 .agents/skills/，按 description 匹配后再加载。
0.2 项目地图：PROJECTS.md（本工作流条目、当前优先级、状态行）。
0.3 当前 Focus：Projects/from-attention-to-search/main/focus/focus_sae_flat_router_functional_training.md
    （problem_key A15.sae_hierarchical_teacher_construction，focus_role SECONDARY，
     cycle_start 2026-09-09，result_state NOT_AVAILABLE）。同时检查
     daily_research_reports/0910/ 下是否已有更新的 Focus；若没有，明确写"未见更新的 Focus"，
     不要臆造新 Focus。
0.4 Anchor（科学设计 owner）：
    Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/
    15_13_semantic_supervision_middle_layer_formation/subanchors/
    15_13_11_structural_routing_incremental_learning_anchor.md
0.5 本实验的科学含义 owner（开发计划）：
    Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_representation_audit_plan_cn.md
0.6 执行状态（非 canonical，仅用于知道"已经跑到哪"）：
    .research/memory/conversations/0910-sft-matrix-execution/memory.md（读全文，最新条目=当前状态）
    Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_matrix_postrun_analysis_plan_cn.md

# 第 1 步：主目标一致性检测（输出一张表）
逐条列出本工作流"已完成 + 已计划"的动作，与 Focus 的核心问题、Anchor 的可否证假设对齐，
判定 ∈ {直接服务, 间接支撑, 无关/漂移, 无法判定}。每行必须给出 canonical 源的具体位置
（文件 + 小节/原句要点）。
必答的三个问题：
(1) 本矩阵 = 14 条件 {task, sae_a, sae_b, gmm_a, gmm_b, high28_a, high28_b} × {F 冻结最后注意力,
    U 开放最后注意力} × 3 种子 = 42 条轨迹 × 512 更新，39 个对比，表征指标 D/S/R + panel NLL。
    它回答 Focus 里的哪个问题？若它服务的是"结构先验是否让表示更可读"，而 Focus 主句是
    "结构路由是否形成值得局部增量学习的功能分工，以及新旧任务权衡"，请明确写出二者关系
    （支撑关系 / 只是相邻 / 已经换题）。
(2) 若主目标包含"任务依次到达时的复用 vs 局部增长 vs 固定容量"，本矩阵**没有覆盖**的部分是什么？
    逐条列缺口（缺的实验、缺的指标、缺的对照）。
(3) 哪些判断无法从 canonical 源确认？写 Unknown。不得用文件名/运行状态/诊断图补全。
若第 1 步结论含"漂移"：不要自行改题。写出分歧、影响、需要 researcher 决定什么，然后停下。

# 第 2 步：后续规划（最多 3 条路线）
每条给出：要解决的未决问题（引用 Focus/Anchor 原句）、依赖产物（analyze 的具体文件与指标，
路径写到 runs/full-20260909T203104Z/analysis/...）、判据（什么结果支持/否定；用预先固定的对照与
bootstrap CI，不得用训练集 NLL）、成本与依赖、风险。
最后给**一个**最小 next action，并标注：(a) 是否需要 researcher 决策；(b) 是否在已授权范围内。

# 已注入的当前状态（避免重复劳动）
- 集群段已结束，不要重启作业。作业 pt-uwfk144u state=FAILED 属验证器口径问题：
  fm/verify.py:44-47 期望 update_0000.pt.json / recovery.pt.json，而 fm/training.py 的
  checkpoint_save 实际写 update_0000.json / recovery.json → 训练段 found=-882 → cmd_verify 按设计
  非零退出。不是训练/提取失败。独立清点：42/42 轨迹、882/882 检查点、1764/1764 分片、身份失配 0。
- 本地 fm analyze 已于 2026-09-10T05:07Z 后台启动（纯 CPU，setsid nohup），产物写
  runs/full-20260909T203104Z/analysis/；进度看 analysis/progress.json（共 42×21=882 次进度点）。
  先做 123 GB / 1764 分片的 sha256+identity 认证，再进 compute 段。
  **在 inputs.json / metrics.csv 产出前，任何 NLL 或几何数字都不具备 panel 证据资格。**
- 训练集 NLL（诊断，勿当结论）：共同 t0=0.864；512 处种子 17 端点 F 0.577-0.583 / U 0.545-0.546；
  U 比 F 低约 0.035；教师臂间差异 ≲0.003，种子间离散 ~0.14；步间比值 std≈0.09-0.12，
  单步 40% 上升属噪声。update 1 的 task_router_gradient_norm 位精确为 0.0 已闭合解释
  （专家上投影零初始化 → t0 无任务梯度进入 router），非 bug。

# 红线
- 不改 fm/** 下任何源文件：fm 源在 source_hashes() 内，改一行即作废 run_identity.json、
  target manifest 与全部已记录产物身份。验证器缺陷一律用 fm 之外的后处理器。
- 不 commit / 不 push / 不改 Graph / 不做外部同步（需 researcher 明确指示）。
- 不得把文件名、作业状态、训练损失、诊断图当科学证据；Unknown 是合法状态。
- 若本对话将改动已注册科学问题，先运行：
    ./researchctl context A15.sae_hierarchical_teacher_construction --task "<具体部分>" --path "<预期路径>"
  结束时 ./researchctl release。当前状态显示该 problem_key 已有 3 个其他对话的开放任务
  （A6R1 post_training_analysis protocol、0909 离线两阶段计划、A5_balanced_h detailed）——
  重叠只是提示，不转移科学权限，是否需要协调由 researcher 决定。
```

---

**边界声明**：本文所有数字均来自本机对共享存储上产物的直接清点与 `training.json` 的读取，属**训练诊断与完成度核验**，不构成科学结论；科学判决与 claim boundary 由 researcher 拥有。任何需要改动 `fm/**` 源文件的想法都必须先停下来——那会作废 `run_identity.json` 与 target manifest，必须在同一批内重建并重新冻结。
