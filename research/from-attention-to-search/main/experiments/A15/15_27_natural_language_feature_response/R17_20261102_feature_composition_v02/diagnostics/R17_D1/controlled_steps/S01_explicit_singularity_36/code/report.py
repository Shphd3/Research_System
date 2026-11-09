"""Describe the fixed native-behavior panel, then stop. No learned readout or feature analysis."""
from pathlib import Path
import json,datetime,hashlib,math,shutil
import pandas as pd
R=Path(__file__).resolve().parents[1];S=Path('/data/250010109/Research_System');E=S/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S01_explicit_singularity_36';D1=E.parents[1]
def rows(p):return [json.loads(x)for x in Path(p).open()if x.strip()]
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n')
def table(d):return pd.DataFrame(d).to_markdown(index=False,floatfmt='.6f')
completion=json.load(open(R/'evidence/completed.json'));assert completion['status']=='COMPLETED_STEP1_STOP_FOR_JOINT_REVIEW';plan=json.load(open(R/'frozen_plan.json'));panel=rows(R/'data/panel.jsonl');raw=rows(R/'results/raw_scores.jsonl');assert len(raw)==74;d={x['id']:x for x in panel};lab={'unknown':'无法确定','yes':'是','no':'否'};conditions={'square_only':'方阵／奇异性未知','singular_square':'奇异方阵','invertible_square':'可逆方阵'};flat=[];decision=[];checks=[]
for r in raw:
 assert len(r['candidates'])==3 and {c['label']for c in r['candidates']}==set(lab)
 for c in r['candidates']:
  assert abs(math.fsum(c['token_logprobs'])-c['total_logprob'])<1e-10
  assert c['candidate_tokens']==len(c['candidate_token_ids'])==len(c['token_logprobs']);assert all(math.isfinite(v)and v<=0 for v in c['token_logprobs'])
  flat.append(dict(id=r['id'],family=r['family'],condition=r['condition'],format=r['format'],gold=r['gold'],candidate_label=c['label'],candidate_text=c['candidate'],candidate_token_ids=json.dumps(c['candidate_token_ids']),candidate_tokens=c['candidate_tokens'],total_logprob=c['total_logprob'],preferred=c['label']==r['preferred_label'],correct=r['correct']))
 winner=max(r['candidates'],key=lambda x:x['total_logprob'])['label'];assert winner==r['preferred_label'];assert r['correct']==(None if r['gold']is None else winner==r['gold'])
 if r['gold']is not None:
  assert r['gold']==d[r['id']]['singularity'];decision.append(dict(id=r['id'],family=r['family'],condition=r['condition'],format=r['format'],gold=r['gold'],preferred=r['preferred_label'],correct=r['correct'],margin=r['margin'],correct_margin=r['correct_margin'],text=d[r['id']]['text']))
F=pd.DataFrame(flat);P=pd.DataFrame(decision);assert len(P)==72 and P.groupby('format').size().to_dict()=={'F1':36,'F2':36};F.to_csv(R/'results/candidate_scores.csv',index=False);P.to_csv(R/'results/decisions.csv',index=False);F[F.id=='neutral'].to_csv(R/'results/neutral_scores.csv',index=False)
counts=[];conf=[];summ=[]
for fmt in ['F1','F2']:
 t=P[P.format==fmt];summ.append(dict(format=fmt,correct=int(t.correct.sum()),N=36,fully_correct_families=int(t.groupby('family').correct.all().sum()),families=12))
 for gold in ['unknown','yes','no']:
  q=t[t.gold==gold];counts.append(dict(format=fmt,condition=conditions[q.condition.iloc[0]],gold=lab[gold],correct=int(q.correct.sum()),N=12))
  conf.append(dict(format=fmt,gold=lab[gold],pred_unknown=int((q.preferred=='unknown').sum()),pred_yes=int((q.preferred=='yes').sum()),pred_no=int((q.preferred=='no').sum())))
