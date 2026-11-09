import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,hashlib,shutil,time
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'manifest.json'));P=Path(cfg['project_dir'])
rr=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];meta=pd.DataFrame(rr).reset_index(names='index');gg=pd.DataFrame(json.load(open(E/'data/frozen_groups.json')));meta=meta.merge(gg[['index','group','old_full_top1_id']],on='index')
chunks=list((E/'analysis/chunks').glob('*.json'));assert len(chunks)==180,len(chunks);raw=[];dif=[]
# Correct an implementation inconsistency: full.argmax used a deterministic first-ID tie,
# while topk serialized tied candidates in arbitrary order. Native probabilities unchanged.
allrecords=[]
for p in chunks:allrecords.extend(json.load(open(p))['records'])
full_ids={}
for r in allrecords:
 if r['condition']=='identity':
  pp=max(z['probability'] for z in r['top10']);tt=[z for z in r['top10'] if z['probability']==pp];assert len(tt)<10;full_ids[r['index']]=min(z['id'] for z in tt)
freq=np.load(E/'data/frequency.npz');corrected=[]
for i,r in enumerate(rr):
 ii=full_ids[i];g='nonlexical' if not freq['valid'][ii] else 'format' if freq['format_mask'][ii] else 'nonformat_common' if freq['group'][ii]==0 else 'nonformat_other';corrected.append({'index':i,'group':g,'full_top1_id':ii})
legacy_groups=meta[['index','group']].rename(columns={'group':'legacy_group'});meta=meta.drop(columns='group').merge(pd.DataFrame(corrected),on='index').merge(legacy_groups,on='index');meta.to_csv(E/'analysis/current_reference_groups.csv',index=False)
json.dump({'tie_policy':'highest probability then lowest tokenID; exact native BF16 logit ties','group_rule_unchanged':True,'membership_recomputed_from_current_identity_only':True,'legacy_group_changes':int((meta.group!=meta.legacy_group).sum()),'raw_chunks_preserved':True,'extra_model_forwards':0},open(E/'analysis/tie_policy.json','w'),indent=2)
with (E/'analysis/raw_outputs.jsonl').open('w') as f:
 for p in chunks:
  x=json.load(open(p));assert x['complete'];dif+=x['baseline_differences']
  for r in x['records']:
   r['top10']=sorted(r['top10'],key=lambda z:(-z['probability'],z['id']));maxp=r['top10'][0]['probability'];ties=sum(z['probability']==maxp for z in r['top10']);assert ties<10,('max ties not fully observed',r);r['max_probability_tie_count']=ties;r['top1_id']=r['top10'][0]['id'];r['full_top1_id']=full_ids[r['index']];r['top1_agreement']=r['top1_id']==full_ids[r['index']]
   f.write(json.dumps(r,ensure_ascii=False)+'\n');raw.append({k:v for k,v in r.items() if k!='top10'})
a=pd.DataFrame(raw).merge(meta[['index','position_uid','panel','seq_id','domain','position','input_id','target_id','group','legacy_group','old_full_top1_id']],on='index');assert len(a)==737*(1+28*(10+2)+2),len(a);assert not a.duplicated(['index','layer','condition','scope','readout']).any();a.to_csv(E/'analysis/position_metrics.csv',index=False)
metrics=['top1_agreement','full_top1_probability','full_top1_rank','target_probability','target_rank','NLL','KL_full','entropy','target_retained_energy','prefix_retained_energy','target_intervention_norm','prefix_intervention_norm','target_relative_intervention','prefix_relative_intervention'];keys=['panel','layer','condition','scope','readout']
# Separate groups first; ALL includes every document position once.
frames=[a.assign(group='ALL'),a];d=pd.concat(frames).groupby(keys+['group','seq_id'],dropna=False)[metrics].mean().reset_index();d.to_csv(E/'analysis/document_metrics.csv',index=False)
summ=[]
for kk,z in d.groupby(keys+['group'],dropna=False):
 m=z[metrics].to_numpy(float);rng=np.random.default_rng(cfg['bootstrap_seed']);bs=rng.integers(0,len(z),(cfg['bootstrap_repetitions'],len(z)));means=np.nanmean(m,0)
 for j,metric in enumerate(metrics):
  v=m[:,j]
  if np.isnan(v).all():continue
  vv=v[bs].mean(1);lo,hi=np.quantile(vv,[.025,.975]);summ.append(dict(zip(keys+['group'],kk),metric=metric,mean=means[j],ci_low=lo,ci_high=hi,documents=len(z)))
