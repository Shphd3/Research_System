# 原始投影 SAE 分析子阶段

当前执行状态：全部已授权SAE子阶段工程完成并登记。Qwen九状态及S7列表共760矩阵/9,120干预，S7自然文本64条件通过GPU测量加CPU均值验收修复；S7复用已有SAE。详见[当前Summary](summary_cn.md)、[完整Detailed](detailed_cn.md)和[完成核验](/data/250010109/MoE_Router/experiments/20261010_a17_pipeline/completion_audit_20261010T1048Z.json)。科学机制判断仍Unknown，总体分析待研究者讨论。

以下保留准备及分阶段执行历史；其中STARTING、NOT_RUN、pending只表示相应记录写成时的状态，不能代替上面的当前状态。

本记录从属于唯一 [E03 Protocol](protocol_cn.md)。匹配raw SAE完整1B已实际完成，工程资格及中央登记通过。旧分析 `pt-azc2zkl5` 已FAILED，并非仍在运行：八个Qwen状态和S7列表有完整分支产物，Qwen seed71/update100未完成，S7原生DCLM梯度核验失败。工程修订A05保留旧失败。恢复任务 `pt-czzk7rb3` 于北京时间2026-10-10 17:45:52实际提交，最近17:47:05平台核验为STARTING；GPU修复、终态资格及机制判断尚未完成，科学判断仍Unknown。

分析对象是最后 Attention 投影输入 `a`、原始输出 `h`、实际可表示的矩阵扰动 `delta_W`、绝对端点SAE编码及原生答案损失。Qwen采用新训的匹配原始输出SAE；旧归一化MLP输入SAE不兼容。S7采用其原生嵌入式原始Attention输出SAE。两者的encoder、bias、字典归一化、checkpoint与学习历史分别保留。

## 目的、假设与边界

分析检查：只由discovery冻结的decoder子空间能否描述固定heldout内容组上的局部帮助或干扰，移除/改向该空间后原生有限作用是否区别于同rank PCA和随机空间。出现净伤害不是入场门槛；不强迫产生common-feature赢家，也不从局部作用跳到Expert必要性。强对手解释是模型主要提高答案词表质量或适应答案格式，并没有复用按位置选项的计算。因此保留完整词表CE/准确率、20答案词内条件CE、答案池概率这三层读数。

## 冻结输入与选择

使用直接矩阵L的29/43/71三seed，全部0/16/100状态，eta=.001/.01和全步/半步。已登记的checkpoint家族保存真实可训练矩阵，必须配精确Base。原生运行时恢复资格由本分析实际补证，不倒改旧实验状态。

每state保留全dev800原生基线。结构discovery及有限干预采用固定120条discovery、120条heldout。无序内容组按hash分侧；各侧每种nominal novelty固定20组，保留组内全部双规则/顺序记录。这是开发数据复用，不能叫blind confirmation。nominal面板不改，各state另按真实训练ledger记录实际见过的row/group。state0没有在本轮训练中见过组；virtual sources不计入训练曝光。

`data_a17_raw_sae_list_analysis_selection_v2` SHA256为 `c6db6d645d5b260e7bfcd65a46c5236d5ab763c7f5bf435d065e93b72de23d6e`。新source排除全部dev内容组及旧三seed pooled discovery来源组。FIRST/LAST各五批、每批20答案各1条；十批共74组，批间组互斥，source与recipient联合discovery/heldout交集为0。每批20条来自7或8组，批内有依赖；固定virtual批不能当科学重复，两规则来源未配对。每规则前两批发现候选，后三批评估候选。

原Full保存的全部矩阵另列为batchID敏感性读取，其原批次独立抽样不保证记录/组独立。分析审计三seed/两规则pooled overlap；原probe FP32 before与全800原生值逐record核对，before/after/delta与固定240结构记录逐record核对。报告实际误差，不声称旧更新运算被精确重建。已注册v1保持原字节，作为历史；v2在模型分析提交前修复11个source/recipient跨fold组交叉，recipient不变、没有按模型效果选择。

## 计算与有限控制

逐state直接重算原生来源梯度 `G`，保存parent/state/记录/组身份，并核验其等于末层有效位置外积的均值。真实梯度方向内积/余弦是次级几何读数；不把舍入后的 `delta_W/eta` 叫G。

