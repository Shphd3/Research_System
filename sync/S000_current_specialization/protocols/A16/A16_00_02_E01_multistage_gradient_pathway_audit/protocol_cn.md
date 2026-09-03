---
experiment_id: A16_00_02_E01_multistage_gradient_pathway_audit
anchor_id: A16_00_02_multistage_gradient_pathway
status: approved_for_implementation_smoke_and_full_audit
approved_by: user
approval_date: 2026-08-09
resource_profile: 5090-8-spot
primary_metric: centered_mediation_of_lb_shadow_step_nll
---

# Protocol：训练早中晚阶段的负载控制梯度路径审计

## 0. 审批摘要

**决策问题：** 在配对的早期、中期、后期状态中，running-centering 是否降低 Switch 负载均衡（LB）梯度的即刻语言学习代价；该降低是否同时伴随 Router source、Gate 与路由后专家更新冲突的减少？

**处理与对照：** Centered-Full 为处理，Vanilla-Full 为对照；seed 17/29 和 50M、6B、10B checkpoint 配对。每个比较内固定架构、checkpoint 状态、数据、tokenizer、$\lambda_{LB}=0.01$ 与评价文档。

**主指标：** 从同一个完整状态分别执行 LM-only 与 LM+LB AdamW 影子一步，计算二者在 WoS validation 上的配对 NLL 差 $\Delta NLL_{LB}$，单位 nat/token。处理效应为 $M=\Delta NLL^{Vanilla}_{LB}-\Delta NLL^{Centered}_{LB}$；正值表示 centering 减少了 LB 即时代价。

**裁定：** Outcome Pass 要求两个 seed 都至少两个阶段为正，并且冻结的三阶段中位数的文档 bootstrap 下界为正。共享路径与专家更新机制分别裁定。optimizer shard 缺失、batch 不配对、分支状态不一致、某层自身 LB 项对同层专家出现非零直接导数或任一 cell 缺失均为 Insufficient。

**批准范围：** Protocol、实现、单卡合成测试、一次 8×5090 smoke，以及四个完整审计任务均已批准。本实验只读 checkpoint，不续训。

**不能声称：** 不能证明一步效应解释完整 30B 轨迹、冲突更少必然形成有用专业化，或 dynamic expert bias 已更优。

## A. Anchor 对齐 — CONFIRMED

本 Protocol 实现 [A16_00_02](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_02_multistage_gradient_pathway_anchor_cn.md)，不改变其假设、主结果或边界。最强竞争解释是有益正则与 hard/soft 负载控制失配。

## B. 数据与阶段合同 — CONFIRMED

### B1. Checkpoint

Vanilla-Full 与 Centered-Full、seed 17/29 均固定：early=step 64（50,331,648 tokens），middle=step 7,629（5,999,951,872 tokens），late=step 12,716（10,000,269,312 tokens）。选择规则分别是首个非零保存点、首个不小于 10B 一半的保存点、注册终点。每个 cell 必须有一个模型状态和八个 optimizer shard，并在执行前记录大小与 SHA-256。

### B2. DCLM optimizer batch

