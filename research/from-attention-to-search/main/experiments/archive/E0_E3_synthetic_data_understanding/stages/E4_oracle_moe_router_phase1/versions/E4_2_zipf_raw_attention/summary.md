# 假设闭环：E4.2 Zipf Raw-Attention Oracle-MoE - 0519

## 1. 原始目的

uniform 数据已经说明：C7e 在 shortcut controls 中最接近 one-feature-one-expert reference。E4.2 要进一步问：

```text
如果 feature frequency 变成长尾，C7 系列还能不能保持 feature assignment、readback、expert utility 的一致性？
```

这是必要的，因为真实语言特征通常不是均匀出现；低频 feature 最容易被高频/common geometry 淹没。

## 2. 主线锚点与待判定假设

数据为 all-trigram Zipf/long-tail：

| feature | relation | count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

待判定假设：

```text
H4.2: 如果 C7 oracle-initialized prototype router 真的能提供稳定 routing reference，
那么在 Zipf 长尾频率下，它仍应保持较高 readback、feature-expert alignment、selected-best expert。
```

## 3. 直接结果

C0-C7e 在 Zipf 数据上均完成 5 seeds full run、D0-D7 behavior diagnostic、D* boundary audit。

主结果：

| variant | readback | feature-expert NMI | feature-boundary alignment | selects-best | top-shared energy |
|---|---:|---:|---:|---:|---:|
| C0 standard linear | 0.997 | 0.601 | 0.391 | 0.995 | 0.784 |
| C3 inhibition | 0.996 | 0.639 | 0.413 | 0.996 | 0.832 |
| C7d oracle-init + prototype losses | 0.994 | 0.819 | 0.283 | 0.990 | 0.540 |
| C7e oracle-init + performance feedback | 0.997 | 0.822 | 0.343 | 0.993 | 0.535 |

C7d/C7e 仍是最强 feature-aligned candidates。C7a random prototype 的 NMI 约 0.001，说明“prototype 形式本身”不足以产生 feature routing；oracle initialization 是关键。

## 4. 关键图片

![zipf core metrics](figures/e4_zipf_core_metrics.png)

这张图显示 Zipf 下 C7d/C7e 仍保持较高 feature-expert NMI 和 selected-best rate。

![zipf factor MI](figures/e4_zipf_factor_mi.png)

这张图用于检查 expert assignment 与 feature、target token、prefix token 等 audit variables 的关系。

![zipf top shared energy](figures/e4_zipf_top_shared_energy.png)

这张图显示 C7d/C7e 的 top-shared energy 低于 C0/C3/C4，但仍不为零；因此不能说 boundary 完全是纯 feature direction。

## 5. 解释

Zipf 结果支持 uniform closure 的主结论，但强度略弱：

```text
C7d/C7e 能在长尾频率下保留较高 feature assignment 和 utility alignment；
但低频条件下 readback 和 boundary purity 没有达到“完全干净”的程度。
```

这说明 oracle initialization 的价值不仅是 uniform shortcut artifact；它在长尾下仍有稳定作用。但它仍然不是自然 router 自发 specialization，也不是纯 feature-direction routing。

## 6. Claim 边界

支持：

- C7d/C7e 在 Zipf 长尾下仍明显优于 random prototype C7a。
- C7d/C7e 可以作为当前最强的 synthetic routing reference。

弱支持：

- C7d/C7e 在长尾下仍保持 `NMI≈0.82`，说明 feature assignment 有一定频率鲁棒性。

不能声称：

- 不能说低频 feature 已完全稳定分开。
- 不能说自然 MoE 不加 oracle init 就能做到。
- 不能说 boundary 已经纯粹对应语义方向；top-shared energy 仍明显存在。
- 不能直接说可以进入真实语言 Reverse Index。

## 7. 最弱点与下一步

最弱点：Zipf 中最低频 JKL 只有 100 次，虽然总体 NMI 较高，但仍需要 per-feature 低频稳定性分析，尤其看 JKL 是否跨 seed 稳定。

下一步：

1. 做 per-feature / per-seed stability table，专门看低频 feature；
2. 对 C7e 做 Reverse Index 前的 candidate-generator smoke，但 claim 必须限制在 synthetic reference router；
3. 若 low-frequency feature 不稳定，则需要增加低频增强或更强 routing reference。

## 8. 30 秒汇报版本

目的：uniform 下 C7e 看起来能按 feature 分 expert，我们要确认它在长尾频率下是否还成立。  
假设：如果 oracle-initialized prototype router 是可靠 routing reference，那么 Zipf 长尾下仍应保持 readback、feature-expert alignment 和 selected-best expert。  
结论：Zipf 下 C7d/C7e 仍是最强，NMI 约 0.82，readback 接近 1，selected-best 约 0.99；random prototype C7a 基本不行。  
证据：C7e 在 Zipf 中 `readback=0.997`、`NMI=0.822`、`selected-best=0.993`。  
边界：低频 feature 还不能说完全稳定；boundary 仍混有 common directions。下一步要做低频 per-feature 稳定性和 Reverse Index smoke。
