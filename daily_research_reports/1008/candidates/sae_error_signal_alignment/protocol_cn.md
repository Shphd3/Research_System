# Protocol：20261008_sae_error_signal_alignment

## 0. 授权快照

- 文档状态：`USER_AUTHORIZED_DIRECT_CANDIDATE_DIAGNOSTIC`。
- 授权依据：研究者明确要求构建 Anchor、Protocol，直接分析执行，提交四卡 H100 reserved，无需审计通过，先放当日 candidate。授权仅覆盖本候选诊断，不代表科学结论确认或发布授权。
- A–G 逐块人审：`USER_WAIVED_BLOCK_CONFIRMATION`，不伪称各块已经 `CONFIRMED`。
- 跨块一致性：提交前核对候选实现与冻结配置，不作为科学审批门槛。
- [候选 Anchor](anchor_cn.md)；不创建或修改 active Focus。
- 目的：检验仅凭输入 SAE 相似性，能否预测两套冻结模型的真实下一词误差信号方向。
- 实验角色：H2 的 operationalization/proxy test，不是 Router 方法实验。
- 主比较：fit 的 SAE 五近邻，与匹配随机参考二十次抽样比较。
- 主指标：记录平均、四领域等权的 δ 余弦优势 S；近邻绝对平均余弦 B 是同向性门槛。
- 支持：S、B 的 95% 区间下界均大于零；非支持：S 的上界不大于零；其余或测量不合格：不足。
- 执行：一个 ACP 任务，`h100-4-reserved`、`shphd-lite-0911`，最长四小时，即十六 GPU 小时；四个只读测量 worker。
- 冻结时间、scientific body/config/code/data 实际 hash：`2026-10-08T08:29:25.982472+00:00`; configs/freeze_manifest.json records exact scientific-body/config/code/data hashes before execution，执行负责人在提交前登记真实值，不虚构 hash。
- 冻结时科学结果 `NOT RUN`；研究者解释 `Unknown`。

## 1. 术语与定义

record 是一条选定自然文本，position 是其中一个有上下文的下一词预测位置。fit 提供固定近邻参考池；test/readout 提供查询位置。a 是 SAE 观测的原生张量，δ=∂ℓ/∂a 是真实下一词交叉熵的梯度，z 是完整非负 Top-32 激活码。相似 SAE 原子在本轮指激活码相似，不指词表 token 相同或 decoder 列相似。

两模型各自定义 a 和 δ。次级线性投影审计中，`param_input` 是投影输入 u，`param_delta` 是其输出梯度 κ，不能自动替换为 a、δ。余弦无量纲；CE 单位为每真实目标的 nat。

## 2. Anchor 对齐

检验 Anchor 中 SAE 相似性与原生误差方向的未解决关联。流程是：采集原生表征和真实 loss 梯度 → 不看答案和梯度选 fit 近邻 → 在 readout 比较同向程度、对照与区间。完成标准是两模型都有完整测量资格和独立的支持/非支持/不足分支。作业完成或实现检查不能自动推进 canonical 科学状态。

## 3. 被检验假设

readout 位置的五个 SAE 近邻，其平均 δ 余弦高于二十次匹配随机参考，且绝对平均 δ 余弦为正。检验的是方向同向，不是欧氏距离下降或平均 loss 降低。两个模型分别判断，不能相互挽救结果。

## 4. 竞争解释

| 解释 | 对照 | 剩余边界 |
|---|---|---|
| 领域、位置造成相关 | 同领域、同 floor(position/64) 候选池 | 其他上下文差异仍在 |
| 普通输入相似性即可解释 | 同池中的原生 a 五近邻 | 不识别 SAE 语义因果贡献 |
| 当前 token 身份造成相关 | 严格相同当前 token 子群 | 可能覆盖不足，不偷偷回退 |
| 真实下一词相同造成相关 | 相同/不同下一词事后分层 | 不能用答案选近邻 |
| 层内共有方向或实现错误 | 匹配 strata 打乱 δ、已知案例 | 负对照不是语义因果干预 |

## 5. 数据构造与来源

