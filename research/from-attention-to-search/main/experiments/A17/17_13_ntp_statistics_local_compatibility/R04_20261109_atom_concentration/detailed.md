# R04 Detailed: execution and evidence

Status: seven arms analyzed. Researcher judgment: Unknown.

The [Chinese Detailed](detailed_cn.md) is the complete bilingual record's evidence ledger, with equations, exact setup, conformance and deviations, numerical audit, all source tables, artifact manifests, stages and failure boundaries. This English companion preserves the same result and eligibility.

| arm     |     总体NLL |     M中位数 |   频次加权logM |        bin0 |        bin1 |        bin2 |
|:--------|------------:|------------:|---------------:|------------:|------------:|------------:|
| A5      | 4.039118998 | 1.344967711 |   -0.080334963 | 3.720251498 | 3.872186784 | 3.865717683 |
| A0      | 4.083141622 | 1.010460056 |   -0.401735217 | 3.794580477 | 3.942305977 | 3.929827148 |
| A1-deep | 4.085093112 | 0.870828768 |   -0.360922850 | 3.789857108 | 3.930946271 | 3.917200750 |
| A4      | 4.129441802 | 0.810891851 |   -0.472061195 | 3.867186691 | 4.009898194 | 3.986286052 |
| A1      | 4.157604347 | 0.585752336 |   -0.453948743 | 3.901086299 | 4.028563391 | 3.998681224 |
| A6      | 4.174997252 | 0.924780174 |   -0.284026317 | 3.985564060 | 4.104733180 | 4.059321536 |
| A2      | 4.286027700 | 0.256798644 |   -1.345580429 | 4.187885924 | 4.277627418 | 4.202913688 |

| arm     |   learned |   forgotten |   net_forgotten |   chi_mean |   position_flip_rate |
|:--------|----------:|------------:|----------------:|-----------:|---------------------:|
| A0      |     29281 |         212 |             236 |   0.407636 |             0.392096 |
| A1      |     29244 |         181 |             526 |   0.197567 |             0.198141 |
| A2      |     29553 |         130 |             275 |   0.002753 |             0.002755 |
| A4      |     29295 |         212 |             158 |   0.560060 |             0.569260 |
| A1-deep |     29277 |         171 |             120 |   0.275392 |             0.262880 |
| A6      |     29525 |         133 |             381 |   0.771362 |             0.762490 |
| A5      |     29229 |         199 |             547 |   0.082039 |             0.088713 |

The teacher is the same eight-layer MoE trained through33billion tokens; its frozen SAE reads the output of blocks.7.norm2 and retains32 positive activations among30000 coordinates. DEV defines the frequency p and all group/weight selection; EVAL contains2097152 fixed next-token positions. Teacher exposure to training tokens is retained as a boundary.

For each atom and layer, c is expert inclusion conditional on activation, pi is activation conditional on expert inclusion, and p is the frozen DEV activation frequency. The registered concentration is

$$
\bar M_j=\frac1L\sum_l\sum_e\frac{c_j^{(l)}(e)}k\frac{c_j^{(l)}(e)\pi_j^{(l)}(e)}{p_j},\qquad L=8,\ k=2.
$$

A6 computes amplitude-weighted atom-conditioned soft probabilities from router(stopgrad(hidden)), excluding load bias, and minimizes order3 Renyi entropy H3(q)=−0.5log(sum q³). Atoms must appear at least twice in each microbatch; frozen weights are min(log(1/p)/median(log(1/p)),3). The objective is CE plus lambda times the layer- and weighted-atom mean H3. Only router weights receive the auxiliary gradient; language-model CE still updates the whole student. Lambda is frozen from the50-update router-gradient norm calibration. Auxiliary gradients are averaged across ranks and layers, then added after the native DDP CE reduction and before global clipping.

A5 uses frozen normalized-coactivation spectral groups, with8 groups and seed2026110902. Group scores sum weighted activation magnitudes; Top2(score+bias) selects experts with equal0.5 gates at all8 layers. Group amplitude mass is balanced within±20% on DEV; this does not impose equal hard expert load. Router weights stay unchanged in this fixed-score path. Its scoring geometry and bias sensitivity differ from token-cosine clustering, so A5 versus A1 is a comparison of complete routing constructions, not an isolated proof about the partition unit.

The student has507988992 parameters,8 layers,hidden1024,16 query/8 KV heads,head width128,8 experts/Top2,expert width1536,vocabulary151936,and tied embeddings. All arms use seed17,the same initial state and DCLM sample order,context2048,4 ranks times microbatch16 times accumulation2,262144 valid targets/update. AdamW uses beta(.9,.95),epsilon1e-8,weight decay.1,peak LR3e-4,warmup1000 then constant,gradient clip1,bf16 with TF32 disabled. No balance loss is added; load bias changes by.001 times the sign of target minus actual assignment count. Comparison coordinates are updates and valid training targets; online-teacher GPU time is reported separately.

Per-position loss is stored as fp16 and unordered hard Top2 IDs as uint8. The pre-quantization aggregate NLL is retained separately. For atoms with at least50 activations, interval changes use paired position means and SE, two-sided normal tests, BH q<.05 and an absolute.01nat threshold. Net forgetting compares against that atom's earlier minimum, with a correction for choosing among earlier checkpoints followed by BH. Relative learning subtracts the all-position mean change. These are position-level descriptive tests, not independent-seed or document-cluster confidence statements. P1 requires higher A6 hard concentration than A0; P2 requires lower NLL in bins0–2 with overall deterioration no greater than.01nat; P3 jointly requires higher concentration and lower NLL for A5 versus A1. Differences below the declared adjacent-checkpoint change reference remain insufficient.

