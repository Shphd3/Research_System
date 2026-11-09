"""Delete same-layer centeredhead64, retain960; exact R16 assets, no refit/training."""
from native_support import *
R=Path(cfg['parent_round'])
def remove(h,mu,q):return (h.float()-((h.float()-mu)@q)@q.T).to(h.dtype)
def selected(n,h,projected,ts,l):
 hh=h.expand(1+len(ts),-1,-1).clone();hh[0,:192]=projected[0,:192]
 for j,t in enumerate(ts):hh[j+1,t]=projected[0,t]
 mask=torch.zeros((len(hh),256),dtype=torch.long,device=n.dev);mask[:,:192]=1;yy=n.body(None,mask,start=l+1,emb=hh);taken=torch.cat([yy[0,ts],yy[torch.arange(1,len(ts)+1,device=n.dev),torch.tensor(ts,device=n.dev)]],0)
 return n.decode(taken)
def old_records(sid):return {(r['index'],r['layer'],r['condition'],r['scope']):r for r in json.load(open(E/'data/reference_outputs'/(sid+'.json')))}
def verify_original(n,cap,inds,sid,base):
 oldh=np.load(R/'data/eval_targets'/(sid+'.npz'));assert oldh['indices'].tolist()==inds;maximum=0.
 for l in range(28):
  h=cap[l][0,[rr[i]['position'] for i in inds]].float().cpu().numpy();maximum=max(maximum,float(abs(h-oldh['h'][l]).max()))
 assert maximum==0,('native layerstate replay drift',sid,maximum)
 ref=old_records(sid);nll=max(abs(r['NLL']-ref[(r['index'],0,'identity','none')]['NLL']) for r in base);top=sum(r['top1_id']!=ref[(r['index'],0,'identity','none')]['top1_id'] for r in base);assert nll<=1e-6 and top==0,(sid,nll,top)
 return {'seq_id':sid,'all28_targeth_max_abs':maximum,'identity_NLL_max_abs':nll,'identity_top1_changes':top}
rr=rows(E/'data/positions.jsonl')
@torch.inference_mode()
def smoke(model,rank):
 n=Native(model,rank);docs=rows(E/'data/evaluation_documents.jsonl');d=next(x for x in docs if x['seq_id']=='R11_A02_134');sid=d['seq_id'];inds=[i for i,r in enumerate(rr) if r['seq_id']==sid];ts=[rr[i]['position'] for i in inds];targets=[rr[i]['target_id'] for i in inds];y,cap=n.capture(d);full=n.decode(y[0,ts]);base=n.metrics(full,full,targets,inds);replay=verify_original(n,cap,inds,sid,base);old=old_records(sid);checks=[];t=144;j=ts.index(t);x,mask=n.inputs(d)
 for l in range(28):
  b,mu,q=basis(l,n.dev);h=cap[l];a=h[0,ts].double();mm=torch.tensor(b['mean'],device=n.dev,dtype=torch.float64);v=torch.tensor(b['V'],device=n.dev,dtype=torch.float64);z=a-mm;comp=a-(z@v[:,:64])@v[:,:64].T;direct=mm+(z@v[:,64:])@v[:,64:].T;err=float(abs(comp-direct).max());assert err<1e-8,(l,err)
  fullDelete=a-(z@v)@v.T;em=float(abs(fullDelete-mm).max());assert em<1e-8
  assert torch.equal(remove(h,mu,q[:,:0]),h),'empty delete must be exactidentity'
  back=n.decode(n.body(None,mask,start=l+1,emb=h)[0,ts]);noop=float(abs(back-full).max());nn=float(abs(back.log_softmax(-1)[torch.arange(len(ts),device=n.dev),torch.tensor(targets,device=n.dev)]-full.log_softmax(-1)[torch.arange(len(ts),device=n.dev),torch.tensor(targets,device=n.dev)]).max());assert noop<=.5 and nn<=.05
  check={'layer':l+1,'complement_vs960_FP64_max_abs':err,'deleteall_vsmean_FP64_max_abs':em,'noop_suffix_logits_max_abs':noop,'noop_suffix_NLL_max_abs':nn}
  if l in [0,13,27]:
   # replay oldkeep64 with identical combined batch shape and decoder shape.
   lg=selected(n,h,n.project(h,mu,q),ts,l);metrics=[]
   for k,scope in enumerate(cfg['scopes']):
    mets=n.metrics(lg[k*len(ts):(k+1)*len(ts)],full,targets,inds)
    for r in mets:
     ref=old[(r['index'],l+1,'head64',scope)];dif=abs(r['NLL']-ref['NLL']);assert dif<=.05 and r['top1_id']==ref['top1_id'],('keep64 replay',l,scope,r['index'],dif);metrics.append(dif)
   check['keep64_replay_NLL_max_abs']=max(metrics)
   for scope in cfg['scopes']:
    pp=remove(h,mu,q);hh=h.clone()
    if scope=='all_prefix':hh[:,:192]=pp[:,:192]
    else:hh[:,t]=pp[:,t]
    suffix=n.decode(n.body(None,mask,start=l+1,emb=hh)[0,t:t+1])
    def hook(mod,a,out):
     raw=out[0] if isinstance(out,tuple) else out;z=raw.clone();pp=remove(raw,mu,q)
     if scope=='all_prefix':z[:,:192]=pp[:,:192]
     else:z[:,t]=pp[:,t]
     return (z,*out[1:]) if isinstance(out,tuple) else z
    hd=n.layers[l].register_forward_hook(hook)
    try:hooked=n.decode(n.body(x,mask)[0,t:t+1])
    finally:hd.remove()
    e=float(abs(hooked-suffix).max());ne=float(abs(hooked.log_softmax(-1)[0,targets[j]]-suffix.log_softmax(-1)[0,targets[j]]));assert e<=.5 and ne<=.05 and hooked.argmax()==suffix.argmax(),('native deletehook mismatch',l,scope,e,ne);check[scope]={'logits_max_abs':e,'NLL_abs':ne}
  checks.append(check)
 xp=x.clone();mp=mask.clone();xp[:,t+1:]=0;mp[:,t+1:]=0;pr=n.decode(n.body(xp,mp)[0,t:t+1]);causal=float(abs(pr-full[j:j+1]).max());assert causal<=.5
 dump(E/'audit/03_numerics_smoke.json',{'pass':True,'replay':replay,'layers':checks,'causal_prefix_max_logits':causal,'torch':torch.__version__,'transformers':__import__('transformers').__version__,'device':torch.cuda.get_device_name(rank),'trainable_parameters':0,'PCA_refits':0,'training_updates':0,'top1_rule':'nativeargmax minID; complete top10 boundary tie=IDascending'})
 print('SMOKE_PASS',flush=True)
