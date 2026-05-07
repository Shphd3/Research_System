# round_continual_2 实验说明与结果记录

## 1. 实验具体描述

- 实验对象：`/data/250010109/spectral_router/output_moe` 下全部可用模型（排除非 `acp_lite` 的 `acp_on` 命名模型，且必须存在 `checkpoint-40000`）。
- 实验目标：回答 `quadratic_nosvd_debias @ ckpt40000` 是否存在 learned variance routing。
- 实验类型：`mechanism_audit_before_cl`。
- 方法：对每个模型在同一批 WOS 样本上计算三项核心量：
  - `rho`：二阶项与一阶项 margin attribution 比值（仅 quadratic 可定义）
  - `NMI(E,C)`：expert assignment 与 domain 的归一化互信息
  - `r_{0.9}`：expert 内 covariance 达到 90% 能量所需秩

## 2. 结果产物与指标说明

- 输出目录：`/data/250010109/spectral_router/exp_TRACE/output/round_continual_2`
- 主要文件：
  - `run_plan.json`：本次运行的冻结配置与模型清单
  - `per_model_metrics.json`：每模型完整指标与逐层明细
  - `overall_summary.json`：聚合后的主表与决策结论
  - `analysis_report.md`：面向结论汇报的 Markdown 报告
  - `result_card.md`：Experiment -> Theory Result Card
  - `<model_name>/mechanism_metrics.json`：单模型明细指标

## 3. 运行命令

```bash
python /data/250010109/spectral_router/exp_TRACE/scripts/round_continual_2/run_round_continual_2.py \
  --config /data/250010109/spectral_router/exp_TRACE/configs/round_continual_2/ckpt40000_all_models.json
```

## 4. 核心结果表

| Alias | rho | NMI(E,C) | r_{0.9} | CV_load |
| --- | ---: | ---: | ---: | ---: |
| acp_lite | NA | 0.024682 | 74.541667 | 0.768128 |
| linear_no_center | NA | 0.004733 | 82.583333 | 0.761167 |
| linear_running_center | NA | 0.053235 | 67.583333 | 0.926735 |
| low_rank_running_center | NA | 0.024555 | 73.666667 | 0.799530 |
| quadratic_nosvd_debias | 0.151085 | 0.057678 | 68.083333 | 1.131160 |

## 5. 指标计算定义（含公式）

### 5.1 `rho`（quadratic only）

对每个 token 的 router logits 定义 margin：

$$
\mathrm{margin}(z)=z_{(1)}-z_{(2)}
$$

其中 $z_{(1)},z_{(2)}$ 是 logits 的前二大值。  
在 quadratic router 中把 logits 分解为：

$$
\ell(x)=W_1 x_c + W_2 q(x),\quad
q(x)=x_c\odot x_c-\lambda_t
$$

令

$$
m_1(x)=\mathrm{margin}(W_1 x_c),\quad
m_2(x)=\mathrm{margin}(W_2 q(x))
$$

逐层计算：

$$
\rho_{\text{layer}}=
\frac{\mathbb{E}(|m_2(x)|)}{\mathbb{E}(|m_1(x)|)}
$$

模型级别为所有 quadratic 层的均值：

$$
\rho_{\text{model}}=\mathrm{mean}_{l\in\mathcal{L}_{quad}}(\rho_l)
$$

### 5.2 `NMI(E,C)`

记 `E` 为 top1 expert assignment，`C` 为 domain label。先计算联合概率 $p(e,c)$ 与边缘分布 $p(e),p(c)$：

$$
I(E;C)=\sum_{e,c}p(e,c)\log\frac{p(e,c)}{p(e)p(c)}
$$

$$
H(E)=-\sum_e p(e)\log p(e),\quad
H(C)=-\sum_c p(c)\log p(c)
$$

$$
\mathrm{NMI}(E,C)=\frac{I(E;C)}{\sqrt{H(E)H(C)}}
$$

### 5.3 `r_{0.9}`

对某 expert 的 routed feature covariance $C_e$，其特征值（降序）为 $\lambda_1\ge\cdots\ge\lambda_d\ge0$，定义：

$$
r_{0.9}(e)=\min\left\{k:\frac{\sum_{i=1}^{k}\lambda_i}{\sum_{i=1}^{d}\lambda_i}\ge0.9\right\}
$$

模型报告值为按层、按 expert 的均值聚合（实现里先 expert 均值再层均值）。

### 5.4 `CV_{load}`

令 expert 负载分布 $p_e=\frac{n_e}{\sum_j n_j}$，专家数为 $E$，则

$$
\mu=\frac{1}{E},\quad
\sigma=\sqrt{\frac{1}{E}\sum_{e=1}^{E}(p_e-\mu)^2},\quad
CV_{load}=\frac{\sigma}{\mu}
$$

## 6. 代码实现映射（可直接给理论侧核对）

### 6.1 `rho` 实现

- 入口：`evaluate_one_model(...)` 中 quadratic 分支  
- 文件：`/data/250010109/spectral_router/exp_TRACE/scripts/round_continual_2/evaluate_round_continual_2.py`

```python
linear_logits = q_router.linear_router(x_router)
quad_logits = q_router.quadratic_router(x2)
m1 = compute_margin(linear_logits).detach().cpu()[valid_mask]
m2 = compute_margin(quad_logits).detach().cpu()[valid_mask]
rho_linear_sum[lid] += float(torch.sum(torch.abs(m1)).item())
rho_quad_sum[lid] += float(torch.sum(torch.abs(m2)).item())
rho_value = m2_mean / m1_mean if m1_mean > 0 else math.nan
```

### 6.2 `NMI(E,C)` 实现

- 函数：`compute_nmi(...)`  
- 文件：同上

```python
joint = np.zeros((num_experts, num_clusters), dtype=np.float64)
np.add.at(joint, (e, c), 1.0)
p_ec = joint / total
p_e = p_ec.sum(axis=1)
p_c = p_ec.sum(axis=0)
mi += float(p_ec[i, j] * np.log(p_ec[i, j] / (p_e[i] * p_c[j])))
nmi = mi / math.sqrt(max(h_e, 0.0) * max(h_c, 0.0))
```

### 6.3 `r_{0.9}` 实现

- 函数：`compute_r090_from_cov(...)`  
- 文件：同上

```python
eigvals = torch.linalg.eigvalsh(cov)
eigvals = torch.clamp(eigvals, min=0.0)
desc = torch.flip(eigvals, dims=[0])
csum = torch.cumsum(desc, dim=0)
k = int(torch.searchsorted(csum, torch.tensor(0.9 * total, device=csum.device)).item()) + 1
```

### 6.4 `CV_load` 实现

- 函数：`compute_cv_load(...)`  
- 文件：同上

```python
p = counts / total
mean = 1.0 / float(counts.shape[0])
std = float(np.sqrt(np.mean((p - mean) ** 2)))
return float(std / mean)
```

## 7. 预期与假设更新

- 机制判决规则要求 `rho > 1` 才能支持“二阶项主导 margin”。
- 本次 `quadratic_nosvd_debias` 的 `rho=0.151085`，未达到阈值。
- 当前结论：不支持该 checkpoint 已学到稳定 variance routing，暂不进入 two-task forgetting verdict。
