# S09 详细记录：单成员频率与联合结构

## 实验对象、公式与执行顺序

原始Qwen3-0.6B-Base（28block、宽1024）及两个block27、30000维ReLU-Top32字典，来源及hook沿用S08：Attention为o_proj输出、残差前；MLP输入为mlp实际输入、残差和post_attention_layernorm后。不同字典ID不对应。S09只读取稀疏缓存，没有加载模型/权重或重新前向。3源各257篇问题，原8个位置floor((j+.5)*min(全长,128)/8)不变。Magicoder只用problem、GSM8K/MMLU只用question，无答案或MMLU选项。S08源路径/revision/字段在源data/sources.json，实际缓存SHA在本轮冻结计划。

划分：在各源按SHA256(seed2026110409+'S09'+文档ID)排序，前128发现、后129留出，不重新抽样文本。同篇8位置不跨组。留出排序保持冻结顺序，内部全部i<j，跨源循环偏移1..64，各8256个不同文档对；同一篇不与自身比较。每对平均8个对齐位置的实际Jaccard=交集/并集，不把位置或反复参与的边当独立文档。

A预测参照：对每源每分位计算全部30000个发现频率p_f，独立Bernoulli生成129篇×8位置，重复256面板；每行只保证期望成员数32。每个模拟支持实际求Jaccard，报告真实三组均值/参考/差值及MCSE。独立文档交集期望为sum p_Af p_Bf；同域plugin的sum p_f²包含频率估计噪声，另列无偏交集估计sum c_f(c_f−1)/(128×127)，它不是Jaccard期望。对严格Top32的A解释，则使用留出自身次数的条件零模型，不能把这项描述性参照冒充发现预测。

当两行均32时，J=I/(64−I)=I/64+I²/[64(64−I)]。完整同域无序对的mean I=sum c_f(c_f−1)/(n(n−1))，列次数固定便严格不变；共同出现可改变高阶项、从而改变平均J。跨源若取全部n²对，mean I=sum c_Af c_Bf/n²；等数量循环子图不是全集，允许因行分配产生波动。两种交集/J参考都保存，避免把J剩余直接等同于所有联合结构。交集分布补充只用事前固定的8个审计快照（每链首/末），明确不是256个完整null的全部分布。

B零模型：每个源、划分和分位分别对“行=位置、列=feature”交换。等概率选不同两行，保留交集，独有成员的并集随机等分给两行（均32）；不变/失败交易也计入，保证对称性。4个独立链、burn100扫，thin10扫、每链64样本。每扫ceil(n/2)次提议。每个快照检查每行唯一/32与全30000列计数。源/位置边际严格固定，不固定其他文档属性或跨位置连贯性。原成员保留率与sum c_f²/(n²×32)的约束期望比较；检查多链Rhat/ESS，不能只用移动量宣称混合。小4×4行列次数均2的90状态空间用20000样本校准；此实现检查不是研究发现。

联合统计：发现集按pooled频率/文档支持先固定24ID，不查看联合效应挑ID；全部276对进入主要统计。每篇q_ij=8位置中两成员共同为正的比例。各源发现残差r_d=mean q_d−E_null q_d，方向v_d=r_d/||r_d||；两源方向v_AB=(r_A−r_B)/||r_A−r_B||。留出本源统计v_d·(q_test−E_null q_test)；跨源统计v_AB·(r_A,test−r_B,test)。同一源有残差并不能替代后者。独立零模型样本投影给条件null p，各自六检验Holm。方向为发现统计权重，不能命名为语义轴。置信区间由129篇整篇bootstrap999次；这是给定方向和估计null中心的条件区间，不宣称完整抽样误差已整合。null算法的蒙特卡洛误差另报，256个null不是256个新增实验文档。

补充：24成员中激活个数0..24的分布；发现集pooled最常见8个精确24bit组合+OTHER；12示例对在276对内按6个pooled正残差、6个最大源间残差范围选，须某源至少4发现文档共现。该选择规则先于留出固定，所有结果包含支持不足/零/相反情况。token探索额外固定当前token为发现最常见3ID（279=' the',315=' of',13='.'）或OTHER；使用原发现方向，不重选特征。其他分层、独立格式匹配、分类或干预均NOT_RUN。

