# A17_01：受控列表规则与共享学习

[English](17_01_controlled_list_prediction_rules_anchor.md) · [A17](../README_cn.md)

问题标识 `list_rule_shared_update`，经批准迁移后保留身份。研究者确认首末、Qwen3-0.6B tokenizer、答案损失和两类未见。2026-10-10研究者采纳末层Attention `o_proj`直接矩阵为主、rank8 LoRA为容量对照，授权E03 Smoke→4卡H100 reserved Full、独立频率实验及匹配原始输出SAE训练/分析，并要求监督至终点。共识内具体实现设置委托AI；机制判断仍 Unknown。

`task_state=E03_NATIVE_FULL_COMPLETE_SAE_PENDING`；`question_state=HUMAN_CONFIRMED`；`design_state=DIRECT_PROJECTION_ADOPTED_EXACT_SETTINGS_DELEGATED`；`result_state=DESCRIPTIVE_NATIVE_EFFECTS_RECORDED`。

## 1. Problem Definition

同一共享模型状态下，有效学习列表首项规则会帮助还是损害末项预测，反向如何？上位目的为有限资源下理解有益/有害共享学习。控制内容、答案边际，可以改变显式条件规则。

首末列表相同、指令不同，完整前文不同，标签可同时满足。任务不同不自动需要专家。独立A17_02频率问题比较呈现策略；SAE已获授权，用于解释/干预观测到的原生作用，不要求它一定成为成功代理。数据/工程失败要求修复载体，不反证共享。

## 2. Physical Priors

研究者直觉：两规则可能复用读列表，但需不同位置选择；功能复用未验证。三词互异且指令可见，足够表达能力的条件预测器可同时满足两任务。当前误差、位置偏好和更新大小可能改变共享更新后果。

基础处理加有效条件性修正属于候选功能分解，更后面才是候选架构。一条样本可同时需要两者；正交或共同激活不能识别功能。只开放末层也不能盘点上游已完成的共同功能。

## 3. Falsifiable Hypotheses

有效首项更新可能增加独立末项损失，反之亦然。竞争解释是学习列表解析/答案词表使双方受益。位置难度和过大步长也与内在冲突解释竞争。

保留来源×接收规则四格及不更新参照。有效来源加真实有限接收损失定义局部帮助/伤害，梯度重合为次级。AI频率扩展问增加A后B的后果是否随同/异规则变化；正交互可能只是帮助较少，不能称净伤害。Smoke验证实现，不裁决科学复现。

## 4. Mathematical Model

有序列表 L=(w_1,w_2,w_3)，可见规则 r为首末，前文 x=T(r,L)止于答案标记。正确词合法出现在列表候选，标记后无已填答案。

\[
f_{\mathrm{FIRST}}(L)=w_1,\qquad f_{\mathrm{LAST}}(L)=w_3.
\]

合格续写 y为一个词元；全词表答案损失 \(\ell_\theta(x,y)=-\log p_\theta(y\mid x)\)，单位nat/答案，其他标签忽略。同一状态θ，来源s产生θ'_s，独立接收者记录D_r定义