原生完整前向资格核验尾重放。每个请求扰动先转成稳定的FP32实际差值 `(W_new-W_before)`，保存请求/实际误差。原始投影关系是 `delta_h = a @ delta_W.T`。先编码两个绝对端点，再取 `delta_z = E(h1)-E(h0)`；保留 `D delta_z`、两个端点重构残余、残余差 `delta_u`、数值恒等误差、有符号atom贡献、损失加权遗漏及有限Taylor余项。特别检查任务小分量是否被总解码/数值误差吞没。

候选分数只读取discovery来源和recipient：对recipient规则/novelty格，以及source规则/批/eta/全半步等权平均 `abs(delta_z_k * (D_k dot g_h)) / ||delta_W||_F`。取64个atom，再取decoder SVD rank32；数值rank不足时报实际rank。读取heldout有限作用前写盘冻结坐标。PCA及随机seed1729/1730/1731严格同rank。heldout作用不选择feature、rank、阈值或方向。

每个heldout来源矩阵都评估 `P delta_W`、`(I-P) delta_W` 的原幅度，以及恢复完整矩阵Frobenius范数后的改向；保存实际矩阵范数和 `delta_h` 范数。实际FP32写入后的矩阵还可能有舍入引起的子空间泄漏；追加实际投影违约范数、basis正交误差、请求/实际端点位移误差与其损失线性贡献，避免将有效矩阵作用直接称为纯子空间机制。原完整矩阵、显式零扰动保留。每variant在固定heldout四格各5条、共20条上做原生回放资格；资格记录按hash选择，不按作用选择。原生no-op重复以及W/CE/表征恢复必须确切。20条是实际资格范围，不冒充全部recipient完整原生重放。

保存actual replay/zero漂移及其相对有限作用的误差。有限符号只有超过实际资格误差10倍才称分辨；SAE线性方向解释还需超过分解误差与Taylor余项。端点CE绝对资格上界2e-5、有限差值4e-5并不自动分辨小于该量级的分量。同规则heldout来源下降资格对全部source报告，不删除不利或未分辨的来源。

## S7及频率边界

S7保留同列表dev800原生基线、同120/120观察面板及载体内SAE/有限干预。初始没有学会列表规则或来源无效，只能限制该局部任务的机制解释，不能据此支持共享/差异功能分解。原生DCLM分支对全部固定validation窗口逐一保留零扰动、CE/表征恢复确切、实际有限差值误差与分辨尺度；范围是各窗口全部256个位置。另用S7已学的原生DCLM资格面板：4个训练窗口共1024预测位置，4个validation窗口分成512 discovery、512 heldout recipient位置。已登记选择记录文件/offset/257-token内容hash，8窗口无完全重复，未核验语义近重复。S7不新增训练，natural DCLM与Qwen列表绩效不合并。

频率阶段owner独立实现已授权终点描述：9seed、两B方向、A200/A800，共36个diff-vs-same成对contrast。复用匹配raw SAE，保存真实两个终点W/绝对编码，以same终点梯度为reference，保留原生loss差、损失加权残余/余项及答案池/条件CE。A200/A800两条interaction腿都报告；这些终点差异不能解释整条Adam路径或证明因果分工。

## 当前实现与证据

执行目录 `/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae`。`carriers.py`适配Qwen和已资格S7的原生尾；`analysis_core.py`保存有符号端点代数及同rank空间；`analyze_list.py`执行列表有限作用/干预；`analyze_s7_native.py`执行原生DCLM工具资格。提交前冻结源码/配置/唯一Protocol只读副本及当前输入访问检查。`freeze_analysis.py`要求最终SAE已实际登记、244380步/1,000,002,960 valid/PASS，并验证实际路径SHA；没有把计划末点或Smoke当分析输入。`run_bounded_analysis.sh`将三Qwen seed各分配一GPU，第四GPU依次做S7列表与native DCLM，整轮仍仅四H100。输出登记请求使用representation/ARRAY_FILES_PRESENT，绑定实际文件清单SHA、payload manifest、inputs/hook/state/selection/source；不改中央catalog。

CPU实际收集并通过19个代数/native-interface/FP32舍入、实际manifest导出及监督资格测试；Python及shell语法检查通过。v2样本平衡、内容组隔离、v1字节保持已实际核验。GPU恢复、原生有限回放、新raw SAE重构、候选空间作用、频率终点结果均 **NOT RUN**。准备代码及CPU资格不能当科学支持。

