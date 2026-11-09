# D* Router Boundary Direction Audit - Detailed Notes

## 1. Source Runs

D* 汇总了两组主要诊断：

- uniform / raw-attention C-series:
  `Attention_Search_Experiments/active/synthetic_data_understanding/outputs/router_behavior_raw_attn_dingyi_c7_20260519/c_boundary_direction_audit/analysis.md`
- Zipf / raw-attention C-series:
  `Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e4_zipf_raw_attn/router_behavior_raw_attn_c0_c7_20260519/c_boundary_direction_audit/analysis.md`

这些运行产物在 ignored workspace 中；本文件夹只保留 report-ready 的结论和图。

## 2. What D* Measures

### Feature direction

对每个 feature 收集 prefix-end 位置的 `attention_output`，取中心：

$$
c_f = \mathrm{mean}(z_t \mid f)
$$

两个 feature 的方向为：

$$
d_{f,f'} = \frac{c_f - c_{f'}}{\|c_f - c_{f'}\|}
$$

### Router boundary

对 linear router，expert 之间的边界方向为：

$$
b_{e,e'} = \frac{W_e - W_{e'}}{\|W_e - W_{e'}\|}
$$

对 center router，边界方向为：

$$
b_{e,e'} = \frac{c_e - c_{e'}}{\|c_e - c_{e'}\|}
$$

D* 计算 $d_{f,f'}$ 与 $b_{e,e'}$ 的 cosine，用来判断 router 是否沿 feature 差异方向切空间。

### SVD band energy

对 collected `attention_output` 做 PCA / SVD，把 router boundary 投影到不同谱段：

- top shared: 前 25% 主方向，通常代表 common / 高频 / 大方差方向；
- middle: 25%-75%；
- tail: 后 25%。

如果 router boundary 能量集中在 top shared，说明它主要沿 common geometry 切；如果更多在 middle / tail，说明它可能使用更细的区分方向。

### Utility alignment

对每个 feature 强制走每个 expert，比较哪个 expert 的 CE 最低。`router-selects-best` 表示 router 选中的 expert 是否也是 forced-routing 下最有用的 expert。

## 3. Key Numbers

### Uniform

| variant | feature-boundary alignment | top | middle | tail | selected-best |
|---|---:|---:|---:|---:|---:|
| C0 | 0.375 | 0.787 | 0.163 | 0.049 | 0.993 |
| C1 | 0.115 | 0.313 | 0.445 | 0.242 | 0.621 |
| C3 | 0.391 | 0.853 | 0.098 | 0.049 | 0.996 |
| C4 | 0.303 | 0.916 | 0.077 | 0.007 | 0.989 |
| C7d | 0.384 | 0.743 | 0.189 | 0.068 | 1.000 |
| C7e | 0.413 | 0.728 | 0.187 | 0.085 | 1.000 |

### Zipf

| variant | feature-boundary alignment | top | middle | tail | selected-best |
|---|---:|---:|---:|---:|---:|
| C0 | 0.391 | 0.784 | 0.169 | 0.047 | 0.995 |
| C1 | 0.107 | 0.289 | 0.482 | 0.229 | 0.304 |
| C3 | 0.413 | 0.832 | 0.123 | 0.045 | 0.996 |
| C4 | 0.278 | 0.930 | 0.053 | 0.017 | 0.996 |
| C7d | 0.283 | 0.540 | 0.191 | 0.269 | 0.990 |
| C7e | 0.343 | 0.535 | 0.369 | 0.096 | 0.993 |

## 4. Figure Index

- `figures/uniform_boundary_feature_alignment.png`: uniform 中各 C 变体的 feature-boundary alignment。
- `figures/uniform_boundary_band_energy.png`: uniform 中 router boundary 的 top / middle / tail 能量。
- `figures/uniform_boundary_alignment_vs_utility.png`: uniform 中 boundary alignment 与 selected-best 的关系。
- `figures/zipf_boundary_feature_alignment.png`: Zipf 中 feature-boundary alignment。
- `figures/zipf_boundary_band_energy.png`: Zipf 中 top / middle / tail 能量。
- `figures/zipf_boundary_alignment_vs_utility.png`: Zipf 中 boundary alignment 与 selected-best 的关系。

## 5. Interpretation Boundary

D* 能说明 router boundary 使用了哪些方向，以及这些方向是否和 feature / utility 对齐。

D* 不能单独说明真实语言语义，也不能单独证明 Reverse Index 会成功。
