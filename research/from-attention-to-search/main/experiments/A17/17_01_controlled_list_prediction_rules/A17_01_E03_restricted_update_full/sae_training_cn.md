# 原始 o_proj 输出 SAE 训练子阶段

本记录从属于 E03 唯一 [Protocol](protocol_cn.md) 的 SAE 阶段，不另建 Protocol。研究者已授权：现有 Qwen SAE 与原始输出不匹配时，同配置重训 1B token SAE。科学判断仍为 Unknown。

当前：首次远程Smoke `pt-8bnbcqqj` 整体FAIL并保留；修复后的Smoke `pt-cr4i6ge9` 平台SUCCEEDED且21/21门PASS；授权1B Full `pt-h5t3h09w` 已于2026-10-09 18:21:42 UTC提交，现已平台SUCCEEDED，244380步完整1B及15项trainer门、独立TensorBoard末点门全部PASS；真实100M/300M/1B与可恢复状态已保存。整轮最多并发占用一个四卡 H100 reserved 节点。Stage1 和频率短阶段已先运行；这是资源排程，不是重新请求研究者审批。

E16 SAE 实际观察第27层归一化后的 MLP 输入；本轮要求最后 Attention `o_proj` 在残差相加前的原始输出。其 official parent 与当前 Base 的 config、safetensors 已逐字节一致核验。新 SAE 从 seed17 初始化，不把旧 MLP 输入字典转用到新接口。Base 全冻结、eval，没有 LM 优化器和参数更新。

原样复用 E16 字典、归一化 MSE 和确定性二进制流代码。字典30000、ReLU Top32、每步 decoder列归一化、不先单位化输入、不先减 decoder bias。AdamW LR3e-4、beta=(0.9,0.999)、eps1e-8、weight_decay0；10步线性warmup后恒定LR、clip1。AuxK512、dead-after50、权重1/32；norm异常值quantile0.999。序列1024，每rank一条、DP4、每批一步。保留原来各rank局部归一化MSE的平均作为优化目标；新增全局归一化诊断不替换该目标。

数据是 `dclm_pair_v1` 原2419训练文件及独立validation文件；模型与分词器ID为 `model_qwen3_0p6b_base_official_a5`、`tokenizer_qwen3_0p6b_base_official_a5`。2026-10-09 17:03:35 UTC 的本次限定输入访问检查通过；实际GPU加载仍由 Smoke 核验。

三个计数独立：每步4096个原始激活位置、4092个有实测下一词的预测位置、norm过滤后数量可变的SAE位置。沿用E16，SAE目标读所有无padding的原始激活，包括末位置；仅原生CE排除末位置。旧E16的1B是1,000,001,536 raw tokens。新Full固定244380步：1,000,002,960 valid prediction曝光、1,000,980,480 raw激活；向上取完整原globalbatch多2960 valid tokens，过滤后的实际SAE曝光另报。100M/300M/1B里程碑为24438/73314/244380步，对应100,000,296/300,000,888/1,000,002,960 valid tokens。每10000步和里程碑/末点存可恢复状态。

工程补齐TensorBoard全局原生CE及损失分量、valid/raw/eligible计数、每rank RNG、dead-feature状态、优化器、冻结配置/源码/数据身份、持久pod日志及实际保存清单。旧激活脚本已不存在；沿当前A17 runtime复用挂载的Python3.10 Transformers依赖层，提交采用 `shphd-lite-0911`。

Smoke提交前独立审计修复：clip返回norm及各梯度在opt.step前通过all-rank MIN finite guard；finite loss不代替finite gradient。保存重载还检查decoder字典及全部SAE参数有限。运行时核对精确Base config/weights磁盘SHA，rank0使用单writer lock；resume同时检查训练器及核心依赖SHA。Full单段wall cap6小时，预算仍为1B valid；必要时按已授权exact resume续段，不缩减token预算。ETA等待新Smoke/Full实际吞吐。

Smoke检查：开启观察hook与原生hidden精确一致；原始投影重放一致；全量Base状态digest保持；valid mask与计数一致；CE/重构/AuxK有限；重构优于零及初值；Top32；保存重载精确；TensorBoard必需tag有限、坐标单调。独立100步参考，对比60步保存退出后由新进程恢复到100步的SAE/optimizer/每rank dead状态/计数精确一致。所有Smoke通过后才从seed17全新初始化进入Full。

