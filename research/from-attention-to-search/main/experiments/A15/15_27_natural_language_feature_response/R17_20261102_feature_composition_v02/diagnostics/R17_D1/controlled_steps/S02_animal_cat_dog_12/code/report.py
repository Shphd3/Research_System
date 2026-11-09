from pathlib import Path
import json,hashlib,math,datetime,shutil,sys,ast
import pandas as pd
R=Path(__file__).resolve().parents[1];S=Path('/data/250010109/Research_System');E=S/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S02_animal_cat_dog_12';D1=E.parents[1]
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rows(p):return [json.loads(l)for l in Path(p).open()if l.strip()]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def table(x):return pd.DataFrame(x).to_markdown(index=False,floatfmt='.6f')
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n')
receipt=json.load(open(R/'evidence/completed.json'));assert receipt['status']=='COMPLETED_S02_WAIT_FOR_JOINT_REVIEW';plan=json.load(open(R/'frozen_plan.json'));panel=rows(R/'data/panel.jsonl');raw=rows(R/'results/raw_scores.jsonl');tokenized=rows(R/'data/prompts_tokenized.jsonl');assert len(panel)==12 and len(raw)==13;P={x['id']:x for x in panel};T={x['id']:x for x in tokenized};dec=[];cs=[]
for r in raw:
 t=T[r['id']];assert t['prefix']==r['prefix']and t['prefix_token_ids']==r['prefix_token_ids'];assert [c['label']for c in r['candidates']]==['cat','dog']
 for c,tc in zip(r['candidates'],t['candidates']):
  assert c['candidate']==tc['text']and c['candidate_token_ids']==tc['candidate_token_ids'];assert c['candidate_tokens']==len(c['candidate_token_ids'])==len(c['token_logprobs']);assert abs(math.fsum(c['token_logprobs'])-c['total_logprob'])<1e-10;assert all(math.isfinite(x)and x<=0 for x in c['token_logprobs']);cs.append(dict(id=r['id'],family=r['family'],gold=r['gold'],candidate=c['candidate'],label=c['label'],token_ids=json.dumps(c['candidate_token_ids']),tokens=c['candidate_tokens'],sequence_logprob=c['total_logprob']))
 a,b=[x['total_logprob']for x in r['candidates']];assert abs((a-b)-r['delta_cat_minus_dog'])<1e-10;assert r['choice']==('cat'if a>=b else'dog');assert r['correct']==(None if r['gold']is None else r['choice']==r['gold'])
 if r['gold']is not None:
  assert r['gold']==P[r['id']]['fine_label'];dec.append(dict(id=r['id'],family=r['family'],coarse='animal',gold=r['gold'],S_cat=a,S_dog=b,delta_cat_minus_dog=a-b,choice=r['choice'],correct=r['correct'],text=r['text'],prefix=r['prefix']))
D=pd.DataFrame(dec);C=pd.DataFrame(cs);assert len(D)==12 and len(C)==26;D.to_csv(R/'results/decisions.csv',index=False);C.to_csv(R/'results/candidate_scores.csv',index=False)
pairs=[]
for fid,t in D.groupby('family'):
 a=t[t.gold=='cat'].iloc[0];b=t[t.gold=='dog'].iloc[0];pairs.append(dict(family=fid,cat_choice=a.choice,dog_choice=b.choice,cat_delta=a.delta_cat_minus_dog,dog_delta=b.delta_cat_minus_dog,choice_changed=a.choice!=b.choice,both_correct=bool(a.correct and b.correct),reversed_switch=a.choice=='dog'and b.choice=='cat'))
