from common import *
import numpy as np,pyarrow.ipc as ipc,unicodedata,re,shutil,itertools,collections
from tokenizers import Tokenizer
assert not (R/'frozen_plan.json').exists()
for name in ['data','cache','results','figures','evidence']: (R/name).mkdir(exist_ok=True)
C.mkdir(parents=True,exist_ok=True)
prior=json.load(open(R.parent/'S06_semantic_hierarchy_1104/frozen_plan.json'));T=Tokenizer.from_file(prior['model']+'/tokenizer.json');rng=np.random.default_rng(20261104)
sources={
 'Magicoder':dict(asset='hf_prepared_ise_uiuc_magicoder_oss_instruct_75_k',repo='ise-uiuc/Magicoder-OSS-Instruct-75K',revision='5f839b1f368a76b161028bb9edff055db34022b2',field='problem',split='train',file='/data/share/109_cache_dir/hf_data/datasets/ise-uiuc___magicoder-oss-instruct-75_k/default/0.0.0/5f839b1f368a76b161028bb9edff055db34022b2/magicoder-oss-instruct-75_k-train.arrow'),
 'GSM8K':dict(asset='hf_prepared_gsm8k',repo='gsm8k',revision='e53f048856ff4f594e959d75785d2c2d37b678ee',field='question',split='train',file='/data/share/109_cache_dir/hf_data/datasets/gsm8k/main/0.0.0/e53f048856ff4f594e959d75785d2c2d37b678ee/gsm8k-train.arrow'),
 'MMLU':dict(asset='hf_prepared_cais_mmlu',repo='cais/mmlu',revision='c30699e8356da336a370243923dbaf21066bb9fe',field='question',split='test',file='/data/share/109_cache_dir/hf_data/datasets/cais___mmlu/all/0.0.0/c30699e8356da336a370243923dbaf21066bb9fe/mmlu-test.arrow')}
pools={};availability=[];cross=collections.defaultdict(set);excluded=[]
for ds,source in sources.items():
 raw=ipc.open_stream(source['file']).read_all();field=source['field'];columns=[field]+([x for x in ['index','lang','subject'] if x in raw.column_names]);data=raw.select(columns).to_pylist();seen={};empty=0
 for i,r in enumerate(data):
  text=str(r[field] or '').replace('\r\n','\n').replace('\r','\n').strip()
  if not text:empty+=1;continue
  norm=re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip().casefold();h=hashlib.sha256(norm.encode()).hexdigest()
  if h in seen:excluded.append(dict(dataset=ds,row=i,reason='within_dataset_normalized_duplicate',canonical_row=seen[h]['row']));continue
  p=dict(dataset=ds,row=i,text=text,normalized_sha256=h,source_native_id=r.get('index'),language=r.get('lang'),subject=r.get('subject'));seen[h]=p;cross[h].add(ds)
 pools[ds]=list(seen.values());source['sha256']=sha(source['file']);availability.append(dict(dataset=ds,raw_records=len(data),empty=empty,unique_nonempty=len(seen),within_duplicates=len(data)-empty-len(seen),source_file=source['file']))
shared={h for h,sets in cross.items() if len(sets)>1}
for ds,pool in pools.items():
 pools[ds]=[p for p in pool if p['normalized_sha256'] not in shared]
 for r in availability:
  if r['dataset']==ds:r.update(cross_dataset_duplicates_removed=len(pool)-len(pools[ds]),available_after_text_dedup=len(pools[ds]))
