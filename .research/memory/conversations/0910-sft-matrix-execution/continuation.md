# Continuation Brief: SFT 路由表示全矩阵 — 收尾链与后续训练

```text
Workstream:     SFT routing/representation full matrix (收尾 + 后续训练)
Problem key:    none registered for this execution; scientific home is A15
Role:           SECONDARY (execution workstream)
Record:         .research/memory/conversations/0910-sft-matrix-execution/
Continues from: 0910-clustering-change/memory.md
Supersedes:     daily_research_reports/0910/docs/sft_continuation_prompt_cn.md
                daily_research_reports/0910/docs/sft_audit_agent_handoff_cn.md
                daily_research_reports/0910/docs/sft_audit_full_run_prompt_cn.md
                daily_research_reports/0910/docs/sft_framework_resume_cn.md
                daily_research_reports/0911/0911_0130_0530_document_inventory/handoff_cn.md
Updated at:     2026-09-11 (consolidated; source snapshot 2026-09-10T12:33Z)
Status:         CURRENT
Non-canonical:  points at canonical sources; owns no claim, approval, verdict,
                or next decision.
```

> **Consolidation note.** 本文件把上述 5 份互相指认的入口文档合并为唯一入口。
> **合并，非删除**：5 份原件全部保留，仅加 SUPERSEDED 头指针。原件中的状态快照
> 来自 2026-09-10T12:33Z 的文件清点；**之后的状态以产物本身为准**，本文件的
> F 段亦然。

---

## A. Environment roots

| Root | Path | Readable here? |
|---|---|---|
| Repository root | `/data/250010109/Research_System/` | 容器 yes ／ Windows checkout `C:\Users\250010109\data\Research_System` yes |
| Execution root | `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/` | **容器 yes ／ Windows no** |
| Run root (全部证据) | `<execution root>/runs/full-20260909T203104Z/` | **容器 yes ／ Windows no** |
| `/root/**`（字体等） | `/root/...` | **no**（容器回收即丢失） |

**环境约束（会改变你能做什么）**

- 容器为 cgroup 约 8 CPU；**大约每 4 小时被回收一次**。`/data` 是网络挂载
  （`quarkfs_client`），在回收中存活；`/root` 不存活 —— 字体一类资源必须放
  `<execution root>/postprocess/fonts/`。
- **长 CPU 任务必须放远端 pod**，或自带续算。容器内不适合作业。
- 容器内跑 python 需前缀：`PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`。
- `sco` 不在 PATH；提交必须走 `docs/execution_envelope.md` 登记的入口。
- **`./researchctl` 依赖 `fcntl`，只能在 Linux 容器运行，Windows checkout 上不可用**
  （实测 `ModuleNotFoundError: No module named 'fcntl'`）。因此 `researchctl envelope`
  与一切凭它解析的提交动作**都必须在容器里做**。
- 根标为 `no` 的引用是**不可核验**，不是「过期」：报告它，不要静默丢弃。

## B. Read list — 按顺序；`required` 缺失即停下报告