从已有 N8_v1 自然文本抽 1024 records：计算机、数学、物理、生物四领域共八类别；每类别每 split 固定 64 条，即 fit/test 各 512。抽样 key 固定 `h2-20261008-v1`。使用已核验 Qwen tokenizer 的 256 token IDs；输入前 255 个，位置为 `14,30,…,254` 共十六个，真实目标为原序列 position+1。每模型每 split 计划 8192 次预测。

排除与 20260925 旧 1024 条选择精确 sample 身份、文本或 token-ID 序列重合的记录；本轮 split 之间去重。数据文件位于执行根目录的 `data/selected.jsonl`、`data/data_manifest.json`。

已生成 manifest：与旧 1024-record 面板重叠为零；与 20260930 旧 2048-record NTP-statistics 面板重叠 **768 条**；在本轮所有选择文本中，five-token Jaccard≥0.85 的近重复碰撞为零。N8 来源语料曾被审计，不是 fresh holdout，不能称未接触 confirmation。paper ID 不可用，记录仅近似独立。selected payload hash 为 `22a8c4d23a29d1508778ba2702c65f724bd022c1f36490735f8ca6679042857a`；来源、tokenizer、排除计数与文件 hash 保留在真实 manifest。

## 6. 学习任务与允许信息

本轮没有学习任务训练。测量原模型真实下一词 CE。近邻选择可使用 fit 的 a/z、领域、位置区间，当前 token 仅用于预声明子群；同分按 record ID、位置排序。不得使用 δ、下一词、loss、更新后果或 readout 结果排名。真实下一词只用于 CE 与事后分层。不生成或反转标签；δ 不含 SAE 重构梯度。

## 7. 模型、接口与冻结条件

**S7fresh：** 使用已核验 exact 33B 状态：

`/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/state.pt`。

研究者已纠正名称为 s7fresh。此处 33B 是训练 token 数，不是参数量；optimizer step 125894。八层，hook 为 `blocks[7].attn.o` 输出、残差相加前，a 为 1024 维。SAE 为 30000 features、Top-K 32，训练重构权重 0.1。state manifest SHA 为 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`。

复用 `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/scripts/core.py` 的已检查原生测量，适配 batch 和位置。a=Wc，c 为 2048 维，`param_input=c`、`param_delta=δ`。调用该模型自己的 SAE encode 和 decoder 列归一化。

**Qwen：** `/data/250010109/model_cache/Qwen3-0.6B-Base-official`，28 层、hidden 1024。model.safetensors 实际 SHA 为 `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`。对应 SAE：

`/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt`。

SAE 实际 SHA 为 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`，config SHA `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59` 与其 metadata 一致。复用 E16 的 `sae_core.TopKSAE.from_pretrained` / `encode_topk`，适配 Hugging Face 原生 hook 与下游重放。

a 是 `base.model.layers[27].mlp` 的输入，即 post_attention_layernorm 之后，不是 Attention 输出或最终 hidden。次级 down projection 的 u 为 3072 维门控中间激活，κ 为 1024 维 down 输出梯度；a 的 δ 通常不等于 κ。

两套主干与 SAE 均 float32、eval、冻结，TF32 关闭；从 float32 原生 logits 用 float64 logsumexp 计算 CE。HF runtime 可用路径为 `/data/250010109/dependency_packages/hf_transformers_qwen3`，版本 4.53.3；实际镜像/runtime 随运行登记。不加 LoRA 分支。

## 8. 损失与优化

每真实位置计算 ℓ=logsumexp(logits)−logit[y]。末层下游按位置独立，对选定位置的 loss 求和再反传，保留逐位置 δ；first-batch 前两条记录检查采集的逐位置δ与原生单目标梯度一致，避免误存带 batch 平均比例的梯度。

optimizer、训练 schedule、模型更新、SAE 更新均为零。训练观测 contract 为 `NOT_APPLICABLE`；仍记录有效目标/record 数、设备、持久日志、冻结与 no-op 检查。重构仅诊断，不据此删除不利样本。

## 9. 条件、种子与 checkpoint

