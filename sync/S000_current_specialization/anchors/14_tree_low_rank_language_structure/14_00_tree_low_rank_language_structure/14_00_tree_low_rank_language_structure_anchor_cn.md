# A14_00：层次语言组合何时保持共享低秩状态？

Thinking Card：
[14_00_tree_low_rank_language_structure_thinking_card_cn.md](14_00_tree_low_rank_language_structure_thinking_card_cn.md)

## 1. 问题定义

节点状态是一个树节点的 $d$ 维向量 $h_v$；秩只定义在跨多棵树、同一树层或同一尺度节点堆叠得到的矩阵 $H_\ell$ 上。单个节点或单个根向量的秩恒不超过 1，不是研究对象。

主要低秩误差为

$$
\tau_k(H)=\frac{\sum_{i>k}\sigma_i(H)^2}{\sum_i\sigma_i(H)^2},
$$

95% 能量秩为 $r_{0.05}(H)=\min\{k:\tau_k(H)\le0.05\}$。

**唯一决策问题：**共享低维叶子状态与稳定层次组合，是否能对合成树、真实成分结构和预训练语言模型中的低秩节点表示给出非空泛解释？

## 2. 物理先验

1. 局部语言因素的复用使不同叶子短语靠近共享低维仿射空间。
2. 父节点主要变换和聚合子节点状态，而不是每个节点都创建新的独立坐标系。
3. 若层次结构是原因，树特异压缩应在训练后出现，并在保持 token 边际和长度、破坏层次关系时减弱。

只有下面的条件传播结论是定理；这些先验需要实验判断。

## 3. 可证伪假设

**主假设：**叶子存在共享 rank-$k$ 逼近且组合创新有界时，每层最佳 rank-$k$ 误差受递归稳定项控制；真实表示中，真树节点应比匹配伪树有更低 held-out 有效秩和更低共享组合残差。

**最强替代解释：**表面低秩由样本形状、长度、pooling、全局均值、位置、异常维度、架构或 probe 容量造成，真实父子关系没有额外解释力。

- Pass：数值定理校验无越界；真实叶子子空间可泛化；真实树的压缩和组合优势为正；层次干预改变秩。
- Fail：实现与能力检查通过，但真树优势为零或反向，层次干预也无效。
- Insufficient：$n<d$ 造成形状低秩；效应在中心化/长度控制后消失；初始化已有同等效应；或能力无法匹配。

## 4. 数学模型

设

$$
H_{\ell+1}=A_\ell H_\ell W_\ell^\top+E_{\ell+1}.
$$

定义

$$
\Delta_k(H)=\min_{\operatorname{rank}(S)\le k}\|H-S\|_F,
$$

以及

$$
g_\ell=\|A_\ell\|_2\|W_\ell\|_2,
\quad
B_0=\Delta_k(H_0),
\quad
B_{\ell+1}=g_\ell B_\ell+\|E_{\ell+1}\|_F.
$$

**定理：**对所有 $\ell$，$\Delta_k(H_\ell)\le B_\ell$。若 $B_\ell^2\le\eta\|H_\ell\|_F^2$，则 $r_\eta(H_\ell)\le k$。

**证明：**取 $H_0=S_0+R_0$，其中 $\operatorname{rank}(S_0)\le k$ 且 $\|R_0\|_F=\Delta_k(H_0)$。递归定义 $S_{\ell+1}=A_\ell S_\ell W_\ell^\top$，矩阵乘法不增加秩，所以所有 $S_\ell$ 的秩不超过 $k$。令 $R_\ell=H_\ell-S_\ell$，则

$$
R_{\ell+1}=A_\ell R_\ell W_\ell^\top+E_{\ell+1}.
$$

由范数次乘性，

$$
\|R_{\ell+1}\|_F
\le g_\ell\|R_\ell\|_F+\|E_{\ell+1}\|_F
\le B_{\ell+1}.
$$

归纳得到 $\|R_\ell\|_F\le B_\ell$；由于 $S_\ell$ 是合法 rank-$k$ 逼近，$\Delta_k(H_\ell)\le\|R_\ell\|_F\le B_\ell$。证毕。

## 5. 计算实现

证据链分七步：精确/含噪合成校验；必要条件反例；使用 full-dimensional PPMI 的真实 gold constituency 树；使用共同单 token readout 的预训练 decoder-only 模型；层次语料与叶子打乱语料上的匹配小模型训练；固定同一父节点和全部 token 的替代切分；对每个父节点等权使用左右两个替代边界。

主表示不使用 mean pooling；mean pooling 只作为诊断。所有数据按整棵树或完整句子划分，$k$ 只在训练叶子上选择并在高层冻结。

## 6. 最小证伪测试

1. 任意理论界越界即说明实现不一致。
2. 真实叶子不优于同长度非成分片段，则共享叶子空间前提不获支持。
3. 预训练 final 的真树压缩差不存在或 step0 已同样存在，则训练所得树特异解释不获支持。
4. 真父子边不优于置换边，则共享组合条款不获支持。
5. 层次/打乱干预在能力匹配后不改变秩，则缺乏因果证据。
6. 固定父内容后，真实切分不优于替代切分，则原优势主要来自内容包含。
7. 等权左右替代边界消除效应，则真实切分优势依赖边界方向而非模型一般机制。

