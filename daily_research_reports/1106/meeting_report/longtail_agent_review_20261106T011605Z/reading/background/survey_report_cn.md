# 1105-长尾知识学习与蒸馏摸底：事实执行报告

**AI 建议：下一轮优先验证4B作为有真实原文监督的低成本教师候选；最终教师选择仍为Unknown。** 8B确实多答对部分闭卷知识，但证据任务只比4B多答对一道改写题；闭卷优势对提示变化的配对区间仍不稳定。本轮不能证明额外成本值得，也不能证明学生能通过蒸馏学会这些知识。

本轮完成40条事实、三模型，保留1200次测试回答及另外的运行诊断。没有训练、蒸馏、SAE重训、模型/数据集下载、软件包安装、其他任务改动或提交推送。界面重命名工具不可用；已按用户指定名称建立真正的本地research-memory记录。

## 模型、硬件与加载

三个主模型实际路径是`/data/share/Qwen3-0.6B`、`/data/share/Qwen3-4B`、`/data/share/Qwen3-8B`，均为原版后训练聊天/混合推理模型，非Base、非2507版。实际唯一参数量分别为596,049,920、4,022,468,096、8,190,735,360。全部同一tokenizer文件、BF16、原生聊天模板且关闭thinking；greedy、seed1105、batch8、max_new_tokens48。没有量化或CPU offload。配置支持的位置长度字段40960，tokenizer元数据131072、rope_scaling=null；没有验证131072上下文支持。

8B配置缓存revision为`b968826d9c46dd6066d109eabc6255188de91218`；0.6B为`c1899de289a04d12100db370d81485cdf75e47ca`。4B只有ModelScope master记录，确切commit为Unknown。已检查配置/tokenizer哈希、分片布局完整大小、header哈希和实际加载；没有重算全部模型权重哈希。0.6B文件重复存储输入嵌入/输出头，二者实际哈希一致；751,632,384个存储元素不能当作独立参数量。

物理GPU是H100 80GB，可见资源是60SM的MIG 3g.40gb，总40,448MiB；初查占用44MiB且无计算进程。所有模型逐进程顺序加载并释放。使用现有Python3.10.12、torch2.3.0a0 NVIDIA24.04、transformers4.53.3、safetensors0.5.3及SDPA。进程变量解决protobuf兼容问题，没有修改安装包。四条诊断问题在单条/批8、SDPA/eager以及已有torch2.8的隔离诊断中输出相同；这是局部实现检查，不是所有问题都经过独立后端验证。

## 数据、频率与评分

