# 图册：频率优先分发的量、现象与边界

本轮共19幅实测／示意图，每幅都有PNG、SVG、PDF。A是示意图；B为七策略各两页；C为数量、目标和全频率画像三个页面；D单列关系增量。P未运行，没有伪造图E。样本是EVAL 65,402有效位置、64个1024-token切块上下文，原低频964项。正式统计仍以完整窗口和表为准，184张文本卡只是固定规则抽样。

[一页结论](summary_cn.md) · [完整定义和结果](detailed_cn.md) · [文本卡](text_cases_cn.md) · [源图清单](provenance/canonical_payload_manifest.json)

## 先把几个对象分清

- feature ID：固定CrossCoder字典编号，不是已确认的知识名称。8个expert编号只是路由选项，本轮没有训练专家。
- p：原TRAIN全局激活频率；q：EVAL进入这个专家的位置中feature出现的比例；n：该专家实际收到且feature命中的位置数；N_e：该专家总输入数。p/q在B页均写百分比。
- LISTED OWNER（名单负责）：feature指定给该专家。CO-ARRIVING（伴随进入）：它随完整输入进入这里，但不是该专家名单负责项。不是从输入里拆feature分送。
- T10：可靠池内TRAIN最高频的10个ID；C是原962项高频名单，二者不同。主图隐藏T10只为看清其他项，输入和旁图q仍保留。
- F：全部可靠项log频率K-means；T：排除T10再按同法分；Tphi即Tφ：保人数且频率容差内用共现边交换；R11/22/33：相同候选及T组人数的随机名单；O：原线性组。P为缺资产未运行的联合第一方向旁支。
- NA：分母不足导致不可估，不是0。∞：专家有输入、头部项出现，但该目标没有收到，不能用大平滑数隐藏。
- 图名B与指标B不同：图B是专家／文本图；指标B是头部相对目标的平均正log10频率优势。B≤1、≤2只是固定描述点，不是学习成功门槛。

## 图A：对照流程

![对照流程](figures/figureA_comparison_map.png)

量：这是操作示意，不是测量结果。观察：原h/z、候选名单、评分、实际完整输入四个对象分开，O→F、F→T、T→Tφ分别对应三个不同改变，P单独标缺H。边界：箭头不代表已识别因果机制或学习收益。来源为原Protocol、`design_freeze.json`和执行侧`branch_assets.json`。

## 图B：专家→实际feature→文本位置

每策略两页，每页四专家。每列最多6项：非T10最高p两项、最低p且支持n≥5两项、负责L里支持最大的两项；去重不补位，最终按p降序。每项从EVAL真实接收且命中位置随机取1例，固定种子20261019，优先不同上下文。完整列表不是6项：全部286,341条策略／专家／实际feature记录保存在执行侧`metrics/visual/all_actual_feature_lists.csv`，本图只选显示。

文本为逐token解码数组：前2｜当前｜后2。引号内前导空格也是内容；`\n`为换行转义，数组逗号表示token边界，不是把一段句子随意截词。逐token解码遇多字节片段可有替代字符；原始token ID、ByteLevel原片段与完整前文保留在执行侧`texts/dispatch_text_cases.json`。原片段中的`\u0120`对应ByteLevel的Ġ空格标记，不代表文本里真的出现这些六个字符。后2token只作事后说明，不参与路由；没有跨文件或缓存窗口拼接，原文档边界未知。

**每页底部T10小条的左→右固定ID顺序为：13964、516、8060、10807、7388、5147、5913、7415、8345、13830。** 数字是该专家中该feature的实际q（%），不是ID；无输入专家写NA。颜色固定0–100%。ID与p的完整对应见[tables/T10.json](tables/T10.json)。

