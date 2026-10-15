# 详细记录：A17_04_E02 旧规则学习诊断

主 Anchor：[A17_04_01](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor_cn.md)。  
冻结 Protocol：[protocol_cn.md](protocol_cn.md)，版本 `a17_04_e02_acquisition_diagnosis_v1`。  
Summary：[summary_cn.md](summary_cn.md)。本记录不裁定研究者的科学判断。  
证据资格：CPU／数据、旧状态读数、Smoke 与五臂正式输出分别具备限定的诊断／工程资格；五臂均完成固定预算，独立分析与 Full 当前严格访问检查通过。平台Full已SUCCEEDED；末端物理张量／整体freeze终验通过，与科学合格分开记录。研究者科学判断与问题关闭均为 `Unknown`。

## 0. 结果速览

目的：判断旧规则没学会，究竟在已见训练输入上就存在，还是只在未见输入上发生；随后比较有界的优化器、可训练范围与数据表述调整。

假设：至少一种预定路线能在固定预算内可靠学会两条旧口令。竞争解释包括曝光量／优化不足、未见输入泛化困难、表述或可训练计算范围受限。不要求某一臂必须成功。

实验逻辑：先读原三个旧训练终点在固定训练面板与 DEV 上的行为，再让五个新训练臂分别从相同 Base 开始。每臂先做微型拟合，再重新从 Base 开始完整数据训练。本轮不含新模式更新、敏感方向删除、SAE 或专家比较。

目前直接结果：原旧状态在已见训练面板上的准确率只有44.5%–45.5%，DEV 为44.375%–44.75%；同一训练列表的两条口令都选对的比例只有4.5%–5.5%。因此，原问题并非只发生在未见列表上。五臂 Smoke 和独立进程下一步恢复均通过。正式任务 `pt-qsqimkvo` 的五臂固定训练均完成：C中性口令扩大attention和D自然措辞通过四格门槛；A／B／E未通过。C在240步的四格已均为100%，1200步仍为100%；D终点合并86.75%、最低格82%。这提供了可行学习路线，不定位纯参数数量机制。

边界：旧三种子是既有状态读数，不是新训练的三次复现。Smoke 证明实现可运行，不能证明规则学会。新五臂只有一个训练种子，并使用已暴露的 DEV；本轮是诊断，不是独立确认或任务间干扰证据。

## 1. 对象与术语

| 术语 | 白话与具体计算 | 单位 | 用途与边界 |
| --- | --- | --- | --- |
| 旧映射 | 可见模式一，甲取首项、乙取末项 | 一个答案词元 | 两条规则可以同时满足，没有相同完整输入的矛盾标签 |
| 训练面板 | 预定200个已见训练列表，各问甲乙，不反传 |400答案 | 区分已见拟合与未见表现；不是独立确认 |
| `order_new` | 三个词的组合见过，排列没见过 |200列表／400答案 | 只检验新排列 |
| `combination_new` | 三个词的无序组合没见过 |200列表／400答案 | 仍来自同20词表 |
| 微型拟合 | 固定32训练列表、64答案，循环训练160步 |实际呈现3,200答案 | 可以是记忆，不能等同泛化 |
| 双口令都对 | 同一列表的甲乙答案均为全词表预测正确 | 列表比例 | 直接要求按口令改变答案 |
| 两口令同答 | 同一列表甲乙的全词表最大概率词相同 | 列表比例 | 揭示未能稳定切换，不能定位内部机制 |
| 口令响应 | 两口令“末项相对首项”对数优势之差的一半 | nat | 均值为正不代表可靠学会 |
| 资格门槛 | 四个 DEV 口令／面板格子准确率都至少80% | 四格最小准确率 | 操作性门槛，不是统计置信度 |

## 2. 与主问题的衔接

