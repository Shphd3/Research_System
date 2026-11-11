# 1111 原子集中度与学会/遗忘账本

状态：七臂已纳入。以下解释为AI分析，研究者判断Unknown。完整事实记录：[R04 Summary](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R04_20261109_atom_concentration/summary_cn.md)；[覆盖账本](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/coverage.md)。

## 目的

要回答：让同一低频原子更集中地进入专家，能否改善其相关位置的学习，而不只提高一个路由指标？现有五臂描述训练轨迹；A6和A5分别直接优化集中度、改变固定划分单位。

## 结论

1. A6相对A0的总体NLL差为+0.091856，A5相对A1为-0.118485，学习收益需同时结合低频结果与预设波动规则。

| arm     |     总体NLL |     M中位数 |   频次加权logM |        bin0 |        bin1 |        bin2 |
|:--------|------------:|------------:|---------------:|------------:|------------:|------------:|
| A5      | 4.039118998 | 1.344967711 |   -0.080334963 | 3.720251498 | 3.872186784 | 3.865717683 |
| A0      | 4.083141622 | 1.010460056 |   -0.401735217 | 3.794580477 | 3.942305977 | 3.929827148 |
| A1-deep | 4.085093112 | 0.870828768 |   -0.360922850 | 3.789857108 | 3.930946271 | 3.917200750 |
| A4      | 4.129441802 | 0.810891851 |   -0.472061195 | 3.867186691 | 4.009898194 | 3.986286052 |
| A1      | 4.157604347 | 0.585752336 |   -0.453948743 | 3.901086299 | 4.028563391 | 3.998681224 |
| A6      | 4.174997252 | 0.924780174 |   -0.284026317 | 3.985564060 | 4.104733180 | 4.059321536 |
| A2      | 4.286027700 | 0.256798644 |   -1.345580429 | 4.187885924 | 4.277627418 | 4.202913688 |

原始数据：[总体及十bin逐checkpoint表](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/A1_eval_nll_by_step.csv)，上表M来自[B3](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B3_Mbar_distribution.csv)。

2. A5相对A1的集中度与NLL改善均超过既定检查点变化参照；相对A0的NLL优势方向存在，但幅度仍不足。

| arm     |     M中位数 |   频次加权logM |     总体NLL |
|:--------|------------:|---------------:|------------:|
| A5      | 1.344967711 |   -0.080334963 | 4.039118998 |
| A0      | 1.010460056 |   -0.401735217 | 4.083141622 |
| A1-deep | 0.870828768 |   -0.360922850 | 4.085093112 |
| A4      | 0.810891851 |   -0.472061195 | 4.129441802 |
| A1      | 0.585752336 |   -0.453948743 | 4.157604347 |
| A6      | 0.924780174 |   -0.284026317 | 4.174997252 |
| A2      | 0.256798644 |   -1.345580429 | 4.286027700 |

读图：横轴分别取M中位数和频次加权logM，纵轴均为2000步NLL；更靠下表示预测更好，不能由这些臂的相关推出因果。

![集中与NLL](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/F_B7_Mbar_vs_nll.png)

3. 固定分数A1在1000→2000区间仍有19.81%的位置Top2集合发生变化，P4的固定路由近零翻转预期未成立。

| arm     |   learned |   forgotten |   net_forgotten |   chi_mean |   position_flip_rate |
|:--------|----------:|------------:|----------------:|-----------:|---------------------:|
| A0      |     29281 |         212 |             236 |   0.407636 |             0.392096 |
| A1      |     29244 |         181 |             526 |   0.197567 |             0.198141 |
| A2      |     29553 |         130 |             275 |   0.002753 |             0.002755 |
| A4      |     29295 |         212 |             158 |   0.560060 |             0.569260 |
| A1-deep |     29277 |         171 |             120 |   0.275392 |             0.262880 |
| A6      |     29525 |         133 |             381 |   0.771362 |             0.762490 |
| A5      |     29229 |         199 |             547 |   0.082039 |             0.088713 |

A4与A1-deep各仅一个可用相邻区间，因此各自无法提供要求的第二个区间例子；这些缺失不以重训补造。

原始数据：[共同区间账本](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C8_matched_1000_2000.csv)；各相邻区间见[C8完整表](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C8_learn_forget_ledger.csv)。数目表示达到统计与0.01nat阈值的原子数，不能直接称为语义知识的获得或丢失。