| # | Path（相对仓库根，除注明外） | 回答什么问题 | Required |
|---|---|---|---|
| 1 | `AGENTS.md` ＋ `CLAUDE.md` | 治理：科学不变量、状态归属、审批边界 | yes |
| 2 | 按 description 加载 `.agents/skills/` 下的 SKILL.md：`research-progress-core`、`experiment-card-writer`、`research-memory`、`remote-experiment-workflow` | 结果写作完成合同、memory 合约、远端工作流 | yes |
| 3 | `.research/memory/conversations/0910-sft-matrix-execution/memory.md`（**读全文**，最新条目＝当前状态） | 上一对话的累积工作上下文 | yes |
| 4 | `daily_research_reports/0910/docs/sft_representation_audit_plan_cn.md` | **本实验的科学定义 owner**：14 条件、教师定义、梯度范围、检查点合同、完成合同 | yes |
| 5 | `daily_research_reports/0910/docs/sft_matrix_postrun_analysis_plan_cn.md` | 收尾链 L1–L6 定义、两个 `fm` 缺陷完整归因、12 项审计清单 | yes |
| 6 | `daily_research_reports/0910/docs/sft_matrix_full_analysis_cn.md` | 全维分析读面（四段式）；§5 含研究者边界**逐字原句** | yes |
| 7 | `daily_research_reports/0910/docs/sft_matrix_training_dynamics_cn.md` | 「训练中的剧烈变化」读面：五通道表、时间表、训练结果表 | yes |
| 8 | `daily_research_reports/0909/docs/0909_组会逐句校订稿_含原文对照.md` | 导师提问原始语境（09:05 / 09:35 / 10:36 / 14:52）；判断「我们答的是不是被问的问题」 | yes |
| 9 | `docs/execution_envelope.md` | 运行在哪、什么镜像、走哪个入口、回执必须留什么 | yes（要提交或要判断资源时才需要） |
| 10 | 执行根 `README.md`、`matrix.json` | 阶段表、14 条件 × 3 种子执行清单、39 个对比定义 | yes |
| 11 | `<run root>/run_identity.json`、`analysis/compute_receipt.json`、`postprocess/complete_chain.sh` | 身份冻结值、分析回执、完成链本体（marker 与 flock 语义） | yes |
| 12 | `PROJECTS.md`；A15 当前 Focus 与 Anchor | 判断科学归属或要改动已注册问题时 | no（**只读不推断**） |

**按需读**：`sft_audit_postrun_brief_cn.md`（要独立审计时；五层阅读顺序、断言→产物对照、八个攻击点）、
`sft_matrix_analysis_review_cn.md`（P1/P2 分析优先级）、`sft_audit_matrix_v2.json` /
`sft_audit_sources_cn.md`（**2026-09-09 执行前**合同，只能当逐项判定清单，**不能当现状依据**）、
`sae_hierarchy_offline_extension_cn.md`（十配置离线定义）、`sae_relations_explained_cn.md`
（分不清原子/层级/输入聚类/路由/专家输出时读）。

**不得作证据**：

- 对话 memory 里的数字与判断（非 canonical；科学判决只在 Focus / Anchor / Protocol / Summary / Detailed 上）。
- 旧实验（A6R1、0909 离线、A5）的结果 —— 不能替代本轮证据。
- 原始日志、检查点、后台进程日志 —— **除非**在核验身份或归因失败。
- 文件名、作业状态名、运行标签（`COMPLETE`、`RENDERED_NOT_SCIENTIFIC_VERDICT`、
  `COMPUTED_NOT_SCIENTIFIC_VERDICT`）**都不是**科学证据或完成证明。

## C. Authority and boundaries

**已授权**：Phase A 收尾链的监督与兜底、Phase B 回填、Phase C 建 memory 记录、
Phase E 派只读审计 agent。授权本体见对应 Protocol 与 `docs/execution_envelope.md`。

**未授权 —— 不得启动**：

- **后续训练范围由 researcher 拥有且尚未陈述**。收到明确陈述前：不臆测、不自行设计条件、
  **不提交任何 GPU 作业**。收到后先写一页范围说明（条件、种子、步数、资源规格、判据、
  完成合同、与现有 14 条件的关系）交 researcher 确认，再执行。
- 不 commit / 不 push / 不改 Graph / 不做外部同步，除非 researcher 明确指示。
- 不切 SPOT、不用多节点。
- 不干涉其他用户或其他任务的作业。不输出任何凭证或密钥。

**不得声称（研究者边界句，逐字保留，不得改写或解除）**：

> "这批模型适合观察'预训练模型局部微调中的结构变化'。固定八簇不能证明自然类别何时诞生，
> 也不能替代语义解释。审计末尾采集仍未齐全，尚不能交完整表征结论。"

**仍开着的人工决策**：① `sft_matrix_full_analysis_cn.md` 中若有【待填】占位，由产物回填，
**不得凭印象填数**；② 审计结论是否成立由 researcher 判定；③ Phase D 训练范围。
在 researcher 判定前，一切交付物标 `DRAFT_NOT_CANONICAL` / `PENDING_RESEARCHER`。

## D. Execution prerequisites

