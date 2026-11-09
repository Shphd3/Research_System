# Execution Plan: R0/R1 Two-Pass Reverse Index Diagnostic

## 1. Run Goal

训练 2-layer diagnostic Transformer，并用 two-pass RI 评估：

```text
router bucket 取 KV 是否比 random same-count 更低 CE。
```

## 2. Data Construction

两套数据：

Uniform:

```text
ABC / DEF / GHI / JKL = 3900 / 3900 / 3900 / 3900
```

Zipf:

```text
ABC / DEF / GHI / JKL = 10000 / 5000 / 500 / 100
```

共同设置：

```text
vocab_size = 1000
corpus_length = 1000000
patterns = [1,2]->22, [3,4]->23, [6,7]->20, [8,9]->21
```

## 3. Model / Training Setup

模型：

```text
2-layer Transformer
layer1 attention_output -> top-1 router -> MoE FFN
layer2 full attention -> teacher attention
```

训练任务：

```text
NTP
```

训练变体：

```text
M0: L = L_NTP + 0.01 L_LB
M1: L = L_NTP + 0.01 L_LB + 0.05 L_feature_router
M2: L = L_NTP + 0.01 L_LB + 0.20 L_feature_router
```

其中：

$$
L_{\text{feature-router}}
=
\mathrm{CE}(\text{router logits at feature prefix-end}, \text{feature id})
$$

注意：这个 loss 使用 synthetic feature label，只是为了构造 soft feature-aligned router diagnostic，不是现实语言方法 claim。

## 4. Configs And Commands

Config:

```text
configs/r0_r1_two_pass_ri_uniform_zipf_soft_router.json
```

Script:

```text
scripts/run_two_pass_reverse_index_diagnostic.py
```

Run:

```bash
python scripts/run_two_pass_reverse_index_diagnostic.py \
  --mode full \
  --config configs/r0_r1_two_pass_ri_uniform_zipf_soft_router.json \
  --skip-completed
```

## 5. Metrics And Artifacts

主指标：

$$
\Delta CE
=
CE_{\text{candidate attention}} - CE_{\text{full attention}}
$$

越低越好。正数表示 candidate attention 比 full attention 更差。

和 random 的差：

$$
\mathrm{CEImprovement}_{RI-random}
=
\Delta CE_{\text{random}} - \Delta CE_{\text{RI}}
$$

正数表示 RI 比 random 更好。

其他指标：

```text
feature-expert NMI
candidate count
attention top-M recall
attention mass retained
attention output cosine
target probability delta
```

输出：

```text
aggregate_ri_summary_by_generator.csv
ri_vs_random_ce_summary.csv
figures/
```

## 6. Pass / Fail Criteria

Strong support:

- M1/M2 的 NMI 高；
- `ri_same_bucket` 的 CE delta 明显低于 random；
- RI 接近 local / same-feature oracle；
- uniform 和 Zipf 都成立。

Weak support:

- RI 比 random 好，但明显弱于 local / same-feature oracle；
- 只在 uniform 成立，Zipf 变弱；
- M1 有效，M2 过强正则反而变差。

No support:

- NMI 高但 RI CE delta 不优于 random；
- RI mass 提高但 CE 不降；
- local / same-feature oracle 远好于 router bucket。

## 7. Failure Modes To Check

- feature-router CE 太强，形成 clean routing 但扰乱 NTP；
- bucket candidate count 与 random 不匹配；
- dense attention 主要由 local 或 feature oracle 解释；
- Zipf 低频 feature 无法形成稳定候选；
- attention mass retained 提高但 logits/CE 没改善。

## 8. Result Location

Mainline-safe:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/R0_R1_two_pass_reverse_index_diagnostic/
```

Ignored workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
  outputs/r0_r1_two_pass_ri_uniform_zipf_soft_router_20260520/
  figures/r0_r1_two_pass_ri_uniform_zipf_soft_router_20260520/
```
