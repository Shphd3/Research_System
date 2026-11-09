# 训练资产与预算可比性核查

这里的Dense是原生8层、seed17的281431040参数轨迹，Baseline是Dense顺序对齐的普通8专家top2 MoE，不是官方Qwen Base、S7、SALL或SAE字典。每个实际加载状态的model键、真实tokens_seen和全文件SHA均经过本轮验证。

|对象|Dense|普通MoE Baseline|
|---|---|---|
|层／hidden／Qheads／KVheads／headdim|8／1024／16／8／128|相同|
|FFN|SwiGLU中间维3072|每专家1536，8专家、每token选2|
|总参数|281431040|507988992|
|常规激活矩阵参数|281431040|281496576|
|context／RoPE theta／词表|2048／1000000／151936|相同|
|权重共享|embedding与输出头共享|相同|
|tokenizer|/data/share/Qwen3-0.6B-Base|相同路径、当前hash见构造receipt|
|训练源|DCLM-Baseline配对视图dclm_pair_v1|相同|
|逻辑训练子集上限／是否循环|30000000000 token、cycle|相同规模，后段epoch映射有差异|
|有效目标token／常规update|262144|262144；实际里程碑边界可短更新|
|AdamW配置lr／betas／eps／wd|0.0003／(0.9,0.95)／1e-8／0.1|相同|
|warmup／后续LR|1000 updates／原生engine实际常数|同历史LR序列，经既有审计|
|原始硬件|八RTX5090及历史续训切换|四H100及真实续训／提速切换|

激活参数采用常规“参与矩阵规模”口径，包含共享embedding矩阵、attention和选中FFN；它不是单个token实际查到的embedding行数，也不等于实耗FLOP。MoE多出的65536常规激活参数来自八层router矩阵。topk、softmax、dispatch、优化器内存和硬件效率也使两者wall-clock不能由参数数目推断。没有完整匹配的总训练计算预算，不能宣称纯路由收益。

[Dense早期resolved config](/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/resolved_config.json)、[Dense后段resolved config](/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/resolved_config.json)、[MoE正式config](/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/configs/formal.json)给出配置记录；本轮使用每个状态对应的真实config，不以目录名猜模型。优化器一行是配置与历史运行审计证据，不是本轮重新训练的优化器测量。

[历史训练／验证loss与日志来源审计](/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/analysis/20261104_dense_moe_full_comparison/report_cn.md)核实前84000更新、22.018691584B之前的样本／mask顺序一致；后段的Dense LogicalLane把四参考流映射换成普通八流。[采样器根因审计](/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/analysis/20261104_sampler_root_cause/report_cn.md)给出实际首批指纹核查及影响边界；不能把该变化归因于当前行为评测。本轮重用这些已存证据，没有重跑采样／训练。

数据manifest为 `/data/250010109/training_data_views/dclm_pair_v1/manifest.json`，已登记hash `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`；同数据源不等于全程相同数据顺序，也不说明模型见过哪些本轮合成模式。实际37状态列表、配置路径、真实进度与每个全文件hash在执行audit/selected.json与各receipt。

30B指训练器通过 `max_tokens=unique_data_tokens` 采用的逻辑训练子集，不是整个dclm_pair_v1物理视图的总token数；后者保留约302.089B个token IDs。当前任务没有重新统计或更改训练数据。
