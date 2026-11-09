from pathlib import Path
import sys,json
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));B=cfg['bands'];P=dict(np.load(E/'analysis/pca.npz'));G=dict(np.load(E/'analysis/head_geometry.npz'));V=151936
out=[]
for name in ['h','y']:
 ev=P[name+'_eigenvalues']
 for i,(a,b) in enumerate(B):out.append({'coordinates':name,'band':i,'start0':a,'end0_exclusive':b,'dimensions':b-a,'dimension_fraction':(b-a)/1024,'retained_variance':ev[a:b].sum()/ev.sum(),'mean_eigenvalue':ev[a:b].mean(),'min_eigenvalue':ev[a:b].min(),'max_eigenvalue':ev[a:b].max()})
pd.DataFrame(out).to_csv(E/'analysis/spectra_bands.csv',index=False)
U=P['y_V'];head=G['U'];gain=np.sqrt(np.maximum(np.einsum('ij,ij->j',U,G['Gc']@U),0)/V);rawgain=np.sqrt(np.maximum(np.einsum('ij,ij->j',U,G['G']@U),0)/V);isotropic=float(np.sqrt(np.trace(G['Gc'])/V/1024))
pd.DataFrame({'PC_index0':np.arange(1024),'postnorm_variance':P['y_eigenvalues'],'postnorm_PC_centered_logit_gain':gain,'postnorm_PC_raw_logit_gain':rawgain,'relative_to_isotropic_gain':gain/isotropic,'head_centered_singular_value':np.sqrt(np.maximum(G['eigenvalues'],0)),'head_raw_singular_value':np.sqrt(np.maximum(G['raw_eigenvalues'],0)),'h_eigenvalue':P['h_eigenvalues'],'y_eigenvalue':P['y_eigenvalues']}).to_csv(E/'analysis/representation_head_spectra.csv',index=False)
over=[]
for b,(a,end) in enumerate(B):
 for k in [16,64,256,end-a]:
  over.append({'representation_coordinates':'postnorm_y','representation_band':b,'band_dimensions':end-a,'head_right_top_dimensions':k,'overlap_per_representation_dimension':float(np.sum((U[:,a:end].T@head[:,:k])**2)/(end-a)),'random_expectation':k/1024})
pd.DataFrame(over).drop_duplicates().to_csv(E/'analysis/representation_head_subspace_overlap.csv',index=False)

readout=[];power=P['y_eigenvalues']*gain**2
for b,(a,end) in enumerate(B):readout.append({'coordinates':'postnorm_y','band':b,'dimensions':end-a,'representation_variance_fraction':float(P['y_eigenvalues'][a:end].sum()/P['y_eigenvalues'].sum()),'variance_weighted_centered_logit_variance_fraction':float(power[a:end].sum()/power.sum()),'mean_unit_direction_gain':float(gain[a:end].mean()),'mean_gain_over_isotropic':float((gain[a:end]/isotropic).mean()),'not_a_language_phenomenon_claim':True})
pd.DataFrame(readout).to_csv(E/'analysis/postnorm_band_readout_geometry.csv',index=False)

json.dump({'head_vocab_rows':V,'isotropic_centered_logit_RMS_per_unit_delta_y':isotropic,'uniform_shift_removed_Gram_trace_fraction':float((np.trace(G['G'])-np.trace(G['Gc']))/np.trace(G['G'])),'postnorm_PC_gain_min':float(gain.min()),'postnorm_PC_gain_max':float(gain.max()),'gain_is_not_accuracy_or_semantic_importance':True},open(E/'analysis/head_gain_reference.json','w'),indent=2)

old=np.load(E/'data/historical_math_bio_basis.npz');oldV=old['V'];inner=P['h_V'].T@oldV;old_var=np.sum(inner**2*P['h_eigenvalues'][:,None],axis=0);old_rows=[]
for k in [16,64,128,256,512]:
 old_rows.append({'dimensions':k,'basis_old_origin':'R04 60math/bio9600positions;notbroadnatural-languagebasis','old_basis_new_discovery_variance_fraction':float(old_var[:k].sum()/P['h_eigenvalues'].sum()),'new_basis_discovery_variance_fraction':float(P['h_eigenvalues'][:k].sum()/P['h_eigenvalues'].sum()),'old_new_head_subspace_overlap_per_dim':float(np.sum((oldV[:,:k].T@P['h_V'][:,:k])**2)/k)})
