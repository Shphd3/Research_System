from common import *
import shutil,pickle,resource
A=OUT/'analysis';E=PROJECT
(E/'figures').mkdir(exist_ok=True);(E/'evidence').mkdir(exist_ok=True);(E/'provenance').mkdir(exist_ok=True)
for p in (OUT/'figures').glob('*'):
 if p.suffix in ['.png','.pdf']:shutil.copy2(p,E/'figures'/p.name)
selected=['readout_metrics','finite_sample_bounds','contrasts','reconstruction','coverage','features_top12','frequency_signed_contributions','feature_preference_validation','feature_relations','pair_increment_contrasts','D_H_text_lexicon_validation','strict_source_position_matching','granularity_interactions_Holm4','training_subset_sensitivity','nearby_band_sensitivity','quantization_summary','multi_token_transfer','feature_and_residual_readouts','fit_ledger','numerical_checks']
for n in selected:shutil.copy2(A/(n+'.csv'),E/'evidence'/(n+'.csv'))
for name in ['config.json','freeze.json']:shutil.copy2(OUT/name,E/'provenance'/name)
for name in ['smoke.json','spectrum.json','independent_validation.json']:shutil.copy2(OUT/'audits'/name,E/'provenance'/name)
read=lambda n:list(csv.DictReader((A/(n+'.csv')).open()))
m=read('readout_metrics');b=read('finite_sample_bounds');r=read('reconstruction');features=read('features_top12');lex=read('D_H_text_lexicon_validation');inter=read('granularity_interactions_Holm4');cov=read('coverage');nm=json.load(open(OUT/'audits/independent_validation.json'))
TN={'coarse':'数学／生物','math_fine':'代数／分析','bio_fine':'细胞／生态进化'};TE={'coarse':'Math / biology','math_fine':'Algebra / analysis','bio_fine':'Cell / ecology-evolution'}
def val(t,k):return float(next(x for x in m if x['task']==t and x['condition']=='standardized__'+k)['balanced_accuracy'])
def acc_table(lang):
 s='| '+('任务｜留出独立文档' if lang=='cn' else 'Task / heldout documents')+' | '+('头64 | 中64 | 尾64 | 全1024' if lang=='cn' else 'Head64 | Middle64 | Tail64 | Full1024')+' |\n|---|---:|---:|---:|---:|\n'
 for t,n in [('coarse',37),('math_fine',17),('bio_fine',18)]:s+=f'| {(TN if lang=="cn" else TE)[t]} · n={n} | '+ ' | '.join(f'{val(t,k):.1%}' for k in ['head','middle','tail','full'])+' |\n'
 return s