- **Profile / image**：`docs/execution_envelope.md` 的 `default_profile: h100-4-reserved`、
  `default_image: shphd-lite-0911`。**不要内联镜像 URL 或存储挂载**，按 key 引用。
- **提交入口**：`/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v1/scripts/sco_acp_compat.sh`，
  解析器 `./researchctl envelope`（**仅容器**），模板 `templates/execution/acp_submit_template.sh`。
  门：`DRY_RUN=0, ALLOW_SUBMIT=1, PROTOCOL_APPROVED=1, SMOKE_GATE_PASSED=1`。
  模板默认 `DRY_RUN=1`（只打印元组与命令）。
- **本收尾链是纯 CPU 路径**：`gpu_used: false`。**除训练新一批条件外，不要重提 4×H100 reserved。**
  预留节点的价值在核心数与不受容器回收影响。路由见 `execution_envelope.md` §3。
- **固定参数**：14 条件 = {task, sae_a, sae_b, gmm_a, gmm_b, high28_a, high28_b} × {F 冻结主干, U 只开放最后 attention}，
  每条件种子 17/29/43，512 更新 ⇒ 42 轨迹、882 检查点、1764 主分片、39 个 G1–G6 配对对比。
- **输出与回执**：结果落 `<run root>/analysis/`；提交回执按
  `templates/execution/run_receipt_template.md`，**缺展开镜像 URL 的回执不能证明跑过什么**。

## E. Action list — 按顺序；每步带分支

| # | Action | Verify | If pass | If fail |
|---|---|---|---|---|
| 0 | 读 B 段 1–11，**只回报阅读回执** | 列出实读文件、核验出的产物状态、与本文不一致处 | 进 1 | 停下报告 |
| 1 | 查收尾链状态 | `<run root>/postprocess_chain/*.done` ＋ `<run root>/acp/REMOTE_STATUS` | 有 `figures.done` → 4 | 无 → 2 |
| 2 | 判远端是否仍在推进 | `analysis/render_progress.json` 的 mtime/内容 ＋ `analysis/figures/G7/` 目录计数是否增长 | 在推进 → 3 | 停滞 → 3b |
| 3 | **什么都不做**，等待 | 远端在写同一输出目录 | 回到 1 | — |
| 3b | 本地兜底：`bash postprocess/complete_chain.sh` | 幂等、带 marker、自带 flock；自己会等收据 | 回到 1 | 远端确已 FAILED 且无收据 → `WORKERS=16 OMP_NUM_THREADS=1 bash postprocess/run_parallel_analyze.sh`（带续算，复用已算产物） |
| 4 | 回填 `sft_matrix_full_analysis_cn.md` 的【待填】 | 对照 `analysis/` **实际产物** | 核对 `analysis/postprocess/figures_manifest.json` 与 `figures/G7` 的 42 个轨迹目录 | 缺产物即报缺，不补数 |
| 5 | 按 C 段收官汇报 | 见 G 段 | 交付 | — |

**信号纪律（最容易踩的坑）**

1. **判完成只看 `*.done` 与 `acp/REMOTE_STATUS`，绝不看链日志里的"完成"字样。**
   `complete_chain.sh` 的 `step()` 记录 `FAIL` 但**不中止**。
2. **远端在推进时本地什么都不做**：远端正往同一目录写 render，并发会重复渲染、
   争用 8-CPU cgroup、可能损坏画廊。脚本自带 flock，仍以不并发为原则。
3. **接手前必须先确认上一会话的定时任务已停**。历史事故：会话内 cron `fc9038cb`
   会在"收据已出、链未跑完"时自动本地执行 `complete_chain.sh`，与接手方抢同一输出目录。
   `execution_envelope.md` §6 因此明令：**用受管后台作业监控，不要建会话内定时任务**。
   该 cron 已于 2026-09-10T12:41Z 停止；接手前仍需复认。
4. 一个 run root 只能有**一个** monitoring owner；接手即显式取得 owner 角色，
   前任先停轮询，并把 owner 记进回执。

## F. Current state

**Done**（各以其产物为证）

