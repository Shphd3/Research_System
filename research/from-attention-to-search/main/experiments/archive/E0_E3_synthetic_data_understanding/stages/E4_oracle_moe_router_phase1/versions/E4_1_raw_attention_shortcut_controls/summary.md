# 假设闭环：E4 Raw-Attention Oracle-MoE 与 Shortcut Controls - 0519

## 1. 原始目的

我们要验证一个更严格的问题：

```text
如果 MoE router 接收 raw attention_output，它能不能把 synthetic trigram feature 稳定分给不同 experts，
并且这种分配不是 prefix token / target token 的表面捷径？
```

本轮只讨论均匀 feature frequency。zipf 长尾版本单独闭环。

## 2. 主线锚点与待判定假设

主线锚点：前面 E2/E3 显示，模型能学到 feature readback，但自然 router 不一定按 feature 做 one-feature-one-expert。因此 E4 进一步问：如果采用 Oracle-MoE 设置，并引入 Dingyi-style oracle initialization，能不能构造一个可靠的 routing reference。

待判定假设：

```text
H4: 在 raw-attention Oracle-MoE 中，若 attention_output 已包含可聚类的 feature context 信息，
则 oracle-initialized prototype router 应比普通 router 更稳定地形成 feature-aligned functional specialization。
```

判断标准不是单独看 NMI，而是同时看四件事：

- feature prefix 下能否 readback target；
- feature 是否稳定映射到 expert；
- router boundary 是否与 feature direction 有一定对齐；
- router 选中的 expert 是否也是 forced-routing 下最有用的 expert。

## 3. 直接结果

四个 uniform 数据集均已完成 C0-C7e full run 与诊断：

| 数据集 | 控制目的 | 结果 |
|---|---|---|
| `unique_uniform` | 标准四 feature 数据 | C7e 最强，NMI 0.920，readback 1.000 |
| `shared_b_uniform` | 排除 prefix-end token shortcut | C7e 仍强，NMI 0.919，readback 1.000 |
| `shared_target_uniform` | 排除 target token shortcut | C7e 仍强，NMI 0.893，readback 1.000 |
| `crossed_factorial_uniform` | 同时打散 first token / end token / target token | C7e 仍保持 NMI 0.834，readback 1.000 |

关键对照：

- C0-C6 大多能 readback，但在 shortcut controls 中 feature-expert NMI 不稳定。
- C7a random prototype 几乎不能形成 feature assignment。
- C7b/C7c 说明 oracle center 初始化本身有效，但还不总是最稳。
- C7e 在四个数据集上同时保持高 readback、高 feature assignment、高 selected-best rate，是当前最强 routing reference。

## 4. 关键图片

![core metrics](figures/e4_uniform_shortcut_core_metrics.png)

这张图显示：C7e 在四个 shortcut 数据集上同时保持 readback、feature-expert NMI、selected-best rate。

![factor MI](figures/e4_uniform_shortcut_factor_mi.png)

这张图用于检查 expert assignment 与 feature、target token、prefix token 等 audit variables 的关系。它提示 unique 数据上的解释会受 token/target 绑定影响，因此必须看 crossed-factorial。

![top shared energy](figures/e4_uniform_shortcut_top_shared_energy.png)

这张图显示：即使 C7e 功能上最好，router boundary 仍有较高 top shared energy；因此不能说它纯粹沿 feature direction 切分。

## 5. 解释

本轮最重要的结果不是“所有 MoE 都会自然分开”，而是：

```text
普通 router 不稳定；
oracle-initialized prototype router 可以把已经存在的 feature-related regions 固定成较稳定 expert basins；
其中 C7e 在 shortcut-controlled uniform 数据上最接近 one-feature-one-expert reference。
```

这推进了我们的理解：router specialization 不是 representation separability 的自动结果。需要把 feature-related region 转成 router 可用的中心或反馈结构，才更容易形成稳定分配。

## 6. Claim 边界

支持：

- 在 controlled uniform trigram 数据上，C7e 可以形成接近 one-feature-one-expert 的功能性路由 reference。
- 这个结论不是单靠 NMI，因为 C7e 同时满足 readback 和 selected-best expert。

弱支持：

- C7e 的分配在 crossed-factorial 中仍保持，说明它不只是简单 prefix-end token 或 target token shortcut。

不能声称：

- 不能说自然 top-1 router 会自发发现 relation-level feature。
- 不能说 C7e 的 boundary 是纯 feature direction；top shared energy 仍高。
- 不能说真实语言 MoE 会复现该结果。
- 不能说 zipf 长尾下也成立，zipf 还在训练。

## 7. 最弱点与下一步

最弱点：C7 使用 oracle initialization，仍依赖 synthetic feature-position 信息；它是 routing reference，不是自然发现机制。此外，uniform frequency 比长尾数据更容易。

下一步：

1. 继续监督 zipf C0-C7e full run；
2. 写单独 zipf closure；
3. 若 C7e 在 zipf 中仍保持 readback、feature assignment、utility alignment，再把 C7e 作为 Reverse Index 前的 routing reference。

## 8. 30 秒汇报版本

目的：我们想知道 MoE router 能不能按 synthetic feature 做稳定的一 feature 一 expert，而不是只靠 token 捷径。  
假设：如果 attention output 里已经有 feature 区域，用 oracle-initialized prototype router 应该能把这些区域固定成专家分工。  
结论：均匀分布下，普通 C0-C6 不稳定；C7e 最接近目标，在 shared-token、shared-target、crossed-factorial 控制下仍能 readback，并保持较高 feature-expert alignment。  
证据：C7e 在 crossed-factorial 中 `readback=1.000`、`NMI=0.834`、`router_selects_best=1.000`。  
边界：这不是自然 router 自发发现，也不是纯 feature direction 切分；下一步要看 zipf 长尾是否还能保持。
