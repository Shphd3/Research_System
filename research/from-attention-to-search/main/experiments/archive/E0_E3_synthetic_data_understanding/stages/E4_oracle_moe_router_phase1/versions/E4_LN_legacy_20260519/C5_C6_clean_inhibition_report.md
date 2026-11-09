# C5/C6 Clean Inhibition Report

## 1. 实验目的

本实验只回答一个问题：

```text
clean inhibition 能不能帮助 expert 形成更真实的 functional specialization？
```

旧版 C3/C4 的 inhibition 会重新前向每个 expert，并让梯度可能穿过 shared path、router、LN 和 LM head。因此它可以说明“排他性是否出现”，但不能干净说明“other experts 是否被单独反向排斥”。

C5/C6 修正为 expert-only clean inhibition：主 NTP 路径正常更新 selected expert 和 shared path；inhibition 辅助项只更新 other experts。

## 2. 方法定义

令 router 选择的 expert 为：

$$
e^\* = \arg\max_e \mathrm{router\_logit}_e
$$

主任务仍然是：

$$
L_{\mathrm{NTP}}=\mathrm{CE}(y, f(x;e^\*))
$$

clean inhibition 使用 detached shared representation：

$$
h_{\mathrm{detach}}=\mathrm{stopgrad}(h)
$$

对每个非选中 expert：

$$
L_{\mathrm{clean-inhibit}}
=
\frac{1}{E-1}
\sum_{e\neq e^\*}
\max(0,\ m-(\mathrm{CE}_e-\mathrm{CE}_{e^\*}^{\mathrm{ref}}))
$$

其中 $\mathrm{CE}_{e^\*}^{\mathrm{ref}}$ 只作为 detached reference，不给 selected expert 或 shared path 额外梯度。

本地 smoke 的梯度检查：

| variant | shared grad norm | expert grad norm |
|---|---:|---:|
| C5 | 0.0000 | 0.0170 |
| C6 | 0.0000 | 0.0134 |

这说明 clean inhibition 辅助项只更新 expert 参数。

## 3. 训练与诊断

主实验使用 LB：

| ID | 名称 | 结构 |
|---|---|---|
| C5 | `linear_clean_expert_inhibition` | linear router + clean inhibition |
| C6 | `center_clean_expert_inhibition` | trainable center + repulsion + clean inhibition |

no-LB 只作为消融：

| ID | 名称 |
|---|---|
| C5-noLB | `linear_clean_expert_inhibition_no_lb` |
| C6-noLB | `center_clean_expert_inhibition_no_lb` |

运行记录：

- C5/C6 LB full run：`pt-vpz17hmx`，5 seeds，成功。
- C5/C6 no-LB ablation：`pt-f0r8jlf2`，3 seeds，成功。
- D* 诊断：`pt-fell1avk` 生成了全部可用诊断；ACP 状态为 failed 是因为 no-LB 只训练 3 seeds，但诊断请求包含 seed16/17，实际可用结果完整。

## 4. 主表：LB Variants

| variant | loss | readback | NMI | selected-best | CE gap | inhibition gap | violation | boundary align | top energy | load entropy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C0 | 6.643 | 0.9999 | 0.462 | 0.999 | 0.0000 | - | - | 0.312 | 0.786 | 0.556 |
| C1 | 6.641 | 0.9998 | 0.773 | 0.295 | 2.2010 | - | - | 0.099 | 0.289 | 0.849 |
| C2 | 6.642 | 1.0000 | 0.663 | 1.000 | 0.0000 | - | - | 0.334 | 0.798 | 0.618 |
| C3 | 6.660 | 1.0000 | 0.685 | 0.995 | 0.0002 | 3.967 | 0.0187 | 0.355 | 0.885 | 0.929 |
| C4 | 6.658 | 0.9999 | 0.364 | 0.996 | 0.0001 | 4.007 | 0.0002 | 0.278 | 0.923 | 0.518 |
| C5 | 6.651 | 0.9999 | 0.346 | 1.000 | 0.0000 | 3.414 | 0.0000 | 0.112 | 0.124 | 0.416 |
| C6 | 6.652 | 0.9999 | 0.697 | 1.000 | 0.0000 | 2.648 | 0.0000 | 0.087 | 0.053 | 0.684 |

解释：

- C5/C6 的 selected-best rate 都达到 1.0，CE gap 为 0，说明 router 选中的 expert 确实是 forced-routing 下最会做该样本的 expert。
- C5/C6 的 inhibition violation 为 0，说明 clean inhibition 成功拉开 selected expert 与 other experts 的 CE 差距。
- C5 的 feature-expert NMI 低，C6 的 NMI 较高；但两者 boundary align 都低，说明 clean inhibition 改善的是 functional utility，不是明确把 boundary 拉到人工 feature direction。
- C5/C6 的 top shared energy 比 C0-C4 低很多，但这不能单独解释为 feature routing，因为 boundary-feature alignment 仍然弱。

## 5. no-LB 消融

| variant | loss | readback | NMI | selected-best | inhibition gap | violation | load entropy | dead experts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C5-noLB | 6.647 | 1.0000 | 0.000 | 1.000 | 2.414 | 0.0758 | 0.000 | 3.0 |
| C6-noLB | 6.647 | 1.0000 | 0.000 | 1.000 | 2.647 | 0.0000 | 0.000 | 3.0 |

解释：no-LB 下 readback 仍然成功，但 expert allocation collapse 到极少数 expert，feature-expert NMI 接近 0。因此 clean inhibition 不能替代 LB 来维持可用 expert allocation。

## 6. 关键图

![C0-C6 main alignment utility](../../figures/c5_c6_main_alignment_utility.png)

![C0-C6 boundary geometry](../../figures/c5_c6_boundary_geometry.png)

![Clean inhibition gap](../../figures/c5_c6_clean_inhibition_gap.png)

![LB vs no-LB ablation](../../figures/c5_c6_lb_vs_nolb_ablation.png)

![Selected minus best CE](../../figures/c5_c6_selected_minus_best_ce.png)

## 7. 结论

clean inhibition **能增强 functional exclusivity**：C5/C6 都让 selected expert 成为 best forced expert，并且把 other experts 的 CE 拉高。

但 clean inhibition **还不能证明 clean one-feature-one-expert specialization**：C5 的 feature assignment 很弱，C6 的 assignment 较强但 boundary-feature alignment 仍弱。因此当前更安全的说法是：

```text
clean inhibition improves expert utility separation, but it does not by itself prove relation-level feature-aligned routing.
```

## 8. Claim Boundary

可以说：

- C5/C6 的 clean inhibition 梯度链路更干净；
- clean inhibition 可以让 selected expert 相对 other experts 形成更强功能优势；
- no-LB 下会 collapse，说明 LB 仍是维持 expert allocation 的关键条件。

不能说：

- natural router 已经学会 relation-level one-feature-one-expert；
- NMI 高就等于 functional specialization；
- clean inhibition 已经足以推进 Reverse Index。

## 9. 下一步

暂不进入 Reverse Index。下一步仍应做 E4.1 shortcut-controlled Oracle-MoE：

- shared prefix-end；
- shared target；
- crossed-factorial relation；
- raw `attention_output` router 对照。

只有在 shortcut controls 下仍同时满足 feature assignment、boundary alignment、utility diagonality 和 readback，才推进 Reverse Index。
