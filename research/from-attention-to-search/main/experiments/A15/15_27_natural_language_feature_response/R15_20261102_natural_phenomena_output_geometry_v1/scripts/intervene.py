from pathlib import Path
import os,sys,json,hashlib,time
import numpy as np,pandas as pd,torch
from safetensors import safe_open
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));F=json.load(open(E/'validation_selection_frozen.json'));DOC=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];LABEL=pd.read_json(E/'data/labels_effective_v1p2.jsonl',lines=True);torch.set_num_threads(2)
if not F['conditional_interventions']:
 json.dump({'status':'NOT_RUN_BY_PROTOCOL','reason':'no development-supported explanation;no replacement synthetic task'},open(E/'audit/intervention_receipt.json','w'),indent=2);print('NO_SUPPORTED_DEV_INTERVENTION');sys.exit(0)
P=dict(np.load(E/'analysis/pca.npz'));G=dict(np.load(E/'analysis/head_geometry.npz'));D=np.load(E/'data/decoder_last_scale.npz')['D'];grp=json.load(open(E.parent/'R14_20261102_concept_specificity_v1/data/feature_groups.json'))
# Input-label-only choice before reading any validation result table.
selection=[]
for c in F['conditional_interventions']:
 flag=c['phenomenon'];pool=[]
 for doc in DOC:
  if doc['split']!='validation':continue
  ids=np.array(doc['token_ids'])[doc['positions']];start=doc['row_start'];labels=LABEL.iloc[start:start+len(ids)][flag].to_numpy(bool);used=set()
  for j in np.flatnonzero(labels):
   neg=[k for k in np.flatnonzero(~labels) if k not in used and ids[k]==ids[j]]
   if not neg:continue
   k=min(neg,key=lambda k:(abs(doc['positions'][k]-doc['positions'][j]),k));used.add(k);h=hashlib.sha256(f'110206:{flag}:{doc["doc_id"]}:{doc["positions"][j]}'.encode()).hexdigest();pool.append((h,doc,int(j),int(k)))
 chosen=[];used_docs=set()
 for h,doc,j,k in sorted(pool,key=lambda x:x[0]):
  if doc['doc_id'] in used_docs:continue
  used_docs.add(doc['doc_id'])
  for index,v in [(j,True),(k,False)]:chosen.append({'phenomenon':flag,'feature':c['feature'],'band':c['band'],'doc_id':doc['doc_id'],'local_index':index,'row':doc['row_start']+index,'positive':v,'pair_hash':h,'same_current_token_control':True})
  if len(chosen)>=128:break
 for x in chosen:
  for seed in cfg['random_seeds']:
   group=next(k for k in ['low','middle','high'] if c['feature'] in grp[k]);x['random_member_'+str(seed)]=min((f for f in grp[group] if f!=c['feature']),key=lambda f:hashlib.sha256(f'{seed}:{c["feature"]}:{f}'.encode()).hexdigest())
 selection+=chosen
selection_path=E/'data/intervention_positions_frozen.json'
if selection_path.exists():assert json.load(open(selection_path))==selection
else:selection_path.write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
with safe_open(cfg['model']+'/model.safetensors',framework='pt',device='cpu') as f:
 key='lm_head.weight' if 'lm_head.weight' in f.keys() else 'model.embed_tokens.weight';W=f.get_tensor(key).to(torch.bfloat16)
weight=torch.tensor(G['final_norm_weight'],dtype=torch.bfloat16);eps=float(G['norm_eps'])
def norm(h):
 x=h.to(torch.bfloat16);fp=x.float();return weight*(fp*torch.rsqrt(fp.pow(2).mean(-1,keepdim=True)+eps)).to(torch.bfloat16)
def head(h):
 n=len(h);x=torch.zeros((512,1024),dtype=torch.bfloat16);x[:n]=norm(h);return (x@W.T)[:n].float()
def sparse_get(cache,j,f):
 lo,hi=cache['z_indptr'][j:j+2];ix=cache['z_indices'][lo:hi];loc=np.flatnonzero(ix==f);return float(cache['z_values'][lo+loc[0]]) if len(loc) else 0.
