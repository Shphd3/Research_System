from pathlib import Path
import json,hashlib,itertools,datetime
import numpy as np,pandas as pd
from scipy.sparse import load_npz
R=Path(__file__).resolve().parent;ROOT=R.parent;S06=ROOT/'S06_semantic_hierarchy_1104';S08=ROOT/'S08_dataset_support_overlap_1104';S09=ROOT/'S09_marginal_vs_joint_1104'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
panel=[json.loads(l) for l in open(S06/'data/panel.jsonl')];lookup={p['id']:i for i,p in enumerate(panel)};families=[f'F{i:02d}' for i in range(9,17)];summary=[];frows=[];checks=[];seed=20261104;B=20000;choice=np.random.default_rng(seed).integers(0,8,(B,8));effects=pd.read_csv(S06/'results/family_effects.csv');orig=json.load(open(S06/'results/primary.json'));csr={}
for site in ['ATTN_SAE','MLPIN_SAE']:
 z=load_npz(S06/'data'/f'{site}_all_z_csr.npz');csr[site]=z;vals=[]
 def support(i):return set(int(j) for j in z.getrow(i).indices[z.getrow(i).data>0])
 for fam in families:
  aa=[lookup[f'S06_{fam}_explicit_{label}'] for label in ['animal','cat','dog']];bb=[lookup[f'S06_{fam}_explicit_{label}'] for label in ['vehicle','car','bicycle']]
  jac=lambda a,b:len(support(a)&support(b))/len(support(a)|support(b));va=np.mean([jac(a,b) for a,b in itertools.combinations(aa,2)]);vb=np.mean([jac(a,b) for a,b in itertools.combinations(bb,2)]);vc=np.mean([jac(a,b) for a in aa for b in bb]);vals.append([va,vb,vc]);frows.append(dict(site=site,family=fam,animal_within=va,vehicle_within=vb,cross=vc,animal_pairs=3,vehicle_pairs=3,cross_pairs=9))
  for domain,v in [('animal',va),('vehicle',vb)]:
   q=effects[(effects.site==site)&(effects.family==fam)&(effects.hypothesis=='H1')&(effects.wording=='explicit')&(effects.domain==domain)].iloc[0];assert abs(v-q['within'])<1e-12;assert abs(vc-q['cross'])<1e-12
 v=np.array(vals);boot=v[choice].mean(1);ci=np.quantile(boot,[.025,.975],axis=0)
 expected={'ATTN_SAE':[.525,.438,.304],'MLPIN_SAE':[.667,.639,.479]}[site]
 for j,(label,Chinese) in enumerate([('animal_within','动物类内'),('vehicle_within','交通工具类内'),('cross','跨大类')]):
  mean=float(v[:,j].mean());assert round(mean,3)==expected[j];summary.append(dict(site=site,comparison=label,label_cn=Chinese,mean=mean,display=f'{mean:.3f}',CI_lo=float(ci[0,j]),CI_hi=float(ci[1,j]),N_families=8,bootstrap_reps=B,seed=seed,CI_origin='New presentation-only percentile bootstrap of original eight family-level means; not original within-minus-cross interval'))
 checks.append(dict(site=site,means=v.mean(0).tolist(),original_difference_CIs=[r for r in orig if r['site']==site and r['hypothesis']=='H1']))
