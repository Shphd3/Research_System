"""Build requested bilingual meeting reading materials; selected evidence only."""
from pathlib import Path
import json,csv,shutil,hashlib
O=Path(__file__).resolve().parent
ROOT=Path('/data/250010109/Research_System')
DAY=ROOT/'daily_research_reports/1031'
MEET=DAY/'meeting_report';D=MEET/'crosscoder_domain_members'
for x in [MEET,D/'figures',D/'tables',D/'appendix',D/'scripts']:
    x.mkdir(parents=True,exist_ok=True)
def js(p):return json.loads(Path(p).read_text())
def rows(n):return list(csv.DictReader((O/'tables'/n).open(encoding='utf-8-sig')))
def mdtable(headers,data):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |' for r in data])
def link(label,path):return f'[{label}]({path})'
def image(name):return f'![{name}]({D}/figures/{name}.png)'
def esc(s):return s.replace('|','\\|').replace('\n',' ')
fr=js(O/'freeze.json');res=js(O/'analysis/results.json');audit=js(O/'analysis/audit.json');spec=res['spectrum'];g=res['geometry']
assert audit['passed']
for p in (O/'figures').glob('*.png'):shutil.copy2(p,D/'figures'/p.name)
for p in (O/'appendix').glob('*.png'):shutil.copy2(p,D/'appendix'/p.name)
for p in (O/'tables').glob('*.csv'):shutil.copy2(p,D/'tables'/p.name)
for name in ['analyze.py','render.py','audit.py','deliver.py']:
    shutil.copy2(O/name,D/'scripts'/name)
for p in [O/'freeze.json',O/'frequency_history.json',O/'source_manifest.json',O/'analysis/results.json',O/'analysis/spectrum.json',O/'analysis/token_summary.json',O/'analysis/list_definitions.json',O/'analysis/audit.json']:
    shutil.copy2(p,D/p.name)
for source,name in [('/tmp/meeting_five_inputs_20261030.json','input_access.json'),('/tmp/meeting_tokenizer_inputs_20261030.json','tokenizer_access.json')]:
    if Path(source).exists():shutil.copy2(source,D/name)