Q=pd.DataFrame(pairs);Q.to_csv(R/'results/pairs.csv',index=False);counts=[dict(class_label=k,correct=int(D[D.gold==k].correct.sum()),N=6)for k in ['cat','dog']];counts.append(dict(class_label='all',correct=int(D.correct.sum()),N=12));pd.DataFrame(counts).to_csv(R/'results/counts.csv',index=False)
neutral=next(x for x in raw if x['id']=='neutral');C[C.id=='neutral'].to_csv(R/'results/neutral.csv',index=False);errors=D[~D.correct];errors.to_csv(R/'results/errors.csv',index=False);ncorrect=int(D.correct.sum());nswitch=int(Q.choice_changed.sum());nboth=int(Q.both_correct.sum());nreverse=int(Q.reversed_switch.sum())
summary=dict(correct=ncorrect,N=12,cat_correct=counts[0]['correct'],dog_correct=counts[1]['correct'],pairs=6,changed_choice_pairs=nswitch,both_correct_pairs=nboth,reversed_switch_pairs=nreverse,neutral_choice=neutral['choice'],neutral_cat_minus_dog=neutral['delta_cat_minus_dog'],errors=len(errors));dump(R/'results/summary.json',summary)
for name,digest in plan['data_SHA256'].items():assert sha(R/'data'/name)==digest
assert sha(R/'frozen_plan.json')==receipt['frozen_plan_SHA256'];assert sha(R/'results/raw_scores.jsonl')==receipt['raw_scores_SHA256'];assert datetime.datetime.fromisoformat(plan['frozen_UTC'])<=datetime.datetime.fromisoformat(receipt['started_UTC'])
oldfiles=json.load(open(R/'evidence/S01_immutable_before.json'))
for p,digest in oldfiles.items():assert sha(p)==digest,p
check=dict(status='PASS',prefixes=13,test_rows=12,pairs=6,candidate_sequences=26,all_token_sums_argmax_labels_and_deltas_replayed=True,exact_prefix_and_candidate_tokenization_matches=True,frozen_before_responses=True,model_and_tokenizer_same_as_S01=True,old_S01_files_unchanged=len(oldfiles),max_duplicate_lane_error=receipt['max_duplicate_lane_difference'],training=0,dictionary_loads=0,feature_hooks=0,probe_fits=0,formats=1,nextstep='NOT_RUN_WAIT_FOR_REVIEW');dump(R/'evidence/verification.json',check)
# Complete casebook, not a favorable subset.
case=['# 12条原文、前缀与完整候选分数','每条的类别标签均为animal加cat或dog。精确候选固定为ASCII前导空格加cat/dog及句号：`" cat."`、`" dog."`。分数为全部候选token的条件自然对数概率总和，越大越优，差值定义S_cat−S_dog。表显示6位小数，JSONL保留完整精度和逐token分数。','[中文小结](summary_cn.md) · [原始记录](results/raw_scores.jsonl) · [精确token拼接](data/prompts_tokenized.jsonl)']
for fid in sorted(D.family.unique()):
 case.append('## '+fid)
 for p in [x for x in panel if x['family']==fid]:case += ['### '+p['id']+' — 标签 '+json.dumps(p['labels']),'原文：\n\n```text\n'+p['text']+'\n```','完整续写前缀（候选紧接末尾a）：\n\n```text\n'+p['prefix']+'\n```']
 t=D[D.family==fid];case += [table(t[['gold','S_cat','S_dog','delta_cat_minus_dog','choice','correct']]),table([dict(id=r['id'],candidate=json.dumps(c['candidate']),token_ids=json.dumps(c['candidate_token_ids']),tokens=c['candidate_tokens'],sequence_logprob=c['total_logprob'])for r in raw if r['family']==fid for c in r['candidates']])]
case += ['## 唯一中性前缀','```text\n'+neutral['prefix']+'\n```',table(C[C.id=='neutral']),f"差值={neutral['delta_cat_minus_dog']:.9f}；首选={neutral['choice']}。没有正确标签，不计入12条准确率，不校正其他分数。"]
write(E/'casebook_cn.md','\n\n'.join(case))
errtext=['# 全部错误记录',f'错误数：{len(errors)}/12。']
if errors.empty:errtext.append('本轮12条均正确，没有错误例；不额外造例或另试提示。')
else:
 for _,r in errors.iterrows():errtext += ['## '+r.id,'```text\n'+r.prefix+'\n```',table([dict(gold=r.gold,S_cat=r.S_cat,S_dog=r.S_dog,delta=r.delta_cat_minus_dog,choice=r.choice)])]
