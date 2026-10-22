# 研究资产库

本目录维护资产的**准确地址、身份、用途和访问证据**。当前登记 **514 条资产、10 个项目／存储入口**，覆盖当前共享／路由／SAE研究、原始预训练Qwen3-0.6B相关资产和实查的109缓存。条目包含checkpoint家族、不同版本、大小写别名和准备格式，不能当成同等数量的独立数据集。原始数据、权重和表征保留在原存储位置。

[English](README.md) · [唯一机器可读目录](catalog.json) · [历史全库访问快照](checks/2026-10-09_access_v4.json) · [检查工具](../tools/check_assets.py) · [项目访问与旧路径处理](../docs/project_access_cn.md)

[原始Qwen3-0.6B的SAE专项梳理](qwen3_0p6b_sae_cn.md)解释独立SAE、旧适配器与缓存，和fresh S7分别选用。

## 新对话怎样访问

1. 定位本次需要的资产ID。有明确地址时，先对照这个地址找到登记项；未登记时，在指定项目／缓存范围内查实际文件与来源，再补登记，不因没有索引项就宣称文件不存在。
2. 对**本次必需项**执行下列检查，实际尝试读取文件、遍历目录、读取注册的probe文件。不要只引用旧快照或看目录名。`--list`只是列ID，不能作为访问检查。
3. 需要使用内容时，再核对父检查点、层／张量位置、数据版本、分割、字段和原加载实现。`--strict`通过只证明登记的访问条件通过；不证明全量下载、权重hash相符、可完整加载、数据无污染或实验获准。
4. 若检查失败，检查登记位置、原manifest／config、实际挂载与符号链接；文档旧路径按项目访问说明使用迁移解析器。只有确认是同一身份的地址才可登记为替代位置，不能通过猜换`/data/share`与`/mnt/bucket`前缀、换模型或换数据解决。
5. 必需资产经过这些尝试仍缺失、不可读、已知不完整，或实际加载失败，就**暂停依赖它的工作**，报告资产ID、准确路径、错误、检查时间／用户上下文和已试位置。可选辅助路径缺失只记录；不能阻断不依赖它的工作。不得擅自下载、重训或重建缺失资产。
6. 访问与身份足够后，继续用户已授权的原任务。可读资产、已保存状态、执行完成都不授予新的训练或科学审批。

```sh
# 找ID，不读取大文件
python tools/check_assets.py --list --category model_checkpoint

# 当前S7＋对应固定SAE＋已有后训练数据；只检查所需依赖
python tools/check_assets.py --strict \
  --asset model_s7_fresh_lambda0p1_33b \
  --asset sae_fresh_s7_33b_embedded \
  --asset eighttask_audited_data

# 查询项目关联资产，并在新文件中保留访问快照
python tools/check_assets.py --project from-attention-to-search \
  --output /tmp/assets-access-NEW-TIMESTAMP.json
```

工具只做stat、文件首字节读取、目录遍历及注册probe检查。它不加载大tensor、不解码全部数据、不算GB文件hash、不访问网络、不调用GPU。保存快照拒绝覆盖旧文件。`--strict`退出码0为所选必要访问条件通过，1为所选依赖未通过，2为ID／配置／命令错误；未知ID应先查目录，不能当成资产不存在。

## 本次访问范围

最新检查：**2026-10-09 16:03:00，北京时间；有效UID=0**。10个项目／存储入口可访问，151条资产中150条的注册地址／必要probe本次可读；其中**9条只有元数据、1条模型下载不完整，另1条历史精确SFT数据路径缺失**。这11条不作为数据／模型通过strict。项目访问检查只覆盖目录和登记入口，不等于读完全部项目，也不保证新对话、普通用户或GPU容器权限相同。

