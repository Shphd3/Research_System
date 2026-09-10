# SFT 矩阵 · 跨对话交接包（可粘贴 Prompt ＋ 资料清单）

日期：2026-09-10。性质：**交接材料，非证据本体**。本文只负责把已完成的工作、未完成的工作、红线与读面完整交给下一位 agent；不含新的科学结论，不改变任何 canonical 记录，不代替 researcher 的科学判断。

交接发起方：DeepSeek via Claude（harness: Claude Code；model: unknown）
交接对象：新开的对话
执行根：`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`
运行根：`runs/full-20260909T203104Z/`
仓库根：`/data/250010109/Research_System/`

---

## §0 研究者用法（三步）

1. 新开一个对话（模型 DeepSeek V4.1 flash 即可，本任务不需要长上下文以外的特殊能力）。
2. 把 **§3 的整段代码块**贴进去，作为第一条消息。
3. **处理本会话遗留的定时任务**：本会话有一个会话内 cron（id `fc9038cb`，每小时 :11 与 :41 触发）在监督同一条远端链，且其第 4 步会在"收据已出但链未跑完"时**自动在本地执行 `complete_chain.sh`**。若新对话接手监督，请先让本会话停止该 cron，避免两个 agent 同时动手（远端正在往同一输出目录写 `render`）。

---

## §1 交接时的状态快照（事实基线，2026-09-10T12:33Z）

**已完成**

