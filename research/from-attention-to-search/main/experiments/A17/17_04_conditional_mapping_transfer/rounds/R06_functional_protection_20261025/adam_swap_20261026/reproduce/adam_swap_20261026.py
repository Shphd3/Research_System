"""Fixedtheta×namedAdam-moment2x2; everybatchindependentstep120; noF."""
from pathlib import Path
import importlib.util,json,csv,hashlib,datetime,copy,time,traceback
import torch
import numpy as np
from torch import nn
E=Path(__file__).resolve().parents[1];O=E/'analysis/adam_swap_20261026';V=O/'provenance';PLAN=json.load(open(V/'plan.json'));OWN=json.load(open(V/'ownership.json'));R=Path(OWN['round']);A=Path(OWN['anchor'])
spec=importlib.util.spec_from_file_location('previouslocal',E/'ops/local_dynamics_20261026.py');prev=importlib.util.module_from_spec(spec);spec.loader.exec_module(prev);eng=prev.eng;r=eng.r05;C=eng.CFG;DEVICE='cuda:0'
def read(p):return json.loads(Path(p).read_text())
def write(p,x):r.write(p,x)
def sha(p):return r.sha(p)
def dump(n,rs):
 if not rs:return
 keys=list(dict.fromkeys(k for row in rs for k in row))
 with (O/'tables'/n).open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rs)
class Counted(nn.Module):
 def __init__(self,m):super().__init__();self.native=m;self.count=0;self.phase='start';self.calls=[]
 def forward(self,h,mask,lengths,targets,modes=None):
  n=int(h.shape[0]);assert self.count+n<=PLAN['sequence_budget'],'budgetexceeded'
  self.count+=n;self.calls.append({'phase':self.phase,'sequences':n,'total':self.count});return self.native(h,mask,lengths,targets,modes)

def load_named_states(base,params):
 originalfreeze=read(E/'provenance/freeze.json');assert originalfreeze['files'][str(E/'source/engine.py')]['sha256']==sha(E/'source/engine.py')
 ref=eng.optimizer(params);serial=ref.state_dict();objects={id(p):n for n,p in base.named_parameters()};namemap={};groupspec=[]
 for gi,(live,ser) in enumerate(zip(ref.param_groups,serial['param_groups'])):
  assert len(live['params'])==len(ser['params'])
  for p,pid in zip(live['params'],ser['params']):
   name=objects[id(p)];assert name in r.NAMES;namemap[name]={'id':pid,'group':gi,'shape':list(p.shape),'dtype':str(p.dtype)}
  groupspec.append({k:v for k,v in ser.items() if k!='params'})
 assert set(namemap)==set(r.NAMES)
 states={};ident=[]
 for it in PLAN['states']:
  path=Path(it['checkpoint']);meta=read(path.with_suffix('.json'));assert sha(path)==meta['sha256'];s=torch.load(path,map_location='cpu',weights_only=False)
  assert s['optimizer_step']==s['data_cursor']==120 and s['old_nonzero']==4 and s['source_freeze_sha256']==sha(E/'provenance/freeze.json')
  assert set(s['trainable_weights'])==set(namemap)
  assert len(s['optimizer']['param_groups'])==len(serial['param_groups'])
  for gi,g in enumerate(s['optimizer']['param_groups']):
   assert {k:v for k,v in g.items() if k!='params'}==groupspec[gi],'optimizerconfigmismatch'
   assert g['params']==serial['param_groups'][gi]['params'],'producerIDlayoutchanged; cannotblindlyremap'
  assert set(s['optimizer']['state'])=={x['id'] for x in namemap.values()}
  for n,m in namemap.items():
   st=s['optimizer']['state'][m['id']];assert set(st)=={'step','exp_avg','exp_avg_sq'} and float(st['step'])==120
   assert list(s['trainable_weights'][n].shape)==m['shape']
   for field in ['exp_avg','exp_avg_sq']:
    assert list(st[field].shape)==m['shape'] and st[field].dtype==torch.float32 and torch.isfinite(st[field]).all()
   assert (st['exp_avg_sq']>=0).all()
  states[it['seed'],it['origin']]=s
  ident.append({'seed':it['seed'],'origin':it['origin'],'path':str(path),'sha256_before':meta['sha256'],'optimizer_sha256':prev.staterawhash(s['optimizer']),'source_freeze_verified':True,'named_state_mapping':{n:{**m,'exp_avg_sha256':prev.staterawhash(s['optimizer']['state'][m['id']]['exp_avg']),'exp_avg_sq_sha256':prev.staterawhash(s['optimizer']['state'][m['id']]['exp_avg_sq'])} for n,m in namemap.items()}})
 write(V/'named_mapping_and_inputs.json',{'status':'PASS','mapping_method':'verifiedfrozenproducerengine+currentliveoptimizerparameterobjectidentity; sourceproducesparamsinr05.NAMES; exchangebynames,notbyunverifiedlistorK/Vshapes','explicit_paramnames_in_checkpoint':False,'source_engine_sha256':sha(E/'source/engine.py'),'live_named_mapping':namemap,'groupspec':groupspec,'states':ident})
 del ref;return states,namemap,ident

