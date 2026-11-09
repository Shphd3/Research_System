from pathlib import Path
import json,hashlib,datetime,re
from tokenizers import Tokenizer
R=Path(__file__).resolve().parents[1];S=Path('/data/250010109/Research_System');D1=R.parents[1];E=S/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S01_explicit_singularity_36'
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not (R/'frozen_plan.json').exists(),'Preparation is one-shot; never revise a frozen panel after responses.'
for d in ['data','evidence','results']: (R/d).mkdir(exist_ok=True)
templates=[
 ('exercise','In this exercise, A is a {property}.'),
 ('problem statement','The problem statement specifies that A is a {property}.'),
 ('section example','Let A be a {property} for the example in this section.'),
 ('calculation instruction','For the calculation described here, take A to be a {property}.'),
 ('lecture notes','The lecture notes introduce A as a {property}.'),
 ('short report','For the model in this short report, A is a {property}.'),
 ('table heading','The table heading identifies A as a {property}.'),
 ('symbol definition','Throughout this example, the symbol A denotes a {property}.'),
 ('fronted noun phrase','A {property}, denoted by A, is used in the following discussion.'),
 ('procedure step','For this step of the procedure, the supplied object A is a {property}.'),
 ('relative clause','The exercise concerns A, which is a {property}.'),
 ('accompanying description','The accompanying description states: A is a {property}.')]
props=[('square_only','square matrix','unknown',['square']),('singular_square','singular square matrix','yes',['singular','square']),('invertible_square','invertible square matrix','no',['invertible','square'])]
pp=[]
for i,(context,temp)in enumerate(templates,1):
 for cond,prop,lab,words in props:
  text=temp.format(property=prop).replace('a invertible','an invertible').replace('A invertible','An invertible');pp.append(dict(id=f'S01_F{i:02d}_{cond}',family=f'F{i:02d}',family_context=context,condition=cond,text=text,is_square=True,singularity=lab,explicit_property_words=words,property_phrase=prop,property_span=[text.index(prop),text.index(prop)+len(prop)],label_basis={'square_only':'Square shape is explicit; no invertibility/singularity property is supplied.','singular_square':'Singular square matrix is explicitly asserted.','invertible_square':'Invertible square matrix is explicitly asserted; hence it is not singular.'}[cond],scope='Each row is an independent described object A; three rows are alternative descriptions, not simultaneous assertions about one fixed matrix.'))
formats=[dict(id='F1',question='根据已知信息，A 是否为奇异矩阵？回答是、否或无法确定。',answer_prefix='答案：',candidates=[{'label':'yes','text':'是。'},{'label':'no','text':'否。'},{'label':'unknown','text':'无法确定。'}]),dict(id='F2',question='只使用给定信息，判断矩阵 A 是否奇异。请选择：无法判断、不是奇异矩阵、是奇异矩阵。',answer_prefix='回答：',candidates=[{'label':'unknown','text':'无法判断。'},{'label':'no','text':'不是奇异矩阵。'},{'label':'yes','text':'是奇异矩阵。'}])]
model=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official');tok=Tokenizer.from_file(str(model/'tokenizer.json'));prompts=[]
for f in formats:
 for p in pp+[dict(id='neutral',family='neutral',condition='neutral',text='This note refers to an object denoted A.',singularity=None)]:
  prefix=p['text']+'\n\n'+f['question']+'\n'+f['answer_prefix'];ids=tok.encode(prefix,add_special_tokens=False).ids;cs=[]
  for rank,c in enumerate(f['candidates']):
   full=tok.encode(prefix+c['text'],add_special_tokens=False).ids;assert full[:len(ids)]==ids,(f,p,c);tail=full[len(ids):];assert tail and len(full)<=192
   cs.append(dict(**c,order=rank,candidate_token_ids=tail,candidate_tokens=len(tail),full_input_token_ids=full))
  prompts.append(dict(id=p['id'],family=p['family'],condition=p['condition'],format=f['id'],gold=p['singularity'],prefix=prefix,prefix_token_ids=ids,prefix_tokens=len(ids),candidates=cs))
assert len(pp)==36 and len({p['text']for p in pp})==36 and len(prompts)==74
for fi in range(1,13):
 fam=[x for x in pp if x['family']==f'F{fi:02d}'];assert len(fam)==3 and len({x['text'].replace(x['property_phrase'],'{property}').replace('an {property}','a {property}').replace('An {property}','A {property}')for x in fam})==1
