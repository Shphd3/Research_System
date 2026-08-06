# Phase8p2：Formal Matched-Forgetting 裁决报告

## 0. 一页结论

这轮不是新结构探索，而是在已经由 `Phase8-smoke` 和 `Phase8.1` 锁定的设置上，做一次正式的 continual-learning 裁决：

- 固定 expert input = `u50_ext`
- 固定 `U = 8`
- 只比较 `G0 / G2_u50_ext / G4_u50_ext / G0_ER`
- 主问题是：在学到同样多新知识时，结构组是否比 `G0` 忘得更少，以及它们是否接近或超过 `G0_ER`

最终 gate 是：

- `Gate A (G2_u50_ext > G0) = True`
- `Gate B (G4_u50_ext > G2_u50_ext) = False`
- `Gate C (best structure vs G0_ER) = near_but_below`

这轮最稳的结论是：

1. `u50_ext` 上的 split-dense 结构已经给出了真实 CL 价值，不再只是静态表征信号。
2. routed 版本 `G4_u50_ext` 在 fixed-budget `RAS` 上略强，但在 matched forgetting 和 `ReachRate` 上没有稳定赢过 `G2_u50_ext`，所以 routing 的额外 CL 价值当前还不稳。
3. 当前最优结构已经接近 `G0_ER`，但还不能宣称超过 replay baseline。

一句话压缩为：

$$
\text{今晚这轮已经支持 factorized } u50\_ext \text{ block 进入正式 CL 主线，但还不支持“routing 明显优于 split-dense”或“结构已经超过 replay”。}
$$

## 1. 固定协议

这轮严格锁死以下设置，没有再开 band、layer、`U` 或更多结构：

- model: `Qwen3-0.6B`
- layer: `8`
- hook: `post_attention_layernorm`
- expert input: fixed `u50_ext`
- old domains: `CS, Civil, MAE, Medical, Psychology`
- new domains: `ECE, biochemistry`
- support: `1 support chunk of 256 tokens`
- query: `16 query chunks of 256 tokens`
- replay token count = support token count
- `gamma = 1`
- adaptation horizon: `U = 8`
- lr multiplier only: `0.5x / 1.0x`
- seeds: `20260418 / 20260419 / 20260420`

并且沿用 `Phase8.1` 已锁定的共享 calibration：

- same `\mu`
- same `V_16`
- same `r95`

## 2. 比较组与参数更新规则

今晚只跑四组：

- `G0 = baseline_ffn`
- `G2_u50_ext = split_dense_u50_ext`
- `G4_u50_ext = raw_router_expert_u50_ext`
- `G0_ER = baseline_ffn_replay`

冻结规则保持一致：

- backbone、非第 8 层、attention、LN、LM head、projector、common branch 全冻结

仅更新：

- `G0 / G0_ER`：replacement FFN
- `G2_u50_ext`：tail branch
- `G4_u50_ext`：router + tail experts

`G0_ER` 的 old-stage 直接复用同 seed 的 `G0` old-stage checkpoint；差异只发生在 adaptation loss。

## 3. 参数公平性

这轮同时报告 old-stage 和 adaptation-stage 的可训练参数量，而不是只报总参数量。

| Group | LR | Old-Stage Params | Adaptation-Stage Params | Ratio vs G0 |
|---|---:|---:|---:|---:|
| `G0` | `0.5x / 1.0x` | `9,437,184` | `9,437,184` | `1.0000` |
| `G0_ER` | `0.5x / 1.0x` | `9,437,184` | `9,437,184` | `1.0000` |
| `G2_u50_ext` | `0.5x / 1.0x` | `9,437,184` | `9,437,184` | `1.0000` |
| `G4_u50_ext` | `0.5x / 1.0x` | `9,441,280` | `9,441,280` | `1.0004` |

因此这轮比较里：

- `G2_u50_ext` 与 `G0` 完全等参
- `G4_u50_ext` 只比 `G0` 多 `0.0434%`

所以当前结论不依赖明显的参数量偏置。

## 4. 主表

主裁决只看最稳的 `0.5x` regime，因为：

- `1.0x` 下 `G0 / G0_ER / G2_u50_ext` 都掉回负 `RAS`
- `G4_u50_ext @ 1.0x` 虽然 `LG > 0`，但 `ReachRate = 0`
- 因而 formal CL 比较最有解释力的点仍然是 `0.5x`

### 4.1 `0.5x` 主结果

| Group | Fixed-Budget LG | Fixed-Budget FC | Fixed-Budget RAS | ReachRate | Matched Forgetting | WoS-Old Rare FC | New Middle LG | New Rare LG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `G0` | `-0.000251 ± 0.000547` | `0.000786 ± 0.000305` | `-0.001121 ± 0.000767` | `0.450 ± 0.132` | `-0.000017 ± 0.000234` | `0.003577 ± 0.001948` | `-0.000867 ± 0.000448` | `0.000868 ± 0.001287` |
| `G0_ER` | `0.000774 ± 0.000340` | `-0.000282 ± 0.000336` | `0.000571 ± 0.000442` | `0.367 ± 0.104` | `-0.000502 ± 0.000299` | `0.001474 ± 0.001734` | `0.000448 ± 0.000334` | `0.002247 ± 0.000446` |
| `G2_u50_ext` | `0.000803 ± 0.000539` | `0.000082 ± 0.000415` | `0.000503 ± 0.000766` | `0.217 ± 0.153` | `-0.000212 ± 0.000192` | `0.002881 ± 0.000431` | `0.000643 ± 0.000460` | `0.001148 ± 0.001557` |
| `G4_u50_ext` | `0.000785 ± 0.000345` | `-0.000122 ± 0.000205` | `0.000671 ± 0.000395` | `0.200 ± 0.180` | `-0.000184 ± 0.000158` | `0.001193 ± 0.001591` | `0.000681 ± 0.000213` | `0.000452 ± 0.000916` |

