# 12L 内部评估说明（ckpt60000，顺序 1→2→3→0）

## 1. 评估目标与口径

- 目标：在 12L 五模型集合上复跑一轮，checkpoint 从 70000 切换为 60000。
- 模型集合：`/data/250010109/spectral_router/output_moe` 下可用 12L 模型，排除 fixedbeta 模型。
- checkpoint：统一使用 `checkpoint-60000`。
- 顺序：Round1 → Round2 → Round3 → Round0（Round0 最耗时，最后执行）。
- 输出根目录：`/data/250010109/spectral_router/exp_expert_lowrank/output/round_12L/ckpt60000`。

## 2. Round1：专家低秩专门化（结构性）

### 2.1 实验目的

- 验证不同路由模型在专家输入空间上的“压缩与分离”能力。
- 关键关注：ED、ED_comp、子空间重叠、路由语义一致性、负载均衡。

### 2.2 数据集与采样

- 数据集：WOS（`river-martin___web-of-science-with-label-texts`），默认 `train`。
- 文本采样：按标签轮转抽样（label round-robin diverse），最大样本数 `max_samples=96`。
- 网络采样：
  - 从每层有效 token（`attention_mask==1`）抽取专家路由标签；
  - 按专家聚合 token 特征并做协方差统计；
  - 序列长度由 tokenizer 截断到 `max_length=128`。

### 2.3 指标公式

- 有效维度（ED）：
  $$
  \mathrm{ED}=\frac{\left(\sum_i \lambda_i\right)^2}{\sum_i \lambda_i^2}
  $$

- 补偿有效维度（ED_comp）：
  - 先基于专家 token 构造 chunk 协方差并统计；
  - 再按中位数 chunk 数对低样本专家补采样，降低负载不均造成的偏差；
  - 最后聚合得到补偿后的 ED。

- 子空间重叠（Overlap@r）：
  $$
  \mathrm{Overlap}(U_i,U_j)=\frac{\|U_i^\top U_j\|_F^2}{r}
  $$

- 路由条件熵：
  $$
  H(E|C)=\sum_c p(c)\left[-\sum_e p(e|c)\log_2 p(e|c)\right]
  $$

- 负载变异系数：
  $$
  CV=\frac{\sigma(p)}{\mu},\quad p_e=\frac{n_e}{\sum_e n_e},\ \mu=\frac{1}{E}
  $$

### 2.4 脚本实现位置

- 入口脚本：`exp_expert_lowrank/scripts/round1/run_round1_expert_low_rank_enhanced.py`
- 公式实现：`router_eval/evaluate_expert_low_rank_specialization.py`
- 结果文件：
  - 单模型：`round1_expert_low_rank/<model>/enhanced_low_rank_metrics.json`
  - 汇总：`round1_expert_low_rank/enhanced_low_rank_summary.json`

## 3. Round2：特征扰动鲁棒性（稳定性）

### 3.1 实验目的

- 测试路由器对中间层特征噪声的敏感性。
- 关键关注：clean/noisy 路由 top1 一致率随噪声的退化曲线。

### 3.2 数据集与采样

- 数据集：WOS `train`。
- 文本采样：与 Round1 相同（label round-robin diverse）。
- 网络采样：
  - 扰动位置：`post_attention_layernorm` 输出；
  - 扰动方式：$\epsilon\sim\mathcal N(0,\sigma^2)$；
  - 比较对象：同一 token 的 clean 与 noisy top1 expert。

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
  - `build_plots`：输出一致率曲线图。
- 结果文件：
  - 单模型：`round2_feature_perturbation/<model>/round2_feature_perturbation_metrics.json`
  - 汇总：`round2_feature_perturbation/round2_feature_perturbation_summary.json`

## 4. Round3：谱干扰与路由置信度（跨域）

### 4.1 实验目的

- 评估跨领域输入在专家空间中的干扰强度与路由 margin 变化。
- 关键关注：谱干扰 SI 是否降低、margin 是否提高。

### 4.2 数据集与采样

- 数据集：WOS `train`。
- 域划分：
  - Domain A：`CS`
  - Domain B：`Medical`
- 每域采样：`max_samples_per_domain=64`。
- 网络采样：按层按专家收集有效 token 特征，并抓取 router logits。

### 4.3 指标公式

- 专家协方差：
  $$
  C=\frac{(X-\bar X)^\top(X-\bar X)}{N-1}
  $$

- 专家级谱干扰：
  $$
  \mathcal I_i=\frac{\mathrm{Tr}(C_{A,i}C_{B,i})}{\|C_{A,i}\|_F\|C_{B,i}\|_F}
  $$

- 层级平均谱干扰：
  $$
  \bar{\mathcal I}_l=\frac{1}{E_l}\sum_i \mathcal I_i
  $$

- 路由 margin：
  $$
  m=\text{Top1Logit}-\text{Top2Logit}
  $$

- 域间 margin 差：
  $$
  \Delta m=\mathbb E[m_A]-\mathbb E[m_B]
  $$

### 4.4 脚本实现位置

- 入口脚本：`exp_expert_lowrank/scripts/round3/run_round3_spectral_interference.py`
- 关键实现：
  - `compute_spectral_interference`：计算 SI；
  - `compute_margin_from_router_logits`：计算 margin；
  - `evaluate_spectral_interference`：按层汇总 SI 与 margin。
- 结果文件：
  - 单模型：`round3_spectral_interference/<model>/spectral_interference_with_margin.json`
  - 汇总：`round3_spectral_interference/spectral_interference_with_margin_summary.json`

## 5. Round0：下游任务表现（最终耗时评测）

### 5.1 实验目的

- 用统一任务集检验结构指标与真实任务性能的一致性。
- 作为 Round1-3 结构分析后的最终外部效能对照。

### 5.2 数据集与任务

- 评测框架：`lm_eval`
- 任务集合：`arc_easy, arc_challenge, piqa, hellaswag, openbookqa, winogrande, boolq`
- 评测口径：完整任务评测（无 `limit` 截断）

### 5.3 脚本实现位置

- 入口脚本：`exp_expert_lowrank/scripts/round0/run_round0_downstream_eval.py`
- 调度与汇总：
  - `router_eval/eval_methods/lm_eval/run_dispatch.py`
  - `router_eval/eval_methods/lm_eval/run_summary.py`
- 结果文件：
  - 单模型：`round0_downstream_fulltasks/<model>/lm_eval_results_step60000.json`
  - 汇总：`round0_downstream_fulltasks/round0_downstream_summary.csv`

## 6. 结果图与执行脚本

- 图输出脚本：`exp_expert_lowrank/scripts/round_12L/plot_round12l_comparison.py`
- 图输出目录：`/data/250010109/spectral_router/exp_expert_lowrank/docs/round_12L/ckpt60000/figures`
- 顺序执行脚本：`exp_expert_lowrank/scripts/round_12L/run_round12l_ckpt_eval.py`
