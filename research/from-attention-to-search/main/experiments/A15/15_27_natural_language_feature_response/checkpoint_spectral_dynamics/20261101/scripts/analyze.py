"""Frozen Dense training-dynamics statistics and independently refitted readouts."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','4');os.environ.setdefault('OMP_NUM_THREADS','4')
from pathlib import Path
import json,hashlib,time,csv,warnings,datetime,argparse
import numpy as np
from scipy import linalg,stats
from metrics import moments,spectral,subspace,alignment,stream_cka
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis';OUT.mkdir(exist_ok=True)
CFG=json.load(open(ROOT/'config.json'));MAN=json.load(open(ROOT/'manifest.json'))

def js(p,x):
 p=Path(p);p.parent.mkdir(exist_ok=True,parents=True);q=p.with_suffix(p.suffix+'.partial');q.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n');os.replace(q,p)
def csvout(name,rows):
 if not rows:return
 p=OUT/name;fields=list(dict.fromkeys(k for r in rows for k in r));p.parent.mkdir(exist_ok=True,parents=True)
 with open(p,'w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def loadstats(p):return dict(np.load(p,allow_pickle=False))
def savestats(p,s):p.parent.mkdir(exist_ok=True,parents=True);np.savez(p,**s)
def bands():return {**{f'top{k}':np.arange(k) for k in CFG['nested']},**{b:np.arange(*v) for b,v in CFG['bands'].items()}}
def main_index():return {r['tokens']:r for r in json.load(open(ROOT/'cache_index.json'))}
def array(t,l=7,bridge=False):return np.load(Path(main_index()[t]['path'])/f"{'bridge' if bridge else 'geometry'}_layer{l}.npy",mmap_mode='r')
def centered(t,split,l=7):
 a=array(t,l);ix=np.flatnonzero(np.load(ROOT/'data/geometry.npz')['split']==split);s=loadstats(OUT/'stats'/f'{t}_layer{l}.npz')
 return a[ix].reshape(-1,1024).astype(np.float64)-s['mean']

def make_spectra():
 fit=np.load(ROOT/'data/geometry.npz')['split']=='fit';rows=[];spectrum=[]
 for r in MAN['checkpoints']:
  t=r['tokens'];layers=[0,3,7] if t in CFG['semantic_tokens'] else [7]
  for l in layers:
   p=OUT/'stats'/f'{t}_layer{l}.npz'
   if p.exists():s=loadstats(p)
   else:s=moments(array(t,l)[fit]);savestats(p,s)
   row=dict(tokens=t,training_B=t/1e9,layer=l,N=int(s['n']),documents=int(fit.sum()),trace=float(s['eigenvalues'].sum()),effective_rank=float(s['effective_rank']),numeric_rank=int(s['rank']),mean_norm=float(np.linalg.norm(s['mean'])),eigen_residual=float(s['eigen_residual']),orthogonality_error=float(s['orthogonality_error']))
   for frac in CFG['explained_fractions']:row[f'dim_{int(frac*100)}']=int(np.searchsorted(np.cumsum(s['p']),frac)+1)
   for b,ix in bands().items():
    if b.startswith('top'):continue
    row[f'{b}_variance_fraction']=float(s['p'][ix].sum())
   rows.append(row)
   if l==7:
    for i,(w,sv,pv) in enumerate(zip(s['eigenvalues'],s['singular_values'],s['p'])):spectrum.append(dict(tokens=t,training_B=t/1e9,index=i+1,eigenvalue=float(w),singular_value=float(sv),normalized_eigenvalue=float(pv),cumulative_fraction=float(s['p'][:i+1].sum())))
   print('SPECTRUM',t,l,row['trace'],flush=True)
 csvout('checkpoint_statistics.csv',rows);csvout('spectrum.csv',spectrum)
 # Endpoint projected variances: no reordering, distinct from eigenvalues.
 end=loadstats(OUT/'stats'/'33000000000_layer7.npz');projection=[]
 for r in MAN['checkpoints']:
  t=r['tokens'];s=loadstats(OUT/'stats'/f'{t}_layer7.npz');v=end['basis'];w=np.sum(v*(s['cov']@v),axis=0)
  for i,x in enumerate(w):projection.append(dict(tokens=t,training_B=t/1e9,endpoint_direction=i+1,projected_variance=float(x),fraction_of_own_trace=float(x/s['eigenvalues'].sum())))
 csvout('fixed_endpoint_projected_variance.csv',projection)

def pair_metrics(t,u,l=7):
 p=OUT/'pairs'/f'{t}_{u}_layer{l}.json'
 if p.exists():return json.load(open(p))
 a=loadstats(OUT/'stats'/f'{t}_layer{l}.npz');b=loadstats(OUT/'stats'/f'{u}_layer{l}.npz');xf=centered(t,'fit',l);yf=centered(u,'fit',l)
 R=np.eye(1024) if t==u else alignment(xf,yf)
 x=centered(t,'test',l);y=centered(u,'test',l);norm=np.linalg.norm(y)
 row=dict(tokens=t,comparison_tokens=u,layer=l,training_B=t/1e9,comparison_B=u/1e9,token_gap_B=abs(t-u)/1e9,**spectral(a['eigenvalues'],b['eigenvalues']),mean_drift=float(np.linalg.norm(a['mean']-b['mean'])),mean_drift_relative_to_target=float(np.linalg.norm(a['mean']-b['mean'])/np.linalg.norm(b['mean'])),raw_eval_relative_residual=float(np.linalg.norm(x-y)/norm),aligned_eval_relative_residual=float(np.linalg.norm(x@R-y)/norm),raw_fit_relative_residual=float(np.linalg.norm(xf-yf)/np.linalg.norm(yf)),aligned_fit_relative_residual=float(np.linalg.norm(xf@R-yf)/np.linalg.norm(yf)),cka=stream_cka(x,y),R_orthogonality_error=float(np.linalg.norm(R.T@R-np.eye(1024))),R_mean_squared_distance_from_identity=float(np.linalg.norm(R-np.eye(1024))**2/1024))
 sub=[];angles=[]
 for name,ix in bands().items():
  for space,base in [('raw',a['basis']),('aligned',R.T@a['basis'])]:
   dd,aa=subspace(base[:,ix],b['basis'][:,ix]);sub.append(dict(band=name,coordinates=space,**dd))
   angles.extend(dict(band=name,coordinates=space,angle_index=i+1,degrees=float(np.rad2deg(an))) for i,an in enumerate(aa))
 # Isolated-vector diagnostics: no sign-sensitive tracking and no forced IDs.
 vec=[]
 def gap(w,i):
  z=[]
  if i>0:z.append((w[i-1]-w[i])/max(w[i-1],1e-300))
  if i<len(w)-1:z.append((w[i]-w[i+1])/max(w[i],1e-300))
  return min(z)
 for i in range(1024):
  ga=gap(a['eigenvalues'],i);gb=gap(b['eigenvalues'],i);ok=ga>=.05 and gb>=.05 and min(a['eigenvalues'][i],b['eigenvalues'][i])>max(a['eigenvalues'][0],b['eigenvalues'][0])*1e-10
  vec.append(dict(index=i+1,eligible=bool(ok),status='ISOLATED' if ok else 'UNIDENTIFIABLE',source_relative_gap=float(ga),target_relative_gap=float(gb),absolute_cosine=float(abs(a['basis'][:,i]@b['basis'][:,i])) if ok else None))
 savestats(OUT/'alignments'/f'{t}_{u}_layer{l}.npz',dict(R=R))
 out=dict(metrics=row,subspaces=sub,principal_angles=angles,isolated_vectors=vec);js(p,out);print('PAIR',t,u,l,row['cka'],flush=True);return out

def make_pairs():
 ts=[r['tokens'] for r in MAN['checkpoints']];rows=[];subs=[];angs=[];vecs=[]
 for kind,pairs in [('adjacent',list(zip(ts[:-1],ts[1:]))),('endpoint',[(t,ts[-1]) for t in ts])]:
  for t,u in pairs:
   out=pair_metrics(t,u);r=dict(comparison=kind,**out['metrics']);gap=r['token_gap_B']
   for k in ['absolute_spectrum_l2','relative_absolute_spectrum_l2','normalized_spectrum_TV','mean_drift']:r[k+'_per_B']=r[k]/gap if gap else None
   rows.append(r)
   for d in out['subspaces']:subs.append(dict(comparison=kind,tokens=t,comparison_tokens=u,training_B=t/1e9,comparison_B=u/1e9,token_gap_B=gap,**d,projection_distance_per_B=d['projection_distance']/gap if gap else None))
   angs.extend(dict(comparison=kind,tokens=t,comparison_tokens=u,layer=7,**d) for d in out['principal_angles'])
   vecs.extend(dict(comparison=kind,tokens=t,comparison_tokens=u,**d) for d in out['isolated_vectors'])
 for l in CFG['supplement_layers']:
  es=CFG['semantic_tokens']
  for t,u in list(zip(es[:-1],es[1:]))+[(t,es[-1]) for t in es]:
   out=pair_metrics(t,u,l);rows.append(dict(comparison='supplement',**out['metrics']))
   for d in out['subspaces']:subs.append(dict(comparison='supplement',layer=l,tokens=t,comparison_tokens=u,training_B=t/1e9,comparison_B=u/1e9,token_gap_B=abs(t-u)/1e9,**d))
 csvout('pair_metrics.csv',rows);csvout('subspace_distances.csv',subs);csvout('principal_angles.csv',angs);csvout('isolated_vector_diagnostics.csv',vecs)
 # Raw eigengaps and own-basis indices are explicit for band identifiability.
 gaps=[]
 for t in ts:
  s=loadstats(OUT/'stats'/f'{t}_layer7.npz');w=s['eigenvalues']
  for name,ix in bands().items():
   lo,hi=int(ix[0]),int(ix[-1]);gaps.append(dict(tokens=t,band=name,index_start=lo+1,index_stop=hi+1,left_relative_gap=float((w[lo-1]-w[lo])/w[lo-1]) if lo else None,right_relative_gap=float((w[hi]-w[hi+1])/w[hi]) if hi<1023 else None))
 csvout('band_boundary_gaps.csv',gaps)
 return [r for r in rows if r['comparison']=='adjacent']

def uncertainties(adj):
 rates=np.array([r['normalized_spectrum_TV_per_B'] for r in adj]);change=np.abs(np.diff(np.log(np.maximum(rates,1e-300))));turn=int(adj[int(np.argmax(change))+1]['comparison_tokens']);selected=sorted(set(CFG['semantic_tokens']+[turn]));js(OUT/'uncertainty_selection.json',dict(early_mid_late=CFG['semantic_tokens'],key_turn_tokens=turn,rule=CFG['key_turn_rule'],selected=selected,rate_log_changes=change.tolist()))
 doc=np.flatnonzero(np.load(ROOT/'data/geometry.npz')['split']=='fit');split=[];paired=[]
 for rep in range(CFG['reference_split_replicates']):
  rng=np.random.default_rng(CFG['seed']+rep);ix=rng.permutation(doc);halves=[ix[:512],ix[512:]]
  for t in selected:
   st=[]
   for side,ds in enumerate(halves):
    p=OUT/'splitstats'/f'{t}_{rep}_{side}.npz'
    if p.exists():s=loadstats(p)
    else:
     s=moments(array(t)[ds]);s={k:v for k,v in s.items() if k!='cov'};savestats(p,s)
    st.append(s)
   row=dict(tokens=t,training_B=t/1e9,replicate=rep,**spectral(st[0]['eigenvalues'],st[1]['eigenvalues']),mean_drift=float(np.linalg.norm(st[0]['mean']-st[1]['mean'])))
   for name,ixb in bands().items():row[name]=subspace(st[0]['basis'][:,ixb],st[1]['basis'][:,ixb])[0]['projection_distance']
   split.append(row)
  print('SPLIT',rep,selected,flush=True)
 for t in selected:
  for rep in range(CFG['reference_split_replicates']):
   for side in range(2):
    a=loadstats(OUT/'splitstats'/f'{t}_{rep}_{side}.npz');b=loadstats(OUT/'splitstats'/f'33000000000_{rep}_{side}.npz')
    r=dict(tokens=t,replicate=rep,side=side,**spectral(a['eigenvalues'],b['eigenvalues']))
    for name,ix in bands().items():r[name]=subspace(a['basis'][:,ix],b['basis'][:,ix])[0]['projection_distance']
    paired.append(r)
 csvout('within_checkpoint_split_sensitivity.csv',split);csvout('paired_endpoint_split_sensitivity.csv',paired)
 summaries=[]
 for t in selected:
  ss=[r for r in split if r['tokens']==t]
  for key in ['absolute_spectrum_l2','relative_absolute_spectrum_l2','normalized_spectrum_TV','mean_drift']+list(bands()):
   vals=[r[key] for r in ss];q=np.quantile(vals,[.025,.5,.975]);summaries.append(dict(tokens=t,training_B=t/1e9,metric=key,lower=float(q[0]),median=float(q[1]),upper=float(q[2]),interval_type='8fixedpairedhalf-splitdescriptiverange'))
 csvout('sampling_reference_summary.csv',summaries)
 ratios=[]
 for r in adj:
  # Only directly measured sensitivity points are used; no interpolated floor.
  t=r['comparison_tokens'];ref=[s for s in summaries if s['tokens']==t]
  for q in ref:
   metric=q['metric'];observed=r.get(metric)
   if metric in bands():
    d=pair_metrics(r['tokens'],t);observed=next(x['projection_distance'] for x in d['subspaces'] if x['band']==metric and x['coordinates']=='raw')
   if observed is not None:
    ratio=observed/q['median'] if q['median'] else None;ratios.append(dict(tokens=r['tokens'],comparison_tokens=t,metric=metric,observed=observed,sampling_reference=q['median'],ratio=ratio,below_half=bool(ratio<.5) if ratio else None,below_one=bool(ratio<1) if ratio else None,below_two=bool(ratio<2) if ratio else None,interpretation='descriptive_not_onset'))
 csvout('distance_sampling_ratio_sensitivity.csv',ratios)


def readouts():
 from sklearn.pipeline import make_pipeline
 from sklearn.preprocessing import StandardScaler
 from sklearn.linear_model import LogisticRegression
 from sklearn.metrics import balanced_accuracy_score
 from sklearn.exceptions import ConvergenceWarning
 meta=json.load(open(ROOT/'data/bridge_metadata.json'));fitids=json.load(open(ROOT/'data/bridge_fitted_ids.json'));lookup={r['seq_id']:i for i,r in enumerate(meta)}
 end=loadstats(OUT/'stats'/'33000000000_layer7.npz');predrows=[];scores=[];fits=[];contrast=[];taskinfo=[]
 def label(r,task):
  if task=='coarse':return int(r['domain']=='math')
  return int(r['topic']==('algebra' if task=='math_fine' else 'cell'))
 for task in ['coarse','math_fine','bio_fine']:
  train=[lookup[r['seq_id']] for r in fitids if r['task']==task and r['role']=='discovery'];dev=[lookup[r['seq_id']] for r in fitids if r['task']==task and r['role']=='development']
  test=[i for i,r in enumerate(meta) if r['split']=='heldout' and r['eligible'] and (task=='coarse' or (r['fine_eligible'] and r['domain']==('math' if task=='math_fine' else 'biology') and r['topic'] in (['algebra','analysis'] if task=='math_fine' else ['cell','ecology_evolution'])))]
  assert len(train)==16 and len(dev)==8 and set(train).isdisjoint(test) and set(dev).isdisjoint(test)
  assert not {meta[i]['document_family'] for i in train+dev}&{meta[i]['document_family'] for i in test}
  y=np.array([label(r,task) for r in meta]);groups=[np.flatnonzero(y[test]==c) for c in [0,1]]
  taskinfo.append(dict(task=task,TRAIN=len(train),DEV=len(dev),H=len(test),H_class_counts=[len(x) for x in groups],family_overlap=0,exposure='original R12 H already exposed'))
  rng=np.random.default_rng(CFG['seed']);draws=np.array([np.concatenate([rng.choice(g,len(g),replace=True) for g in groups]) for _ in range(CFG['readout_bootstrap'])])
  for t in CFG['semantic_tokens']:
   h=np.array(array(t,bridge=True),np.float64);own=loadstats(OUT/'stats'/f'{t}_layer7.npz')
   for basis,base in [('own',own),('fixed33B',end)]:
    z=(h-base['mean'])@base['basis'];prediction={};boots={}
    for name,ix in CFG['readout_sets'].items():
     best=None
     for C in CFG['C_grid']:
      model=make_pipeline(StandardScaler(),LogisticRegression(C=C,class_weight='balanced',solver='lbfgs',max_iter=3000,tol=1e-8,random_state=CFG['seed']))
      with warnings.catch_warnings(record=True) as ww:
       warnings.simplefilter('always',ConvergenceWarning);model.fit(z[np.ix_(train,ix)],y[train])
      conv=not any(isinstance(w.message,ConvergenceWarning) for w in ww);assert conv,('READOUT_NOT_CONVERGED',task,t,basis,name,C)
      val=float(balanced_accuracy_score(y[dev],model.predict(z[np.ix_(dev,ix)])));fits.append(dict(task=task,tokens=t,basis=basis,subspace=name,C=C,train_n=len(train),dev_n=len(dev),trainable_parameters=len(ix)+1,dev_balanced_accuracy=val,converged=conv,standardization='TRAIN_ONLY',objective='class-balancedL2logistic'))
      if best is None or val>best[0]:best=val,C,model
     _,C,model=best;yp=model.predict(z[np.ix_(test,ix)]);acc=float(balanced_accuracy_score(y[test],yp));prediction[name]=yp
     correct=(yp==y[test]).astype(float);bootstrap=np.mean([correct[draws[:,np.isin(draws[0],g)]] for g in []],axis=0) if False else .5*(correct[draws[:,:len(groups[0])]].mean(1)+correct[draws[:,len(groups[0]):]].mean(1))
     boots[name]=bootstrap;q=np.quantile(bootstrap,[.025,.975]);scores.append(dict(task=task,tokens=t,training_B=t/1e9,basis=basis,subspace=name,dimension=len(ix),selected_C=C,train_n=len(train),dev_n=len(dev),H_n=len(test),balanced_accuracy=acc,lower=float(q[0]),upper=float(q[1]),interval='pairedstratifieddocumentbootstrap2000'))
     for j,i in enumerate(test):predrows.append(dict(task=task,tokens=t,basis=basis,subspace=name,seq_id=meta[i]['seq_id'],document_family=meta[i]['document_family'],true_label=int(y[i]),prediction=int(yp[j]),correct=int(yp[j]==y[i])))
    for plus in ['head_middle','head_tail']:
     for base in ['head128','head']:
      d=boots[plus]-boots[base];a=next(s['balanced_accuracy'] for s in scores if s['task']==task and s['tokens']==t and s['basis']==basis and s['subspace']==plus);b=next(s['balanced_accuracy'] for s in scores if s['task']==task and s['tokens']==t and s['basis']==basis and s['subspace']==base);q=np.quantile(d,[.025,.975]);p=float(min(1,2*(min(np.sum(d<=0),np.sum(d>=0))+1)/(len(d)+1)))
      contrast.append(dict(task=task,tokens=t,training_B=t/1e9,basis=basis,addition=plus,control=base,difference=a-b,lower=float(q[0]),upper=float(q[1]),two_sided_bootstrap_p=p,primary=base=='head128'))
   print('READOUT',task,t,flush=True)
 primary=[r for r in contrast if r['primary']];assert len(primary)==36
 order=sorted(range(len(primary)),key=lambda j:primary[j]['two_sided_bootstrap_p']);last=0
 for rank,j in enumerate(order):last=max(last,min(1,(len(order)-rank)*primary[j]['two_sided_bootstrap_p']));primary[j]['holm36_p']=last;primary[j]['positive_increment_established']=bool(last<.05 and primary[j]['lower']>0)
 csvout('readout_metrics.csv',scores);csvout('fit_ledger.csv',fits);csvout('readout_predictions.csv',predrows);csvout('increment_contrasts.csv',contrast);js(OUT/'semantic_task_counts.json',taskinfo)

def coverage():
 ts=[r['tokens'] for r in MAN['checkpoints']];rows=[]
 for task,n,artifact in [('checkpoint_inventory',len(ts),'../manifest.json'),('paired_geometry',len(ts),'checkpoint_statistics.csv'),('own_covariance_spectrum',len(ts),'spectrum.csv'),('original_and_aligned_subspaces',2*(len(ts)-1)+1,'subspace_distances.csv'),('fixed_endpoint_projection',len(ts),'fixed_endpoint_projected_variance.csv'),('CKA_Procrustes',2*(len(ts)-1)+1,'pair_metrics.csv'),('mean_scale_shape_rates',len(ts)-1,'pair_metrics.csv'),('sampling_sensitivity',len(json.load(open(OUT/'uncertainty_selection.json'))['selected']),'sampling_reference_summary.csv'),('supplement_layers',6,'checkpoint_statistics.csv'),('semantic_readouts',126,'readout_metrics.csv'),('matched_dimension_increments',36,'increment_contrasts.csv')]:rows.append(dict(task=task,status='DONE_EXPLORATORY',count=n,evidence=artifact,boundary='one trajectory;record independence approximation;historical exposure'))
 rows.extend([dict(task='missing_checkpoint_payloads',status='BLOCKED',count=sum(x['reason'].startswith('PAYLOAD') for x in MAN['excluded']),evidence='../manifest.json',boundary='source manifests remain;not interpolated'),dict(task='Dense_dictionary_analysis',status='NOT_APPLICABLE',count=0,evidence='../protocol.md',boundary='not requested;no QwenCrossCoder use'),dict(task='stability_onset',status='NOT_ESTIMATED_BY_DESIGN',count=0,evidence='../protocol.md',boundary='no scientifically justified universal tolerance'),dict(task='scientific_acceptance',status='UNKNOWN',count=0,evidence='../anchor.md',boundary='researcher owns judgment')]);csvout('coverage_ledger.csv',rows)

if __name__=='__main__':
 start=time.time()
 try:
  make_spectra();adj=make_pairs();uncertainties(adj);js(OUT/'geometry_complete.json',dict(status='COMPLETE',seconds=time.time()-start))
  from plot import geometry_figures,semantic_figure
  geometry_figures();readouts();semantic_figure();coverage();js(OUT/'completion.json',dict(status='COMPLETED_BOUNDED_DESCRIPTIVE_ANALYSIS',checkpoints=len(MAN['checkpoints']),seconds=time.time()-start,language_model_updates=0,scientific_acceptance='Unknown',ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 except BaseException as e:js(OUT/'failure.json',dict(error=repr(e),time=datetime.datetime.now(datetime.timezone.utc).isoformat()));raise
