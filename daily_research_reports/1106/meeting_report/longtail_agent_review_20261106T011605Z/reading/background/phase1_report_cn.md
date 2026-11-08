# 1105-知识学习任务与蒸馏基建：第一阶段报告

**第一阶段完成。Base可以在这批DEV资料上基本理解问答并使用原文；模型、SAE与CE/KL接口已经核查。完整知识训练基建尚未取得正式运行资格。** 新确认数据、别名/跨来源去重、正式曝光调度与全模型优化/恢复仍需补齐。以下任务设计是AI建议，未转成研究者确认的Anchor/Protocol，也未授权正式训练。

当前环境无对话界面重命名工具，未声称已改名。本对话继续使用原有research-memory日志的稳定路径，更新用户请求的名称为“1105-知识学习任务与蒸馏基建”，保留此前全部记录，不新建第二份对话日志。

## 实际资产与运行环境

| Role / 角色 | Actual local path | Type / 类型 | Layers / width | Config positions | Runtime evidence |
| --- | --- | --- | --- | --- | --- |
| Main student | /data/250010109/model_cache/Qwen3-0.6B-Base-official | Base | 28 / 1024 | 32768 | Loaded;200 generation +78 candidate comparisons +engineering probes |
| Ability control | /data/share/Qwen3-0.6B | Original post-trained | 28 / 1024 | 40960 | Prior survey reused; current metadata checked |
| Primary teacher candidate | /data/share/Qwen3-4B | Original post-trained | 36 / 2560 | 40960 | Prior survey and fresh real-logit forward |
| Optional teacher | /data/share/Qwen3-8B | Original post-trained | 36 / 4096 | 40960 | Prior survey reused; current metadata checked |
| Optional Base teacher | /data/share/Qwen3-4B-Base | Base | 36 / 2560 | 32768 | Header/config/tokenizer only; not forward tested |
| Optional Base teacher | /data/share/Qwen3-8B-Base | Base | 36 / 4096 | 32768 | Header/config/tokenizer only; not forward tested |

主学生596,049,920参数。实际Base权重SHA256为`cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`，本轮完整重算并与SAE历史父模型记录一致。4B/8B分别约4.022B/8.191B；本轮未重算这些大模型全部权重哈希，实际文件/header/config检查在asset_audit.json。Base教师确实存在，但当前只有资产检查，没有任务正确性或速度结论，不能只凭Base标签选教师。

GPU为H100 80GB上的MIG3g.40gb、60SM、40,448MiB，初查44MiB且无计算进程。驱动580.95.05，驱动显示CUDA13.0，实际torch运行时CUDA12.4。Python3.10.12、torch2.3 NVIDIA24.04、Transformers4.53.3、safetensors0.5.3、TensorBoard2.9.0可用；使用已有hf_transformers_qwen3层及进程内protobuf兼容变量，未安装软件。accelerate、peft、datasets在当前层缺失，LLaMA-Factory不能直接宣布可运行。教师与学生顺序加载，未打断其他任务、未提交远程任务。

模型配置的上下文长度Base为32768，后训练版为40960；tokenizer元数据长度不等于本轮验证过的长上下文能力。实际tokenizer为Qwen2TokenizerFast。六模型的完整151,669个token字符串→ID映射一致，输出头151,936维，另有267个未分配维度。KL检查统一掩码这些维度并重新归一化，同时检查实际答案续写token，而非只比较词表大小。原生Base EOS151643，后训练聊天结束EOS151645，不能将结束符位置直接纳入同一KL。

## SAE父模型和接口

| SAE | Exact hook | Dimensions | Historical NMSE | Fresh16-token sanity NMSE |
| --- | --- | --- | --- | --- |
| MLP input | model.layers[27].mlp forward_pre_hook, after post_attention_layernorm | 1024 →30000; ReLU/Top32 | 0.05338209 | 0.03471486 |
| Attention output | model.layers[27].self_attn.o_proj output, before residual addition | 1024 →30000; ReLU/Top32 | 0.16841863 | 0.20130238 |

两套权重分别为：

- `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt`
- `/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/sae_full_final.pt`

本轮实际用各自原生TopKSAE加载器，在正确Base的F10原文前16个token捕获接口；1024维输入、30000维字典、每token32个正特征、重建有限值均成立。表中的新NMSE是极小且无异常值过滤的接口检查，不是历史质量复现，也不作为两套SAE质量排名。没有将它们应用于后训练学生；该迁移仍未验证。

## Base资格检查：全部是开发资料

旧40条事实及此前看过的问法、反事实和教师输出全部标为DEV。提示试验只用F01/F08/F10/F32四事实，比较纯文本问答和两示例格式；两格式原文题均4/4，选取更少额外续写的纯文本格式，随后冻结规则。其余36条也只是非pilot DEV，不是盲测试。

