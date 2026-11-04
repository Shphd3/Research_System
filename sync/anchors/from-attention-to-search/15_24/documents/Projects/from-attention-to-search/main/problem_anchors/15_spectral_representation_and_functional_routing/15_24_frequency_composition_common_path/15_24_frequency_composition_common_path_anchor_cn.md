派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor_cn.md`。
[精确原始文件](../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor_cn.md)；研究修改仍回到原件。

---

# Anchor：频率混合表征与高频路径的调用

## 1. Problem Definition

总任务是在固定计算预算下建立更有效的按feature频率分发方式。现有事实是同一输入会同时含多个频段，评分校准改善目标接收但旧学习未改善；均值相减与比值不同，不能把高频称为全部common。导师进一步问：独特成分能否使用一部分已学共同计算。冻结Base始终保留，故本轮只研究新增残差FFN的调用与更新，不能说原架构删掉了共同能力。

**本轮唯一决策问题：在相同top2和专家预算下，保留一条预指定高频路径，相比动态选择两条路径，是否改善低频输入的留出学习；这一增量是否依赖按频率组织的名单？** 先分析token、feature、几何和暴露，后按预定门槛学习检验。静态覆盖只能诊断路由，不能替代NLL。

这是用户授权的自主探索具体化。研究者已授权建模、分析后必要学习、4H100 Reserved；下列模型与设计是AI在该范围内的明确操作化，不代表导师已认可机制。不新建或重置Focus；最终科学判断Unknown。

## 2. Physical Priors

1. 输入可能携带多频段成分，但共现不等于统计依赖或共同学习相容；Base仍提供共同计算。【导师直觉＋既有证据，机制待检验】
2. 非负字典幅度是路由代理，真实表征向量可抵消，均值与中心化PCA是不同对象。【定义与数学关系】
3. 路由改变新增专家接收的样本与更新次数；增益可能来自一般共享/负载，而非频率特有语义。【竞争解释】

## 3. Falsifiable Hypotheses

H-T：固定当前token身份后，feature激活和频率组成仍随上下文变化；若同ID条件预测已几乎完全解释复核变化、或支持不足，则相应解释减弱/不足。下一token只作解释标签，不进入路由。

H-G：高频段可能承担中心化表征的主要变化方向，即使它并非原始均值的正向主体；用真实h的TRAIN PCA与有符号投影检验，不以decoder范数代替。

H-L：强制保留高频路径的低频留出NLL增量ΔT为负，且相对匹配随机名单的交互I为负。若ΔT≥0则未改善；只有I<0但ΔT≥0只能说较少恶化；有限种子区间跨0记不足。负结果保留，不调整路由/预算追结果。

## 4. Mathematical Model

位置t含当前token和可见前文，预测y_t=token(t+1)。共享z由冻结14层联合编码。h为真实第28层residual-post；d_i为还原原坐标的该层decoder，b含预处理均值。

\[
h_t=b+\sum_{j=1}^4v_j(t)+v_U(t)+e_t,\quad v_j(t)=\sum_{i\in B_j}z_i(t)d_i,\quad p_i=P_{TRAIN}(z_i>0).
\]

这是重建加残差的定义，不假设原子正交。中心化后方差含频段交叉项，不能把各段幅度之和当能量。TRAIN中心化PCA基U_k来自真实h，k=1,16。几何量为η_i=||U_k^Td_i||²/||d_i||²；实际有符号投影为β_j=E< U_k^Tδv_j,U_k^Tδh>/E||U_k^Tδh||²，残差一起加和为1。η描述方向，β包含真实激活；都不直接证明优化主导或语义功能。

令c_i=z_i||d_i||，M_j=Σ_{B_j}c_i，a_j=E_TRAIN M_j。F选择M/a最大的两个不同组对，各对选原始子组幅度最大者；H强制索引3组对一个，再选其余3对最高者。两条路径恒定各1/2权重，完整h不投影、不删common。

\[
h'_t=h_t+\frac{s_h}{2}\{f_{r_1(t)}(h_t/s_h)+f_{r_2(t)}(h_t/s_h)\}.
\]

s_h仅由TRAIN估计，8个普通FFN参数全部可训练，基座/头/字典冻结；down零初始，初始logits等价。T名单按原四频段，每段用固定哈希均分两子组，避免继承旧φ关系及单项子组；R全池随机分配并精确匹配8组人数。频率段仍是原对数等宽，不是等人数频率分箱。

四臂T_F/T_H/R_F/R_H在相同数据、初始化、top2、宽度、步数下比较。

\[
\Delta_T=L(T_H)-L(T_F),\quad \Delta_R=L(R_H)-L(R_F),\quad I=\Delta_T-\Delta_R.
\]

L为共同T-B1 feature集合的DEV逐feature平均NLL，另报位置平均及整体。I不是common中介效应；调用、负载与更新暴露是共同变化的策略效果。两seed只作探索性判断。

## 5. Computational Realization

1. 复用相同TRAIN/EVAL/DEV缓存，完整核对h/z/token/target/位置。TRAIN定义频率、名单、分数、代理标签和PCA，随后同型复核。
2. 全feature统计当前/目标token对应；同token上下文变化、随机/高激活/同ID未激活文本；支持不足保留。全量低频每项仅1–17次TRAIN命中，不宣称稳定单义。
3. 新名单和四路由精确计数、q/r恒等式与多频段混合；旧top1失败与同预算事后oracle仅作诊断。F/H若完全等价复用结果，不重复训练。
4. 静态证据留下“不同更新分配是否有学习差异”这一缺口且代码资格通过时，提交4H100 Reserved，训练四臂两seed同预算1epoch，统一最终DEV揭示；不按DEV改路由、步数或选赢家。

## 6. Minimal Falsification Tests

H-T以TRAIN条件统计对EVAL与DEV预测及同ID激活异质性区分词汇身份解释；有限支持记不足。H-G用真实h PCA、频段向量投影和残差/交叉项区分幅度大与真实方向承载。H-L的主比较是ΔT与I，低NLL为好；需二者同向支持，不能用“相对较少恶化”写成学习更好。

学习门槛：路由实际不同、每位置2个不同专家、完整输入相同、预处理及分母正确，zero旁支/梯度/样本拟合/保存恢复检查通过。该门槛不要求先观察H比分发更漂亮。若全部训练条件异常恶化，先做既定共同LR有界诊断，保留未完成/失败，不无限扩展条件。

## 7. Current Evidence

旧末层幅度路由0→72.22%的低频接收，不认证学习。减均值17.58%，其中87.33%送入低频段的位置无原B1激活。原h均值与高频平均向量有符号投影为负；中心化重编码MSE变差。完整来源见旧bridge与mean记录，原结果不覆盖。

本轮结果尚未计算，不能预填成功。两份会议有18类intuition，逐条可检验性台账放本轮Detailed附录；容量倍数、学习率优越、大模型优越、attention生成因果与参数谱主导不由这些静态统计裁定。

## 8. Claim Boundary And Next Decision

最多裁定当前冻结表示、SFT数据与top2预算下的分发/学习增量。不是从头预训练容量、知识难度、语义单义、φ学习效用、梯度干扰或common机制证明。DEV是原语料的新固定复核面板而非独立外部测试，近重复未知。唯一下一决策是保留哪种明确频率调用假设，或在阴性/不足时停止该解释；不自动扩大训练或换数据追正结果。
