"""One declared sensitivity: strict16is all-panel selected,so match all-panel support too."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,csv,numpy as np,shutil
from scipy import sparse
B=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response');S=B/'R10_domain_member_atlas_20261030';O=B/'R11_three_domain_replication_20261030/cached_spectral_baseline';D=O/'support_matching_audit';D.mkdir(exist_ok=True)
cfg={'revision':'strict-full-panel-support-sensitivity-v1','timing':'method audit after original cached discovery-matched result;not preregistered independent confirmation','reason':'strict16uses all120docs for zero-opposite selection while original A01reference matches discovery60only;check directional full-panel support as a stronger conditioning diagnostic','strata':'half-octave DCLM hits x floor(math all60active docs/5) x floor(biology all60active docs/5)','pool':'unchanged original discovery-qualified pool,INCLUDING strict16;exact sizes/counts,groups disjoint','draws':1000,'seed':2026103009,'new_model_forwards':0,'old_results_preserved':True}
if (D/'config.json').exists():assert json.loads((D/'config.json').read_text())==cfg
else:(D/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
f=json.loads((S/'presentation_variants/pooled_simple_20261030/freeze.json').read_text())['sets'];G={g:np.array(f['all_cached_strict_'+g]) for g in ['math','biology']};docs=[json.loads(x) for x in (B/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];agg=np.load(B/'R04_domain_usage_20261027/forward/documents_CC.npz');order={str(s):i for i,s in enumerate(agg['seq_id'])};ct=agg['counts'][[order[d['seq_id']] for d in docs]];sm=(ct[np.array([d['domain']=='math' for d in docs])]>0).sum(0);sb=(ct[np.array([d['domain']=='biology' for d in docs])]>0).sum(0);screen=list(csv.DictReader((S/'tables/all_dictionary_screen.csv').open()));hits=np.rint(np.array([float(r['DCLM_feature_occurrence']) for r in screen])*65536).astype(int);met=np.load(S/'analysis/discovery_metrics.npz');P=np.load(S/'analysis/all_decoder_projection.npz')['per_pc'];pool=np.flatnonzero(met['support']);keys=list(zip(np.where(hits>0,np.floor(2*np.log2(np.maximum(hits,1))).astype(int),-1),sm//5,sb//5));lookup={k:i for i,k in enumerate(sorted(set(keys)))};st=np.array([lookup[k] for k in keys]);ids=np.r_[G['math'],G['biology']];draw={g:np.empty((1000,len(G[g])),int) for g in G};rng=np.random.default_rng(cfg['seed']);stratarows=[]
for s in np.unique(st[ids]):
 cand=pool[st[pool]==s];loc={g:np.flatnonzero(st[G[g]]==s) for g in G};nm,nb=len(loc['math']),len(loc['biology']);assert nm+nb<=len(cand)
 for b in range(1000):
  p=rng.choice(cand,nm+nb,replace=False);draw['math'][b,loc['math']]=p[:nm];draw['biology'][b,loc['biology']]=p[nm:]
 stratarows.append(dict(stratum=int(s),eligible_candidates=len(cand),selected_math=nm,selected_biology=nb))
means={};stats={}
for g in G:
 ds=draw[g];weights=sparse.csr_matrix((np.full(ds.size,1/len(G[g])),(np.repeat(np.arange(1000),len(G[g])),ds.ravel())),shape=(1000,16384));means[g]=weights@P;lo,hi=np.quantile(means[g][:,:64].sum(1),[.025,.975]);obs=float(P[G[g],:64].sum(1).mean());stats[g]=dict(head_mean=obs,fullpanel_matched_head95=[float(lo),float(hi)],above=bool(obs>hi+1e-12),below=bool(obs<lo-1e-12),reference_selected_fraction=float(np.isin(ds,ids).mean()));np.savez_compressed(D/f'{g}_background.npz',feature_ids=ds,mean_per_pc=means[g])
for b in range(1000):
 assert not set(draw['math'][b])&set(draw['biology'][b])
 for g in G:assert np.array_equal(np.bincount(st[draw[g][b]],minlength=len(lookup)),np.bincount(st[G[g]],minlength=len(lookup)))
ov=np.minimum(means['math'],means['biology']).sum(1);ob=np.minimum(means['math'].reshape(1000,16,64).sum(2),means['biology'].reshape(1000,16,64).sum(2)).sum(1);qm=P[G['math']].mean(0);qb=P[G['biology']].mean(0);obs=float(np.minimum(qm,qb).sum());stats['overlap_per_PC']={'observed':obs,'matched95':np.quantile(ov,[.025,.975]).tolist(),'matched_median':float(np.median(ov)),'below':bool(obs<np.quantile(ov,.025)-1e-12)};stats['overlap_64PC']={'observed':float(np.minimum(qm.reshape(16,64).sum(1),qb.reshape(16,64).sum(1)).sum()),'matched95':np.quantile(ob,[.025,.975]).tolist()};stats['strata']=stratarows;stats['new_model_forwards']=0
if (D/'summary.json').exists() and not (D/'summary_before_numeric_flag_audit.json').exists():shutil.copy2(D/'summary.json',D/'summary_before_numeric_flag_audit.json')
stats['numeric_flag_audit']='1e-12absolute floating-comparison tolerance only;math observed equals upper bound to5.6e-17. No value,draw,stratum or scientific margin changes.'
(D/'summary.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats,indent=2),flush=True)
