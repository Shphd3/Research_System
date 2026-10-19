from common import *
import argparse,contextlib,traceback
from torch.utils.tensorboard import SummaryWriter

def optimizer(m,lr=3e-4):return torch.optim.AdamW(m.parameters(),lr=lr,betas=(.9,.95),eps=1e-8,weight_decay=.01)
def lr_at(step,total):
 warm=math.ceil(.05*total)
 return 3e-4*((step+1)/warm if step<warm else .1+.9*.5*(1+math.cos(math.pi*(step-warm)/(max(1,total-1-warm)))))
def step_batch(m,head,opt,c,ix,device,name,micro=128,lbcoef=0,lr=None):
 opt.zero_grad(set_to_none=True)
 if lr is not None:
  for pg in opt.param_groups:pg['lr']=lr
 fixed=routes('train',name)[ix] if m.router is None else None
 raw=0.;weighted=0.;nll=0.;counts=np.zeros(8,np.int64);ce_router=0.
 if m.router is not None:
  hh=c['hidden'][ix].to(device).float();P=torch.softmax(m.router(hh/m.scale),-1);r=P.argmax(-1);fractions=F.one_hot(r,8).float().mean(0).detach();lb=8*(fractions*P.mean(0)).sum();raw=float(lb.detach());weighted=raw*lbcoef
  if lbcoef: (lb*lbcoef).backward()
 for a in range(0,len(ix),micro):
  sub=ix[a:a+micro];h=c['hidden'][sub].to(device);y=c['target'][sub].to(device);fr=torch.as_tensor(fixed[a:a+micro],device=device) if fixed is not None else None
  ho,d=m(h,fr);loss=F.cross_entropy(head(ho).float(),y);scaled=loss*(len(sub)/len(ix));scaled.backward();nll+=float(loss.detach())*len(sub)/len(ix);counts+=np.bincount(d['route'].detach().cpu().numpy(),minlength=8)
 if not np.isfinite(nll) or any(p.grad is not None and not torch.isfinite(p.grad).all() for p in m.parameters()):raise FloatingPointError('Nonfinite loss/gradient')
 gradnorm=float(torch.nn.utils.clip_grad_norm_(m.parameters(),1.0));updates=np.array([int(any(p.grad is not None for p in e.parameters())) for e in m.experts])
 opt.step();return dict(nll=nll,total=nll+weighted,lb_raw=raw,lb_weighted=weighted,grad_norm=gradnorm,counts=counts.tolist(),expert_update=updates.tolist())
def checkpoint(path,m,opt,step,epoch,next_batch,seen,orders,counts,updates,name,seed):
 save(path,dict(schema='normalized_route_learning_complete_v1',model=cpu_tree(m.state_dict()),optimizer=cpu_tree(opt.state_dict()),rng=rng(),step=step,epoch=epoch,next_batch=next_batch,seen=seen,orders=[o.tolist() for o in orders],expert_exposures=counts.tolist(),expert_updates=updates.tolist(),condition=name,seed=seed,config_sha=sha(ROOT/'config/frozen.json'),scale=float(m.scale)))
