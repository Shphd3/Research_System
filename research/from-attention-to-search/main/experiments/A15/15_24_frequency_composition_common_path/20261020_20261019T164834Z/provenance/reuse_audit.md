# 表征分析可复用资产与最小扩展审计

处理者：/root/representation_reuse_audit。时间：2026-10-20 Asia/Shanghai。只读；未启动统计、模型前向、GPU、训练或改项目文件。已读 root/project AGENTS、科研推理审计技能、assets/README。当前严格访问回执 `/tmp/representation_reuse_access_20261020.json` 通过所需10个资产及依赖项目。

## 1. 可以直接复用的确切输入

统一执行根 `E=/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder`。

- 字典资产 `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`。文件 `E/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`，保存999,997,440接触位置。资产登记SHA `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`（本审计只访问检查，未新hash5.6GB）。F=16,384，hidden1024，实际2/4/…/28层（零基1/3/…/27）residual-post，最终RMSNorm前。z来自14层联合编码，冻结TRAIN中心化/vector-RMS，冻结阈值0.051281172782182693，不是14套独立特征。
- 模型/tokenizer：`model_qwen3_0p6b_base`、`tokenizer_qwen3_0p6b_base`，`/data/share/Qwen3-0.6B-Base`。本轮若只分析已有缓存，无须模型前向。
- 数据资产 `data_tulu_sft_route_20261019t012300z` 与表征资产 `representation_tulu_sft_route_20261019t012300z`。执行 `E/analysis/sft_route_learning/20261019T012300Z/`。
  - `cache/train.pt`：85,548位置、1,024对话、26,299,223个正z事件、388,181,399 bytes。
  - `cache/dev.pt`：10,340位置、128对话、3,181,096事件、46,954,105 bytes。
  - `cache/eval.pt`：22,446位置、256对话、6,838,973事件、101,373,256 bytes。
  - 原始字段实际mmap核对：`hidden` BF16[N,1024]，`target` INT64[N]，`feature_ids` INT32[nnz]，`feature_z` FP32[nnz]，`feature_ptr` INT64[N+1]，`block_id` INT32[N]，`position_id` INT64[N]，另有旧DCLM名单的`low_ids/high_ids/mask_low/mask_high`。旧mask不是当前SFT本地最低段，不能混用。
  - 同目录`data/{train,dev,eval}.jsonl`字段：id、dataset、user、assistant、prompt_sha256、source_file、row、input_ids、answer_start、answer_tokens、prefix。
  - source Tulu revision `6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752`。dataset有cot/sharegpt/code_alpaca/gpt4_alpaca/wizardlm/flan_v2/oasst1及少量science等。仅首轮user/assistant；base格式`### Instruction ... ### Response`。cache位置t从answer_start-1到len(input_ids)-2，target=input_ids[t+1]，包含EOS答案目标；current=input_ids[t]。第一条答案的预测表征在Response前缀结尾，不能把所有current都叫答案token。
  - 可严格配回source_file/parquet row、完整可见前文`input_ids[:t+1]`、当前token、下一个标签、答案相对位置、来源和对话。不把右文当模型证据。
  - 精确归一化首user prompt去重；近重复未知。EVAL已多轮暴露。审计命名源代码：train.py只训练train并测eval；prepare_sft.py为DEV生成路由但不作exposure；bridge/mean/large-token只train/eval。因此DEV可作为本轮固定新复核面板，但不称新语料、外部独立或正式盲确认。

## 2. 可避免重算的派生输入

`B=E/analysis/frequency_contribution_bridge/20261019T025630Z`，资产`analysis_crosscoder_frequency_contribution_bridge_20261019t025630z`。