| 阶段 | 结果 | 位置 |
|---|---|---|
| 训练 | 42/42 轨迹 × 512 更新，882 检查点 + sidecar，身份失配 0 | `conditions/` |
| 提取 | 1764/1764 主分片（42×21×2），身份失配 0 | `representations/` |
| 分析（`fm analyze`） | 已由远端 pod 完成，回执 10:50:45Z，641 s | `analysis/compute_receipt.json` |
| 离线 G8 十配置 | 本机独立完成 | `offline_hierarchy/` |
| 本机测试 | 43/43 通过（需 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`） | `tests/` |
| 图族 fig01–fig07 | 162 文件 + 各家族 `method_cn.md` | `analysis/postprocess/fig0*/` |
| 两个结果读面稿 | 四段式全维分析稿 + 训练动态稿 | `daily_research_reports/0910/docs/` |
| 审计入口 | 审计阅读清单与攻击面 | `daily_research_reports/0910/docs/sft_audit_postrun_brief_cn.md` |

**正在运行**

- 远端 ACP 作业 **`pt-qb1ffm7q`** 上的完成链正在 `fm render` 的 G7 画廊阶段。12:33Z 时 `analysis/figures/G7/` 有 **20/42** 个轨迹目录，`analysis/render_progress.json` 每 1–3 分钟更新一次，当前轨迹 `sae_b_f__seed29`。按此速率剩余约 1 小时完成画廊，其后自动进入 verify → correct_verify(deep) → finalize → splice_coverage → figures。
- 链的标记写在 `runs/full-20260909T203104Z/postprocess_chain/<name>.done`；**当前该目录只有 `complete_chain.log`，没有任何 `.done`**。

**尚未完成**

1. 远端完成链剩余阶段（render 剩余画廊 → verify → finalize → splice → figures）。判定规则见 §3 的红线段。
2. `sft_matrix_full_analysis_cn.md` 中若有【待填】占位，需按实际产物回填。
3. 后续训练 —— **范围由 researcher 拥有，尚未陈述**（见 §3 的 Phase D）。

**已知的、必须继承的判断（不要重新推翻）**

- 作业 `pt-uwfk144u` 的终态 `FAILED` **不是训练或提取失败**，而是 `fm/verify.py:44-47` 期望的 sidecar 命名（`update_SSSS.pt.json`）与 `fm/training.py:checkpoint_save` 实际写出的（`update_SSSS.json`）不符，导致训练段 `found=-882` → `cmd_verify` 按设计非零退出。独立清点已用真实命名重数：882/882、42/42、1764/1764 全在位。
- 该缺陷**冻结不就地修**：`source_hashes()` 覆盖 `fm/**/*.py`，改一行即作废全部 42 条 `run_identity.json` 与教师目标清单。处置方式是在 `fm/` 之外写后处理器（`postprocess/correct_verify.py`、`postprocess/splice_coverage.py`）。
- 不要重复提交 4×H100 reserved 节点，除非要训练**新的一批条件**。本轮分析全部是 CPU 数值计算，4 张 H100 从未被使用；预留节点的价值只在 192 vCPU 与不受容器回收影响。

---

## §2 需要阅读的相关资料

### A. 必读（按顺序，不读会踩坑）

| # | 路径（相对仓库根，除注明外） | 为什么必须读 |
|---|---|---|
| 1 | `AGENTS.md` ＋ `CLAUDE.md` | 仓库治理：科学不变量、状态归属、审批边界、Skill 路由 |
| 2 | 按 description 匹配后加载 `.agents/skills/` 下的 SKILL.md：`research-progress-core`、`experiment-card-writer`、`research-memory`、`remote-experiment-workflow` | 结果写作与收尾的完成合同；memory 合约；远端工作流 |
| 3 | `.research/memory/conversations/0910-sft-matrix-execution/memory.md`（**读全文**，最新条目＝当前状态） | 上一对话的累积工作上下文。**非 canonical**：可据它知道发生过什么，不可据它取得科学权威 |
| 4 | `daily_research_reports/0910/docs/sft_matrix_postrun_analysis_plan_cn.md` | 收尾链 L1–L6 的定义、两个 `fm` 缺陷的完整归因、12 项审计清单、§10 交接 Prompt |
| 5 | `daily_research_reports/0910/docs/sft_representation_audit_plan_cn.md` | **本实验的科学定义 owner**：14 条件、教师定义、梯度范围、检查点合同、完成合同 |
| 6 | `daily_research_reports/0910/docs/sft_matrix_full_analysis_cn.md` | 全维分析读面（四段式）；§5 含研究者边界的**逐字原句** |
| 7 | `daily_research_reports/0910/docs/sft_matrix_training_dynamics_cn.md` | 「训练中的剧烈变化」读面：五通道表、时间表、训练结果表 |
| 8 | `daily_research_reports/0909/docs/0909_组会逐句校订稿_含原文对照.md` | 导师提问的原始语境（09:05 / 09:35 / 10:36 / 14:52）；判断"我们答的是不是被问的问题" |
| 9 | `daily_research_reports/0910/docs/sft_audit_postrun_brief_cn.md` | 若新对话要接着做审计：五层阅读顺序、断言→产物对照、八个攻击点、可粘贴的审计开场指令 |
| 10 | 执行根 `README.md`、`matrix.json` | 阶段表、14 条件 × 3 种子的执行清单、39 个对比定义 |
| 11 | `PROJECTS.md`；A15 当前 Focus 与 Anchor | 只在需要判断科学归属或要改动已注册问题时读，且**只读不推断** |
| 12 | `runs/full-20260909T203104Z/run_identity.json`、`analysis/compute_receipt.json`、`postprocess/complete_chain.sh` | 身份冻结值、分析回执、完成链本体（含 marker 与 flock 语义） |

### B. 按需读（只在对应问题出现时）

- `sft_audit_matrix_v2.json` / `sft_audit_agent_handoff_cn.md` / `sft_audit_sources_cn.md`：**2026-09-09 的执行前**合同。只能当"逐项判定"的清单用，不能当现状依据。
- `sft_matrix_analysis_review_cn.md`：2026-09-10 上午的中间评估与修正建议（P1/P2 分析优先级）。
- `sae_hierarchy_offline_extension_cn.md`：十配置离线的定义。
- `postprocess/` 下探针与图脚本：`probe_change_timing.py`、`probe_routing_churn.py`、`figures/fig01…fig07*.py`、`common.py`、`correct_verify.py`、`splice_coverage.py`、`parallel_analyze.py`。
- `sae_relations_explained_cn.md`：分不清原子/层级/输入聚类/路由/专家输出时读。

### C. 不要读，或读了也不得作证据

- 对话 memory 里的数字与判断（非 canonical；科学判决只在 Focus / Anchor / Protocol / Summary / Detailed 上）。
- 旧实验（A6R1、0909 离线、A5）的结果——它们不能替代本轮的证据。
- 原始日志、检查点、后台进程日志——**除非**在核验身份或归因失败。
- 不得把文件名、作业状态名、运行标签（`COMPLETE`、`RENDERED_NOT_SCIENTIFIC_VERDICT`、`COMPUTED_NOT_SCIENTIFIC_VERDICT`）当作科学证据或完成证明。

---

## §3 可粘贴 Prompt（整段复制给新对话）

```text
# 角色

你是这个研究任务的新主 agent，接手一个**已完成绝大部分、只差收尾**的 SFT 路由表示全矩阵实验，并在 researcher 陈述训练范围后接续后续工作。你没有上文上下文，以下内容与 §2 列出的文件是你全部的起点。

# 工作位置与环境

- 仓库根（治理/文档/memory）：/data/250010109/Research_System/
- 执行根（代码/合同/后处理）：/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/
- 运行根（全部证据）：<执行根>/runs/full-20260909T203104Z/
- 本机是容器：cgroup 约 8 CPU，/data 是网络挂载（quarkfs_client）因而在容器回收中存活；/root 会在回收时丢失，字体等资源必须放 <执行根>/postprocess/fonts/。容器大约每 4 小时被回收一次——长 CPU 任务必须放远端 pod 或带续算。
- 本机跑 python 需要前缀：PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# 第 0 步：先读、先核验，不要先动手

