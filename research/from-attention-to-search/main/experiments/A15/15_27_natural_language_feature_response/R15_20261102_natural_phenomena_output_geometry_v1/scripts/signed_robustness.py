from pathlib import Path
import sys,json
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];sys.path.insert(0,str(E/'scripts'));import analyze as A
P=dict(np.load(E/'analysis/pca.npz'));cases=[('first_person',1),('quantity',2),('recent_paragraph',0),('recent_paragraph',2)];rows=[];seen={d['host'] for d in A.DOC if d['split']!='validation'}
for flag,pc in cases:
 others=['quantity','recent_paragraph'] if flag=='first_person' else ['recent_paragraph'] if flag=='quantity' else ['quantity'];out=[]
 for d in [d for d in A.DOC if d['split']=='validation']:
  h=np.load(E/'cache'/(d['doc_id']+'.npz'))['h'].astype(float)-P['h_mean'];v=h@P['h_V'][:,pc];resp={'signed_trainSD':v/np.sqrt(P['h_eigenvalues'][pc]),'signed_cosine':v/np.maximum(np.linalg.norm(h,axis=1),1e-20)};lab=A.LABEL.iloc[d['row_start']:d['row_start']+128];loose=A.pairs(d,lab[flag].to_numpy(bool));strict=A.pairs(d,lab[flag].to_numpy(bool),True);conditioned=np.array([(p,n) for p,n in strict if all(lab.iloc[p][c]==lab.iloc[n][c] for c in others)],dtype=int).reshape(-1,2)
  for mode,pp in [('same_token',loose),('same_token_same_quartile',strict),('quartile_and_other_properties_equal',conditioned),('new_hosts_same_token',loose if d['host'] not in seen else np.zeros((0,2),int))]:
   if not len(pp):continue
   for metric,r in resp.items():out.append({'phenomenon':flag,'PC_index0':pc,'mode':mode,'metric':metric,'doc_id':d['doc_id'],'host':d['host'],'effect':float(np.mean(r[pp[:,0]]-r[pp[:,1]])),'pairs':len(pp),'mean_position_gap':float(np.mean(abs(np.array(d['positions'])[pp[:,0]]-np.array(d['positions'])[pp[:,1]])))})
 D=pd.DataFrame(out);rows+=out
summary=[];D=pd.DataFrame(rows);D.to_csv(E/'analysis/signed_sensitivity_document_effects.csv',index=False)
for (flag,pc,mode,metric),q in D.groupby(['phenomenon','PC_index0','mode','metric']):
 v=q.effect.to_numpy();boot=v[np.random.default_rng(110204).integers(0,len(v),(2000,len(v)))].mean(1);lo,hi=np.quantile(boot,[.025,.975]);summary.append({'phenomenon':flag,'PC_index0':pc,'mode':mode,'metric':metric,'effect':v.mean(),'low95':lo,'high95':hi,'documents':len(v),'hosts':q.host.nunique(),'pairs':q.pairs.sum(),'mean_position_gap':q.mean_position_gap.mean(),'status':'POST_A6_EXPLORATORY_SENSITIVITY_NOT_CONFIRMATION'})
pd.DataFrame(summary).to_csv(E/'analysis/signed_direction_sensitivity.csv',index=False);print('SIGNED_SENSITIVITY',len(summary),flush=True)
# Discovery-document stability of all prelisted root directions; no validation basis fitting.
means=[];moments=[];docs=[d for d in A.DOC if d['split']=='discovery']
for d in docs:
 X=np.load(E/'cache'/(d['doc_id']+'.npz'))['h'].astype(float)-P['h_mean'];means.append(X.mean(0));moments.append(X.T@X/len(X))
means=np.array(means);moments=np.array(moments);rng=np.random.default_rng(110207);result=[]
for i in range(30):
 ix=rng.integers(0,len(docs),len(docs));weights=np.bincount(ix,minlength=len(docs))/len(docs);mu=weights@means;C=np.tensordot(weights,moments,axes=(0,0))-np.outer(mu,mu);ev,U=np.linalg.eigh(C);U=U[:,::-1]
 for pc in A.cfg['PC_candidates']:result.append({'bootstrap':i,'PC_index0':pc,'squared_direction_overlap':float((U[:,pc]@P['h_V'][:,pc])**2),'unit':'discoverydocument','signarbitrary':True})
 if i%10==0:print('ROOT_STABILITY',i,flush=True)
pd.DataFrame(result).to_csv(E/'analysis/h_direction_document_bootstrap_stability.csv',index=False)
