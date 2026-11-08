# 配套评测计划与统计映射

工具只写任务计划、读取基础设施元数据。没有模型库导入、GPU执行或成绩分析。正式超参数冻结文件和缓存名单必须先存在，不用默认谱系数代替DEV选择。当前精确锁定source v4；生成greedy文件仍与v3逐字节相同。

`build_evaluation_plan.py`支持指定的--freeze、--scale、--cohort-data、--eval-data、--cache、--lm-cache、--diag-data、--stage、--out。相对路径均按本执行根目录解释。必须是两个seed1105/1106、完整六训练臂；支持2048起至20000的偶数共同规模，优先2048、8192后再整套扩量。命令和字段见英文README。

每规模预评测只产生4个物理任务：全量生成、AB缓存概率、通用LM、独立固定子集基线。A后36任务。B后76任务：36个常规任务，加五个memory臂×两个seed×active/off/仅错配K/仅错配V四状态。active子集不能用全AB成绩替代，因为batch形状不同。所有生成统一batch64、最多32新token、三种问法及v3显式greedy。全AB在A后和B后均全部评测，包括尚未训练的B。

AB缓存概率/诊断使用--without-teacher避免教师I/O，LM也无教师。没有sentinel缓存，因此sentinel只测生成，NLL如实为未执行。所有数据按冻结ID、原文、问题、答案和来源/实体家族核对；诊断64A+64B+64sentinel必须预先指定，不按成绩选。工具写独立元数据视图，把sentinel的candidate/空标签改为zero_exposure_reference并保留旧值，原文件不改；不把零曝光对照当成教师已知。

计划适配现有run_parallel，实际收据约定batch_logs/<scale>_<stage>/<name>.json。生成器不会调用执行器。训练checkpoint路径仍为runs/<scale>/seed<seed>/<arm>/A或B/checkpoints/final.pt。

`build_stats_mapping.py --plans pre.json after_A.json after_B.json --out 映射.json`要求真实执行收据到齐。只读收据、checkpoint侧车manifest、计划曝光、冻结文件和缓存元数据，不打开预测、逐事实评分、metrics、日志或训练loss内容。真实greedy配置、记录数、argv、计划哈希、缓存/数据和checkpoint身份不符时停止生成映射。

B父哈希只取真实batch_logs/<scale>_train_B/<scale>_seed<seed>_<arm>_B.json的input_checkpoints['--continue-from']，核对实际argv及已评测A manifest；没有就报缺证，绝不造哈希。stats v2随后还会哈希当前父checkpoint字节。

主映射78个虚拟运行条目：基线物理结果复用于两个训练seed的配额标签，另外72个阶段/评测类型条目。它们不是独立的多次基线测量。teacher_mode统一mixed后由原始行分组；cohort为student_not_both_correct。全量生成、AB答案概率、通用LM各自严格使用完整名单。诊断另存companion映射42条及70个显式配对，避免把重叠子集加进主分母。主/诊断统计分别调用analysis_tools/v2/aggregate_facts.py，生成器不会运行统计。

CPU测试使用明确标注的假数据和假收据。原始成绩文件特意放不可解析文本，验证映射生成器没有读取它们。任何SYNTHETIC_SMOKE产物都不能引用为模型实验结果。


v4资格额外要求formal freeze明确source_manifest、source_manifest_sha256、source_sha256完整映射、gpu_qualification_path。源码manifest精确SHA为e8d77b70e9c5e7530f9e77aae867e97dbb3f427f63eb131787ff2865fdf3504c，逐文件核验，不自动信任latest。GPU资格引用只记路径/哈希，不解析loss数值。

正式AB缓存必须是semantic_content_v4完整mask policy与新prepare源码。只把逐token解码后纯空白的前导token移进已知前缀，含内容的合并token保留；完整输入ID不变、空语义答案拒绝、EOS排除。正式AB拒绝DEV CPU-derived缓存；派生DEV有独立父layout/stage/deepverify/copy/fullIDs收据核验，inference_executed明确false，不能冒称重新GPU推理。正式缓存完成由student/teacher绑定新layout的CUDA rank收据核对。

LM是原文next-token：只排首token，其余空白也预测，不要求QA mask、不做semantic裁剪。AB缓存概率必须按v4重算，旧mask DEV训练不能定正式超参数。原source3 provisional工具和测试保存在history_provisional_v3，原假smoke也保留；当前smoke另用SYNTHETIC_SMOKE_V4。所有这些都不是模型结果。
