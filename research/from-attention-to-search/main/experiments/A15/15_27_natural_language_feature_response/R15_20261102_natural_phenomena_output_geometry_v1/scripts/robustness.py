from pathlib import Path
import json,sys,time
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));F=json.load(open(E/'validation_selection_frozen.json'));A=pd.read_csv(E/'analysis/validation_document_effects.csv');rows=[]
all_docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];seen_hosts={d['host'] for d in all_docs if d['split']!='validation'}
for c in F['selected_explanations']:
 q=A[(A.phenomenon==c['phenomenon'])&(A.response==c['response'])&(A.matching=='same_token')]
 if not len(q):continue
 dominant=q.host.value_counts().index[0]
 for view,vv in [('all_documents',q),('exclude_dominant_host',q[q.host!=dominant]),('hosts_unseen_in_discovery_development',q[~q.host.isin(seen_hosts)]),('same_token_same_quartile',A[(A.phenomenon==c['phenomenon'])&(A.response==c['response'])&(A.matching=='same_token_same_quartile')])]:
  if not len(vv):continue
  v=vv.value.to_numpy();boot=v[np.random.default_rng(110204).integers(0,len(v),(2000,len(v)))].mean(1);lo,hi=np.quantile(boot,[.025,.975]);rows.append({'phenomenon':c['phenomenon'],'feature':c['response'],'view':view,'excluded_host':dominant if view!='all_documents' else '', 'documents':len(v),'hosts':vv.host.nunique(),'effect':v.mean(),'low95':lo,'high95':hi})
 for host,qq in q.groupby('host'):rows.append({'phenomenon':c['phenomenon'],'feature':c['response'],'view':'individual_host','host':host,'documents':len(qq),'effect':qq.value.mean(),'low95':None,'high95':None})
pd.DataFrame(rows).to_csv(E/'analysis/validation_source_robustness.csv',index=False)
# Stability of fixed subspaces,notsemantic identities of single near-degenerate roots.
P=dict(np.load(E/'analysis/pca.npz'));docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines() if json.loads(l)['split']=='discovery'];bands=cfg['bands'];st=[];meta=[]
for space in ['h','y']:
 t=time.time();means=[];seconds=[]
 for doc in docs:
  X=np.load(E/'cache'/(doc['doc_id']+'.npz'))[space].astype(np.float64)-P[space+'_mean'];means.append(X.mean(0));seconds.append(X.T@X/len(X))
 means=np.array(means);seconds=np.array(seconds);rng=np.random.default_rng(110207)
 for iteration in range(30):
  ix=rng.integers(0,len(docs),len(docs));weights=np.bincount(ix,minlength=len(docs))/len(docs);mu=weights@means;C=np.tensordot(weights,seconds,axes=(0,0))-np.outer(mu,mu);ev,U=np.linalg.eigh(C);U=U[:,::-1]
  for b,(a,end) in enumerate(bands):st.append({'coordinates':space,'bootstrap':iteration,'band':b,'dimensions':end-a,'subspace_overlap_per_dimension':float(np.sum((P[space+'_V'][:,a:end].T@U[:,a:end])**2)/(end-a))})
  if iteration%10==0:print('STABILITY',space,iteration,time.time()-t,flush=True)
 del seconds;meta.append({'space':space,'seconds':time.time()-t,'draws':30,'unit':'discovery_document','moment_precision':'FP64','eigen_precision':'FP64','not_independent_basis_replication':True})
pd.DataFrame(st).to_csv(E/'analysis/pca_document_bootstrap_stability.csv',index=False);json.dump(meta,open(E/'audit/pca_stability.json','w'),indent=2);print('ROBUSTNESS_COMPLETE',flush=True)
