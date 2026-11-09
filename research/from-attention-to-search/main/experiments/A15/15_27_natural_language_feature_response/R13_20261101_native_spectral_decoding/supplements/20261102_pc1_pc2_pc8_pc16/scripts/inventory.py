import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
import json,collections,sys,shutil
import numpy as np,pandas as pd
sys.path.insert(0,'/data/250010109/dependency_packages/hf_transformers_qwen3');from tokenizers import Tokenizer
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements')/P.name;O=E.parents[1]
f=np.load(O/'data/frequency.npz');tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');groups=pd.read_csv(O/'analysis/recovery_group_members.csv');positions=[json.loads(l) for l in (O/'data/native_positions.jsonl').read_text().splitlines()];output=[]
needed=set(np.flatnonzero(f['valid'] & ((f['group']==0)|f['format_mask'])).tolist())|set(groups.full_top1_id.astype(int))
for i in sorted(needed):
 g='format' if f['format_mask'][i] else 'nonformat_common' if f['group'][i]==0 else 'nonformat_other';output.append({'token_id':int(i),'fragment':tok.decode([int(i)],skip_special_tokens=False),'reference_count':int(f['counts'][i]),'format':bool(f['format_mask'][i]),'reference_top1pct':bool(f['group'][i]==0),'class':g})
ref=pd.DataFrame(output);ref[ref['class'].isin(['format','nonformat_common'])].sort_values(['class','reference_count','token_id'],ascending=[True,False,True]).to_csv(E/'evidence/reference_group_IDs_complete.csv',index=False)
obs=[]
for (panel,g,i),z in groups.groupby(['panel','recovery_group','full_top1_id']):
 row=ref[ref.token_id==i].iloc[0];n=int(z.shape[0]);obs.append({'panel':panel,'group':g,'token_id':int(i),'fragment':row['fragment'],'positions':n,'documents':z.seq_id.nunique(),'reference_count':int(row['reference_count'])})
obs=pd.DataFrame(obs).sort_values(['panel','group','positions','token_id'],ascending=[True,True,False,True]);obs.to_csv(E/'evidence/observed_original_top1_IDs_complete.csv',index=False)
# Exactly which original predictions survive PC1/PC16, available before new GPU conditions.
old=[json.loads(l) for l in (O/'analysis/raw_outputs.jsonl').read_text().splitlines()];keep=[]
for x in old:
 if x['condition'] not in ['k1','k16']:continue
 r=positions[x['index']];full=groups[groups['index']==x['index']].iloc[0];keep.append({'panel':r['panel'],'seq_id':r['seq_id'],'position':r['position'],'condition':x['condition'],'group':full.recovery_group,'original_ID':int(full.full_top1_id),'original_fragment':full.full_top1_fragment,'projected_ID':x['top20'][0]['id'],'projected_fragment':x['top20'][0]['fragment'],'retained':bool(x['top1_agreement'])})
pd.DataFrame(keep).to_csv(E/'evidence/old_condition_membership.csv',index=False)
lines=['# 常见ID和空白／标点究竟是什么','\n这是token ID分组；空格前缀、大小写、子词分别计ID。符号组是Unicode标点或空白组成的片段，数学符号不自动加入。常见组是参考词频最高1% ID，再排除符号组，并不保证是完整英文词。','\n参考全集：常见非格式'+str(int(np.sum(f['valid']&(f['group']==0)&~f['format_mask'])))+'个ID；符号／空白'+str(int(np.sum(f['format_mask'])))+'个ID。完整全集见reference_group_IDs_complete.csv。']
for panel in ['natural','the']:
 for g,title in [('nonformat_common','常见ID（排除标点空白）'),('format','空白／标点')]:
  a=obs[(obs.panel==panel)&(obs.group==g)];lines+=['\n## '+panel+'：'+title,f'实际原模型首选涉及{len(a)}个不同ID、{int(a.positions.sum())}个位置。文档可跨组，不能相加。','|ID|可读片段（repr保留空格／转义）|位置数|文档数|独立训练参考次数|','|---:|---|---:|---:|---:|']
  for r in a.to_dict('records'):lines.append(f"|{r['token_id']}|`{repr(r['fragment']).replace('|','/')} `|{r['positions']}|{r['documents']}|{r['reference_count']}|")
(P/'inventory_cn.md').write_text('\n'.join(lines)+'\n');shutil.copy2(P/'inventory_cn.md',E/'inventory_cn.md')
for p in (E/'evidence').glob('*.csv'):shutil.copy2(p,P/'evidence'/p.name)
print('reference counts',ref['class'].value_counts().to_dict())
for panel in ['natural','the']:
 for g in ['nonformat_common','format']:
  a=obs[(obs.panel==panel)&(obs.group==g)];print(panel,g,len(a),'IDs',int(a.positions.sum()),'positions');print(a.head(24).to_string(index=False))
