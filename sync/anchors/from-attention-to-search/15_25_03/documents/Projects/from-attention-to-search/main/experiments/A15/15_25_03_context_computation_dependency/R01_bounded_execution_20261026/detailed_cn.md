派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/detailed_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/detailed_cn.md)；研究修改仍回到原件。

---

# 完整执行记录：冻结数据门槛未通过

## 问题与资格层次

目标是源层C干预的后层R与预测效应。当前只执行到其前提——是否存在足够同token、不同续词的独立上下文。数据门槛失败不能替代功能假设的阴性证据。结果类型为数据资格不足；下游所有条件NOT_RUN。

## 授权、冻结与实际复用

本轮用户明确指令“继续执行本协议……资格不足就如实报告”。沿用R00英文／中文Protocol和JSON配置，不改科学体或阈值；执行前将其与实际源码SHA记录在`provenance/execution_freeze.json`。源码只使用原TRAIN JSON与原tokenizer，未复用训练器、优化器或MoE；旧`extract_sft.py`用于明确位置连接：t从answer_start−1到n−2，目标为input_ids[t+1]。唯一实现细化为：目标无关固定SHA挑每token每文档一处，支持按两类较少一类计，分层内固定SHA平衡。该细化记录于执行前freeze，并且本轮在分层之前已不满足64门槛。

## 数据流与完整分母

TRAIN源SHA为5530f9676c3d7941150e404c045ad62815a11310d8b1ec4904c209121ddb8ad5，原tokenizer JSON SHA为c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539。总85548答案位置中，按互斥先后筛选：特殊当前／下一token排除1024；当前词片无Unicode字母排除20262；不足16个后续答案目标排除10872；完整前缀加目标超512排除0。余53390；这些条件之外没有按准确率或梯度筛选。特征频率未使用。

每个(token,prompt_sha256)按固定SHA取一个位置，得到35546个上下文。每token只按该池支持最多两种下一token分类（平局按ID）。4024个有两类的token逐项保留，较少类最大43，无一达到64。匹配键为(dataset,答案位置//16,前缀长度//32)，每层两类取同样多文档、SHA固定选择；最大23/class。样本本就每token每文档一处，因此没有把同文档多次出现计作独立支持。

## 预定／实际对照

| 项目 | 预定 | 实际 | 证据／影响 |
|---|---|---|---|
| 输入 | 固定Tulu TRAIN发现，EVAL探索性留出 | 只读TRAIN；EVAL/TEST均未读 | 原数据hash、访问回执 |
| 候选门槛 | 每类64独立文档、同token | 最大较少类43 | 数据资格不通过，不能后退门槛 |
| C/R池及局部读数 | 合格token后选择并核验 | NOT RUN | C/R身份未形成，R资格未知 |
| 0.05/0.10与匹配对照 | 资格通过后独立配对 | NOT RUN | 没有损失、R效应或区间 |
| 预算 | 计划4864，硬上限12000 | 前向0 | 剩余额度不授权扩展数据 |
| 模型／资产 | 冻结、不训练、不分配资源 | 未加载模型，未写权重 | 没有新增checkpoint |

## 实际产物与复现

执行侧`source/discover_support.py`是原始发现程序；`source/report_data_gate.py`只做报告、保存表核对及解释性TRAIN文本抽样。原始完整表`tables/token_support_all.csv`含4024行，停止回执`support_receipt.json`、访问/冻结/不变性回执在provenance。保存表重新聚合证实最大43／23与0合格，所有85548位置分母闭合。tokenizer当前SHA与原始绑定一致。大权重SHA未重算，因为没有进入首次模型加载，不把它写成成功核验。

四条原始文本只是最强支持失败对象的事后解释性样本，非C/R案例；没有feature反例可分类，明确记未形成。无模型输出，故无结果图或bootstrap区间。运行CPU；GPU可用显存查询返回Insufficient Permissions，未据此推断可用显存，也未创建资源；本轮首先因数据门槛停止，未依赖GPU。

## 判断与收束

已经知道：这份数据在冻结筛选／去重／匹配下没有合格对象。尚不知道：C是否支持R、局部方向测量是否可靠、目标预测是否受特异干预影响。H1/H2/H3均未检验。没有理由将数据不足改写为“计算独立”或“字典失败”；本轮不另选数据、降低门槛或搜索更好看的对象。

科学机制接受和问题关闭仍Unknown。本次授权执行已达到其停止分支；如后续更改数据或门槛，需要作为新协议修订记录，不是本轮结果。本记录不给新的自动实验指令。
