"""Frozen-cache analysis. No model load, inference, training, graph construction or pair counts."""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false')
import sys,json,csv,time,hashlib,io,platform,subprocess,traceback,resource,fcntl
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from collections import deque,Counter
import multiprocessing as mp
import numpy as np
from scipy.stats import rankdata

F=16384
R=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z')
E=R.parents[2]
BASE='/data/share/Qwen3-0.6B-Base'
LAYERS=np.arange(2,29,2)
HASHES={'decoder_geometry.npz':'b74cc20f563ea535c5b4d05e9f58bb3411f6bd6138d969afe4b25edbe4c28a8e','feature_frequency.npz':'f345204412633144a7f1af36668cb3e2a98dbcaf03ef66f43ce3ace40c916c7c','graphs/reduced_D.json':'d1c42c3c82c34057b8edb3a5203aee607e592bcc7318260dc7f2e60e5ae878b5','graphs/reduced_V.json':'5615253d0aba4ee186c2e3498f8f538db159e50d98b080c1c5dd7c23870b701a','graphs/raw_edges.npz':'e017e5d43235f4ed74691e2afc4ca003387e1ac96dee76de1f635ecade5806e1','split_manifest.json':'372cbbb82ed0bd7433b377b637a27c27f0b607224a2eec90549339c76f909c35','input_identity.json':'cb5d65d45fcb345af207e767afbd429dcc45f71768e47a8139e280081cdd1113','cache_binding.json':'f0808ca0dd060a97b2b4b3dcb219a45c2c60976cf63299507803152e52ec7ee8'}

def read(p):return json.loads(Path(p).read_text())
def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float) and not np.isfinite(x):return None
 return x
