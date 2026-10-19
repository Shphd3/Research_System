# Feature 频率 Protocol：当前资产核对

日期：2026-10-15，Asia/Shanghai。处理者：Codex `/root/assets_inventory`。
[English](assets_checked.md)。

**建议复用已经保存完整的 final 14层/F16384 稀疏推理缓存及其完整 D/V 共同命中矩阵。** 这只是可执行输入的建议，不代替研究判断，也不授予分析运行许可。本次只检查本机现有路径、元数据及小型源代码；没有训练、推理、新特征统计、绘图、加载 checkpoint 或计算大型 checkpoint 全量哈希。

当前回执：[严格访问检查](asset_access_20261015.json)，北京时间22:11:00完成，七个选定资产全部通过，退出码0；[缓存元数据与源代码核对](asset_metadata_20261015.json)。访问通过不等于运行时可加载、内容哈希完整、原始文档独立或科学资格通过。

## 1. 对象与精确身份

Base 模型有28个 block。已经完成的 A22 CrossCoder 只观察预先指定的14个 block：从0开始编号为 `1,3,...,27`，从1开始编号为 `2,4,...,28`。字典包含16,384个 feature，隐藏维数为1,024，接口是最终全局 norm 之前的 block residual-post。其0.5B和final属于同一架构的不同学习状态。feature编号相同不能证明两者中的 feature 已经匹配。

执行根目录：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder`。

| 对象 | 当前精确资产ID | 必需地址 |
|---|---|---|
| 冻结Base | `model_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base` |
| Tokenizer | `tokenizer_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base` |
| 准备好的TRAIN/VAL | `dclm_crosscoder_direct_bins_1b_a15_20261013` | 执行根目录 + `/data/direct_dclm_bins_a15` |
| A22 0.5B | `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_499998720_20261013` | 执行根目录 + `/runs/formal_14layer_batchtopk_a22/checkpoint_000499998720.pt` |
| A22 final | `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013` | 执行根目录 + `/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt` |
| 完整final稀疏缓存 | `representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z` | phase-one根目录 + `/feature_cache` |
| 已有phase-one分析 | `analysis_crosscoder_feature_relation_phase1_20261013t173130z` | phase-one根目录 |

phase-one根目录是 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`。

final checkpoint由 `pt-2639gg8p` 生成，训练计数为999,997,440个配对位置曝光。记录的SHA256为 `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`；数据manifest的SHA256为 `874794a8657f8982f7abb12ee517ec551fce840d9f20dfe103f48589a6779849`。本次读取已有身份记录，没有重新扫描大型payload计算这些哈希。对应证据是phase-one根目录下的 `input_identity.json`、`cache_binding.json` 和 `feature_cache/manifest.json`。

缓存总manifest没有内嵌资产ID字段。稳定ID来自catalog登记；checkpoint、数据、配置绑定及四个rank manifest构成保存时的身份链。当前640个chunk全部存在，文件大小与记录一致，各自的绑定与总绑定一致。所有chunk的全量新哈希和数组内容均为 `NOT_CHECKED`。

## 2. 已保存的推理与数据契约

| 项目 | 已有契约或观察 |
|---|---|
| 推理门控 | 先计算ReLU code；只有按decoder范数加权的score严格大于已保存TRAIN EMA阈值才保留 |
| 阈值 | `0.051281172782182693`；从完整TRAIN状态冻结 |
| 其它状态 | `k=256`；completed updates为244,140；TRAIN归一化校准位置数65,536 |
| 归一化 | 每个观察层使用冻结的TRAIN均值与vector RMS，目标范数1 |
| 精度 | Base及GEMM为BF16；CrossCoder状态、score及保存的正code为FP32 |
| 原推理分批 | 原四个rank区间；每次Base前向16个完整1,024-token上下文；每次CrossCoder编码1,024个有效位置；SDPA |
| 有效位置 | `N=10,485,760`；排除special ID 151643—151656；一行是一个有效位置，14层不乘入样本数 |
| 缓存量 | 已有manifest记录2,669,034,642个非零项；平均门控L0为 `254.538978767395`；本窗口290个feature零命中 |
| 既有D/V划分 | 81个块，每块至多128个完整上下文，源顺序成块；种子20261014；保留尾块；按有效位置数平衡 |
| 既有计数 | `N_D=5,238,097`；`N_V=5,247,663`；共10,249个上下文 |
| 数据源 | 一个VAL bin，`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000001_processed.bin` |

