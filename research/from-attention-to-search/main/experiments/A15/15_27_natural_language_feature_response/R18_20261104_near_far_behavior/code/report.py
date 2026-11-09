from common import *
import csv,math,shutil
cfg=json.load(open(R/'config.json'));res=json.load(open(R/'results/summary.json'));summ=res['summaries'];pairs=list(csv.DictReader(open(R/'tables/family_pairs.csv')))
data={x['id']:x for x in rows(R/'data/panel.jsonl')};scores={x['id']:x for x in rows(R/'results/smoke.jsonl')+rows(R/'results/heldout.jsonl')};families={x['family']:x for x in json.load(open(R/'data/families.json'))}
def pct(x):return f'{100*float(x):.1f}%'
def mdtable(head,rr):return '| '+' | '.join(head)+' |\n|'+'|'.join(['---']*len(head))+'|\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rr)+'\n'
main=[s for s in summ if s['split']=='heldout' and s['mode']=='main'];para=[s for s in summ if s['split']=='heldout' and s['mode']=='paraphrase'];lure=next(s for s in summ if s['split']=='heldout' and s['mode']=='lure')
tbl=mdtable(['actual gap','families','accuracy (prompts)','paired correct/24','paired rate [95% Wilson]','mean correct margin [95% family CI],nat','point>=80%','evidence eligibility'],[[s['planned_distance'],s['families'],f"{s['correct_A']+s['correct_B']}/48 ({pct(s['accuracy'])})",s['paired_success'],f"{pct(s['paired_rate'])} [{pct(s['paired_wilson_lo'])},{pct(s['paired_wilson_hi'])}]",f"{s['mean_margin']:.4f} [{s['margin_lo']:.4f},{s['margin_hi']:.4f}]",s['point_gate'],s['evidence_eligibility']] for s in main])
ptbl=mdtable(['planned gap','actual range','paired correct/24','correct prompts/48','mean margin,nat'],[[s['planned_distance'],f"{s['actual_distance_min']}–{s['actual_distance_max']}",s['paired_success'],s['correct_A']+s['correct_B'],f"{s['mean_margin']:.4f}"] for s in para])
chosen=[]
for d in [128,64,16]:
    q=[x for x in pairs if x['mode']=='main' and x['split']=='heldout' and int(x['planned_distance'])==d and x['paired_success']=='1']
    if q: chosen.append(('成功配对',q[0]));break
for d in [128,64,16]:
    q=[x for x in pairs if x['mode']=='main' and x['split']=='heldout' and int(x['planned_distance'])==d and x['paired_success']=='0']
    if q:chosen.append(('失败配对',q[0]));break
q=[x for x in pairs if x['mode']=='lure' and x['paired_success']=='0']
if q:chosen.append(('近处错误物品诱饵：失败',q[0]))
for extra in [x for x in pairs if x['mode']=='main' and x['split']=='heldout' and x['paired_success']!=x['item_only_paired_success']]:
    chosen.append(('预定去句号敏感性：全部不一致案例',extra))
if len(chosen)<2:
    # Fulfil the user's two-complete-examples requirement even when the main panel has no failure.
    extra=[x for x in pairs if x['mode']=='paraphrase' and x['split']=='heldout' and x['paired_success']=='0']
    if extra:chosen.append(('自然改写失败（附加展示）',extra[0]))
    else:
        extra=[x for x in pairs if x['mode']=='main' and x['split']=='heldout' and int(x['planned_distance'])==128 and x['family']!=chosen[0][1]['family']]
        chosen.append(('第二组完整原文（附加展示）',extra[0]))
