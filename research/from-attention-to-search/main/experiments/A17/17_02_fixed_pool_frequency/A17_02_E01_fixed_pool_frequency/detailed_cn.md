# Detailed：A17_02_E01 固定池呈现频率实验

[English](detailed.md) · [Summary](summary_cn.md) · [Protocol](protocol_cn.md)

## 0. Quick Recap：当前事实

Full 完成126条轨迹、90,000个训练答案、4500步。工程1520/1520通过，实际曝光下未见资格126/126通过。确认 n6 满足 `REGISTERED_POSITIVE_MEDIAN_INTERACTION`，中位数0.066142 nat/答案。同规则额外 CE 收益更大，异规则相对 B-only 仍有净 CE 收益；准确率未必提高。人类机制解释与关闭判断 `Unknown`。

## 1. Terminology / Definitions：对象先定义

A 是增加的练习，B 是被评估的接收任务；每次呈现只监督一个下一个答案。FIRST/LAST 都有可见指令，可以同时满足。A/B 组名只在元数据，不进入提示。频率重复固定200列表池。顺序未见保留实际训练过的 B 内容组、改变顺序；组合未见使用实际 A/B 训练中没出现的内容组。CE 是正确答案的全词表交叉熵，accuracy 是全词表 argmax 是否正确，两者方向可能不同。

## 2. Anchor Link And Decision Point：问题与下一判断

[独立 Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor_cn.md) 拥有固定 B 的规则×呈现交互设计；[频率 Focus](../../../../focus/focus_fixed_pool_frequency_shared_learning_cn.md) 拥有研究者下一步机制判断。本记录补齐实际测量与统计分支，不关闭问题、不批准架构结论。

## 3. Protocol Freeze, Conformance, And Deviations：冻结、符合与修订

唯一 Protocol、源码、配置、数据在 Smoke 或探索之前归档：[Full冻结来源](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/frozen_sources.json)。config SHA256 `a8bb067fa5f4b4fe47a7430576bc8fdfa25866c7a410fe43f02bd77fdfcf596d`；归档 Protocol SHA256 `3c94773c97c12d5ce7fdbdd9aef7dc88f9625f64d13732941fe1807444cda3d0`。实际训练读取 run/source，不使用后来可修改的辅助脚本。

提交前 amendment01：v1 仅生成、从未在本实验提交或模型评估，其 test 有40条规则记录与旧 E01 已评估 dev 重合。保留 v1 和原未提交冻结。实际 v2 排除旧全部30个内容轨道，新 A/B/dev/test 与旧 train/dev/test 内容组交集全部为零。只按列表身份过滤，不用模型效果选择；规模、均衡、条件、估计对象没有改变。[数据资格](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/data/fixed_pool_v2/qualification.json)。

没有按 dev 选择参数、条件、种子或阈值；所有有效不利结果保留。两个 Full 阶段无运行修复、无打开 test 后调参重跑。事后曝光审计、登记导出、汇总和图是派生产物，独立于不可变训练来源与原产物清单。Full 每个末点未做独立外进程恢复，保持 NOT_CHECKED，不能把存了状态等同于已验证可恢复。

## 4. Actual Setup：实际设置

输入 `model_qwen3_0p6b_base`、`data_a17_fixed_pool_frequency_v2`，tokenizer 与 Base 一致。A/B 各400条首末配对记录＝200个不同有序列表＝100个无序内容组；dev/test 各800条，每个规则×未见分项200条，每个词在每个位置及答案恰好10次。两规则共享模板，答案来自20个合格中文单词元。

每轨迹恢复原 Base。只更新 `model.layers.27.self_attn.o_proj.weight`，FP32[1024,2048]，2,097,152参数。AdamW 恒定 LR1e-4 从第一步生效，betas(.9,.95)、eps1e-8、weight_decay0、clip1。micro5×累积4×DP1＝20有效答案/步；BF16训练，原生 FP32主评估，BF16次评估。其余参数每 worker 前后完整字节 hash 一致，每轨迹参数版本不变。频率学习器没有路由器、专家、LoRA 或 SAE 更新。

| 条件 | A呈现 | B呈现 | 更新步 |
|---|---:|---:|---:|
| b_only | 0 | 200 | 10 |
| same_200 / diff_200 | 200 | 200 | 20 |
| same_800 / diff_800 | 800 | 200 | 50 |
| same_budget / diff_budget | 500 | 500 | 50 |