Top32资格保留原E16两项：mean positive features≥31.99；全rank实际使用feature union>32（原源码先MAX归并再资格）。另报告四rank各自使用数及范围，不把仅bias重构改叫字典合格。全局valid/raw计数每步由实际mask/激活行数归并累计，再与step期望核对，eligible独立累计。外进程resume还比较每rank RNG确切。TensorBoard覆盖6个raw/weighted损失组件的tokens/updates配对、原生CE、LR及eligible进度，保留两套坐标的相同数值。当前CPU真实收集5个分析代数/接口/舍入测试并通过，复用核心6项测试在实际runtime环境中通过；这些只授予工程准备资格。

执行目录 `/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae`：`configs/`保存真实配置，`source/`保存runtime/训练器/启动，`provenance/`保存复用哈希、差异与本次资产检查。实际Smoke/Full输出通过 `registration_request.json` 交根agent统一登记，未保存的计划末点不登记为现有资产。

训练完成不证明语义、稳定冲突、Router收益、Expert必要性或长期收益。后续分析保留真实模型状态、位置与字典parent/interface身份。

## 首次Smoke及工程修复

首个run `runs/smoke_20261009T174900Z` 实测4张H10080GB，每张81559MiB。100步参考与60步后新进程续到100步的trainer门分别全部通过：Base byte digest/no-op/raw projection精确，validation global NMSE .7532375→.4389872，正激活均32、实际feature union21960。两端有效预测409200、raw409600、eligible408800；全部TensorBoard组件及计数/RNG/dead状态精确。但最终SAE/Adam权重逐字节比较失败，因此整体Smoke FAIL，未进入Full。

独立只读审计由 `/root/stage1_full` 量化：最终encoder6/30,720,000元素不同、最大1.862645149230957e-9；decoder1/30,720,000元素不同、最大5.820766091346741e-11，bias同。Adam moments极小差异；所有共有JSON double metrics完全相同。原reference60状态被循环slot覆盖，首差不能定位到61。fresh与连续DDP桶重建/归约顺序是可信候选，尚未独立证明原因。

已授权的工程修复保留rank0参数bootstrap、DP4、局部归一化目标各rank平均、所有E16超参/数据流/dead状态；采用固定named_parameter顺序显式SUM/4再clip/Adam，避免重启依赖桶顺序。非capturable Adam step恢复CPU hosting；这恢复原状态载体，不改变算法。与原DDP在有限精度下可能有不同末位，明确记录。新Smoke永久保留60/61状态，阈值不放宽，重冻后通过全部门才执行1B。失败的源/配置/Protocol快照及实际产物保留；登记仅作ENGINEERING_SMOKE失败诊断资产。

## 修复后Smoke与实际Full提交

`runs/smoke_fix_20261009T1810Z` 的原生trainer门及外进程60→100比较全部通过；永久60/61状态额外通过SAE/optimizer与四rank RNG/dead/feature状态精确比较。全部21项Smoke门PASS。独立审计又按uint8字节复核60/61/100，并确认两端Adam step实际storage均为CPU。平台 `pt-cr4i6ge9` SUCCEEDED，监督于18:20:48 UTC保存实际terminal receipt。旧Smoke审计另确认原reference Adam step为CPU而旧resume为CUDA；这是状态hosting差异事实，尚未单独证明7个权重末位差的原因。

同一监督在双门满足后自动提交Full `pt-h5t3h09w`，执行目录 `runs/full_20261009T182142Z`。Full freeze manifest SHA为 `64ee50753d076dcc1c250f9eb4883375a4ff5f49238d33ccf1f8056648f092b0`，trainer SHA `82c656e24b0114520ad7bb82c3f234eef7f5ecd7ecf0b466d3cb1ff1d7e75119`、full config SHA `f32871af8aee37a22f5a7c7496a43759b1129a287bd0b756e2db6c4acbd38230`。预算/DP4/globalbatch未改。Smoke密集日志与60/61永久保存的吞吐不外推Full ETA；等待Full1000/2000步实测。