## 数值校验与未运行项

evidence/independent_verification.json核对原S08全部80文件未改、771文档划分、200直接集合Jaccard、32审计快照的276对共同出现、768个层的列次数、固定交集恒等式、两组Holm与24个主要/探索投影重放。Rhat/ESS均达冻结阈值，无需事前允许的延长重跑。没有为了结果选更好的零模型或修改判据。独立格式匹配NOT_RUN，NuminaMISSING；分类器/模型前向/训练/功能干预NOT_RUN，科研接受/关闭Unknown。

## A全部原始组内/跨组结果

| site | A | B | comparison | real_J | real_CI_lo | real_CI_hi | discovery_Bernoulli_J | real_minus_Bernoulli | heldout_fixed32_margin_J | real_minus_fixed32_margin |
|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | within_A | 0.035707 | 0.033468 | 0.038309 | 0.037457 | -0.001750 | 0.034054 | 0.001653 |
| ATTN_SAE | Magicoder | GSM8K | within_B | 0.017482 | 0.016263 | 0.018747 | 0.020486 | -0.003004 | 0.017342 | 0.000139 |
| ATTN_SAE | Magicoder | GSM8K | cross | 0.012468 | 0.011609 | 0.013428 | 0.011863 | 0.000605 | 0.012401 | 0.000067 |
| ATTN_SAE | Magicoder | GSM8K | pooled_gap | 0.014126 | 0.012725 | 0.015598 | 0.017108 | -0.002982 | 0.013297 | 0.000829 |
| ATTN_SAE | Magicoder | MMLU | within_A | 0.035707 | 0.033468 | 0.038309 | 0.037457 | -0.001750 | 0.034054 | 0.001653 |
| ATTN_SAE | Magicoder | MMLU | within_B | 0.026412 | 0.023358 | 0.030711 | 0.027848 | -0.001436 | 0.024380 | 0.002032 |
| ATTN_SAE | Magicoder | MMLU | cross | 0.020494 | 0.020062 | 0.020962 | 0.020806 | -0.000312 | 0.020456 | 0.000038 |
| ATTN_SAE | Magicoder | MMLU | pooled_gap | 0.010565 | 0.008896 | 0.012869 | 0.011846 | -0.001281 | 0.008760 | 0.001805 |
| ATTN_SAE | GSM8K | MMLU | within_A | 0.017482 | 0.016263 | 0.018747 | 0.020486 | -0.003004 | 0.017342 | 0.000139 |
| ATTN_SAE | GSM8K | MMLU | within_B | 0.026412 | 0.023358 | 0.030711 | 0.027848 | -0.001436 | 0.024380 | 0.002032 |
| ATTN_SAE | GSM8K | MMLU | cross | 0.012047 | 0.011212 | 0.012958 | 0.011521 | 0.000526 | 0.012016 | 0.000031 |
| ATTN_SAE | GSM8K | MMLU | pooled_gap | 0.009900 | 0.008126 | 0.012198 | 0.012646 | -0.002746 | 0.008845 | 0.001055 |
| MLPIN_SAE | Magicoder | GSM8K | within_A | 0.119809 | 0.116053 | 0.123955 | 0.119551 | 0.000258 | 0.117224 | 0.002585 |
| MLPIN_SAE | Magicoder | GSM8K | within_B | 0.098103 | 0.095286 | 0.100882 | 0.099485 | -0.001383 | 0.097680 | 0.000422 |
| MLPIN_SAE | Magicoder | GSM8K | cross | 0.062319 | 0.060568 | 0.063950 | 0.063178 | -0.000859 | 0.062212 | 0.000107 |
| MLPIN_SAE | Magicoder | GSM8K | pooled_gap | 0.046637 | 0.044233 | 0.049093 | 0.046341 | 0.000296 | 0.045240 | 0.001396 |
| MLPIN_SAE | Magicoder | MMLU | within_A | 0.119809 | 0.116053 | 0.123955 | 0.119551 | 0.000258 | 0.117224 | 0.002585 |
| MLPIN_SAE | Magicoder | MMLU | within_B | 0.079965 | 0.076133 | 0.084679 | 0.081924 | -0.001959 | 0.077960 | 0.002005 |
| MLPIN_SAE | Magicoder | MMLU | cross | 0.070354 | 0.068269 | 0.072429 | 0.070937 | -0.000582 | 0.070260 | 0.000094 |
| MLPIN_SAE | Magicoder | MMLU | pooled_gap | 0.029533 | 0.027126 | 0.032378 | 0.029801 | -0.000268 | 0.027332 | 0.002201 |
| MLPIN_SAE | GSM8K | MMLU | within_A | 0.098103 | 0.095286 | 0.100882 | 0.099485 | -0.001383 | 0.097680 | 0.000422 |
| MLPIN_SAE | GSM8K | MMLU | within_B | 0.079965 | 0.076133 | 0.084679 | 0.081924 | -0.001959 | 0.077960 | 0.002005 |
| MLPIN_SAE | GSM8K | MMLU | cross | 0.062726 | 0.060686 | 0.064973 | 0.061205 | 0.001520 | 0.062612 | 0.000114 |
| MLPIN_SAE | GSM8K | MMLU | pooled_gap | 0.026308 | 0.023444 | 0.029783 | 0.029499 | -0.003191 | 0.025209 | 0.001100 |