pd.DataFrame(counts).to_csv(R/'results/by_condition.csv',index=False);pd.DataFrame(conf).to_csv(R/'results/confusion.csv',index=False);pd.DataFrame(summ).to_csv(R/'results/overall.csv',index=False)
wide=P.pivot(index=['id','family','condition','gold'],columns='format',values=['preferred','correct']);same=int((wide['preferred']['F1']==wide['preferred']['F2']).sum());both=int((wide['correct']['F1']&wide['correct']['F2']).sum());agree=[]
for cond,t in wide.groupby(level='condition'):agree.append(dict(condition=conditions[cond],N=len(t),same=int((t['preferred']['F1']==t['preferred']['F2']).sum()),both_correct=int((t['correct']['F1']&t['correct']['F2']).sum())))
pd.DataFrame(agree).to_csv(R/'results/format_agreement_by_condition.csv',index=False);dump(R/'results/agreement.json',dict(N=36,same_preferred_label=same,different=36-same,both_correct=both))
# Reconstruct frozen tokenized inputs and check exact response-prefix identity.
ps={(x['id'],x['format']):x for x in rows(R/'data/prompts_tokenized.jsonl')}
for r in raw:
 p=ps[(r['id'],r['format'])];assert p['prefix']==r['prefix']and p['prefix_token_ids']==r['prefix_token_ids']
 for a,b in zip(p['candidates'],r['candidates']):assert a['text']==b['candidate']and a['candidate_token_ids']==b['candidate_token_ids']
for name,digest in plan['data_SHA256'].items():assert sha(R/'data'/name)==digest
assert datetime.datetime.fromisoformat(plan['frozen_UTC'])<=datetime.datetime.fromisoformat(completion['started_UTC']);assert sha(R/'frozen_plan.json')==completion['frozen_plan_SHA256'];assert sha(R/'results/raw_scores.jsonl')==completion['raw_scores_SHA256'];assert completion['dictionaries_loaded']==completion['hooks']==completion['probes_fitted']==completion['model_updates']==0
checks=dict(status='PASS',frozen_data_hashes=True,all_74_prefixes_match=True,all_222_token_sums_match=True,all_argmax_and_correctness_match=True,rows=36,formats=2,native_decisions=72,neutral_decisions=2,candidate_sequences=222,training=0,dictionaries_loaded=0,feature_hooks=0,readout_fits=0,max_duplicated_lane_error=completion['max_duplicate_lane_score_error'],old_results_reused=False,first_scores_after_final_freeze=True,scientific_acceptance='Unknown',nextstep='NOT_RUN_WAIT_FOR_JOINT_REVIEW')
dump(R/'evidence/verification.json',checks)
# Exact family casebook, every text and both three-candidate scores.
case=['# 36条受控文本与两格式全部分数','[中文小结](summary_cn.md) · [精确候选与问法](data/formats.json) · [全部原始记录](results/raw_scores.jsonl)','所有行的“是否方阵”标签均为是。奇异性未知指给定文本不足以判断。各行独立，不能把一个家族的三条描述当成同时成立。分数是完整候选条件自然对数概率之和，越大越优；各格式按自己的候选文本评分，不跨格式比较分数大小。表仅显示6位小数，原始记录保留完整精度。']
for family in sorted(P.family.unique()):
 pp=[x for x in panel if x['family']==family];case += ['## '+family+' — '+pp[0]['family_context']]
 for x in pp:case += [f"**{conditions[x['condition']]}**；方阵=是，奇异性={lab[x['singularity']]}；性质词={', '.join(x['explicit_property_words'])}。",'```text\n'+x['text']+'\n```']
 tt=[]
 for x in pp:
  row={'条件':conditions[x['condition']],'正确':lab[x['singularity']]}
  for fmt in ['F1','F2']:
   r=next(y for y in raw if y['id']==x['id']and y['format']==fmt)
   for c in r['candidates']:row[fmt+' '+lab[c['label']]]=c['total_logprob']
   row[fmt+' 首选']=r['preferred_text'];row[fmt+' 正确']=r['correct']
  tt.append(row)
 case += [table(tt)]
