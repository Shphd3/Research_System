"""Same-state single-step counterfactuals. No continuation or candidate checkpoints."""
from pathlib import Path
import importlib.util,sys,os,json,hashlib,copy,math,time,csv,datetime,traceback
import numpy as np
import torch
from torch import nn
E=Path(__file__).resolve().parents[1];O=E/'analysis/local_dynamics_20261026';V=O/'provenance';PLAN=json.load(open(V/'plan.json'));OWN=json.load(open(V/'ownership.json'));R=Path(OWN['round']);A=Path(OWN['anchor'])
spec=importlib.util.spec_from_file_location('r06local',E/'source/engine.py');eng=importlib.util.module_from_spec(spec);spec.loader.exec_module(eng);r=eng.r05;C=eng.CFG;DEVICE='cuda:0'

def write(p,x):r.write(p,x)
def dump(name,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for z in rows for k in z))
 with (O/'tables'/name).open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
def append(p,x):eng.append(p,x)
def sha(p):return r.sha(p)
def staterawhash(x):
 h=hashlib.sha256()
 def rec(v):
  if torch.is_tensor(v):h.update(str((v.shape,v.dtype)).encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
  elif isinstance(v,dict):
   for k in sorted(v,key=str):h.update(str(k).encode());rec(v[k])
  elif isinstance(v,(list,tuple)):
   for z in v:rec(z)
  else:h.update(repr(v).encode())
 rec(x);return h.hexdigest()
class Counted(nn.Module):
 def __init__(self,model):super().__init__();self.native=model;self.count=0;self.phase='init';self.calls=[]
 def forward(self,h,mask,lengths,targets,modes=None):
  n=int(h.shape[0]);assert self.count+n<=PLAN['sequence_budget'],'sequence budget reached'
  self.count+=n;self.calls.append({'phase':self.phase,'sequences':n,'total':self.count})
  return self.native(h,mask,lengths,targets,modes)

def log_trajectory():
 curvepath=E/'analysis/meeting_20261026/tables/02_rule_mode_stats_all.csv';stats=list(csv.DictReader(open(curvepath)));curves=[];steps=[]
 for seed in [29,43,71]:
  for k in [0,4]:
   for m in ['U','F']:
    case=E/'runs'/f'seed_{seed}'/f'old_{k:02}'/m
    ms=[json.loads(l) for l in (case/'metrics.jsonl').read_text().splitlines()]
    for x in ms:
     gnorm=math.sqrt(x['probe_g2']);dn=x['candidate_norm'];q=x['g_dot_candidate'];removed=q/gnorm if q>0 and x['probe_g2']>1e-24 else 0.
     steps.append({'seed':seed,'old_slots':k,'method':m,'step':x['step'],'probe_loss':x['probe_loss'],'new_batch_CE':x['new_train_ce'],'old_active_batch_CE':x['old_active_train_ce'],'projection_condition':x['projection_needed'],'F_applied':m=='F' and x['projection_needed'],'g_dot_candidate':q,'g_dot_actual':x['g_dot_actual'],'candidate_norm':dn,'actual_norm':x['actual_norm'],'ideal_projection_removed_norm':removed,'ideal_projection_removed_fraction':removed/dn if dn else 0.,'actual_probe_loss_change':x.get('probe_loss_change'),'finite_remainder':x.get('first_order_remainder'),'label':'removednormderivedunderidealprojection, notsavedactualremovedvector'})
    for step in [0,1,2,4,8,16,32,64,120,180,240]:
     a=json.load(open(case/f'eval_{step:06}.json'));agg=a['aggregates'];sc=next(z for z in stats if z['seed']==str(seed) and z['method']==m and z['old_slots']==str(k) and z['step']==str(step) and z['panel']=='combined' and z['command']=='both')
     r0={'seed':seed,'old_slots':k,'method':m,'step':step,'new_targets':36*step,'old_accuracy_pct':100*agg['mode1/both/combined']['accuracy'],'new_accuracy_pct':100*agg['mode2/both/combined']['accuracy'],'old_CE':agg['mode1/both/combined']['ce'],'new_CE':agg['mode2/both/combined']['ce'],'old_newrule_pct':float(sc['new_rule_endpoint_pct']),'both_mode_correct_pct':float(sc['both_correct_pct']),'same_mode_answer_pct':float(sc['same_prediction_pct']),'endpoint_logit_advantage':'NOT_SAVED forentiretrajectory; noforwardreconstruction'}
     if step:
      part=steps[-240:];upto=[x for x in part if max(0,step-16)<x['step']<=step]
      r0.update(last16step_projection_condition_fraction=sum(x['projection_condition'] for x in upto)/len(upto),last16step_ideal_removed_fraction_mean=float(np.mean([x['ideal_projection_removed_fraction'] for x in upto])))
     curves.append(r0)
 dump('trajectory_alignment_132.csv',curves);dump('trajectory_step_logs_2880.csv',steps)
 write(V/'trajectory_only_receipt.json',{'status':'PASS','points':len(curves),'step_logs':len(steps),'raw_logit_margins':'NOT_SAVED exceptprevioussmallreadout; notmanufactured','origins_differ':'crossrunassociationonly','newforward_sequences':0})
 return curves

def measure(model,cache,indices,group):
 mb=12 if group=='new' else 16;losses=[];correct=[];margins=[]
 with torch.no_grad():
  for j in range(0,len(indices),mb):
   ix=indices[j:j+mb];_,logits,ls=model(*r.cache_batch(cache,ix,DEVICE))
   records=[cache['records'][i] for i in ix]
   oldgold=[];newgold=[]
   for rr in records:
    ws=rr['words'];ids=dict(zip(C['answer_words'],C['answer_ids']));oldgold.append(ids[ws[0]] if rr['command']=='甲' else ids[ws[-1]]);newgold.append(ids[ws[-1]] if rr['command']=='甲' else ids[ws[0]])
   ar=torch.arange(len(ix),device=DEVICE);og=torch.tensor(oldgold,device=DEVICE);ng=torch.tensor(newgold,device=DEVICE)
   margins.extend((logits[ar,og]-logits[ar,ng]).double().cpu().tolist());losses.extend(ls.double().cpu().tolist());pr=logits.argmax(-1).cpu().tolist();correct.extend(int(p==rr['target_id']) for p,rr in zip(pr,records))
 return {'n':len(indices),'CE':float(np.mean(losses)),'accuracy_pct':100*sum(correct)/len(indices),'old_minus_new_margin_mean':float(np.mean(margins)),'per_item_CE':losses,'per_item_correct':correct,'per_item_old_minus_new_margin':margins}

def restore(params,s,opt=None):
 with torch.no_grad():
  for n,p in zip(r.NAMES,params):p.copy_(s['trainable_weights'][n].to(DEVICE))
 if opt is not None:opt.load_state_dict(copy.deepcopy(s['optimizer']))
 r.restore_rng(s['rng'],DEVICE)
 for p in params:p.grad=None

def old4grad(model,params,train,order):
 for p in params:p.grad=None
 loss=0.
 for j in range(0,36,12):
  ix=order['old'][j:j+12];h,ma,le,y,mo=r.cache_batch(train,ix,DEVICE);weights=torch.tensor(order['mask4'][j:j+len(ix)],device=DEVICE,dtype=torch.float32);y=torch.where(weights.bool(),y,torch.zeros_like(y));_,_,ls=model(h,ma,le,y,mo)
  ((ls*weights).sum()/4).backward();loss+=float((ls.detach()*weights).sum())
 g=[p.grad.detach().clone() for p in params]
 for p in params:p.grad=None
 return g,loss/4

def proposal(model,params,s,train,order,k):
 opt=eng.optimizer(params);restore(params,s,opt);before=[p.detach().clone() for p in params];opt.zero_grad(set_to_none=True);total=0.
 ix=order['new']+order['old'];mask=[1.]*36+(order['mask4'] if k else [0.]*36)
 for j in range(0,72,12):
  inds=ix[j:j+12];h,ma,le,y,mo=r.cache_batch(train,inds,DEVICE);w=torch.tensor(mask[j:j+len(inds)],device=DEVICE);y=torch.where(w.bool(),y,torch.zeros_like(y));_,_,ls=model(h,ma,le,y,mo);((ls*w).sum()/72).backward();total+=float((ls.detach()*w).sum())
 raw=eng.length([p.grad for p in params]);torch.nn.utils.clip_grad_norm_(params,1.,foreach=False);clipped=eng.length([p.grad for p in params]);opt.step()
 with torch.no_grad():d=[(p-b).clone() for p,b in zip(params,before)]
 post=r.cpu_tree(opt.state_dict());assert all(float(x['step'])==121 for x in post['state'].values())
 info={'objective':total/72,'raw_gradient_norm':raw,'clipped_gradient_norm':clipped,'clip_triggered':raw>1.,'candidate_norm':eng.length(d),'optimizer_pre_sha256':staterawhash(s['optimizer']),'optimizer_post_sha256':staterawhash(post),'jointAdamdirect':True}
 del opt;return d,info,post

def main():
 assert not (O/'receipt.json').exists(),'do not repeat alreadycompleteddiagnostic'
 log_trajectory()
 # Establish actual six recoverable states without selecting on functional outcomes.
 checkpointreceipts=[]
 for item in PLAN['states']:
  p=Path(item['checkpoint']);meta=json.load(open(item['checkpoint_manifest']));assert sha(p)==meta['sha256'];s=torch.load(p,map_location='cpu',weights_only=False)
  assert s['optimizer_step']==s['data_cursor']==120 and len(s['optimizer']['state'])==4 and set(s['trainable_weights'])==set(r.NAMES)
  assert all(set(['step','exp_avg','exp_avg_sq'])<=set(x) and float(x['step'])==120 for x in s['optimizer']['state'].values())
  checkpointreceipts.append({'path':str(p),'sha256_before':meta['sha256'],'bytes':p.stat().st_size,'recoverable_Adam':True,'optimizer_sha256':staterawhash(s['optimizer'])})
 write(V/'six_state_precheck.json',{'status':'PASS','states':checkpointreceipts,'fallback':False})
 freeze_files=[Path(__file__),V/'plan.json',*[A/p for p in ['anchor.md','anchor_cn.md']],*[R/p for p in ['protocol.md','protocol_cn.md']],E/'source/engine.py',E/'source/retention_r05_v1.py',E/'config/frozen.json',E/'provenance/orders.json']
 write(V/'freeze.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before_new_functional_results':True,'files':{str(p):sha(p) for p in freeze_files}})
 r.configure(29,DEVICE);train=r.load_cache(C,'train');dev=r.load_cache(C,'dev');orders=json.load(open(E/'provenance/orders.json'))
 # Ensure exact data and independently sampled record identity.
 assert [dev['records'][i]['record_id'] for i in PLAN['independent_old_DEV_indices']]==PLAN['independent_old_DEV_ids']
 assert not set(PLAN['independent_old_DEV_ids'])&set(orders['record_ids'])
 carrier,native,params,w0,projs,frozen=eng.model_load();model=Counted(native);carrier.model.eval()
 versions=[(n,p,p._version) for n,p in carrier.model.named_parameters() if n not in r.NAMES]
 allrows=[];peritems=[];directions=[];noise=[];statesummary=[];origmetreplay=[];begun=time.time()
 try:
  for state_index,item in enumerate(PLAN['states']):
   seed=item['seed'];origin=item['origin_method'];s=torch.load(item['checkpoint'],map_location='cpu',weights_only=False);order=orders['seeds'][str(seed)][120]
   restore(params,s);state_start_count=model.count;baseweights=[p.detach().clone() for p in params];original_opt_hash=staterawhash(s['optimizer']);groups={'probe':(train,order['probe']),'new':(train,order['new']),'independent_old':(dev,PLAN['independent_old_DEV_indices'])}
   noops=[]
   for rep in range(2):
    restore(params,s);model.phase=f'{seed}/{origin}/noop{rep}';noops.append({g:measure(model,ca,ix,g) for g,(ca,ix) in groups.items()})
   restore(params,s);model.phase=f'{seed}/{origin}/probe_gradient';gp,probegradloss=eng.take_grad(model,params,train,order['probe'],16)
   model.phase=f'{seed}/{origin}/old4_gradient';g4,old4loss=old4grad(model,params,train,order)
   gradinfo={'g_probe_norm':eng.length(gp),'g_old4_norm':eng.length(g4),'g4_dot_gprobe':float(eng.dot(g4,gp)),'g4_probe_cosine':float(eng.dot(g4,gp))/(eng.length(gp)*eng.length(g4)) if eng.length(gp)*eng.length(g4) else None,'g_old4_mean_CE':old4loss,'g_probe_forward_CE':probegradloss}
   taus={}
   for g in groups:
    a,b=noops[0][g],noops[1][g];span=abs(a['CE']-b['CE']);floor=1e-8*(1+abs(a['CE']));gradgap=abs(probegradloss-a['CE']) if g=='probe' else 0.;taus[g]=max(span,floor,gradgap)
    noise.append({'seed':seed,'origin':origin,'group':g,'n':a['n'],'noop_CE_1':a['CE'],'noop_CE_2':b['CE'],'noop_span':span,'grad_forward_no_grad_gap':gradgap,'precision_floor':floor,'noise_tolerance':taus[g],'same_prediction_all':a['per_item_correct']==b['per_item_correct'],'same_per_item_CE_all':a['per_item_CE']==b['per_item_CE']})
   model.phase=f'{seed}/{origin}/Adam_d0';d0,di0,post0=proposal(model,params,s,train,order,0)
   model.phase=f'{seed}/{origin}/Adam_d4';d4,di4,post4=proposal(model,params,s,train,order,4)
   with torch.no_grad():
    f0,fi0=eng.filter_step(d0,gp,'F',projs,120);f4,fi4=eng.filter_step(d4,gp,'F',projs,120);dd4,_=eng.filter_step(d4,gp,'D',projs,120)
   proposalinfo={'d0':di0,'d4':di4};proposalpost={'d0':post0,'F0':post0,'d4':post4,'F4':post4,'D4':post4}
   displacements={'d0':d0,'d4':d4,'F0':f0,'F4':f4,'D4':dd4};reference={'d0':d0,'F0':d0,'d4':d4,'F4':d4,'D4':d4};allconds=[(m,1.) for m in ['d0','d4','F0','F4','D4']]+[(m,a) for m in ['d4','F4'] for a in [.5,.25]]
   # Verify unscaled d4/F4 agrees with original step121 diagnostics on origin's actualrule.
   origms=[json.loads(l) for l in (Path(item['checkpoint']).parents[1]/'metrics.jsonl').read_text().splitlines()];orig=origms[120]
   target=f4 if origin=='F' else d4
   with torch.no_grad():actual_original=[(b+d-b) for b,d in zip(baseweights,target)]
   replay={'seed':seed,'origin':origin,'source_step':121,'original_candidate_norm':orig['candidate_norm'],'replayed_candidate_norm':eng.length(d4),'candidate_norm_abs_error':abs(orig['candidate_norm']-eng.length(d4)),'original_actual_norm':orig['actual_norm'],'replayed_actual_norm':eng.length(actual_original),'actual_norm_abs_error':abs(orig['actual_norm']-eng.length(actual_original)),'original_g_dot_candidate':orig['g_dot_candidate'],'replayed_g_dot_candidate':float(eng.dot(gp,d4)),'probe_pre_loss_original':orig['probe_loss'],'probe_pre_loss_replayed':probegradloss,'batch_shapes':'identical12objective/16probe','interpretation':'same-nativecomputation onexistingMIG; reportnumericdifference, notblindbyteidentityclaim'}
   assert replay['candidate_norm_abs_error']<max(1e-6,orig['candidate_norm']*1e-4),'proposal/source mismatch'
   origmetreplay.append(replay)
   # Baseline records and all objective/check indices written perstate as scalar evidence.
   statesummary.append({'seed':seed,'origin':origin,'checkpoint_step':120,**gradinfo,'proposal0':di0,'proposal4':di4,'F0':fi0,'F4':fi4,'original_checkpoint_sha256':sha(item['checkpoint']),'probe_ids':[train['records'][i]['record_id'] for i in order['probe']],'new_ids':[train['records'][i]['record_id'] for i in order['new']],'active_old4_ids':[train['records'][i]['record_id'] for i,mask in zip(order['old'],order['mask4']) if mask]})
   for condition,alpha in allconds:
    branchopt=eng.optimizer(params);restore(params,s,branchopt);assert staterawhash(r.cpu_tree(branchopt.state_dict()))==original_opt_hash
    # Use independently cloned postproposal moments only as a diagnostic state;
    # it is never stepped again, and every following branch reloads step120.
    branchopt.load_state_dict(copy.deepcopy(proposalpost[condition]));expectedpost=proposalinfo['d0' if condition in ['d0','F0'] else 'd4']['optimizer_post_sha256'];assert staterawhash(r.cpu_tree(branchopt.state_dict()))==expectedpost
    with torch.no_grad():
     desired=[alpha*x for x in displacements[condition]]
     for p,b,d in zip(params,baseweights,desired):p.copy_(b+d)
     actual=[(p-b).clone() for p,b in zip(params,baseweights)];removed=[alpha*x-a for x,a in zip(reference[condition],actual)];rounderror=[a-b for a,b in zip(actual,desired)]
     pdot=float(eng.dot(gp,actual));odot=float(eng.dot(g4,actual));pn=eng.length(gp);on=eng.length(g4);err=eng.length(rounderror);candidate_dot=float(eng.dot(gp,[alpha*x for x in reference[condition]]));tau0=max(1e-10,abs(candidate_dot)*1e-5);dot_tau=tau0+pn*err+6291456*np.finfo(float).eps*pn*eng.length(actual)
     direction={'seed':seed,'origin':origin,'condition':condition,'alpha':alpha,'actual_displacement_norm':eng.length(actual),'reference_candidate_scaled_norm':alpha*eng.length(reference[condition]),'actual_removed_component_norm':eng.length(removed),'removed_fraction':eng.length(removed)/(alpha*eng.length(reference[condition])) if eng.length(reference[condition]) else 0.,'actual_probe_gradient_dot':pdot,'actual_old4_gradient_dot':odot,'deleted_probe_gradient_dot':float(eng.dot(gp,removed)),'deleted_old4_gradient_dot':float(eng.dot(g4,removed)),'reference_probe_gradient_dot':candidate_dot,'reference_old4_gradient_dot':float(eng.dot(g4,[alpha*x for x in reference[condition]])),'writeback_roundoff_norm':err,'probe_dot_tolerance':dot_tau,'probe_final_positive_beyond_tolerance':pdot>dot_tau,'probe_gradient_norm':pn,'old4_gradient_norm':on,'g4_probe_cosine':gradinfo['g4_probe_cosine'],'F_active':fi0['projection_needed'] if condition=='F0' else fi4['projection_needed'] if condition=='F4' else None,'alpha_scope':'fixed-displacement diagnostic; noproposaldecompositionorLRsearch'}
    directions.append(direction);model.phase=f'{seed}/{origin}/{condition}/alpha{alpha}'
    activegroups=groups if alpha==1. else {k:v for k,v in groups.items() if k!='new'}
    for g,(ca,ix) in activegroups.items():
     after=measure(model,ca,ix,g);before=noops[0][g];change=after['CE']-before['CE'];firstorder=pdot if g=='probe' else odot if g=='old4' else None
     row={'seed':seed,'origin':origin,'condition':condition,'alpha':alpha,'group':g,'n':after['n'],'before_CE':before['CE'],'after_CE':after['CE'],'CE_change':change,'noise_tau':taus[g],'CE_change_resolved':abs(change)>2*taus[g],'before_accuracy_pct':before['accuracy_pct'],'after_accuracy_pct':after['accuracy_pct'],'accuracy_change_pp':after['accuracy_pct']-before['accuracy_pct'],'before_old_minus_new_margin':before['old_minus_new_margin_mean'],'after_old_minus_new_margin':after['old_minus_new_margin_mean'],'margin_change':after['old_minus_new_margin_mean']-before['old_minus_new_margin_mean'],'first_order_prediction':firstorder,'finite_remainder':change-firstorder if firstorder is not None else None,'actual_displacement_norm':direction['actual_displacement_norm'],'removed_component_norm':direction['actual_removed_component_norm'],'gprobe_actual_dot':pdot,'g_old4_actual_dot':odot}
     allrows.append(row)
     for i,index in enumerate(ix):
      rr=ca['records'][index];peritems.append({'seed':seed,'origin':origin,'condition':condition,'alpha':alpha,'group':g,'record_id':rr['record_id'],'panel':rr['panel'],'command':rr['command'],'before_CE':before['per_item_CE'][i],'after_CE':after['per_item_CE'][i],'CE_change':after['per_item_CE'][i]-before['per_item_CE'][i],'before_correct':before['per_item_correct'][i],'after_correct':after['per_item_correct'][i],'before_old_minus_new_margin':before['per_item_old_minus_new_margin'][i],'after_old_minus_new_margin':after['per_item_old_minus_new_margin'][i]})
    # Every branch returnsθandAdamtooriginalandverifiesexactcopies.
    restore(params,s,branchopt);assert all(torch.equal(p,b) for p,b in zip(params,baseweights));assert staterawhash(r.cpu_tree(branchopt.state_dict()))==original_opt_hash
    assert all(p._version==v for _,p,v in versions),'frozen tensor changed'
    del branchopt
   assert model.count-state_start_count==1904,(model.count-state_start_count)
   append(O/'state_completion.jsonl',{'seed':seed,'origin':origin,'status':'PASS','sequence_forwards':model.count-state_start_count,'restored_original_weights_and_optimizer':True})
   dump('candidate_group_losses_138.csv',allrows);dump('candidate_directions_54.csv',directions);dump('per_item_losses.csv',peritems);dump('noop_noise_18.csv',noise);dump('source_step121_replay_6.csv',origmetreplay);write(O/'state_summary.json',statesummary)
   print(json.dumps({'event':'state_complete','seed':seed,'origin':origin,'sequence_forwards':model.count,'elapsed':time.time()-begun}),flush=True)
   del s,baseweights,gp,g4,d0,d4,f0,f4,dd4,displacements,reference,post0,post4,proposalpost
  assert model.count==11424
  assert r.frozen_hash(carrier.model,set(r.NAMES))==frozen
  for x in checkpointreceipts:
   x['sha256_after']=sha(x['path']);x['unchanged']=x['sha256_after']==x['sha256_before'];assert x['unchanged']
  frozenfiles=json.load(open(V/'freeze.json'));assert all(sha(p)==h for p,h in frozenfiles['files'].items())
  write(V/'original_asset_immutability.json',{'status':'PASS','states':checkpointreceipts,'frozen_model_bytes_unchanged':True,'frozen_diagnostic_source_plan_contracts_unchanged':True,'candidate_checkpoint_exports':0})
  write(O/'sequence_forward_calls.json',model.calls)
  receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'states':6,'proposals_per_state':2,'temporary_Adam_proposals':12,'continuation_training_updates':0,'candidate_checkpoint_saves':0,'sequence_forwards':model.count,'sequence_budget':12000,'remaining_budget':12000-model.count,'all_branches_independent_restores':True,'full120Adam_moments_restored':True,'GPU':str(torch.cuda.get_device_properties(0)),'new_job_or_resource':False,'TEST_opened':False,'elapsed_seconds':time.time()-begun,'rows':{'losses':len(allrows),'directions':len(directions),'noise':len(noise)},'finite_scaling_new_batch_readout':'NOT_RUN_BY_PLAN forbudget; oldprobeandindependentoldmeasured','source_step_replay':'numericagreementchecked for12/16batch; notclaimedallbitwise'}
  write(O/'receipt.json',receipt);print(json.dumps(receipt),flush=True)
 except Exception:
  write(O/'failure.json',{'status':'FAILED_PARTIAL','error':traceback.format_exc(),'sequence_forwards':model.count,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoint_writes':False});raise
if __name__=='__main__':main()
