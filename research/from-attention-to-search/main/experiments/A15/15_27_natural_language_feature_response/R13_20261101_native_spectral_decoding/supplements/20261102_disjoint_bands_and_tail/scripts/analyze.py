import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,shutil,collections
import numpy as np,pandas as pd
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements')/P.name;O=E.parents[1]
assert (E/'terminal_receipt.json').exists();M=json.load(open(E/'manifest.json'));ctx=[json.loads(l) for l in (E/'analysis/contexts.jsonl').read_text().splitlines()];contexts={r['index']:r for r in ctx};old=[json.loads(l) for l in (O/'analysis/raw_outputs.jsonl').read_text().splitlines()];base=[r for r in old if r['index'] in contexts and r['condition'] in ['identity','mean_only','k64']];records=[r for p in sorted((E/'analysis/chunks').glob('*.json')) for r in json.load(open(p))['records'] if r['index'] in contexts];assert len(records)==7700;out=records+base;lookup={(r['index'],r['condition']):r for r in out};F=np.load(O/'data/frequency.npz');rows=[];basecols=['NLL','KL_full','entropy','top1_agreement','top10_recovery','top1_correct','target_probability','target_rank','format_mass','expected_log_frequency']
for r in out:
 i=r['index'];c=contexts[i];y=c['target_id'];g='format' if F['format_mask'][y] else 'common_nonformat' if F['group'][y]==0 else 'other_nonformat';z={k:r[k] for k in basecols};z.update(index=i,position_uid=c['position_uid'],seq_id=c['seq_id'],domain=c['domain'],condition=r['condition'],position_zero_based=c['position_zero_based'],position_one_based=c['position_one_based'],input_id=c['input_id'],target_id=y,target_group=g,freq_top1pct=r['frequency_mass'][0],output_top1_id=r['top20'][0]['id'],output_top1_fragment=r['top20'][0]['fragment'],output_top1_probability=r['top20'][0]['probability']);z.update({k:r.get(k) for k in ['shuffle_eligible','same_token_other_document_NLL','real_context_NLL_gain','centered_energy_fraction','target_NLL_improvement_vs_mean']});rows.append(z)
