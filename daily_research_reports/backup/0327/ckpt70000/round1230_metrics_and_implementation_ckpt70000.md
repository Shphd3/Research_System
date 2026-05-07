# 12L 内部评估说明（ckpt70000，顺序 1→2→3→0）

## 1. 评估目标与口径

- 目标：将新增模型 `qwen3-moe-H768-quadratic_nosvd_running_center_8gpu-center_running-gate_off-acp_off-lb_0-quadratic_nosvd` 纳入 12L 内部评估。
- 模型集合：`/data/250010109/spectral_router/output_moe` 下所有 12L 模型，排除 `qwen3-moe-H768--linear_running_center_fixedbeta_rho099_8gpu_gbs768-center_running-gate_off-lb_0-linear`。
- checkpoint：统一使用 `checkpoint-70000`。
- 顺序：Round1 → Round2 → Round3 → Round0（Round0 最耗时，最后执行）。
- 输出根目录：`/data/250010109/spectral_router/exp_expert_lowrank/output/round_12L/ckpt70000`。

## 2. Round1：专家低秩专门化（结构性）

### 2.1 实验目的

- 验证不同路由模型在专家输入空间上的“压缩与分离”能力。
- 关键关注：ED、ED_comp、子空间重叠、路由语义一致性、负载均衡。

### 2.2 数据集与采样

- 数据集：WOS（`river-martin___web-of-science-with-label-texts`），默认 `train`。
- 文本采样：按标签轮转抽样（label round-robin diverse），保证类别覆盖。
  - 先按 `label_col` 分桶，再对每个桶内文本随机打乱，随后按“每个标签取 1 条”的顺序循环取样，直到达到 `max_samples`（默认 96）或样本耗尽。
  - 这一步保证多类别尽量均衡进入评估，减少单一类别主导。
- 网络采样：
  - 从每层有效 token（`attention_mask==1`）抽取专家路由标签；
  - 按专家聚合 token 特征；
  - 对专家特征做协方差统计与分块补偿。
  - 序列长度由 tokenizer 截断到 `max_length`（默认 128），因此每条样本最多贡献 128 个 token（去除 padding 后按有效 token 计数）。

### 2.3 指标公式

- 有效维度（ED）：
  $$
  \mathrm{ED}=\frac{\left(\sum_i \lambda_i\right)^2}{\sum_i \lambda_i^2}
  $$
  其中 $\lambda_i$ 为协方差特征值。

- 补偿有效维度（ED_comp）：在每专家最小 token 阈值下补偿采样后，再按层/专家聚合 ED。
  - 核心原因：不同专家收到的 token 数可能差异很大，直接计算会让“高负载专家”主导统计。
  - 代码做法：按每个专家累计到的协方差 chunk 数，取中位数作为目标 chunk 数；chunk 少于中位数的专家，从该专家 token 池随机补采样并补算协方差 chunk，再更新该专家 ED，最后再聚合。
  - 这样做不是追求“完美无偏”，而是让不同专家在统计量上更可比，能更稳定反映低秩趋势。

- 子空间重叠（Overlap@r）：
  $$
  \mathrm{Overlap}(U_i,U_j)=\frac{\|U_i^\top U_j\|_F^2}{r}
  $$
  - 仅对 token 数达到阈值（`min_tokens_per_expert`，默认 256）的专家构建子空间，避免小样本专家引入噪声。
  - 若可用专家不足 2 个，返回 NaN，不强行给出误导性重叠值。

- 路由条件熵：
  $$
  H(E|C)=\sum_c p(c)\left[-\sum_e p(e|c)\log_2 p(e|c)\right]
  $$
  - 这里 $C$ 不是原始数据集标签，而是 teacher 模型最后一层特征经 KMeans 得到的伪语义簇（pseudo clusters）。
  - 先统计每个簇内 token 到各专家的分布 $p(e|c)$，再用簇权重 $p(c)$ 做加权平均。
  - 当某些簇没有样本或总样本数为 0 时，会跳过或返回 NaN。

- 负载变异系数：
  $$
  CV=\frac{\sigma(p)}{\mu},\quad p_e=\frac{n_e}{\sum_e n_e},\ \mu=\frac{1}{E}
  $$
  - 其中 $n_e$ 是专家 $e$ 接收的 token 数。
  - 若总 token 数为 0，返回 NaN；否则按标准离散系数计算。

### 2.4 代码中“数据如何进入公式”的具体流程（Round1）