summary_cn='''# R12：谱位置与语义粒度

[English](summary.md) · [协议](protocol_cn.md) · [完整证据、控制与不足](detailed_cn.md) · [真实文本实例](text_cases_cn.md) · [资产与数据口径](assets_and_data_cn.md)

**认识更新：这份小样本自然文本面板没有建立“大奇异值对应粗类别、中小奇异值补充细类别”的稳定排序。谱头同时能读出粗、细类别，生物细分类在中段也有信号；中尾相对谱头的专属新增收益未超过同维数对照。CrossCoder保留了约80%–82%的当前类别平均判别分数差，残差仍携带可读类别关联。这个百分比不是信息解释率。**

这是实测后的AI认识更新，供研究者审阅；科研接受、机制判断与问题关闭仍为Unknown。结论限于当前面板和线性读出。原留出曾在R11使用，本轮虽在新选型冻结后才读其数值，也只能算探索性评估。

阅读分三条：①分类读出及因素对照；②表征谱组织；③测量质量。这里的“预测”是读出分类，不是语言模型原生回答；功能干预未运行。

## 先定义研究对象

我们研究同一Qwen3-0.6B-Base最后block27输出、最终归一化之前的1024维向量。把旧R04发现自然文本的9600个向量共同中心化并做PCA，得到按方差递减的正交方向。固定头1–64、中481–544、尾961–1024，三段各64维。R07／R10用的是同一个谱，复用不是独立复现。

类别在表征之外定义：数学下的代数／分析，生物下的细胞／生态进化。每篇固定选择位置96–191中最后一个前导空格the，只用该位置之前已读文本核查标签。100个四叶候选文档中96篇有此目标，发现／开发／留出39／20／37，每篇一处；含混细标签保留在粗任务、从主细任务排除。三个任务均以每类8篇发现、4篇开发训练和选参。数学与生物细任务留出分别17、18篇，不能把多个任务中的重复文档相加。

## 认识更新一：类别信息没有整齐地按粗细分到不同谱段

目的不是比较哪个任务更容易，而是对同一任务换谱段，再比较这种差值是否随类别层级改变。下表是训练集逐坐标标准化、同流程线性读出的平衡正确率，即两个类别正确率的平均；机会水平50%。

'''+acc_table('cn')+'''
![不同谱段的类别可读性](figures/figure2_band_readability.png)

图2横轴是输入空间，纵轴是类别均衡正确率。三图分别固定同一任务及同一组留出文档；全空间和预定随机64维也有参照。误差线使用按类别的保守文档二项界，避免18篇全对时把经验bootstrap的[100%,100%]当作高精度证据。数学细任务的全空间点估计87.5%，但保守界约46.0%–98.9%，其强结论仍受小样本限制。全空间没有胜过头部不表示它数学上含有更少信息，而是有限样本和正则化下的拟合表现。

更直接的粒度检验是“中／尾减谱头”的细任务差值，再减粗任务同一差值。生物的中、尾交互点值为+32.5、+32.3个百分点，配对区间为[+7.6,+57.2]、[+2.2,+65.2]；四个交互检验Holm校正后p为0.076、0.117，尚未确认。数学两项区间跨零。因而不能用这张表宣布由粗到细的规律。

![谱与分析区间](figures/figure1_spectrum.png)

图1展示参考协方差特征值（与奇异值平方成比例）和累计方差。三段分别占53.07%、2.32%、0.53%参考方差；低方差不等于无类别信息。1024个特征值全正，但924个相邻相对谱隙小于1%，因此解释固定子空间及其读出轴，不给单根方向强贴语义。

## 认识更新二：增加中尾方向没有显示稳定的专属增量

![同维数新增信息](figures/figure3_increment.png)

图3固定头64，新增64维后比较头延长、中、尾和与头正交的随机方向；四个条件都128维，纵轴是相对头64的百分点变化。生物“头+中”由88.9%到100%，但“头延长”同样100%，不能把+11.1点归为中段独有贡献。数学“头+中／尾”分别比头部低6.2／18.8点，而头延长提高5.6点。所有主增量相对同维参照的检验均未建立正收益。

这只说明当前线性读出没有确认中尾的独立增益，不证明这些谱段没有信息。10个固定训练子集种子显示，数学头／中正确率中位数约70.5%／69.8%，主次会随取样变化；生物头部、中段相对稳定。完整标准化、原尺度、所有随机种子、邻近区间和量化敏感性保留于附录，未选择新赢家替换主结果。

## 认识更新三：CrossCoder保留多数当前判别分数，却没有吞掉全部区别

![重构保留与残差信息](figures/figure4_reconstruction_residual.png)

先在真实h上拟合一次谱投影、尺度和读出，再原样施加于完整重构。粗任务正确率89.3%→84.1%，数学细任务87.5%→87.5%，生物细任务100%→100%。但正确率不变不意味着分数不变：重构分别保留82.1%、79.6%、81.2%的两类平均固定分数差，余下17.9%、20.4%、18.8%落在残差。总体归一化平方重构误差为11.6%、14.0%、9.4%，不能换写成信息解释比例。

残差另拟合读出的正确率为76.3%、75.7%、88.9%，与上面的固定保留测试单列。A22的z来自14层联合编码，因此重构重新拟合后偶尔更好，也不代表仅从最后层创造了新信息。完整有符号成员贡献加上常数和残差，逐样本重现原固定分数，最大误差约1.8e−15。

## 认识更新四：成员使用可分解，精确语义与功能关系仍不能跳步

![成员频率、响应和真实前文](figures/figure5_features_text.png)

图5每个点是一篇留出文档在同一the处的原生共享z，零也保留。f3098在数学17/19篇、生物1/18篇激活；但数学内部仍有高、零响应反例。f8693在代数5/8、分析3/9篇激活，正值均值约0.110／0.053，说明出现比例和正值强度都可参与同一份差异。只有两类各≥3个正文档时才解释条件幅值；单侧零或支持少时不强分幅值效应。

独立DCLM参考发生率分别为f3098 0.835%、f8693 0.465%、f9533 1.671%、f63 0.221%，原分组属于中、中、高、低；不是当前样本发生率，更不是谱段标签。完整16384成员全部进入有符号账目，包含增强和抵消，没有只分析旧16个严格成员。

发现集冻结的每任务12名中，留出均值偏向点估计同向为11／12、9／12、12／12；36名统一Holm校正后，仅粗任务4名通过探索性规则，两项细任务均0名。词汇解释也有正反面：发现集提出的词项与粗任务头部、生物头／中段分数在留出保持关联（Holm9 p≈0.0007／0.022／0.035），数学三段未通过。它支持特定词汇／对象关联，不足以给整段或每个feature贴单一语义名。

反例很具体：f9533在古蚂蚁捕食、形态和生态变化的前文中z≈0.1114，在同属生态进化标签、讨论哺乳动物后代性别策略的前文中z=0。同一细类不保证同一成员响应。完整高／居中／低文本、当前词面、位置和后续文字的独立标记见实例页。

18个预定成员对在控制基础发生频率及来源后，没有BH q<0.05关系（最小约0.782）。加入成对出现乘积，相比同参数数目的单成员新增，三个任务差值−7.9／0／−11.1点，没有组合增益证据。共同响应因此只保留统计含义。

## 竞争解释与结论边界

同token控制排除了纯目标身份解释，但不同前文的词汇、格式、长度和来源仍会变化。严格同平台、同文体且位置差≤32时，仅粗任务5对、数学细任务1对、生物细任务3对；两个细任务不足，不能认证纯语义差异。来源／格式基线在数学细任务也达到69.4%，竞争解释仍然强。旧留出暴露、每类少量文档和标签体系的领域交叉共同限制推广。

**假设状态：**“谱头只承担粗类”的简单独占说法被这些细类读出削弱；“细类相对更偏后部”和“中尾有超出同维数对照的独立增量”均未建立；“字典已解释全部类别区别”被残差账目及残差读出削弱。没有因果、训练动态或MoE收益结论。

**AI建议的唯一下一步：**若继续检验粒度规律，优先建立全新、来源与文体交叉均衡、常见token覆盖充分的四叶确认面板；先提高独立文档支持，而不是增加层数、分类器或换谱段。当前不自动启动该新面板。

本轮计算全部在CPU完成：新增模型前向0、语言模型／字典训练0、GPU使用0。5组主图和1组敏感性图、全部要求的适用分析及不足记录已交付；科学接受仍Unknown。
'''
(E/'summary_cn.md').write_text(summary_cn)
summary='''# R12: spectral position and semantic granularity

[中文](summary_cn.md) · [Protocol](protocol.md) · [Detailed evidence](detailed.md) · [Actual text cases](text_cases.md) · [Asset/data bindings](assets_and_data.md)

**Recognition update: this small natural-text panel does not establish a stable coarse-to-fine spectral ordering. The head reads both domains and within-domain topics; biological fine categories are also readable in the middle. Middle/tail augmentation has no established benefit beyond matched-dimensional controls. CrossCoder preserves about80–82% of the current between-class mean fixed-readout score difference, while residuals retain readable class association. This fraction is not an information-explained percentage.**

This is a bounded AI interpretation for researcher review; scientific acceptance, mechanism judgment and closure remain Unknown. R11 H was exposed previously. R12 froze new choices before numeric H access, but its evaluation remains exploratory.

The three reading paths are prediction/factor controls; representation organization; measurement quality. Predictions here are classifier readouts, not native LM answers. Functional interventions were NOT RUN.

## Objects, tasks and evidence scope

Use frozen Qwen3-0.6B-Base, zero-based block27 residual-post before final norm,1024 dimensions. The fixed old R04/R10 basis is pooled PCA of9600 centered discovery vectors. R07 used the same basis: reuse is not independent replication. Prespecified64D bands are1–64,481–544,961–1024. They carry53.07%,2.32%,0.53% of reference variance.

External labels are algebra/analysis within math and cell/ecology-evolution within biology. Select the last token279, leading-space the, at position96–191, one observation per document, and review only its visible prefix. Of100 candidate documents,96have this token:39D/20V/37H. Ambiguous fine labels remain in the coarse task but are excluded from primary fine tasks. Each task fits8D and selects on4V documents per class. Fine H sizes are17and18; overlapping tasks are not additional independent documents.

## Bands do not form an established granularity hierarchy

'''+acc_table('en')+'''
![Band readability](figures/figure2_band_readability.png)

Balanced accuracy averages the two class recalls; chance is50%. Error bars are conservative classwise exact document intervals, including uncertainty when18/18are correct. Math-fine full-space87.5% has a conservative interval about46.0–98.9%; strong claims remain sample-limited. A fitted full-space model losing to head64does not mean the containing space has less information; finite-sample estimation and regularization differ.

The relevant granularity interaction compares middle/tail-minus-head within each task and then fine-minus-coarse, sharing document resamples. Biology interactions are+32.5/+32.3pp, paired intervals[+7.6,+57.2]/[+2.2,+65.2], but Holm4p=.076/.117. Math intervals cross zero. No general hierarchy is confirmed.

![Fixed spectrum](figures/figure1_spectrum.png)

The curve shows covariance eigenvalues, proportional to squared singular values, and cumulative variance. All1024values are positive, but924adjacent relative gaps are<1%; interpret bands/classifier axes, not stable individual-root semantics.

## Augmentation is not a middle/tail-specific increment

![Equal-dimensional additions](figures/figure3_increment.png)

All additions have128dimensions: head+next64, head+middle64, head+tail64 and head+orthogonal-random64. Biology head+middle rises88.9→100%, but head extension also reaches100%. Math middle/tail additions change head accuracy by−6.2/−18.8pp, while head extension adds5.6pp. Main comparisons establish no positive increment beyond equal-dimensional controls.

Ten fixed training-subset seeds show math head/middle medians70.5/69.8%, with changing ordering. Biology head/middle are more stable. Original-scale, all-random-seed, nearby-boundary and quantization checks are retained without selecting replacements.

## Reconstruction retains most fixed score contrast, not all distinctions

![Reconstruction and residual](figures/figure4_reconstruction_residual.png)

Freeze the projection, training scaler and readout fitted on actual h, then apply them to complete reconstruction. Coarse accuracy89.3→84.1%, math-fine87.5→87.5%, biology-fine100→100%. Yet reconstructed mean class-score contrasts retain82.1/79.6/81.2%; residual contributions are17.9/20.4/18.8%. Overall normalized squared errors11.6/14.0/9.4% are a different quantity.

Separately refitted residual classifiers reach76.3/75.7/88.9%. This is re-accessibility, not fixed-readout preservation. A22 zjointlyencodes14layers: refitted reconstruction outperforming actual-h fitting cannot show that last-layer information was created. Full signed feature+bias+residual accounting reproduces original scores within about1.8e−15.

## Features, text hypotheses and relations

![Features and actual prefixes](figures/figure5_features_text.png)

Each dot is one document at the same the, including zeros. f3098activates in17/19math and1/18biology documents, with within-math high/zero counterexamples. f8693activates in5/8algebra and3/9analysis documents; positive means are.110/.053, illustrating both occurrence and amplitude differences. Conditional-positive amplitude interpretation requires>=3positive documents in BOTH classes; zero-filled algebraic splits do not identify amplitude effects otherwise.

Independent DCLM rates for f3098/f8693/f9533/f63are.835/.465/1.671/.221%, middle/middle/high/low under inherited cuts. These are neither panel response counts nor spectral ranks. All16384features enter the signed accounting, including cancellation and reference-insufficient members.

D-selected12features/task have same-direction Hpoint preferences11/12,9/12,12/12. Holm36leaves4coarse features and0in either fine task under exploratory rules. D-derived lexical hypotheses generalize for coarse head and biological head/middle (Holm9p≈.0007/.022/.035), not mathematical bands. These are lexical/object associations, not a semantic ontology. f9533responds.1114to an ancient-ant morphology/predation prefix but0to another ecology-evolution prefix about mammalian offspring sex strategy: category membership does not ensure feature use.

None of18prespecified frequency/source-adjusted pairs has BHq<.05(min≈.782). Pair products versus equally parameterized single-feature additions give−7.9/0/−11.1pp. There is no reliable combination increment or functional-interaction evidence.

## Rivals, boundaries and next decision

Fixed token identity does not fix prefix vocabulary, source, style or length. Strict same-platform/genre/within32positions matching supplies5coarse,1math-fine and3bio-fine pairs. Fine semantic attribution remains insufficient. Math source/format-only accuracy69.4% retains a credible rival. Exposed H, few documents, overlapping subject definitions and conditional readout fitting limit generalization.

The simple exclusive head=coarse account is weakened by fine readout observations. Relative later-band preference and matched-control independent increments are NOT_ESTABLISHED. Complete dictionary explanation is weakened by residual accounting/readout. No native causal, training-dynamic or MoE benefit claim follows.

**One AI-proposed next decision:** whether to collect a fresh source/genre-crossed four-leaf common-token confirmation panel. Improve independent-document support before expanding layers, classifiers or band search. It is not automatically started here.

All computation used CPU. New model forwards0,LM/dictionary updates0,GPU usage0. Five main figures,one sensitivity appendix and all applicable measurements/insufficiency records are complete; scientific acceptance remains Unknown.
'''
(E/'summary.md').write_text(summary)
# Curated actual examples: selection was frozen on D ranks, then fixed H extremes.
examples=json.load(open(A/'text_examples.json'));keep=[]
for t in TN:
 f=next(r for r in list(csv.DictReader((A/'D_feature_freeze.csv').open())) if r['task']==t)['feature_id']
 keep += [r for r in examples if r['task']==t and r['kind'] in ['feature_'+f+'_high','feature_'+f+'_low','band_head_high','band_head_low']]
