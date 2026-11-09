from pathlib import Path
import json,collections,hashlib
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));F=json.load(open(E/'validation_selection_frozen.json'));names=json.load(open(E/'data/phenomenon_definitions_v1p2.json'))['name'];docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines()];labels=pd.read_json(E/'data/labels_effective_v1p2.jsonl',lines=True);selected=[];eligibility=[];matched=pd.read_csv(E/'analysis/validation_matched_positions.csv');partners={}
for _,r in matched.iterrows():partners[(r.phenomenon,int(r.positive_row))]=int(r.negative_row);partners[(r.phenomenon,int(r.negative_row))]=int(r.positive_row)
# Rule fixed: strongest positive, strongest non-property response and weakest property response; diagnostic cases,not prevalence estimates.
for explanation in F['selected_explanations']:
 flag=explanation['phenomenon'];feat=int(explanation['response'].split('_')[1]);j=cfg['candidate_features'].index(feat);pool=[]
 for d in docs:
  if d['split']!='validation':continue
  z=np.load(E/'cache'/(d['doc_id']+'.npz'))['z_selected'][:,j]
  for ix,v in enumerate(z):
   row=d['row_start']+ix
   if (flag,row) not in partners:continue
   pool.append({'phenomenon':flag,'feature':feat,'doc_id':d['doc_id'],'host':d['host'],'row':row,'response':float(v),'property_present':bool(labels.iloc[row][flag]),'paired_other_response':float(z[partners[(flag,row)]-d['row_start']])})
 modes=[('support_high_response',[x for x in pool if x['property_present']],True),('counter_high_without_property',[x for x in pool if not x['property_present']],True),('counter_low_with_property',[x for x in pool if x['property_present']],False)] if explanation['effect_discovery']>0 else [('support_low_with_property',[x for x in pool if x['property_present']],False),('counter_high_with_property',[x for x in pool if x['property_present']],True),('counter_low_without_property',[x for x in pool if not x['property_present']],False)]
 for kind,sub,reverse in modes:
  if kind=='support_high_response':sub=[x for x in sub if x['response']>x['paired_other_response']]
  if kind=='support_low_with_property':sub=[x for x in sub if x['response']<x['paired_other_response']]
  if not sub:eligibility.append({'phenomenon':flag,'feature':feat,'slot':kind,'status':'NOT_FOUND_PREDICTED_DIRECTION_CASE'});continue
  if sub:
   x=sorted(sub,key=lambda x:((-x['response'] if reverse else x['response']),x['row']))[0].copy();x['case_type']=kind;x['partner_row']=partners[(flag,x['row'])]
   if kind in ['support_high_response','counter_high_without_property','counter_high_with_property'] and x['response']<=0:eligibility.append({'phenomenon':flag,'feature':feat,'slot':kind,'status':'NOT_FOUND_NONZERO_RESPONSE'});continue
   selected.append(x)
# Explicit unexplained case: first fixed candidate that has no frozen proposed interpretation; highest discovery response,not validation search.
cards=[json.loads(l) for l in (E/'analysis/discovery_cards.jsonl').read_text().splitlines()];named={'feature_'+str(int(x['response'].split('_')[1])) for x in F['selected_explanations']}
for x in cards:
 if x.get('object')=='feature_6743' and x.get('level')=='high' and 'row' in x:
  selected.append({'phenomenon':'UNEXPLAINED','feature':int(x['object'].split('_')[1]),'row':x['row'],'doc_id':x['doc_id'],'host':x['host'],'response':x['response'],'case_type':'discovery_unexplained_fixed_member'});break
needed={x['row'] for x in selected}|{x['partner_row'] for x in selected if 'partner_row' in x};index={row:{} for row in needed}
for line in (E/'data/positions.jsonl').open():
 p=json.loads(line)
 if p['row'] in index:index[p['row']]['position_metadata']=p