df=pd.DataFrame(rows);df.to_csv(E/'analysis/position_metrics.csv',index=False);(E/'analysis/raw_outputs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out));doc=df.groupby(['seq_id','domain','condition'])[basecols+['freq_top1pct','centered_energy_fraction','target_NLL_improvement_vs_mean']].mean().reset_index();doc.to_csv(E/'analysis/document_metrics.csv',index=False)
rng=np.random.default_rng(20261104);summary=[];control=[]
for co,z in doc.groupby('condition',sort=False):
 n=len(z);bs=rng.integers(0,n,(2000,n))
 for metric in basecols+['freq_top1pct','centered_energy_fraction','target_NLL_improvement_vs_mean']:
  v=z[metric].to_numpy(float)
  if not np.isfinite(v).all():continue
  lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);summary.append({'condition':co,'metric':metric,'mean':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':n,'positions':700})
for conf in M['bands']:
 co=conf['condition'];z=df[(df.condition==co)&(df.shuffle_eligible==True)]
 for g in ['all','format','common_nonformat','other_nonformat']:
  zz=z if g=='all' else z[z.target_group==g]
  if zz.empty:continue
  d=zz.groupby('seq_id').real_context_NLL_gain.mean();v=d.to_numpy();n=len(v);bs=rng.integers(0,n,(2000,n));lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);control.append({'condition':co,'target_group':g,'mean_NLL_gain_real_vs_same_token_other_document':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':n,'positions':len(zz),'positive_documents':int(np.sum(v>0)),'negative_documents':int(np.sum(v<0))})
pd.DataFrame(summary).to_csv(E/'analysis/summary_metrics.csv',index=False);pd.DataFrame(control).to_csv(E/'analysis/context_controls.csv',index=False)
B=np.load(O/'data/bases.npz');ev=B['eigenvalues'];spec=[]
for c in M['bands']:
 lo,hi=c['numpy_slice'];spec.append({**c,'reference_variance_fraction':float(ev[lo:hi].sum()/ev.sum())})
pd.DataFrame(spec).to_csv(E/'analysis/band_definitions.csv',index=False)
counts=[]
for (co,i),z in df.groupby(['condition','output_top1_id']):counts.append({'condition':co,'token_id':int(i),'fragment':z.iloc[0].output_top1_fragment,'positions':len(z),'documents':z.seq_id.nunique(),'mean_probability_on_selected_positions':float(z.output_top1_probability.mean())})
pd.DataFrame(counts).sort_values(['condition','positions','token_id'],ascending=[True,False,True]).to_csv(E/'analysis/output_top1_counts.csv',index=False)
# Completecasebooks show each realvisibleprefix once andallbandoutputs for thatsameposition.
conds=[c['condition'] for c in M['bands']]+['mean_only','identity'];names={c['condition']:f"PC{c['PC_start_one_based']}–{c['PC_stop_exclusive_one_based']-1}（{c['dimensions']}维）" for c in M['bands']};names.update(mean_only='仅训练均值',identity='原模型',k64='前64维')
def probstr(p):return f'{100*p:.2e}%' if p<1e-5 else f'{100*p:.5f}%'
def esc(s):return s.replace('|','\\|').replace('\n','[换行]').replace('\r','')
def section(c,neighborhood=False):
 i=c['index'];ls=[f"\n## {c['position_uid']}\n",f"输入文档：{c['seq_id']}；领域：{c['domain']}／{c['topic']}；来源：[原始来源]({c['url']})。",f"**当前输入token：ID{c['input_id']}，片段 `{esc(repr(c['input_fragment']))}`；0基位置t={c['position_zero_based']}，即第{c['position_one_based']}个token。可见输入共{c['visible_token_count']}个token。**",'当前句子／段落已经可见的部分：\n\n> '+c['current_visible_sentence_or_paragraph'].replace('\n','\n> '),'全部可见输入（没有省略号；到当前token为止）：\n\n```text\n'+c['visible_prefix']+'\n```',f"在此预测下一个token。真实后继：ID{c['target_id']}，片段 `{esc(repr(c['target_fragment']))}`。后继是语料参考，不等于原模型一定首选。"]
 if neighborhood:
  ls+=['\n|0基位置|第几个token|ID|片段|是否已见|标记|','|---:|---:|---:|---|---|---|']
  for t in c['token_neighborhood']:ls.append(f"|{t['position_zero_based']}|{t['position_one_based']}|{t['token_id']}|`{esc(repr(t['decoded_fragment']))}`|{'是' if t['visible_at_target'] else '否'}|{'当前输入' if t['selected_input'] else '真实后继' if t['actual_successor'] else ''}|")
 ls+=['\n|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|','|---|---|---:|---:|---:|---:|']
 for co in conds:
  x=lookup[i,co];top='；'.join(f"{t['id']} `{esc(repr(t['fragment']))}` {100*t['probability']:.3f}%" for t in x['top20'][:3]);ls.append(f"|{names[co]}|{top}|{probstr(x['target_probability'])}|{x['target_rank']}|{x['NLL']:.4f}|{x['KL_full']:.4f}|")
 ls+=['\n原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：\n\n```text\n'+c['original_sentence_reference_only_not_all_seen']+'\n```']
 return '\n\n'.join(ls)
header='# 固定自然文本：完整输入、token位置与分段解码\n\n所有解码为在同一当前位置的下一token分布，不是把各位置首选拼成自回归生成。区间单独保留并加回训练均值；当前位置t读到x_t后预测x_(t+1)。输入句子可能尚未结束，原文后续仅参考。'
fixed=[c for c in ctx if c['position_uid'] in M['all_fixed_cases']];(P/'casebook_cn.md').write_text(header+'\n'+''.join(section(c,True) for c in fixed)+'\n');shutil.copy2(P/'casebook_cn.md',E/'casebook_cn.md')
folder=E/'all_contexts';folder.mkdir(exist_ok=True);index=['# 全部700自然位置：完整语境与解码\n','每个条目有准确输入token／位置、全部可见前文、11个独立谱段及原模型／均值输出。可见前文与原文后续分开。位置不是独立文档。\n']
for domain in ['math','biology','physics']:
 cc=[c for c in ctx if c['domain']==domain];file=folder/(domain+'_all_positions_cn.md');file.write_text(header+'\n'+''.join(section(c) for c in cc)+'\n');index.append(f"- [{domain}：{len(cc)}位置]({file.name})\n")
(folder/'index_cn.md').write_text('\n'.join(index))
(P/'all_contexts_cn.md').write_text('# 全部自然位置的完整输入与输出\n\n[全部700位置分领域入口]('+str(folder/'index_cn.md')+')。完整原始逐token窗口和当前位置索引：[contexts.jsonl]('+str(E/'analysis/contexts.jsonl')+')。\n\n[项目内固定12例](casebook_cn.md)提供相同格式的精读材料；其中三例在看本轮输出前固定为主图。\n')
# Actualallcontextinputwindowsaredurable; no trainingornewlabelisintroduced.
for f in ['summary_metrics.csv','context_controls.csv','band_definitions.csv','output_top1_counts.csv','document_metrics.csv']:shutil.copy2(E/'analysis'/f,P/'evidence'/f)
print(pd.DataFrame(summary).query("metric in ['NLL','KL_full','entropy','top1_agreement','target_NLL_improvement_vs_mean']").pivot_table(index='condition',columns='metric',values='mean').round(4).to_string());print(pd.DataFrame(control).query("target_group=='all'").round(4).to_string(index=False));print('casebooksbytes',[(x.name,x.stat().st_size) for x in folder.glob('*.md')])
