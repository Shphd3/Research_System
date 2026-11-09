from core import *
import pandas as pd, shutil, zipfile
from datetime import datetime,timezone
P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs')
res=json.loads((R/'results/result_summary.json').read_text());cells=pd.read_csv(R/'results/all_cells_final.csv');primary=pd.read_csv(R/'results/primary_336_final.csv');support=json.loads((R/'results/lexical_support.json').read_text());cases=json.loads((R/'results/selected_cases.json').read_text());audit=json.loads((R/'provenance/results_audit.json').read_text());assert audit['status']=='PASS'
for d in ['figures','evidence','code','provenance']: (P/d).mkdir(exist_ok=True)
for p in (R/'figures').glob('*.png'):shutil.copy2(p,P/'figures'/p.name)
for name in ['primary_336_final.csv','matching_coverage.csv','selected_cases.json','case_pair_walkthrough.json','case_organization.json','composition_diagnostic.json','lexical_support.json','result_summary.json']:
 shutil.copy2(R/'results'/name,P/'evidence'/name)
for name in ['outcome_freeze.json','text_freeze.json','matching.json','bootstrap.json','synthetic_checks.json','reference_metric_check.json','runtime_smoke.json','results_audit.json','three_audits.md','input_file_hashes.json','input_access_resume.json','nulls_completed.json']:
 shutil.copy2(R/'provenance'/name,P/'provenance'/name)
for p in (R/'results/nulls').glob('*diagnostics.json'):shutil.copy2(p,P/'evidence'/p.name)
for p in (R/'code').glob('*.py'):shutil.copy2(p,P/'code'/p.name)
shutil.copy2(R/'config.json',P/'code/config.json')
base=cells[(cells.tier==1)&(cells.pair_class=='lexical')&(cells.same_id==0)&(cells.frequency=='all')]
sel=[]
for k,dom in [('SAE','math'),('SAE','biology'),('CC','math'),('CC','biology')]:
 near=base[(base.dictionary==k)&(base.domain==dom)&(base.metric=='identity')&(base.distance_bin==0)].iloc[0];far=base[(base.dictionary==k)&(base.domain==dom)&(base.metric=='identity')&(base.distance_bin==4)].iloc[0]
 sel.append(dict(dictionary=k,domain=dom,near_real=100*near.real,near_control=100*near.control,near_delta=100*near.delta,far_real=100*far.real,far_control=100*far.control,far_delta=100*far.delta,near_blocks=int(near.blocks),far_blocks=int(far.blocks)))