# Same row can serve different explanation; fill using exact row map.
Geom=dict(np.load(E/'analysis/head_geometry.npz'));PCA=dict(np.load(E/'analysis/pca.npz'));iso=json.load(open(E/'analysis/head_gain_reference.json'))['isotropic_centered_logit_RMS_per_unit_delta_y']
for x in selected:
 x['position_metadata']=index[x['row']]['position_metadata']
 if 'partner_row' not in x:continue
 x['partner_metadata']=index[x['partner_row']]['position_metadata'];doc=next(d for d in docs if d['doc_id']==x['doc_id']);cache=np.load(E/'cache'/(x['doc_id']+'.npz'));a=x['row']-doc['row_start'];b=x['partner_row']-doc['row_start'];dy=cache['y'][a].astype(float)-cache['y'][b].astype(float);dh=cache['h'][a].astype(float)-cache['h'][b].astype(float);rms=float(np.sqrt(max(0,dy@Geom['Gc']@dy)/151936));yn=float(np.linalg.norm(dy));gain=rms/max(yn,1e-12);x.update({'actual_pair_delta_h_norm':float(np.linalg.norm(dh)),'actual_pair_delta_y_norm':yn,'actual_pair_centered_logit_RMS':rms,'actual_pair_gain':gain,'actual_pair_gain_over_isotropic':gain/iso,'partner_feature_response':float(cache['z_selected'][b,cfg['candidate_features'].index(x['feature'])])})
(E/'analysis/text_case_slot_eligibility.json').write_text(json.dumps(eligibility,ensure_ascii=False,indent=2)+'\n')
(E/'analysis/text_case_selection.json').write_text(json.dumps({'selection_rule':'result-selected diagnostics explicitly named;allfixedvalidationtestsretained;not representative samples','cases':selected},ensure_ascii=False,indent=2)+'\n')
T=['# R15真实文本：支持例、反例与未解释例','\n以下是按公开规则选出的诊断例，不代替总体统计。正例按发现阶段关联方向，取验证集符合现象的高响应或低响应位置；反例同时保留与该预测不符或不具专属性的位置。正方向的高响应槽位要求非零，找不到时明确记未找到。无法解释例按发现精读固定为成员6743：screw、choked等高响应前文没有得到一致可复查命名，不依据验证结果另挑。四个正式feature候选整体未通过验证；这里的正例只指与发现方向一致的个别配对，不表示功能解释成立。完整可见前文保留到当前token为止；没有用后文命名。','\n文字片段编号是分词器整数；feature编号是字典成员整数；两者不是同一类对象。片段可能不是完整词。']
for i,x in enumerate(selected):
 p=x['position_metadata'];d=next(d for d in docs if d['doc_id']==p['doc_id']);flag=x['phenomenon'];T+=['\n## '+str(i+1)+'．'+names.get(flag,'未获解释的固定成员')+'／'+x['case_type'],f'\n文档`{d["doc_id"]}`；位置{p["position"]}；来源[{d["host"]}]({d["url"]})；{p["split"]}；完整来源行{d["source_line"]}。当前片段`{p["token_fragment"]}`，文字片段编号{p["token_id"]}；成员{ x["feature"] }，系数{x["response"]:.8g}。', '\n完整可见前文：\n\n```text\n'+p['visible_prefix']+'\n```']
 if flag!='UNEXPLAINED':
  pm=x['partner_metadata'];T+=['\n同文档、相同当前文字片段的匹配参照（当前位置'+str(pm['position'])+'；成员系数'+str(x['partner_feature_response'])+'）：\n\n```text\n'+pm['visible_prefix']+'\n```',f'\n这对真实上下文的变化：归一化前向量差长度{x["actual_pair_delta_h_norm"]:.6g}，归一化后长度{x["actual_pair_delta_y_norm"]:.6g}，去共同平移后的logit均方根变化{x["actual_pair_centered_logit_RMS"]:.6g}；单位归一化后变化的输出增益{x["actual_pair_gain"]:.6g}，相对各向同性方向参照{x["actual_pair_gain_over_isotropic"]:.4g}倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。']
  T+=['\n可复查属性：'+names[flag]+'。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为'+str(x['property_present'])+'。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。']
 else:T+=['\n本例没有满足冻结解释选择的名称。保留原始响应及上下文，不从一个片段猜测该成员的功能。']
(E/'text_cases_cn.md').write_text('\n'.join(T)+'\n');print('CASES',len(selected),flush=True)