Qwen SAE训练按E16使用BF16 Base/训练autocast，参数保存FP32；本主分析延续学习实验的FP32科学reader，SAE绝对编码也用FP32。parent weights及raw接口匹配不意味着这两个数值路径位等同。每state实测绝对端点重构误差、损失加权残余和有限reader误差，不预设字典足以描述任务小分量。S7保留其原生FP32载体与嵌入字典。

比较的信息边界：SAE候选使用discovery目标梯度与编码位移筛选，PCA只使用h方差，random不使用相同目标信息。相对这两控制的优势不能分离字典本身与任务相关筛选的贡献。有限干预结论只针对本轮冻结候选空间。**AI建议，供明日研究者选择**：用同样discovery目标信息选择一个非SAE空间，作为后续检验；本轮不新增该实验，也不改已冻结候选、控制或主指标。

提交前的身份绑定补齐：实际消费的config路径及SHA、analysis run root、input-access路径及SHA必须与同一个freeze manifest匹配。另配置即使字节相同也拒绝。CPU资格覆盖5个路径/字节绑定案例。绝对端点证据新增同一次编码的稀疏z0/z1（含在delta_z中抵消的活跃feature），以及D delta_z、delta_u、真实delta_h、两端残余、恒等误差和线性项数组；Qwen/S7实际流程均调用导出，文件统一纳入实际payload SHA清单。新增保存不重编码、不改候选/控制/科学主指标。19项CPU测试在19:12 UTC全通过；GPU分析仍NOT RUN。

三条轨迹的state0都来自同一个精确Base。新strict sources/recipient选择也相同，因此这三份state0不当独立模型重复；仍保留全部记录与各seed旧来源敏感性。有限干预终点核验追加完整条件tuple唯一覆盖及payload manifest/实际文件集合覆盖，不仅核数量。4项针对截断日志、重复条件与缺文件的CPU检查通过；真实GPU末点资格仍待执行。


## 实际分析提交

run：`/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/analysis_20261009T210339Z`。12个实际input IDs fresh strict PASS，包含登记后的 `sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z`。freeze SHA `3d02a3276e7b6ae3a097c99bc1146b879b015ec7b43942fbc1c971754c7912b5`，actual config SHA `16a6562b23c92d3f1a8f5a555bed7523c880d73510894b6360f9e0ac719b1c50`；实际config/run/input-proof绑定复核PASS后经root模板提交。原训练及本轮科学合同未改。

同一四H100reserved节点，GPU0/1/2各处理一个L seed的全部0/16/100，GPU3先S7 list再native DCLM。完整规模保留：每Qwen state80矩阵设置/960干预，S7 list40/480，native DCLM64元组。墙钟上限5400秒仅管理执行，不缩案例/门槛；频率owner等待本分析终态及root登记后再使用同一资源。实测4张H10080GB、各81559MiB，carrier日志及writer locks已建立。首state耗时将用于校准ETA；此处不预报科学结论。

Qwen与S7的母模型架构、预训练历程和SAE训练历程均不同。raw hook类型、TopK/字典规模的兼容只支持各自接口的分析，不构成受控模型优劣比较，也不逐坐标对齐不同字典的feature。S7 native DCLM与Qwen list不合并成同任务结论。


## 原生reader恢复提交：2026-10-10

本次恢复只读，不新增模型或SAE训练。使用同一已授权单节点4H100 reserved：Qwen seed71/update100逐字节复用旧发现阶段冻结candidate及80矩阵，对全部960干预的固定120条留出样本新增完整模型原生before/after/restore，并重新核验S7原生梯度及64条件。旧tail门槛2e-5/4e-5与超限失败保留；其他八个Qwen状态保留归档reader，跨reader差异不能被合并为统一三seed比较。

执行run：`/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/native_recovery_20261010T094522Z`。freeze SHA82d37b8e0a3adb9750857552f4a9112ea237a5250e52bd97f1c050be8661fac9。实际19项CPU与独立源码审核通过，并绑定实际source字节。已登记旧partial资产 `representation_a17_raw_sae_analysis_20261009t210339z_qwen_l_s71_u00100_partial_recovery` 保存80矩阵及104/960干预，旧工程FAIL不因访问通过而改成完整结果。尚待GPU原生资格、80/960完整覆盖、S7全部64条件、实际输出登记与事实综合；上文准备阶段的NOT RUN只说明当时状态，不代表当前任务未提交。