pd.DataFrame(old_rows).to_csv(E/'analysis/historical_basis_comparison.csv',index=False)

# Three different views: decoder direction, actual coefficient-scaled use, actual matched h/y changes.
if (E/'validation_selection_frozen.json').exists() and (E/'analysis/validation_matched_positions.csv').exists():
 F=json.load(open(E/'validation_selection_frozen.json'));docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];D=np.load(E/'data/selected_decoder.npy');feat=cfg['candidate_features'];pairs=pd.read_csv(E/'analysis/validation_matched_positions.csv');meta={d['doc_id']:d for d in docs};rows=[];ledger=[];examples=[]
 for c in F['selected_explanations']:
  f=int(c['response'].split('_')[1]);j=feat.index(f);d=D[j].astype(np.float64);pd_=d@P['h_V'];den=d@d
  for b,(a,end) in enumerate(B):rows.append({'phenomenon':c['phenomenon'],'feature':f,'view':'decoder_direction_only','doc_id':'GLOBAL_FIXED_DECODER','band':b,'energy':float(np.sum(pd_[a:end]**2)),'fraction':float(np.sum(pd_[a:end]**2)/den),'coefficient_difference':None})
  for doc_id,q in pairs[pairs.phenomenon==c['phenomenon']].groupby('doc_id'):
   doc=meta[doc_id];cache=np.load(E/'cache'/(doc_id+'.npz'));ip=q.positive_row.to_numpy()-doc['row_start'];im=q.negative_row.to_numpy()-doc['row_start'];zp=cache['z_selected'][ip,j];zm=cache['z_selected'][im,j];vz=zp[:,None]*d;dv=(zp-zm)[:,None]*d;vp=vz@P['h_V'];dp=dv@P['h_V'];dh=cache['h'][ip].astype(np.float64)-cache['h'][im].astype(np.float64);dr=cache['reconstruction'][ip].astype(np.float64)-cache['reconstruction'][im].astype(np.float64);res=dh-dr
   for view,v,proj,zd in [('actual_positive_zD',vz,vp,zp),('actual_matched_delta_zD',dv,dp,zp-zm)]:
    norm=np.sum(v**2,1);nonzero=norm>0
    for b,(a,end) in enumerate(B):rows.append({'phenomenon':c['phenomenon'],'feature':f,'view':view,'doc_id':doc_id,'band':b,'energy':float(np.mean(np.sum(proj[:,a:end]**2,1))),'fraction':float(np.mean(np.sum(proj[nonzero,a:end]**2,1)/norm[nonzero])) if nonzero.any() else None,'coefficient_difference':float(np.mean(zd)),'nonzero_positions':int(nonzero.sum()),'pairs':len(ip)})
   # Exact identity dh=one selected contribution+(rest of reconstruction)+(original residual).
   other=dr-dv;ener=[np.sum(v**2,1) for v in [dv,other,res]];cross=2*np.sum(dv*other+dv*res+other*res,1);total=np.sum(dh**2,1);ledger.append({'phenomenon':c['phenomenon'],'feature':f,'doc_id':doc_id,'mean_delta_h_squared':float(total.mean()),'selected_feature_squared':float(ener[0].mean()),'other_dictionary_squared':float(ener[1].mean()),'original_residual_squared':float(ener[2].mean()),'all_cross_terms':float(cross.mean()),'identity_abs_error':float(np.max(abs(total-(ener[0]+ener[1]+ener[2]+cross))))})
 pd.DataFrame(rows).to_csv(E/'analysis/three_feature_geometry_views.csv',index=False);pd.DataFrame(ledger).to_csv(E/'analysis/nonadditive_residual_ledger.csv',index=False)
print('GEOMETRY_COMPLETE',isotropic,float(gain.min()),float(gain.max()),flush=True)
