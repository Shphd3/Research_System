from pathlib import Path
import json,csv,shutil
R=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z')
V=R/'visual_revision_20261014T025700Z'
D=Path('/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z')
H=D.parent

def link(label,path):return f'[{label}]({path})'
def tab(label,name):return link(label,D/'tables'/name)
def fig(label,name):return f'![{label}]({D}/figures/{name}.png)'
def put(name,s):
 (V/name).write_text(s.strip()+'\n');shutil.copy2(V/name,D/name)
old=(V/'before/detailed_cn.md').read_text()
# Reuse the complete original setup/history without changing any measurement.
setup=old.split('## 1. 目的与实际对象\n\n')[1].split('## 2.')[0]
graph=old.split('## 3. 既有图事实与完整集合\n\n')[1].split('## 4.')[0]
text=old.split('## 8. 文本与同位置幅度：完整交付\n\n')[1].split('## 9.')[0]
conformance=old.split('## 9. Protocol符合性、修正与成本\n\n')[1].split('## 10.')[0]
# Preserve historical claims as history, correct only the outdated publication sentence in current exposition.
conformance=conformance.replace('或commit/push。','。正式计算之后曾按用户明确请求单独提交并推送旧版portable ZIP；本次修订没有commit/push。')
terminology='''| 固定术语 | 对象、计算与单位 | 不能当作什么 |
|---|---|---|
| 统计图层级 h | 在完整约简统计图中，到无出边节点的最长出边路径；叶节点为 0；无量纲 | 模型层号、语义复杂度或因果先后 |
| 模型层号 | Qwen3 实际 block 的一基编号：2、4、…、28 | 图中节点的纵向位置 |
| 激活频率 | 某侧有效位置中该 Feature 命中的比例；图节点明确写“V 激活频率：×%” | 解码占比 p |
| 跨层解码幅度占比 p | 同一 Feature 的 14 层 decoder 向量 L2 范数分别除以其总和；图中单位 %，每 Feature 合计 100% | 激活概率、重构能量或功能贡献 |
| 幅度加权平均层号 L | 用 p 对实际模型层号求加权平均；单位为模型层号 | 整条 p 分布后移或前移的证明 |
'''
method='''固定最终 14 个选定模型层、16,384 个 Feature 的 CrossCoder，复用冻结 TRAIN 归一化和原推理规则产生的已有统计图与 decoder 几何。主集合是 D/V 支持均 ≥200、且 V 图非孤立的同一批 **15,537 个 Feature**。各统计图层级 h 的样本数依次为 **20、8,896、5,347、1,209、63、2**。每个 Feature 等权；图中四分位范围描述节点差异，不是置信区间。

三类图回答不同问题：图1看固定节点的统计关联；图2及图4—7看跨层解码幅度占比 p；图3看全部合格 Feature 的 h—L 关系。图8是频率解释边界。TRAIN 归一化坐标与恢复原始坐标使用同一批节点；恢复原始坐标是将各层范数乘回保存的 TRAIN 向量 RMS，再计算 p 和 L。

本次按用户要求重画已有结果，并从保存的 p **新增一次事后峰值比例描述**：逐 Feature 取 14 层最大 p，分为“第 2 层最大”“第 28 层最大”“其他层最大”。两种坐标均无精确并列最大值。类别只描述幅度峰值，不命名功能。没有重跑推理、训练、缓存扫描、关系计数或频率比较，也没有新 GPU 任务。
'''
phenomenon='''整体描述性 Spearman 在 TRAIN 归一化坐标为 **−0.277976**，恢复原始坐标为 **−0.157788**；方向保留，数值差异明显。TRAIN 归一化坐标下，h=1、2、3 的 L 中位数为 **19.902、15.007、14.305**，h=4 回升至 16.226；不是逐级严格单调。

完整 6×14 组平均 p 显示，TRAIN 归一化坐标下 h=1、2、3 的第 2 层平均 p 为 **15.39%、25.06%、30.20%**，第 28 层平均 p 为 **17.00%、13.95%、13.25%**。浅层和深层可以同时有幅度，不能把 L 的变化说成整条分布平移。两种坐标的完整热图使用相同 0–40% 色标。

事后峰值比例中，TRAIN 归一化坐标下 h=1、2、3 的“第 2 层最大”分别占 **34.95%、60.58%、74.19%**；恢复原始坐标下，这一类别均为 0，但第 2 层的 p 并非为 0。h=0 的 20 个节点在两种坐标下都以第 28 层为最大分量，完整轮廓仍不同。h=5 仅 937、3461 两点，其 TRAIN 归一化坐标 L 分别为 **22.118、14.899**。
'''
explanation=f'''为什么整体负相关，频率内却有 7 格为正？两者比较的对象与权重不同。整体相关包含不同 h 组之间的频率构成差异，使用全部 15,537 个节点的秩；频率格只比较固定频率组的共同范围内、某一对相邻 h 的 L 中位数。建边规则要求箭头指向至少常见两倍的节点，所以 h 与激活频率本来就耦合。不同频率构成可能与整体负向同时出现，但本轮没有识别它造成了多少差异。

必须看全部 **25 格**：11 格可比较，7 正、4 负；其余 10 格缺组、1 格无共同范围、3 格样本不足。可比较格的差值大小并不对称，例如 +0.170 与 −8.982 都各被算作“一格”。h=0↔1 和 h=4↔5 都没有合格格，不能用 11 格替代整体。五分位和范围交集也不保证组内频率分布相同。这不是“控制频率后的效应”。

{fig('全部25格频率共同范围内比较', 'figure8_frequency_all25')}

读图：横轴为相邻统计图层级 h 对，纵轴为预定的 5 个 D 激活频率组。颜色是高 h 减低 h 的 L 中位差，单位为模型层号；每格标低 h／高 h 的样本数。灰格保留原因，不表示差值为 0。缺组／无共同范围格另标交集前组内人数。{tab('完整频率源表','frequency_comparison_25cells_source.csv')}。

坐标尺度是另一条边界：恢复原始坐标后，整体负向仍在，但相关数值和峰值类别明显改变。这说明数值依赖层尺度；它没有删除 Feature，也不能被讲成功能差异。峰值类别相同也不代表完整 p 相同。

D 图参照的描述性 Spearman 为 **−0.279321**，D 频率检查也有 11 个合格格、7 正 4 负。D/V 来自同 bin，V 曾参与资格筛选和原始边复核，文档独立性未知；这些不是独立总体检验。节点也不独立，不报告 p 值或独立节点置信区间。h=5 只有两个节点，不能代表最高统计图层级的总体规律。
'''
conclusions=f'''### 认识一：统计图层级 h 不能直接承担模型深度的正向排序，需要另外测跨层分布

{fig('相同15537节点两种坐标的h—L对照','figure3_all_features')}

关键数据：两面板使用完全相同的 **15,537 个 Feature、横向抖动、坐标范围和绘图规则**，分别给出中位数、四分位范围、各组 n 与描述性 Spearman；h=5 单列两个点。相关分别为 −0.277976、−0.157788。{tab('逐点双坐标源表','figure3_coordinate_comparison_source.csv')}；{tab('中位数与四分位源表','depth_vs_layer_summary.csv')}。

推断的变化：保留 h 作为统计关联结构的描述，不再直接用“h 更高”代替“模型中更深”。**下一项研究决策（待研究者讨论）：选取学习对象时，是否要求明确所用坐标，并同时保留完整 p，而不是只按 h 排序？** 本报告不因此启动新的学习实验。

### 认识二：同级内部存在不同轮廓，后续应同时看具体节点、关联分支和跨层分布

{fig('同级内部峰值类别比例，事后描述','figure5_peak_composition_posthoc')}

关键数据：TRAIN 归一化坐标 h=1 有 3,109 个“第 2 层最大”、4,493 个“第 28 层最大”、1,294 个“其他层最大”，都在同一个 h 内。h=5 的 937 与 3461 也具有不同 p 轮廓。恢复原始坐标改变峰值排序，因此不把类别命名成功能。{tab('完整峰值比例与计数（事后描述）','peak_composition_posthoc.csv')}。

{fig('最高统计图层级的两个个体轮廓','figure7_h5_individual_curves')}

图7保留两个节点各自的 14 层 p 与 L；n=2，不作最高级总体推断。{tab('两个节点逐层源表','h5_curves_source.csv')}。全部 20 个 h=0 节点的逐个热图、固定 30 节点热图，以及原关联分支见 {link('完整图与读图说明',D/'figures_cn.md')}。

推断的变化：组平均和 L 能概括差异，但不能替代个体轮廓。不同 h 组含不同 Feature，本轮没有观察“同一个 Feature 随 h 增长而移动”。**下一项研究决策（待研究者讨论）：比较候选学习对象时，是否将具体节点、关联分支和 p 作为共同保留的信息，而不是仅使用层级或峰值类别？** 当前不能据此判断 common／unique、共享／分离学习或专家收益。
'''
summary=f'''# 结果摘要：统计图层级与跨层解码幅度分布（图表修订版）

**整体负相关不能把 h 解释为模型深度；同级内的完整 p 轮廓仍须保留。** 本版按用户要求修订图与叙述；新增峰值比例只作事后描述，原主结果和科学状态不变。

## 目的

回答固定问题：统计图层级较高的 Feature，其跨层解码幅度分布是否更偏深层？本轮帮助判断 h 能承担哪种描述，不评估共享／分离学习或专家分发收益。

## 方法

{method}

h 是统计图中的最长出边路径；p 是同一 Feature 各模型层 decoder 范数的占比；L 是 p 加权的模型层号。**L 变大只表示幅度加权平均层号 L 变大，不证明整条 p 分布向深层移动。** 激活频率是命中位置比例，与 p 是不同的量。

## 现象

{phenomenon}

完整均值图及逐节点图见 {link('图索引',D/'figures_cn.md')}；精确值见 {link('源表索引',D/'tables_cn.md')}。

## 解释

{explanation}

## 结论

{conclusions}

原文本 150 条随机＋90 条高激活记录原样保留；本次没有新增文本抽样。{link('完整报告及执行追溯',D/'detailed_cn.md')}；{link('全部文本',D/'text_examples_cn.md')}。此次完成图表与报告修订后停止，不 commit/push，不进入训练或新实验。
'''
put('summary_cn.md',summary)
# Detailed has only two main conclusions; complete audit and history live in appendices.
detailed=f'''# 完整报告：统计图层级与跨层解码幅度分布（图表修订版）

本报告是原运行 `20261014T020014Z` 的图表与解释修订，不是第二次正式实验。处理者：Codex，线程 `01a1343f-32aa-7500-9835-000956218089`。原任务 `pt-icv8hyi3`。**原全体趋势、频率比较、节点选择和文本均保持不变；新峰值类别统计标记为事后描述。**

Anchor：{link('研究者给定问题',H/'hierarchy_decoder_distribution_anchor_user_20261014_cn.md')}。冻结 Protocol：{link('原执行契约',D/'provenance/protocol_frozen.md')}，SHA256 `39530a9a36eee0403a8bc3ee53ad19d3e82a5dcb18c86fa7287c1ca4cc8894fb`。{link('简短报告',D/'summary_cn.md')}；{link('本次修订范围',D/'provenance/visual_revision_scope_cn.md')}。

执行结果可用于冻结定义下的描述性比较；不能升级为机制或效用证明。研究者的机制判断、科学状态转移与后续实验决策仍为 Unknown。本次修订没有改变 Focus、Anchor 或原冻结 Protocol。

## 目的

本轮要判断统计图层级 h 是否可以直接作为模型深度的正向排序。这关系到未来如何选择学习对象，但目前不直接测共享／分离学习的收益。原待检验预期是较高 h 对应更偏深层的解码分布；竞争解释是建边规则使 h 与激活频率耦合，且不同模型层的尺度改变幅度比较。

若两种坐标均支持正向，且完整 p 与频率内比较一致，才可能保留这种描述性排序；若方向不支持或高度依赖尺度，必须缩窄代理含义；覆盖不足的频率格保持不足。以上不把相关升级为因果或训练效用。

## 方法

### 实际对象与术语

{setup}

{terminology}

{method}

### p 和 L 的具体含义

一个 Feature 在一个位置只有一个联合非负激活值 z。该 Feature 在某模型层的解码向量是 z 乘该层 decoder 向量，幅度是 z 乘 decoder L2 范数。p 将同一 Feature 的 14 层幅度按总和归一；共同 z 约消，所以 p 和 L 是固定 decoder 的几何描述，不随展示文本改变。

对模型层号 ℓ∈{{2,4,…,28}}，记该层的 decoder 范数为 dℓ，则 pℓ=dℓ/Σdℓ，L=Σℓ·pℓ。恢复原始坐标时先以保存的该层 TRAIN 向量 RMS 乘 dℓ，再重复同样计算。p 无量纲，图中乘 100 显示百分比；L 的单位是实际模型层号。p 总和为 1；16,384 个 Feature 都没有零总范数或非有限几何，主集合 15,537 个全部有效。

L 只表示幅度加权平均层号。浅层与深层可同时有峰；L 增减不推出整个分布平移。不同 Feature 的解码向量可能抵消，因此幅度相加不是重构能量，更不是独立功能贡献。

### 图、集合与比较规则

边 A→u 要求两端支持 ≥200、共同支持 ≥20、P(u|A)≥0.8、P(A|u)≤0.5、n_u≥2n_A。在 D 发现，在 V 只复核这些原始边，然后分别约简。箭头标签固定为“A→更常见的 u”。h 在完整约简图上计算；显示子图不会另改 h。沿路径频率至少翻倍是构造约束，不是机制发现。

{graph}

频率规则保持原样：Q 上以 D 侧 log10 激活频率固定 5 个分位组，在每组内比较相邻 h 的实际频率共同范围；双方有效节点各 ≥20 才可比较。共同范围只有一个值时同样适用各 ≥20 的规则。本轮无合格单值格。频率比较使用 TRAIN 归一化坐标；本次没有追加恢复原始坐标的频率版本。

原全体结果与 D/raw 参照直接复用。新图3共享节点、横向抖动、横纵轴范围及绘图规则。新组平均热图直接取旧表中各 Feature 等权平均的 p，未按激活频率加权。新峰值比例从已存 p 取唯一最大层后分类计数，不做检验；小于 3% 的柱段仍保留，精确值在源表。h=0 热图包括全部 20 个合格非孤立叶节点；h=5 为两个个体曲线。

## 现象

{phenomenon}

{fig('TRAIN归一化坐标6×14组平均p','figure4_mean_p_train')}

{fig('恢复原始坐标6×14组平均p','figure4_mean_p_raw')}

读图：行是统计图层级 h 与该组 Feature 数，列是实际模型层号；每格为组内等权平均 p 的百分比，每行合计 100%。两图共用 0–40% 色标；少数单元超过 40% 时以色标上限显示，格内数字保留实值。均值保留双端幅度，但不能说明组内每个节点都相同。{tab('原完整均值源表（含D参照）','hierarchy_mean_p.csv')}；{tab('两坐标168格展示源表','group_mean_p_source.csv')}。

| 统计图层级 h | n | TRAIN 归一化坐标 L 中位数 | 恢复原始坐标 L 中位数 |
|---|---:|---:|---:|
| 0 | 20 | 22.717 | 24.015 |
| 1 | 8,896 | 19.902 | 22.359 |
| 2 | 5,347 | 15.007 | 21.099 |
| 3 | 1,209 | 14.305 | 21.025 |
| 4 | 63 | 16.226 | 21.905 |
| 5 | 2 | 18.509 | 22.778 |

这不是逐级严格单调，也不是同一个 Feature 的变化轨迹。源表含每组四分位数以及 D 参照；h=5 正文与图均保留两个个体，不用两点概括总体。

## 解释

{explanation}

另外，原第 28 层工具 FVE 86.4722%、固定替换 CE +0.305962 nats 是既有评估，本轮没有重测。解码几何无法直接说明语义复杂度、模型层功能、层间因果组合，亦不能证明训练或专家分发收益。

## 结论

{conclusions}

认识变化是：原先待检验“较高 h 也许对应更深解码分布”；现在全体 L 的方向不支持正向排序，完整 p 显示同级差异和尺度依赖；保留 h 对统计关联的描述，缩窄 h 作为模型深度代理的说法。频率构成能解释多少、具体分支为何形成、何种对象值得共同学习仍未回答。AI 建议下一次只先讨论上述信息应如何共同保留；不自动启动计算。

## 附录 A：全部图与文本的可追溯性

{fig('全部20个合格h=0节点的两坐标p','figure6_h0_individual')}

图6两面板共用 0–50% 色标；每行是一个 Feature，百分比在全部 14 层合计 100%。20 个节点都以第 28 层为最大分量，但各层幅度比例不同，不能将相同峰值类别当成相同完整轮廓。源表 {tab('20节点×14层×2坐标','h0_individual_source.csv')}。这不是新增文本选择，新增展示的 h=0 节点不自动有新的文本例子。

{link('图索引',D/'figures_cn.md')}完整保留两个原关联子图及密集边分面、同 30 节点 p 热图；不能用 30 个局部节点代替全体比较。

{text}

本次没有重扫缓存、重抽文本或新语义标注。原 240 记录全部保留。

## 附录 B：原正式执行符合性、历史与成本

{conformance}

以上是原正式执行历史，不是本次修订的新开销。原始报告、图与 manifest 的修订前版本另存于 `{V}/before/`，此前已推送的 portable ZIP 保持原字节及 hash。原执行目录与冻结表不被覆盖。

## 附录 C：本次图表修订与证据链

| 项目 | 输入／操作 | 输出与边界 |
|---|---|---|
| 术语与箭头 | 原节点支持数、频率及原图；只更换标签 | V 激活频率明确单位 %；图层级与模型层号分开 |
| 双坐标 h—L | 原 p/L、固定 Q、原抖动、原分位数和相关 | 同 15,537 节点；源表 figure3_coordinate_comparison_source；无重新选择 |
| 完整均值 p | 原 hierarchy_mean_p | 2×6×14 展示格，共用色标；无新均值口径 |
| 峰值类别【事后描述】 | 原 p 逐 Feature 取唯一最大层 | 31,074 个坐标—Feature 标签、36 个比例格；不是预注册检验 |
| 逐节点 p | 原 p 与固定 h | h=0 的全部 20 个、h=5 的原两点；不是扩展文本抽样 |
| 全部频率格 | 原 frequency_overlap_comparison 的 V 25 行 | 原差值与样本数，灰格保留原因；不将不足数值用于比较 |
| 推理审计 | research-reasoning-auditor 对定义、尺度、比较和决策桥的核查 | 保留两个有限认识；不能从描述跳到功能、因果或效益 |

本次本地 CPU 渲染与事后比例计数 23.424 秒，修复图6色标排版另用 3.921 秒；这两个测量程序的最大 RSS 分别约 0.421、0.781 GiB。复核／复制／写报告成本另计，完成回执记录其墙钟。没有新 GPU 分配或远程任务。中文字体只保留执行侧；PDF/SVG 以嵌入字形／路径保证可读，不将字体包加入交付。

修订执行侧：`{V}`；源输入：`{R}` 与原阶段一目录；阅读副本：`{D}`。{link('修订记录与输入hash',D/'provenance/visual_revision_record.json')}；{link('修订完成回执',D/'visual_revision_receipt.json')}；{link('全部源表',D/'tables_cn.md')}；`payload_manifest.json` 记录当前每个文件的来源、字节与 hash。

本次用户只要求图与报告修订；未 commit/push，未修改 Focus、Anchor 或原科学状态。完成后停止，不启动共享／分离学习实验、额外参数扫描或训练。
'''
put('detailed_cn.md',detailed)
# Copy exactly revised figures and source tables; historical tables are unchanged.
for p in (V/'figures').iterdir():shutil.copy2(p,D/'figures'/p.name)
for p in (V/'tables').iterdir():shutil.copy2(p,D/'tables'/p.name)
for p in (V/'code').iterdir():shutil.copy2(p,D/'code'/p.name)
# All twelve figure entries, purpose and interpretation boundaries.
entries=[
('figure1_anchor_937','图1a：937 关联分支','19 节点、45 边；纵轴为统计图层级 h，横向只排版。节点频率以 V 的 5,247,663 位置为分母。箭头 A→更常见的 u；边编号查支持数表。'),
('figure1_anchor_937_details','图1a密集边分面','同一分支的 h=1→0 边，标 D/V 共同命中与 V 条件概率；不改变完整图层级。'),
('figure1_anchor_3461','图1b：3461 关联分支','22 节点、56 边；与另一分支合并为 30 节点、101 边。图的高低不表示模型深浅。'),
('figure1_anchor_3461_details','图1b密集边分面','同一边与支持数分面，避免密集区遮蔽。频率单位为 %，不是 p。'),
('figure2_decoder_distribution','图2：固定30节点的跨层解码幅度占比 p','TRAIN 归一化坐标；行按 h 再 ID，列为模型层号 2、4、…、28。每行 100%，不是激活概率。'),
('figure3_all_features','图3：全体h—L的双坐标对照','相同 15,537 节点、抖动、范围和规则。橙色是中位数及四分位范围，不是置信区间；h=5 单列两点。负向保留，幅度依赖坐标。'),
('figure4_mean_p_train','图4a：TRAIN归一化坐标的6×14平均p','全部 h 的等权平均 p；样本数逐行标明，共用 0–40% 色标，颜色上限截断时仍标真实值。不能替代个体轮廓。'),
('figure4_mean_p_raw','图4b：恢复原始坐标的6×14平均p','相同 Feature、层号和色标。恢复层 RMS 后计算 p，单位 %；不据尺度差异命名功能。'),
('figure5_peak_composition_posthoc','图5：各h的峰值类别比例【事后描述】','同一 15,537 节点；每柱 100%；第 2 层／第 28 层／其他层最大。小于 3% 的段仍保留。没有精确并列最大；类别不是功能标签。'),
('figure6_h0_individual','图6：全部20个合格h=0节点','两个坐标各 20×14，共用 0–50% 色标，逐格标 p。峰值类别相同不等于完整轮廓相同；不含 847 个孤立节点。'),
('figure7_h5_individual_curves','图7：h=5的两个个体','937 与 3461 各自完整 p；横轴实际模型层号、纵轴 %。n=2，只描述这两个节点。'),
('figure8_frequency_all25','图8：频率共同范围内比较','全部 25 格；颜色是高 h 减低 h 的 L 中位差，单位模型层号；11 合格格，14 灰格。格内人数和不足原因保留；不是严格控制频率的效应。')]
index='''# 图与读图说明（修订版）

三类证据分开：**关联分支**看统计边；**跨层解码幅度占比 p**看幅度分布；**全体 h—L**看整体关系。频率格是解释边界。图1—3主类保留，图4—8补充完整分布与边界。

所有图提供 PNG／PDF／SVG。图节点写“V 激活频率”，不再用 pV；解码占比专用 p。图3及分布图使用相同 Q，n=15,537；原输入与阈值未改变。每个 Feature 的 p 合计 100%，L 只是其加权平均层号。
'''
for name,title,desc in entries:
 index+=f'\n## {title}\n\n{desc}\n\n{fig(title,name)}\n\n'+link('PDF',D/'figures'/f'{name}.pdf')+' · '+link('SVG',D/'figures'/f'{name}.svg')+'\n'
