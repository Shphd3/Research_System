"""Preserve the historical brief; package selected evidence and the current speaking entry."""
from pathlib import Path
import json,shutil,hashlib,datetime,csv
R=Path('/data/250010109/Research_System');W=R/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030';S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');O=S/'presentation_variants/near_single_domain_20261030';T=S/'presentation_variants/token_context_audit_20261030';D=W/'figure_variants/near_single_domain_20261030';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
origin={}
for p in (O/'figures').iterdir():
    if p.suffix not in ['.png','.pdf']:continue
    dest=D/p.name;shutil.copy2(p,dest);origin[dest.name]=str(p)
for n in ['config.json','freeze.json','near95_members.csv','frequency_composition.csv','selection_sensitivity.csv','figureA_plot_data.csv','high_token_frequency_composition.csv','matched_same_token_group_summary.csv','predetermined_member_matched_examples.csv','per_member_token_top10.csv','matching_config.json','matching_summary.json','prefix_annotation_v2_codebook.json','prefix_annotation_v2_summary.json','audit.json','summary.json','token_detail_summary.json']:
    shutil.copy2(O/n,D/n);origin[n]=str(O/n)
for cn in [False,True]:
    src=W/('supplement_near_domain_tokens_cn.md' if cn else 'supplement_near_domain_tokens.md');dest=D/('README_cn.md' if cn else 'README.md')
    # A reading pointer, rather than a divergent second editable report.
    dest.write_text(('# 阅读入口\n\n' if cn else '# Reading entry\n\n')+f'[{src.stem}]({src})\n\n'+('本目录为有来源清单的精选证据，原始缓存保留在执行侧。\n' if cn else 'Selected evidence with a payload manifest; raw caches remain execution-side.\n'));origin[dest.name]=str(src)