## A交集与非线性审计

| site | comparison | analytic_discovery_plugin_E_intersection | discovery_unbiased_E_intersection | MC_Bernoulli_mean_intersection | real_heldout_intersection | fixed32_null_mean_intersection | fixed32_null_intersection_range | real_J_linear_I_over64 | real_J_curvature | null_J_curvature_mean | full_cross_real_J | full_cross_null_J |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | within_Magicoder | 2.285522 | 2.051550 | 2.285406 | 2.080245 | 2.080245 | 0.000000 | 0.032504 | 0.003203 | 0.001550 | nan | nan |
| ATTN_SAE | within_GSM8K | 1.277649 | 1.035741 | 1.277881 | 1.076490 | 1.076490 | 0.000000 | 0.016820 | 0.000662 | 0.000522 | nan | nan |
| ATTN_SAE | within_MMLU | 1.715714 | 1.477255 | 1.715194 | 1.512536 | 1.512536 | 0.000000 | 0.023633 | 0.002779 | 0.000746 | nan | nan |
| ATTN_SAE | Magicoder/GSM8K | 0.740791 | 0.740791 | 0.741330 | 0.777647 | 0.775616 | 0.007025 | 0.012151 | 0.000317 | 0.000282 | 0.012435 | 0.012402 |
| ATTN_SAE | Magicoder/MMLU | 1.288101 | 1.288101 | 1.287259 | 1.278192 | 1.277729 | 0.005950 | 0.019972 | 0.000523 | 0.000492 | 0.020485 | 0.020455 |
| ATTN_SAE | GSM8K/MMLU | 0.719322 | 0.719322 | 0.719914 | 0.751438 | 0.751862 | 0.006480 | 0.011741 | 0.000306 | 0.000268 | 0.012055 | 0.012016 |
| MLPIN_SAE | within_Magicoder | 6.756134 | 6.557363 | 6.752419 | 6.636234 | 6.636234 | 0.000000 | 0.103691 | 0.016118 | 0.013533 | nan | nan |
| MLPIN_SAE | within_GSM8K | 5.733582 | 5.526759 | 5.734544 | 5.653358 | 5.653358 | 0.000000 | 0.088334 | 0.009769 | 0.009347 | nan | nan |
| MLPIN_SAE | within_MMLU | 4.796555 | 4.582354 | 4.798862 | 4.577580 | 4.577580 | 0.000000 | 0.071525 | 0.008441 | 0.006436 | nan | nan |
| MLPIN_SAE | Magicoder/GSM8K | 3.765572 | 3.765572 | 3.765533 | 3.714950 | 3.712700 | 0.011825 | 0.058046 | 0.004273 | 0.004201 | 0.062277 | 0.062209 |
| MLPIN_SAE | Magicoder/MMLU | 4.193459 | 4.193459 | 4.193485 | 4.151814 | 4.156009 | 0.017518 | 0.064872 | 0.005482 | 0.005322 | 0.070433 | 0.070262 |
| MLPIN_SAE | GSM8K/MMLU | 3.649780 | 3.649780 | 3.655132 | 3.730802 | 3.730937 | 0.014323 | 0.058294 | 0.004432 | 0.004316 | 0.062727 | 0.062614 |

