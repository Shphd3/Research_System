# 合并两批初始能力筛选

命令：`python analysis_orchestration/merge_behavior_screens.py --data 完整20000名单 --sources 首4096目录 剩15904目录 --out 新目录`。按相同mode分别调用；现在只实现和测试，未对真实输出运行。

核对两批ID无交叉、总集合恰好等于完整20000，每事实恰好train_question与eligibility_question两问。所有rank收据必须COMPLETE，rank范围/文件哈希/记录数一致；mode、模型路径、配置SHA、seed、完整解码配置和显式greedy参数一致。

允许cache_io整文件SHA因mask修改不同，但必须能找到原始版本快照，并逐函数AST核对student/teacher prompt不变；还逐条核实际prompt与原问题/原文的固定序列化契约。评分/生成helper和筛选脚本SHA仍需相同。输入来源、gold、问法、prompt变化会拒绝合并。

原始JSON记录逐行字节保留，按全名单+两问顺序输出；fact_scores也原样保留。没有重算、修正或优化任何评分，没有准确率解读。源文件/行号/哈希全部记录。只有缺行末换行时补一个换行，并明确计数。

新目录写outputs_rank000、fact_scores、summary、merge_receipt和row_provenance。rank000仅为select_cohorts兼容文件名；不生成GPU的receipt_rank收据。状态明确CPU_MERGE_NO_NEW_INFERENCE。原始文件、冻结plan/core不改，已有输出目录拒绝覆盖。

5项小合成测试通过：原字节/顺序、v3/v4提示函数等价、重复/缺问法、greedy/配置异常、未完成收据与教师prompt改动拒绝。正式CLI固定20000，不能用测试小样本冒充完整数据。