- `cache/train_definition.npz`：p[16384]、band[16384]、log_edges[5]、hit、coverage、top10。四段按正TRAIN p在log10上等宽，U单列；不是原来线性八段。
- `cache/groups.npz`：names[21]、owners[21,16384]、half_owners[2,16384]，phi及20个频率匹配随机组。四段各2子组，不能假设人数相等。
- `cache/{train,eval}_profiles.npz`：M[N,4]、R[N,4]、U/Ushare/total[N]、current/target/block/position/answer_position/identity以及hit/coverage。当前token词频、频率画像、严格位置身份已齐，可复用。
- `cache/routes_phi_{raw,calibrated}.npz`和`routes_random11...random30_{raw,calibrated}.npz`。已有42路由，不重算可复现主条件。
- 完整表：frequency_bands、train_feature_members、group_memberships、relation_review、half_stability、random_matching、designated_low_feature_exposure、dispatch_summary、expert_loads、composition_consistency、bridge_strata、token_ID_review、same_ID_sampling_status、text_sampling_coverage等。文本302卡可先复用，别重新挑漂亮例子。

`M=E/analysis/mean_component_frequency_routing/20261019T082513Z`，资产`analysis_crosscoder_mean_component_frequency_routing_20261019t082513z`。

- `metrics/train_fixed.npz`已含mu[1024]、m[16384]、raw decoder[16384,1024]、offset[1024]、learned_bias[1024]、bias、norms[16384]、a[4]、ak[8]、band、owner、p、scale。可直接计算字典方向/PCA投影，无需读5.6GB全ckpt。
- `metrics/{train,eval}_scores.npz`：M[N,4]、S[N,8]、route[4,N]（R0/R1/R2/R2b）、block/position，raw_winner/raw_runner、margin/baseline_margin/deviation_margin、all_below/fallback。
- `metrics/{train,eval}_C.npz`只有M/S/route及diagnostics[N,10]，**没有完整中心化后z，也没有14层原始h缓存**。C重新编码曾重做Base前向；本轮勿再做。
- 37张源表包括mean_components、feature_mean_projections、raw_margin_decomposition、route_transitions、feature_exposure、outside_composition、input_composition、reencoding_quality_summary及16张文本卡。

`L=E/analysis/token_feature_layer_validation/20261019T_validation`，资产`analysis_crosscoder_token_feature_layer_validation_20261019`。

- 已完成10,485,760 DCLM位置全窗，D5,238,097/V5,247,663；相同bin，文档独立未知。14层仅使用共享z乘各层decoder范数，并无14套层内编码。
- `tables/feature_token_correspondence.csv`、feature_level_support、layer_metrics、binary_metrics、groups、block_correlations、block_stability、migration与对应4图已有，不能把低频联系当未检验问题。
- 原cache `E/analysis/feature_relation_phase1/20261013T173130Z/feature_cache/rank*/...`约15GiB，完整z但**没有全量原始hidden**，若本轮主分析SFT，不应重复扫10M缓存。

## 3. 之前已经得到什么：新分析不得伪装新发现

1. 原末层幅度竞争把95.83%输入给最高段，低频接收0%；除TRAIN段均值R1后低频逐feature接收72.22%，162/1198仍零接收。完整输入共存：典型低频接收槽平均约1.38个B1激活、195.54个B4激活。激活项数不是信息/梯度/容量。
2. 关系细分相对随机接收增量小（72.22% vs20随机均值70.99%），组2/4严重5670/3及1096/1，成员稳定性不足。
3. 减均值R2接收17.58%，其最低频槽87.33%输入没有B1。ratio和subtraction不等价；真实h中心化C重建MSE33.59→61.99、低频仍0%。不是成功删除common。
4. 高频B4沿真实TRAIN均值方向投影-0.0931（EVAL-0.0712），offset和decoder bias不能遗漏。高频幅度大不等于表征均值。
5. 低频token与低频feature描述性对应受统计单位/语料影响：DCLM位置rho .006191、token-ID等权-.119041；Tulu .259051/.124371；feature等权support>=20为.339147/.119556。最低段极低支持，不能单义token标签/稀有知识认证。
6. 参数/响应谱：`representation_tulu_epoch1_expert_pca_svd_20261019t030056z`，执行`E/analysis/epoch1_expert_geometry/20261019T030056Z`，20个epoch1模型、130个exposure-qualified专家，W及DeltaW上/下/门投影完整1024谱、top16方向、固定probe响应PCA已有。属于**训练后专家参数/响应**，不能冒充冻结原始h的PCA或feature频率成分谱。此前`analysis_crosscoder_phi_group_input_spectrum_20261016`已读Daily报告：冻结186个R/F/N组，在旧DCLM EVAL512原始h上每组取128位置，145共同支持组；逐组中心化PCA、去各自第一主方向后残谱已有，R首份额12.5324% vs F13.1439% vs N14.0502%，剩余8.5749/9.0896/9.3402%。这不是当前Tulu四频段，也不是全局TRAIN PCA；不要重跑这个已答对照或混淆两种PCA对象。相关小源表/NPZ与4图在`daily_research_reports/1016/crosscoder_phi_input_spectrum/`，原执行`E/analysis/report_spectrum/20261016_phi_input_spectrum/`。另`analysis_crosscoder_report_spectra_20261016`为1119组×14成员的同频/混频组，不是186个phi组。

