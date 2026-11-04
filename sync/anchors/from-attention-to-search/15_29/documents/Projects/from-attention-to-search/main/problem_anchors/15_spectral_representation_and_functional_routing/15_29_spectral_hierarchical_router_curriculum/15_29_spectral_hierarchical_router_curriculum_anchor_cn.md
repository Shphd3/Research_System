派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor_cn.md`。
[精确原始文件](../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor_cn.md)；研究修改仍回到原件。

---

# A15_29：渐进谱层级路由监督是否改善固定MoE的学习？

## 1. 问题定义

研究者于2026-10-31固定本轮：头部先监督，随后加入中部、后部的P组，相比从开始使用同一全部层级的F组是否改善学习？两组从同一普通MoE随机初态训练到50B有效预测token。唯一主动差别是中后层级系数随token启用的进度。普通MoE作参考，P与F隔离这一固定课程，不把它解释为所有teacher方法的效益。

## 2. 物理先验

冻结33B Dense提供上下文FFN输入。中心化协方差的谱序表示方差，不是激活频率或语义粗细。人为二叉分组是否有路由价值仍需检验；子空间稳定不推出分组稳定。1031谱解释分析未建立普遍粗细谱排序。

## 3. 可证伪假设

P可能因推迟深层约束而获益；竞争解释是从开始获得相同深层信息同样好或更好。匹配验证loss轨迹上P更低，仅描述性支持本seed的这套课程；P相同或更差削弱它。目标塌缩、不稳定、曝光不匹配或恢复失败使比较证据不足。跨seed稳定和天然语义层级均未验证。

## 4. 数学模型

teacher第i层、t位置h为实际学习型norm2之后的FFN输入。A拟合均值和协方差，1024维按特征值下降，在128、512处分段，只允许按记录规则作邻近谱间隙调整。各段用固定整体RMS尺度，不逐token单位化，也不按极小特征值倒数白化。头部二分，中部每父组二分，后部每中组二分形成8叶；节点概率为负平方距离除温度后的softmax，子节点对所有位置使用父组软权重拟合。叶编号4a+2b+c固定，父概率由叶求和。

teacher叶分布q与student未加bias的8维softmax p定义：

\[
D_H=\mathrm{KL}(q_a\Vert p_a),\quad
D_M=\sum_aq_a\mathrm{KL}(q_{b|a}\Vert p_{b|a}),\quad
D_T=\sum_{a,b}q_{ab}\mathrm{KL}(q_{c|ab}\Vert p_{c|ab}).
\]

链式分解满足\(D_H+D_M+D_T=\mathrm{KL}(q_{abc}\Vert p_{abc})\)，没有重复相加父级KL。总目标为

\[
L=L_{LM}+\lambda(N)(D_H+\gamma_M(N)D_M+\gamma_T(N)D_T).
\]

按有效位置和8层平均。N为本次更新前已完成的有效token；监督分支对student FFN输入停止梯度，直接仅更新router，LM仍联合训练主干、专家及router。teacher、树全部冻结。loss-free bias只作用于选专家，不进入监督概率。

所有节点从加权中位数初始化，只执行一次最近中心重分配和加权中心更新。根沿头段第一谱方向初始化，中后段沿原隐藏状态固定坐标的投影初始化。子拟合使用全部样本并按父软概率加权。此规则限制中心漂移，不宣称无约束 kmeans 最优。

## 5. 计算实现

复用修正baseline的模型、DCLM packing、4参考rank的样本及mask顺序、优化器、warmup后constant LR和精确保存里程碑。student507988992参数，8层、hidden1024、每层8个1536宽独立专家、top2、无共享专家。最终v5校准A/B/C5为262144/262144/16384位置，物理文档和完整2048token上下文互不交叉。A拟合生产树，B独立重拟合，C复核目标概率和文档支持。B仅在A上选择保持树结构的子节点交换，C不用于配准。在线teacher使用与student相同因果输入，不物化50B缓存。

## 6. 最小证伪检验

正式前要求KL链式一致、监督梯度只到router、零监督时LM路径一致、2/4/8rank mask一致、teacher前缀因果性、目标独立稳定性、GPU有限更新、无丢分配、虚拟token阶段边界及两组各自真实退出全部训练进程后的恢复对照。工程阈值及限制见Protocol。P/F按相同token点验证loss比较，P减F的符号仅作本seed描述，不能宣称跨seed显著性。缺少配对验证不得用训练loss替代。

## 7. 当前证据

已核对精确teacher实际hash、CPU加载及前缀因果性，冻结校准上下文并通过CPU合同检查。树拟合和GPU执行实际状态由Detailed及执行回执拥有，尚无P/F训练结论。实际5090访问已验证。v5八层离线目标均通过；两卡资格作业om-to4cwwnz已通过GPU因果性、梯度及目标重算检查，正在测吞吐和两组真实进程重启恢复。v1–v4失败保留。两个正式作业共享8卡的调度机制仍未核实。1031分析只作为动机，保留原否定或不足边界。

## 8. 主张边界与下一决策

本轮检验固定的人为谱课程，不证明天然语义层级、自适应收敛切换或跨seed稳健性。研究者已授权实现、离线拟合、2卡RTX5090spot smoke和通过后顺序提交两个8卡RTX5090spot的50B任务，保留普通baseline。当前操作决策为实际工程门及共享8卡上限是否核实；全部通过才正式提交。后续科研判断仍由研究者在配对结果后作出。

[Protocol](../../../experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/protocol.md) · [Detailed](../../../experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/detailed.md) · [Baseline](../../../../../../../UNAVAILABLE.md) · [1031 spectral analysis](../../../../../../../UNAVAILABLE.md)