按 §2-A 的顺序读完必读项（1–12）。读 `0910-sft-matrix-execution/memory.md` 全文（最新条目＝当前状态）。然后**只回报**一份简短阅读回执：你实际读了哪些文件、你核验出的当前状态（哪些产物已存在、完成链跑到哪一步）、以及任何与本文不一致之处。不要在这一步写文件、不要提交作业。

# 不可越界的红线（违反其中任何一条都会造成不可逆损失）

1. **绝不修改 `fm/**` 下的任何源文件。** `source_hashes()` 覆盖 `fm/**/*.py` 及 matrix.json、runtime.sh、vendor_provenance.json、acp_full.sh、README.md。改任何一行会当场作废全部 42 条 run_identity.json、1764 个分片的来源记录与教师目标清单。验证器的缺陷一律用 `fm/` 之外的独立后处理器解决（已有 `postprocess/correct_verify.py` 与 `postprocess/splice_coverage.py` 为先例）。
2. **pod 运行时绝不编辑实时 fm 代码**：集群 pod 通过共享 /data 看到同一份文件。集群阶段一律从冻结快照 `$RUN/source/` 运行。
3. **不 commit / 不 push / 不改 Graph / 不做外部同步**，除非 researcher 明确指示。不得把产物提升进 research mainline。
4. **不输出任何凭证或密钥。** 不干涉其他用户或其他任务的作业。不切 SPOT、不用多节点；本轮资源规格是 SCO ACP 单节点 `n6ls.iu.i40.4`、4×H100、reserved、normal，仅在训练新一批条件时才需要。
5. **不得把文件名、作业状态、训练集损失、诊断图当科学证据。** `Unknown` 是合法状态。不得代 researcher 解除其科学边界、不得替 researcher 宣告科学结论或下一步决定。
6. **尚未公开的边界（逐字保留，不得改写或解除）**：
   > "这批模型适合观察'预训练模型局部微调中的结构变化'。固定八簇不能证明自然类别何时诞生，也不能替代语义解释。审计末尾采集仍未齐全，尚不能交完整表征结论。"

# 科学背景（只读到能做事的程度，全部定义以 §2-A 第 5 项为准）

矩阵为 14 条件 = {task, sae_a, sae_b, gmm_a, gmm_b, high28_a, high28_b} × {F 冻结全部主干, U 只开放最后 attention}，每条件 3 个种子（17/29/43）× 512 更新，共 42 条轨迹、882 检查点、1764 个 dev/test 主分片、39 个 G1–G6 配对对比。结构梯度只更新 router；教师冻结；F/U 面对同一套共同 t0 教师目标。本实验服务的研究问题是「局部 SFT 中，在不同教师约束与不同注意力可训练状态下，表示、路由和输出怎样变化」。

# Phase A：接续并完成远端完成链（最高优先级，先做）

远端 ACP 作业 `pt-qb1ffm7q` 上正在跑 `postprocess/complete_chain.sh`，当前处于 `fm render` 的 G7 画廊阶段（交接时 20/42 个轨迹目录，`analysis/render_progress.json` 每 1–3 分钟更新）。链的步骤是：render → verify --lenient → correct_verify(deep) → finalize → splice_coverage → figures。

判定与操作规则：

1. **判完成只看 `<run>/postprocess_chain/*.done` 与 `<run>/acp/REMOTE_STATUS`，绝不看链日志里的"完成"字样。** `complete_chain.sh` 的 `step()` 记录 `FAIL` 但**不中止**，日志里出现 FAIL 不等于链已停。
2. **判远端是否仍在推进**：看 `analysis/render_progress.json` 的 mtime 与内容、`analysis/figures/G7/` 的目录计数是否继续增长。
3. **远端在推进时，本地什么都不要做。** 尤其不要本地执行 `complete_chain.sh`：远端正在往同一输出目录写 render（重复渲染、8-CPU cgroup 争用、画廊可能损坏）。脚本自带 flock，但仍以不并发为原则。
4. **仅当远端停滞**（`render_progress.json` 长时间不更新且 G7 目录计数不变）时才在本地兜底：`bash postprocess/complete_chain.sh`（幂等、带 marker、可安全重启；它自己会等待收据）。若远端作业确已 FAILED 且无收据，用 `WORKERS=16 OMP_NUM_THREADS=1 bash postprocess/run_parallel_analyze.sh` 带续算重启（会复用已算产物）。
5. 该链是纯 CPU 路径，不需要 GPU。

