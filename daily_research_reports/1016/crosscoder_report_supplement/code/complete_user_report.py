"""Minimally supplement the user's visible screenshot, preserving source order."""
from pathlib import Path
import json,shutil,difflib
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
D=Path('/data/250010109/Research_System/daily_research_reports/1016/crosscoder_report_supplement')
S=E/'analysis/report_spectrum/20261016_spectrum'
REPLACEMENTS=[('排除高频common feature之后','考虑边际频率和φ选择偏好之后','没有删除高频或已认定common的feature；原统计条件是考虑边际频率与φ筛选偏好。'),('构建正则化项时','构建输入分配规则时','已有试验改变输入分配，没有增加按组计算的正则化损失。'),('并进行参数谱的分析。','并进行组贡献表征谱的分析。','新分析测量组贡献在文本位置间变化的协方差，不测参数矩阵的谱。')]

def put_after(text,anchor,addition):
 assert text.count(anchor)==1,anchor
 return text.replace(anchor,anchor+'\n\n'+addition)

def cap(name):
 x=(D/'provenance/figures12_captions_cn.md').read_text()
 if name==1:return x.split('# 图1：组内频率差异\n\n')[1].split('\n\n来源：')[0]
 return x.split('# 图2：预测损失\n\n')[1].split('\n\n来源：')[0]

