import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,shutil,hashlib
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));R=Path(c['parent_round']);P=Path(c['project_dir']);rr=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];meta=pd.DataFrame(rr).reset_index(names='index');g=pd.read_csv(R/'analysis/current_reference_groups.csv');meta=meta.merge(g[['index','group','full_top1_id']],on='index');chunks=list((E/'analysis/chunks').glob('*.json'));assert len(chunks)==180,len(chunks);flat=[];replays=[];count=0
with (E/'analysis/raw_outputs.jsonl').open('w') as f:
 for p in chunks:
  x=json.load(open(p));assert x['complete'] and x['freeze_sha256']==hashlib.sha256((E/'freeze.json').read_bytes()).hexdigest();replays.append(x['native_replay'])
  for r in x['records']:
   r['data_source']='NEW_DELETE' if r['condition']!='identity' else 'NEW_NATIVE_IDENTITY';f.write(json.dumps(r,ensure_ascii=False)+'\n');flat.append({k:v for k,v in r.items() if k!='top10'});count+=1
 for line in (R/'analysis/raw_outputs.jsonl').open():
  r=json.loads(line)
  if r['readout']=='continuation' and r['condition']=='head64':
   r['condition']='keep_head64';r['data_source']='R16_REUSED_EXACT';f.write(json.dumps(r,ensure_ascii=False)+'\n');flat.append({k:v for k,v in r.items() if k!='top10'})
a=pd.DataFrame(flat).merge(meta[['index','position_uid','panel','seq_id','domain','position','input_id','target_id','group']],on='index');assert len(a)==207097,len(a);assert not a.duplicated(['index','layer','scope','condition']).any();assert (a.top1_agreement==(a.top1_id==a.full_top1_id)).all();assert a[a.condition=='identity'].top1_agreement.all();freq=np.load(E/'data/frequency.npz');ii=a.top1_id.to_numpy(dtype=int);a['output_type']=np.select([~freq['valid'][ii],freq['format_mask'][ii],freq['group'][ii]==0],['nonlexical','format','nonformat_common'],default='nonformat_other');a.to_csv(E/'analysis/position_metrics.csv',index=False);pd.DataFrame(replays).to_csv(E/'analysis/native_replay.csv',index=False)
a.groupby(['panel','layer','scope','condition','full_top1_id','top1_id']).size().reset_index(name='positions').to_csv(E/'analysis/token_transitions.csv',index=False)
outs=[]
for typ in ['format','nonformat_common','nonformat_other','nonlexical']:
 b=a.assign(fraction=(a.output_type==typ).astype(float)).groupby(['panel','layer','scope','condition','seq_id']).fraction.mean().reset_index().groupby(['panel','layer','scope','condition']).fraction.mean().reset_index();b['output_type']=typ;outs.append(b)
pd.concat(outs).to_csv(E/'analysis/output_type_fractions.csv',index=False)
keys=['panel','layer','scope','condition'];metrics=['top1_agreement','NLL','KL_full','entropy','target_probability','target_rank','full_top1_probability','full_top1_rank','target_retained_energy','prefix_retained_energy','target_intervention_norm','prefix_intervention_norm','target_relative_intervention','prefix_relative_intervention'];stack=pd.concat([a.assign(group='ALL'),a]);doc=stack.groupby(keys+['group','seq_id'])[metrics].mean().reset_index();doc.to_csv(E/'analysis/document_metrics.csv',index=False)
summary=[]
for kk,z in doc.groupby(keys+['group']):
 m=z[metrics].to_numpy(float);rng=np.random.default_rng(c['seeds']['bootstrap']);bs=rng.integers(0,len(z),(2000,len(z)))
 for j,metric in enumerate(metrics):
  v=m[:,j]
  if np.isnan(v).all():continue
  lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);summary.append(dict(zip(keys+['group'],kk),metric=metric,mean=float(v.mean()),ci_low=float(lo),ci_high=float(hi),documents=len(z)))
s=pd.DataFrame(summary);s.to_csv(E/'analysis/summary_metrics.csv',index=False)
# Perposition jointly retain/delete, all outcomes kept.
cols=['index','layer','scope','top1_id','top1_agreement','NLL','KL_full','target_probability','target_rank'];k=a[a.condition=='keep_head64'][cols].rename(columns={x:'keep_'+x for x in cols[3:]});dd=a[a.condition=='delete_head64'][cols].rename(columns={x:'delete_'+x for x in cols[3:]});joint=k.merge(dd,on=cols[:3],validate='one_to_one').merge(meta[['index','position_uid','panel','seq_id','group']],on='index');joint['pattern']=np.select([joint.keep_top1_agreement&joint.delete_top1_agreement,joint.keep_top1_agreement, joint.delete_top1_agreement],['both','keep_only','delete_only'],default='neither');joint.to_csv(E/'analysis/joint_position_results.csv',index=False);patterns=[]
for pattern in ['both','keep_only','delete_only','neither']:
 b=joint.assign(value=(joint.pattern==pattern).astype(float));b=pd.concat([b.assign(group='ALL'),b]);b=b.groupby(['panel','layer','scope','group','seq_id']).value.mean().reset_index()
 for kk,z in b.groupby(['panel','layer','scope','group']):
  v=z.value.to_numpy();rng=np.random.default_rng(c['seeds']['bootstrap']);bs=rng.integers(0,len(v),(2000,len(v)));lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);patterns.append(dict(zip(['panel','layer','scope','group'],kk),pattern=pattern,mean=float(v.mean()),ci_low=float(lo),ci_high=float(hi),documents=len(v)))