def smoke(device):
 configure(device);c=loadcache('train');head=FrozenHead(device);ix=np.arange(64);m=Branch(11,True).to(device);opt=optimizer(m);h=c['hidden'][ix].to(device);y=c['target'][ix].to(device)
 with torch.no_grad():
  b=head(h);p=head(m(h)[0]);logit_error=float((b.float()-p.float()).abs().max());assert logit_error==0
 assert sum(p.numel() for p in m.experts.parameters())==25165824
 assert all(not p.requires_grad for p in head.parameters())
 init=tensorhash(m.experts.state_dict());loss=F.cross_entropy(head(m(h)[0]).float(),y);loss.backward();first_router_grad=float(m.router.weight.grad.norm());assert first_router_grad==0
 down_grad=sum(float(e.down.weight.grad.norm()) for e in m.experts if e.down.weight.grad is not None);assert down_grad>0;opt.step();opt.zero_grad(set_to_none=True)
 loss=F.cross_entropy(head(m(h)[0]).float(),y);loss.backward();ce_grad=float(m.router.weight.grad.norm());assert ce_grad>0
 assert head.weight.grad is None and head.norm.grad is None
 # Resume serialization check: restore model, optimizer, all RNG; compare next matched update exactly.
 sm=ROOT/'smoke';sm.mkdir(exist_ok=True);save(sm/'resume.pt',dict(model=cpu_tree(m.state_dict()),optimizer=cpu_tree(opt.state_dict()),rng=rng()))
 m0=cpu_tree(m.state_dict());o0=cpu_tree(opt.state_dict());r0=rng();first=[]
 losses=[]
 for s in range(100):
  row=step_batch(m,head,opt,c,ix,device,'Learned',micro=64);losses.append(row['nll'])
  if s==0:first=cpu_tree(m.state_dict())
 m.load_state_dict(m0);opt.load_state_dict(o0);setrng(r0);step_batch(m,head,opt,c,ix,device,'Learned',micro=64);assert tensorhash(first)==tensorhash(m.state_dict())
 # Timing copy, full effective batch and CE microbatch semantics.
 del m,opt;torch.cuda.empty_cache();m=Branch(11,False).to(device);opt=optimizer(m);times=[]
 for s in range(10):
  sync(device);t=time.monotonic();step_batch(m,head,opt,c,np.arange(s*512,(s+1)*512),device,'T_S1');sync(device);times.append(time.monotonic()-t)
 t=time.monotonic();evaluate(None,head,c,device,indices=np.arange(2048));sync(device);eval_sec=(time.monotonic()-t)/2048
 rec=dict(status='PASS',initial_logits_max_abs=logit_error,expert_params=25165824,router_params=8192,first_router_CE_grad=first_router_grad,post_first_update_router_CE_grad=ce_grad,first_down_grad=down_grad,frozen_head_no_grad=True,small_fit_steps=100,small_fit_start=losses[0],small_fit_end=losses[-1],small_fit_min=min(losses),resume_next_update_exact=True,timing_full_batch512_micro128_seconds=times,median_step_seconds=float(np.median(times[2:])),eval_seconds_per_position=eval_sec,estimated20_training_eval_wall_seconds=20*(768*np.median(times[2:])+4*65402*eval_sec)/4,**memory(device))
 baseline,rr,gg=evaluate(None,head,loadcache('eval'),device);np.savez_compressed(sm/'baseline_eval.npz',nll=baseline,route=rr,gate=gg);write_json(sm/'receipt.json',rec);write_json(sm/'fit_losses.json',losses);print(json.dumps(rec),flush=True)
