from pathlib import Path
import json,hashlib,sys
import numpy as np
E=Path(__file__).resolve().parents[1];sys.path.insert(0,str(E/'scripts'));import analyze as A
selected=[]
for flag in ['identifier_fragment','clock_fragment','recent_paragraph','non_ascii_letters']:
 pool=[]
 for d in A.DOC:
  if d['split']!='validation':continue
  lab=A.LABEL.iloc[d['row_start']:d['row_start']+128][flag].to_numpy(bool)
  for p,n in A.pairs(d,lab):
   key=hashlib.sha256(f'110208:{flag}:{d["doc_id"]}:{p}:{n}'.encode()).hexdigest();pool.append((key,d,int(p),int(n)))
 used=set()
 for key,d,p,n in sorted(pool,key=lambda x:x[0]):
  if d['host'] in used:continue
  used.add(d['host']);selected.append({'phenomenon':flag,'doc_id':d['doc_id'],'host':d['host'],'positive_row':d['row_start']+p,'negative_row':d['row_start']+n,'local_positive':p,'local_negative':n,'selection_hash':key})
  if len(used)==2:break
f=E/'data/band_example_pairs_input_only.json';payload={'selection':'fourdiscoveryoriginproperties;twofirsthashsame-tokenpairsindistincthosts;noresponseinput;notchosenforprettyresults','validation_effect_statistics_read':False,'pairs':selected}
if f.exists():assert json.load(open(f))==payload
else:f.write_text(json.dumps(payload,indent=2)+'\n')
if '--freeze-only' in sys.argv:print('INPUT_ONLY_BAND_CASES_FROZEN',len(selected));sys.exit()
P=dict(np.load(E/'analysis/pca.npz'));G=dict(np.load(E/'analysis/head_geometry.npz'));iso=np.sqrt(np.trace(G['Gc'])/151936/1024);needed={i for s in selected for i in [s['positive_row'],s['negative_row']]};texts={}
for l in (E/'data/positions.jsonl').open():
 p=json.loads(l)
 if p['row'] in needed:texts[p['row']]=p
out=['# 输入文字规则预定的谱现象真实案例','\n四条来自发现视图的文字属性，各取哈希排序最前的两个不同来源、同文档同token配对。样例选择不读取响应，不保证符合总体平均；缺少配对时不补漂亮例子。每个前文均截到当前token，不使用后文。以下变化包含两个真实前文的全部差异，不是只改变一个属性的最小干预。'];metrics=[]
for i,s in enumerate(selected):
 d=next(d for d in A.DOC if d['doc_id']==s['doc_id']);q=np.load(E/'cache'/(d['doc_id']+'.npz'));p=s['local_positive'];n=s['local_negative'];hp=q['h'][p].astype(float);hn=q['h'][n].astype(float);yp=q['y'][p].astype(float);yn=q['y'][n].astype(float);dh=hp-hn;dy=yp-yn;rms=float(np.sqrt(max(0,dy@G['Gc']@dy)/151936));gain=rms/max(np.linalg.norm(dy),1e-12);pc=dh@P['h_V'];fractions=[float(np.sum(pc[a:b]**2)/max(dh@dh,1e-20)) for a,b in A.BANDS];before=[]
 for h in [hp,hn]:
  proj=(h-P['h_mean'])@P['h_V'];before.append([float(np.sum(proj[a:b]**2)/max(np.sum((h-P['h_mean'])**2),1e-20)) for a,b in A.BANDS])
 s.update({'delta_h_norm':float(np.linalg.norm(dh)),'delta_y_norm':float(np.linalg.norm(dy)),'centered_logit_RMS':rms,'gain_over_isotropic':gain/iso,'delta_h_band_fractions':fractions,'positive_h_band_fractions':before[0],'negative_h_band_fractions':before[1]});metrics.append(s);pp=texts[s['positive_row']];nn=texts[s['negative_row']]
 out+=['\n## '+str(i+1)+'．'+A.NAMES[s['phenomenon']],f'\n文档`{d["doc_id"]}`，来源[{d["host"]}]({d["url"]})。当前位置分别{pp["position"]}和{nn["position"]}，相同片段`{pp["token_fragment"]}`，编号{pp["token_id"]}；相距{abs(pp["position"]-nn["position"])}个token。','\n属性为真的完整可见前文：\n\n```text\n'+pp['visible_prefix']+'\n```','\n属性为假的完整可见前文：\n\n```text\n'+nn['visible_prefix']+'\n```',f'\n原始向量差长度：h={np.linalg.norm(dh):.8g}，真实final norm后的y={np.linalg.norm(dy):.8g}；有效logit变化均方根={rms:.8g}；相对各向同性单位方向增益={gain/iso:.8g}倍。', '\n八个固定h谱段中的实际变化平方范数比例：'+', '.join(f'{v:.4%}' for v in fractions)+'。','\n现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：'+', '.join(f'{(a-b)*100:+.5f}个百分点' for a,b in zip(before[0],before[1]))+'。','\n反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。']
(E/'band_text_cases_cn.md').write_text('\n'.join(out)+'\n');(E/'analysis/band_case_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print('BAND_CASES',len(metrics),flush=True)