for language in ['cn','en']:
 s=('# 真实前文与反例\n\n' if language=='cn' else '# Actual prefixes and counterexamples\n\n')
 s+=('每个目标都是同一token279。下面只展示模型已经看见的完整前文；截断后的内容不参与解释。选择规则是发现集首位成员，以及冻结头部轴在H的高／低分位端点；不根据故事是否漂亮换例。全部54个高／居中／低案例留执行侧analysis/text_examples.json。\n\n' if language=='cn' else 'All targets are token279. Only the complete already-visible prefix is displayed. Cases use the D-frozen top feature or fixed head-axis Hextremes; no replacement for readability. All54high/median/low cases remain execution-side.\n\n')
 for r0 in keep:
  score0=r0.get('z',r0.get('score'));s+=f'## {r0["task"]} · {r0["kind"]} · {r0["seq_id"]}\n\nTopic `{r0["topic"]}`; zero-based position {r0["position"]}; '+('native z' if 'z' in r0 else 'fixed readout score')+f' = {score0:.6f}.\n\n```text\n{r0["prefix"]}\n```\n\n'
 s+=('具体反例：f3098的低响应也来自数学前文，f9533的高／低都可来自生态进化前文。它们限制单一领域／细类语义命名。来源和格式没有被这些实例消除。\n' if language=='cn' else 'Counterexamples: f3098can be zero in math; f9533can be high or zero within ecology/evolution. These limit a single category name and do not eliminate source/format rivals.\n')
 (E/('text_cases_cn.md' if language=='cn' else 'text_cases.md')).write_text(s)