def train(name,seed,device,background=False):
 configure(device,seed);c=loadcache('train');e=loadcache('eval');co=condition(name);out=ROOT/('target/background' if background else f'training/{name}/seed{seed}');out.mkdir(parents=True,exist_ok=True)
 if (out/'complete.json').exists():print('REUSE COMPLETE',out,flush=True);return
 m=Branch(seed,co['router']=='learned').to(device);head=FrozenHead(device);opt=optimizer(m)
 allowed=np.arange(len(c['target']));epochs=3
 if background:
  target=json.load(open(ROOT/'config/target.json'))['feature_id'];hit=np.asarray(csr(c,True)[:,target].toarray()).flatten()>0;allowed=allowed[~hit];epochs=2
 gen=np.random.default_rng(seed);orders=[gen.permutation(allowed) for _ in range(epochs)];steps_per=math.ceil(len(allowed)/512);total=steps_per*epochs;start=time.monotonic();counts=np.zeros(8,np.int64);updates=np.zeros(8,np.int64);seen=step=0;start_epoch=start_batch=0
 init_hash=tensorhash(m.experts.state_dict());write_json(out/'identity.json',dict(condition=name,seed=seed,background=background,expert_init_sha=init_hash,parameters_experts=25165824,parameters_router=8192 if m.router is not None else 0,total_steps=total,epochs=epochs,positions=len(allowed)*epochs,TRAIN_unique=len(allowed),config_sha=sha(ROOT/'config/frozen.json')))
 writer=SummaryWriter(str(out/'tensorboard'))
 resume=out/'latest.pt'
 if resume.exists():
  st=torch.load(resume,map_location='cpu',weights_only=False);assert st['config_sha']==sha(ROOT/'config/frozen.json');m.load_state_dict(st['model']);opt.load_state_dict(st['optimizer']);setrng(st['rng']);step=st['step'];seen=st['seen'];start_epoch=st['epoch'];start_batch=st['next_batch'];counts=np.array(st['expert_exposures']);updates=np.array(st['expert_updates'])
 def assess(epoch):
  
  if epoch==0:
   n=np.load(ROOT/'smoke/baseline_eval.npz')['nll'];r=routes('eval',name) if m.router is None else np.full(len(n),-1,np.int16);g=np.ones(len(n),np.float32) if m.router is None else np.full(len(n),np.nan,np.float32)
   if m.router is not None:
    with torch.no_grad():
     for aa in range(0,len(n),2048):
      rt,gt,_=m.routing(e['hidden'][aa:aa+2048].to(device));r[aa:aa+len(rt)]=rt.cpu().numpy();g[aa:aa+len(rt)]=gt.cpu().numpy()
  else:n,r,g=evaluate(m,head,e,device,name)
  met,feat,support=metrics(n,e);np.savez_compressed(out/f'eval_epoch{epoch}.npz',nll=n,route=r,gate=g,feature_nll=feat,feature_support=support);trix=np.random.default_rng(20261019).choice(allowed,min(2048,len(allowed)),False);tr,_,_=evaluate(m,head,c,device,name,indices=trix);met.update(condition=name,seed=seed,epoch=epoch,step=step,seen=seen,train_diagnostic=float(tr.mean()),elapsed_seconds=time.monotonic()-start);write_json(out/f'metrics_epoch{epoch}.json',met)
  for field in ['overall','M_L','M_H','low_union','non_low_union','train_diagnostic']:writer.add_scalar('eval/'+field,met[field],seen)
  writer.flush();print('EPOCH',json.dumps(met),flush=True)
 if step==0:
  with torch.no_grad():
   ix=np.arange(64);base=head(c['hidden'][ix].to(device));pred=head(m(c['hidden'][ix].to(device),torch.as_tensor(routes('train',name)[ix],device=device) if m.router is None else None)[0]);assert torch.equal(base,pred)
  checkpoint(out/'epoch0.pt',m,opt,0,0,0,0,orders,counts,updates,name,seed);assess(0)
 deadline=__import__('datetime').datetime.fromisoformat(CFG['training_deadline_utc']).timestamp()
 for ep in range(start_epoch,epochs):
  order=orders[ep]
  for bi in range(start_batch if ep==start_epoch else 0,steps_per):
   if time.time()>=deadline:
    checkpoint(out/'latest.pt',m,opt,step,ep,bi,seen,orders,counts,updates,name,seed);write_json(out/'partial.json',dict(status='PARTIAL',reason='fixed training deadline',step=step,seen=seen));writer.close();return
   ix=order[bi*512:(bi+1)*512];t=time.monotonic();row=step_batch(m,head,opt,c,ix,device,name,micro=128,lbcoef=co['lambda_balance'],lr=lr_at(step,total));step+=1;seen+=len(ix);counts+=row['counts'];updates+=row['expert_update'];row.update(step=step,epoch=ep+1,seen=seen,N=len(ix),lr=opt.param_groups[0]['lr'],seconds=time.monotonic()-t)
   append(out/'steps.jsonl',row)
   tags={'train_lm_loss':row['nll'],'train_total_loss':row['total']}
   if m.router is not None:tags.update({'loss_component/load_balance_raw':row['lb_raw'],'loss_component/load_balance_weighted':row['lb_weighted']})
   for axis,value in [('updates',step),('tokens',seen)]:
    for k,v in tags.items():writer.add_scalar(axis+'/'+k,v,value)
   writer.add_scalar('updates/learning_rate',row['lr'],step);writer.add_scalar('progress/tokens_seen',seen,step);writer.add_scalar('progress/optimizer_step',step,seen);writer.add_scalar('progress/effective_tokens_per_update',len(ix),step)
   if step%64==0:checkpoint(out/'latest.pt',m,opt,step,ep,bi+1,seen,orders,counts,updates,name,seed);writer.flush();print('PROGRESS',name,seed,step,seen,flush=True)
  checkpoint(out/f'epoch{ep+1}.pt',m,opt,step,ep+1,0,seen,orders,counts,updates,name,seed);checkpoint(out/'latest.pt',m,opt,step,ep+1,0,seen,orders,counts,updates,name,seed);assess(ep+1)
 assert seen==epochs*len(allowed) and step==total
 # Natural routing and all feature exposure at endpoint; assigned owner only for fixed arms.
 for split,cc in [('train',c),('eval',e)]:
  if m.router is None:r=routes(split,name);owner=np.load(PREV/'metrics/core/owners.npz')[co['group']]
  else:
   rr=[]
   with torch.no_grad():
    for a in range(0,len(cc['target']),2048):rr.append(m.routing(cc['hidden'][a:a+2048].to(device))[0].cpu().numpy())
   r=np.concatenate(rr);owner=None
  if not background:exposure(split,r,name+f'_seed{seed}',owner)
 write_json(out/'complete.json',dict(status='COMPLETE',condition=name,seed=seed,background=background,steps=step,seen=seen,expert_exposures=counts,expert_updates=updates,seconds=time.monotonic()-start,init_expert_sha=init_hash,final_expert_sha=tensorhash(m.experts.state_dict()),**memory(device)));writer.close()
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--name',default='T_S1');ap.add_argument('--seed',type=int,default=11);ap.add_argument('--device',default='cuda:0');ap.add_argument('--smoke',action='store_true');ap.add_argument('--background',action='store_true');a=ap.parse_args()
 if a.smoke:smoke(a.device)
 else:train(a.name,a.seed,a.device,a.background)
