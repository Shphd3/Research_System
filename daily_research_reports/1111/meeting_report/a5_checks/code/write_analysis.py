from common import *
import pandas as pd

def read(name):return pd.read_csv(R/f'results/{name}.csv')
def raw(name,cols=None):
 d=read(name)
 if cols is not None:d=d[cols]
 return d.to_markdown(index=False,floatfmt='.6f')
def main():
 hint=read('check1_hint_probes');info=read('check1a_route_information');lead=read('check2_step_lead');boot=read('check3_document_bootstrap');bias=read('check4_bias_rule');gates=read('check5_layer_gates');st=R/'evidence/check6a_complete.json';sd=R/'evidence/check6b_complete.json'
 text='''# A5增益来源：详细结果与判读（AI分析）

研究者判断：Unknown。协议规则在运行前冻结，原SHA见evidence/protocol_freeze.json；用户随后接受A1既有约9.91e-6nat数值微差并要求继续。本轮不改变R04结论记录；下面的新证据单独归属本轮。全部主模型冻结，仅训练小探针和稀疏字典。

## 检查1：没有在冻结的小探针中检测到足以解释A5优势的增量提示收益。

'''
 text+=hint[hint.band=='overall'][['host','distribution','I_X','real_probe_nll','shuffled_probe_nll','delta_hint']].to_markdown(index=False,floatfmt='.9f')+'\n\n'
 z=json.load(open(R/'evidence/check1_complete.json'));text+=f'''预登记规则套用：以A0宿主为准，A5的 $\Delta^{{hint}}={z['delta_A5']:.9f}$ nat ≤0.010，归为“泄露不是主要解释”；与A1提示量之差为{z['extra_A5_minus_A1']:+.9f}nat，占0.1185的有符号比为{z['ratio_to_01185']:.3%}。差值为负，未观察到正的提示解释比例，不能把负值解释为负信息。

读法：$I_X$ 是按分发分组的有限样本条件unigram在留出集上的改善，并非精确互信息；随机A2可因分组估计方差而为负。A0-L7的 $I_X$ 高于A5，但它来自宿主自身表征，不能把该信息量直接当成teacher泄露。主判据是相同冻结宿主上的real/shuffled独立训练配对。

边界：g为输入h和28维onehot的1024宽残差MLP，只训练固定524288个DEV位置、1epoch512updates；超参数未根据结果调整。阴性只约束这一预登记探针，不能给所有解码器的泄露能力作上界。h缓存fp16、冻结head bf16；real/shuffled共享相同精度。A0宿主配A0-L7及A1宿主配A1这两格先前已使用过对应分发，不是理想“未用过分发”控制；按用户指定矩阵保留，主要判断仍是未训练A5分发的A0宿主。

![提示量按频段](check1_hint_by_frequency.png)

原表：[check1_hint_probes.csv](check1_hint_probes.csv)含宿主×分发×11频段；[check1a_route_information.csv](check1a_route_information.csv)；各probe原始训练loss另在执行根probes/*_metrics.csv。

## 检查2：nat差缩小未对应可观测晚期步数领先的持续缩小，但终点删失阻止完整1000–2000判定。

'''
 text+=lead[(lead.metric=='EVAL_NLL')&(lead.band=='overall')&(lead.step>=1000)].to_markdown(index=False,floatfmt='.6f')+'\n\n'
 text+='''预登记规则套用：可见EVAL区间A5相对A0的领先约85.5→149.5→181.8→160.9步，不是持续下降；相对A1约141.3→281.2→396.1步后删失。训练CE晚期领先也有明显非单调变化，不强判持平或持续下降。所有晚期有效点的线性斜率为正，但终点t′超出2000，完整区间判读保留不足；不补造归零步数。对确实观测到持续下降的局部分频段，原表保留OLS归零外推，并明确外推而非实测。

![等loss领先](check2_overall_lead.png)

三角与向上箭头仅表示领先量下界，尤其2000步的下界0不表示实际领先为0。首次达到时间使用比较臂累计最小loss曲线作线性插值；它不假定不同训练步的样本难度恒定。原表：[check2_step_lead.csv](check2_step_lead.csv)、[check2_lead_trend.csv](check2_lead_trend.csv)；[双比较臂频段图](check2_frequency_lead.png)。

## 检查3：固定种子2000步的A5优势明显大于当前EVAL文档抽样误差。

'''
 text+=boot[boot.band=='overall'][['step','pair','paired_difference','ci95_low','ci95_high','documents']].to_markdown(index=False,floatfmt='.9f')+'\n\n'
 text+='''预登记规则套用：这些配对文档95%区间只反映给定模型的评估文档抽样，种子方差仍为Unknown；不能把不跨0改写成跨初始化可复现。文档从EOS恢复，共1871个有观察位置的文档块，不以2048序列替代文档。每次重抽样对所有臂和频段使用相同文档计数，共2000次；总体按位置加权，频段按该bin原子激活次数加权，和R04原条件NLL一致。

![文档块bootstrap](check3_bootstrap.png)

原表：[check3_document_bootstrap.csv](check3_document_bootstrap.csv)含1000/1500/2000×3对比×11频段。数值使用原fp16逐位置loss，与未量化训练评估的差另列original_eval_difference；A1原缓存微差已获用户接受，未做“校正”或修改旧结果。

## 检查4：A1受bias干扰的幅度大于A5，原子分组身份与分数／bias效应仍未分离。

'''
 text+=bias.to_markdown(index=False,floatfmt='.9f')+'\n\n'
 text+='''预登记规则套用：A5相对变化<10%，A1>10%，因此单列“A1一部分劣势来自bias干扰”的操作性证据；它直接测到的是硬分发集中度的干扰，并没有反事实量化这部分造成多少NLL劣势。将score/bias匹配后再比较仍属于未来干预；不能把总体M的下降泛化到所有低频原子，例如A1的bin0反而由约0.6596升至0.7393，完整分频表保留这一反向读数。

[check4_score_bias.csv](check4_score_bias.csv)逐层给margin/bias极差及bias改变Top2比例；[check4_combinations.csv](check4_combinations.csv)含28组合全频数与[组合图](check4_score_combinations.png)。[check4_concentration_variants.csv](check4_concentration_variants.csv)包含b0、actual、b0/actual Top1及D2 weighted变体、全部10bin；Top1随机基准k/E变为0.125，weighted也改变估计量，不能混为同一hard M。

原子分组：[check4_atom_groups.csv](check4_atom_groups.csv)的质量定义为DEV中Σz_j占全部正激活幅值的比例，沿用原A5质量平衡定义，不是互斥token比例；各组频率分布列出DEV十bin原子数及p分位。[check4_group_top_atoms.csv](check4_group_top_atoms.csv)使用真正全局atom ID，富集=P(组专家进入b0 Top2|原子激活)/P(组专家进入Top2)，只在自身组成员中选Top10；[check4_group_contexts.csv](check4_group_contexts.csv)每原子3个最强DEV激活例子。组标签不被预先当作语义类别。

缺失的A5/A0相关已补：[check4_A5_A0_spearman.csv](check4_A5_A0_spearman.csv)，500/1000/1500/2000，全体与10bin，$G_j=NLL_{A0,j}-NLL_{A5,j}$，$\Delta_j=\log M_{A5,j}-\log M_{A0,j}$。该相关仍非因果中介检验。

## 检查5：A6层间异质性很强，六个塌缩层整体没有满足>80% bias改变与gate退化的联合阈值。

'''
 text+=gates[gates.arm=='A6'][['layer','collapsed_from_R04','max_gate_q10','max_gate_median','max_gate_q90','selected_raw_mass_median','bias_changes_top2','hard_M_median','flip_1000_2000']].to_markdown(index=False,floatfmt='.6f')+'\n\n'
 text+='''预登记规则套用：六层合并bias改变率70.17%<80%，故不对全部A6强判“实际路由变成由bias驱动”。逐层L6/L7同时满足>80%和median(maxgate)≥0.95；L4/L5的bias影响约100%，但maxgate中位数约0.84/0.78；L1/L3的gate接近1，但bias影响较低。原概率塌缩不必然意味着所有层的硬选择都由bias决定。

AI分析：硬Top2 M把两个选中专家按相同assignment计算，即使其中一个gate几乎为0；因此相近硬M可以对应不同有效混合。L4/L5则在原最高概率专家被bias排除时，所选原概率质量很低。两种模式都与“soft H3下降不等于硬分工改善”相容，但仍未独立识别NLL损失的中介。

[check5_layer_gates.csv](check5_layer_gates.csv)含A0逐层对照；[check5_layer_groups.csv](check5_layer_groups.csv)用同一L1/3/4/5/6/7和L0/2分组比较A0，组M先按原子对层平均再取中位数，不能把所有层×原子摊平。[七臂散点原表](check5_seven_arm_scatter.csv)和图：

![七臂代理和NLL](check5_scatter.png)

前向gate来自用户指定权重快照（A6 bf16），原硬M/跨checkpoint翻转来自R04原评估缓存；这些是有明确来源的诊断拼合，不声称bf16前向与原FP32状态逐位一致。

## 检查6：student自行产生A5式分发的预检

'''
 if st.exists():
  d=read('check6a_readability');rules=read('check6a_rules');text+='### 6a：可读性探针\n\n'+d[['step','layer','probe','exact_set_accuracy','at_least_one_expert','Mbar_median']].to_markdown(index=False,floatfmt='.6f')+'\n\n'+rules.to_markdown(index=False,floatfmt='.6f')+'\n\n原10个百分点／L7>60%规则逐项套用见表；这里的“必要”和“可行”是原提示中的操作性判读，不是对所有线性函数不可能的证明，也不是蒸馏后语言模型NLL收益；这里线性探针为28类分类器，并不等价于原生8个logit再Top2的router。全部DEV训练、EVAL测试，未按结果调参；L7 MLP至少一个expert一致率为97.3%–99.0%，说明存在部分可读信息，未达到60%完整集合阈值不等于完全不可读。\n\n![student可读性](check6a_readability.png)\n\n'
 else:text+='6a尚未完成，不代填结果。\n\n'
 if sd.exists():
  d=read('check6b_bootstrap_atoms');text+='### 6b：独立student稀疏字典\n\n'+d[['step','layer','updates','training_seconds','Mbar_median','top2_exact_after_hungarian','top2_overlap_fraction','I_X','normalized_reconstruction_error','dead_atom_fraction','rule']].to_markdown(index=False,floatfmt='.6f')+'\n\n预登记1.08和1.01阈值逐配置套用见rule列；teacher坐标中的M是比较接口，不用于student字典训练。字典重建在DEV均值中心化及固定标量RMS尺度下报告normalized MSE；死原子按完整EVAL未出现定义。谱图边权、kmeans及boundary-move平衡全部复用A5源，仅宽度适配8192；具体源停止条件为最大相对质量偏差≤20%，0.80–1.05是原A5观察范围，实际偏差已在protocol末尾记录；谱求解固定2000迭代/原tol，实际eigen_residual_max约6e-5–1e-4亦保留在原表，没有观察结果后增加迭代或更换聚类。匈牙利使用EVAL集合共现来比较组号，报告的是对齐后的重合而非未经对齐预测。\n\n![student自举](check6b_bootstrap.png)\n\n'
 else:text+='6b尚未完成，不代填结果。\n\n'
 text+='''## 下一步讨论（AI建议，尚未执行）

当前最应区分的是A5的原子组身份与分数尺度／bias接口，而不是将它直接升级为已识别的“更好分工”机制。AI建议优先设计在DEV预先固定共同score归一化、相同bias更新规则与gate的A1/A5对照，避免把teacher原子分组和score量纲共同改变当作同一个机制；多种子复现仍是独立未解决项。

本轮6a未达到L7>60%条件，不能据此宣布蒸馏已可行，MLP相对线性的优势也没有达到10个百分点；6b的1000步L7、2000步L4和L7达到1.08，因此自举路线已有部分操作性支持，值得作为下一候选。另两配置低于1.01、一配置位于两阈值之间，不能把六个结果合并成“student已普遍足够”。

实现接口需要先定清：本轮6b是在冻结A0的指定层上离线提取student原子，不是一套已部署的teacher-free全层router。L7特征不能在一次因果前向里驱动L0–6；另跑一份冻结A0来提供L7分数仍有外部模型成本。若研究者选自举路线，AI建议先把L4或L7字典接在同层FFN输入，仅改变该层或可因果访问的后层路由，并保持其余层原生，以最小干预区分“分组可用”与“早层接口不可用”。固定字典在student继续学习时的表示漂移，也需要在新协议中预先规定处理方式。本轮未执行这些主模型训练，不把离线M达标改写为NLL收益。

## 完成与来源边界

所有数字为AI分析，研究者判断Unknown。GPU时间按已测量GPU阶段的墙钟记录（含阶段内数据I/O，部分初始化／归档读取不在该计时区间），不是CUDA kernel时间或精确资源计费；共享A0前向不重复算到每项。纯CPU统计为0。源脚本、冻结SHA、接受偏差、归档恢复哈希与小模型清单见执行根evidence/和最终交付清单。A0 500步原state被外部归档，本轮只从已验证archive复制到独立执行根；原路径未写回。R04原始结果和存档不由本轮更改；无commit/push。
'''
 (REPORT/'analysis_cn.md').write_text(text)
if __name__=='__main__':main()