def mix_optimizer(theta_state,moment_state,mapping):
 mixed=copy.deepcopy(theta_state['optimizer'])
 for name,info in mapping.items():
  receiver=mixed['state'][info['id']];donor=moment_state['optimizer']['state'][info['id']]
  assert float(receiver['step'])==float(donor['step'])==120
  # Mapping keys, not a loop zip over source list positions, identify each matrix.
  for field in ['exp_avg','exp_avg_sq']:
   receiver[field]=donor[field].detach().clone()
   assert prev.staterawhash(receiver[field])==prev.staterawhash(donor[field])
 assert mixed['param_groups']==theta_state['optimizer']['param_groups']
 return mixed

def restore(params,theta_state,opt=None,mixed=None):
 with torch.no_grad():
  for name,p in zip(r.NAMES,params):p.copy_(theta_state['trainable_weights'][name].to(DEVICE))
 if opt is not None:opt.load_state_dict(copy.deepcopy(theta_state['optimizer'] if mixed is None else mixed))
 r.restore_rng(theta_state['rng'],DEVICE)
 for p in params:p.grad=None

def main():
 assert not (O/'receipt.json').exists(),'completed; refuse rerun'
 freeze_files=[Path(__file__),V/'plan.json',*[A/q for q in ['anchor.md','anchor_cn.md']],*[R/q for q in ['protocol.md','protocol_cn.md']],E/'source/engine.py',E/'source/retention_r05_v1.py',E/'ops/local_dynamics_20261026.py',E/'config/frozen.json',E/'provenance/orders.json']
 write(V/'freeze.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before_new_functional_results':True,'files':{str(p):sha(p) for p in freeze_files}})
 r.configure(29,DEVICE);train=r.load_cache(C,'train');dev=r.load_cache(C,'dev');carrier,native,params,w0,projs,frozen=eng.model_load();model=Counted(native);carrier.model.eval()
 states,mapping,inputreceipts=load_named_states(carrier.model,params);frozen_versions=[(n,p,p._version) for n,p in carrier.model.named_parameters() if n not in r.NAMES]
 assert [dev['records'][i]['record_id'] for i in PLAN['old_DEV_indices']]==PLAN['old_DEV_ids']
 assert [dev['records'][i]['record_id'] for i in PLAN['new_DEV_indices']]==PLAN['new_DEV_ids']
 baselines={};grads={};replay_pre={};noiserows=[];effectrows=[];geometry=[];peritems=[];replayrows=[];momentrows=[];maincontexts=[];begun=time.time()
 groups={'old_DEV':PLAN['old_DEV_indices'],'new_DEV':PLAN['new_DEV_indices']}
 previous=list(csv.DictReader(open(E/'analysis/local_dynamics_20261026/tables/candidate_group_losses_138.csv')))
 previousdi=list(csv.DictReader(open(E/'analysis/local_dynamics_20261026/tables/candidate_directions_54.csv')))
 def candidate(seed,batchno,thetaorigin,momentorigin,replay=False):
  s=states[seed,thetaorigin];donor=states[seed,momentorigin];b=PLAN['batches'][str(seed)][batchno-1];opt=eng.optimizer(params);mixed=mix_optimizer(s,donor,mapping);restore(params,s,opt,mixed);before=[p.detach().clone() for p in params];preopthash=prev.staterawhash(r.cpu_tree(opt.state_dict()));assert preopthash==prev.staterawhash(mixed)
  opt.zero_grad(set_to_none=True);model.phase=f'{seed}/batch{batchno}/{thetaorigin}{momentorigin}/objective';indices=b['new']+b['old'];mask=[1.]*36+b['mask4'];newsum=oldsum=0.
  for j in range(0,72,12):
   ix=indices[j:j+12];h,ma,le,y,mo=r.cache_batch(train,ix,DEVICE);w=torch.tensor(mask[j:j+len(ix)],device=DEVICE);y=torch.where(w.bool(),y,torch.zeros_like(y));_,_,ls=model(h,ma,le,y,mo);((ls*w).sum()/72).backward()
   if j<36:newsum+=float((ls.detach()*w).sum())
   else:oldsum+=float((ls.detach()*w).sum())
  assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in params)
  gradienthash=prev.staterawhash({n:p.grad for n,p in zip(r.NAMES,params)});rawnorm=eng.length([p.grad for p in params]);clip_pre=torch.nn.utils.clip_grad_norm_(params,1.,foreach=False);clipcoef=min(1.,1/(float(clip_pre)+1e-6));clippednorm=eng.length([p.grad for p in params]);opt.step()
  with torch.no_grad():
   proposal=[(p-a).clone() for p,a in zip(params,before)]
   for p,a,d in zip(params,before,proposal):p.copy_(a+d)
   actual=[(p-a).clone() for p,a in zip(params,before)];err=[a-b for a,b in zip(actual,proposal)];gold=grads[seed,thetaorigin];gdot=float(eng.dot(gold,actual))
  opost=r.cpu_tree(opt.state_dict());assert all(float(st['step'])==121 for st in opost['state'].values())
  context={'seed':seed,'batch':batchno,'original_order_index':b['original_order_index'],'theta_origin':thetaorigin,'moments_origin':momentorigin,'cell':thetaorigin+momentorigin}
  geom={**context,'objective_CE':(newsum+oldsum)/72,'new_TRAIN_CE':newsum/36,'active_old4_TRAIN_CE':oldsum/4,'raw_gradient_norm':rawnorm,'gradient_clip_coefficient':clipcoef,'clipped_gradient_norm':clippednorm,'gradient_hash_by_name':gradienthash,'proposal_norm':eng.length(proposal),'final_actual_displacement_norm':eng.length(actual),'writeback_roundoff_norm':eng.length(err),'fixed_old_DEV_gradient_norm':eng.length(gold),'actual_dot_old_DEV_gradient':gdot,'optimizer_step_before':120,'optimizer_step_after':121,'optimizer_pre_hash':preopthash,'optimizer_post_hash':prev.staterawhash(opost),'F_projection_applied':False}
  geometry.append(geom);maincontexts.append(context)
  # Verify named moment identity before the step, without exporting any state.
  momentrows.append({**context,'named_moments_source_verified':True,'prehash':preopthash,'receiving_theta_checkpoint_sha':next(x['sha256_before'] for x in inputreceipts if x['seed']==seed and x['origin']==thetaorigin),'donor_moments_checkpoint_sha':next(x['sha256_before'] for x in inputreceipts if x['seed']==seed and x['origin']==momentorigin)})
  model.phase=f'{seed}/batch{batchno}/{thetaorigin}{momentorigin}/DEV'
  measured={g:prev.measure(model,dev,ix,g) for g,ix in groups.items()}
  for group,a in measured.items():
   beforegroup=baselines[seed,thetaorigin,group];tau=beforegroup['tau'];change=a['CE']-beforegroup['CE']
   row={**context,'group':group,'n':a['n'],'before_CE':beforegroup['CE'],'after_CE':a['CE'],'CE_change':change,'noise_tau':tau,'CE_change_resolved':abs(change)>2*tau,'before_accuracy_pct':beforegroup['accuracy_pct'],'after_accuracy_pct':a['accuracy_pct'],'accuracy_change_pp':a['accuracy_pct']-beforegroup['accuracy_pct'],'before_old_minus_new_margin':beforegroup['old_minus_new_margin_mean'],'after_old_minus_new_margin':a['old_minus_new_margin_mean'],'margin_change':a['old_minus_new_margin_mean']-beforegroup['old_minus_new_margin_mean'],'actual_displacement_norm':geom['final_actual_displacement_norm'],'actual_dot_old_DEV_gradient':gdot,'first_order_prediction':gdot if group=='old_DEV' else None,'finite_remainder':change-gdot if group=='old_DEV' else None}
   effectrows.append(row)
   for i,index in enumerate(groups[group]):
    rr=dev['records'][index];peritems.append({**context,'group':group,'record_id':rr['record_id'],'panel':rr['panel'],'command':rr['command'],'before_CE':beforegroup['per_item_CE'][i],'after_CE':a['per_item_CE'][i],'CE_change':a['per_item_CE'][i]-beforegroup['per_item_CE'][i],'before_correct':beforegroup['per_item_correct'][i],'after_correct':a['per_item_correct'][i]})
  if replay:
   model.phase=f'{seed}/{thetaorigin}/native_replay_extra_after'
   extra={'probe':prev.measure(model,train,b['probe'],'probe'),'new':prev.measure(model,train,b['new'],'new')}
   checkgroups={'independent_old':(baselines[seed,thetaorigin,'old_DEV'],measured['old_DEV']),**{g:(replay_pre[seed,thetaorigin,g],a) for g,a in extra.items()}}
   gate=True
   for group,(pre,post) in checkgroups.items():
    ref=next(x for x in previous if x['seed']==str(seed) and x['origin']==thetaorigin and x['condition']=='d4' and x['alpha']=='1.0' and x['group']==group)
    changes=post['CE']-pre['CE'];tol=2e-6*(1+abs(float(ref['before_CE'])));errors={'baseline_abs_error':abs(pre['CE']-float(ref['before_CE'])),'after_abs_error':abs(post['CE']-float(ref['after_CE'])),'change_abs_error':abs(changes-float(ref['CE_change']))};ok=all(x<=tol for x in errors.values());gate &=ok
    replayrows.append({'seed':seed,'native_cell':thetaorigin+thetaorigin,'group':group,'reference_condition':'previousunprojectedd4','reference_before_CE':float(ref['before_CE']),'replay_before_CE':pre['CE'],'reference_after_CE':float(ref['after_CE']),'replay_after_CE':post['CE'],'reference_delta_CE':float(ref['CE_change']),'replay_delta_CE':changes,**errors,'tolerance':tol,'PASS':ok})
   dr=next(x for x in previousdi if x['seed']==str(seed) and x['origin']==thetaorigin and x['condition']=='d4' and x['alpha']=='1.0');ne=abs(float(dr['actual_displacement_norm'])-geom['final_actual_displacement_norm']);nt=max(1e-6,1e-4*float(dr['actual_displacement_norm']));gate &=ne<=nt
   replayrows.append({'seed':seed,'native_cell':thetaorigin+thetaorigin,'group':'actual_displacement_norm','reference_condition':'previousunprojectedd4','reference_delta_CE':None,'replay_delta_CE':None,'tolerance':nt,'change_abs_error':ne,'PASS':ne<=nt})
   dump('native_firstbatch_replay.csv',replayrows)
   assert gate,'nativefirstbatchreplayfailed; stopbeforehybrids'
  restore(params,s,opt,mixed);assert all(torch.equal(p,a) for p,a in zip(params,before));assert prev.staterawhash(r.cpu_tree(opt.state_dict()))==preopthash
  assert all(p._version==v for _,p,v in frozen_versions)
  dump('candidate_DEV_effects_72.csv',effectrows);dump('candidate_geometry_36.csv',geometry);dump('per_item_DEV_effects_4608.csv',peritems);dump('moment_source_identity_36.csv',momentrows)
  print(json.dumps({'event':'candidate_complete',**context,'sequence_forwards':model.count,'native_replay':replay}),flush=True)
  del opt,before,proposal,actual,err,opost,mixed
 try:
  # BaselineandoldDEVgradientdependonthetaonly; reusedacrossmomentcellsandbatches.
  for seed in [29,43,71]:
   for theta in ['U','F']:
    s=states[seed,theta];b=PLAN['batches'][str(seed)][0];measurements=[]
    for repeat in range(2):
     restore(params,s);model.phase=f'{seed}/{theta}/noop{repeat}';measurements.append({g:prev.measure(model,dev,ix,g) for g,ix in groups.items()})
    restore(params,s);model.phase=f'{seed}/{theta}/oldDEVgradient';gold,gloss=eng.take_grad(model,params,dev,groups['old_DEV'],16);grads[seed,theta]=gold
    for group in groups:
     a,before2=measurements[0][group],measurements[1][group];span=abs(a['CE']-before2['CE']);gradgap=abs(gloss-a['CE']) if group=='old_DEV' else 0.;tau=max(span,1e-8*(1+abs(a['CE'])),gradgap);a['tau']=tau;baselines[seed,theta,group]=a
     noiserows.append({'seed':seed,'theta_origin':theta,'group':group,'n':a['n'],'baseline_CE':a['CE'],'noop_span':span,'gradient_forward_no_grad_gap':gradgap,'noise_tau':tau,'per_item_CE_equal':a['per_item_CE']==before2['per_item_CE'],'per_item_correctness_equal':a['per_item_correct']==before2['per_item_correct']})
    restore(params,s);model.phase=f'{seed}/{theta}/native_replay_extra_before';replay_pre[seed,theta,'probe']=prev.measure(model,train,b['probe'],'probe');replay_pre[seed,theta,'new']=prev.measure(model,train,b['new'],'new')
  dump('baseline_noop_noise_12.csv',noiserows)
  # Allsixnativefirstbatchreplaygatesbeforenewhybridmeasurement.
  for seed in [29,43,71]:
   for origin in ['U','F']:candidate(seed,1,origin,origin,replay=True)
  assert all(r0['PASS'] for r0 in replayrows)
  write(V/'native_replay_gate.json',{'status':'PASS','native_states':6,'checks':len(replayrows),'all_before_hybrids':True,'max_CE_error':max(x.get('change_abs_error',0) for x in replayrows if x['group']!='actual_displacement_norm'),'reference':'previousunprojectedd4,notF4'})
  for seed in [29,43,71]:
   for batch in [1,2,3]:
    for theta in ['U','F']:
     for moment in ['U','F']:
      if batch==1 and theta==moment:continue
      candidate(seed,batch,theta,moment)
  assert len(maincontexts)==36 and len({(x['seed'],x['batch'],x['cell']) for x in maincontexts})==36
  assert model.count==10320
  for x in inputreceipts:x['sha256_after']=sha(x['path']);x['unchanged']=x['sha256_after']==x['sha256_before'];assert x['unchanged']
  assert r.frozen_hash(carrier.model,set(r.NAMES))==frozen
  freeze=read(V/'freeze.json');assert all(sha(p)==h for p,h in freeze['files'].items())
  write(V/'original_assets_immutable.json',{'status':'PASS','states':inputreceipts,'non_target_model_bytes_unchanged':True,'contract_source_plan_unchanged':True,'original_weights_or_optimizer_files_written':False})
  write(O/'sequence_calls.json',model.calls)
  receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parameter_origins':6,'cells_per_seed':4,'batches_per_seed':3,'independent_candidates':36,'ordinary_temporary_Adam_steps':36,'all_proposals_from_step120':True,'F_projection_applied':False,'sequence_forwards':model.count,'budget':12000,'remaining':12000-model.count,'native_firstbatch_replay':'PASS all6beforehybrids','original_checkpoint_changes':0,'candidate_checkpoint_saves':0,'full_continuation_runs':0,'new_resources_or_jobs':0,'TEST_labels_read':False,'old_new_diagnostic_n':64,'GPU':str(torch.cuda.get_device_properties(0)),'elapsed_seconds':time.time()-begun}
  write(O/'receipt.json',receipt);print(json.dumps(receipt),flush=True)
 except Exception:
  write(O/'failure.json',{'status':'FAILED_PARTIAL','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sequence_forwards':model.count,'error':traceback.format_exc(),'no_sourcewrites':True});write(O/'partial_sequence_calls.json',model.calls);raise
if __name__=='__main__':main()
