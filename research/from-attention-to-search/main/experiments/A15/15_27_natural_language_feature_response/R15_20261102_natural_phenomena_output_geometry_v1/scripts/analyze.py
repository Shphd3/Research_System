from pathlib import Path
import json,hashlib,collections,sys,time
import numpy as np,pandas as pd
from scipy.stats import norm
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));DOC=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];LABEL=pd.read_json(E/'data/labels_effective_v1p2.jsonl',lines=True);FLAGS=[x for x in LABEL.columns if x!='row'];BANDS=cfg['bands'];SEEDS=cfg['random_seeds'];NAMES=json.load(open(E/'data/phenomenon_definitions_v1p2.json'))['name']
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(split):
 ds=[x for x in DOC if x['split'] in split];A={k:[] for k in ['h','y','z_selected','reconstruction']};rows=[]
 for doc in ds:
  q=np.load(E/'cache'/(doc['doc_id']+'.npz'))
  for k in A:A[k].append(q[k])
  rows.extend(range(doc['row_start'],doc['row_start']+len(doc['positions'])))
 return ds,{k:np.concatenate(v) for k,v in A.items()},np.array(rows)
def fit():
 if (E/'analysis/pca.npz').exists():return
 ds,A,rows=load(['discovery']);out={};meta={}
 for name in ['h','y']:
  X=A[name].astype(np.float64);mu=X.mean(0);C=(X-mu).T@(X-mu)/len(X);ev,V=np.linalg.eigh(C);ix=np.argsort(ev)[::-1];ev=ev[ix];V=V[:,ix]
  # Fix reproducible display signs only; positive/negative are not semantic directions.
  signs=np.sign(V[np.argmax(abs(V),axis=0),np.arange(1024)]);V*=signs
  out[name+'_mean']=mu;out[name+'_V']=V;out[name+'_eigenvalues']=ev
  p=ev/ev.sum();meta[name]={'positions':len(X),'documents':len(ds),'centered':True,'numerical_rank':int((ev>ev[0]*1e-10).sum()),'entropy_effective_rank':float(np.exp(-(p[p>0]*np.log(p[p>0])).sum())),'min_eigenvalue':float(ev[-1]),'relative_eigengaps':((ev[:-1]-ev[1:])/ev[:-1]).tolist(),'eigen_residual':float(np.linalg.norm(C@V-V*ev)/np.linalg.norm(C))}
 for seed in SEEDS:
  Q,_=np.linalg.qr(np.random.default_rng(seed).normal(size=(1024,1024)));out['random_'+str(seed)]=Q
 out['z_SD']=np.maximum(A['z_selected'].std(0,dtype=np.float64),1e-8);np.savez(E/'analysis/pca.npz',**out);dump(E/'audit/pca_fit.json',meta);print('PCA_FIT',meta['h']['entropy_effective_rank'],meta['y']['entropy_effective_rank'],flush=True)