write(E/'errors_cn.md','\n\n'.join(errtext))
first=D[D.family=='F01'];firsttexts='\n\n'.join('```text\n'+p['prefix']+'\n```'for p in panel if p['family']=='F01');cand=[dict(candidate=json.dumps(c['candidate']),token_ids=json.dumps(c['candidate_token_ids']),tokens=c['candidate_tokens'],neutral_sequence_logprob=c['total_logprob'])for c in neutral['candidates']]
observation=(f'本固定续写格式下，12条全部正确，6组均随明确的cat/dog词变化而向正确方向改变首选。'if ncorrect==12 and nboth==6 else f'本固定格式下正确{ncorrect}/12，{nboth}/6组两条均正确；失败样本完整保留，未继续搜索提示。')
cn=f'''# S02：animal—cat/dog普通语言续写检查

**{observation}** 本步已完成并停止，等待共同审阅。只有一种事先冻结的续写格式，没有追加prompt或数据。

## 目的与S01的关系

S01方阵三选一的两格式大多固定选否／是，中性前缀也有相似偏好。本步按用户指定，改用明确animal+cat/dog的短英文文本及二候选续写，只检查同一冻结模型能否随明示类别改变后续偏好。方阵实验原文、脚本、分数和结论均保留，核验{len(oldfiles)}个原文件SHA不变；没有修改研究假设。

两轮同时改变了概念、语言、任务和候选形式，不是单因素对照。因此即使本步成功，也不能把差异唯一归因“改成二选一”或“自然概念更简单”。

## 数据与唯一格式

6短语境家族，每组cat/dog一对，共12条；每对只替换细类词，其他句子和背景一致。标签为animal+cat或animal+dog，12条均人工式逐条审核后、任何模型响应前冻结。无预测筛选，无新增同义词／属性推断。

全部文本使用相同后缀：换行后`The animal is a`，紧接两个固定完整候选。实际tokenizer逐项检查26个拼接，未预设token数：

{table(cand)}

候选字符串中的前导空格和句号都保留；token长度恰好同为2，包含句号token13。主指标是完整候选的条件自然对数概率总和，单位为nats；取最大总分，不做长度、先验或温度校正。FP32原生模型/logsoftmax、FP64求和；同一官方Qwen3-0.6BBase和tokenizer，权重/配置/tokenizer SHA与S01实际加载版本一致；CPU2线程、无chat模板。没有另训分类器、字典加载、feature记录/分析/干预。

## 结果

{table(counts)}

配对中首选发生变化：**{nswitch}/6组**；两条都判断正确：**{nboth}/6组**；反向切换：{nreverse}/6组。“发生切换”与“正确跟随”分别记账，避免把两条都反向误判当成正确跟随。

{table(Q)}

错误共{len(errors)}条，见[全部错误](errors_cn.md)。没有错误时明确注明；没有筛选只展示有利家族。[完整逐家族记录](casebook_cn.md)给全部12条原文、标签、完整前缀、token ID/长度、两分数、差值、首选与对错。

## 固定第一组的完整前缀与分数

F01在响应前已固定为展示组。原文分别为“This animal is a cat.”和“This animal is a dog.”，标签分别animal+cat、animal+dog。

{firsttexts}

{table(first[['gold','S_cat','S_dog','delta_cat_minus_dog','choice','correct']])}

## 中性前缀与基础偏好

中性文本不指明猫或狗，后缀和候选完全相同：

```text
{neutral['prefix']}
```

上方候选表已列中性两分数；S_cat−S_dog={neutral['delta_cat_minus_dog']:.9f}，首选**{neutral['choice']}**。中性记录没有正确标签、不计准确率；它仅描述一个固定前缀下的基础偏好，未用于扣分、调阈值或改选候选。

## 本步能说明什么、不能说明什么

本步说明该冻结模型在这6组明确词语的受控文本、固定续写位置及完整候选计分下的实际偏好，及偏好是否随cat/dog替换改变。候选恰好等长，排除了本轮两个候选token数量不等这一具体因素；词汇先验、上下文概率及句号条件概率仍是总分的组成部分，等长不代表先验相同。

**成功可以只是复制／复述前文中完全相同的cat或dog。** 本步没有用未出现的细类词、没有测试类别抽象或未知动物，因此不能证明抽象概念理解、animal与细类的内在层级组织、feature成员或强弱组合、因果使用及广泛泛化。这是二候选续写偏好，不是自由生成准确率；中性前缀也不作为未知类别题评分。

**停止：仅S02完成，下一步未运行，等待共同审阅。** 没有自动增加数据、修改假设或开展feature分析。

[协议](protocol_cn.md) · [数据](data/panel.jsonl) · [完整原始分数](results/raw_scores.jsonl) · [逐候选CSV](results/candidate_scores.csv) · [原生评分脚本](code/score_native.py) · [核验](evidence/verification.json)
'''
write(E/'summary_cn.md',cn)
en=f'''# S02: animal/cat/dog native continuation

Observed{ncorrect}/12correct (cat{counts[0]['correct']}/6,dog{counts[1]['correct']}/6). Choice changes{nswitch}/6pairs, both correct{nboth}/6, reversed{nreverse}/6. Complete and stop for joint review; no hypothesis revision or next-step execution.

Six matched English context pairs differ only by explicitcat/dog; labelsanimal+cat/dog. One fixed newline+'The animal is a' suffix; exact candidates ' cat.'/' dog.'. Token IDs/lengths and neutral scores:

{table(cand)}

All26token concatenations frozen/checked before model responses. Same officialQwen3-0.6BBase/tokenizer hashes asS01, FP32CPU2threads, native full sequence logprob, FP64sum, argmax without length/prior correction, includingperiod and noEOS/chattemplate. No trained classifier, dictionary, feature capture/analysis, intervention, extra data or prompt search. Both candidates happen to contain2tokens; lexical priors and contextual/period probabilities still differ.

{table(counts)}

{table(Q)}

Neutralprefix: '{neutral['prefix']}'. Delta S_cat−S_dog={neutral['delta_cat_minus_dog']:.9f}, preferred{neutral['choice']}; diagnostic only, not a correction. Allerrors={len(errors)}, explicitly[retained or absent](errors_cn.md). [All12texts,prefixes,scores,IDs](casebook_cn.md).

Success may be literal copying of the visiblecat/dog word. It does not prove abstraction, hidden concept hierarchy, feature composition or causal use/generalization. The change fromS01also changes task, language and candidates, so it cannot isolate one explanation for between-round differences. All{len(oldfiles)}S01sourcefiles remain byte-identical. H1–H4and scientific acceptance are unchanged; next decision awaits researcher review.
'''
write(E/'summary.md',en)
# Exact small copies explicitly requested by the researcher; preserve execution ownership.
for folder in ['data','code','results','evidence']:
 (E/folder).mkdir(exist_ok=True)
 for p in(R/folder).iterdir():
  if p.is_file():shutil.copy2(p,E/folder/p.name)
