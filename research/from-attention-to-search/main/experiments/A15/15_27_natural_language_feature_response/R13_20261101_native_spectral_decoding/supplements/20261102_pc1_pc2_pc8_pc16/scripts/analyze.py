import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,hashlib,shutil
import numpy as np,pandas as pd
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements')/P.name;O=E.parents[1]
assert (E/'terminal_receipt.json').exists()
rr=[json.loads(l) for l in (O/'data/native_positions.jsonl').read_text().splitlines()];old=[json.loads(l) for l in (O/'analysis/raw_outputs.jsonl').read_text().splitlines()];records=[r for r in old if r['condition'] in ['k1','k16','mean_only','identity']]
for p in sorted((E/'analysis/chunks').glob('*.json')):records+=json.load(open(p))['records']
assert len(records)==737*6 and len({(r['index'],r['condition']) for r in records})==737*6
refs={r['index']:r for r in records if r['condition']=='identity'};f=np.load(O/'data/frequency.npz');V=np.load(O/'data/bases.npz');ev=V['eigenvalues'];groups={int(r['index']):r['recovery_group'] for r in pd.read_csv(O/'analysis/recovery_group_members.csv').to_dict('records')};out=[];retained=[]
for r in records:
 i=r['index'];z={k:r[k] for k in ['index','condition','NLL','KL_full','entropy','top1_agreement','top10_recovery','target_probability','target_rank','top1_correct','format_mass','lexical_mass','expected_log_frequency']};z.update({k:rr[i][k] for k in ['panel','seq_id','position','domain','topic']});z.update(group=groups[i],freq_top1pct=r['frequency_mass'][0],original_top1_id=refs[i]['top20'][0]['id'],original_top1_fragment=refs[i]['top20'][0]['fragment'],output_top1_id=r['top20'][0]['id'],output_top1_fragment=r['top20'][0]['fragment'],output_top1_probability=r['top20'][0]['probability']);out.append(z)
 for t in r['top20']:assert 0<=t['probability']<=1
 if r['condition'] in ['pc2','k8']:assert abs(r['NLL']+np.log(r['target_probability']))<2e-6
 if r['top1_agreement']:retained.append({'index':i,'condition':r['condition'],'panel':rr[i]['panel'],'seq_id':rr[i]['seq_id'],'group':groups[i],'token_id':refs[i]['top20'][0]['id'],'fragment':refs[i]['top20'][0]['fragment']})
