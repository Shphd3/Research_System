"""Actual residual-preserving last-block interventions with full-hook equivalence checks."""
from common import *
import numpy as np,torch,torch.nn.functional as F,sys,importlib.util,time,math,os
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
 for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
from scipy import sparse
plan=json.load(open(R/'frozen_plan.json'));selection=json.load(open(R/'data/selection.json'));pp=rows(R/'data/panel.jsonl');rng=np.random.default_rng(plan['seed']);start=time.time()
for f,h in json.load(open(R/'evidence/protocol_freeze.json'))['hashes'].items():assert sha(f)==h
assert not (R/'results/conditions.jsonl').exists(),'Do not overwrite existing intervention responses'
torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(plan['seed'])
model=AutoModelForCausalLM.from_pretrained(plan['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False);model.config.use_cache=False
layer=model.model.layers[27];saes={};D={};metadata={};tok=Tokenizer.from_file(plan['model']+'/tokenizer.json')
for s,ss in plan['sites'].items():
 assert sha(ss['path'])==ss['sha256'];spec=importlib.util.spec_from_file_location('s07_'+s,ss['loader']);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);sae=mod.TopKSAE.from_pretrained(ss['path'],map_location='cpu').eval().requires_grad_(False);saes[s]=sae;D[s]=sae.decoder.weight.detach().numpy().copy()
 metadata[s]=dict(decoder_column_norm_min=float(np.linalg.norm(D[s],axis=0).min()),decoder_column_norm_max=float(np.linalg.norm(D[s],axis=0).max()),decoder_bias_norm=float(sae.decoder.bias.norm()),decoder_shape=list(D[s].shape),column_renormalized=False,injection_bias=False,hook=ss['hook'])
dump(R/'evidence/decoder_identity.json',metadata);dump(R/'evidence/started.json',dict(UTC=now(),pid=os.getpid(),device='CPU',threads=2,code_sha256=sha(__file__),selection_sha256=sha(R/'data/selection.json')))
wordlabels=['cat','dog','car','bicycle'];wordids=torch.tensor([8251,5562,1803,34986]);mainb={p['id']:p for p in rows(MAIN/'data/behavior_all.jsonl')};allmain=rows(MAIN/'data/panel.jsonl');mi={p['id']:i for i,p in enumerate(allmain)};mainz={s:sparse.load_npz(MAIN/f'data/{s}_all_z_csr.npz').toarray() for s in SITES}
@torch.inference_mode()
def native(p,site=None,delta=None):
 n=len(p['token_ids']);xx=torch.zeros(4,128,dtype=torch.long);mask=torch.zeros_like(xx);cap={}
 for j,c in enumerate(p['candidates']):xx[j,:len(c['full_ids'])]=torch.tensor(c['full_ids']);mask[j,:len(c['full_ids'])]=1
 hooks=[]
 def bpre(m,a):cap['r']=a[0][:,n-1].detach().clone()
 def attn(m,a,y):
  cap['attn']=y[:,n-1].detach().clone()
  if site=='ATTN_SAE':
   yy=y.clone();yy[:,n-1]+=torch.as_tensor(delta);return yy
 def mlpin(m,a):
  cap['mlpin']=a[0][:,n-1].detach().clone()
  if site=='MLPIN_SAE':
   x=a[0].clone();x[:,n-1]+=torch.as_tensor(delta);return (x,)
 hooks=[layer.register_forward_pre_hook(bpre),layer.self_attn.o_proj.register_forward_hook(attn),layer.mlp.register_forward_pre_hook(mlpin)]
 try:hh=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state
 finally:
  for h in hooks:h.remove()
 lp=model.lm_head(hh[:,n-1:n+1]).float().log_softmax(-1);first=lp[0,0];period=lp[:,1,13];scores=first[wordids].double()+period.double()
 cap={k:v[0].numpy() for k,v in cap.items()};cap['final']=hh[0,n-1].numpy();return cap,first.numpy(),period.numpy(),scores.numpy()
@torch.inference_mode()
def tail(base,site,delta):
 delta=torch.as_tensor(delta,dtype=torch.float32);delta=delta.reshape(-1,1024);n=len(delta);rs=torch.as_tensor(base['r']+base['attn']).expand(n,-1)
 if site=='ATTN_SAE':rr=rs+delta;out=rr+layer.mlp(layer.post_attention_layernorm(rr))
 else:out=rs+layer.mlp(torch.as_tensor(base['mlpin']).expand(n,-1)+delta)
 return model.lm_head(model.model.norm(out)).float().log_softmax(-1)

baselines=[];coords={};basepack={};maxreplay=0;maxz=0
for j,p in enumerate(pp):
 cap,lp,period,scores=native(p);expected=np.array([c['total_logprob'] for c in mainb[p['id']]['candidates']]);err=float(np.max(abs(scores.astype(float)-expected)));maxreplay=max(maxreplay,err);assert err<1e-4,(p['id'],err)
 for s in SITES:
  h=cap['attn' if s=='ATTN_SAE' else 'mlpin']
  with torch.inference_mode():zz=saes[s].encode_topk(torch.tensor(h).reshape(1,-1))[2].numpy()[0]
  ze=float(abs(zz-mainz[s][mi[p['id']]]).max());maxz=max(maxz,ze);assert ze<1e-4
  coords[(p['id'],s)]=zz
 basepack[p['id']]=dict(**cap,period=period,scores=scores)
 baselines.append(dict(id=p['id'],scores=scores.tolist(),period_logp=period.tolist(),word_logp=lp[wordids.numpy()].tolist()))
 if (j+1)%16==0:print('BASE',j+1,'/96',round(time.time()-start,1),flush=True)
np.savez_compressed(R/'cache/baseline_tail.npz',ids=np.array([p['id'] for p in pp]),**{k:np.array([basepack[p['id']][k] for p in pp]) for k in ['r','attn','mlpin','final','period','scores']})
jsonl(R/'data/native_baselines.jsonl',baselines)

def move(v,t,a):
 r=float(np.linalg.norm(v))
 if r==0:return v.copy()
 w=(1-a)*v/r+a*np.array(t);n=np.linalg.norm(w);return v.copy() if n==0 else r*w/n
def changed(ids,original,new):return (np.asarray(new)-original[ids])@D[current_site][:,ids].T
def matched_move(v,t,ids,target_norm,site):
 grid=np.linspace(0,1,65);vv=np.array([move(v,t,a) for a in grid]);deltas=(vv-v)@D[site][:,ids].T;norms=np.linalg.norm(deltas,axis=1);j=int(np.argmin(abs(norms-target_norm)))
 crossing=next((k for k in range(64) if (norms[k]-target_norm)*(norms[k+1]-target_norm)<=0),None)
 if crossing is not None:
  lo,hi=grid[crossing],grid[crossing+1]
  for _ in range(20):
   mid=(lo+hi)/2;nn=np.linalg.norm((move(v,t,mid)-v)@D[site][:,ids].T)
   if nn<target_norm:lo=mid
   else:hi=mid
  a=(lo+hi)/2
 else:a=float(grid[j])
 new=move(v,t,a);norm=float(np.linalg.norm((new-v)@D[site][:,ids].T));return new,a,norm
def make_edits(p,s,d):
 ss=selection[s][d];original=coords[(p['id'],s)];groups=ss['groups'];labels=DOMAINS[d];common=groups['common'];out=[]
 def add(arm,group,ids,new,alpha=None,destination=None,reference=None,qualified=True,beta=None):
  old=original[ids];delta=(np.array(new)-old)@D[s][:,ids].T;norm=float(np.linalg.norm(delta));support=bool(np.array_equal(old>0,np.array(new)>0));ranges=ss['discovery_ranges'];lower=np.minimum(ranges[labels[1]]['min'],ranges[labels[2]]['min']);upper=np.maximum(ranges[labels[1]]['max'],ranges[labels[2]]['max']);outside=None if ids!=common else int(((np.array(new)<lower-1e-6)|(np.array(new)>upper+1e-6)).sum())
  rec=dict(text_id=p['id'],site=s,intervention_domain=d,arm=arm,group=group,alpha=alpha,destination=destination,beta=beta,feature_ids=list(ids),old_z=old.tolist(),new_z=np.asarray(new).tolist(),old_group_L2=float(np.linalg.norm(old)),new_group_L2=float(np.linalg.norm(new)),active_before=int((old>0).sum()),active_after=int((np.array(new)>0).sum()),deleted_active=int(((old>0)&(np.array(new)==0)).sum()),support_preserved=support,delta_hidden_L2=norm,reference_norm=reference,norm_ratio=None if reference is None or reference==0 else norm/reference,discovery_matched=bool(qualified),outside_discovery_coordinates=outside)
  out.append((rec,delta.astype(np.float32)))
 add('identity','none',[],[],alpha=0)
 for group,ids in groups.items():
  add('delete',''+group,ids,np.zeros(len(ids)));target=out[-1][0]['delta_hidden_L2'];matched=ss['matched_controls'][group];ci=matched['ids'];add('delete_matched',group,ci,np.zeros(len(ci)),reference=target,qualified=matched['qualified'])
  # Same number of actually active coordinates; explicit positive-addition norm reference, not deletion.
  m=int((original[ids]>0).sum());pool=np.array([i for i in np.flatnonzero(original>0) if i not in set(ids)]);choose=rng.choice(pool,min(m,len(pool)),replace=False).tolist() if m else []
  vv=abs(rng.standard_normal(len(choose)));dv=vv@D[s][:,choose].T if choose else np.zeros(1024);fac=target/np.linalg.norm(dv) if np.linalg.norm(dv)>0 else 0;add('norm_random_add',group,choose,original[choose]+fac*vv,reference=target)
 for dest in labels[1:]:
  own=labels[1] if dest==labels[2] else labels[2];typ=ss['typical'][dest];v=original[common]
  for alpha in [.25,.5,1.]:
   new=move(v,typ,alpha);add('strength','common',common,new,alpha,dest);target=out[-1][0]['delta_hidden_L2']
   st=np.array(typ)[ss['component_shuffle']];mv,beta,nn=matched_move(v,st,common,target,s);add('strength_shuffle','common',common,mv,alpha,dest,target,True,beta)
   mv,beta,nn=matched_move(v,ss['typical'][own],common,target,s);add('strength_own','common',common,mv,alpha,dest,target,True,beta)
   ci=ss['matched_controls']['common']['ids'];mv,beta,nn=matched_move(original[ci],ss['other_typical'][dest],ci,target,s);add('strength_other','common',ci,mv,alpha,dest,target,ss['matched_controls']['common']['qualified'],beta)
   if alpha==.5:
    diff=abs(np.array(ss['typical'][labels[2]])-np.array(ss['typical'][labels[1]]));a=int(np.argmax(diff));add('strength_single','common',[common[a]],[new[a]],alpha,dest)
 return out

# Full-hook numerical calibration precedes any batch of effects; only prescribed families/conditions.
cal=[]
for label in ['cat','car']:
 p=next(p for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==label);d=p['domain']
 for s in SITES:
  all_edits=make_edits(p,s,d);dest=next(c for c in DOMAINS[d][1:] if c!=label)
  checks=[next(v for v in all_edits if v[0]['arm']=='identity'),next(v for v in all_edits if v[0]['arm']=='delete' and v[0]['group']=='common'),next(v for v in all_edits if v[0]['arm']=='strength' and v[0]['destination']==dest and v[0]['alpha']==.5)]
  for rec,delta in checks:
   _,lp,period,score=native(p,s,delta);tlp=tail(basepack[p['id']],s,delta)[0].numpy();ts=tlp[wordids.numpy()]+basepack[p['id']]['period'];err=float(abs(ts-score).max());pe=float(abs(period-basepack[p['id']]['period']).max());assert err<1e-4 and pe<1e-4,(s,rec,err,pe);cal.append(dict(id=p['id'],site=s,arm=rec['arm'],max_complete_score_error=err,max_period_change=pe,delta_norm=rec['delta_hidden_L2']))
dump(R/'evidence/calibration.json',dict(UTC=now(),status='PASS',records=cal,max_main_baseline_error=maxreplay,max_main_z_error=maxz,tail_is_exact_final_block=True))
print('CALIBRATION_PASS',max(r['max_complete_score_error'] for r in cal),flush=True)
# Reset control RNG: calibration cannot shift the registered control draw stream.
rng=np.random.default_rng(plan['seed']);hdelta=[];conditionids=[];keydeltas=[];keyids=[];maxnormerr=0.;counts=0
with (R/'results/conditions.jsonl').open('x') as of,(R/'results/top20.jsonl').open('x') as tf:
 for pi,p in enumerate(pp):
  base=basepack[p['id']];base_lp=model.lm_head(torch.tensor(base['final']).reshape(1,-1)).float().log_softmax(-1).detach()[0];base_scores=torch.tensor(base['scores']);gold=p['behavior_gold'];global_siblings=DOMAINS[p['domain']][1:] if gold else None
  for s in SITES:
   for d,labels in DOMAINS.items():
    edits=make_edits(p,s,d);all_delta=np.stack([v[1] for v in edits]);all_logp=[]
    for lo in range(0,len(edits),32):all_logp.append(tail(base,s,all_delta[lo:lo+32]))
    all_logp=torch.cat(all_logp,0)
    for ei,(rec,delta) in enumerate(edits):
     lp=all_logp[ei];prob=lp.exp();scores=lp[wordids].double()+torch.tensor(base['period']).double();q4=scores.softmax(0);ranks=[1+int((lp>lp[a]).sum()) for a in wordids];vl,vid=lp.topk(20);kl=float((prob.double()*(lp-base_lp).double()).sum());entropy=float(-(prob.double()*lp.double()).sum());scorelist=scores.tolist();choice=wordlabels[int(scores.argmax())]
     score_by=dict(zip(wordlabels,scorelist));base_by=dict(zip(wordlabels,base['scores'].tolist()));margin=None if gold is None else score_by[gold]-score_by[next(a for a in global_siblings if a!=gold)];base_margin=None if gold is None else base_by[gold]-base_by[next(a for a in global_siblings if a!=gold)]
     cid=f'{p["id"]}__{s}__{d}__{ei:03d}';record=dict(condition_id=cid,**rec,family=p['family'],wording=p['wording'],label=p['label'],text_domain=p['domain'],gold=gold,baseline_scores=base['scores'].tolist(),scores=scorelist,candidate_order=wordlabels,candidate_vocab_token_ids=wordids.tolist(),candidate_vocab_ranks=ranks,candidate_vocab_prob=prob[wordids].tolist(),candidate_sequence_prob4=q4.tolist(),choice4=choice,correct4=None if gold is None else choice==gold,sibling_correct=None if gold is None else margin>0,correct_sibling_margin=margin,baseline_correct_margin=base_margin,correct_margin_change=None if gold is None else margin-base_margin,intervention_domain_margin=score_by[labels[2]]-score_by[labels[1]],baseline_intervention_domain_margin=base_by[labels[2]]-base_by[labels[1]],KL_new_vs_baseline=kl,entropy_nats=entropy,top20_mass=float(vl.exp().sum()),tail_mass=float(1-vl.exp().sum()),period_terms_unchanged=True)
     of.write(json.dumps(record,ensure_ascii=False,allow_nan=False)+'\n');tf.write(json.dumps(dict(condition_id=cid,top=[dict(rank=k+1,token_id=int(a),token_piece=tok.id_to_token(int(a)),decoded=tok.decode([int(a)]),p_vocab=float(v.exp())) for k,(a,v) in enumerate(zip(vid,vl))]),ensure_ascii=False)+'\n');hdelta.append(delta);conditionids.append(cid);counts+=1
     if p['family']=='F09' and p['wording']=='explicit' and p['label'] in ['cat','car'] and rec['arm'] in ['identity','delete','strength','strength_shuffle']:keydeltas.append(delta);keyids.append(cid)
  of.flush();tf.flush()
  if (pi+1)%8==0:print('INTERV',pi+1,'/96','conditions',counts,'seconds',round(time.time()-start,1),flush=True)
np.savez_compressed(R/'cache/all_injected_deltas.npz',condition_ids=np.array(conditionids),delta_hidden=np.array(hdelta));np.savez_compressed(R/'data/key_injected_deltas.npz',condition_ids=np.array(keyids),delta_hidden=np.array(keydeltas))
for f,h in json.load(open(R/'evidence/main_immutable_before.json')).items():assert sha(f)==h,('main modified',f)
dump(R/'evidence/run_complete.json',dict(UTC=now(),status='COMPLETED',prefixes=96,conditions=counts,seconds=time.time()-start,calibration_full_forward_calls=len(cal),main_baseline_forwards=96,tail_batch_max32=True,CPU_threads=2,GPU=0,model_trainable=0,SAE_trainable=0,weights_modified=False,main_files_unchanged=True,code_sha256=sha(__file__),conditions_sha256=sha(R/'results/conditions.jsonl'),top20_sha256=sha(R/'results/top20.jsonl')))
print('S07_COMPLETE',counts,time.time()-start,flush=True)
