# Protocol：A17_04_E01 R02 单层 AdamW 条件映射迁移

## 0. 审批快照

状态：APPROVED_FOR_BOUNDED_TRANSFER_AND_SMALL_OPTIMIZER_PROBE。单层获取完成后，研究者明确授权最后层Q/K/V/O＋AdamW迁移与小型优化器诊断。该新授权仅在本有限范围覆盖E03先等待的旧要求；机制判断、采用与问题闭合仍Unknown。

版本 a17_04_e01_r02_single_layer_adamw_v1。本文件是E01新轮次，不是第四个核心实验。原E01冻结Protocol、结果与快照保留。GPU前冻结本两语合同和当前[Anchor](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md)/[Focus](../../../../../../focus/focus_conditional_mapping_transfer_cn.md)、代码配置/输入；实际时间哈希由执行清单持有。

目的：旧规则已学会后，比较新可见模式的同向/反转映射对旧规则保持的作用。独立小probe测当前步的优化位移/范数/继承动量，不把局部效应解释为完整轨迹原因。角色root-cause audit，A–G授权内一致性自审PASS，仍需工程预检/Smoke。

条件：29/43/71三个续训顺序种子，各consistent/reversed/joint_reversed，都从**同一个E03 AdamW1200旧终点**出发；每分支重置AdamW、1200步×20目标。仅第27层四投影6291456参数可训练。probe在Base/SGD240/AdamW240、两批旧TRAIN做34个固定局部条件。

主量：24000新答案后，反转减同向的旧正确答案相对反规则答案margin变化；两DEV分别再等权合并。支持须旧起点合格、反转新规则学会、主效应描述一致为负；净旧损害还须相对共同起点绝对变坏。较小收益不等于净损害。

主分支固定旧权重、模型分词/数据、新前缀和答案边际、种子内顺序、可训练范围、新优化器和新答案量；只变新模式口令到位置标签。DEV已使用，TEST不读。joint多旧监督、仅12000新答案，是可行性对照，不是同监督收益赢家。完成九有限分支/34probe或明确部分失败、资格/保存/登记/两语结果，不按成功加预算，不增架构/SAE/发布/commit/push；科学与后续仍由研究者决定。

## 1. 术语与定义

旧模式一：甲取首、乙取末。新模式二consistent保持，reversed交换。模式可见，每个世界独立标签一致。joint_reversed混合旧模式一与反转模式二监督。

一记录是一前缀/单答案；列表配对含两口令。order_new为熟悉三元组未见排列，combination_new为未见三元组，均用已见词表。

续训种子只改变新训练列表顺序；三个路径共享一个已训练旧终点，不是三个独立旧模型。native更新指裁剪优化后实际FP32参数位移；范数匹配缩放该位移后复测舍入，不匹配累计训练历史。

## 2. Anchor对齐

父问题研究条件关系是否改变共享更新。原E01旧规则未学会，E03提供合格单层终点。R02从此实际状态重做关系干预，保留输出拆分。当前Anchor改为四权重完整原生前向，Q/K/V可训练时不能沿用旧固定上游的 \(\Delta h=\Delta W a(x)\) 表达全部干预。

| 项目 | 模型项/竞争解释 | 用途 | 支持/不支持/不充分 | 产物 |
|---|---|---|---|---|
| 同向/反转 | 映射关系、\(E_s\) | 同输入曝光只改标签 | 合格且一致负/无或反向/获取或工程失败 | 种子面板效应 |
| 共同旧终点 | 已学规则前提 | 避免未学会冒充保持 | 四格≥80%/未合格/缺状态 | 起点读数/资产 |
| 同新熟练度 | 难度初始熟悉度 | 首个保存四格达标点 | 有且保留路径边界/未跨越/无效 | 选择回执 |
| joint | 可见模式可行性 | 有旧监督能否同学 | 两模式四格都≥80%/失败留Unknown/不完整 | joint表 |
| 优化probe | 方向步幅历史 | 同状态实际位移/有限变化 | 局部差异/无/梯度匹配无效 | probe表 |
| CE/模式配对 | 候选适应 | 分访问与选择 | 选择变化/仅访问/恒等式无效 | 拆分/模式表 |

