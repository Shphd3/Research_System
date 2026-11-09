"""CPU document-weighted paired analysis, no classifier or PCA fit."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,gzip,hashlib,shutil,sys
import numpy as np,pandas as pd
sys.path.insert(0,'/data/250010109/dependency_packages/hf_transformers_qwen3')
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));R=Path(c['parent_round']);P=Path(c['project_dir']);tok=Tokenizer.from_file(str(Path(c['model_dir'])/'tokenizer.json'))
rr=[json.loads(s) for s in (E/'data/positions.jsonl').read_text().splitlines()];meta=pd.DataFrame(rr).reset_index(names='index');g=pd.read_csv(R/'analysis/current_reference_groups.csv');meta=meta.merge(g[['index','group','full_top1_id']],on='index');meta.to_json(E/'analysis/input_positions.jsonl',orient='records',lines=True,force_ascii=False)
freq=np.load(R/'data/frequency.npz');parts=[];outputs=[];replay=[];seen=[];headchanges=0;headnll=0.;fixed=c['fixed_cases'];nrows=0
chunks=sorted((E/'analysis/chunks').glob('*.npz'));assert len(chunks)==180,len(chunks);repairs=list((E/'analysis/batch1_repair_chunks').glob('*.npz'));assert len(repairs)==5,len(repairs);chunks=[E/'analysis/batch1_repair_chunks'/p.name if (E/'analysis/batch1_repair_chunks'/p.name).exists() else p for p in chunks];freeze=hashlib.sha256((E/'freeze.json').read_bytes()).hexdigest()
with gzip.open(E/'analysis/position_metrics.csv.gz','wt',compresslevel=1) as stream,(E/'analysis/fixed_case_outputs.jsonl').open('w') as cases:
 for n,p in enumerate(chunks):
  z=np.load(p);assert str(z['freeze_sha256'])==freeze
  ZI=z['ints'];ZF=z['floats'];ZT=z['top10_ids'];ZP=z['top10_probs'];ZC=z['condition_names']
  a=pd.concat([pd.DataFrame(ZI,columns=z['int_fields']),pd.DataFrame(ZF,columns=z['float_fields'])],axis=1);ids=a['index'].to_numpy();a['condition']=np.array(ZC)[a.condition.to_numpy()];a['scope']=np.array(['all_prefix','target_only','none'])[a.scope.to_numpy()];a=a.merge(meta[['index','seq_id','panel','group','position_uid','position','input_id','target_id']],on='index',sort=False)
  assert (a.top1_agreement.astype(bool)==(a.top1_id==a.full_top1_id)).all();assert (a[a.condition=='identity'].top1_agreement==1).all();assert np.isfinite(a.select_dtypes('number').to_numpy()).all()
  seen+=a[a.condition=='identity']['index'].tolist();out=a.top1_id.to_numpy(int);a['output_format_fraction']=freq['format_mask'][out].astype(float);a['output_special_fraction']=(~freq['valid'][out]).astype(float);a['output_common_fraction']=(freq['valid'][out]&~freq['format_mask'][out]&(freq['group'][out]==0)).astype(float);a['output_other_fraction']=1-a.output_format_fraction-a.output_special_fraction-a.output_common_fraction
  a.to_csv(stream,index=False,header=n==0);nrows+=len(a)
  metrics=[str(x) for x in z['float_fields']]+['output_format_fraction','output_special_fraction','output_common_fraction','output_other_fraction']
  stack=pd.concat([a,a.assign(group='ALL')]);parts.append(stack.groupby(['panel','group','seq_id','layer','condition','scope'])[metrics].mean().reset_index())
  for j in np.where(np.isin(ids,fixed))[0]:
   i=int(ids[j]);r={'index':i,'layer':int(ZI[j,1]),'condition':str(ZC[ZI[j,2]]),'scope':['all_prefix','target_only','none'][ZI[j,3]],**{str(k):float(v) for k,v in zip(z['float_fields'],ZF[j])},'top1_id':int(ZI[j,4]),'top10':[{'id':int(t),'fragment':tok.decode([int(t)],skip_special_tokens=False),'probability':float(q)} for t,q in zip(ZT[j],ZP[j])]};cases.write(json.dumps(r,ensure_ascii=False)+'\n')
  h=z['oldhead_replay'];headnll=max(headnll,float(h[:,0].max()));headchanges+=int(h[:,1].sum());replay.append({'seq_id':p.stem,**json.loads(str(z['baseline_replay']))})
  if n%30==0:print('parsed',n,len(a),flush=True)
assert sorted(seen)==list(range(737));assert nrows==737*(1+28*34*2),nrows
D=pd.concat(parts,ignore_index=True);del parts;D['source']='NEW';metrics=[str(x) for x in z['float_fields']]+['output_format_fraction','output_special_fraction','output_common_fraction','output_other_fraction']
# Reuse exact old affine mean/random controls; never relabel them as new measurements.
old=pd.read_csv(R/'analysis/document_metrics.csv');old=old[(old.readout=='continuation')&old.condition.isin(['mean_only','random1031','random1032','random1033'])].copy();old['source']='R16_REUSED_EXACT';old=old.rename(columns={'target_retained_energy':'target_band_energy','prefix_retained_energy':'prefix_band_energy'});D=pd.concat([D,old.reindex(columns=D.columns)],ignore_index=True)
D.to_csv(E/'analysis/document_metrics.csv.gz',index=False,compression={'method':'gzip','compresslevel':1});pd.DataFrame(replay).to_csv(E/'analysis/native_replay.csv',index=False)
keys=['panel','group','layer','condition','scope'];S=D.groupby(keys)[metrics].mean().reset_index();counts=D.groupby(keys).size().rename('documents').reset_index();S=S.merge(counts,on=keys)
# Shared document draws across every condition preserve paired uncertainty.
paired=[];headcomp=[];baselinecomp=[];ci_frames=[]
for (panel,group),d in D.groupby(['panel','group']):
 docs=sorted(d.seq_id.unique());rng=np.random.default_rng(c['bootstrap_seed']);weights=rng.multinomial(len(docs),np.full(len(docs),1/len(docs)),size=c['bootstrap_repetitions'])/len(docs)
 for metric in ['top1_agreement','NLL']:
  mat=d.pivot(index='seq_id',columns=['layer','condition','scope'],values=metric).reindex(docs);vals=mat.to_numpy();samples=weights@np.nan_to_num(vals);lo,hi=np.quantile(samples,[.025,.975],axis=0)
  cc=pd.DataFrame(list(mat.columns),columns=['layer','condition','scope']);cc['panel']=panel;cc['group']=group;cc['metric']=metric;cc['lo']=lo;cc['hi']=hi;ci_frames.append(cc)
  if metric=='top1_agreement':
   for l in range(1,29):
    for scope in ['all_prefix','target_only']:
     for b in range(16):
      x=mat[(l,f'add_b{b:02d}',scope)].to_numpy()-mat[(l,f'no_b{b:02d}',scope)].to_numpy();bs=weights@x;ci=np.quantile(bs,[.025,.975]);paired.append(dict(panel=panel,group=group,layer=l,scope=scope,band=b,add_minus_no=x.mean(),ci_low=ci[0],ci_high=ci[1],documents=len(x)))
      for mode,base in [('add','mean_only'),('no','zero')]:
       x=mat[(l,f'{mode}_b{b:02d}',scope)].to_numpy()-mat[(l,base,scope)].to_numpy();ci=np.quantile(weights@x,[.025,.975]);baselinecomp.append(dict(panel=panel,group=group,layer=l,scope=scope,mode=mode,band=b,band_minus_baseline=x.mean(),ci_low=ci[0],ci_high=ci[1],documents=len(x)))
      if b:
       for mode in ['add','no']:
        x=mat[(l,f'{mode}_b00',scope)].to_numpy()-mat[(l,f'{mode}_b{b:02d}',scope)].to_numpy();ci=np.quantile(weights@x,[.025,.975]);headcomp.append(dict(panel=panel,group=group,layer=l,scope=scope,mode=mode,band=b,head_minus_band=x.mean(),ci_low=ci[0],ci_high=ci[1],documents=len(x)))
CI=pd.concat(ci_frames,ignore_index=True)
for metric in ['top1_agreement','NLL']:
 q=CI[CI.metric==metric].drop(columns='metric').rename(columns={'lo':metric+'_ci_low','hi':metric+'_ci_high'});S=S.merge(q,on=keys,how='left',validate='one_to_one')
pd.DataFrame(baselinecomp).to_csv(E/'analysis/paired_band_vs_baseline.csv',index=False)
S.to_csv(E/'analysis/summary_metrics.csv',index=False);pd.DataFrame(paired).to_csv(E/'analysis/paired_mean_effect.csv',index=False);pd.DataFrame(headcomp).to_csv(E/'analysis/paired_head_vs_band.csv',index=False)
# Complete equal-rank display matrix, including every layer/segment and both scopes/modes.
S[(S.panel=='natural')&(S.group=='ALL')&S.condition.str.match('(add|no)_b')].to_csv(E/'analysis/natural_equal64_matrix.csv',index=False)
coverage=meta.groupby(['panel','group']).agg(positions=('index','size'),documents=('seq_id','nunique')).reset_index();coverage.to_csv(E/'analysis/group_coverage.csv',index=False)
validation={'pass':True,'new_rows':nrows,'singleton_document_repair_count':5,'all_175_main_chunks_original_unchanged':True,'documents_physical':len(chunks),'positions':len(seen),'all28_native_states_replay_max_abs':max(x['targeth_max_abs'] for x in replay),'baseline_NLL_replay_max_abs':max(x['baseline_NLL_max_abs'] for x in replay),'oldhead_top1_changes':headchanges,'oldhead_NLL_max_abs':headnll,'last_layer_scopes':'checked exact per GPU chunk','new_PCA_fits':0,'parameter_updates':0,'intervals':'paired document pointwise, not simultaneous','acceptance':'Unknown'}
assert headnll<=.05,validation
(E/'audit/analysis_validation.json').write_text(json.dumps(validation,indent=2)+'\n')
for name in ['summary_metrics.csv','paired_mean_effect.csv','paired_head_vs_band.csv','paired_band_vs_baseline.csv','natural_equal64_matrix.csv','group_coverage.csv','native_replay.csv']:
 shutil.copy2(E/'analysis'/name,P/'evidence'/name)
shutil.copy2(E/'audit/analysis_validation.json',P/'audit/analysis_validation.json')
print(json.dumps(validation),flush=True)
