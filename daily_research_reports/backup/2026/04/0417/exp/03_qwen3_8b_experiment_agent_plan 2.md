# 真实表征空间与真实场景科研迭代执行计划

## 0. 文档定位

本文档是面向远程实验 agent 的执行计划，不是本地调研笔记。  
默认执行机器为远程 Linux 集群，默认工作仓库为：

`/data/250010109/spectral_router`

本轮所有新增实验内容统一放在：

`/data/250010109/spectral_router/exp_hierarchical`

本文档的任务是把当前研究主线转成可执行的远程实验计划，明确：
- 背景与研究主线；
- 本轮目的；
- 已经验证的结论；
- 三个实验环节的目标、输入、产物、门槛；
- 环境搭建要求；
- 集群运行命令文档的生成要求。

---

## 1. 背景与研究主线

### 1.1 全局研究主线

本研究的核心问题是：  
**为什么 Flat MoE 无法稳定学到 Zipfian long tail 结构，以及怎样的解耦式结构才能真正形成专家专业化。**

当前主线认为，传统 Flat MoE 的失败并非单一原因，而是两个物理瓶颈叠加：

1. **表示层的几何致盲**
   - 真实语言表征中存在共享的高频主方向；
   - 这些方向主导 hidden state 的大方差结构；
   - 稀有、细粒度、领域相关的 tail 语义被淹没在 shared head 中；
   - 因此 router 在 full hidden state 上难以看到真正用于专业化的信号。

2. **优化层的梯度饥饿**
   - 即便 tail 信号被正确暴露，如果 Common 与 Tail 共用统一 WD / LR；
   - tail 会因为激活稀疏、更新次数少而在训练中逐步死亡；
   - 统一 Weight Decay 会压低 tail 的稳态上限；
   - 全局 LR decay 会过早关闭 tail 的学习窗口。

这条主线最终指向同一个结构结论：

> **真正的专业化必须同时做表示解耦、结构解耦和优化解耦。**

### 1.2 我们当前的目的

toy 阶段已经结束。  
本轮科研迭代的目标，不是继续做 toy 变体，而是：

> **进入真实表征空间和真实训练场景，检验我们的理论与方法是否成立。**

具体来说，本轮需要回答三件事：

1. 在真实大模型 hidden state 中，shared head 是否真实存在；
2. 切掉 shared head 后，tail residual 是否真的更有利于语义分发；
3. 在真实训练中，分支解耦与优化解耦是否能稳定保住 rare / domain-specific 知识。

### 1.3 已经验证的结论

当前已经在 toy model 级别验证了以下结论：

1. **命题 A：Mean-centering 不够，必须切 shared high-variance head**
   - 单纯去均值不能从根本上释放 tail 语义；
   - 真正有效的是切除协方差谱中的共享高方差方向。

2. **命题 B：残差空间可能依然包含局部共享结构**
   - 全局切 head 之后，局部 coarse group 内仍可能存在 local nuisance；
   - 这为后续层级式架构提供了必要性。

3. **命题 C：Tail 必须拥有独立优化条件**
   - 统一 WD + 全局 LR decay 会让 tail 死亡；
   - 只改 WD 或只改 LR 都只能部分救援；
   - Common / Tail 物理拆分 + Tail 独立低 WD + 持久 LR，才能显著恢复 tail。

因此，本轮不是从零开始探索，而是要把 toy 级结论搬到真实模型中，完成从“理论正确”到“真实场景有效”的迁移验证。

---

## 2. 远程资源与固定路径

### 2.1 模型路径

本轮固定测试两个模型：

- `Qwen3-8B`
  - `/data/share/Qwen3-8B`
- `Qwen3.5-9B`
  - `/data/share/Qwen3.5-9B`

### 2.2 数据路径

本轮固定使用两类数据：

- WoS：
  - `/data/share/109_cache_dir/hf_data/datasets/river-martin___web-of-science-with-label-texts`
- DCLM：
  - `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`

本轮默认语义角色划分为：
- `DCLM`：Common / 通用分布侧
- `WoS`：Tail / 领域语义侧

### 2.3 仓库工作目录

实验 agent 必须进入：

`/data/250010109/spectral_router/exp_hierarchical`

并在其中组织本轮的全部内容。

---

## 3. 目录组织要求

本轮有三个实验环节，每个环节都必须有独立子文件夹。  
每个环节都必须至少包含：
- `data/`
- `scripts/`
- `results/`
- `docs/`

推荐目录结构如下：