### 4.2 `1.0x` 的作用

`1.0x` 主要起到了一个边界确认作用：

- `G0 @ 1.0x`：明显过冲，`LG < 0` 且 `FC` 很高
- `G0_ER @ 1.0x`：也没有救回 formal CL 区间
- `G2_u50_ext @ 1.0x`：比 `G0` 稳，但仍没有回到正 `RAS`
- `G4_u50_ext @ 1.0x`：fixed-budget `LG` 仍略正，但 `ReachRate = 0`

所以这轮真正可用于正式 matched-forgetting 裁决的仍然是 `0.5x`。

## 5. Gate 判读

### 5.1 Gate A：`G2_u50_ext` 是否优于 `G0`

答案是：**是**。

关键证据有三条：

1. `G2_u50_ext` 的 fixed-budget `LG` 从负变正：
   - `G0`: `-0.000251`
   - `G2_u50_ext`: `0.000803`

2. `G2_u50_ext` 的 forgetting 更低：
   - `G0` 的 fixed-budget `FC = 0.000786`
   - `G2_u50_ext` 的 fixed-budget `FC = 0.000082`

3. `G2_u50_ext` 的 matched forgetting 更优：
   - `G0`: `-0.000017`
   - `G2_u50_ext`: `-0.000212`

因此，这轮已经可以写出：

$$
\text{在固定 } u50\_ext \text{ 与 } U=8 \text{ 的 protocol 下，split-dense block 相对 dense baseline 给出了真实 CL 价值。}
$$

### 5.2 Gate B：`G4_u50_ext` 是否优于 `G2_u50_ext`

答案是：**当前还不能成立**。

原因是：

- `G4_u50_ext` 的 fixed-budget `RAS` 略高：
  - `G2_u50_ext`: `0.000503`
  - `G4_u50_ext`: `0.000671`

但它没有同时在更关键的 CL 指标上稳定占优：

- matched forgetting 没有比 `G2_u50_ext` 更好：
  - `G2_u50_ext`: `-0.000212`
  - `G4_u50_ext`: `-0.000184`

- `ReachRate` 也没有更高：
  - `G2_u50_ext`: `0.217`
  - `G4_u50_ext`: `0.200`

这意味着当前只能说：

$$
\text{routing 版本在 fixed-budget score 上有弱优势，但它的额外 CL 价值还没有在 matched forgetting 口径下稳定成立。}
$$

### 5.3 Gate C：最佳结构是否接近或超过 `G0_ER`

答案是：**接近，但还低于 replay baseline**。

当前最优结构是 `G4_u50_ext @ 0.5x`。  
它与 `G0_ER @ 0.5x` 的关系是：

- fixed-budget `RAS`：
  - `G4_u50_ext`: `0.000671`
  - `G0_ER`: `0.000571`
  - 这里 `G4` 略高

- matched forgetting：
  - `G4_u50_ext`: `-0.000184`
  - `G0_ER`: `-0.000502`
  - 这里 `G0_ER` 明显更好

- `ReachRate`：
  - `G4_u50_ext`: `0.200`
  - `G0_ER`: `0.367`
  - 这里也是 `G0_ER` 更强

所以 Gate C 的合理表述不是“结构超过 replay”，而是：

$$
\text{最佳结构已经在 fixed-budget 评分上接近 replay，但在更严格的 forgetting / reach 口径下仍低于 replay。}
$$

## 6. 当前到底成立了什么

### 6.1 已成立

1. `u50_ext` 方向已经不仅是表征猜想，而是进入了真实 CL 训练收益。
2. `G2_u50_ext` 相对 `G0` 的优势是当前最稳的单层结构结论。
3. `G4_u50_ext` 是当前 fixed-budget 指标下的最优结构，但其“routing 额外收益”尚未被 matched forgetting 稳定支持。

### 6.2 还不能成立

1. 还不能写成：

$$
\text{raw-router expert 在 CL 中已经显著优于 split-dense。}
$$

2. 还不能写成：

$$
\text{结构组已经超过 simple replay baseline。}
$$

3. 这轮也不是 hierarchy、band search 或更多 router 变体的证据。

## 7. 失败与异常

`failures.csv` 为空，这轮没有被静默丢弃的失败实验。

需要明确保留的一点是：

- `1.0x` 不是“失败 run”，而是正式比较中的负结果
- 它的科学含义是：当前裁决仍然主要站在 `0.5x` 这个稳定 regime 上

## 8. 下一步最自然应该做什么

这轮最自然的下一步不是 hierarchy，也不是重新开 band，而是：

1. 保留 `G2_u50_ext` 作为当前最稳的 formal CL 强基线。
2. 继续检查 `G4_u50_ext` 的优势到底能否通过更合理的 router calibration / CL-aware router 稳定下来。
3. 在进入更复杂结构之前，先把“routing 是否真的带来额外 CL 价值”这条线钉实。

因此当前最稳的主线应写成：

$$
\text{u50\_ext factorized block} \rightarrow \text{formal CL value established}
$$

而不是：

$$
\text{routing advantage established} \quad \text{or} \quad \text{hierarchy ready}
$$

## 9. 图

- ![lg_curve](./figures/lg_curve.png)
- ![fc_curve](./figures/fc_curve.png)
- ![ras_bar](./figures/ras_bar.png)
- ![matched_forgetting_bar](./figures/matched_forgetting_bar.png)
- ![reachrate_bar](./figures/reachrate_bar.png)