Base提示是普通文本：闭卷为“Answer each question with one short answer.”加`Question: ...
Answer:`；原文条件使用完整段落加对应问题。greedy、seed1105、batch8、最多64个新token、Base EOS151643。解析仅取首个非空行并去可选Answer:/A:前缀；所有原始续写、token IDs、达到上限和边界标记均保留。后训练0.6B使用上轮原生聊天/非thinking提示及48-token上限；这不是格式严格相同的胜负比较。

| 条件 / Condition | Base：40 DEV | Base：36 nonpilot DEV | 后训练0.6B：旧40 DEV |
| --- | --- | --- | --- |
| 闭卷 / closed | 3/40 | 2/36 | 1/40 |
| 原段落 / evidence | 39/40 | 35/36 | 35/40 |
| 闭卷改写 / closed paraphrase | 4/40 | 3/36 | 1/40 |
| 段落改写 / evidence paraphrase | 40/40 | 36/36 | 38/40 |
| 替换证据 / replacement | 39/40 | 35/36 | 34/40 |

Base原问法闭卷25/40达到续写上限，28/40首行后继续输出；但39/40有可识别的答案行边界。3条为格式/非回答问题。原文三条件均无达到上限的回答，输出更稳定。主要失败是F27：把制作人Greg Kurstin答成录音歌手Kelly Clarkson；换问法后正确。由此可说当前DEV上的基本证据理解不是明显阻塞，不能据此证明知识能被训练学会。

固定四候选辅助评分，预先固定所有候选与计分方法；F34分类体系歧义统一排除，分母39。主分数为完整答案内容token的log-prob之和，均值另报：

| Condition | Sum-logprob primary | Per-token-mean secondary |
| --- | --- | --- |
| closed | 16/39 | 19/39 |
| evidence | 39/39 | 39/39 |

这衡量给定候选下的识别，不是自由生成；粗粒度干扰答案与长度偏差限制结论。不能挑19/39替代主16/39，更不能把16/39和后训练自由生成1/40直接比较。候选识别高于自由生成，进一步说明生成错误不等于预训练完全没见过知识。所有来源和人工语义复核记录均沿用可核查真值，没有用待测模型打分。

## 最小学习任务：闭卷内化，而非仅阅读

建议学生训练时只接收问题，不接收原文；答案来自已经核查的真实资料。教师可读原文后提供监督。训练后学生闭卷回答原问法和真正未训练过的等价问题。先测训练前状态，再测学习后状态；所有事实保留并分为预先已知、混合、未知，不能按模型错误挑出样本后声称预训练长尾。

必须分清两层划分：外层按实体/事实/资料家族区分方法开发与最终确认，内层在同一学习事实中区分训练问法与未训练问法。**最终确认事实会按约定被训练；它们独立于方法选择，测试问法独立于训练问法。** 完全未训练的新事实只用于额外迁移或污染参照，其错误不是“没学好已给知识”。

建议的资料规模是旧40条仅DEV，另准备64条方法选择事实、128条确认学习事实、32条零曝光参照。新资料均未构建，数量是目标而非已有合格样本数。除旧40篇外，保守禁止使用旧检索已触及的71个标题家族作为新确认资料。每条需保留来源固定版本/行与哈希、规范实体ID、事实关系与答案、训练问题、两条独立核查的未训练改写、教师输入输出与版本、原事实/增强父链、集合身份及实际曝光账本。反事实改写仅作诊断，不当作真实知识训练。

当前已经实现按显式source/entity/fact/augmentation-parent连通分量检查，160个DEV视图形成40组，故意跨池的改写被拒绝；别名归一化与跨资料同事实语义去重仍需补齐。不能把显式ID检查通过称为未来确认集无泄漏。

## 受控曝光与对照

为使单次运行总更新预算一致，建议128事实各半随机分配1次和8次监督；两个数据顺序seed中对调分配。每次运行总576条监督，global batch8对应72次更新。先进行高曝光组的7轮，再在最终轮混合两组，正式调度器需让匹配的低/高曝光事实末次监督位于同一有效batch，控制新近性。64条方法选择对应288条监督、36次更新。当前CPU夹具只验证曝光次数和组约束，正式新近性匹配调度尚未实现。

每个seed中CE与KD必须使用同样的事实、曝光、顺序、canonical答案、掩码、批量和更新数；有效答案token账本因此逐步一致。CE+KL仍只算一次事实监督。记录实际有效token数与输入token/padding/时间，不仅报steps。这里的1/8次是可控监督曝光，Qwen原预训练曝光仍Unknown。相互干扰和数据顺序属于模型训练过程，曝光组效果不是独立事实的无干扰因果效应。

