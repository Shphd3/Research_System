"""Frozen TRAIN-only lexical/document eligibility. No model/coder/cache tensor load."""
from pathlib import Path
import json,hashlib,csv,datetime,collections,unicodedata,shutil
from tokenizers import Tokenizer
S=Path('/data/250010109/Research_System');E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder');R=S/'Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026';O=E/'analysis/context_dependency_20261026/execution';V=O/'provenance';T=O/'tables'
for p in [V,T]:p.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def dump(p,rows,keys):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
# Scope/identity freeze precedes reading TRAIN contents/outcomes.
assert not (O/'support_receipt.json').exists(),'completed support discovery; refuse overwrite'
files=[Path(__file__),R/'protocol.md',R/'protocol_cn.md',R/'protocol_config.json',R/'preparation_freeze.json']
write(V/'execution_freeze.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scientific_body':{str(p):sha(p) for p in files},'before_reading_current_discovery_results':True,'authorization':'currentuser继续执行本协议;no training/new resources','operational_resolution':'eligibility counted on unique dialogue positions selected by fixed SHA independent of target;support=min class counts;same-stratum balancing uses fixed SHA;all before results'})
shutil.copy2('/tmp/crosscoder_context_dependency_execution_access_20261026.json',V/'input_access.json')
p=E/'analysis/sft_route_learning/20261019T012300Z/data/train.jsonl';rows=[json.loads(l) for l in p.open()];assert len(rows)==1024
cfg=json.load(open(R/'protocol_config.json'));tokenizer_path=Path('/data/share/Qwen3-0.6B-Base/tokenizer.json');tok=Tokenizer.from_file(str(tokenizer_path));tj=json.load(open(tokenizer_path));special={x['id'] for x in tj.get('added_tokens',[]) if x.get('special')};decoded={}
def text(i):
 if i not in decoded:decoded[i]=tok.decode([i],skip_special_tokens=False)
 return decoded[i]
def rank(x):return hashlib.sha256(f"20261026|{x['dialogue_id']}|{x['position']}|{x['token_id']}".encode()).hexdigest()
valid=[];excluded=collections.Counter();rawpairs=collections.defaultdict(lambda:collections.defaultdict(set));docgroups=collections.defaultdict(list)
for row in rows:
 ids=row['input_ids'];aid=row['id'];a0=row['answer_start'];doc=row['prompt_sha256'];assert isinstance(a0,int)
 for t in range(a0-1,len(ids)-1):
  v,y=ids[t],ids[t+1]
  if v in special or y in special:excluded['special_current_or_next']+=1;continue
  if not any(unicodedata.category(ch).startswith('L') for ch in text(v)):excluded['current_piece_no_unicode_letter']+=1;continue
  if len(ids)-t-1<16:excluded['fewer_than_16_future_answer_targets']+=1;continue
  if t+17>512:excluded['complete_prefix_plus_targets_exceeds_512']+=1;continue
  rec={'token_id':v,'target_id':y,'dialogue_id':doc,'original_id':aid,'dataset':row['dataset'],'position':t,'answer_position':t-(a0-1),'prefix_length':t+1,'position_bin':(t-(a0-1))//16,'prefix_bin':(t+1)//32,'source_file':row['source_file'],'source_row':row['row']}
  valid.append(rec);rawpairs[v][y].add(doc);docgroups[v,doc].append(rec)
# One context per token per dialogue, chosen independent of y/model behavior.
dedup=[min(v,key=rank) for v in docgroups.values()];bytoken=collections.defaultdict(list)
for r in dedup:bytoken[r['token_id']].append(r)
statistics=[];eligible=[];selected_contexts={}
for v,recs in bytoken.items():
 targets=collections.Counter(x['target_id'] for x in recs);ys=sorted(targets,key=lambda y:(-targets[y],y))
 if len(ys)<2:continue
 a,b=ys[:2];strata=collections.defaultdict(lambda:{a:[],b:[]})
 for x in recs:
  if x['target_id'] in [a,b]:strata[(x['dataset'],x['position_bin'],x['prefix_bin'])][x['target_id']].append(x)
 balanced=[];n_common=0
 for key,d in sorted(strata.items()):
  n=min(len(d[a]),len(d[b]))
  if n:n_common+=1
  for y in [a,b]:balanced += sorted(d[y],key=rank)[:n]
 n=len(balanced)//2
 rawys=sorted(rawpairs[v],key=lambda y:(-len(rawpairs[v][y]),y))
 rr={'token_id':v,'token_text':text(v),'target_A':a,'target_A_text':text(a),'target_B':b,'target_B_text':text(b),'dedup_unique_A':targets[a],'dedup_unique_B':targets[b],'min_raw_unique_support_best_two':min(len(rawpairs[v][y]) for y in rawys[:2]) if len(rawys)>=2 else 0,'same_stratum_balanced_unique_each_class':n,'shared_strata':n_common,'eligible_pre_stratum':min(targets[a],targets[b])>=64,'eligible_after_matching':n>=64}
 statistics.append(rr)
 if rr['eligible_after_matching']:
  eligible.append(rr);selected_contexts[v]=balanced
statistics.sort(key=lambda x:(-x['same_stratum_balanced_unique_each_class'],x['token_id']));eligible.sort(key=lambda x:(-x['same_stratum_balanced_unique_each_class'],x['token_id']));chosen=eligible[:2]
dump(T/'token_support_all.csv',statistics,list(statistics[0]) if statistics else ['token_id']);selected=[]
for x in chosen:
 for r in selected_contexts[x['token_id']]:selected.append(r)
if selected:dump(T/'selected_discovery_contexts.csv',selected,list(selected[0]))
receipt={'status':'PASS_DATA_DISCOVERY' if chosen else 'INSUFFICIENT_ELIGIBLE_TOKEN_CONTEXTS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'TRAIN_file':str(p),'TRAIN_sha256':sha(p),'TRAIN_dialogues':len(rows),'valid_positions':len(valid),'unique_token_dialogue_contexts':len(dedup),'exclusions':dict(excluded),'token_types_with_two_targets':len(statistics),'tokens_passing_two_target_64docs_before_stratum':sum(x['eligible_pre_stratum'] for x in statistics),'tokens_passing_matching_and_64docs_each':len(eligible),'required_each_class':64,'best_same_stratum_support':statistics[0] if statistics else None,'largest_pre_stratum_balanced_support':max((min(x['dedup_unique_A'],x['dedup_unique_B']) for x in statistics),default=0),'selected_tokens':chosen,'model_sequence_forwards':0,'model_or_coder_loaded':False,'cache_tensor_loaded':False,'EVAL_or_TEST_read':False,'threshold_relaxed':False,'new_resources_or_training':False,'gate':'stop before C/R feature selection and interventions if no eligible token'}
write(O/'support_receipt.json',receipt)
write(V/'original_input_immutability.json',{'TRAIN_sha256_after':sha(p),'TRAIN_unchanged':sha(p)==receipt['TRAIN_sha256'],'protocol_freeze_unchanged':all(sha(f)==h for f,h in json.load(open(V/'execution_freeze.json'))['scientific_body'].items())})
print(json.dumps(receipt,ensure_ascii=False,indent=2))
