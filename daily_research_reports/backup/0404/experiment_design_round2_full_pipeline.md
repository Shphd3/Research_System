# continuous_hmm_v3 实验设计全流程（Round 2 设计稿）

## 1. 文档目标与适用范围

- 目标：把当前 synthetic MoE 实验从“可跑通”提升到“可审计、可复核、可改进”的完整流程文档。
- 适用实验：
  - 数据：`continuous_hmm_v3`
  - 路由：`linear_running_center / acp_lite / hybrid_subspace_energy / subspace_energy`
  - 模型：`TinyTwoLayerMoEModel`（synthetic）与 `MyQwen3SparseMoeBlock`（主项目 MoE 实现映射）
- 不含内容：
  - 不执行新实验
  - 不直接给 CL 终局结论
  - 不回流 `old_diagonal_quadratic` 到 active 对比

---

## 2. 当前结果快照（来自 r20260404_v3full）

数据源：`/data/250010109/spectral_router/exp_synthetic_data/docs/summary_continuous_hmm_v3_r20260404_v3full.md`

### 2.1 Type1（mean-separable）

| Router | TaskLoss(mean±std) | NMI(mean±std) | ARI(mean±std) | CV_load(mean±std) |
|---|---:|---:|---:|---:|
| linear_running_center | 8.659419±0.483624 | 0.101187±0.047825 | 0.097568±0.049826 | 0.225964±0.050418 |
| acp_lite | 9.677728±2.312728 | 0.000245±0.000202 | 0.000025±0.000034 | 1.642967±0.125729 |
| hybrid_subspace_energy | 7.953464±0.600586 | 0.009317±0.013177 | 0.000530±0.000750 | 1.711011±0.029755 |
| subspace_energy | 9.641444±1.387861 | 0.020394±0.001564 | 0.017786±0.001410 | 0.177520±0.114124 |

### 2.2 Type2（covariance-separable）

| Router | TaskLoss(mean±std) | NMI(mean±std) | ARI(mean±std) | CV_load(mean±std) |
|---|---:|---:|---:|---:|
| linear_running_center | 10.065698±0.419102 | 0.015243±0.004649 | 0.012623±0.003982 | 0.142834±0.013994 |
| acp_lite | 11.163553±2.309496 | 0.012330±0.003326 | 0.001547±0.001765 | 1.532563±0.232723 |
| hybrid_subspace_energy | 9.389329±0.629696 | 0.006450±0.008226 | 0.002127±0.002994 | 1.601874±0.179705 |
| subspace_energy | 11.062676±1.368037 | 0.035419±0.010137 | 0.032278±0.007678 | 0.136580±0.047333 |

### 2.3 Type3（hybrid-separable）

| Router | TaskLoss(mean±std) | NMI(mean±std) | ARI(mean±std) | CV_load(mean±std) |
|---|---:|---:|---:|---:|
| linear_running_center | 9.328427±0.454763 | 0.029860±0.013503 | 0.029093±0.013935 | 0.165920±0.047894 |
| acp_lite | 10.382928±2.311055 | 0.005535±0.003095 | 0.000427±0.000503 | 1.591866±0.174343 |
| hybrid_subspace_energy | 8.631163±0.610984 | 0.003505±0.004774 | 0.000389±0.000554 | 1.659270±0.101935 |
| subspace_energy | 10.317553±1.377337 | 0.005820±0.001724 | 0.005035±0.001565 | 0.131953±0.089155 |

当前口径下的核心观察：
- `subspace_energy` 在 Type2 的 NMI/ARI 最强，支持“协方差可分情形下二阶子空间信息有效”。
- `hybrid_subspace_energy` 的优势更偏 TaskLoss，但 `CV_load` 明显偏弱，尚未形成“全面优势”。
- `acp_lite` 在 v3 强均值遮蔽下负载显著劣化，当前不再是稳定强 comparator。

---

## 3. 可复核实验全流程（从数据到汇总）

### 3.1 一键流程入口

主入口脚本：`/data/250010109/spectral_router/exp_synthetic_data/scripts/run_protocol_v3.sh`

执行顺序：
1. 造数据：`generate_continuous_hmm.py`
2. 几何 sanity：`sanity_check_geometry.py`
3. 四路由 × type × seed 扫描：`run_router_sweep.sh -> run_synth_moe.sh -> train_synth_moe.py`
4. 多 seed 汇总：`summarize_router_runs.py`

### 3.2 建议命令模板（仅供复核，不在本文执行）

```bash
cd /data/250010109/spectral_router
RUN_MODE=v3full \
DATA_RUN=continuous_hmm_v3 \
DATA_TYPES=type1,type2,type3 \
SEEDS=20260404,20260405,20260406 \
NPROC_PER_NODE=2 \
BATCH_SIZE=128 \
EPOCHS=12 \
bash /data/250010109/spectral_router/exp_synthetic_data/scripts/run_protocol_v3.sh
```

### 3.3 产物目录规范

