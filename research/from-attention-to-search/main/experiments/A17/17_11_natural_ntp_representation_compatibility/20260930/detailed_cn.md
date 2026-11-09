# 完整证据记录：自然 NTP 表征预测局部更新相容性

[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_11_natural_ntp_representation_compatibility/17_11_natural_ntp_representation_compatibility_anchor_cn.md) · [冻结 Protocol](protocol_cn.md) · [中文摘要](summary_cn.md) · [English detailed](detailed.md) · [执行记录](natural_ntp_execution_record_cn.md)

**状态：**Full 工程完成；主结果合格且 `NON_SUPPORT`；确认有限步 `NOT_RUN_BY_BRIDGE`；14 个结构读出 `NOT_RUN_BY_GATE`；研究者科学判断 `Unknown`。下文 **R** 指 `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result`，ACP 任务为 `pt-dgpld36j`。原始文件都留在 R；本仓库只存阅读和证据路径。

## 0. 直接结果

固定 S7 检查点后，以自然文档的真实下一词损失测量矩阵梯度内积 \(K\)，让仅接收更新前矩阵输入表征的读出器预测它。DEV 在开封前选中完整表征读出器。确认集 1,024 个不共享文档端点的数据对上，相对训练集均值常数的 MSE 改善 \(Q=-0.000138\)，配对 bootstrap 95% 区间 \([-0.002768,0.002294]\)。预注册规则为区间上界低于 0.05 即 `NON_SUPPORT`；本次符合。这个结论只否定当前操作化的 5% 门槛，不是“表征绝无信息”的定理。

有限步 DEV 校准中，所有候选步长都未满足至少 80% 一阶作用高于测量分辨率的要求；没有运行确认集实际损失后果。结构比较以前述主结果获支持为门槛，故 14 个读出均未运行。两项跳过各有原因，不能当作额外负结果。

## 1. 对象、计算和能回答的问题

每个事件是文档开头 256 个词元和第 257 个真实目标。在前缀最后位置，\(c\in\mathbb R^{2048}\) 进入末块注意力输出矩阵 \(W\in\mathbb R^{1024\times2048}\)，\(a=Wc\)；\(e=\partial\ell/\partial a\) 是全词表纯 NTP 交叉熵的下游导数。单事件矩阵梯度 \(G=ec^\top\)，两事件相容性标签 \(K_{ij}=(c_i^\top c_j)(e_i^\top e_j)\)。这是精确恒等式。\(K\) 的符号仅给出标量 SGD 下的一阶交叉更新倾向；实际有限步损失 \(I\) 需另测。

预测时读出器只能看 \(c_i,c_j\)，不能看目标、\(e\)、真实 \(K\) 或更新后量。因而主 \(Q\) 只检验这些读出器能否在未见文档提取统计预测信息。恒等式成立、主结果、有限步、长期共享／分开训练收益分别是不同层面的命题。

## 2. 资格、执行偏差和尝试

2026-09-29 研究者明确批准按 [Protocol v1](protocol_cn.md) 实现和执行 Smoke，通过后提交 Full。冻结中文 Protocol 的 SHA256 是 `67406eb9f69359f0c78510caa3915cd9829a4d85be3d61e0c88d453e31fce521`；Anchor 为 `7fa24bb31b0f3058c0696d9684558099e0873bfbd316f1ae541a3b5f77c60614`。注册文件内的两项哈希仍与当前文件相同；数据、选择、训练统计、有限步校准及执行脚本哈希也全部核对相符。没有在开封后改样本、模型选择或门槛。