# Phase B：回填与结果读面

链跑完后：

1. 检查 `daily_research_reports/0910/docs/sft_matrix_full_analysis_cn.md` 中是否仍有【待填】占位；有则按 `analysis/` 实际产物回填，**不得凭印象填数**。
2. 核对 `analysis/postprocess/figures_manifest.json` 与 `figures/G7` 的完整性（42 个轨迹目录）。
3. 若产生新的量化结论，按 experiment-card-writer 的四段式（Purpose / Hypothesis / Analysis method / Conclusion）写，并区分直接结果、观测、解释、主张、限制、决定。
4. **任何科学结论必须经 researcher 确认后才能写入 canonical Summary。** 在确认之前，交付物一律标注 `DRAFT_NOT_CANONICAL` / `PENDING_RESEARCHER`。

# Phase C：建立本对话自己的 memory 记录

按 `.agents/skills/research-memory` 的合约（先完整读 `references/memory_contract.md`）：

- 在 `.research/memory/conversations/<本对话名>/memory.md` **新建**一条记录，`Continues from: .research/memory/conversations/0910-sft-matrix-execution/memory.md`。
- 目录名由本对话的真实标题推导；**绝不覆盖**上一对话的 `memory.md`。
- 记 `Processed by: DeepSeek via Claude (harness: Claude Code; model: <仅在确证时写模型，否则 unknown>)`。
- 条目只写 resume 所需：当前目标、当前工作、下一步动作、最小引用集合。不要塞代码、diff、日志、完整表格或凭证。

# Phase D：后续训练（范围由 researcher 拥有，未确认时不要启动）

researcher 已表示要"接续后续的训练"，但**具体范围尚未陈述**。在收到明确陈述之前：

- 不要臆测、不要自行设计训练条件、不要提交任何 GPU 作业。
- 收到陈述后，先把它对照 §2-A 第 5 项的 v2 主计划与 A15 的 Focus/Anchor，写出一页范围说明（条件、种子、步数、资源规格、判据、完成合同、与现有 14 条件的关系），交 researcher 确认后再执行。
- 已记录的历史约束：结构梯度只更新 router；教师冻结；共用固定 t0；保留原始单条件目录；不做跨条件 all-reduce；**所有新代码必须放在 `fm/` 之外**（允许只读导入 fm 模块）。
- 已知不需要重训的候选工作（若 researcher 只想推进分析，可据此建议，但**标为 AI 建议而非决定**）：教师约束是否真正进入路由的测量、有效监督暴露与梯度统计、从输入变化推进到输出变化的测量——这些都可复用已有产物，无需重训。详见 `sft_matrix_analysis_review_cn.md` 的 P1/P2 段。

# Phase E：若需要独立审计

`daily_research_reports/0910/docs/sft_audit_postrun_brief_cn.md` 是给审计方的入口：五层阅读顺序、断言→产物对照表、八个攻击点、以及可整段复制给审计 agent 的开场指令。可直接按它派一个只读审计 agent。

# 复查与交付标准

1. 每一个决策性数字都能追到 `analysis/` 或 `conditions/` 的具体文件与字段。
2. 复核时不得直接读 `analysis/clusters/<label>/<step>_h.npz` 的 `transition_from_previous`：它存在于**显示对齐空间**，对齐置换翻转会把稳定分区误报成大量流动；必须先做匈牙利重匹配，且结果只能标为**下界**。
3. 不得把跨主机（容器 ↔ pod）产物称为逐位相同：同主机重算是逐位一致，容器与 pod 之间只是数值等价（实测 1e-16 量级），归因于主机级 BLAS GEMM 分发差异。
4. 不得把 39 个对比 × 21 个时刻中的任意一个区间不跨零当作确认性发现；CI95 只覆盖记录抽样，不含种子间训练方差（种子间在 u512 约 0.14 nats）。
5. 完成后按顺序回报：Phase A 的结局（哪些 `.done` 存在、REMOTE_STATUS 内容）、Phase B 的回填清单、当前显式未知项、以及需要 researcher 决定的那一个问题。
6. **不要以"脚本已准备好""作业已提交""一个阶段已完成"作为结束。** 外部不可恢复阻塞时，保留证据与恢复入口，写出真实的未完成清单，标 PARTIAL，不削减合同来换取 COMPLETE。

# 语言

对话用中文，canonical 研究产物用英文，中文伴随件用 `_cn.md`。
```

---

## §4 边界声明

本文是交接材料，不是证据源，也不构成科学判决。§1 的状态快照来自 2026-09-10T12:33Z 的直接文件清点；之后的状态以产物本身为准。任何 claim boundary 与下一步科学决定仍由 researcher 拥有；新 agent 不得据本文加重任何结论。