| 条件 | 作用 | 输出 |
|---|---|---|
| decoder 范数加权的原始 SAE 五近邻 vs 随机二十次 | 主 H2 | pair/record/domain 表、S 和 B |
| 原生 a 五近邻 vs 自己的随机参考 | 输入相似竞争解释 | 次级同指标 |
| 严格当前 token 相同的 SAE/a 近邻 | 词汇对照、不回退 | 子群指标和覆盖 |
| fit 均值中心化 SAE 码、中心化 δ sanity | 次级诊断 | 不挽救主指标 |
| 匹配 strata 内打乱 δ | 负对照 | null 同向诊断 |

随机配对与 bootstrap seed `20261008`。没有种子扫描、checkpoint 选择或事后挑工作点。microbatch为4条记录；每个worker首两条进行单记录资格检查。按准备后的整数 record_id%4 分配；每 worker 256 条，先 S7，再 Qwen。没有自动重跑。

## 10. 主指标与冻结分析

全部 30000 坐标的稀疏码乘对应 decoder 列范数，再单位化计算余弦；主指标不中心化。fit 候选仅凭输入排除 code norm≤1e-12，且匹配领域和 floor(position/64)。每 readout 位置选五近邻。随机参考在同池排除该条件的五近邻后，允许重复抽二十次。主候选池至少二十五个；严格当前 token 子群至少六个；不能按 δ 或答案打破同分。

记 b_i 为五近邻 δ 平均余弦，r_i 为随机平均余弦，s_i=b_i−r_i。先在每条有效 readout record 内平均，再领域内平均，最后四领域等权，得到 S、B。bootstrap 固定 fit 参考、配对 ID 和随机抽样；按领域对 readout records 有放回抽 2000 次，保持各领域有效记录数，seed 20261008，取双侧 95% percentile 区间。

统计独立单位近似为 record，不是 token 或 pair；共同论文依赖未知。两模型分别检验，没有合并胜利或总体多重检验声明，次级结果不挽救主结果。

先用输入选邻居，再检查 δ。任何非有限测量使 qualification/collection 失败；零范数 δ 仅在评分阶段 mask，不重新选邻居。工程 epsilon 固定 1e-12。主 query position 必须五近邻与二十随机比较全部有有效 δ，否则记 invalid；不补配、不删不利配对。有效 record 至少一个有效主位置。测量资格：至少 256 有效 query records、四领域均有记录，且 8192 个计划 query positions 中至少 90% 有效。完整记录缺失和覆盖。

## 11. 次级指标与保护条件

报告 δ norm 均值/分位数、负 δ 余弦比例、SAE support Jaccard、code/a 余弦、打乱 δ 对照及相同/不同真实下一词分层。严格当前 token 子群候选须至少六个，不足则 uncovered，不退回不匹配参考；少于 64 条 query records 时仅描述。

中心化 SAE 码只减 fit code 均值；中心化 δ sanity 对两 split 减 fit δ 均值，并保留已选配对。不进入原始主选择与判定。原生 a 控制用自己有效性表，不补主指标缺失。重构误差记录但不筛不利样本。真正投影参数梯度余弦计算 cos(κ_i,κ_j)cos(u_i,u_j)，两模型使用各自真正的 u/κ；其恒等式检查是实现合格，不是 H2 科学支持或有限更新证据。

## 12. 已知正确、错误与易混案例

- 相同非零 δ 的余弦为 1，正交为 0；相反方向为 −1。
- 相同 SAE 码不能强制 δ 相同；下一词不同仍是合法样本。
- 零向量标 invalid，不用有利向量替换；非有限数组使测量失败。
- first-batch 核对原生/重放 CE、δ，一次投影真实 autodiff 梯度与 κu^T；Qwen 的两个梯度接口不能混用。

数值 tolerance 在提交前 `configs/h2_v1.json` 固定并按已有源代码核对，不虚构已通过。qualification 只证明测量实现性质，不叫科学审计 PASS。

## 13. 科学流程与阶段约定

