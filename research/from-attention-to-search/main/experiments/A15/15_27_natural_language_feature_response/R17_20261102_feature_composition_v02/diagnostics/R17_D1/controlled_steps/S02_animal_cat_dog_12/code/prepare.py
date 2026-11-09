from pathlib import Path
import json,hashlib,re,datetime
from tokenizers import Tokenizer
R=Path(__file__).resolve().parents[1];S=Path('/data/250010109/Research_System');BASE=S/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps';E=BASE/'S02_animal_cat_dog_12';OLD=R.parent/'S01_explicit_singularity_36'
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not(R/'frozen_plan.json').exists(),'Prepare only once, before responses.'
for name in ['data','results','evidence']:(R/name).mkdir(exist_ok=True)
# Preserve the entire previous tiny experiment, both canonical and execution evidence.
oldfiles={str(p):sha(p)for root in [OLD,BASE/'S01_explicit_singularity_36']for p in root.rglob('*')if p.is_file()}
dump(R/'evidence/S01_immutable_before.json',oldfiles)
templates=[('direct','This animal is a {label}.'),('story','In this story, the animal is a {label}.'),('two sentences','We are describing an animal. It is a {label}.'),('note','The note identifies this animal as a {label}.'),('fronted animal name','A {label} is the animal described in this example.'),('report','The report calls the animal a {label}.')]
suffix='\nThe animal is a';candidates=[dict(label='cat',text=' cat.'),dict(label='dog',text=' dog.')];panel=[]
for i,(context,temp)in enumerate(templates,1):
 for fine in ['cat','dog']:
  text=temp.format(label=fine);assert len(re.findall(r'\b'+fine+r'\b',text))==1;assert not re.search(r'\b'+('dog'if fine=='cat'else'cat')+r'\b',text);assert re.search(r'\banimal\b',text)
  panel.append(dict(id=f'S02_F{i:02d}_{fine}',family=f'F{i:02d}',context=context,text=text,coarse_label='animal',fine_label=fine,labels=['animal',fine],explicit_fine_word=fine,fine_word_span=[text.index(fine),text.index(fine)+len(fine)],prefix=text+suffix,label_basis='The English text explicitly states the fine animal name; no model output used for selection.'))
for i in range(1,7):
 pair=[x for x in panel if x['family']==f'F{i:02d}'];assert len(pair)==2;assert len({re.sub(r'\b(cat|dog)\b','{fine}',x['text'])for x in pair})==1
assert len({x['text']for x in panel})==12
model=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official');T=Tokenizer.from_file(str(model/'tokenizer.json'));prompts=[];neutral='An animal is mentioned in this note.'
for p in panel+[dict(id='neutral',family='neutral',text=neutral,prefix=neutral+suffix,fine_label=None,coarse_label='animal')]:
 ids=T.encode(p['prefix'],add_special_tokens=False).ids;cs=[]
 for order,c in enumerate(candidates):
  full=T.encode(p['prefix']+c['text'],add_special_tokens=False).ids;assert full[:len(ids)]==ids and len(full)<=192;tail=full[len(ids):];assert tail;cs.append(dict(**c,order=order,candidate_token_ids=tail,candidate_tokens=len(tail),full_input_token_ids=full))
 prompts.append(dict(id=p['id'],family=p['family'],text=p['text'],prefix=p['prefix'],prefix_token_ids=ids,prefix_tokens=len(ids),gold=p['fine_label'],coarse_label='animal',candidates=cs))