- 数据目录：`/data/250010109/spectral_router/exp_synthetic_data/data/continuous_hmm_v3/{type1,type2,type3}`
- 单 run 输出：`/data/250010109/spectral_router/exp_synthetic_data/output/continuous_hmm_v3/<run_name>/`
- 汇总输出：
  - `summary_*.json`
  - `summary_*.md`
  - 位于：`/data/250010109/spectral_router/exp_synthetic_data/docs/`

---

## 4. 造数据机制（continuous_hmm_v3）

数据脚本：`/data/250010109/spectral_router/exp_synthetic_data/data/generate_continuous_hmm.py`

### 4.1 隐变量生成（统一 HMM 结构）

- 先构造类间转移矩阵：
  - 对角为 `hmm_stickiness`
  - 非对角均分剩余概率
- 对每条序列采样 `z_{1:T}`，得到 token latent label。

### 4.2 观测生成（分 type）

统一形式：
- `x_t = mu_global + mu_local[z_t] + noise_t`

其中：
- `mu_global`：全局大范数偏置（默认 `global_mean_norm=40`），用于制造 Cone Effect。
- `mu_local` 与 `cov`：根据 type 区分。

Type1（mean-separable）：
- 类别主要由均值差异主导。
- 协方差为各类同构的近似各向同性噪声。

Type2（covariance-separable）：
- 均值差弱化（`type2_mean_scale` 较小）。
- 每类在独立低秩子空间方向上有额外 stretch，制造协方差主分离。

Type3（hybrid-separable）：
- 时序分段混合 Type1 与 Type2 生成机制。
- 通过 `type3_segment_len` 控制切换节奏。

### 4.3 训练样本组织

- 自回归切分：
  - `source = x[:, :-1, :]`
  - `target = x[:, 1:, :]`
- token 标签对齐：
  - `z_token = z[:, 1:]`
- 注意：当前 token 标签仍来自同一序列过程，后续 controlled benchmark 要进一步显式解耦 token latent / sentence-task / nuisance。

---

## 5. 模型架构（synthetic 训练使用）

训练脚本：`/data/250010109/spectral_router/exp_synthetic_data/train/train_synth_moe.py`

### 5.1 主干结构（TinyTwoLayerMoEModel）

前向链路：
1. `embedding`: `input_dim -> d_model`
2. `layer1`: 单层 Transformer block（MHA + FFN）
3. `moe_ln`: LayerNorm
4. `moe`: Top-1 MoE（四种 router 可切换）
5. 残差：`h2 = h1 + moe_out`
6. `out_proj`: `d_model -> input_dim`

训练目标：
- `TaskLoss = MSE(pred, target)`

### 5.2 MoE 层（Top1MoE）

- 路由输出 `logits` 后做 softmax 得到 `probs`。
- `top1 = argmax(logits)`，每 token 只派发给一个 expert。
- 按 expert mask 分组执行 MLP，再写回原 token 位置。

---

## 6. 四路由实现细节（train_synth_moe.py）

### 6.1 `linear_running_center`

- 先 running center：`x_c = x - mu_running`
- 再线性打分：`l_e = w_e^T x_c`
- 作用：作为最干净一阶中心化 baseline。

### 6.2 `acp_lite`

- 先算 `x_c` 与 `mu_running` 单位方向 `u`。
- 拆分均值平行分量：
  - `x_parallel = (u^T x)u`
- 打分：
  - `l_e = <w_parallel,e, x_parallel> + <w_centered,e, x_c>`
- 作用：把“均值相关方向”与“中心化残差”显式拆开。

### 6.3 `hybrid_subspace_energy`

- 延续 `acp_lite` 的两路一阶项，再加 expert 子空间能量：
  - `z_{e,r} = <v_{e,r}, x_c>`
  - `energy_e = sum_r z_{e,r}^2`
  - `l_e = linear_parallel + linear_centered + energy_e`
- 作用：测试“保留一阶有效信息 + 二阶子空间能量”的 hybrid 路线。

### 6.4 `subspace_energy`

- 仅保留中心化后子空间能量项：
  - `l_e = ||V_e x_c||_2^2`
- 作用：测试纯二阶子空间机制在 covariance-separable setting 的能力上界。

---

## 7. 优化、日志与指标口径

### 7.1 参数组与学习率解耦

- 参数分组：
  - `embedding_params`
  - `router_params`
  - `backbone_params`
- 默认学习率：
  - `embedding_lr=3e-4`
  - `router_lr=3e-3`
  - `backbone_lr=2e-4`
- 可选 `freeze_backbone=true`，当前主流程默认开启。

### 7.2 关键日志文件（每 run）

- `config.json`：完整超参快照
- `metrics.json`：val/test 指标 + 优化器 LR + 参数统计
- `param_report.json`：参数量分解
- `eigen_log.jsonl`：`moe_in` 协方差特征值谱演化
- `train.log`：训练过程日志

### 7.3 评估指标

- `TaskLoss`：MSE，越低越好
- `NMI/ARI`：`top1` 与 `z_token` 对齐，越高越好
- `CV_load`：专家负载变异系数，越低越好
- `expert_counts`：各专家分配样本量

---

## 8. 与主项目 MyQwen 架构的映射关系

