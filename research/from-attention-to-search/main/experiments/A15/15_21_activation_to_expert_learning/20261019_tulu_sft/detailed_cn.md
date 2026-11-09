# Detailed：Tulu答案SFT复核

问题、模型、假设和认识更新见[Summary](summary_cn.md)。本记录保存执行事实与完整可追溯边界；不将工程完成作为科学认可。

## 1 执行与资格

任务pt-ihan2rw2；单次h100-4-reserved，shphd-lite-0911，既有runtime.sh，无新依赖下载。20/20完成，无训练失败或追加重跑；每模型504更新、256644有效答案目标。远程协调进程活动墙钟345.096秒，CPU统计与制图18.529秒；不冒称纯GPU kernel时间。

输出根目录：/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z。

数据身份：hf_hub_allenai_tulu_v2_sft_mixture，revision6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752；派生data_tulu_sft_route_20261019t012300z；表征representation_tulu_sft_route_20261019t012300z。模型model_qwen3_0p6b_base；字典crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013。训练输出实际状态及注册见[产物manifest](artifact_manifest.json)。

## 2 实际数据、监督与模型

原Tulu326154条，仅上游train；取首user→assistant对，规范化user问题hash去重并80/10/10隔离，hash排序取1024/128/256。prompt≤256token，答案含EOS8–256token，总长≤512，无答案截断；短输入过滤导致当前分布不能代表全Tulu。三份原始parquet新鲜hash和抽样JSON hash见[evidence/manifest.json](evidence/manifest.json)。不同来源既不等人数，也不等token权重，监督总量按有效答案token计。

prefix与answer分别用冻结Base tokenizer编码，首答案token对应prefix末端预测位置。全部缓存目标和位置已逐条CPU核对：85548/10340/22446全部匹配，无prompt/padding目标；每条终目标为EOS151643。首批native/cached核对623/509/911位置，logit/NLL最大差0。没有额外扰动未来token测试。

冻结Base/字典及原norm/head，只训练末层残差旁支。u=h/a，a=sqrt(mean_TRAIN||h||²/1024)，无中心化；h_out=h+a*g*E_k(u)。固定路由g=1；学习参考g为所选softmax概率。因旁支位于最后Transformer block之后且逐位置工作，缓存训练与此架构的teacher-forced答案监督对象相同；不等于完整模型SFT。

## 3 条件与预算

T/R11×S0/S1/S2/S3，外加Learned与LearnedLB，两个模型seed11/22。原T/R11为固定旧参考名单（T是log频率聚类），新TRAIN重新估计p,m,组均值及旁支尺度；字典原TRAIN normalization/threshold保持冻结。评分公式见[协议](protocol_cn.md)。原分母0与地板触发见[evidence/denominators.json](evidence/denominators.json)。所有组人数相同于父实验，R11只是一个固定随机名单，两个模型seed不等于两个随机分组。

每模型3epoch，共504更新；有效batch512，micro128，尾批44；同seed数据顺序和专家初始化配对。AdamW3e-4、(.9,.95)、eps1e-8、wd.01，前26步warmup，cosine至.1，clip1；学习router均衡λ=.01，仅LearnedLB。每64步latest，每epoch稳定保存完整model/optimizer/RNG/顺序/计数。原始steps与TensorBoard在执行目录training/条件/seed/中。

## 4 工程检查和偏差

零旁支误差0；专家down梯度非零，首次更新后router任务梯度非零；64位置拟合1.23079→0.00007083，恢复后下一更新严格一致。正式20条流的tokens/train_lm_loss、updates/train_lm_loss、train_total_loss、tokens_seen等实测finite且504条计数最终256644，非仅检查文件存在。

父实现复用common.py、train.py，适配读取本轮cache、训练N和epoch配置；重新实现问答抽样、answer-only提取与新TRAIN统计。未复用父DCLM实际输入，也未重跑父训练、target适配或谱分析。

