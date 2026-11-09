"""TRAIN-only support diagnosis for the already-reported token; no candidate search/inference."""
from pathlib import Path
import json,hashlib,collections,csv
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder');O=E/'analysis/context_dependency_20261026/design_review';D=E/'analysis/sft_route_learning/20261019T012300Z/data/train.jsonl';v=304;ya=279;yb=264
assert hashlib.sha256(D.read_bytes()).hexdigest()=='5530f9676c3d7941150e404c045ad62815a11310d8b1ec4904c209121ddb8ad5'
rows=[json.loads(l) for l in D.open()];early=[];valid=[]
for row in rows:
 ids=row['input_ids'];a0=row['answer_start']
 for t in range(a0-1,len(ids)-1):
  if ids[t]!=v:continue
  r={'y':ids[t+1],'doc':row['prompt_sha256'],'dataset':row['dataset'],'t':t,'answer_bin':(t-(a0-1))//16,'prefix_bin':(t+1)//32}
  early.append(r)
  if len(ids)-t-1>=16 and t+17<=512:valid.append(r)
def counts(rs):
 return {str(y):{'occurrences':sum(r['y']==y for r in rs),'unique_dialogues':len({r['doc'] for r in rs if r['y']==y})} for y in [ya,yb]}
def rank(r):return hashlib.sha256(f"20261026|{r['doc']}|{r['t']}|304".encode()).hexdigest()
g=collections.defaultdict(list)
for r in valid:g[r['doc']].append(r)
one=[min(rs,key=rank) for rs in g.values()]
def match(rs,keys):
 strata=collections.defaultdict(lambda:{ya:[],yb:[]})
 for r in rs:
  if r['y'] in [ya,yb]:strata[tuple(r[k] for k in keys)][r['y']].append(r)
 return sum(min(len(s[ya]),len(s[yb])) for s in strata.values())
stages=[{'stage':'01same_token_two_fixed_targets_before_16_future_filter',**{f'{c}_{metric}':q for c,vals in counts(early).items() for metric,q in vals.items()}},{'stage':'02require_16_future_targets_and_512_complete_prefix',**{f'{c}_{metric}':q for c,vals in counts(valid).items() for metric,q in vals.items()}},{'stage':'03one_position_per_token_per_dialogue_fixed_SHA',**{f'{c}_{metric}':q for c,vals in counts(one).items() for metric,q in vals.items()}}]
assert counts(one)['279']['unique_dialogues']==91 and counts(one)['264']['unique_dialogues']==43
balanced={'source_only':match(one,['dataset']),'source_and_answer_position_bin16':match(one,['dataset','answer_bin']),'source_and_answer_position16_and_prefix_length32':match(one,['dataset','answer_bin','prefix_bin'])};assert balanced['source_and_answer_position16_and_prefix_length32']==23
out={'scope':'posthoc feasibility diagnosis, not intervention experiment or power analysis','token_id':304,'token':' in','fixed_targets':{'279':' the','264':' a'},'data_sha256':hashlib.sha256(D.read_bytes()).hexdigest(),'stages':stages,'matched_dialogues_each_class':balanced,'independence_boundary':'distinct first-user-prompt hashes, not proven statistical independence','model_forwards':0,'EVAL_TEST_read':False,'original_protocol_modified':False,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(O/'support_decomposition.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