pd.DataFrame(sel).to_csv(P/'evidence/distance_reading.csv',index=False)
cnrows='\n'.join(f'| {x["dictionary"]}／'+('数学' if x['domain']=='math' else '生物')+f' | {x["near_real"]:.2f}%／{x["near_control"]:.2f}% | +{x["near_delta"]:.2f} | {x["far_real"]:.2f}%／{x["far_control"]:.2f}% | +{x["far_delta"]:.2f} | {x["near_blocks"]}／{x["far_blocks"]} |' for x in sel)
enrows='\n'.join(f'| {x["dictionary"]} / {x["domain"]} | {x["near_real"]:.2f}% / {x["near_control"]:.2f}% | +{x["near_delta"]:.2f} | {x["far_real"]:.2f}% / {x["far_control"]:.2f}% | +{x["far_delta"]:.2f} | {x["near_blocks"]} / {x["far_blocks"]} |' for x in sel)
h1qualified=primary[(primary.metric=='identity')&(primary.qualified_positive_excess==True)];qualified_nonrepeat=int((h1qualified.same_id==0).sum());matched_nonrepeat=int(((primary.metric=='identity')&(primary.same_id==0)&(primary.matched_verdict=='POSITIVE_MATCHED')).sum())
# Exact formal examples, selected for explanation; full family remains in the evidence table.
ex=primary[(primary.dictionary=='CC')&(primary.domain=='biology')&(primary.metric=='identity')&(primary.frequency=='middle')&(primary.distance=='16-31')&(primary.same_id==0)].iloc[0]
qtext=f'{100*ex.real:.2f}% 对 {100*ex.control:.2f}%，差值 +{100*ex.delta:.2f} 个百分点，同时区间 [{100*ex.simultaneous_lo:.2f}, {100*ex.simultaneous_hi:.2f}]'
formal=f'主比较中，H1 有 {res["matched_positive"]-int(((primary.metric!="identity")&(primary.matched_verdict=="POSITIVE_MATCHED")).sum())} 个条件的匹配差值同时区间高于零，其中 {res["qualified_H1"]} 个同时超过合格的保边际随机基线；非重复词面条件分别为 {matched_nonrepeat} 和 {qualified_nonrepeat} 个。每个条件的领域、频率、距离和缺项见[完整 336 项表](evidence/primary_336_final.csv)。'
summary_cn=f'''# 句内 feature 如何组织：同坐标延续明确，旧图覆盖尚未证明关联替换

**问题。** 一句话前面激活的 feature，后面是同一个坐标再次出现，还是出现与它有旧图联系的其他坐标？这些联系能否超过无关文档背景？本轮使用既有数学、生物缓存，完成三类图及随机基线；属于已暴露文本的探索性复用。

**先说明表征对象。** 每个 token 对应一列稀疏激活：每行是同一字典中的一个固定 feature 坐标。SAE 每个位置有 32 个正激活；CrossCoder 使用跨 14 层的共享坐标，不是每层各一份激活。沿句子向右，部分坐标重复出现，部分间断后重现，也有大量坐标只在一个位置出现。热图中靠上的行只是按出现次数排序，不是更高语义层级。

## 结论与认识更新

以下是证据支持的有界结论及 AI 解读；研究者机制判断与问题关闭仍为 `Unknown`。

1. **在能严格匹配的范围内，存在额外的同坐标延续；不能只归因于两端 token ID 相同。** H1 在不同 ID 条件下也有正差值。一个跨到 16–31 token 的主比较是 CrossCoder／生物／中频：{qtext}。保边际随机基线是否合格逐格记录，空分母格不补零。{formal}
2. **近处额外延续通常更强，较远处仍可存在。** 下表的全频描述性差值从距离 1 的约 20–27 个百分点，降到 16–31 的约 7–11 个百分点。它不是单调衰减定律；不同距离涉及不同长句、位置和匹配支持。64+ token 无严格词面匹配，不能说那里没有联系。
3. **图三很高的覆盖率没有证明坐标沿旧图发生替换。** 正向覆盖在真实和对照中都接近 99%，低／中频常达 100%。生物高频、距离 1 的条件性差值为 +0.590 个百分点；但在全部 2,383 个严格匹配的非重复词面位置对中，固定为双方共同消失的源坐标后，所有可定义的正向差值均为 0；使用全部源坐标也为 0。原正差值由两组采用不同的消失成员集合产生，不能读成同一批前成员更倾向连接真实后文。

**结论范围很窄。** 严格匹配覆盖 SAE 3,529／161,251＝2.19%、CrossCoder 2,383／161,251＝1.48% 的非重复词面候选对。约 84% 的匹配目标是 `the、and、of、a、with`。因此本轮回答的是这些可匹配位置上的表征关系，尚不能推广到所有数学／生物概念词，更不能证明信息完整保留、因果传递或语义层级提升。SAE 旧图接口不兼容，其 H2 单独受阻。

## 结果分析：先看真实减对照，再看原始覆盖

下表是 **T1 严格匹配、不同 token ID、词面 token、全频** 的描述性汇总；不是用全频次级读数替代分频主检验。单位“差值”为百分点。每列先对句内位置对平均，再对句子、源文档和固定两文档块等权平均。[数据](evidence/distance_reading.csv)；[逐频率主比较与同时区间](evidence/primary_336_final.csv)。

| 字典／领域 | 距离 1：真实／对照 | 差值 | 距离 16–31：真实／对照 | 差值 | 两端有效文档块数 |
| --- | ---: | ---: | ---: | ---: | ---: |
{cnrows}

**图一读“如何出现”。** 横轴是全部 token，纵轴是固定坐标，深色为正激活。每句每字典只按冻结规则展示 24 行，省略成员数和逐 token 省略数均保留。生物例有 222 个 SAE 坐标，其中 161 个只在一个位置出现，1 个贯穿全部 13 个位置；CrossCoder 有 1,681 个坐标，其中 963 个只出现一次，12 个贯穿全句。因此“持续的背景坐标与局部出现的坐标并存”是观察到的组织形式。不能因图中优先展示常出现的行，就说所有坐标都持续。[数学热图](figures/figure1_math.png) · [生物热图](figures/figure1_biology.png) · [弱例热图](figures/figure1_counterexample.png)。

**图二读“是否超过背景，以及距离差别”。** 每格上半部蓝线是真实、橙线是同领域另一文档的匹配目标；下半部紫线是真实减对照。横轴距离档是类别，不是假装等宽的实际距离。上方阴影是逐格区间，下方是主比较同时区间；无阴影可能表示区间不可计算，不能自动读成确定为零。[图二](figures/figure2_distance.png)。

**图三读“旧边是否提供额外区分”。** 正／反向分开。纵轴分母是该条件下已经消失的前成员，不能与图二相加。真正关键的是下方差值和共同消失集合诊断，而不是顶部接近 100% 的线。连线图中不少目标坐标早已在其他位置出现；画出旧箭头本身不能证明状态转换。[图三](figures/figure3_distance.png) · [真实句子连线](figures/figure3_sentence_edges.png) · [分母组成诊断](evidence/composition_diagnostic.json)。

## 两个真实例子与一个弱例

- **数学例：** “Power is determined by computing the Banzhaf power index for each player, resulting in a power distribution for the weighted voting system.” 这句讲参与者的投票权力如何由 Banzhaf 指数计算。在 5 个可匹配的不同 ID 位置对上，SAE 延续为 42.50% 对 9.38%，差值 +33.12 个百分点。其中 `computing → the` 是 21／32 对 4／32。它说明同一后目标词面下仍有坐标差别，不等于已识别出“投票权力概念”的专属坐标。5 对共用同一真实目标与同一对照目标，不能当作 5 个独立重复。该句没有合格的 CC T1 对。
- **生物例：** “Cell division in the papilla is either rare or non-existent.” 这句说乳头部位的细胞分裂很少发生或不存在。3 个可匹配对中，CC 同坐标延续为 37.98% 对 18.46%；正向旧图覆盖为 99.76% 对 98.12%。但在 `Cell → the` 这一对上，真正共同消失的 165 个坐标在两组都全部能沿旧图相连：100% 对 100%。它正好说明为什么正向覆盖的小优势不能直接叫替换。
- **弱例：** “A typical example here is to use the abstract tensor formalism to understand Hopf algebras.” 4 个匹配对的 SAE 延续为 21.88% 对 26.56%，CC 为 28.77% 对 29.44%，均未超过对照；CC 正向差值 −0.336、反向 +0.115 个百分点。按冻结规则，**没有找到 H1、正向 H2、反向 H2 三项都非正的严格反例**，这里展示的是最弱可用例。它反对“每句话都有额外同坐标延续”的泛化，不证明原始延续为零。

例子均按事先固定的极值规则选取，是刻意选择的解释材料，不是代表性样本。[完整选例与成员](evidence/selected_cases.json)；[逐位置算例](evidence/case_pair_walkthrough.json)。

完整设置、随机基线、缺项、源文件、脚本与审计见 [Detailed](detailed_cn.md)。唯一待研究者决定的问题仍是：在这些限定和词面偏向下，哪一个残余模式值得另行设计上下文替换干预。本轮未执行该干预，也未关闭问题。
'''
summary_en=f'''# Within-sentence organization: coordinate recurrence, without established old-graph replacement

**Question.** Do earlier active coordinates recur later in the same math/biology sentence, or connect to different later coordinates through an old graph, beyond unrelated-document controls? This completed cache analysis reuses exposed texts and is exploratory.

**Representation.** Each token is a column of native sparse positive activations, each row a fixed dictionary coordinate. SAE has 32 active coordinates per position. CrossCoder has one shared code across 14 residual-post hooks, not independent layerwise activations. Persistent, intermittent and position-local coordinates coexist; heatmap row order has no semantic-level meaning.

## Conclusion and recognition update

These are bounded evidence-based conclusions and AI interpretation. Human mechanism acceptance and question closure remain Unknown.

1. **Matched positions exhibit extra same-coordinate recurrence, including different token IDs.** Of the primary H1 cells, {res['qualified_H1']} pass both positive simultaneous matched intervals and qualified fixed-margin-null diagnostics; {qualified_nonrepeat} of these are different-ID cells. For CC/biology/middle-frequency at distance 16–31, real persistence is {100*ex.real:.2f}% versus {100*ex.control:.2f}%, an excess of {100*ex.delta:.2f} percentage points with simultaneous interval [{100*ex.simultaneous_lo:.2f}, {100*ex.simultaneous_hi:.2f}]. Random empty denominators invalidate the affected cell-null envelope; they are never converted to zero. The [336-cell ledger](evidence/primary_336_final.csv) retains all missing and insufficient cells.
2. **Excess is descriptively larger nearby and can persist farther away.** All-frequency diagnostic excess is about 20–27 points at distance 1 and 7–11 points at 16–31. This is not a monotonic decay law or a causal effect of distance: sentence length, positions and matching support differ. There are no exact-ID lexical matches at 64+.
3. **Near-saturated old-graph coverage does not establish replacement.** Forward coverage is about 99% in both conditions, often 100% for low/middle-frequency sources. The biology/high-frequency distance-1 conditional excess is +0.590 points. Yet all defined common-lost-source forward differences are exactly zero across the 2,383 T1 different-ID lexical pairs; all-source forward differences are also zero. Changing lost-source composition generates the small conditional advantage, without demonstrating preferential connection for a fixed source set.

**Scope.** T1 covers only 3,529/161,251 (2.19%) SAE and 2,383/161,251 (1.48%) CC different-ID lexical pairs. About 84% of matched target instances are `the`, `and`, `of`, `a`, or `with`. Findings therefore concern this narrow support, not all scientific concept words. No causal transfer, complete retention or semantic hierarchy is established. SAE H2 remains blocked by the old graph's unqualified activation interface.

## Analysis and reading the figures

The following all-frequency table is descriptive; it does not replace the frequency-specific primary tests. Real and control use the identical matched mask and equal pair-within-sentence, sentence-within-document, document-within-block, then block weights. [Source table](evidence/distance_reading.csv).

| Dictionary/domain | Distance 1: real/control | Excess (pp) | Distance 16–31: real/control | Excess (pp) | Contributing blocks, near/far |
| --- | ---: | ---: | ---: | ---: | ---: |
{enrows}

**Figure 1:** token order horizontally, fixed coordinates vertically, binary positive activity in dark color. Only the frozen top 24 recurring rows are displayed; omitted union and per-token counts are saved. The biology sentence has 222 SAE coordinates (161 occur at one position, one at all 13 positions) and 1,681 CC coordinates (963 occur once, 12 at every position). This shows coexistence of recurring backgrounds and local coordinates, not that all features persist. [Math](figures/figure1_math.png), [biology](figures/figure1_biology.png), [weak case](figures/figure1_counterexample.png).

**Figure 2:** top blue/orange curves are real/control persistence, bottom purple is real minus control. Horizontal categories are token-distance bins; top uncertainty is pointwise, bottom uncertainty simultaneous across the registered primary family. A missing band does not imply a known zero. [Figure 2](figures/figure2_distance.png).

**Figure 3:** separate forward/reverse old-edge coverage of lost source coordinates. Its denominator differs from H1, so the percentages cannot be added. Read the excess and common-source diagnostic, not the near-100% forward level alone. The arrow diagram uses actual old same-token coactivation edges; it does not show information flow or state transitions. [Figure 3](figures/figure3_distance.png), [sentence edges](figures/figure3_sentence_edges.png), [composition audit](evidence/composition_diagnostic.json).

## Actual examples and weakest case

- **Math:** “Power is determined by computing the Banzhaf power index for each player, resulting in a power distribution for the weighted voting system.” Five eligible different-ID pairs give SAE 42.50% versus 9.38%, +33.12 points. `computing → the` gives 21/32 versus 4/32 retained coordinates. All five pairs share one target/control, so they are not independent replicates. No qualifying CC T1 pair exists for this sentence; no coordinate has been assigned a voting-power semantic label.
- **Biology:** “Cell division in the papilla is either rare or non-existent.” Three eligible pairs give CC identity 37.98% versus 18.46%, and forward graph coverage 99.76% versus 98.12%. For `Cell → the`, all 165 common-lost coordinates connect in both conditions: 100% versus 100%. This is a concrete denominator-composition warning.
- **Weak case:** “A typical example here is to use the abstract tensor formalism to understand Hopf algebras.” Four pairs give SAE 21.88% versus 26.56%, CC 28.77% versus 29.44%; CC forward excess is −0.336 points, reverse +0.115. No sentence meets the frozen requirement that all three CC excesses be nonpositive. This is the weakest available case and a counterexample to universal extra identity recurrence, not zero raw recurrence.

Examples were selected by frozen extremes and are not representative. [Selected cases](evidence/selected_cases.json), [pair walkthrough](evidence/case_pair_walkthrough.json). Full methods, null qualification, limitations and lineage are in [Detailed](detailed.md). The researcher decides whether any bounded residual warrants a separate context-replacement intervention; none was run or authorized by these results.
'''
(P/'summary_cn.md').write_text(summary_cn);(P/'summary.md').write_text(summary_en)
# A concise first reading, with results before detailed analysis.
(P/'one_page_cn.md').write_text('''# 一页结果：句内 feature 延续与旧图关联

**问题：前面激活的坐标，后面如何再次出现，是否超过无关背景？** 每个 token 有自己的稀疏活跃集合；一句话中既有多处重复的坐标，也有只在局部出现的坐标。不同字典分别统计，坐标编号没有预设语义标签。

**本轮认识更新：同坐标延续获得有界支持；旧图的高覆盖尚不能证明关联坐标替换。** 非重复词面条件下，近处真实减对照的全频差值约为 20–27 个百分点，16–31 token 处约为 7–11 个百分点。旧图正向覆盖在真实和对照中都接近 99%；固定共同消失的源成员后，严格匹配条件下的正向差值全部为零。

这些结论只覆盖可匹配子集。严格匹配率为 SAE 2.19%、CrossCoder 1.48%，约 84% 的目标是 `the、and、of、a、with`。64+ 无主比较匹配；SAE 的旧图接口不合格。结果不证明因果传递、信息完整保留或语义提升。

先读 [完整结论与认识更新](summary_cn.md)，再看三类图：

1. [数学热图](figures/figure1_math.png)／[生物热图](figures/figure1_biology.png)：横轴 token、纵轴坐标，深色为激活。常出现的 24 行不能代表所有成员。
2. [同坐标延续与距离](figures/figure2_distance.png)：重点看下方紫色“真实减对照”，同时看区间与文档块数。
3. [旧图覆盖与距离](figures/figure3_distance.png)：正反向分开；接近 100% 的原始覆盖不代表额外句内联系。[实际旧边示意](figures/figure3_sentence_edges.png)。

[两个实句及最弱例的逐项解释](summary_cn.md#两个真实例子与一个弱例) · [完整证据、脚本和缺项](detailed_cn.md)。严格“三项均非正”的反例未找到，未补造。研究者机制判断和问题关闭仍为 Unknown；本次仅本地保存与同步，未 commit/push。
''')
(P/'one_page.md').write_text('''# One-page result: within-sentence coordinate recurrence and old-graph association

The question is whether earlier active coordinates recur or connect to later coordinates beyond unrelated-document background. Each token has a sparse native active set; recurring, intermittent and local coordinates coexist.

**Bounded update:** same-coordinate recurrence is supported on qualified matched strata; saturated old-graph coverage does not establish associated-coordinate replacement. Different-ID all-frequency diagnostic excess is about 20–27 percentage points at distance 1 and 7–11 at distance 16–31. Forward graph coverage is about 99% in both conditions; every defined T1 different-ID common-lost-source forward contrast is zero.

T1 matching covers only 2.19% of eligible SAE and 1.48% of CC different-ID lexical pairs, with about 84% of targets among five common function words. No primary lexical match exists at 64+; SAE graph interface qualification is unavailable. Causal transmission, complete retention and semantic upgrading are not established.

Read [Summary](summary.md), then [sentence heatmaps](figures/figure1_biology.png), [identity versus distance](figures/figure2_distance.png), and [old-edge coverage](figures/figure3_distance.png). [Detailed](detailed.md) contains the actual examples, weakest available case, controls, nulls, scripts and limitations. Human mechanism acceptance/closure remain Unknown. Local delivery only; no commit/push.
''')
print('Summary and one-page written',res)
