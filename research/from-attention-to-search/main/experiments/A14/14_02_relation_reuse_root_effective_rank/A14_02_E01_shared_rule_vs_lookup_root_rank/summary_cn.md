---
experiment_id: A14_02_E01_shared_rule_vs_lookup_root_rank
status: completed_insufficient
verdict: insufficient
run_id: a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427
job_id: pt-q6hu0fq5
canonical_source: summary.md
---

# A14_02_E01 共享规则与 Lookup 根状态功能秩：结果摘要

主子锚点：
[A14_02 任务根状态功能秩](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)

协议：[English](protocol.md) · [中文](protocol_cn.md)

## 直接结论

**预注册主问题的正式判定是 `insufficient`（证据不足）。**

低曝光主对比的两组都把训练条目记到了 100% accuracy，却都没有学会在新
context 中保持答案：

- `shared_unique`：0/5 seeds 通过能力门，test accuracy 均值 0.179；
- `lookup_unique`：0/5 seeds 通过能力门，test accuracy 均值 0.088。

因此，自动结果中包括 `-36` 方向在内的主秩差**不能解释为科学结果**。完整
状态本身都不能完成任务时，“保留任务需要多少方向”没有有效含义。

## 本次真正确定的认识更新

1. **重复次数本身不够；跨上下文多样性是形成新 context 不变性的必要条件。**
   `shared_repeat_duplicate` 虽然训练 accuracy 为 1.0，但 0/5 通过能力门，
   test accuracy 均值只有 0.199。相同曝光次数下，`shared_repeat_diverse`
   有 4/5 seeds 通过；通过者 test accuracy 均值为 0.991。

2. **任务可解时，独立 lookup 映射越多，ROOT 功能秩越高。**固定曝光和
   context 多样性后，`K=1/4/16` 三组均为 5/5 通过，post-norm ROOT 功能秩
   均值依次为 **10.2、11.0、12.8** 个方向。

3. **高曝光 shared 相对 lookup 的压缩只能视为线索，不能升级为结论。**
   在双方都通过的 4 个配对 seed 中，`lookup K=16 - shared` 的秩差为
   4、3、1、2，均值 2.5，低于冻结的 4 方向阈值；shared 还有 1/5 seed
   训练失败。更关键的是，通过能力门的四个 shared seed 在未见组合上的
   accuracy 仅为 0.547、0.063、0.250、0.516，全部低于 0.80。因此不能说
   模型已经学会共享组合算法。

## 中心图

![能力门与能力过滤后的功能秩](capability_and_functional_rank.png)

左图先回答任务是否真正学会；右图只在通过能力门的运行中比较功能秩，避免
把任务失败造成的数字误读为“低秩”。

## 能力过滤后的关键数字

| 条件 | 能力门 | Held-out accuracy | Post-norm ROOT 功能秩 |
| --- | ---: | ---: | ---: |
| Shared，`F=1` | 0/5 | 0.179，全部 seeds | 不可解释 |
| Lookup `K=16`，`F=1` | 0/5 | 0.088，全部 seeds | 不可解释 |
| Shared，`F=8`，重复相同 context | 0/5 | 0.199，全部 seeds | 不可解释 |
| Shared，`F=8`，多样 context | 4/5 | 0.991，通过 seeds | 10.25 |
| Lookup `K=1`，`F=8`，多样 context | 5/5 | 1.000 | 10.20 |
| Lookup `K=4`，`F=8`，多样 context | 5/5 | 1.000 | 11.00 |
| Lookup `K=16`，`F=8`，多样 context | 5/5 | 1.000 | 12.80 |

## 守卫审计

- 数据生成和匹配守卫通过，35/35 个 condition-seed 任务完整结束。
- 打乱 ROOT 状态后，通过能力门的任务 accuracy 平均下降 0.925--0.946，
  CE 增加 8.90--10.28 nat，说明该状态确实被任务使用。
- 在选定秩下，通过能力门的所有运行中，同秩随机子空间通过率均为 0；
  学得子空间并非任意投影。
- 满秩重放的冻结阈值在 16/35 runs 中被超过。19 个能力通过运行中只有
  1 个略超阈值：\(1.16\times10^{-5}\)，阈值为 \(1.00\times10^{-5}\)。
  该量级符合 float32 满基重建误差，但按冻结合同，硬门仍记为失败。

## Claim Boundary

现在可以说：

> 在这项合成 NTP 任务中，单纯增加相同样本的出现次数并不能形成跨 context
> 稳定的任务根状态；多样 context 暴露是必要条件。对已经学会的 lookup
> 任务，独立映射数从 1 增到 16 时，任务所需 ROOT 方向数同步上升。

现在不能说：

- 低频共享组合会降低 ROOT 功能秩；
- 模型已学会共享组合算法；
- 频率单独导致低秩；
- lookup 规则数与秩存在普适定律；
- 自然语言天然是低秩树；
- 该结果已经支持某种 Router。

## 唯一下一决策

决定是否修订 A14_02：先单独完成能力校准，使 shared 与 lookup 都通过新
context 能力门，并要求 shared 的未见组合 accuracy 通过，再开始解释任何
秩差。

