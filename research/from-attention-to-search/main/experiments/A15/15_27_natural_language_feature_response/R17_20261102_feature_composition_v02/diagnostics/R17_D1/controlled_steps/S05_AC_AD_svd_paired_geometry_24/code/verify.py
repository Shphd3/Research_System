from common import *
import numpy as np,itertools
plan=json.load(open(R/'frozen_plan.json'));D=np.load(R/'data/S04_frozen_activations.npz');panel=rows(R/'data/panel.jsonl');freeze=json.load(open(R/'evidence/bases_frozen_before_check.json'));man=rows(R/'results/matrix_manifest.jsonl');tops=list(csv.DictReader(open(R/'results/top_loading_members.csv')));projs=list(csv.DictReader(open(R/'results/projections_all24.csv')))
for n,h in plan['data_SHA256'].items():assert sha(R/'data'/n)==h
for n,h in json.load(open(R/'evidence/protocol_freeze.json'))['protocol_SHA256'].items():assert sha(R/n)==h
for n,h in freeze['code_SHA256'].items():assert sha(R/'code'/n)==h
for n,h in freeze['matrix_SHA256'].items():assert sha(R/n)==h
assert sha(R/'results/top_loading_members.csv')==freeze['top_loading_SHA256']
for p,h in json.load(open(R/'evidence/old_immutable_before.json')).items():assert sha(p)==h
errs={k:0. for k in ['centering','orthogonality','reconstruction','gram_spectrum_squared','projection','difference_projection','mean_cosine_cross_terms','between_within_SS']};nproj=0;ndiff=0;nmembers=0
for m in man:
 site,scale,g=m['site'],m['scale'],m['group'];zz=D[site+'__z'].astype(float);x=zz if scale=='raw_z' else zz*D[site+'__decoder_norm'];a=np.load(R/m['cache']);ii=a['row_indices'];ci=1 if g=='AC' else 2
 assert ii.tolist()==[j for f in range(3) for j in [f*4,f*4+ci]] and a['X'].shape==(6,30000) and np.array_equal(a['X'],x[ii]);assert all(i<12 for i in ii)
 assert m['row_ids']==[panel[i]['id'] for i in ii] and int(a['rank'])<=5
 mean=x[ii].mean(0);A=x[ii]-mean;V=a['components'];s=a['singular_values'];rank=int(a['rank'])
 errs['centering']=max(errs['centering'],float(abs(mean-a['mean']).max()),float(abs(A.mean(0)).max()));errs['orthogonality']=max(errs['orthogonality'],float(abs(V@V.T-np.eye(6)).max()));errs['reconstruction']=max(errs['reconstruction'],float(abs((A@V[:rank].T)@V[:rank]-A).max()))
 eig=np.linalg.eigvalsh(A@A.T)[::-1];errs['gram_spectrum_squared']=max(errs['gram_spectrum_squared'],float(abs(eig-s*s).max()))
 for k in [0,1]:
  expected=np.lexsort((np.arange(30000),-abs(V[k])))[:5].tolist();tt=[v for v in tops if v['site']==site and v['scale']==scale and v['group']==g and int(v['direction'])==k+1];assert [int(v['atom']) for v in tt]==expected;assert all(abs(float(t['coefficient'])-V[k,int(t['atom'])])<1e-15 for t in tt)
 pc=(x-mean)@V[:2].T
 for p in [r for r in projs if r['site']==site and r['scale']==scale and r['basis']==g]:
  j=next(i for i,r in enumerate(panel) if r['id']==p['id']);err=max(abs(pc[j,0]-float(p['PC1'])),abs(pc[j,1]-float(p['PC2'])));errs['projection']=max(errs['projection'],float(err));nproj+=1