| 阶段 | 目标与输入 | 操作与理由 | 输出与停止 |
|---|---|---|---|
| Prepare | N8_v1 中的合规 1024 条 | 固定 hash 抽样、split/category 与旧面板排除 | selected/manifest；缺计数/hash/目标即停 |
| Qualify | 每 model/rank 第一 batch 两条 | 原生/重放 CE、δ、投影梯度和 no-op | qualification receipt；失败使该 worker 后续测量无资格 |
| Collect | 冻结模型、assigned records | 四 worker，各先 S7 后 Qwen，采 a/δ/z/u/κ/目标 | features 与 receipt；不偷偷另起任务重试 |
| Analyze | 合并测量与 fit 参考池 | 输入选配对、记录 bootstrap，避免 pair 数伪独立 | CSV/summary；资格或覆盖失败为不足 |
| Deliver | 可审查证据 | 数据表、简洁 PNG/SVG、有限结论 | completion receipt；不发布、不训练 Router |

一个已授权 ACP 任务内完成全部阶段，first-batch qualification 不是另一次审批或外部 Smoke。遇 hash/schema、hook、恒等式/no-op、资源错误或四小时上限即停止。不自动换硬件、不重复提交、不持续监控。

## 14. 算法、输出与来源

执行根目录为 `/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment`；配置为 `configs/h2_v1.json`。

算法顺序：核对 hash → 加载冻结模型 → first-batch qualification → S7/Qwen 采集 → 按 record ID 合并与验证 → 构建 fit 输入参考池并固定配对 → 计算 δ 与真实参数梯度方向 → record/domain 聚合 → 固定参考池 bootstrap → 应用判定分支 → 输出图表与收据。

产物包括：`collection/shard_*/{s7,qwen}/features.npz` 与各自收据，保留 record ID、位置、a/δ、稀疏 indices/values、真实下一词/当前 token、loss、重构诊断、param_input/param_delta；`analysis/<model>/` pair/record/domain CSV、summary.json、coverage/null；PNG/SVG、来源和完整产物 manifest、completion receipt；ACP 提交收据、镜像/runtime/资源和真实 code/config/Anchor/Protocol/data hash。

candidate 保留文档和小证据；raw arrays、模型、字体和 checkpoint 归执行仓库，不复制到 Research_System。

## 15. 支持、非支持与证据不足

各模型达到资格后独立判断：

1. `SUPPORT`：lower95(S)>0 且 lower95(B)>0。
2. `NON_SUPPORT`：upper95(S)≤0。
3. `INSUFFICIENT`：其他情况，或测量/产物/记录数/90% 覆盖不合格。

如果 S 已确定为正，但 B 未确定为正，则写“有相对同向优势，但尚未确定绝对同向”，归 `INSUFFICIENT`。零是关联方向门槛，不是实用效果门槛。机械完成与经验判定分开，人的科学确认继续 Unknown。

## 16. 不能声称什么

不能证明原子语义、SAE 相似性的因果作用、有限步 loss 帮助、完整梯度冲突解决、Expert 共享政策、路由收益、长期训练改善、未接触 confirmation，或不同模型接口等价。真实答案只作诊断分层，不能当可部署路由输入。原话“路由真正需要的性质”只能作为待验证方向，δ 同向不是已证明充分条件。

## 17. 分块确认、冻结与修订记录

| Block | 内容 | 人类确认状态 |
|---|---|---|
| A | H2 与局部结论范围 | 用户激活 H2，数值方案为 candidate |
| B | 数据、split、排除 | AI 在直接执行授权中操作化 |
| C | 纯真实下一词测量 | 没有新监督训练任务 |
| D | verified 模型与原 SAE hook | 资产已查；S7fresh 名称由用户纠正 |
| E | 不优化、不训模型或 SAE | 有界诊断 |
| F | 配对、对照、分支 | AI 候选定义，不伪称人已确认科学判断 |
| G | 一个四卡 H100 reserved 任务 | 用户明确授权 |

用户“无需审计通过，直接分析执行，先 candidate”豁免本轮通常的 A–G 逐块确认流程。登记 `USER_AUTHORIZED_DIRECT_CANDIDATE_DIAGNOSTIC`，不倒填 `CONFIRMED`，不升级 canonical 设计或科学结论。

提交前执行负责人补实际 scientific-body、config、code、data hash 和冻结时间，把 operational freeze 从 pending 改为 registered。这是重现性核对，不向用户再次请批。首次执行后保留本科学正文，实质变更追加 amendment：时间、旧/新值、原因、已看结果、受影响 block/condition、授权和证据资格影响。结果另写，不回填为本协议预期。