父实验 E01 的旧 DEV 分项只有33%–54%，因此尚不能解释“已学规则的保留／遗忘”。本子实验只寻找合格的旧规则起点。A/B 比较固定矩阵下的优化路线，B/C 扩大可训练 attention，B/D 改口令措辞，B/E 改列表分隔。未来要决定的是采用哪种学习起点，而不是直接拆专家。即使诊断成功，也不会自动进入新的迁移实验。

## 3. 冻结、符合性与偏离

冻结时间为北京时间2026-10-11 21:18:16.854727（13:18:16.854727UTC）；[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/freeze.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/freeze.json) 绑定45个决定性文件。双语 Anchor／Protocol 均在 GPU 运行前保存了快照。

| 预定内容 | 实际快照 | 状态与资格影响 |
| --- | --- | --- |
| 不再中间审批的有界诊断 | 用户授权诊断、数据／参数评估及可行的增加参数训练 | 已授权；不制造研究者机制判断 |
| 注册 Base、源旧 TRAIN／DEV | 模型、分词器、源数据及三个旧状态家族的当前严格检查通过 | 输入合格 |
| 三种派生表述、十二文件 | 合同后正式生成，manifest 与派生数据严格检查通过 | 诊断数据合格 |
| 五臂共同 Base、seed29、batch20 | 五臂 Smoke 与 Full 均按冻结设置完成 | 符合；单一种子诊断 |
| FP32／原生 SDPA／冻结／恢复 | Smoke 环境与五条独立恢复记录通过 | 工程证据 |
| 微型160步＋独立完整1200步 | Smoke 合格后提交 `pt-qsqimkvo`，五臂均达到160／1200 | worker完成与独立分析PASS；总6,800步／136,000答案 |
| 正式流程排除原 TEST | 正式生成器／训练器／分析器均不加载原 TEST | 保留下面的早期暴露事实 |
| 旧状态文件名 | Protocol 的概念产物名为 `prior_endpoint_diagnostic.json`；实际是 `audit/seed_N/{train_panel,dev,completion}.json` | 文件组织区别，读数内容一致 |
| 恢复记录阶段名 | receipt 中仍写旧别名 `full_data`，实际恢复目录和循环是 `main` | 元数据别名，不改变实际状态重放 |
| 提交证书状态 | 创建时保留 RUNNING、Full 待资格的文字；后续平台证据记录 Smoke 成功与 Full 提交 | 历史提交记录不冒充最终完成 |

本轮无训练重试、臂排除或看到结果后改预算。五臂均完整执行；源码／配置／数据继续冻结。末端物理张量与全freeze终验分别通过，不能拿平台成功替代。

早期暴露边界：此前 CPU 结构审计看过父数据 TEST 的 schema／分词。一次初始审计还反序列化了含 DEV 与 TEST 预测记录的旧 JSON，但所有模型读数计算均筛选 `split == 'dev'`。所以不能声称 TEST 预测记录从未打开。没有用 TEST 模型结果选择本轮设置，也不把它报告为本轮新证据。本轮明确使用 DEV 做诊断；后续正式确认需要新的 heldout 数据。

