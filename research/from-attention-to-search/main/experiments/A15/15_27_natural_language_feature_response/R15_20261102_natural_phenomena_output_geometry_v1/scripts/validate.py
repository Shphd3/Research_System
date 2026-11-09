from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,torch
from safetensors import safe_open
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];torch.set_num_threads(2);P=dict(np.load(E/'analysis/pca.npz'));G=dict(np.load(E/'analysis/head_geometry.npz'));F=json.load(open(E/'validation_selection_frozen.json'));freeze=json.load(open(E/'freeze.json'));errors=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for f,h in freeze['sha256'].items():
 if sha(f)!=h:errors.append('frozen_source_changed:'+f)
rows=0;normerror=0;mean={k:np.zeros(1024) for k in ['h','y']};nfit=0;reconstruction=[]
for d in docs:
 a=np.load(E/'cache'/(d['doc_id']+'.npz'));rows+=len(a['h']);assert str(a['freeze_hash'])==sha(E/'freeze.json');x=torch.tensor(a['h'],dtype=torch.bfloat16);n=(x.float()*torch.rsqrt(x.float().pow(2).mean(-1,keepdim=True)+float(G['norm_eps']))).to(torch.bfloat16)*torch.tensor(G['final_norm_weight'],dtype=torch.bfloat16);normerror=max(normerror,float(np.max(abs(n.float().numpy()-a['y']))))
 if d['split']=='discovery':
  nfit+=len(a['h'])
  for k in mean:mean[k]+=a[k].sum(0,dtype=np.float64)
 residual=a['h'].astype(float)-a['reconstruction'].astype(float);reconstruction.extend((np.sum(residual**2,1)/np.maximum(np.sum(a['h'].astype(float)**2,1),1e-20)).tolist())
meanerror=max(float(np.max(abs(mean[k]/nfit-P[k+'_mean']))) for k in mean)
D=pd.read_csv(E/'analysis/validation_document_effects.csv');A=pd.read_csv(E/'analysis/validation_associations.csv');maxerror=0
for (phen,response,mode),q in D.groupby(['phenomenon','response','matching']):
 r=A[(A.phenomenon==phen)&(A.response==response)&(A.matching==mode)].iloc[0];maxerror=max(maxerror,abs(r.effect-q.value.mean()));assert len(q)==int(r.documents)
# Actual matched changes checked by direct block multiplication,not only a random Gram-vector check.
T=pd.read_csv(E/'analysis/validation_matched_positions.csv');case_rows=[]
with safe_open(cfg['model']+'/model.safetensors',framework='pt',device='cpu') as handle:
 key='lm_head.weight' if 'lm_head.weight' in handle.keys() else 'model.embed_tokens.weight';W=handle.get_tensor(key).to(torch.bfloat16);vocab=len(W)
 for _,r in T.iloc[::max(1,len(T)//6)].head(6).iterrows():
  d=next(d for d in docs if d['doc_id']==r.doc_id);a=np.load(E/'cache'/(r.doc_id+'.npz'));v=a['y'][int(r.positive_row)-d['row_start']].astype(float)-a['y'][int(r.negative_row)-d['row_start']].astype(float);direct=0.
  for lo in range(0,vocab,4096):w=W[lo:lo+4096].double().numpy()-G['vocab_mean'];delta=w@v;direct+=float(delta@delta)
  q512=torch.zeros((512,1024),dtype=torch.bfloat16);q512[0]=torch.tensor(a['y'][int(r.positive_row)-d['row_start']],dtype=torch.bfloat16);q512[1]=torch.tensor(a['y'][int(r.negative_row)-d['row_start']],dtype=torch.bfloat16);native=(q512@W.T)[:2].float().numpy();nd=native[0]-native[1];nd-=nd.mean();native_rms=float(np.sqrt(np.mean(nd**2)));quadratic=float(v@G['Gc']@v);case_rows.append({'positive_row':int(r.positive_row),'negative_row':int(r.negative_row),'direct_centered_logit_RMS':float(np.sqrt(direct/vocab)),'Gram_centered_logit_RMS':float(np.sqrt(quadratic/vocab)),'actual_BF16_centered_logit_RMS':native_rms,'BF16_vs_FP64_RMS_relative_difference':abs(native_rms-np.sqrt(quadratic/vocab))/max(np.sqrt(quadratic/vocab),1e-12),'relative_error':abs(direct-quadratic)/max(direct,1e-12)})
pd.DataFrame(case_rows).to_csv(E/'analysis/actual_change_direct_head_audit.csv',index=False)
ledger=pd.read_csv(E/'analysis/nonadditive_residual_ledger.csv') if (E/'analysis/nonadditive_residual_ledger.csv').exists() and (E/'analysis/nonadditive_residual_ledger.csv').stat().st_size>10 else pd.DataFrame()
result={'positions_checked':rows,'cache_norm_replay_max_abs':normerror,'discovery_only_PCA_mean_error_max':meanerror,'validation_document_mean_reaggregation_error':maxerror,'actual_change_direct_vs_Gram_relative_max':max((r['relative_error'] for r in case_rows),default=0),'matched_rows_checked_directly':case_rows,'original_frozen_input_changes':errors,'effective_label_version':'1.2','effective_labels_sha256':sha(E/'data/labels_effective_v1p2.jsonl'),'validation_response_statistics_after_selection_freeze':(E/'validation_selection_frozen.json').stat().st_mtime < (E/'analysis/validation_associations.csv').stat().st_mtime,'dictionary_NMSE_mean_all_positions':float(np.mean(reconstruction)),'decomposition_max_absolute_error':float(ledger.identity_abs_error.max()) if len(ledger) else None,'h_PCA_trace_sum':float(P['h_eigenvalues'].sum()),'y_PCA_trace_sum':float(P['y_eigenvalues'].sum()),'head_eigen_residual':json.load(open(E/'audit/head_geometry.json'))['eigen_residual']}
result['effective_labels_and_selection_hashes_match']=(F['effective_label_table_sha256']==sha(E/'data/labels_effective_v1p2.jsonl') and F['effective_definition_sha256']==sha(E/'data/phenomenon_definitions_v1p2.json') and F['discovery_sha256']==sha(E/'analysis/discovery_associations.csv') and F['development_sha256']==sha(E/'analysis/development_associations.csv'))
result['pass']=result['effective_labels_and_selection_hashes_match'] and not errors and normerror==0 and meanerror<1e-9 and maxerror<1e-9 and result['actual_change_direct_vs_Gram_relative_max']<1e-10 and result['validation_response_statistics_after_selection_freeze'];(E/'audit/final_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['pass']