B=FIRST、LAST 都运行七条件。探索29/43/71：42轨迹、30,000答案、1500步，只评 dev。确认101/113/127/139/151/163：84轨迹、60,000答案、3000步，用模型未评估的新 test。同一种子/角色/配额下，同/异规则使用配对池身份与呈现位置。500次由两次完整200加五个完整20循环块构成100余数，保持精确均衡。

硬件：ACP h100-4-reserved，share-space/share-cluster，n6ls.iu.i40.4，单 reserved 节点、四个独立 GPU worker，各策略间没有 DDP。Smoke pt-cgmiw5f3：UTC17:35:59→17:37:05。Full pt-ho4byzg4：UTC2026-10-09 17:40:21→17:48:33／北京时间2026-10-10 01:40:21→01:48:33。[执行证书](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/execution_certificate.md)、[平台终态](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/platform_terminal.json)。

## 5. Metrics And Registered Decision Rules：指标与判据

L 是种子 s、B规则 r、A呈现 n、未见面板 p、同/异规则关系下，B 的 FP32平均答案 CE。B 固定200时，唯一主指标为：

\[
I_s=\frac14\sum_{r\in\{\mathrm{FIRST},\mathrm{LAST}\}}\sum_{p\in\{\mathrm{order},\mathrm{combination}\}}
\left[(L^{\mathrm{different}}_{s,r,800,p}-L^{\mathrm{same}}_{s,r,800,p})-(L^{\mathrm{different}}_{s,r,200,p}-L^{\mathrm{same}}_{s,r,200,p})\right].
\]

每个种子等权合并两个 B规则和两种未见。独立重复 n6；六个 I 都大于+0.01或都小于−0.01，通过冻结保守双侧符号规则 p=.03125。[min,max] 在独立同分布种子效果假设下对种子总体中位数覆盖率至少96.875%；不是均值置信区间，也不是跨数据集区间。探索 n3 仅描述。分项必须保留，不能救回主指标。

净加练比较各 A 条件减 B-only，B200固定但总计算不同。预算比较 A800/B200 减 A500/B500，答案总计1000相同但 B 机会不同。次级结果没有额外确认检验。A 源有效学习不门控完整训练策略估计；如要说局部更新机制需另守资格。日志保留答案归一化损失、梯度范数、LR、批次/token/步计数、epoch equivalents、耗时、峰值显存和 TensorBoard；评估 token 不进入训练答案计数。

## 6. Evidence Lineage：证据链

数据资格与清单→当轮严格输入检查→11项 CPU 配额/oracle/统计反例测试→不可变源码/配置/Protocol冻结→Smoke外进程恢复与 no-op→所有轨迹日志/呈现顺序/保存状态→Full工程审计与主次分析→终点和平台验证→独立实际曝光审计→保存家族 SHA 核验及登记。

[Raw Full](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z) · [Confirmation](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/analysis_confirmation.json) · [Engineering](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/engineering_audit_confirmation.json) · [Terminal](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/terminal_verification.json) · [Platform](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/platform_terminal.json) · [Actual asset registration](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/asset_registration_request_registered_outputs.json)

[探索](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/analysis_exploration.json) · [曝光资格](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/actual_exposure_novelty_audit.json) · [原产物清单](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/artifact_manifest.json) · [描述汇总](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/descriptive_aggregates.json) · [实际登记request](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/asset_registration_request.json)。root独立核验126家族1008个成员文件 SHA，全部126严格输出检查通过。snapshot `assets/checks/2026-10-10_a17_outputs_20261009T175342Z.json`。每家族真实保存 update0、2、中间、最终；原始 Base 仍是必须的外部父权重。

正确 loader：`state.pt['trainable_weights']` 是完整 FP32 Tensor[1024,2048]，不是带名字的字典或 ΔW。状态包含 AdamW、Python/NumPy/CPU/CUDA RNG、optimizer_step、tokens_seen、next_data_position、task、config_sha256、presentation_order_sha256、parent_asset_id、data_asset_id。恒定 LR 不需 scheduler。Smoke 已验证外进程2→3精确恢复；Full终点是实际保存，未逐个验证恢复。

## 7. Main Results：完整结果

