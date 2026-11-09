"""Equal64 native interventions, two mean modes, fixed R16 coordinates."""
from native_support import *
R=Path(cfg['parent_round']);rr=rows(E/'data/positions.jsonl')
FM=['top1_agreement','full_top1_probability','full_top1_rank','target_probability','target_rank','NLL','KL_full','entropy','target_band_energy','prefix_band_energy','target_intervention_norm','target_relative_intervention','target_norm_ratio','prefix_intervention_norm','prefix_relative_intervention','prefix_norm_ratio','mean_norm','target_centered_norm']
IM=['index','layer','condition','scope','top1_id','full_top1_id','max_ties']
NAMES=[f'add_b{i:02d}' for i in range(16)]+[f'no_b{i:02d}' for i in range(16)]+['zero','full_centered','identity']
def projected(h,mu,v,code):
 a=h.float()-mu
 if code==32:return torch.zeros_like(h),torch.zeros_like(a[...,0])
 if code==33:return a.to(h.dtype),torch.ones_like(a[...,0])
 b=code%16;q=v[:,64*b:64*(b+1)];z=(a@q)@q.T;en=z.square().sum(-1)/a.square().sum(-1).clamp_min(1e-20)
 return (z+mu if code<16 else z).to(h.dtype),en

def continue_batch(n,h,zs,ts,l):
 B=1+len(ts);hh=h.expand(len(zs)*B,-1,-1).clone()
 for c,z in enumerate(zs):
  hh[c*B,:192]=z[0,:192]
  for j,t in enumerate(ts):hh[c*B+j+1,t]=z[0,t]
 mask=torch.zeros((len(hh),256),dtype=torch.long,device=n.dev);mask[:,:192]=1;y=n.body(None,mask,start=l+1,emb=hh);taken=[]
 for c in range(len(zs)):
  taken.extend([y[c*B,ts],y[torch.arange(c*B+1,(c+1)*B,device=n.dev),torch.tensor(ts,device=n.dev)]])
 return n.decode(torch.cat(taken)).reshape(len(zs),2*len(ts),-1)

def quantities(h,z,mu,en,ts,scope):
 hf=h.float();zf=z.float();pert=(zf-hf).square().sum(-1).sqrt();hn=hf.square().sum(-1).sqrt().clamp_min(1e-20);rel=pert/hn;ratio=zf.square().sum(-1).sqrt()/hn;cn=(hf-mu).square().sum(-1).sqrt();out=[]
 for t in ts:
  if scope==0:pre=(en[0,:t+1].mean(),pert[0,:t+1].mean(),rel[0,:t+1].mean(),ratio[0,:t+1].mean())
  else:pre=((en[0,t]+t)/(t+1),pert[0,t]/(t+1),rel[0,t]/(t+1),(ratio[0,t]+t)/(t+1))
  out.append(torch.stack([en[0,t],pre[0],pert[0,t],rel[0,t],ratio[0,t],pre[1],pre[2],pre[3],mu.norm(),cn[0,t]]))
 return torch.stack(out).cpu().numpy().astype(np.float32)

def metrics(logits,full,targets,indices,l,code,scope,extra):
 lp=logits.log_softmax(-1);flp=full.log_softmax(-1);p=lp.exp();fp=flp.exp();fi=full.argmax(-1);ti=logits.argmax(-1);ii=torch.arange(len(targets),device=logits.device);yy=torch.tensor(targets,device=logits.device)
 ff=logits[ii,fi];tt=logits[ii,yy]
 mt=torch.stack([(ti==fi).float(),p[ii,fi],(logits>ff[:,None]).sum(-1).float()+1,p[ii,yy],(logits>tt[:,None]).sum(-1).float()+1,-lp[ii,yy],(fp*(flp-lp)).sum(-1),-(p*lp).sum(-1)],-1).cpu().numpy()
 # Native BF16 logit ties are sorted by token ID; obtain every boundary tie if top32 is insufficient.
 vv,kk=logits.topk(32,-1);vv=vv.cpu().numpy();kk=kk.cpu().numpy();outids=[];outp=[]
 for j in range(len(indices)):
  order=np.lexsort((kk[j],-vv[j]));ids=kk[j,order[:10]]
  if vv[j].min()==vv[j,order[9]]:
   threshold=float(vv[j,order[9]]);above=torch.where(logits[j]>threshold)[0];equal=torch.where(logits[j]==threshold)[0];ids=torch.cat([above,equal[:10-len(above)]]).cpu().numpy();vals=logits[j,torch.tensor(ids,device=logits.device)].cpu().numpy();ids=ids[np.lexsort((ids,-vals))]
  outids.append(ids)
 tids=torch.tensor(np.array(outids),device=logits.device);probs=p.gather(1,tids).cpu().numpy()
 ints=np.column_stack([np.array(indices),np.full(len(indices),l),np.full(len(indices),code),np.full(len(indices),scope),ti.cpu().numpy(),fi.cpu().numpy(),(logits==logits.max(-1).values[:,None]).sum(-1).cpu().numpy()]).astype(np.int32)
 return ints,np.concatenate([mt,extra],1).astype(np.float32),np.array(outids,dtype=np.int32),probs.astype(np.float32)

