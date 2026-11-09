from common import *
from tokenizers import Tokenizer
import shutil,re,itertools,difflib
assert not (R/'frozen_plan.json').exists()
for n in ['data','cache','results','figures','evidence','versions']: (R/n).mkdir(exist_ok=True)
C.mkdir(parents=True,exist_ok=True)
old=R.parent/'S04_neutral_suffix_fixed_candidates_24'; prior=json.load(open(old/'frozen_plan.json'))
tok=Tokenizer.from_file(prior['model']+'/tokenizer.json')
# Each frame is a whole independent writing context. A frame and all its domains/wordings stay in one split.
frames=[
 'During a quiet inspection at the observation booth, Mira recorded {np}. Her note refers to that single subject.',
 'The afternoon inventory lists {np}. A numbered card identifies the subject of this entry.',
 'Before the exhibition opened, a guide prepared a short label about {np}. The label is attached to the relevant display.',
 'A visitor sent the archive a photograph showing {np}. The archivist kept the photograph with its description.',
 'In a classroom exercise, the teacher asked the students to describe {np}. Their worksheet concerns only that subject.',
 'One paragraph in the travel journal discusses {np}. The author saved the paragraph for a later revision.',
 'The museum audio recording introduces {np}. Listeners hear a brief account of the same subject.',
 'An illustrated catalogue contains a page devoted to {np}. An editor checked the caption on that page.',
 'Asked what the survey was about, the researcher replied that it concerned {np}. The interview then ended.',
 'Please file this record under the entry describing {np}. A clerk will use the description to retrieve it tomorrow.',
 'I remember the subject of the report: it was {np}. That is the subject I am referring to here.',
 'Only one item appears in the drawing, namely {np}. Nothing else is included in the drawing.',
 'What did the witness describe? The account identifies {np}. This passage summarizes that account.',
 'For the next reading exercise, consider {np}. Keep the subject in mind while reading the following label.',
 'Yesterday the assistant received a request for information about {np}. The response will discuss the requested subject.',
 'Title of the new archive entry: a description of {np}. The accompanying note supplies a little context.'
]
nps={
 'explicit':{'animal':'an animal','cat':'a cat','dog':'a dog','vehicle':'a vehicle','car':'a car','bicycle':'a bicycle','chair':'a chair','stone':'a stone'},
 'synonym':{'animal':'a nonhuman creature','cat':'a domestic feline','dog':'a domestic canine','vehicle':'a conveyance','car':'an automobile','bicycle':'a pedal cycle','chair':'a seat with a backrest','stone':'a piece of rock'},
 'property':{'animal':'a living organism that eats organic matter and moves on its own','cat':'a small furry pet that meows and has retractile claws','dog':'a furry pet that barks and wags its tail','vehicle':'a manufactured object used to carry people between places','car':'a road machine with four wheels, an engine, and an enclosed cabin','bicycle':'a two-wheeled machine propelled by a rider pushing pedals','chair':'a piece of furniture for one person to sit on, with a back and legs','stone':'a small solid lump of natural mineral material'}
}
panel=[];suffix='\nDescription:'
for fi,frame in enumerate(frames,1):
 split='discovery' if fi<=8 else 'heldout'
 for wording,mp in nps.items():
  for label,nptext in mp.items():
   dom=next((d for d,ls in DOMAINS.items() if label in ls),'negative')
   text=frame.format(np=nptext);prefix=text+suffix;enc=tok.encode(prefix,add_special_tokens=False);cs=[]
   for cand in ['cat','dog','car','bicycle']:
    full=tok.encode(prefix+' '+cand+'.',add_special_tokens=False).ids;assert full[:len(enc.ids)]==enc.ids
    ids=full[len(enc.ids):];cs.append(dict(label=cand,text=' '+cand+'.',token_ids=ids,token_count=len(ids),full_ids=full))
   p=dict(id=f'S06_F{fi:02d}_{wording}_{label}',family=f'F{fi:02d}',domain=dom,split=split,wording=wording,label=label,
          level='parent' if label in DOMAINS else 'child' if dom!='negative' else 'negative',
          template_id=f'T{fi:02d}',template=frame,category_phrase=nptext,text=text,prefix=prefix,suffix=suffix,
          literal_target_words=re.findall(r'\b(?:animal|cat|dog|vehicle|car|bicycle)s?\b',text.lower()),
          explicit_label_word=bool(re.search(r'\b'+label+r's?\b',text.lower())),
          token_ids=enc.ids,token_pieces=enc.tokens,token_offsets=enc.offsets,target_index_zero_based=len(enc.ids)-1,
          target_token_id=enc.ids[-1],target_token_piece=enc.tokens[-1],candidates=cs,
          behavior_gold=label if label in ['cat','dog','car','bicycle'] else None)
   assert enc.ids[-1]==25 and max(len(c['full_ids']) for c in cs)<=128;panel.append(p)