```text
/data/250010109/spectral_router/exp_hierarchical/
  README.md
  docs/
    overall_plan.md
    environment.md
    acp_run_phase1.md
    acp_run_phase2.md
    acp_run_phase3.md
    blockers.md
  env/
    environment.yml
    requirements.txt
    install.sh
  phase1_real_representation_probe/
    data/
    scripts/
    results/
    docs/
  phase2_split_ffn_decoupling/
    data/
    scripts/
    results/
    docs/
  phase3_hierarchical_moe/
    data/
    scripts/
    results/
    docs/
```

要求：
- 所有脚本必须放在对应阶段的 `scripts/`
- 所有阶段总结必须放在对应阶段的 `docs/summary.md`
- 全局阻塞项统一记录到：
  - `/data/250010109/spectral_router/exp_hierarchical/docs/blockers.md`

---

## 4. 本轮执行原则

### 4.1 单变量推进

本轮必须严格按以下顺序推进：

1. 先做真实表征诊断
2. 再做无路由 split-FFN 解耦
3. 最后做 Hierarchical MoE

禁止把 projector、split-FFN、router、experts、optimizer 一起改完再汇报。  
每一阶段都只能在上一阶段已经形成正结论后再推进。

### 4.2 双模型策略

本轮有两个模型，但不要求一开始两个模型同步做完整闭环。  
推荐执行策略是：

1. 先在 `Qwen3-8B` 上跑完整的 `Phase 1`
2. 若 `Phase 1` 结论清晰，再在 `Qwen3.5-9B` 上复现 `Phase 1`
3. `Phase 2 / 3` 优先从 `Qwen3-8B` 启动
4. 若 `Qwen3-8B` 上结论成立，再扩展到 `Qwen3.5-9B`

原因：
- 本轮最大的未知量是“真实表征解耦是否成立”
- 不是“多模型多配置一开始一起跑得越多越好”

### 4.3 输出优先级

实验 agent 的输出优先级为：

1. 数值表
2. 图
3. 文字结论

若图和数值冲突，以数值表和原始日志为准。

---

## 5. 预备环节：环境搭建与运行文档

这一环节不是三大实验阶段之一，但必须优先完成。  
若环境不稳定，后续实验结果无意义。

### 5.1 环境目标

需要创建一个更纯净的大模型训练环境，满足：
- 能运行大模型前向与训练；
- 能运行 `lm_eval`；
- PyTorch 版本不要太新；
- 包依赖尽量收敛，避免历史环境污染。

### 5.2 环境建议

建议环境基线：
- Python `3.10`
- PyTorch `2.1.x`
- CUDA 版本与远程机器驱动兼容

环境中至少应覆盖以下包族：
- `torch`
- `transformers`
- `accelerate`
- `datasets`
- `tokenizers`
- `sentencepiece`
- `safetensors`
- `scikit-learn`
- `scipy`
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `pyarrow`
- `lm_eval`
- 若仓库训练代码需要：
  - `deepspeed`
  - `flash-attn`
  - `peft`
  - `einops`
  - `wandb`

说明：
- 本计划只规定环境目标与版本边界；
- 具体安装方式可以是 `conda + pip`，也可以是已有集群标准方案；
- 但最终必须沉淀为：
  - `env/environment.yml`
  - `env/requirements.txt`
  - `env/install.sh`

### 5.3 lm_eval 任务集

你提到“lm_eval 测试项目设置为如图”，但当前文本上下文中没有该图片内容。  
因此，本计划做如下硬性要求：

1. 实验 agent **不得自行猜测** `lm_eval` 任务集合；
2. 必须把任务集合记录到：
   - `/data/250010109/spectral_router/exp_hierarchical/docs/environment.md`
3. 若 agent 无法从用户提供图片、已有配置文件或上游文档中恢复完整任务列表，则必须停止这一步，并在 `blockers.md` 中记录：
   - 缺失项：`lm_eval task list`
   - 状态：`blocked`

### 5.4 ACP 运行命令文档

需要生成与以下参考文档风格一致的运行命令文档：

`/data/250010109/spectral_router/docs/quadratic_low_rank/acp_run.md`

新文档保存到：

`/data/250010109/spectral_router/exp_hierarchical/docs`

至少需要生成：
- `acp_run_phase1.md`
- `acp_run_phase2.md`
- `acp_run_phase3.md`

要求：
- 命令结构、文档风格、集群提交流程应参考上游 `acp_run.md`
- 但不得硬抄无关参数
- 必须根据本轮阶段对应的脚本与目录改写
- 若 agent 无法读取参考文档，则必须在 `blockers.md` 中记录并停止该步骤

---

## 6. Phase 1：真实表征空间诊断

### 6.1 目标