共享路径梯度与 AdamW 影子更新精确重放 checkpoint sampler/data cursor 指向的下一组 DCLM 全局 batch，来源是 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`。预期为 768×1,024 tokens；两个影子分支的逐 rank 与全局 token hash 必须一致。

### B3. Web of Science 文档

来源目录是 `/data/share/109_cache_dir/hf_data/datasets/river-martin___web-of-science-with-label-texts/default/0.0.0/1a243df40ebf701e0d6a8c402ad9ae05f7ee5002/`。

train/validate/test 分别有 32,890/7,048/7,047 行，SHA-256 分别为 `213765a7be46524fddcc14b9fa0bc6a8c3ac094730b85d7e6c79117792358aed`、`d19cff6a15d295c6a5da2dd390934892b373aa8f2f037bc743cd91e4593f198e`、`25fc1fc037077315c97552054daad8c4b4d5076ded0d7bfd02a9959eb397f979`。

在七个 `domain` 内按文档 SHA-256 预先排序。专家冲突每个 domain 取 32 篇 train，拆成两个固定的 16 文档分片，共 14 组；影子 NLL 每个 domain 取 16 篇 validation，共 112 篇；test 保持未触碰。每篇摘要独立 tokenize、截断到 512、右侧 padding，padding label 屏蔽，禁止跨文档拼接。

## C. 模型与目标合同 — CONFIRMED

模型为已完成的四层、H768、八稀疏专家加一个 shared expert、top-1 DCLM MoE。Vanilla 使用 $z=Wg$；Centered 使用 checkpoint running mean 得到 $z=W(g-m)$；两者专家均接收完整本层表征。

在每个 DCLM optimizer batch 上分别重建 LM loss、未乘系数的 Switch LB loss、乘 $\lambda_{LB}=0.01$ 的 LB loss，以及训练时的 LM+LB 总目标。LB 必须读取原生 `aux_loss`，不得用其他平衡 proxy 替代。

## D. 梯度与影子一步合同 — CONFIRMED

1. **Router 上游表征：** 逐层捕获 centering 前的 Router source $g_\ell$，分别保留 LM-only 与 LB-only 的张量梯度，报告余弦、范数与负余弦质量。
2. **Router 更新：** 逐层记录完整 Gate weight 的 LM 梯度、乘系数 LB 梯度、余弦、范数和 AdamW 实际更新对齐。
3. **专家更新：** 按 WoS 文档组计算每层每专家的全部稀疏参数 LM 梯度；只比较双方都至少有 256 个非 padding 路由 token 的组对。主机制量是按路由 token 加权的负余弦质量，并报告同 domain 与跨 domain；同时记录每个专家的 LM 梯度与总 LB 梯度的余弦和范数。
4. **同层直接导数守卫与跨层机制：** 第 $\ell$ 层自身 LB 项对第 $\ell$ 层专家参数的直接导数，相对 Gate LB 梯度不得高于 $10^{-10}$。但深层 LB 可以通过 Router source 表征反传到前层专家；该跨层上游梯度是正式机制指标，不是实现失败。
5. **精确影子分支：** 每个 cell 从同一 checkpoint 独立初始化两个 DeepSpeed engine，一个执行 LM-only，一个执行 LM+LB；模型、optimizer、scheduler、RNG、Router buffer 和 batch hash 必须一致。两者都在同一 112 篇 WoS validation 和负载 guard token 上评价，不保存为续训 checkpoint。

## E. 比较与分析 — CONFIRMED

每个 seed 与阶段计算 $M_{s,t}=\Delta NLL^{Vanilla}_{LB,s,t}-\Delta NLL^{Centered}_{LB,s,t}$。seed 摘要固定为三个阶段的中位数。按 112 篇 WoS 文档配对重采样，先重算各阶段均值，再取阶段中位数；2,000 次给出 95% 区间。阶段与 seed 始终单独展示。

- Outcome Pass：每个 seed 至少两个阶段 $M>0$，且阶段中位数的 bootstrap 下界大于零。
- Shared-path Pass：每个 seed 至少两个阶段中，Centered 的 Router-source 与 Gate LM/LB 余弦都更高。
- Expert-conflict Pass：每个 seed 至少两个阶段中，Centered 的专家负余弦质量更低，并且四层都有合格 cell。
- Combined H1：前三项都通过，且将正 NLL 代价归因于均衡时，LB 分支确实降低硬集中。
- 完整有效数据不通过上述规则为 Fail；任何硬守卫失败或十二 cell 不完整为 Insufficient。

不增加人为效应阈值。负余弦但 NLL 不变支持有益正则；NLL 变差但硬负载不改善支持无效干扰。

## F. Preflight、Smoke 与失败规则 — CONFIRMED

Preflight 核对十二个 checkpoint cell、model/optimizer shard、seed/step、DCLM、WoS hash/schema、tokenizer 与空间。单元测试覆盖余弦聚合、零范数、专家 pair 资格、manifest 确定性、配对 bootstrap 和 typed verdict。

8×5090 smoke 使用一个 early checkpoint、一个 optimizer microbatch、每 domain 两篇 WoS、真实双加载与影子一步；必须通过状态/batch 身份、原生 loss 重建、三类梯度捕获、同层专家直接导数为零、跨层上游专家梯度登记和输出重建。

NaN/Inf、OOM、通信失败、checkpoint 不匹配、全局梯度不完整、分支状态不一致、数据 hash 不符或产物缺失会停止受影响任务；科学上的负余弦、负载差或 NLL 变差不能触发停止。

## G. 执行与产物合同 — CONFIRMED

每个任务使用 ACP 单节点 8×RTX 5090（`5090-8-spot`）、八进程、workspace `share-space`、cluster `computing-cluster-5090-01g`、spec `n12lp.nn.i10a.8`、`SPOT`。四个任务名为 `a16-gradpath-vanilla-s17/s29` 与 `a16-gradpath-centered-s17/s29`。

原始产物位于 `/data/250010109/MoE_Router/outputs/a16_multistage_gradient_pathway/`，必须包含数据/checkpoint manifest、逐 cell JSON、逐文档影子 NLL、梯度汇总、专家 pair 表、job ledger、日志和 source manifest。证据审计后只把策展表图复制到本实验目录。

跨块一致性：`PASS`。首次 smoke 开始时冻结科学正文与裁定规则；后续更改只能以 append-only amendment 记录，并说明证据资格影响。

## H. Amendment 1：跨层专家梯度路径（2026-08-09）

**触发原因：** 第一次真实 checkpoint smoke 观察到前层稀疏专家存在非零总 LB 梯度。逐层求导与实现核对表明，后层 LB 项依赖前层专家产生的表征，因此旧版“所有专家 LB 梯度必须为零”过于宽泛。

**修订：** 零梯度守卫只约束第 $\ell$ 层自身 LB 项对同层专家参数的直接导数；后层 LB 通过 Router source 传到前层专家的梯度，改为与其 LM 梯度比较并作为正式跨层机制报告。

**资格影响：** 无。决策问题、处理条件、checkpoint、数据、一步影子 NLL 主结果和裁定方向均不变；该修订只避免把真实跨层机制误判成实现失败，没有根据结果调参。

## I. Amendment 2：可微 LB 影子引擎与源训练轨迹边界（2026-08-09）

**触发原因：** 第一轮全链影子 smoke 复用了原训练命令中的 re-entrant activation checkpointing。LM-only 与名义上的 LM+LB 分支虽然记录了不同的总目标，但八个 optimizer shard 和全部保存模型张量完全一致。原模型把 LB 放在嵌套的辅助输出字典中；在注册的 re-entrant checkpoint 路径下，首遍 forward 的该张量没有连接到重算后的 backward graph。因此 30B 源训练记录了配置中的 LB 数值，却没有实际施加 LB 梯度。

**执行修复：** 两个反事实一步分支共同关闭 activation checkpointing；模型、源 checkpoint、batch、目标、optimizer 状态和超参数均不改变。硬守卫要求：修复后的 LM-only 应用更新与原 LM-only 应用更新逐张量完全一致；修复后的 LM+LB 相对修复后的 LM-only 必须改变至少一个 optimizer shard。原来的 detached 分支保留为带无后缀名称的失效工程证据，合格分支统一使用 `v2` 后缀。

**解释修复：** A16 现在回答：在已完成轨迹的冻结状态上，如果让注册的 LB 目标真正可微，它会造成怎样的即刻梯度路径和语言损失变化。不得声称这些源轨迹已经受到有效 LB 正则训练。Centered 与 Vanilla 的比较、WoS 影子 NLL 主指标、阶段、seed 与裁定方向保持冻结。

**资格影响：** 第一轮 smoke 的影子结果无资格进入科学结论；显式求导得到的梯度路径仍合格，因为它在无 activation checkpointing 下直接对原生 LB 求导。只有 LM-only 等价守卫和 LM+LB optimizer-effect 守卫均通过后，full 执行才具备资格。