冻结config保留若干未被新pipeline使用的旧stamp/deadline/priority字段；smoke旧估时字段仍硬编码父768步/65402 EVAL。它们不参与本轮调度和训练，已在[派生元数据解释](metadata_interpretation.json)中逐项说明；不改冻结原件。实际内部上限30分钟；504步中位计时.04660秒仅提供117秒四卡纯训练下界，不能当作全流程耗时。导航检查存在两个预存无关入口问题，本轮未修其他项目。

## 5 全部学习结果与比较

冻结基座整体1.242698，原参考低频宏1.218116。全部20模型终点见[完整表](tables/all_condition_results.csv)，全部原始曲线见[曲线表](tables/learning_curves.csv)。

|条件|模型seed|整体答案NLL|原参考低频宏NLL|TRAIN固定诊断NLL|
|---|---:|---:|---:|---:|
|T_S0|11|1.339095|1.342981|0.541431|
|T_S0|22|1.339539|1.339754|0.540920|
|T_S1|11|1.402563|1.400290|0.161427|
|T_S1|22|1.404536|1.397362|0.167953|
|R11_S1|11|1.421407|1.417152|0.163327|
|R11_S1|22|1.416413|1.400125|0.160197|
|Learned|11|1.282203|1.278311|0.738079|
|Learned|22|1.282382|1.278514|0.745359|
|LearnedLB|11|1.275709|1.276210|0.673958|
|LearnedLB|22|1.274871|1.272510|0.685536|

主比较已在Summary逐项列明。差值是同seed配对，负数有利于前者。全部1000次对话bootstrap、同名单各评分对S0、S3对S2、同评分T对R11及学习均衡参考均保留[配对表](tables/paired_comparisons.csv)。未以单个最好checkpoint代替第三轮终点。首轮部分整体改善属于全曲线直接观察，不是事后成功终点。

逐feature宏指标先在feature命中的预测位置平均NLL，再在可估feature间等权；一位置可命中多feature，不能当独立知识样本。964中960可估；无命中项保留NA。逐feature结果见[低频表](tables/low_feature_nll.csv)，不同频率变化见[频率对照](tables/frequency_shift.csv)。

## 6 实际分发与来源

原名单成员和新TRAIN p/m见[成员表](tables/group_members.csv)。完整q、命中计数与负载在执行目录metrics/exposure/{split}_{condition}.npz，其中N_e是接收位置数、counts[i,e]为共同命中数、q=counts/N_e，空专家为NA。逐feature接收是counts[i,owner]/feature总命中数，未命中为NA，命中但未到达为0。随机/频率名单都接收完整h，不能将分组原子的名单属性当实际输入纯度。

来源标签分解见[source_nll](tables/source_nll.csv)，对话均值见[dialogue_nll](tables/dialogue_nll.csv)。来源标签小样本不作强领域判断；没有对来源标签进行路由或监督学习。

## 7 图阅读

图1：主对照整体与原低频宏学习曲线；看早期下降及后期反弹，第三轮终点固定。

图2：学习router无/有均衡参考单独展示；参数另8192，所选概率乘数与固定路由不同，不当作严格同参数因果对照。

图3：左为实际token负载，右为原参考低频指定专家接收；分发改善不等于学习改善。

图4：来源标签上的整体NLL相对基座差值，柱为两个模型seed平均，正值更差；括号n是留出对话数，小样本来源明确显示。完整逐seed数值在表中，不将来源称为纯领域。

## 8 认识与下一决策

AI解释：本轮不能把数据更换视为充分修复；部分整体指标早期下降而终点恶化，与有限数据过度更新一致。尚未区分学习率、训练轮数、样本量、末层旁支与路由。Base预训练文本/格式暴露未知。旧DCLM与本轮SFT同时改变任务、mask和预算，不能直接跨任务比较绝对NLL，也不能唯一识别旧失败根因。

AI建议唯一下一验证：用DEV确定各臂统一训练预算，再在新的问题隔离留出上固定比较T_S0/T_S1/R11_S1。本轮完成即停止；没有执行该建议。研究者科学判断/下一决定Unknown。