| 项目／存储 | 地址 | 本次检查 |
|---|---|---|
| System：规则与访问入口 | `/data/250010109/Research_System` | 本次入口可访问 |
| 当前主研究项目 | `/data/250010109/Research_System/Projects/from-attention-to-search` | 本次入口可访问 |
| 路由表征梯度反馈独立项目 | `/data/250010109/Research_System/Projects/router-representation-coupling` | 本次入口可访问 |
| 扩散语言模型项目 | `/data/250010109/Research_System/Projects/diffusion-language-models` | 本次入口可访问 |
| 训练实现参考 | `/data/250010109/Research_System/Projects/decommon-router-training` | 本次入口可访问 |
| 评估实现参考 | `/data/250010109/Research_System/Projects/decommon-router-evaluation` | 本次入口可访问 |
| KV cache参考项目（只登记目录访问） | `/data/250010109/Research_System/Projects/kv_cache` | 本次入口可访问 |
| 学术写作项目 | `/data/250010109/Research_System/Projects/academic_writing` | 本次入口可访问 |
| 实验代码与原始产物执行工作区 | `/data/250010109/MoE_Router` | 本次入口可访问 |
| 共享数据与模型缓存存储 | `/data/share/109_cache_dir` | 本次入口可访问 |

## 优先使用的资产

下表是目录的阅读入口。完整对象、构造来源、接口、版本、probes和边界以`catalog.json`及原manifest／Protocol为准。

| 资产ID | 具体对象 | 实际地址 |
|---|---|---|
| `model_s7_fresh_lambda0p1_33b` | 当前8层fresh S7，精确33B token | [token_033000000000](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000) |
| `sae_fresh_s7_33b_embedded` | 当前S7末层SAE，与模型同一state.pt | [state.pt](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/state.pt) |
| `model_dense_33b` | Dense 33B对照 | [token_033000000000](/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_033000000000) |
| `model_sall_unit_weight_33b` | SALL 33B及八层SAE | [token_033000000000](/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/sall_unit_weight_continue_from_23b_8x5090/milestones/token_033000000000) |
| `sae_fresh_s7_step_zero` | 训练前随机SAE；不能当作已学特征 | [step_zero_sae.pt](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/analysis/step_zero_sae.pt) |
| `model_qwen3_0p6b_base` | 原始28层Qwen3预训练模型 | [Qwen3-0.6B-Base](/data/share/Qwen3-0.6B-Base) |
| `model_qwen3_0p6b_base_official_a5` | 历史训练实际记录的28层官方父模型 | [Qwen3-0.6B-Base-official](/data/250010109/model_cache/Qwen3-0.6B-Base-official) |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | 零起算索引27（第28层）MLP输入的独立SAE | [sae_full_final.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt) |
| `model_rrc_a3_a_endpoint` | A3路由反馈A：12层MoE，无SAE | [token_001999896576](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/runs/formal_coupled/milestones/token_001999896576) |
| `model_rrc_a3_b_endpoint` | A3路由反馈B：12层MoE，无SAE | [token_001999896576](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/runs/formal_router_input_detached/milestones/token_001999896576) |
| `representation_probe_33b_three_model` | 1003三模型c/a/r/e与SAE编码 | [dense_33b](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/probe_33b_01/dense_33b) |
| `representation_common_rule_controlled_0927` | 0927构造任务表征与虚拟更新位移 | [full_h100_20260928T010310Z](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z) |
| `representation_retention_smoke_1007` | 1007真实8+8步前后的表征读数 | [20261007T145134Z](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/runs/20261007T145134Z) |
| `adapter_checkpoint_retention_smoke_1007` | 1007工程Smoke适配器/恢复状态 | [20261007T145134Z](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/runs/20261007T145134Z) |
| `dclm_token_bins_global01` | DCLM原始分词bin，2420份/约1.21TB | [global-shard_01_of_10](/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10) |
| `dclm_pair_v1` | DCLM训练/验证配对视图 | [dclm_pair_v1](/data/250010109/training_data_views/dclm_pair_v1) |
| `dclm_raw_holdout_global02` | DCLM原始留出源；bucket地址 | [shard_00000000_processed.jsonl.zst](/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst) |
| `eighttask_audited_data` | GSM8K等八任务已准备tensor | [data](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data) |
| `m2d2_n8_v1` | M2D2八类自然文本面板 | [N8_v1](/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/data/N8_v1) |
| `ntp_statistics_panel_2048` | 0930/1002已曝光2048条自然面板 | [data](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data) |
| `data_rrc_a3_locked_analysis_documents` | A3冻结分析面板；TEST尚未分析 | [analysis_documents.jsonl](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/inputs/analysis_documents.jsonl) |
| `shared_109_cache_root` | 109共享缓存入口 | [109_cache_dir](/data/share/109_cache_dir) |

