import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,hashlib,math,shutil
import pandas as pd,numpy as np
import sys
sys.path.insert(0,'/data/250010109/dependency_packages/hf_transformers_qwen3')
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);V=json.load(open(E/'audit/validation.json'));rr=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];docs={r['seq_id']:r for r in [json.loads(l) for l in (E/'data/evaluation_documents.jsonl').read_text().splitlines()]};tok=Tokenizer.from_file(str(Path(c['model_dir'])/'tokenizer.json'));visible=0
for r in rr:
 ids=docs[r['seq_id']]['token_ids'];t=r['position'];assert ids[t]==r['input_id'];assert tok.decode(ids[:t+1],skip_special_tokens=False)==r['visible_prefix'];visible+=1
 if t<191:assert ids[t+1]==r['target_id']
 else:assert r['seq_id']=='R11_A02_090' and r['target_id']==34259
count=0;maxnll=0.;zeros=0;maxties=0
for line in (E/'analysis/raw_outputs.jsonl').open():
 r=json.loads(line);ts=r['top10'];assert len(ts)==10 and ts[0]['id']==r['top1_id'];assert all(0<=x['probability']<=1 for x in ts);assert all(ts[j]['probability']>=ts[j+1]['probability'] for j in range(9));assert r['top1_agreement']==(r['top1_id']==r['full_top1_id']);assert r['KL_full']>=-1e-5 and r['entropy']>=0
 if r['target_probability']>0:maxnll=max(maxnll,abs(-math.log(r['target_probability'])-r['NLL']))
 else:zeros+=1
 maxties=max(maxties,r.get('max_probability_tie_count',0));count+=1
assert count==207097 and maxnll<1e-4,(count,maxnll)
# Sourcefreeze has no model changes and original same reference/version.
for p,h in json.load(open(E/'freeze.json'))['sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
s=pd.read_csv(E/'analysis/position_metrics.csv');a=s[(s.panel=='natural')&(s.condition.isin(['keep_head64','delete_head64']))];regroup=a.groupby(['layer','scope','condition','seq_id'])[['top1_agreement','NLL']].mean().groupby(['layer','scope','condition']).mean();ss=pd.read_csv(E/'analysis/summary_metrics.csv');maxerr=0
for (l,scope,cond),r in regroup.iterrows():
 for metric in ['top1_agreement','NLL']:
  mean=ss[(ss.panel=='natural')&(ss.group=='ALL')&(ss.layer==l)&(ss.scope==scope)&(ss.condition==cond)&(ss.metric==metric)]['mean'].iloc[0];maxerr=max(maxerr,abs(mean-r[metric]))
assert maxerr<1e-10;V.update(all737_visible_prefixes_and_shifts_verified=visible,all_records_top1_from_candidate_probs_consistent=True,max_NLL_vs_saved_target_probability_error=maxnll,underflow_target_probability_records=zeros,max_observed_native_ties=maxties,independent_reaggregation_error=maxerr,source_freeze_unchanged=True)
for b in [P,E]:(b/'audit/validation.json').write_text(json.dumps(V,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(V,indent=2))
