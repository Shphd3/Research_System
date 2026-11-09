from pathlib import Path
import json,shutil,hashlib,datetime
import pandas as pd,numpy as np
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')/P.name
s=pd.read_csv(E/'analysis/summary_metrics.csv');c=pd.read_csv(E/'analysis/paired_contrasts.csv');rec=pd.read_csv(E/'analysis/recovery_by_full_top1_type.csv');m=json.load(open(E/'manifest.json'));receipt=json.load(open(E/'terminal_receipt.json'));val=json.load(open(E/'audit/final_validation.json'));pos=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];out=[json.loads(l) for l in (E/'analysis/raw_outputs.jsonl').read_text().splitlines()]
assert val['pass']
def v(panel,condition,metric):return s[(s.panel==panel)&(s.condition==condition)&(s.metric==metric)].iloc[0]
def ci(x):return f"{x['mean']:.3f} [{x['ci_low']:.3f}, {x['ci_high']:.3f}]"
def tab(panel):
 lines=['|保留条件|真实后继NLL，nat [95%区间]|与原模型KL，nat|首选ID一致率|常见1% ID概率质量|空白／标点质量|','|---|---:|---:|---:|---:|---:|']
 for co,label in [('mean_only','仅训练均值'),('k1','前1维'),('k64','前64维'),('k128','前128维'),('k256','前256维'),('k512','前512维'),('identity','原表征／原生头')]:
  lines.append(f"|{label}|{ci(v(panel,co,'NLL'))}|{v(panel,co,'KL_full')['mean']:.3f}|{v(panel,co,'top1_agreement')['mean']:.1%}|{v(panel,co,'freq_top1pct')['mean']:.1%}|{v(panel,co,'format_mass')['mean']:.1%}|")
 return '\n'.join(lines)
def gain_table():
 z=['|加入的64维|the面板NLL改善，nat [95%区间]|自然面板NLL改善，nat [95%区间]|','|---|---:|---:|']
 for cond,label in [('k128','紧接头部的下一64维'),('head_middle','中64维'),('head_tail','尾64维'),('head_random1034','正交随机1'),('head_random1035','正交随机2'),('head_random1036','正交随机3')]:
  a=[]
  for panel in ['the','natural']:
   x=c[(c.panel==panel)&(c.baseline=='k64')&(c.condition==cond)&(c.metric=='NLL')].iloc[0];a.append(f"{-x.difference_condition_minus_baseline:.3f} [{-x.ci_high:.3f}, {-x.ci_low:.3f}]")
  z.append(f'|{label}|{a[0]}|{a[1]}|')
 return '\n'.join(z)