assert len(panel)==384
# No near-duplicate frames after removing the manipulated category phrase. This does not establish independent semantic contents.
similar=[dict(a=i+1,b=j+1,ratio=difflib.SequenceMatcher(None,a,b).ratio()) for i,a in enumerate(frames[:8]) for j,b in enumerate(frames[8:],8)]
assert max(r['ratio'] for r in similar)<.8
jsonl(R/'data/panel.jsonl',panel);dump(R/'data/templates.json',dict(frames=frames,phrases=nps))
shutil.copy2(old/'data/S03_frozen_selection.json',R/'data/S03_frozen_selection.json')
shutil.copy2('/tmp/sae_hierarchy_1104_assets.json',R/'evidence/input_access.json')
shutil.copy2('/tmp/sae_hierarchy_navigation.txt',R/'evidence/navigation_check.txt')
protected={str(p):sha(p) for d in R.parent.iterdir() if d.is_dir() and d.name.startswith(('S02_','S03_','S04_','S05_')) for p in d.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
dump(R/'evidence/old_immutable_before.json',protected)
for p,h in prior['input_SHA256'].items():assert sha(p)==h
for ss in prior['sites'].values():assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
plan=dict(experiment=R.name,UTC=now(),authorization='Current user explicitly authorizes end-to-end H1/H2 hierarchy research, bounded inference, controls, reports and package; no intermediate confirmation.',
          model=prior['model'],input_SHA256=prior['input_SHA256'],sites=prior['sites'],data_sha256=sha(R/'data/panel.jsonl'),
          rows=384,families_per_domain=16,independence='16 template clusters, 8 discovery/8 heldout; two domains share frames and are correlated',
          discovery_families=[f'F{i:02d}' for i in range(1,9)],heldout_families=[f'F{i:02d}' for i in range(9,17)],
          suffix=suffix,shape=[4,128],device='CPU',threads=2,seed=20261104,wall_ceiling_seconds=3600,
          selection='Only explicit discovery; save selection and directions before any heldout forward or any synonym/property analysis.',
          H1_common='Per domain, P/C/D triple-active frequency >=6/8 in explicit discovery; rank frequency then mean raw z across triples descending; top8.',
          H1_events='For each child, recruit (P=0,child>0) and loss (P>0,child=0): frequency>=4/8, rank frequency then mean absolute delta; top6 per event.',
          H2_members='Per domain, triple-active in ALL8 explicit discovery families, rank mean raw z descending; top8; selection independent of sibling contrast.',
          H2_primary='Sibling difference of fixed-list L2-normalized z projected on explicit-discovery mean sibling difference, unit-normalized direction; only same fixed-list support and >=2 positive members. >=6/8 eligible families needed. Parent-child descriptive secondary.',
          H1_primary='Per domain each family mean Jaccard over P-C/P-D/C-D minus mean Jaccard of its three rows against the other-domain three rows (9 pairs).',
          tests='8 explicit-primary tests: H1/H2 x 2 domains x 2 SAE, Holm p<=.05. H1 six labels permuted within heldout family (4095 random permutations,+1); H2 exact independent sibling sign swaps on eligible heldout families. Four H1 contrasts correlated, not independent.',
          uncertainty='4096 family bootstrap resamples, seed20261104, 95% percentile intervals; 8 clusters only, constructed-stimulus uncertainty, not population semantic inference.',
          random='512 independent support pairs, k=32: uniform30000 and discovery-activation-frequency weighted sampling without replacement (frequency+.5 smoothing). Candidate sets:256 sets matched within +/-2 of discovery active count per feature, excluding own list; report failed matches.',
          support='active iff native Top32 z>0. Pairwise intersection/union/Jaccard/intersection over parent active count, plus triple intersection. Recruit/loss equality structural if both counts32.',
          relative='q=z_C/||z_C||2 on exact frozen list C; zero norm undefined; raw z, full-z L2/L1 and fixed-list L2 also reported. decoder-norm-weighted sensitivity descriptive.',
          verdict='AI operational verdict only. Local explicit support requires positive heldout estimate, lower bootstrap bound>0 and Holm pass, plus sibling behavior>=.75 each label. Cross-wording support additionally requires same positive lower bound on property and synonym, adequate H2 eligibility, and each child behavior>=.75. If valid/adequate but prediction reverses or misses primary criterion: NOT_SUPPORTED at that scope; if behavioral/eligibility/sample-power limits: INSUFFICIENT. Failure of CI to exclude0 alone does not falsify.',
          optional='No classifier, no SVD, no model/dictionary/router training, no interventions. Joint differences/rank orders and pairwise coactivation are analyzed. Shared-parent cosine compared to parent-matched structural label shuffle, never semantic direction named.',
          display='F09 preselected complete heldout animal and vehicle cases, both SAE. First heldout family opposite joint direction or least aligned family if none reverses; all failures retained.')
dump(R/'frozen_plan.json',plan)
dump(R/'evidence/data_audit.json',dict(UTC=now(),rows=len(panel),max_tokens=max(len(x['token_ids']) for x in panel),cross_split_max_frame_similarity=max(r['ratio'] for r in similar),cross_split_frame_similarities=similar,split_frozen_before_forward=True,property_wording_literal_target_rows=sum(bool(p['literal_target_words']) for p in panel if p['wording']=='property'),near_duplicates='No frame shared across splits; fixed task category phrases repeat and limit independence. No source corpus or unseen-training claim.',parent_label_limits='nonhuman creature is broader than animal; conveyance is a near synonym; property parents are compatible broad descriptions. These are deliberately imperfect lexical controls, no gold abstraction claim.'))
# Preserve existing formal Anchor identities and old hypotheses, adding the user-activated bounded operational scope within their eight sections.
ar=SYS/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
anchors=[ar/'15_27_06_common_members_extra_responses_anchor.md',ar/'15_27_07_conditional_relative_strength_anchor.md']
for a in anchors:
 for f in [a,a.with_name(a.stem+'_cn.md')]:
  shutil.copy2(f,R/'versions'/f.name)
  oldtxt=f.read_text();is_cn=f.stem.endswith('_cn')
  if is_cn:
   addition=f'\n### 2026-11-04 研究者激活的自然语言层级轮次\n\n本轮目的：通过动物→猫／狗、交通工具→汽车／自行车及跨大类对照，观察成员更替和共同成员的强弱搭配如何对应自然文本。当前用户明确授权设计、执行、检查、结论更新和打包。旧矩阵命题及S02–S05冻结结果保留。本轮H1是共同使用与换入换出的可复现关联；H2是共同成员强弱搭配的可复现关联。它们是本轮可观察命题，不替代旧的额外信息／功能命题。\n\n竞争解释包括显式词复制、同义词和属性提示、模板／后缀／位置、固定Top32竞争、整体幅度、字典重构及小样本筛选。本轮固定两个大类各16家族，模板整体8发现／8留出，三种措辞及椅子／石头负类。相同末尾Description:冒号取样；两套原生SAE分别分析。共同成员既报告逐对交集，也报告发现集固定列表；q为固定列表原始z除其L2范数。零范数未定义。\n\n最小检验是留出家族内的成员关系对照、固定共同列表的联合相对差及改写／属性复现。若仅显式词成功，更新为词面条件下的组合候选；有效对照下不复现则未支持对应预测；行为或共同成员资格不足则证据不足。H3/H4和真实router训练留在parking lot。研究者科学接受及关闭仍Unknown。\n\n当前状态：NOT RUN。具体协议与先于推理的冻结规则见[本轮Protocol]({C}/protocol.md)。\n'
  else:
   addition=f'\n### Researcher-activated natural-language hierarchy round, 2026-11-04\n\nPurpose: inspect richer natural-text differences through SAE member combinations: animal→cat/dog and vehicle→car/bicycle, including cross-domain comparisons. The current user authorizes the complete design, execution, checks, bounded conclusion update and package. Frozen matrix hypotheses and S02–S05 remain intact. Round H1 predicts reproducible shared/recruited/lost-member associations; round H2 predicts reproducible relative-strength combinations among common members. These observable claims do not replace the older incremental-information or functional hypotheses.\n\nLive rivals are explicit-word copying, synonym/property cues, template/suffix/position, Top32 competition, total scale, reconstruction limits and selection/small-sample effects. Observe two independent native 30000-coordinate Top32 dictionaries at the same final Description: colon. Sixteen families per domain share sixteen frame clusters; eight discovery/eight heldout, three wordings and chair/stone negatives. Distinguish per-pair common supports from discovery-fixed lists; relative q is raw z on the exact fixed list divided by its L2 norm, undefined at zero. No cross-dictionary ID correspondence.\n\nMinimal falsifiers: heldout within/cross-domain overlap, frozen common-list joint relative differences, and synonym/property replication. Explicit-only correspondence is local; adequate but contrary comparisons do not support the tested prediction; failed behavior or support eligibility yields insufficient evidence. Anticipated update concerns category/wording dependence, not universal hierarchy or semantic directions. H3/H4 and router training remain parked. Researcher acceptance and closure remain Unknown.\n\nCurrent round: NOT RUN. The [Protocol]({C}/protocol.md) owns exact frozen computations and decision rules.\n'
  # Insert under section5, not a parallel design file or ninth top-level section.
  marker='\n## 6.'
  assert marker in oldtxt
  f.write_text(oldtxt.replace(marker,addition+marker,1))
en=f'''# S06 Protocol: SAE combinations and semantic hierarchy

## 0. Approval and scope

APPROVED_FOR_BOUNDED_INFERENCE_AND_ANALYSIS by current direct user request. Anchor owners 15_27_06 and 15_27_07 retain their identities; older functional hypotheses and records are preserved. Engineering operationalizations below are AI choices within the explicitly delegated design/execution scope, not researcher scientific acceptance. No waiting gate remains. Scientific acceptance, mechanism judgment and closure: Unknown.

Purpose: distinguish reproducible member replacement (round H1) and joint relative strengths (round H2), including category and wording dependence. No training, classifier, SVD, interventions or router. Complete all applicable steps, figures, bilingual results, daily brief, memory and <20MB package.

## 1. Definitions and design

An SAE feature is a coordinate in its own dictionary. Active means native Top32 output z>0. Top32 bounds support size; if all selected values are positive, both samples have32 members and recruitment equals loss structurally. The Attention hook is final zero-based block27 self_attn.o_proj output before residual addition. MLPIN is actual block27.mlp input, after residual addition and post_attention_layernorm. Both use native linear encoder, ReLU and Top32, no input normalization or decoder-bias subtraction. They are not MLP before/after causal comparisons. Model/SAE/loader IDs, absolute paths and hashes are in frozen_plan.json, inherited and verified from S04.

## 2. Data and confirmation boundary

Exactly16 independently authored frames,8 discovery F01–F08 and8 heldout F09–F16, fixed before responses. Each frame contains animal/cat/dog, vehicle/car/bicycle and chair/stone, each in explicit/synonym/property wording:384 prefixes. This is16 families/domain, but only16 correlated frame clusters, not32 independent clusters. A frame/domain/wording never crosses splits. Fixed manipulated category phrases repeat; this is a controlled panel, not training-unseen language. Record every literal string, template, label, phrase, full tokenizer IDs/pieces/offsets, final suffix token index and explicit-label flag. Three wordings share semantic intent but synonym parents and broad property descriptions are imperfect, stated in data_audit. No sample removal on behavior or representations.

All end with exact newline+Description:, no trailing space. Sample final colon ID25 before any candidate; absolute token positions may vary and are recorded. Semantic swaps within frames control syntax; cross-domain and chair/stone serve negative controls. Synonym/property variants probe lexical dependence. Repeated forms are not independent families. No prompt search.

## 3. Native behavior and extraction

Use frozen official Qwen3-0.6B Base in FP32 CPU2threads, eval/no gradients, physical shape4x128. Complete candidates in fixed order: ' cat.', ' dog.', ' car.', ' bicycle.'. Verify concatenated tokenization retains the prefix; record actual lengths and all per-token log probabilities, including punctuation. Main score=sum log conditional probabilities in nats, no prior/length calibration; max wins, fixed-order ties recorded. Fine children get sibling binary accuracy (each label denominator8/split/wording) and four-candidate accuracy; parent/negative get preferences only. Counts on all384 retained prefixes; behavioral eligibility>=.75 per child on heldout for semantic interpretation; failure limits semantic claims, not descriptive feature reporting. Secondary length-mean scores are explicitly diagnostic if lengths differ.

Representation at prefix end can be captured in teacher-forced candidate calls because causal attention excludes future candidate tokens. Validate prefix-only equivalence, lane equivalence, no-op hooks, native SAE encoding equality, finite values, and reconstruction=residual ledger before extraction. Save preactivation, Top32 ranks/cutoffs, raw z, decoder norms, h and reconstruction error; sparse full z supports portable audit. Freeze input hashes and old S02–S05 hashes. No changes to weights.

## 4. H1 computations

For P→C, P→D, C↔D and all9 cross-domain pairs within frame/wording compute intersection I, union U, J=I/U, I/parent-active-count, counts, recruited/lost IDs and triple intersections. Negative pair comparisons are descriptive. Primary per-domain family contrast = mean of3 within-domain J minus mean of9 cross-domain J. Label null permutes the six labels within each heldout frame independently (4095 Monte Carlo draws, plus-one p); maintains family correlations, TopK and each vector's scale. Also permute family pairing while preserving labels as a template-control diagnostic.

Explicit-discovery common candidates: triple-active in>=6/8, rank frequency then mean raw z, top8. Child recruitment/loss candidates: event frequency>=4/8, rank frequency then absolute mean delta, top6 each. Freeze IDs and direction before heldout inference, then report every candidate/event/wording, including failures. Counts are proportions out of8, not independent candidate replications. Frequency is panel activation rate (count/64 explicit discovery rows), not training-corpus rarity.

Baselines:512 uniform32-of30000 support pairs and512 discovery-frequency-weighted pairs (count+.5 smoothing), sampling without replacement. Report exact budgets and baseline distributions. For selected lists,256 count-matched random lists, each coordinate active-count within+/-2 on explicit discovery, own list excluded; unmatched lists remain failures, never broaden matching after results. Compare common/event coverages and joint projection pattern against matched references; primary label-null judgment remains separate from these descriptive random diagnostics.

## 5. H2 computations and joint patterns

H2 list per domain consists of triple-active features in ALL8 explicit discovery families, sorted mean raw z descending, max8; no selection on class contrast. All raw values and q=z_list/L2(z_list), along with whole-z L1/L2 and list L2, are reported. Zero norm undefined. Decoder norm weighted sensitivity uses its own exact denominator and is retained even if equivalent. Fixed-list q is distinct from pair-dynamic common-member normalization; the latter is paired explanation only and never a single-input router.

For each of P→C/P→D/C→D calculate discovery mean q difference. Primary sibling statistic is heldout q difference projected onto unit discovery mean sibling difference; only pairs with identical support on the fixed list and>=2 positive members are eligible. Need>=6/8 eligible heldout families; insufficient otherwise. Freeze discovery directions before heldout; report all ineligible pairs and full-vector values descriptively. Exact independent sibling sign swaps yield p. Parent-child and pair-dynamic common deltas are descriptive, not rescue tests. Show four discovery-chosen most changing pairwise member strength orders, joint support patterns and all paired difference vectors. Distinguish raw total scale from relative differences.

For full30000 differences decompose retained-amplitude/recruited/lost components (disjoint per pair); squared-norm shares denominator=full paired squared norm, pooled shares=sum component squared norms/sum full squared norms. Mean components can overlap across families, so do not add their squared lengths. Cat−P/dog−P and car−P/bicycle−P share P; report similarity against within-frame random reassignments of P/C/D preserving shared-parent structure and against family-mismatched pairs; never call positive cosine itself a semantic direction. SVD and classifier are NOT RUN by choice; joint differences answer the present question without them.

## 6. Uncertainty and verdict

Explicit primary tests: H1/H2 x2 domains x2 SAE=8; Holm familywise .05, no auxiliary rescue.4096 family bootstrap resamples(seed20261104),95% percentile intervals, equal family weights. These small constructed-frame intervals do not estimate all natural language. Local support: eligible, behavior>=.75 per child, positive estimate/lower interval>0 and Holm pass. Cross-wording support additionally needs positive lower interval and behavior qualification in synonym/property, plus H2 same-support eligibility. Valid contrary/failed replication limits or does not support that specific prediction; inadequate behavior, matching, eligibility or resolving power is insufficient, not falsification. Explicit-only results may be locally supported while generalized hypotheses remain insufficient. All posthoc observations labeled exploratory. Human scientific acceptance remains Unknown.

## 7. Ordered execution, outputs and audits

1. Asset/schema/old-source audit, write Anchors/Protocol, freeze panel and hashes.2. Explicit-discovery extraction+native scoring and numerical calibration.3. Select candidates/directions on discovery ONLY, save hash gate.4. Extract remaining discovery controls and all heldout conditions.5. Compute all H1/H2/negative/random/lexical/family/preactivation/reconstruction comparisons without further fitting.6. Figures: preselected complete F09 animal and vehicle, within/cross comparisons with every family, wording-control and failures.7. Independent numerical recomputation and source preservation.8. Bilingual Summary/Detailed, Chinese daily report, bounded Anchor evidence update, append-only own memory, synchronized local reading copies.9. Package complete sparse activations/texts/summaries/selected preactivations and scripts, full cache external indexed with bytes; check<20,000,000bytes, ZIP CRC, extraction and main files.

CPU time ceiling3600s for extraction, no cloud job or GPU use. On isolated failure preserve partial receipts and finish independent work. Resume only missing output IDs, never silently rerun completed outputs. Scientific, data/statistics and implementation audits recorded separately. Environment dependencies reused from /data/250010109/dependency_packages/hf_transformers_qwen3; native loaders reused; S04 capture/scoring adapted to384rows/four candidates, new analysis separately authored. Training reuse index inspected; training infrastructure unused. No commit, push, external publication or Graph edits.

## 8. Freeze and amendment ledger

Initial revision: {now()}. Scientific body, data, config and script hashes in evidence/protocol_freeze.json. User authorizes delegated in-scope design and execution now; operational thresholds are AI registered choices, not attributed human mechanism judgment. A–G cross-consistency PASS for this bounded scope. After first forward, preserve initial body. Material repairs are appended with timestamp, old/new value, reason, response exposure and eligibility impact in amendments.md; original versions remain in versions/. No result-driven candidate or threshold changes.
'''
(R/'protocol.md').write_text(en)
cn='''# S06协议：SAE组合与语义层级

当前用户明确授权从设计到推理、留出验证、结论更新和打包；不用中途确认。沿用15_27_06／07身份，不改变旧冻结结果和旧功能命题。科学接受与关闭Unknown。

目的：分别观察动物→猫／狗、交通工具→汽车／自行车的成员组合(H1)和共同成员强弱搭配(H2)，允许类别之间不同。两套SAE各30000维、原生ReLU-Top32，在block27的o_proj残差前输出和实际MLP输入分别观测。同号ID不对齐。

固定16个模板家族：F01–08发现，F09–16留出；两个大类共享模板所以只有16个模板簇。每家族含六类别及椅子／石头，三种措辞(显式词／同义词／属性描述)，384条。每大类16家族。一个模板及所有改写不能跨划分。固定类别短语会重复，不宣称训练未见。每条统一换行Description:，末尾冒号ID25取样，位置和完整token全部保存。原模型四完整候选cat/dog/car/bicycle各带前导空格、句号；总条件对数概率计分，逐token记录。细类报同父二选一和四选一，父类／负类只报偏好。行为不佳的样本不删除。

H1逐对／三方支持交集、并集、Jaccard、保留／换入／换出逐家族报告；主比较是同域三对平均Jaccard减与另一域九对平均值。原生固定Top32使同样32活跃时换入=换出，这是结构约束。发现集选共同(三方>=6/8，频率再平均z排序，最多8)及每子类换入／换出(>=4/8，最多6)候选。冻结后才打开留出。参照含512次均匀／发现频率加权32成员随机支持，256组活动计数±2匹配随机候选；匹配失败保留，不放宽条件。

H2固定列表取发现8家族三方全激活的最多8成员，按平均z选，不按差异选。原始z、全体L1/L2、列表L2、q=z列表/列表L2及decoder加权补充并列；零范数不可定义。主判断为兄弟类q差沿发现平均差方向的投影，只在固定列表支持相同且至少2个成员为正的配对上，留出至少6/8组才有资格。父子差、动态共同成员、联合支持、成对强弱顺序和完整配对差作解释分析，不能伪装router。差平方范数的共同强弱／换入／换出分母是完整差平方范数；跨家族平均分项能量不能直接相加。共享父向量导致两子类差相似，用保留共享父结构的类内打乱参照检查。

显式词8项主检验(H1/H2×两域×两SAE)，Holm .05；H1家族内六标签随机置换4095次加一，H2兄弟标签成对精确换序。4096次模板家族bootstrap、95%百分位区间，只描述该构造面板。局部支持需行为每子类>=.75、资格足、效应/区间正且Holm通过；跨措辞还需同义及属性方向区间正和行为／共同成员资格足。有效但反向或未复现不支持该预测；行为、资格或检验能力不足记证据不足。不能把区间跨零写成证伪。

执行顺序：冻结→显式发现→候选及方向哈希门→所有控制和留出→全部比较与反例→图和独立复算→中英报告及daily→本会话memory与Anchor本地阅读副本→小于20MB包。预选F09两域完整示例；首个反向或最弱对齐反例，不删除其余家族。SVD、分类器、训练、干预和H3/H4均不运行。CPU2线程、4×128、推理3600秒上限，不使用GPU或云任务。任何实质修订追加时间、前后值、理由和可见数据，保留原版。英文协议与frozen_plan.json拥有完整可复算定义。
'''
(R/'protocol_cn.md').write_text(cn)
for n in ['protocol.md','protocol_cn.md']:shutil.copy2(R/n,C/n)
for name,text in {
 'identification':'H1/H2 are associations in controlled natural English; literal/synonym/property cues and broad parent ambiguity remain. No causal intervention or router; no human scientific verdict inferred.',
 'data':'16 frame clusters/8 heldout; no split-crossing frames. All384 samples retained.8 primary tests Holm; family resampling, no feature-as-independent-sample inflation. Behavioral insufficiency restricts semantics, not descriptions.',
 'implementation':'Reuse same verified official model and native SAE loaders; FP32 CPU2threads. Zero trainable parameters; LM training telemetry not applicable. Prefix-only causality/lane/noop checks and native Top32 reconstruction ledger required. Candidate gate before heldout.'
}.items():(R/'evidence'/('audit_'+name+'.md')).write_text('# '+name+'\n\n'+text+'\n')
freeze=dict(UTC=now(),state='APPROVED_BY_DIRECT_CURRENT_USER_SCOPE',hashes={str(p):sha(p) for p in [R/'protocol.md',R/'protocol_cn.md',R/'frozen_plan.json',R/'data/panel.jsonl']},initial_anchor_hashes={str(a):sha(a) for a in anchors},source_code={str(p):sha(p) for p in (R/'code').glob('*.py')},scientific_acceptance='Unknown')
dump(R/'evidence/protocol_freeze.json',freeze)
mp=SYS/'.research/memory/conversations/1104-sae特征组合与语义层级/memory.md';mp.parent.mkdir(parents=True,exist_ok=True);assert not mp.exists()
mp.write_text(f'''# Conversation Memory: SAE特征组合与语义层级

Conversation name: 1104-SAE特征组合与语义层级
Conversation ID: 01a1a24a-9577-7280-8c1d-499bfd7e5c36
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: {now()}
Latest update at: {now()}
Continues from: ../1102-feature组合与自然语言关系四路线初步实验/memory.md
Environment: repo={SYS}; exec={R}

## {now()} -- 设计与数据先于推理冻结

- Summary: 用户授权H1/H2上下位自然语言组合完整轮次。已读两指定对话、原memory及S02–S05报告/源码，核验同一模型/两独立SAE。H3/H4和router停放。
- Current work: S06协议、384条数据、16家族/域及8/8模板划分已冻结；尚未前向。旧候选原样保留，新候选仅来自新显式发现。
- Next action: CPU冻结推理→发现候选哈希门→留出及改写/属性控制→图/数值检查/完整报告/包。无需再次确认。
- References: {R}/frozen_plan.json；{C}/protocol.md；15_27_06／07现有Anchor。
''')
print('S06_FROZEN',len(panel),max(len(p['token_ids']) for p in panel),sha(R/'frozen_plan.json'),flush=True)