shutil.copy2(R/'frozen_plan.json',E/'frozen_plan.json')
write(E/'README.md','# S02普通语言原生续写\n\n[中文小结](summary_cn.md) · [English](summary.md) · [全部12条全文和分数](casebook_cn.md) · [全部错误](errors_cn.md) · [协议](protocol_cn.md) · [数据](data/panel.jsonl) · [原始分数](results/raw_scores.jsonl) · [评分代码](code/score_native.py) · [核验](evidence/verification.json)\n\n本步完成即停止，共同审阅前不执行后续分析。此处data/code/results/evidence为用户要求的小型核验副本；执行侧原件保留，不覆盖S01。')
# Append only a narrow record to the existing D1 reading entry.
p=D1/'README.md';text=p.read_text();marker='## 受控小例子：普通语言猫狗续写（S02）';assert marker not in text
p.write_text(text+f'''\n\n{marker}

S01方阵格式出现近似固定答案偏好后，按用户指定改做6组animal+cat/dog配对共12英文文本，只有一种固定续写后缀及` cat.`/` dog.`两个完整候选，另1个中性前缀。不调整原模型、不做先验／长度校正。结果{ncorrect}/12正确，{nswitch}/6组切换、{nboth}/6组两条都对；中性首选{neutral['choice']}。[本步中文小结](controlled_steps/S02_animal_cat_dog_12/summary_cn.md)和[完整12条分数](controlled_steps/S02_animal_cat_dog_12/casebook_cn.md)独立保存。S01原件SHA保持；本步成功仍可能只是复制，不改H1–H4，也不自动进入feature分析。状态：完成S02，等待共同审阅。
''')
# Register actual saved analysis only; never a new model/dictionary checkpoint.
cat=S/'assets/catalog.json';j=json.load(open(cat));aid='data_analysis_r17_d1_s02_animal_cat_dog12_20261103';assert not any(x['id']==aid for x in j['assets']);j['assets'].append(dict(id=aid,title_cn='R17D1受控S02：animal猫狗12条原生续写',category='analysis',kind='paired_native_continuation',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=x,expected='file',required=True)for x in ['data/panel.jsonl','data/format.json','results/raw_scores.jsonl','results/pairs.csv','evidence/completed.json','evidence/verification.json']])],identity=dict(rows=12,families=6,formats=1,neutral=1,model='model_qwen3_0p6b_base_official_a5',correct=ncorrect,both_correct_pairs=nboth,model_updates=0,dictionaries_loaded=0,feature_analysis=False,old_S01_unchanged=True,scientific_acceptance='Unknown',nextstep='NOT_RUN_WAIT_FOR_JOINT_REVIEW',data_sha256=sha(R/'data/panel.jsonl'),scores_sha256=sha(R/'results/raw_scores.jsonl')),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(E/'summary_cn.md'),str(E/'protocol.md')]));dump(cat,j)
manifest=[]
for folder in ['data','code','results','evidence']:
 for p in sorted((E/folder).glob('*')):
  if p.is_file():manifest.append(dict(path=str(p.relative_to(E)),origin=str(R/folder/p.name),bytes=p.stat().st_size,sha256=sha(p),role='userexplicitlyrequestedsmallgeneratedcopy;executionownerretained'))
dump(E/'payload_manifest.json',dict(files=manifest,scope='onlyS02:12texts+1neutral,oneformat,nativeonly;no weights/features',authority='current directuser request for data/scripts/rawscores within projectnewsubdirectory'))
dump(R/'output_manifest.json',dict(canonical=str(E),state='COMPLETED_S02_WAIT_FOR_JOINT_REVIEW',files=manifest,scientific_acceptance='Unknown',nextstep='NOT_RUN'))
print('S02_SUMMARY',json.dumps(summary),flush=True);print('NEUTRAL',json.dumps(cand),flush=True);print('FIRSTPAIR',first[['gold','S_cat','S_dog','delta_cat_minus_dog','choice','correct']].to_string(index=False),flush=True)