def case(pair,title):
    fam=pair['family'];d=pair['planned_distance'];mode=pair['mode'];f=families[fam]
    s=f"## {title}：{fam}，{f['A']} / {f['B']}，{mode}，计划d={d}\n\n"
    for gold in 'AB':
        key=f'{fam}_{mode}_{d}_{gold}';p=data[key];x=scores[key]
        s+=f"### 事实{gold}；正确答案{families[fam][gold]}\n\n```text\n{p['text']}\n```\n\n"
        s+=f"前缀320token；证据物品`{p['evidence_item']}`的全部token ID={p['evidence_token_ids']}、位置={p['evidence_token_positions']}；最后e={p['evidence_last_position']}；p={p['target_position']}、目标token ID={p['target_token_id']}。实际间隔d={p['actual_distance']}，两端都排除。完整前缀ID／offset见panel.jsonl中`{key}`。\n\n"
        s+=mdtable(['候选','完整token序列','逐token logprob','总分 nat','每token均分'],[[c['text'],c['token_ids'],[round(a,9) for a in c['token_logprobs']],f"{c['total_logprob']:.9f}",f"{c['mean_logprob']:.9f}"] for c in x['candidates']])
        s+=f"\n模型候选首选={x['choice']}；是否正确={x['correct']}；正确减错误={x['correct_margin']:.9f} nat。\n\n"
    s+=f"两事实均正确={pair['paired_success']}；A事实下正确边际={float(pair['margin_A']):.6f}，B事实下正确边际={float(pair['margin_B']):.6f}；无确定事实基线A减B={float(pair['baseline_A_minus_B']):.6f} nat。\n\n"
    return s
caseheader=f'''# 原文和原始分数

每组完整A/B前缀与所有候选token分数均保留。自然对数为单位nat，总分越高越偏好；每token均分不代替主判定。展示规则在评分前冻结：优先128首个成功、首个失败，若无再查64／16；另报首个诱饵失败。本轮不是自由生成测试。全部原始记录在{R/'data/panel.jsonl'}与results/*.jsonl。

'''
selected=caseheader+''.join(case(pair,title) for title,pair in chosen)
if not any(title=='失败配对' for title,pair in chosen):selected+='主实验留出没有失败配对；不虚构失败例。\n'
if not any(title=='成功配对' for title,pair in chosen):selected+='主实验留出没有成功配对；不虚构成功例。\n'
(C/'cases_selected_cn.md').write_text(selected)
allcases=caseheader+''.join(case(pair,'原始配对') for pair in pairs)
(R/'results/casebook_all_cn.md').write_text(allcases)
familyrows=[]
for fam in sorted({x['family'] for x in pairs if x['split']=='heldout'}):
    ps=[next(x for x in pairs if x['family']==fam and x['mode']=='main' and int(x['planned_distance'])==d) for d in [16,64,128]];fm=families[fam]
    familyrows.append([fam,fm['template'],fm['A']+' / '+fm['B']]+[f"{int(z['paired_success'])}; A={float(z['margin_A']):.3f}, B={float(z['margin_B']):.3f}" for z in ps])