R04=ROOT/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027'
R09=R04.parent/'R09_domain_difference_decomposition_20261029'
mathids=', '.join('f'+str(f) for f in fr['groups']['math']);bioids=', '.join('f'+str(f) for f in fr['groups']['biology'])
main_cn=f'''# 10月31日组会：领域区分成员的五项分析

准备日期：2026-10-30，北京时间。对象是同一个 A22 CrossCoder 的数学偏向16名、生物偏向16名。它们是**领域区分成员，不默认是领域专有知识**。本轮只读 R04—R09 缓存并补离线统计；新增模型前向、模型／字典训练、新 PCA、距离扩展均为0。原记录没有覆盖。科学接受与问题关闭仍为 Unknown。

先讲五条结论，再按编号读五组主图。定义、全名单、逐成员图和全部统计在[附录]({D}/appendix_cn.md)。

1. **频率：中高频占多数，具体组名依赖分组。** 原冻结分组下，数学组低／中／高为0／8／8，生物组为3／10／3。合格池8113名本身高频占52.53%；数学组50%没有高于这个组成，生物组18.75%反而较少。换成 R09 log 等宽后变为0／14／2和4／10／2，不能把“高频”当稳定语义类别。
2. **decoder 方向平均偏向谱前部，但不都集中在前部。** PC1–64 的平方投影均值为数学20.55%、生物19.85%，中位数18.96%、14.89%；全字典均值8.85%。数学组超过其精确匹配随机组95%范围上界11.81%；生物组匹配背景因支持不足为NA。数学0/16、生物1/16成员在PC1–64具有超过一半的投影，平均前偏不是“每个成员都主要在头部”。
3. **两域的谱分布相似程度取决于分辨率。** 逐PC重合系数0.7784，64-PC谱段重合系数0.9800。后者掩盖了段内差异。是否高于频率／支持量匹配背景**尚未回答**。它们的实际decoder子空间平均平方主夹角余弦为0.0765，不能把0.7784或0.9800说成方向、语义或功能重合。
4. **真实输入响应跨很多token；与token频率的稳定联系尚未回答。** 每名成员在本面板命中306–2972个不同token ID。激活所在token的面板领域分布与所选方向一致，但这是同一批自然文档的描述。已见token条件下，两种参考发生率的整体Spearman相关为0.022；未见token占8.1%–56.4%，因此不能把这个条件统计当完整关系。
5. **部分成员具有固定token后的上下文响应，不能对全名单作身份归因。** 5/32名达到本轮明确的描述性A类规则；0名分到B类；27名为C类，其中19名在固定目标测试上始终不激活。全零表示覆盖不足。A类削弱纯token身份解释，仍未排除前文术语与主题。

## 统一对象与冻结名单

R04的120篇真实英文文档每域60篇，发现／开发／原留出为30／10／20。每篇192 tokens，先在第33–192位（从0计32–191，共160位，含0）取原生共享激活z的文档均值，再用两域30×30篇文档的排序概率评分。相等计半次。原生最后层贡献幅度只是为每个成员乘固定正数，因此逐成员的排序概率不变。所有文档权重相同，没有把token当独立文档。

沿用R04区分度分析的资格：两域发现集各至少5篇文档有正激活。8113名合格，其中17名评分恰为0.5，保留在背景池、不进入有方向的排名。按距0.5的绝对距离降序、ID升序打破并列，分别截取数学、生物各16名。这与既有自然文档各64名排序的前16一致，但本次16+16汇报截取仍标**探索性**。旧留出已多次暴露，仅作检查。方向固定后的原留出区分度中位数为0.9750／0.9406，最低0.9075／0.8175，没有用于换人。

- 数学偏向，按冻结排序：{mathids}。
- 生物偏向，按冻结排序：{bioids}。

[冻结回执]({D}/freeze.json) · [主表：版本、区分度、两域支持、发生率和五项状态]({D}/tables/master_members.csv) · [旧新名单映射]({D}/tables/list_mapping.csv)。五图全部保留同一32名，不激活、不复现均不替换。

## 1．这些成员属于哪些激活频率组？

**我们问什么：最具文档区分度的成员是否主要低频，是否超出合格池组成？**

{image('figure1_frequency')}

**读图。** 左列横轴为数学／生物组，每柱16名，纵轴是成员数，颜色为低／中／高／支持不足。右列给同一合格池8113名的组成，使用比例轴避免数量级遮蔽。上排沿用原冻结等数量三分组，下排仅作R09 log等宽敏感性对照。这是成员计数，不是R09全字典均值差贡献。

**证据与一句结论。** 原分组阈值为发生率0.259399%与1.344299%；20次参考命中以下单列支持不足。合格池低／中／高／支持不足=602／3241／4262／8。数学0／8／8、生物3／10／3，均无支持不足。中高频占多数，但数学高频比例与候选池接近，生物偏向组比池中更少高频、更多低频；这些只是组成比较，没有选择流程的不确定性或显著性宣告。

**修正的直觉。** “领域区分成员必然罕见”不符合这份名单；“它们大多高频”又依赖阈值。R09 log等宽阈值0.451726%／6.686506%，数学0／14／2、生物4／10／2；同一池为1345／6128／632／8。

**还缺什么。** 参考发生率是原生共享z>0次数／65536个独立参考位置，既不是强度，也不是谱位置。候选资格和评分会影响组成，尚未说明频率为何形成。[原始计数]({D}/tables/frequency_counts.csv) · [分组变更]({D}/frequency_history.json)。

## 2．decoder方向位于协方差谱的哪一部分？

**我们问什么：这32个最后层方向是否共同朝向自然文本高方差方向，均值是否由少数成员主导？**

{image('figure2_decoder_spectrum')}

**读图。** 两面板分别16名；横轴为PC1–64、65–128，直到961–1024，共16段。纵轴为单位decoder的平方投影比例，每条浅线是一名成员，实线是均值，黑虚线是中位数。灰点线为全字典16384名均值。数学组灰带是1000个同规模、频率／文档支持量精确匹配集合的2.5%–97.5%范围；生物组保留NA。

**证据与一句结论。** 数学／生物PC1–64均值20.55%／19.85%，中位数18.96%／14.89%。全字典均值8.85%、中位数7.14%。数学匹配背景的均值范围6.73%–11.81%，中位8.71%，低于观察值。生物的f9491位于无法替代的稀有匹配格子，故其“超过匹配背景”尚未回答。最大两名分别贡献各组头段总投影的26.80%／34.39%，并非均值完全由一两名决定；但数学0/16、生物1/16超过50%，仍不能称所有方向都主要位于头段。

**修正的直觉。** 平均前偏是分布形状，不表示每名成员都头部集中，更不等于领域知识集中。**还缺什么。** 单位化去掉decoder长度；这里不乘z、RMS或特征值。所有1024个比例合计1，零范数为0/32。没有测量实际贡献或功能。[逐成员谱表]({D}/tables/member_spectrum.csv) · [背景支持]({D}/tables/matched_pool_support.csv)。

## 3．重点：同一协方差谱上的分布重合多少？

**我们问什么：两域成员是否占据相似谱位置，而不是ID是否相同？**

{image('figure3_spectral_overlap')}

**读图。** 横轴为同一16谱段；纵轴是组内16个单位decoder的平方投影等权平均。两条曲线各总和1，阴影是每段两组较小的份额。图旁同时保留逐PC与合并谱段的重合系数。

**证据与一句结论。** 逐PC重合0.778438，分段重合0.980014。两域有相似的粗尺度谱位置；合并把22.16%的逐PC差异压成约2.00%的谱段差异。未经频率／支持量匹配的1000对全字典随机16+16集合，逐PC重合95%范围为0.7792–0.8078、分段0.9285–0.9797，只能说明很高的粗分段重合也可在普通字典集合出现。由于完整匹配背景NA，本轮不宣告两域重合高于匹配背景。

**修正的直觉。** “两组ID互斥，所以谱空间分开”错误；“曲线几乎重合，所以方向相同”同样错误。附录256对成员绝对余弦均值0.03044，最大f359–f12266为0.97850；两个16维decoder子空间的平均平方主夹角余弦为0.07647，只有第一主夹角余弦很高（0.97934），其余至多0.25187。存在一个近同向或反向的成员对，不能据此说两组整体相同。

**还缺什么。** 主匹配格子使用floor(log2(参考命中+0.5)) × floor(两域发现文档总支持/5)，排除全部32名。f9491参考39次、数学／生物文档支持5／27，所在格要求1名、可用0名。未放宽、未复制、未换人。固定名单的几何量没有选择波动置信区间；随机集合范围也不是这种区间。谱平方丢失符号和组合，不能推出相同语义、计算需求、学习方向或功能重合。[逐PC数据]({D}/tables/group_PC_overlap.csv) · [256对绝对余弦]({D}/tables/pair_absolute_cosine.csv) · [实际子空间数值]({D}/spectrum.json)。

## 4．响应哪些真实token？与token频率有什么联系？

**我们问什么：响应是否局限少数词，两种发生率是否稳定相关？**

{image('figure4_tokens')}

**读图。** 4a固定展示两组发现排名第一名f8963、f11710的高激活、普通激活、同token低／不激活例子；不按谱或测试结果挑换代表。表中保留token ID、字符串、0起算位置与已经读到的前文尾部。完整前文、来源和每名最多每文档2例在附录。4b每点为主名单一名，共32点；横轴为feature参考发生率，纵轴为激活位置上**参考中已见token**的参考频率中位数，误差线为其10%–90%分位范围；两轴取对数。不同成员间相同数值可重叠。

**证据与一句结论。** 120篇×160位=19200个真实输入位置；每名命中306–2972个不同ID，最常见一个ID占其激活位置0.78%–32.34%。f8963在token5322 ` problems`上的一处z=0.16433，另一篇生物文档同ID为0；f11710在token785 `The`上一处z=0.11758，数学文档同ID为0。自然文档没有做严格配对，因此这些只是上下文实例。数学16名激活所在token的面板数学占比中位数均>0.5，生物16名均<0.5；各组再取成员中位数为0.631／0.278。该描述仍受来源、词面和发现选择影响。

**频率关系。** feature发生率分子为该成员z>0位置数；token发生率分子为该token ID在同tokenizer参考中的计数；二者分母恰好同为65536，但计数对象不同。32名的已见token条件相关Spearman ρ=0.02165，按两域自然文档整篇重采样300次的区间[-0.01377,0.04735]。数学组ρ=-0.1001，区间[-0.1605,-0.0507]；生物组ρ=-0.0147，区间[-0.0590,0.0252]，没有一致的正向关联。这些区间只反映固定名单的文档构成波动，未重做成员选择，不能当选择不确定性或独立泛化。

**修正的直觉。** 高频feature不必只响应常见词，领域偏向也不等于只响应某个术语。**还缺什么。** 参考256窗来自254个规范文档组。成员各有8.1%–56.4%激活位置token在参考中未见。它们标缺失并单列，不设伪计数、不把未见当真实零概率。故无条件中位数和完整频率关系**尚未回答**；不能由本面板单域出现称全语料专有。本轮没有decoder到词表的输出词分析。[全部token计数]({D}/tables/active_token_counts.csv) · [独立参考计数]({D}/tables/reference_token_counts.csv) · [全部实例]({D}/tables/real_token_examples.csv)。

## 5．上下文相关，还是主要反映token identity？

**我们问什么：固定当前token后，仅改变领域前文与措辞，响应方向是否仍复现？**

{image('figure5_context')}

**读图。** 每组冻结前两名作为主面板示例；所有32名见附录，未用成功者替换失败者。横轴为固定token与W0／W1措辞，纵轴为原生z的数学减生物平均差。蓝点是24个发现家族，橙点是12个原留出家族；每家族保留两域配对，区间以整个家族为单位重采样2000次。不同成员的z刻度不可当共同重要性刻度。

**证据与一句结论。** 同一个384位置的R07文本／R08共享z缓存覆盖全部32名，开发12家族也保存在表中。按example W0/W1、explanation W0/W1，有激活的成员数分别为发现11／11／8／8，原留出12／9／7／8，分母都32。13/32名至少在一个条件有激活，19/32名始终全零，保留为“测试覆盖不足”。

本轮先定义描述性读图规则：某一固定目标词的两种措辞，在发现和原留出都沿自然文档选定方向，四个单元的点态95%家族区间都不跨0，每单元至少一域有3个活跃家族，才记A。它是本轮说明标签，不冒充R09原复现标准，不是多重校正显著性。A类为f8963、f14394、f3464、f10937、f652；其中f8963／f3464／f652两目标都满足，f14394／f10937仅example满足。B类要求有受控目标激活且自然响应前5个token合计≥50%、同时不满足A，本次0名；这是词面集中描述，也不证明身份专一。其余27名C，含19名全零和8名稳定性不足。

**修正的直觉。** 固定目标后仍有跨措辞响应的5名削弱纯身份解释；自然文档中很有区分度却在固定目标上全零的f11710不能反过来被判为identity成员。旧R09的36名复现名单仅与本名单交5名（f8963、f14394、f3464、f359、f652），其结论不能覆盖32名；本轮A类5名与这个交集也不是同一批。

**还缺什么。** example换explanation同时改变目标词与结尾，二者差异不能单独证明上下文作用。A类仍可能响应前文术语、主题或措辞；没有因果／功能证据。区间是探索性点态区间，旧留出已暴露。[所有条件与支持]({D}/tables/context_effects.csv) · [家族原值]({D}/tables/context_family_values.csv) · [逐成员A/B/C]({D}/tables/context_categories.csv)。

## 汇报时的两条追问

**为什么这次比较能区分主要解释？** 文档评分先固定领域排序；谱图把激活大小拿掉，只比较方向几何；同token测试再把当前token身份固定。三者回答不同问题，只有最后一项能直接削弱“当前token身份单独决定响应”的解释，且仍保留前文词面竞争解释。

**为什么还不能说领域知识共享、功能共享？** 谱平方投影不保留符号，平均后也丢失成员组合；实际方向／子空间检查与谱分布重合不等价。我们也没有干预、任务性能或学习梯度。本次五项分析完成后停止，不从这些统计自动启动训练、前向或距离实验。

## 交付与缺项

已有结果：R04文档与参考缓存、发现评分和各64名排序、R07自然文本PCA、R08全部共享z、R09还原decoder及旧名单。本轮补统计：冻结16+16汇报截取、两套频率计数、重算的单位decoder分布与重合、可支持的匹配背景、真实token实例／参考计数、32名固定目标效应和A/B/C描述。

**需要新增前向才能补的证据，未运行：** 若要进一步区分C类的词面与上下文解释，需要在本名单实际响应的真实token上做固定token与位置、配对改变前文的测试；现有19名全零和8名不稳定成员没有这项证据。这里仅登记缺项，不设计或执行新实验。匹配格子空缺、参考中未见token属于背景／计数限制，不能靠新增前向冒充解决。

主表、冻结名单、旧新映射、分组历史、全部原始统计表、脚本和哈希均在[材料目录]({D})；[复现与定义]({D}/appendix_cn.md)。独立重算通过{audit['checks']}项检查，包含AUC、几何、token分母、无未来前文、家族区间、精确匹配与输入未变。图像已目视自检；没有独立听众理解测试，数学只作源文件检查。
'''
(MEET/'meeting_brief_crosscoder_domain_members_cn.md').write_text(main_cn)

