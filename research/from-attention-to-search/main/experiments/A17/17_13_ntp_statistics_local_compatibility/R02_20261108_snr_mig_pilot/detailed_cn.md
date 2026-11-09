# R02 详细记录：一步更新均值项／噪声项分解

[Summary](summary_cn.md) · [执行契约](protocol_cn.md)

执行根目录：`/data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/`（下文路径均相对于此）。代码、原始行表与证据都在执行侧，本页不复制原始数据。

## 1. 复用说明

读过 `docs/training_reuse_index.md` 与 `docs/training_observability_contract.md`。本轮不是训练（无优化器状态、无多步），TensorBoard 契约不适用。

- **复用：**S15 `collect_routes.py` 的模型／SAE 加载与 hook 约定（DenseAlignedMoE、TopKSAE，fp32，TF32 关闭）。
- **改造：**A15_05_04 `e01.py` 的“快照→一步 SGD→精确恢复”与浮点读出。改动：在 float64 中只重算 block-7 expert e 之后的尾部。因为只有 block-7 的一个 expert 改变，而它位于本层 router 之后，原生路由与 load bias 不受影响，无须路由回放。
- **不复用：**训练器、优化器与数据流代码。

## 2. 任务 A：资产与测速

| 项 | 实测 |
|---|---|
| GPU | NVIDIA H100 80GB HBM3 MIG 3g.40gb，可用 39.5 GiB（`nvidia-smi -L`：`MIG 3g.40gb Device 0`） |
| checkpoint 顶层键 | checkpoint_schema_version, model, optimizer, scheduler, optimizer_step=125894, tokens_seen=33e9, epoch=1, batch_in_epoch=11462, parallel, extra_training_state；RNG 在同目录 `rng_rank_0000{0..3}.pt` |
| milestones | 0, 0.5, 1, 3, 5, 10, 13.000238080, 15, 17, …, 37（B token，两 B 间隔） |
| 模型 | 8 层，hidden 1024，intermediate 1536，8 expert，Top-2，vocab 151936，tie embedding；参数 507,988,992（expert 301,989,888） |
| block-7 load bias | [2.3770, 2.3960, 2.3880, 2.3730, 2.4000, 2.3800, 2.3900, 2.3970] |
| SAE | 30000 latent，k=32，接口“blocks.7.moe.router input = blocks.7.norm2 output, before linear router and load bias”；本数据上平均 NMSE 0.233 |
| 数据 | S14 `reference_general.jsonl`，6000 篇，5589 篇有完整 128-token 正文；来源 `/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/…`，不是模型训练所用 global-shard_01。DCLM-Baseline 数据卡标注 CC-BY-4.0；逐文档许可未核对 |
| 前向吞吐 | fp32 40,830 token/s（batch 64×128），峰值 6.4 GiB |
| 单 expert 反向（原生 fp32，16×128） | 0.127 s/步，峰值 3.9 GiB |
| 本轮探针峰值 | 18.8 GiB（float64 缓存 137,386×1024×3） |

据此估算任务 B 全量 <15 分钟，未缩规模。实际 GPU 墙钟：stage1 两次（首次在测速步因字段名报错，已修正重跑；划分文件哈希两次相同）共 67 秒，stage3 554 秒，合计约 10.4 分钟（`evidence/gpu_clock.log`）。

## 3. 划分与分组

- 5589 篇；171 个近重复组（共享 ≥1 个 13-token 片段）整体分到同侧。DEV 1957 / GRAD 1956 / EVAL 1676 篇。`data/split.json` SHA256 `cd3e92bc…0f89`。
- DEV 负载份额：e0 .211、e1 .237、e2 .204、e3 .218、e4 .289、e5 .229、e6 .357、e7 .254 → expert 7。
- expert 7 位置 137,386；保留 13,338 个 feature。簇支持（DEV/GRAD/EVAL）：c0 7409/7761/6327；c1 4408/5377/4126；c2 6463/6505/5336；c3 5874/5804/4807；c4 5170/5666/4663；c5 6528/5389/4962；c6 3066/3820/2585（GRAD 不足，不合格）；c7 8320/9090/7930。Y=c7，X=c1（余弦 0.28）。
- 各组：