manifest={'parent_asset_id':'analysis_a15_27_04_r10_domain_member_atlas_20261030','new_asset_ids':['analysis_a15_27_r10_token_context_audit_20261030','analysis_a15_27_r10_near_domain_token_context_20261030'],'files':[dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p),origin=origin[p.name]) for p in sorted(D.iterdir()) if p.name in origin],'raw_payloads_in_execution':True,'font_not_tracked':True,'new_model_forwards':0}
(D/'payload_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

M=R/'daily_research_reports/1031/meeting_report';H=M/'history';H.mkdir(exist_ok=True);history=[]
for name in ['meeting_brief_crosscoder_domain_members_cn.md','meeting_brief_crosscoder_domain_members.md']:
    p=M/name;old=H/(p.stem+'_pre_near_domain_20261030'+p.suffix)
    if not old.exists():shutil.copy2(p,old)
    history.append({'current_path':str(p),'historical_copy':str(old),'historical_sha256':sha(old)})

cn=f'''# 组会总稿：领域区分成员、近单域使用与真实 token

目的：最能区分数学／生物的 CrossCoder 成员，在参考频率、共同谱和真实上下文里如何组织？三个待检验直觉是“区分成员更罕见”“两域分占不同谱位置”“领域偏向来自领域专属词或语义”。模型、字典和原门控固定；本轮只复用缓存。以下认识是观察证据支持的有限解释，科研接受仍为 Unknown。

## 认识更新一：能区分领域与几乎单域使用不同，关于稀疏性的判断须说明选的是哪一组

**结果分析。** R10从16,384坐标出发，发现集至少一域5篇激活、包含零的文档平均z排序概率≥0.75，冻结数学433／生物527名。频率可判定者432／525名，高频占66.7%／54.3%，并不以低频为主。

在同一名单中，以偏向域≥5篇、另一域≤1/30篇，且≥95%正激活位置来自偏向域的发现规则，另冻结近单域31／24名。频率可判定30／22名，数学低/中/高9/19/2，生物12/9/1；比父集合更偏低中频。参考频率中位数0.400%／0.217%。旧留出19/31、21/24仍满足近单域规则，其余保留，不重新选人。严格零异域激活为14／15名，留出仍严格8／13名；它与55名是不同分母。

![近单域参考频率]({D}/figure_frequency_near_domain.png)

**如何读图。** 横轴是父集合／近单域／严格子集／支持池，纵轴是可判定成员人数比例；柱顶为可判定／冻结人数。独立DCLM频率=z>0计数/65,536，原分组切点0.259399%和1.344299%，至少20次。近单域3名参考支持不足，保留另表。log等宽规则下数学多数改称低频，故“中频最多”依规则；不能把组名当绝对属性。

## 认识更新二：领域响应可以不同，而共同谱位置相近；几何与真实使用是不同读数

**结果分析。** 完整960名单位decoder在同一发现集共同谱上的逐PC分布重合0.9493；64PC合并后0.9686。匹配背景逐PC95%参照0.9466–0.9576，实测在其中，未建立超出字典背景的特殊重合。前64份额数学10.03%、生物11.52%，PC1仅0.053%／0.120%，其余前部方向承担主要前偏；两组均落在细匹配背景内。不能仅从前部高就称领域成员特殊。

![完整名单的谱位置与重合]({W}/figures/figure3_overlap_and_use.png)

**如何读图。** 上排横轴共同PC／谱段，纵轴为单位decoder的组平均平方投影；阴影是较小份额。下排固定同一输入域，先对全部组成员z×还原decoder求向量和，再投影平方；它是组贡献向量自身能量分布，不是完整表征方差解释率。数学组在数学／生物文本前64能量51.93%／27.27%，生物组20.88%／49.70%。相近几何与不同使用方式可以并存，不能推出功能相同。

本轮55名另算逐PC0.8303、分段0.9562；相同31/24组规模及频率/支持匹配背景0.8203–0.8459，实测仍在其中。[55名谱图]({D}/appendix_near_geometry.png)放附录。组规模变小会改变平均分布，不能直接与960名0.9493比较而称更分离；未新增55名重构能量。

## 认识更新三：近单域使用不等于词面专属；同词面仍有前文关联，但整组主要成因和领域语义尚未确定

**结果分析：真实激活了哪些 token。** 高响应沿用发现集正激活p90，不改阈值。数学25/31、生物18/24名满足≥5高响应事件、≥2文档的构成支持；各6名留表，不换人。每名先统计位置比例，再成员等权。类别只按发现集输入文档覆盖冻结，留出40篇6,400位置评估。

![图A：哪些token，两域共用还是本语料偏域]({D}/figureA_token_categories_and_names.png)

**如何读图A。** 上排横轴四类token，纵轴成员等权高响应份额；彩柱对照全部可用位置灰柱，黑菱形再匹配高响应所在文档的暴露量。两域各≥5篇出现才称共用；某域≥5且另一域≤1篇才称本语料偏域，均不是语义专属性。

数学／生物的共用份额33.2%／31.7%，本域关联5.4%／10.2%；其他或支持不足61.2%／58.0%。不能把未归类多数当成领域词，也不能说多数是共用词。共用份额并未高于37.0%的全部位置背景。数学本域5.4%与同文档5.1%很接近，生物本域10.2%对2.4%有组成偏移，但这仍非语义证明。

下排按预定份额排名保留前8个真实ID和标点。数学常见` the`、` of`、` a`、逗号，也有`sum`、` =`、`}}`；生物有` cells`、` cell`、句点、` the`、逗号。`cells`5.17%来自3/18名，不能代表全部；` Bat`来自一名一篇，保留但不赋予群体含义。菱形还显示生物组`the`高响应份额低于输入背景，常见不能直接称偏好。

**结果分析：同token比前文。** 匹配不使用激活，精确固定目标及前一token ID、体裁、40位置区间与句/段边界；来源层级再固定网站。主词为用户指定、发现集中最常见共用词` the`（279），留出118数学／171生物位置，各20文档。

![图B：同一token不同前文]({D}/figureB_same_token_context.png)

**如何读图B。** 上排横轴为偏向域减另一域的高响应成员比例差；对全部31/24名含零统计，再对文档对等权，线为1,000次文档对重采样95%探索区间。15文档对／24位置对下，数学+1.22百分点[0.43,2.15]，生物+1.39[0.14,3.06]。至少一次匹配高响应者仅6/31、5/24名。再匹配来源仅6文档对／10位置对，保留原the位置8.5%／5.8%，只有一网站；生物区间[0,4.51]触及零，来源解释保留。

下排固定两组发现排名首位，不换成员。f16271同ID在数学前文后z=0.0934、另一前文为0；f1391两边都0，明确覆盖不足。例子只示意，完整匹配支撑统计。总共34个共用ID均尝试匹配，只有5个达到≥5文档对；其他4个的区间均触及零，不能把the图推广成所有token或全部55名的复现。

**认识边界。** 当前token身份不足以解释部分响应；前文术语、主题、格式和来源尚未分离。因此“主要由哪一因素驱动整组”和“是否编码领域对象”尚未回答，不把共用词上的激活直接称领域语义。

## `the`指代对象：已读前文与事后描述分开

已生成全部6,400个前文盲标注窗口，只有随机ID与目标之前的40token。五类为领域术语/对象、领域关系/推理、通用叙述、格式/引用、无法判断。规则提议、反例和人工核查栏保存，人工状态PENDING。初版把术语未命中误当通用叙述；保留旧版并另记v2改为需正面话语证据，否则无法判断。规则标签不是人工语义真值，主结论不使用其比例。

后续名词短语只作事后描述。四种the/The精确ID共333位置，主279有289位置，55名×289=15,895行核查表保留全部前文、z、单列后文和空白对象标签。主ID后续首词223种，其中211次在发现结构未见，48次仅单域≤2篇支持；不能靠后续词给对象判专属性。`set`发现仅数学而生物留出也出现，是反例。**the所指对象是否强领域特殊，尚缺可靠标注；没有把缺标注当成否定结果。**

## 汇报追问与证据入口

**为什么这个比较有用？** 固定当前及前一token，限制位置和体裁后仍有差异，削弱当前词面单独解释；同文档输入背景检查避免把“词本来常见”当偏好。它们不等于配对干预，仍有前文词汇与来源的竞争解释。

**为什么还不说领域语义或功能？** 语义对象尚未人工标注，来源匹配覆盖损失大，旧留出已暴露，匹配只近似局部句法；没有模型干预或任务收益。谱分布相似也会隐藏方向符号和组合。

[完整五项 R10 Summary]({W}/summary_cn.md) · [本轮定义、全部结果与复现]({W}/supplement_near_domain_tokens_cn.md) · [55名逐成员总表]({D}/near95_members.csv) · [每成员前10 token]({D}/per_member_token_top10.csv) · [全34ID匹配状态]({D}/matched_same_token_group_summary.csv)。全部高响应阈值、原始z与排序保留；完成18类数值/分母核查。3张主图，其余3张附录。新前向0、训练0、新PCA0；人工对象核查仍待完成。此次缓存汇总后停止，不自动开新实验。

历史16+16小名单总稿已逐字节保留在[历史副本](history/meeting_brief_crosscoder_domain_members_cn_pre_near_domain_20261030.md)，不能混用旧分母或将旧R07称独立谱稳健性。
'''
(M/'meeting_brief_crosscoder_domain_members_cn.md').write_text(cn)
en=f'''# Meeting brief: discriminators, near-single-domain use and real tokens

Purpose: distinguish stable math/biology discrimination, sparse single-domain use, spectral location and token/context response using the unchanged A22 shared-z dictionary and cached natural documents. Scientific acceptance remains Unknown; exposed heldout statistics are exploratory.

## Belief update1: discrimination and near-single-domain use select different frequency compositions

R10 starts from16,384coordinates, either-domain≥5active discovery documents and oriented zero-inclusive document-mean AUC≥.75, yielding433math/527biology. High reference-frequency shares are66.7%/54.3%among classified members.

The discovery-frozen near-domain subset requires≥5preferred active documents,≤1/30opposite document and≥95%preferred positive positions:31math/24biology. Classified30/22members have low/middle/high9/19/2and12/9/1, median DCLM rates.400%/.217%. Thus near-single-domain use shifts lower, without implying global rarity. Heldout19/31and21/24retain the rule; all55remain. Strict14/15is separate, with8/13remaining strict. Original cuts.259399%/1.344299%and≥20reference hits apply; log-bin majority labels differ.

![Frequency]({D}/figure_frequency_near_domain.png)

Read columns as populations and y as member fractions; top labels give classified/frozen counts. DCLM nativez>0over65,536positions measures feature frequency, not token frequency or spectral location.

## Belief update2: similar spectral location can coexist with different actual use

Parent960unit-decoder PC overlap.9493and64PCoverlap.9686fall within the finer matched-PC reference.9466–.9576. First64means10.03%/11.52%,PC1only.053%/.120%,also within matched references. Geometry does not establish a special location beyond dictionary composition.

![Parent spectrum and actual use]({W}/figures/figure3_overlap_and_use.png)

Top plots use unit-direction squared projection in one common pooled-discovery spectrum. Bottom uses the sum of scaledz×decoder vectors before projection and squaring. First64group-vector energy changes with input:mathgroup51.93%onmath/27.27%onbiology;biologygroup20.88%/49.70%. These are group-vector energy shares, not full-h variance explained. Near55geometry is separate:.8303PC/.9562binned,within same-size matched.8203–.8459. Do not compare different group sizes as special separation, or spectral distribution as function.

## Belief update3: near-single-domain use is not lexical exclusivity; partial same-token context association remains, but principal cause and semantics are unresolved

Fixed discovery-positivep90thresholds and≥5events/2heldout-document composition support retain25/31mathand18/24biology,with six per group insufficient. Normalize within features then average equally. Token categories freeze discovery INPUT coverage, not activation:shared≥5documents/domain;domain-associated≥5preferredand≤1opposite;remainingother/low-support. Evaluate40old-heldoutdocuments/6,400positions.

![FigureA]({D}/figureA_token_categories_and_names.png)

Read top x as categories,y as equal-member high-position fractions;gray bars use all available positions,diamonds match document exposure. Shared shares33.2%/31.7%,own-domain5.4%/10.2%,unclassified61.2%/58.0%. Neither a shared majority nor semantic domain-exclusive tokens are established. Shared input background37.0%;matched34.9%/38.2%. Math own-domain5.4%versus5.1%matched is small;biology10.2%versus2.4%is a panel composition shift.

Bottom shows actual top8IDs,including punctuation.Math includes`the`,`of`,`a`,comma,`in`,`sum`,`=`,`}}`;biology includes`cells`,`cell`,period,`the`,comma.`cells`5.17%comes from3/18members.`Bat`comes from one member/one document and is retained without a group-level claim.Biology`the`is below its document-matched background.Commonness alone is not preference.

![FigureB]({D}/figureB_same_token_context.png)

Match exact target/previous-token IDs,genre,40-position-bin and sentence/paragraph boundary without activations;source level additionally matches host. All34eligible shared IDs are attempted;5reach≥5local-documentpairs. MainID279` the`has118math/171biologypositions across20documents/domain. Average high indicators across ALL31/24members,including zeros,within document pairs and then across pairs equally.15pairs/24positions give preferred-minus-other+1.22pp[.43,2.15]mathand+1.39[.14,3.06]biology;only6/31and5/24have any matched high support. Source matching leaves6pairs/10positions,one host,8.5%/5.8%of opportunities;biologyinterval[0,4.51]touches zero. Other4sufficiently paired IDs'intervals touch zero. These are1,000document-pair-bootstrap exploratory intervals,not all-token or all-member replication.

Bottom examples retain the first discovery-ranked member/domain:f16271respondsz=.0934above.0817after a math prefix versus0after a biology prefix.Fixedf1391is0on both matched prefixes and is insufficient coverage,not replaced.Cases illustrate;all pairs drive inference.Current identity alone does not explain every response,but terminology,topic,format and source remain live explanations.Full syntactic/semantic matching is absent.

## Prior visible context and later referents remain separate

6,400activation-blind40-token prior windows have randomizedIDs,rule proposals,five categories and blank human-review fields.Human review PENDING.Version1mistook no lexicon hit for generic narration;it is preserved,andv2requires a positive discourse cue or marks undetermined.No unreviewed semantic percentages support the main claims.`polygon`is a lexicon-miss counterexample;low-response`species`shows a term need not activate.

Fourthe/TheIDs have333positions;ID279has289and223following-first-word types,with211occurrences unseen in the discovery structure and48supported by≤2single-domain documents.All55×289=15,895rows keep prior text,z,thresholds,separate future previews and blank human noun-phrase/referent labels.Later lexical text is posthoc description only.The domain specificity of referents remains unanswered;missing labels are not a null result.

## Q&A and evidence

Why useful?Fixing word IDs and local environment weakens a current-identity-only account;document-matched backgrounds separate input commonness from composition shift.Why not semantics or function?Source/previous vocabulary remain confounded,human referent labels are missing,oldheldout is exposed,and no intervention/task benefit was measured.

[Full five-part Summary]({W}/summary.md) · [Definitions/results/reproduction]({W}/supplement_near_domain_tokens.md) · [Members]({D}/near95_members.csv) · [Per-member top10tokens]({D}/per_member_token_top10.csv).18audit categories pass.Three main figures/three appendices;0new forwards/training/PCAfits.Stop after cache-supported delivery.Historical16+16brief bytes are retained in[history](history/meeting_brief_crosscoder_domain_members_pre_near_domain_20261030.md);different denominators must not be pooled.
'''
(M/'meeting_brief_crosscoder_domain_members.md').write_text(en)
(D/'meeting_history_receipt.json').write_text(json.dumps(history,indent=2)+'\n')
idx=R/'daily_research_reports/1031/README.md';idx.write_text('''# October31 meeting

[Current speaking entry: CrossCoder domain discrimination and near-single-domain tokens](meeting_report/meeting_brief_crosscoder_domain_members.md) · [中文组会总稿](meeting_report/meeting_brief_crosscoder_domain_members_cn.md).

One current brief covers R10 main433math/527biology and the separately frozen near-domain31/24subset. It presents belief updates before analysis, main figuresA/Band reference-frequency composition, source/coverage limits, and pending human referent annotation. Cache-only; zero new forwards/training.

[Owning R10 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary.md) · [中文](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary_cn.md) · [Near-domain supplement](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/supplement_near_domain_tokens.md).

The older16+16speaking entry is preserved byte-for-byte in[history](meeting_report/history/meeting_brief_crosscoder_domain_members_pre_near_domain_20261030.md). Its support rule, PCA interpretation and denominators are historical and must not replace R10.
''')
print('PACKAGED',D,'AND UPDATED',M)