验证以下命题在真实大模型上是否成立：

> 在真实 hidden state 中，存在 shared head 主导的高方差结构；切除该结构后，tail residual 更适合承载领域语义与路由语义。

### 6.2 输入

模型：
- `/data/share/Qwen3-8B`
- `/data/share/Qwen3.5-9B`

数据：
- WoS：`/data/share/109_cache_dir/hf_data/datasets/river-martin___web-of-science-with-label-texts`
- DCLM：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`

### 6.3 默认设定

- hidden state 位置：`post-attention / pre-FFN`
- DCLM 用作 common 统计池
- WoS 用作 tail/domain probe 数据
- 协方差估计默认 `DCLM:WoS = 4:1`
- 首轮扫描 4 个代表性层位
- 首轮扫描 $k \in \{4, 8, 16, 32, 64\}$
- 若 explained variance 不足，再补 $\{96, 128\}$

### 6.4 实验问题

本阶段必须回答：

1. hidden state 的协方差谱是否呈现 head-heavy 结构？
2. `raw`、`centered`、`tail residual` 三种空间中，哪一种对 WoS 领域标签最友好？
3. 是否存在相对稳定的最佳层位和最佳 $k$？

### 6.5 执行步骤

1. 在两个模型上分别准备 WoS 与 DCLM 数据入口。
2. 对选定层位提取 hidden states。
3. 用混合 token 池估计每层的 $\mu$ 与 $\Sigma$。
4. 对每个 $k$ 构造：
   - `raw`
   - `centered`
   - `tail = (I - V_kV_k^T)(h - mu)`
5. 用 WoS 领域标签做文档级或 token 级 probe / router 代理评估。
6. 统计：
   - eigenspectrum
   - explained variance
   - probe accuracy
   - purity / NMI
   - $\mathrm{Sep}_F$（若代码实现方便）
7. 选出最佳层与最佳 $k`，并形成阶段总结。

### 6.6 产物要求

`phase1_real_representation_probe/` 下必须形成：

- `scripts/`
  - hidden state 提取脚本
  - 协方差 / SVD 脚本
  - probe / router 评估脚本
- `results/`
  - layer-k 指标表
  - eigenspectrum 数据
  - probe / router 结果表
  - 图
- `docs/summary.md`
  - 回答是否存在 shared head
  - 最优层位
  - 最优 $k$
  - `tail residual` 是否优于 `centered`

### 6.7 通过门槛

只有在以下条件满足时，才能进入 `Phase 2`：

1. 至少一个模型上存在清晰的 head-heavy 谱结构；
2. 至少一个层位和一个 $k$ 上，`tail residual` 相比 `centered` 在 probe / purity / NMI 上稳定更优；
3. 该结论不是单个 seed 的偶然结果；
4. 最优层与最优 $k$ 可以被明确写入阶段总结。

若不满足，则本轮实验优先继续打磨表征定义，不进入 `Phase 2`。

---

## 7. Phase 2：无路由 Split-FFN 解耦验证

### 7.1 目标

在真实训练中验证：

> 即便先不引入专家路由，只做 common / tail 分支拆分，并给 tail 独立 WD / LR，是否已经能改善 rare / domain-specific 表现。

### 7.2 进入条件

必须先完成 `Phase 1`，并拿到：
- 至少一个正结论模型
- 一个最佳层位
- 一个最佳 $k$

### 7.3 默认策略

- 优先在 `Qwen3-8B` 上执行
- backbone 默认冻结或尽量少改动
- 只改造 `Phase 1` 选出的一个关键层位
- projector 先固定，不在线更新

### 7.4 对比配置

1. `Baseline FFN`
2. `Split-FFN / coupled-optim`
3. `Split-FFN / decoupled-optim`

### 7.5 关键问题

本阶段要判断：

1. 分支化本身是否足够；
2. 优化解耦是否必要；
3. rare / domain-specific 指标改善时，common 指标是否稳定。

### 7.6 数据角色

- DCLM：保持通用分布约束
- WoS：提供领域 / tail 语义验证

训练时可采用混合数据流，但必须在阶段文档中明确记录：
- 混合比例
- 采样策略
- batch 构成

### 7.7 产物要求

`phase2_split_ffn_decoupling/` 下必须形成：

- `scripts/`
  - 数据混合与 dataloader 脚本
  - split-FFN 训练脚本
  - 评估脚本
- `results/`
  - ppl 表
  - rare / domain-specific 指标表
  - 参数范数 / 更新统计
- `docs/summary.md`
  - 是否仅分支化就够
  - 优化解耦是否必要
  - 是否允许进入 `Phase 3`