\[
\Delta_{s\to r}=\overline\ell_{D_r}(\theta'_s)-\overline\ell_{D_r}(\theta).
\]

负值帮助、正值伤害。E01冻结一次普通SGD虚拟更新，不改训练优化器；E02校准受限实现；E03在早期及终点冻结有效矩阵更新，同一实际扰动分别由FP32/BF16读出，区分有限局部作用与训练轨迹。

末层无bias投影输入a、输出h，上游冻结时，真实有效ΔW精确给出Δh=ΔW a。原生损失导数e_h给出一阶e_hᵀΔh；余项由真实有限损失定义。既有局部模型不作为新经验发现。候选频率观测为B200终点，比较A800与A200下的“异−同”损失差；预算分配另估计。SAE保留重构残余和实际hook，不能代替原生损失。

## 5. Computational Realization

确认载体为本地Qwen tokenizer、20个不同中文单词元续写、首末配对显式规则、答案全词表CE。E01训练4,000/dev800/test800行。列表候选可含正确词，已填答案不输入；结构均衡不作为自然文本证据。

两类预先构造的未见面板相对于注册训练集成员关系；每个检查点另核验实际呈现过的内容组，不能把未被抽到的组称为已见内容。原面板与全800汇总保留，真实曝光分类仅为资格后处理，不更换主指标。顺序未见定义为：顺序未见保留已见无序内容，仅隐藏顺序；组合未见隐藏整组。dev/test列表及新组合组互斥。规则×类型分开及加权合并，保留组依赖。除采纳的确认契约许可，模型test入口关闭。

E01短适配全LMDense/Qwen，S7仅测初始；架构/历史不同，S7 sidecar不建立SAE分析或随机初始化习得。

**已采纳受限学习器：**原始Qwen Base，只开放layer27 Attention `o_proj`，其他权重全冻结。直接1024×2048有2,097,152参数；共享rank8 LoRA有24,576因子且累计变化rank≤8。二者不等价，同LR不匹配实际位移。[E03 Protocol](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/protocol_cn.md)冻结三seed、100次均衡更新、全dev探针及仅终点打开test。受限范围定位更新，不保证只学格式或更慢饱和；E01/E02契约保留历史。

**独立频率与匹配观察器：**[A17_02 Anchor](../17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor_cn.md)及其[Protocol](../../../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/protocol_cn.md)拥有固定池呈现次数加练及独立分配比较，不继承本Anchor的局部估计量。分析位置选择末层原始`o_proj`输出、残差相加之前。现Qwen E16 SAE读归一化MLP输入，位置不一致；沿用30,000 latent/Top32配置，在匹配原始输出训练至少1B有效预测词元，另计原始激活及可重构词元。S7用自身匹配字典及精确父模型。E03追加SAE阶段契约拥有训练/分析、保留残余的位移分解和留出有限干预。字典不匹配或分布迁移失败仅限制SAE解释，不撤销原生作用。[派生说明](../../../research_notes/A17_shared_learning_logic_cn.md)不拥有设计。

## 6. Minimal Falsification Tests

数据准入核验oracle、续写边界、配对/计数、两未见定义和无已填答案泄漏；失败拒绝版本。

Smoke检查四GPU、有限答案归一损失、独立来源/答案计数、必需TensorBoard、初始原生一致、冻结权重精确、实际保存、外进程恢复及有限no-op/跨规则读数。初始能力单列；100%dev准确率标记饱和，不证明完全掌握。

科学局部帮助/伤害需来源有效，接收有限作用区间可辨正/负；来源/符号未解则不足。重复来源batch只是seed内敏感性，不是独立科学复现；三个训练seed仅报告描述性不确定性。来源改善不门控频率主轨迹，只限定有效更新机制解释。确认前须独立seed、冻结阈值和test边界。SAE保留重构残余，核验适配状态读数，并在留出有限干预中比较同有效rank的PCA/随机及扰动大小对照。新分析来源组和接收者discovery/heldout组独立冻结；旧Full来源batch留出可能重复记录，仅作敏感性面板。代理失败保留原生证据。

## 7. Current Evidence

研究者提供1009正文定义载体。E01数据与31工程门通过，job pt-2m4rvpt4在4卡H100 reserved完成。Summary报告初始能力/短适配；来源覆盖和饱和限制科学解释。E02重试pt-i3ianttt完成，64/64工程检查通过；Summary/Detailed保留首失败零步、修复及数值边界。E03 Smoke pt-fleom0t0通过64/64工程门；Full pt-ujjb8f7a已SUCCEEDED，六轨迹/12,000答案、96/96工程PASS；[当前Summary](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/summary_cn.md)拥有完整原生事实和有界局部读数。SAE待执行；机制Unknown。

旧向量实验调节帮助且四格仍有利，要求净损失控制；非本列表结果，裁决保留。

## 8. Claim Boundary And Next Decision

合格数据建立条件规则，合格Smoke只建立实现和有界dev读数。局部作用不识别完整共同/差异功能、专家必要、自然预训练效应或长期收益。SAE描述/干预和架构收益需各自证据。

研究者已采纳更新范围并授权完整顺序。AI完成注册测量与事实记录；证据齐全后的下一项研究者决定是：有界共享作用和观察器对照是否支持机制解释，或需调整载体。训练完成不能关闭科学问题。E01/E02冻结契约、结果及本问题身份保留。

[Focus](../../../focus/focus_list_rule_shared_update_cn.md) · [E01 Summary](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E01_stage1_smoke/summary_cn.md)

### 2026-10-10：已授权配对答案优势补充分析

[子 Anchor](subanchors/17_01_01_rule_conditioned_answer_margin_anchor_cn.md) 与 [sub Protocol](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/subprotocols/paired_rule_margin/protocol_cn.md) 固定更新前后相对答案选择读数；不改变父问题、现有证据与机制 Unknown。该新补充尚未运行，旧的 E03 完成状态只指此前授权阶段。
