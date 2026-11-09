"""Frozen-basis projections and direct paired differences. No SVD or member selection here."""
from common import *
from geometry import signed_cos,decompose
import itertools,numpy as np
plan=json.load(open(R/'frozen_plan.json'));freeze=json.load(open(R/'evidence/bases_frozen_before_check.json'));panel=rows(R/'data/panel.jsonl');source=np.load(R/'data/S04_frozen_activations.npz');top=list(csv.DictReader(open(R/'results/top_loading_members.csv')));H2=json.load(open(R/'data/S03_frozen_selection.json'))['sites']
for n,h in freeze['matrix_SHA256'].items():assert sha(R/n)==h
assert sha(R/'results/top_loading_members.csv')==freeze['top_loading_SHA256']
projrows=[];classrows=[];pairrows=[];deltaproj=[];eventrows=[];partrows=[];dotrows=[];meanparts=[];varrows=[];membervals=[];zeroaudit=[];counters=[];meansummary=[]
for site in SITES:
 z=source[site+'__z'].astype(float);pre=source[site+'__pre'].astype(float);dn=source[site+'__decoder_norm'].astype(float);active=z>0
 # Member membership was fixed by fit.py before this script accesses check values.
 for scale in SCALES:
  x=z if scale=='raw_z' else z*dn;fits={g:np.load(R/f'cache/{site}/{scale}/{g}.npz') for g in ['AC','AD']};tol=float(fits['AC']['near_zero_tol']);coords={}
  for g,fit in fits.items():
   V=fit['components'][:2];mu=fit['mean'];pc=(x-mu)@V.T;coords[g]=pc
   for j,p in enumerate(panel):projrows.append(dict(site=site,scale=scale,basis=g,id=p['id'],family=p['family'],split=p['split'],condition=p['condition'],fit_row=bool(j in fit['row_indices']),PC1=float(pc[j,0]),PC2=float(pc[j,1]),centering='saved own exploration mean',target_token_id=25))
   for split,condition in itertools.product(['exploration','heldout_check'],CONDS):
    ix=[j for j,p in enumerate(panel) if p['split']==split and p['condition']==condition];cc=pc[ix];center=cc.mean(0);rad=float(np.sqrt(np.mean(np.sum((cc-center)**2,axis=1))))
    classrows.append(dict(site=site,scale=scale,basis=g,split=split,condition=condition,N=len(ix),centroid_PC1=float(center[0]),centroid_PC2=float(center[1]),RMS_radius_2D=rad,PC1_population_std=float(cc[:,0].std()),PC2_population_std=float(cc[:,1].std()),role='descriptive class summaries in frozen axes;not refitting or classifier'))
   fitix=fit['row_indices'];train=pc[fitix].reshape(3,2,2);mid=train.mean(1);dif=train[:,1]-train[:,0]
   for k in range(2):
    between=float(2*np.sum(mid[:,k]**2));within=float(.5*np.sum(dif[:,k]**2));total=float(np.sum(train[:,:,k]**2));assert abs(total-between-within)<1e-8
    varrows.append(dict(site=site,scale=scale,group=g,direction=k+1,total_score_SS=total,between_family_midpoint_SS=between,within_family_parent_fine_SS=within,between_fraction=between/total,within_fraction=within/total,identity_residual=total-between-within))
  differences={};parts={};mu={};checkmu={}
  for fine,ci in [('cat',1),('dog',2)]:
   dd=[];pp=[]
   for fi in range(6):
    a=fi*4;b=a+ci;delta,component,masks=decompose(x[a],x[b]);assert np.allclose(component.sum(0),delta,rtol=0,atol=0);dd.append(delta);pp.append(component)
    den=float(delta@delta)
    for pi,part in enumerate(PARTS):
     m=masks[pi];energy=float(component[pi]@component[pi]);idx=np.flatnonzero(m)
     partrows.append(dict(site=site,scale=scale,family=panel[a]['family'],split=panel[a]['split'],fine=fine,part=part,members=len(idx),parent_active=int(active[a].sum()),fine_active=int(active[b].sum()),component_L2=float(np.sqrt(energy)),component_squared_norm=energy,total_difference_L2=float(np.sqrt(den)),squared_norm_share=energy/den if den>tol*tol else None,zero_parent_pre_positive=int(((z[a]==0)&(pre[a]>0)&m).sum()),zero_fine_pre_positive=int(((z[b]==0)&(pre[b]>0)&m).sum())))
     for i in idx:eventrows.append(dict(site=site,scale=scale,family=panel[a]['family'],split=panel[a]['split'],fine=fine,atom=int(i),event=part,parent_z=float(z[a,i]),fine_z=float(z[b,i]),parent_active=bool(active[a,i]),fine_active=bool(active[b,i]),parent_pre=float(pre[a,i]),fine_pre=float(pre[b,i]),decoder_norm=float(dn[i]),difference=float(delta[i])))
    for g,fit in fits.items():
     cp=delta@fit['components'][:2].T;by_coords=coords[g][b]-coords[g][a];assert np.allclose(cp,by_coords,rtol=0,atol=1e-10)
     deltaproj.append(dict(site=site,scale=scale,basis=g,family=panel[a]['family'],split=panel[a]['split'],fine=fine,kind='family_pair',PC1=float(cp[0]),PC2=float(cp[1]),parent_PC1=float(coords[g][a,0]),fine_PC1=float(coords[g][b,0]),parent_PC2=float(coords[g][a,1]),fine_PC2=float(coords[g][b,1])))
   differences[fine]=np.array(dd);parts[fine]=np.array(pp);mu[fine]=np.mean(dd[:3],axis=0);checkmu[fine]=np.mean(dd[3:],axis=0)
   for kind,vec in [('exploration_mean',mu[fine]),('check_mean_descriptive',checkmu[fine])]:
    for g,fit in fits.items():
     cp=vec@fit['components'][:2].T;deltaproj.append(dict(site=site,scale=scale,basis=g,family='MEAN',split='exploration' if kind=='exploration_mean' else 'heldout_check',fine=fine,kind=kind,PC1=float(cp[0]),PC2=float(cp[1]),parent_PC1=None,fine_PC1=None,parent_PC2=None,fine_PC2=None))
  for fi in range(6):
   a=differences['cat'][fi];b=differences['dog'][fi];rec=dict(site=site,scale=scale,family=panel[fi*4]['family'],split=panel[fi*4]['split'],cat_delta_L2=float(np.linalg.norm(a)),dog_delta_L2=float(np.linalg.norm(b)),cat_dog_delta_signed_cosine=signed_cos(a,b,tol),cat_to_exploration_mean_cosine=signed_cos(a,mu['cat'],tol),dog_to_exploration_mean_cosine=signed_cos(b,mu['dog'],tol),cat_length_over_exploration_mean=float(np.linalg.norm(a)/np.linalg.norm(mu['cat'])) if np.linalg.norm(mu['cat'])>tol else None,dog_length_over_exploration_mean=float(np.linalg.norm(b)/np.linalg.norm(mu['dog'])) if np.linalg.norm(mu['dog'])>tol else None)
   pairrows.append(rec)
  payload=dict(family_ids=np.array([f'F{i+1:02d}' for i in range(6)]),delta_cat=differences['cat'],delta_dog=differences['dog'],components_cat=parts['cat'],components_dog=parts['dog'],mean_exploration_cat=mu['cat'],mean_exploration_dog=mu['dog'],mean_check_cat=checkmu['cat'],mean_check_dog=checkmu['dog'])
  np.savez_compressed(R/f'cache/{site}/{scale}/paired_differences.npz',**payload)
  mparts={f:parts[f][:3].mean(0) for f in ['cat','dog']};den=np.linalg.norm(mu['cat'])*np.linalg.norm(mu['dog']);totalcos=signed_cos(mu['cat'],mu['dog'],tol)
  for a,pa in enumerate(PARTS):
   meanparts.append(dict(site=site,scale=scale,part=pa,cat_mean_component_L2=float(np.linalg.norm(mparts['cat'][a])),dog_mean_component_L2=float(np.linalg.norm(mparts['dog'][a])),same_part_signed_cosine=signed_cos(mparts['cat'][a],mparts['dog'][a],tol),note='Mean component supports may overlap across families; do not add their squared norms as disjoint energy.'))
   for b,pb in enumerate(PARTS):dotrows.append(dict(site=site,scale=scale,cat_part=pa,dog_part=pb,dot_product=float(mparts['cat'][a]@mparts['dog'][b]),contribution_to_total_mean_cosine=float(mparts['cat'][a]@mparts['dog'][b]/den) if totalcos is not None else None))
  meansummary.append(dict(site=site,scale=scale,exploration_cat_dog_signed_cosine=totalcos,check_cat_dog_signed_cosine=signed_cos(checkmu['cat'],checkmu['dog'],tol),exploration_cat_L2=float(np.linalg.norm(mu['cat'])),exploration_dog_L2=float(np.linalg.norm(mu['dog'])),check_cat_L2=float(np.linalg.norm(checkmu['cat'])),check_dog_L2=float(np.linalg.norm(checkmu['dog'])),cat_check_mean_to_exploration_mean=signed_cos(checkmu['cat'],mu['cat'],tol),dog_check_mean_to_exploration_mean=signed_cos(checkmu['dog'],mu['dog'],tol)))
  # Fixed counterexample selection affects only displayed cases, never fitted atoms/directions.
  pairs=[p for p in pairrows if p['site']==site and p['scale']==scale];chosen=None
  for rec in pairs[3:]:
   for fine in ['cat','dog']:
    cos=rec[fine+'_to_exploration_mean_cosine']
    if cos is not None and cos<=0:chosen=dict(site=site,scale=scale,family=rec['family'],fine=fine,rule='heldout paired vector nonpositive alignment with exploration mean',value=cos);break
   if chosen:break
  if chosen is None:
   for fi in range(3,6):
    for fine,g in [('cat','AC'),('dog','AD')]:
     mproj=float(mu[fine]@fits[g]['components'][0]);pval=float(differences[fine][fi]@fits[g]['components'][0])
     if abs(mproj)>tol and pval*mproj<0:chosen=dict(site=site,scale=scale,family=f'F{fi+1:02d}',fine=fine,rule='heldout own-group PC1 paired projection reverses exploration mean projection',value=pval,reference=mproj);break
    if chosen:break
  if chosen is None:
   low=min(p['cat_dog_delta_signed_cosine'] for p in pairs[:3] if p['cat_dog_delta_signed_cosine'] is not None)
   for rec in pairs[3:]:
    if rec['cat_dog_delta_signed_cosine'] is not None and rec['cat_dog_delta_signed_cosine']<low:chosen=dict(site=site,scale=scale,family=rec['family'],fine='cat_and_dog',rule='heldout paired cat/dog cosine below exploration minimum',value=rec['cat_dog_delta_signed_cosine'],reference=low);break
  counters.append(chosen or dict(site=site,scale=scale,family='F04',fine='both',rule='NO_COUNTEREXAMPLE_MEETS_PRESET_RULE;show firstcheck descriptively'))
 # Raw member values across ALL24 rows, for exact exploration top5 and original H2 lists.
 selected=sorted({int(r['atom']) for r in top if r['site']==site});extra=set(H2[site]['H2']);allids=sorted(set(selected)|extra)
 for i in allids:
  roles=[f"{r['scale']}:{r['group']}:PC{r['direction']}:rank{r['loading_rank']}" for r in top if r['site']==site and int(r['atom'])==i]
  if i in extra:roles.append('original_S03_H2')
  for j,p in enumerate(panel):membervals.append(dict(site=site,atom=i,id=p['id'],family=p['family'],split=p['split'],condition=p['condition'],z=float(z[j,i]),decoder_norm=float(dn[i]),u=float(z[j,i]*dn[i]),Top32=bool(i in source[site+'__topk_indices'][j]),active=bool(z[j,i]>0),preactivation=float(pre[j,i]),roles=';'.join(roles)))
 zeroaudit.append(dict(site=site,decoder_norm_min=float(dn.min()),decoder_norm_max=float(dn.max()),max_abs_decoder_norm_minus1=float(abs(dn-1).max()),rows=24,all_positive_counts=active.sum(1).tolist()))