两个checkpoint家族也已登记：`checkpoint_family_fresh_s7_lambda0p1`、`checkpoint_families_dense_sall_continue`。只记录已在磁盘的milestones；配置里计划到35–50B不表示对应文件已存在。家族的latest指针不能替代指定的精确检查点身份。

## 109共享缓存

总入口：`/data/share/109_cache_dir`。`hf_data/hub`登记42个dataset repo别名及1个Qwen2.5分词器repo；`hf_data/datasets`登记39条Arrow准备缓存；`hf_data/dclm_bin`登记2420份token bin。不同repo别名／snapshot／Arrow配置保留原地址，不静默合并成同一数据身份。

已列入GSM8K、MMLU、HumanEval、MBPP、ARC、HellaSwag、PIQA、RACE、LAMBADA、SocialIQA、CommonsenseQA、Winogrande、SciQ、OpenBookQA、IFEval，以及UltraChat、UltraFeedback、Tulu、Magpie、Orca-DPO、Magicoder、Code-Feedback、MetaMathQA、OpenHermes等缓存。另登记执行目录中的M2D2、PAWS、P_rel和八任务准备数据。存在的revision、refs、代表文件和实际准备路径已保存；没有核对上游全量文件清单，不能称为所有分割完整下载。

DCLM有2420个uint32 bin，总文件字节约1.21TB；`dclm_pair_v1`把2419个训练shard和1个验证shard分开。原始compressed holdout的登记地址在`/mnt/bucket`，同名`/data/share`候选不存在；它仅是可选历史地址，当前有效源仍可访问。

下列项的目录／元数据可访问，但不能当成准备完整的数据或权重：

| 资产ID | 对象 | 资格限制 |
|---|---|---|
| `hf_hub_magpie_align_magpie_qwen2_pro_200k_chinese` | Magpie-Align/Magpie-Qwen2-Pro-200K-Chinese 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_allenai_social_i_qa` | allenai/social_i_qa 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_derek_thomas_scienceqa` | derek-thomas/ScienceQA 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_m_a_p_coig_cqia` | m-a-p/COIG-CQIA 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_piqa` | piqa 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_social_i_qa` | social_i_qa 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_tatsu_lab_alpaca` | tatsu-lab/alpaca 本地Hub缓存 | `METADATA_ONLY` |
| `hf_hub_ybisk_piqa` | ybisk/piqa 本地Hub缓存 | `METADATA_ONLY` |
| `hf_prepared_web_of_science` | web_of_science Arrow缓存 | `METADATA_ONLY` |
| `qwen3_next_80b_incomplete` | Qwen3-Next-80B-A3B-Instruct未完成下载 | `INCOMPLETE` |
| `data_qwen3_0p6b_senior_exact_sft_legacy_missing` | 历史外部精确SFT数据路径不可用，未确认同身份替代地址 | `PAYLOAD_MISSING` |

Qwen3-Next-80B下载含8个`.incomplete`，没有登记成完整可用模型。其余`NOT_VERIFIED`的evaluate／metrics／modules／NLTK缓存只登记目录，未核对运行依赖。

## 使用时必须保留的区别