main_en=f'''# October 31 meeting: five analyses of domain-discriminating CrossCoder members

Prepared 2026-10-30, Asia/Shanghai. [Chinese speaking entry](meeting_brief_crosscoder_domain_members_cn.md). This is a derived meeting record; scientific acceptance/closure remain Unknown. No new model forwards, training, PCA fitting or distance expansion. Existing R04–R09 results are preserved.

## Five bounded conclusions

1. **Frequency:** original groups contain low/middle/high counts 0/8/8 for math and 3/10/3 for biology (16 each). The eligible pool has 602/3241/4262 plus8 low-support members, n=8113. Math's 50% high-frequency fraction is close to the pool's52.53%; biology's18.75% is lower. R09 log-width sensitivity changes these counts to0/14/2 and4/10/2. Group labels depend on binning.
2. **Decoder geometry:** mean PC1–64 squared unit projections are20.55%/19.85%, medians18.96%/14.89%; dictionary mean8.85%. Math exceeds its exact frequency/support-matched set range6.73%–11.81%. Biology matching is unavailable. No math and one biology member exceed50% head energy; an average head bias does not mean every member is head-concentrated, or that head energy is knowledge.
3. **Spectral overlap:** per-PC overlap0.778438; 64-PC-band overlap0.980014. Aggregation hides within-band differences. Above-matched-background overlap is unanswered because one required bin has no noncandidate. Unmatched dictionary16+16 pairs have per-PC95% range0.7792–0.8078 and band range0.9285–0.9797, a descriptive context only. Actual decoder subspaces have mean squared principal cosine0.07647, not0.7784/0.9800. Spectral overlap is not semantic or functional overlap.
4. **Real input tokens:** each member activates on306–2972 observed token IDs across19200 natural positions. Single most frequent ID contributes0.78%–32.34% of a member's active positions. Active-token panel domain composition follows selection direction, descriptively. Reference-seen-token conditional median frequency has pooled Spearman correlation0.02165 with member occurrence; fixed-list document-bootstrap interval[-0.01377,0.04735]. Reference-unseen IDs occupy8.1%–56.4% of active positions and remain missing. The unconditional frequency relationship is unanswered.
5. **Context versus identity:**5/32 have descriptive same-target context replication across wordings, discovery and exposed old heldout;0 are B;27 are C. Nineteen never activate on either fixed target and have insufficient coverage, not identity-only evidence. A members are f8963,f14394,f3464,f10937,f652; three pass both targets, two onlyexample. Lexical/topic rivals remain.

## Unified objects and selection

A22: native14-layer joint shared z,16384 coordinates, fixed999997440-token checkpoint SHA25609b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628. Only its zero-based block27 residual-post decoder is analyzed, before final norm. No last-layer-only encoder is used.

R04 has120 real English documents:60/domain, discovery/development/old-heldout30/10/20. Each has192 tokens; native z is averaged over positions32–191 including zeros. A member qualifies with positive activation in at least5 discovery documents in each domain. The math-oriented AUC is the probability a random math document has a higher mean than a random biology document, counting tieshalf. A fixed positive decoder norm leaves this within-member AUC unchanged. Rank by absolute distance from0.5, IDascending for ties, take first16/sign. Pool8113 includes17 exact-chance ties excluded from directional selection. The 16+16 prefixes agree with the existing natural-document64/sign ranking; this reporting cut is exploratory. Old heldout is repeatedly exposed and never used to replace members. Direction-fixed heldout AUC medians0.9750/0.9406; minima0.9075/0.8175.

Math: {mathids}.

Biology: {bioids}.

Reference basis is R07's independently acquired natural-document PCA,1024 orthonormal columns, fit on9600 positions from the60 R04 discovery documents. It is not R08's refitted mixed basis. Every decoder is unit-normalized; squared projections sum1. No activation, norm, RMS or eigenvalue weighting. Zero norms0/32.

## 1. Activation-frequency groups

{image('figure1_frequency')}

Question: are discriminating members unusually rare or frequent? Left axes show16 members/group as stacked counts; right axes show8113-eligible-pool proportions. Main equal-count cuts are0.259399%/1.344299%, minimum20 reference hits; sensitivity log-width cuts0.451726%/6.686506%. Frequency is native z>0 count/65536 DCLM positions. The result revises an assumption that domain discrimination requires rarity; the labels and pool composition limit stronger interpretation. No contribution totals substitute for member counts, and no selection-uncertainty inference is claimed.

## 2. Unit decoder direction

{image('figure2_decoder_spectrum')}

Question: which covariance ranks contain decoder orientation, and is an average driven by a few members? Sixteen bands have64 PCs each; pale lines are individual members, solid means, dashed medians, dotted full-dictionary mean. The math gray band is a1000-set exact-matching composition range. Its observed head mean exceeds the matched range; biology matching remains NA. Top2 members account for26.80%/34.39% of group head mass. This revises 'all selected members sit in head PCs'; the quantity is orientation, not actual activation/contribution or knowledge amount.

## 3. Shared spectral distribution

{image('figure3_spectral_overlap')}

Question: how much do group-mean squared projections cover the same PC ranks? Both curves average16 unit decoders equally. Shading sums the smaller group fraction in each64-PC band; separate per-PC overlap retains within-band differences. The two overlap resolutions differ substantially. Pairwise absolute cosine mean0.03044, maximum0.97850 (f359–f12266); both actual decoder spans rank16. Principal cosines start0.97934 then at most0.25187, with average square0.07647. Similar spectral position does not imply equal direction or subspace. Matching bins are floor(log2(reference hits+0.5)) × floor(total discovery active documents/5), excluding all32. f9491 has39 reference hits and5/27 discovery supporting documents: its required bin has0 alternatives. No fallback or forced retention was used. Full matched pair comparison and observed selection-uncertainty intervals remain unavailable; random-set ranges are not such intervals.

## 4. Real tokens and token occurrence

{image('figure4_tokens')}

Question: does a member respond across input IDs, and does feature frequency track token frequency? Panel4a uses the first discovery rank/domain, with high, median-positive and same-ID low/inactive examples, at most2 examples/document/member. Exact input IDs, strings, positions and read prefixes are saved; future text is excluded. Panel4b has one point/member, log axes, conditional median of reference-seen input-token rates and10th–90th percentiles. For f8963, input5322 ` problems` has observed z0.16433 versus0 in another document; for f11710,785 `The` has0.11758 versus0. Natural examples are not controlled edits. All16 math member active-token panel math-fraction medians exceed0.5; all16 biology ones fall below0.5 (group medians0.631/0.278), still a same-panel selected association.

Feature frequency counts positive feature positions; token frequency counts token IDs in the same independent65536-position reference (256windows/254canonical document groups). Unseen IDs are excluded from rate quantiles, reported separately, never declared zero true probability. Within-group correlations are-0.1001 (math, document interval[-0.1605,-0.0507]) and-0.0147 (biology,[-0.0590,0.0252]). The300-draw within-domain document bootstrap keeps selection/reference fixed and is not selection uncertainty or independent generalization. No consistent positive relation or complete unconditional relation is established. No decoder-to-vocabulary output analysis was added.

## 5. Fixed-token context responses

{image('figure5_context')}

Question: does the selected direction persist while current token identity stays fixed? Main examples are the first2 ranks/domain, retaining the all-zero case. The appendix plots all32. X=example/explanation × W0/W1; y=raw mean z(math)-z(biology). Discovery24 versus old-heldout12 families are separate; whole-family paired2000-draw bootstrap gives pointwise95% intervals. Development12-family values are also saved. Active-member counts in the four cells are11/11/8/8 in discovery and12/9/7/8 in old-heldout, denominator32. Thirteen members are ever active;19 never are.

Descriptive A requires, for at least one fixed target, both wordings in discovery and old heldout to retain the natural-discovery direction with all four pointwise95% intervals excluding0 and at least3 active families in one domain/cell. This is not the original R09 rule or multiplicity-corrected inference. B requires nonzero controlled-target support, no A, and at least50% natural activation concentrated on5 IDs; it still cannot prove identity-only encoding. Otherwise C. A=5,B=0,C=27 (19zero+8unstable). Old R09's36-member rule intersects this list only at f8963,f14394,f3464,f359,f652; that intersection differs from the new A set. Comparingexample with explanation changes both token and ending and cannot itself establish context response. A weakens pure current-token identity while retaining earlier-term/topic rivals.

## Evidence, missing items and stopping

Existing: R04 natural/reference cache and discovery ranking, R07 fixed PCA, R08 full joint z, R09 decoder and old candidate lists. New offline: the16+16 reporting cut, member-count frequency summaries, geometry/overlap/background recomputation, actual-token examples/counts, and per-member fixed-target effects/categories. All {audit['checks']} independent checks passed. Images received visual self-review; no independent listener test or rendered-math validation was claimed.

Further resolving the19zero/8unstable C members would require fixed-token/position paired-prefix tests on actual responding natural IDs, hence new forwards; these are recorded as missing and NOT RUN. Missing match alternatives and reference-unseen token rates are distinct background/counting gaps, not permissions for forwards. No new execution is proposed or started. See [definitions, full list and reproduction]({D}/appendix.md), [master]({D}/tables/master_members.csv), [frozen list]({D}/tables/frozen_list.csv), [mapping]({D}/tables/list_mapping.csv), [frequency history]({D}/frequency_history.json). Computation stops after this delivery.
'''
(MEET/'meeting_brief_crosscoder_domain_members.md').write_text(main_en)

