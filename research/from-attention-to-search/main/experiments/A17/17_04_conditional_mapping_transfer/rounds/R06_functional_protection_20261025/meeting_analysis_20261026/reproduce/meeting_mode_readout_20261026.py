"""Nine existing endpoints, locked64modepairs; no training/update/TEST."""
from pathlib import Path
import importlib.util,json,datetime,time,hashlib,csv,math,os,sys
import numpy as np
import torch
E=Path(__file__).resolve().parents[1];O=E/'analysis/meeting_20261026';V=O/'provenance';cfg=json.load(open(E/'config/frozen.json'));lock=json.load(open(V/'representation_sampling_lock.json'))
spec=importlib.util.spec_from_file_location('r05read',E/'source/retention_r05_v1.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

def dump(name,rs):
 with (O/'tables'/name).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rs[0]));w.writeheader();w.writerows(rs)
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def main():
 deadline=datetime.datetime(2026,10,26,1,40,tzinfo=datetime.timezone.utc).timestamp()
 assert time.time()<deadline,'analysis cutoff reached; no forward'
 device='cuda:0';r.configure(29,device);torch.cuda.set_device(device)
 cache=r.load_cache(cfg,'dev');carrier=r.load_parent(cfg,device);base=carrier.model;model=r.CachedAnswerLM(base);base.eval().requires_grad_(False)
 assert not any(p.requires_grad for p in base.parameters())
 named=dict(base.named_parameters());before_frozen=r.frozen_hash(base,set(r.NAMES));pairs=lock['pairs'];indices=[j for p in pairs for j in [p['old_index'],p['new_index']]];allrows=[];states=[];inputvectors=[];outputvectors=[];summaries=[];sequences=0
 capture={}
 handles=[model.layer.self_attn.q_proj.register_forward_pre_hook(lambda mod,inp:capture.__setitem__('input',inp[0].detach())),model.layer.self_attn.o_proj.register_forward_hook(lambda mod,inp,out:capture.__setitem__('output',out.detach()))]
 try:
  for item in lock['conditions']:
   assert time.time()<deadline,'analysis cutoff reached'
   path=Path(item['checkpoint']);manifest=json.load(open(path.with_suffix('.json')));assert r.sha(path)==manifest['sha256'];saved=torch.load(path,map_location='cpu',weights_only=False);assert saved['optimizer_step']==240 and saved['counters']['new_targets']==8640
   with torch.no_grad():
    for n in r.NAMES:named[n].copy_(saved['trainable_weights'][n].to(device))
   xy={site:[] for site in ['input','output']};logits_all=[];preds=[];losses=[]
   with torch.no_grad():
    for j in range(0,len(indices),16):
     assert time.time()<deadline,'analysis cutoff reached'
     ix=indices[j:j+16];batch=r.cache_batch(cache,ix,device);lengths=batch[2]
     _,logits,ce=model(*batch);ar=torch.arange(len(ix),device=device)
     for site in xy:xy[site].append(capture[site][ar,lengths-1].cpu())
     # Only save two predefined endpoint logits, no large logits dump.
     oldgold=torch.tensor([pairs[(j+n)//2]['old_target_id'] for n in range(len(ix))],device=device);newgold=torch.tensor([pairs[(j+n)//2]['new_target_id'] for n in range(len(ix))],device=device)
     logits_all.extend((logits[ar,oldgold]-logits[ar,newgold]).cpu().tolist());preds.extend(logits.argmax(-1).cpu().tolist());losses.extend(ce.cpu().tolist());sequences+=len(ix)
   x=torch.cat(xy['input']);y=torch.cat(xy['output']);inputvectors.append(x.numpy());outputvectors.append(y.numpy())
   existing=json.load(open(path.parents[1]/'eval_000240.json'));source={z['record_id']:z for z in existing['records']};maxce=0.;predequal=True
   rows=[]
   for i,p in enumerate(pairs):
    oldr=cache['records'][p['old_index']];newr=cache['records'][p['new_index']]
    assert oldr['target_id']==p['old_target_id'] and newr['target_id']==p['new_target_id']
    for pos,rr in [(2*i,oldr),(2*i+1,newr)]:
     predequal &= preds[pos]==source[rr['record_id']]['prediction_id'];maxce=max(maxce,abs(losses[pos]-source[rr['record_id']]['ce']))
    row={k:item[k] for k in ['seed','method','old_slots']};row.update(pair_id=p['old_record_id'],panel=p['panel'],command=p['command'],old_correct=int(preds[2*i]==p['old_target_id']),new_correct=int(preds[2*i+1]==p['new_target_id']),same_answer=int(preds[2*i]==preds[2*i+1]),old_mode_old_minus_new_logit=logits_all[2*i],new_mode_old_minus_new_logit=logits_all[2*i+1],mode_margin_change=logits_all[2*i+1]-logits_all[2*i])
    for site,z in [('input',x),('output',y)]:
     a=z[2*i].double();b=z[2*i+1].double();gap=float((b-a).norm());den=float(((a.square().sum()+b.square().sum())/2).sqrt());cos=float(torch.dot(a,b)/(a.norm()*b.norm()))
     row[site+'_mode_gap_norm']=gap;row[site+'_baseline_RMS_norm']=den;row[site+'_mode_gap_ratio']=gap/den if den else 0;row[site+'_mode_cosine']=cos
    rows.append(row);allrows.append(row)
   assert predequal and maxce<=2e-4,('sample replay differs',item,maxce,predequal)
   summaries.append({k:item[k] for k in ['seed','method','old_slots']}|{'sample_pairs':64,'old_accuracy_pct':sum(z['old_correct'] for z in rows)/64*100,'new_accuracy_pct':sum(z['new_correct'] for z in rows)/64*100,'same_answer_pct':sum(z['same_answer'] for z in rows)/64*100,**{q:float(np.mean([z[q] for z in rows])) for q in ['input_mode_gap_ratio','output_mode_gap_ratio','input_mode_cosine','output_mode_cosine','old_mode_old_minus_new_logit','new_mode_old_minus_new_logit','mode_margin_change']},'source_prediction_exact':predequal,'source_CE_maxabs':maxce,'sampling_boundary':'posthoc correctness-stratified; descriptive only; not fullDEVestimate'})
   states.append({'condition':item,'checkpoint_sha256':manifest['sha256'],'sequences':128,'replay_max_CE_error':maxce,'all_predictions_equal':predequal});del saved
   print(json.dumps({'event':'condition_complete',**{k:item[k] for k in ['seed','method','old_slots']},'sequences':sequences}),flush=True)
 finally:
  for h in handles:h.remove()
 assert r.frozen_hash(base,set(r.NAMES))==before_frozen and sequences==1152 and len(states)==9
 dump('04_representation_pairs_576.csv',allrows);dump('04_representation_summary_9.csv',summaries)
 np.savez_compressed(O/'representation_raw.npz',inputs=np.stack(inputvectors),outputs=np.stack(outputvectors))
 receipt={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoint_count':9,'sequence_forwards':sequences,'optimizer_updates':0,'TEST_opened':False,'resource':'existing collaboration H100 MIG; no new job or allocation','GPU':str(torch.cuda.get_device_properties(0)),'frozen_upstream_unchanged':True,'input_site':'q_proj normalized input at final prefix token','output_site':'raw o_proj output at final prefix token before residual addition','source_logit_targets':'oldgold and counterfactual newgold, one token each; verified originaltokenIDs','sample_selection_lock_sha256':r.sha(V/'representation_sampling_lock.json'),'states':states,'inference_boundary':'within-model mode differences; neither representational availability nor nonzero gap proves actual causal use; posthoc correctness-stratified64pairs not representative fullDEV estimate'}
 write(V/'representation_receipt.json',receipt);print(json.dumps({'status':'PASS','sequences':sequences}))
if __name__=='__main__':
 try:main()
 except Exception:
  import traceback
  write(V/'representation_failure.json',{'status':'FAILED','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':traceback.format_exc(),'new_training':False});raise
