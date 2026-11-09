from common import *
import numpy as np,shutil,itertools
assert not (R/'frozen_plan.json').exists()
assert json.load(open(MAIN/'evidence/verification.json'))['status']=='PASS'
assert (MAIN/'evidence/final_delivery.json').exists() and (MAIN/'evidence/completed.json').exists()
for n in ['data','cache','results','figures','evidence','versions']: (R/n).mkdir(exist_ok=True)
C.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(20261104)
plan0=json.load(open(MAIN/'frozen_plan.json'));dis=np.load(MAIN/'cache/discovery.npz');allpp=rows(MAIN/'data/panel.jsonl');byid={p['id']:p for p in allpp};ps=[byid[str(a)] for a in dis['ids']];lookup={(p['family'],p['label']):i for i,p in enumerate(ps)};oldsel=json.load(open(MAIN/'results/selection.json'))['sites'];selection={};audit=[]
for s in SITES:
 z=dis[s+'__z'].astype(float);freq=(z>0).mean(0);counts=(z>0).sum(0);meanpos=np.divide(z.sum(0),counts,out=np.zeros(30000),where=counts>0);selection[s]={}
 for d,labels in DOMAINS.items():
  ss=oldsel[s][d];groups={'common':ss['H2']}
  groups.update({name:ids[:3] for name,ids in ss['events'].items() if ids})
  excluded=set(a for ids in groups.values() for a in ids);controls={}
  for name,ids in groups.items():
   chosen=[];details=[]
   for a in ids:
    pool=np.array([j for j in np.flatnonzero(counts>0) if j not in excluded and j not in chosen]);assert len(pool)
    intensity=np.maximum(meanpos[pool],1e-12)/max(meanpos[a],1e-12);quality=(abs(counts[pool]-counts[a])<=2)&(intensity>=.5)&(intensity<=2)
    distance=abs(freq[pool]-freq[a])+abs(np.log(intensity))*.5;eligible=pool[quality];j=int(eligible[np.argmin(distance[quality])]) if len(eligible) else int(pool[np.argmin(distance)])
    matched=bool(abs(counts[j]-counts[a])<=2 and .5<=meanpos[j]/meanpos[a]<=2);chosen.append(j);details.append(dict(candidate=a,control=j,candidate_frequency=float(freq[a]),control_frequency=float(freq[j]),candidate_positive_mean=float(meanpos[a]),control_positive_mean=float(meanpos[j]),qualified=matched))
   controls[name]=dict(ids=chosen,qualified=all(x['qualified'] for x in details),matches=details)
  def patterns(ids):
   out={};ranges={}
   for l in labels[1:]:
    a=z[[lookup[(f'F{i:02d}',l)] for i in range(1,9)]][:,ids];n=np.linalg.norm(a,axis=1,keepdims=True);q=np.divide(a,n,out=np.zeros_like(a),where=n>0);m=q.mean(0);m=m/np.linalg.norm(m) if np.linalg.norm(m)>0 else m
    out[l]=m.tolist();ranges[l]=dict(min=a.min(0).tolist(),max=a.max(0).tolist(),min_norm=float(n.min()),max_norm=float(n.max()))
   return out,ranges
  typ,ranges=patterns(groups['common']);other,other_ranges=patterns(controls['common']['ids'])
  selection[s][d]=dict(groups=groups,matched_controls=controls,typical=typ,discovery_ranges=ranges,other_typical=other,other_discovery_ranges=other_ranges,component_shuffle=np.roll(np.arange(len(groups['common'])),1).tolist(),selection_source='Only original64explicit discovery rows and frozen S06 selection; no use of S06 heldout scores to choose IDs.',frequencies_denominator=64)
  for name,ids in groups.items():audit.append(dict(site=s,domain=d,group=name,ids=json.dumps(ids),controls=json.dumps(controls[name]['ids']),frequency_intensity_match=controls[name]['qualified']))
