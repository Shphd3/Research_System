import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import numpy as np,json,pandas as pd
E=Path(__file__).resolve().parents[1]
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines() if l]
def main():
 r=rows(E/'data/prefixes.jsonl');F=rows(E/'data/families.jsonl');B=np.load(E/'data/bases.npz');V=B['V'];H=np.load(E/'cache/merged.npz');vs=np.load(E/'cache/vectors.npz');ref=np.load(E/'data/reference_frequency.npz');decoder=np.load(E/'data/decoder_last_scale.npz');D=decoder['D'];groups=json.load(open(E/'data/feature_groups.json'));bounds=[0,1,16,64,128,256,512,768,1024];first=[q['candidate_map']['U']['position_indices'][0] for q in r];spec=[];cross=[];feature=[];representatives=[];counterexample_status=[];groupnames=['low','middle','high','insufficient_positive','zero_reference'];scores={g:vs[g][first].astype(np.float64)@V for g in groupnames}
 for g in groupnames:
  gs=scores[g];gnorm=np.sum(gs**2,1)
  for i,q in enumerate(r):
   for b,(l,h) in enumerate(zip(bounds[:-1],bounds[1:]),1):
    energy=float(np.sum(gs[i,l:h]**2));spec.append({'prefix_id':q['prefix_id'],'family_id':q['family_id'],'domain':q['domain'],'split':q['split'],'paraphrase_id':q['paraphrase_id'],'context_type':q['context_type'],'group':g,'band':f'B{b}','left':l,'right':h,'squared_projection_norm':energy,'group_squared_norm':gnorm[i],'fraction_of_group_vector':energy/gnorm[i] if gnorm[i]>0 else np.nan})
 for i,q in enumerate(r):
  for ai,a in enumerate(groupnames):
   for bb in groupnames[ai+1:]:
    for b,(l,h) in enumerate(zip(bounds[:-1],bounds[1:]),1):cross.append({'prefix_id':q['prefix_id'],'family_id':q['family_id'],'group_a':a,'group_b':bb,'band':f'B{b}','cross_term_2dot':float(2*np.dot(scores[a][i,l:h],scores[bb][i,l:h]))})
 pd.DataFrame(spec).to_csv(E/'analysis/group_spectral_contributions.csv.gz',index=False,compression='gzip');pd.DataFrame(cross).to_csv(E/'analysis/group_spectral_cross_terms.csv.gz',index=False,compression='gzip')
 # Whole-family actual activation support, independent reference frequencies kept separate.
 z=H['z'];nz=(z>0).sum(0);l2=np.linalg.norm(D.astype(np.float64),axis=1)
 for j in range(16384):feature.append({'feature_number':j,'reference_hits':int(ref['hits'][j]),'reference_positions':65536,'reference_frequency':float(ref['rate'][j]),'reference_group':int(ref['group'][j]),'task_scoring_position_hits':int(nz[j]),'task_scoring_positions':len(z),'task_mean_coefficient':float(z[:,j].mean()),'raw_last_decoder_norm':l2[j]})
 pd.DataFrame(feature).to_csv(E/'analysis/all_feature_support.csv',index=False)
 supports=[]
 for domain in ['biology','mathematics','physics']:
  selected=[(i,q) for i,q in enumerate(r) if q['split']=='evaluation' and q['domain']==domain];ii=[first[i] for i,q in selected]
  for group in ['low','middle','high','insufficient_positive','zero_reference']:
   members=groups[group];zz=z[np.array(ii)[:,None],np.array(members)[None,:]];positive=zz>0;active=positive.any(1);families_positive=len({q['family_id'] for (i,q),fired in zip(selected,active) if fired});v=vs[group][ii]
   supports.append({'domain':domain,'group':group,'members':len(members),'evaluation_families':12,'positive_families':families_positive,'first_answer_positions':len(ii),'nonzero_first_positions':int(active.sum()),'activation_instances':int(positive.sum()),'mean_active_members_per_position':float(positive.sum(1).mean()),'conditional_positive_coefficient_mean':float(zz[positive].mean()) if positive.any() else None,'mean_actual_group_vector_norm':float(np.linalg.norm(v,axis=1).mean())})
 pd.DataFrame(supports).to_csv(E/'analysis/evaluation_first_position_group_support.csv',index=False)
 fixed=json.load(open(E/'config.json'))['fixed_families'];zc=z[first]
 for fid in fixed:
  rr=[(i,q) for i,q in enumerate(r) if q['family_id']==fid]
  za=np.array([zc[i] for i,q in rr if q['context_type']=='A']);zb=np.array([zc[i] for i,q in rr if q['context_type']=='B']);contrast=np.mean(abs(za-zb),0)*l2;pooled=np.mean((za+zb)/2,0)
  for g in ['low','middle','high']:
   members=np.array(groups[g]);order=np.lexsort((members,-contrast[members]));chosen=members[order[:2]].tolist();median=float(np.median(contrast[members]));neg=members[(contrast[members]<=median)&(pooled[members]>0)];counterexample_status.append({'family_id':fid,'group':g,'predeclared_absolute_difference_limit':median,'eligible_nonzero_members':len(neg),'status':'AVAILABLE' if len(neg) else 'NOT_FOUND_NO_NONZERO_RESPONSE_UNDER_ORIGINAL_RULE'});
   if len(neg):negative=int(neg[np.lexsort((neg,-pooled[neg]))[0]]);chosen.append(negative)
   for j in chosen:
    for i,q in rr:representatives.append({'family_id':fid,'prefix_id':q['prefix_id'],'domain':q['domain'],'context_type':q['context_type'],'paraphrase_id':q['paraphrase_id'],'group':g,'feature_number':j,'coefficient':float(zc[i,j]),'activated':bool(zc[i,j]>0),'reference_hits':int(ref['hits'][j]),'reference_frequency':float(ref['rate'][j]),'absolute_cue_response_vector_difference':float(contrast[j]),'selection':'largest_cue_difference_top2' if j in chosen[:2] else 'high_response_small_difference_counterexample'})
 pd.DataFrame(representatives).to_csv(E/'analysis/representative_member_responses.csv',index=False)
 (E/'analysis/member_counterexample_eligibility.json').write_text(json.dumps(counterexample_status,indent=2)+'\n')
 # Compare intended norm control to actual BF16 displacement across EVERY scoring position.
 norms=[];conditions=json.load(open(E/'data/conditions.json'))['unique']
 for c in conditions:
  if c['kind'] not in ['feature_normmatch','spectral_normmatch']:continue
  target=f'feature_delete_{c["target_group"]}' if c['kind']=='feature_normmatch' else c['target'];a=np.load(E/'analysis'/f'condition_{c["condition"]}.npz');b=np.load(E/'analysis'/f'condition_{target}.npz');intended=a['perturbation_norm'];itarget=b['perturbation_norm'];applied=a['applied_perturbation_norm'];actualtarget=b['applied_perturbation_norm'];valid=actualtarget>0
  norms.append({'condition':c['condition'],'target':target,'positions':len(applied),'intended_norm_max_abs_difference':float(abs(intended-itarget).max()),'actual_relative_norm_difference_mean':float(np.mean(abs(applied[valid]-actualtarget[valid])/actualtarget[valid])) if valid.any() else 0.,'actual_relative_norm_difference_max':float(np.max(abs(applied[valid]-actualtarget[valid])/actualtarget[valid])) if valid.any() else 0.,'target_actual_zero_positions':int((~valid).sum()),'control_actual_zero_positions':int((applied==0).sum()),'target_intended_nonzero_but_actual_zero':int(((itarget>0)&(~valid)).sum())})
 pd.DataFrame(norms).to_csv(E/'analysis/applied_norm_matching_audit.csv',index=False)
 print('SPECTRUM_AND_MEMBERS',len(spec),len(cross),len(representatives))
if __name__=='__main__':main()