该bin记录的SHA256为 `664d07bcb4db743ac9ec62a9c6e4df245f3fd4fde35b8536dece439fcaac9697`。每行以全局有效位置索引标识，可通过固定的 `index_val/records.npy`、`index_val/prefix.npy`、源bin身份及排除ID映射到token偏移。这些是token/上下文身份。**原始文档边界、URL身份、原始文档和近重复组之间的独立性仍为 `Unknown`。** 原始数据准备manifest中的 `activation_cache=NONE` 描述的是phase one之前的数据准备状态，不否认后来已经保存的缓存。

D和V都已在此前分析中被查看。新Protocol可以把它们用于明确标记为“已接触的单bin内部探索”的分析。改名、重排或重新划分不能将它们变成未接触确认集。原始文档独立的确认分支，需要保持身份的文档映射及另行核定的数据划分；现有缓存未满足这些前提。

已有 `original_validation_replay_check.json` 记录所有16,384个feature边际命中数与原始final验证完全一致。rank回执记录原前向计算完全相等和buffer不变。这些是历史工程回执，本次没有重放推理。

## 3. 无需重新推理即可复用的对象

下表路径均相对于上文phase-one根目录。本次只读取大型数组的文件头，并核对保存时的生产代码，没有加载其全部内容。

| 保存对象 | 形状、类型、体积 | 复用范围与限制 |
|---|---|---|
| `counts/total0.npy` | `(16384,16384)`，int64；2,147,483,776 bytes | D的完整共同命中矩阵，可以查任意pair，包括旧图未保留的pair |
| `counts/total1.npy` | 同上 | V的完整共同命中矩阵 |
| `feature_frequency.npz:n` | `(2,16384)`，int64 | D/V边际命中；侧编号0=D、1=V |
| `feature_frequency.npz:zsum` | `(2,16384)`，float64 | 已保存的边际门控幅度和 |
| `feature_frequency.npz:block_n` | `(81,16384)`，int64 | 每个既有块中任意feature的边际命中 |
| `feature_frequency.npz:block_zsum` | 同形状，float64 | 每个块的边际门控幅度和 |
| `block_edges/block_000.npy` 至 `block_080.npy` | 每个`(214711,)`，uint32 | 只有旧214,711条发现边的共同计数，与 `graphs/raw_edges.npz` 对齐；不覆盖任意新pair |
| `feature_cache/rank0..3/*.npz` | 640个CSR chunk；文件合计16,098,567,532 bytes | 审核通过后，可用于指定新pair的块计数或上下文展示 |
| `decoder_geometry.npz` | 已保存decoder范数、TRAIN RMS及均值 | 几何描述；不能据此决定频率、语义或因果依赖 |

CSR即压缩稀疏行格式。字段为 `ptr`（uint64行偏移）、`ids`（排序的uint16 feature编号）和 `z`（正FP32门控激活）。普通chunk有16,384行。第一个chunk的文件头是 `ptr:(16385,)`、`ids:(4126432,)`、`z:(4126432,)`；这只是格式例子，不能假定所有chunk的非零数相同。元素本体的体积公式是 `8*(N+640)+6*nnz`，实际文件另含NPY/ZIP元数据。

完整共同命中矩阵可用内存映射按行或按候选索引读取。只要激活指示器、窗口、侧标签及输入身份保持一致，就无需重建全pair计数。全体无序pair数为 `F*(F-1)/2=134,209,536`。旧候选列表Jaccard搜索使用的合格pair池为120,380,886，定义不同，不能默认为新Anchor中的全部feature总体。

单凭 `block_n` 不能恢复任意pair的分块共同命中。旧 `block_edges` 只覆盖旧发现边。如果新选pair不在旧集合中，后续必须读取稀疏缓存补算其块共同计数，或诚实标为 `NOT_RUN`。已有token层面的汇总也不能提供原始文档独立的不确定性。

## 4. 已有图、绘图代码与provenance

phase-one图是经过阈值筛选的有向统计图。其 `code_snapshot_v2/core.py:rule` 要求两端边际支持数均≥200、共同支持数≥20、`P(u|A)≥0.8`、`P(A|u)≤0.5`、`n_u≥2*n_A`，随后进行传递约简，并据此计算候选列表的重合。这一构图过程已经包含频率方向和阈值选择，不是对所有可能pair的无条件展示。

`figure_provenance.json` 绑定约简V图、完整共同计数、频率、decoder贡献表及四对选定feature。`code_snapshot_manifest_v2.json` 固定 `code_snapshot_v2/` 中八个生产文件；本次八个小文件哈希全部与manifest一致。它们是可审查的来源。执行 `features.py` 会加载模型和checkpoint，并可能生成激活/计数，本次没有运行许可。