## 4. 最小且有区分力的表征扩展（建议，不是执行结果）

### A. 先区分“评分没选中”与“top1本身冲突”

冻结同一四段/8owner，使用现有每位置z，统计同位置有几个owner实际命中、低频命中横跨几个owner。先报告拥有低频目标的输入中，存在多owner低频同时命中的比例。再逐目标feature分解失败：第一阶段段竞争失败、段已选但子组竞争失败、tie/fallback。R1已有M/S，直接定位。

只改评分不改feature池可以改变winner，但一个token只送一个owner，不可能同时满足同位置所有不同owner目标。可给**诊断性事后oracle上界**：若macro接收定义是均值_i sum_t A_ti 1(route_t=e_i)/n_i，对每位置选择最大 sum_{i:e_i=e} A_ti/n_i。由可加性其值是该固定面板、固定名单的top1宏接收理论上界。此上界使用复核命中n_i，只是可行性诊断，不能部署或称泛化效果，也不能用来挑评分。部署建议评分只能用TRAIN统计冻结。

主要区分：若R1离上界很远，评分仍有改进空间；若接近上界，继续调评分无法解决多owner共存。两者都不能判断学习好坏。

### B. 同token的上下文差异，而不只做词频相关

TRAIN预选有>=50次、>=10对话支持的current ID（已有8ID抽样若不足，可新登记由TRAIN取支持最充足的8–16ID；不以EVAL画像选）；在DEV保留全部实际出现及NA，做within-ID低频份额/路由变异，来源dataset与答案位置分层，排除首答案预测前缀位置。固定ID输入不同上下文是否改变owner、是否只由newline/space/数字格式说明。对比current token identity、target身份和来源说明角色边界；target只作关联，不作路由输入。

比重复一条Spearman更区分“稀有token标签”与“上下文敏感的表征画像”。真实语义必须用随机/高份额完整可见前文、反例和支持数；字典feature可能多义，不能自动标签。

### C. 用现有h做中心化PCA与有符号几何，而非再减h重编码

仅TRAIN拟合mu和h中心化协方差，冻结前1/16个方向；DEV投影。报告完整谱摘要/前16及每频段解码向量在这些方向上的投影。使用raw decoder，保留offset/learned_bias/残差，区分有符号投影、平方能量与z||D||幅度代理。若计算各组向量和 v_b=sum_i z_i d_i，它们非正交，||sum_b v_b||²中有交叉项；不能强迫份额相加100%。可分开report组范数、方向对齐和总重建误差。

这能检验“高频主要位于大方差方向/共同方向”是否实际成立。PCA大方向不是功能common，也不是均值；固定编码z的几何投影不等于删除方向后再次编码。若本轮预算有限，优先A+B，C只做TRAIN PCA和decoder方向投影，不再次模型前向。

## 5. 建议本轮问题与边界

明确问题可缩到：**在固定末层表征和同一频率名单下，低频目标接收失败主要来自分数尺度，还是单token top1无法兼顾共同出现的不同频率/不同owner目标；上下文表征能否提供超出token稀有度的、可复核的分发信息？**

先复用R0/R1/R2，不以更多评分网格替代理解；任何新增评分在TRAIN设计、DEV固定复核。保留旧EVAL为描述参照，不称独立确认。深度分析可得“接收/组成/几何”的认识更新，不能得学习收益、容量、梯度干扰或语义知识难度。新训练、额外模型前向、扩大缓存并非本审计推荐的必要依赖。