探索交互：29=0.084158、43=0.072401、71=0.080150；中位0.080150、均值0.078903，状态 EXPLORATORY_ONLY，没有据此调整确认。

确认中位0.066142、均值0.066663、最小0.051485、最大0.078583。六个都超过δ；统计分支 REGISTERED_POSITIVE_MEDIAN_INTERACTION，保守双侧 p=.03125。24个规则/面板分项完整保留：

| Seed | FIRST/order | FIRST/combination | LAST/order | LAST/combination | Combined I |
|---|---:|---:|---:|---:|---:|
| 101 | 0.050108 | 0.058124 | 0.077245 | 0.085900 | 0.067844 |
| 113 | 0.049365 | 0.046607 | 0.043948 | 0.066021 | 0.051485 |
| 127 | 0.084904 | 0.080098 | 0.059640 | 0.089692 | 0.078583 |
| 139 | 0.049090 | 0.053218 | 0.070306 | 0.085149 | 0.064441 |
| 151 | 0.061409 | 0.065484 | 0.072749 | 0.095515 | 0.073789 |
| 163 | 0.062496 | 0.058504 | 0.050445 | 0.083892 | 0.063834 |


| B rule / panel | Median across six seeds | Minimum | Maximum |
|---|---:|---:|---:|
| FIRST/order_new | 0.055758 | 0.049090 | 0.084904 |
| FIRST/combination_new | 0.058314 | 0.046607 | 0.080098 |
| LAST/order_new | 0.064973 | 0.043948 | 0.077245 |
| LAST/combination_new | 0.085524 | 0.066021 | 0.095515 |


正 I 表示 A200→800 期间，同规则带来更大的额外 CE 收益，没有直接表示异规则造成净伤害。下表先对每个种子/面板等权平均两 B规则，再取六种子的中位数；combined 先平均两种未见再取中位数。分项中位数不要求能相加得出合并中位数。

| Policy | Order-new CE | Combination-new CE | Combined CE | Combined accuracy |
|---|---:|---:|---:|---:|
| b_only | 0.801364 | 0.796052 | 0.798928 | 83.4375% |
| same_200 | 0.708025 | 0.699505 | 0.703617 | 87.1875% |
| diff_200 | 0.725715 | 0.721578 | 0.723807 | 85.5000% |
| same_800 | 0.590033 | 0.574224 | 0.582623 | 89.1250% |
| diff_800 | 0.669000 | 0.666243 | 0.667780 | 83.2500% |
| same_budget | 0.576972 | 0.570751 | 0.573273 | 89.7500% |
| diff_budget | 0.629074 | 0.627753 | 0.627808 | 85.6875% |


未更新的原 Base 在800条确认 test 上 CE1.007858、accuracy78.1250%，已经有部分能力但未完整掌握本任务。这里不研究从头学习。

| Extra A policy at B200 | Median seed combined CE minus B-only | Negative role/panel cells |
|---|---:|---:|
| same_200 | -0.095448 | 24/24 |
| diff_200 | -0.074815 | 24/24 |
| same_800 | -0.216990 | 24/24 |
| diff_800 | -0.131207 | 24/24 |


四加练条件的全部96个分项 CE 差值均为负。异规则 A800/B200 的 CE 优于 B-only，但准确率中位83.2500% 对83.4375%；同规则 A800/B200 为89.1250%。保留 CE 与正确率两个观察，不把“帮助少”改称净干扰。

| Relation | Median seed combined CE: A800/B200 minus A500/B500 | Positive role/panel cells |
|---|---:|---:|
| same | 0.008747 | 16/24 |
| diff | 0.040762 | 24/24 |


两个关系中六个合并预算差值都为正；same 分项16正8负，diff分项24正。这是改变 B 机会后的分配结果，不是纯频率。FP32 是冻结主读数；每个终点的 final_evaluation_bf16.json 均保留，不用精度选择替换主结果。

次级 BF16 合并交互中位0.065845，六个描述值也都超过0.01。全部确认策略中 FP32/BF16 分项 CE 最大差0.007634 nat/答案，正确率最大相差3个百分点。这些精度差异保留，没有以次级检验替代冻结 FP32 主结果。[精度记录](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/secondary_precision_description.json)。

## 8. Visualization Results, When Decision-Relevant：图怎样支持结论

