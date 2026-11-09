"""A01 method audit: retain v1 and add tighter occurrence/support matched references."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,numpy as np,datetime,hashlib,argparse,csv,shutil
from scipy import sparse
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'));args=parser.parse_args();O=args.output;A=O/'analysis';T=O/'tables'
f=json.loads((O/'freeze.json').read_text());groups={g:np.array(f['sets']['main_'+g]) for g in ['math','biology']};x=np.load(A/'discovery_metrics.npz');sm=x['support_math'];sb=x['support_biology'];eligible=x['support'];P=np.load(A/'all_decoder_projection.npz')['per_pc'];M=np.r_[groups['math'],groups['biology']];F=len(P)
screen=list(csv.DictReader((T/'all_dictionary_screen.csv').open()));rate=np.array([float(r['DCLM_feature_occurrence']) for r in screen]);hits=np.rint(rate*65536).astype(int)
config={'revision':'R10-A01','reason':'method audit: original three occurrence classes are too broad for close matching, especially the high class','timing':'after v1 results; explicit offline method correction, not a preregistered confirmation','seed':2026103005,'reps':1000,'strata':'floor(2*log2(DCLM hits)), floor(total positive discovery documents/5), floor(max domain positive documents/5); zero hits separate','pool':'entire support eligible dictionary INCLUDING main; preserve exact per-stratum counts, same group sizes, no replacement, groups disjoint','occurrence_ratio_within_positive_stratum_max':float(np.sqrt(2)),'support_total_max_difference':4,'support_maxdomain_max_difference':4,'frozen_main_sha256':hashlib.sha256((O/'freeze.json').read_bytes()).hexdigest()}
cp=O/'fine_background_config.json'
if cp.exists():assert json.loads(cp.read_text())==config
else:cp.write_text(json.dumps(config,indent=2)+'\n')
rng=np.random.default_rng(config['seed']);loghits=np.where(hits>0,np.floor(2*np.log2(np.maximum(hits,1))).astype(int),-1);keys=list(zip(loghits,(sm+sb)//5,np.maximum(sm,sb)//5));keyidx={k:i for i,k in enumerate(sorted(set(keys)))};strata=np.array([keyidx[k] for k in keys]);pool=np.flatnonzero(eligible);draw={g:np.empty((1000,len(ids)),np.int32) for g,ids in groups.items()};checks=0;records=[]
for st in np.unique(strata[M]):
 candidates=pool[strata[pool]==st];loc={g:np.flatnonzero(strata[ids]==st) for g,ids in groups.items()};nm,nb=len(loc['math']),len(loc['biology']);assert len(candidates)>=nm+nb
 for b in range(1000):
  picked=rng.choice(candidates,nm+nb,replace=False);draw['math'][b,loc['math']]=picked[:nm];draw['biology'][b,loc['biology']]=picked[nm:]
 h=hits[candidates];pos=h[h>0];assert len(pos)==0 or pos.max()/pos.min()<=np.sqrt(2)+1e-12
 records.append(dict(stratum=int(st),log2_half_octave=int(loghits[candidates[0]]),total_docs_bin=int((sm[candidates[0]]+sb[candidates[0]])//5),max_domain_docs_bin=int(max(sm[candidates[0]],sb[candidates[0]])//5),pool=len(candidates),math=nm,biology=nb,hits_min=int(h.min()),hits_max=int(h.max())))
bg={};selected=np.zeros(F,bool);selected[M]=True
for g,ids in groups.items():
 for b in range(1000):
  assert len(set(draw[g][b]))==len(ids);assert np.array_equal(np.bincount(strata[draw[g][b]],minlength=len(keyidx)),np.bincount(strata[ids],minlength=len(keyidx)));checks+=1
 rr=np.repeat(np.arange(1000),len(ids));w=sparse.csr_matrix((np.full(draw[g].size,1/len(ids)),(rr,draw[g].ravel())),shape=(1000,F));bg[g]=w@P
 np.savez_compressed(A/f'{g}_fine_matched_background.npz',feature_ids=draw[g],mean_per_pc=bg[g],selected_inclusion_fraction=selected[draw[g]].mean(1))
for b in range(1000):assert not (set(draw['math'][b])&set(draw['biology'][b]));checks+=1
with (T/'fine_matched_strata.csv').open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
for name in ['geometry.json','results.json']:
 old=A/(name.replace('.json','_v1_coarse_reference.json'))
 if not old.exists():shutil.copy2(A/name,old)
geo=json.loads((A/'geometry_v1_coarse_reference.json').read_text());original=json.loads((A/'results_v1_coarse_reference.json').read_text())
def interval(x):return np.quantile(x,[.025,.975],axis=0).tolist()
def band(x):return x.reshape(-1,16,64).sum(2)
geo['overlap_pc_bg95']=interval(np.minimum(bg['math'],bg['biology']).sum(1));geo['overlap_band_bg95']=interval(np.minimum(band(bg['math']),band(bg['biology'])).sum(1));geo['PC2_64_bg95']=interval(np.minimum(bg['math'][:,1:64]/bg['math'][:,1:64].sum(1,keepdims=True),bg['biology'][:,1:64]/bg['biology'][:,1:64].sum(1,keepdims=True)).sum(1))
for g in groups:
 geo['groups'][g]['head_background95']=interval(bg[g][:,:64].sum(1));geo['groups'][g]['PC1_background95']=interval(bg[g][:,0]);geo['groups'][g]['PC2_64_background95']=interval(bg[g][:,1:64].sum(1));geo['groups'][g]['background_selected_inclusion_mean']=float(selected[draw[g]].mean())
geo['background_method']='A01 finer occurrence/support matching; v1 coarse reference preserved separately';original['geometry']=geo
(A/'geometry.json').write_text(json.dumps(geo,indent=2)+'\n');(A/'results.json').write_text(json.dumps(original,indent=2)+'\n')
audit={'revision':'R10-A01','checks_passed':checks,'strata':len(records),'same_frozen_main':True,'main_freeze_sha256':config['frozen_main_sha256'],'scientific_thresholds_changed':False,'new_forwards':0,'all_results_v1_preserved':True,'reference_ranges':{g:geo['groups'][g] for g in groups},'overlap_pc_bg95':geo['overlap_pc_bg95'],'timing':'offline method audit after original v1 outputs; descriptive robustness only'}
(A/'fine_background_audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))

# The same fixed reference rule for all pre-frozen rank / threshold sensitivity sets.
sensrows=[]
for prefix in ['main','top16','top64','top128','auc0.70','auc0.80']:
 ids={g:np.array(f['sets'][prefix+'_'+g]) for g in groups}
 if prefix=='main':means=bg
 else:
  ds={g:np.empty((1000,len(ids[g])),np.int32) for g in groups}
  for st in np.unique(strata[np.r_[ids['math'],ids['biology']]]):
   candidates=pool[strata[pool]==st];loc={g:np.flatnonzero(strata[ids[g]]==st) for g in groups};nm,nb=len(loc['math']),len(loc['biology']);assert nm+nb<=len(candidates)
   for b in range(1000):
    pick=rng.choice(candidates,nm+nb,replace=False);ds['math'][b,loc['math']]=pick[:nm];ds['biology'][b,loc['biology']]=pick[nm:]
  means={}
  for g in groups:
   rr=np.repeat(np.arange(1000),len(ids[g]));w=sparse.csr_matrix((np.full(ds[g].size,1/len(ids[g])),(rr,ds[g].ravel())),shape=(1000,F));means[g]=w@P
   np.savez_compressed(A/f'{prefix}_{g}_fine_matched_ids.npz',feature_ids=ds[g])
 ov=np.minimum(P[ids['math']].mean(0),P[ids['biology']].mean(0)).sum();ovref=np.minimum(means['math'],means['biology']).sum(1);olo,ohi=interval(ovref)
 for g in groups:
  observed=float(P[ids[g],:64].sum(1).mean());lo,hi=interval(means[g][:,:64].sum(1));sensrows.append(dict(selection=prefix,domain_bias=g,members=len(ids[g]),head_mean=observed,head_matched_low=lo,head_matched_high=hi,head_above_reference95=bool(observed>hi),overlap_pc=float(ov),overlap_matched_low=olo,overlap_matched_high=ohi,overlap_above_reference95=bool(ov>ohi)))
with (T/'fine_matched_sensitivity.csv').open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(sensrows[0]));w.writeheader();w.writerows(sensrows)
print('SENSITIVITY',json.dumps(sensrows))