- **模型与SAE身份：**S7是8层、隐藏1024；末层Attention输出SAE内嵌同一个`state.pt`。SALL有八层SAE；原始Qwen3-0.6B是28层。A3是12层、隐藏512的另一套MoE，没有SAE；不能给它挂上S7的SAE。训练前随机SAE另列，不能当作训练后的分析工具。
- **表征字段：**1003的`c`是投影输入、`a`是投影输出、`r`是真实原生残差、`e`是损失对`a`的梯度；`e`不是SAE重构残差。每个模型有自己的坐标，不能默认对齐。0927有限位移来自一次虚拟矩阵更新；1007是真实短程支路训练读数。两者用途不同。
- **数据来源：**八任务缓存的train／dev／test是内部重新划分，含官方test来源记录；自然面板已曝光。可访问不等于新的确认集。M2D2 N8_v1的`math.AG`与legacy的`math.AP`分别登记。A3冻结分析面板存在不代表TEST或功能分析已执行。
- **代码迁移：**0927旧worker仍引用已迁走的daily helper；合法迁移地址与小文件hash已记录在对应表征资产中。读取数值资产可用，直接重跑旧worker前需要处理引用，不能据此重写历史结果。

## 训练与分析的资产闭环

### 使用前：核对本阶段真正需要的输入

按上面的访问流程检查，并把稳定资产ID写入Protocol／config或分析输入manifest：
父模型、tokenizer、数据版本与划分，以及实际用到的固定SAE、适配器或已保存表征。
加载适配器或内嵌SAE时，也要列出必需的父检查点。核对准确的层、张量位置、预处理与加载实现；
隐藏维数相同不代表模型版本或挂点兼容。旧访问快照不能代替本次检查。
只阅读报告、查询作业状态时，不要求加载该项目的全部原始资产。

训练Protocol／config必须写明最终checkpoint及必要里程碑的保存位置。
已获准的实现将其保存在执行目录中。只保存权重的文件与能够接续训练的完整状态是不同对象；
明确需要哪一种，不能把任何权重文件都说成可精确恢复训练。

### 保存后：登记实际产生的checkpoint

训练保存产物后，在结束资产交接前完成登记；工程Smoke和正式训练都适用，但保留各自用途。
选定的最终／可复用版本使用稳定ID。其余实际里程碑可以通过家族条目的明确成员列表或已保存manifest统一登记；
计划的token预算、会变化的latest指针不能代替成员身份。新训练版本不能覆盖旧版本的ID。

| 需要登记的信息 | 具体写什么 |
|---|---|
| 对象与实际访问 | 类别／类型、已保存文件的绝对路径、必需权重probe、payload状态、原存储归属 |
| 产生来源 | Protocol地址／版本、可查的run／job ID、实际代码／config与来源manifest |
| 必需输入 | 父模型／adapter／SAE的ID、tokenizer、数据版本／划分；补录历史时可先写待登记的外部地址，这不豁免使用前检查 |
| 模型／SAE接口 | 架构、准确层／张量或state key、适配器插入位置、SAE维数／TopK／预处理、原加载源码 |
| 实际训练进度 | 已保存的optimizer step、实际有效训练token数、计数口径和证据；不能用计划预算替代 |
| 身份与核实程度 | 原manifest记录的hash／大小及来源；区分转录的hash证据与本次重算，缺失字段写Unknown |
| 能否接续训练 | 实际保存了哪些权重、optimizer／scheduler、RNG、计数器和数据位置；恢复证据或NOT_CHECKED |
| 使用边界 | 工程Smoke、随机初态、已训练端点或部分产物；可读产物与科学证据资格分别记录 |

字段按实际对象填写：不适用写NOT_APPLICABLE，证据缺失写Unknown，未做的核实写NOT_CHECKED。
后续实际使用时，必需的历史输入若尚无ID，要先按查找流程补登记，再进行访问检查。