# Supporting definitions, computational contracts and explicit list identities.
definition_rows=[
['领域区分度 / domain discriminability','同一成员的文档平均z在数学高于生物的概率；相等计半次','发现每域30文档；留出每域20文档；token非独立文档'],
['参考发生率 / feature occurrence','原生共享z>0计数／65536','单独DCLM参考；不是激活强度'],
['token参考频率 / input-token frequency','同tokenizer的token ID计数／65536','未见标缺失；已见条件分位数单列'],
['单位decoder / unit decoder','最后block27原空间decoder除以L2范数','去掉长度；未乘z、RMS或特征值'],
['参考PCA / reference PCA','R07沿用R04自然发现文本9600真实residual-post位置的1024PC','固定原基，不用R08混合PCA'],
['逐PC谱分布 / per-PC spectrum','每个单位decoder与PC内积平方；组内等权平均','1024项和1；平方不保留符号'],
['谱分布重合 / spectral overlap','各PC两组均值的较小值之和','范围0–1；分段合并可提高重合'],
['实际子空间 / decoder subspace','两组decoder分别取正交基，再计算主夹角余弦','本次rank16/16；平均平方余弦0.07647'],
['上下文差 / context difference','同家族／目标／措辞的数学z减生物z','家族整组重采样；点态区间非多重校正'],
['A/B/C','A有固定token跨措辞响应；B主要词面集中；C证据不足','本轮描述规则；旧R09复现资格独立保留']]
mapping=js(O/'analysis/list_definitions.json');listrows=[]
for name,ls in mapping['lists'].items():listrows.append([name,len(ls),mapping['main_intersections'][name]])
def_text=r'''
令 d_f 为成员f在block27的decoder，u_f=d_f/||d_f||，p_k为固定PC列。对组G，逐PC分布为：

\[
q_G(k)=\frac{1}{|G|}\sum_{f\in G}(u_f^\top p_k)^2,\qquad \sum_{k=1}^{1024}q_G(k)=1.
\]

数学、生物组各16名，单位方向等权；这里没有激活、范数或特征值权重。重合系数的精确定义是：

\[
O_{\mathrm{PC}}=\sum_{k=1}^{1024}\min(q_M(k),q_B(k))
=1-\frac12\sum_{k=1}^{1024}|q_M(k)-q_B(k)|.
\]

分段先把各64项相加再取较小值，得到O_band，必有O_band≥O_PC。它们衡量组平均平方谱分布，均不是实际方向夹角。若两个单位方向分别为(p1+p2)/sqrt(2)与(p1-p2)/sqrt(2)，逐PC平方分布完全相同，方向却正交。因此另算256对绝对余弦和真实decoder跨度的正交基Q_M、Q_B；后者平均平方主夹角余弦为||Q_M^T Q_B||_F^2/16。本次无秩不足，不把这个量改名为功能重合。
'''
table_defs=mdtable(['对象 / Object','计算 / Calculation','分母或边界 / Denominator or limit'],definition_rows)
master=rows('master_members.csv');token=rows('token_member_summary.csv');cat=rows('context_categories.csv')
compact=mdtable(['组/排名','成员','发现AUC(Math)','原留出AUC(Math)','发现支持M/B','DCLM%','原组/log组','上下文'],[[f"{r['group']} {r['rank']}",'f'+r['feature'],f"{float(r['discovery_AUC_math']):.4f}",f"{float(r['heldout_AUC_math']):.4f}",r['discovery_math_active_documents']+'/'+r['discovery_biology_active_documents'],f"{float(r['feature_reference_rate'])*100:.4f}",r['original_frequency_group']+'/'+r['R09_log_frequency_group'],r['test5_context']] for r in master])
newforward=mdtable(['C类原因','成员','状态'],[['固定目标始终全零',', '.join('f'+str(f) for f in res['context_allzero_members']),'NOT RUN：缺自然响应token上的配对前文测试'],['已有激活但稳定性不足',', '.join('f'+r['feature'] for r in cat if r['category']=='C' and int(r['fixed_target_active_positions'])>0),'NOT RUN：不能从不稳定直接判identity']])
source_text=f'''R04正式来源：[Summary]({R04}/summary.md)、[对象设置]({R04}/objects_and_settings_cn.md)。自然文本评分来源：[R04区分度配置]({O.parent}/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/config.json)。R09旧结果：[Summary]({R09}/summary.md)、[补充A–D]({R09}/supplement_ABCD.md)。完整输入哈希与实际缓存路径见[source_manifest.json]({D}/source_manifest.json)。

所有新增计算由[analyze.py]({O}/analyze.py)执行；先以--freeze输出freeze.json，再读冻结名单完成五项分析。[render.py]({O}/render.py)只作图；[audit.py]({O}/audit.py)从原始输入独立重算。指定解释器为/root/anaconda3/envs/spectral-hier/bin/python，使用本地tokenizers读取原tokenizer.json，不构建模型或加载模型权重。

```bash
/root/anaconda3/envs/spectral-hier/bin/python {O}/analyze.py --freeze
/root/anaconda3/envs/spectral-hier/bin/python {O}/analyze.py
/root/anaconda3/envs/spectral-hier/bin/python {O}/audit.py
/root/anaconda3/envs/spectral-hier/bin/python {O}/render.py
```

上述命令只会重算本轮新建执行目录的派生结果；不会自动运行，这里保留复现入口。要在全新目录复现，复制四个脚本和freeze.json并设置原缓存父目录（analyze.py的B、render/audit的B）后先审阅路径；脚本默认用自身目录的父目录作为原缓存根。本轮已完成并停止。统计种子：匹配/普通字典背景2026103001，固定名单文档重采样2026103002（300次），固定目标家族重采样2026103003（每分割2000次）。R04旧留出AUC区间直接沿用旧2000次文档重采样结果，已重新核对AUC本身。

独立检查{audit['checks']}项全部通过；它验证数值和来源，不是科学批准或独立读者理解。导航检查报告已有37项登记／组织问题（多数为未跟踪入口，另有15_25_03缺map、15_27/15_28 map来源陈旧），本次没有改旧Graph、Focus、Anchor或科研状态。输入资产本轮10项及tokenizer严格访问检查通过；这不等于重新验证checkpoint训练资格。没有commit、push或外部发布。
'''
appendix_cn=f'''# 五项分析：定义、完整成员、统计与复现

[唯一中文汇报入口]({MEET}/meeting_brief_crosscoder_domain_members_cn.md) · [English companion](appendix.md)

## 定义表

{table_defs}

## 冻结主名单

下表AUC始终是数学高于生物的原方向概率，生物偏向自然应接近0；主表另给方向固定AUC和原留出点态区间。发现支持是有激活文档数，分母每域30篇；开发10、原留出20也在CSV中。统一字典ID见freeze.json，SHA25609b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628。原生共享z来自14层；decoder只取block27。

{compact}

## 重合与真实子空间的计算

{def_text}

## 名单身份与历史分母

{mdtable(['名单','原名单人数','与本次32名交集'],listrows)}

R04_new_top16是两域混合全局前16，方向人数9／7；R04_expanded_*64是自然文档区分度排序。R04_old_*16是更早的原生使用率偏向名单，评分门槛不同；R04_same_token_*是后来同token资格筛选，仍不是本次名单。R09_*64来自受控目标上的符号与方向贡献规则；R09_contribution32按结尾分别选；R09_union141保留其贡献候选并集；R09_replicated36沿用其原复现规则。本轮不把任何一个分母换成本次32，不继承不存在交集的验证结论。全部ID和各自排名在[list_mapping.csv](tables/list_mapping.csv)。

## 频率分组变更

R05冻结等数量三分组并保留相同发生率的并列，20次以下支持不足。R09为自己的频率贡献分析引入log等宽；它没有废除旧分组或改变原z。当前主图恢复旧分组，R09新分组只作对照。边界、完整字典与合格池的分母均在[分组历史](frequency_history.json)、[计数表](tables/frequency_counts.csv)。

## 附图：全名单与方向检查

![32名×16谱段]({D}/appendix/member_band_heatmap.png)

每行同一冻结成员，16格合计1；两域内部顺序与主表一致。

![逐PC曲线与256对方向]({D}/appendix/per_PC_and_pair_cosine.png)

上图不合并PC；下图每格是一对数学／生物成员的绝对余弦，不同于谱平方重合。完整主夹角与实际秩保存在[spectrum.json](spectrum.json)。

![全部数学16名上下文]({D}/appendix/all_context_math.png)

![全部生物16名上下文]({D}/appendix/all_context_biology.png)

每格分母是一个成员，横轴四目标／措辞，蓝24发现家族、橙12原留出家族，纵轴未标准化数学减生物z，区间为家族bootstrap点态95%。19个全零格在标题保留active0/384，应读作覆盖不足。

## 真实token：完整实例与词频支持

[完整可读实例](real_token_examples_cn.md)保存所有32名的高、普通和同ID低／不激活实例；[原表](tables/real_token_examples.csv)保留完整已读前文与当前token，当前后方文本未输出。每成员每文档最多2例；高激活两例跨文档，普通为正激活中位附近。token字符串由同一tokenizer解码真实输入ID，不来自decoder词表投影。

[成员token统计](tables/token_member_summary.csv)含活跃位置数、活跃文档数、不同ID数、前1/5ID份额、参考未见份额、已见条件频率分位数和token在两域面板的出现比例。[全部成员×输入ID](tables/active_token_counts.csv)与[参考计数](tables/reference_token_counts.csv)给可核查的原计数；两域自然面板分母各9600位置。某ID只在一域出现只说明本面板。

## 未回答与需要前向的缺项

{newforward}

这些缺项只登记、不自动运行。A类也没有前文术语／主题之外的语义排除证据，未做因果或功能测试。完整双组频率／支持量匹配背景因f9491格无替代而NA；数学单组匹配可估且已完成。不能用低支持成员替换、保留原候选占位或放宽匹配后宣称原比较完成。token未见导致无条件频率关系未回答，不是identity的负结果。

## 来源、复现与检查

{source_text}

## 表格入口

{mdtable(['表','作用'],[[link(p.name,'tables/'+p.name),'本轮离线统计；原缓存只读'] for p in sorted((D/'tables').glob('*.csv'))])}
'''
(D/'appendix_cn.md').write_text(appendix_cn)
appendix_en=f'''# Definitions, frozen members, full evidence and reproduction

[English brief]({MEET}/meeting_brief_crosscoder_domain_members.md) · [Chinese full appendix](appendix_cn.md)

## Definition table

{table_defs}

## Frozen member table

Raw AUC is always math-higher-than-biology, so biology-biased members approach0. Discovery support denominators are30documents/domain. The master CSV also includes development10 and old-heldout20 support, direction-fixed heldout AUC/interval, checkpoint/interface, both frequency labels and all five test statuses. One A22 checkpoint and one block27 decoder are used throughout; fourteen-layer shared activation is not independently encoded block27 activation.

{compact}

## Equations and scope

For unit decoder u_f and orthonormal PC p_k, each member distribution is the squared dot product. Average equally within each16-member group, then sum the smaller group fraction at each of1024 PCs. This equals one minus half the L1 distance between group distributions. Aggregating64 PCs before taking minima can only increase overlap. Sign and member combinations are lost: (p1+p2)/sqrt(2) and(p1-p2)/sqrt(2) are orthogonal but have identical squared PC distributions. Pairwise absolute cosine and actual decoder-span principal angles are therefore separately reported. Both spans rank16; squared Frobenius overlap of their orthonormal bases divided by16 is0.07647.

## Distinct old lists

{mdtable(['List','Original denominator','Intersection with frozen32'],listrows)}

R04_new_top16 is the earlier global16 (math9,biology7), not16/domain. Expanded natural64 lists use document AUC. Earlier original-R04 usage lists and later same-token lists have distinct gates; controlled R09 per-domain64 and per-ending contribution32 use distinct selection objects. R09 union141 and replicated36 retain original denominators. [All ID/rank mappings](tables/list_mapping.csv) preserve them separately. The new16+16 reporting cut is exploratory, even though it reuses the ordered prefixes of old64 lists.

## Frequency history and unavailable matching

Original equal-count cuts are0.002593994140625 and0.0134429931640625, minimum20 reference hits. R09 introduced log-width cuts0.0045172553628813825 and0.06686505701697326 for its own analysis. Both are preserved, original primary. The exact matched-background joint bins use floor(log2(hits+0.5)) and floor(total positive discovery-document support/5), the same eligibility pool, excluding every frozen member and no replacement within a set. f9491's bin(hits39,support5+27) has no alternative; complete biology and paired backgrounds remain NA. Math's supported1000 draws were retained. The unmatched dictionary background is labeled explicitly and does not answer above-matched-background enrichment. No observed selection bootstrap is claimed.

## All-member figures

![All32 unit decoder band projections]({D}/appendix/member_band_heatmap.png)

![Per-PC spectrum and256 pair cosines]({D}/appendix/per_PC_and_pair_cosine.png)

![All16 math context responses]({D}/appendix/all_context_math.png)

![All16 biology context responses]({D}/appendix/all_context_biology.png)

Context x-axis contains example/explanation × W0/W1; y is unstandardized math-minus-biology z. Discovery24 and old-heldout12 paired families are separately bootstrapped2000times; intervals are pointwise descriptive95%. Active0/384 indicates insufficient test coverage, not token identity.

## Token evidence and missing estimates

[Complete actual-input examples](real_token_examples_cn.md), [CSV](tables/real_token_examples.csv), [member summaries](tables/token_member_summary.csv), [active-ID counts](tables/active_token_counts.csv), [reference counts](tables/reference_token_counts.csv). High and median-positive examples plus same-ID low/inactive controls obey maximum2examples/document/member and contain read prefixes only. Reference-unseen IDs are missing estimates, never declared zero true probability. Medians/10th–90th percentiles in the plot condition on seen IDs; the complete unconditional frequency association is unanswered. Domain token counts have9600positions/domain and describe this selected panel only. No vocabulary decoding of decoder weights was added.

Further separating C from identity-only responses would require new paired-prefix acquisition at actual responding natural IDs for the19all-zero and8unstable members. Those tests are missing/NOT RUN. They are not authorized by a delivery or available cache. No further experiments follow this report.

## Reproduction and provenance

Producer directory: {O}. Run the local spectral-hier Python with analyze.py --freeze, analyze.py, audit.py, then render.py. Scripts infer their original cache root from the parent directory, so audit paths before relocating. Copies are in scripts/. [Input hashes](source_manifest.json), [freeze](freeze.json), [frequency history](frequency_history.json), [audit](audit.json) and all CSVs are included. Seeds2026103001/2/3 cover background, fixed-list document variability300draws, and context-family2000draws. Old AUC intervals reuse their original2000document-draw receipt; scalar AUCs were independently recomputed.

All {audit['checks']} independent checks passed. Visual checks were self-review; math checks concern source only. Existing navigation issues were reported without changing graph/Focus/Anchor states. Ten selected input assets and tokenizer passed current strict access. No commit, push or external publication occurred. Existing work is clearly separated from new offline statistics in the speaking brief.
'''
(D/'appendix.md').write_text(appendix_en)