# Exactly64explicit heldout prefixes (fine,parent,negative) plus32property fine prefixes, untouched main strings.
panel=[p for p in allpp if p['split']=='heldout' and (p['wording']=='explicit' or p['wording']=='property' and p['level']=='child')]
assert len(panel)==96;jsonl(R/'data/panel.jsonl',panel);dump(R/'data/selection.json',selection);table(R/'data/candidate_match_audit.csv',audit)
shutil.copy2('/tmp/S07_input_assets.json',R/'evidence/input_access.json');shutil.copy2(MAIN/'evidence/final_delivery.json',R/'evidence/main_delivery_before_S07.json')
protected={str(p):sha(p) for p in MAIN.rglob('*') if p.is_file() and '__pycache__' not in p.parts};dump(R/'evidence/main_immutable_before.json',protected)
for p,h in plan0['input_SHA256'].items():assert sha(p)==h
plan=dict(UTC=now(),authorization='Current follow-up user request explicitly authorizes temporary SAE feature deletion/strength interventions after complete saved main experiment; no training or permanent weights edits.',main=str(MAIN),main_package=json.load(open(MAIN/'evidence/final_delivery.json')),model=plan0['model'],input_SHA256=plan0['input_SHA256'],sites=plan0['sites'],panel_sha256=sha(R/'data/panel.jsonl'),selection_sha256=sha(R/'data/selection.json'),rows=96,seed=20261104,device='CPU',threads=2,capture_shape=[4,128],tail_batch=32,
           interventions='Native hook h_new=h_original+W_decoder*(z_new-z_original), decoder bias cancels; preserve original reconstruction residual. Only last prefix colon at block27, not other positions or layers.',
           groups='Exact main discovery H2 common list; each nonempty recruited/lost list first3 in its original discovery ranking. Empty lists stay unavailable. Per-domain/site independent.',
           deletion='Zero selected z coordinates. Match baseline: same-size frozen other-feature list selected in discovery by frequency(+/-2/64) and positive-mean intensity ratio[.5,2], or closest unqualified list with full discrepancy reporting. Additional exact representation-norm random positive-combination addition on noncandidate currently active coordinates; separate operation, not a claimed deletion match.',
           swap='For each destination child and alpha in[.25,.5,1], w=(1-alpha)*v/r+alpha*t_destination; v_new=r*w/||w||2; r=||v||2. Typical t=unit-normalized mean of8discovery per-row unit vectors. Other features unchanged, nonnegative. Mark support changes if an originallyzero member is recruited. alpha0 is identity.',
           controls='Same-member component-shuffled destination typical pattern, matching actual decoder-space perturbation norm via deterministic65grid and20bisection on beta in[0,1]. Own-side typical pattern control similarly norm-matched where feasible. Other frozen frequency/intensity-nearest members with their discovery typical patterns, similarly norm-matched. Exact match tolerance10%; report failures, no output-based beta tuning. Random deletion-norm combination draw uses independent seed and active noncandidate members, positive additions normalized in representation space.',
           primary='8 explicit tests:2sites x2domains x(deletion common;strength opposite alpha.5). Family-mean correct-sibling-margin loss, candidate minus comparator; deletion comparator is discovery matched list only if qualified and per-text active count equal; strength comparator shuffled same-members only if decoder norm ratio within10% and original support retained. Need>=6/8 eligible template clusters; exact family sign flips, Holm .05 and4096family bootstrap intervals. Also report raw intervention-vs-baseline effects, classwise and all norm/count controls independently. Replacement groups,alpha sweep,property and offdomain checks are secondary, not rescue tests.',
           outputs='All4complete candidate scores including period; correct sibling margin/counts; full-vocabulary first-token ranks/probabilities,top20token probabilities/tail mass,entropy,KL vs baseline, and four-candidate normalized probabilities. Full vocabulary rank is not constrained4candidate rank. No generated examples substituted for scores.',
           tail='Because edits occur after final block27 attention, final-layer prefix edits cannot affect candidate-position hidden states/period scores: their K/V use pre-edit final-block inputs, and no later attention layer exists. ATT delta: r_after_attn=block_input+attn_output+delta, output=r_after_attn+MLP(RMSNorm(r_after_attn)); MLPIN delta: output=r_after_attn+MLP(original_MLP_input+delta). Apply finalRMSNorm/head. This is exact architecture-specific computation, not a linear approximation. Validate complete-hook forwards against cached-tail full candidate scores,zero/noop before scaling up; tolerance1e-4FP32, otherwise full forward fallback with same scope.',
           ranking='Compute each candidate first-word rank=1+number vocabulary logits strictly greater; tie rank recorded implicitly. p_vocab uses full vocabulary softmax; p_four uses logsoftmax over4complete sequence scores. Save top20 strings/IDs/probabilities, tail mass, entropy and distribution shift. No need to save multi-GB full logits.',
           calibration='F09 cat and car, both sites: identity, common deletion,alpha.5opposite; full hooked4candidate call vs cached tail. Native baseline for every96prefix must replay S06 within1e-4. Actual decoder norms/bias and injected norms retained.',
           stop='Complete all feasible groups, preserve unavailable/zero/ineligible cases, audit, figures and bounded AI effect update, package with main<20MB. No router, checkpoint update or automatic unbounded follow-up.',scientific_acceptance='Unknown')