(C/'families_cn.md').write_text('# 全部留出家族：每格为是否成对成功及A/B正确边际\n\n'+mdtable(['家族','模板','候选','d16','d64','d128'],familyrows)+'\n每格首位1要求A/B都正确；0表示至少一侧失败。边际单位nat，正为正确候选分高。原始全精度与基线见family_pairs.csv。\n')
num=', '.join(f"d{s['planned_distance']}:{s['paired_success']}/24" for s in main)
passed=[s['planned_distance'] for s in main if s['point_gate']];strong=[s['planned_distance'] for s in main if s['evidence_eligibility']=='CLEARS_BOUNDED_BEHAVIOR_GATE']
scope=f'主条件成对正确切换为{num}。数值80%门槛满足的距离：{passed or "无"}；按预定不确定性分支清楚跨过本轮行为关卡的距离：{strong or "无"}。'
baseline=mdtable(['名义槽位d','无事实时偏A/24','偏B/24','A减B平均分差,nat'],[[x['distance'],x['A_preferred'],x['B_preferred'],f"{x['mean_A_minus_B']:.4f}"] for x in res['baseline']])
itemdiff=sum(x['paired_success']!=x['item_only_paired_success'] for x in pairs if x['split']=='heldout' and x['mode']=='main')
summarycn=f'''# 近处与远处物品事实：首轮行为结果

模型在没有竞争物品的受控文本中，能随近处或远处的明示物品事实正确切换候选；近处加入另一容器的竞争物品时可靠性下降。{scope} 这是本轮构造英语任务的候选选择结果；是否进入下一步由研究者共同审阅决定，未自动执行SAE分析。

阅读路径：①行为与因素对照，见下表和[全部24家族](families_cn.md)；②表征与层组织，本轮NOT RUN；③功能干预，本轮NOT RUN，质量由token、完整评分和原始数值复核支持。正文给决定性数值；[详细方法](detailed_cn.md)、[完整成功／失败原文](cases_selected_cn.md)和执行侧完整casebook保留审计细节。

## 目的、模型和待检验行为
最终研究方向是不同距离的SAE组合。先确认模型确实随物品事实正确改变答案，才有相应行为可供之后研究。固定token的feature随上下文变化，只是表征响应，不能替代这项行为证据。旧R09测的是前一种对象。本轮不加载任何SAE。

复用官方Qwen3-0.6B Base、原tokenizer及原生前向／输出头，28层、隐藏维1024。28个英语家族中4个只做smoke，24个留出覆盖24个物品对、六类模板，每模板4家族。局部提问不列出选项。A/B配对只替换关键事实里的物品。答案前的前缀一律320token，最后位置p=319。

证据位置e取关键物品短语的最后一个token。距离d=p-e-1，只数两端之间的token。因此主条件d=16/64/128对应e=302/254/190，全部实测一致。移动同一批完整填充句，保持同一家族／模式的总长、提问和token多重集合。事实绝对位置和相对填充顺序同时变化；不能把差异全归于抽象距离。

行为假设是两个事实版本都选对；竞争解释包括固定候选先验、熟悉措辞与复制最近物品。完整候选为前导空格＋物品短语＋句号，分数逐token条件概率取自然对数后相加。所有配对长度一致，25对为2token、3对为3token。两边全对才记1，平分失败。常识或固定先验本身不能让同一对A/B都正确。正确标签是事实中实际写出的物品名称；cup/mug、book/notebook等有概念包含，因此本轮更直接测指定词面事实回忆，不把它写成开放描述中只有一个合理答案。

## 原始数据：主条件
{tbl}
正确率分母为48条A/B提示，但区间和统计以24家族为单位；它们不是48个独立样本。切换率用95%Wilson家族区间；平均分差是每家族两侧正确减错误后等权平均，区间为10000次家族重采样。六模板聚类敏感性另存在distance_summary.csv，不能把24个构造家族等同于自然语言随机总体。

![距离与成对正确切换](figures/distance_switch.png)
左图横轴为主条件实际间隔、纵轴为两个版本都答对的家族比例，误差线为家族Wilson区间；标明成功数／24。橙线为独立自然事实改写，近距实际16–18；红叉为128的近处错误物品诱饵，位置微移只为可见性。右图每行保留一个家族、每列一个主距离，1为两侧均正确，0为至少一侧失败。它不展示SAE或因果机制。

## 候选先验、自然改写和近处错误物品
无确定事实基线用object／small object代替可识别物品；没有正确答案，不计算其准确率。以下只显示候选先验偏好。主指标仍依据原始完整总分，不经基线校正。

{baseline}
长度匹配排除了本轮“一个候选多token”的明显差异，未排除词汇先验。删除句号后重新按物品部分评分，主留出72个家族×距离配对中{itemdiff}个配对的成功标签改变；详见family_pairs.csv。三组多token物品的逐token分数全部保留。

这一个不一致是F28的card／stamp、d64。stamp事实下，物品词分数为card −9.556379、stamp −9.757874，单看物品词偏card；加入各自句号条件分数−3.940424／−3.508816后，完整总分为−13.496803／−13.266689，转而偏stamp。于是去句号的主成对正确数为d16=24/24、d64=23/24、d128=24/24。原协议的含句号判定保持；这项敏感性说明完整候选成功不能全部归到答案前那个位置的物品首token读出。[完整敏感性原文](cases_selected_cn.md)保留两侧全部token分数。

自然改写预先固定，不按结果迭代。它与主条件的填充库存可能不同，因此若表现改变，不能单独归因于措辞；实际近距16–18也须一起保留：

{ptbl}
128条件的近处另一容器错误物品诱饵：成对正确{lure['paired_success']}/24，准确率{pct(lure['accuracy'])}，平均正确边际{lure['mean_margin']:.4f} nat。其A/B同时交换目标与诱饵，作为竞争诊断单列，不称为纯距离效应或单事实因果估计。[完整反例](cases_selected_cn.md)给出真实前文与原始分数。失败可与最近复制、容器绑定或干扰敏感性相容，当前诊断不能独自确定唯一原因。

## 可能原因与认识边界
原始A/B两侧和无事实先验必须一起看：一侧总是高分，可能来自词先验；两侧正确切换则说明当前事实改变参与了本任务的候选排序。若自然改写或诱饵比主任务弱，认识须限定在原措辞和干扰条件。本文只给这些可检验的可能原因，不把现象升级为内部机制。

可以得出的认识是当前冻结模型在这些明确任务条件下的事实利用程度及各距离是否达到首轮操作门槛。不能据这几个距离判断普遍长程能力，也不能从行为曲线推断哪个SAE成员负责存储、检索或组合。词面复制、对象绑定、词先验和填充顺序没有被全部识别。

门槛是研究者给定的80%点估计，证据资格按事先记录的保守区间分支另报。只在区间下界高于80%且覆盖完整时标为清楚通过；区间跨80%为证据不足；上界低于80%为当前任务未通过。附加结果不能挽救主指标。即使某个距离数值达标，也没有自动进入SAE。

## 位置与停止
[锚点](anchor_cn.md) · [冻结协议](protocol_cn.md) · [逐家族数据](families_cn.md) · [完整原文及原始候选分数](cases_selected_cn.md) · [实际产物索引](artifacts.md)。原始token／输出分数、脚本、配置在{R}；对话记忆在{SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md'}。

本轮已在完整行为交付处停止。科学接受、机制判断、是否以及如何进入下一步保持Unknown，等待研究者讨论。
'''
(C/'summary_cn.md').write_text(summarycn)
summaryen=f'''# Near and far object facts: first behavior round

The frozen model correctly switches candidates with explicit near and far object facts in the main records; reliability falls when a competing object fact is introduced nearby. Main heldout paired success: {num}. Numerical80%threshold satisfied at {passed}; the frozen uncertainty rule clearly clears the bounded behavior gate at {strong}. These are complete-sequence candidate rankings for constructed English records, not unrestricted generation or general memory. No SAE, training or activation intervention ran. The researcher owns the next decision after reviewing raw data.

Reading paths:1behavior and factor controls;2representations/layer organization NOT RUN;3functional intervention NOT RUN, measurement quality audited separately. The complete [Chinese Summary](summary_cn.md), [Detailed](detailed.md), [all families](families_cn.md) and [full original cases](cases_selected_cn.md) preserve the same observations and boundaries.

Purpose: verify the behavioral prerequisite before studying SAE combinations. A feature changing at a fixed token does not establish successful downstream fact use; R09's distance response is a different observable. Frozen official Qwen3-0.6B Base, original tokenizer/native output head,28layers/hidden1024,FP32CPU2threads. Four smoke families precede24heldout families,24pairs/six heldout template strata. Main paired prefixes change only one object; question bytes are identical, candidates absent from question/filler. Prefix320tokens,p319; gap=p-e-1 excludes both endpoints, taking the item's LAST token. Exact main16/64/128=e302/254/190. Same filler inventory and token multiset move around the fact; absolute fact position/order co-vary with distance.

Hypothesis: both A and B fact versions select their respective correct candidates. Fixed prior is a rival; neutral-item baseline measures it. Natural fact paraphrase and recent wrong-item foil bound wording and nearest-copying alternatives. Score the complete leading-space noun phrase plus period by summing teacher-forced token logprobs. All within-pair lengths match (25 two-token,3 three-token pairs). Equal lengths do not eliminate lexical priors. Gold is the literal noun phrase stated in the fact; overlapping categories such as cup/mug or book/notebook make this a stated-word recall test rather than a claim that unrestricted descriptions have only one semantically valid answer. Ties fail; family is the analysis unit. Main data:

{tbl}
![Behavior and all family outcomes](figures/distance_switch.png)
Left: paired correctness and95%familyWilson interval; numbers are successful families/24. Orange is a separate fact paraphrase, near actual16–18; foil is separately shown at128. Right: every heldout family's0/1main outcome, never averaged away. Mean margin intervals use10000paired-family resamples; template-cluster sensitivity remains in the CSV. Constructed families are not random natural-language samples.

No-identifiable-fact preference:

{baseline}
Natural paraphrase is a predeclared separate condition. Its filler inventory may also differ from main, so between-mode performance changes cannot be assigned to wording alone; actual near gaps16–18 remain explicit:

{ptbl}
Recent wrong-item foil at128: paired{lure['paired_success']}/24; accuracy{pct(lure['accuracy'])}; mean correct margin{lure['mean_margin']:.4f}nat. Both target and opposite foil change across A/B, so this is diagnostic rather than a single-fact causal treatment. Main item-only scoring changes{itemdiff}/72pair labels versus complete scoring. All token scores retained.

The sole changed pair is F28 card/stamp at64. Under the stamp fact, item-only card/stamp scores are−9.556379/−9.757874; adding period scores−3.940424/−3.508816 yields full totals−13.496803/−13.266689 and changes preference to stamp. Item-only paired successes are24/24,23/24,24/24 at16/64/128. The frozen full-answer verdict is preserved, but it cannot all be assigned to the answer-start token's object-word readout. The complete sensitivity example is retained.

Interpretation: a correct paired switch shows that changed fact content controls candidate ordering in that condition; a one-sided success can reflect prior. Wording/foil failures limit the usable condition. They are compatible with copying, binding or interference explanations and do not select an internal mechanism. This round can describe bounded factual behavior, not universal memory, arbitrary relation understanding, feature semantics or router usefulness.

The80%point gate and uncertainty sufficiency are separate. A Wilson interval crossing80%means insufficient stable eligibility; an upper bound below80%means the current task fails; lower bound above80%with full coverage clears this bounded gate. These are first-round operational decisions, not a universal ability criterion or SAE permission. Complete raw inputs/scores/config/code are indexed in[artifacts](artifacts.md); independent arithmetic/token checks are reproducible. Execution is complete and STOPPED for researcher discussion. Scientific acceptance/closure and further execution remainUnknown.
'''
(C/'summary.md').write_text(summaryen)
sm=json.load(open(R/'evidence/smoke_complete.json'));he=json.load(open(R/'evidence/heldout_complete.json'));ve=json.load(open(R/'evidence/verification.json'))
detail=f'''# Detailed behavior record

Purpose: with identical local question, test correct answer switching after a remote object fact changes. [Anchor](anchor.md), original[Protocol](protocol.md),[Summary](summary.md). Frozen Protocol body unchanged; all444prefixes retained. Eligibility: engineered/constructed-stimulus behavior with paired family statistics. Scientific acceptanceUnknown. No missing condition and no outcome-based exclusions.

## Actual procedure and why controls matter
Each record has a header, irrelevant weather/time sentences, exactly one target container fact, more of the same filler inventory, then a question without candidates. Split the filler into blocks so moving the fact yields exact gaps16/64/128while preserving320prefix length and the token multiset. Offset-derived evidence location uses whole item phrases, avoiding “cord” matching in “According”. A/B prefixes are identical outside the item. The output head separately scores every token of each hypothetical noun-phrase-plus-period completion. A score is a log probability, not an activation. Positive correct-minus-wrong margin means candidate ranking is correct; two positive margins are necessary for a paired success.

Neutral baseline replaces item identity withobject/small object and has no correctness label. Paraphrase restates the fact with a different grammatical order while leaving the family question; some near actual gaps are17/18because the item appears earlier in the fact. Other-container foil deliberately introduces the opposite candidate near the question at128and swaps it with target identity acrossA/B. Main/auxiliary inventories can differ, so mode contrasts are not pure wording interventions. No extra template round was attempted.

## Provenance, freezes and execution
Raw panel SHA256={cfg['panel_sha256']}; family metadata SHA256={cfg['family_sha256']}. Model/tokenizer config and full weights SHA are in config.json. Full model hash verified before and after both stages. Tokenizer source{MODEL/'tokenizer.json'}, no chat wrapping/special tokens. RuntimeTorch={sm.get('torch','2.3.0a0+6ddf5cf85e.nv24.04')}andTransformers4.53.3from mounted dependency directory. LocalCPU2threads,FP32,SDPA,physical2x328shape,zero gradients/optimizers. No cloudjob, no GPU allocation; job IDNOT_APPLICABLE. Smoke36prefixes took{sm['seconds']:.2f}s; heldout408took{he['seconds']:.2f}s. Fixed320target sampling throughout. Public full-forward token-score and prefix-only checks are in stage receipts; no precision tolerance changed.

Development construction failed once when substring “cord” matched inside “According”; repaired with whole-word regex before saved panel/freeze/forward. Old source retained in versions. Main data and scoring rules were unchanged after freeze. No Protocol amendment was needed during inference. Additional analysis implementation was hashed before heldout model start; statistical rules were already frozen inProtocol. Later report formatting is not response selection.

## Complete results and uncertainty
{tbl}
{ptbl}
Foil128 paired{lure['paired_success']}/24. Full repeated-family table: tables/family_pairs.csv,180pairs including84main/72paraphrase/24foil; baseline84rowsseparate. Token_scores.csvretains every candidate token. All24heldout main families appear in[families](families_cn.md). FamilyWilson binary intervals and paired bootstrap margins at10000replicatesseed20261104; template-cluster sensitivity resamples six whole template groups. Same-family distances remain paired in paired_distance_changes.csv; no distance-as-independent error bars or multiple-comparison significance claim. Means and every value survive negative outcomes.

## Evidence ledger and quality
Implementation/measurement audit: {ve['checks']}checksPASS, recomputed with separate token/arithmetic implementation by the same agent; not independent human/scientific review. Every original text retokenized; prefix/candidate ID alignment, whole-item span,last evidence endpoint,p319,gap arithmetic,all token-score sums,invariance/leakage,split disjointness,pair success,margins,aggregate means andWilson interval recomputed. Frozen source/input hashes checked. Public model-forward numerical agreement is separately measured, not inferred from sum identities. Full output-head distribution was not saved; top10first-token IDs/logprobs plus complete candidate scoring were saved. No claim of rendered math verification; source check is separate.

Coverage: assets/definitions/data/smoke/all main distances/neutral baseline/paraphrases/nearest foil/full family data/figure/raw cases/scoring code/config allDONE_VALIDas execution artifacts. Representations/training/activation interventionsNOT_RUN_BY_PROTOCOL. Operational failure to meet a behavior gate does not make its measurements invalid. All scientific next decisions remain pending.

## Raw artifacts and continuation
{R/'data/panel.jsonl'} full actual texts/IDs/offsets. {R/'results/smoke.jsonl'} andheldout.jsonlraw scores. {R/'results/casebook_all_cn.md'} every complete paired original. [Artifact index](artifacts.md) lists code/config/manifests/current receipts. Canonical source remains project-side; frozen execution copies are evidence, not competing editable Protocols. All further SAE activity requires discussion; STOP.
'''
(C/'detailed.md').write_text(detail)
(C/'detailed_cn.md').write_text(f'''# 完整执行说明

问题：局部提问相同，仅改变前文关键物品时，模型能否在不同实际token距离都正确切换？本轮全部444前缀完成，无剔除、无重新改模板。正式科学判断仍待研究者。

## 实际计算及对照含义
记录由标题、无关天气／时间句、一个容器事实、同批无关句和提问组成。把事实插入填充库存的不同位置，保持320token、目标p319与词元多重集合不变，主距离真实16/64/128。物品按完整词匹配，再依据tokenizer偏移取最后token；不能用字符数。A/B在关键物品之外字节相同。

每个候选为“空格＋物品＋句号”。逐token将其前缀送入冻结原模型，取对应条件自然对数概率并求和。主指标要求A事实答A、B事实答B。准确率另按家族两侧平均；正确减错误的分数差不替代成对切换。

无确定事实基线不知道物品身份，只观察先验偏好。自然改写将物品放到句内不同语法位置，因此近距真实16–18单列。近处错误物品写在另一容器事实中，仅在128测；A/B还同步交换诱饵，故只作竞争解释诊断。模式间填充库存不必相同，不能把差异全归于改写因素。

## 实际数量和结果
{tbl}
自然改写：

{ptbl}
诱饵128成对{lure['paired_success']}/24。28家族＝4smoke＋24留出；留出24对物品、6模板。180完整配对＝84主＋72改写＋24诱饵；另84无事实基线。每个候选每个token的分数全部保存。smoke36前缀用时{sm['seconds']:.2f}秒，留出408前缀用时{he['seconds']:.2f}秒；无云作业、未申请GPU，job ID不适用。

## 复用、冻结与偏差
复用官方模型／tokenizer以及S06CPU原生前向和完整序列评分，去掉SAE hook。FP32，CPU2线程，固定2×328形状。模型／tokenizer完整哈希在两阶段前后均一致，无可训练参数、优化器或模型／SAE训练。源代码、输入和协议冻结收据见evidence/freeze.json；统计实现代码另在留出前哈希。未改原始协议正文。

前向前生成阶段曾把cord定位到According内，未生成完整数据即失败；改用完整词边界，重查全体，没有删除家族、观察响应或调统计阈值。旧脚本在versions。前向期间无科学协议更改。完整公开前向逐token与评分器最大误差见smoke_complete；因果前缀状态一致，所有检查维持预定容差。

## 统计、质量与边界
家族为主单位，A/B和跨距离不当独立样本。二值成对切换给95%Wilson；分差10000次家族bootstrap，种子20261104；另给六模板整组重采样。24个构造家族不等于自然语料随机总体。跨距离配对变化见paired_distance_changes.csv。没有显著性筛选或只报最好点。去句号敏感性改变主留出{itemdiff}/72个配对的成功标签。

独立算式／token实现由同一处理agent复核{ve['checks']}项PASS，不冒充独立研究者审核。逐条重新分词、检查全部候选链、token逐分总和、端点／间隔、只改物品、词元多重集合、泄漏、模板划分、每对正确性／边际、各汇总和Wilson公式。质量校验不是机制发现。未保存完整词表分布，只保存候选完整分数和答案前top10。

所有行为、对照、图、原始案例、配置和代码执行交付DONE_VALID；表征、训练、激活干预NOT_RUN_BY_PROTOCOL。行为门槛失败仍是有效测量结果。科学接受、机制归因和下一轮授权Unknown。

## 证据位置与停止
[逐家族](families_cn.md) · [成功／失败完整原文及分数](cases_selected_cn.md) · [实际数据／代码索引](artifacts.md)。完整180配对原文在{R/'results/casebook_all_cn.md'}；token化数据在data/panel.jsonl；原始输出results/smoke.jsonl与heldout.jsonl。全部英文合同、哈希、环境与复核详见[detailed.md](detailed.md)。完成后停止，与研究者共同判断下一步；不自动进入SAE。
''')
artifacts=f'''# Actual artifacts

Canonical owner: {C}; sole[Anchor](anchor.md) with[Chinese companion](anchor_cn.md),[Protocol](protocol.md),[中文](protocol_cn.md),[Summary](summary.md),[中文](summary_cn.md),[Detailed](detailed.md),[中文](detailed_cn.md).

| Artifact | Actual absolute location | Role |
|---|---|---|
| Full actual text/token IDs/offsets/candidates | {R/'data/panel.jsonl'} |444prefixes, exact evidence/target/gap |
| Families/splits | {R/'data/families.json'} |28families, smoke vs heldout |
| Templates/filler | {R/'data/templates.json'} |all literal construction rules |
| Raw complete scores | {R/'results/smoke.jsonl'}; {R/'results/heldout.jsonl'} |all candidate token/sum scores |
| Per-token flat table | {R/'tables/token_scores.csv'} |auditable scoring |
| All paired families | {R/'tables/family_pairs.csv'} |both directions separately |
| Distance/controls/intervals | {R/'tables/distance_summary.csv'} |registered operational gate |
| No-fact baseline | {R/'tables/baseline.csv'} |all candidate priors |
| All complete original pairs | {R/'results/casebook_all_cn.md'} |180paired cases |
| Scoring | {R/'code/run.py'} |native complete candidate chain |
| Construction/analysis/replay | {R/'code'} |prepare.py,analyze.py,verify.py,report.py |
| Frozen config | {R/'config.json'} |model,hashes,seed,precision,shape |
| Freeze and numerical checks | {R/'evidence'} |freeze,smoke,heldout,verification |
| Figure | {C/'figures/distance_switch.png'} |actual gap vs family rate and all family outcomes |
| Conversation memory | {SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md'} |append-only operational context |

No model/SAE weights, full output distributions or hidden representations copied. Execution raw outputs stay execution-side. Selected small tables/figure are project evidence copies with a payload manifest. Scripts mirror actual executed source; the scientific owner remains the project. No commit,push or external publication.
'''
(C/'artifacts.md').write_text(artifacts)
for sub in ['code','figures','evidence','tables']:(C/sub).mkdir(exist_ok=True)
for p in (R/'code').glob('*.py'):shutil.copy(p,C/'code'/p.name)
for p in (R/'figures').glob('*'):shutil.copy(p,C/'figures'/p.name)
for name in ['distance_summary.csv','family_pairs.csv','baseline_summary.csv','template_summary.csv','paired_distance_changes.csv']:shutil.copy(R/'tables'/name,C/'tables'/name)
for name in ['freeze.json','input_access.json','smoke_complete.json','heldout_complete.json','verification.json','analysis_code_frozen.json','referenced_chats_read.json','construction.json','pre_run_audits.json']:shutil.copy(R/'evidence'/name,C/'evidence'/name)
shutil.copy(R/'config.json',C/'config.json')
dump(C/'payload_manifest.json',dict(UTC=now(),purpose='selected small behavioral evidence and provenance; raw remains execution-side',execution_root=str(R),files={str(p.relative_to(C)):dict(source=str(R/p.relative_to(C)),sha256=sha(p),bytes=p.stat().st_size) for sub in ['figures','tables','evidence'] for p in sorted((C/sub).glob('*')) if p.is_file()},scientific_acceptance='Unknown',external_publication=False))
dump(R/'results/display_selection.json',dict(rule='prefrozen first successful/failed family at128 then64then16; separate first foil failure',selected=[dict(title=title,family=p['family'],mode=p['mode'],distance=p['planned_distance']) for title,p in chosen]))
print(scope)