pd.DataFrame(patterns).to_csv(E/'analysis/joint_patterns.csv',index=False)
contrasts=[]
for kk,z in doc[doc.condition!='identity'].groupby(['panel','layer','scope','group']):
 for metric in ['top1_agreement','NLL','KL_full']:
  w=z.pivot(index='seq_id',columns='condition',values=metric);comparisons={'delete_minus_keep':w.delete_head64-w.keep_head64,'headdelete_minus_mean_randomdelete':w.delete_head64-w[[f'delete_random{x}' for x in c['seeds']['random']]].mean(axis=1)}
  for name,val in comparisons.items():
   v=val.to_numpy();rng=np.random.default_rng(c['seeds']['bootstrap']);bs=rng.integers(0,len(v),(2000,len(v)));lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);contrasts.append(dict(zip(['panel','layer','scope','group'],kk),contrast=name,metric=metric,mean=float(v.mean()),ci_low=float(lo),ci_high=float(hi),documents=len(v)))
pd.DataFrame(contrasts).to_csv(E/'analysis/paired_contrasts.csv',index=False)
overview=s[s.group=='ALL'].pivot(index=keys,columns='metric',values='mean').reset_index();overview.to_csv(E/'analysis/layerwise_overview.csv',index=False);meta.groupby(['panel','group']).agg(positions=('index','size'),documents=('seq_id','nunique')).reset_index().to_csv(E/'analysis/group_coverage.csv',index=False)
# Sanity: lastlayer scope equality, retainedrank exact and sharedoldresults unchanged.
z=a[(a.layer==28)&a.condition.str.startswith('delete_')];u=z[z.scope=='all_prefix'].set_index(['index','condition']).sort_index();v=z[z.scope=='target_only'].set_index(['index','condition']).sort_index();assert np.array_equal(u[['NLL','KL_full','top1_id']].values,v[['NLL','KL_full','top1_id']].values)
old=pd.read_csv(R/'analysis/summary_metrics.csv');err=0
for r in s[s.condition=='keep_head64'].itertuples():
 q=old[(old.panel==r.panel)&(old.layer==r.layer)&(old.scope==r.scope)&(old.group==r.group)&(old.metric==r.metric)&(old.condition=='head64')&(old.readout=='continuation')]
 if len(q):err=max(err,abs(r.mean-q['mean'].iloc[0]))
assert err<1e-10,err
assert all(r['identity_NLL_max_abs']<=1e-6 and r['identity_top1_changes']==0 and r['all28_targeth_max_abs']==0 for r in replays)
geom=[]
for l in range(28):
 b=np.load(E/'data/bases'/f'layer{l+1:02d}.npz');V=b['V'];ev=b['eigenvalues'];geom.append({'layer':l+1,'condition':'delete_head64','retained_rank':960,'reference_variance_retained':float(ev[64:].sum()/ev.sum())})
 for seed in c['seeds']['random']:
  q=np.load(E/'data'/f'random{seed}.npy');removed=float((ev[:,None]*(V.T@q)**2).sum()/ev.sum());geom.append({'layer':l+1,'condition':f'delete_random{seed}','retained_rank':960,'reference_variance_retained':1-removed})
pd.DataFrame(geom).to_csv(E/'analysis/reference_variance.csv',index=False)
for f in ['summary_metrics.csv','layerwise_overview.csv','paired_contrasts.csv','joint_patterns.csv','group_coverage.csv','native_replay.csv','reference_variance.csv']:shutil.copy2(E/'analysis'/f,P/'evidence'/f)
meta[['index','position_uid','panel','seq_id','position','input_id','target_id','group']].to_csv(E/'analysis/input_position_index.csv',index=False);shutil.copy2(E/'analysis/input_position_index.csv',P/'evidence/input_position_index.csv')
validation={'pass':True,'native_original_documents':180,'new_records':count,'combined_records':len(a),'new_conditions':4,'reused_keep_records':len(a[a.condition=='keep_head64']),'unique_positions':737,'natural_positions':700,'PCA_refits':0,'training_updates':0,'keep64_summary_max_abs_error':err,'identity_h28layer_max_abs':max(r['all28_targeth_max_abs'] for r in replays),'identity_NLL_max_abs':max(r['identity_NLL_max_abs'] for r in replays),'identity_top1_changes':sum(r['identity_top1_changes'] for r in replays),'lastlayer_scopes_exact':True,'scientific_acceptance':'Unknown'}
for b in [E,P]:(b/'audit/validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(validation,indent=2));print(overview[(overview.panel=='natural')&(overview.condition.isin(['delete_head64','keep_head64']))&(overview.layer.isin([1,7,14,21,28]))][['layer','scope','condition','top1_agreement','NLL','target_retained_energy']].round(4).to_string(index=False))