n=min(257,min(len(v) for v in pools.values()));n-=1-n%2;assert n>=3
panel=[];lengths=[];tokenstats=[]
for ds in DATASETS:
 order=rng.permutation(len(pools[ds]));chosen=[];short=0
 for j in order:
  p=pools[ds][int(j)];enc=T.encode(p['text'],add_special_tokens=False)
  if len(enc.ids)<16:short+=1;excluded.append(dict(dataset=ds,row=p['row'],reason='fewer_than16tokens_before_sampling',canonical_row=None));continue
  L=min(128,len(enc.ids));pos=np.floor((np.arange(8)+.5)*L/8).astype(int).tolist();assert len(set(pos))==8
  native=p['source_native_id'];id=f"{ds}:{sources[ds]['split']}:row{p['row']}";q={**p,'id':id,'selection_index':len(chosen),'source':sources[ds]['repo'],'source_revision':sources[ds]['revision'],'source_split':sources[ds]['split'],'source_field':sources[ds]['field'],'full_token_count':len(enc.ids),'visible_length':L,'input_ids':enc.ids[:L],'positions':pos,'position_token_ids':[enc.ids[k] for k in pos],'position_token_pieces':[enc.tokens[k] for k in pos],'position_decoded':[T.decode([enc.ids[k]]) for k in pos],'position_offsets':[enc.offsets[k] for k in pos],'fixed32_position':31 if L>=32 else None,'fixed32_token_id':enc.ids[31] if L>=32 else None,'newline_count':p['text'].count('\n'),'has_code_fence':'```' in p['text'],'has_question_mark':'?' in p['text'],'raw_chars':len(p['text'])}
  chosen.append(q)
  if len(chosen)==n:break
 assert len(chosen)==n
 for r in availability:
  if r['dataset']==ds:r.update(sampled=n,sample_candidates_examined=len(chosen)+short,short_candidates_rejected=short,minimum_actual_eligible=n,all_population_token_length_eligibility='not exhaustively tokenized; uniform seeded rejection sampling from deduplicated pool')
 panel.extend(chosen)
 for scope,tokens in [('visible_window',[t for q in chosen for t in q['input_ids']]),('sampled_positions',[t for q in chosen for t in q['position_token_ids']])]:
  counts=collections.Counter(tokens)
  for t,c in counts.most_common(25):tokenstats.append(dict(dataset=ds,scope=scope,token_id=t,piece=T.id_to_token(t),decoded=T.decode([t]),count=c,denominator=len(tokens),fraction=c/len(tokens)))
 lengths.append(dict(dataset=ds,N=n,median_full_tokens=float(np.median([q['full_token_count'] for q in chosen])),min_full_tokens=min(q['full_token_count'] for q in chosen),max_full_tokens=max(q['full_token_count'] for q in chosen),median_visible_tokens=float(np.median([q['visible_length'] for q in chosen])),truncated=sum(q['full_token_count']>128 for q in chosen),code_fence=sum(q['has_code_fence'] for q in chosen),with_newline=sum(q['newline_count']>0 for q in chosen),with_question_mark=sum(q['has_question_mark'] for q in chosen)))
