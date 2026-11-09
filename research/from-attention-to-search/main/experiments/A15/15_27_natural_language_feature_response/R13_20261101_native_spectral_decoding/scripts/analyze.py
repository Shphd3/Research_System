"""Paired document-level analysis of fixed native-head predictions; no fitting."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,csv,shutil,hashlib
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')/P.name
MET=['NLL','KL_full','entropy','top1_agreement','top10_recovery','top1_correct','expected_log_frequency','h_norm','centered_energy_fraction','lexical_mass','format_mass','nonlexical_mass','freq_top1pct','freq_next9pct','freq_next40pct','freq_last50pct']
def rows(p):return [json.loads(l) for l in p.read_text().splitlines() if l]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
assert (E/'terminal_receipt.json').exists(),'numeric task not complete'
manifest=json.load(open(E/'manifest.json'));pos=rows(E/'data/positions.jsonl');data=[];outputs=[]
# BF16 logit ties: topk(10) vs topk(20) can order equal values differently.
# Canonical top1/top10 choose probability descending, then ID ascending.
rawrecords=[r for f in sorted((E/'analysis/chunks').glob('*.json')) for r in json.load(open(f))['records']]
assert all(r['top20'][9]['probability']>r['top20'][19]['probability'] for r in rawrecords),'stored20 must cover all top10 cutoff ties'
canon={}
for r in rawrecords:
 r['top20']=sorted(r['top20'],key=lambda x:(-x['probability'],x['id']));canon[r['index'],r['condition']]=r
reference={r['index']:r for r in rawrecords if r['condition']=='identity'}
for r in rawrecords:
 ref=reference[r['index']];top=r['top20'];r['top1_agreement']=top[0]['id']==ref['top20'][0]['id'];r['top10_recovery']=len({t['id'] for t in top[:10]}&{t['id'] for t in ref['top20'][:10]})/10;r['top1_correct']=top[0]['id']==pos[r['index']]['target_id']
(E/'audit/topk_tie_fix.json').write_text(json.dumps({'reason':'BF16 logit ties; K-dependent torch.topk order','max_tied_top1_members':max(sum(t['probability']==r['top20'][0]['probability'] for t in r['top20']) for r in rawrecords),'all_top10_cutoffs_covered_by_saved20':True,'policy':'probability descending then ID ascending','new_GPU_computation':0,'NLL_KL_entropy_probabilities_unchanged':True},indent=2)+'\n')

for f in sorted((E/'analysis/chunks').glob('*.json')):
 for old in json.load(open(f))['records']:
  r=canon[old['index'],old['condition']]
  info=pos[r['index']];z={k:v for k,v in r.items() if k not in ['top20','frequency_mass']};z.update({k:info[k] for k in ['panel','seq_id','domain','topic','platform_family','source_stratum','position','target_id','input_id']});z.update(dict(zip(['freq_top1pct','freq_next9pct','freq_next40pct','freq_last50pct'],r['frequency_mass'])));z['nonlexical_mass']=1-z['lexical_mass'];data.append(z);outputs.append(r)
df=pd.DataFrame(data);assert len(df)==737*21 and not df.duplicated(['index','condition']).any(),len(df)
df.to_csv(E/'analysis/position_metrics.csv',index=False)
(E/'analysis/raw_outputs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in outputs))
# Each document contributes equally regardless of its number of cached positions.
doc=df.groupby(['panel','seq_id','domain','condition'],sort=False)[MET].mean().reset_index();doc.to_csv(E/'analysis/document_metrics.csv',index=False)
rng=np.random.default_rng(20261102);summary=[];contrasts=[]
for panel in ['the','natural']:
 dd=doc[doc.panel==panel];ids=sorted(dd.seq_id.unique());bs=rng.integers(0,len(ids),(2000,len(ids)))
 for c in [x['condition'] for x in manifest['conditions']]:
  a=dd[dd.condition==c].set_index('seq_id').loc[ids];cr=next(x for x in manifest['conditions'] if x['condition']==c)
  for m in MET:
   v=a[m].to_numpy(float);lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);summary.append({'panel':panel,'condition':c,'metric':m,'mean':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':len(ids),'positions':int((df.panel==panel).sum()/21),'dimensions':cr['dimensions'],'reference_variance_fraction':cr['reference_variance_fraction']})
 for base in ['identity','k64']:
  for c in [x['condition'] for x in manifest['conditions'] if x['condition']!=base]:
   a=dd[dd.condition==c].set_index('seq_id').loc[ids];b=dd[dd.condition==base].set_index('seq_id').loc[ids]
   for m in ['NLL','KL_full','entropy','top1_agreement','top10_recovery','expected_log_frequency','freq_top1pct']:
    v=(a[m]-b[m]).to_numpy(float);lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);contrasts.append({'panel':panel,'condition':c,'baseline':base,'metric':m,'difference_condition_minus_baseline':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'n_documents':len(ids),'positive_documents':int(np.sum(v>1e-8)),'negative_documents':int(np.sum(v<-1e-8)),'near_equal_documents':int(np.sum(abs(v)<=1e-8))})
pd.DataFrame(summary).to_csv(E/'analysis/summary_metrics.csv',index=False);pd.DataFrame(contrasts).to_csv(E/'analysis/paired_contrasts.csv',index=False)
# Counterexamples to monotonic recovery, fixed comparisons, and top1-rank numerical audits.
wide=df.pivot(index='index',columns='condition',values='NLL');mon=[]
for panel in ['the','natural']:
 idx=[i for i,r in enumerate(pos) if r['panel']==panel]
 for a,b in zip(['k1','k4','k16','k64','k128','k256','k512','k768'],['k4','k16','k64','k128','k256','k512','k768','k1024']):
  v=wide.loc[idx,b]-wide.loc[idx,a];mon.append({'panel':panel,'from':a,'to':b,'NLL_worsens_positions':int((v>1e-6).sum()),'NLL_improves_positions':int((v<-1e-6).sum()),'positions':len(idx)})
pd.DataFrame(mon).to_csv(E/'analysis/nonmonotonic_positions.csv',index=False)
# Raw visible prefixes, named fixed examples, ordinary examples, and separately selected extrema.
lookup={(x['index'],x['condition']):x for x in outputs};fixed=[i for i,r in enumerate(pos) if r['fixed_example']];post=[]
for panel in ['the','natural']:
 idx=[i for i,r in enumerate(pos) if r['panel']==panel];delta=wide.loc[idx,'k256']-wide.loc[idx,'k64'];post.extend([int(delta.idxmin()),int(delta.idxmax())])
def safe(s):return s.replace('|','\\|').replace('\n','↵').replace('\r','')
text=['# 固定前文与原始输出\n','原生 block27 residual-post → 最终 RMSNorm → 冻结输出头。原始 ID／片段／概率不是完整词的语义标签。排名以严格更高 logit 的 ID 数加1计算；并列同分使用最小排名。前文之后的文字只用于语料描述，不进入本位置计算。\n']
for label,ii in [('预先固定展示',fixed),('事后极值：仅按 k256−k64 目标NLL最小／最大选择',list(dict.fromkeys(post)))]:
 text+=['\n## '+label+'\n']
 for i in ii:
  r=pos[i];following=r['future_description'] or next((a['following_source_preview'] for a in manifest['target_recovery'] if a['seq_id']==r['seq_id']),'');text += [f"\n### {r['position_uid']} · {r['topic']}\n",f"真实后继：ID **{r['target_id']}**，片段 **{safe(repr(r['target_fragment']))}**。原文：[来源]({r['url']})。\n",'完整可见前文：\n\n```text\n'+r['visible_prefix']+'\n```\n','\n原文后续（仅用于辨认完整拼写；未进入本位置输入）：`'+safe(following[:100])+'`\n','\n|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|\n|---|---|---:|---:|---:|---:|']
  for c in ['mean_only','k1','k4','k16','k64','middle','tail','head_middle','head_tail','k128','head_random1034','head_random1035','head_random1036','k256','k512','k768','k1024','identity']:
   z=lookup[i,c];top='；'.join(f"{t['id']} {safe(repr(t['fragment']))} {t['probability']:.4f}" for t in z['top20'][:3]);text += [f"|{c}|{top}|{z['target_probability']:.5f}|{z['target_rank']}|{z['NLL']:.4f}|{z['KL_full']:.4f}|"]
(E/'analysis/text_cases_cn.md').write_text('\n'.join(text)+'\n')
# Other documents checked without selecting their outputs. Deterministic hash rule selects one position/document and first4/domain.
validation=[]
for domain in ['math','biology','physics']:
 dd=[(i,r) for i,r in enumerate(pos) if r['panel']=='natural' and r['domain']==domain and r['seq_id'] not in manifest['fixed_examples']]
 dd=sorted(dd,key=lambda ir:hashlib.sha256(('R13-text-validation|'+ir[1]['position_uid']).encode()).hexdigest());seen=set()
 for i,r in dd:
  if r['seq_id'] in seen:continue
  seen.add(r['seq_id']);validation.append(i)
  if len(seen)==4:break
val=[]
for i in validation:
 r=pos[i];val.append({'position_uid':r['position_uid'],'visible_prefix':r['visible_prefix'],'true_target_id':r['target_id'],'true_target_fragment':r['target_fragment'],'metrics':{c:{k:lookup[i,c][k] for k in ['NLL','target_rank','top20']} for c in ['k1','k64','k256','identity']}})
dump(E/'analysis/unselected_text_validation.json',{'selection_rule':'SHA256 R13-text-validation|position_uid; first distinct4documents/domain, natural panel only, excluding all7 fixed-example documents; selection does not inspect output','cases':val})
# Descriptive domain and shared-document sensitivities use the same already frozen outputs.
strata=[]
shared=set(doc[doc.panel=='the'].seq_id)&set(doc[doc.panel=='natural'].seq_id)
for panel in ['the','natural']:
 for label,subset in [('all',doc[doc.panel==panel]),('shared_documents',doc[(doc.panel==panel)&doc.seq_id.isin(shared)])]+[(d,doc[(doc.panel==panel)&(doc.domain==d)]) for d in ['math','biology','physics']]:
  if subset.empty:continue
  for cond,aa in subset.groupby('condition'):
   for metric in ['NLL','KL_full','top1_agreement','entropy','expected_log_frequency','freq_top1pct','format_mass']:
    strata.append({'panel':panel,'stratum':label,'condition':cond,'metric':metric,'mean':float(aa[metric].mean()),'documents':aa.seq_id.nunique()})
pd.DataFrame(strata).to_csv(E/'analysis/stratified_metrics.csv',index=False)
diversity=[]
for panel in ['the','natural']:
 for cond in [x['condition'] for x in manifest['conditions']]:
  ids=[r['top20'][0]['id'] for r in outputs if r['condition']==cond and pos[r['index']]['panel']==panel]
  u,cnt=np.unique(ids,return_counts=True);j=cnt.argmax();diversity.append({'panel':panel,'condition':cond,'positions':len(ids),'distinct_top1_IDs':len(u),'modal_top1_ID':int(u[j]),'modal_top1_positions':int(cnt[j]),'modal_fraction':float(cnt[j]/len(ids))})
pd.DataFrame(diversity).to_csv(E/'analysis/top1_diversity.csv',index=False)
# Fixed illustrative raw outputs are selected evidence; complete raw outputs stay execution-side.
fixedraw=[r for r in outputs if r['index'] in fixed]
(P/'evidence/fixed_case_raw_outputs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in fixedraw))

# Source tables curated in project (all small, raw top20/hidden cache stay execution-side).
for name in ['summary_metrics.csv','paired_contrasts.csv','document_metrics.csv','nonmonotonic_positions.csv','text_cases_cn.md','unselected_text_validation.json','stratified_metrics.csv','top1_diversity.csv']:shutil.copy2(E/'analysis'/name,P/('text_cases_cn.md' if name=='text_cases_cn.md' else 'evidence/'+name))
print(pd.DataFrame(summary).query("metric in ['NLL','KL_full','entropy','top1_agreement','expected_log_frequency','freq_top1pct'] and condition in ['mean_only','k1','k64','k128','k256','k512','k1024','head_middle','head_tail']").pivot_table(index=['panel','condition'],columns='metric',values='mean').round(4).to_string())