### 7.8 通过门槛

只有在以下条件满足时，才允许进入 `Phase 3`：

1. `Split-FFN / decoupled-optim` 明显优于 baseline 与 coupled 版本；
2. 改善主要集中在 rare / domain-specific 指标，而不是靠牺牲通用性能换来；
3. tail 分支的更新与参数生存状态显著优于 coupled 版本。

---

## 8. Phase 3：Hierarchical MoE 验证

### 8.1 目标

在真实结构中验证最终命题：

> router 应工作在 `h_tail` 上，而不是 raw hidden state 上；同时 tail experts 必须拥有独立 WD / LR。

### 8.2 进入条件

只有当 `Phase 2` 已明确支持“优化解耦有效”时，才允许执行本阶段。

### 8.3 默认策略

- 优先从 `Qwen3-8B` 启动
- 只在 `Phase 1 / 2` 已确认的 1 到 2 个关键层插入 Hierarchical MoE
- common path 保持 dense
- tail path 接收 `h_tail`
- tail experts 默认从小规模开始

### 8.4 对比配置

1. `Flat MoE / raw router / uniform WD+LR`
2. `Tail-router only`
3. `Tail-router + decoupled WD`
4. `Tail-router + decoupled WD + decoupled LR`

### 8.5 关键问题

本阶段必须判断：

1. 在 `h_tail` 上 routing 是否让语义纯度更高；
2. rare / domain-specific ppl 是否下降；
3. tail experts 的存活是否更健康；
4. 是否形成真正的 specialization，而不是只做了结构重参数化。

### 8.6 产物要求

`phase3_hierarchical_moe/` 下必须形成：

- `scripts/`
  - 层级式 MoE 训练脚本
  - 路由分析脚本
  - expert 动力学分析脚本
- `results/`
  - router purity / NMI
  - ppl
  - expert occupancy
  - expert survival
- `docs/summary.md`
  - 是否闭合主线
  - 是否支持后续更大规模推进

### 8.7 通过门槛

本阶段判为成功，需要同时满足：

1. Hierarchical 配置在 purity / NMI 上优于 flat 对照；
2. rare / domain-specific 指标优于 flat 对照；
3. tail expert 生存状态优于 flat 对照；
4. common 侧性能未明显崩塌。

---

## 9. 文档与运行命令的硬性要求

### 9.1 每个阶段必须有总结文档

每个阶段结束后，必须产出：

- `docs/summary.md`

格式至少包含：

```text
Question:
Setup:
Model:
Data:
Best layer:
Best k:
Main metrics:
Conclusion:
Passed:
Next action:
Risks:
```

### 9.2 每个阶段必须有 ACP 运行命令文档

每个阶段都必须形成与集群运行相匹配的命令文档：

- `docs/acp_run_phase1.md`
- `docs/acp_run_phase2.md`
- `docs/acp_run_phase3.md`

这些文档必须参考：

`/data/250010109/spectral_router/docs/quadratic_low_rank/acp_run.md`

要求：
- 采用相近的文档风格；
- 保留集群提交逻辑；
- 根据本阶段脚本、目录、模型、数据路径改写；
- 明确日志目录、输出目录、resume 策略；
- 若无法读取上游文档，则必须在 `blockers.md` 中记录并暂停该步骤。

### 9.3 所有阻塞项必须显式记录

以下情况都不能静默跳过：
- 无法确定 lm_eval 任务集
- 无法读取参考 `acp_run.md`
- 模型路径不通
- 数据路径不通
- 环境安装冲突

这些问题必须写入：

`/data/250010109/spectral_router/exp_hierarchical/docs/blockers.md`

---

## 10. 本轮最低完成标准

本轮最低完成标准不是三阶段全部跑完，而是：

1. 完成远程环境搭建文档与依赖沉淀
2. 完成 `Phase 1`
3. 若 `Phase 1` 结论足够强，则进入 `Phase 2` 的最小实现
4. 同时生成对应的 ACP 运行命令文档

也就是说，本轮最重要的闭环是：

> **证明在真实大模型表征中，shared head -> tail residual 的主线是否成立。**

如果这一点都还不成立，就不应急着推进完整 Hierarchical MoE。

---

## 11. 一句话执行指令

**进入 `/data/250010109/spectral_router/exp_hierarchical`，先完成环境搭建与运行文档沉淀，再用 `Qwen3-8B` 和 `Qwen3.5-9B` 在 `DCLM + WoS` 上做真实表征诊断；只有当 `tail residual` 的优势被稳定验证后，才进入 split-FFN 与 Hierarchical MoE。**