复用本地`/data/share/wikitext-2-v1/wikitext-2-v1.json`，36,718行、11,300,311字节。文件SHA256为`cbfbce6a8c4c30bf09661c7f7fd60cf2d31fa1a8940f036c3a78bcb691324d1b`。[官方WikiText说明](https://huggingface.co/datasets/Salesforce/wikitext/blob/main/README.md)将其来源描述为Wikipedia优质文章。本地副本的确切上游revision未核实；实际来源以本地固定字节、原文章标题、行号和字符范围为准。panel中的自动标题外链未核验，不作为来源证据。25篇段落带有预处理的`<unk>`，答案文字可见，不称为原始未处理文本。

从开头65个检测到的主标题中人工筛查40篇，每篇一条稳定事实；AI编写问题并回原文逐条核对，两种问法不增加事实样本数。它是便利样本，不是随机代表性样本；未用待测模型的答案作真值。先冻结样本和规则再测三个模型。初版720条回答保留。其后发现代词片段缺主语，另行冻结完整原段落的三模型修正（360条）；再保留一组事后冻结的简短闭卷提示检查（120条）。下表明确使用修正后的原段落条件；闭卷与移除条件沿用初版。不能把这些适应性修正说成事前注册。

频率是固定文件中大小写不敏感、词边界约束的**实体/关键词字符串提及代理**，包括标题和自身文章重复，无别名扩展和实体消歧。中位数9；较低组≤9共21条、范围2–9，较高组>9共19条、范围11–142。Tina、Devin、Atlanta、Route4等宽泛字符串有混淆风险。两组段落平均122.5/112.5空格词，问题9.67/9.21词，但年份题为13/21与4/19，未充分匹配。只能描述组内结果，不能推出事实频率效应、长尾效应或Qwen预训练曝光。

评分先做Unicode/大小写/标点归一化精确比对，再保留AI逐条语义复核。初版278条、补充137条非精确回答均有绑定输出哈希的复核记录；未使用待测模型打分。拒答、错误断言、格式/非回答分别标注，均不静默丢弃；当前无未决输出，无达到输出上限的回答。没有独立人类复核。

F34真菌科名题有分类体系差异：原文为Diplocystaceae，NCBI/EPPO为Astraeaceae。闭卷接受已核验的后一回答，证据题按显示原文评分；同时保留所有模型统一去除F34后的39条敏感性分析，没有改写冻结样本。简短提示的一条8B回答认出WASP但错误展开为Wide Area，答案实体获分，额外错误已单独标记，不能直接当作教师文本。

## 当前修正结果

所有主条件分母均为40个事实。

| Condition | 0.6B | 4B | 8B |
| --- | --- | --- | --- |
| Closed book / 闭卷 | 1/40 | 4/40 | 10/40 |
| Original paragraph / 给定原段落 | 35/40 | 40/40 | 40/40 |
| Closed paraphrase / 闭卷改写 | 1/40 | 4/40 | 11/40 |
| Paragraph paraphrase / 原段落改写 | 38/40 | 39/40 | 40/40 |
| Replaced paragraph / 替换证据 | 34/40 | 40/40 | 40/40 |
| Excerpt removed / 移除证据 | 12/40 | 40/40 | 40/40 |

完整原文与替换原文同时答对：0.6B为34/40，4B和8B均40/40。移除是删除整段后要求信息不足，属于明确缺证据检查，不代表能识别细微证据缺口。

## 两组的描述性结果

单元格顺序为较低代理组/较高代理组；分母21/19固定。

| Condition | 0.6B low / high | 4B low / high | 8B low / high |
| --- | --- | --- | --- |
| Closed book / 闭卷 | 0/21 / 1/19 | 2/21 / 2/19 | 2/21 / 8/19 |
| Original paragraph / 给定原段落 | 19/21 / 16/19 | 21/21 / 19/19 | 21/21 / 19/19 |
| Closed paraphrase / 闭卷改写 | 0/21 / 1/19 | 1/21 / 3/19 | 2/21 / 9/19 |
| Paragraph paraphrase / 原段落改写 | 20/21 / 18/19 | 21/21 / 18/19 | 21/21 / 19/19 |
| Replaced paragraph / 替换证据 | 18/21 / 16/19 | 21/21 / 19/19 | 21/21 / 19/19 |
| Excerpt removed / 移除证据 | 7/21 / 5/19 | 21/21 / 19/19 | 21/21 / 19/19 |

## 问法稳定性与配对不确定性

表中分别报告回答等价、两种问法都正确；稳定答错不算成功。

| Model | Closed: equivalent / both correct | Paragraph: equivalent / both correct |
| --- | --- | --- |
| Qwen3-0.6B | 13/40 ; 0/40 | 37/40 ; 35/40 |
| Qwen3-4B | 16/40 ; 3/40 | 39/40 ; 39/40 |
| Qwen3-8B | 25/40 ; 9/40 | 40/40 ; 40/40 |

| Condition | 8B − 4B percentage points | Paired bootstrap 95% |
| --- | --- | --- |
| closed | +15.0 | +2.5 / +27.5 |
| evidence | +0.0 | +0.0 / +0.0 |
| closed_paraphrase | +17.5 | +5.0 / +32.5 |
| evidence_paraphrase | +2.5 | +0.0 / +7.5 |
| replaced | +0.0 | +0.0 / +0.0 |
| removed | +0.0 | +0.0 / +0.0 |

区间采用20,000次事实级配对bootstrap，seed1105；各准确率的Wilson95%区间见英文报告。40/40的Wilson区间约91.2%–100%，完美配对的经验差值区间[0,0]不能证明总体等效。便利选择、相关主题、多个比较与事后修正均限制推断。

简短闭卷提示检查：

| Model | Neutral prompt correct |
| --- | --- |
| Qwen3-0.6B | 3/40 |
| Qwen3-4B | 7/40 |
| Qwen3-8B | 11/40 |

该条件8B−4B为+10个百分点，95%配对区间[-2.5,+25]。原提示闭卷+15个百分点、区间[+2.5,+27.5]；不能只挑有利提示宣布8B优势稳定。原问法、改写与简短提示均答对且4B原闭卷答错的8B额外案例包括F10/F15/F20/F23/F31。

## 事实级差距、成本与候选建议

给定完整原文，两教师均正确而0.6B错误的是F03、F08、F22、F25、F27；闭卷为F22、F32。完整段落改写时4B在F27把唱片公司RCA Records答成演唱者，8B正确。两教师闭卷也有大量错误，完整错误列表如下及supplement_analysis.json中保留。

| Model | Peak allocated GiB | Peak reserved GiB | Load s | 120 answers: generation s | Output tokens | Batched output tok/s |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3-0.6B | 1.58 | 1.71 | 9.45 | 3.040 | 634 | 208.5 |
| Qwen3-4B | 8.28 | 8.58 | 31.63 | 4.839 | 610 | 126.0 |
| Qwen3-8B | 16.07 | 16.43 | 59.83 | 5.286 | 524 | 99.1 |

上表是120次完整段落条件的实测，不含加载的同步生成时间；输出长度不同，不能视为固定生成长度的速度基准。4B/8B峰值已分配显存为8.28/16.07GiB，生成4.839/5.286秒，加载31.63/59.83秒。初版句子条件8B输出更短、总生成时间更少，不能据此宣称8B普遍更快。没有测训练算力或实际计费。

**AI建议**：若下一轮目标是从已核验真实资料生成监督，优先验证4B，保留8B作交叉核对；8B额外知识有事实支持，但当前没有证明其综合收益值得约两倍显存。若教师必须闭卷提供新知识，最终选择为暂不确定：两模型当前闭卷正确率都不足以直接产生未经核验的真值。所有学生差距只是蒸馏候选，不是可学性证据。

## 辅助baseline与SAE

原Qwen3-0.6B-Base父模型是`/data/250010109/model_cache/Qwen3-0.6B-Base-official`，与本轮后训练0.6B不同。两个原模型SAE均零基第27层、输入1024、字典30000、ReLU/Top32。MLP输入SAE：`/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt`，hook为MLP forward_pre_hook、post_attention_layernorm之后；原验证NMSE0.05338209、dead features0、reload差0。Attention输出SAE：`/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/sae_full_final.pt`，hook为self_attn.o_proj输出、残差相加前；原验证global NMSE0.16841863。这些是本轮重新读取的既有质量记录，不是新测重建质量，也不证明能直接用于后训练0.6B。

容易定位的较小baseline实际为Dense0.281B与普通MoE总0.508B，并非恰好0.2B/0.5B。Dense的33B-token状态位于`/data/250010109/MoE_Router/experiments/20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/milestones/token_033000000000`，无内嵌SAE。MoE为507,988,992总参数、281,496,576常规激活参数，状态位于`/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/runs/formal/milestones/token_033000000000`；匹配的独立router输入SAE位于`/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/runs/formal/sae_full_final.pt`，block7.norm2输出、1024→30000、Top32，原验证NMSE0.22674462。33B指训练tokens。相关S7的SAE属于另一独立训练模型，不是Dense的SAE。原生state.pt需配套源码/config加载，不能直接作为HF模型替换。详见auxiliary_assets.json与auxiliary_source_records.json；本轮未加载这些baseline或运行SAE。

## 可复查交付与未执行事项

完整40条原文/反事实全文、问题、两个问法和三模型逐字输出：cases.md（[包外资料 E001](../../EXTERNAL_REFERENCES.tsv)）。初版与修正的全部原始JSONL、freeze manifest、协议、代码、失败日志、复核记录、区间和按事实配对均在本目录；verification.json验证冻结字节、来源跨度、1200条覆盖、复核绑定和代码编译。测试模型进程已退出，资源释放；没有持续监控。导航检查原有4个untracked问题不由本任务修改。

尚未执行：蒸馏/训练、记忆架构设计、SAE分析、长尾机制因果判断、训练曝光估计、中文/长上下文/复杂多跳基准，以及最终科学选择。下一步需要研究者决定监督来源与任务，确认Base还是后训练学生及SAE对应关系，定义更可靠且匹配的频率参考、独立事实/来源划分、无蒸馏对照、目标与预算及保持/泛化/拒答评价，形成获批执行契约。本轮完成后等待用户决定是否进入蒸馏。

## 完整事实配对索引

- closed: {"both_teachers_correct_student_wrong": ["F22", "F32"], "teacher4_wrong": ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F20", "F21", "F23", "F24", "F25", "F26", "F27", "F28", "F29", "F30", "F31", "F33", "F35", "F36", "F37", "F38", "F39", "F40"], "teacher8_wrong": ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F11", "F12", "F13", "F14", "F16", "F18", "F21", "F24", "F25", "F27", "F28", "F29", "F30", "F33", "F34", "F35", "F36", "F37", "F38", "F39", "F40"], "only8_correct_vs4": ["F10", "F15", "F17", "F20", "F23", "F26", "F31"], "only4_correct_vs8": ["F34"]}
- evidence: {"both_teachers_correct_student_wrong": ["F03", "F08", "F22", "F25", "F27"], "teacher4_wrong": [], "teacher8_wrong": [], "only8_correct_vs4": [], "only4_correct_vs8": []}
- closed_paraphrase: {"both_teachers_correct_student_wrong": ["F19", "F22", "F32"], "teacher4_wrong": ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F20", "F21", "F23", "F24", "F25", "F26", "F27", "F28", "F29", "F30", "F31", "F33", "F34", "F35", "F36", "F37", "F38", "F39", "F40"], "teacher8_wrong": ["F01", "F02", "F04", "F05", "F06", "F07", "F08", "F09", "F11", "F12", "F13", "F14", "F16", "F17", "F18", "F21", "F24", "F25", "F27", "F29", "F30", "F33", "F34", "F35", "F36", "F37", "F38", "F39", "F40"], "only8_correct_vs4": ["F03", "F10", "F15", "F20", "F23", "F26", "F28", "F31"], "only4_correct_vs8": ["F18"]}
- evidence_paraphrase: {"both_teachers_correct_student_wrong": ["F22", "F25"], "teacher4_wrong": ["F27"], "teacher8_wrong": [], "only8_correct_vs4": ["F27"], "only4_correct_vs8": []}
- replaced: {"both_teachers_correct_student_wrong": ["F03", "F04", "F08", "F22", "F25", "F27"], "teacher4_wrong": [], "teacher8_wrong": [], "only8_correct_vs4": [], "only4_correct_vs8": []}
- removed: {"both_teachers_correct_student_wrong": ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F10", "F11", "F12", "F13", "F14", "F15", "F18", "F21", "F23", "F24", "F26", "F27", "F28", "F29", "F30", "F31", "F32", "F35", "F36", "F37", "F40"], "teacher4_wrong": [], "teacher8_wrong": [], "only8_correct_vs4": [], "only4_correct_vs8": []}
