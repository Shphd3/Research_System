# Dense checkpoint、固定文本和缓存身份

下表12个实际可读状态属于同一条原生Dense seed17预训练轨迹。统一架构为8block、隐藏1024、MLP3072、16query/8KV头、head128、词表151936、输入输出共享、SAE none、281431040参数。B表示十亿有效预测token。状态内部计数、权重摘要与严格加载由实际缓存收据验证；manifest写complete不代表权重当前存在，也不代表恢复训练已验证。

| Training tokens (B) | Actual valid tokens | Step | Saved state/version | Exact checkpoint path | Payload SHA256 |
| --- | ---: | ---: | --- | --- | --- |
| 0.5 | 500000000 | 1908 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_000500000000` | `a1cccdefbaffa1bfb33291a7c26cd68fc82d72bafb01d1af8b10e87044b5bfd9` |
| 1 | 1000000000 | 3816 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_001000000000` | `92943fd775a95be35caa9ea8b18744d08af25bfe6507d18b198f53e8811ed169` |
| 3 | 3000000000 | 11446 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_003000000000` | `a2ae7f02bf3f8eabf217cc9f780b0c87b0ce0f103d7ecc7f4652f191c3e6ff1b` |
| 5 | 5000000000 | 19076 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_005000000000` | `740792483041d21672451c4ccf7d2a982c6ce117e3323ffdeef47f1b50c7bf75` |
| 10 | 10000000000 | 38150 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/milestones/token_010000000000` | `afa294d5fada38600708c1449a1c62330d421a72b38be91c6e3c950224b3e936` |
| 15 | 15000000000 | 57224 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/milestones/token_015000000000` | `1956120a63a6cd555bd90eca7883413367611117f0f3574079d1d1159bdc2c4f` |
| 17 | 17000000000 | 64854 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/milestones/token_017000000000` | `890925657c576192f07c18d14c03a539ca7e8d6a15e29fb56c41ca48cabb6cb3` |
| 19 | 19000000000 | 72484 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/continuation_checkpoints/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/target_019000000000_actual_019000000000_step_00072484` | `c9175ccea2a818a7d05462869cf3b18eb0a9244c84971e35083ed19d0b23434a` |
| 21 | 21000000000 | 80114 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/milestones/token_021000000000` | `12e5645c3944ba43af83122f95ab22a9166c438ef5f26067990d6555c603edd7` |
| 22.0186916 | 22018691584 | 84000 | complete recovery; schema2 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/checkpoints/step_00084000` | `6157e6ccd31afe4b811d85a210a4a10552c0696a601e6ba1b4fe494a6b0b8d2e` |
| 31 | 31000000000 | 118264 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_031000000000` | `0679e4fd93a233dc8b5fe2d4a84d76920e9d1c5585991537e941f3a91a587424` |
| 33 | 33000000000 | 125894 | complete milestone; schema2 | `/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_033000000000` | `a0b21cb3b8c5217aa5638101ed60c28747edf474bd33ae62f91cda57952586cd` |

| Actual valid tokens | Exact original path | Status |
| ---: | --- | --- |
| 9698669056 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/checkpoints/step_00037000` | PAYLOAD_MISSING; manifest remains |
| 9960813056 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/checkpoints/step_00038000` | PAYLOAD_MISSING; manifest remains |
| 21756547584 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/checkpoints/step_00083000` | PAYLOAD_MISSING; manifest remains |
| 13000238080 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/milestones/token_013000000000` | PAYLOAD_MISSING; manifest remains |
| 23000000000 | `/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_023000000000` | PAYLOAD_MISSING; manifest remains |
| 25000000000 | `/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_025000000000` | PAYLOAD_MISSING; manifest remains |
| 27000000000 | `/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_027000000000` | PAYLOAD_MISSING; manifest remains |
| 29000000000 | `/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_029000000000` | PAYLOAD_MISSING; manifest remains |

19B采用摘要相同的原始续训归档。三段源训练通过原10B启动指针、22.018691584B来源checkpoint规范连接。本轮不加载优化器或RNG，不声称恢复训练合格。排除mutable latest和窗口外状态。名为13B的缺失状态实际记录13000238080token，横轴不能只读文件名。缺失状态不插值为观测。

原模型代码为20260913_dense_baseline_pretraining/dense_sae/model；当前modeling、config和SAE辅助源码与训练resolved记录完全相符，见[身份审计](audit/native_source_tokenizer_identity.json)。分词器为本地Qwen3-0.6B-Base，五个记录文件已重新核验，总文件摘要3b602daf74810b313b8e1eca542d50b639a4e3f9de9b7185a309e09289306eda。相同分词器不等于相同Qwen模型权重。

主测点final_raw_h是最后block residual-post、model.norm之前。原生forward手动展开block7，因此用norm前hook确认相等。早/中/晚另存block0/3真实输出。旧pre_mlp_input是最后block norm2之后的MLP输入，不可混用。排除Qwen R12激活和A22字典。

主几何复用ntp_statistics_panel_2048的2048条256token序列，固定零基位置7、15、…、255。fit/test各1024记录、32768向量，八学科每类各128记录，文档等权。记录家族、全文、token序列的跨集完全重复均为0；论文级身份和穷尽近重复归组不可用。既有暴露审计将此面板限定为描述性。每点均值/PCA/Procrustes只拟合参考记录；test自身中心化仅定义CKA统计，不是迁移拟合。

语义桥接保留R12的96篇同the文本、token279位置、192token前缀、家族划分、外部可见前缀标签审查与每任务16TRAIN/8DEV名单。先用大N8参考集拟合谱基，再应用到独立桥接文本。旧Qwen数值不是Dense观测。原来源匹配不足和留出暴露仍然存在。只在0.5/17/33B重拟合同容量读出。

复用入口由[manifest](manifest.json)、[config](config.json)、[冻结身份](freeze.json)、[Protocol](protocol_cn.md)和[缓存索引](cache_index.json)界定。缓存键绑定checkpoint权重/manifest、面板和位置、层位、FP32原始预处理和collector源码。协方差/PCA/对齐FP64。数组均有摘要及原子完成收据，partial不可复用。大数组、对齐矩阵、均值/谱基和拆分统计留在执行根。scripts中的代码是精确审阅副本，实际从`/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics`运行`bash scripts/run.sh`；缓存完整时复用，不改原checkpoint。

输入当前访问核查已记录初始9项与完整12状态家族/配对面板，详情见配置与审计。访问、工程完成和研究者科学接受分别记录。