## 3. 待检验假设

候选H：相同新答案曝光后，反转比同向更降低旧答案优势。更强遗忘判断需绝对旧损害。局部候选问题是优化方向、位移范数与继承moment会改变固定状态的下一步预测；probe不预设方向，也不外推完整迁移轨迹。

旧/新获取与工程合格后，主效应没有描述一致负值构成局部不支持，反向保留。反转没学会或旧起点不合格为不充分，非假设被否定。

## 4. 竞争解释

1. 反转更难或起始更不熟：报起点/轨迹、最终新四格与最早同熟练点，但路径不等价。
2. 候选概率改变不代表保持选择：看margin、配对、候选访问/条件选择。
3. 旧状态/优化历史决定：主分支同旧state、freshAdam；三顺序不是独立旧状态不确定性。
4. 实际步幅/方向不同：同状态比较native和交叉范数；不能全局消除历史/预条件。
5. 无法利用模式：joint成功给可行见证，失败混合预算监督优化，不能证明容量不足。
6. 工程/标签/批次伪效应：身份、no-op、冻结、恢复、计数保护资格。

## 5. 数据构造与来源

不新生成、不评TEST。复用 data_a17_conditional_mapping_v1 的 train.jsonl/dev.jsonl，位于 /data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1。每世界TRAIN2400条=1200列表×两口令；DEV800=两面板各200列表×两口令。原TEST历史已暴露，本轮不载入、不称确认。

新两世界前缀/inputIDs相同，只按口令交换首末target。每配对批答案边际相同；底层TRAIN列表跨模式复用、完整输入随模式不同。保留记录/列表/orbit/无序组/面板/模式/口令/world/词/标签/input身份；原order允许复用、combo隔离不变。GPU前查结构、目标、完整前缀边界与配对。

输入ID：model_qwen3_0p6b_base_official_a5、tokenizer_qwen3_0p6b_base_official_a5、data_a17_conditional_mapping_v1、data_a17_mapping_acquisition_diagnostic_v1、adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main、adapter_a17_04_single_attention_20261011t145214z_full_attn1_sgd_main。Adam家族1200用于迁移，240权重/moments用于probe；SGD家族240用于probe。probe使用登记E02的neutral TRAIN/DEV（data_a17_mapping_acquisition_diagnostic_v1），旧前缀标签来自原映射，精确成员hash冻结。两个probe TRAIN批取E03 Main步0保存的batch_order_record_ids前两批，各20记录、三状态共用。probe旧DEV每面板按list_id排序取前20列表、两口令，共80记录；冻结具体ID/hash。迁移Smoke每面板前10排序列表、两口令/world，不TEST。

读载荷前查registry、当前选定strict。Base目录 /data/250010109/model_cache/Qwen3-0.6B-Base-official。用登记家族成员/SHA/父Base绑定实际1200/240/0状态，不用latest。

## 6. 学习任务与监督边界

登记前缀后的单答案词元CE；前文/填充忽略。模型只看到模式、口令、三词（正确词在候选中），不看显式target/split/隐藏world。确定映射给监督，世界分开，不把同完整输入相反标签混在一世界。joint旧/反转新标签明确。无SAE/router/专家/分类辅助/蒸馏/自然文本。

## 7. 模型与冻结变体

28层Qwen3-0.6B，仅 model.layers.27.self_attn.{q_proj,k_proj,v_proj,o_proj}.weight 训练。Q2048×1024，K/V1024×1024，O1024×2048，四张6291456。早层、偏置/q-k norm、MLP、embed、末norm、lm_head冻；运行时查名形/数，每步版本、初始化/阶段末字节。

FP32原生SDPA、eval无dropout、确定性、无TF32；不cache冻结可训练依赖。迁移从E03Adam Main1200四权重/登记Base开始；不继承旧优化器/RNG/计数。每分支freshAdam、种子顺序、阶段新坐标。分支中精确恢复要继承该分支状态，与主动分支起点reset不同。

## 8. 训练目标与优化

每20答案经验损失 \(L=20^{-1}\sum_i-\log p_\theta(y_i\mid x_i)\)，nat/答案；4个micro5，每批loss和除20。前文填充不分母，无正则辅助，组件空。独立worker DP1，节点四卡不乘每步答案。