| 已注册项 | 实际 | 资格影响与证据 |
| --- | --- | --- |
| 模型和损失 | S7 \(\lambda_{rec}=0.1\)，恰为 33B **训练词元**的状态；state SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`；纯 NTP，全词表 CE，末块注意力 \(W\)；主干优化器更新数 0 | 一致；`R/environment.json`、`R/collection/scope_registry.json`、`R/verification.json` |
| 数据与划分 | 来源 59,812 行，合格 47,760，候选 20,000，去重组 19,997；OPS/TRAIN/DEV/CONFIRM 事件 64/4,096/1,024/2,048 | 数量一致；历史所有窗口是否曝光无法完整确认，外推边界收窄 |
| 数据对 | OPS 32、TRAIN 32,768、DEV 512、CONFIRM 1,024；独立核验确认集 2,048 个端点互异，冻结预测和真值 pair 索引一致 | 符合主分析单位；同站点／语义依赖仍可能存在 |
| 预测器训练 | 2 家族 × 2 学习率 × 2 weight decay × 3 种子 = 24 次拟合，全部 50 epoch，每次 3,200 更新，batch 为 512 对；24 收据 PASS | 一致；仅离线预测器训练，主干／SAE未训练 |
| DEV 选择 | 几何：epoch 24，学习率 0.001、decay 0.0001、MSE 0.909142；完整表征：epoch 1、学习率 0.0003、decay 0.0001、MSE 0.908408；后者被选主读出器 | 开封前固定，无确认集调参 |
| 确认封存 | 注册 SHA256 `c9f2265dc5575adfd8b1d5e3ecb38402dc60bfafc852e000ce5d39cf45b46d91`；预测 SHA256 `751f7f19965a5a92b973400fc45d960f7470968ac0f034fc9633aee0f32064cd`；代码和日志顺序为先封存预测再分析确认真值 | 主比较合格 |
| 工程／数值 | 第二次 Smoke 通过；梯度因子误差 0、非末位置比例 0、\(Wc-a\) 误差 0、最大尾部 CE 差 \(2.53\times10^{-6}\)；临时更新复原和拟合恢复通过。Full OPS：\(\delta_L=6.69\times10^{-6}\)、\(\delta_K=1.82\times10^{-6}\) | 实质护栏有收据；Protocol 所列单独 `preflight.json` 未生成，是文件 schema 偏差，未缺失决定性护栏数据 |
| Full 资源与完成 | 4× H100 80GB，`shphd-lite-0911`，210.54 秒，4,699,652,035 字节；平台 SUCCEEDED、持久 pod log 和 `verification.json` 均完成；源检查点不变 | 时间／存储合格，无 Full `failure.json` |

首次 Smoke `pt-5k6mv35t` 在测量 worker 通过后，因预测器恢复时把 CPU 随机数状态装到 CUDA 而失败；没有开放确认真值。修复后第二次 Smoke `pt-1lqply7o` 用 50.57 秒完成，预测器下一步重放相对误差为 0；之后才提交 Full。首次 Smoke 是工程失败，不参与科研样本；Full 没有重启或剔除结果对。`preflight.json` 名称缺失已在上表标出。由于门槛，Protocol 中确认有限步 CSV/NPZ、结构次级 CSV 和相关图均没有生成；这是有记录的 `NOT RUN`，并非遗漏测量结果。主图是事后阅读副本，不参与选择或检验。

## 3. 实际训练和数据边界

原始数据来自 DCLM 留出分片 `global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst`，来源 SHA256 `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`，tokenizer SHA256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`。资格、去重、划分及配对在测结果前按种子 20260930 固定。每个文档只用开头一个事件；这不是所有自然文本位置的随机样本。[曝光账本](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/data_v1/exposure_ledger.json)注明该来源曾用于早期只读审计，无法完整建立与历史所有事件窗口的不相交性。

TRAIN 真 \(K\) 是监督标签：训练均值 0.00644025、总体标准差 0.8470065；拟合时标准化，开发和确认指标还原到原始 \(K\)。B1 使用四项两事件几何量；B2 使用两个 2048 维标准化 \(c\)、共享编码器和交换对称配对头。AdamW 的学习率为 {0.001,0.0003}、decay 为 {0,0.0001}、种子为 {17,29,43}，betas (0.9,0.999)、eps \(10^{-8}\)、全局裁剪 1，无学习率调度。每配置／种子确实跑完 50 epoch；B2 选中 epoch 1 是 DEV 事后从已保存 epoch 中挑选，并非提前停止训练。三个种子的预测取平均。入选 B2 在其 epoch 的标准化 TRAIN MSE 约 0.982–0.987，初始约 1.001–1.007；B1 入选约 0.9996–0.9998，初始约 1.023–1.145，均达到预定的拟合改善检查。后续 epoch 的 TRAIN MSE 更小，但 DEV 没有选它们。主干及 SAE 参数未更新，未做 LM 任务训练。