| Arm / 对照 | Student input | Supervision | Matching / 边界 |
| --- | --- | --- | --- |
| Base before learning | Q only | No updates | Closed pretest on all learning facts; preserve known/mixed/unknown strata |
| Ordinary answer SFT | Same Q only | Canonical answer+Base EOS CE | Same facts,exposures,order,masks,batch,updates |
| 4B soft distillation | Same Q only | Same CE +lambda*T²*KL on content | Teacher sees original source+same train Q; held-out question forms never supplied |
| Post-trained0.6B ability control | Native recorded prompt | No training in minimal comparison | Independent ability reference, not the SAE parent |
| Optional8B / Base teacher | Same student input if later run | Same objective and schedule | Only after teacher task correctness and cost qualification; not forced now |

三个监督对象不同：教师闭卷回答是对其已有知识的调用；教师读原文生成是证据条件回答；token-KL是给定同一规范答案前缀后，对下一token分布的监督。后训练教师可以监督Base学生；前缀和EOS不同需要显式对齐，不是禁止条件。

若教师硬答案归一化后等于gold，那么它与普通答案CE的标签完全相同，不能将相同目标包装成独立蒸馏收益。最小有信息量的比较是CE与CE+KL。令CE位置包含答案内容及Base EOS，KL位置只含答案内容；教师条件为原文+训练问题+答案前缀，学生条件为训练问题+答案前缀；概率均在相同已定义token支持上归一化：

\[
L = L_{\mathrm{CE}} + \lambda T^2\,\operatorname{mean}_{t\in A_{\mathrm{content}}}\mathrm{KL}\!\left(p_T^{(T)}(\cdot\mid x,q,y_{<t})\;\|\;p_S^{(T)}(\cdot\mid q,y_{<t})ight).
\]

其中x是真实资料，q是同一训练问题，y是规范答案，T为温度、lambda为附加损失系数；KL按有效内容token取均值，教师分布detach。本轮测试实现掩码、相同分布零KL、真实4B→Base答案token匹配与梯度有限。建议初始T=2、lambda=0.5，尚待研究者选择；控制lambda=0可在实际可行时保留同一原始KL诊断及零加权tag。任何额外推理文字、问法或事实均增加数据，须有匹配数据对照，当前最小任务不加入。

正式候选参数：全模型Base微调、AdamW lr2e-5、betas(0.9,0.999)、weight_decay0、clip1、microbatch2×accum4=global8、FP32主权重/Adam状态＋BF16 autocast，学生最大128 tokens且超长拒收、不截断答案；短程常数学习率。全模型还是LoRA仍为研究者选择，不能由norm-only冒烟替代。有效预测token为主轴，TensorBoard按已有合同记录CE、KL raw/weighted、total、学习率、更新/数据位置/曝光账本，累计只在完整有效更新后推进。

## 实际工程冒烟与边界

本轮一次全模型CE反向涉及596,049,920参数，梯度norm有限，无全模型优化更新。真实4B读F10原文后，答案内容与Base使用同一token ID74623，T=2的KL为49.30525、Base最终norm梯度有限，没有执行KL参数更新。

参数更新测试仅针对原生最终RMSNorm的1024参数，AdamW lr1e-5，参考分支两步分别用F10/F32，监督token数2/4，累计6；独立进程恢复后重放第二步。因此共有3次实际更新操作、2个逻辑step，不能写成正式知识训练。第二步参数、Adam、scheduler、Python/NumPy/torch CPU/CUDA RNG、计数与数据位置逐项完全一致，loss均0.688321948；全部必要TensorBoard tags与坐标通过。峰值已分配显存约7.59GiB，包含此前全梯度检查，不能视为完整Adam训练峰值。

恢复了内存中的原始norm并退出；原始模型路径没有写操作，权重哈希在任务结束再核查。按精确清单清理两个临时step2文件，保留28,780字节的绑定父模型step1恢复凭据及全部JSON/TensorBoard/源码。该凭据不是完整微调模型，不能独立HF加载。已登记`dataset_knowledge_learning_dev40_20261105`与`checkpoint_knowledge_phase1_norm_smoke_20261105`，限定访问检查通过。完整模型、累积窗口中断与分布式恢复仍未验证。

## 基建状态与最小修复

