from common import *
import pandas as pd,numpy as np,textwrap
out=pd.read_csv(R/'tables/overlap_summary.csv');main=out[out['mode']=='main'];diag=pd.read_csv(R/'tables/SAE_diagnostics.csv');fmt=pd.read_csv(R/'data/basic_format.csv');source=json.load(open(R/'data/sources.json'));ex=rows(R/'tables/deterministic_examples.jsonl');amp=pd.read_csv(R/'tables/amplitude_supplement.csv')
def mdtable(df,cols):
 def vv(v):
  if isinstance(v,(float,np.floating)):return f'{v:.6f}'
  return str(v)
 return '| '+' | '.join(cols)+' |\n|'+'|'.join(['---']*len(cols))+'|\n'+'\n'.join('| '+' | '.join(vv(row[c]) for c in cols)+' |' for _,row in df.iterrows())+'\n'
mt=[]
for _,r in main.iterrows():mt.append(dict(SAE=r.site,pair=r.A+'/'+r.B,A_within=f'{r.within_A:.4f}',B_within=f'{r.within_B:.4f}',cross=f'{r.cross:.4f}',pooled_difference_95CI=f'{r.pooled_minus_cross:.4f} [{r.pooled_minus_cross_lo:.4f},{r.pooled_minus_cross_hi:.4f}]',Holm_p=f'{r.holm_primary:.3f}',both_sides=r.status))
mt=mdtable(pd.DataFrame(mt),list(mt[0]));ctl=mdtable(out[out['mode']!='main'],['site','A','B','mode','N_A','within_A','within_B','cross','A_minus_cross_lo','B_minus_cross_lo','pooled_minus_cross','pooled_minus_cross_lo','pooled_minus_cross_hi','p_pooled_one_sided','cross_actual_pairs'])
which=[f'{r.site}:{r.A}/{r.B}' for _,r in main.iterrows() if r.status=='BOTH_WITHIN_HIGHER'];mixed=[f'{r.site}:{r.A}/{r.B}' for _,r in main.iterrows() if r.status!='BOTH_WITHIN_HIGHER'];pairs=3;passes=len(which)
summarycn=f'''# S08：自然数据集内部的 SAE 成员是否更相似？

在本轮3个可读数据集、每组257篇问题、两套原生 SAE 的6个比较中，{passes}/6 满足预设的“双侧内部高于跨域”判据。成立条件：{'; '.join(which) or '无'}。其余比较：{'; '.join(mixed) or '无'}。这描述数据集条件下的激活成员相似性；来源、格式、题型与词面仍可能参与形成差异，不能直接归因于领域知识，也不证明功能机制。

本轮事实分析路径：行为与因素控制只检查文本长度、格式和词面，没有答案正确率；表征分析比较固定 Qwen3-0.6B 的二值激活成员；功能干预与训练均 NOT_RUN，本轮只审核采集接口和数值可信度。科研接受与问题关闭 Unknown。

{mt}

表中 A/B 顺序见 pair 列。Jaccard=两位置共同激活成员数÷两位置并集成员数；每个文档对平均8个相同分位位置。pooled difference=两侧内部均值的平均−跨域均值。每组257篇，内部与跨域各32896个不同文档对，但独立统计单位是文档。区间来自1999次文档级 bootstrap；999次整篇标签置换，6个主要合并差检验 Holm 校正。每侧差值及95%区间、实际比较数在[完整统计表](tables/overlap_summary.csv)，不能只用合并差替代两侧判断。

![主要重叠结果](figures/01_main_overlap.png)

图1三个点依次为A内、B内和跨A/B，误差线是文档级95%区间；两套字典独立读图，不对齐 feature ID。所有主要配对均展示。

![对照](figures/02_controls.png)

图2横轴是合并内部−跨域差。完整题干长度分箱后，各配对仅11、59、121篇/侧；Magicoder/GSM8K的匹配不足，区间宽不能写成无差异。固定32-token上下文各249、161、161篇/侧；固定16-token上下文全部257篇/侧。它们固定已见上下文长度，不能替代完整题干长度匹配。相同 token 对照只比较事前固定的最多3种高频 token，许多文档对没有匹配位置；其区间描述这些可比较的对，不做置换显著性判断。

数据使用 Magicoder-OSS75K 的 problem(train)、GSM8K 的 question(train)、MMLU 的 question(test)，排除答案、解答、代码 seed 和 MMLU 选项。规范化精确去重后用固定种子20261104从题干长度≥16token的候选均匀抽样，保留每篇原文和ID。读取前128token，不加指令或后缀；每篇8个正文分位位置，同时保存第16/32token。三组题干长度中位数252/56/50；代码围栏比例158/257、0/257、0/257；换行比例257/257、0/257、27/257。这些明显差异使“领域知识”的单一解释不成立。见[长度和格式图](figures/03_format_and_length.png)、[高频 token](data/top_tokens.csv)与[完整报告](detailed_cn.md)。

Numina在指定缓存与已记录搜索范围未找到；不把三组分析冒充四组结果。学长精确SFT路径当前不可读，使用可信现有缓存版本，不声称完全复现其设置。MMLU混合学科，省略选项的题干有时不独立完整；语料公开且与预训练可能重叠，未验证去污染或训练未见。仅做精确去重，近重复仍是竞争解释。不同 token 有不同因果上下文；本轮不是整篇语义向量的比较。

共同成员幅值另列[补充表](tables/amplitude_supplement.csv)；全向量激活规模和重构误差见[SAE质量表](tables/SAE_diagnostics.csv)，均不进入 Jaccard。两字典实际激活数的范围：{'; '.join(s+':'+str(int(g.active_min.min()))+'–'+str(int(g.active_max.max())) for s,g in diag.groupby('site'))}，Top32的名额约束不是语义发现。

已完成采集、全部主要比较、文档不确定性、长度/格式/词面对照、幅值补充及独立集合运算复核。认识更新限于上表和对照实际覆盖的条件；下一步科学判断由研究者审核。本轮没有模型、SAE或读出训练，没有功能干预。
'''
summaryen=f'''# S08: Are SAE support sets more similar within natural datasets?

Across the three readable sources with257 questions each, {passes}/6 native-SAE/source-pair comparisons meet the frozen both-sides-higher criterion. Passing conditions: {'; '.join(which) or 'none'}. Other conditions: {'; '.join(mixed) or 'none'}. This is dataset-conditioned member similarity, not an identification of domain knowledge or a functional mechanism.

Factual paths: behavior/factor controls describe length, format and literal tokens without answer scoring; representation analysis compares binary supports in the frozen model; functional intervention and training are NOT_RUN. Hook and numerical checks concern measurement quality. Scientific acceptance and closure remain Unknown.

{mt}

A/B order follows the pair column. Each document-pair value averages8 aligned-quantile Jaccards, intersection/union of strictly positive native coordinates. Within A, within B and cross use32,896 distinct pairs each at257 documents/source, not32,896 independent units. Pooled difference is mean(within A,within B)-cross.1,999 document-count bootstrap samples;999 whole-document label permutations; Holm across six main pooled tests. Individual side intervals remain in [full statistics](tables/overlap_summary.csv).

![Primary binary overlap](figures/01_main_overlap.png)

![Controls](figures/02_controls.png)

Full-question-length bin matching leaves11/59/121documents per source for the three source pairs. Fixed32prefix samples are249/161/161; fixed16uses all257. Equal observed context length does not equal matching complete question length. Literal-token comparisons condition on preselected frequent tokens and retain missing eligible pairs; no permutation inference is claimed for this conditional control. Controls are exploratory and do not rescue failed primary outcomes.

Use only Magicoder-OSS problem(train), GSM8K question(train), MMLU question(test), no solutions/answers/choices/seeds. Uniform seeded sampling after normalized exact dedup and>=16token eligibility; max128visible tokens, no prompt/suffix/special tokens. Full lengths have medians252/56/50; code fences158/257,0/257,0/257; newlines257/257,0/257,27/257. Source, task, syntax, current token, topic and near duplicates remain live rivals. MMLU stems can depend on omitted options. No contamination-free or heldout-pretraining claim.

Numina was not found in the recorded bounded locations. The exact senior SFT legacy path is unavailable; these are verified existing versions, not an exact replication. Native dictionaries are independent; feature IDs do not correspond. Top32constraints and raw amplitude do not enter the semantic claim. See [Detailed](detailed.md), [raw amplitude supplement](tables/amplitude_supplement.csv), [quality diagnostics](tables/SAE_diagnostics.csv), [source identities](data/sources.json) and [reproduction](reproduce.md). Execution completed; scientific interpretation beyond these conditions is pending researcher review.
'''
top=pd.read_csv(R/'data/top_tokens.csv');tokenlines=[]
for d in DATASETS:
 q=top[(top.dataset==d)&(top.scope=='visible_window')].head(5);tokenlines.append(d+': '+', '.join(repr(v.decoded)+' '+str(int(v['count']))+'/'+str(int(v.denominator)) for _,v in q.iterrows()))