1) 采样文本（最多 96 条）并分 batch（`batch_size=2`）。  
2) 模型前向得到每层 `expert_labels` 与隐藏状态；仅保留有效 token。  
3) 每个 token 按 top1 专家路由归档到对应专家池。  
4) 对每个专家池按 chunk（默认 256 token）构造协方差并求特征值。  
5) 由特征值计算 ED；再做中位数 chunk 补偿得到 ED_comp。  
6) 对满足样本阈值的专家做子空间分解并计算 Overlap。  
7) 基于 teacher 伪簇与专家分配矩阵计算 $H(E|C)$。  
8) 基于各专家 token 占比计算 CV。

### 2.5 脚本实现位置与实现正确性评估

- 入口脚本：`exp_expert_lowrank/scripts/round1/run_round1_expert_low_rank_enhanced.py`
- 公式实现：
  - `router_eval/evaluate_expert_low_rank_specialization.py` 中 ED、Overlap、H(E|C)、CV 的计算函数。
- 结果文件：
  - 单模型：`round1_expert_low_rank/<model>/enhanced_low_rank_metrics.json`
  - 汇总：`round1_expert_low_rank/enhanced_low_rank_summary.json`
- 评估（是否能反映问题）：
  - 结论：实现整体可靠，且针对“专家负载不均衡”做了必要防护（阈值过滤 + chunk 补偿 + NaN 回退）。
  - 局限：$H(E|C)$ 使用伪簇而非真实标签，语义解释偏“表征簇一致性”，不是严格监督语义一致性；但用于横向模型比较是有价值的。

## 3. Round2：特征扰动鲁棒性（稳定性）

### 3.1 实验目的

- 测试路由器对中间层特征噪声的敏感性。
- 关键关注：clean/noisy 路由 top1 一致率是否随噪声稳定衰减。

### 3.2 数据集与采样

- 数据集：WOS `train`。
- 文本采样：与 Round1 相同的 label round-robin diverse。
- 网络采样：
  - 扰动位置：`post_attention_layernorm` 输出；
  - 扰动方式：$\epsilon\sim\mathcal N(0,\sigma^2)$；
  - 比较对象：同一批 token 的 clean 与 noisy top1 expert。
  - 数据长度：每样本最多 `max_length=128`，有效比较 token 由 `attention_mask==1` 决定。

### 3.3 指标公式

- 层内一致率：
  $$
  \mathrm{CR}_l=\frac{1}{N_l}\sum_{t=1}^{N_l}\mathbf{1}\left[\hat e_{t,l}^{clean}=\hat e_{t,l}^{noisy}\right]
  $$

- 总一致率：
  $$
  \mathrm{Overall\_CR}=\frac{1}{L}\sum_{l\in\mathcal L}\mathrm{CR}_l
  $$

### 3.4 脚本实现位置

- 入口脚本：`exp_expert_lowrank/scripts/round2/run_round2_feature_perturbation.py`
- 关键实现：
  - `LayerNoiseInjector`：注入高斯噪声；
  - `evaluate_model_consistency`：按层统计匹配率；
  - `build_plots`：生成 round2 一致率曲线图。
- 结果文件：
  - 单模型：`round2_feature_perturbation/<model>/round2_feature_perturbation_metrics.json`
  - 汇总：`round2_feature_perturbation/round2_feature_perturbation_summary.json`
- 评估（是否能反映问题）：
  - 结论：实现直接衡量“路由决策对噪声的稳定性”，与目标一致，解释清晰。
  - 局限：是 top1 一致率，不反映概率分布细节；但用于比较不同路由策略鲁棒性已经足够。

## 4. Round3：谱干扰与路由置信度（跨域）

### 4.1 实验目的

- 评估跨领域输入在专家空间中的干扰强度与路由 margin 变化。
- 关键关注：谱干扰 SI 是否降低、margin 是否提高。

### 4.2 数据集与采样

- 数据集：WOS `train`。
- 域划分：
  - Domain A：`CS`
  - Domain B：`Medical`
- 多类别情形怎么取：
  - `--domain_a_labels` 和 `--domain_b_labels` 都支持多个类别标签。
  - 代码会遍历数据集，把 `domain` 字段属于 A 列表的样本放入 A，属于 B 列表的放入 B。
  - 每个域最多取 `max_samples_per_domain`（默认 64），达到上限后停止继续加入。
- 网络采样：
  - 对两域分别提取专家输入特征，构建专家协方差；
  - 同时抓取 router logits，计算 top1-top2 margin。
  - 数据长度：每条样本 tokenized 后截断到 `max_length=128`，协方差和 margin 都基于有效 token。

### 4.3 指标公式

- 专家协方差：
  $$
  C=\frac{(X-\bar X)^\top(X-\bar X)}{N-1}
  $$