迁移全用freshAdamW lr1e-4、betas(.9,.999)、eps1e-8、wd0、foreach=False/fused=False、恒定率。四张合梯度globalL2clip1，记原始/裁剪/实际位移。不跳步/调参/早停/自适应延长。

每consistent/reversed1200步=24000新答案，2400记录十遍。joint每步5列表×两口令×两模式，10旧+10新；1200步24000总=12000旧+12000新，各五遍。三种子主分支共144000新；joint加72000总=36000旧+36000新。九分支共216000训练答案。旧已训练、probe梯度、Smoke、重放、评估另计。

## 9. 条件、种子与检查点

29/43/71各三分支，共用同Adam1200。种子内同向/反转顺序相同；joint取对应种子列表流、每批5完整四元组。

保存/评估0、1、16、50、120、240、600、1200步，对应0/20/320/1000/2400/4800/12000/24000目标。joint旧/新各半，单列。每分支8状态，齐全为72；不按效果选终点。

Smoke仅seed29，三分支×3步×20=180答案；每分支外部步1→2，3×20=60重放另计。Full从登记旧终点重启，不接Smoke。Smoke小DEV，Full全DEV。

状态保存四权重、Adammoments/step、恒定schedule、Python/NumPy/CPU/CUDA RNG、实际步/目标、旧新数、branch/seed、旧起点身份、cursor/order/nextIDs、代码/配置/父hash。适配器依赖Base，非独立LM。

## 10. 主指标与冻结分析

旧输入正确端点\(y\)、相反端点\(o\)，\(m_A=\log p(y\mid x)-\log p(o\mid x)\)，\(M_A\)为固定旧DEV均值。1200步

\[
E_s=[M_A(\theta^{\mathrm{reversed}}_{s,1200})-M_A(\theta_0)]
 -[M_A(\theta^{\mathrm{consistent}}_{s,1200})-M_A(\theta_0)].
\]

\(\theta_0\)共同已学旧state、\(s\)续训顺序，单位nat/答案。两panel分别、再等权，口令/种子等权。报3效应、均值、范围、样本SD。三效应都<0且均值≤−.01nat为继承的描述一致负效应；均>0且均值≥.01为正一致；其它弱/异质，不证明相等。无p值/独立旧模型推断/事后删种子列表/未接触确认。

旧起点四口令×面板格均≥80%；新最终四格均≥80%。两世界初始→最终CE/accuracy/margin照报。consistent起点已合格，不强求再涨.01nat/1pp，明确天花板。解释反转负迁移还需其最终学会、实际新目标margin上升；否则已学信号解释不充分，不保证训练成功。

净旧损害单独报相对\(\theta_0\)的CE升、准确率降、margin降及幅度；反转较差不等于净损害。材料报告惯例CE .005nat、accuracy1pp、margin.01nat，非显著性。

次同熟练读数取首个保存点新四格均≥80%，起点已达选0；没跨越记不可用，不续训。该点旧新照报，难度路径仍不同。joint终点两模式各四格均≥80%才作可行见证；多旧标签/新曝光半量，不能同监督赢家。

有限完成/冻结后仅用TRAIN/DEV。记录/列表为观察单位，续训seed是在同旧state条件下的顺序变化单位。缺配对格/点阻断对应estimand、不填补。analysis保存主种子/panel、轨迹、同熟练选择、loss/mode/配对和资格。

## 11. 次指标与局部优化器probe

保留CE、全词表准确率、正确/反规则margin、正确/最强全词表竞争margin/ID、三词概率、双口令同对/同argmax。候选\(S\)访问 \(-\log\sum_{w\in S}p(w)\) 加条件选择 \(-\log[p(y)/\sum_{w\in S}p(w)]\) 精确为CE，非内部模块。

\(s_{m,c}=\log p(L_3\mid x_{m,c})-\log p(L_1\mid x_{m,c})\)，\(a_m=(s_{m,乙}-s_{m,甲})/2\)，\(q_m=(s_{m,乙}+s_{m,甲})/2\)，\(C=(a_1+a_2)/2\)，\(K=(a_2-a_1)/2\)。旧/同向期望a>0、反转新a<0；这是精确输出对比，不是参数分解。

