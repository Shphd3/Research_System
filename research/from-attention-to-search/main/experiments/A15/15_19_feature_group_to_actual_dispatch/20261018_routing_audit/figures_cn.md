# 四张图怎么读

四图均读取已经保存的表，不重新提取激活或训练。每图有PNG、可放大的SVG和PDF；[完整产物与来源manifest](payload_manifest.json)。英文图面术语在下面解释。

## 图1：实际接收与负责目标零接收

![实际接收](figures/figure1_actual_reception.png)

上排横轴是专家编号，纵轴是全部TRAIN有效输入中进入该专家的比例（%）；下排纵轴是该专家名单内、没有任何命中进入负责专家的feature比例（%）。Original是原路由；C score terms zero仅表示高频C的评分项置零，输入表征没有变。A/B1/B2各用自己的名单和路由；expert编号不表示跨规则相同语义。

看什么：原A输入集中，三个专家完全为空；删C后全部去0，暴露出退化。不能推出什么：非空或均衡即学习好、删C是一种有效策略。上下两排分母不同，不可混读。

来源：执行侧 `metrics/score/expert_loads_original_and_C_zero.csv` 与 `feature_owner_original_and_C_zero.csv`；筛选split=TRAIN，分rule、expert。N=130,712，名单池9,615，具体每组人数见[expert表](tables/expert_summary.csv)。

## 图2：全局频率与负责专家内频率

![全局与负责专家内频率](figures/figure2_global_vs_owner_frequency.png)

横轴Global activation frequency p是feature在全部有效位置中出现的比例；纵轴Frequency inside assigned expert q是进入名单指定专家的位置中含该feature的比例，两轴均为线性百分比。Assigned expert指负责专家；不是“接收最多的专家”。Low-frequency为冻结低频964项，Other为其余可靠项。q=p虚线表示没有相对全局频率的富集。

看什么：A只有55项负责专家q可定义，30项确实为0，其余9,560项因负责专家无输入而NA，不在散点中伪造零。B仍有大量低频项q低或为0。不能推出什么：NA项被证明无用；q增大代表预测学得更好。

来源：执行侧 `metrics/core/feature_owner_summary.csv`，split／rule分面，横轴p_i、纵轴owner_q，缺项原因owner_q_NA_reason。每分面同9,615项；TRAIN N=130,712，EVAL N=65,402。

## 图3：目标与伴随高频项进入专家后的频率

![目标与伴随项](figures/figure3_target_common.png)

每行一个固定目标feature，U是目标本身，C:ID是原高频名单中的伴随feature。C不表示通用语义、主成分或噪声。三个C按TRAIN P(c|i)选定；纵轴为EVAL专家内频率q（%）。N_e是该专家接收位置数，n_U是目标在全部EVAL的命中数。

Assigned为名单负责专家；Most receiving是目标实际最常到达的专家。A的左列负责专家0没有输入，所以全部q不可估计；第二列显示实际主要接收专家7，不能把它重新命名成负责专家。B列用各自名单。不要把分母不同的柱高直接解释成策略学习效果。

看什么：输入到专家后，目标与伴随项分别多常见，以及空专家为何不能谈q。不能推出什么：伴随项必须删除、同频最优或少数案例代表全体。

来源：[108行绘图表](tables/case_common_plot_source.csv)，字段expert_role／expert／N_expert／n_expert_i与n_expert_c／q_i与q_c，TRAIN冻结选择记录在执行侧 `metrics/cases/case_common_plot_selection_train.json`。三个目标EVAL支持分别162、145、111，图中同时给分母。

## 图4：文本位置和原评分

![文本评分](figures/figure4_text_and_score.png)

每列取一个ID的第一条冻结随机命中。Prefix是模型可见前文的截短显示；Current token是当前输入token；Next target是下一token标签，只用于解释，不参与当前路由。下排Group／expert为原名单组编号，Original score是原分母下的decoder范数加权平均激活分数，无概率单位。Assigned表示目标名单负责组，Winner表示分数最高的实际去向。

看什么：目标确实在当前输入中激活，但目标所属A0得分远低于A7，完整输入仍送A7。不能推出什么：下一标签已被模型看见；目标无用；单个词就是该feature的完整语义。

来源：执行侧 `texts/text_cases.json`、`metrics/cases/text_case_scores.csv`、`text_sampling.json`。完整12张随机／高激活卡见[文本附录](text_cases_cn.md)，含可见前文、原bin、位置、组分、伴随feature和移除U评分项的局部检查。

## 统一术语

- feature（特征）：固定CrossCoder联合编码的一个编号，不是一条已认证知识。
- 负责专家：名单为feature指定的专家。实际接收专家：当前完整输入真正到达的专家。
- 激活频率p：全部位置中feature出现的比例。专家内频率q：该专家输入中feature出现的比例。
- 接收率a：含feature的位置中，进入指定专家的比例。负载：全部位置中进入该专家的比例。
- NA：定义所需分母为0或缺项，不是0。零接收：feature出现过，但负责专家没有收到其命中。
- C：原TRAIN高频962项名单，非“所有输入共有”；U：当前案例目标。
- TRAIN／EVAL：本轮固定训练侧／留出位置侧。上下文是1024-token切块，非已确认独立文档。