![冻结确认与独立净收益](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/figures/frequency_confirmation.png)

左上：六个独立主交互全部超过0.01；右上：首末规则和两种未见分项都保留。左下：按策略分别画顺序未见、组合未见与合并 CE 中位数；右下：六种子的净加练 CE 都低于 B-only。点是种子，线标中位数，不是置信带。策略横轴是类别，不是时间。[独立PDF](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/figures/frequency_confirmation.pdf)、[图来源/hash](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/figures/provenance.json) 保存输入和绘图源码 SHA，图没有引入新的统计检验。

## 9. Stage Evidence And Failure Decomposition：工程与科学状态分开

v2数据通过，CPU11/11通过。Smoke56/56通过：4条各8步＝640训练答案/32步；额外80答案是恢复校准，不计科学轨迹。截断 Smoke 实际覆盖只有部分 B组，不能给所有预设 order-new 标签完整资格，始终只作工程证据。[Smoke曝光审计](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/smoke_4h100_v2_20261009T172146Z/actual_exposure_novelty_audit.json)。

Full探索508/508、确认1012/1012通过，126条实际曝光未见资格全部满足。平台 SUCCEEDED 独立落盘，不由日志猜测。126个最终权重及家族里程碑真实保存并登记。v1重合是提交前资格修复，不是训练失败或科学负结果。Full末点外进程恢复仍为 NOT_CHECKED。确认统计分支通过，不能代替人类机制解释、用途或关闭判断。

## 10. Full Experiment Record：本轮完整记录及后续

本轮北京时间2026-10-10：问题/假设是固定 B 的规则×呈现中位交互（§2、§5）。设置/对照是恢复原 Base、末层直接矩阵、七策略、均衡固定池、两个 B规则及恒定20答案更新（§4）。数据/确认划分是 v2、dev探索和六个新种子模型未评估 test（§3–4）。结果是已完成的正统计分支、净 CE 收益、单独保留的正确率与预算观察（§7）。启发是异规则仍能提供净 CE 收益，同规则的额外收益更大。研究者下一判断是此边界内交互是否值得进一步机制研究，问题关闭仍 Unknown。

已获授权的后续终点描述固定36对＝9种子×2个B规则×A200/A800，各用全部800条 frequency dev，无 test 或效果选择。[冻结选择](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/frequency_endpoint_selection_frozen.json)、[输入配置](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/frequency_endpoint_selection.json)、[独立模块](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/source/analyze_frequency_endpoints.py)、[CPU接口/代数11项通过](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/frequency_endpoint_interface_check.json)。72个终点ID均已登记；匹配 raw-o_proj 的实际1B SAE仍待完成，SAE分析 NOT_RUN。描述真实 ΔW=Wdiff−Wsame、SAE绝对终点编码差及显式残差、same终点损失梯度加权、真实有限 CE 差与余项、20答案池的概率质量和条件 CE。这不是 Adam 全训练路径分解，也不是特征因果证据。[SAE分析owner](../../17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/sae_analysis_cn.md)。SAE占用4GPU训练时没有额外分析 job。


## 附录：匹配 SAE 的真实频率终点描述已完成（北京时间2026-10-10）

本附录回答：在已经观察到的频率策略终点差中，匹配 raw projection 的 SAE 是否给出足够完整的损失变化说明。原频率训练、确认 test、主统计量和统计分支原样保留。固定9种子×2个B规则×A200/A800，共36个异规则减同规则终点对，每对读取全部800条 frequency dev。原确认 test 的交互中位0.0661424387仍是主结果；以下只描述 dev，没有新的显著性检验。

实际使用 `sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z`：Qwen第27层`self_attn.o_proj`原始输出、残差相加前，30000特征/TopK32，244380步、1000002960个valid prediction token。最终权重SHA为1e16759da1ef1bad953d3df1bcf641c01b81edc87ca6b56d61b32251f41ebe64。它是实际完成并合格的1B SAE，分析中保持冻结。

同一条 dev 输入上，h0是同规则训练终点的投影输出，h1是异规则训练终点的输出。SAE分别对两个绝对输出编码一次，得到z0/z1及各自重构残差u0/u1。真实输出差由解码变化D(z1−z0)、显式残差变化u1−u0及实测数值误差共同记账。损失梯度在同规则终点计算，保留真实有限CE差、梯度加权的解码/残差项及有限步余项。再把A800的终点账减去A200的账，描述dev交互。两个A条件的参考终点不同；这不是整个交互的单点线性化，也不是Adam训练路径的分解。