# Formal coverage ledger; no optional layer is disguised as executed.
ledger=[('01_assets_authority','DONE_VALID','Anchor15_27_05,protocol,stable input IDs,current selected access','no new training'),('02_prefix_labels_splits','DONE_EXPLORATORY','100candidates;96primary documents/positions;39D20V37H;five fine-mixed exclusions','AI labels;H exposed;fine source matching insufficient'),('03_spectrum_numeric','DONE_VALID','1024positive eigenvalues;64D fixed bands;orthogonality3.4e-15','same old basis;924small gaps;no individual semantic root'),('04_band_readouts','DONE_EXPLORATORY','3tasks;shared budgets16D/8V;all predefined scales/random/full controls','17/18fine H;math sensitive;finite fitted-model uncertainty'),('05_increment','DONE_EXPLORATORY','128D matched additions and document error corrections','no established middle/tail advantage beyond controls'),('06_text_explanation','DONE_EXPLORATORY','9D-derived lexical hypotheses;54actual cases;proxy and counterexample tables','coarse head/bio head-middle lexical associations;math not confirmed'),('07_reconstruction_residual','DONE_EXPLORATORY','fixed original heads;separate refit heads;signed additivity;NMSE','14layer joint encoder;not information quantity or causal use'),('08_feature_frequency_presence_amplitude','DONE_EXPLORATORY','all16384features;36D-selected members;independent65536position rate','one-sided amplitude undefined;fine per-feature confirmation insufficient'),('09_relations_combinations','DONE_EXPLORATORY','18D-selected pairs;frequency/source-controlled tests;19parameter controls','no adjusted relation or combination advantage'),('10_stability_validation','DONE_VALID','15independent CSR/score replays;10subset seeds;3nearby bands;30quantization draws','sensitivities not independent replications;primary unchanged'),('11_delivery','DONE_VALID','bilingual Summary/Detailed,5main+1appendix figures,actual asset registration','scientific acceptance/closure Unknown;local only')]
table(E/'evidence/coverage_ledger.csv',[dict(task=k,status=v,evidence=e,boundary=bd) for k,v,e,bd in ledger]);table(OUT/'analysis/coverage_ledger.csv',[dict(task=k,status=v,evidence=e,boundary=bd) for k,v,e,bd in ledger])
# Compact auditable input identity, including current cache file digests.
old=json.load(open(OLD/'analysis/scientific_freeze.json'));oldhash=old.get('sha256',{});unique={r['seq_id']:r for r in rows(OUT/'data/selected_metadata.jsonl')};inputhash={};match=0
for row in unique.values():
 p=get_cache(row);h=sha(p);inputhash[str(p)]=h
 if str(p) in oldhash:assert oldhash[str(p)]==h;match+=1