index+='\n所有图的源表对应关系与处理记录见 '+link('修订记录',D/'provenance/visual_revision_record.json')+'；'+link('源表索引',D/'tables_cn.md')+'。图已逐幅视觉检查，图6色标移至绘图区外后复查。没有只用公式检查代替实际渲染检查。\n'
put('figures_cn.md',index)
oldindex=(V/'before/tables_cn.md').read_text()
newroles={
'figure1_nodes_display.csv':'图1术语修订：V命中、激活频率百分比与h；原节点未变',
'figure3_coordinate_comparison_source.csv':'图3同一15537节点、h、固定抖动及两坐标L',
'group_mean_p_source.csv':'原V均值表转长表，2坐标×6h×14层；p仍为0—1',
'peak_feature_labels_posthoc.csv':'事后描述：每个坐标—Feature唯一最大层及峰值类别',
'peak_composition_posthoc.csv':'事后描述：2坐标×6h×3类别计数与比例',
'h0_individual_source.csv':'全部20合格h0节点，2坐标×14层p',
'h5_curves_source.csv':'937、3461的2坐标×14层p及L',
'frequency_comparison_25cells_source.csv':'原V全部25格加显示标记；不足显示为NA而非0'}
newindex=oldindex+'\n## 本次图表修订新增展示源表\n\n除峰值类别计数外均为原表／已存几何的展示转换。峰值计数为用户要求的事后描述，没有新增正式检验。\n\n| 表 | 数据行数 | 用途 |\n|---|---:|---|\n'
for name,role in newroles.items():
 with (V/'tables'/name).open() as f:n=sum(1 for _ in csv.DictReader(f))
 newindex+=f'| {tab(name,name)} | {n:,} | {role} |\n'