下表均为9种子、两个B规则的算术均值，单位nat/答案。分别汇报顺序未见、组合未见及等权合并。每对终点都保存了两个规则的读数；交互只取该对的B规则。三个带符号的分项在记录的算术误差内相加为真实有限交互。

| dev未见类型 | 真实有限交互 | SAE解码线性项 | 显式残差线性项 | 有限步余项 |
|---|---:|---:|---:|---:|
| 顺序未见 |0.114125|0.004599|0.051953|0.057573|
| 组合未见 |0.051010|−0.000716|−0.006226|0.057952|
| 等权合并 |0.082567|0.001942|0.022863|0.057762|

9个种子的合并dev交互范围0.0723689–0.0973117，中位0.0823579。分别计算的分项中位数不保证相加。20个固定候选答案池内的条件CE差均值为0.081613，答案池log概率质量差为−0.000954；二者给出全词表CE差0.082567。这个算术关系本身不能建立模型内部的任务机制。

SAE在B规则列表表征上的重构并不充分：36对终点的原始能量归一化重构MSE中位，同规则端为0.548377，异规则端为0.537822。这是列表任务测量，不能替换成DCLM训练验证指标。残差变化范数/真实变化范数中位1.48649，范围1.37617–1.61853；带符号抵消允许该比值超过1，不能把它读作“未解释百分比”。在当前冻结字典和读数下，SAE解码线性项没有覆盖主要有限损失变化，显式残差和有限步余项不可省略。完整机制解释、共同/差异功能划分、特征因果作用和专家收益仍未建立；也不能反推不存在相关特征。

执行与资格：fresh75 strict、72真实矩阵加载/800条tokenizer与oracle/40条CPU native、实际1B CPU4检查均通过。旧22文件GPU未运行的冻结保持字节不变。root核验旧主分析job为FAILED后释放4卡slot，再追加不可变launch extension。sole template于2026-10-10 09:27:19UTC提交`pt-h6ke4emg`，资源仍为`h100-4-reserved`和`shphd-lite-0911`。首先4对×800的reader资格211/211通过，随后全部36对×800的audit1683/1683通过，最终独立复核1685项通过。native尾部CE最大误差0.0000185966；投影变化恒等式相对误差最大3.10245e−6；SAE记账恒等式相对误差最大6.79216e−7。冻结上游输出、恢复Base完整字节和字典字节均通过。受管payload181.43秒、exit0，无训练更新/token。平台于09:31:23UTC／北京时间17:31:23达到SUCCEEDED。91个实际manifest文件和22个冻结文件全部独立SHA核验通过。首轮本地CPU命令未加载既有runtime.sh，import失败且未创建payload；补上既有runtime后通过，科学输入不变。没有GPU重跑。

证据：[完整运行目录](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z)、[9种子dev账及全部分项](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/description/descriptive_aggregate.json)、[派生事实及独立面板](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/endpoint_result_facts.json)、[工程终态](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/terminal_verification.json)、[平台终态观测](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/supervision/terminal_observation.json)、[91文件manifest](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/artifact_manifest.json)、[独立hash核验](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/independent_postflight_20261010T0933Z.json)、[实际产物登记request](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/registration_request_current_execution.json)。实际payload包括36组JSON/NPZ，保存同一次编码的稀疏绝对z0/z1（包括在delta-z中抵消的坐标）、dense解码/残差/真实变化及梯度加权数组，没有重新编码替代。待root中央登记资产为`analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`；本次追加时仅剩root独占catalog登记receipt未生成。研究者机制判断及下一科学决策仍为Unknown。

登记已完成：root实际登记`analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`，含manifest的92个实际文件SHA通过、strict选定资产通过。[登记receipt](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/endpoint_description/runs/actual1b_36pairs_20261009T2118Z/registration_request_current_execution_registered_outputs.json)、[fresh strict snapshot](/data/250010109/Research_System/assets/checks/2026-10-10_a17_outputs_20261010T093323Z.json)补齐前述待登记步骤。原频率策略科学统计和判定不变。