def put(p,x):
 p=Path(p);q=p.with_name(p.name+'.tmp');q.write_text(json.dumps(clean(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n');os.replace(q,p)
def table(p,rows,fields=None):
 it=iter(rows);first=next(it,None)
 with Path(p).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or (list(first) if first else ['status']));w.writeheader()
  if first is not None:w.writerow(clean(first))
  for row in it:w.writerow(clean(row))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def log(out,event,**kw):
 x=clean({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'event':event,**kw});print(json.dumps(x,ensure_ascii=False),flush=True)
 with (out/'events.jsonl').open('a') as f:f.write(json.dumps(x,ensure_ascii=False)+'\n')
def rho(h,l):
 ok=np.isfinite(l);a=h[ok];b=l[ok]
 if len(a)<2 or np.ptp(a)==0 or np.ptp(b)==0:return None
 return float(np.corrcoef(rankdata(a,method='average'),rankdata(b,method='average'))[0,1])
def summary(a):
 a=np.asarray(a);a=a[np.isfinite(a)]
 if not len(a):return {'valid_n':0,'mean':None,'q25':None,'median':None,'q75':None,'min':None,'max':None}
 q=np.quantile(a,[.25,.5,.75],method='linear')
 return dict(valid_n=len(a),mean=float(a.mean()),q25=q[0],median=q[1],q75=q[2],min=a.min(),max=a.max())
def share(norm):
 if norm.shape[0]!=14 or np.any(~np.isfinite(norm)) or np.any(norm<0):raise ValueError('INVALID_GEOMETRY_OR_LAYER_COUNT')
 den=norm.sum(0,dtype=np.float64)
 return np.divide(norm,den,out=np.full(norm.shape,np.nan),where=den>0)
def reservoir_merge(old,seen,pos,z,rng,k=5):
 total=seen+len(pos)
 if not total:return [],0
 take=rng.choice(total,size=min(k,total),replace=False)
 old_count=int((take<seen).sum())
 chosen=[old[i] for i in rng.choice(len(old),size=old_count,replace=False)] if old_count else []
 chosen.extend((int(pos[i-seen]),float(z[i-seen])) for i in take if i>=seen)
 return sorted(chosen),total

def correctness():
 assert np.allclose((share(np.ones((14,1)))*LAYERS[:,None]).sum(0),15)
 for index,val in [(0,2),(13,28)]:
  x=np.zeros((14,1));x[index]=1;assert float((share(x)*LAYERS[:,None]).sum())==val
 assert np.isnan(share(np.zeros((14,1)))).all()
 x=np.arange(1,29).reshape(14,2).astype(float);assert np.allclose(share(x),share(7*x))
 for invalid in [np.full((14,1),np.nan),np.ones((13,1)),-np.ones((14,1))]:
  try:share(invalid)
  except ValueError:pass
  else:raise AssertionError('known-bad geometry accepted')
 def reservoir_test():
  rng=np.random.Generator(np.random.PCG64(20261014));old=[];seen=0
  for pos in [np.arange(3),np.arange(3,8),np.arange(8,20)]:old,seen=reservoir_merge(old,seen,pos,np.ones(len(pos)),rng)
  return old,seen
 assert reservoir_test()==reservoir_test();ss,nn=reservoir_test();assert nn==20 and len({i for i,z in ss})==5
 # Single-frequency overlap is valid if both groups have actual >=20 observations.
 assert max(np.ones(20).min(),np.ones(20).min())==min(np.ones(20).max(),np.ones(20).max())
 return {'status':'PASS','uniform_L':15,'endpoints':[2,28],'zero_norm':'NA','bad_input_rejected':True,'reservoir_fixed_order_determinism':True,'performance_smoke':'NOT_RUN_USER_EXCLUDED'}

def geometry(out):
 import torch
 assert torch.cuda.device_count()==4,'EXPECTED_EXACTLY_FOUR_GPUS'
 devices=[torch.cuda.get_device_properties(i) for i in range(4)]
 assert all(('H100' in d.name or 'N6LS' in d.name) and d.total_memory>70<<30 for d in devices),'WRONG_GPU_PROFILE'
 torch.set_num_threads(1);torch.cuda.set_device(0);torch.cuda.set_per_process_memory_fraction((4<<30)/devices[0].total_memory,0)
 env={'host':platform.node(),'python':sys.version,'numpy':np.__version__,'torch':torch.__version__,'cuda':torch.version.cuda,'gpu_names':[d.name for d in devices],'gpu_total_bytes':[d.total_memory for d in devices],'cpu_affinity':sorted(os.sched_getaffinity(0)),'profile':os.environ.get('RESOURCE_PROFILE'),'image':os.environ.get('IMAGE_URL')};put(out/'environment.json',env)
 checks=correctness();put(out/'correctness.json',checks)
 manifest=[]
 for rel,wanted in HASHES.items():
  p=R/rel;actual=sha(p);assert actual==wanted,('INPUT_HASH_MISMATCH',rel);manifest.append({'path':str(p),'sha256':actual,'bytes':p.stat().st_size})
 binding=read(R/'cache_binding.json');sp=read(R/'split_manifest.json');identity=read(R/'input_identity.json')
 assert binding['checkpoint_sha256']==identity['checkpoint']['checkpoint_sha256']
 assert binding['layers_zero_based']==list(range(1,28,2)) and binding['window_positions']==10485760 and binding['F']==F
 assert sp['N_D']==5238097 and sp['N_V']==5247663
 fd=np.load(R/'feature_frequency.npz');n=fd['n'];zs=fd['zsum'];norms=np.load(R/'decoder_geometry.npz');norm=norms['norm'].astype(np.float64);rawnorm=norms['raw_norm']
 assert norm.shape==(14,F) and np.array_equal(rawnorm,norm*norms['rms'][:,None])
 graphs=[read(R/f'graphs/reduced_{s}.json') for s in ['D','V']];h=np.array([g['depth'] for g in graphs]);indeg=[];outdeg=[]
 for g in graphs:
  ii=np.zeros(F,np.int64);oo=np.array(list(map(len,g['lists'])))
  for a,us in enumerate(g['lists']):
   ii[us]+=1;assert g['depth'][a]==(1+max(g['depth'][u] for u in us) if us else 0)
  indeg.append(ii);outdeg.append(oo)
 qualified=(n>=200).all(0);isolated=(np.array(indeg)+np.array(outdeg))==0;Q=qualified&~isolated[1]
 assert Q.sum()==15537 and np.array_equal(Q,qualified)
 anchors=sorted(np.flatnonzero(Q&(h[1]==h[1,Q].max())).tolist())[:3];assert anchors==[937,3461]
 subsets={}
 for a in anchors:
  seen=set();todo=[a]
  while todo:
   v=todo.pop()
   if v in seen:continue
   seen.add(v);todo.extend(graphs[1]['lists'][v])
  subsets[a]=sorted(seen)
 nodes=sorted(set().union(*map(set,subsets.values())));edges=sorted({(a,u) for a in nodes for u in graphs[1]['lists'][a]});assert len(nodes)==30 and len(edges)==101
 # Freeze graph-only selection and D frequency edges before the first new p/L readout.
 x=np.log10(n[0]/sp['N_D'],where=n[0]>0,out=np.full(F,np.nan));bound=np.unique(np.quantile(x[Q],np.linspace(0,1,6),method='linear'));bins=np.searchsorted(bound[1:-1],x,side='right') if len(bound)>1 else np.zeros(F,int)
 put(out/'selection_frozen_before_geometry.json',{'anchors':anchors,'subsets':subsets,'nodes':nodes,'edges':edges,'primary_n':int(Q.sum()),'D_log10_frequency_edges':bound,'frequency_bin_count':max(1,len(bound)-1),'selection_does_not_use_decoder':True})
 put(out/'input_reuse_manifest.json',{'files':manifest,'binding':binding,'asset_ids':['representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z','analysis_crosscoder_feature_relation_phase1_20261013t173130z','dclm_crosscoder_direct_bins_1b_a15_20261013','tokenizer_qwen3_0p6b_base'],'code_sha256':sha(__file__),'protocol_sha256':sha(out/'protocol_frozen.md'),'no_checkpoint_or_model_load':True})
 # FP64 GPU normalization; CPU formula identity checked on the complete small geometry array.
 gn=torch.as_tensor(norm,device='cuda:0',dtype=torch.float64);den=gn.sum(0);gp=torch.where(den[None,:]>0,gn/den[None,:],torch.full_like(gn,float('nan')));p=gp.cpu().numpy();L=(gp*torch.as_tensor(LAYERS[:,None],device='cuda:0')).sum(0).cpu().numpy()
 assert np.allclose(p,share(norm),atol=1e-14,rtol=1e-14,equal_nan=True)
 pr=share(rawnorm);Lr=(pr*LAYERS[:,None]).sum(0);good=np.isfinite(L);assert np.allclose(p[:,good].sum(0),1,atol=1e-12) and np.all((L[good]>=2-1e-12)&(L[good]<=28+1e-12))
 np.savez(out/'derived_geometry.npz',p=p,L=L,p_raw=pr,L_raw=Lr,h=h,n=n,Q=Q,nodes=nodes,layers=LAYERS,frequency_bins=bins,D_log10_frequency=x)
 def members():
  for a in range(F):yield {'feature':a,'n_D':n[0,a],'n_V':n[1,a],'h_D':h[0,a],'h_V':h[1,a],'in_D':indeg[0][a],'out_D':outdeg[0][a],'in_V':indeg[1][a],'out_V':outdeg[1][a],'support_qualified':qualified[a],'primary_Q':Q[a],'L':L[a],'L_raw':Lr[a]}
 table(out/'hierarchy_members.csv',members());counts=[]
 for si,s in enumerate(['D','V']):
  for depth in range(int(h[si].max())+1):
   sel=h[si]==depth
   for category,mask in [('all',np.ones(F,bool)),('both_support_ge200',qualified),('primary_Q',Q),('local_zero',n[si]==0),('local_1_to199',(n[si]>0)&(n[si]<200)),('isolated',isolated[si]),('nonisolated_leaf',~isolated[si]&(outdeg[si]==0))]:counts.append({'side':s,'h':depth,'category':category,'nodes':int((sel&mask).sum())})
 table(out/'hierarchy_counts.csv',counts)
 means=np.vstack([zs[0]/sp['N_D'],zs[1]/sp['N_V'],zs.sum(0)/10485760])
 def response():
  for a in range(F):
   for li,l in enumerate(LAYERS):
    row={'feature':a,'layer_one_based':l,'h_V':h[1,a],'h_D':h[0,a],'primary_Q':Q[a],'norm':norm[li,a],'raw_norm':rawnorm[li,a],'p':p[li,a],'p_raw':pr[li,a],'L':L[a],'L_raw':Lr[a]}
    for si,s in enumerate(['D','V','all']):row.update({f'mean_z_{s}':means[si,a],f'mean_amplitude_{s}':means[si,a]*norm[li,a],f'mean_raw_amplitude_{s}':means[si,a]*rawnorm[li,a]})
    row['missing_reason']='' if good[a] else 'ZERO_TOTAL_DECODER_NORM';yield row
 table(out/'feature_layer_response.csv',response())
 stats=[];meanp=[];correlations={}
 for label,hh,ll,pp in [('V_train_normalized',h[1],L,p),('D_train_normalized',h[0],L,p),('V_raw_coordinate',h[1],Lr,pr)]:
  correlations[label]={'rho':rho(hh[Q],ll[Q]),'valid_features':int((Q&np.isfinite(ll)).sum())}
  for depth in range(int(hh[Q].max())+1):
   mask=Q&(hh==depth);stats.append({'condition':label,'h':depth,'n_features':int(mask.sum()),**summary(ll[mask]),'rho_overall':correlations[label]['rho']})
   valid=mask&np.isfinite(ll);row={'condition':label,'h':depth,'n_features':int(mask.sum()),'valid_n':int(valid.sum()),'NA_n':int((mask&~valid).sum())}
   for li,l in enumerate(LAYERS):row[f'mean_p_layer{l}']=pp[li,valid].mean() if valid.any() else None
   meanp.append(row)
 table(out/'depth_vs_layer_summary.csv',stats);table(out/'hierarchy_mean_p.csv',meanp)
 freqrows=[];freqsummary={}
 for si,s in [(1,'V'),(0,'D')]:
  rows=[]
  for b in range(max(1,len(bound)-1)):
   for loh in range(5):
    a=Q&(bins==b)&(h[si]==loh)&good;u=Q&(bins==b)&(h[si]==loh+1)&good
    row={'graph':s,'frequency_bin':b,'h_low':loh,'h_high':loh+1,'bin_low':bound[b] if len(bound)>1 else bound[0],'bin_high':bound[b+1] if len(bound)>1 else bound[0],'pre_n_low':int(a.sum()),'pre_n_high':int(u.sum()),'overlap_low':None,'overlap_high':None,'n_low':0,'n_high':0,'delta_median_L':None,'status':'NO_GROUP','fixed_frequency_local':False}
    if a.any() and u.any():
     left=max(x[a].min(),x[u].min());right=min(x[a].max(),x[u].max());row.update(overlap_low=left,overlap_high=right)
     if left>right:row['status']='NO_OVERLAP'
     else:
      aa=a&(x>=left)&(x<=right);uu=u&(x>=left)&(x<=right);na=int(aa.sum());nu=int(uu.sum());fixed=left==right;row.update(n_low=na,n_high=nu,fixed_frequency_local=fixed)
      for label,sel in [('low',aa),('high',uu)]:
       for k,v in summary(x[sel]).items():row[f'x_{label}_{k}']=v
       for k,v in summary(L[sel]).items():row[f'L_{label}_{k}']=v
      row['delta_median_L']=float(np.median(L[uu])-np.median(L[aa])) if na and nu else None
      row['status']=('FIXED_FREQUENCY_LOCAL' if fixed else 'COMPARABLE_RANGE') if na>=20 and nu>=20 else 'SMALL_N' if na and nu else 'NO_ACTUAL_NODES'
    rows.append(row)
  accepted=[v for v in rows if v['status'] in ['COMPARABLE_RANGE','FIXED_FREQUENCY_LOCAL']];ds=np.array([v['delta_median_L'] for v in accepted]);freqsummary[s]={'accepted_cells':len(accepted),'median_delta':float(np.median(ds)) if len(ds) else None,'positive':int((ds>0).sum()),'zero':int((ds==0).sum()),'negative':int((ds<0).sum()),'covered_frequency_bins':sorted({v['frequency_bin'] for v in accepted}),'covered_h_pairs':sorted({(v['h_low'],v['h_high']) for v in accepted}),'fixed_frequency_accepted':sum(v['fixed_frequency_local'] for v in accepted),'statuses':dict(Counter(v['status'] for v in rows))};freqrows+=rows
 fields=list(dict.fromkeys(k for row in freqrows for k in row));table(out/'frequency_overlap_comparison.csv',freqrows,fields)
 binrows=[]
 for b in range(max(1,len(bound)-1)):
  for si,s in enumerate(['D','V']):
   for depth in range(6):binrows.append({'frequency_bin':b,'graph':s,'h':depth,'n':int((Q&(bins==b)&(h[si]==depth)).sum())})
 table(out/'frequency_bin_counts.csv',binrows)
 raw=np.load(R/'graphs/raw_edges.npz');lookup={(int(a),int(u)):i for i,(a,u) in enumerate(zip(raw['A'],raw['u']))};nr=[];er=[]
 for a in nodes:nr.append({'feature':a,'h':h[1,a],'n_D':n[0,a],'n_V':n[1,a],'frequency_V':n[1,a]/sp['N_V'],'panels':','.join(str(k) for k,vs in subsets.items() if a in vs)})
 for i,(a,u) in enumerate(edges):
  k=lookup[a,u];assert bool(raw['passV'][k]);er.append({'edge_id':i+1,'A':a,'u':u,'h_A':h[1,a],'h_u':h[1,u],'nA_D':n[0,a],'nA_V':n[1,a],'nu_D':n[0,u],'nu_V':n[1,u],'c_D':raw['cD'][k],'c_V':raw['cV'][k],'P_u_given_A_V':raw['cV'][k]/n[1,a],'panels':','.join(str(k) for k,vs in subsets.items() if a in vs)})
 table(out/'graph1_nodes.csv',nr);table(out/'graph1_edges.csv',er)
 table(out/'figure2_source.csv',({'feature':a,'h':h[1,a],'layer':l,'p':p[li,a]} for a in sorted(nodes,key=lambda a:(h[1,a],a)) for li,l in enumerate(LAYERS)))
 rng=np.random.Generator(np.random.PCG64(20261014));jit=rng.uniform(-.12,.12,F)
 table(out/'figure3_source.csv',({'feature':a,'h':h[1,a],'L':L[a],'x_for_plot':h[1,a]+jit[a],'n_D':n[0,a],'frequency_bin':bins[a]} for a in np.flatnonzero(Q)))
 result={'correlations':correlations,'group_stats':stats,'frequency_summary':freqsummary,'main_features':int(Q.sum()),'primary_equals_support_only':bool(np.array_equal(Q,qualified)),'nodes':nodes,'anchors':[{'feature':a,'h_V':int(h[1,a]),'h_D':int(h[0,a]),'L':float(L[a]),'p':p[:,a].tolist()} for a in anchors],'mean_p':meanp,'geometry_identity_max_abs':float(np.nanmax(np.abs(p-share(norm)))),'GPU_parent_peak_allocated':torch.cuda.max_memory_allocated(0),'independence':'features dependent; one bin; original documents UNKNOWN','no_pvalues_or_CI':True}
 put(out/'results.json',result);log(out,'GEOMETRY_COMPLETE',correlations=correlations,frequency=freqsummary,anchors=result['anchors'])
 return result

_torch=None;_device=None
def worker_init():
 global _torch,_device
 import torch
 _torch=torch;rank=(mp.current_process()._identity[0]-1)%4;torch.set_num_threads(1);torch.cuda.set_device(rank);torch.cuda.set_per_process_memory_fraction((4<<30)/torch.cuda.get_device_properties(rank).total_memory,rank);_device=rank

def scan_chunk(args):
 meta,nodes,blocks=args;tick=time.monotonic();cpu=time.process_time();buf=Path(meta['file']).read_bytes();assert hashlib.sha256(buf).hexdigest()==meta['sha256'],'CSR_CHUNK_HASH_MISMATCH'
 lo=meta['start'];hi=meta['end'];ends=np.array([b['position_end'] for b in blocks]);labels=np.array([b['side']=='V' for b in blocks]);rowside=labels[np.searchsorted(ends,np.arange(lo,hi),side='right')]
 if not rowside.any():return {'features':np.empty(0,np.uint16),'positions':np.empty(0,np.int64),'z':np.empty(0,np.float32),'device':_device,'bytes':len(buf),'seconds':time.monotonic()-tick,'cpu_seconds':time.process_time()-cpu,'peak_allocated':0,'chunk':meta['file']}
 with np.load(io.BytesIO(buf),allow_pickle=False) as d:ptr=d['ptr'];ids=d['ids'];z=d['z']
 assert len(ptr)==hi-lo+1 and ptr[0]==0 and ptr[-1]==len(ids)==len(z) and len(ids)==meta['nnz']
 torch=_torch;dev=f'cuda:{_device}'
 with torch.inference_mode():
  lut=torch.zeros(F,dtype=torch.bool,device=dev);lut[torch.tensor(nodes,device=dev)]=True;ii=torch.from_numpy(ids.astype(np.int64)).to(dev);selected=lut[ii].nonzero().flatten();pp=torch.from_numpy(ptr.astype(np.int64)).to(dev);row=torch.searchsorted(pp,selected,right=True)-1;sv=torch.from_numpy(rowside).to(dev);keep=sv[row];selected=selected[keep];row=row[keep]
  selected_cpu=selected.cpu().numpy();rows_cpu=row.cpu().numpy();feature=ids[selected_cpu].copy();values=z[selected_cpu].copy()
 assert np.isfinite(values).all() and (values>0).all()
 peak=torch.cuda.max_memory_allocated(_device);del ii,selected,pp,row,sv,keep,lut
 return {'features':feature,'positions':lo+rows_cpu,'z':values,'device':_device,'bytes':len(buf),'seconds':time.monotonic()-tick,'cpu_seconds':time.process_time()-cpu,'peak_allocated':peak,'chunk':meta['file']}

def texts(out,result):
 tick=time.monotonic();nodes=result['nodes'];sp=read(R/'split_manifest.json');fd=np.load(R/'feature_frequency.npz');chunks=[]
 for i in range(4):chunks+=read(R/f'feature_cache/rank{i}/manifest.json')['chunks']
 chunks.sort(key=lambda d:d['start']);assert chunks[0]['start']==0 and chunks[-1]['end']==10485760 and all(a['end']==b['start'] for a,b in zip(chunks,chunks[1:]))
 for c in chunks:assert c['binding']==read(R/'cache_binding.json') and Path(c['file']).stat().st_size==c['bytes']
 pools={a:[] for a in nodes};tops={a:[] for a in nodes};seen={a:0 for a in nodes};rngs={a:np.random.Generator(np.random.PCG64(int.from_bytes(hashlib.sha256(f'20261014:hierarchy_decoder:V:{a}:random'.encode()).digest()[:8],'little'))) for a in nodes};tele=[]
 with ProcessPoolExecutor(max_workers=4,mp_context=mp.get_context('spawn'),initializer=worker_init) as pool:
  jobs=iter((c,nodes,sp['blocks']) for c in chunks);pending=deque()
  for _ in range(8):
   arg=next(jobs,None)
   if arg is not None:pending.append(pool.submit(scan_chunk,arg))
  count=0
  while pending:
   d=pending.popleft().result();count+=1
   for a in nodes:
    m=d['features']==a;pos=d['positions'][m];z=d['z'][m]
    if len(pos):
     pools[a],seen[a]=reservoir_merge(pools[a],seen[a],pos,z,rngs[a]);k=min(3,len(pos));order=np.lexsort((pos,-z))[:k];tops[a]=sorted(tops[a]+[(int(pos[i]),float(z[i])) for i in order],key=lambda t:(-t[1],t[0]))[:3]
   tele.append({k:v for k,v in d.items() if k not in ['features','positions','z']});arg=next(jobs,None)
   if arg is not None:pending.append(pool.submit(scan_chunk,arg))
   if count%32==0:log(out,'CSR_PROGRESS',chunks=count,total=640,read_GiB=sum(v['bytes'] for v in tele)/(1<<30),selected_V_seen=sum(seen.values()))
 assert all(seen[a]==fd['n'][1,a] for a in nodes),'SELECTED_FEATURE_SUPPORT_MISMATCH'
 assert len(tele)==640
 put(out/'cache_scan_receipt.json',{'chunks':len(tele),'bytes_read':sum(v['bytes'] for v in tele),'all_chunk_hashes_match':True,'counts_match_saved_nV':True,'seconds':time.monotonic()-tick,'worker_cpu_seconds_sum':sum(v['cpu_seconds'] for v in tele),'gpu_devices_used':sorted({v['device'] for v in tele}),'peak_allocated_by_device':{str(i):max(v['peak_allocated'] for v in tele if v['device']==i) for i in range(4)},'chunks_detail':tele})
 selections=[]
 for a in nodes:
  d={}
  for mode,vals in [('random',pools[a]),('high_activation',tops[a])]:
   for pos,z in vals:
    if pos not in d:d[pos]={'feature':a,'eligible_position':pos,'z':z,'selection_labels':[]}
    d[pos]['selection_labels'].append(mode)
  selections.extend(d[pos] for pos in sorted(d))
 put(out/'text_sample_selection.json',{'examples':selections,'sampling_population':'all V positions where this feature active','random_slots':150,'high_slots':90,'unique_feature_position_rows':len(selections),'global_position_order_fixed':True,'seeds':'SHA256 first8 little endian, per feature; PCG64'})
 # Local tokenizer only; this API loads no model weights.
 from transformers import AutoTokenizer
 tokenizer=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 data=E/'data/direct_dclm_bins_a15/index_val';manifest=read(data/'manifest.json')
 for name,digest in manifest['files'].items():assert sha(data/name)==digest,'TOKEN_INDEX_HASH_MISMATCH'
 records=np.load(data/'records.npy',mmap_mode='r');prefix=np.load(data/'prefix.npy',mmap_mode='r');maps={};norm=np.load(R/'decoder_geometry.npz')['norm'].astype(np.float64);geom=np.load(out/'derived_geometry.npz');h=geom['h'];ends=np.array([b['position_end'] for b in sp['blocks']]);examples=[];amp=[]
 for row in selections:
  pos=row['eligible_position'];a=row['feature'];ctx=int(np.searchsorted(prefix,pos,side='right')-1);fi,start,n,limit=map(int,records[ctx]);source=manifest['sources'][fi]
  if fi not in maps:
   sourcepath=Path(source['path']);st=sourcepath.stat();assert st.st_size==source['bytes'] and st.st_mtime_ns==source['mtime_ns'];maps[fi]=np.memmap(sourcepath,dtype='<u4',mode='r')
  ids=np.asarray(maps[fi][start:start+n]);eligible=np.flatnonzero(~np.isin(ids,manifest['excluded_ids']))[:limit];local=pos-int(prefix[ctx]);t=int(eligible[local]);bl=int(np.searchsorted(ends,pos,side='right'));assert sp['blocks'][bl]['side']=='V'
  tokens=ids.astype(int).tolist();decode=lambda tok:tokenizer.decode(tok,skip_special_tokens=False,clean_up_tokenization_spaces=False)
  ex=dict(row,side='V',h_V=int(h[1,a]),h_D=int(h[0,a]),block=bl,context_index=ctx,source_bin=source['path'],source_sha256=source['sha256'],target_absolute_offset=start+t,target_context_offset=t,target_token_id=tokens[t],target_token_text=decode([tokens[t]]),left_text=decode(tokens[max(0,t-80):t]),right_reading_aid=decode(tokens[t+1:min(n,t+81)]),model_visible_prefix=decode(tokens[:t+1]),model_visible_prefix_includes_target=True,original_document_id='UNKNOWN',layer_amplitude=(row['z']*norm[:,a]).tolist());examples.append(ex)
  for li,l in enumerate(LAYERS):amp.append({'feature':a,'eligible_position':pos,'layer':l,'z':row['z'],'norm':norm[li,a],'amplitude':row['z']*norm[li,a]})
 with (out/'text_examples.jsonl').open('w') as f:
  for ex in examples:f.write(json.dumps(clean(ex),ensure_ascii=False)+'\n')
 table(out/'text_layer_amplitude.csv',amp);profiles=[]
 for a in nodes:
  for mode in ['random','high_activation']:
   rows=[v for v in examples if v['feature']==a and mode in v['selection_labels']];c=Counter(v['context_index'] for v in rows);profiles.append({'feature':a,'mode':mode,'rows':len(rows),'unique_contexts':len(c),'largest_context_display_count':max(c.values()) if c else 0,'context_counts':dict(c),'target_tokens':[v['target_token_text'] for v in rows]})
 put(out/'text_profiles.json',profiles)
 with (out/'text_examples_cn.md').open('w') as f:
  f.write('# 固定30节点文本：随机与高激活\n\n每节点从V活跃位置均匀抽5条随机，并取z最大的3条。随机不是独立文档抽样。目标token与包含它的前文用于解释；右文仅辅助阅读。完整位置与14层幅度见JSONL及text_layer_amplitude.csv。不得从8条例子认证单义语义。\n\n')
  for a in nodes:
   f.write(f'## Feature {a}，h_V={h[1,a]}\n\n')
   for ex in (v for v in examples if v['feature']==a):
    f.write(f"### 位置{ex['eligible_position']}｜{','.join(ex['selection_labels'])}｜z={ex['z']:.7g}\n\n上下文{ex['context_index']}，目标offset={ex['target_context_offset']}，目标token={json.dumps(ex['target_token_text'],ensure_ascii=False)}；原文档未知。\n\n包含目标的模型可见前文：\n\n")
    f.write('<pre>'+__import__('html').escape(ex['model_visible_prefix'])+'</pre>\n\n右文（仅阅读辅助）：\n\n<pre>'+__import__('html').escape(ex['right_reading_aid'])+'</pre>\n\n')
 log(out,'TEXT_COMPLETE',feature_count=30,example_rows=len(examples),random_slots=150,high_slots=90,unique_contexts=len({v['context_index'] for v in examples}))
 return {'status':'COMPLETE','examples':len(examples),'features':30,'random_slots':150,'high_slots':90,'unique_contexts':len({v['context_index'] for v in examples})}

def main(out):
 out=Path(out);lock=(out/'execution.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);start=time.monotonic();stage={'geometry':'NOT_RUN','texts':'NOT_RUN','figures':'NOT_RUN'}
 assert sha(out/'protocol_frozen.md')==read(out/'execution_record.json')['protocol_sha256']
 allowed=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,allowed[:8])
 try:
  result=geometry(out);stage['geometry']='COMPLETE'
 except Exception:
  put(out/'analysis_state.json',{'state':'FAILED_GEOMETRY','stages':stage,'traceback':traceback.format_exc()});raise
 renderer=subprocess.Popen([sys.executable,str(out/'code/render.py'),str(out)],stdout=(out/'render.log').open('w'),stderr=subprocess.STDOUT)
 try:stage['texts']=texts(out,result)
 except Exception:
  stage['texts']={'status':'FAILED','traceback':traceback.format_exc()};log(out,'TEXT_FAILED',error=stage['texts']['traceback'])
 rc=renderer.wait();stage['figures']='COMPLETE' if rc==0 else 'FAILED';stage['render_exit_code']=rc
 complete=stage['texts'].get('status')=='COMPLETE' and rc==0
 put(out/'analysis_state.json',{'state':'COMPUTATION_COMPLETE_REPORT_PENDING' if complete else 'PARTIAL_COMPUTATION','stages':stage,'formal_active_seconds':time.monotonic()-start,'parent_cpu_seconds':time.process_time(),'parent_max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'no_model_load':True,'no_inference':True,'no_training':True,'no_new_graph_or_cooccurrence':True});log(out,'COMPUTATION_FINISHED',complete=complete,seconds=time.monotonic()-start)
 return 0 if complete else 2

if __name__=='__main__':sys.exit(main(sys.argv[1]))