newindex+='\nCSV中的p与share保留0—1原始精度，图中乘100显示%。原12张表均未覆盖修改。来源hash见 '+link('修订记录',D/'provenance/visual_revision_record.json')+'。\n'
put('tables_cn.md',newindex)
readme=f'''# 阅读入口：统计图层级与跨层解码幅度分布

当前为 **2026-10-14 图表修订版**。同一正式运行的读取副本，不是第二次实验。原始趋势、频率格、文本与节点选择保持不变；新增峰值比例明确为事后描述。

先读 {link('简短中文报告',D/'summary_cn.md')}，再看 {link('全部图与读图说明',D/'figures_cn.md')} 和 {link('完整中文报告与追溯',D/'detailed_cn.md')}。

- {link('全部源表',D/'tables_cn.md')}：原12表＋本次8张展示／峰值表。
- {link('随机及高激活文本',D/'text_examples_cn.md')}：原240条，未重抽。
- {link('本次修订范围',D/'provenance/visual_revision_scope_cn.md')} 与 {link('修订完成回执',D/'visual_revision_receipt.json')}。
- {link('原正式计算完成回执',D/'completion_receipt.json')}：只代表原任务pt-icv8hyi3，不代表本次成本。

执行侧本次修订：`{V}`。原报告和图的修订前版本完整保存在该目录的 before/；原正式输出仍在 `{R}`。

此前已推送的 {link('portable ZIP（此前版本）',H/'results_20261014T020014Z_portable.zip')} 保持原字节，其SHA256为 `2411367ff2f533e7e98bc7f64699db4a9dcac01cd898c28049a633033bfaca75`；它不含本次修订，不应与当前报告混用。本次没有commit/push或重打该ZIP。

图中的统计图层级 h、模型层号、激活频率、跨层解码幅度占比 p、幅度加权平均层号 L 是五种不同量。频率格不是因果效应；峰值类别不是层功能。交付后停止，后续研究决策由研究者讨论。
'''
put('README_cn.md',readme)
scope=f'''# 用户授权的图表与报告修订范围

修订ID：`visual_revision_20261014T025700Z`；处理者Codex，线程01a1343f-32aa-7500-9835-000956218089。

用户当前请求授权：统一五项术语与箭头；双坐标全体h—L对照；两张完整6×14组平均p热图；各h峰值类别比例；20个h0个体、2个h5曲线；完整25频率格；将报告重排为目的→方法→现象→解释→结论，保留两条主要认识并接到下一研究决策。

这是一项**事后图表和解释修订**。原Anchor和冻结Protocol、阈值、Q、h、D/V划分、频率边界与有效性门槛、文本选择不改。原执行报告及图先备份到 `{V}/before/`；原执行目录中的正式表、几何和冻结Protocol不覆盖。原已推送ZIP不改。

唯一新增统计为用户明确要求的峰值比例事后描述：在每坐标下，逐Feature取14层p的唯一最大值，按模型第2层最大／第28层最大／其他层最大分类；每h等权计数，比例分母为该h的Q节点数。两坐标全体无精确并列最大值。保留完整p，类别不用作功能或common/unique标签，不增加p值、参数扫描或候选排名。

报告第一用语处明确对象与计算；审计重点为整体相关与局部频率格不可相互替代、L不是整分布移动、坐标尺度不是功能差异、局部节点不是全体证据、描述结果不授权训练或科学状态转移。

本次无GPU/远程新任务、推理、训练、缓存扫描、全量共现计数、重新构图、重新抽文本、commit/push。计算输入hash和新图hash见同目录修订记录与payload_manifest；完成回执区分原正式成本与本次修订成本。
'''
(V/'visual_revision_scope_cn.md').write_text(scope)
shutil.copy2(V/'visual_revision_scope_cn.md',D/'provenance/visual_revision_scope_cn.md')
print('Revised reports, 12x3 figures and 8 tables copied; validation/receipt pending.')