ex=rows('real_token_examples.csv');chunks=['# 全32名真实输入token实例\n\n只显示已读前文。当前位置从0起算；不显示未来文本。每成员每文档最多2例。未见参考ID标缺失。\n']
for f in fr['ordered_union']:
    chunks.append(f'\n## f{f}\n')
    for r in [r for r in ex if int(r['feature'])==f]:
        chunks.append(f"\n### {r['example_type']}：token {r['token_id']} {r['token_string']!r}\n\n文档{r['document']}（{r['domain']}，{r['split']}）；0起算位置{r['position_zero_based']}，原生z={float(r['z']):.7g}；参考计数{r['reference_token_count']}/65536。来源：[{r['source_url']}]({r['source_url']})。\n\n已读前文：\n\n```text\n{r['read_prefix']}\n```\n\n当前token：{r['token_string']!r}。\n")
(D/'real_token_examples_cn.md').write_text(''.join(chunks))
(D/'real_token_examples.md').write_text('# Complete observed-input examples\n\n[Full bilingual-field examples](real_token_examples_cn.md) and [CSV](tables/real_token_examples.csv) preserve IDs, decoded strings, zero-based positions, native z, sources and read prefixes for all32 frozen members. No future text is shown; maximum2examples/document/member.\n')
(DAY/'README_cn.md').write_text('# 10月31日组会\n\n[唯一发言入口：领域区分成员的五项分析](meeting_report/meeting_brief_crosscoder_domain_members_cn.md)。同一A22、同一block27 decoder、同一R07自然文本PCA、冻结数学16与生物16；只读缓存与离线补统计。科学判断仍由项目记录持有。\n')
(DAY/'README.md').write_text('# October31 meeting\n\n[Single speaking entry: five analyses of domain-discriminating members](meeting_report/meeting_brief_crosscoder_domain_members.md). Fixed A22,block27 decoder,R07 natural-text PCA and16members/domain. Cache-only; no new forwards or training.\n')
# Explicit selected evidence exception: no raw representations or fonts copied.
payload=[]
for p in sorted(D.rglob('*')):
    if p.is_file() and p.name!='payload_manifest.json':payload.append(dict(path=str(p.relative_to(D)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),origin=str(O/p.relative_to(D)) if (O/p.relative_to(D)).exists() else 'derived communication by deliver.py'))
(D/'payload_manifest.json').write_text(json.dumps(dict(scope='selected meeting evidence exception: figures and statistical CSV; no checkpoints, raw z cache or fonts',files=payload,total_bytes=sum(r['bytes'] for r in payload)),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(main_cn=str(MEET/'meeting_brief_crosscoder_domain_members_cn.md'),selected_files=len(payload),selected_bytes=sum(r['bytes'] for r in payload)),ensure_ascii=False))