执行根 [源码与数据](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility)；[Full 来源清单](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/source_manifest.json)与[注册文件](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/frozen/registration.json)可核代码身份。四个 H100 worker 各自测量／拟合，彼此没有梯度平均。运行环境 Torch `2.3.0a0+6ddf5cf85e.nv24.04`、CUDA 12.4。

## 4. 主判据和证据链

以 TRAIN 均值常数 \(m\) 为固定参照，原始 \(K\) 上 \(Q=1-\sum(K-q_*)^2/\sum(K-m)^2\)。确认集按 1,024 个不共享端点的文档对等权；PCG64 种子 20260931，2,000 次每次有放回抽 1,024 对，用线性分位数给双侧 95% 区间。bootstrap 不重训。区间下界 >0.05 才支持，上界 <0.05 为不支持，其余为不足。基线 MSE 0.638792、真实 \(K\) 方差 0.638767，远高于 \(100\delta_K^2\approx3.31\times10^{-10}\) 的分辨率门槛；全部标签有限且未截尾。

| 判断 | 原始文件→计算 | 观测 | 资格与结论 | 边界 |
| --- | --- | --- | --- | --- |
| 主 5% 预测 | `R/collection/sealed/truth_confirm.npz` + `R/frozen/confirmation_predictions.npz` + `R/fits/train_stats.npz` → `R/analysis/primary.json`；另行独立重算 Q、随机抽样区间 | B2 \(Q=-0.00013819096\)，95% 区间 \([-0.00276836487,0.00229365299]\) | 合格，`NON_SUPPORT` | 固定读出器和语料条件区间 |
| 简单几何读出 | 同真值、预测及 bootstrap 索引 | B1 \(Q=-0.00128504158\)，区间 \([-0.00376803268,0.00116466200]\)；B2 比 B1 的归一化 MSE 增益 0.00114685 | 次级描述 | 不能称纯信息损失差异 |
| 注册的秩相关 | 同一封存真值／预测 → `R/analysis/secondary.csv` / `secondary.json`；同 2,000 次配对抽样，每次重新排秩 | B2 Spearman \(\rho_s=-0.004266\)，区间 \([-0.06710,0.05653]\)；B1 \(-0.007232\)，区间 \([-0.07159,0.05172]\) | 开封后补齐的预定描述性读数，未重选模型 | 多项描述区间未作多重校正 |
| 标签变化 | 确认真 \(K\) NPZ → 计数和方差 | 正 508/1024，负 516/1024；范围 \([-5.4919,8.2636]\)；方差 0.638767 | 合格描述 | 符号不代表稳定自然冲突群 |
| 梯度余弦 \(\kappa\) | 确认真值 NPZ 的 pair \(K\) 与事件梯度范数 → `secondary.csv` / `secondary.json` | 均值 0.0010118，区间 \([-0.0000372,0.0020812]\)；中位 −0.0001183，区间 \([-0.0007992,0.0006415]\)；无零范数对 | 开封后补齐的预定描述 | 接近零不能诊断预测失败原因 |
| 有限步损失桥 | `R/finite/dev_finite.jsonl` + 测量分辨率 → `step_selection.json`，独立核对 512 行 | 最大 alpha \(10^{-4}\)：余项、源降损、更新幅度护栏通过；作用分辨率仅 62.5%／50% | `FINITE_BRIDGE_UNQUALIFIED`；确认 \(Q_I\) 未运行 | 没有合格的确认有限损失预测估计 |
| 结构读出 | 主结果 → `R/structure/condition_ledger.json` | 14/14 `NOT_RUN_BY_GATE` | 无结构比较结果 | PCA／随机／full-a／SAE-a 均不能比较 |

