from pathlib import Path
import json,sys
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];sys.path.insert(0,str(E/'scripts'));import analyze as A
P=dict(np.load(E/'analysis/pca.npz'));PC=A.cfg['PC_candidates'];V=P['h_V'][:,PC];sd=np.sqrt(P['h_eigenvalues'][PC]);all_rows=[];summaries=[]
for split in ['discovery','development','validation']:
 for d in [x for x in A.DOC if x['split']==split]:
  h=np.load(E/'cache'/(d['doc_id']+'.npz'))['h'].astype(float)-P['h_mean'];proj=h@V;resp={'signed_trainSD':proj/sd,'signed_cosine':proj/np.maximum(np.linalg.norm(h,axis=1),1e-20)[:,None]};labels=A.LABEL.iloc[d['row_start']:d['row_start']+128]
  for flag in A.FLAGS:
   pairs=A.pairs(d,labels[flag].to_numpy(bool))
   if not len(pairs):continue
   p,n=pairs.T
   for metric,rr in resp.items():
    diff=(rr[p]-rr[n]).mean(0)
    for j,pc in enumerate(PC):all_rows.append({'split':split,'phenomenon':flag,'PC_index0':pc,'metric':metric,'doc_id':d['doc_id'],'host':d['host'],'pairs':len(p),'effect':float(diff[j])})
 D=pd.DataFrame([x for x in all_rows if x['split']==split])
 for (flag,pc,metric),q in D.groupby(['phenomenon','PC_index0','metric']):
  v=q.effect.to_numpy();boot=v[np.random.default_rng(110204).integers(0,len(v),(2000,len(v)))].mean(1);lo,hi=np.quantile(boot,[.025,.975]);summaries.append({'split':split,'phenomenon':flag,'PC_index0':pc,'metric':metric,'effect':v.mean(),'low95':lo,'high95':hi,'documents':len(v),'hosts':q.host.nunique(),'pairs':q.pairs.sum()})
 print('SIGNED_SUMMARY',split,len(D),flush=True)
D=pd.DataFrame(all_rows);S=pd.DataFrame(summaries);D.to_csv(E/'analysis/signed_direction_document_effects.csv',index=False);S.to_csv(E/'analysis/signed_direction_associations.csv',index=False);val=D[D.split=='validation'].copy();val['key']=val.phenomenon+'::'+val.PC_index0.astype(str)+'::'+val.metric;M=val.pivot(index='doc_id',columns='key',values='effect');mat=M.to_numpy();rng=np.random.default_rng(110204);draw=rng.integers(0,len(mat),(2000,len(mat)));boot=np.nanmean(mat[draw],axis=1);mean=np.nanmean(mat,axis=0);se=np.nanstd(boot,axis=0);den=np.maximum(se,1e-12);maxt=np.nanmax(abs((boot-mean)/den),axis=1);critical=np.quantile(maxt,.95);lookup={k:i for i,k in enumerate(M.columns)};out=[]
for _,r in S[S.split=='validation'].iterrows():
 k=lookup[r.phenomenon+'::'+str(int(r.PC_index0))+'::'+r.metric];q=r.to_dict();q.update({'low_simultaneous':mean[k]-critical*se[k],'high_simultaneous':mean[k]+critical*se[k],'familywise_p':(np.sum(maxt>=abs(mean[k])/den[k])+1)/2001,'eligibility':'EXPLORATORY_PROTOCOL_COMPLETION_A6_AFTER_BAND_RESULTS;notfreshconfirmatoryendpoint'});disc=S[(S.split=='discovery')&(S.phenomenon==r.phenomenon)&(S.PC_index0==r.PC_index0)&(S.metric==r.metric)];dev=S[(S.split=='development')&(S.phenomenon==r.phenomenon)&(S.PC_index0==r.PC_index0)&(S.metric==r.metric)];same=len(disc)>0 and len(dev)>0 and disc.iloc[0].effect*dev.iloc[0].effect>0 and disc.iloc[0].effect*r.effect>0;q['three_split_same_sign']=same;q['exploratory_consistent_association']=bool(same and r.documents>=12 and r.hosts>=2 and q['familywise_p']<.05);out.append(q)
pd.DataFrame(out).to_csv(E/'analysis/signed_direction_validation.csv',index=False);(E/'audit/signed_direction_family.json').write_text(json.dumps({'tests':len(M.columns),'candidate_PC_indices0':PC,'metrics':['signed_trainSD','signed_cosine'],'bootstrap':2000,'max_stat_critical':float(critical),'status':'EXPLORATORY_A6_NOT_RETROACTIVE_CONFIRMATION','basis_sign_convention':'largestloadingpositive;signnotintrinsicsemantic','allfixedPCsandallfrozenpropertiesincluded':True},indent=2)+'\n');print('SIGNED_COMPLETE',sum(x['exploratory_consistent_association'] for x in out),flush=True)