jsonl(R/'data/panel.jsonl',panel);jsonl(R/'data/exclusions.jsonl',excluded);table(R/'data/availability.csv',availability);table(R/'data/basic_format.csv',lengths);table(R/'data/top_tokens.csv',tokenstats);dump(R/'data/sources.json',sources)
# Pair-specific matching on full question length, before any activation is observed.
edges=[16,32,48,64,96,128,192,256,512,1024,2048,10**9]
def lengthbin(p):return int(np.searchsorted(edges,p['full_token_count'],side='right')-1)
controls=[];selection=[];lexsets={}
for a,b in itertools.combinations(DATASETS,2):
 pa=[p for p in panel if p['dataset']==a];pb=[p for p in panel if p['dataset']==b];matched_a=[];matched_b=[];strata=[]
 for k in range(len(edges)-1):
  aa=[p for p in pa if lengthbin(p)==k];bb=[p for p in pb if lengthbin(p)==k];m=min(len(aa),len(bb))
  if m:
   aa=[aa[int(j)] for j in rng.permutation(len(aa))[:m]];bb=[bb[int(j)] for j in rng.permutation(len(bb))[:m]];matched_a+=aa;matched_b+=bb;strata.append(dict(bin=k,range=[edges[k],edges[k+1]],A=m,B=m))
 if len(matched_a)%2==0 and matched_a:
  k=lengthbin(matched_a[-1]);matched_a.pop();j=max(j for j,p in enumerate(matched_b) if lengthbin(p)==k);matched_b.pop()
  for st in strata:
   if st['bin']==k:st['A']-=1;st['B']-=1
 def ids(ps):return [p['id'] for p in sorted(ps,key=lambda p:hashlib.sha256(('S08'+p['id']).encode()).hexdigest())]
 controls.append(dict(A=a,B=b,mode='length_matched',A_ids=ids(matched_a),B_ids=ids(matched_b),N=len(matched_a),strata=strata))
 aa=[p for p in pa if p['fixed32_position'] is not None];bb=[p for p in pb if p['fixed32_position'] is not None];m=min(len(aa),len(bb));m-=1-m%2
 controls.append(dict(A=a,B=b,mode='fixed32',A_ids=ids([aa[int(j)] for j in rng.permutation(len(aa))[:m]]),B_ids=ids([bb[int(j)] for j in rng.permutation(len(bb))[:m]]),N=m,strata=[]))
 for ds,ps in [(a,pa),(b,pb)]:selection.extend(dict(A=a,B=b,mode='main',dataset=ds,id=p['id']) for p in ps)
 # Literal-token control, selected only by document coverage in the two question panels, not SAE response.
 counts=[]
 for ps in [pa,pb]:
  c=collections.Counter(t for p in ps for t in set(p['position_token_ids']));counts.append(c)
 common=sorted(set(counts[0])&set(counts[1]),key=lambda t:(-min(counts[0][t],counts[1][t]),t));tokens=[t for t in common if min(counts[0][t],counts[1][t])>=20][:3]
 lexsets[a+'__'+b]=[dict(token_id=t,piece=T.id_to_token(t),decoded=T.decode([t]),A_docs=counts[0][t],B_docs=counts[1][t]) for t in tokens]
