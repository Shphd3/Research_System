from pathlib import Path
import json,collections
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];rows=[]
for doc in docs:
 a=np.load(E/'cache'/(doc['doc_id']+'.npz'));z=a['z_selected'];re=a['h']-a['reconstruction'];norm=np.sum(a['h']**2,1);nmse=np.sum(re**2,1)/np.maximum(norm,1e-20)
 for j,f in enumerate(cfg['candidate_features']):
  pos=z[:,j]>0;rows.append({'split':doc['split'],'doc_id':doc['doc_id'],'host':doc['host'],'domain_keyword_cohort':doc['domain'],'feature':f,'reference_frequency_group':next(k for k,v in cfg['candidate_feature_groups'].items() if f in v),'positions':len(z),'positive_positions':int(pos.sum()),'positive_coefficient_mean':float(z[pos,j].mean()) if pos.any() else None,'coefficient_mean_all':float(z[:,j].mean()),'dictionary_residual_NMSE_mean':float(nmse.mean())})
pd.DataFrame(rows).to_csv(E/'analysis/selected_feature_document_support.csv',index=False)
D=pd.DataFrame([{k:d[k] for k in ['doc_id','domain','split','host','source_line','source_token_count','window_tokens','document_group','url']} for d in docs]);D.to_csv(E/'analysis/document_source_index.csv',index=False)
D.groupby(['domain','split','host'],as_index=False).agg(documents=('doc_id','count'),source_tokens_min=('source_token_count','min'),source_tokens_median=('source_token_count','median'),source_tokens_max=('source_token_count','max'),window_tokens_min=('window_tokens','min'),window_tokens_median=('window_tokens','median'),window_tokens_max=('window_tokens','max')).to_csv(E/'analysis/source_and_length_coverage.csv',index=False)
print('SUPPORT_COMPLETE',len(rows),flush=True)