## 机制假设与模型

原子是冻结SAE的激活坐标，不预设等同人类概念。位置$x$ 的次token损失为$\ell_x(t)$ ；原子$j$ 的支撑集为$A_j=\{x:z_{x,j}>0\}$ ，出现次数为$n_j$ 。原子条件NLL是这些位置损失的平均，不等于已证明模型学会了该语义。

专家数$E=8$ ，每个位置选择$k=2$ 个专家。对原子$j$ 、层$l$ 、专家$e$ ，覆盖$c_j^{(l)}(e)=P(e\in S\mid j\text{激活})$ ，纯度$\pi_j^{(l)}(e)=P(j\text{激活}\mid e\in S)$ ，参考频率$p_j$ 在DEV冻结：

$$
\bar M_j=\frac1L\sum_l\sum_e\frac{c_j^{(l)}(e)}k\frac{c_j^{(l)}(e)\pi_j^{(l)}(e)}{p_j},\qquad L=8.
$$

它是无量纲富集读数，允许大于1；负载均衡且EVAL与DEV频率相同时，随机Top2参照为k/E=0.25。它不单独测量梯度是否兼容。频段NLL按bin内原子激活次数加权，同一位置可进入多个原子，不是互斥token分桶。

A6保留原生路由，只向router权重加入集中正则的梯度。令$\operatorname{sg}$ 截断隐藏状态$h$ 的梯度，$\tilde P=\operatorname{softmax}(W_r\operatorname{sg}(h))$ ，用正激活幅值加权形成$q_j$ ，再最小化三阶Rényi熵：

$$
q_j(e)=\frac{\sum_xz_{x,j}\tilde P_x(e)}{\sum_xz_{x,j}},\qquad H_3(q_j)=-\frac12\log\sum_eq_j(e)^3.
$$

各层、micro-batch内出现至少2次的原子按冻结$w_j$ 加权，再加到语言模型CE；λ按50步router梯度范数规则冻结。A5在DEV共激活图中把原子划为8组，以组内$w_jz_j$ 之和形成固定score，8层相同、gate各0.5。两者均保留动态load bias。训练q按激活幅值和soft概率加权，评估M按二元激活和硬Top2计数；H3下降并不由定义保证硬M上升。统一的末层teacher原子也未必能被学生早层隐藏状态识别，截断表征梯度的辅助项只能使用该层已有可读信息；按层诊断可定位这一接口，不能直接证明不可读。A6在推理时只需原生学生router；A5仍需要teacher/SAE与原子分组生成外部分数。

候选机制是同一重复信号的更新被分散到不同参数，集中或能降低有效更新波动；最强竞争解释是集中只是学习结果，或正则/gate/负载本身起作用。另一个可区分的接口解释是：soft H3下降而动态bias补偿硬负载，实际硬M不随之提高；通过既定H3、原始概率、熵、load/bias与硬M联合诊断，避免把操纵不足误写成学习机制失败。A6−A0检验集中正则的联合学习效果；A5−A1检验原子划分相对token划分。它们都没有单独替换或识别梯度噪声中介。

其中$\mathcal J$ 为本micro-batch出现至少两次的原子集合，冻结$w_j=\min(\log(1/p_j)/\operatorname{median}_j\log(1/p_j),3)$ ，实际目标为

$$
\mathcal L_{\rm total}=\mathcal L_{\rm CE}+\lambda\frac1L\sum_l\frac{\sum_{j\in\mathcal J}w_jH_3(q_j^{(l)})}{\sum_{j\in\mathcal J}w_j}.
$$



终点AI分析：A5比A1同时提高硬集中度并降低NLL，支持当前固定分发条件下原子分组路线的联合价值；分组身份、score尺度、bias和gate的作用尚未隔离。A6的H3下降而硬M低于A0，说明soft训练目标没有实现预期的硬集中操纵，不能把它当作集中机制已被充分检验。其NLL方向较差，但按原检查点变化规则保留不足。终点8层中6层平均raw概率有超过99.5%落到单个专家，边际熵仅0.007–0.037nat，与全局soft偏置及bias补偿的解释相容；其余2层并无同等坍缩，且这些诊断未独立识别NLL变化的原因。原始值见D13_A6_raw_probability_marginals.csv。下一步优先考虑A0/A1/A5配对复现及分发尺度控制，尚未授权新训练。

## 实验分析

### 设置