这些内容放入既有的identity、source_paths、locations、notes_cn与payload_status字段，
不另建一套目录格式。内嵌SAE关联承载它的model state；独立SAE关联训练它时使用的父模型和输入位置；
适配器关联加载它所需的基座权重。分析产生可复用的表征或SAE特征时，也登记产生它的模型、SAE、数据划分及字段定义。

检查新增产物ID，在checks/保存**新的**访问快照，并由执行manifest／Detailed链接资产ID和快照。
登记不要求重训、计算GB级hash或启动GPU加载；使用已有核实证据，并注明哪些未检查。
权重、数据与表征仍在原执行／存储地址，不能放进Git。

保存或访问失败时保留失败事实，只登记确实存在的部分产物与限制；必要时标INCOMPLETE／PAYLOAD_MISSING。
不能根据作业成功消息就说checkpoint已保存、可恢复。不能为补齐目录擅自重跑、下载或改变科学判断；
应明确交付仍缺哪个checkpoint。

## 怎样维护

`catalog.json`是唯一资产地址／身份登记；本README解释使用规则与核心条目，`checks/`保存时间化访问证据。登记时写ID、类别、用途、所属项目、绝对地址／必要probe、父模型／数据版本、原manifest／加载实现、已知缺口。`projects`表示使用关系；`required_projects`才表示必须同时可访问的项目依赖。optional位置是辅助信息，不能自动替代required主位置。

新增版本登记新身份或追加有理由的更正。重新检查保存新快照，不覆盖旧快照；当前地址改变不改旧实验收据、原数据、历史配置或结果。`2026-10-09_access.json`是首次整合的旧检查，三个JSON数据文件一度误归元数据位置；原因及更正在catalog中记录，v2保留更正后的历史检查。v3增加Qwen资产，v4明确检查全10个入口和151条资产，当前全库检查以v4为准。

本轮保存的是小型目录／来源与访问记录，没有复制1.21TB数据、checkpoint或表征payload。Git同步目录不保证另一环境取得实际资产；项目科学设计与授权仍由原Anchor／Protocol／Summary拥有。

登记后同步受影响的阅读指南和当前快照链接；条目数从catalog计算，说明快照实际覆盖范围。
不能为了整理索引改写旧快照，或移动归属其他执行目录的资产。

[A17 list-rule release and Smoke assets](a17_list_rules.md): newly generated dataset; scoped access checks do not replace the dated whole-library inventory.

## A17新增实际产物（2026-10-10）

首末规则E03原生Full六家族、42个实际milestone，频率Full126家族、504个实际milestone均已登记；另登记各Smoke和两版选择manifest，保留工程/科学边界。当前权重检查只覆盖本轮所选ID，不把历史全库快照当成新增资产的访问证据。

[E03当前访问检查](checks/2026-10-10_a17_outputs_20261009T173255Z.json) · [频率当前访问检查](checks/2026-10-10_a17_outputs_20261009T175342Z.json) · [SAE选择v2检查](checks/2026-10-10_a17_outputs_20261009T174031Z.json)。精确resume、实际保存成员/哈希和父模型仍见catalog与执行receipt，目录存在不等于独立完整LM。

匹配raw `o_proj`的新SAE已完成获授权的1B有效预测位置Full。旧E16仍是MLP输入字典；新字典使用独立资产身份，不替换旧字典。

匹配原始输出的首次 SAE Smoke（`pt-8bnbcqqj`）未通过权重/优化器逐字节恢复。六个实际 SAE/恢复输出已登记，整体工程 FAIL、科学 NOT_EVALUATED；可读性通过不赋予1B字典资格。[失败输出登记证据](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/smoke_20261009T174900Z/registration_request_failure_schema_fixed_registered_outputs.json)。

修复 SAE Smoke（`pt-cr4i6ge9`）成功，21/21检查及独立逐字节复审通过。十个实际权重/恢复资产（含永久60/61步）可读性和14个文件SHA核验通过。[Smoke实际输出登记](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/smoke_fix_20261009T1810Z/registration_request_enriched_root_bound_registered_outputs.json)。