Full本地监督仅接收已有job/run，60秒采样，并分别记observed_at_utc与平台update_time。单writer锁与现有训练输出锁独立；前job实际终态之后，必要的6小时cap续段才按同配置/源码/数据合同恢复。续段前核实际恢复checkpoint的SHA、优化器CPU step、4rank状态与step/valid/raw/eligible计数；交root登记实际partial状态后fresh strict再消费。数值失败或未判明工程失败先诊断，不重置为新初始化Full，也不缩减预算。

18:42 UTC的实际Full进度：30000步、122,760,000 valid、122,880,000 raw、122,640,001 eligible；首100M的24438步SAE已实际保存，validation global NMSE0.1861948843、E16 rankmean0.1828896580、正激活均32。累计Full吞吐105885.73 valid/s，初步ETA约21:01 UTC；最终Base byte digest/重载/Top32/里程碑全门仍未检查。原生LM CE随固定Base读取不同语料窗变化，不代表Base训练改善。详见执行run的 [execution certificate](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/execution_certificate.md)。

19:10 UTC采样确认 Full 74000步、302,808,000 valid、303,104,000 raw、302,512,006 eligible。300M里程碑73314步/300,000,888 valid已真实保存，独立validation global NMSE0.1734112577、E16 rankmean0.1702980287、正激活均32。累计Full吞吐106056.83 valid/s，预计剩余约1.83小时（约21:00 UTC）；最终预算/冻结/重载门仍待终点。没有消费100M/300M字典选择本轮分析候选。


## 实际完整1B终态与保存资格

2026-10-09 20:59:44 UTC，平台 `pt-h5t3h09w` 完成SUCCEEDED；监督于21:00:36 UTC记录terminal PASS。单segment完整执行244380更新，实际1,000,002,960 valid预测曝光、1,000,980,480 raw激活、999,025,471 norm过滤后SAE位置。没有续段、reset或缩减预算。最终累计吞吐106374.50 valid/s只描述本次Full；Base没有更新。

全部15项trainer门PASS。独立validation的global normalized MSE从0.7532375346降到0.1684186278；E16目标对应rankmean从0.7532625124降到0.1652429625。平均正激活32；全rank使用feature union为30000，各rank为29999/29998/29998/29999。Base byte digest、观察no-op、原始投影、重载差0、参数/字典有限、计数与全部里程碑资格均通过。这证明当前冻结语料/接口上的工程与总体重构资格，不证明任务小分量保留、feature语义或功能分工。

独立末点遥测核验PASS：246条完整冻结cadence；6个raw/weighted组件tokens/updates数值与原生metrics逐项一致、末坐标精确到1,000,002,960 valid与244380更新。TensorBoard progress scalar的float32值为1,000,002,944（−16），与该整数的精确float32编码一致；整数event坐标、summary和checkpoint计数没有放宽。冻结源/config复核再次PASS。

最终SAE实际文件 `sae_full_final.pt`，SHA256 `1e16759da1ef1bad953d3df1bcf641c01b81edc87ca6b56d61b32251f41ebe64`。100M/300M/1B weights及recovery0/1均真实保存；初始随机SAE未另存，明确NOT_SAVED。100M/300M milestone没有保存eligible计数，保持NOT_RECORDED；raw标DERIVED_STEP_X_4096，不倒填历史metadata。1B/final及两个resume均使用原生valid/raw/eligible计数。CPU-native恢复完整性核验保留合同、四个optimizer state、四rank RNG/dead/feature状态；CPUmap检查不证明原storage hosting，也不声称Full实际执行续段。

实际交付root的独立 [enriched registration request](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/registration_request_enriched.json) 有3个asset条目及6个实际weight/state成员，全部SHA fresh重读，绑定当前run/job/summary/terminal/TB/freeze。producer初始字节与fresh子进程导出的独立字节副本均保留。该请求的工程身份通过27个CPU合法/失败案例及独立source复审；中央登记由root单独执行。证据在run的summary、terminal_verification、full_telemetry_qualification及training_freeze_terminal_verification中。后续分析只消费root实际登记后的1B字典。

root已实际登记最终SAE及两个resume ID，实际6成员加summary manifest的7个SHA复核通过，fresh strict3 PASS；receipt在run的`registration_request_enriched_root_bound_registered_outputs.json`，本次registry snapshot为`assets/checks/2026-10-10_a17_outputs_20261009T210301Z.json`。最终SAE ID：`sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z`。科学判断未由登记改变。
