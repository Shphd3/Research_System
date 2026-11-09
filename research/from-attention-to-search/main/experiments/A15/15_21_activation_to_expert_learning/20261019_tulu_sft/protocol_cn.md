# Tulu 指令微调数据上的冻结表征专家学习复核

状态：APPROVED_FOR_BOUNDED_EXECUTION。2026-10-19 用户明确要求检查资产库、选择微调数据、开展实验并快速交付认识更新；授权覆盖本轮读取、派生数据、必要 smoke 与完整有限训练。继承原 Anchor 的学习问题，不改变 Focus 科学状态，不替研究者作机制裁决。

## 目的、假设与边界

检验此前“接收改善但留出学习失败”是否在指令回答微调设置下仍出现，并比较组级校准相对原评分与匹配随机组织的学习增量。候选解释是旧语料和监督任务与微调需求不匹配；竞争解释是冻结末层旁支本身、优化或有限样本泛化仍限制学习。换语料同时改为回答监督，不能唯一归因于数据、格式新颖性或预训练污染。Qwen3 Base 是否见过这些文本/格式 Unknown；CrossCoder 训练使用 DCLM 不证明 Base 完整预训练来源。

## 数据、划分和任务

选择已实际读取的 allenai/tulu-v2-sft-mixture 本地快照6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752。原数据326154条，字段dataset/id/messages；dataset是来源/任务标签，不是纯语义领域。使用每条首个user→assistant对，后续轮次不入本轮。先对user文本NFKC、压缩空白、SHA256去相同问题；相同问题不跨侧。固定种子20261019的hash桶80/10/10，桶内按hash排序，依次取合格TRAIN1024/DEV128/EVAL256条。prefix='### Instruction:\n'+user+'\n\n### Response:\n'，用原Base tokenizer分别编码prefix/answer，无新增词；答案末尾加原EOS。prefix≤256token，答案含EOS为8–256token，总长≤512。不截断合格答案。过滤及来源分布全部保存。

TRAIN有效答案目标85548，DEV10340，EVAL22446。右侧padding和全部prompt标签屏蔽；仅预测assistant答案token及EOS，每个预测位置t的标签严格为t+1。保留前文、答案此前token供因果预测；不把参考答案未来token送入路由。报告answer-token NLL和对话均值NLL，不把NLL当作生成准确率。DEV保留，不按EVAL或DEV选择评分、学习率或终点。本轮无超参搜索。

相同规范化问题已隔离；近重复、改写、Base预训练污染未知，不能称彻底独立泛化。原数据单一train拆出的本轮EVAL不是官方benchmark测试。

## 模型与对照

复用上一轮已检查的common.py/train.py：冻结同一Qwen3-0.6B Base及原final RMSNorm/词表头、冻结最终14选层/F16384 CrossCoder及其原TRAIN中心/尺度/阈值0.051281172782182693。在第28层完整residual-post之后、原final RMSNorm之前加8个1024→1024→1024无偏置SwiGLU专家，25165824参数，top1；原h完整输入，旁支h_out=h+a*g*E(h/a)，a仅从本轮TRAIN计算，输入不减均值。gate/up随机、down零。固定router g=1；学习参考g为所选softmax概率，router另8192参数。

保留原T/R11名单、原可靠9615、候选9605、Top10、L964/H962，避免换数据时同时重新分组。T是先前已冻结的log频率聚类名单，不冒称本轮线性等宽或语义分组；L仍称“原参考TRAIN低频feature”。本轮p_i/m_i/μ_e用新TRAIN答案预测位置重新估计并冻结；原字典推理规范不重估。

a_i=z_i Σ_l||D_li||，S0=组均a；S1=S0/本组TRAIN均S0；S2=组均a/m_i；S3=组均a/(p_i*m_i)。互不叠加，未激活0，分母仍名单人数。原分母0贡献0并单列；正分母下限为该类正中位数×10^-6，报告触发。并列/全零沿现有源身份+位置hash，种子20261019，保留全部输入。

8固定条件=T/R11×S0/S1/S2/S3，另Learned与LearnedLB(8 Σstopgrad(f_e)mean(P_e)，λ=.01)；每条件模型seed11/22，共20。原T_S1为主方案；主比较T_S1−T_S0、T_S1−R11_S1；其余扩展全部报告，不按结果挑最好者。固定臂不加均衡项，不丢溢出token。

## 训练、检查与停止

所有条件3epoch，256644有效答案位置，504更新；全局batch512，micro128，尾批44。相同seed的初始化与PCG64每epoch不放回顺序配对。AdamW lr3e-4、betas(.9,.95)、eps1e-8、wd.01；有效位置轴5%warmup(26步，取整后13312位置)，cosine到.1倍，clip1。epoch0/1/2/3原始曲线全保留，终点固定epoch3。checkpoint保存权重/优化器/RNG/顺序/游标/真实位置数；TensorBoard继承系统要求，不降低遥测。

单次h100-4-reserved，shphd-lite-0911，既有runtime.sh；GPU allocated≤32GiB/卡、aggregate RSS≤256GiB、新增磁盘≤64GiB；活动计算≤30分钟，墙钟目标≤90分钟，超限保存PARTIAL。首先同一任务内提取严格对齐h/z/labels，进行native/cached头数值检查、零旁支等价、梯度、64位置拟合、恢复下一更新一致、遥测和10步吞吐 smoke；失败阻塞正式训练。四卡用于独立条件并行，不改变全局batch。已有20模型、target和谱保留；本轮不重复旧实验、不新增目标适配或谱工程。不commit/push。

## 测量、判读与交付

每模型epoch0/1/2/3报告全EVAL NLL、原L逐feature宏NLL/位置均值及支持量、H宏NLL、固定TRAIN诊断；最终按来源标签报告NLL并注明混合/小样本。无命中feature记NA、不填0；额外列EVAL支持≥5的描述，不改主集合。统计新TRAIN/EVAL实际负载、目标接收及q_i,e和零接收/零暴露。对话为重采样单位，1000次配对bootstrap，seed20261019；只作本设置描述区间。

事前实用门槛沿原实验：两个seed的T_S1相对T_S0及R11_S1均改善低频宏NLL≥.01，整体恶化≤.01；还需明确是否优于冻结基座。若SFT的留出下降，则排除“这个旁支在所有此类任务上均无法学习”；不能证明旧失败仅由DCLM导致。若仍全部差，则不支持仅换SFT足够，不能宣布所有微调无效。接收与学习单独判读，失败和不足如实保存。

交付summary/detailed中英记录、完整结果表、学习曲线/接收/来源图、输入与实际checkpoint资产注册、smoke与执行回执。科学结论与下一决策由研究者确认，本轮完成即停止。

## 公开审计

A问题：复核有限设置，非从头预训练容量。B数据：原始文件hash、问题隔离、语义领域与来源区分，污染未知。C监督：answer-only shift与EOS明确。D模型：原末层残差旁支全量复用，h/z同次提取。E优化：各臂同预算、无EVAL挑选。F对照：配对T/R、S0/S1、冻结基座；数据和mask同时变化的解释边界保留。G执行：仅一次既有4H100Reserved配置，内部smoke先于正式更新，输出独立保存。用户本次显式授权覆盖执行；具体抽样与小规模复核数量由AI作为执行选择在训练前冻结，不声称研究者逐项审定。