def replay(n,cap,inds,sid,full):
 old=np.load(R/'data/eval_targets'/(sid+'.npz'));assert old['indices'].tolist()==inds
 error=max(float(abs(cap[l][0,[rr[i]['position'] for i in inds]].float().cpu().numpy()-old['h'][l]).max()) for l in range(28));assert error==0,(sid,error)
 prior=json.load(open(R/'supplements/20261104_delete_head64_keep960/data/reference_outputs'/(sid+'.json')));refs={r['index']:r for r in prior if r['condition']=='identity'};lp=full.log_softmax(-1);errors=[]
 for j,i in enumerate(inds):
  ref=refs[i];errors.append(abs(float(-lp[j,rr[i]['target_id']])-ref['NLL']));assert int(full[j].argmax())==ref['top1_id']
 assert max(errors)<=1e-6
 return {'targeth_max_abs':error,'baseline_NLL_max_abs':max(errors)}

@torch.inference_mode()
def smoke(model,rank):
 n=Native(model,rank);doc=next(d for d in rows(E/'data/evaluation_documents.jsonl') if d['seq_id']=='R11_A02_134');inds=[i for i,r in enumerate(rr) if r['seq_id']==doc['seq_id']];ts=[rr[i]['position'] for i in inds];targets=[rr[i]['target_id'] for i in inds];y,cap=n.capture(doc);full=n.decode(y[0,ts]);rp=replay(n,cap,inds,doc['seq_id'],full);old=json.load(open(R/'supplements/20261104_delete_head64_keep960/data/reference_outputs'/(doc['seq_id']+'.json')));old={(r['index'],r['layer'],r['condition'],r['scope']):r for r in old};checks=[]
 for l in range(28):
  b=np.load(R/'data/bases'/f'layer{l+1:02d}.npz');mu=torch.tensor(b['mean'],device=n.dev,dtype=torch.float32);v=torch.tensor(b['V'],device=n.dev,dtype=torch.float32);h=cap[l];x,mask=n.inputs(doc);back=n.decode(n.body(None,mask,start=l+1,emb=h)[0,ts]);err=float(abs(back-full).max());assert err<=.5
  hd=h.double();md=torch.tensor(b['mean'],device=n.dev,dtype=torch.float64);vd=torch.tensor(b['V'],device=n.dev,dtype=torch.float64);recon=md+((hd-md)@vd)@vd.T;ident=float(abs(recon-hd).max());assert ident<1e-8
  exact=(mu+(h.float()-mu)).to(h.dtype);relative=float((exact.float()-h.float()).norm()/h.float().norm());assert relative<=1e-6
  ck={'layer':l+1,'identity_FP64_max_abs':ident,'identity_FP32_BF16_relative':relative,'noop_logits_max_abs':err}
  if l in [0,13,27]:
   codes=[0,15,16,31];zs=[projected(h,mu,v,c)[0] for c in codes];bat=continue_batch(n,h,zs,ts,l);worst=0.;topchanges=0
   for j,c in enumerate(codes):
    single=continue_batch(n,h,[zs[j]],ts,l)[0];delta=float(abs(single-bat[j]).max());nll_delta=float(abs(single.log_softmax(-1)-bat[j].log_softmax(-1)).max());assert delta<=.5 and nll_delta<=.05,(l,c,delta,nll_delta);worst=max(worst,delta);topchanges+=int((single.argmax(-1)!=bat[j].argmax(-1)).sum())
   ck.update(batch_logits_max_abs=worst,batch_top1_changes=topchanges)
   for scope in range(2):
    for j,i in enumerate(inds):
     ref=old[(i,l+1,'head64',cfg['scopes'][scope])];val=float(-bat[0,scope*len(ts)+j].log_softmax(-1)[rr[i]['target_id']]);assert abs(val-ref['NLL'])<=.05 and int(bat[0,scope*len(ts)+j].argmax())==ref['top1_id']
   t=144;which=ts.index(t)
   for c in [0,7,15,16,23,31]:
    z,_=projected(h,mu,v,c);suffix=continue_batch(n,h,[z],ts,l)[0]
    for scope in range(2):
     def hook(mod,a,out):
      raw=out[0] if isinstance(out,tuple) else out;repl,_=projected(raw,mu,v,c);hh=raw.clone()
      if scope==0:hh[:,:192]=repl[:,:192]
      else:hh[:,t]=repl[:,t]
      return (hh,*out[1:]) if isinstance(out,tuple) else hh
     handle=n.layers[l].register_forward_hook(hook)
     try:actual=n.decode(n.body(x,mask)[0,t:t+1])[0]
     finally:handle.remove()
     expected=suffix[scope*len(ts)+which];delta=float(abs(actual-expected).max());nd=float(abs(actual.log_softmax(-1)[targets[which]]-expected.log_softmax(-1)[targets[which]]));assert delta<=.5 and nd<=.05,(l,c,scope,delta,nd)
   ck['actual_hook_pass']=True
  checks.append(ck)
 xp=x.clone();mp=mask.clone();xp[:,145:]=0;mp[:,145:]=0;pr=n.decode(n.body(xp,mp)[0,144:145]);ce=float(abs(pr-full[ts.index(144):ts.index(144)+1]).max());assert ce<=.5
 dump(E/'audit/03_numerics_smoke.json',{'pass':True,'layers':checks,'baseline_replay':rp,'causal_prefix_logits_max_abs':ce,'device':torch.cuda.get_device_name(rank),'torch':torch.__version__,'transformers':__import__('transformers').__version__,'PCA_refits':0,'training_updates':0,'parameter_updates':0})
 print('SMOKE_PASS',flush=True)