def main():
 base=(D/'sources/user_report_transcription_cn.md').read_text();text=base
 for old,new,_ in REPLACEMENTS:
  assert text.count(old)==1
  text=text.replace(old,new)
 text=put_after(text,'下一步验证学习效果，同时给出对于这种分发具体机制解释。','**补充（当前进展与指标边界）**：该学习验证已有三种分配、三个配对种子的完整结果，见下文图2；这里保留原句作为原计划。原文“低频知识”属于研究目标，已有读数只测低频feature出现位置上的预测损失，尚不是知识准确率，也没有证明MoE容量提升。原文提出的“正则项”仍是待定义设想；本轮实际没有训练额外正则损失。')
 model=r'''**补充（填入本轮实际模型）**：固定Qwen3-0.6B及最终14源层CrossCoder。feature是固定字典的一个latent坐标，令 \(z_i(t)>0\) 表示它在已见位置 \(t\) 激活；模型据此前缀预测下一位置 \(t+1\)。原关系组为 \(G_g\)，其命中成员占比为 \(c_g(t)=|G_g|^{-1}\sum_{i\in G_g}\mathbf1[z_i(t)>0]\)，再用D侧已固定的均值与标准差校准为组分数，只在有命中的组中选择胜组 \(g^*(t)\)，并由D侧固定映射 \(a\) 指定专家 \(e(t)=a(g^*(t))\)；无命中时使用原固定哈希回退。

实际 \(K=4\)，每个专家接收完整的末端hidden \(h_t\)，在第28个block输出、最终RMSNorm之前加入rank32残差适配器：

\[
h'_t=h_t+A_{e(t)}B_{e(t)}h_t.
\]

这里 \(A_e\in\mathbb R^{1024\times32}\)、\(B_e\in\mathbb R^{32\times1024}\) 是仅有的可训练矩阵；基座、CrossCoder、最终归一化及词表头均冻结。三种分配使用相同参数量、输入曝光、优化器及配对种子，训练目标仍是所有有效下一token的交叉熵；“低频feature条件”仅用于评估，不把feature当作被路由的token，也不删除其余输入信息。'''
 text=put_after(text,'给定专家数量K，使用以下下给定的feature共现分组规则下，专家分配问题可以定义为：',model)
 figure1='''**补充图1：组内频率差异**

![组内频率差异](figures/figure1_frequency_difference.png)

'''+cap(1)+r'''

计算中的 \(p_i^V=n_i^V/N_V\)，\(N_V=5,247,663\)。每组先计算：

\[
s_g^V=\sqrt{\frac1{|G_g|}\sum_{i\in G_g}\left(\log_{10}p_i^V-\frac1{|G_g|}\sum_{k\in G_g}\log_{10}p_k^V\right)^2},
\qquad \bar s^V=\frac1{186}\sum_{g=1}^{186}s_g^V.
\]

匹配随机组在D侧按同组大小、平均log10频率容差±0.1 dex构造，每组的抽样标准差先取均值，再对186组等权；不是先把全部成员合成一组求标准差。来源是已修复的[186组完整对照](data/full_group_controls.csv)和[完整汇总](provenance/full_repair_summary.json)，没有使用旧142组版本；抽样资格不等于已证明全局混合。

现有全流程固定边际随机化也有读数，但限每侧4096位置、99次随机化与事后平滑端点；原严格组内频率端点 T_b 仍不可估，不能用图1两柱或该有限随机化宣称完全排除phi选择偏好。'''
 text=put_after(text,'   a. 检查局部边、完整组和组内频率；补充保留边际命中数的随机对照。验证这种关系是否在文本中稳定存在的特征结构',figure1)
 figure2='''**补充图2：预测损失**

![预测损失](figures/figure2_prediction_loss.png)

'''+cap(2)+'''

每个种子和曝光节点的数值保存在[作图数据](data/figure2_seed_plot_data.csv)，三种子的均值在[均值表](data/figure2_mean_plot_data.csv)；[总体损失另表](data/overall_loss_table.csv)，没有混入图2。训练曝光是累计有效预测目标次数，包含重复训练文本，不是互不重复的新样本数。已有局部更新干预只支持固定中点、同计数及等参数位移范数下的有界比较，完整训练损害根因尚未识别；新的谱分析也不能替代这个因果缺口。'''
 text=put_after(text,'   b. 检验学习效用：将关系组压缩成4个专家的输入分配，与频率、匹配随机规则做配对训练；随后做局部更新干预，并进行组贡献表征谱的分析。',figure2+'\n\n@@SPECTRUM@@')
 spectrum_note=(D/'spectrum_insert_cn.md').read_text() if (D/'spectrum_insert_cn.md').exists() else '**补充（组贡献表征谱）**：数据和计算条件已核对，正式分组、测点与单次列置乱seed已冻结；当前尚未填入经验谱结果，不用其他谱代替。'
 text=text.replace('@@SPECTRUM@@',spectrum_note)
 conclusion='''2. 已有关系、频率、匹配随机分配都没有改善本轮低频feature条件预测损失；这限制当前末端适配器分配方案，尚不能外推为所有同频学习方案无效。

'''
 if (D/'spectrum_conclusion_cn.md').exists():conclusion+=(D/'spectrum_conclusion_cn.md').read_text()+'\n\n'
 conclusion+='修改范围、原句与术语更正见[修改清单](modification_list_cn.md)；截图及逐段转录保存在[sources](sources/)，公式推导、层与尺度还原及推理边界见[审计](reasoning_audit_cn.md)。'
 text=text.rstrip()+'\n\n'+conclusion+'\n'
 (D/'report_cn.md').write_text(text)
 # Every unchanged source line remains in source order; only declared terminology replacements may alter a source line.
 cursor=0;preserved=0
 for line in base.splitlines():
  if not line.strip():continue
  for old,new,_ in REPLACEMENTS:line=line.replace(old,new)
  pos=text.find(line,cursor)
  assert pos>=0,('missing or moved original line',line)
  cursor=pos+len(line);preserved+=1
 changes='# 修改清单\n\n仅以用户确认的截图可见部分为底稿；保留标题“1016”和目的→机制直觉 & 假设→模型→实验分析→结论的原顺序，未推测截图外原文。\n\n## 原句术语更正\n\n| 原词句 | 更正为 | 原因 |\n| --- | --- | --- |\n'
 for old,new,why in REPLACEMENTS:changes+=f'| {old} | {new} | {why} |\n'
 changes+='''
## 填空与插入

1. 在原目的段后标明既有验证已完成，并解释低频feature条件指标与低频知识目标的区别；保留原目标、原假设和原计划文字。
2. 填充“模型”冒号后的空白，说明实际胜组→四专家映射、完整输入、末端rank32适配器与固定训练目标。
3. 在原分析a后插入图1、四句图注与标准差/匹配定义，使用完整186组修复版。
4. 在原分析b后插入图2、四句图注、低频指标定义及总体损失另表。
5. 在同一分析位置补组贡献表征谱定义、固定分组及测点、图3/4；列置乱对照与组平均频率分布另附，不把新分组与原186个phi组混合。
6. 保留原结论第1句，补既有学习结果和新谱结果的有界解释；不将负结果写成容量或全部同频方案的结论。
7. 按用户追加要求，另插原始hidden图5/6；与decoder贡献矩阵及其不同文本窗口明确区分，不用前者冒充后者。

## 明确保留的内容

原目的/动机、研究思路、phi定义、频率不同时phi上界推导与1%/50%示例均保留。φ示例的0.1005是正确近似，不是需要修正的错误。原文“构造正则项？”仍保留为研究设问，并明确它不属于本轮已实现训练。

独立对照原截图检查逐段转录；数学仅按仓库默认公式分隔符排版，不冒充网页原始排版。所有实质改动均见上表与补充位置，未重排或整篇重写。
'''
 (D/'modification_list_cn.md').write_text(changes)
 (D/'source_preservation_check.json').write_text(json.dumps({'status':'PASS','source':'sources/user_report_transcription_cn.md','visible_source_nonempty_lines_preserved_in_order':preserved,'declared_original_phrase_replacements':len(REPLACEMENTS),'original_heading_order':['1016','目的','机制直觉 & 假设','模型','实验分析','结论'],'unseen_text_inferred':False,'new_training':False},indent=2,ensure_ascii=False)+'\n')
 (D/'source_diff.patch').write_text(''.join(difflib.unified_diff(base.splitlines(True),text.splitlines(True),fromfile='visible_original',tofile='supplemented_report')))
 for name in ['figures12.py','complete_user_report.py']:
  p=E/'analysis_tools/report_spectrum'/name
  if p.exists():shutil.copy2(p,D/'code'/name)
 print(D/'report_cn.md')
if __name__=='__main__':main()