dump(R/'data/control_selections.json',controls);dump(R/'data/lexical_control_tokens.json',lexsets);table(R/'data/sample_ids.csv',[dict(id=p['id'],dataset=p['dataset'],row=p['row'],normalized_sha256=p['normalized_sha256'],full_tokens=p['full_token_count'],visible_length=p['visible_length'],source_field=p['source_field']) for p in panel])
missing=dict(Numina=dict(status='NOT_FOUND_IN_BOUNDED_SEARCH_SKIP',searched=['/data/share/109_cache_dir name search depth5','/data/250010109 name search depth3','asset catalog names/locations'],claim='No matching readable named asset in these checked locations; not a global absence claim'),senior_exact=dict(path='/mnt/workspace/zx_workspace/sae-guided-router/sft_mixture_6000_each_with_mmlu_bbh_mmlu_eval_aligned/train.parquet',exists=False,claim='Current path not readable/present; no exact replication claim'),cache_reuse=dict(decision='REJECT_OLD_E18_FOR_THIS_PANEL',reason='Historical cache cannot bind exact current document IDs/positions and both native hooks; only MLP dictionary historically available. New dual-SAE extraction uses existing frozen model, no training.'),Magicoder_alternative=dict(repo='ise-uiuc/Magicoder-Evol-Instruct-110K',revision='b0079beaa0361d82412520b873715bee59cc7dd4',used=False,reason='Use OSS problem field as one fixed Magicoder version; no post-result version selection.'))
dump(R/'evidence/source_audit.json',missing);shutil.copy2('/tmp/S08_input_access.json',R/'evidence/input_access.json');shutil.copy2('/tmp/S08_navigation.txt',R/'evidence/navigation.txt')
plan=dict(UTC=now(),authorization='Current user directly authorizes fast existing-data H1 member-overlap analysis, extraction if needed, all feasible datasets independently; no model training or interventions.',primary_anchor='15_27_06',model=prior['model'],input_SHA256=prior['input_SHA256'],sites=prior['sites'],datasets=DATASETS,missing_datasets=['Numina'],N_per_dataset=n,documents=len(panel),positions_per_document=8,max_input_tokens=128,auxiliary_fixed_position=31,minimum_tokens=16,seed=20261104,device='CPU',threads=2,shape=[8,128],main_metric='Per document pair, average8aligned-quantile token-position Jaccards; activation z>0 native Top32; no amplitude in Jaccard.',pairing='Each dataset ordered by SHA256(S08+id). Within all unordered i<j: N(N-1)/2. Cross cyclic offsets1..(N-1)/2 moduloN: same N(N-1)/2 distinct pairs, each document degree(N-1)/2. N odd, no within self or duplicate unordered pair. All positions/repeated document incidences stay one cluster.',bootstrap='1999 independent multinomial document-count resamples in each dataset, original pair graph reweighted by count_i*count_j, full document including all positions moves together. Weighted pair mean,95%percentile intervals; no independent token/pair bootstrap.',permutation='999 whole-document label permutations plus-one p; fixed random-order pairing rule reapplied after relabeling, N unchanged. Main null requires exchangeability of entire document representations under labels, not randomized topic intervention. Length-matched permutes within full-token-length strata preserving both counts. Same-token control descriptive bootstrap only.',primary_tests='2SAEs x3datasetpairs=6 one-sided pooled-within-minus-cross tests, Holm.05. A-minus-cross and B-minus-cross each reported with document CIs; claim both higher only if both lower bounds>0 and pooled Holm passes. Controls exploratory with raw p, no rescue. Interval spanning0 means inconclusive, not absence.',controls='Pair-specific matched full-token-length histograms, same question-only field rule and8sampling; fixed absolute31position (same32token visible prefix); preselected up to3 literal token IDs each occurring in>=20docs of each dataset, compare equal token at any of8sampled positions, document-pair mean, no conditional permutation p.',amplitude='Supplement only: at aligned positions compute RMS raw-z difference on intersection coordinates, average document pairs with shared-member coverage. Also whole-z L2 by dataset. Do not fold it into binary overlap.',freeze_data_sha256=sha(R/'data/panel.jsonl'),control_selection_sha256=sha(R/'data/control_selections.json'),lexical_sha256=sha(R/'data/lexical_control_tokens.json'),training=False,intervention=False,scientific_acceptance='Unknown')
dump(R/'frozen_plan.json',plan)
protocol=f'''# S08 Protocol: within/cross dataset SAE support overlap

APPROVED_FOR_BOUNDED_EXTRACTION_AND_STATISTICS by current direct user request. The existing H1 owner15_27_06 supplies the member-overlap question. This is a new natural-dataset robustness round, not a new hypothesis of domain knowledge. No model/SAE/readout training or functional interventions.

## Data and object

Actual readable cached Magicoder-OSS75K problem(train), GSM8K question(train), MMLU question(test), as exact Arrow files/revisions/SHA in data/sources.json. Exclude Magicoder solution/seed and MMLU choices/answer; no prompts/chat wrappers or answer suffixes. Neither Numina nor the senior exact SFT path was found in the bounded recorded locations. Continue the three available sources; do not claim senior replication. Historical E18 caches lack this exact two-hook/document/position binding and are not reused.

Deduplicate full question text by NFKC+casefold+collapsed whitespace hash; retain original internal formatting for inference. Remove all occurrences of exact normalized cross-dataset duplicates symmetrically; within-dataset retain first source row. Seeded uniform rejection sampling requires>=16token questions, selecting {n}per dataset. Available source counts refer to complete deduplicated text pools; token length eligibility is checked on uniformly shuffled candidates until quota, not falsely claimed for every corpus row. Save all IDs, source rows, texts, exclusions, full/visible lengths and actual tokens/offsets.

Use the same verified official Qwen3-0.6B Base and two separate native30000/ReLU-Top32 dictionaries. Attention hook=zero-based block27.o_proj output before residual addition; MLPIN hook=actual block27.mlp input after residual/post_attention_layernorm. No input renormalization or decoder-bias subtraction. Active iff native z>0; same feature IDs across dictionaries unrelated. Frozen FP32 CPU2threads, physical8x128, no output scoring.

For each question use first min(full_length,128)tokens without special tokens. Sample8positions floor((j+.5)*visible_length/8),j0..7; min16makes them distinct. No suffix. Keep all selected tokens as one document cluster. Also capture absolute position31when available, excluded otherwise. Each position is causal prefix-only; later tokens cannot affect it. Check full-window vs truncated32state equivalence at this position and a hook no-op before scaling.

## Metrics and pairing

Per token pair J=|support intersection|/|support union|, binary only. Main document-pair kernel averages8same-quantile-position Jaccards. Within each dataset use all distinct unordered pairs; cross-domain use cyclic offsets1..(N-1)/2 in pre-fixed hash order. Odd N gives exactly N(N-1)/2distinct pairs for A-within,B-within,cross; no within self pair. Cross graph has equal document degree. Report original unique pairs and8position comparisons, not independent sample counts. Save explicit pair IDs.

Report A-within,B-within,cross, A-minus-cross,B-minus-cross and pooled average-within-minus-cross.1999document bootstrap resamples independently in A/B; all original edges involving a resampled document get multiplicity count_i*count_j, same weighting for all its token positions. No token/edge bootstrap.999whole-document label permutations, plus-one p; reapply same balanced pairing rule to each relabeling. This tests source-label association under whole-document exchangeability, not causal semantic content. Main6pooled tests (3pairs x2dictionaries) Holm.05; preserve each side even if pooled is positive.

## Controls, amplitudes and limits

Pair-specific length controls match exact counts in frozen full-question token bins16/32/48/64/96/128/192/256/512/1024/2048+, selected before activations; oddify by removing one from the same bin in both groups. Same text part and8positions remain. Length-null permutes whole documents within bins, retaining counts. Fixed31control uses equal odd document counts from questions with>=32tokens, same32-token causal prefix, all else fixed. Literal-token control uses up to3tokens selected before activations by minimum document coverage>=20/source; average only same-token pairs among sampled positions within each document pair. Missing matching pairs remain missing, coverage and effective document counts reported; bootstrap document clusters, no label-permutation claim for this conditional control. These controls are exploratory and cannot rescue failed main tests.

Supplement: shared-coordinate raw RMS amplitude difference=sqrt(mean over shared positive members of(z_i-z_j)^2) per aligned position, then average eligible positions/document pairs; report coverage and whole-zL2. Separate from Jaccard. Publish frequent tokens/punctuation, newline/code/question-mark rates and full/visible-length distributions. Dataset source, topic, language, code format, task structure, near duplicates and128token truncation remain alternatives to domain-knowledge interpretation. MMLUsubject mixture is not homogeneous. No claimed training-unseen split or task accuracy.

## Outcome and delivery

Support only the bounded statement that within-source activations are more similar if both side differences have positive95%document intervals and the pooled Holm test passes; report local/asymmetric/reversed cases. Persistence/shrinkage under controls narrows interpretation, not uniquely identifies a cause. Wide intervals, matching loss or missing datasets are insufficient, never fabricated negatives. Statistical thresholds are AI operational choices frozen before activations within the user's delegated scope, not researcher mechanism approval. Scientific acceptance/closure Unknown.

Sequence: source/asset audit→text/sample/control freeze→dual-hook capture→all dataset-pair/SAE metrics and document uncertainty→controls/format/amplitude→independent numerical audit and plots→bilingual result, concise daily meeting report and review package. Old S06/S07 untouched. Reuse native model/SAE loaders and adapt extraction, write this dataset/document-pair analysis separately. Record code/data hashes, actual resources/time and any amendment without replacing initial protocol. No commit/push/publication. Exact registered definitions in frozen_plan.json; freeze UTC {now()}.
'''
(R/'protocol.md').write_text(protocol);(R/'protocol_cn.md').write_text('''# S08协议：同数据集／跨数据集SAE成员重叠

本轮用户直接授权查找、提取和统计，沿用H1 owner15_27_06；不训练或功能干预。实际使用Magicoder-OSS的problem、GSM8K和MMLU的question，排除答案、选项、指令包装。Numina及学长精确数据在已查路径未找到，跳过，不冒充复现。

固定种子20261104；NFKC/大小写/空白规范化做去重哈希，推理保留原格式。对规范重复跨数据集两侧都排除，域内保留首行。随机顺序拒绝少于16token的问题，各取257篇(若可用量不足按实际奇数上限)。每篇首128token内均匀取8个分位位置，另取有条件的第32token；不追加后缀。所有位置属于同一文档簇。

每文档对主指标为8个对齐分位token支持Jaccard的平均，只看z>0，不掺幅值。域内全不同文档无序对；跨域按固定哈希顺序的循环位移1..(N−1)/2取对，每类比较各N(N−1)/2对且跨域每文档参与数相同。记录具体ID对，不把重复参与文档当独立。1999次文档重采样，对所有关联边统一乘该文档抽中次数；999次整文档标签置换后重新应用相同配对规则。6项主比较(twoSAE×3pair)Holm.05，分别报告A内、B内、跨域、两侧差及合并差和文档区间。主标签置换只在文档整体与标签可交换的零假设下成立，不解释语义因果。

长度对照在实际全文token长度分箱内两侧等量，推理/取样不变，整文档标签仅在长度层内置换；再做同32token上下文位置控制。词面控制预先按两侧文档覆盖选最多3个共同token(每侧至少20篇)，只比较同token的真实采样位置，报告有效对数和文档覆盖，用文档bootstrap描述而不额外声称可交换置换。对照均不救主检验。额外分别列共同激活成员的原始幅值RMS差和整体L2，分母与覆盖写清，与0/1重叠分开。

三数据集不同来源、主题、语言/代码、格式、长度、MMLU学科混合及近重复仍是解释；128token窗口不是全文表示。只可得所测数据条件下成员相似度，不能直接称领域知识。完整英文协议和frozen_plan.json先于激活冻结。输出来源、样本ID、位置/token、全部配对、表图、文档统计、组会报告和小型包。科学接受Unknown。
''')
for name in ['protocol.md','protocol_cn.md']:shutil.copy2(R/name,C/name)
for p,h in prior['input_SHA256'].items():assert sha(p)==h
for s,ss in prior['sites'].items():assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
dump(R/'evidence/protocol_freeze.json',dict(UTC=now(),hashes={str(p):sha(p) for p in [R/'protocol.md',R/'protocol_cn.md',R/'frozen_plan.json',R/'data/panel.jsonl',R/'data/control_selections.json',R/'data/lexical_control_tokens.json']},state='APPROVED_FOR_S08_BY_CURRENT_USER',scientific_acceptance='Unknown'))
for name,text in [('identification','Dataset-label association, not knowledge causality; question field only, source/template/token/topic/truncation rivals retained.'),('data','Equal257documents/source, fixed balanced pair graphs. Document bootstrap/permutations preserve all positions and repeated edges. Controls fixed before responses, all pairs/SAEs reported.'),('implementation','Same frozen official model/nativeSAE hashes, CPUFP32/2threads,8x128. Hook/noop/prefix-equivalence, native support and pair arithmetic checked; no training telemetry applicable.')]: (R/'evidence'/('audit_'+name+'.md')).write_text('# '+name+'\n\n'+text+'\n')
print('S08_FROZEN',len(panel),availability,'lengthcontrols',[(c['A'],c['B'],c['mode'],c['N']) for c in controls],'lexical',lexsets,flush=True)