## 7. 当前证据

0623 归档受控实验只提供一个机制先验：不同新增组合特征可共享 $W_Q/W_K/W_{\mathrm{out}}$ 高增益子空间，而 $W_V$ 集中较弱。它不是自然语言或真实大模型证据。

当前注册证据链已经完成：

| 审计 | 判定 | 直接证据 |
| --- | --- | --- |
| [E01 理论/合成](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E01_theory_synthetic/summary.md) | 通过 | 最大归一化越界 $2.92\times10^{-8}$，17 个反例全部复现 |
| [E02 金标准句法 + PPMI](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E02_gold_syntax_ppmi/summary.md) | 已归档／证据不足 | 真实成分投影优势 34.2%，但 $r_{0.05}/d=32.1\%$ 未过 25% 门槛 |
| [E03 预训练解码器](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E03_pretrained_tree_geometry/summary.md) | 已归档／证据不足 | Qwen 叶子/组合差异为正且训练后增强，但界比为 10.80；Pythia 不复现训练增量 |
| [E04 因果干预](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E04_causal_hierarchy_training/summary.md) | 已归档／证据不足 | 全配对描述性树效应 $+0.180$、组合效应 $-0.047$、秩相关 0.949，且非空泛界为 0/48 |
| [E05 同父节点切分](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E05_same_parent_split_stability/summary.md) | 已归档／证据不足 | Qwen 切分优势 $-0.0415$；Pythia $+0.1486$ 但随边界方向反转；Qwen 最小界比 1.3369 |
| [E06 双侧切分](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/boundary/A14_E06_two_sided_split_robustness/summary.md) | 边界证据 | 等权后 Qwen/Pythia 效应为 $+0.0064/-0.0001$，预测—稳定兼容点为 0 |
| [E07 可达空间核算](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E07_reachable_space_accounting/summary.md) | 通过 | 950 条登记记录全部精确匹配维数恒等式，7 个负对照全部通过 |
| [E08 参数—状态桥](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E08_relation_reuse_state_bridge/summary_cn.md) | 证据不足／独立重建有条件为正 | 无法完成来源重放；独立重建的极端状态秩为 13/10/10 对 16/13/12，但中间条件不单调，QK 差远大于状态差 |
| [A14_02 ROOT 秩与桥接链](../14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md) | 混合；有限桥得到支持 | E01/E02 未建立 shared 组合能力；E04 在 5/5 支持局部 H9；E06 在 5/5 否定有限位移的单点线性化，而真实 learned secant 通过八维功能守卫 |

跨实验可确认：真树跨度存在共享子空间几何，受控层次顺序可以使树边界对齐压缩
从近零初始差异中出现。E05 固定父内容后，Qwen 没有注册的真实切分优势，Pythia
效应随边界移动方向反转；E06 在每个父节点内等权左右方向后，两个预训练效应都接近
零。随机初始化效应仍然很大，所有真实/训练稳定界仍为空泛。

## 8. 主张边界与下一决策

本定理不证明真实语言是树、叶子天然低秩、注意力严格实现该线性组合，或低能量空间被行为使用。真实语料结论依赖标注与表示；预训练结果依赖模型；合成训练只能建立受控机制可能性。

当前裁决是：定理在数学上正确，树对齐子空间压缩也有经验桥梁，但全局稳定共享线性
传播机制没有得到支持。固定内容和方向平衡的对照都没有产生模型一般的真实切分优势，
所有训练/预训练注册界也都为空泛。E08 只增加了一条 toy 独立重建中的极端复合条件
到任务状态功能秩的桥；它没有重新打开全局主张，也没有分离频率。

E08 独立重建保留为有边界的 standalone evidence；原始来源重放仍是证据不足。
A14_02 的 E01 确定了两条受控诊断：重复相同样本没有形成新 context 不变性；
在能力通过的 lookup 任务中，独立映射数从 1、4、16 增加时，ROOT 功能秩均值
从 10.2、11.0、12.8 上升。E02 随后在 0/5 seeds 通过 shared 未见组件重组门，
因此 shared 组合结构本身仍未得到裁定。E04--E06 则确定了桥接边界：训练点的
共享 Jacobian 像可以是局部低维的，但一个 endpoint/reference Jacobian 不能
代表完整训练位移；受控模型中的真实 learned ROOT secant 仍然有效八维且功能
充分，所以有限训练采用 secant／path-integrated image。
[A14_03](../14_03_state_parameter_functional_rank_demand/14_03_state_parameter_functional_rank_demand_anchor_cn.md)
是被 A14_02 阻塞的候选后继：只有 A14_02 先建立稳定且任务充分的状态秩差异，
它才检验该差异是否因果地要求已注册参数算子的更多功能方向。

**唯一下一决策：**先构造一个通过组合能力门的 shared 任务表面，再重新检验规则
复用是否因果地降低功能秩。A14 的全局共享线性传播主张继续关闭；有限训练桥保持
为 secant／path-integrated image；Router protocol 仍不属于本轮决策。