for site,scale in itertools.product(SITES,SCALES):
 zz=D[site+'__z'].astype(float);x=zz if scale=='raw_z' else zz*D[site+'__decoder_norm'];d=np.load(R/f'cache/{site}/{scale}/paired_differences.npz');AC=np.load(R/f'cache/{site}/{scale}/AC.npz');AD=np.load(R/f'cache/{site}/{scale}/AD.npz');assert np.array_equal(AC['X'][::2],AD['X'][::2]),'Same parents'
 for fine,ci in [('cat',1),('dog',2)]:
  delta=x[ci::4]-x[0::4];assert np.array_equal(delta,d['delta_'+fine]);assert np.array_equal(d['components_'+fine].sum(1),delta)
  assert np.allclose(delta[:3].mean(0),d['mean_exploration_'+fine],rtol=0,atol=1e-13)
  for fi in range(6):
   components=d['components_'+fine][fi];assert np.count_nonzero((components!=0).sum(0)>1)==0
   assert abs(np.sum(components**2)-np.sum(delta[fi]**2))<1e-8
   for fit in [AC,AD]:
    V=fit['components'][:2];mu=fit['mean'];out=delta[fi]@V.T;pair=(x[fi*4+ci]-mu)@V.T-(x[fi*4]-mu)@V.T;errs['difference_projection']=max(errs['difference_projection'],float(abs(out-pair).max()))
   ndiff+=1
 ms=list(csv.DictReader(open(R/'results/mean_difference_summary.csv')));main=next(v for v in ms if v['site']==site and v['scale']==scale);dot=[v for v in csv.DictReader(open(R/'results/mean_difference_cross_parts.csv')) if v['site']==site and v['scale']==scale];errs['mean_cosine_cross_terms']=max(errs['mean_cosine_cross_terms'],abs(sum(float(v['contribution_to_total_mean_cosine']) for v in dot)-float(main['exploration_cat_dog_signed_cosine'])))
 # Subspace overlap independently via principal singular values (not explicit30000x30000 projectors).
 va=AC['components'][:2];vb=AD['components'][:2];sv=np.linalg.svd(va@vb.T,compute_uv=False);record=next(v for v in rows(R/'results/geometry_comparisons.jsonl') if v['site']==site and v['scale']==scale);assert abs(float(np.sum(sv*sv)/2)-record['top2_normalized_overlap'])<1e-12
 for v in csv.DictReader(open(R/'results/SVD_between_within_family.csv')):
  if v['site']==site and v['scale']==scale:errs['between_within_SS']=max(errs['between_within_SS'],abs(float(v['total_score_SS'])-float(v['between_family_midpoint_SS'])-float(v['within_family_parent_fine_SS'])))
for v in csv.DictReader(open(R/'results/selected_member_all24_values.csv')):
 j=next(j for j,p in enumerate(panel) if p['id']==v['id']);i=int(v['atom']);site=v['site'];assert float(v['z'])==float(D[site+'__z'][j,i]) and float(v['preactivation'])==float(D[site+'__pre'][j,i]);nmembers+=1
boot=rows(R/'results/bootstrap_raw.jsonl')
for site,scale in itertools.product(SITES,SCALES):
 rr=[v for v in boot if v['site']==site and v['scale']==scale];assert len(rr)==27 and len({tuple(v['sequence']) for v in rr})==27;assert len({tuple(sorted(v['sequence'])) for v in rr})==10
 assert all(set(v['sequence'])<=set(plan['split']['exploration']) for v in rr)
 assert sum(v['top2_overlap'] is None for v in rr)==3
 assert all(v['AC_rank']<=2*v['distinct_families']-1 and v['AD_rank']<=2*v['distinct_families']-1 for v in rr)
 for v in rr:
  for k in ['PC1_absolute_cosine','top2_overlap','AC_PC1_vs_full','AD_PC1_vs_full','AC_top2_vs_full','AD_top2_vs_full']:
   if v[k] is not None:assert -1e-12<=v[k]<=1+1e-12
assert errs['centering']<1e-10 and errs['orthogonality']<1e-10 and errs['reconstruction']<1e-9 and errs['gram_spectrum_squared']<1e-7 and errs['projection']<1e-10 and errs['difference_projection']<1e-10 and errs['mean_cosine_cross_terms']<1e-12 and errs['between_within_SS']<1e-8
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',matrix_fits=8,bootstrap_fits=216,bootstrap_records=108,valid_top2_per27=24,undefined_top2_per27=3,old_files_unchanged=len(json.load(open(R/'evidence/old_immutable_before.json'))),projection_replays=nproj,paired_difference_replays=ndiff,member_value_replays=nmembers,max_errors=errs,source_S04_neutral_suffix_verified=True,means_topmembers_exploration_only=True,model_forwards=0,SAE_updates=0,probe=0,intervention=0,scientific_acceptance='Unknown',next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW'))
print('S05_VERIFIED',errs,nproj,ndiff,nmembers,flush=True)
