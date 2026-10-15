# CrossCoder 分析交接

来源对话：1012-全层 Qwen3 CrossCoder训练；thread `01a13046-9276-7d13-9af9-a2bda6aa9e5b`。更新：2026-10-13T15:46:17.249648+00:00；本记录内 CURRENT。Codex /root（Codex desktop；模型 unknown）。非科学权威，不替代接收方用户的范围和批准。

## 交接对象

A22 `pt-2639gg8p` 已完成约10亿唯一配对位置、244140次更新。冻结 Qwen3-0.6B Base，选第2、4、…、28层 residual-post，hidden1024、共享字典16384。最终与0.5B状态均已登记，本次严格读取访问通过；Base未变化PASS。

最终固定验证：平均激活254.54，窗口未出现特征1.77%，各层FVE86.47%–99.93%。第28层仍最弱；小预测面板重构替换使CE增加0.306nats。工程完成，测量质量全面合格与科学结论均未确认。

## 首先读取与复用

1. [完整训练小结和七张图](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/final_training_20261013T115447Z/report_cn.md)：结果、定义和限制。
2. [精确绑定](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/handoff_20261013T154617Z/bindings.json)：不可变final/0.5B路径、资产ID/hash、base/data身份、加载代码与当前访问证据。
3. [实际配置](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/configuration.json)、[输入契约](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/input_contract.json)：复用最终方法。接收环境依[资产规范](/data/250010109/Research_System/assets/README.md)重新strict检查。

执行根目录 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder`。最终为 `checkpoint_000999997440.pt`，中间为 `checkpoint_000499998720.pt`，不要用mutable latest识别状态。加载复用 `FastBatchTopKCrossCoder`，构造/恢复参考 `crosscoder/train_a22.py:328`；分析恢复完整crosscoder权重与buffer、保存normalization，不需要Adam或启动trainer。提取同一位置14层激活，保存TRAIN均值/RMS归一化，`eval/no_grad/use_threshold=True`，解码后逆变换。最终TRAIN阈值0.051281，不在VAL重拟合。

实际方法是ReLU＋全局BatchTopK，k256为整批平均预算，L1=0；主loss是未平方向量L2平均＋AuxK/32。Base/GEMM BF16，主状态/损失FP32。提取、损失和指标分别复用 `crosscoder/extraction_a16.py`、`batchtopk_a18.py`、`metrics.py`。

## 下一步与完成标准

AI建议：逐特征检查层分布 → 验证多层重构作用 → 检查文本实例 → 汇总共享特征贡献。第5张图只是全部特征幅度总量，尚未识别共享集合。同一latent编号或非零decoder不证明语义共享；0.5B/最终稳定性先匹配特征，不能直接比编号。接收方首先确认具体分析问题与成本；首轮产出应包含方法、证据和限制。

## 保留的边界

本次没有启动新分析实验。新输出放执行侧新analysis目录，保护训练源码/配置/checkpoint/原始结果及其他对话。新GPU长任务或追加训练需明确范围与预算，勿重提已完成A22，不commit/push。

VAL固定10485760位置。DCLM文件级留出，原始文档/近重复独立性Unknown。FVE是整个窗口SSE比值、固定TRAIN均值基线，与部分论文EV不同；训练失活年龄与验证零命中也不同。非因果编码、多层绝对覆盖的最高层支配效应只支持重构保真度解释。不能据此证明特征因果、expert收益或Base预训练出现时间。A23/A24为独立对象，当前状态未在此刷新。