Full `pt-h5t3h09w`成功完成244,380次更新：1,000,002,960个有效预测位置、1,000,980,480个原始激活、999,025,471个SAE可用位置。资产`sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z`登记最终字典及三个实际milestone权重，另有两个独立恢复checkpoint ID。三ID均通过[当前所选访问检查](checks/2026-10-10_a17_outputs_20261009T210301Z.json)，七个载荷/manifest SHA核验通过。[登记收据](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/registration_request_enriched_root_bound_registered_outputs.json)绑定实际job、15项trainer门、246点完整遥测与原生保存计数。100M/300M milestone未记录eligible计数，raw计数明确来自合同推导；Full未执行续段。分析尚待完成，可访问与重建资格不建立功能分工结论。


### A17 analysis outputs recovered on 2026-10-10

当前访问/保存状态：频率36对终点SAE描述已由`pt-h6ke4emg`完成，共28,800条记录，实际载荷登记为`analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`。上段“分析尚待完成”是1B训练报告写成时的历史状态。主SAE旧作业`pt-azc2zkl5`实际FAILED，保留全部失败：八个完整Qwen状态、S7列表，以及Qwen71/u100的104/960条不完整干预分别按范围登记为五个representation资产；部分输入可访问不授予完整结果资格。新原生梯度/回放恢复尚未完成GPU测量。

[旧作业五个范围登记收据索引](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/provenance/recovery_registration/root_registered_request_index.json) · [频率终点访问检查](checks/2026-10-10_a17_outputs_20261010T093323Z.json)。这些是当前所选新增资产访问检查，不是重做全库inventory；字节完整性、原生测量资格、SAE重构质量和功能解释保持不同边界。


### A17当前分析完成状态

全部已授权分析分支已工程完成并登记；旧job失败状态不变。S7复用嵌入式SAE，64原生条件在独立CPU均值验收恢复后通过。新资产`representation_a17_raw_sae_s7_summary_recovery_20261010t104246z_s7_native_dclm`及[当前选定输出访问快照](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z_access.json)由[完成核验](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z.json)绑定；此次核验不是全库访问复查。上方准备记录中的分析pending为历史状态，科学机制判断仍Unknown。

### A17 paired-rule margin output (2026-10-10)

完整分析资产 `representation_a17_paired_rule_margin_20261010t141041z` 已登记：7状态、280有限更新条件、每条件60对列表；330输入/642产物哈希核验通过。18个主要更新均改善接收loss，但双答案优势12提高、6下降，冻结描述性判定为异质/不足；机制/关闭Unknown。 [Registration](/data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin/audit/registration_request_registered_outputs.json) · [Selected access](checks/2026-10-10_a17_outputs_20261010T144031Z.json).

### A17_03 actual sequential outputs (Asia/Shanghai2026-10-11)

已登记40个实际检查点家族（16Smoke、24Full）、一个原生读数/梯度子空间家族，保存状态44Smoke/114Full。全部父模型、数据、代码、有效答案计数和状态哈希在收据；登记不授予科学机制结论。 [Receipt](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/registration_request_registered_outputs.json) · [Selected access](checks/2026-10-10_a17_outputs_20261010T172742Z.json).

2026-10-11 A17成分分析输出：[本次选择访问检查](checks/2026-10-11_a17_component_causality_outputs_0233.json)仅覆盖新登记的Smoke和Full读数家族，两者可访问；不是全库刷新。实际Smoke140条件、Full630条件，没有新训练检查点。


### A17 trajectory-state analysis completed (2026-10-11)

Smoke12/replay4 and Full108 actual finite readouts are registered, no new trained checkpoints. [Current selected access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_trajectory_20261011T090921Z.json) covers these two output IDs only. [Canonical Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_03_old_task_sensitive_update/A17_03_E03_trajectory_mechanism/summary_cn.md) preserves state/order heterogeneity and incomplete100-step mechanism boundary.

