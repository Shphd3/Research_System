from pathlib import Path
import json,shutil
import pandas as pd
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);RR=[json.loads(s) for s in (E/'data/positions.jsonl').read_text().splitlines()];rs=[json.loads(s) for s in (E/'analysis/fixed_case_outputs.jsonl').read_text().splitlines()];lookup={(r['index'],r['layer'],r['scope'],r['condition']):r for r in rs}
# Reuse existing mean-only text controls to avoid attributing suffix/context output to a tiny band.
meanrefs={};inherited=[]
R=Path(c['parent_round'])
for sid in sorted({RR[i]['seq_id'] for i in c['fixed_cases']}):
 old=json.load(open(R/'analysis/chunks'/(sid+'.json')))
 for r in old['records']:
  if r['index'] in c['fixed_cases'] and r['condition']=='mean_only' and r['readout']=='continuation':
   r['top10']=sorted(r['top10'],key=lambda t:(-t['probability'],t['id']));r['source']='R16_REUSED_EXACT';meanrefs[(r['index'],r['layer'],r['scope'])]=r;inherited.append(r)
with (E/'analysis/fixed_mean_only_outputs.jsonl').open('w') as f:
 for r in inherited:f.write(json.dumps(r,ensure_ascii=False)+'\n')
def token(t):return repr(t['fragment']).replace('|','\\|').replace('`','\\`')+f" [ID {t['id']}] {100*t['probability']:.3f}%"
lines=['# 固定真实文本：等维谱段与均值对照','','9例沿用R16预先固定位置，不按本轮结果筛选。下列前文是本次输入窗口内、模型在目标位置能够看到的完整文本；真实后继只作为评估目标，不作为输入。位置编号属于192-token窗口。所有输出均继续运行剩余网络；不是中间层直接输出头读出。token片段不代表完整词。','', '主表固定展示第1、14、25、28层，全部28层前10候选见执行侧 fixed_case_outputs.jsonl；所有位置前10精确ID/概率保存在按文档压缩NPZ。','']
for idx in c['fixed_cases']:
 r=RR[idx];base=lookup[(idx,0,'none','identity')];lines += [f"## index {idx} / {r['position_uid']}",'',f"当前位置：0基{r['position']}／第{r['position']+1}个token；ID{r['input_id']}，片段{repr(r['input_fragment'])}。真实后继：ID{r['target_id']}，片段{repr(r['target_fragment'])}。",'', '```text',r['visible_prefix'],'```','', '完整模型前10候选：'+'；'.join(token(t) for t in base['top10'])+'。',f"真实后继概率{100*base['target_probability']:.5f}%，排名{int(base['target_rank'])}，负对数概率{base['NLL']:.5f}nat。",'']
 for scope,title in [('target_only','只改当前位置'),('all_prefix','改整个前缀')]:
  lines += [f'### {title}','']
  for l in [1,14,25,28]:
   mean=meanrefs[(idx,l,scope)]
   lines += [f'第{l}层：','', '旧结果仅均值参照：'+token(mean['top10'][0])+f"；真实后继概率{100*mean['target_probability']:.5f}%。",'', '|保留主成分|加回均值：实际首选|不加均值：实际首选|真实后继概率：加／不加|', '|---|---|---|---|']
   for b in range(16):
    a=lookup[(idx,l,scope,f'add_b{b:02d}')];n=lookup[(idx,l,scope,f'no_b{b:02d}')];lines.append(f"|{64*b+1}—{64*b+64}|{token(a['top10'][0])}|{token(n['top10'][0])}|{100*a['target_probability']:.5f}%／{100*n['target_probability']:.5f}%|")
   lines.append('')
(E/'casebook_cn.md').write_text('\n'.join(lines)+'\n');shutil.copy2(E/'casebook_cn.md',P/'casebook_cn.md')
S=pd.read_csv(E/'analysis/summary_metrics.csv');S=S[(S.panel=='natural')&(S.group=='ALL')]
lines=['# 原始汇总读数：所有16段、固定4层','','每格为“加回均值保持率／不加均值保持率”，单位%。175文档、700位置，先文档内平均再文档等权。完整28层、区间、损失、能量见 evidence/summary_metrics.csv；逐位置原始数据位于执行侧。','']
for scope,title in [('target_only','只改当前位置'),('all_prefix','改整个前缀')]:
 lines += [f'## {title}','','|主成分区间|第1层|第14层|第25层|第28层|','|---|---:|---:|---:|---:|']
 for b in range(16):
  vals=[]
  for l in [1,14,25,28]:
   a=S[(S.layer==l)&(S.scope==scope)&(S.condition==f'add_b{b:02d}')].iloc[0];n=S[(S.layer==l)&(S.scope==scope)&(S.condition==f'no_b{b:02d}')].iloc[0];vals.append(f'{100*a.top1_agreement:.2f}／{100*n.top1_agreement:.2f}')
  lines.append('|'+f'{64*b+1}—{64*b+64}'+'|'+'|'.join(vals)+'|')
 lines.append('')
(E/'matrix_cn.md').write_text('\n'.join(lines)+'\n');shutil.copy2(E/'matrix_cn.md',P/'matrix_cn.md')
print('CASEBOOK_DONE')
