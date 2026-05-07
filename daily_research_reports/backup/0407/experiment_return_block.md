# Experiment Return Block (analysis_v6.6_paper_ready_20260407)

## Round 1: Token Decoupling & Expert Assignment

- 实验目标  
  在中等规模样本下复核 function/domain token 分发差异，并补齐 hybrid 三项 logit 记录。
- 实验步骤  
  固定 WoS 清单（1200 样本）→ 单-token清洗 → 在 `linear_running_center/acp_lite/hybrid` 统计 token assignment 与 hybrid 分项 logit。
- 实验结果  
  function: `44 -> 43`；domain: `127 -> 109`；function top-share 均值：`linear 0.5778 / acp 0.6036 / hybrid 0.6094`。
- 实验分析  
  function sink 倾向在 `acp_lite/hybrid` 更明显；hybrid 子空间项量级高于一阶项，但这不等价于语义路由已被严格证明。
- 更新了什么假设  
  H1/H7 增强；H8 获得中等支持但仍待词频分层。

## Round 2: Specialization Metric Tracking

- 实验目标  
  复核四模型 `rho_sep/sRank` 的相对关系，验证强 baseline 是否稳定。
- 实验步骤  
  四模型逐层抽取 `x_c + assignment`，每层计算 `rho_sep/sRank`，再做跨层均值。
- 实验结果  
  `rho_sep_mean`: `acp_lite 0.1015 > hybrid 0.0645 > linear_running_center 0.0615 >> linear_no_center 0.0060`。  
  `sRank_mean`: `acp_lite 66.09 > linear_running_center 55.33 > hybrid 43.77 > linear_no_center 30.31`。
- 实验分析  
  `acp_lite` separation 仍最强；`linear_no_center` 继续作为反例成立。
- 更新了什么假设  
  H1 继续增强；H3/H5 仍为部分支持。

## Round 3: Empirical Separation & Subspace Audit

- 实验目标  
  比较 KMeans 与 K-Subspaces 在六层上的几何解释力。
- 实验步骤  
  对每模型每层抽取 `12000` 个 `x_c`，分别执行 KMeans 与 K-Subspaces，比较 `rho_sep/avg_sRank`。
- 实验结果  
  三模型在六层均满足 `rho_sep(KMeans) > rho_sep(K-Subspaces)`（`6/6`）；`K-Subspaces` 未稳定给出更低 `avg_sRank`。
- 实验分析  
  当前口径更偏 mean-separable；“子空间聚类普遍更优”在本轮未获支撑。
- 更新了什么假设  
  H1 增强；H3 暂未强化。

## Round 4: Routing Logit Dynamics

- 实验目标  
  检查 hybrid 一阶/二阶分支是否出现单边梯度压制。
- 实验步骤  
  随机初始化 step0 起跑，训练 100 步，逐步记录 logit 均值方差与梯度 L2。
- 实验结果  
  `ratio_sub_to_first_order_grad` 区间 `[0.2756, 2.0896]`，均值 `0.8685`，中位数 `0.8183`；末步 `subspace_grad > centered_grad > mean_grad`。
- 实验分析  
  二阶分支并未全程饿死，更像“存在竞争与波动”的动态博弈。
- 更新了什么假设  
  H2 更新为“竞争存在但非单边压制”。

## Round 5: Overhead Audit

- 实验目标  
  用统一口径给出参数/FLOPs/latency 的工程代价证据。
- 实验步骤  
  六模型统一输入设置，统计参数与 FLOPs，并进行 warmup+12次测时。
- 实验结果  
  hybrid: `7.23M router params, 1.196M FLOPs/token, 36.61ms`。  
  quadratic_low_rank: `7.08M, 1.180M, 35.60ms`。  
  线性族: `73.7K, 6.1K, 26.28-33.27ms`；acp_lite: `221.2K, 15.4K, 32.75ms`。
- 实验分析  
  二阶/混合路线开销显著更高，论文中必须用 regime-specific 收益抵偿叙事。
- 更新了什么假设  
  regime-dependent necessity 的工程代价维度获得直接支撑。

## Current Decision Update

- `analysis_v6.6_paper_ready_20260407` 的 Round1-5 已完成。  
- 当前更稳妥叙事：  
  1. `acp_lite` 是强一阶基线；  
  2. covariance-aware 价值是 regime-dependent，而非 universal；  
  3. 对 “specialization -> low-rankness -> forgetting” 仍保持谨慎，不超额宣称。  