write(E/'casebook_cn.md','\n\n'.join(case))
# Examples are selected mechanically, first ID within each class/format/outcome, including explicit absence.
examples=['# 每类正确／错误实例','选择规则在响应前固定：每格式、每类分别取id排序的首个正确和首个错误；不存在则注明。完整36条见[casebook](casebook_cn.md)。'];example_rows=[]
for fmt in ['F1','F2']:
 for cond in conditions:
  examples.append('## '+fmt+' / '+conditions[cond])
  for correct,name in [(True,'正确'),(False,'错误')]:
   t=P[(P.format==fmt)&(P.condition==cond)&(P.correct==correct)].sort_values('id')
   if t.empty:examples.append(f'**无{name}例**：本类在该格式的12条中不存在{name}判断。');example_rows.append(dict(format=fmt,condition=cond,outcome=name,id=None,status='NONE_EXISTS'));continue
   q=t.iloc[0];r=next(x for x in raw if x['id']==q.id and x['format']==fmt);examples += ['### '+name+'：'+q.id,'```text\n'+q.text+'\n```',f'正确标签：{lab[q.gold]}；模型首选：{r["preferred_text"]}。',table([dict(候选=c['candidate'],token数=c['candidate_tokens'],总分=c['total_logprob'],首选=c['label']==r['preferred_label'])for c in r['candidates']])];example_rows.append(dict(format=fmt,condition=cond,outcome=name,id=q.id,status='OBSERVED'))
write(E/'examples_cn.md','\n\n'.join(examples));pd.DataFrame(example_rows).to_csv(R/'results/example_selection.csv',index=False)
# Candidate identities and neutral priors.
candidates=[]
for fmt in ['F1','F2']:
 r=next(x for x in raw if x['id']=='neutral'and x['format']==fmt)
 for c in r['candidates']:candidates.append(dict(format=fmt,label=lab[c['label']],candidate=c['candidate'],token_ids=json.dumps(c['candidate_token_ids']),tokens=c['candidate_tokens'],neutral_total_logprob=c['total_logprob'],neutral_preferred=c['label']==r['preferred_label']))