| 组 | token | 文档 | 初始 CE | gate 权重均值（sd） |
|---|---|---|---|---|
| A_grad（c1） | 5377 | 1485 | 1.589 | 0.202 (0.178) |
| B′_grad（c7） | 9090 | 1333 | 4.296 | 0.487 (0.186) |
| A_eval（c1） | 4126 | 1260 | 1.734 | 0.196 (0.178) |
| B_eval（c7） | 7930 | 1145 | 4.332 | 0.486 (0.181) |

A 与 B 在初始损失和 gate 上没有匹配，按规则未重选。

## 4. 数值与控制

- float64 尾部对原生 fp32：4096 个随机位置末层隐状态最大差 4.55×10⁻⁵，单 token CE 最大差 3.07×10⁻⁵ nat，均值 3.46603 vs 3.46603。
- 基线重复评估逐位相同；零更新 ΔL＝0（A_eval、B_eval）；全部分支恢复 `torch.equal`；原模型参数版本号与 load bias 不变（`evidence/probe_complete.json`）。
- DEV 预检（`data/probe_plan_frozen.json`）：η=1/16…2 时单 batch 平均 ΔL_B 为 3.4×10⁻⁵…2.0×10⁻²，均值分支 4.8×10⁻⁶…2.0×10⁻⁴（均为正）。η_hi＝2。

## 5. 结果全表

完整单元（来源×评估集×n×η：均值分支、一阶预测、单 batch 平均及区间、噪声项及区间）在 `results/probe_cells.csv`；斜率、交叉点、半步比、SNR 在 `results/probe_analysis.json`；A01 在 `results/probe_supplement_A01.json`；原始 5064 行 `results/probe_rows.csv`（SHA256 `5057d492…91f5`）。

### 5.1 主比较的噪声项（nat，B_eval）

| η | A→B n=32 | n=64 | n=128 | B′→B n=32 | n=64 | n=128 |
|---|---|---|---|---|---|---|
| 1/32 | 2.0e-6 | 2.8e-6 | 2.0e-6 | 1.33e-4 | 1.22e-4 | 5.2e-5 |
| 1/8 | 4.8e-5 | 2.4e-5 | 1.5e-5 | 2.66e-3 | 1.87e-3 | 8.5e-4 |
| 1/2 | 8.6e-4 | 3.3e-4 | 1.8e-4 | 4.85e-2 | 3.02e-2 | 1.37e-2 |
| 2 | 1.42e-2 | 6.2e-3 | 2.9e-3 | 1.07 | 0.50 | 0.22 |

### 5.2 均值分支（nat，B_eval）

| η | 1/32 | 1/8 | 1/2 | 1 | 2 | 4 |
|---|---|---|---|---|---|---|
| A→B | −1.73e-6 | −6.48e-6 | −1.88e-5 | −1.84e-5 | +3.94e-5 | +3.83e-4 |
| B′→B | −8.28e-5 | −3.00e-4 | −7.00e-4 | +1.5e-6 | +6.04e-3 | +3.99e-2 |

### 5.3 斜率

η 斜率（12 个主单元）1.95–2.35；n 斜率见 `slopes_n`，η=1/16–2 下 −0.77 至 −1.39，η=4 时 −1.17 至 −1.58。半步比：同组噪声项相邻 η 之比 3.9–4.3（n=64/128；二次项的预期为 4），跨组 n=128 小 η 处 2.6–3.3（小 η 区间宽）。

### 5.4 次要跨组（各簇 GRAD → B_eval，R=16）

一阶投影 z：c0 1.48、c2 2.45、c3 2.86、c4 2.36、c5 0.27（全为帮助）。η 斜率 1.77–2.31。控制变量 η\*（n=128）：c0 0.049、c3 0.037（CI 未全负）、c4 0.052；n=64：c4 0.036；c2、c5 未在网格内交叉。

## 6. 偏差与失败

- stage1 首次运行在测速步报 `ModelOutput` 无 `loss` 字段，已改为 `lm_loss_sum/lm_tokens` 重跑；数据与划分不变。
- 预检网格由 DEV 的“伤害”端确定，下限 1/32 恰在跨组 η\* 附近，导致网格内难以直接看到帮助区——这是网格设计的局限，已在 Summary 中按“不足”报告。
- 噪声项估计含 ḡ 自身噪声的偏差约 (η²/2)tr(HΣ)/(128M)，n=128、M=42 时约为噪声项的 2–3%。

## 7. 资产

新分析登记见 `assets/catalog.json` 中 `analysis_snr_one_step_decomposition_20261108`。未保存新权重或表示缓存；探针缓存只在显存中。