### A17_04 条件映射执行完成（2026-10-11）

Smoke 与 Full 实际保存120个状态，归入28个 adapter 族与两个原生读数族。派生分析 `analysis_a17_04_mapping_20261011t095038z` 独立登记。[30产物访问](checks/2026-10-11_a17_mapping_output_access.json)与[派生分析访问](checks/2026-10-11_a17_mapping_analysis_access.json)通过选定检查，不是全库刷新。[正式 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary_cn.md)记录旧映射学习资格不足；完成不证明已学规则干扰。检查点需要精确登记的父 Base。


## A17联合与模式分区视图（2026-10-12）

`data_a17_shared_routed_joint_v1`登记4800条TRAIN／1600条已暴露DEV；`data_a17_shared_routed_mode_partition_v1`登记同一数据的模式一／二精确分区。两ID引用同一派生版本，不增加标签，不建立未暴露TEST。载荷位于 `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1`。[本次严格可读性检查](checks/2026-10-12_a17_e04_prepared_views.json)不证明学习或路由收益。


E04实际输出已登记10族／55状态，来自pt-1rb3s2t0。[严格输出可读性](checks/2026-10-12_a17_e04_actual_checkpoints.json)。工程PASS与学习资格NOT_PASSED分别记录，不构成正式结构收益结论。

### Qwen3 全层 CrossCoder 的 DCLM 试跑数据（2026-10-12）

`data_qwen3_alllayer_crosscoder_dclm_pilot_50m_v3` 登记实际生成的 50,000,000 个 TRAIN 位置和 1,048,576 个 VAL 位置，使用冻结 Qwen3 Base 的分词器，并按文档及已发现的重复组划分。[本次定向访问检查](checks/2026-10-12_qwen_crosscoder_pilot_50m.json)通过；这不是计划中的正式 20 亿数据集。近重复检索有上限，不代表穷举去重。登记时尚无训练后的 CrossCoder checkpoint。

[S7 跨checkpoint CrossCoder输入与任务](s7_temporal_crosscoder_cn.md)：精确1B/5B/15B/31B输入已核验；提交任务不等于存在训练完成的字典。


[CrossCoder阶段一实存缓存与分析](crosscoder_feature_phase1_cn.md)：最终14层完整VAL；图、文本、热图与当前访问检查。登记不授予科研结论或下一阶段执行权。

## 2026-10-16 CrossCoder关系分组到学习验证产物

[阅读入口](../daily_research_reports/1016/crosscoder_relation_learning/README_cn.md)。两版缓存、54正式状态/9final、Smoke及完整有界分析已登记并通过选定严格访问检查。稳定ID见英文同节与catalog；访问不授予科学批准，报告保留负学习结果及原strict样本NA。


### 2026-10-19 频率贡献桥梁与关系细分

`analysis_crosscoder_frequency_contribution_bridge_20261019t025630z` 登记已保存的无训练A–C分析：4个频率段、21种名单、42种路由、84套分发矩阵及302张文本卡。[中文概要](../Projects/from-attention-to-search/main/experiments/A15/15_22_frequency_contribution_relation_refinement/20261019_bridge_dispatch/summary_cn.md) · [本次输出访问核验](checks/2026-10-19_frequency_contribution_bridge_outputs.json)。仅为已查看EVAL上的探索性结构与分发证据，不授予学习、容量结论或下一轮执行权限。

## 大样本与跨层token—feature关联

注册资产 `analysis_crosscoder_token_feature_layer_validation_20261019`：复用DCLM发现/复核5,238,097/5,247,663位置及原Tulu，14层共享z上的解码幅度；无模型前向或训练。分开保留feature、位置、tokenID等权及旧池迁移。仅注册实际分析产物，不提升科学结论。