dump(R/'frozen_plan.json',plan)
protocol='''# S07 Protocol: residual-preserving feature-combination interventions

## Purpose and authorization

The current follow-up explicitly authorizes this supplement after the complete main S06 experiment. S06 raw files, results, scripts, selected candidates and3.96MBpackage are frozen and preserved. Test whether perturbing candidate combinations changes native candidate-answer tendencies relative to matched interventions. Existing Anchors15_27_06/07 retain scientific ownership; original and observational hypotheses are not rewritten.

## Objects and exact injection

For each native SAE site separately, original code z and original hidden h are frozen observations. Decoder is b+Wz with columns W[:,i]. Change only chosen coordinates to z'. Inject h'=h+W(z'-z), using no decoder bias in the change. Then h'=(b+Wz')+(h-b-Wz), so the original reconstruction residual remains exactly. Columns are used at their actual stored scale; no renormalization. Both hidden tensors have width1024, dictionaries30000/ReLU-Top32. Attention output is block27.o_proj before residual addition. MLP input is after residual and post_attention_layernorm; do not confuse sites or add another RMSNorm there. All parameters remain frozen.

## Candidate, text and control freeze

Exact selection and every discovery intensity/frequency are in data/selection.json and candidate_match_audit.csv, frozen before intervention responses. Common lists are the original explicit-discovery H2 lists; nonempty recruit/loss groups use the first3original ranked members. Nothing is selected on main heldout success. Typical child patterns average the8discovery normalized common vectors, then normalize this mean. Main96unchanged heldout prefixes=64explicit(all8labels) plus32property fine. The explicit32fine prefixes determine target effects; offdomain/parent/negative rows expose generalized output shifts. Property failure cases remain descriptive.

Delete: set group z to zero, all other members unchanged. Control1 deletes a same-size other-member list selected on discovery frequency count±2/64 and positive intensity ratio[.5,2]. If none exists use the deterministic closest list but mark unqualified; this cannot establish specificity. Report actual active deletions and injected norm for every row. Control2 uses a same-active-count positive random combination on other active coordinates, scaled to exact representation norm; it is an addition/random-direction norm control, not a deletion matching claim. Count and norm controls answer different rivals.

Strength: for v=z_common, r=L2(v), source q=v/r and destination typical t, interpolate w=(1-alpha)q+alpha*t; set v'=r*w/L2(w). Alpha0,.25,.5,1pre-fixed. r=0is a zero intervention/ineligible, not a rescued new list. v'>=0; all original positives remain positive, but original zeros can become positive and are separately labeled identity-changing. The rest of z stays fixed. Record every old/new coordinate, feature ID, original/changed raw norm and whether values exceed combined discovery child min/max.

Strength controls: use the same members and a fixed cyclic permutation of destination typical coordinates (component-shuffled discovery pattern), and the own-side typical pattern; additionally intervene on other discovery-matched members using their typical patterns. Match their decoder-space norm to the candidate condition using a fixed65-point beta grid, then20bisection when a crossing exists, beta in[0,1]. Matching uses measured representations only, never scores; norm ratio outside.9–1.1is explicitly unmatched. No output-driven direction/strength selection. For parents/offdomain texts apply both destination patterns; primary in-domain child edit moves toward the opposite child, a controlled label-conditioned edit rather than an automatic router.

## Reading model scores and distributions

Same exact suffix and complete four2token candidates as S06, summed log conditional probabilities including period, no calibration. Report old/new scores, correct-sibling margin, correctness, first-word full-vocabulary ranks/probabilities, full top20token strings/probabilities plus remaining mass, entropy and KL from original distribution, and normalized four-complete-candidate probabilities. Candidate-set probabilities and full-vocabulary probabilities have different denominators. No causal claim from rank alone.

Last-block specialization: at only the final-prefix colon, a block27output/MLP edit cannot change hidden states at later candidate positions within this forward because there is no later attention layer. Their final-layer keys/values are formed before the edit. Thus complete period scores are invariant under this intervention; the first-word logits change. Cache the exact block27input, attention output and actual MLP input and recompute the nonlinear frozen tail and final head. This retains all downstream computation, not first-order attribution. Full-hook forwards on preselectedF09cat/car, both sites, identity/deletion/alpha.5must agree within1e-4FP32 for all4complete scores; native baselines on96prefixes replay main. If equivalence fails, use full forward rather than loosening tolerance.

## Judgments and uncertainty

Primary8comparisons:2SAEs×2domains×(common deletion and opposite-patternalpha.5), explicit heldout families only. Unit=family mean over the two children. Positive effect is loss of original correct-vs-sibling log-score margin; compare candidate loss with qualified matched deletion or norm-matched same-member shuffle. Need>=6/8 eligible families,4096family bootstrap95% interval, exact sign-swap p and Holm.05across8. All replacement groups, otheralphas,property,per-class/offdomain and distributions are reported as secondary/exploratory. If candidate and random effects are similar, no targeted specificity. If matching/active support is inadequate, specificity insufficient even if an intervention changes logits. Broad offdomain/KL shifts limit a semantic-directed interpretation. Opposite or negligible effects weaken the candidate's proposed local role without proving global irrelevance. Repeated score effect supports only these directions under this model/site/position/strength, not uniqueness, a true concept conversion or MoE expert dispatch.

## Execution and artifacts

Main completion receipt and all main hashes saved first. CPU2threads,4x128capture,32-lane tail batches; no GPU/cloud job, training or permanent checkpoint writes. Scientific/data/numerical audits precede effects. Preserve amendment history if needed. Save per-condition latent edits, actual hidden deltas/norms, all scores/ranks/distribution summaries, controls, family tables, counterexamples, at least2figures and bilingual reports. Package main+supplement<20,000,000bytes; weights/full logits omitted with exact index. Stop after scoped delivery. Researcher scientific acceptance and closure Unknown.
'''
(R/'protocol.md').write_text(protocol)
(R/'protocol_cn.md').write_text('''# S07干预协议（中文阅读）

主实验已完成并保存后，按用户追加授权启动本补充。保留主实验全部原文、候选、缓存、结果和独立包。

分别在两原生hook注入：h新=h原+Wdecoder(z新−z原)，不含decoder偏置，保留原残差。删除固定组只将对应z置零；共同成员强弱采用发现8家族各自L2归一化后平均、再单位化的典型模式。固定alpha=0/.25/.5/1；v新=r[(1−alpha)v/r+alpha t]/该括号L2范数，r=原固定列表L2。非负，原成员消失／新增均单列。

候选仅使用主发现集名单：完整H2共同组及每个非空换入／换出列表的原排序前3个；不按留出成功重筛。64条显式留出(包含父／负类／跨大类)+32条属性细类，原文不改。删除对照为发现频率±2/64且正激活均值比[.5,2]匹配的同数成员；匹配不到则报最近但不合格，不冒充匹配。另加其他活跃成员随机正组合，匹配实际表征扰动范数，这是加法方向对照而非同类删除。强弱对照含相同成员打乱典型模式、同侧典型模式、其他匹配成员，65点网格+20次二分只按扰动量匹配，不用输出挑方向。

同一四个2token完整候选全部计分含句号。报告正确候选对兄弟差、逐文本正确数、原始/干预分数、全词表首词排名/概率、top20及剩余质量、熵/KL，以及四完整候选归一化分布。两种概率分母分开。最后一层在冒号处的修改不改变候选位置的句号分数，使用精确末层非线性重算；预选F09猫/汽车、两hook、无改动/删除/alpha.5完整前向验证，1e-4不通过就全前向，不放宽阈值。

主判断8项=两SAE×两域×共同删除/alpha.5反侧强弱。按8家族两子类均值计算候选正确边际损失减合格对照，至少6家族、4096bootstrap95%区间、精确家族符号置换及Holm.05。具体干预有效、匹配特异作用和语义定向作用分开判断。匹配/共同支持不足记证据不足；广泛无关词变化限制语义定向解释；不能证明唯一机制或真实router分工。其余剂量／换入换出组／属性／跨域作为补充分析，不救主检验。

CPU2线程、采样4×128、末层批32。不训练、不永久改checkpoint。先freeze和三份审核，再效果。输出完整记录、至少两图、中英结果和与主实验合并的小于20MB包。主协议英文与frozen_plan.json提供完整定义。科研接受、关闭仍Unknown。
''')
audit_text='''# Reasoning audit: actual role of SAE combination directions

Main observations established conditional coordinate patterns, not native use. The missing empirical arrow is edited hidden-state contribution→native output score. The requested residual-preserving decoder delta directly tests that arrow; replacing h by a reconstruction would introduce an unnecessary reconstruction confound and is rejected. The algebra preserving residual is exact; the downstream logits require empirical intervention.

The actual final-block source was inspected. Attention-output and normalizedMLP-input edits have different downstream maps; each will be recomputed separately. Final-token tail reuse is valid only at block27after attention with no later attention, and must agree with full-hook forwards before use. It is not a model of arbitrary layers or multi-position edits. Full two-token sequence scores remain the observable, including the invariant period term.

Rivals: arbitrary equal-norm hidden perturbations, mismatch of active deletion count/strength, generic logit shifts, intervention out of discovery range, incomplete common support, and lexical-answer copying. Frozen discovery matched-list and same-list shuffled-pattern controls discriminate some of them. Failure of strict matching remains an identification gap rather than a reason to fabricate controls or abandon feasible interventions. Classwise/crossdomain/rank-distribution readouts separate movement of target preference from general distribution damage. No candidate is selected on S06heldout results, although those observational results are already visible; this is a prospective intervention test on observation-exposed but intervention-unseen families, not entirely blind semantic confirmation.

Permissible update: a repeated controlled score effect establishes functional sensitivity to these injected SAE directions at this interface/position. It cannot establish unique natural mechanisms, a genuine concept replacement, learning benefit or expert routing. All judgement wording is AI operational interpretation, researcher acceptance Unknown.
'''
(R/'evidence/reasoning_audit.md').write_text(audit_text)
(R/'evidence/audit_data.md').write_text('# Data/statistics\n\nOnly64explicit discovery for IDs/typicals/matching. Same96untouched heldout prefixes;8templateclusters. Observation-exposed, intervention-unseen. Eight primary Holm tests; ineligibility and matching failures retained. No output-based selection.\n')
(R/'evidence/audit_implementation.md').write_text('# Numerics\n\nFrozen CPUFP32, exact decoder linear delta/bias cancellation and nonlinear tail. Original residual maintained. Native full-forward calibration mandatory1e-4. Tokenizer/shape/period invariant checked. Trainable parameters0; training telemetry not applicable.\n')
shutil.copy2(R/'protocol.md',C/'protocol.md');shutil.copy2(R/'protocol_cn.md',C/'protocol_cn.md')
ar=SYS/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
for stem in ['15_27_06_common_members_extra_responses_anchor','15_27_07_conditional_relative_strength_anchor']:
 for cn in [False,True]:
  p=ar/(stem+('_cn' if cn else '')+'.md');text=p.read_text();shutil.copy2(p,R/'versions'/p.name)
  para=f'\n### S07 intervention supplement, authorized2026-11-04\n\nAfter completed/saved S06, the researcher authorizes temporary deletion and relative-pattern edits on discovery-frozen nativeSAE combinations. Inject original h plus decoder linear delta, retaining reconstruction residual. Compare frozen count/frequency/intensity controls and measured norm controls, then native full-candidate scores, vocabulary ranks/distributions and offdomain effects on original heldout families. This tests local functional sensitivity, not uniqueness or a concept conversion. [Exact S07 Protocol]({C}/protocol.md). NOT RUN at scope freeze; scientific acceptanceUnknown.\n'
  p.write_text(text.replace('\n## 6.',para+'\n## 6.',1))
dump(R/'evidence/protocol_freeze.json',dict(UTC=now(),state='APPROVED_FOR_S07_BY_DIRECT_USER_REQUEST',hashes={str(p):sha(p) for p in [R/'protocol.md',R/'protocol_cn.md',R/'frozen_plan.json',R/'data/panel.jsonl',R/'data/selection.json']},main_saved=True,scientific_acceptance='Unknown'))
print('S07_FROZEN',len(panel),json.dumps(audit),flush=True)