| Component / 基建 | State | Evidence / gap |
| --- | --- | --- |
| Model/source assets | AVAILABLE / 已可用 | Exact official Base weight SHA matches historical SAE parent; all6 model headers/config/tokenizers accessible. |
| Base generation/scoring | AVAILABLE_DEV / DEV可用 | 4-fact pilot, frozen plain completion parser,200 retained generations and explicit review; post-trained comparison uses different prompt/length settings. |
| Candidate answer likelihood | AVAILABLE_AUX / 辅助可用 | 78 comparisons on39 facts; sum vs mean recorded; distractors coarse and not difficulty matched. |
| SAE loader/hook | AVAILABLE_BOUNDED / 有限可用 | Both native loaders and exact Base hooks finite and Top32 on16 tokens; post-trained SAE use NOT_QUALIFIED. |
| DEV lineage/group check | AVAILABLE_EXPLICIT_IDS / 显式ID可用 | 40 groups ×4 views all DEV; cross-pool paraphrase fixture rejected. |
| New confirmation data | NEEDS_PREPARATION / 需准备 | 64 method-selection +128 confirmation +32 unexposed facts are proposed, not created;71 inspected source families blocked. |
| Entity aliases/near duplicates | NEEDS_REPAIR / 需补齐 | Current exact-ID guard does not discover aliases, shared facts across articles or semantic near duplicates automatically. |
| CE / token KL / target mask | AVAILABLE_INTERFACE / 接口可用 | Real4B→Base logits, common answer token ID and KL backward tested; teacher gradients detached; EOS excluded from KL. |
| Training loop/exposure sampler | PARTIAL / 部分可用 | CPU exposure-count fixture exists; full72-update runner, recency matching, accumulation denominators and stop gates not implemented/qualified. |
| Optimizer/TensorBoard/counters | PASS_NORM_ONLY / 仅norm通过 | 1024 existing parameters,2 logical steps,6 valid prediction tokens; full-gradient-only probe had no optimizer update. |
| Checkpoint/restart | PASS_NORM_ONLY / 仅norm通过 | Separate-process exact norm/Adam/scheduler/RNG/counter/data-position replay; full-model/accumulation/distributed resume NOT_VERIFIED. |
| LLaMA-Factory runtime | SOURCE_ONLY / 仅源码参考 | accelerate/peft/datasets absent in active dependency layer; no installation; not advertised as directly runnable. |
| Formal SFT/distillation/forgetting | NOT_RUN / 未运行 | No formal training, remote job, SAE retraining or scientific mechanism conclusion. |

正式训练前的最小工程修复是：补新事实及两层划分/别名去重；实现并核对曝光调度、有效token加权累积及断点位置；准备并核验冻结教师cache；按完整Base+Adam+RNG+sampler+曝光账本保存恢复；对实际正式参数策略做短程、真实进程退出恢复的资格检查。已存在代码会按source_reuse_audit.json复用或适配，不能直接套用MoE架构或旧缺失RNG的adapter恢复。

## 预算与待决事项

确认学习比较建议2目标×2个对调曝光分配/顺序seed×72更新，共288次学生更新；方法选择另144次，额外超参数搜索另算。教师只为独立事实/训练问题生成一次cache并跨曝光/seed复用，但教师生成、校验、缓存I/O与KL额外开销都计入成本。若128事实每答案平均3个内容token，BF16全分布cache约111MiB，实际大小按token数算。FP32模型及Adam两份矩的完整恢复状态约6.66GiB/份，不含小型元数据；全优化器显存尚未实测。

数据准备好之后，初次端到端资格检查及小规模比较暂估1–3小时，小训练臂含评测为数分钟到数十分钟；这不是全模型吞吐实测，不能据norm-only耗时承诺正式ETA。新资料人工核验时间另计。8B/Base教师是额外候选，不强制多训练，也未启动远程资源。

进入正式阶段前需要研究者决定：是否采用这一闭卷学习任务；新事实规模、来源与确认集规则；全模型还是LoRA；4B原文条件soft-KL是否为主教师方案及lambda/T；受控1/8曝光分配与预算；是否后来增加共同遗忘阶段。若确认提升只出现在训练问法/输出格式，不能称为稳健知识获得；区间宽、教师真值不可靠、泄漏或预算不匹配时保留不足结论。没有SAE机制判断、共享参数方案或问题关闭。

## 可复查文件

`asset_audit.json`、`base_parent_identity.json`、`registered_input_access.json`；`base_eval_frozen.json`、`base_prompt_pilot.jsonl`、`base_dev_outputs.jsonl`、`base_manual_review.json`、`base_scores.jsonl`、`base_generation_summary.json`；`candidate_frozen.json`与`base_candidate_outputs.jsonl`；`dev_fact_records.jsonl`、`already_inspected_source_families.json`、`data_interface_checks.json`；`smoke_contract.json`、`smoke_reference.json`、`smoke_resumed.json`、`smoke_verification.json`、`smoke_cleanup_receipt.json`、小型step1 delta和两个TensorBoard目录；`source_reuse_audit.json`、`interfaces.py`、`task_proposal.json`。上一轮文件保持原字节，全部属于DEV。

第一阶段结束，等待用户决定是否进入正式训练。