probe三状态：Base、E03单层SGD240、AdamW240。每状态每固定旧TRAIN批，每条件前恢复全部四权重/相应优化器。五条件：noop、nativeSGD、nativeAdamFresh、SGD实际位移缩至AdamFresh范数、AdamFresh实际位移缩至SGD范数。设置同E03：clip1/SGD.01/Adam1e-4,.9/.999,eps1e-8,wd0。Adam240每批再做继承moments/step的nativeAdamCarry及其缩至SGD范数。Full共3×2×5+2×2=34；Smoke仅Base第一批5条件。源梯度用旧TRAIN，接收读数/梯度用固定80旧DEV；不测模式二迁移。

源梯度\(g_{\mathrm{src}}\)与真实FP32位移\(\delta=\theta_{\mathrm{after}}-\theta_{\mathrm{before}}\)分开。缩放native位移后复测实际舍入位移，范数误差≤1%；零native位移记ZERO_NO_DIRECTION，不任意替换。保存总体/各投影梯度与位移范数、两优化器方向cosine、下降对齐\(\cos(-g_{\mathrm{src}},\delta)\)。不同历史状态的差异是描述，不能当同状态反事实。

接收旧DEV均值CE为\(L_R\)，同state梯度\(g_R=\nabla L_R(\theta)\)，报

\[
\Delta L_R=L_R(\theta+\delta)-L_R(\theta),\qquad
R_{\mathrm{finite}}=\Delta L_R-\langle g_R,\delta\rangle .
\]

该余项是实际四张位移下一阶预测与测量有限变化的定义差。probe CE由原生FP32 logits用FP64 log-softmax复算，梯度用原生FP32答案CE，保留nativeCE对照。因此测量余项包含有限步非线性及剩余精度差，不是纯数值误差估计，也不证明某原因造成余项。Adam实际位移不能用负原梯度替代；局部等范数不能解释1200步历史。

每迁移分支7个TB标签：tokens/train_lm_loss、updates/train_lm_loss、tokens/train_total_loss、updates/learning_rate、progress/tokens_seen、progress/optimizer_step、progress/effective_tokens_per_update。答案加权CE/total、学习率、目标更新坐标/effective20；分支局部，旧24000另记。probe是固定state分析、非未记录的连续训练。

保护：有限、noop一致、四张清单、冻结版本/末byte、无跳步、独立目标/批ID、必需finite tags、完整optimizer/RNG/order外部精确恢复、CE误差<2e-5nat、范数误差≤1%、代码配置数据freeze不变。失败停受影响项保留部分。

## 12. 正确、错误、易混案例

正确：旧甲首乙末，同向不变、反转交换；前缀/配对答案边际相同；noop/分支起点一致；probe每条件独立restore。

错误：混矛盾标签不带模式、前缀target、超允许划分泄漏、TEST、主顺序不配对、只训O、声明fresh却继承moments、probe累积、joint计数错误。拒绝/无效。

易混：反转较同向差但二者都帮助旧；CE好选择坏；consistent步0已合格；joint失败；局部等范数差不能解释长期。保留。

## 13. 科学步骤与阶段契约

| 阶段 | 目的/输入 | 怎么/为什么 | 产物 | 状态/失败/交接 |
|---|---|---|---|---|
| 预检 | 旧状态/Base/TRAINDEV/probe | 当前strict、SHA成员/结构/配对/四张 | 输入/顺序清单 | 错误阻依赖GPU |
| 冻结 | 防结果驱动 | 当前owner/合同、codecfgdata/ID/env | freeze/certificate | 缺身份不启动 |
| Smoke/replay | 迁移/probe工程 | seed29三×3、小DEV、各1→2外部；Base5probe | 状态/读数/tags/gate | FAIL阻Full至合格修复 |
| Full迁移 | 已学起点的关系 | 三顺序×三fresh分支、1200 | 各8保存/旧新读数 | 有限；没学会不充分，不延长 |
| Fullprobe | 局部更新后果 | 三state两批34独立干预 | 位移/有限变化/余项/normcos | nonfinite/zero/norm失败限结论 |
| 分析登记 | 有限可审计认识 | 相对/绝对效应与获取/同熟练/joint；实际登记 | Summary/Detailed/manifest | 交事实，科学/后续独立 |

