from pathlib import Path
import json,numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];V=E/'versions/data_v1p2'
def main():
 R=[json.loads(l) for l in (V/'data/prefixes.jsonl').read_text().splitlines()];conditions=json.load(open(E/'data/conditions.json'));old={};summary=[];current=pd.read_csv(E/'analysis/family_metrics.csv');curS=pd.read_csv(E/'analysis/summary.csv');domains=['biology','mathematics','physics']
 for c in conditions['unique']:
  name=c['condition'];a=np.load(V/'analysis'/f'condition_{name}.npz')['logp'];raw={}
  for r in R:
   if r['split']!='evaluation':continue
   p={}
   for j,k in enumerate(['U','V','A','B']):
    ii=np.array(r['candidate_map'][k]['position_indices']);col=np.zeros(len(ii),int);col[0]=j;p[k]=float(a[ii,col].sum(dtype=np.float64))
   raw[r['prefix_id']]={'r':p['A']-p['B'],'u':p['U']-p['V']}
  fam={}
  for fid in sorted({r['family_id'] for r in R if r['split']=='evaluation'}):
   rr=[]
   for pi in [0,1]:
    A=raw[f'{fid}_p{pi}_A'];B=raw[f'{fid}_p{pi}_B'];b=raw[f'{fid}_p{pi}_broad'];rr.append({'J':(A['r']-B['r'])/2,'specific_correct':(int(A['r']>0)+int(B['r']<0))/2,'upper_correct':sum(int(x['u']>0) for x in [A,B,b])/3})
   fam[fid]={k:float(np.mean([r[k] for r in rr])) for k in rr[0]}
  old[name]=fam
  for domain in domains+['overall_equal_domains']:
   ids=[f for f in fam if domain=='overall_equal_domains' or f.startswith(domain+'_')];s=curS[(curS.condition==name)&(curS.domain==domain)].iloc[0]
   for m in ['J','specific_correct','upper_correct']:
    before=np.mean([fam[f][m] for f in ids]);summary.append({'condition':name,'domain':domain,'metric':m,'data1p2':before,'data1p3':float(s[m]),'correction_difference':float(s[m])-before,'eligibility':'version1.2 had literal-U exposure;not an independent replication'})
 pd.DataFrame(summary).to_csv(E/'analysis/data_correction_impact.csv',index=False)
 # Show whether the predeclared primary matched comparisons change with the data repair.
 draws=np.load(E/'analysis/bootstrap_family_draws.npz');comp=[]
 for group in ['low','middle','high']:
  for typ in ['same_count','norm_matched']:
   controls=[f'feature_delete_random_{group}_{se}' if typ=='same_count' else f'feature_normmatch_{group}_{se}' for se in [11021,11022,11023]];target='feature_delete_'+group;bs=[];means=[]
   for d in domains:
    ids=sorted(f for f in old['full'] if f.startswith(d+'_'));x=np.array([np.mean([old[c][f]['J'] for c in controls])-old[target][f]['J'] for f in ids]);means.append(x.mean());bs.append(x[draws[d]].mean(1))
   b=np.mean(bs,axis=0);comp.append({'group':group,'control_type':typ,'data1p2_excess_J_loss':np.mean(means),'data1p2_low_simultaneous6':np.quantile(b,.05/12),'data1p2_high_simultaneous6':np.quantile(b,1-.05/12)})
 currentC=pd.read_csv(E/'analysis/primary_feature_contrasts.csv');m=currentC[currentC.domain=='overall_equal_domains'].merge(pd.DataFrame(comp),on=['group','control_type']);m.to_csv(E/'analysis/data_correction_primary_impact.csv',index=False)
 # Exact unchanged-state/output assertions across the versioned cache reuse.
 patch=json.load(open(E/'audit/upper_name_correction_patch.json'));ix=np.array(patch['affected_position_indices']);keep=np.ones(2640,bool);keep[ix]=False;oldm=np.load(V/'cache/merged.npz');newm=np.load(E/'cache/merged.npz');result={'unchanged_positions':int(keep.sum()),'same_h':bool(np.array_equal(oldm['h'][keep],newm['h'][keep])),'same_z':bool(np.array_equal(oldm['z'][keep],newm['z'][keep])),'all_unchanged_condition_logprobs_exact':True,'max_untouched_score_error':0.}
 for c in conditions['unique']:
  n=c['condition'];a=np.load(V/'analysis'/f'condition_{n}.npz')['logp'];b=np.load(E/'analysis'/f'condition_{n}.npz')['logp'];err=float(abs(a[keep]-b[keep]).max());result['max_untouched_score_error']=max(result['max_untouched_score_error'],err)
 result['all_unchanged_condition_logprobs_exact']=result['max_untouched_score_error']==0
 (E/'audit/correction_reuse_validation.json').write_text(json.dumps(result,indent=2)+'\n');assert result['same_h'] and result['same_z'] and result['all_unchanged_condition_logprobs_exact'];print(m[['group','control_type','data1p2_excess_J_loss','excess_J_loss']].to_string(index=False))
if __name__=='__main__':main()