summary='''# 累积谱投影与原生解码：先看观察，不下语义层级结论

本轮按三条线阅读：**行为与因素对照**（同一前文只改投影）；**表征与谱位置**（固定训练侧谱）；**输出干预与可信度**（原生输出头、恒等与缓存重放）。

本轮已完成全部冻结条件。观察到累计的预测恢复和按参考频率分组的恢复速度差异；**尚未测出一个外部定义的“由粗到细语义顺序”**。尤其要区分：低维输出偏常见标点，和原模型原有的常见预测先恢复，是两个不同现象。

## 对象、样本和先决检查

沿用 R12 的官方 Qwen3-0.6B-Base 权重、tokenizer 和最后 block27 的 residual-post（最终全局 RMSNorm 之前）。每个投影都先加回原训练均值，再接原生 RMSNorm 与绑定的冻结输出头；没有训练模型、分类器或字典。

“前 k 维”指训练表征协方差按方差排序的前 k 个主成分，不是词频排序。谱来自 R04 的60篇发现文档、9,600个位置，1024维全部非零，复用它不构成独立复现。主面板为 R12 的37篇固定文档，读完同一个输入ID279（` the`）后预测真实后继；补充面板为175篇、700个预先随机固定的自然位置。两面板分别报告，有32篇文档重合，合计180篇物理文档。文档已暴露，全部为探索性。

旧缓存未通过当前5090的预设重放阈值，因此用相同模型／测点／固定文本重提取180篇，未重拟合谱。新缓存三篇重放与同形状因果前文检查的NLL误差均为0；全部PC与真正恒等的logits、NLL误差均为0。失败记录、修订与原缓存都保留在[详细记录](detailed_cn.md)。

## 1. 随 k 恢复的是预测，而不是已标注的语义层级

NLL是模型给真实后继的负对数概率，越低越好；KL衡量投影分布偏离未投影原生头分布的程度，越低越接近原模型。两者不能替代。

**固定 the：37篇／37位置。**

'''+tab('the')+'''

**自然位置：175篇／700位置，先在每篇4个位置内平均。**

'''+tab('natural')+'''

![随k的NLL、KL与熵](figures/01_cumulative_native_metrics.png)

- **实际测量：**相同前文和目标，在固定原生头下保留不同累积子空间的目标概率、分布接近程度与输出熵。阴影是按文档重采样的95%区间。
- **排除的解释：**结果不依赖另训分类器的容量或调参。恒等与全PC检查排除了测点／少接或多接norm造成的假恢复。它未排除保留能量和分布外投影的解释。
- **对下一步设计的影响：**必须分开预测保真与真实后继成绩，不能把平均恢复曲线直接命名为语义粒度。

从仅均值到前1维，NLL反而上升（the：12.794→13.677；自然：10.377→10.594）。the面板的熵从均值3.104升至前64维5.515，再降至原模型3.000；这不是单向的“越来越确定”。

## 2. 常见预测较早恢复；中尾部的平均增益并不特殊

“常见”只指独立DCLM训练片段中频率最高1%的非特殊token ID。参考共4,194,304个token，采用加0.5平滑。它不是Qwen真实预训练曝光次数，更不是CrossCoder feature的频率。“格式”仅指解码完全由空白或Unicode标点构成的ID，不是句法或语义标签。

自然面板按原模型的首选ID分组：非格式常见ID为386位置／163篇，其余非格式ID为206位置／125篇，空白标点为108位置／81篇。前64维恢复原模型首选的组内文档均值分别为30.3%、2.0%、38.3%；前256维分别为52.8%、13.6%、51.0%。前述两个非格式组的原模型首选平均概率为0.500与0.519；后者并不更不确定，但这仍不是完整的置信度或语义匹配对照。the面板常见／其余组为16／20篇，前64维恢复率18.8%／5.0%，区间较宽；格式组只有1篇，不能判断格式恢复次序。

与此同时，**mean-only本来就把55.5%概率放在空白／标点上**，前三候选为 ` (`、`,`、空格；原模型在the后只有2.0%格式质量。低维大量输出标点主要包含过量背景偏置，不能都叫“恢复了正确格式”。

![参考频率、分组恢复与同维新增](figures/02_frequency_and_equal_rank_controls.png)

- **实际测量：**左列是常见ID概率质量，中列是按原模型首选ID类型分组的恢复率；右列固定头64，再加等量64维，比较配对NLL改善。中列分层是在看输出后补作的描述性分析，频率及格式掩码已于输出前固定，未换阈值或筛结果。
- **排除的解释：**自然面板的方向与the面板相似，现象不限于在the后预测；分开非格式ID后仍有频率差异。等维比较排除了新增维数不等，但不能把差异都归因于语义内容。
- **对下一步设计的影响：**需要在词频之外定义对象或关系区别；中尾部不能因为有正增益就被指定为细语义载体。

'''+gain_table()+'''

中部新增相对三个随机新增参照，在自然面板的NLL差为+0.025、+0.024、+0.044 nat，95%区间均跨0；the面板只优于其中一个种子，没有稳定的随机参照优势。直接加下一段前部64维，在两面板均优于加中部（配对差约0.402、0.497 nat）。尾部也有平均增益，但比自然面板的三个随机新增更小。因此这些数据支持“后部加入能改变并改善部分预测”，尚不支持“后部具有特殊的细语义增益”。

相同64维的头／中／尾／随机解码参见[等维附图](figures/A02_equal_rank64_controls.png)。训练参考中头／中／尾保留方差为53.07%／2.32%／0.53%；实际自然位置的平均中心化能量为41.44%／对应增量约3.55%／1.86%。训练方差、单次输入能量和预测增益不是同一个量。

## 3. 真正的上下文例子与反例

![固定样本输出分布](figures/03_fixed_text_output_distributions.png)

- **实际测量：**预先固定的四篇生物错例与数学090，在每个投影条件下的前三候选ID／片段／概率，并另列真实后继概率与排名。同行使用相同横轴尺度。完整可见前文和全部条件见[原始文本表](text_cases_cn.md)。
- **排除的解释：**样例不是按本轮漂亮输出选择。原模型在五例中只有262把真实目标列为首选，因此“接近原模型”本身不能代表恢复真实语义答案。
- **对下一步设计的影响：**未来必须预先定义可裁决的候选区别，不能只用几个从通用词变成领域词的例子命名语义层级。

**262（cell）：**可见末句是 `Many of the biochemical reactions involved in cellular respiration take place within the`。真实后继ID53942为 ` mitochond`，在原文中拼成mitochondria。其概率从头64的0.27%升到前256维7.50%、前512维67.81%、原模型89.64%。但头64已经以24.41%预测 ` cell`；在另一个预先随机固定的普通样本283，`out of the` 后的 ` cell` 在头64已经是首选（24.11%，原模型78.59%）。这是具体对象词的不同恢复速度，不能仅凭这两例建立粗细关系。

**292（ecology/evolution，反例）：**真实目标为 ` capacity`，原模型首选却是 ` ability`（88.51%）。加入中部后，KL由2.373降为2.171，更接近原模型；真实capacity的NLL却从4.849恶化到5.604，概率由0.784%降至0.368%。加入尾部反过来改善目标NLL至4.416，却使KL略升到2.408。准确性与保真在同一个固定样例中分离。

**090（数学定义）：**原模型本身把真实 ` summ`（summation开头）排在第14，首选为 ` process`；不能要求投影恢复一个原模型本来未命中的首选。另一个普通数学样本123从前256到512维，KL下降1.440→1.014，但目标NLL变坏6.233→6.359。

另按输出无关哈希规则，检查12篇未参与命名的自然文本（每域4篇，排除全部7篇固定展示文档）。其原始前文／输出保存于[验证样例](evidence/unselected_text_validation.json)。其中段落起始的 `The` 在64维已恢复；`polygons` 到256维仍未成为首选；但表示关系的常见 ` same` 也要更多方向才接近原模型。低维并非只含格式，高维也并非只补低频对象。所有12例逐一记录，不把这次阅读当作语义分类统计。

## 竞争解释与边界

1. **均值与输出头偏置：**已观察到，mean-only足以产生强常见／标点偏置；“先出现”不等于“正确恢复”。
2. **维数／能量恢复：**头部高效，下一前部64维优于中尾部；等维随机控制不支持中部特殊优势。尚未进行严格逐位置等能量比较。
3. **词频、置信度与语义混杂：**分组恢复是token-ID频率关系，不是外部粗细类别检验。参考词频是一个固定DCLM片段的代理，原始bin生成版本追溯仍不完整。标点也可能承担关系或格式作用；非格式不等于内容语义。
4. **预测不等于唯一正确续写：**原文后继只是一个真实参考答案。投影有时偏离原模型却改善其NLL；自然面板前256维有183/700位置的目标NLL优于原模型。256→512时有147/700位置出现KL改善但目标NLL恶化，不能把每个token当独立复现。
5. **探索与参考谱：**两面板旧文档已暴露，共用权重／谱基且共享32篇。925左右相邻谱间隙很小，本轮不命名单根方向；精确计数为924/1023个相邻相对间隙<1%。尾部非数值零空间，但稳定的单根语义解释仍无依据。

## 唯一下一步（AI建议，未执行）

只补一组**词频匹配、同token不同可见前文的对象／关系最小对照**，固定候选后继，检查恢复的是哪一种已外部定义的语义区别。本轮不继续增加层、分类器或生成样例。

**我们观察到：常见ID／表面格式预测较早接近原模型，更多方向继续恢复分布；这支持有限的预测恢复与词频相关偏置，但还不能说明由粗到细的语义排序；最值得补的是频率匹配的语义最小对照。** 研究者的机制判断与问题闭合仍为Unknown。

[完整统计](evidence/summary_metrics.csv) · [逐文档配对结果](evidence/document_metrics.csv) · [新增参照配对差](evidence/addition_control_contrasts.csv) · [协议](protocol_cn.md) · [详细记录](detailed_cn.md)
'''
# Correct wording to use exact gap count once.
summary=summary.replace('925左右相邻谱间隙很小，本轮不命名单根方向；精确计数为924/1023个相邻相对间隙<1%。','924/1023个相邻相对谱间隙<1%，本轮不命名单根方向。')
(P/'summary_cn.md').write_text(summary)
english='''# Cumulative spectral projection and native decoding

Behavior and factor controls hold prefix/head fixed; representation analysis uses the fixed TRAIN spectrum; intervention quality is checked by native decoding, identity and cache replay. All applicable measurements are complete. These results establish bounded prediction-recovery observations, not a coarse-to-fine semantic hierarchy.

We use the exact R12 official Qwen3-0.6B-Base weights/tokenizer and block27 residual-post before final RMSNorm. Projections add the inherited TRAIN mean, apply the original final norm, then the tied frozen lm_head. No model/classifier/dictionary is trained. The1024-dimensional PCA basis was fit to9600 positions from60 R04 discovery documents and is reused, not independently replicated. All37 fixed R12/the documents and175 natural-position documents/700 positions are evaluated separately;32 documents overlap,180 physical documents total. All are exploratory exposed-document reuse.

The old cache failed the unchanged5090 native replay gate; all180 documents were refreshed using the same weights/hook/input and original fixed shape. Fresh replay and same-shape causal-prefix NLL differences are zero on three smoke documents. Full-PC and direct identity logits/NLL differences are zero on all737 positions. The legacy failure, zero-roundoff guard repair and BF16 top-k tie correction are retained in Detailed. The reference PCA is unchanged.

For the/the natural panels, head64 target NLL is6.196/5.901 nats, head2564.188/3.914, and unprojected2.471/2.342. KL falls3.180/3.612 at64 to1.470/1.593 at256. First-PC NLL is worse than mean-only in both panels; entropy is nonmonotonic. Fidelity and target probability are distinct.

In the natural panel, original-top1 predictions on non-format common reference IDs (386positions/163documents), other non-format IDs(206/125), and whitespace/punctuation(108/81) recover at64 dimensions at30.3%,2.0%,38.3% respectively (within-group document means); at256,52.8%,13.6%,51.0%. Mean full-model top1 probabilities are0.500 vs0.519 for the two non-format groups; this does not replace a matched confidence control. The/the common/other groups have16/20 documents and broad intervals; format has only one document. Masks/reference frequency were frozen before outputs; this stratification was added descriptively after outputs.

Mean-only already puts55.5% mass on whitespace/punctuation and98.3% on the most-common1% of reference IDs; its top outputs are ` (`, comma and space. Unprojected/the format mass is only2.0%. Thus early format mass contains a substantial background bias and cannot all be called correct format recovery. Reference commonness comes from a fixed4,194,304-token DCLM TRAIN slice with alpha0.5 smoothing, not Qwen's actual pretraining exposure or CrossCoder feature frequency. Original bin-generation provenance remains incomplete.

Adding64 middle/tail directions to head64 improves NLL by0.458/0.155 nats on/the and0.427/0.151 on natural positions. Adding the next64 head directions improves0.859/0.924. Middle additions do not consistently outperform the three equal-rank orthogonal random additions; all three natural middle-minus-random intervals cross zero. Tail gains are smaller than all three random gains on natural positions. Rank controls rule out unequal added dimension; retained energy, direction/head alignment and out-of-distribution projection remain rivals.

The fixed262 case increases ` mitochond` probability from0.27% at64 to7.50% at256,67.81% at512 and89.64% unprojected. Yet the ordinary283 context already predicts the concrete noun ` cell` at64. In fixed292, adding middle reduces KL2.373→2.171 while worsening true ` capacity` NLL4.849→5.604; the original model prefers ` ability`. Original090 itself ranks true ` summ`14th. Twelve output-blind selected other natural documents provide raw checks and counterexamples, not semantic-classification prevalence. A common relational ` same` can also require many directions.

Three primary figure groups and all raw selected cases are linked below. Document bootstrap2000 draws gives pointwise95% intervals; within-document positions are not independent samples. First/continued recovery is not assumed monotone. CrossCoder attribution, unknown T5 replication, semantic mechanism and architecture benefits are not established by this round. Researcher acceptance/closure remain Unknown.

The sole proposed next decision is one frequency-matched, same-token minimal context comparison with externally specified object/relation alternatives, not additional layers/classifiers/generations.

![Cumulative metrics](figures/01_cumulative_native_metrics.png)
![Frequency, type recovery, equal-rank additions](figures/02_frequency_and_equal_rank_controls.png)
![Fixed outputs](figures/03_fixed_text_output_distributions.png)

See [Chinese factual reading](summary_cn.md), [full statistics](evidence/summary_metrics.csv), [paired document metrics](evidence/document_metrics.csv), [fixed full prefixes and outputs](text_cases_cn.md), [Detailed](detailed.md), and [Protocol](protocol.md).
'''
(P/'summary.md').write_text(english)
# Complete derived data provenance, without changing frozen sampling metadata.
native=[]
for r in pos:
 x=dict(r);x['legacy_h_source']=x['h_source'];x['h_source']=str(E/'data/native_h27_fresh'/(x['seq_id']+'.npz'));native.append(x)
(E/'data/native_positions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in native))
for name in ['terminal_receipt.json','manifest.json','freeze.json']:
 if name!='manifest.json':shutil.copy2(E/name,P/'provenance'/name)
for file in (E/'audit').glob('*.json'):shutil.copy2(file,P/'provenance'/file.name)
for name in ['summary_cn.md','summary.md','text_cases_cn.md']:shutil.copy2(P/name,E/name)
# Shared full-spelling English entry refers to original English contexts, not an invented translation.
(P/'text_cases.md').write_text('# Fixed prefixes and raw native outputs\n\nAll source prefixes and token fragments are English. [The raw bilingual reading table](text_cases_cn.md) preserves every original prefix, token ID/probability/rank and explicitly separated following-text description. Fixed cases and posthoc extrema are separate. [Machine-readable selected raw outputs](evidence/fixed_case_raw_outputs.jsonl) contain all21 conditions for all7 prespecified examples. No generated text substitutes these observations.\n')
print('bilingual summaries and native-position provenance written')