复用A0的8层hidden1024、8专家Top2、expert1536、共同初始化seed17、DCLM顺序、2048上下文、262144有效token/update，AdamW和1000步预热后3e-4恒定学习率。实际冻结λ=0.0141867728347，50步×8层CE范数中位数=0.0135657322，正则范数中位数=0.956223965；沿用预定规则，原单micro的几十量级预计未得到实测支持。比较坐标为有效训练token/更新数，在线teacher开销包含在另列的GPU用时中。固定EVAL共2,097,152位置。A0原生、A1 token聚类固定score、A2随机固定score、A4 teacher蒸馏原生router、A1-deep前4层原生/后4层固定；A6和A5定义如上。checkpoint复用清单见[原始覆盖](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/coverage.md)。

### 原始数据与读图

![总体学习曲线](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/F_A1_eval_nll.png)

横轴是训练更新数，纵轴为原训练评估NLL；右图放大1000–2000步。训练CE原始值/50步尾随均值在[训练曲线](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/F_A1_train_ce.png)；[各频段差值](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/F_A2_bin_contrasts.png)的0线以下表示前者更好。

D1沿用全部250步评估统计：A0从第250步起已高于A1，不支持“500–750步才超过”的原预测。D2复用[原始变体表](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/D2_A1_concentration_variants.csv)：A1去掉bias的M中位数0.696911，实际bias为0.585752；低频bin0反而由0.659596升为0.739287，故总体下降不能泛化到所有原子。Top1的k与随机基准不同，加权M也改变估计量，不能当作纯粹改善。

学会/遗忘：每个区间计算固定支撑集内的平均位置损失差δ及配对SE；n≥50，跨原子BH q<.05且|δ|≥.01nat。净遗忘与此前最低checkpoint比较，另校正最低值选择。相邻区间不一，区间δ与χ的主要跨臂对照采用1000→2000；净遗忘仍依赖各臂此前可用检查点数量，不能把不同历史分辨率的net_forgotten直接解释为臂效应。χ按实际Top2集合变化、再对层平均，A1-deep另分前后4层。

![遗忘与翻转](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/F_C11_forget_vs_flip.png)

横轴是在同一共同区间内按χ分位的组，纵轴为遗忘原子比例；这只描述关联。

| arm     |   quartile |   atoms |   P_forget |
|:--------|-----------:|--------:|-----------:|
| A0      |          1 |    7499 |   0.007068 |
| A0      |          4 |    7499 |   0.012268 |
| A1      |          1 |    7499 |   0.018002 |
| A1      |          4 |    7499 |   0.001200 |
| A2      |          1 |    7500 |   0.003600 |
| A2      |          4 |    7497 |   0.004268 |
| A4      |          1 |    7499 |   0.011868 |
| A4      |          4 |    7499 |   0.007601 |
| A1-deep |          1 |    7499 |   0.009068 |
| A1-deep |          4 |    7498 |   0.005201 |
| A6      |          1 |    7499 |   0.005734 |
| A6      |          4 |    7498 |   0.006135 |
| A5      |          1 |    7500 |   0.006667 |
| A5      |          4 |    7498 |   0.010269 |

最高χ分位并非在所有可学习路由臂都有最高遗忘率，因而P4的统一预测不获支持。同一原子可跨组共同出现，原子数不是独立种子数。[逐原子完整表](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/per_atom)与[上下文例子](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/C12_examples_decoded.md)保留完整读数。

| arm     |   atoms |   median_t50 |   rho_t50_logp |   rho_t50_Mbar |
|:--------|--------:|-------------:|---------------:|---------------:|
| A0      |   29986 |   750.000000 |      -0.254618 |      -0.091187 |
| A1      |   29994 |   750.000000 |      -0.323613 |       0.032443 |
| A2      |   29995 |   750.000000 |      -0.307450 |      -0.092040 |
| A4      |   29987 |   750.000000 |      -0.269457 |      -0.068819 |
| A1-deep |   29994 |   750.000000 |      -0.295193 |      -0.025698 |
| A6      |   29992 |   750.000000 |      -0.290461 |      -0.104031 |
| A5      |   29990 |   750.000000 |      -0.311032 |      -0.062519 |

t50以第250步为起点，用250→2000的净改善达到一半的首个checkpoint；不改善的原子未定义。它的分辨率是250步，存在成员选择与时间离散化限制。既有五臂t50与log频率的相关约−0.25至−0.32，与末端M的相关绝对值不超过0.092；这里描述的是条件位置学习时间，不能当作独立语义知识获得。