## B本源联合结构

| site | dataset | mode | heldout_real_projection | heldout_null_projection | heldout_excess | doc_CI_lo | doc_CI_hi | p_null | Holm_p | mixing_pass | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | position | 0.186106 | 0.097805 | 0.088301 | 0.064902 | 0.110268 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | position | 0.216684 | 0.090062 | 0.126622 | 0.099632 | 0.155953 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | MMLU | position | 0.077154 | 0.027513 | 0.049641 | 0.036945 | 0.062883 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | position_token3 | 0.186106 | 0.102254 | 0.083852 | 0.061037 | 0.105257 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | position_token3 | 0.216684 | 0.092557 | 0.124128 | 0.097466 | 0.153167 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | MMLU | position_token3 | 0.077154 | 0.032407 | 0.044748 | 0.033044 | 0.057352 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | position | 0.383465 | -0.074431 | 0.457896 | 0.431771 | 0.483500 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | position | 0.368308 | 0.053087 | 0.315221 | 0.275806 | 0.354469 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | MMLU | position | 0.171067 | -0.240288 | 0.411355 | 0.399029 | 0.424048 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | position_token3 | 0.383465 | -0.053158 | 0.436623 | 0.410488 | 0.463270 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | position_token3 | 0.368308 | 0.083922 | 0.284386 | 0.246002 | 0.322759 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | MMLU | position_token3 | 0.171067 | -0.207783 | 0.378851 | 0.366457 | 0.390974 | 0.003891 | nan | True | SUPPORTED_STATISTIC |

## B源间差异（两侧保留）

| site | A | B | mode | heldout_A_excess | heldout_B_excess | heldout_difference | doc_CI_lo | doc_CI_hi | p_null | Holm_p | mixing_pass | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | position | 0.049623 | -0.098536 | 0.148159 | 0.120497 | 0.176919 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | MMLU | position | 0.065604 | -0.008821 | 0.074425 | 0.055799 | 0.095029 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | MMLU | position | 0.114482 | -0.016618 | 0.131101 | 0.102118 | 0.160289 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | GSM8K | position_token3 | 0.047050 | -0.096692 | 0.143742 | 0.116514 | 0.172176 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | Magicoder | MMLU | position_token3 | 0.062442 | -0.008735 | 0.071177 | 0.052980 | 0.091847 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| ATTN_SAE | GSM8K | MMLU | position_token3 | 0.112102 | -0.015034 | 0.127136 | 0.098364 | 0.156005 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | GSM8K | position | 0.315661 | -0.085220 | 0.400881 | 0.355508 | 0.447682 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | MMLU | position | 0.236749 | -0.141447 | 0.378195 | 0.347057 | 0.413916 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | MMLU | position | 0.067408 | -0.243117 | 0.310525 | 0.263189 | 0.356736 | 0.003891 | 0.023346 | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | GSM8K | position_token3 | 0.306558 | -0.074816 | 0.381374 | 0.335781 | 0.428185 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | Magicoder | MMLU | position_token3 | 0.233239 | -0.135879 | 0.369119 | 0.338627 | 0.402540 | 0.003891 | nan | True | SUPPORTED_STATISTIC |
| MLPIN_SAE | GSM8K | MMLU | position_token3 | 0.060298 | -0.221665 | 0.281962 | 0.235467 | 0.328211 | 0.003891 | nan | True | SUPPORTED_STATISTIC |

## 实际约束与随机化预算