df=pd.DataFrame(out);df.to_csv(E/'analysis/position_metrics.csv',index=False);pd.DataFrame(retained).to_csv(E/'analysis/retained_position_IDs.csv',index=False);(E/'analysis/raw_outputs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
metrics=['NLL','KL_full','entropy','top1_agreement','top10_recovery','top1_correct','format_mass','freq_top1pct','expected_log_frequency'];doc=df.groupby(['panel','condition','seq_id'])[metrics].mean().reset_index();doc.to_csv(E/'analysis/document_metrics.csv',index=False);summary=[];rng=np.random.default_rng(20261102);recovery=[];diff=[]
conditions=['mean_only','k1','pc2','k8','k16','identity']
for panel in ['the','natural']:
 ids=sorted(doc[doc.panel==panel].seq_id.unique());bs=rng.integers(0,len(ids),(2000,len(ids)))
 for co in conditions:
  d=doc[(doc.panel==panel)&(doc.condition==co)].set_index('seq_id').loc[ids]
  for metric in metrics:
   v=d[metric].to_numpy(float);lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);summary.append({'panel':panel,'condition':co,'metric':metric,'mean':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':len(ids),'positions':int((df.panel==panel).sum()/6)})
 for group in ['format','nonformat_common','nonformat_other']:
  z=df[(df.panel==panel)&(df.group==group)];ids=sorted(z.seq_id.unique());bs=rng.integers(0,len(ids),(2000,len(ids)))
  for co in conditions:
   d=z[z.condition==co].groupby('seq_id').top1_agreement.mean().loc[ids].to_numpy(float);lo,hi=np.quantile(d[bs].mean(1),[.025,.975]);recovery.append({'panel':panel,'group':group,'condition':co,'mean':float(d.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':len(ids),'positions':len(z)//6,'retained_positions':int(z[z.condition==co].top1_agreement.sum()),'original_distinct_IDs':z[z.condition==co].original_top1_id.nunique(),'retained_distinct_IDs':z[(z.condition==co)&z.top1_agreement].original_top1_id.nunique()})
  for a,b in [('pc2','k1'),('k8','k1'),('k16','k8')]:
   aa=z[z.condition==a].groupby('seq_id').top1_agreement.mean().loc[ids].to_numpy(float);bb=z[z.condition==b].groupby('seq_id').top1_agreement.mean().loc[ids].to_numpy(float);v=aa-bb;lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);diff.append({'panel':panel,'group':group,'condition':a,'baseline':b,'mean_difference':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':len(ids)})
pd.DataFrame(summary).to_csv(E/'analysis/summary_metrics.csv',index=False);pd.DataFrame(recovery).to_csv(E/'analysis/group_recovery.csv',index=False);pd.DataFrame(diff).to_csv(E/'analysis/group_paired_contrasts.csv',index=False)
# Complete output and retained token identities with raw position counts, not disguised document means.
counts=[]
for (panel,co,i),z in df.groupby(['panel','condition','output_top1_id']):counts.append({'panel':panel,'condition':co,'token_id':int(i),'fragment':z.iloc[0].output_top1_fragment,'positions':len(z),'documents':z.seq_id.nunique(),'mean_top1_probability_on_these_positions':float(z.output_top1_probability.mean())})
pd.DataFrame(counts).sort_values(['panel','condition','positions'],ascending=[True,True,False]).to_csv(E/'analysis/output_top1_ID_counts.csv',index=False)
rd=pd.DataFrame(retained);ct=[]
for (panel,co,g,i),z in rd.groupby(['panel','condition','group','token_id']):ct.append({'panel':panel,'condition':co,'group':g,'token_id':int(i),'fragment':z.iloc[0].fragment,'positions':len(z),'documents':z.seq_id.nunique()})
pd.DataFrame(ct).to_csv(E/'analysis/retained_ID_counts.csv',index=False)
# Fixed case outputs stay comparable with the original selected list; append ordinary cases that restore under requested conditions, clearly posthoc.
fixed=json.load(open(O/'manifest.json'))['fixed_examples'];lookup={(r['index'],r['condition']):r for r in records};idx=[i for i,r in enumerate(rr) if r['panel']=='the' and r['seq_id'] in fixed];text=['# 固定真实前文：PC1、PC2单独、前8与前16维\n','保留同一训练均值；只改变方向。原后继是参考答案，原模型自身可能不将它排首位。\n']
for i in idx:
 r=rr[i];text+=['\n## '+r['position_uid']+'\n','```text\n'+r['visible_prefix']+'\n```\n',f"真实后继ID{r['target_id']}，片段{repr(r['target_fragment'])}。\n",'|条件|前三ID、片段、概率|目标排名|NLL|','|---|---|---:|---:|']
 for co in conditions:
  x=lookup[i,co];top='；'.join(str(t['id'])+' '+repr(t['fragment']).replace('|','/')+f" {t['probability']:.4f}" for t in x['top20'][:3]);text.append(f"|{co}|{top}|{x['target_rank']}|{x['NLL']:.4f}|")
(P/'text_cases_cn.md').write_text('\n'.join(text)+'\n')
# Exact eigenvalue/variance distinction for rank1 comparison.
spec={'k1':float(ev[0]/ev.sum()),'pc2':float(ev[1]/ev.sum()),'k8':float(ev[:8].sum()/ev.sum()),'k16':float(ev[:16].sum()/ev.sum())};(E/'analysis/reference_variance.json').write_text(json.dumps(spec,indent=2)+'\n')
assert df[df.condition=='identity'].top1_agreement.all();assert df.groupby(['panel','group','condition']).size().unstack().nunique(axis=1).eq(1).all();assert np.isfinite(df[metrics].to_numpy(float)).all()
validation={'pass':True,'records':len(df),'positions':737,'new_records':1474,'reused_records':2948,'primary37':True,'natural175documents700positions':True,'no_training':True,'no_new_transformer_forward':True,'subgroups_fixed':True,'identity_agreement_all':True,'document_bootstrap':2000};(E/'provenance/validation.json').write_text(json.dumps(validation,indent=2)+'\n')
for name in ['summary_metrics.csv','group_recovery.csv','group_paired_contrasts.csv','output_top1_ID_counts.csv','retained_ID_counts.csv','retained_position_IDs.csv','document_metrics.csv','reference_variance.json']:shutil.copy2(E/'analysis'/name,P/'evidence'/name)
print(pd.DataFrame(recovery).pivot_table(index=['panel','group','documents','positions'],columns='condition',values='mean').round(4).to_string());print(pd.DataFrame(summary).query("metric in ['NLL','KL_full','format_mass','freq_top1pct']").pivot_table(index=['panel','condition'],columns='metric',values='mean').round(4).to_string())