table(R/'results/projections_all24.csv',projrows);table(R/'results/class_spread_frozen_coordinates.csv',classrows);table(R/'results/paired_differences_summary.csv',pairrows);table(R/'results/paired_projections_both_bases.csv',deltaproj);table(R/'results/difference_member_events.csv',eventrows);table(R/'results/difference_decomposition.csv',partrows);table(R/'results/mean_difference_cross_parts.csv',dotrows);table(R/'results/mean_difference_component_norms.csv',meanparts);table(R/'results/SVD_between_within_family.csv',varrows);table(R/'results/selected_member_all24_values.csv',membervals);table(R/'results/mean_difference_summary.csv',meansummary);jsonl(R/'results/counterexamples.jsonl',counters);dump(R/'results/scale_identity.json',zeroaudit)
dump(R/'evidence/analysis_complete.json',dict(UTC=now(),projected_rows=len(projrows),paired_differences=len(pairrows),paired_projections=len(deltaproj),member_values=len(membervals),decomposition_rows=len(partrows),mean_cross_dot_rows=len(dotrows),basis_freeze_SHA256=sha(R/'evidence/bases_frozen_before_check.json'),heldout_refits=0,check_selected_atoms=0,model_forwards=0,training=0,intervention=0,next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW'))
print('S05_ANALYSIS_COMPLETE',json.dumps(meansummary),json.dumps(counters),flush=True)