@torch.inference_mode()
def evaluate(model,rank):
 assert json.load(open(E/'audit/03_numerics_smoke.json'))['pass'];n=Native(model,rank);docs=sorted(rows(E/'data/evaluation_documents.jsonl'),key=lambda x:x['seq_id']);start=time.time();bas=[basis(l,n.dev)[1:] for l in range(28)];qs={f'delete_random{s}':torch.tensor(np.load(E/'data'/f'random{s}.npy'),device=n.dev,dtype=torch.float32) for s in cfg['seeds']['random']};count=0;chunks=E/'analysis/chunks';chunks.mkdir(exist_ok=True);freezehash=sha(E/'freeze.json')
 for ordinal,d in enumerate(docs):
  if ordinal%2!=rank:continue
  path=chunks/(d['seq_id']+'.json')
  if path.exists():
   prior=json.load(open(path));assert prior['complete'] and prior['freeze_sha256']==freezehash;continue
  sid=d['seq_id'];inds=[i for i,r in enumerate(rr) if r['seq_id']==sid];ts=[rr[i]['position'] for i in inds];targets=[rr[i]['target_id'] for i in inds];y,cap=n.capture(d);full=n.decode(y[0,ts]);base=n.metrics(full,full,targets,inds);replay=verify_original(n,cap,inds,sid,base);records=[]
  for r in base:r.update(layer=0,condition='identity',scope='none',readout='continuation')
  records+=base
  for l in range(28):
   h=cap[l];mu,q=bas[l];conds={'delete_head64':q,**qs}
   for name,qq in conds.items():
    projected=remove(h,mu,qq);st=norms(h,projected,mu,ts);logits=selected(n,h,projected,ts,l)
    if l==27:assert torch.equal(logits[:len(ts)],logits[len(ts):]),('last layer scope mismatch',sid,name)
    for k,scope in enumerate(cfg['scopes']):
     result=n.metrics(logits[k*len(ts):(k+1)*len(ts)],full,targets,inds)
     for j,r in enumerate(result):
      r.update(layer=l+1,condition=name,scope=scope,readout='continuation',**st[j]);r['prefix_retained_energy']=st[j]['prefix_retained_energy'] if scope=='all_prefix' else (st[j]['target_retained_energy']+ts[j])/(ts[j]+1);r['prefix_intervention_norm']=st[j]['prefix_intervention_norm'] if scope=='all_prefix' else st[j]['target_intervention_norm']/(ts[j]+1);r['prefix_relative_intervention']=st[j]['prefix_relative_intervention'] if scope=='all_prefix' else st[j]['target_relative_intervention']/(ts[j]+1)
     records+=result
  dump(path,{'complete':True,'seq_id':sid,'positions':len(inds),'freeze_sha256':freezehash,'native_replay':replay,'records':records});count+=1
  print(json.dumps({'rank':rank,'documents_done':count,'last':sid,'seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(rank)}),flush=True)
 assert all(not p.requires_grad and p.grad is None for p in model.parameters())
 dump(E/f'terminal_rank{rank}.json',{'complete':True,'rank':rank,'new_documents_this_attempt':count,'seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(rank),'PCA_refits':0,'training_updates':0})
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['smoke','evaluate'],required=True);p.add_argument('--rank',type=int,default=0);a=p.parse_args();model=init(a.rank)
 if a.stage=='smoke':smoke(model,a.rank)
 else:evaluate(model,a.rank)
if __name__=='__main__':
 try:main()
 except Exception as ex:dump(E/'audit'/f'failure_{int(time.time())}_{os.getpid()}.json',{'error':repr(ex),'traceback':traceback.format_exc()});raise