| site | mode | split | rows_per_source | per_snapshot_strata | checked_snapshots | max_column_error | row_degree | changed_trade_fraction | proposals | moved_edges | mean_abs_retention_error | lowN_strata | total_strata | locked_feature_edges | total_edges |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | position | heldout | 129 | 24 | 6144 | 0 | 32 | 0.999998 | 4617600 | 140577616 | 0.000224 | 0 | 24 | 1032.000000 | 99072 |
| ATTN_SAE | position_token3 | heldout | 129 | 89 | 22784 | 0 | 32 | 0.999993 | 4626480 | 139972208 | 0.002349 | 52 | 89 | 1511.000000 | 99072 |
| MLPIN_SAE | position | heldout | 129 | 24 | 6144 | 0 | 32 | 0.999998 | 4617600 | 121811576 | 0.000321 | 0 | 24 | 1677.000000 | 99072 |
| MLPIN_SAE | position_token3 | heldout | 129 | 89 | 22784 | 0 | 32 | 0.999993 | 4626480 | 120114102 | 0.002084 | 52 | 89 | 3245.000000 | 99072 |


最高Rhat=1.02761321985865；最低ESS=129.93745861364076。完整各统计量见null_mixing.csv，实际成员ID及锁定列在每个constraints.jsonl。

## 认识更新、原文、反例及边界

 Attention的GSM8K候选#17625/#14773，发现集共同出现比例0.214844、本源零模型0.129898；留出真实221/1032位置=0.214147，零模型0.115708，超额0.098440，94/129篇文档至少出现一次。原文例子：On a moonless night, three fireflies danced in the evening breeze.  They were joined by four less than a dozen more fireflies, before two of the fireflies flew away.  How many fireflies remained? 原S08的GSM8K:train:row5923，位置19，token=' by'；两成员原激活分别9.756166、12.859011。这里观察的是两个ID的共现，不给它们自动命名概念。

**相反例子也保留。** MLP输入#20989/#24338在GSM8K发现集中为低于零模型：真实2/1024、参照0.003948；留出却为高于零模型：真实12/1032=0.011628、参照0.003138，共8篇，差0.008490。该单对没有按发现方向复现；主联合向量复现不表示每对稳定。另有发现/留出支持为0的格，不能称为反向。[全部已选12对](tables/B_selected_pairs.csv)与[276对完整分量](tables/B_all276_components.csv)均保留，未只报最显著项。

**零模型实际质量。** 每模式4链×64样本；burn100扫，每10扫取样。主留出每套字典提出4,617,600次行对交易，改变比例>99.999%；所有已检查快照行32/唯一ID和列次数精确满足，最大列误差0。判定统计的Rhat最高1.0276、ESS最低129.9，达到冻结阈值，无需延长。存在无法交换的固定成员：主留出Attention为1032/99072条激活边、MLP输入1677/99072，均已保留并逐层列ID。高交换率不被单独当成充分混合证据。

**仍未排除。** 仅按数据集×分位固定边际；探索额外按发现最常用token ` the`、` of`、`.`及OTHER分层后，联合信号仍为正，但89个层中52个少于8行，部分约束近乎锁定。它没有匹配所有词面或格式。S08主要是格式描述，**没有独立格式匹配**，本轮同样未做。完整长度中位数252/56/50、代码围栏158/257对0/257对0/257、来源/题型/学科/近重复均保留为竞争解释。跨源差异是各自边际条件下的超额共现差，并不是把两源改成相同边际后比较统一依赖参数；可达效应量仍受边际支持范围影响。

区间以文档为单位，给定发现方向和估计零模型中心，不整合发现选择、频率预测误差和所有零模型估计误差；MCSE另列。零模型打破跨位置的文档连贯性，不能理解为自然文本的因果替代。原S08文档已暴露，本轮只保证新候选未用留出联合值筛选，不声称外部新样本复现。Numina仍缺失。没有读出分类、功能或router结论。

[详细报告](detailed_cn.md) · [协议](protocol_cn.md) · [约束](tables/null_constraints_summary.csv) · [混合](tables/null_mixing.csv) · [复算](reproduce.md)。本轮停止，等待审阅。


探索分布：[24成员激活个数](tables/B_member_count_distribution.csv)、[精确组合](tables/B_exact_pattern_distribution.csv)；后者pattern_code的二进制位对应data/feature_universe.json内各字典24ID顺序，OTHER=-1，0为空候选组合，不是feature0。每源每split分母为文档数×8；文档仍是独立单位。