|策略／图页|画的量与观察|能／不能推出|
|---|---|---|
|[O，专家0–3](figures/figureB_O_experts_0_3.png)（[SVG](figures/figureB_O_experts_0_3.svg)／[PDF](figures/figureB_O_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；0／1／2完全空，专家3收到64位置|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[O，专家4–7](figures/figureB_O_experts_4_7.png)（[SVG](figures/figureB_O_experts_4_7.svg)／[PDF](figures/figureB_O_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；专家4／5／6／7分别收到97／184／6,934／58,123位置|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[F，专家0–3](figures/figureB_F_experts_0_3.png)（[SVG](figures/figureB_F_experts_0_3.svg)／[PDF](figures/figureB_F_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；只有专家7有65,402位置，其他七列为空|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[F，专家4–7](figures/figureB_F_experts_4_7.png)（[SVG](figures/figureB_F_experts_4_7.svg)／[PDF](figures/figureB_F_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；只有专家7有65,402位置，其他七列为空|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[T，专家0–3](figures/figureB_T_experts_0_3.png)（[SVG](figures/figureB_T_experts_0_3.svg)／[PDF](figures/figureB_T_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；专家0只有1位置、专家7有65,401；其余六列为空，专家0的q=100%只能解释这1次命中|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[T，专家4–7](figures/figureB_T_experts_4_7.png)（[SVG](figures/figureB_T_experts_4_7.svg)／[PDF](figures/figureB_T_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；专家0只有1位置、专家7有65,401；其余六列为空，专家0的q=100%只能解释这1次命中|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[Tphi，专家0–3](figures/figureB_Tphi_experts_0_3.png)（[SVG](figures/figureB_Tphi_experts_0_3.svg)／[PDF](figures/figureB_Tphi_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；与T实际输入完全相同，负责名单标签可以不同；空列保留|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[Tphi，专家4–7](figures/figureB_Tphi_experts_4_7.png)（[SVG](figures/figureB_Tphi_experts_4_7.svg)／[PDF](figures/figureB_Tphi_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；与T实际输入完全相同，负责名单标签可以不同；空列保留|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[R11，专家0–3](figures/figureB_R11_experts_0_3.png)（[SVG](figures/figureB_R11_experts_0_3.svg)／[PDF](figures/figureB_R11_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；全部八专家非空，展示实际目标与伴随成员，不能把随机专家号对齐成频率语义|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[R11，专家4–7](figures/figureB_R11_experts_4_7.png)（[SVG](figures/figureB_R11_experts_4_7.svg)／[PDF](figures/figureB_R11_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；全部八专家非空，展示实际目标与伴随成员，不能把随机专家号对齐成频率语义|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[R22，专家0–3](figures/figureB_R22_experts_0_3.png)（[SVG](figures/figureB_R22_experts_0_3.svg)／[PDF](figures/figureB_R22_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；全部八专家非空，展示三类固定挑选项与随机实际位置|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[R22，专家4–7](figures/figureB_R22_experts_4_7.png)（[SVG](figures/figureB_R22_experts_4_7.svg)／[PDF](figures/figureB_R22_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；全部八专家非空，展示三类固定挑选项与随机实际位置|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[R33，专家0–3](figures/figureB_R33_experts_0_3.png)（[SVG](figures/figureB_R33_experts_0_3.svg)／[PDF](figures/figureB_R33_experts_0_3.pdf)）|p、q、n、完整输入专家及token位置；全部八专家非空；与另两随机组是名单敏感性参考，不是学习复现|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|
|[R33，专家4–7](figures/figureB_R33_experts_4_7.png)（[SVG](figures/figureB_R33_experts_4_7.svg)／[PDF](figures/figureB_R33_experts_4_7.pdf)）|p、q、n、完整输入专家及token位置；全部八专家非空；与另两随机组是名单敏感性参考，不是学习复现|可检查名单与实际去向是否一致；抽样卡不是全部频率分布，也不是单义语义标签或功能证据。|

![T的真实稀疏接收](figures/figureB_T_experts_0_3.png)

图B源：执行侧`metrics/visual/selected_text_index.csv`、`texts/dispatch_text_cases.json`、`counts_eval_<策略>.npz`。显示修复只让token文字可读、避免误读舍入，184个选择和全部统计未改变。所有样例的route／feature命中／支持／当前及下一token／边界已核查。

## 图C1：量纲分开的数量

![实际数量](figures/figureC1_actual_counts.png)

量：左上为各专家输入比例（%），右上／左下为实际见过的可靠feature种类数（支持≥1／≥5），右下为实际见过的L种类数≥1。观察：F完全集中，T/Tφ的e0仅0.0015%、e7为99.9985%，随机组非空且覆盖种类多。边界：种类数依赖输入量，不是模型容量；同号专家也没有跨策略天然功能对应。完整N_e、低频≥5版与上下文数见[expert_metrics.csv](tables/expert_metrics.csv)。源表为执行侧`metrics/visual/figureC_counts.csv`和core专家表，图注四位小数不能代替原始整数。

## 图C2：接收和头部差距分开

![低频接收和B](figures/figureC2_low_target_outcomes.png)

量：左上低频零接收比例；右上每目标接收率的中位数／四分位和1.5IQR须（不绘外点），橙菱形是等权均值；左下B≤1／2占固定964项比例；右下finite／∞／NA项数。观察：F/T/Tφ仍大量零接收，随机接收增多但B差距仍大。边界：不丢零项或NA；T四个有限B=0只来自一个输入，不能从有限均值0推出普遍同频。B列描述点不是训练通过线。源为[低频逐项表](tables/low_target_metrics.csv)和[各策略汇总](tables/core_summary.json)。

## 图C3：全部可靠项的实际q画像

![完整q画像](figures/figureC3_all_feature_q_profiles.png)

量：每策略8行专家，横轴9,615个可靠ID按原TRAIN p从高到低排列，含T10；颜色为q比例0–1，白色NA、黑色接近0。观察：T和Tφ整幅实际q相同，头部随完整输入进入，主图不显示它们不等于输入去除了它们。边界：横轴相邻只代表排序近，不代表语义近；整幅不能替代逐目标负责接收。全矩阵是执行侧`counts_eval_<策略>.npz`，summary在`metrics/visual/actual_frequency_profile_summary.csv`，颜色范围在全部策略间一致。

## 图D：关系构造与分发的增量

![关系增量](figures/figureD_relation_increment.png)

量：上排分别是名单log频率平方离散D和固定TRAIN图的组内归一化无向边权；下排是EVAL低频宏平均接收率与固定964分母的B比例。紫色带是三套随机名单范围，非置信区间。观察：489次交换、175最终改组，关系目标提高，接收／B描述比例却未改善；右下T/Tφ仍是相同4项贡献。边界：上排是被优化的构造目标，不能当独立成功证据；该阴性增量不否定其他图、算法或评分的潜力。源为执行侧`metrics/visual/figureD_construction_and_dispatch.csv`、[关系汇总](tables/relation_summary.json)和固定边表。

## 没有图E的原因

P缺同位置原预处理十四层联合H。末层hidden和zD不能代替，未运行投影／重编码／误差，所以不画假结果；具体查找范围和最小缺项见[Detailed第11节](detailed_cn.md)。

图册实际文件与源表／脚本／hash在[payload manifest](provenance/canonical_payload_manifest.json)及执行侧`provenance/figures_manifest.json`。每幅图已分工逐张查看；需要修的token展示、极小负载舍入与图例位置在不改结果的前提下修正，视觉检查与数值检查分别记录。
