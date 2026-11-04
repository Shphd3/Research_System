"""Independent recomputation from saved inputs; no forwards or fitting."""
from pathlib import Path
import json,csv,hashlib,os
os.environ['OPENBLAS_NUM_THREADS']='2'
import numpy as np
O=Path(__file__).resolve().parent;B=O.parent;R=B/'R04_domain_usage_20261027'
def js(p):return json.loads(Path(p).read_text())
def rows(p):return list(csv.DictReader(Path(p).open(encoding='utf-8-sig')))
def jl(p):return [json.loads(s) for s in Path(p).read_text().splitlines()]
checks=[]
def check(name,v):
    checks.append(dict(name=name,passed=bool(v)))
    assert v,name
fr=js(O/'freeze.json');ids=fr['ordered_union'];master=rows(O/'tables/master_members.csv');a=np.load(R/'forward/documents_CC.npz');docs=jl(R/'data/documents.jsonl')
check('same32_and_order_every_master',ids==[int(r['feature']) for r in master] and len(set(ids))==32)
check('sign_groups_disjoint',not set(fr['groups']['math'])&set(fr['groups']['biology']))
labels=np.array([d['label'] for d in docs]);splits=np.array([d['split'] for d in docs]);score=a['sum_z']/160
for j,f in enumerate(ids):
    for split in ['discovery','development','heldout']:
        m=score[(splits==split)&(labels==1),f];b=score[(splits==split)&(labels==0),f];v=np.mean((m[:,None]>b).astype(float)+.5*(m[:,None]==b))
        check(f'AUC_f{f}_{split}',abs(v-float(master[j][split+'_AUC_math']))<1e-12)
    for lab,name in [(1,'math'),(0,'biology')]:
        check(f'qualification_f{f}_{name}',int(master[j]['discovery_'+name+'_active_documents'])>=5)
q=np.load(O/'analysis/discovery_qualification.npz')
for s,sign in [('math',1),('biology',-1)]:
    rank=[f for f in q['order'] if q['direction'][f]==sign][:16]
    check('discovery_rank_'+s,rank==fr['groups'][s])