summarycn+='\n可见正文高频token（次数/该源可见token总数）：'+ '; '.join(tokenlines)+'。这些是token计数，不是独立文档数。抽查原文均为英文题干；未做全面语言识别，Magicoder的lang字段指编程语言，不是自然语言标签。\n'
summaryen+='\nFrequent visible-body token counts (count/visible-token denominator): '+ '; '.join(tokenlines)+'. Sampled examples are English questions, without comprehensive language detection; Magicoder lang denotes programming language, not a natural-language label.\n'
(R/'summary_cn.md').write_text(summarycn);(R/'summary.md').write_text(summaryen)
counter=rows(R/'tables/posthoc_counterexamples.jsonl');pc=pd.read_csv(R/'tables/per_document_counts.csv');neg=next(x for x in counter if x['site']=='MLPIN_SAE' and x['pair']=='Magicoder/MMLU' and x['dataset']=='MMLU')
updatecn=f'''\n认识更新：H1中“同条件文本的成员更相似”这一重叠子预测，从构造家族扩展到了三种自然题干来源。四类对照的两侧差值95%区间也都大于0；未观察到这些有限对照消除差异。它没有验证父子成员换入换出的语义规律。共同成员幅值只是补充，不构成本轮H2裁决。\n\n均值规律不覆盖每篇文档。事后描述性检查中，MLPIN的MMLU文档相对Magicoder有57/257篇自身内部邻居均值低于跨域；Attention的GSM8K相对Magicoder有48/257篇。例子 {neg['id']}：{neg['text']} 其MMLU内部均值{neg['within_neighbor_mean']:.6f}，跨Magicoder均值{neg['cross_neighbor_mean']:.6f}，差{neg['within_minus_cross']:.6f}。这是事后展示的反例，不重新筛选数据或变更主要检验，也不能仅凭词语为其指定feature语义。见[逐文档反例图](figures/05_document_counterexamples.png)与[tables/per_document_counts.csv](tables/per_document_counts.csv)。\n\n相同token后MLPIN的MMLU相对Magicoder这一侧差仅0.005388，95%区间[0.000601,0.011027]，比主分析0.008862更接近边界；不能将有限词面控制写成彻底排除词面。控制使用不同token分布；长度/32token控制还改变文档子集，不能将其相对主分析的数值变化解释为某个因素的因果贡献。\n'''
updateen=f'''\nRecognition update: the overlap subprediction generalizes from constructed families to these three natural question sources. Both-side95% intervals remain positive in the four limited controls; none removes the observed association. This does not test semantic parent/child recruitment or adjudicate H2. Group means do not describe every document:57/257 MMLU documents have lower same-source neighbor means than cross-Magicoder means in MLPIN;48/257 GSM8K documents do so against Magicoder in Attention. A posthoc descriptive counterexample is {neg['id']}, text: {neg['text']!r}. Its within-MMLU mean={neg['within_neighbor_mean']:.6f}, cross-Magicoder={neg['cross_neighbor_mean']:.6f}. These are dependent descriptive points, not new confirmatory tests. Same-token MLPIN MMLU-minus-cross-Magicoder is only.005388[.000601,.011027], closer to the boundary than main.008862. Control subsets/token distributions differ; their change from main is not a causal effect estimate.\n'''
summarycn+=updatecn;summaryen+=updateen
(R/'summary_cn.md').write_text(summarycn);(R/'summary.md').write_text(summaryen)
first=next(r for r in ex if r['site']=='ATTN_SAE' and r['quantile_index']==0 and r['A_id'].startswith('Magicoder') and r['B_id'].startswith('GSM8K'))
case=f'''预先按ID哈希顺序选择的例子（不是挑最高重叠）：{first['A_id']} / {first['B_id']}，ATTN_SAE，首个分位。前者位置{first['A_position']} token={first['A_token']!r}，后者位置{first['B_position']} token={first['B_token']!r}。交集{first['intersection']}、并集{first['union']}，J={first['Jaccard']:.6f}。共同ID={first['shared_ids']}；前者幅值={first['A_shared_values']}；后者幅值={first['B_shared_values']}。\n\nA全文：\n\n> {first['A_text'].replace(chr(10),chr(10)+'> ')}\n\nB全文：\n\n> {first['B_text'].replace(chr(10),chr(10)+'> ')}\n'''
methodcn='''每个源完整读取指定 Arrow 表并使用指定问题字段。规范化 NFKC/casefold/空白折叠哈希用于去重，推理仅strip边缘并统一CRLF，保留内部格式；跨源精确重复对称排除，本次为0。MMLU14042行→13866唯一问题，176重复；Magicoder75197、GSM8K7473均未减少。从均匀打乱的唯一题干候选逐条 tokenize 到257篇合格；MMLU检查359篇，其中102篇不足16token。没有声称对全语料做完token长度筛选。最低样本可用量足够，本轮为快速分析预先定额257；不冒充分析全部75K/14K问题。

每篇实际推理 min(全长,128) token；位置 floor((j+.5)L/8)，j=0..7，L≥16确保8个不同位置。对齐相同分位的8对token，而不是8×8全配对。文档对内平均后再对文档对取均值，文档等额；不同文档的token从不当成独立文档。无后缀、无chat模板、无答案。Magicoder较长且大部分截断，因此主结果是这些问题前缀的局部状态统计。

模型 official Qwen3-0.6B-Base，28block、宽1024；使用FP32 CPU2线程、固定8×128物理批形状，尾批填充但只保存真文档。两个block27原生SAE均30000维ReLU-Top32，激活定义为所选z>0。Attention读self_attn.o_proj输出、残差之前；MLPIN读mlp实际输入，残差相加和post_attention_layernorm之后。二者各用自己的encoder/decoder，直接输入原表征，无额外归一化或偏置减法。配置、权重与加载器SHA见frozen_plan。抽取仅加载模型主体，避免无关词表logits成本。本轮无候选答案评分任务。

配对：每源按SHA256('S08'+文档ID)固定顺序。内部全体i<j；跨域对A_i与B_(i+offset mod N)，offset=1..(N−1)/2。奇数N使两种各N(N−1)/2对，跨域每篇度数相同。保存pair_graphs.npz的整数边端点及全局ID表。主分析每组32896对、每对8个位置，共263168位置比较；这个数不是独立样本量。

文档 bootstrap1999次，每源独立multinomial重采样N篇，原边乘文档重数c_i c_j后加权求均值。同篇所有位置和重复配对同步移动；原自配对不新增。保存所有重采样统计向量。999次整篇标签置换保留两组N，重新按同一固定配对规则计算，不把原边作为独立可交换项。主要零假设为源标签与整篇表征可交换；这是关联性零假设，不是领域内容的随机因果实验。主要6个pooled单侧检验Holm校正，95%区间为边际区间；两侧各自区间不另作独立阳性筛选。每配对、每控制的实际种子见CSV，基种子20261104。

完整题干长度分箱用[16,32,48,64,96,128,192,256,512,1024,2048,∞)，各箱两源取最小数量，并在同箱两侧各去一篇使总数为奇数。分箱内进行标签置换，保留每箱两侧数量。它是粗粒度长度匹配，不是逐字相等长度。固定31位置只用≥32token文档；固定15位置所有文档可用。后者在激活读取前因Magicoder/GSM8K完整长度匹配仅11篇追加，原协议/计划/面板原字节保留，见amendment_fixed16与时间戳。两个前缀控制均不等于完整问题长度匹配。

词面控制：发现激活前按8个位置中的文档覆盖选每源均≥20篇、最多3种相同token，token表见lexical_control_tokens.json。每文档对仅对相同所选token的位置两两比较后均值；没有匹配的位置对保留缺失。仍用原文档图，不补抽文档或挑激活好的词。这个条件统计中的有效边数和端点文档覆盖见CSV；只报告文档bootstrap，不赋予标签置换意义。它改变被比较的token/上下文分布，不能将与主结果的差直接当作去掉词面因素后的因果净效应。

幅值补充：每位置只在共同正成员上计算sqrt(sum((z_i−z_j)^2)/共同成员数)，共同数为0则缺失，文档对平均可用8位置，再平均边。它混合规模和搭配差异，不替代二值成员J。质量表另列z向量L2、原hL2、重构相对误差以及decoder列范数。
'''
methoden='''Read complete selected Arrow tables and the exact question field; normalized NFKC/casefold/whitespace hashes remove exact repeats, while inference retains internal formatting. MMLU14042rows become13866unique questions;176duplicates. Magicoder75197and GSM8K7473remain unique. Uniform permutation/rejection sampling selects257 questions with>=16tokens/source; MMLU examines359candidates with102short exclusions. Full-population token eligibility was not counted.257is the frozen fast-analysis quota, not a claim of full-corpus inference.

Input the first min(full_length,128)tokens without special tokens, instruction wrappers or answer suffix. Eight positions floor((j+.5)*visible_length/8) are paired by equal quantile index. Main Jaccard averages eight support-set ratios per document pair; it does not pool amplitudes or treat token positions as independent documents.

Frozen official Qwen3-0.6B-Base,28blocks,width1024, FP32CPU2threads,physical8x128. Attention is block27.self_attn.o_proj output before residual addition; MLPIN is actual block27.mlp input after residual/post_attention_layernorm. Each native dictionary is30000/ReLU-Top32; active iff selected z>0. No extra input normalization or decoder-bias subtraction; dictionaries have unrelated IDs. Model body forward avoids unnecessary vocabulary logits. No answer scoring, training, readout fitting or interventions. Source hashes and native loaders are in frozen_plan.json.

Order each source by SHA256('S08'+document ID). Within use all unordered i<j; cross pair A_i with B_(i+offset mod N), offsets1..(N-1)/2. Each group hasN(N-1)/2unique edges; cross has equal degree. Main32896edges/group times8positions=263168token-position comparisons, not independent samples. Explicit graph endpoints and global IDs are saved.

1999independent within-source multinomial document-count bootstraps reweight each original edge by c_i*c_j, retaining all position/pair incidences together. No original self edges are added.999 whole-document label permutations reapply the same pairing rule after relabeling; plus-one p. The null is whole-document representation exchangeability under source labels, not randomized semantic content. Six main one-sided pooled differences use Holm.05; confidence intervals are marginal document-bootstrap intervals and individual sides are retained. Exact per-cell seeds are saved.

Full-token-length bins16/32/48/64/96/128/192/256/512/1024/2048+/infinity take equal counts per source/bin; remove one same-bin document per side if needed for oddN. Stratified permutations preserve bin counts. Fixed32and16causal prefixes control observed context length, not total question length. Fixed16 was added before activation availability due only to11-doc full-length matching for Magicoder/GSM8K; original frozen protocol, plan and panel remain byte-identical.

Same-token controls fix up to3literal token IDs with>=20document coverage/source before responses. Average matching token-position Jaccards within each document pair; leave nonmatching edges missing and report coverage. Document bootstrap only, no conditional permutation claim. This selects a different token/context distribution, so its change from main is not a causal lexical-effect estimate.

The separate amplitude supplement computes raw RMS coordinate difference on positive shared members per aligned position, denominator=shared member count, missing if none, then eligible-position/document-pair averaging. Whole-zL2, hL2, decoder norms and reconstruction error remain separate diagnostics.
'''
detailcn='# S08 详细结果与审计\n\n'+summarycn.split('\n',1)[1].split('![主要重叠结果]')[0]+'\n## 实验做法和每项比较的含义\n\n'+methodcn+'\n## 全部对照结果\n\n'+ctl+'\n## 实际来源与格式\n\n```json\n'+json.dumps(source,ensure_ascii=False,indent=2)+'\n```\n\n'+mdtable(fmt,list(fmt.columns))+'\n## 字典规模和重构限制\n\n'+mdtable(diag,list(diag.columns))+'\n## 幅值补充（非Jaccard）\n\n'+mdtable(amp,['site','A','B','within_A','within_B','cross','pooled_minus_cross'])+'\n## 指回原文和坐标的例子\n\n'+case+'\n其余同源和跨源例子、每个共同ID的两侧幅值、换入换出集合在tables/deterministic_examples.jsonl。该文件包括反例可能出现的全部预定例子，未按结果筛选。\n\n## 竞争解释与边界\n\n主数据集差异同时包含题型、格式、词面、来源、主题；两个控制不能唯一裁决知识解释。代码围栏及换行尤其不平衡；Numina缺失，学长版本未复现。精确去重不排除近重复；MMLU混合学科、问题省略选项；未检验模型预训练污染。Top32强制限制激活名额，重叠变化不等于新增语义容量；不同SAE ID不对应，重构误差限制将字典当真实feature。单一固定模型、block27、前128token和有限文档采样只支持本条件的观察。小样本长度对照或区间跨0为证据不足；不能升级为不存在差异。控制是探索性的，不救主要失败。\n\n## 数值审核和复现\n\n先校验hook零扰动与第32token前缀等价，再用直接Python集合运算独立复核200文档对、重放90个已存边均值、核对所有图的边数/文档度数及六个Holm值。独立脚本和evidence/independent_verification.json保留结果。每篇原文、source row/字段/revision、ID、token和位置在data/panel.jsonl，原生Top32 ID/激活值在cache/activations.npz；大kernel缓存见large_files_index。训练/功能干预均NOT_RUN，科学接受Unknown。\n'
detailen='# S08 Detailed result\n\n'+summaryen.split('\n',1)[1].split('![Primary binary overlap]')[0]+'\n## Methods and interpretation of each comparison\n\n'+methoden+'\n## All controls\n\n'+ctl+'\n## Exact source versions\n\n```json\n'+json.dumps(source,ensure_ascii=False,indent=2)+'\n```\n\n'+mdtable(fmt,list(fmt.columns))+'\n## Native dictionary quality\n\n'+mdtable(diag,list(diag.columns))+'\n## Separate shared-member amplitude\n\n'+mdtable(amp,['site','A','B','within_A','within_B','cross','pooled_minus_cross'])+'\n## Limits and numerical audit\n\nFormatting, topic, task/source and lexical choices co-vary; controls cannot uniquely identify domain knowledge. Near duplicates, pretraining exposure and incomplete MMLU stems remain. Native Top32competition is a measurement constraint, not a semantic finding. Reconstruction and one-model/one-layer/prefix sampling limit claims. Weak length matching and intervals crossing0are insufficient, not evidence of no difference. No-op and fixed32prefix equivalence,200independent Python-set checks,90saved-edge mean replays, graph degrees and six Holm adjustments are audited in evidence/independent_verification.json. Full texts and exact token positions in data/panel.jsonl, native sparse coordinates in cache/activations.npz, deterministic unselected examples in tables/deterministic_examples.jsonl. Scientific acceptance Unknown.\n'
detailcn+='\n主题和来源构成：Magicoder为编程问题，lang是编程语言（样本python139/257），不是英文识别；GSM8K为小学数学故事题；MMLU混合学科，均匀按题干抽样而非学科平衡，样本professional_law36/257、moral_scenarios30/257。相同源可以包含与另一来源主题更近的题干，因此不能用数据集标签替代细粒度语义类别。\n';detailen+='\nSource/topic mixture: Magicoder programming questions (python139/257 as programming-language metadata), GSM8K grade-school math stories, MMLU mixed subjects (professional_law36/257,moral_scenarios30/257), uniformly sampled by question rather than subject-balanced. Dataset identity is not a fine semantic class.\n';detailcn+='\n## 认识更新和个体反例（事后描述）\n\n'+updatecn+mdtable(pc,list(pc.columns));detailen+='\n## Bounded recognition update and posthoc descriptive counterexamples\n\n'+updateen+mdtable(pc,list(pc.columns));(R/'detailed_cn.md').write_text(detailcn);(R/'detailed.md').write_text(detailen)
brief=f'''# 1104 组会：自然数据集内部 SAE 成员更重叠吗？

**问题。** 将构造文本上的H1成员重叠观察扩展到自然问题语料：同源文档是否比跨源更相似？

**观察结论。** 两套字典、3个配对中，{passes}/6满足预设双侧判据；仅在已测模型、题干前缀与采样条件内成立，不能直接解释为领域知识。

**结论下关键数据。** 每源257篇，8位置/篇；各组32896个不同文档对。文档级95%区间及六检验Holm如下。

{mt}

![两套SAE全部配对](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/figures/01_main_overlap.png)

**实验做法。** Magicoder-OSS problem、GSM8K/MMLU question；相同题干字段规则，不用解答、选项或答案。固定种子精确去重抽样；原Qwen3-0.6B、block27 Attention输出/MLP输入分别用自己的Top32字典。每文档对平均8个相同分位位置的交集÷并集；1999文档bootstrap、999文档标签置换。补充完整长度分箱、16/32token固定上下文和相同字面token控制；幅值单列。

**边界。** Numina限定搜索未找到，学长精确SFT数据当前不可读，不冒充复现。长度中位数252/56/50token；Magicoder代码围栏158/257，另外两源0/257。完整长度匹配Magicoder/GSM8K仅11篇/侧，证据能力弱。固定前缀与同token对照不能排除来源、主题、任务和格式。两套SAE ID不对应，本轮无训练、无干预，也不推导router功能。科研接受/问题关闭Unknown。

[完整中文Summary]({C}/summary_cn.md) · [全部对照与局限]({C}/detailed_cn.md) · [逐格原始统计]({C}/tables/overlap_summary.csv)
'''
brief+='\n**认识更新与反例。** 上述四类有限对照均保留正向两侧区间；重叠子预测扩展到三种自然问题来源，尚不识别知识机制。MLPIN中MMLU相对Magicoder仍有57/257篇文档呈反向局部差，均值相似性不等于每篇更相似；题干含softmax与entropy的MMLU:test:row6874，内部0.071092、跨Magicoder0.086829。这是事后描述性反例。\n';(R/'meeting_report_cn.md').write_text(brief)
(R/'reproduce.md').write_text('''# Reproduction and saved evidence

All execution paths are bound in frozen_plan.json and data/sources.json. Native model/SAE weights and full source Arrow files are intentionally excluded. CPU2threads, no GPU, training or interventions.

```bash
export PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python code/extract.py
python code/analyze.py
python code/verify.py
python code/figures.py
python code/describe.py
python code/report.py
```

The extraction refuses to overwrite an existing activation cache. For full fresh rerun, copy this folder to a new execution location and remove generated caches only in that new copy; original freezes and source paths remain. prepare.py also refuses to replace the frozen plan. No re-preparation is needed for the saved771-document panel. For a quick model-free numerical replay, analyze.py uses cache/activations.npz and writes only derived analysis outputs; verify.py checks independent set/edge arithmetic after kernels are regenerated. Empty optional short fixed32records are marked invalid and never used in that control.

Raw data inventory: data/panel.jsonl contains every selected original question, source row, metadata, token IDs/pieces/offsets and sampling positions; sample_ids.csv/exclusions.jsonl retain selection; pair_graphs.npz stores all original graph endpoints with global document IDs; cache/activations.npz stores all771x10x32 native IDs/values per dictionary and measured quality; tables/overlap_summary.csv stores every primary/control estimate/CI/count/seed; document_resamples.npz stores complete document-bootstrap/permutation values; deterministic_examples.jsonl contains fixed unselected within/cross examples with concrete shared IDs/values. Large derived kernels stay execution-side if excluded; exact path/size/hash in large_files_index.json. Package payload manifest states exactly which files are portable.

Protocols were frozen before extraction; fixed16amendment is explicitly timestamped before first forward and preserves original files. Scientific approval/closure Unknown; no publication or commit.
''')
print('REPORTS_COMPLETE',passes,'of6')