独立只读核查重算了注册、预测、真值三个 SHA256，核对注册中的全部源码哈希；pair 索引一致且确认 2,048 个端点互异。用相同的 2,000 次 PCG64 抽样重算两种读出器的 Q 与区间，与 `primary.json` 数值一致。冻结预测 NPZ 只有 pair 索引、常数、几何和完整预测；未在确认集重选模型。

Protocol §11 还列出秩相关和梯度余弦，但原 Full 分析没有输出 `secondary.csv`。主分析完成**之后**，用只读 [compute_secondary.py](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/compute_secondary.py) 从已经封存的预测和已开放的真值补齐 `R/analysis/secondary.csv` 与 `secondary.json`，复用注册抽样种子／索引，并重新核对注册、预测、真值哈希。这是预定量的描述性补录，不改权重、DEV 选择、Q、区间或主裁决；零梯度余弦本应未定义，本次为零对。

## 5. 主结果与图

常数确认 MSE 为 0.6387922755，B1 为 0.6396131501，B2 为 0.6388805508。B2 预测值标准差 0.01578，而真实确认 \(K\) 的标准差 0.79923；B1 预测标准差 0.01410。读出器在这批数据上大多给接近均值的预测。这不能辨别是表征本身信息弱，还是读出器、训练对数、优化或目标噪声限制了提取。DEV 上 B1、B2 相对 DEV 常数的 Q 分别仅 +0.000704 与 +0.001510；小优势在 CONFIRM 未保持。

![确认集真实与预测 K，以及条件性 Q 区间](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/primary_q_and_prediction.png)

左图横轴是真 \(K\)，纵轴是封存预测；虚线为 TRAIN 均值。右图是无量纲 Q 的配对 bootstrap 95% 区间，竖线分别表示常数 Q=0 与注册门槛 0.05。点和区间靠近零；决定结论的是冻结的 Q 判据和区间，散点仅辅助阅读。[图源、脚本与哈希](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/SOURCES.md)。

## 6. 有限步校准、停止位置和失败类型

OPS 测得 \(\delta_L=6.6912473\times10^{-6}\) nat/目标、\(\delta_K=1.8191311\times10^{-6}\)；\(\|W\|_F=55.8860\)，OPS 梯度范数中位 6.54944。四个 alpha 各在 32 个 DEV 对上做两个方向、全步／半步，从同一 \(W_0\) 出发并恢复。每个步长均须 ≥90% 余项在容差内、≥90% 来源自损失下降超过 \(5\delta_L\)、≥80% 的 \(|\eta K|>20\delta_L\)，且全部相对更新 ≤\(10^{-3}\)。

| alpha | 全步可分辨 | 半步可分辨 | 两步余项 | 两步来源改善 | 更新幅度 | 判断 |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| \(10^{-4}\) | 62.5% | 50.0% | 100% | 93.75% | 100% | 分辨率失败 |
| \(3\times10^{-5}\) | 43.75% | 9.375% | 100% | 92.1875% | 100% | 分辨率失败 |
| \(10^{-5}\) | 3.125% | 3.125% | 100% | 90.625% | 100% | 分辨率失败 |
| \(3\times10^{-6}\) | 0% | 0% | 100% | 90.625%／89.0625% | 100% | 分辨率及半步来源失败 |

最大候选的全步 \(\eta=0.000853295\)，半步 \(0.000426647\)。在 DEV 这些行里，余项在预设容差内并不能救回作用分辨率不足；按冻结规则不得再扩搜索或开封确认有限步。这个失败仅限制从 \(K\) 推及实际 \(I\) 的证据，不推翻主 \(K\) 结果，也不能算“有限损失预测不支持”。

S0 溯源、S1 通过的 Smoke、S2 采集与预测器训练/DEV 选择、S3 冻结及主确认分析、S6 工程审计均完成；S4 在 DEV 有限步桥停止；S5 在主结果门槛停止。首次 Smoke 的 RNG 问题已在合格 Smoke 前修复，是实现故障，不是科研观测。平台 `SUCCEEDED` 只与持久日志、收据和独立计算一起使用。

## 7. Reasoning audit 与结论边界

