---
experiment_id: A15_05_05_E01_2b_matched_band_dispatch
status: completed_fail_distribution_only
created: 2026-07-31
approval_date: 2026-07-31
primary_anchor: 15_05_05_matched_fixed_band_dispatch
canonical_protocol: protocol.md
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
resource_profile: 5090-8-spot
result: summary_cn.md
---

# Protocol 中文伴随版：九臂 2B 匹配频带分发训练

## 0. Approval Snapshot

**执行结果（2026-07-31）：** 九个条件均完成 step 2544（2.000683B nominal
tokens）。四个真实频带都改变了固定 token 的专家分发，但相对 native 的配对
held-out NLL 均严格更差。head 优于 random64、但仍输给 native；middle 与
middle+tail 输给同维随机；tail 与 random448 无法区别。注册裁定为
**Fail / distribution-only**。见 [summary_cn.md](/Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary_cn.md)。

研究者明确授权无需再次审批，直接实现、提交多个 8×5090 作业并完成 2B 训练。
本实验不是被旧 compatibility gate 解锁；它是新的完整因果消融。

## 1. Terminology / Definitions

`band-only` 表示 Gate 只用冻结频带内的 token 变化，但 experts 仍接收完整表示。
真实频带 H/M/T/N 分别为 ranks 1--64、65--320、321--768、65--768；每个都有
独立同维 Haar random。`matched branch` 表示 model、optimizer、scheduler、
data cursor 与 RNG 全部来自同一个 step-800 checkpoint。

## 2. Anchor Alignment

主指标是 2B 共同终点 DCLM held-out NLL。固定 token 的 route disagreement 是
必须通过的 manipulation check；它只证明分发被改变，不能替代质量指标。

## 3. Tested Hypothesis

至少一个真实频带既改变分发，又相对 native 与同维 random 降低 held-out NLL。
若只改变分发而不改善 NLL，裁定“几何有效、功能无收益”。

## 4. Rival Explanations

同维 random 排除普通降维；load/overflow/drop 排除负载伪影；共同 branch、数据
与实测 FLOPs 排除初始化/计算差；frozen/current overlap 检查谱身份是否失效。

## 5. Data / Model / Algorithm / Objective

- 训练：DCLM shard 01；独立 DCLM held-out 1024 documents。
- 解释性评估：WOS test abstracts，domain/topic 标签不进训练与 Router。
- 模型：H768、4 layers、8 sparse experts + 1 shared、top-1、running center、
  $\lambda_{LB}=0.01$。
- batch：seq 1024、local 12/GPU、8 GPUs、accumulation 8、global 768。
- optimizer：AdamW，LR $10^{-4}$，weight decay 0.01，warmup 636 steps，旧
  100B scheduler horizon。
- branch：既有 step 800（629,145,600 tokens）；终点 step 2544
  （2,000,683,008 nominal tokens）。

投影用等价的 projected-weight 形式计算：

$$z=W\mu+(WP)(r-\mu).$$

所有臂保持同形状 Gate；每层 $P,\mu$ 从 branch actual-input DCLM calibration
估计并冻结。experts 与上游网络正常训练。

## 6. Conditions, Seeds, And Checkpoints

| Arm | rank | 对照目的 | 能回答多少 |
| --- | ---: | --- | --- |
| native | 768 | 原设计 | 频带限制相对基线 |
| H64 / R64 | 64 | head 与同维随机 | head rank-specific effect |
| M256 / R256 | 256 | middle 与同维随机 | middle effect |
| T448 / R448 | 448 | tail 与同维随机 | tail effect |
| N704 / R704 | 704 | middle+tail 与同维随机 | 完整 non-head effect |

注册 checkpoint：800、954、1272、1908、2544。九臂使用一个 paired branch
seed；这是该分叉的严格因果消融，不是跨初始化复现。

## 7. Primary Metric

在相同 DCLM held-out token 上计算每文档 next-token NLL：

$$\Delta L_{a:b}=L_a^{heldout}(2B)-L_b^{heldout}(2B).$$

每个 true arm 必须同时与 native 和对应 random 比较；文档 paired bootstrap
2000 次。它回答当前 branch 下的语言建模收益/伤害，不能建立 scaling law。

## 8. Secondary Metrics

- 固定 probe token 相对 native/branch 的 expert disagreement；目的：证明分发改变。
- margin、expert load、entropy、overflow/drop；目的：解释确定性与负载混杂。
- WOS 的 $p(e\mid domain/topic)$、条件间 Jensen--Shannon 距离与标签预测率；
  目的：描述分发是否更条件化，不能当功能目标。
- expert 参数位移/每 routed token；目的：看学习压力分配。
- frozen/current band overlap；目的：决定还能否称为谱带。
- held-out loss--token AUC；目的：区分早期速度与终点差。

## 9. Known Good / Known Bad / Known Confusing Cases

native identity 必须重放原 logits/top-1；P 必须对称、幂等且 rank 正确。route
disagreement 大但 NLL 不变是有效的功能 Fail，不是实验失败。random 变好说明
降维/正则化，不说明真实频带有价值。WOS domain purity 高也不等于 LM loss 好。

## 10. Stage-Level Profiling Plan

S0 checkpoint/data/code hash；S1 branch basis 与 algebraic no-op；S2 单臂 2-step
resume smoke；S3 九臂提交与 milestone 监督；S4 DCLM/WOS/route/expert 评估；
S5 paired verdict 与认识更新。

## 11. Runtime And Resource Contract

每 arm 一个 ACP job：workspace `share-space`，AEC2
`computing-cluster-5090-01g`，spec `n12lp.nn.i10a.8`，1 node、8×RTX5090、
spot、normal priority、固定 Blackwell image。资源不足允许排队/顺序完成，不允许
改为 debug cluster 或缩短 2B 终点。

## 12. Pass / Fail / Insufficient

- **Pass band-specific benefit：** true arm route manipulation 通过，且 2B NLL
  相对 native 和同维 random 的 paired CI 上界均 $<0$；load/compute guards 通过。
- **Distribution-only：** route 明显改变，但 NLL 不优于两基线。
- **Generic reduction：** true 与 random 相似，二者同向优/劣于 native。
- **Fail harmful/no benefit：** 所有 true arms 精确不优于 random/native。
- **Insufficient：** resume、2B completion、evaluation、compute/load 或 basis guards 失败。

## 13. Output Contract

保存 job IDs、hashes、milestone logs、每文档 NLL、route/load/domain/topic/expert
表和中央图；写 summary/detailed；写
`A15_05_05_E01_2b_matched_band_dispatch_focus_cn.md`，遵守 Focus 五段结构但不命名为
`focus.md`。不更新 graph/root sync，不 commit/push。

## 14. Claim Boundary And Next Decision

结论限于一个 H768 四层 DCLM branch seed 的 2B 因果消融。没有固定频带通过
注册收益规则，因此不进入跨 seed 复现。关闭 band-only 分发；任何下一次大训练
前，候选必须先通过直接面向专家更新或任务效用的功能准入。