expanded图的执行目录是：
`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/expanded_graph_20261014T032050Z`。

其 `receipt.json` 和 `selection_rules_frozen.json` 说明输入是已保存的约简V图、旧原始边支持表、频率及几何。图中选了320个节点，保留它们之间全部1,250条已有直接边。完整合格总体有15,537个节点，h0—h5总体数为 `20,8896,5347,1209,63,2`；展示数为 `20,80,80,75,63,2`。图沿用完整图的h，使用固定名额和D频率秩分层。它是选定展示，不代表完整频率分布，也不是新模型机制证据。

绘图来源包括 `code/draw_expanded_graph.py`，后续排版、标题修订代码及回执均有保留。仓库副本与阅读入口见[已有expanded交付目录](../../1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/README_cn.md)。这些记录只支持复用已有统计进行展示，不构成新的独立确认数据。本次没有重画或重新解释旧图。

## 5. 0.5B与另一个全28层运行

A22的14层0.5B和final checkpoint都通过当前严格访问检查。这里核实的完整稀疏缓存**只属于final**。本次沿所检查的phase-one/analysis导航，没有找到对应0.5B完整稀疏缓存或feature匹配证书。因此，0.5B/final稳定性需要独立的匹配和输入准备，不能以相同feature编号成立；本次未运行该比较。

全28层/F32768的A23是另一个从头开始的运行，不是本缓存的生产者。当前本机记录表明它已经在retry中继续推进，不能写成 `NOT_RUN`。本次有限检查时，`recovery_20261015/a23/run_retry_01/current_progress.json` 记录step8,700、35,635,200个位置曝光；`latest_checkpoint.json` 记录在24,997,888曝光处实际保存了可变的 `/latest.pt`，其 `asset_id:null`。

所查A23原目录和指定retry目录中没有0.5B或final checkpoint；当前catalog亦没有登记A23的0.5B/final资产。这只表示在这些有限路径中尚无目标资产证据，不是全存储不存在或平台当前状态的断言。本次未查询平台、连接新设备、持续监控、登记或操作作业。后续若研究者选择A23，必须重新核定实际输入。

## 6. 历史资源与估计边界

旧phase-one生产作业是 `pt-zwh6g95p`，此前 `pt-io5c5h2p` 经工程修复。使用4张H100 80GB。成功终态回执记录629.63秒active compute；资源回执记录聚合RSS峰值12,248,944,640 bytes、新增磁盘峰值46,226,108,170 bytes。稀疏激活生成日志中的已采样GPU allocated最大值为5,181,352,448 bytes。这是**生成阶段的记录，不是已经核实的整个作业显存峰值**。

| 成功阶段 | 历史秒数 |
|---|---:|
| 稀疏激活编码 | 127.26 |
| 完整共同计数 | 87.51 |
| 合并 | 121.54 |
| 原始边 / 传递约简 | 2.39 / 2.64 |
| pair选择 | 39.66 |
| 敏感性 | 2.92 |
| 指定旧边分块计数 / 汇总 | 29.18 / 12.63 |
| 检查 / 交付 | 134.13 / 25.91 |

这些值来自保存的 `events_75.jsonl`，其计时口径不等同于终态active counter，不能相加后当作新账单时长。expanded展示另记CPU墙钟63.91秒、RSS峰值1,217,056,768 bytes、GPU作业0、缓存扫描0。

本次没有新benchmark。历史时间不能核定新零模型、重采样方案或其它运行时的全总体扫描。本次建议的缓存复用路线可避免重新推理和GPU全pair计数；任意新pair的块计数仍可能需读取约16.1GB缓存。待实施方案和执行环境冻结前，精确耗时为 `Unknown`。

## 7. Protocol必须保留的缺口

1. 原始文档独立确认：缺少原始文档/重复组身份及另行核定的划分；既有D/V只能作为已接触的单bin内部探索。
2. 0.5B/final稳定性：匹配证书及匹配的推理缓存尚未建立；本次未比较。
3. 任意新pair的块共同计数：只有旧214,711条发现边可直接查已有数组，其它pair需要经批准读取缓存补算。
4. 当前访问已经核实；全缓存新哈希、完整数组内容验证、checkpoint加载能力和测量质量审批仍按实际情况保留 `NOT_CHECKED` 或 `Unknown`。
5. 这份清单不授权新分析、训练、启动、提交、推送、发布、Graph编辑或科学状态转换。
