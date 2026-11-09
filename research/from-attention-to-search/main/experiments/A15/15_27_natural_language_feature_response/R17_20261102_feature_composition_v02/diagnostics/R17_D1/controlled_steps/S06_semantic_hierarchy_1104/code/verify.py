from common import *
import numpy as np,math,subprocess,sys,itertools
pp=rows(R/'data/panel.jsonl');ix={p['id']:i for i,p in enumerate(pp)};checks=[]
def check(name,ok,detail):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));assert ok,(name,detail)
freeze=json.load(open(R/'evidence/protocol_freeze.json'))
for f,h in freeze['hashes'].items():check('frozen '+Path(f).name,sha(f)==h,'Original protocol/config/panel bytes preserved')
old=json.load(open(R/'evidence/old_immutable_before.json'));bad=[f for f,h in old.items() if sha(f)!=h];check('old S02-S05 immutable',not bad,dict(files=len(old),changed=bad))
gate=json.load(open(R/'evidence/candidates_frozen.json'));check('selection unchanged',sha(R/'results/selection.json')==gate['selection_sha256'],gate['UTC'])
start=json.load(open(R/'evidence/remaining_started.json'));check('candidate before remaining',gate['UTC']<start['UTC'],dict(freeze=gate['UTC'],remaining=start['UTC']))
ids=[];minpos=[];maxledger=0
for stage in ['discovery','remaining']:
 a=np.load(R/f'cache/{stage}.npz');ids.extend(a['ids'].tolist());check(stage+' source',sha(R/f'cache/{stage}.npz')==json.load(open(R/f'evidence/{stage}_complete.json'))['cache_sha256'],'actual output SHA')
 for s in SITES:
  z=a[s+'__z'];pre=a[s+'__pre'];ii=np.argsort(np.maximum(pre,0),axis=1)[:,-32:];replay=np.zeros_like(z);np.put_along_axis(replay,ii,np.take_along_axis(np.maximum(pre,0),ii,axis=1),axis=1)
  check(stage+' '+s+' Top32 from full pre',np.array_equal(z,replay),dict(max_error=float(abs(z-replay).max()),positive_counts=np.unique((z>0).sum(1)).tolist()))
  check(stage+' '+s+' all finite',all(np.isfinite(a[s+'__'+k]).all() for k in ['h','z','pre','reconstruction_relative_L2']),'full inputs and observations')
check('panel exact384',len(ids)==384 and len(set(ids))==384 and set(ids)==set(ix),dict(observed=len(ids)))
behavior=rows(R/'data/behavior_all.jsonl');check('all behavior rows',len(behavior)==384 and {r['id'] for r in behavior}==set(ix),'none excluded')
for r in behavior:
 p=pp[ix[r['id']]];scores={c['label']:math.fsum(c['token_logprobs']) for c in r['candidates']}
 check('scores '+r['id'],all(abs(scores[c['label']]-c['total_logprob'])<1e-10 and len(c['token_logprobs'])==len(c['token_ids'])==2 for c in r['candidates']),'two token sums')
 if r['gold'] is None:check('no invented gold '+r['id'],r['correct4'] is None and r['sibling_correct'] is None,'parent/negative')
pc=subprocess.run([sys.executable,str(R/'code/reproduce_portable.py'),str(R)],capture_output=True,text=True);check('portable independent numeric replay',pc.returncode==0,pc.stdout+pc.stderr)
parts=list(csv.DictReader(open(R/'results/difference_decomposition.csv')));groups={}
for r in parts:groups.setdefault((r['site'],r['domain'],r['family'],r['wording'],r['pair']),[]).append(r)
maxerr=max(abs(sum(float(r['squared_norm']) for r in rr)-float(rr[0]['total_squared_norm'])) for rr in groups.values());check('paired energy closure',maxerr<1e-9,dict(groups=len(groups),max_error=maxerr))
primary=json.load(open(R/'results/primary.json'));check('eight primary tests',len(primary)==8,'H1/H2 x domains x SAE')
ordered=sorted(primary,key=lambda x:x['p']);prev=0
for j,r in enumerate(ordered):
 prev=max(prev,min(1.,r['p']*(8-j)));check('Holm '+r['site']+r['domain']+r['hypothesis'],abs(prev-r['p_holm'])<1e-12,'independent monotone replay')
check('suffix exact',all(p['suffix']=='\nDescription:' and p['target_token_id']==25 for p in pp),'all384')
check('no frame split leak',all(len({p['split'] for p in pp if p['family']==f'F{i:02d}'})==1 for i in range(1,17)),'all conditions grouped')
check('property no literal targets',not any(p['literal_target_words'] for p in pp if p['wording']=='property'),'128property rows')
# Absolute positions are exactly controlled for explicit swaps; report other wording ranges honestly.
position=[]
for w in ['explicit','synonym','property']:
 for f in [f'F{i:02d}' for i in range(1,17)]:
  ps=[p for p in pp if p['family']==f and p['wording']==w];position.append(dict(family=f,wording=w,min_index=min(p['target_index_zero_based'] for p in ps),max_index=max(p['target_index_zero_based'] for p in ps),all8same=len(set(p['target_index_zero_based'] for p in ps))==1))
table(R/'evidence/position_audit.csv',position)
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',checks=len(checks),failed=0,old_files_verified=len(old),records=checks,portable_stdout=pc.stdout,paired_energy_max_error=maxerr))
print('VERIFY_PASS',len(checks),'old',len(old),pc.stdout,flush=True)