| 阶段 | 结果 | 位置 |
|---|---|---|
| 训练 | 42/42 轨迹 × 512 更新，882 检查点 + sidecar，身份失配 0 | `conditions/` |
| 提取 | 1764/1764 主分片（42×21×2），身份失配 0 | `representations/` |
| 分析 `fm analyze` | 由远端 pod `pt-qb1ffm7q` 完成，回执 10:50:45Z，641 s | `analysis/compute_receipt.json` |
| 离线 G8 十配置 | 本机独立完成，`OFFLINE_COMPUTED_WITH_TYPED_INSUFFICIENCY_NOT_SCIENTIFIC_VERDICT` | `offline_hierarchy/` |
| 本机测试 | 43/43 通过（需 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`） | `tests/` |
| 图族 fig01–fig07 | 162 文件 + 各家族 `method_cn.md`，全部 `DERIVED_NOT_SCIENTIFIC_VERDICT` | `analysis/postprocess/fig0*/` |
| 两个结果读面稿 | 四段式全维分析稿 ＋ 训练动态稿 | `daily_research_reports/0910/docs/` |

**Pending**：收尾链剩余阶段（render 画廊 → verify → finalize → splice → figures）；
`full_analysis` 的【待填】回填；Phase D 后续训练（范围未陈述）。

**必须继承、不要重新推翻的判断**

- 作业 `pt-uwfk144u` 的终态 `FAILED` **不是**训练/提取失败，而是 `fm/verify.py:44-47`
  期望 `update_SSSS.pt.json` 而 `fm/training.py:checkpoint_save` 实写 `update_SSSS.json`，
  导致 `found=-882` → `cmd_verify` 按设计非零退出。独立清点用真实命名重数：全在位。
- 该缺陷**冻结不就地修**：`source_hashes()` 覆盖 `fm/**/*.py`（及 `matrix.json`、`runtime.sh`、
  `vendor_provenance.json`、`acp_full.sh`、`README.md`），改一行即作废全部 42 条
  `run_identity.json`、1764 分片来源记录与教师目标清单。处置一律用 `fm/` 之外的后处理器。
- **pod 运行时绝不编辑实时 `fm` 代码**：集群 pod 经共享 `/data` 看到同一份文件；
  集群阶段一律从冻结快照 `$RUN/source/` 运行。

**已撤回的主张（不得复活）**

- 「单步 `train_nll` 大幅上升聚集在 update 261/356/447/462」—— 步间比值 std ≈ 0.09–0.12，
  +35–40% 上升约 3σ 噪声，**不可复现，已撤回**。趋势读数须用窗口均值/EMA。
- 「跨来源 mover 占比是独立期望的 0.35–0.43× ⇒ 显著不足」—— **已撤回**。正确读法：
  实测 0.56–0.74 对来源盲、簇大小感知的零假设 0.837，比值 0.67–0.89，且每条件仅
  20–31 条记录，**两个方向都不构成证据**。

**Live concurrency risk**：上一会话的会话内 cron `fc9038cb` 已于 2026-09-10T12:41Z 停止；
远端 `pt-qb1ffm7q` 可能仍在写 `<run root>/analysis/`。接手前复认 cron 已停、远端状态，
再决定是否兜底。

## G. Completion contract

**Deliverables**：收尾链至 `figures.done`；`full_analysis` 无【待填】；按 C 段边界的收官汇报；
（被要求时）canonical Summary/Detailed 草稿，标 `PENDING_RESEARCHER`。

**Done when**：每个决策性数字都能追到 `analysis/` 或 `conditions/` 的具体文件与字段；
收尾链 markers 齐备；未知项与需 researcher 决定的那**一个**问题被显式列出。

**复核时不得违反**（写进交付物）

1. 不得直接读 `analysis/clusters/<label>/<step>_h.npz` 的 `transition_from_previous`：
   它在**显示对齐空间**，对齐置换翻转会把稳定分区误报成大量流动；必须先做匈牙利重匹配，
   且结果只能标为**下界**。
2. 不得把跨主机（容器 ↔ pod）产物称为逐位相同：同主机重算逐位一致；容器 ↔ pod 只是数值等价
   （实测 `max|ΔS|=4.4e-16`、`max|ΔNLL|=6.7e-16`、`max|ΔD|=3.1e-33`），归因于主机级 BLAS GEMM 分发。
3. 不得把 39 个对比 × 21 个时刻中任一区间不跨零当作确认性发现：CI95 只覆盖记录抽样，
   **不含种子间训练方差**（u512 约 0.14 nats）。
4. t0 专家输出严格为 0（42/42 分片 `max|E|=max|shared|=0`），t0 归属在功能上是空转的。

**Stop and ask the researcher when**：Phase D 范围需要陈述；需要动 `fm/**`；需要
commit/push/发布；发现与 canonical 记录冲突。

**不得以"脚本已准备好""作业已提交""一个阶段已完成"作为结束。** 外部不可恢复阻塞时，
保留证据与恢复入口，写出真实未完成清单，标 `PARTIAL`，**不削减合同换 `COMPLETE`**。

## H. Reusable assets — 先复用，不要重写

| Asset | Path | Reuse for | Verified? |
|---|---|---|---|
| 执行前合同矩阵 | `daily_research_reports/0910/docs/sft_audit_matrix_v2.json` | 逐项判定清单 | 执行前合同，非现状 |
| 科学定义 owner | `daily_research_reports/0910/docs/sft_representation_audit_plan_cn.md` | 条件/教师/梯度/检查点/完成合同的定义 | 是 |
| 收尾链定义与缺陷归因 | `daily_research_reports/0910/docs/sft_matrix_postrun_analysis_plan_cn.md` | L1–L6、两个 `fm` 缺陷、12 项审计清单 | 是 |
| 两个结果读面 | `.../sft_matrix_full_analysis_cn.md`、`.../sft_matrix_training_dynamics_cn.md` | 直接引用，不重写结论 | 是（§5/§8 边界句逐字） |
| 审计入口 | `daily_research_reports/0910/docs/sft_audit_postrun_brief_cn.md` | 派只读审计 agent 的开场指令、八个攻击点 | 是 |
| 后处理器 | `<exec root>/postprocess/correct_verify.py`、`splice_coverage.py`、`parallel_analyze.py` | 绕开冻结的 `fm` 缺陷；带续算的分析 | 已在真实数据上跑通 |
| 只读探针 | `<exec root>/postprocess/probe_change_timing.py`、`probe_routing_churn.py` | 变化时机、路由改选的量化 | 是 |
| 图族代码 | `<exec root>/postprocess/figures/fig01…fig07*.py`、`common.py` | 复用坐标轴/配色/渲染（注意 `common.axis_limits()` 优先读 `analysis/global_axis_limits.json`） | 是；已修 5 个真实数据缺陷 |
| 运行身份与回执 | `<run root>/run_identity.json`、`analysis/compute_receipt.json` | 身份冻结值、分析回执 | 是 |
| 完成链本体 | `<exec root>/postprocess/complete_chain.sh` | 幂等、marker、flock 语义 | 是 |
| 提交模板与回执模板 | `templates/execution/acp_submit_template.sh`、`templates/execution/run_receipt_template.md` | 提交与回执 | 是 |
| 续接文件模板 | `templates/research_process/continuation_brief_template.md` | 写下一份续接文件 | 是 |
| 可离线复用的分析候选 | `sft_matrix_analysis_review_cn.md` 的 P1/P2 段 | **无需重训**即可推进的分析（教师约束是否进入路由、有效监督暴露与梯度统计、从输入变化到输出变化） | 标为 `AI 建议`，非决定 |

**规则**：本表任一项**不要重新实现或重新推导**，先读；复用前核验身份（hash/version/provenance）
并记录你引入的偏差；**本表是工具表，不是证据表** —— 证据资格由证据记录拥有。

**已知不可复用的东西（会误导）**

- `<run root>/panel_metadata.csv` 的 `index` 是数据集行号 0..8479；
  只有 `analysis/postprocess/panel_metadata.csv` 的 `index` 才是面板位置。
- `clusters/*.npz` 的 `transition_from_previous` 在显示对齐空间（见 G 段第 1 条）。
- 旧实验（A6R1 / 0909 离线 / A5）的模型与结果不能替代本轮。