neutral_winners={fmt:next(r['preferred_text']for r in raw if r['format']==fmt and r['id']=='neutral')for fmt in ['F1','F2']}
shortest={fmt:sum(next(c['candidate_tokens']for c in r['candidates']if c['label']==r['preferred_label'])==min(c['candidate_tokens']for c in r['candidates'])for r in raw if r['format']==fmt and r['gold']is not None)for fmt in ['F1','F2']}
cn=f'''# 第一步：明确写出性质时，0.6B能否判断奇异性？

本步已完成并停止，等待共同审阅。两套格式的原始正确数如下；不据结果继续调prompt，也不自动进入feature分析。

{table(summ)}

## 目的与假设

沿“方阵→奇异方阵”建立可理解的测试对象：当正文明确说奇异／可逆时，原生模型是否能对应到是／否；只说方阵时，是否保留无法确定。竞争解释包括候选表达和长度、基础答案偏好、问答格式及英中文本组合。本步只描述行为，不裁定内部机制。

## 数据与模型

12家族、36英文文本；每家族3条，只有必要性质词不同，冠词按a/an语法一致。每类12条。三类是否方阵都为是；奇异性分别未知、是、否。没有行列式、秩、特征值或其他推断性质。12家族确有句式／语境变化，完整原文与两套全部分数在[逐家族记录](casebook_cn.md)。

同一冻结官方Qwen3-0.6B Base与tokenizer，模型／tokenizer SHA与R17 D1一致；FP32、CPU2线程，无chat模板。旧D1数据包含推断证书和不同任务后缀，不直接复用，不合并旧分数。新数据和结果独立存放。只使用原生候选序列评分，未加载SAE/CC、未记录feature、未拟合读出，也无训练或干预。

## 方法：固定两格式，按完整候选总分选最大

F1：根据已知信息，A 是否为奇异矩阵？回答是、否或无法确定。\n
前缀末尾为“答案：”。候选顺序：是。／否。／无法确定。

F2：只使用给定信息，判断矩阵 A 是否奇异。请选择：无法判断、不是奇异矩阵、是奇异矩阵。\n
前缀末尾为“回答：”。候选顺序：无法判断。／不是奇异矩阵。／是奇异矩阵。

所有原文、换行、候选全文及token ID在响应前冻结。主分数是每个候选所有token的条件log probability相加，包含句号，不含问题／EOS；单位为自然对数。得分越大越优，**不做长度、先验或温度校正**。因此它测的是三个规定完整回答的相对偏好，不是自由生成答案的准确率。

下表同时给精确候选和中性前缀“This note refers to an object denoted A.”的总分。中性记录不计入36条准确率，仅诊断基础偏好。

{table(candidates)}

## 结果

### 各类正确数

{table(counts)}

### 混淆表

行是真实标签，列是模型首选含义；unknown=无法确定。每行12条。

{table(conf)}

### 两格式是否一致

36条中，首选含义一致{same}/36，不一致{36-same}/36；两格式均正确{both}/36。12家族内的完整三条均正确数见开头。两个格式是同36对象的配对观测，不能当成72个独立家族。

{table(agree)}

[每类正确与错误例](examples_cn.md)逐格式列出；某类没有正确或没有错误时已明确标记，没有虚构例子。全部36条仍完整交付，不只交筛选案例。

## 如何理解长度、基础偏好和表达方式

中性前缀的首选分别为F1“{neutral_winners['F1']}”、F2“{neutral_winners['F2']}”。36条任务中，首选属于该格式最短候选的次数为F1 {shortest['F1']}/36、F2 {shortest['F2']}/36；这只是长度与表述共同作用下的观测，不把相关性解释成纯长度因果。

F1三个候选为2／2／3个token；F2为3／4／4个token。完整序列总分会同时反映回答内容及其后续措辞和句号的概率。长度不同是当前测量的一部分；本步没有假定较长必输，也没有用平均token分数替换主指标。F2更短的是未知回答，而F1更长的是未知回答，需结合两套结果和上表中性分数一起看。

中性前缀提供单个固定外壳下的基础偏好，不是总体先验估计。不能把测试分数减去中性分数后重判对错。F2同时改变了问题措辞、答案顺序和等义回答表述，故格式差异不能唯一归因顺序或长度。英文正文、中文问题／回答也引入跨语言指令因素；冻结Base模型没有改成chat模型。

## 本步能说明与不能说明

能说明：这个冻结模型在这36条明确文本、两套固定问法和候选序列计分下，如何区分明确奇异、明确可逆和信息不足；哪些家族／条件判断改变。它为后续讨论提供完整可复核对象，而不是证明后续步骤应当启动。

不能说明：全体方阵概念能力、复杂数学推理或自然语料泛化；不能说明任何feature成员／强弱、组合机制或因果使用。本步“是否方阵”是人工标签，不是另一个模型问题；没有非方阵对照，因此也没有独立测出方阵识别能力。未知是文本证据不足，不是同一个具体矩阵具有矛盾性质。

**停止点：已完成第一步，等待你我共同审阅。模型、文本、任务或问法是否调整均不自动决定。**

[协议](protocol_cn.md) · [核验和执行说明](detailed_cn.md) · [数据](data/panel.jsonl) · [原始完整分数](results/raw_scores.jsonl) · [逐候选CSV](results/candidate_scores.csv) · [原生评分脚本](code/score_native.py)
'''
write(E/'summary_cn.md',cn)
en=f'''# Step1: native singularity judgment on explicit36texts

Completed and stopped for joint review. Original H1–H4 are not retested or reinterpreted.

## Purpose and data

Test the current frozen Qwen3-0.6B Base when square/singular-square/invertible-square is explicitly stated.12English sentence/context families×3independent descriptions=36, with matched objects/skeletons and necessary a/an agreement only. Square=True for all; singularity unknown/yes/no. No determinant/rank or inferential certificates. Unknown is insufficient textual information, not contradictory properties of one matrix. OldD1texts/scores are not pooled.

## Method

Same official checkpoint/tokenizer hashes asD1, FP32 CPU2threads. Fixed2Chinese question/candidate formats saved before responses. F1 uses yes/no/unknown (2/2/3tokens), F2 equivalent unknown/no/yes(3/4/4tokens). Sum every candidate-token conditional logprob including period, excluding prompt/EOS, FP32token probabilities/FP64accumulation; choose max without length/prior correction. Neutral property-free text scored once/format, diagnostic only. No dictionaries/hooks/features/probes/training/intervention or prompt search.

## Observations

{table(summ)}

{table(counts)}

{table(conf)}

Paired preferred labels agree on{same}/36; both correct on{both}/36. Per-condition agreement:

{table(agree)}

Exact candidates, IDs, lengths and neutral scores:

{table(candidates)}

[Full36text-and-score casebook](casebook_cn.md) and [first correct/error per class/format](examples_cn.md) retain every outcome and explicitly identify absent examples. OriginalJSONL keeps fullprecision, prefix/candidate/token identities and tokenlogprobs.

## Boundary and stop

Sequence totals can reflect candidate length, lexical prior, period and format. No length-normalized or neutral-corrected alternative decision is substituted. F2changes wording, option order and answer realization together, so no factor is individually identified. English bodies with Chinese questions/answers also involve cross-language instruction behavior of a Base model. This is constrained candidate preference, not free-generation accuracy or universal concept competence. Square labels are manuallyaudited, not a separately asked model task; no nonsquare contrast.

No feature mechanism or concept hierarchy is inferred. Scientific acceptance and next decision remain Unknown. STOP_AFTER_STEP1_FOR_JOINT_REVIEW. No automatic adjustment of text/task/model or next experiment.

[Protocol](protocol.md) · [Detailed](detailed.md) · [Raw](results/raw_scores.jsonl).
'''
write(E/'summary.md',en)
# All user-requested small payloads are present inside the project, as exact generated evidence copies.
for name in ['data','code','results','evidence']:
 (E/name).mkdir(exist_ok=True)
 for p in (R/name).iterdir():
  if p.is_file():shutil.copy2(p,E/name/p.name)