主项目脚本：`/data/250010109/spectral_router/src/model/qwen3_moe/myqwen.py`

### 8.1 路由类型映射

- synthetic `subspace_energy` 对应主项目 `router_type="quadratic_low_rank"` 的核心二阶子空间分支（`SubspaceEnergyRouter`）。
- synthetic `acp_lite` 与主项目 `router_acp_transform` + center/residual 双门控设计在结构上同源。
- synthetic running center 与主项目 `router_center_mode="running"` 同属 EMA 风格中心更新。

### 8.2 主项目中额外能力（synthetic 尚未覆盖）

- Top-k（非仅 Top-1）与归一化
- shared expert + 多 expert 融合
- load balancing 辅助损失（`lb_loss`）
- quadratic_low_rank 的子空间正交/跨专家重叠正则
- 多头 MoE 路由（`moe_type="multihead"`）

这意味着当前 synthetic 实验用于机制对比是有效的，但要映射到 LLM 主干，还需要在训练脚本中补齐正则与机制日志口径。

---

## 9. 本轮设计改进（Round 2）

### 9.1 设计目标

- 不是扩大 benchmark，而是提高证据质量：
  - 指标与机制统计同时成立
  - 多 seed 方向一致
  - 负载稳定性可部署

### 9.2 MVP -> Gate 流程

1. MVP（只跑 Type2）：
   - 路由固定四路由
   - seeds 固定 3 个
   - 输出 `mean±std` 与 `Δ vs linear / Δ vs acp`
2. Gate-A（是否进入 Type3）：
   - 至少一个二阶相关路由在 `NMI + TaskLoss` 同时优于 `acp_lite`
   - 且 `CV_load` 不劣化超过 20%
3. Gate-B（是否进入 Type1）：
   - Type3 结果仍支持主线，且 std 无同量级反转
4. Gate-C（是否扩 train=5000 或 10000）：
   - 仅当排序受高方差影响无法判读时触发

### 9.3 本轮必须补齐的机制统计

- 几何分解：`||x||`, `u^T x`, `||x_c||`, `||V_e x_c||^2` 分布（mean/std/quantile）
- 路由分配：每 epoch 专家占比轨迹、token->expert 转移矩阵
- 二阶稳定性：`||V_eV_e^T-I||`、`||V_iV_j^T||` 轨迹
- 优化动态：router grad norm / embedding grad norm 比值

### 9.4 判定规则（支持/削弱/否定）

- 支持主线：
  - Type2（并随后 Type3）多 seed 下二阶相关路由对 `acp_lite` 有方向一致优势
  - 优势同时体现在最终指标与机制证据
- 削弱主线：
  - 仅单指标偶发胜出，或机制证据缺失
- 否定主线（当前协议下）：
  - 对 `acp_lite` 无稳定优势且负载/机制均不成立

---

## 10. 复核清单（供你逐条检查）

### 10.1 数据层

- `metadata.json` 中 `global_mean_norm_actual` 是否接近配置值
- Type1/2/3 的 train/val/test 文件是否齐全
- `dataset_type` 与 `type3_mode` 字段是否按预期写入

### 10.2 训练层

- `config.json` 中 `router_lr > embedding_lr` 是否成立
- `freeze_backbone` 是否按本轮协议固定
- 各 run 是否完整产生 `metrics.json / eigen_log.jsonl / train.log`

### 10.3 汇总层

- `summary_*.md` 是否覆盖四路由 × 三 type × 三 seeds
- `missing_runs` 是否为 0
- 是否同时给出 `Δ vs linear` 与 `Δ vs acp`（若无，作为下一步改进项）

---

## 11. 下一步最小修改建议（仅设计，不在本文实施）

1. 在 `train_synth_moe.py` 增加机制 telemetry 落盘（能量分布、梯度范数比、子空间重叠）。
2. 在 `summarize_router_runs.py` 增加 `Δ vs baseline` 列与 Gate 判定摘要。
3. 在数据脚本新增 controlled 版本：
   - 显式拆分 token latent label 与 sentence/task label
   - 独立注入 nuisance factor
   - 输出可直接用于“token-level routing”证伪协议的数据字段。

---

## 12. 关键文件索引

- 迭代状态文档：`/data/250010109/spectral_router/exp_synthetic_data/docs/MoE - 迭代状态存档 v6.5.md`
- 当前结果汇总：`/data/250010109/spectral_router/exp_synthetic_data/docs/summary_continuous_hmm_v3_r20260404_v3full.md`
- 训练脚本：`/data/250010109/spectral_router/exp_synthetic_data/train/train_synth_moe.py`
- 数据脚本：`/data/250010109/spectral_router/exp_synthetic_data/data/generate_continuous_hmm.py`
- 协议脚本：`/data/250010109/spectral_router/exp_synthetic_data/scripts/run_protocol_v3.sh`
- 汇总脚本：`/data/250010109/spectral_router/exp_synthetic_data/scripts/summarize_router_runs.py`
- 主项目 MoE 架构：`/data/250010109/spectral_router/src/model/qwen3_moe/myqwen.py`