Route-flip chi is the fraction of a fixed atom's support positions whose unordered Top2 set changes, averaged over layers. A1-deep also reports layers0–3 and4–7 separately. Fixed scores still have changing load bias. t50 is the first250-step checkpoint that attains half the net250-to2000 improvement, and is undefined without positive endpoint improvement. Context examples rank significant atoms by delta and display their three strongest EVAL activation contexts; missing states or fewer significant members are not filled with invented examples.

All models share the original507,988,992-parameter8-layer MoE,8 experts/Top2,1024 hidden width,1536 expert width,seed17,DCLM order,262144 valid targets/update,AdamW and the original warmup schedule. A6 uses router-only entropy gradients on frozen teacher-SAE atoms; A5 uses fixed coactivation-group scores. The teacher/SAE interface is blocks.7.norm2 output, not the pre-normalization residual. The2000-update token budget is524288000 per arm.

Conformance and deviations:

| 项目         | 预期                             | 实际                                                              | 影响                                  |
|:-------------|:---------------------------------|:------------------------------------------------------------------|:--------------------------------------|
| 资源         | share 4H100 Reserved             | pt-lcxcxgyw；原pt-nmcuobkl冒烟后控制器失败，正式更新0，修复后续提 | 排队不代表更新；无P12                 |
| 输入/配置    | 复用A0与冻结teacher/SAE/DEV/EVAL | 输入strict与冻结分组已登记                                        | 访问不替代数值/训练完成               |
| 旧checkpoint | 每250步位置数据                  | A0四点；A4/A1-deep各两点；A1/A2各八点                             | 250步账本缺失；共同1000→2000补充      |
| NLL复现      | 逐位一致                         | 见position_consistency.csv，存在微小非零差                        | BOUNDED，未放宽训练冒烟门             |
| 新臂位置数据 | 由bf16快照复算                   | 同一次FP32训练评估直接捕获                                        | 避免快照舍入偏差；快照照存            |
| 恢复冒烟     | 真实中断恢复                     | step10完整存档后外部SIGKILL，再续至20                             | PASS须看真实smoke_summary，不提前宣称 |
| teacher精度  | 沿用A1记录                       | bf16；Top32索引一致率0.98962                                      | 与EVAL FP32编码存在接口差异           |
| P4固定路由   | χ约0                             | 按实测硬Top2；动态bias未冻结                                      | 不得人为零填充或作纯因果结论          |

Source chain: original eval JSONL and per-feature PT artifacts → analysis/ledger.py → [NLL](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/A1_eval_nll_by_step.csv), [M](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B3_Mbar_distribution.csv), [correlations](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B6_gain_vs_concentration_spearman.csv), [ledger](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C8_learn_forget_ledger.csv), [t50](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C9_t50.csv), [examples](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C12_examples_decoded.md), [consistency](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/position_consistency.csv), [coverage](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/coverage.md). All per-atom fields have CSV/Markdown exports in[per_atom](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/per_atom). Figures have PNG/PDF and reading notes in[figure_table_notes.json](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/figure_table_notes.json).

Original Protocol remains frozen;[implementation amendment](implementation_amendment_20261110_cn.md) records repairs before training launch. A6/A5 positions are captured during the same FP32-state training-time evaluation, avoiding bf16-snapshot rerun error. Old-arm MIG reruns are not all bitwise equal; actual differences are retained. Quantized fp16 loss averages have separate rounding errors. No tolerances were changed to relabel failed training smoke as passing.

Runtime: share-only job pt-lcxcxgyw, one4H100 Reserved16CPU256GiB worker. [Runner](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/runner.py), [actual run config](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/runs), [events](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/evidence/runner_events.jsonl), [durable pod logs](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/acp_receipts/pod). Only a real smoke_summary certifies lambda0 alignment, lambda calibration,20-step evaluations and external SIGKILL resume equivalence. Full states include optimizer,scheduler,RNG,cursor,bias; only latest2 recovery states plus endpoint retained, with8bf16 snapshots per new arm. Deleted states remain explicitly absent; receipts record paths,bytes,time. Registration and current access receipts are produced by[register_outputs.py](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/register_outputs.py).

| prediction   | AI_assessment                                                                                                                                                                                                        |
|:-------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P1           | NOT_SUPPORTED_OR_MIXED: concentration change A6-A0=-0.085679882; per-bin changes and reference magnitudes in prediction_metric_fluctuation.csv                                                                       |
| P2           | INSUFFICIENT: overall A6-A0 NLL=+0.091855630; low-bin differences=[0.19098358296192108, 0.1624272028831233, 0.12949438803992175]; metric-specific adjacent-checkpoint reference in prediction_metric_fluctuation.csv |
| P3           | DIRECTIONALLY_SUPPORTED: A5-A1 concentration=+0.759215375, NLL=-0.118485348; joint direction and metric-specific fluctuation conditions applied                                                                      |
| P4           | NOT_SUPPORTED as a blanket prediction: fixed-score A1 flips19.81% of position-level route sets; high-chi quartiles do not uniformly forget most. Causal attribution remains insufficient.                            |

P1–P4 are reported without promotion of researcher judgment in[prediction_assessment](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/prediction_assessment.md). One seed,2000 updates,teacher exposure,shared-dictionary circularity,bf16 teacher index agreement98.962%,missing old250-step states,within-document dependence and discrete t50 bound every claim. Route-flip correlations do not identify a causal mediator. Next scientific decision: Unknown. No commit/push.
