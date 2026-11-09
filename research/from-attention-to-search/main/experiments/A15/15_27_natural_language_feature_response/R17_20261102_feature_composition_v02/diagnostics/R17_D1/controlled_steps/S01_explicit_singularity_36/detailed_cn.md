# 第一步详细记录与核验

本记录只覆盖S01，不改R17 D1旧结论，不开启第二步。[小结](summary_cn.md) · [全家族](casebook_cn.md) · [正确／错误例](examples_cn.md)。

## 资产和复用

只加载D1同一官方Base模型与tokenizer，路径/data/250010109/model_cache/Qwen3-0.6B-Base-official。模型配置、tokenizer、模型权重SHA均与原D1输入指纹相同，actual receipt见[evidence/completed.json](evidence/completed.json)。复用D1原生backbone+LM head完整候选计分方法，独立实现3候选批次，不导入会加载字典的Capture。没有旧数据／分数拼接，没有模型／SAE／CC训练。CPU，零GPU新作业。

## 文本与三个标签

全部12模板及36条在[data/panel.jsonl](data/panel.jsonl)。每家族相同对象A和主句，仅square/singular square/invertible square性质短语差异；invertible前a/an作必要语法改变。初稿12处“a invertible”不合语法，响应前已修，初稿保留于执行侧versions/pre_response_article_fix。修复没有改变语义标签、问法或模型。其他36行核查未见语义歧义；[逐条审计](evidence/data_audit.json)记录检查。

全部是方阵；奇异性未知／是／否分别来自：未给性质、显式奇异、显式可逆。三行是独立描述，不是把同一固定A同时断言为奇异和可逆。旧D1多数描述要求从证书推断，不能替代本步直接属性词测试。

## 问题、分数与数值实现

F1使用用户原句，F2提前固定等义问法及逆向选项顺序，字节全文见[data/formats.json](data/formats.json)。每条完整prefix和候选实际拼接的token也已冻结于[data/prompts_tokenized.jsonl](data/prompts_tokenized.jsonl)。不使用chat模板、BOS或EOS，所有候选句号均评分；前缀token边界逐候选一致，无截断，最大输入49token≤192。

物理4×192：前三槽分别为三候选，第四槽重复第一槽作为数值检查；不是第四个问题。输入各自attentionmask，原生模型无hooks、不保存中间表征，只取候选后续位置的LM词表logsoftmax并查目标token，相加得总分。FP32前向/logsoftmax、FP64求和。最长候选长度不同，主指标不变，不拿中性分数或平均token分数重新排序。tie按冻结顺序并在原始记录显式列出。

## 有界修复与执行

首次加载前遇到已安装protobuf与旧生成文件不兼容，在尚无模型响应时设置PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python，与D1既有环境一致。失败日志和首次启动回执保留；无安装、权重／文本／提示修改。第二次运行完成全部74prefix＝72矩阵任务+2neutral，222完整候选。耗时255.3秒；模型更新、字典加载、feature hooks、probe拟合均0。并未遍历prompt。

## 三项审计与复算

1. 识别审计：目标是明确属性下的原生候选判断，不是复杂推理或feature机制；第一步范围和停止点由本次用户直接指定。
2. 数据审计：12匹配家族、每类12，标签与冠词修改在响应前冻结；两个格式是同一批文本配对，不是独立72家族；中性prefix不计准确率，无训练／开发选择。
3. 实现审计：冻结模型和输入SHA、全部74prefix、222候选token边界／逐token求和、首选argmax／正确性独立复算通过；重复槽最大分数误差0。无feature hooks或学习参数。

[evidence/verification.json](evidence/verification.json)是数值与范围回执。原生分数是规定候选内的相对序列偏好；没有通过自由生成验证回答合规。格式和先验诊断的证据不作语义机制归因。

## 载荷位置与结束状态

本次用户明确要求数据、脚本、原始分数位于项目合适新目录，因此这里附小型审核载荷副本，来源和SHA在[payload_manifest.json](payload_manifest.json)。实际执行源码／原始文件owner为/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S01_explicit_singularity_36；此处code/data/results是准确生成副本，避免形成两个可编辑源码。修改执行侧后须重新核验生成副本，不直接改原始分数。权重不复制。

状态：COMPLETED_STEP1_STOP_FOR_JOINT_REVIEW。下一步NOT_RUN。未提交、推送、外部发布；没有改变任何Focus或Anchor科学接受状态。