- 专家级谱干扰：
  $$
  \mathcal I_i=\frac{\mathrm{Tr}(C_{A,i}C_{B,i})}{\|C_{A,i}\|_F\|C_{B,i}\|_F}
  $$
  - 若分母过小（接近 0），实现中返回 0.0 并对结果 clamp 到 $[0,1]$，防止数值爆炸。

- 层级平均谱干扰：
  $$
  \bar{\mathcal I}_l=\frac{1}{E_l}\sum_i \mathcal I_i
  $$
  - 这里是对“有效专家集合”做平均，而不是按 token 数加权。

- 路由 margin：
  $$
  m=\text{Top1Logit}-\text{Top2Logit}
  $$

- 域间 margin 差：
  $$
  \Delta m=\mathbb E[m_A]-\mathbb E[m_B]
  $$

### 4.4 代码中“两个域如何真正计算”的具体流程（Round3）

1) 根据 `domain` 字段把样本放到 A/B 两个集合。  
2) 每个集合最多取 `max_samples_per_domain` 条文本（默认 64）。  
3) tokenization 截断到 `max_length=128`，形成批次。  
4) 对 A/B 分别前向，按层、按专家收集有效 token 特征。  
5) 每个专家若有效样本足够，构造协方差 $C_{A,i},C_{B,i}$，计算 $\mathcal I_i$。  
6) 对层内所有可用专家求平均得到 $\bar{\mathcal I}_l$。  
7) 同时用 router logits 计算每个 token 的 margin，分别求 A/B 均值和差值 $\Delta m$。  
8) 若某层无可用专家或无有效 margin，写 NaN（不强行补值）。

### 4.5 脚本实现位置与实现正确性评估

- 入口脚本：`exp_expert_lowrank/scripts/round3/run_round3_spectral_interference.py`
- 关键实现：
  - `compute_spectral_interference`：计算 SI；
  - `compute_margin_from_router_logits`：计算 margin；
  - `evaluate_spectral_interference`：按层汇总 SI 与 margin。
- 结果文件：
  - 单模型：`round3_spectral_interference/<model>/spectral_interference_with_margin.json`
  - 汇总：`round3_spectral_interference/spectral_interference_with_margin_summary.json`
- 评估（是否能反映问题）：
  - 结论：SI 与 Margin 的实现基本正确，能用于比较模型“跨域干扰 vs 路由置信度”的相对差异。
  - 需要注意：
    - 采样是按遍历顺序截取而非 round-robin，若数据原顺序偏置可能带来轻微样本偏差；
    - SI 使用专家均值而非 token 加权，更关注“专家层面结构差异”，不是“流量主导差异”。

## 5. Round0：下游任务表现（最终耗时评测）

### 5.1 实验目的

- 用统一任务集检验结构指标与真实任务性能的一致性。
- 作为 Round1-3 结构分析后的最终外部效能对照。

### 5.2 数据集与任务

- 评测框架：`lm_eval`。
- 任务集合（默认）：`arc_easy, arc_challenge, piqa, hellaswag, openbookqa, winogrande, boolq`。
- 采样策略：`limit=None`，完整任务评测。

### 5.3 指标说明

- 任务分数取值优先级：
  - `acc_norm,none` > `acc_norm` > `acc,none` > `acc`
- 综合比较可使用任务均值或对基线增量（由汇总文件二次分析）。

### 5.4 脚本实现位置

- 入口脚本：`exp_expert_lowrank/scripts/round0/run_round0_downstream_eval.py`
- 调度与汇总：
  - `router_eval/eval_methods/lm_eval/run_dispatch.py`
  - `router_eval/eval_methods/lm_eval/run_summary.py`
- 结果文件：
  - 单模型：`round0_downstream_fulltasks/<model>/lm_eval_results_step70000.json`
  - 汇总：`round0_downstream_fulltasks/round0_downstream_summary.csv`

## 6. 本轮建议输出图（美观对比）

- Round1：`ED_comp + Overlap` 双轴柱状图（模型对比）
- Round2：`Overall CR - sigma` 折线图（鲁棒性曲线）
- Round3：`Mean SI vs Mean Margin` 散点图（结构-置信度权衡）
- Round0：下游任务分数热力图（模型 × 任务）

图输出脚本：`exp_expert_lowrank/scripts/round_12L/plot_round12l_comparison.py`  
图输出目录：`.../output/round_12L/ckpt70000/figures`

## 7. 顺序执行脚本

- 一键顺序执行（1→2→3→0）：
  - `exp_expert_lowrank/scripts/round_12L/run_round12l_ckpt_eval.py`
- dry-run（先检查模型发现、命令与输出路径）：
  - `python -u .../run_round12l_ckpt_eval.py --checkpoint_step 70000 --dry_run`
