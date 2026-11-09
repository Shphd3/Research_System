"""Create bounded reading records from completed R10 statistics, preserving old rounds."""
from pathlib import Path
import json,csv,shutil,hashlib,datetime,collections
ROOT=Path('/data/250010109/Research_System');OWN=Path(__file__).resolve().parents[1];BASE=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response');O=BASE/'R10_domain_member_atlas_20261030';A=O/'analysis';T=O/'tables'
ANCHOR=ROOT/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor.md'
R=json.loads((A/'results.json').read_text());AUD=json.loads((A/'audit.json').read_text());G=R['geometry'];F=json.loads((O/'freeze.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert AUD['failed']==0
def write(p,s):p.write_text(s.strip()+'\n')
def rows(p):return list(csv.DictReader(p.open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Small, explicit reading payload only. Large pair/position arrays and pair tables stay execution-side.
selected_tables=['master_members.csv','flow_counts.csv','frequency_counts.csv','sensitivity_summary.csv','member_spectrum.csv','group_pc_spectrum.csv','group_reconstruction_energy.csv','context_categories.csv','context_effects.csv','matched_strata.csv','fine_matched_strata.csv','old_list_intersections.csv','real_token_examples.csv','panel_token_counts.csv']
for name in selected_tables:shutil.copy2(T/name,OWN/'tables'/name)
for folder in ['figures','appendix']:
 (OWN/folder).mkdir(exist_ok=True)
 for p in (O/folder).glob('*.png'):shutil.copy2(p,OWN/folder/p.name)
for p in [O/'freeze.json',O/'source_manifest.json',A/'results.json',A/'numerical_checks.json']:
 shutil.copy2(p,OWN/'provenance'/p.name)
shutil.copy2(A/'audit.json',OWN/'provenance/numerical_audit.json')

# NOT RUN target-only completion proposal, derived offline from existing exact E0 prefixes.
from tokenizers import Tokenizer
tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')
panel=[json.loads(s) for s in (BASE/'R07_fixed_target_domain_spectrum_20261029/data/panel.jsonl').read_text().splitlines()];proposal=[]
for r in panel:
 if r['split']=='heldout' and r['ending']==0:
  assert r['text'].endswith('example');text=r['text'][:-len('example')]+'explanation';ids=tok.encode(text,add_special_tokens=False).ids
  proposal.append(dict(source_seq_id=r['seq_id'],family=r['family'],domain=r['domain'],wording=r['wording'],text=text,token_ids=ids,target_token_id=ids[-1],target_position=len(ids)-1,source_target_position=r['target_position'],target_position_unchanged=len(ids)-1==r['target_position'],status='NOT_RUN'))
assert len(proposal)==48
(O/'proposed_B_NOT_RUN.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in proposal))
validtokens=sum(len(r['token_ids']) for r in proposal);padded=48*256
write(OWN/'missing_evidence.md',f'''# Evidence gaps and minimal NOT RUN supplement

Pure target-only comparison B is missing. Existing E0/E1 keep the core text but change `This passage presents a concrete example` to `This passage provides a brief explanation`. Treat it as target-plus-suffix sensitivity. A is available: target IDs3110/16148 are fixed per ending, and every math/biology pair has the same target index; global family positions range30–38.

A minimal **AI proposal**, not authorization: reuse the48 existing E0 rows from12 exposed-heldout families ×2domains ×2wordings. Add `explanation` under the EXACT E0 preceding prefix, giving96 crossed conditions with48 cached and48 new. Offline tokenization gives{validtokens} valid prefix tokens; all target positions unchanged={all(r['target_position_unchanged'] for r in proposal)}. A sequential256-padded implementation would process{padded} model token positions and48 new complete-prefix forwards. Native joint-14-layer z and original gate remain required. Actual batching, wall-clock and GPU cost are Unknown until execution design/authorization. Save all main960 responses, no reselection. Proposed texts are execution-side `proposed_B_NOT_RUN.jsonl`; executed forwards0. New target wording also changes meaning; this comparison estimates a target-form/meaning effect and cannot prove pure identity. No new blind families are created.

An independent natural-reference PCA is also MISSING: R07's archived basis is byte-identical to the R04 pooled discovery basis. R08's target-token PCA is a different object. No independent robustness claim is made and no new representation extraction is run.
''')

definition='''# Definitions and protocol changes

| Object | Computation / denominator | Interpretation and boundary |
|---|---|---|
| Native member | A22 joint14-layer shared z, original norm-weighted threshold | Not an independently encoded final-layer activation |
| Document response | mean z over positions32–191 including zeros,160 positions/document | All documents have equal weight |
| Support | >=5 positive discovery documents in at least ONE domain | Failed support is insufficient data, not no information |
| Raw AUC | all30×30 math/bio document comparisons, ties half | Stable ranking discriminator, not every nonlinear rule |
| Main set | support and direction-fixed discovery AUC>=.75 | All members retained regardless of later results |
| Heldout check | fixed direction,20docs/domain;1000 document bootstraps | Exposed exploratory reuse, not a new blind test |
| Feature occurrence | DCLM positive positions/65536; >=20 hits for bins | Occurrence is not activation strength or spectral position |
| Original frequency bins | low<=.002593994140625; middle<=.0134429931640625; otherwise high | Cuts belong to lower group; support<20 outside plotted denominator |
| Log-width sensitivity | cuts.0045172553628813825/.06686505701697326 | R09 used this as main; R10 uses original labels as main |
| Common spectrum | pooled9,600 raw block27 residual-post discovery h rows; one shared mean | Equal domain/doc/position weights,1024 full-rank PCs; no per-domain centering, whitening or h unit normalization |
| Unit projection | squared dot of unit decoder and each PC;1024 sum1 | No z, decoder norm or eigenvalue factor |
| Group overlap | sum PCwise minima of member-equal mean distributions | Band aggregation hides differences; not direction/function overlap |
| Matched background | eligible dictionary, same frequency/support strata/group sizes,1000 disjoint pair draws | Includes selected members; conditional reference range, not a generalization interval |
| Group reconstruction energy | sum z times restored decoder first, project/square, doc-equal mean, normalize | Cross terms preserved; not full-h variance explained |
| Panel token frequency | count ID within19200 natural analysis positions | Type bins: count1/count2/count>=3; type vs position denominators separate |
| High response | >discovery-positive-z90th percentile, threshold fixed before heldout | Quantile needs20 positives; composition needs5events/2heldoutdocs; otherwise retained as insufficient |
| Context A | paired math−bio native z at same target ID and paired position | Changes context/terms/format together; not isolated semantics |
| Ending contrast | E1−E0 at matched core text | Target AND suffix change; pure target identity B missing |

This round changes the support gate (both domains→either), replaces16+16 with all AUC>=.75, fixes Top16/64/128 and.70/.80 sensitivities, makes pooled natural-all-token covariance explicit and uses panel-token counts. It does not splice old32-member values into the new960-member figures. Old R07 “independent natural spectrum” wording is corrected for this analysis: it is the same R04 discovery spectrum. Old rounds are preserved. Old global Top16=9math+7bio is distinct from old per-domain16; every old membership has a separate mapping.
'''
write(OWN/'definitions.md',definition)
write(OWN/'definitions_cn.md','''# 对象定义与协议变更

| 对象 | 本轮定义 | 解释边界 |
|---|---|---|
| 成员 | A22原生14层联合编码、共享z、原门控 | 不是最后层单独编码的激活 |
| 文档响应 | 每篇第32–191位置的z均值，160个位置，含零 | 文档等权，不把token当独立文档 |
| 支持合格 | 发现集至少一域有5篇不同文档激活 | 未通过不等于没有区分信息 |
| 区分度 | 数学文档响应大于生物的概率，平局半次；偏向由发现集冻结 | 稳定排序差异，不穷尽非线性区分 |
| 主集合 | 支持合格且方向校正区分度≥0.75的全部成员 | 不按留出表现换人；0.75是操作阈值 |
| 留出复核 | 每域20文档，1000次文档重采样，固定发现方向 | 旧数据已经看过，探索性复核 |
| feature发生率 | DCLM中z>0的位置数/65536，至少20次才分组 | 不等于强度或谱位置 |
| 原频率阈值 | 低≤0.2593994140625%；中≤1.34429931640625%；其余高 | 边界归较低组；<20次不画入三组分母 |
| log敏感性 | 0.4517255362881382%与6.686505701697326% | R09曾作主分组，本轮保留作对照 |
| 共同谱 | 60篇发现文档×160个真实block27 residual-post向量；共同均值 | 两域/文档等权，完整1024PC；不分域去均值、不白化、不先单位化h |
| 单位投影 | 单位decoder与PC内积的平方，完整合计1 | 不乘z、范数或特征值 |
| 谱重合 | 两组等权平均投影逐位置取较小值再求和 | 不是方向、语义或功能重合 |
| 匹配背景 | A01合格池按发生次数半octave区间、总支持篇数/最大域支持篇数各5篇区间匹配组规模，1000次无放回抽取，两组不重叠 | 池包含主集合；是条件字典参照，非泛化区间 |
| 实际贡献能量 | 先求组内z×尺度还原decoder的向量和，再投影平方，文档等权归一化 | 保留交叉项，不是完整表征方差解释率 |
| token语料内频率 | 本批19200位置中token ID计数 | 类型分位点为1/2次；同频不拆，三组不等大 |
| 高响应事件 | 严格超过发现集正z第90百分位 | 定阈值至少20正事件；留出组成至少5事件且跨2文档，不足保留 |
| 上下文对照A | 同目标ID、同配对位置，数学减生物z | 词汇、格式和主题仍共同改变 |
| 词面/后缀对照 | 核心前文相同，E1减E0 | 同时改变目标词和后缀；纯换目标词B未运行 |

与旧版的变化：两域均需5篇→至少一域5篇；每域16→全部AUC≥0.75；固定Top16/64/128和0.70/0.80敏感性；明确两域自然文本全token共同谱；token频率改用本批语料。旧R07谱并非独立来源，而是同一R04发现谱。旧全局Top16（数学9/生物7）、旧每域16、R09贡献Top32/141并集/36复现均单列映射，不混用分母。
''')

cn=f'''# R10：领域区分成员的频率、共同谱与真实响应

[English](summary.md) · [冻结协议](protocol_cn.md) · [详细证据](detailed_cn.md) · [定义与变更](definitions_cn.md) · [主名单](tables/master_members.csv)

目的：数学／生物文档中最能稳定区分两域的CrossCoder成员，在使用频率、共同表征谱以及词面／上下文响应上如何组织？三条待检验直觉是“较少出现者更能区分”“两域成员分占不同谱位置”“领域偏向体现跨措辞上下文”。竞争解释分别是高频成员的强度差、相近谱位置、领域词汇及格式或交互。以下认识更新是基于本批数据的AI解释，科研接受与问题关闭仍为Unknown。

## 如何选成员，以及这次修正了什么

用同一个A22原生14层共享z字典，完整16,384坐标起步。发现集每域30篇，每篇固定第32–191共160位置，对z取包含零的文档均值；不同文档等权。先要求至少一域有5篇激活，再算数学均值超过生物均值的配对概率，平局半次。按偏离0.5的程度和ID排序，冻结方向校正区分度≥0.75的全部成员：数学433，生物527，共960。0.75只表示约四分之三跨域文档对能排对，不是语义真理。

| 阶段 | 数学偏向 | 生物偏向 | 总数 |
|---|---:|---:|---:|
| 完整字典 | — | — | 16,384 |
| 发现集至少一次激活 | — | — | 13,997 |
| 支持合格 | 5,473 | 4,586 | 10,076，另有17个AUC=0.5无方向 |
| 主集合：AUC≥0.75 | 433 | 527 | 960 |
| 原留出区间下界>0.5 | 357 | 431 | 788 |

未合格者中2,387个发现集全零，3,921个虽激活但两域各自均不足5篇；这是支持不足，不是证明无信息。留出方向与发现一致为429/433、525/527；方向一致也不等于区间排除0.5。留出是已反复使用的数据，只能称探索性复核。960个成员全部保留，不换人。

新门槛允许领域单侧支持。例如数学排名前两位f16122、f16271的发现文档支持分别为30/3、30/1，原始AUC均为1，不在旧“两域均5篇”截取内；真实高响应也可能落在`and`、`or`等词上。这正是不能预先把领域区分成员解释为领域词条的原因。各坐标的支持、频率及五项状态在同一主表相连。

## 认识更新一：领域区分并不主要由少见成员承担；高复用成员也能区分这两域

**结果分析。** 在频率可判定成员中，数学低/中/高为19/125/288（分母432），生物为58/182/285（分母525）。高频比例66.7%/54.3%，高于支持合格池的44.1%；低频4.4%/11.0%，低于池的16.7%。主集合并没有低频富集。发生率是独立DCLM的z>0次数/65,536，主分组阈值0.259399%和1.344299%，至少20次。数学1、生物2、池101个支持不足，只从本图三组分母排除，仍保留主表。

![图1 参考feature发生率](figures/figure1_frequency.png)

**如何读图。** 对象为主集合433/527以及支持池10,076成员；筛选样本每域30篇。横轴为低/中/高feature发生率组，纵轴为成员比例；每根柱代表一组成员，柱上同时标人数与比例。先比较同颜色三柱，再在同频组比较领域柱与灰色背景。图中高频是本字典相对分组，不表示在多数token上激活；也不是谱的前部。

**竞争解释与边界。** 原分组下Top16两域以中频最多；扩大到主集合则高频最多，所以“中频最多”依赖排名截断。Top16/64/128、AUC0.70/0.80均保存，不能用16人的组成代表960人。log等宽分组下中频83.3%/65.0%，但低频仍低于池背景；“低频没有富集”的方向保留，具体组名的多数会改变。筛选本身偏向稳定文档响应，对极罕见区分信息的覆盖有限，不能推断整个字典或所有知识皆由高频承担。

## 认识更新二：领域响应偏向不同，并不要求占据分开的谱位置；相近朝向下，实际使用仍随输入改变

**图2结果分析。** 共同谱来自两域发现集60篇×160位置=9,600个真实block27 residual-post向量，以一个共同均值中心化。每域、每文档、每位置等权；不先按域去均值。完整1024PC满秩，decoder先单位化，逐PC内积平方合计1。旧R04谱经原h协方差审计正好满足此定义，因此固定复用；R07用的也是同一谱，不能再称独立稳健性证据。

数学/生物PC1–64均值10.03%/11.52%，中位数6.84%/8.79%。匹配背景均值95%参照区间9.11–10.21%/10.59–11.76%。A01匹配了实际发生次数半octave区间（同层最多相差√2倍）、总支持篇数和最大域支持篇数各5篇区间以及组规模；两组均值均落在细匹配参照内，特殊前偏未建立。原粗频组匹配参照为8.09–9.33%/9.24–10.62%，会让前偏看起来更特殊，故保留为旧版方法对照；参照池含入选成员，平均约40.0%/40.5%的抽样成员也属于主集合，因此是条件字典比较，不是独立空假设或选择重采样区间。

PC1仅占完整单位长度的0.053%/0.120%，PC2–64占9.98%/11.40%，后者的维数参照为63/1024=6.15%。前偏不是由PC1主导。数学约55.0%、生物74.0%的成员前64份额超过64/1024；均值高于中位数说明尾部仍在抬均值，不能称所有成员都有同等前偏。去掉前偏最高10%后均值7.40%/9.48%，该值是附加描述，不是重新筛选。

![图2 decoder谱位置与PC1拆分](figures/figure2_decoder_spectrum.png)

**如何读图2。** 对象始终为433/527成员和相同9,600个发现位置。上方横轴是16个64-PC谱段，纵轴是完整单位decoder平方长度份额。淡点是成员，实线为均值、虚线中位数、灰带为匹配字典参照、黑点线为全字典。先读均值和灰带，再看淡点与中位数是否支持“多数”。下方分成1/63/960维，菱形是维数比例；不能直接比较不同维数段的绝对总份额来判断富集。这里是几何朝向，不是知识量或实际贡献。

**图3结果分析。** 两组逐PC平均平方分布重合0.9493，每64PC合并后0.9686。匹配参照的逐PC范围为0.9466–0.9576，观测位于其中；原粗匹配为0.9508–0.9610，仅作方法对照。没有证据说这两组“比匹配字典更重合”。PC2–64原始全谱质量分别9.98%/11.40%，在该段内各自归一化后的重合0.9192，不能把0.9192当全谱份额。两组实际decoder子空间秩433/527，trace/min-rank重合0.5314；逐对绝对余弦均值0.0251。这些对象与0.9493不是同一种“重合”。

在40篇原留出自然文本上，先对组内所有z×尺度还原decoder求向量和，再投影平方，保留交叉项。数学组在数学/生物输入上的前64能量份额51.93%/27.27%；生物组在数学/生物输入上为20.88%/49.70%。对应总平均平方范数分别22,684.6/2,034.1、2,625.8/27,591.6，均远离零，不是小分母制造的比例。它们描述组重构向量自身的能量，不能称完整h的方差解释率。

![图3 谱分布重合与实际重构能量](figures/figure3_overlap_and_use.png)

**如何读图3。** 上排沿用图2的单位几何量：横轴共同PC或谱段，纵轴组内成员等权平均平方投影，阴影是两组较小份额。右上只放大PC2–64，曲线仍以完整单位长度为分母。下排换成实际贡献量，横轴同谱段，纵轴是组向量平方能量归一化份额；左/右固定数学/生物输入，各20文档×160位置，蓝/橙分别为433/527成员组。先在同输入图内比较两组，再跨输入比较同一颜色，避免把成员与输入差别混为一谈。

**竞争解释与边界。** 单位几何谱位置相近，与实际使用方式不同可以同时成立。谱平方分布隐藏符号和方向组合，不能推出功能或学习方向相同。平均谱分布会随组规模变平：Top16/64/128逐PC重合0.7652/0.8797/0.9110，不能把主集合0.9493当排名规模不变的量。AUC0.70/0.80为0.9593/0.9295，仍显示大量谱位置重合。共同谱由这两域本身构成；领域差异被它容纳不算独立验证，真正独立自然谱稳健性尚缺。

## 认识更新三：领域偏向不等于词汇专属或纯token身份；上下文与词面／后缀关联可以并存，但当前覆盖很有限

**图4结果分析。** token频率改为本批120文档的19,200分析位置，同tokenizer按ID计数。类型计数分位点落在1/2次，同频不拆，因此低/中/高类型数2,782/888/1,203，位置数2,782/1,776/14,642；本批没有特殊token。子词、标点均保留。高响应阈值来自每成员发现集正z第90百分位，在留出严格超过它；371/433数学、472/527生物满足量化/事件支持，另62/55保留为不足。

数学高响应位置的低/中/高token频率组份额为11.2%/8.1%/80.6%；生物27.1%/13.6%/59.3%，先按成员统计再等权平均。全部位置背景为14.5%/9.25%/76.3%。故数学更偏本批高计数token，生物相对背景更多低计数token，但都不能说只响应罕见词。支持成员的高响应不同token ID中位数17/20，前5种ID占比中位数45%/40%，既跨词又有集中性。feature参考发生率与高响应token计数中位数的Spearman相关为−0.052/−0.388；不能据此说两组存在统一的稳定正相关。

![图4 真实token与语料内频率](figures/figure4_real_tokens.png)

**如何读图4。** 左上横轴是本批token ID计数低/中/高组，纵轴是每成员高响应位置比例的成员等权均值；灰柱是全部有效位置背景，分母与类型数不同。右上每点为一个有支持主名单成员，横轴独立DCLM feature发生率，纵轴其高响应位置token在本语料出现比例的中位数，细线为10–90分位范围，两轴为对数；本批计数均正，未把未见当零。下方实例固定取发现排名前两位/域，显示真实输入token和已读前文，数值分别为高响应与另一文档同ID低响应。完整前三名实例及全部成员的高/普通/同ID低例子均在执行表中。字符串`and`等不能被词义直接判断为该feature语义。

**图5结果分析。** 现有384条件=48家族×2域×2措辞×2目标+后缀；发现/开发/原留出为24/12/12家族。example目标ID3110、explanation为16148，各域配对的目标token和位置都一致，跨家族目标索引30–38。数学33、生物21个在至少一个固定目标上跨措辞并跨发现/原留出复现上下文方向；其中11/2个跨两个目标都符合。词面+后缀复现59/35，交互26/19，其中仅22/12个的复现上下文方向也与自然文本领域偏向一致；其余11/9个在受控条件下方向反过来，更不能泛称同一种领域语义。这些标签可以重叠，均为逐成员点式探索区间，未做多成员确认性发现。

按互斥汇总口径：仅当前上下文响应1/1；词面+后缀敏感26/16；两者或交互33/20；不足373/490。此处“仅”只指本次标签，不证明没有另一种效应。所有划分始终不激活318/471，共789个，应判覆盖不足。高区分文档筛选从未排除领域词汇、来源或格式；固定token后的上下文响应可以削弱纯身份解释，却不能排除前文术语与主题。

![图5 上下文与目标加后缀](figures/figure5_context.png)

**如何读图5。** 上条为960成员的互斥描述标签人数/比例；紫色包含交互，不能直接当全部上下文成员。下方按目标词和措辞分列，发现/原留出分行。横轴为数学/生物前文，纵轴为原生z，0.001以下线性、以上对数。每条淡线连接一个成员×家族在两域的实际值；所有零计入，粗线及区间是成员等权均值和家族重采样。每格标题给有激活支持的成员数；两组颜色始终蓝数学/橙生物。读配对强度变化，不要求由有变无。

**尚未回答。** 纯粹固定前文只换目标词的B缺失。example/explanation同时换了后缀，不能当identity证明。[最小NOT RUN方案](missing_evidence.md)复用48条E0，再补48条同前缀explanation输入；预计{validtokens}有效token、256填充实现为{padded}模型token位置，实际耗时Unknown，当前新增前向0。需另行确认才执行，不能用现有结果填补该结论。

## 五项问题的直接结论

1. feature参考频率：全主集合高频最多且相对池更多；低频未富集，“中频最多”随TopK/分组规则改变。
2. decoder谱位置：温和前偏主要在PC2–64，非PC1主导；均值在细匹配参照内，特殊性未建立，且受长尾影响。
3. 谱分布重合：逐PC0.9493、分段0.9686；不高于匹配参照。实际贡献能量随输入变化，几何与使用要分开。
4. 真实token：高响应跨多个token，数学/生物的语料内频率组成不同；尚无统一稳定的feature频率→token频率联系证据。
5. 上下文/词面：少数有跨措辞上下文响应，多数目标覆盖不足；纯身份判断尚未回答。

## 交付与完成边界

已有测量是R04文本、z、真实h与DCLM计数，R07/R08受控文本及目标z，R09 decoder尺度。本轮新增的是全字典筛选、离线统计、匹配参照、贡献求和、token统计、成套图表及审计；模型前向0、训练0、距离扩展0。{AUD['passed']}项数值/契约断言及3000项A01细匹配核对通过，投影完整和误差约1.1e−15。9张精选图中仅5组主图，其他放附录。未覆盖旧结果，未提交或推送；科学接受Unknown，按范围完成后停止。
'''
write(OWN/'summary_cn.md',cn)

en=f'''# R10: A whole-dictionary atlas of domain-biased CrossCoder members

[中文](summary_cn.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [Definitions](definitions.md) · [Member master](tables/master_members.csv)

Purpose: determine whether strong math/biology document discriminators are uncommon, occupy distinct positions in a common representation spectrum, and respond to vocabulary versus context. Three hypotheses compete with frequent reuse/intensity differences, similar spectral position, and vocabulary/format/interaction explanations. The following bounded conceptual updates are AI interpretations; researcher acceptance and closure remain Unknown.

## Selection and coverage

Start with all16,384 A22 native shared-z coordinates. Each discovery document contributes one mean over positions32–191 including zeros. There are30 documents/domain. Require >=5 active documents in EITHER domain, rank the math-over-biology pair probability with half-credit ties, and freeze every direction-corrected AUC>=.75. This operational threshold is not a semantic definition. There are13,997 discovery-active coordinates;10,076 eligible, including17 exact AUC ties;433 math/527 biology main members. Of the6,308 rejected for support,2,387 are discovery-zero and3,921 positive but under5 documents in both domains. Support failure does not establish no information.

On the exposed original heldout20 documents/domain,429/433 and525/527 retain direction;357/431 have oriented AUC pointwise95% document-bootstrap lower bounds>.5. Keep all960 main IDs. These are exploratory checks, not blind confirmation. The same master connects supports, reference rates, all five tests and missing statuses.

## Update1: domain discrimination need not be carried mainly by rare members

Frequency-classified math members are19low/125middle/288high (n432, one insufficient); biology58/182/285 (n525, two insufficient). Eligible-pool counts are1670/3904/4401 (n9975,101 insufficient). High proportions66.7%/54.3% exceed pool44.1%; low4.4%/11.0% fall below pool16.7%. Feature occurrence is positive native-z positions/65,536 independent DCLM positions. Original cutpoints are.002593994140625/.0134429931640625, inclusive below; at least20 hits are required.

![Figure1: feature occurrence](figures/figure1_frequency.png)

Read Figure1: x=low/middle/high reference-occurrence groups; y=member proportions among classified members; bars=math433,biology527 and eligible10076, with exact plotted denominators/counts. Selection used30 discovery docs/domain. Compare a group against gray before claiming enrichment. This updates the rare-member intuition; occurrence is not spectrum location or activation intensity. Top16 is middle-dominated whereas the full set is high-dominated. Log-width sensitivity gives middle83.3%/65.0%, yet low remains depleted versus its pool. Top16/64/128 and AUC.70/.80 are frozen appendix views. Selection favors repeatable document response and may miss extremely rare information.

## Update2: different domain responses do not require separate spectral locations; use can still differ

The common PCA is the pooled9,600 true block27 residual-post positions from60 discovery documents, with one common mean, equal domains/documents/positions, no within-domain recentering/whitening or h unit normalization. All1024 PCs are retained. Raw-h covariance auditing shows the old R04 basis already implements exactly this definition. R07 reused it; it is NOT an independent natural-reference corpus. Unit decoder squared projections sum to1 without z, eigenvalue or norm weighting.

Math/biology mean PC1–64 shares are10.03%/11.52%, medians6.84%/8.79%; fine-matched dictionary mean95% reference ranges9.11–10.21%/10.59–11.76%, both containing the observations. A01 matches half-octave occurrence bins (within-stratum rate ratio<=sqrt2), total/max-domain support bins of5 and group size, drawing disjoint sets from the whole eligible pool, including selected members. Mean selected inclusion is40.0%/40.5%; this is a conditional dictionary reference, not an independent null or selection bootstrap. PC1 shares are only.053%/.120%; PC2–64 shares9.98%/11.40% versus63/1024=6.15% dimensions. Mean front bias does not come from PC1. About55.0%/74.0% of members exceed the64/1024 dimensional share; higher means than medians retain an upper-tail effect.

![Figure2: unit decoder spectrum](figures/figure2_decoder_spectrum.png)

Read Figure2: same433/527 members and60 discovery documents. Upper x=16 equal64-PC bands; y=complete-unit-decoder fraction. Pale points=members, solid=mean,dashed=median,gray=matched reference,black dotted=whole dictionary. Read mean and median together. Lower x splits1/63/960 dimensions; diamonds are dimensional fractions, preventing comparisons of unequal-dimensional absolute totals. This is orientation, not knowledge amount or actual contribution.

PCwise overlap is.9493;64-PC-band overlap.9686. Matched PC overlap range.9466–.9576 contains the observation, so similarity is not above dictionary reference. The preserved coarse-v1 range.9508–.9610 is a method sensitivity, not the active reference. Within-PC2–64 renormalized overlap.9192 is separate from its full-vector masses9.98%/11.40%. Actual decoder subspace ranks433/527 have trace/minrank=.5314; mean cross-member absolute cosine=.0251. These measure different objects and do not imply common functions.

Actual heldout reconstruction sums z times TRAIN-RMS-restored decoder BEFORE squaring, preserving cross terms. Math-group first64 energy on math/bio inputs is51.93%/27.27%; biology-group values20.88%/49.70%. Total mean squared norms are22684.6/2034.1 and2625.8/27591.6, all away from zero. Each input-domain curve averages20 documents×160 positions. This is energy of the group's own reconstructed vector, not full-representation explained variance.

![Figure3: geometry overlap and actual use](figures/figure3_overlap_and_use.png)

Read Figure3: top uses the EXACT unit geometry of Figure2; x=PC/band,y=member-equal mean squared projections,shade=common minimum. Right zoom keeps original full-unit mass on y while reporting the separately normalized segment overlap. Bottom fixes input domain per panel and compares both member groups: x=same band,y=summed-vector energy fraction. Compare same input first, then same color across inputs. Similar orientations and different use coexist. Squared projection hides signs/combinations; none of these overlaps implies same semantics or learning direction. Top16/64/128 PC overlap=.7652/.8797/.9110 and AUC.70/.80=.9593/.9295; list size matters. The spectrum was constructed from these domains, so containing their difference is not independent validation.

## Update3: domain bias is neither lexical exclusivity nor pure token identity; coverage limits the context judgment

Token counts use this120-document19,200-position panel, separately from DCLM feature occurrence. Count-type quantiles land at1/2, with ties kept:2782/888/1203 token types and2782/1776/14642 positions. Punctuation/subwords stay; no special IDs occur. High response is strictly above discovery-positive-z p90. Composition support is adequate for371/433 math and472/527 biology;62/55 remain insufficient. Member-equal token-bin means are11.2/8.1/80.6% and27.1/13.6/59.3%, versus all-position14.5/9.25/76.3%. High responses are not limited to rare words. Median distinct high-response IDs are17/20, and median top5-ID event fractions45%/40%, showing both diversity and concentration. Feature-occurrence/token-count Spearman rho is−.052/−.388; no shared stable positive relation is established.

![Figure4: actual tokens](figures/figure4_real_tokens.png)

Read Figure4: left x=panel token count bins, y=per-feature high-event fractions averaged equally across371/472 usable members; gray=all positions. Right each point=a main member; x=DCLM feature rate, y=median panel token count/19200 at high events, thin lines=10–90% range; both axes log, no unseen IDs treated as zero. Bottom fixes discovery ranks1–2/domain, displaying real heldout input IDs/prefixes and exact-ID low examples elsewhere. Full rank1–3 examples plus all-member high/ordinary/same-ID-low instances remain execution-side. These are inputs, not vocabulary-decoded outputs.

The384 controlled rows contain48 families,2domains,2wordings,2target-plus-suffix endings, split24/12/12. Target IDs3110/16148 and positions match within every domain pair; global target indices range30–38. Recurrent fixed-target context response occurs for33math/21bio members at >=1 ending,11/2 at both. Only22/12 of the context-recurring members also agree with their natural-document direction;11/9 reverse in the controlled panel. Recurrent target-plus-suffix59/35 and interaction26/19 can overlap these tags. All are exploratory pointwise-bootstrap tags without multiple-member confirmatory claims. Mutually exclusive summaries are context1/1, suffix26/16, both-or-interaction33/20, insufficient373/490. No response anywhere in all splits occurs for318/471 (789 total); this is coverage failure, not identity.

![Figure5: context and suffix controls](figures/figure5_context.png)

Read Figure5: top bars count all960 main IDs. Lower columns facet target/wording; rows separate discovery24 from exposed-heldout12 families. Each faint pair is one member×family math/bio z; zeros are retained. Bold pairs and95% bars are equal-member means with family bootstrap. Native-z axis is linear below.001 and logarithmic above; each panel labels active-member counts. Blue/orange retain natural-domain bias group colors. Strength changes count even without on/off switching.

Pure target-only B is **unanswered**: example/explanation also changes the suffix. A minimum NOT RUN proposal reuses48 E0 rows and adds48 identical-prefix `explanation` rows, {validtokens} valid tokens or{padded}256-padded model positions; wall-clock/GPU cost Unknown. It needs separate forward authorization. Target replacement still changes meaning, so even that does not prove pure identity. Vocabulary,source,format and preceding terminology remain competing explanations.

## Five direct answers and completion

1. Feature frequency: full main sets are high-dominated; low is not enriched; majority labels change with TopK/binning.
2. Decoder position: modest orientation in PC2–64, not PC1; observed means are inside fine-matched reference ranges, so special front bias is unestablished.
3. Spectral overlap: PC.9493 / band.9686, not above matched reference; actual use energies depend on input.
4. True tokens: responses span multiple IDs, with different within-panel frequency compositions; no universal stable feature/token frequency law.
5. Context/identity: some recur across wordings, most lack target coverage; pure identity remains unanswered.

Existing measurements: R04 text/z/true h/reference counts; R07/R08 panel target z; R09 decoder scale. New work is offline screening/statistics/matching/vector composition/token/context tables and figures. Zero model forwards,training or distance expansion. {AUD['passed']} numerical/contract assertions pass, with3000 additional A01 background checks; full projection conservation error~1.1e−15. Five main groups plus four appendix images, with all raw tables and reproducible scripts saved. Old outputs unchanged; no commit/push. Stop after cache-supported delivery; researcher scientific acceptance remains Unknown.
'''
write(OWN/'summary.md',en)

if (T/'fine_matched_sensitivity.csv').exists():
 sr=rows(T/'fine_matched_sensitivity.csv');fr=rows(T/'frequency_counts.csv');outlines=[]
 for pre in ['main','top16','top64','top128','auc0.70','auc0.80']:
  pair=[next(r for r in sr if r['selection']==pre and r['domain_bias']==g) for g in ['math','biology']];major=[]
  for g in ['math','biology']:
   rr=[r for r in fr if r['selection']==pre+'_'+g and r['rule']=='original' and r['frequency']!='insufficient'];major.append(max(rr,key=lambda r:int(r['count']))['frequency'])
  outlines.append(f'| {pre} | {pair[0]["members"]}/{pair[1]["members"]} | {major[0]}/{major[1]} | {pair[0]["head_above_reference95"]}/{pair[1]["head_above_reference95"]} | {float(pair[0]["overlap_pc"]):.4f} |')
 cnadd='''## 冻结敏感性：哪些认识随截取改变

| 集合 | 数学/生物数 | 原频率最多组M/B | 前64均值超细匹配95%参照M/B | 逐PC重合 |
|---|---:|---|---|---:|
'''+ '\n'.join(outlines)+'''

主门槛0.75与0.70的两组前偏均未超过细匹配参照，0.80以及Top64/128则超过，Top16没有超过。因此“特殊谱前偏”依赖筛选强度，不能统一推广给全部领域区分成员，也不是确认性多阈值检验。主集合0.70/0.75/0.80的低频比例都低于池；生物Top16/128的低频比例18.75%略高于池16.74%，样本小且只是描述，不能称所有排名截断均低频耗减。主要谱位置大量重合，但数值随成员数而变。

'''
 enadd='''## Frozen sensitivity: conclusions that depend on truncation

| Set | Math/bio n | Largest original frequency class M/B | Head mean above fine95% reference M/B | PC overlap |
|---|---:|---|---|---:|
'''+ '\n'.join(outlines)+'''

Main.75 and.70 head means are inside fine references; .80 and Top64/128 exceed them, while Top16 does not. Thus special front orientation depends on screening strength, not a uniform whole-main property or confirmatory multi-threshold result. Low shares are below pool at.70/.75/.80; biology Top16/128 has18.75% versus pool16.74%, a small descriptive comparison, so depletion is not universal across rank cutoffs. Large spectral overlap persists, but its magnitude depends on group size.

'''
 for name,needle,add in [('summary_cn.md','## 五项问题的直接结论',cnadd),('summary.md','## Five direct answers and completion',enadd)]:
  p=OWN/name;write(p,p.read_text().replace(needle,add+needle))

# Chinese eight-section companion preserves exact decision, model and evidence limits.
write(ANCHOR.with_name(ANCHOR.stem+'_cn.md'),f'''# A15_27_04：领域偏向成员的频率、共同谱几何与输入响应

## 1. Problem Definition

父问题是原生CrossCoder如何响应自然文本与受控前文。用户本轮明确续接：从全字典文档区分成员出发，描述其频率、共同谱位置和词面/上下文关联。旧小名单及目标词分解不回答全字典问题。这里沿用现有自然语言响应Focus，一轮R10缓存分析；比较会更新描述性认识，不自动授予语义或因果机制。科研接受与关闭Unknown。

## 2. Physical Priors

用户给出三条待检验直觉及竞争解释：少见成员承担区分，或高频成员靠强度差；两域分占不同谱位置，或位置相近但响应不同；跨措辞上下文，或词汇/格式及交互。均不是预设事实。字典是固定坐标系，不等于互斥语义词条。

## 3. Falsifiable Hypotheses

H1检验低频相对支持合格池富集；H2检验两域平均单位decoder平方投影相对频率/支持匹配背景的差别；H3检验固定目标的领域响应能否跨措辞和已暴露家族划分复现。未见效应可能削弱直觉，支持不足只能判无法回答，不能把未激活判identity。

## 4. Mathematical Model

每文档响应为\\(r_{{df}}=160^{{-1}}\\sum_{{t=32}}^{{191}}z_{{dtf}}\\)，包含零。原始区分度\\(A_f=P(r_{{mf}}>r_{{bf}})+\\tfrac12P(r_{{mf}}=r_{{bf}})\\)。至少一域有5篇发现文档激活，且\\(\\max(A_f,1-A_f)\\ge.75\\)的全部成员冻结主集合与方向；该指标只识别稳定响应排序。

真实block27 residual-post向量以单一共同均值计算发现集协方差，得到按方差降序的正交PC\\(p_j\\)。单位decoder\\(u_f=d_f/\\|d_f\\|\\)的逐PC量\\(q_{{fj}}=(u_f^Tp_j)^2\\)全谱和为1。组分布是成员等权平均\\(Q_{{gj}}\\)，谱重合\\(O=\\sum_j\\min(Q_{{mj}},Q_{{bj}})\\)；分段会隐藏差别，平方分布相同不推出方向相同。实际使用另算\\(v_{{dtg}}=\\sum_{{f\\in g}}z_{{dtf}}d_f^{{model}}\\)，先求和后投影平方，保留交叉项，不能当完整表征方差解释率。

## 5. Computational Realization

固定A22原生14层共享z、原门控，block27 decoder与真实h同hook及模型单位。R04每域30/10/20发现/开发/旧留出文档，每篇160位置；独立DCLM频率65,536位置。共同谱60发现文档共9,600位置、1024PC满秩；R07复用同谱，不是独立语料。R08保有48家族×2域×2措辞×2目标后缀的384目标z；R09保有TRAIN-RMS还原decoder。本轮无新前向或训练。

## 6. Minimal Falsification Tests

冻结主集合后依次完成五项：feature频率组成；单位谱及PC1拆分；两域谱重合与独立呈现的实际贡献；真实token高响应频率；固定目标上下文及目标+后缀对照。Top16/64/128和AUC0.70/0.80仅作冻结敏感性，不替换主集合。低频认识必须对比池；特殊几何必须对比匹配背景；固定词不激活仅算不足。纯换词B缺失时写NOT RUN方案，不扩展前向。

## 7. Current Evidence

R10缓存统计完成：全字典16,384→支持合格10,076→主集合433数学/527生物；原留出357/431区间下界超过0.5，所有成员保留。频率可判定者高频66.7%/54.3%，池44.1%，没有低频富集。前64单位份额均值10.03%/11.52%，主要来自PC2–64；逐PC谱重合0.9493、分段0.9686，未高于匹配参照。实际组能量随输入改变。固定目标至少一条件的上下文复现33/21；789成员所有划分始终全零。既有R07谱经raw-h审计与本轮共同谱完全一致。详见[Summary]({OWN}/summary_cn.md)。这些是已暴露数据上的描述/探索结果，科研接受Unknown。

## 8. Claim Boundary And Next Decision

可以描述本字典、本批文本的频率、几何、重构能量及输入关联；不能推出领域专有知识、相同功能、因果重要性、学习干扰或MoE收益。纯目标词替换和真正独立谱稳健性仍缺。按用户范围完成缓存统计、图表、原始数据与复现入口后停止，由研究者判断这三条认识如何更新；后续前向需另行确认。[Protocol]({OWN}/protocol_cn.md)限定执行。
''')
# Replace only the new Anchor evidence paragraph; no old Anchor/round rewrite.
an=ANCHOR.read_text();start=an.index('## 7. Current Evidence');end=an.index('## 8. Claim Boundary And Next Decision');an=an[:start]+f'''## 7. Current Evidence

R10 cache-supported analysis completed:16,384 dictionary coordinates→10,076 support-qualified→433 math/527 biology main members; exposed-heldout interval support357/431, with every selected ID retained. Classified high-reference-frequency proportions66.7%/54.3% exceed pool44.1%; low is not enriched. Mean first64 unit shares10.03%/11.52% arise mainly in PC2–64. PCwise overlap.9493 (band.9686) is not above matched reference. Summed group-vector energies change with input domain. Recurrent fixed-target context occurs for33/21 members at >=1 ending;789 members remain zero across all controlled splits. Raw-h numerical checks establish the archived R04/R07 pooled basis is exactly the requested common spectrum, not independent robustness evidence. [R10 Summary]({OWN}/summary.md) owns all values/limits. These are descriptive/exploratory measurements; researcher acceptance remains Unknown.

'''+an[end:];write(ANCHOR,an)

write(OWN/'protocol_cn.md',f'''# Protocol：R10领域成员整体分析

## 0. Approval Snapshot

状态APPROVED_FOR_CACHE_ONLY_ANALYSIS。用户当前完整替代指令已明确授权续接Anchor、Protocol、五项缓存统计、图表和报告，无需逐步再确认。R10-v1冻结于{json.loads((O/'config.json').read_text())['frozen_utc']}；[精确配置](provenance/config.json)。主Anchor[15_27_04]({ANCHOR.with_name(ANCHOR.stem+'_cn.md')})，现有自然语言响应Focus。A–G科学范围来自本次明确指令；下述重采样、匹配和支持标签是范围内AI操作实现，不等于新增科研判断。实验角色为代理指标审计与描述分析。无新模型前向授权，科研接受/关闭Unknown。

## 1. Terminology / Definitions

成员指同A22的16,384共享z坐标。文档响应为固定160位置z均值含零；原始AUC为30×30文档对的数学响应排序概率、平局半次。feature发生率分母DCLM65,536；token频率分母本批19,200。单位几何、实际贡献平方能量、完整表征方差严格分开。

## 2. Anchor Alignment

一个问题：全字典领域区分成员在频率/共同谱/真实输入关联上如何分布？三步：冻结支持与排名；比较频率和共同谱几何/实际使用；检验真实token与固定词上下文。完成所有缓存支持项并列明缺口后停止，不要求出现正结果。

## 3. Tested Hypothesis

低频相对富集、不同谱位置、跨措辞上下文分别检验，互不替代。

## 4. Rival Explanations

候选池本身组成、字典普遍前偏、平方分布隐藏符号、向量交叉项、词汇/格式/后缀共同改变。对应池背景、匹配、余弦/子空间、先向量和再平方、固定目标配对。

## 5. Data Construction And Provenance

R04每域60文档：30发现/10开发/20旧留出；使用原文档分组，位置[32,192)。每篇相同160位置使域/文档等权。检查组无跨划分重复；源文件hash可追溯。留出已经使用，标探索复核，不能称盲测。读取前当前严格资产检查通过。

## 6. Learning Task And Permitted Supervision

不拟合分类器、不训练字典或模型，无优化器。领域标签沿用原真实网页摘录内容审阅；来源、体裁与词汇仍混淆。PCA只是离线协方差统计。

## 7. Model / Architecture And Frozen Variants

固定A22 checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628；14个奇数block1–27联合编码，共享z，门控阈值0.051281172782182693。block27 residual-post为最终归一化前hook；decoder模型尺度=TRAIN_RMS27×原权重，不再按h单位化或白化。零decoder单列。

## 8. Training Objective And Optimization

不适用。模型前向、训练、参数更新、路由干预、距离扩展均为0。

## 9. Conditions, Seeds, And Checkpoints

种子2026103004；文档/家族重采样各1000次，匹配背景1000次。至少一域有5篇发现文档激活即合格，不能要求两域。区分方向按AUC偏离0.5；排序绝对偏离降序再ID升序；精确0.5不入方向排名。主集合取全部方向校正AUC≥0.75；冻结0.70/0.80与每域Top16/64/128敏感性，不补人不调门槛。

## 10. Primary Metric And Frozen Analysis Plan

图1原频率阈值0.002593994140625/0.0134429931640625，边界归低组；少于20次支持不计三组分母、仍保留表。log等宽敏感性0.0045172553628813825/0.06686505701697326。

共同谱用60发现文档9,600个真实h，一次共同均值，域/文档/位置等权。通过raw-h协方差、特征方程和正交性核对后复用完整1024PC；样本分母9599与人口权重只差统一标量、不改方向。旧R07为同一谱，真正独立参照缺失；旧R08目标谱不得替换。

图2单位decoder逐PC内积平方，全谱1；16段各64PC。另拆PC1/PC2–64/PC65+，维数参照1/1024、63/1024、960/1024。保留成员分布、均值、中位数。

匹配背景按原频率低/中/高/不足×总发现支持文档数除10向下取整，支持合格非零decoder池包括入选成员。每层无放回抽相同规模，两组互斥，1000次；报告主集合被抽中比例。此为条件字典参照，非独立零假设或重新选择的文档bootstrap。

图3逐PC和64PC段分别取两组平均平方分布较小值求和；PC2–64同时保留完整质量及段内归一化重合。附全部跨组绝对余弦和真实decoder子空间。实际贡献在40篇旧留出逐token先求组内z×尺度还原decoder向量和，再平方投影，文档等权；四种组×输入条件。总平方范数≤1e−12报NA，不称完整h解释率。

## 11. Secondary Metrics And Guards

留出每域20文档独立重采样1000次，保持发现方向，95%点式百分位区间下界>0.5才标复核支持；不换人，不做确认性多重发现。

图4token按本批120文档19,200有效位置计数，保留子词标点及特殊ID清单；类型计数高位经验1/3、2/3分位，同频不拆。类型/位置分母各报。成员高响应阈值为发现正z第90百分位，留出严格超过；操作支持要求发现至少20正事件，留出至少5高事件跨2文档，不足保留。先成员内比例再成员等权；散点feature参考率对高响应token语料内频率中位数。实例固定发现前三名/域，每文档最多一个高例，优先另一文档同ID低例，只给已读前文。

图5复用48家族24/12/12、2域2措辞2后缀。A为同目标、同配对位置的领域差。上下文复现标签：至少一个目标条件中两措辞在发现/留出同非零方向，目标内措辞均值的家族95%区间两划分均排零，每划分至少3活跃家族。另记与自然文本方向一致与否。词面+后缀标签：E1−E0对两域/措辞均值，发现留出同号且区间排零、支持充分；交互为两目标间领域差的差，同规则。标签点式探索、可重叠；汇总四类，始终零只能覆盖不足。B纯换目标词不存在，不能把同时换后缀当identity。

## 12. Known Good / Known Bad / Known Confusing Cases

相同文档数组AUC应0.5、全数学更高为1、反转为0；全谱份额1、合并谱段不降低重合；直接模型向量求和与PC系数求和再平方一致。各成员平方能量相加是有意保留的错误对照，不准代替实际贡献。全零fixed-token不判identity。

## 13. Scientific Procedure And Stage Contracts

先查资产/hook/分组/逐位置与汇总一致；再仅用发现冻结成员；再核对共同谱并算五项，保留NA；最后公式独立复算、契约审计、查看实际图片、写双语记录与manifest。某项缺失只阻断依赖，不阻断其余。B与独立谱稳健性缺口保留。

## 14. Algorithm, Output, And Provenance Contract

脚本scripts/；执行数据{O}。保存全部16,384筛选表、冻结名单、主表、原新映射、逐成员投影/激活、真实高/普通/同ID低例、重采样及背景索引、绘图数据。研究库仅精选小证据与manifest，raw数组不入库。不覆盖旧结果。

## 15. Success / Failure / Insufficient Evidence

低频需比池富集才支持稀有承担；无富集削弱。特殊几何需匹配比较；相似削弱谱分离，缺覆盖则不足。固定词复现削弱纯身份，但不能证明语义功能；后缀变化只算关联。不得以数值失败为由调科学门槛。

## 16. What This Cannot Claim

领域专有知识、谱重合等于功能、因果必要性、完整h方差解释率、学习干扰/MoE收益、盲测泛化或纯identity。新前向仍需用户另外确认。

## 17. Block Confirmation, Freeze, And Amendment Ledger

A问题边界/B模型/C数据/D筛选/E频率谱/F上下文缺口/G交付范围均由当前详细用户指令明确给定。科学范围已授权；重采样/匹配/事件支持与标签是明确标注的操作实现。机器配置在结果前冻结；新增诊断须标附加描述，不得改主集合。数据/数值/识别三审计入Detailed；执行偏差追加记录，不回改冻结协议。
''')

diags=AUD['descriptive_diagnostics'];code_manifest={str(p.relative_to(OWN)):sha(p) for p in (OWN/'scripts').glob('*.py')}
details=f'''# Detailed evidence ledger: R10

[Summary](summary.md) · [Frozen Protocol](protocol.md) · [Definitions](definitions.md). Eligibility: DONE_EXPLORATORY for exposed-data statistics, DONE_VALID for numerical identities; scientific acceptance Unknown. No model forward or parameter update occurred. This is one continuation experiment, not five model experiments.

## Evidence and execution

R04 supplies120 unique source-document groups,192-token original prefixes and160 selected positions/doc. Source labels are content-reviewed math/bio excerpts, not model-derived semantic ground truth. Discovery/development/heldout sizes per domain30/10/20 remain intact. Feature occurrence has a separate65,536-position,256-window reference whose canonical document groups are disjoint. The source manifest hashes actual cache files. R07 paired input targets have equal position within every math/bio pair, while the family target indices span30–38. E0/E1 core text is equal but suffixes differ. R08 target rows align by seq_id, not arbitrary row position.

All-dictionary screening uses document means INCLUDING zeros; the support gate is OR, not AND. Independent Mann–Whitney rank sums reproduce all16384 pair-probability values. Discovery membership/rank was written to freeze.json before heldout or geometry output. Output freeze hash={sha(O/'freeze.json')}. Config hash={sha(O/'config.json')}. A rerun must reproduce identical sets/hash or refuse. Old legacy both-domain eligibility and small-list results remain unchanged.

The common basis is the existing R04/R07 one, verified against raw discovery h: mean error0, eigen residual~1.8e−15, orthogonality~3.4e−15, rank1024. Decoder/true h are residual-post block27 before final norm, with no h unit normalization. Decoder model units use TRAIN_RMS27={float(__import__('numpy').load(BASE/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz')['rms27'])}. Native BF16 activation readings are reused; linear projection/reconstruction statistics use FP64 saved trained decoder weights. This is a mathematical reconstruction, not an extra native-BF16 model replay.

A01 fine-matched dictionary draws include the main set, preserve half-octave occurrence and5-document total/max-domain support stratum sizes exactly and are disjoint between groups per draw. This avoids a missing replacement stratum without silently changing rules: it estimates conditional dictionary composition, not an outside-main independent population. Source total-pool/stratum counts and all1000 ID arrays remain saved. Bootstrap weights resample documents for AUC and whole paired families for context; per-feature95% tags are pointwise exploratory. No selection-bootstrap uncertainty was claimed.

Contribution uses every heldout token, two groups on both input domains, with scale restored and group vectors summed before square. Direct vector/PC paths agree within5e−14. No vector energy falls below1e−12. The saved deliberately incorrect sum-of-member energies differs and cannot replace the primary values. Shared decoder bias/mean is excluded from group v, since it is not a selected-member term.

Token frequency types count every valid ID, ties stay together. Member thresholds are discovery-positive p90; strict heldout > preserves discreteness. Guarded event-composition summaries exclude62math/55bio only from that panel denominator. All960 remain in master with reasons. All-member high/ordinary/same-ID-low instances and corpus per-ID math/bio counts are stored in execution tables; no future context is used. Because counts are built from this same120-document panel, this is a within-panel association, not independent frequency validation.

## Three audits and conformance

| Audit | Evidence | Result and limit |
|---|---|---|
| Scientific identification | Anchor/Protocol; frequency pool vs matched geometry vs fixed-target controls | Distinguishes descriptive alternatives; pure identity and causal function remain unresolved |
| Data/statistics |120 unique groups,30/10/20 split,disjoint reference; paired family bootstrap; counts/ties retained | All requested cache-supported cells complete; exposed heldout not blind; pointwise tags do not control multiple-member false discoveries |
| Implementation/numerics |Independent ranks,sparse means,OR support,full-PC sums,exact strata,vector sums,token gates,position/ID checks | {AUD['passed']}checks pass,0failed;0trainable parameters/optimizer/forward calls |

| Protocol item | Actual | Status |
|---|---|---|
| Full universe, OR support, AUC.75, fixed rank views |16384→10076→433/527; Top16/64/128 and.70/.80 saved | Conformant |
| New common-all-token discovery spectrum | Archived basis already exactly satisfies requested h/weights; raw covariance audited rather than arbitrary refit | Conformant reuse; R07 independence wording corrected |
| Same main list through five analyses |960 IDs unchanged; missing panel support tagged | Conformant |
| Matched background |1000 exact-stratum same-size disjoint draws from inclusive eligible pool | Conformant with explicit inclusive-pool interpretation |
| Pure target-only B |No such cached contrast;48-new-forward minimum proposal only | BLOCKED by missing measurement/authorization; NOT RUN |
| Independent natural reference spectrum |R07 is same basis; R08 target spectrum is not eligible | BLOCKED for independent robustness only |
| New model/training/distance |0/0/0 | Conformant |

Internal repair ledger: one independently written norm audit initially misread `CC_all_native` as unscaled; source shows it already includes RMS. Comparing saved GPU-FP32 norms with recomputed FP64 norms then exposed relative1.32e−7 rounding. The corrected audit uses the standard1024-term FP32 accumulation bound, not a scientific-effect tolerance; no decoder, membership, metric or result changed. A coding indentation error was caught before execution of that revision. Coverage audit also caught3 members active only in development: the all-zero flag was corrected from discovery+heldout to ALL splits (789 total). The frozen set/context recurrence criterion did not change. Actual image inspection caught an unset symlog transition and crowded legend; set linthresh=.001, correct count labels and re-render. Tail-trimmed/front-dimensional-share and top5-token concentration are labeled additional descriptive diagnostics, never selection criteria.

## Files, replication and bounds

Execution root: {O}. Source hashes: provenance/source_manifest.json. Primary tables: tables/master_members.csv,frequency_counts.csv,member_spectrum.csv,group_pc_spectrum.csv,group_reconstruction_energy.csv,context_effects.csv,context_categories.csv. Full execution-only tables include all_dictionary_screen.csv,old_new_list_mapping.csv,token_member_summary.csv,high_response_token_counts.csv,context_family_pairs.csv. Raw sparse z,PC basis/full feature projections,paired arrays,bootstrap and matched IDs stay execution-side. Five main images and four appendices have explicit payload_manifest.json. No raw/checkpoint payload, no old result replacement and no publication.

Reproduce with the local spectral-hier Python: scripts/analyze.py --output /tmp/r10_reproduction_unique (copies the frozen config; requires accessible registered source caches), then scripts/refine_background.py --output /tmp/r10_reproduction_unique, scripts/render.py --output /tmp/r10_reproduction_unique and scripts/audit.py --output /tmp/r10_reproduction_unique. Each script accepts the same output root; no source edit is required. The reproducibility entry is also in README.md; no forward/training import is present.

Coverage totals: five cache-supported groups DONE_EXPLORATORY; numerical checks DONE_VALID; pure-B and independent-spectrum robustness BLOCKED only for those claims. Completion means the available analysis is delivered, not those missing measurements were run. One next researcher decision: assess these bounded conceptual updates and separately decide whether the48-forward target-only supplement is warranted. Stop without expanding.
'''
write(OWN/'detailed.md',details)
write(OWN/'detailed_cn.md',f'''# R10详细证据记录

[完整结果](summary_cn.md) · [冻结协议](protocol_cn.md) · [定义](definitions_cn.md)。本轮为一个固定模型的缓存描述实验；已暴露数据相关统计为DONE_EXPLORATORY，数值恒等核对为DONE_VALID。科研接受与关闭Unknown。

## 数据、单位与复用

R04的120个原文档组互不重复，每域30/10/20发现/开发/原留出，固定160位置，平均含零；独立DCLM的256窗口65,536位置与本批原文档组不重叠。全字典16,384坐标；OR门槛和原始文档配对概率由逐位置稀疏z独立复算；Mann–Whitney秩和复现全部AUC。成员在任何留出/几何统计之前写入freeze.json并冻结。

真实h与decoder都对应block27 residual-post、final norm之前；h不先L2归一化或白化。共同谱直接使用60发现文档9,600真实h，单一共同均值。旧R04/R07基正好满足本次权重；raw-h均值误差0、特征方程残差约1.8e−15、正交误差约3.4e−15、完整秩1024，因此复用而不另造PCA。R07并非独立稳健性参照；R08最后目标词谱也不能替代全部token谱。

R09 decoder用TRAIN_RMS27=374.3495121024576还原模型单位。原生BF16门控z保持不变；离线向量分解按保存权重做FP64计算，不冒称新增原生BF16前向复现。组向量不含共享bias/均值，因为它们不归某个入选成员。先向量和再投影平方，与直接模型坐标路径误差约5e−14；四种组×输入条件齐全。保存错误的“成员平方能量之和”作数值对照，不能替代主读数。

匹配背景从整个支持合格池含主集合抽样，按A01实际发生率半octave区间及总/最大域支持各5篇区间，每层精确同规模、无放回、两组不重叠，1000次。包含主集合约40.0%/40.5%，属于条件字典背景，不是独立零假设或选择波动区间。所有stratum和ID保存。AUC重采样单位为文档；上下文重采样单位为成套家族，所有条件一起带走；点式标签不作多成员确认性发现。

token计数用19,200位置并按ID保留标点子词；类型分位点1/2次，同频不拆。阈值仅用发现正z，严格>；支持不足62/55只离开该组成图分母，仍在960主表。完整逐成员高、普通激活及同ID低响应实例，以及每ID数学/生物次数保留执行侧，不用未来文本。384个目标条件按seq_id对应；每个数学/生物配对及E0/E1目标位置相同，跨家族位置30–38，目标ID各后缀固定。E0/E1仅核心前文相同，整后缀也改变，故B仍缺。

## 三类审计与修复记录

科学识别审计：频率池、几何匹配、方向检查、实际贡献和固定词控制分别对应竞争解释；不跨越功能/因果边界。数据统计审计：完整文档划分、独立参考分组、点式探索区间及不换人均保留。实现审计：{AUD['passed']}项通过，0失败；全谱投影和误差约1.1e−15；训练、优化器、参数更新、模型前向均0。审计文件provenance/numerical_audit.json保留每项证据。

修复记录：独立审计最初误读旧字段CC_all_native为未还原范数，源代码说明已乘RMS，修正比较对象。FP32保存范数对FP64重算相对误差1.32e−7，以1024项标准舍入误差界核验，未改变decoder或筛选。脚本缩进在运行前编译检查发现并修复。覆盖核对发现3名成员只在开发集激活，将“始终零”改为全划分检查，最终789名；上下文复现规则和主集合未改。实际图片检查修正symlog线性阈值未设置和图例拥挤，数据不变。去最高10%均值、维数参照超出比例和top5词集中性为附加描述诊断，未用于挑人。

## 覆盖与复现

| 请求 | 状态 | 边界 |
|---|---|---|
| 全字典筛选、频率及敏感性 | DONE_EXPLORATORY | 新主集合960，不拼旧32分母 |
| 共同真实谱、单位几何、PC1拆分 | DONE_EXPLORATORY | 验证旧基等价，无独立参考支持 |
| PC/段重合、匹配背景、余弦/子空间、四条件实际能量 | DONE_EXPLORATORY | 几何/使用不等于功能 |
| token计数、高阈值、逐成员真实例子 | DONE_EXPLORATORY | 本语料内频率、支持分母分开 |
| 固定词A及目标+后缀敏感性 | DONE_EXPLORATORY | 大量目标未覆盖，逐成员点式标签 |
| 纯目标词B | BLOCKED / NOT RUN | 最小48新前向方案另列，须确认 |
| 真正独立自然谱稳健性 | BLOCKED | R07同基，R08目标谱不替代 |

脚本见scripts/，执行根{O}。保存源hash、freeze、全部16,384筛选、960主表、旧新全映射、完整1024投影、全部家族配对、真实例子、重采样/匹配索引及绘图原表。研究库只放精选小证据；raw数组与完整大表留执行侧。README给命令。旧结果不覆盖；本地阅读同步不等于提交或推送。完成缓存支持范围后停止，下一决定归研究者。
''')

write(OWN/'README.md',f'''# R10 reproducibility and reading entry

[中文结果](summary_cn.md) · [English results](summary.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [Definitions](definitions.md)

Use `/root/anaconda3/envs/spectral-hier/bin/python`. All operations are CPU cache statistics; no model is imported or called.

```bash
/root/anaconda3/envs/spectral-hier/bin/python {OWN}/scripts/analyze.py --output /tmp/r10_reproduction_unique
/root/anaconda3/envs/spectral-hier/bin/python {OWN}/scripts/refine_background.py --output /tmp/r10_reproduction_unique
/root/anaconda3/envs/spectral-hier/bin/python {OWN}/scripts/render.py --output /tmp/r10_reproduction_unique
/root/anaconda3/envs/spectral-hier/bin/python {OWN}/scripts/audit.py --output /tmp/r10_reproduction_unique
```

The first command writes an independent directory using the frozen R10 config and existing source caches. Default output is the canonical execution root, where an existing freeze is verified and preserved. All four analysis/render/audit scripts accept the same --output root; their default is `{O}`. Raw tables/matched IDs/position arrays remain there. Input registry access must be refreshed before cache use on another host. See provenance/input_access.json for this session. No checkpoint/dataset download, model forward or training occurs. Supplement B is NOT RUN.
''')

# A factual continuation at the existing Focus, retaining historical rounds and Unknown judgment.
for lang in ['','_cn']:
 p=ROOT/f'Projects/from-attention-to-search/main/focus/focus_natural_language_feature_response{lang}.md';s=p.read_text()
 replacements={'question_state: `USER_ACTIVATED_R06_FIXED_TARGET_SEMANTICS`':'question_state: `USER_ACTIVATED_R10_DOMAIN_MEMBER_ATLAS`','design_state: `R06_FIXED_TARGET_SEMANTIC_PROTOCOL_FROZEN`':'design_state: `R10_USER_CACHE_SCOPE_FROZEN`','task_state: `R06_517_FORWARD_APPLICABLE_BRANCHES_ANALYSIS_DELIVERED`':'task_state: `R10_CACHE_SUPPORTED_ANALYSIS_DELIVERED`','result_state: `R06_NEAR52_QUALIFIED_FAR_CONDITIONAL_PRIOR_RESULTS_PRESERVED`':'result_state: `R10_DESCRIPTIVE_RESULTS_B_AND_INDEPENDENT_REFERENCE_MISSING`'}
 for old,new in replacements.items():s=s.replace(old,new)
 if '## R10 domain-member atlas' not in s:
  pos=s.index('## R06 actual endpoint');add=f'''## R10 domain-member atlas

The researcher explicitly continued the existing task with whole-dictionary OR-support screening, AUC>=.75, pooled natural-all-token PCA and within-panel token counts. Three steps: freeze discovery members; compare frequency and common-spectrum geometry/use; evaluate true tokens and paired context. Supporting contrasts update the bounded description; absent contrasts weaken specificity; missing support remains insufficient. Completion is all cache-supported five groups plus exact gaps, then stop. [Anchor]({ANCHOR}) and [R10 Summary]({OWN}/summary{lang}.md) own design and factual endpoint:433math/527bio,0new forwards; pure target-only B and independent-reference PCA missing. Researcher acceptance/closure Unknown. Historical rounds below are preserved.

'''
  if lang:add=f'''## R10 domain-member atlas

用户明确续接全字典至少一域支持、AUC≥0.75、两域自然全token共同谱与语料内token计数。三步：冻结发现主集合；比较频率/共同谱几何与使用；检查真实token与配对上下文。有差别则更新描述，无差别削弱特殊性，支持不足不判无效。完成全部缓存五项并列明缺口后停止。[Anchor]({ANCHOR.with_name(ANCHOR.stem+'_cn.md')})与[R10结果]({OWN}/summary_cn.md)记录433数学/527生物，新增前向0，纯目标词B与独立参考谱缺失。科研接受与关闭Unknown；以下旧轮结果保留。

'''
  s=s[:pos]+add+s[pos:]
 write(p,s)

daily=ROOT/'daily_research_reports/1031/README.md'
write(daily,f'''# October31 meeting

[Current speaking entry: R10 whole-dictionary domain-member atlas]({OWN}/summary.md) · [中文认识更新与五组图]({OWN}/summary_cn.md). Main433math/527biology; AUC>=.75, either-domain support, verified pooled natural-all-token spectrum, within-panel token counts. Cache-only, zero new forwards/training.

Historical smaller-list brief remains [here](meeting_report/meeting_brief_crosscoder_domain_members.md). It used the older both-domain support and16+16 selection; its denominators/results must not be substituted into R10.
''')

# Active method amendment is explicit, after the frozen v1 design; old outputs remain archived.
if (O/'fine_background_config.json').exists():
 fine=json.loads((O/'fine_background_config.json').read_text())
 shutil.copy2(O/'fine_background_config.json',OWN/'provenance/fine_background_config.json')
 shutil.copy2(A/'fine_background_audit.json',OWN/'provenance/fine_background_audit.json')
 for name in ['fine_matched_sensitivity.csv','fine_matched_strata.csv']:shutil.copy2(T/name,OWN/'tables'/name)
 write(OWN/'background_amendment.md',f'''# R10 A01: finer matched dictionary reference

This is an explicitly post-v1 method correction prompted by a design audit: three broad occurrence groups do not ensure close rates, especially within the high group. Keep v1 coarse background arrays, geometry/results snapshots and reading records under execution `reading_v1_coarse_reference/`; no old result is erased. Freeze finer matching before its draw/projection: seed2026103005,1000 repeats, positive DCLM hits half-octaves (floor2log2hits, ratio<=sqrt2; zero separate), total and max-domain positive-discovery-doc bins of5 (within-bin differences<=4), exact group counts, no replacement, two draws disjoint. Pool still includes selected members; their mean inclusion is40.0%/40.5%, so this is a conditional dictionary reference, not an independent null. Membership, AUC/support thresholds, PCA, projections, token/context data and scientific claims are unchanged. See [config](provenance/fine_background_config.json), [checks](provenance/fine_background_audit.json) and [all fixed-set sensitivity](tables/fine_matched_sensitivity.csv).

The main observed head means10.03%/11.52% now lie within finer reference9.11–10.21%/10.59–11.76%. The original coarse ranges8.09–9.33%/9.24–10.62% were insufficient to establish special orientation. PC overlap.9493 lies in fine reference.9466–.9576 rather than just below coarse.9508–.9610. Do not call this a preregistered confirmation. It weakens the specificity interpretation without changing measured geometry. Three thousand additional exact-count/disjointness checks pass; zero model forwards. Actual scientific acceptance remains Unknown.
''')
 write(OWN/'background_amendment_cn.md','''# R10 A01：更细的匹配字典参照

方法审计发现，原三档频率匹配过粗，尤其高频档不能保证实际发生率相近。明确记录为看过v1后的方法修正，不冒称事先确认。旧粗背景数组、geometry/results及阅读文本保留在执行侧reading_v1_coarse_reference/。细匹配先冻结再抽样：种子2026103005，1000次；正发生次数用半octave区间floor(2log2hits)，同层发生率比≤√2，零另列；总支持文档与最大域支持各5篇区间，组内相差≤4篇；每层精确同规模，无放回、两组不相交。池仍含主集合，平均入选比例40.0%/40.5%，所以是条件字典参照，不是独立零假设。主集合、AUC/支持门槛、PCA、单位投影、token/上下文统计均不改变。

主集合前64均值10.03%/11.52%落在细参照9.11–10.21%/10.59–11.76%内；旧粗参照8.09–9.33%/9.24–10.62%会让特殊性显得更强，不能据此建立特殊谱位置。逐PC重合0.9493位于细参照0.9466–0.9576内；旧粗参照0.9508–0.9610只作方法对照。此修正削弱特殊性解释，不改变观测。3,000项精确层计数/无重复/互斥核对通过，新前向0，科研接受Unknown。配置、核对与全部TopK/阈值敏感性见对应provenance及tables文件。
''')
 for name,link in [('protocol.md','background_amendment.md'),('protocol_cn.md','background_amendment_cn.md')]:
  p=OWN/name;s=p.read_text();marker='### Amendment A01: fine background reference'
  if marker not in s:s+='\n'+marker+f'\n\nActive background reference follows [{link}]({link}); frozen v1 coarse draws are retained as method sensitivity. Post-v1 audit correction within authorized cache-only statistics; main feature selection and scientific thresholds unchanged,0new forwards. Precise machine revision in provenance/fine_background_config.json.\n'
  p.write_text(s)

# Source payload declarations, actual metadata registration and local sync happen after visual review.
payload=[]
for folder in ['figures','appendix','tables']:
 for p in sorted((OWN/folder).iterdir()):payload.append(dict(path=str(p.relative_to(OWN)),bytes=p.stat().st_size,sha256=sha(p),origin=str(O/folder/p.name),reason='selected measured evidence; raw arrays excluded'))
write(OWN/'payload_manifest.json',json.dumps({'payload':payload,'excluded':['raw z/h/decoder arrays','checkpoints','full family-pair and all-dictionary tables'],'scientific_acceptance':'Unknown'},indent=2))
write(OWN/'provenance/code_manifest.json',json.dumps(code_manifest,indent=2))
print(json.dumps({'canonical_owner':str(OWN),'main':[433,527],'checks':AUD['passed'],'proposed_not_run_forwards':48,'proposed_valid_tokens':validtokens,'selected_payload_files':len(payload)},indent=2))