def card_candidates(ds,A,rows):
 if (E/'analysis/discovery_cards.jsonl').exists():return
 P=dict(np.load(E/'analysis/pca.npz'));pc=(A['h']-P['h_mean'])@P['h_V'];energy=np.stack([np.sum(pc[:,a:b]**2,1) for a,b in BANDS],1);fraction=energy/np.maximum(energy.sum(1,keepdims=True),1e-20)
 with (E/'analysis/discovery_cards.jsonl').open('w') as sink:
  objects=[('PC_'+str(i),pc[:,i]) for i in cfg['PC_candidates']]+[('band_'+str(i),fraction[:,i]) for i in range(8)]+[('feature_'+str(f),A['z_selected'][:,j]) for j,f in enumerate(cfg['candidate_features'])]
  for name,v in objects:
   # First take one representative per document at each rank level, not repeated top tokens.
   order=np.argsort(v,kind='stable');mid=np.argsort(abs(v-np.median(v)),kind='stable');chosen=[]
   for level,seq in [('high',order[::-1]),('middle',mid),('low',order),('random',np.random.default_rng(int(hashlib.sha256(name.encode()).hexdigest()[:8],16)).permutation(len(v)))]:
    seen=set();c=0
    for ix in seq:
     doc=ds[int(ix)//128]
     if doc['doc_id'] in seen:continue
     if name.startswith('feature_') and level=='high' and v[ix]<=0:break
     seen.add(doc['doc_id']);chosen.append({'object':name,'level':level,'row':int(rows[ix]),'doc_id':doc['doc_id'],'host':doc['host'],'response':float(v[ix]),'split':'discovery'});c+=1
     if c==3:break
    if c==0:chosen.append({'object':name,'level':level,'status':'NOT_FOUND_NONZERO_SUPPORT'})
   for x in chosen:sink.write(json.dumps(x,ensure_ascii=False)+'\n')
 np.savez_compressed(E/'analysis/discovery_arrays.npz',rows=rows,pc_candidates=pc[:,cfg['PC_candidates']],band_energy=energy,band_fraction=fraction,z=A['z_selected'])
def pairs(doc,lab,quartile=False):
 ids=np.array(doc['token_ids'])[doc['positions']];p=np.array(doc['positions']);positive=np.flatnonzero(lab);negative=np.flatnonzero(~lab);used=set();out=[]
 for i in positive:
  candidates=[j for j in negative if j not in used and ids[j]==ids[i] and (not quartile or int(4*p[j]/len(doc['token_ids']))==int(4*p[i]/len(doc['token_ids'])))]
  if not candidates:continue
  j=min(candidates,key=lambda j:(abs(int(p[i])-int(p[j])),int(j)));used.add(j);out.append((int(i),int(j)))
 return np.array(out,dtype=int).reshape(-1,2)
def summaries(split):
 P=dict(np.load(E/'analysis/pca.npz'));G=dict(np.load(E/'analysis/head_geometry.npz'));ds,A,rows=load([split]);H=(A['h'].astype(np.float64)-P['h_mean']);Y=(A['y'].astype(np.float64)-P['y_mean']);ph=H@P['h_V'];py=Y@P['y_V'];en=np.stack([np.sum(ph[:,a:b]**2,1) for a,b in BANDS],1);fr=en/np.maximum(np.sum(H**2,1)[:,None],1e-20);records=[];pairrecords=[];diagnostics=[];geometry=[];raw=[]
 # Actual head eigenspace coordinates used only on real matched deltas.
 for di,doc in enumerate(ds):
  if di%50==0:print('DOCUMENT_EFFECTS',split,di,len(ds),flush=True)
  lo=di*128;loc=np.arange(lo,lo+128);labels=LABEL.iloc[rows[loc]][FLAGS].to_numpy(bool);z=A['z_selected'][loc]
  for fi,flag in enumerate(FLAGS):
   lab=labels[:,fi];pa=pairs(doc,lab);pq=pairs(doc,lab,True);raw.append({'split':split,'doc_id':doc['doc_id'],'source_family':doc['host'],'domain':doc['domain'],'phenomenon':flag,'positive_positions':int(lab.sum()),'negative_positions':int((~lab).sum()),'matched_pairs':len(pa),'quartile_matched_pairs':len(pq)})
   for mode,pp in [('same_token',pa),('same_token_same_quartile',pq)]:
    if not len(pp):continue
    plus=loc[pp[:,0]];minus=loc[pp[:,1]];fd=(A['z_selected'][plus]-A['z_selected'][minus]).mean(0)/P['z_SD'];bd=(fr[plus]-fr[minus]).mean(0)
    for j,v in enumerate(fd):records.append({'split':split,'doc_id':doc['doc_id'],'host':doc['host'],'domain':doc['domain'],'phenomenon':flag,'response':'feature_'+str(cfg['candidate_features'][j]),'value':float(v),'pairs':len(pp),'matching':mode})
    for j,v in enumerate(bd):records.append({'split':split,'doc_id':doc['doc_id'],'host':doc['host'],'domain':doc['domain'],'phenomenon':flag,'response':'band_'+str(j),'value':float(v),'pairs':len(pp),'matching':mode})
    if mode!='same_token':continue
    for pos,neg in zip(plus,minus):pairrecords.append({'split':split,'phenomenon':flag,'doc_id':doc['doc_id'],'host':doc['host'],'positive_row':int(rows[pos]),'negative_row':int(rows[neg]),'position_gap':abs(doc['positions'][pos-lo]-doc['positions'][neg-lo])})
    dh=A['h'][plus].astype(np.float64)-A['h'][minus];dy=A['y'][plus].astype(np.float64)-A['y'][minus];coord=dy@G['U'];out_squared=np.sum(coord**2*G['eigenvalues'],1);ynorm=np.linalg.norm(dy,axis=1)
    # The vocabulary divisor, not hidden dimension; use exact measured vocab shape.
    outRMS=np.sqrt(np.maximum(out_squared,0)/151936);gains=outRMS/np.maximum(ynorm,1e-12)
    dhpc=dh@P['h_V'];dy_pc=dy@P['y_V'];eh=np.stack([np.sum(dhpc[:,a:b]**2,1) for a,b in BANDS],1);ey=np.stack([np.sum(dy_pc[:,a:b]**2,1) for a,b in BANDS],1)
    for b,(a,end) in enumerate(BANDS):
     rv=[]
     for seed in SEEDS:rq=dh@P['random_'+str(seed)][:,:end-a];rv.append(np.sum(rq**2,1))
     geometry.append({'split':split,'doc_id':doc['doc_id'],'host':doc['host'],'domain':doc['domain'],'phenomenon':flag,'band':b,'dimensions':end-a,'pairs':len(pp),'delta_h_energy':float(eh[:,b].mean()),'delta_h_energy_per_dim':float(eh[:,b].mean()/(end-a)),'delta_h_fraction':float(np.mean(eh[:,b]/np.maximum(np.sum(dh**2,1),1e-20))),'delta_y_fraction':float(np.mean(ey[:,b]/np.maximum(np.sum(dy**2,1),1e-20))),'random_same_rank_energy':float(np.mean(rv)),'norm_delta_h':float(np.linalg.norm(dh,axis=1).mean()),'norm_delta_y':float(ynorm.mean()),'centered_logit_RMS':float(outRMS.mean()),'output_gain':float(gains.mean())})
 pd.DataFrame(records).to_csv(E/'analysis'/f'{split}_document_effects.csv',index=False);pd.DataFrame(raw).to_csv(E/'analysis'/f'{split}_phenomenon_support.csv',index=False);pd.DataFrame(pairrecords).to_csv(E/'analysis'/f'{split}_matched_positions.csv',index=False);pd.DataFrame(geometry).to_csv(E/'analysis'/f'{split}_actual_changes.csv',index=False)
 # Summaries are document-weighted, not number-of-matched-pairs weighted.
 R=pd.DataFrame(records);out=[]
 for (flag,response,mode),q in R.groupby(['phenomenon','response','matching'],sort=True):
  v=q.value.to_numpy();rng=np.random.default_rng(110204);draws=rng.integers(0,len(v),size=(2000,len(v)));boot=v[draws].mean(1);low,high=np.quantile(boot,[.025,.975]);m=v.mean();pv=min(1.,2*min((np.sum(boot<=0)+1)/2001,(np.sum(boot>=0)+1)/2001));hostcounts=q.groupby('host').doc_id.nunique();out.append({'split':split,'phenomenon':flag,'response':response,'matching':mode,'effect':m,'low95':low,'high95':high,'bootstrap_p':pv,'documents':len(v),'hosts':q.host.nunique(),'hosts_with_3documents':int((hostcounts>=3).sum()),'max_host_document_fraction':float(hostcounts.max()/len(v)),'pairs':q.pairs.sum(),'positive_documents':int((v>0).sum()),'negative_documents':int((v<0).sum())})
 pd.DataFrame(out).to_csv(E/'analysis'/f'{split}_associations.csv',index=False);print('SUMMARIZED',split,len(ds),len(out),flush=True)
def freeze_selection():
 A=pd.read_csv(E/'analysis/discovery_associations.csv');B=pd.read_csv(E/'analysis/development_associations.csv');cand=A[(A.matching=='same_token')&A.response.str.startswith('feature_')].merge(B[B.matching=='same_token'],on=['phenomenon','response','matching'],suffixes=('_discovery','_development'))
 cand['eligible']=(cand.documents_discovery>=12)&(cand.documents_development>=12)&(cand.hosts_development>=2)&(cand.effect_discovery*cand.effect_development>0)
 cand.to_csv(E/'analysis/development_selection_candidates.csv',index=False);eligible=cand[cand.eligible].copy();eligible['rank']=abs(eligible.effect_discovery);eligible=eligible.sort_values(['rank','phenomenon','response'],ascending=[False,True,True]);chosen=[];phen=set()
 for _,r in eligible.iterrows():
  if r.phenomenon in phen:continue
  phen.add(r.phenomenon);selected={k:(v.item() if hasattr(v,'item') else v) for k,v in r.items()};selected['human_label']=NAMES[r.phenomenon];chosen.append(selected)
  if len(chosen)==4:break
 interventions=[]
 for r in chosen:
  if r['low95_development']>0 or r['high95_development']<0:interventions.append({'phenomenon':r['phenomenon'],'feature':int(r['response'].split('_')[1]),'signed_effect':r['effect_discovery'],'band':int(pd.read_csv(E/'analysis/development_associations.csv').query("phenomenon==@r['phenomenon']")['effect'].abs().idxmax()) if False else None})
  if len(interventions)==2:break
 # Band selection uses discovery effect only; not head-gain or validation.
 for r in interventions:
  q=A[(A.phenomenon==r['phenomenon'])&(A.matching=='same_token')&A.response.str.startswith('band_')];r['band']=int(q.iloc[abs(q.effect).argmax()].response.split('_')[1])
 manifest={'created_at_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'selected_explanations':chosen,'conditional_interventions':interventions,'validation_responses_opened':False,'selection_rule':'max4unique prefix properties;discovery absolute effect rank;development support/same sign;two strongest with development95excluding0eligible intervention;all memberIDs fixed before validation','effective_label_table_sha256':sha(E/'data/labels_effective_v1p2.jsonl'),'effective_definition_sha256':sha(E/'data/phenomenon_definitions_v1p2.json'),'analysis_code_sha256':sha(Path(__file__)),'input_freeze_sha256':sha(E/'freeze.json'),'discovery_sha256':sha(E/'analysis/discovery_associations.csv'),'development_sha256':sha(E/'analysis/development_associations.csv'),'selected_intervention_positions':'input-label/hash-selected before reading validation metrics','all_flag_band_tests':str(len(FLAGS))+'x8andquartile sensitivity retained,not only selected explanations'};dump(E/'validation_selection_frozen.json',manifest);print('SELECTION_FROZEN',[(x['phenomenon'],x['response']) for x in chosen],interventions,flush=True)
def validation_verdict():
 F=json.load(open(E/'validation_selection_frozen.json'));A=pd.read_csv(E/'analysis/validation_associations.csv');rows=[]
 for c in F['selected_explanations']:
  q=A[(A.phenomenon==c['phenomenon'])&(A.response==c['response'])&(A.matching=='same_token')]
  if not len(q):rows.append({'phenomenon':c['phenomenon'],'feature':c['response'],'status':'INSUFFICIENT_NO_MATCHES'});continue
  r=q.iloc[0].to_dict();r['feature']=r.pop('response');r['same_sign']=bool(r['effect']*c['effect_discovery']>0);rows.append(r)
 # Holm across exact frozen selected candidates, not post-hoc winning tests.
 ix=sorted(range(len(rows)),key=lambda i:rows[i].get('bootstrap_p',1));last=0.
 for rank,i in enumerate(ix):
  r=rows[i];adj=max(last,min(1.,r.get('bootstrap_p',1)*(len(ix)-rank)));last=adj;r['holm_p']=adj
  r['status']='REPRODUCED_LEXICAL_OR_FORMAT_ASSOCIATION' if r.get('documents',0)>=12 and r.get('hosts',0)>=2 and r.get('max_host_document_fraction',1)<=.5 and r.get('same_sign',False) and adj<.05 else 'INSUFFICIENT_SUPPORT' if r.get('documents',0)<12 or r.get('hosts',0)<2 or r.get('max_host_document_fraction',1)>.5 else 'NOT_SUPPORTED_AFTER_MULTIPLICITY'
 pd.DataFrame(rows,columns=None if rows else ['phenomenon','feature','status']).to_csv(E/'analysis/validation_selected_verdicts.csv',index=False)
 band=A[(A.matching=='same_token')&A.response.str.startswith('band_')].copy();order=band.bootstrap_p.sort_values().index;last=0
 for rank,i in enumerate(order):last=max(last,min(1.,band.at[i,'bootstrap_p']*(len(order)-rank)));band.at[i,'holm_p_all_bands']=last
 R=pd.read_csv(E/'analysis/validation_document_effects.csv');R=R[(R.matching=='same_token')&R.response.str.startswith('band_')];R['key']=R.phenomenon+'::'+R.response;M=R.pivot(index='doc_id',columns='key',values='value');mat=M.to_numpy();rng=np.random.default_rng(110204);draw=rng.integers(0,len(mat),(2000,len(mat)));boot=np.nanmean(mat[draw],axis=1);mean=np.nanmean(mat,axis=0);se=np.nanstd(boot,axis=0);den=np.maximum(se,1e-12);maxt=np.nanmax(abs((boot-mean)/den),axis=1);critical=np.quantile(maxt,.95)
 lookup={k:i for i,k in enumerate(M.columns)};disc=pd.read_csv(E/'analysis/discovery_associations.csv');dev=pd.read_csv(E/'analysis/development_associations.csv')
 for ix,r in band.iterrows():
  k=lookup[r.phenomenon+'::'+r.response];band.at[ix,'low_simultaneous']=mean[k]-critical*se[k];band.at[ix,'high_simultaneous']=mean[k]+critical*se[k];band.at[ix,'familywise_p']=(np.sum(maxt>=abs(mean[k])/den[k])+1)/2001
  a=disc[(disc.phenomenon==r.phenomenon)&(disc.response==r.response)&(disc.matching=='same_token')];b=dev[(dev.phenomenon==r.phenomenon)&(dev.response==r.response)&(dev.matching=='same_token')];same=len(a)>0 and len(b)>0 and a.iloc[0].effect*b.iloc[0].effect>0 and r.effect*a.iloc[0].effect>0
  band.at[ix,'three_split_same_sign']=bool(same);band.at[ix,'reproduced_band_association']=bool(same and r.documents>=12 and r.hosts>=2 and r.max_host_document_fraction<=.5 and band.at[ix,'familywise_p']<.05)
 dump(E/'audit/band_familywise_bootstrap.json',{'tests':len(M.columns),'draws':2000,'resampling':'common validation-document draws across all band tests;matched-document missingness retained','critical_max_studentized_deviation':float(critical),'method':'simultaneous centered bootstrap max statistic,not p-value-grid limitedHolm','pointwise_Holm_kept_only_as_coarse_audit':True})
 band.to_csv(E/'analysis/validation_band_map.csv',index=False);print('VALIDATION',[(r['phenomenon'],r['status']) for r in rows],flush=True)
if __name__=='__main__':
 stage=sys.argv[1] if len(sys.argv)>1 else 'discovery'
 if stage=='discovery':
  fit();d,a,r=load(['discovery']);card_candidates(d,a,r);del a
  summaries('discovery');summaries('development');print('DISCOVERY_DEVELOPMENT_READY_FOR_CONTEXT_REVIEW',flush=True)
 elif stage=='freeze':freeze_selection()
 elif stage=='validation':
  assert (E/'validation_selection_frozen.json').exists();summaries('validation');validation_verdict()