### 参考频率的事后诊断（AI分析）

  原M的分母p来自DEV，覆盖和纯度却在EVAL上统计。令r为EVAL激活频率，u为实际硬Top2的slot分布，α为EVAL专家assignment负载份额，则严格有M=k(r/p)Σu³/α；即使α均匀，也仍需r=p才能化为EkΣu³。原M因此同时包含分发和参考频率比。

  随机A2中，M与r/p的Spearman相关为0.994165；原M的10%–90%分位为0.189536–0.324290，用EVAL分母后的补充读数缩为0.250370–0.259861，接近随机参照0.25。这是固定数据上的估计量诊断，不是新训练或新的主要指标。

  同一原子跨臂的Δlog M中r/p精确抵消，数值误差小于1.3e-15，所以B6的跨臂相关不因此失效；但同一臂按M分位解释遗忘，会混入频率比和出现次数/检验功效。原主表、P1–P4和冻结M均保留。[推导、原始数据与计数敏感性](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/metric_reference_audit_existing/summary_cn.md)。此分析在观察遗忘分位后提出，属于事后探索。

### 为什么与认识更新（AI分析）

现有比较区分了“teacher定义的固定分发优于随机分发”和“它优于原生可学习分发”；前者的优势不能替代后者。集中度中位数的漂亮排序也会随汇总权重改变，说明需要A6/A5的实际NLL结果来检验学习价值。账本同时保留共同区间、原子支撑与实际χ，避免把区间长度或总体学习趋势误写成遗忘机制。A1路由代码的score对同一EVAL位置固定，选择却是Top2(score+bias)，故动态bias是该固定score路径的时变路由输入；若冻结同一bias，固定层的分发才会真正不随checkpoint变化。这是代码结构推导，尚未测得冻结bias对NLL的训练收益。下一科学决定仍为Unknown；不因这份报告自动增加训练预算。

### P1–P4与边界

| prediction   | AI_analysis                                                                                                                                                                                                                                     | researcher_judgment   |
|:-------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------|
| P1           | 综合AI判定：NOT_SUPPORTED_OR_MIXED；方向非支持；A6−A0的M中位数=-0.085679882，低频幅度见原表。；所列逐指标差异均超过各自相邻checkpoint变化参照。                                                                                                 | Unknown               |
| P2           | 综合AI判定：INSUFFICIENT；方向非支持；总体差=+0.091855630，bin0–2差=[0.19098358296192108, 0.1624272028831233, 0.12949438803992175]；不足（小于预设相邻checkpoint参照）。；逐指标不足：eval_nll,bin0,bin1,bin2的差异小于各自相邻checkpoint参照。 | Unknown               |
| P3           | 综合AI判定：DIRECTIONALLY_SUPPORTED；方向支持；A5−A1的M中位数=+0.759215375，NLL=-0.118485348；超过总体相邻checkpoint变化参照。；所列逐指标差异均超过各自相邻checkpoint变化参照。                                                                | Unknown               |
| P4           | 非支持当前简单预测：A1在共同1000→2000区间的实际位置翻转率为0.198141，固定score不等于固定映射；A4与A1-deep的高翻转四分位也未呈最高遗忘率；对翻转的因果归因仍不足，按分位原表报告。                                                               | Unknown               |

相邻checkpoint变化是原Protocol要求的保守参照，本身混有正常学习趋势，并非独立噪声估计。单种子seed17；仅2000步/每臂524,288,000有效训练token；teacher训练时见过这些训练token；可学习路由的集中可能是学得好的结果；A6用同一SAE字典优化和测量，存在循环风险；teacher bf16的Top32单索引一致率98.962%，沿用原A1选择；旧臂缺失部分checkpoint，账本区间不一；位置SE未消除文档内相关；总体复算与原四卡评估并非全部逐位一致；fp16存储差另报。

数值核查见[逐位置一致性表](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/position_consistency.md)。图均有PNG/PDF，所有表有CSV/Markdown；[图表说明索引](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/figure_table_notes.json)。[实施偏差](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R04_20261109_atom_concentration/implementation_amendment_20261110_cn.md)和[Detailed](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R04_20261109_atom_concentration/detailed_cn.md)解释代码修复、缺失和原始来源。