Host CPU 资格曾遇到 ONNX／protobuf 导入不兼容，随后在已检查的挂载 runtime 的 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` 设置下通过。没有修改基础镜像包或科学设置。

## 4. 实际设置

### 数据与监督

派生资产为 `data_a17_mapping_acquisition_diagnostic_v1`，源资产 `data_a17_conditional_mapping_v1`。每种表述均有 TRAIN2,400、DEV800、训练面板400、微型64条。TRAIN 是1,200个双口令列表；DEV 是400列表，两个未见面板各200列表。训练面板在 GPU 前按固定规则选十个完整20列表词轮换环，保证词表／位置均衡。微型集合取前两个环中的32列表，不强求词频均衡。面板／微型 record IDs 是 TRAIN 子集；三表述的底层列表与目标一致。

所有记录保留 mode1、old world、甲乙别名、列表词、目标及源记录链接。`neutral` 保持原空格列表和甲乙口令；`explicit` 把输入中的甲乙改为“取第一项／取最后一项”，元数据别名不变；`normalized` 保留中性口令，只把列表空格换成顿号“、”，不叠加自然规则措辞。

20个答案词为红、黄、蓝、黑、绿、白、紫、灰、金、银、猫、狗、鸟、鱼、牛、马、羊、虎、龙、花。目标答案为单词元，前文与答案拼接边界也核验通过。原空格输入中，部分候选词的上下文编码不同于其答案词元；这不等于答案边界或标签有错。顿号表述全部候选位置均通过了完整前文中的单词元 ID 检查。标签／源记录／划分一致、双口令、词表／位置均衡及 TRAIN／DEV 排除检查见 [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/qualification.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/qualification.json)。

只对答案位置的一个词元计算 CE；前文和 padding 不进入训练预算或损失分母。正确率使用全词表最大概率答案。

### 模型与五个条件

注册模型／分词器为 `model_qwen3_0p6b_base_official_a5`、`tokenizer_qwen3_0p6b_base_official_a5`；Base 精确目录 `/data/250010109/model_cache/Qwen3-0.6B-Base-official`。28层 Qwen3，FP32、原生 SDPA、eval 无 dropout、确定性算法、关闭 TF32。新臂不从旧 adapter 开始。

| 臂 | 输入 | 可训练对象／参数数 | 优化器 |
| --- | --- | --- | --- |
| A `o_sgd` | neutral | 第27层 `self_attn.o_proj.weight`，1,024×2,048／2,097,152 | 普通 SGD，LR0.01 |
| B `o_adam` | neutral | 相同一个矩阵／2,097,152 | AdamW，LR1e-4 |
| C `attn4_adam` | neutral | 第24–27层 attention q/k/v/o，16个权重／25,165,824 | AdamW，LR1e-4 |
| D `explicit_o_adam` | explicit | 相同末层 o 矩阵／2,097,152 | AdamW，LR1e-4 |
| E `neutral_normalized_o_adam` | normalized | 相同末层 o 矩阵／2,097,152 | AdamW，LR1e-4 |

C 的参数数为原来的12倍，同时改变了可训练计算位置。每次执行完整原生前向；扩展范围没有继续使用固定上游表征缓存。bias、q/k norm、MLP、embedding、final norm、输出头均冻结。实际参数名称／形状／数目对照 safetensors header 独立检查。

每步为4个 microbatch×5记录=20有效答案，累计梯度全局 norm 裁剪1。AdamW 的 betas(0.9,0.999)、eps1e-8、weight decay0，关闭 foreach／fused。SGD 无动量／衰减。恒定学习率，无 warmup、早停或看到结果后续训。

### 预算、保存与资源

每臂微型160步=3,200答案；随后重新恢复 Base 可训练参数、全新 optimizer 与 RNG，完整训练1,200步=24,000答案。五臂实际总量为微型16,000与完整120,000答案。微型不作为完整训练热身。完整里程碑为0、1、240、600、1200步；微型0、1、160步。微型起终点还测训练面板／DEV。保存状态依赖精确 Base，并包含所有可训练张量、优化器、RNG、schedule、计数、数据顺序与来源身份。

Smoke 每臂两个阶段各3步，合计30步／600答案。独立进程恢复每阶段额外重放一步，合计10步／200诊断答案，单列于 Full 预算之外。Smoke 保存30个实际状态：两个阶段×五臂×0、1、3步。

资源为单节点4卡 H10080GB SXM5，`h100-4-reserved`；ACP `share-space`／`share-cluster`，spec `n6ls.iu.i40.4`，镜像 `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423`。lane0/1/2/3并行跑A/B/C/D，lane0随后跑E。各 worker 为独立实验臂，不做 DDP 聚合。每个 job 上限7,200秒。答案曝光量一致，FLOPs／时间／前文词元量不一致。

### 复用、代码与冻结

[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source/diagnose.py](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source/diagnose.py) 适配已实际阅读的父实验 AnswerLM／手动 SGD／观测实现。`native.py`、`carriers.py`、`runtime.sh` 从已读父包复制；新代码扩展参数选择、Adam 状态、拟合对照与双口令读数。已查 clean trainer 源码审计、复用索引与观测合同；不复用它的 MoE／DDP 架构或退役生产配置。复用决定见 [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json)。

| 对象 | SHA256 |
| --- | --- |
| 运行配置 | `2c3450225bac11384df53ac077f612dc64b964111ec745a6c97057ace8b8df1e` |
| 数据 manifest | `05dfb9ac05ebf20dcf560b51d880acdb9472596b2a0a346aa8401d0dc9438a89` |
| 训练器 | `b9f73eb4d797a04f20e9b0aa7b6f4448daea5a3aebfda9b764ba8694ceef74f6` |
| 分析器 | `baa738e4908cf662ae7a6f9894bd4d93441eb6d46ec3436ad5162402f2eecb0f` |
| 冻结英文 Protocol | `1ddc77dce61f26c5ef804d2375bf33c6dc1adfe1facf67b2e4895b04b76d0126` |
| 冻结中文 Protocol | `86fbd7cc8c64cc050090eebe3752e87bf0953b8475212d5e6dbb990322ec4a7d` |

## 5. 指标与预定判断规则

每个口令／面板格子有200目标；正确率是全词表预测正确数除以200。主指标为1200步时四格 DEV 准确率的最小值；每格均达到0.80才合格，合并均值不能补救某个失败格子。两个未见面板分别报告，再等权合并；同时保留已见训练／微型读数。微型拟合没有另设新的二元门槛。

给定列表候选集合 S 和正确答案 y，保留 CE、候选总概率 P(S)、进入候选集合的损失与集合内部选择损失：

\[
-\log p(y\mid x)=-\log P(S\mid x)-\log\frac{p(y\mid x)}{P(S\mid x)}.
\]

双口令读数定义末项相对首项优势 s，以及口令响应：

\[
s_c=\log p(L_3\mid x_c)-\log p(L_1\mid x_c),\qquad a=(s_{乙}-s_{甲})/2.
\]

另存正确答案相对相反端点／最强全词表错误答案的优势、竞争词 ID、双口令都对、两口令同答。损失分解不能证明内部功能模块或因果机制。保留计数与全部预定里程碑；新训练只有一种子，不给总体置信区间／显著性结论。旧三种子的只读评估不会把新五臂变成三种子。

七个 TensorBoard 标签遵守训练观测合同。token 坐标仅用每步20有效答案，前文另计。每步还记 raw／clipped gradient norm、实际 step norm、步前权重 norm、相对位移及吞吐。吞吐包含梯度／更新／norm／冻结版本检查，不含评估／保存／TensorBoard 时间。冻结版本与字节、有限性、no-op、计数及独立恢复用于工程资格。

## 6. 证据链

| 判断 | 规则与原始来源 | 计算／汇总 | 当前观测 | 资格与边界 |
| --- | --- | --- | --- | --- |
| 已见列表也未可靠学会 | 三个原240步状态；`/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/audit/seed_N/train_panel.json` | 每状态400答案、200双口令列表 | 准确率44.5/44.5/45.5%；双口令都对4.5/5.5/4.5% | 既有状态诊断；不是全部训练数据 |
| 经常未随口令换答案 | 同文件 paired 字段 | 每列表两条全词表 argmax 是否相同 | 已见训练面板85.5/85/87% | 行为观察，非内部机制定位 |
| DEV 同样低 | `audit/seed_N/dev.json` | 每状态800答案、两面板 |44.5/44.75/44.375% | 已暴露 DEV 诊断 |
| 实现／恢复可运行 | `smoke_gate.json`、每臂 telemetry／冻结记录／恢复 receipt | 五臂×两个独立阶段 | 全部 PASS | 仅工程 |
| Smoke 保存可复用 | 登记 receipt 与当前严格输出检查 |30状态／10家族＋1native分析家族 |11IDs`REGISTERED_ACCESS_PASS` | 不能据此认定规则学会 |
| 哪种路线可修复 | 冻结四格门槛与`analysis/results.json` | 单一种子、固定1200步 | C四格100%，D最低82%；A43%／B58%／E46% | 两条操作性路线合格；不自动批准后续迁移 |
| 独立完整读数核验 | `analysis/analysis_manifest.json` |91预测文件／46,560记录，40实际Full状态hash |最大损失恒等式误差9.996755e-7 |实际hash／size和manifest字段，不冒充独立反序列化所有张量 |

## 7. 主要结果

### 原旧状态的有资格诊断读数

| 原种子 | 训练 CE | 训练准确率 | 训练双口令都对 | 训练两口令同答 | DEV CE | DEV准确率 | DEV双口令都对 | DEV两口令同答 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|29|1.147346|44.50%|4.50%|85.50%|1.170393|44.50%|7.25%|85.00%|
|43|1.151172|44.50%|5.50%|85.00%|1.171855|44.75%|7.00%|85.25%|
|71|1.147121|45.50%|4.50%|87.00%|1.170798|44.375%|8.00%|80.75%|

数值直接来自上面的逐种子文件。固定已见面板也低，削弱了“只是未见列表泛化失败”的单一解释；不表示每条训练输入都没拟合，也未定位是哪部分计算受限。

### Smoke 工程结果

`pt-2x5gujhd` 已成功。五臂均从独立 Base 起点完成微型／main各3步，原生评估有限；两个阶段均通过新进程从step1恢复后对step2的逐位核验。七标签与冻结检查通过。30状态登记为10checkpoint家族，加1native分析家族。Smoke 不用科学准确率门槛判定工程失败。

### 正式学习修复结果

五臂均按预定预算完成。下表来自 [独立结果JSON](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/analysis/results.json) 与 [完整曲线表](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/analysis/trajectories.csv)。每臂一个训练种子；训练面板400答案，DEV每面板400、合并800答案。C／D是操作性学习资格，不是研究者问题关闭。

| 臂 | 已见训练面板 | 新排列DEV | 新组合DEV | DEV合并 | 四格最小 | DEV双口令都对 | DEV两口令同答 | 最早合格保存步 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
|o_sgd|51.75%|47.75%|51.5%|49.625%|43%|11%|80.75%|未达到|
|o_adam|82.25%|64.25%|72.75%|68.5%|58%|39.5%|52.75%|未达到|
|attn4_adam|100%|100%|100%|100%|100%|100%|0%|240|
|explicit_o_adam|97.25%|84.75%|88.75%|86.75%|82%|73.75%|22.75%|600|
|neutral_normalized_o_adam|81%|58.25%|72.75%|65.5%|46%|36.75%|50.5%|未达到|

四格终点，顺序为甲／新排列、乙／新排列、甲／新组合、乙／新组合，每格200答案：

| 臂 | 甲／新排列 | 乙／新排列 | 甲／新组合 | 乙／新组合 |
| --- | ---: | ---: | ---: | ---: |
|o_sgd|52.5%|43%|59.5%|43.5%|
|o_adam|58%|70.5%|77%|68.5%|
|attn4_adam|100%|100%|100%|100%|
|explicit_o_adam|82%|87.5%|90%|87.5%|
|neutral_normalized_o_adam|46%|70.5%|74.5%|71%|

微型实验和完整训练是两条独立轨迹。微型终点自身拟合与它的 DEV 泛化必须分开：

| 臂 | 微型64目标准确率 | 微型双口令都对 | 仅微型训练后的DEV |
| --- | ---: | ---: | ---: |
|o_sgd|51.562%|9.375%|46%|
|o_adam|85.938%|84.375%|48.75%|
|attn4_adam|100%|100%|100%|
|explicit_o_adam|100%|100%|61.75%|
|neutral_normalized_o_adam|81.25%|78.125%|45.125%|

B在64目标上85.94%，但其微型轨迹DEV仅48.75%；所以小集合上有所拟合并不等于泛化。D微型100%而DEV61.75%，同样如此。C微型与DEV均100%，说明本次任务存在有效的条件学习路线，不能把原失败归为规则本身不可能满足。

完整训练终点的输出分解如下。概率是列表三个候选合计；所有值是DEV800目标均值，CE／两项损失均为nat：

| 臂 | 答案CE | 列表候选总概率 | 候选进入损失 | 候选内选择损失 | 口令响应a |
| --- | ---: | ---: | ---: | ---: | ---: |
|o_sgd|1.0319582|97.898%|0.021794|1.010164|0.110277|
|o_adam|0.70223597|99.747%|0.002567|0.699669|0.953971|
|attn4_adam|2.1249036e-07|100%|≈0|≈0|27.197257|
|explicit_o_adam|0.33283179|99.976%|0.000242|0.332590|2.423928|
|neutral_normalized_o_adam|0.78717761|99.858%|0.001430|0.785748|0.799155|

A候选总概率已97.90%，准确率仍49.625%；B／E候选总概率超过99.7%，准确率仍为68.5／65.5%。所以“预测更集中于候选词”不足以说明条件选择学会。C把候选内部选择误差也降至约0。C训练面板的条件项原始均值为−2.95e-8，这是FP32答案CE与double候选logmass混合的舍入误差；数学条件CE非负，原始值保留，解释写约0，不能当成负损失收益。独立核验最大恒等式误差9.996755e-7，低于预定2e-5。

C在原曝光点240步四格即均100%，A/B/D分别合并44.5/48.75/71.875%。因此扩大范围的成功不必依赖把步数延长到1200，但尚未区分可训练位置、参数数目与优化几何。D的Base DEV已58.125%，中性原表述为33.25%；自然措辞成功可以利用既有语义，不能视为原中性映射完全等价的修复。E整体低于B，既没有达到门槛，也不支持“空格编码是原失败的充分原因”。不据此否定分词对学习的所有影响。

实际main平均每步位移为A0.009976、B0.033880、C0.005446、D0.034135、E0.034078；累计路径长度为11.97078、40.65580、6.53505、40.96238、40.89403。C后期梯度接近0会降低全程平均位移，不能把全程均值当成相同状态下的步幅匹配。完整步级证据见 [training_exposure.csv](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/analysis/training_exposure.csv)。

### 最终工程、复现与精度核验

- [平台终态](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_terminal_status.json)：Full `pt-qsqimkvo` 在北京时间2026-10-11 21:34:17（13:34:17UTC）为SUCCEEDED；创建21:24:04，启动21:24:55。Smoke在21:23:32完成。两个任务均无重试。
- [执行后freeze核验](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/post_execution_freeze_check.json)：45个冻结文件逐一hash一致，原始Base／旧checkpoint／源码／配置／数据／合同快照均未改变。
- [独立实际张量审计](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/independent_checkpoint_tensor_audit.json)：在实际输出strictPASS后，反序列化五臂tiny／main共10个末端状态，权重与optimizer有限、精确参数数量及step／token计数均符合。新A的240步o_proj与原seed29旧240步实际张量逐字节相同；这核验原路径复现，不是新的科学发现。
- [独立精度审计](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/precision_decomposition_audit.json)：从已保存double `target_logp`／`list3_logmass`重算条件CE，最小0；原native混合精度条件项单记录最小−3.33077e-7，在原工程误差范围内。double重算C的DEV条件CE均值4.20291e-8、训练均值1.41525e-8，均约0。原native记录没有覆盖或修饰。

91预测文件、46,560记录及所有40个Full状态由冻结独立分析器检查hash／size与manifest；上述10个实际末端进一步检查了张量内容，不能把二者范围混为“所有40状态均独立反序列化”。无新增GPU更新或后续迁移训练。

## 8. 分阶段证据与失败分解

| 阶段 | 证据 | 状态 | 排除与保留的解释 |
| --- | --- | --- | --- |
| CPU答案损失／Adam恢复 | `configs/cpu_qualification.json` | PASS，toy累计／总批梯度最大差1.49e-8 | helper算术可用，不等于实际模型学会 |
| 正式派生数据 | manifest／qualification／严格资产 | PASS | 未见标签、配对、答案边界错误；表述难度仍是候选因素 |
| 旧状态训练／DEV读数 | 三个原旧状态 | 完成 | 并非只有DEV泛化问题；优化／范围／表述仍未区分 |
| 真实GPU Smoke／独立恢复 | gate／receipts | PASS | Smoke仅证明有限训练／冻结／重放合同可用；学习结论另由Full终点给出 |
| Full路线比较 | 五臂固定终点 | 完成，C／D合格，A／B／E未合格 | 排除任务本身无法学会的强解释；普遍容量或纯参数数目机制仍未识别 |
| 独立终点分析／Full资产 |91files／46,560records／40states，Full11IDs | 分析PASS，strictPASS | 仅有界单种子DEV资格；末端物理张量／整体freeze另有PASS证据 |

本轮没有推翻普遍物理先验或数学容量界限；可行的C路线反对“该任务在此Base上无法学会”的强解释。没有发现能解释旧学习失败的实现错误。候选概率较高、响应均值为正、CE较低，都不能替代双口令可靠选对。

## 9. 完整轮次记录

2026-10-11轮次：

1. 问题：旧失败在已见输入上是否存在；预定优化／范围／表述路线能否修复？
2. 设置：精确注册Base；旧三状态只读；五个新臂按冻结范围、优化器、seed与预算从Base独立开始。
3. 训练：源old TRAIN派生三表述，列表／目标一致；微型训练与完整训练独立。
4. 测试／确认：400目标已见面板、800目标双面板DEV、64微型目标。没有新的独立确认集；保留原TEST早期暴露边界。
5. 结果：CPU／数据／Smoke／恢复PASS；旧状态训练／DEV如上；五臂固定训练完成，C与D通过预定学习资格，A／B／E未通过；Full实际40状态、独立分析与严格访问齐全。平台SUCCEEDED与末端物理／freeze审计PASS另列。
6. 认识与下一决定：旧状态在已见列表也常不随口令切换，因此寻找合格起点是合理诊断。固定比较已完成；AI建议若保持中性口令问题，可考虑C的240步合格状态。后续研究者科学下一决定仍为Unknown。

## 10. 解释

旧状态行为与“主要适应候选词，口令控制选择仍很弱”相容，不能说规则已经学会、只是泛化失败。本轮已区分出实用路线：原SGD增加曝光仍未合格，改Adam有所改善但不足；扩大attention在中性口令下合格，自然措辞也有合格路线，单独改顿号不足。C首先证明可用的可训练计算范围，不是纯参数数量机制。

## 11. 结论边界

可以说：旧状态的已见拟合也不足；五臂固定预算完成；C在本次中性任务、D在自然措辞任务中达到操作性门槛；完整产物、独立读数与当前严格访问通过。

不能说：0.6B普遍容量不足、原末层矩阵绝对不能学会、纯参数数量／独立分词因果、已学规则受新任务干扰、拆专家收益、未见确认或统计复现。

## 12. 下一决定

研究者科学下一决定：`Unknown`。本轮固定训练与独立读数分析已完成；末端物理／freeze检查亦已通过，当前为双语事实交付。AI建议下一科学工作在保留中性口令的合格起点上，用新heldout数据再检验迁移；这不是本轮自动执行范围。不增加新臂、种子、预算或迁移任务。

## 13. 产物清单

| 产物 | 用途／生成者 | 身份与完整性 | 可支撑范围 |
| --- | --- | --- | --- |
| [冻结manifest](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/freeze.json) | GPU前45文件绑定 | 实际hash与时间戳齐 | 工程来源 |
| [运行配置](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/config.json) | 五臂精确设置 | SHA见§4，完整 | 冻结诊断设计 |
| [数据manifest](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/manifest.json) | 源／派生记录与划分 | SHA见§4，十二文件齐 | 数据来源 |
| [数据资格](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/qualification.json) | 标签／划分／边界／顿号offset | 正式生成输出PASS | 数据资格，非学习 |
| [当前输入](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_input_access.json) | 原选定资产 | 使用前strictPASS | 输入可访问 |
| [派生数据访问](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_derived_data_access.json) | 新数据release | strictPASS | 新数据访问 |
| [Smoke gate](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/smoke_gate.json) | worker／重放／旧读数齐全 | 五臂PASS | 工程 |
| [Smoke平台receipt](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/smoke_terminal_status.json) | ACP直接状态 | `pt-2x5gujhd` SUCCEEDED | 仅平台完成 |
| [Smoke登记](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/smoke_registration_receipt.json) |10状态家族＋1native家族 |11IDs、30实际状态 | 实际payload可用 |
| [Smoke严格访问](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_20261011t130809z_smoke_outputs.json) | 选定实际Smoke输出 | PASS | 访问／schema，不等于科学支持 |
| [旧状态审计](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/audit) | 三旧状态训练／DEV | 每种子文件齐 | 既有状态诊断 |
| [Full提交](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_launch_contract.json) | 精确命令／profile／scope | `pt-qsqimkvo`与submitlog | 提交，非完成 |
| [Full输出](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full) | 微型／main曲线与状态 | 五臂完整，40实际states | 单种子DEV诊断资格，平台与末端审计通过 |
| [独立分析器](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source/analyze.py) | CPU重算CE／配对／计数／manifest | 冻结SHA见§4，独立实际分析PASS | 不等于科学批准 |
| [Full平台终态](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_terminal_status.json) | ACP直接终态 | `pt-qsqimkvo` SUCCEEDED，21:34:17北京时间 | 平台完成，与学习门槛分开 |
| [执行后freeze](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/post_execution_freeze_check.json) |45冻结文件hash复核 | PASS | 设计／源码／输入未漂移 |
| [实际末端张量](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/independent_checkpoint_tensor_audit.json) |10末端反序列化＋A240原路径复现 | PASS，A240字节一致 | 工程复现，不是机制支持 |
| [精度分解](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/precision_decomposition_audit.json) | 保存logp64的独立重算 | 条件CE非负，native近零负值为舍入 | 保留原native记录 |

Smoke家族ID为 `adapter_a17_04_acquisition_20261011t130809z_smoke_{ARM}_{tiny|main}`；native家族为 `analysis_a17_04_acquisition_20261011t130809z_smoke`。各member manifest保留实际路径、字节数与hash。Full已按实际40状态登记10家族，另1native分析家族，共11IDs；[Fullreceipt](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/full_registration_receipt.json) 和[当前严格检查](/data/250010109/Research_System/assets/checks/2026-10-11_a17_acquisition_20261011t130809z_full_outputs.json)均为PASS。Smoke／Full合计70个实际状态、20个checkpoint家族，另两组native分析；不复制raw到研究仓库。

## 14. 链接与复现

- Protocol：[英文](protocol.md)、[中文](protocol_cn.md)。
- 源码：[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/source)。
- 复用审计：[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/provenance/reuse_decisions.json)。
- 资源receipt：[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/execution_certificate.md](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/execution_certificate.md)。
- Run：[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z)；日志：[/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/logs](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/runs/acquisition_20261011T130809Z/logs)。
- 按冻结配置和精确Base复现；worker命令例：`python source/diagnose.py --config RUN/config.json --run RUN --arm o_adam --phase full --rank 1`，先加载已检查runtime。这里只记录接口，不表示应重复提交既有任务。
- 任务：Smoke `pt-2x5gujhd`；Full `pt-qsqimkvo`。本快照没有重新提交。