## 14. 算法、输出与来源契约

执行根 /data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer，提交前绑定时间戳run。代码配置、原预测/probe数组位移、logs/TB/权重执行侧；本轮正式Protocol/Summary/Detailed/manifest在此，不Git raw。

复用查过E03四张carrier、AnswerLM/collate、SGD/Adam、恢复/TB/freeze；适配E01world读数、配对分支/joint/mode。拒绝O-only固定上游假设、TEST loader、不合格旧state作迁移起点、敏感投影/SAE/MoE。先查training_reuse_index/源码并记录复用适配拒绝。

root标准acp_submit_template.sh、h100-4-reserved、image shphd-lite-0911、一四H100节点、每job7200秒。GPU0/1/2各一seed顺序三分支；GPU3小probe。Smoke仅seed29：GPU0/1/2各跑其一个分支，GPU3跑probe。四个独立worker不算数据并行副本。保留dryrun/实际规格镜像/直接jobID命令/持久日志/设备视图；Full需合格Smoke，不换硬件、不重复提交active。

每分支run/<phase>/seed_<seed>/<branch>/checkpoints/update_<step>/state.pt+manifest，或冻结配置/源码中明确的等价精确路径。含实际总/旧/新目标、Base/旧终点hash、完整恢复。probe放run/optimizer_probe/<phase>/<state_id>/batch_<index>/及results.json/manifest.json，保存冻结条件/实际delta/norm/noop。

分别登记实际Smoke/Full家族、明确成员/计数/Base与已学旧state依赖/producer代码配置数据hash/恢复资格；probe分析登记实际保存和当前strict。缺/部分显式；平台成功不等科学资格，失败身份保留，不静默修冻结证据。

## 15. 支持、失败、不充分

支持须共同旧起点合格、主两world新终点四格合格、反转新margin实际提升、工程资格、三E负且均值≤−.01nat。只支持在一个旧state条件下的关系依赖旧margin代价；净损害另看绝对变化。

合格无/反向为局部不支持；弱/混合异质非相等。旧起点/反转获取提升失败、缺配对终点、工程无效为不充分/无效。consistent起点熟练不强求任意额外涨幅，保留天花板。

joint两模式四格均≥80%才可行见证，否则Unknown。probe只资格局部，不能救主迁移缺证据。有限负面结果如实完成仍算事实交付。

## 16. 不能声称什么

无必然任务矛盾/遗忘、内部共性差异模块、专家/分开训练收益、纯容量优化原因、自然文本、独立旧state复现。模式可见使两映射原则可兼容；同熟练不消路径，joint监督/曝光不同，probe norm/cos/remainder局部非连续证据。已用DEV是诊断非fresh确认。

## 17. 确认、冻结、修订账本

当前用户授权单层AdamW迁移和有限probe；旧转贴四层建议不覆盖明确单层。GPUfreeze前当前Anchor/Focus应一致；旧E01科学历史/结果保留。

| 块 | 内容 | 来源/状态 |
|---|---|---|
| A | 条件关系问题 | 当前执行请求，科学Unknown |
| B | 原TRAINDEV、固定probe | 已核实，无新TEST确认 |
| C | 模式可见/中性/单答案 | 已采用任务 |
| D | 单层四张/共同已学终点 | 明确选择、实际E03 |
| E | freshAdam、20/1200、joint10+10 | 委托操作、继承优化 |
| F | 相对margin/绝对伤害/新获取/probe | 现Anchor读数、授权诊断 |
| G | Smoke恢复、九分支34probe/四卡 | 当前范围/资源 |

自审任务监督、完整前向、主同曝光/joint区别、同旧state、获取/主分支、局部长程边界/noTEST一致，非机制确认。GPU前绑定ID路径源码配置runtime并冻双语，初始NOT_RUN。

启动前纠正改本两语单轮合同后refreeze；GPU后保留正文，重大修订追加ID/time、前后、原因、已见、影响、授权、资格。后补回执状态/结果链接，不覆盖旧E01或制造科学判断。