for p in pp:
 assert len(re.findall(r'\bsquare\b',p['text']))==1
 assert not re.search(r'determinant|\brank\b|eigen|diagonal|\bzero\b|\bidentity\b|\brows\b|\bcolumns\b',p['text'],re.I)
 assert (p['singularity']=='yes')==bool(re.search(r'\bsingular\b',p['text']))
 assert (p['singularity']=='no')==bool(re.search(r'\binvertible\b',p['text']))
for name,data in [('panel.jsonl',pp),('prompts_tokenized.jsonl',prompts)]:
 (R/'data'/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n'for x in data))
dump(R/'data/formats.json',formats)
plan=dict(step='S01_explicit_singularity_36',authorizing_request='Current explicit user instruction: only36texts/twoformats/nativebehavior, then stop for jointreview.',frozen_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),model=str(model),model_asset='model_qwen3_0p6b_base_official_a5',tokenizer_asset='tokenizer_qwen3_0p6b_base_official_a5',model_dtype='float32',saved_weight_precision='bfloat16 promoted toFP32, samecheckpoint asD1',device='cpu',threads=2,physical_batch=4,physical_length=192,padding_id=0,attention_mask=True,add_special_tokens=False,chat_template=False,answer_EOS_scored=False,primary='sum of all candidate-token conditional natural log probabilities; no length/prior correction',sum_dtype='FP64 accumulation of FP32 token logprobs',decision='argmax total sequence score; exact tie uses frozen listed order, tie explicitly reported',family_count=12,rows=36,conditions=[x[0]for x in props],formats=2,matrix_prompts=72,neutral_prompts=2,candidate_sequences=222,neutral_prefix='This note refers to an object denoted A.',data_SHA256={x.name:sha(x)for x in (R/'data').iterdir()},runtime='PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3; installedCPUtorch; no packageinstallation',reuse='D1samefrozenmodel/tokenizer/FP32, adapt native fullcandidate scoring only; no import of D1Capture because it loads SAE/CC',old_data_reuse='Not pooled or rescored: previous panel mixes implied certificates and summary suffix; newexplicit36 required.',forbidden=['feature_capture','SAE_load','CrossCoder_load','probe_fit','training','intervention','promptsearch','otherconcepts','automaticnextstep'],stop='STOP_AFTER_STEP1_FOR_JOINT_REVIEW',scientific_acceptance='Unknown')
dump(R/'frozen_plan.json',plan);dump(R/'evidence/data_audit.json',dict(rows=36,families=12,per_condition=12,matched_family_skeletons=12,unique_texts=36,labels_checked='all36directlyaudited; no semantic ambiguities;12grammaticalarticles corrected before responses',text_revisions=[{'stage':'before any modelresponse','rows':12,'change':'a invertible→an invertible; A invertible→An invertible','reason':'grammaticalarticleagreement only; labels unchanged','retained_version':'versions/pre_response_article_fix'}],forbidden_inference_cues=0,boundary_token_checks=222,max_full_input_tokens=max(len(c['full_input_token_ids'])for p in prompts for c in p['candidates']),candidates=[dict(format=f['id'],candidates=[{k:v for k,v in c.items()if k not in ['full_input_token_ids']}for c in next(p for p in prompts if p['format']==f['id'])['candidates']])for f in formats]))
E.mkdir(parents=True,exist_ok=True)
protocol='''# S01: explicit singularity, native behavior only

Status: EXECUTION_AUTHORIZED by the current direct user request. This is a first-step prerequisite check within R17_D1, not a feature hypothesis retest or a new Focus. Stop for joint review after reporting.

Purpose: establish a small readable object for square→singular-square concept refinement.12families×3independent descriptions=36Englishtexts, explicit square/singular-square/invertible-square; no determinant/rank or derived certificates. Square=True for all; singularity unknown/yes/no. Unknown means the text does not determine the property, not a contradictory fixed matrix.

Use the exact frozen official Qwen3-0.6B Base and tokenizer from D1. FP32 CPU inference, no optimizer or classifier. Scores adapt only the native sequence-scoring portion of D1; do not import Capture or load any dictionary. Model/source identity checked before execution. No old scores or data are pooled.

Two fixed Chinese questions and equivalent candidate sets are saved byte-for-byte in formats.json. F1 uses the researcher's exact question and order yes/no/unknown. F2 changes question wording and lists unknown/no/yes with equivalent full answers. All36rows use both. A single property-free neutral text is scored once per format. These are diagnostics of candidate expression/length/prior, not corrections. No further formats, examples or prompt search.

For each candidate c, sum log P(c_t | prefix,c_<t) over all answer tokens including the full stop, excluding prompt, EOS and masked padding. Score every candidate's actual concatenated tokenization; require prefix stability and no truncation. Primary argmax uses unnormalized sequence totals; no length/prior adjustment or temperature. Save exact prefix and candidate texts, all token IDs/counts, token logprobs, totals, preferred answer, margins and correctness. Fixed4×192physical shape;3candidate lanes plus duplicated first lane for a numerical identity check. FP32 model/logsoftmax, FP64 score accumulation.

All36labels and within-family matching are audited and frozen before model responses. Report both total correct/36 and each class/12, gold×predicted confusion, family-level agreement across formats, all36texts with both scores, and the first ID correct/error per class/format if such cases exist. If none, explicitly report absence. No inference of feature organization, native causal mechanism or broad mathematical ability.12constructed families are not a natural population sample; repeated formats are paired observations.

Bounded audits: identification—explicit text comprehension, not theorem inference; data/statistics—12matchedfamilies, no fitting/split, fixed2formats andneutral; implementation—frozenmodel/nohooks/nooptimizer, exacttokenboundaries, finite logprobs, token-sum and duplicated-lane checks. Outputdata and rawscores stay execution-side; project owns this Protocol/Summary/casebook.

Completion: deliver records, stop; researcher acceptance and next decision remain Unknown. Do not alter either format after responses. No subsequent feature analysis, training, intervention, other concept, commit/push or publication.
'''
(E/'protocol.md').write_text(protocol)
(E/'protocol_cn.md').write_text('''# S01：明确性质的原生概念判断

用户已明确授权本步，完成即停止，共同审阅后才决定下一步。

目的：用12句式／语境家族×方阵、奇异方阵、可逆方阵=36条英文描述，检查同一冻结Qwen3-0.6B Base的基本三选一判断。每家族三条仅改变必要性质词；不使用行列式、秩等推断线索。三类均为方阵，奇异性依次未知／是／否；每条是独立描述，未知是文本不足以判断。

复用D1官方权重、tokenizer与FP32推理。只改用原生完整候选评分部分，不导入会加载SAE/CC的Capture。CPU2线程，固定4×192物理形状，无截断，不加chat模板／BOS／EOS，不训练分类器或其他模型。

F1原样使用用户问题，候选“是。”“否。”“无法确定。”；F2固定等义问题，候选顺序“无法判断。”“不是奇异矩阵。”“是奇异矩阵。”。完整前缀与精确候选在formats.json及tokenized prompts逐条保存。两个格式同时改变措辞、候选表述及顺序，因此差异不能唯一归因顺序。另对同一个无性质中性前缀各评分一次，仅诊断先验，不据此校正主分数。

主分数是所有候选token的条件自然对数概率之和，包含句号、不含prompt或EOS；token概率FP32、求和FP64。只按总分最大选择，长度／先验均不校正，完全平分按冻结顺序并记录。保存token ID、长度、逐token分数、总分、首选、margin和正确性。第四物理槽重复第一个候选，仅作数值一致性检查，不另加问题。

先冻结36文本、标签、两个格式和全部token；后读取响应。三项审计分别检查识别范围、配对文本和统计单位、实现与数值。所有标签直接逐条审核，有歧义则在响应前修改并保留记录。

输出两格式总计与各类正确数、混淆表、12家族完整原文和候选分数、各类首个正确及错误例（不存在则注明）、格式一致性与长度／基础偏好边界。不能由此判断feature、因果机制或广泛数学能力。无额外prompt搜索、feature提取、线性读出、干预、训练或自动下一步。科学接受Unknown，不提交或外部发布。
''')
print('FROZEN',plan['data_SHA256'],flush=True)
for i in range(1,13):
 print('FAMILY',f'F{i:02d}')
 for x in pp[(i-1)*3:i*3]:print(x['singularity'],x['text'])
print('TOKENIZED',json.load(open(R/'evidence/data_audit.json'))['candidates'],flush=True)