@torch.inference_mode()
def evaluate(model,rank):
 assert json.load(open(E/'audit/03_numerics_smoke.json'))['pass'];n=Native(model,rank);docs=sorted(rows(E/'data/evaluation_documents.jsonl'),key=lambda d:d['seq_id']);start=time.time();freeze=sha(E/'freeze.json');bases=[]
 for l in range(28):
  b=np.load(R/'data/bases'/f'layer{l+1:02d}.npz');bases.append((torch.tensor(b['mean'],device=n.dev,dtype=torch.float32),torch.tensor(b['V'],device=n.dev,dtype=torch.float32)))
 count=0;batch=cfg['condition_batch']
 for ordinal,d in enumerate(docs):
  if ordinal%2!=rank:continue
  path=E/'analysis/chunks'/(d['seq_id']+'.npz')
  if path.exists():
   prior=np.load(path);assert str(prior['freeze_sha256'])==freeze;continue
  inds=[i for i,r in enumerate(rr) if r['seq_id']==d['seq_id']];ts=[rr[i]['position'] for i in inds];targets=[rr[i]['target_id'] for i in inds];y,cap=n.capture(d);full=n.decode(y[0,ts]);rp=replay(n,cap,inds,d['seq_id'],full);parts=[];oldcheck=[]
  zero=np.zeros((len(inds),10),dtype=np.float32);parts.append(metrics(full,full,targets,inds,0,34,2,zero))
  refs=json.load(open(R/'supplements/20261104_delete_head64_keep960/data/reference_outputs'/(d['seq_id']+'.json')));refs={(r['index'],r['layer'],r['condition'],r['scope']):r for r in refs}
  for l in range(28):
   h=cap[l];mu,v=bases[l]
   for lo in range(0,34,batch):
    codes=list(range(lo,min(lo+batch,34)));pairs=[projected(h,mu,v,c) for c in codes];logits=continue_batch(n,h,[z for z,en in pairs],ts,l)
    for j,c in enumerate(codes):
     if l==27:assert torch.equal(logits[j,:len(ts)],logits[j,len(ts):])
     z,en=pairs[j]
     for scope in range(2):
      out=metrics(logits[j,scope*len(ts):(scope+1)*len(ts)],full,targets,inds,l+1,c,scope,quantities(h,z,mu,en,ts,scope));parts.append(out)
      if c==0:
       for k,i in enumerate(inds):
        ref=refs[(i,l+1,'head64',cfg['scopes'][scope])];oldcheck.append([abs(float(out[1][k,5])-ref['NLL']),int(out[0][k,4])!=ref['top1_id']])
  arrays=[np.concatenate([p[j] for p in parts],0) for j in range(4)];temp=path.with_suffix('.npz.tmp')
  with temp.open('wb') as f:np.savez_compressed(f,ints=arrays[0],floats=arrays[1],top10_ids=arrays[2],top10_probs=arrays[3],int_fields=IM,float_fields=FM,condition_names=NAMES,freeze_sha256=freeze,baseline_replay=json.dumps(rp),oldhead_replay=np.array(oldcheck))
  temp.replace(path);count+=1
  print(json.dumps({'rank':rank,'documents_done':count,'last':d['seq_id'],'rows':len(arrays[0]),'seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(rank),'oldhead_NLL_max_abs':float(np.array(oldcheck)[:,0].max()),'oldhead_top1_changes':int(np.array(oldcheck)[:,1].sum())}),flush=True)
 assert all(not p.requires_grad and p.grad is None for p in model.parameters())
 dump(E/f'terminal_rank{rank}.json',{'complete':True,'rank':rank,'documents':count,'seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(rank),'training_updates':0,'PCA_refits':0})
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['smoke','evaluate'],required=True);p.add_argument('--rank',type=int,default=0);a=p.parse_args();m=init(a.rank)
 if a.stage=='smoke':smoke(m,a.rank)
 else:evaluate(m,a.rank)
if __name__=='__main__':
 try:main()
 except Exception as ex:dump(E/'audit'/f'failure_{int(time.time())}_{os.getpid()}.json',{'error':repr(ex),'traceback':traceback.format_exc()});raise
