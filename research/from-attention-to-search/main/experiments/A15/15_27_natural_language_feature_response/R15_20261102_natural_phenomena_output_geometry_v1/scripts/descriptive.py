from pathlib import Path
import json
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));P=dict(np.load(E/'analysis/pca.npz'));docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines() if json.loads(l)['split']=='validation'];pos=pd.read_json(E/'data/positions.jsonl',lines=True);out=[]
for d in docs:
 q=np.load(E/'cache'/(d['doc_id']+'.npz'));X=q['h'].astype(float)-P['h_mean'];pc=X@P['h_V'];energy=np.stack([np.sum(pc[:,a:b]**2,1) for a,b in cfg['bands']],1);fr=energy/np.sum(X**2,1)[:,None];types=pos.iloc[d['row_start']:d['row_start']+128].token_category.to_numpy();positions=np.array(d['positions']);quartile=4*positions//len(d['token_ids'])
 for cat in ['number','punctuation','format']:
  plus=np.flatnonzero(types==cat);minus=np.flatnonzero(types!=cat);used=set();pairs=[]
  for i in plus:
   can=[j for j in minus if j not in used and quartile[j]==quartile[i]]
   if not can:continue
   j=min(can,key=lambda j:(abs(int(positions[i])-int(positions[j])),j));used.add(j);pairs.append((i,j))
  if not pairs:continue
  pp=np.array(pairs);renergy=[]
  for a,b in cfg['bands']:
   rv=[]
   for seed in cfg['random_seeds']:rv.append(np.sum((X[pp[:,0]]@P['random_'+str(seed)][:,:b-a])**2,1))
   renergy.append(float(np.mean(rv)))
  for bi,(a,b) in enumerate(cfg['bands']):out.append({'category':cat,'doc_id':d['doc_id'],'host':d['host'],'band':bi,'dimensions':b-a,'pairs':len(pp),'positive_positions':len(plus),'same_quartile_different_current_token':True,'band_fraction_difference':float((fr[pp[:,0],bi]-fr[pp[:,1],bi]).mean()),'positive_raw_band_energy':float(energy[pp[:,0],bi].mean()),'positive_energy_per_dim':float(energy[pp[:,0],bi].mean()/(b-a)),'random_same_rank_positive_energy':renergy[bi],'inference':'DESCRIPTIVE_WORD_FORM_PROPERTY;cannot control token identity by definition'})
D=pd.DataFrame(out);D.to_csv(E/'analysis/descriptive_token_category_document_effects.csv',index=False);summary=[]
for (cat,b),q in D.groupby(['category','band']):
 v=q.band_fraction_difference.to_numpy();boot=v[np.random.default_rng(110204).integers(0,len(v),(2000,len(v)))].mean(1);lo,hi=np.quantile(boot,[.025,.975]);summary.append({'category':cat,'band':b,'difference':v.mean(),'low95':lo,'high95':hi,'documents':len(v),'hosts':q.host.nunique(),'pairs':q.pairs.sum(),'not_token_identity_controlled':True,'not_confirmatory_functional_selectivity':True})
pd.DataFrame(summary).to_csv(E/'analysis/descriptive_token_category_summary.csv',index=False);print('DESCRIPTIVE_TOKEN_CATEGORIES',len(summary),flush=True)