pd.DataFrame(summary).to_csv(R/'data/figure1_means_and_family_CI.csv',index=False);pd.DataFrame(frows).to_csv(R/'data/figure1_family_values.csv',index=False)
# Original F09 coordinates, exactly the two actual tokenized prefixes.
pa=panel[lookup['S06_F09_explicit_animal']];pc=panel[lookup['S06_F09_explicit_cat']];z=csr['ATTN_SAE'];ia=lookup[pa['id']];ic=lookup[pc['id']];a={int(i):float(v) for i,v in zip(z.getrow(ia).indices,z.getrow(ia).data) if v>0};c={int(i):float(v) for i,v in zip(z.getrow(ic).indices,z.getrow(ic).data) if v>0};shared=sorted(a.keys()&c.keys());lost=sorted(a.keys()-c.keys());gained=sorted(c.keys()-a.keys());assert (len(a),len(c),len(shared),len(lost),len(gained))==(32,32,24,8,8)
assert pa['category_phrase']=='an animal' and pc['category_phrase']=='a cat';assert pa['target_index_zero_based']==pc['target_index_zero_based']==22;assert pa['target_token_id']==pc['target_token_id']==25;changes=[i for i,(x,y) in enumerate(zip(pa['token_ids'],pc['token_ids'])) if x!=y];assert changes==[13,14]
active=pd.read_csv(S06/'results/active_values.csv');assert set(active[(active.site=='ATTN_SAE')&(active.id==pa['id'])].feature_id)==set(a);assert set(active[(active.site=='ATTN_SAE')&(active.id==pc['id'])].feature_id)==set(c)
rows=[]
for col,f in enumerate(shared+lost+gained,1):rows.append(dict(column=col,feature_id=f,status='shared' if f in shared else 'animal_only' if f in lost else 'cat_only',animal_active=int(f in a),cat_active=int(f in c),animal_z=a.get(f,0.),cat_z=c.get(f,0.)))
pd.DataFrame(rows).to_csv(R/'data/figure2_F09_members.csv',index=False)
dump(R/'data/figure2_F09_text_and_position.json',dict(animal={k:pa[k] for k in ['id','text','prefix','category_phrase','token_ids','token_pieces','target_index_zero_based','target_token_id']},cat={k:pc[k] for k in ['id','text','prefix','category_phrase','token_ids','token_pieces','target_index_zero_based','target_token_id']},shared_ids=shared,lost_ids=lost,gained_ids=gained,changed_token_positions_zero_based=changes,reading_token='Final colon in Description:',sample_scope='F09 explicit heldout, ATTN_SAE at block27o_proj output',Jaccard=24/40))
# Source-level supplement, original S08 full257documents/source; S09 separate128/129split.
s8=pd.read_csv(S08/'tables/overlap_summary.csv');natural=s8[s8['mode']=='main'][['site','A','B','N_A','N_B','within_A','within_B','cross','A_minus_cross_lo','B_minus_cross_lo','holm_primary']].copy();assert len(natural)==6;assert (natural.A_minus_cross_lo>0).all() and (natural.B_minus_cross_lo>0).all();natural.to_csv(R/'data/natural_sources_S08_summary.csv',index=False)
s9=pd.read_csv(S09/'tables/A_overlap_references.csv');gap=s9[s9.comparison=='pooled_gap'].copy();gap[['site','A','B','N_discovery','N_heldout','real_J','heldout_fixed32_margin_J','fixed32_gap_reproduction_ratio','real_minus_fixed32_CI_lo','real_minus_fixed32_CI_hi']].to_csv(R/'data/natural_sources_S09_null_context.csv',index=False)
# Pin all decisive inputs, preserving scientific records.
inputs=[S06/'data/panel.jsonl',S06/'data/ATTN_SAE_all_z_csr.npz',S06/'data/MLPIN_SAE_all_z_csr.npz',S06/'results/family_effects.csv',S06/'results/active_values.csv',S06/'results/primary.json',S08/'tables/overlap_summary.csv',S09/'tables/A_overlap_references.csv',S09/'summary_cn.md']
dump(R/'evidence/data_verification.json',dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',six_rounded_means_match_user=True,original_8family_means_independently_recomputed_from_sparse_sets=True,F09_support_counts=[32,32,24,8,8],F09_changed_token_positions_zero_based=changes,no_single_token_change_claim=True,original_difference_CIs_not_used_as_bar_CIs=True,original_statistics_not_modified=True,input_files=[dict(path=str(p),sha256=sha(p)) for p in inputs],summary_checks=checks,bootstrap=dict(seed=seed,resamples=B,unit='8paired heldout family/frame clusters, F09-F16',new_calculation_scope='Display uncertainty for individual original means only, no new model experiment or primary hypothesis test')))
print(pd.DataFrame(summary)[['site','comparison','mean','CI_lo','CI_hi']].to_string(index=False));print('F09',len(shared),len(lost),len(gained),'changed token positions',changes)
