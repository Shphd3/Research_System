"""Independent checks of selection, aggregation, geometry, token and context contracts."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import numpy as np,json,csv,hashlib,datetime,argparse
from scipy import sparse,stats
B=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response');parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=B/'R10_domain_member_atlas_20261030');args=parser.parse_args()
O=args.output;A=O/'analysis';T=O/'tables';R4=B/'R04_domain_usage_20261027';H=R4/'domain_discriminability_spectrum_20261028/real_spectrum_A01'
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));assert ok,(name,detail)
def rows(p):return list(csv.DictReader(p.open()))
d=[json.loads(s) for s in (R4/'data/documents.jsonl').read_text().splitlines()];lab=np.array([r['label'] for r in d]);split=np.array([r['split'] for r in d]);tr=np.flatnonzero(split=='discovery');mi=tr[lab[tr]==1];bi=tr[lab[tr]==0]
x=np.load(A/'discovery_metrics.npz');resp=x['document_response'];raw=x['raw_auc'];supp=x['support'];direction=x['direction'];f=json.loads((O/'freeze.json').read_text());M=np.array(f['sets']['main_math']);Bio=np.array(f['sets']['main_biology']);main=np.r_[M,Bio]
rank=stats.rankdata(np.r_[resp[mi],resp[bi]],axis=0,method='average');independent=(rank[:30].sum(0)-30*31/2)/900
check('auc_independent_Mann_Whitney_ranks_all16384',np.allclose(raw,independent,atol=1e-14),float(abs(raw-independent).max()))
for vals,wanted in [(np.array([0,0,0,0]),.5),(np.array([1,1,0,0]),1.),(np.array([0,0,1,1]),0.)]:
 ra=stats.rankdata(vals);aa=(ra[:2].sum()-3)/4;check('auc_calibration_'+str(wanted),aa==wanted)
Z=sparse.load_npz(A/'native_positions_csr.npz');pk=np.load(A/'position_keys.npz');dc=pk['document_index'];tk=pk['token_id'];po=pk['position'];zdoc=np.array([(Z[j*160:(j+1)*160]>0).sum(0).A1 for j in range(120)])
ms=(zdoc[mi]>0).sum(0);bs=(zdoc[bi]>0).sum(0)
check('either_domain_support_sparse_reconstruction',np.array_equal((ms>=5)|(bs>=5),supp))
expected=np.flatnonzero(supp&(np.maximum(raw,1-raw)>=.75));check('main_exact_all_above075_no_reselection',set(expected)==set(main))
check('main_directions_disjoint',len(set(M)&set(Bio))==0)
check('sparse_document_mean_contains_zeros',all(np.allclose(Z[j*160:(j+1)*160].sum(0).A1/160,resp[j],rtol=2e-6,atol=1e-7) for j in range(120)))
check('documents_independent_original_groups',len({r['document_group'] for r in d})==120)
reference=[json.loads(s) for s in (R4/'data/reference.jsonl').read_text().splitlines()]
from urllib.parse import urlsplit
def urlgroup(r):
 u=urlsplit(r['url']);return u.hostname,u.path.rstrip('/')
check('DCLM_reference_disjoint_document_groups',not ({urlgroup(r) for r in d}&{urlgroup(r) for r in reference}))
for g,sgn in [('math',1),('biology',-1)]:
 candidates=np.flatnonzero(supp&(direction==sgn));ranks=candidates[np.lexsort((candidates,-np.abs(raw[candidates]-.5)))];check('ranked_main_'+g,np.array_equal(ranks[np.maximum(raw[ranks],1-raw[ranks])>=.75],f['sets']['main_'+g]))
 for k in [16,64,128]:check(f'top{k}_'+g,np.array_equal(ranks[:k],f['sets'][f'top{k}_'+g]))
P=np.load(A/'all_decoder_projection.npz')['per_pc'];basis=np.load(A/'common_spectrum.npz');V=basis['PC_columns'];check('full_projection_conservation',np.allclose(P.sum(1),1,atol=1e-12));check('orthonormal_complete1024',np.allclose(V.T@V,np.eye(1024),atol=1e-12))
dec=np.load(B/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz');norm=np.linalg.norm(dec['decoder_model_scale'],axis=1);oldscale=np.load(H/'forward/decoder_scales.npz');norm8=np.load(B/'R08_within_mixed_subspaces_20261029/forward/normalization.npz')
check('TRAIN_RMS27_identity',np.array_equal(oldscale['CC_train_rms'],norm8['rms']) and dec['rms27']==norm8['rms'][-1])
# The historical field name says native, but its loader already multiplies by TRAIN RMS.
norm_relative_error=abs(norm-oldscale['CC_all_native'][-1])/oldscale['CC_all_native'][-1]
# Source computes a1024-component float32 norm before multiplying by float64 RMS.
# Compare against the standard accumulated-roundoff bound, not an effect-tuned tolerance.
u=np.finfo(np.float32).eps/2;gamma1024=1024*u/(1-1024*u)
check('decoder_model_norm_scale_identity_FP32_roundoff_bound',(norm_relative_error<=gamma1024).all(),dict(max_relative_error=float(norm_relative_error.max()),gamma1024=float(gamma1024)))
for fid in main[::47]:
 independent=(V.T@(dec['decoder_model_scale'][fid]/norm[fid]))**2;check('independent_projection_'+str(fid),np.allclose(P[fid],independent,atol=1e-14))
geom=json.loads((A/'geometry.json').read_text());q1=P[M].mean(0);q2=P[Bio].mean(0);totalvariation=.5*abs(q1-q2).sum();check('overlap_equals_one_minus_TV',np.isclose(geom['overlap_pc'],1-totalvariation));check('coarsening_cannot_lower_overlap',geom['overlap_band']>=geom['overlap_pc'])
check('PC2_64_mass_separate_from_renormalized_overlap',np.isclose(q1[1:64].sum(),geom['groups']['math']['PC2_64_mean']) and np.isclose(np.minimum(q1[1:64]/q1[1:64].sum(),q2[1:64]/q2[1:64].sum()).sum(),geom['PC2_64_overlap_renormalized']))
origcuts=[.002593994140625,.0134429931640625];ref=np.load(R4/'forward/reference_CC.npz');hits=ref['counts'].sum(0);freq=np.searchsorted(origcuts,hits/65536,side='left');freq[hits<20]=3;stratum=freq*10+(ms+bs)//10
oldbins=json.loads((B/'R05_distance_attention_20261028/analysis/CC_frequency_bins.json').read_text());check('historical_frequency_cuts_preserved',np.array_equal(oldbins['cuts'],origcuts))
draws={g:np.load(A/f'{g}_matched_background.npz')['feature_ids'] for g in ['math','biology']}
for i in range(1000):
 dm,db=draws['math'][i],draws['biology'][i];check('background_disjoint_unique_'+str(i),len(set(dm)|set(db))==len(dm)+len(db))
 for g,target in [('math',M),('biology',Bio)]:check('background_exact_strata_'+g+'_'+str(i),np.array_equal(np.bincount(stratum[draws[g][i]],minlength=40),np.bincount(stratum[target],minlength=40)))
# A direct model-coordinate sum against stored energy, independent of coefficient multiplication order.
j=next(j for j,r in enumerate(d) if r['split']=='heldout' and r['domain']=='math');v=Z[j*160:(j+1)*160,M]@dec['decoder_model_scale'][M];perpc=(v@V)**2
check('sum_then_square_equals_vector_norm',np.allclose(perpc.sum(1),(v*v).sum(1),rtol=1e-12,atol=1e-10))
con=rows(T/'group_reconstruction_energy.csv');check('all4_contribution_conditions',len(con)==64 and len({(r['member_group'],r['input_domain']) for r in con})==4)
for g in ['math','biology']:
 for dom in ['math','biology']:
  a=[r for r in con if r['member_group']==g and r['input_domain']==dom];check('contribution_fraction_sum_'+g+'_'+dom,np.isclose(sum(float(r['fraction']) for r in a),1))
check('cross_terms_not_replaced',any(abs(float(r['mean_squared_projection'])-float(r['incorrect_member_energy_sum']))>1e-4 for r in con))
tokenrows=rows(T/'panel_token_counts.csv');check('token_total_types_positions',len(tokenrows)==len(set(tk)) and sum(int(r['count']) for r in tokenrows)==19200)
check('token_domains_equal_denominator',sum(int(r['math_count']) for r in tokenrows)==9600 and sum(int(r['biology_count']) for r in tokenrows)==9600)
thr=np.load(A/'token_thresholds.npz')['positive_z_p90'];csc=Z.tocsc();trmask=np.isin(dc,tr);hmask=np.array([d[j]['split']=='heldout' for j in dc]);tm={int(r['feature_id']):r for r in rows(T/'token_member_summary.csv')}
for fid in main:
 lo,hi=csc.indptr[fid:fid+2];rr=csc.indices[lo:hi];vv=csc.data[lo:hi];vals=vv[trmask[rr]]
 if len(vals)>=20:check('discovery_only_p90_'+str(fid),np.isclose(thr[fid],np.quantile(vals,.9)))
 hr=rr[hmask[rr]&(vv>thr[fid])];check('heldout_strict_high_count_'+str(fid),len(hr)==int(tm[fid]['heldout_high_events']))
ex=rows(T/'real_token_examples.csv')
for r in ex:
 j=next(i for i,dd in enumerate(d) if dd['seq_id']==r['seq_id']);pt=int(r['position']);fid=int(r['feature_id']);check('actual_token_position_'+str(fid)+'_'+r['seq_id']+'_'+r['kind'],d[j]['token_ids'][pt]==int(r['token_id']) and np.isclose(Z[j*160+pt-32,fid],float(r['z'])))
panel=[json.loads(s) for s in (B/'R07_fixed_target_domain_spectrum_20261029/data/panel.jsonl').read_text().splitlines()];pr={r['seq_id']:r for r in panel};targetsets={e:{r['target_token_id'] for r in panel if r['ending']==e} for e in [0,1]}
check('fixed_target_ID_within_ending',all(len(v)==1 for v in targetsets.values()));target_positions=sorted({r['target_position'] for r in panel})
check('paired_A_target_positions_equal',all(r['target_position']==pr[r['seq_id'].replace('_math_','_biology_')]['target_position'] for r in panel if r['domain']=='math'))
check('paired_endings_target_positions_equal',all(r['target_position']==pr[r['seq_id'][:-1]+'1']['target_position'] for r in panel if r['ending']==0))
check('target_ID_is_actual_input_at_position',all(r['token_ids'][r['target_position']]==r['target_token_id'] for r in panel))
zero=np.ones(len(main),bool)
for s in ['discovery','development','heldout']:
 ca=np.load(A/f'context_{s}.npz');zero&=(ca['activation']==0).all((0,1,2,3));check('context_member_order_'+s,np.array_equal(ca['feature_ids'],main))
cat=rows(T/'context_categories.csv');cz=np.array([r['all_fixed_target_zero']=='True' for r in cat]);check('all_zero_considers_ALL_splits',np.array_equal(cz,zero));check('zero_is_insufficient_not_identity',all(r['category']=='insufficient' for r,z in zip(cat,zero) if z))
# Numerical interpretation diagnostics, not new selection criteria.
diag={}
for g,ids in [('math',M),('biology',Bio)]:
 head=P[ids,:64].sum(1);trim=np.sort(head)[:int(np.floor(.9*len(ids)))];good=[tm[int(i)] for i in ids if tm[int(i)]['usable']=='True'];diag[g]={'head_above_dimensional_share_fraction':float((head>64/1024).mean()),'head_mean_after_remove_top10pct':float(trim.mean()),'high_response_distinct_token_ids_median':float(np.median([int(r['distinct_high_token_ids']) for r in good])),'high_response_top5_token_share_median':float(np.median([float(r['top5_high_token_share']) for r in good])),'heldout_direction_agrees':sum(r['heldout_direction_agrees']=='True' for r in rows(T/'master_members.csv') if r['domain_bias']==g)}
out={'checks':checks,'passed':sum(r['passed'] for r in checks),'failed':sum(not r['passed'] for r in checks),'target_position_values':target_positions,'descriptive_diagnostics':diag,'new_model_forwards':0,'training_updates':0,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(A/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