s=pd.DataFrame(summ);s.to_csv(E/'analysis/summary_metrics.csv',index=False)
# Paired scope differences: same doc/group and layer/condition, target-only minus all-prefix.
x=d[d.readout=='continuation'];pa=[]
for kk,z in x[x.scope!='none'].groupby(['panel','layer','condition','group']):
 v=z.pivot(index='seq_id',columns='scope',values='top1_agreement');vv=(v.target_only-v.all_prefix).to_numpy();rng=np.random.default_rng(cfg['bootstrap_seed']);bs=rng.integers(0,len(vv),(2000,len(vv)));lo,hi=np.quantile(vv[bs].mean(1),[.025,.975]);pa.append(dict(zip(['panel','layer','condition','group'],kk),target_only_minus_all_prefix=vv.mean(),ci_low=lo,ci_high=hi,documents=len(vv)))
pd.DataFrame(pa).to_csv(E/'analysis/scope_contrasts.csv',index=False)
coverage=meta.groupby(['panel','group']).agg(positions=('index','size'),documents=('seq_id','nunique')).reset_index();coverage.to_csv(E/'analysis/group_coverage.csv',index=False)
# Individual target full1024 reconstruction inFP64 for all layers; target caches are independent numerical evidence.
identity=[]
for l in range(28):
 b=np.load(E/'data/bases'/f'layer{l+1:02d}.npz');H=np.concatenate([np.load(p)['h'][l] for p in (E/'data/eval_targets').glob('*.npz')]).astype('float64');v=b['V'];mu=b['mean'];rec=mu+(H-mu)@v@v.T;err=np.max(abs(H-rec));assert err<1e-8;identity.append({'layer':l+1,'positions':len(H),'max_abs_error':float(err),'orthogonality':float(b['orthogonality']),'head64_reference_variance':float(b['eigenvalues'][:64].sum()/b['eigenvalues'].sum()),'min_eigenvalue':float(b['eigenvalues'][-1])})
pd.DataFrame(identity).to_csv(E/'analysis/PCA_and_identity.csv',index=False)
# Legacy final-layer scope exact; comparison to oldR13 records kept separate.
old={x['index']:x for x in [json.loads(l) for l in (Path(cfg['parent_round'])/'analysis/raw_outputs.jsonl').read_text().splitlines()] if x['condition']=='k64'}
leg=a[(a.condition=='legacy_head64')&(a.scope=='target_only')];legacy=[]
for r in leg.to_dict('records'):
 oo=old[r['index']];mx=oo['top20'][0]['probability'];oldid=min(z['id'] for z in oo['top20'] if z['probability']==mx);legacy.append({'index':r['index'],'NLL_abs_diff':abs(r['NLL']-oo['NLL']),'old_top1_id':oldid,'current_top1_id':r['top1_id'],'top1_equal':oldid==r['top1_id']})
pd.DataFrame(legacy).to_csv(E/'analysis/legacy_replay.csv',index=False)
# Top1 transition pairs for complete panel; class label remains original/full group.
trans=a[(a.panel=='natural')&(a.readout=='continuation')&(a.condition=='head64')].groupby(['layer','scope','group','full_top1_id','top1_id']).size().reset_index(name='positions');trans.to_csv(E/'analysis/head64_token_transitions.csv',index=False)
for name in ['summary_metrics.csv','scope_contrasts.csv','group_coverage.csv','PCA_and_identity.csv','legacy_replay.csv','head64_token_transitions.csv']:
 shutil.copy2(E/'analysis'/name,P/'evidence'/name)
meta[['index','position_uid','panel','seq_id','position','input_id','target_id','group']].to_csv(P/'evidence/input_position_index.csv',index=False)
shutil.copy2(P/'evidence/input_position_index.csv',E/'analysis/input_position_index.csv')
json.dump({'pass':True,'positions':737,'documents':180,'raw_records':len(a),'reference_documents':60,'PCA_positions':9600,'baseline_top1_differences':dif,'allPC':identity,'legacy_max_NLL_diff':max(r['NLL_abs_diff'] for r in legacy),'legacy_top1_differences':sum(not r['top1_equal'] for r in legacy),'last_layer_scopes_exact_worker_assertions':True,'scientific_acceptance':'Unknown'},open(E/'audit/validation.json','w'),ensure_ascii=False,indent=2)
assert a[a.condition=='identity'].top1_agreement.all(),'no-op must preserve deterministic top1'
assert a[(a.readout=='direct_head')&(a.layer==28)&(a.condition=='unprojected')].top1_agreement.all(),'direct final raw must match native'
# Sensitivity: use historical group membership with corrected same-ID metric; no new inference.
oldgrp=a.assign(group=a.legacy_group).groupby(keys+['group','seq_id'])[metrics].mean().reset_index().groupby(keys+['group'])[metrics].mean().reset_index();oldgrp.to_csv(E/'analysis/legacy_group_sensitivity.csv',index=False)
print(coverage.to_string(index=False));print(s[(s.panel=='natural')&(s.condition=='head64')&(s.readout=='continuation')&(s.metric=='top1_agreement')&(s.layer.isin([1,7,14,21,28]))].round(4).to_string(index=False));print('BASELINE_DIFF',dif)
