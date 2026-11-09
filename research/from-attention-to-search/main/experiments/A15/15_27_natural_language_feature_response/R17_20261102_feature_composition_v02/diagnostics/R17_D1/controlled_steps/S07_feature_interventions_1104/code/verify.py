from common import *
import numpy as np,torch,math,subprocess,sys
from scipy import sparse
torch.set_num_threads(2)
assert json.load(open(R/'evidence/run_complete.json'))['status']=='COMPLETED';rec=rows(R/'results/conditions.jsonl');plan=json.load(open(R/'frozen_plan.json'));check=[]
for p,h in json.load(open(R/'evidence/protocol_freeze.json'))['hashes'].items():assert sha(p)==h
old=json.load(open(R/'evidence/main_immutable_before.json'));bad=[p for p,h in old.items() if sha(p)!=h];assert not bad,bad
for p,h in plan['input_SHA256'].items():assert sha(p)==h
deltafile=np.load(R/'cache/all_injected_deltas.npz');deltas=deltafile['delta_hidden'];ids=deltafile['condition_ids'];assert len(rec)==len(ids) and len(set(ids))==len(ids)
base=np.load(R/'cache/baseline_tail.npz');bi={x:i for i,x in enumerate(base['ids'])};mainpp=rows(MAIN/'data/panel.jsonl');mi={p['id']:i for i,p in enumerate(mainpp)};maxerr=0.;maxres=0.;maxnorm=0.;actual=[];reencode=[]
for s in SITES:
 ss=plan['sites'][s];assert sha(ss['path'])==ss['sha256'];cp=torch.load(ss['path'],map_location='cpu',mmap=True,weights_only=False);sd=cp['state_dict'];W=sd['decoder.weight'].numpy();bias=sd['decoder.bias'].numpy();oldz=sparse.load_npz(MAIN/f'data/{s}_all_z_csr.npz').toarray()
 for i,r in enumerate(rec):
  if r['site']!=s:continue
  assert ids[i]==r['condition_id'];at=r['feature_ids'];dz=np.array(r['new_z'])-r['old_z'];expected=dz@W[:,at].T;err=float(abs(expected-deltas[i]).max());maxerr=max(maxerr,err);norm=float(np.linalg.norm(deltas[i].astype(float)));maxnorm=max(maxnorm,abs(norm-r['delta_hidden_L2']));actual.append(dict(condition_id=r['condition_id'],actual_float32_injection_L2=norm,declared_float64_construction_L2=r['delta_hidden_L2'],max_coordinate_rounding_error=err))
  if r['family']=='F09' and r['wording']=='explicit' and r['label'] in ['cat','car'] and (r['arm']=='delete' and r['group']=='common' or r['arm']=='strength' and r['alpha']==.5 and r['destination']!=r['label']):
   h=base['attn' if s=='ATTN_SAE' else 'mlpin'][bi[r['text_id']]].astype(float);z0=oldz[mi[r['text_id']]].astype(float);znew=z0.copy();znew[at]=r['new_z'];residual=h-(W@z0+bias);other=W@znew+bias+residual;maxres=max(maxres,float(abs(other-(h+expected)).max()))
   # Diagnostic only: intended latent edit need not be an encoder fixed point.
   hn=torch.tensor((h+deltas[i]).astype(np.float32)).reshape(1,-1)
   with torch.inference_mode():pre=torch.nn.functional.linear(hn,sd['encoder.weight'],sd['encoder.bias']).relu();v,j=pre.topk(32);zz=torch.zeros_like(pre).scatter(-1,j,v).numpy()[0]
   reencode.append(dict(condition_id=r['condition_id'],site=s,label=r['label'],arm=r['arm'],feature_ids=json.dumps(at),intended_z=json.dumps(r['new_z']),reencoded_z=json.dumps(zz[at].tolist()),intended_deleted=r['deleted_active'],reencoded_group_active=int((zz[at]>0).sum()),total_reencoded_active=int((zz>0).sum()),max_group_difference=float(abs(zz[at]-np.array(r['new_z'])).max())))
assert maxerr<1e-4 and maxres<1e-9 and maxnorm<1e-4,(maxerr,maxres,maxnorm)
table(R/'results/actual_injection_norms.csv',actual);table(R/'results/key_reencoding_diagnostic.csv',reencode)
p=subprocess.run([sys.executable,str(R/'code/reproduce_portable.py'),str(R)],capture_output=True,text=True);assert p.returncode==0,p.stdout+p.stderr
table(R/'evidence/verification_checks.csv',[dict(check='all intended decoder deltas vs injected arrays',value=maxerr,passed=True),dict(check='residual algebra closure on fixed F09 cases',value=maxres,passed=True),dict(check='actual injected norm rounding',value=maxnorm,passed=True),dict(check='main file hashes unchanged',value=len(old),passed=True)])
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',conditions=len(rec),main_files_verified=len(old),full_hook_calibration=json.load(open(R/'evidence/calibration.json')),max_decoder_delta_rounding=maxerr,max_residual_preservation_error=maxres,max_hidden_norm_rounding=maxnorm,offline_replay=p.stdout,reencoding_role='posthoc measurement diagnostic only, does not redefine planned decoder-direction intervention or main tests',weights_unchanged=True,protocol_and_selection_unchanged=True))
print('S07_VERIFY_PASS',len(rec),maxerr,maxres,p.stdout,flush=True)
