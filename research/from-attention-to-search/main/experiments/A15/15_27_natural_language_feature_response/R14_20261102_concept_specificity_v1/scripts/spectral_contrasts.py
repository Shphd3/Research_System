from pathlib import Path
import json,numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1]
F=pd.read_csv(E/'analysis/family_metrics.csv');F=F[F.split=='evaluation'];draws=np.load(E/'analysis/bootstrap_family_draws.npz');C=json.load(open(E/'data/conditions.json'));alias=C['aliases'];domains=['biology','mathematics','physics'];ids={d:sorted(F[F.domain==d].family_id.unique()) for d in domains};Q={n:g.set_index('family_id').J for n,g in F.groupby('condition')};seeds=[11021,11022,11023];out=[]
def resolve(n):return alias.get(n,n)
def compare(target,controls,kind,sign=1):
 target=resolve(target);controls=[resolve(c) for c in controls];v=sign*(Q[target]-sum(Q[c] for c in controls)/len(controls))
 for d in domains+['overall_equal_domains']:
  ds=domains if d=='overall_equal_domains' else [d];boot=np.mean([v.loc[ids[z]].to_numpy()[draws[z]].mean(1) for z in ds],0);kk=sum([ids[z] for z in ds],[])
  out.append({'comparison':kind,'target':target,'controls':'|'.join(controls),'control_count':len(controls),'domain':d,'difference':float(v.loc[kk].mean()),'low95':float(np.quantile(boot,.025)),'high95':float(np.quantile(boot,.975)),'positive_meaning':'more_deletion_loss' if sign==-1 else 'larger_cue_contrast','families':len(kk)})
for k in [1,16,64,128,256,512,768,1024]:
 refs=[f'random_keep_r{k}_s{s}' for s in seeds]
 for c in refs:compare(f'keep_head{k}',[c],'nested_vs_one_random')
 compare(f'keep_head{k}',refs,'nested_vs_random_mean')
for label,width in [(f'B{i}',n) for i,n in enumerate([1,15,48,64,128,256,256,256],1)]+[('H',16)]:
 target='delete_'+label;refs=[f'random_delete_r{width}_s{s}' for s in seeds];nm=[f'normmatch_{target}_s{s}' for s in seeds]
 for c in refs:compare(target,[c],'delete_vs_one_same_rank',-1)
 compare(target,refs,'delete_vs_same_rank_mean',-1)
 for c in nm:compare(target,[c],'delete_vs_one_normmatched',-1)
 compare(target,nm,'delete_vs_normmatched_mean',-1)
 if label!='H':
  refs=[f'random_keep_r{width}_s{s}' for s in seeds]
  compare('keep_'+label,refs,'single_keep_vs_random_mean')
for j in range(3,9):
 target=f'append_B{j}';refs=[f'random_append_B{j}_s{s}' for s in seeds]
 compare(target,[f'head_extension_B{j}'],'append_vs_equal_total_head_extension')
 for c in refs:compare(target,[c],'append_vs_one_random')
 compare(target,refs,'append_vs_random_mean')
pd.DataFrame(out).to_csv(E/'analysis/spectral_matched_contrasts.csv',index=False)
print(pd.DataFrame(out).query("domain=='overall_equal_domains' and comparison in ['append_vs_equal_total_head_extension','append_vs_random_mean']")[['comparison','target','difference','low95','high95']].to_string(index=False))