geo=np.load(O/'analysis/unit_decoder_geometry.npz');pc=np.load(fr['basis'])['PC_columns'];decoder=np.load(B/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz')['decoder_model_scale']
check('basis_full_orthonormal',np.max(abs(pc.T@pc-np.eye(1024)))<1e-9)
check('frozen_basis_hash',hashlib.sha256(Path(fr['basis']).read_bytes()).hexdigest()==fr['basis_sha256'])
for j,f in enumerate(ids):
    u=decoder[f]/np.linalg.norm(decoder[f]);p=np.array([np.dot(u,pc[:,k])**2 for k in range(1024)])
    check(f'perPC_independent_f{f}',np.max(abs(p-geo['per_PC'][j]))<1e-12)
    check(f'full_energy_one_f{f}',abs(p.sum()-1)<1e-9)
    check(f'band_sum_f{f}',np.max(abs(p.reshape(16,64).sum(1)-geo['per_band'][j]))<1e-12)
p=geo['per_PC'][:16].mean(0);qg=geo['per_PC'][16:].mean(0);g=js(O/'analysis/spectrum.json')['geometry']
check('overlap_L1_identity',abs((1-abs(p-qg).sum()/2)-g['overlap_per_PC'])<1e-12)
check('band_coarsening_increases_overlap',g['overlap_per_band']>=g['overlap_per_PC'])
pair=rows(O/'tables/pair_absolute_cosine.csv')
for r in pair:
    i=ids.index(int(r['math_feature']));j=ids.index(int(r['biology_feature']))
    check('pair_cos_'+r['math_feature']+'_'+r['biology_feature'],abs(abs(np.dot(geo['unit_decoder'][i],geo['unit_decoder'][j]))-float(r['abs_cosine']))<1e-12)
qm=np.linalg.svd(geo['unit_decoder'][:16].T,full_matrices=False)[0];qb=np.linalg.svd(geo['unit_decoder'][16:].T,full_matrices=False)[0]
check('subspace_trace_independent_SVD',abs(np.linalg.norm(qm.T@qb,'fro')**2/16-g['subspace_trace_overlap_fraction'])<1e-12)
ref=np.load(R/'forward/reference_CC.npz');hits=ref['counts'].sum(0);check('reference_N',int(ref['n_positions'].sum())==65536)
for j,f in enumerate(ids):check(f'reference_rate_f{f}',abs(float(master[j]['feature_reference_rate'])-hits[f]/65536)<1e-12)

nat=np.load(O/'analysis/natural_selected_positions.npz');z=nat['z'];t=nat['token_id'];di=nat['document_index'];pos=nat['position'];check('positions_window',len(t)==19200 and pos.min()==32 and pos.max()==191)
trs=rows(O/'tables/token_member_summary.csv');rt=np.concatenate([r['token_ids'] for r in jl(R/'data/reference.jsonl')]);counts=np.bincount(rt,minlength=int(max(rt.max(),t.max()))+1)
for j,f in enumerate(ids):
    active=z[:,j]>0;seen=counts[t[active]]>0;rr=next(r for r in trs if int(r['feature'])==f)
    check(f'input_token_n_f{f}',active.sum()==int(rr['active_positions']))
    check(f'token_frequency_median_f{f}',abs(np.median(counts[t[active][seen]]/65536)-float(rr['token_rate_median']))<1e-12)
    check(f'unseen_count_f{f}',int((~seen).sum())==int(rr['token_reference_unseen_n']))
    check(f'input_counts_replay_f{f}',int(active.sum())==int(a['counts'][:,f].sum()))
ex=rows(O/'tables/real_token_examples.csv');quota={}
from tokenizers import Tokenizer
tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')
for k,r in enumerate(ex):
    d=next(x for x in docs if x['seq_id']==r['document']);position=int(r['position_zero_based']);key=(r['feature'],r['document']);quota[key]=quota.get(key,0)+1
    check(f'prefix_no_future_{k}',tok.decode(d['token_ids'][:position],skip_special_tokens=False)==r['read_prefix'])
    check(f'current_token_id_{k}',d['token_ids'][position]==int(r['token_id']))
check('example_document_cap',max(quota.values())<=2)

panel=jl(B/'R07_fixed_target_domain_spectrum_20261029/data/panel.jsonl');tz=np.load(B/'R08_within_mixed_subspaces_20261029/forward/target_readings.npz')['z'][:,ids].astype(float);ef=rows(O/'tables/context_effects.csv');rng=np.random.default_rng(2026103003)
for split in ['discovery','development','heldout']:
    fs=sorted({r['family'] for r in panel if r['split']==split});boots=rng.integers(0,len(fs),(2000,len(fs)))
    for e in [0,1]:
        for w in [0,1]:
            delta=[]
            for f in fs:
                mi=next(i for i,r in enumerate(panel) if r['family']==f and r['domain']=='math' and r['ending']==e and r['wording']==w);bi=next(i for i,r in enumerate(panel) if r['family']==f and r['domain']=='biology' and r['ending']==e and r['wording']==w)
                check(f'same_target_{split}_{e}_{w}_{f}',panel[mi]['target_token_id']==panel[bi]['target_token_id'])
                delta.append(tz[mi]-tz[bi])
            delta=np.array(delta);lo,hi=np.quantile(delta[boots].mean(1),[.025,.975],axis=0)
            for j,f in enumerate(ids):
                r=next(r for r in ef if int(r['feature'])==f and r['split']==split and int(r['wording'])==w and r['target']==['example','explanation'][e])
                check(f'family_mean_CI_{f}_{split}_{e}_{w}',max(abs(float(r['delta_math_minus_biology'])-delta[:,j].mean()),abs(float(r['CI_low'])-lo[j]),abs(float(r['CI_high'])-hi[j]))<1e-12)
cats=rows(O/'tables/context_categories.csv')
for r in cats:
    j=ids.index(int(r['feature']));n=int((tz[:,j]>0).sum());check('zero_coverage_not_identity_'+r['feature'],n!=0 or r['category']=='C')
bg=np.load(O/'analysis/math_matched_background.npz')['ids'];refbin=np.floor(np.log2(hits+.5)).astype(int);supp=(q['support_math']+q['support_biology'])//5
check('math_background_disjoint_main',not np.isin(bg,ids).any())
target=sorted(zip(refbin[ids[:16]],supp[ids[:16]]))
for k,draw in enumerate(bg):check(f'math_exact_match_{k}',len(set(draw))==16 and q['eligible'][draw].all() and sorted(zip(refbin[draw],supp[draw]))==target)
check('biology_unavailable_explicit',g['separate_group_matching']['biology']['status']=='NA_INSUFFICIENT_MATCHED_POOL')
for path,meta in js(O/'source_manifest.json')['sources'].items():check('source_unchanged_'+Path(path).name,hashlib.sha256(Path(path).read_bytes()).hexdigest()==meta['sha256'])
out=dict(passed=all(r['passed'] for r in checks),checks=len(checks),details=checks,scope='independent numerical, identity and input-prefix checks; not scientific approval or rendered math validation')
(O/'analysis/audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['passed','checks']}))