for p in [ROOT/'R10_domain_member_atlas_20261030/analysis/common_spectrum.npz',ROOT/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz',OLD/'data/documents.jsonl'] :inputhash[str(p)]=sha(p)
dump(OUT/'provenance/actual_input_hashes.json',{'sha256':inputhash,'R11_preH_DV_hashes_matched':match,'unique_cache_documents':len(unique),'H_historical_hash_availability':'R11preHfreeze cannot bind later Hpayloads;actual current Hhashes retained here','model_weights_not_rehashed_in_this_round':True})
inputs=['model_qwen3_0p6b_base_official_a5','tokenizer_qwen3_0p6b_base_official_a5','crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013','analysis_a15_27_r04_domain_discriminability_complete_A01_20261028','analysis_a15_27_03_r09_domain_difference_decomposition_20261029','analysis_a15_27_04_r10_domain_member_atlas_20261030','data_a15_27_r11_qualified_three_domain_A02_20261030','representation_a15_27_r11_A02_dv_native_jointz_h27_20261030','representation_a15_27_r11_A02_h_native_jointz_h27_20261030','analysis_a15_27_r11_qualified_three_domain_A02_20261030']
dump(E/'provenance/asset_inputs.json',{'input_asset_ids':inputs,'output_analysis_id':'analysis_a15_27_05_r12_spectral_semantic_granularity_20261031','actual_payload_root':str(OUT),'new_model_forwards':0,'training_updates':0})
print('SUMMARY/TEXT/TABLES saved;',len(unique),'cache documents hashed;',match,'old D/V hashes matched')