shutil.copy2(R/'frozen_plan.json',E/'frozen_plan.json')
for n in ['protocol.md','protocol_cn.md']:shutil.copy2(E/n,R/n)
detail=f'''# 第一步详细记录与核验

本记录只覆盖S01，不改R17 D1旧结论，不开启第二步。[小结](summary_cn.md) · [全家族](casebook_cn.md) · [正确／错误例](examples_cn.md)。

## 资产和复用

只加载D1同一官方Base模型与tokenizer，路径{plan['model']}。模型配置、tokenizer、模型权重SHA均与原D1输入指纹相同，actual receipt见[evidence/completed.json](evidence/completed.json)。复用D1原生backbone+LM head完整候选计分方法，独立实现3候选批次，不导入会加载字典的Capture。没有旧数据／分数拼接，没有模型／SAE／CC训练。CPU，零GPU新作业。

## 文本与三个标签

全部12模板及36条在[data/panel.jsonl](data/panel.jsonl)。每家族相同对象A和主句，仅square/singular square/invertible square性质短语差异；invertible前a/an作必要语法改变。初稿12处“a invertible”不合语法，响应前已修，初稿保留于执行侧versions/pre_response_article_fix。修复没有改变语义标签、问法或模型。其他36行核查未见语义歧义；[逐条审计](evidence/data_audit.json)记录检查。

全部是方阵；奇异性未知／是／否分别来自：未给性质、显式奇异、显式可逆。三行是独立描述，不是把同一固定A同时断言为奇异和可逆。旧D1多数描述要求从证书推断，不能替代本步直接属性词测试。

## 问题、分数与数值实现

F1使用用户原句，F2提前固定等义问法及逆向选项顺序，字节全文见[data/formats.json](data/formats.json)。每条完整prefix和候选实际拼接的token也已冻结于[data/prompts_tokenized.jsonl](data/prompts_tokenized.jsonl)。不使用chat模板、BOS或EOS，所有候选句号均评分；前缀token边界逐候选一致，无截断，最大输入{json.load(open(R/'evidence/data_audit.json'))['max_full_input_tokens']}token≤192。

物理4×192：前三槽分别为三候选，第四槽重复第一槽作为数值检查；不是第四个问题。输入各自attentionmask，原生模型无hooks、不保存中间表征，只取候选后续位置的LM词表logsoftmax并查目标token，相加得总分。FP32前向/logsoftmax、FP64求和。最长候选长度不同，主指标不变，不拿中性分数或平均token分数重新排序。tie按冻结顺序并在原始记录显式列出。

## 有界修复与执行

首次加载前遇到已安装protobuf与旧生成文件不兼容，在尚无模型响应时设置PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python，与D1既有环境一致。失败日志和首次启动回执保留；无安装、权重／文本／提示修改。第二次运行完成全部74prefix＝72矩阵任务+2neutral，222完整候选。耗时{completion['elapsed_seconds']:.1f}秒；模型更新、字典加载、feature hooks、probe拟合均0。并未遍历prompt。

## 三项审计与复算

1. 识别审计：目标是明确属性下的原生候选判断，不是复杂推理或feature机制；第一步范围和停止点由本次用户直接指定。
2. 数据审计：12匹配家族、每类12，标签与冠词修改在响应前冻结；两个格式是同一批文本配对，不是独立72家族；中性prefix不计准确率，无训练／开发选择。
3. 实现审计：冻结模型和输入SHA、全部74prefix、222候选token边界／逐token求和、首选argmax／正确性独立复算通过；重复槽最大分数误差{completion['max_duplicate_lane_score_error']:.12g}。无feature hooks或学习参数。

[evidence/verification.json](evidence/verification.json)是数值与范围回执。原生分数是规定候选内的相对序列偏好；没有通过自由生成验证回答合规。格式和先验诊断的证据不作语义机制归因。

## 载荷位置与结束状态

本次用户明确要求数据、脚本、原始分数位于项目合适新目录，因此这里附小型审核载荷副本，来源和SHA在[payload_manifest.json](payload_manifest.json)。实际执行源码／原始文件owner为{R}；此处code/data/results是准确生成副本，避免形成两个可编辑源码。修改执行侧后须重新核验生成副本，不直接改原始分数。权重不复制。

状态：COMPLETED_STEP1_STOP_FOR_JOINT_REVIEW。下一步NOT_RUN。未提交、推送、外部发布；没有改变任何Focus或Anchor科学接受状态。
'''
write(E/'detailed_cn.md',detail);write(E/'detailed.md',f'''# S01 detailed provenance

SameD1checkpoint/tokenizer identity verified; CPU FP32 native likelihood only. Frozen36texts/twoformats, no fitting. All72matrix decisions and2neutral prefixes completed ({completion['elapsed_seconds']:.1f}s).222candidate sequences, exact token IDs/counts and token logprobs saved. Four physical lanes include duplicatedfirstcandidate, maxscore discrepancy{completion['max_duplicate_lane_score_error']:.12g}; this is not an extra condition.

Pre-response amendment:12a/anarticle errors corrected; initial panel preserved in execution versions, labels unchanged. Initial loader failed dueprotobuf compatibility before responses; pure-Python parser env matchesD1, no installation/model/prompt changes. Both failure and success receipts retained.

[Full detailed procedure, audit and boundaries](detailed_cn.md) · [Numerical checks](evidence/verification.json) · [Input/model hashes and completed runtime](evidence/completed.json) · [Exact data](data/panel.jsonl) · [All scores](results/raw_scores.jsonl).

The user explicitly requested these small datasets, scripts and rawscore files in the project. They are exact generated evidence copies of execution owner{R}, with[payload manifest](payload_manifest.json); no weights copied. Do not edit generated copies as a second source. No feature extraction/analysis, dictionary loading, readout fit, intervention, training, prompt search or automaticnextstep occurred. Only step1 is complete; joint review, scientific interpretation and next decision remain pending. No publication or Focus/Anchor state transition.
''')
write(E/'README.md','# S01：明确性质的原生行为第一步\n\n[中文小结](summary_cn.md) · [English](summary.md) · [36条全文与分数](casebook_cn.md) · [每类正误例](examples_cn.md) · [协议](protocol_cn.md) · [详细核验](detailed_cn.md) · [精确数据](data/panel.jsonl) · [原始分数](results/raw_scores.jsonl) · [脚本](code/score_native.py)\n\n完成后停止，等待共同审阅；不自动分析feature或进入下一步。')
# Small first-step record on the existing main line; old results are not rewritten.
intro=f'''\n\n## 受控小例子第一步：明确奇异性（S01）

目的：先确认模型在性质直接写出时的原生判断。数据为12家族×方阵／奇异方阵／可逆方阵共36英文文本。复用同一冻结0.6B Base，两套预定三候选完整序列评分，无长度／先验校正、无分类器。结果：F1 {summ[0]['correct']}/36、F2 {summ[1]['correct']}/36；同条首选一致{same}/36。详细[中文小结](controlled_steps/S01_explicit_singularity_36/summary_cn.md)和[逐家族分数](controlled_steps/S01_explicit_singularity_36/casebook_cn.md)单独记录。只完成原生行为第一步，下一步NOT_RUN，等待研究者共同审阅；R17 D1旧结论不变。
'''
p=D1/'README.md';text=p.read_text();assert '## 受控小例子第一步：明确奇异性（S01）'not in text;p.write_text(text+intro)
# Requested bounded outputs registered, no checkpoint entry or invented training state.
cat=S/'assets/catalog.json';j=json.load(open(cat));aid='data_analysis_r17_d1_s01_explicit_singularity36_20261103';assert not any(x['id']==aid for x in j['assets'])
j['assets'].append(dict(id=aid,title_cn='R17D1第一步36条明确奇异性原生判断',category='analysis',kind='small_explicit_concept_native_behavior',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=n,expected='file',required=True)for n in ['data/panel.jsonl','data/formats.json','results/raw_scores.jsonl','evidence/completed.json','evidence/verification.json']])],identity=dict(families=12,rows=36,formats=2,native_decisions=72,neutral_prefixes=2,model='model_qwen3_0p6b_base_official_a5',model_updates=0,dictionaries_loaded=0,feature_analysis=False,nextstep='NOT_RUN_WAIT_FOR_JOINT_REVIEW',scientific_acceptance='Unknown',data_sha256=sha(R/'data/panel.jsonl'),raw_scores_sha256=sha(R/'results/raw_scores.jsonl')),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(E/'summary_cn.md'),str(E/'protocol.md')]))
dump(cat,j)
# Manifest every generated small payload and current source, except manifest itself.
manifest=[]
for folder in ['data','code','results','evidence']:
 for p in sorted((E/folder).glob('*')):
  if p.is_file():manifest.append(dict(path=str(p.relative_to(E)),origin=str(R/folder/p.name),bytes=p.stat().st_size,sha256=sha(p),role='explicitlyrequestedsmallauditablecopy;executionremainsowner'))
dump(E/'payload_manifest.json',dict(files=manifest,exception_authority='current user explicitly requests data/scripts/raw scores in projectnewdirectory',scope='36texts/twofixedformats/nativeonly; no weights/features'))
dump(R/'output_manifest.json',dict(canonical=str(E),summary=str(E/'summary_cn.md'),state='COMPLETED_STEP1_STOP_FOR_JOINT_REVIEW',files=manifest))
print('COUNTS',json.dumps(summ),flush=True);print('CLASS',json.dumps(counts,ensure_ascii=False),flush=True);print('CONFUSION',json.dumps(conf,ensure_ascii=False),flush=True);print('AGREEMENT',same,both,flush=True)