for name,data in [('panel.jsonl',panel),('prompts_tokenized.jsonl',prompts)]:
 (R/'data'/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n'for x in data))
dump(R/'data/format.json',dict(suffix=suffix,answer_location='immediately after the final a, before candidate leading space',candidates=candidates,neutral_text=neutral,neutral_prefix=neutral+suffix,formats=1))
plan=dict(step='S02_animal_cat_dog_12',frozen_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),authorization='Current explicit user request:6pairs/12texts, one continuationformat and1neutral, then stop.',model=str(model),model_asset='model_qwen3_0p6b_base_official_a5',tokenizer_asset='tokenizer_qwen3_0p6b_base_official_a5',model_dtype='float32',saved_weight_precision='SameS01savedBF16weights promotedtoFP32',device='cpu',threads=2,physical_batch=4,physical_length=192,padding_id=0,add_special_tokens=False,chat_template=False,EOS_scored=False,sum_dtype='FP64sum ofFP32tokenlogprobs',score='full candidate sequence conditional log probability including leading-space-bearing token and period',decision='argmax unnormalized total; exact tie first candidate with tie recorded',delta='S_cat minus S_dog; positive selects cat',families=6,rows=12,cat_rows=6,dog_rows=6,formats=1,neutral_prefixes=1,total_prefixes=13,total_candidate_sequences=26,paired_choice_change='cat-row chosen label differs from dog-row chosen label; report both-correct separately to detect reversed switches',neutral_use='diagnostic only; no length or prior correction',data_SHA256={p.name:sha(p)for p in(R/'data').iterdir()},runtime='CPU2threads; PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3;PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python; offline',reuse='SameS01model/tokenizer/nativebackbone+LMhead; adapt only2candidate scoring, no Capture or dictionaries',forbidden=['training','dictionary_load','feature_extraction_or_analysis','probe_fit','intervention','prompt_search','additional_data','research_hypothesis_revision','automatic_next_step'],stop='COMPLETE_ONLY_S02_THEN_WAIT_FOR_JOINT_REVIEW',scientific_acceptance='Unknown')
dump(R/'frozen_plan.json',plan);dump(R/'evidence/data_audit.json',dict(rows=12,pairs=6,cat=6,dog=6,explicit_fine_word_all=True,coarse_animal_all=True,within_pair_lexical_difference='only one literal cat/dog substitution',all_labels_audited=True,model_response_used=False,revisions=[],boundary_checks=26,max_full_tokens=max(len(c['full_input_token_ids'])for p in prompts for c in p['candidates']),candidate_encodings=[{k:c[k]for k in ['label','text','candidate_token_ids','candidate_tokens']}for c in prompts[0]['candidates']]))
E.mkdir(parents=True,exist_ok=True)
(E/'protocol.md').write_text('''# S02: animal/cat/dog native continuation only

Authorized by the current direct user request. Complete only this bounded step, then wait for joint review. It follows S01's format/answer preference problem without rewriting S01 or any H1–H4hypothesis.

Purpose: determine whether the same frozen0.6BBase changes continuation preference when the body explicitly changes cat↔dog.6paired English contexts/12texts, labels animal+cat or animal+dog. Only literal fine-class word changes within each pair; varied sentence/context across6families. No prediction-based selection. All text/labels/prefixes/candidate tokenizations freeze before responses.

One fixed suffix, exactly newline+'The animal is a'. Candidate order/text exactly ' cat.' and ' dog.', including initial space and final period. Actual concatenated tokenization must preserve prefix token IDs; record all candidate IDs/counts. One property-free-with-respect-to-cat/dog neutral body 'An animal is mentioned in this note.' uses the same suffix/candidates, diagnostic only, excluded from accuracy. No alternative prompts, calibration or candidate changes.

Use the same official Qwen3-0.6BBase/tokenizer hashes asS01, FP32CPU2threads, no chattemplate or specialtokens/EOS. Fixed4x192physicalshape with2candidate lanes repeated for numeric checks. Score every candidate token including period, FP32logsoftmax and FP64sum. Choose max total without length/prior correction, exact ties use frozenorder and are recorded. No training, classifiers, dictionaries, feature hooks/storage/analysis, or intervention.

Report all12texts and exact prefixes/labels/candidates, full rawscores/token IDs/counts, delta=S_cat−S_dog, chosenlabel/correct; cat/dog counts outof6; all6pair changes and correct-direction changes separately; neutral totals/preference; all errors (explicitlynoneifnone) plus at leastonefullpair. Independently replay token sums/argmax/counts and verify S01hashes unchanged.

This checks constrained continuation sensitivity to explicit animal words. Success may be copying; it does not identify abstraction, feature organization, causal use, generalization or performance improvement caused by a single change from S01. No extra concepts/data, hypothesis revision, automatic next step, commit/push/publication. Researcher judgment and next decision remain pending.
''')
(E/'protocol_cn.md').write_text('''# S02：animal—cat/dog原生续写

按本次用户明确授权，只完成这一步并等待审阅。S01原文、脚本、分数和结论不变，H1–H4不修改。

6句式／语境家族，每家族cat/dog一对，共12英文文本；保存animal+cat或animal+dog标签。配对中只替换明确细类词，不按模型预测筛选。先审查并冻结文本、标签、续写位置、精确候选和token拼接。

唯一续写后缀为换行后“The animal is a”，候选固定为` cat.`、` dog.`，含前导空格和句号。中性正文为“An animal is mentioned in this note.”，不指明猫狗，用完全相同后缀和候选；只诊断基础偏好，不计正确率、不校正分数。

复用S01实际加载的官方Qwen3-0.6BBase与tokenizer，核对同一SHA；FP32CPU2线程，固定4×192，无chat模板／BOS／EOS，无截断。两候选各复制一槽，仅数值核验。逐token条件自然对数概率相加，包含全部候选及句号；不按长度／先验修正，最大总分获选，精确平分按冻结顺序并记录。差值定义S_cat−S_dog。

交付全部12原文／标签／前缀、两候选全文、token ID／长度／完整分数、差值／首选／对错；猫狗各6条正确数；6配对是否改变选择，以及改变方向是否两条都正确；中性分数与偏好；全部错误和至少一对全文与分数。独立复算数值并检查S01所有原文件SHA不变。

这只测明确细类词变化后原生续写的偏好。成功可能只是复述或复制，不能证明抽象概念、feature组合或因果机制。与S01同时变了任务、语言和候选等，不能作单一因素效果归因。无额外数据／prompt、模型／字典训练、分类器、feature提取／分析／干预或自动下一步；不提交发布。
''')
print('FROZEN12',plan['data_SHA256'])
for p in panel:print(p['id'],p['text'])
print('CANDIDATES',json.load(open(R/'evidence/data_audit.json'))['candidate_encodings'])