恒等式 \(K=(c_i^\top c_j)(e_i^\top e_j)\) 说明输入几何与下游误差信号**共同**决定相容性；它不保证依赖真实目标的 \(e_i^\top e_j\) 能从 \(c_i,c_j\) 预测。本次合格主检验否定的是“这两个注册读出器在指定总体上达到 5% 门槛”，没有把“条件信息弱”与“函数族／样本／优化能力有限”拆开。晚期训练集拟合更好而 DEV 没选它，符合泛化能力受限的可能性，却不是原因鉴别。DEV 的小正 Q 也不是第二次独立确认。

仍然存活的竞争解释是：更恰当的读出器、更多独立监督对或不同条件变量可以提取本次读出器没提取到的信息。若研究者认为值得继续，必须另立前瞻合同和未见确认数据；本次 CONFIRM 已开封，不能用来调参后再称确认。确认 \(K\) 正负近半只表明局部一阶标签有变化，不等于稳定自然冲突群或净损失伤害。DEV 余项护栏通过也不能替代未运行的确认实际损失。结构面板未跑，无法下 PCA、随机空间、SAE 或 full-a 的结论；没有做表示因果干预，也没有比较共享／分开训练。

**最大可支持结论：**一个 2.81 亿参数 S7 主干的固定 33B 训练词元检查点、指定矩阵与 DCLM 文档开头总体中，注册读出器未达到相对常数 5% 的留出 \(K\) 预测改善；条件区间上界为 0.002294。研究者对其科学意义、Focus 转移及下一优先事项仍为 `Unknown`。关于能力与信息来源的讨论是 **AI 建议**，不是新实验授权。

## 8. 本轮六项记录与产物索引

**2026-09-29 本轮：**①问题与假设：自然 NTP 的矩阵输入表征能否前瞻预测连续梯度相容性，达到注册 5% 门槛。②设置／对照：固定 S7 \(\lambda_{rec}=0.1\) 和末块 \(W\)，B1/B2 对训练集均值常数；仅预测器输入／函数族改变。③训练数据：4,096 文档、32,768 对用于 24 个监督拟合，主干无更新。④测试数据：DEV 1,024 文档／512 对作选择和步长校准，CONFIRM 2,048 文档／1,024 互异端点对作封存主检验。⑤结果：主 `NON_SUPPORT`，\(Q=-0.000138\)，区间 \([-0.002768,0.002294]\)；有限步和结构分支按门槛未运行。⑥认识／边界／下一决定：当前读出器未呈现注册实用预测增益；原因未分辨；研究者尚未决定是否结束此操作化或注册新的区分测试。

| 产物 | 用途 |
| --- | --- |
| `R/verification.json`、`R/environment.json`、[Full pod log](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/pod/ntpcompat-full-0929-175901-20260929T175955Z.log) | 工程完成、实际设备、原检查点未改 |
| [数据清单](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/data_v1/data_manifest.json)、[曝光账本](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/data_v1/exposure_ledger.json) | 来源、计数、划分、曝光边界 |
| `R/collection` | 特征、真值、pair 及采集收据；确认真值 SHA256 `f11545dc2343e6db6dff7df7163e26ec2a5fc5df4baecd6bfea22ce9b4dc2409` |
| `R/fits` | 24 预测器拟合、统计量、DEV 选择和权重 |
| `R/finite` | 数值分辨率、512 条 DEV 临时更新、步长不合格收据 |
| `R/frozen` | 预开封注册、预测封存、哈希收据 |
| `R/analysis/primary.json`、`finite.json`、`secondary.csv`、`secondary.json` | 主 Q／区间、有限步未运行状态，以及开封后补齐的预定描述性读数 |
| `R/structure/condition_ledger.json` | 14 个结构读出的跳过原因 |
| [主图来源](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/SOURCES.md) | 事后绘制，只读图，不更改主分析 |

复核主 Q 只需从 R 的确认真值、封存预测、TRAIN 统计三个 NPZ 读取数组，按 Protocol §10 和 [analyze.py](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/scripts/analyze.py) 的 PCG64 种子/公式重算；无需重新提交任务。原始数据和检查点均保存在执行仓库，本日期目录仅有小型证据文本及图的阅读副本。
