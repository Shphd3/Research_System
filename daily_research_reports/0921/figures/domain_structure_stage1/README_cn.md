# N8结构诊断阶段I图源清单

这些文件是0921读者报告的日期内阅读副本，不是新的数值来源。

- 原始结果根：`/data/250010109/MoE_Router/experiments/20260921_sae_domain_structure_stage1/runs/full_retry_8x5090_20260921T091543Z/`
- 原始图目录：该根的 `figures/`
- 原始产物清单：该根的 `artifact_manifest.json`
- 复制方式：PNG、PDF、SVG逐文件原样复制；文件名和SHA256与原始产物清单一致。
- 数据口径：N8；21B三模型的第4/8层、正文均值／末词；时间分析为Dense/SALL第8层正文均值的0/0.5/1/3/5/10/15/21B真实检查点。

| 图 | 测量对象 | 诊断职责 |
| --- | --- | --- |
| `stage1_01_full_spectra_21b` | 21B完整方差谱 | 区分方差集中与分散 |
| `stage1_02_time_spectra_l8_mean` | 第8层正文均值谱随训练变化 | 查看方差分配何时改变 |
| `stage1_03_norm_cdf_21b` | 逐记录范数经验分布 | 区分普遍尺度变化与离群点 |
| `stage1_04_within_model_time_cka` | 同模型跨时间CKA矩阵 | 查看样本关系是否持续 |
| `stage1_05_temporal_cka_profiles` | 相邻及相对21B的CKA曲线 | 提供时间关系的读图切面 |
| `stage1_06_direction_stability` | 固定秩8/16/32主方向传递 | 区分关系稳定与坐标方向稳定 |
| `stage1_07_observer_readout` | \(a\)、重构、误差的匹配秩读出 | 检查SAE观察器保留哪些可读信号 |

边界：这些图只呈现事后缓存分析；不能单独证明语义质量、训练因果、模型实际使用或功能收益。