rows=[];smoke=[];t=time.time()
for spec in F['conditional_interventions']:
 chosen=[x for x in selection if x['phenomenon']==spec['phenomenon']];H=[];Y=[];targets=[];vectors={};zeros=[]
 a,b=cfg['bands'][spec['band']];Q=P['h_V'][:,a:b]
 for x in chosen:
  doc=next(d for d in DOC if d['doc_id']==x['doc_id']);cache=np.load(E/'cache'/(x['doc_id']+'.npz'));j=x['local_index'];h=cache['h'][j].astype(np.float64);H.append(h);Y.append(cache['y'][j]);targets.append(doc['token_ids'][doc['positions'][j]+1]);z=sparse_get(cache,j,spec['feature']);v=z*D[spec['feature']].astype(np.float64);band=(h-P['h_mean'])@Q@Q.T;vv={'feature_delete':v,'band_delete':band}
  for seed in cfg['random_seeds']:
   member=x['random_member_'+str(seed)];zr=sparse_get(cache,j,member);vr=zr*D[member].astype(np.float64);rq=P['random_'+str(seed)][:,:b-a];rb=(h-P['h_mean'])@rq@rq.T;vv['random_member_'+str(seed)]=vr;vv['random_band_'+str(seed)]=rb
   for name,target,control in [('feature',v,vr),('band',band,rb)]:
    nn=np.linalg.norm(control);nt=np.linalg.norm(target);vv[name+'_normmatch_'+str(seed)]=control*(nt/nn) if nn>0 else np.zeros(1024);zeros.append({'row':x['row'],'target':name,'seed':seed,'target_nonzero':bool(nt>0),'random_zero':bool(nn==0),'unmatched':bool(nn==0 and nt>0)})
   # Isotropic finite perturbation reference remains defined if random feature was inactive.
   unit=np.random.default_rng(int(hashlib.sha256(f'{seed}:{x["row"]}'.encode()).hexdigest()[:8],16)).normal(size=1024);unit/=np.linalg.norm(unit);vv['isotropic_feature_normmatch_'+str(seed)]=unit*np.linalg.norm(v)
  for k,val in vv.items():vectors.setdefault(k,[]).append(val)
 H=np.array(H);Y=np.array(Y);targets=np.array(targets);N=len(H);ref=[]
 for lo in range(0,N,64):
  h=torch.tensor(H[lo:lo+64]);y=norm(h).float().numpy();smoke.append(float(np.max(abs(y-Y[lo:lo+64]))));ref.append(torch.log_softmax(head(h),1).numpy())
 ref=np.concatenate(ref);names={'identity':np.zeros_like(H),**{k:np.array(v) for k,v in vectors.items()}}
 for name,v in names.items():
  for lo in range(0,N,64):
   lp=torch.log_softmax(head(torch.tensor(H[lo:lo+64]-v[lo:lo+64])),1).numpy();prob=np.exp(lp);full=ref[lo:lo+len(lp)];delta=H[lo:lo+len(lp)]-(H[lo:lo+len(lp)]-v[lo:lo+len(lp)]).astype(np.float32).astype(np.float64);kl=np.sum(np.exp(full)*(full-lp),1);ent=-np.sum(prob*lp,1)
   centered_change=lp-full;centered_change-=centered_change.mean(1,keepdims=True);logit_rms=np.sqrt(np.mean(centered_change**2,1));dy=norm(torch.tensor(H[lo:lo+len(lp)]-v[lo:lo+len(lp)])).float().numpy()-Y[lo:lo+len(lp)];ynorm=np.linalg.norm(dy,axis=1)
   for j in range(len(lp)):
    x=chosen[lo+j];target=targets[lo+j];top=np.argsort(-lp[j],kind='stable')[:5];rows.append({**x,'condition':name,'next_token':int(target),'next_token_log_probability':float(lp[j,target]),'full_next_token_log_probability':float(full[j,target]),'next_NLL_loss':float(full[j,target]-lp[j,target]),'KL_full_to_condition':float(kl[j]),'entropy':float(ent[j]),'finite_delta_y_norm':float(ynorm[j]),'finite_centered_logit_RMS':float(logit_rms[j]),'finite_output_gain':float(logit_rms[j]/max(ynorm[j],1e-12)),'target_perturbation_norm':float(np.linalg.norm(v[lo+j])),'applied_BF16_perturbation_norm':float(np.linalg.norm(H[lo+j]-torch.tensor(H[lo+j]-v[lo+j]).to(torch.bfloat16).float().numpy())),'top5_token_ids':json.dumps(top.tolist()),'top5_probabilities':json.dumps(np.exp(lp[j,top]).tolist())})
 pd.DataFrame(zeros).to_csv(E/'analysis'/('intervention_zeros_'+spec['phenomenon']+'.csv'),index=False)
assert max(smoke)==0,('norm module mismatch',max(smoke))
R=pd.DataFrame(rows);R.to_csv(E/'analysis/intervention_position_results.csv',index=False);Ddoc=R.groupby(['phenomenon','condition','doc_id','positive'],as_index=False)[['next_NLL_loss','KL_full_to_condition','target_perturbation_norm','applied_BF16_perturbation_norm','finite_delta_y_norm','finite_centered_logit_RMS','finite_output_gain']].mean();Ddoc.to_csv(E/'analysis/intervention_document_results.csv',index=False);summary=[]
for (flag,c,positive),q in Ddoc.groupby(['phenomenon','condition','positive']):
 for metric in ['next_NLL_loss','KL_full_to_condition','target_perturbation_norm']:
  v=q[metric].to_numpy();boot=v[np.random.default_rng(110204).integers(0,len(v),(2000,len(v)))].mean(1);lo,hi=np.quantile(boot,[.025,.975]);summary.append({'phenomenon':flag,'condition':c,'positive':positive,'metric':metric,'mean':v.mean(),'low95':lo,'high95':hi,'documents':len(v)})
pd.DataFrame(summary).to_csv(E/'analysis/intervention_summary.csv',index=False);json.dump({'status':'COMPLETED','new_transformer_forwards':0,'positions':len(selection),'phenomena':len(F['conditional_interventions']),'norm_replay_max':max(smoke),'seconds':time.time()-t,'not_free_generation':True},open(E/'audit/intervention_receipt.json','w'),indent=2);print('INTERVENTION_COMPLETE',len(selection),time.time()-t,flush=True)
