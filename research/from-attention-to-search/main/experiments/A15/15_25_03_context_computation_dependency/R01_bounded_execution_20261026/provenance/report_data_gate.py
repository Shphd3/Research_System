"""CPU-only report/illustrative TRAIN samples after prespecified data gate stop."""
from pathlib import Path
import json,csv,hashlib,collections,shutil,unicodedata,datetime
from tokenizers import Tokenizer
S=Path('/data/250010109/Research_System');P=S/'Projects/from-attention-to-search';M=P/'main';E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder');O=E/'analysis/context_dependency_20261026/execution';R0=M/'experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026';R=R0.parent/'R01_bounded_execution_20261026';R.mkdir(exist_ok=True)
for p in [R/'tables',R/'provenance',O/'examples']:p.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
a=json.load(open(O/'support_receipt.json'));table=list(csv.DictReader(open(O/'tables/token_support_all.csv')));assert a['status']=='INSUFFICIENT_ELIGIBLE_TOKEN_CONTEXTS';assert len(table)==4024
assert max(min(int(x['dedup_unique_A']),int(x['dedup_unique_B'])) for x in table)==43
assert max(int(x['same_stratum_balanced_unique_each_class']) for x in table)==23
assert not any(x['eligible_pre_stratum']=='True' for x in table)
assert a['valid_positions']+sum(a['exclusions'].values())==85548
# Original TRAIN identity and tokenizer binding, no model load.
data=E/'analysis/sft_route_learning/20261019T012300Z/data/train.jsonl';assert sha(data)=='5530f9676c3d7941150e404c045ad62815a11310d8b1ec4904c209121ddb8ad5'
tp=Path('/data/share/Qwen3-0.6B-Base/tokenizer.json');assert sha(tp)=='c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539'
freeze=json.load(open(O/'provenance/execution_freeze.json'));assert all(sha(p)==h for p,h in freeze['scientific_body'].items())
write(O/'provenance/saved_table_audit.json',{'status':'PASS','table_rows':len(table),'unique_token_ids':len({r['token_id'] for r in table}),'max_min_unique_target_documents':43,'max_balanced_common_stratum_per_class':23,'prestratum_eligible_count':0,'all_registered_answer_positions_accounted':85548,'TRAIN_sha_matches_original_registered':True,'tokenizer_sha_matches_original_registered':True,'frozen_execution_scientific_body_unchanged':True,'forward_counter':0,'EVAL_TEST_read':False,'scope':'counts and identities only; not local readout qualification'})
# Posthoc illustration of the largest matched-support token; not C/R cases.
# Uniform fixed-hash examples from its matched TRAIN pool, no feature observations used.
best=a['best_same_stratum_support'];v=best['token_id'];ya=best['target_A'];yb=best['target_B'];rows=[json.loads(l) for l in data.open()];tok=Tokenizer.from_file(str(tp));doc=collections.defaultdict(list)
def key(x):return hashlib.sha256(f"20261026|{x['dialogue_id']}|{x['position']}|{x['token_id']}".encode()).hexdigest()
for row in rows:
 ids=row['input_ids'];n=len(ids)
 for t in range(row['answer_start']-1,n-1):
  if ids[t]!=v or n-t-1<16 or t+17>512:continue
  doc[row['prompt_sha256']].append({'token_id':v,'target_id':ids[t+1],'dialogue_id':row['prompt_sha256'],'original_id':row['id'],'dataset':row['dataset'],'position':t,'position_bin':(t-(row['answer_start']-1))//16,'prefix_bin':(t+1)//32,'input_ids':ids,'answer_start':row['answer_start']})
selected=[min(rs,key=key) for rs in doc.values()];classes=collections.Counter(x['target_id'] for x in selected);assert classes[ya]==91 and classes[yb]==43
strata=collections.defaultdict(lambda:{ya:[],yb:[]})
for x in selected:
 if x['target_id'] in [ya,yb]:strata[x['dataset'],x['position_bin'],x['prefix_bin']][x['target_id']].append(x)
matched=[]
for s,d in sorted(strata.items()):
 n=min(len(d[ya]),len(d[yb]))
 for y in [ya,yb]:matched.extend(sorted(d[y],key=key)[:n])
assert len(matched)==46
examples=[]
for y in [ya,yb]:
 part=sorted((x for x in matched if x['target_id']==y),key=lambda x:hashlib.sha256(('example_display_20261026|'+x['dialogue_id']+'|'+str(x['position'])).encode()).hexdigest())[:2]
 for x in part:
  t=x['position'];ids=x['input_ids'];examples.append({'purpose':'posthoc data-construction illustration only;not qualified C/R or intervention evidence','token_id':v,'token_text':tok.decode([v]),'target_id':y,'target_text':tok.decode([y]),'dialogue_id':x['dialogue_id'],'original_id':x['original_id'],'dataset':x['dataset'],'position':t,'left_context_excerpt':tok.decode(ids[:t],skip_special_tokens=False)[-150:],'current_token':tok.decode([v]),'actual_following_excerpt':tok.decode(ids[t+1:t+17],skip_special_tokens=False),'C_or_R_observed':False})
write(O/'examples/data_context_illustrations.json',examples)
with (R/'tables/token_support_top10.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,list(table[0]));w.writeheader();w.writerows(table[:10])
summary='''# 执行结果：当前数据未通过候选支持门槛

**结论：本轮停在数据资格阶段，尚未检验C→R功能依赖。** 这是按冻结规则执行后的“证据不足”，不是H1被否定，也不是H2／H3成立。

目标是在同一token不同上下文中，比较第14层C削弱对第28层R及预测的特异作用。用户已明确授权执行原协议；本轮没有降低其样本门槛或更换数据。

| 数据资格 | 协议要求 | 实际结果 |
|---|---|---|
| 同一token对应两种不同续词，每类来自独立对话 | 每类至少64文档；每token每文档只留一处 | 没有合格token；较少一类的支持最多43文档 |
| 再按来源、答案位置与前缀长度匹配 | 两类同分层、同权重 | 最多各23文档；不补样、不换token |
| 合格对象进入C/R与测量资格 | 先有合格上下文对象 | 未进入；局部R测量可靠性仍未知 |

实际读取原TRAIN1024对话／85548答案位置，按特殊token、词片和16个后续答案目标筛选，留下53390位置；每token每文档固定取一处后有35546个上下文。4024个token类型仍有至少两种续词，但没有达到上述门槛。EVAL与TEST本轮均未读。

支持最多的匹配对象是词片` in`，两类续词为` the`与` a`：按固定去重规则分别91／43文档，分层平衡后各23文档。它只是事后说明数据缺口的实例，不是合格C／R候选。[真实文本示例](examples_cn.md)仅说明该数据构造，没有feature激活或干预结论。

**没有执行的部分：** C/R特征选择、源／后层真实激活前向、层局部测量资格、C削弱及匹配对照。所有功能指标与不确定性均为NOT RUN，不填0、不画效果图。没有依据为“共同计算是否支持上下文计算”作正负裁决。

资源与资产：模型前向0／12000，训练0，新资源0；未加载模型或CrossCoder张量，未改权重。原TRAIN、tokenizer身份与冻结协议／源码哈希核对通过。原协议门槛保留，未转用DCLM、增加数据或改变分层。

本轮已按既定停止分支收束。当前不足仅针对这份Tulu数据在冻结筛选规则下的可检验性；不说明所有现有文本或CrossCoder都不能用于此问题。

[逐项记录](detailed_cn.md) · [前10项支持表](tables/token_support_top10.csv) · [完整4024项原表](ALLTABLE) · [原始停止回执](provenance/support_receipt.json) · [冻结协议](PROTOCOL)。
'''.replace('ALLTABLE',str(O/'tables/token_support_all.csv')).replace('PROTOCOL',str(R0/'protocol_cn.md'))
(R/'summary_cn.md').write_text(summary)
(R/'summary.md').write_text('''# Bounded execution stopped at prespecified data eligibility

Result: INSUFFICIENT_ELIGIBLE_TOKEN_CONTEXTS. C-to-R functional dependence was NOT TESTED; H1/H2/H3 remain unadjudicated. The user's explicit execution instruction authorized the frozen protocol, including its insufficiency stop.

Original TRAIN1024dialogues/85548answer positions yielded53390valid positions and35546unique token-dialogue contexts under fixed target-independent SHA sampling.4024token types retained at least2next-target classes; none had≥64distinct dialogues in each class. The largest smaller-class support was43. After provenance/answer-position/prefix-length stratification, maximum balanced support was23/class.

Illustration only: token ` in`, next targets ` the`/` a`, has91/43unique dialogues, then23/23matched. This was selected posthoc to explain data insufficiency, not as a qualified C/R feature or intervention result. Four fixed-hash real TRAIN excerpts are in the companion examples; no feature labels are invented.

C/R discovery, model/native replay, local-readout qualification and all interventions were NOT RUN. Model sequence forwards0/12000, training0, allocations0. EVAL/TEST not read. No model/coder/cache tensors loaded; no weights modified, thresholds relaxed, fallback data or broader search. Original TRAIN/tokenizer identities and frozen scientific body hashes pass. A complete saved-table/stop receipt accompanies the report. This limits testability under this exact Tulu sampling contract, not all possible data or the CrossCoder's scientific value.

[中文一页](summary_cn.md) · [Detailed record](detailed.md) · [Top10](tables/token_support_top10.csv) · [Receipt](provenance/support_receipt.json).
''')
ex='# 原始上下文示例：只说明数据构造\n\n对象为匹配支持最多但仍不合格的` in`。选择该对象是事后解释性选择；其匹配池内按固定哈希每类随机显示2例。未查看C/R响应，不能给出候选feature的正／反例或功能命名。以下引用保留原始文本，左侧只显示尾部150字符；完整位置、来源及样本键在JSON。\n\n'
for i,x in enumerate(examples,1):
 ex+=f"**例{i}：{x['original_id']}，位置{x['position']}，续词{json.dumps(x['target_text'],ensure_ascii=False)}。**\n\n```text\n{x['left_context_excerpt']}⟦{x['current_token']}⟧{x['actual_following_excerpt']}\n```\n\n"
ex+='`⟦ ⟧`只标出同一个当前词片，不是原始文本。没有按效果挑选，也没有作模型干预。\n';(R/'examples_cn.md').write_text(ex)
(R/'detailed_cn.md').write_text('''# 完整执行记录：冻结数据门槛未通过

## 问题与资格层次

目标是源层C干预的后层R与预测效应。当前只执行到其前提——是否存在足够同token、不同续词的独立上下文。数据门槛失败不能替代功能假设的阴性证据。结果类型为数据资格不足；下游所有条件NOT_RUN。

## 授权、冻结与实际复用

本轮用户明确指令“继续执行本协议……资格不足就如实报告”。沿用R00英文／中文Protocol和JSON配置，不改科学体或阈值；执行前将其与实际源码SHA记录在`provenance/execution_freeze.json`。源码只使用原TRAIN JSON与原tokenizer，未复用训练器、优化器或MoE；旧`extract_sft.py`用于明确位置连接：t从answer_start−1到n−2，目标为input_ids[t+1]。唯一实现细化为：目标无关固定SHA挑每token每文档一处，支持按两类较少一类计，分层内固定SHA平衡。该细化记录于执行前freeze，并且本轮在分层之前已不满足64门槛。

## 数据流与完整分母

TRAIN源SHA为5530f9676c3d7941150e404c045ad62815a11310d8b1ec4904c209121ddb8ad5，原tokenizer JSON SHA为c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539。总85548答案位置中，按互斥先后筛选：特殊当前／下一token排除1024；当前词片无Unicode字母排除20262；不足16个后续答案目标排除10872；完整前缀加目标超512排除0。余53390；这些条件之外没有按准确率或梯度筛选。特征频率未使用。

每个(token,prompt_sha256)按固定SHA取一个位置，得到35546个上下文。每token只按该池支持最多两种下一token分类（平局按ID）。4024个有两类的token逐项保留，较少类最大43，无一达到64。匹配键为(dataset,答案位置//16,前缀长度//32)，每层两类取同样多文档、SHA固定选择；最大23/class。样本本就每token每文档一处，因此没有把同文档多次出现计作独立支持。

## 预定／实际对照

| 项目 | 预定 | 实际 | 证据／影响 |
|---|---|---|---|
| 输入 | 固定Tulu TRAIN发现，EVAL探索性留出 | 只读TRAIN；EVAL/TEST均未读 | 原数据hash、访问回执 |
| 候选门槛 | 每类64独立文档、同token | 最大较少类43 | 数据资格不通过，不能后退门槛 |
| C/R池及局部读数 | 合格token后选择并核验 | NOT RUN | C/R身份未形成，R资格未知 |
| 0.05/0.10与匹配对照 | 资格通过后独立配对 | NOT RUN | 没有损失、R效应或区间 |
| 预算 | 计划4864，硬上限12000 | 前向0 | 剩余额度不授权扩展数据 |
| 模型／资产 | 冻结、不训练、不分配资源 | 未加载模型，未写权重 | 没有新增checkpoint |

## 实际产物与复现

执行侧`source/discover_support.py`是原始发现程序；`source/report_data_gate.py`只做报告、保存表核对及解释性TRAIN文本抽样。原始完整表`tables/token_support_all.csv`含4024行，停止回执`support_receipt.json`、访问/冻结/不变性回执在provenance。保存表重新聚合证实最大43／23与0合格，所有85548位置分母闭合。tokenizer当前SHA与原始绑定一致。大权重SHA未重算，因为没有进入首次模型加载，不把它写成成功核验。

四条原始文本只是最强支持失败对象的事后解释性样本，非C/R案例；没有feature反例可分类，明确记未形成。无模型输出，故无结果图或bootstrap区间。运行CPU；GPU可用显存查询返回Insufficient Permissions，未据此推断可用显存，也未创建资源；本轮首先因数据门槛停止，未依赖GPU。

## 判断与收束

已经知道：这份数据在冻结筛选／去重／匹配下没有合格对象。尚不知道：C是否支持R、局部方向测量是否可靠、目标预测是否受特异干预影响。H1/H2/H3均未检验。没有理由将数据不足改写为“计算独立”或“字典失败”；本轮不另选数据、降低门槛或搜索更好看的对象。

科学机制接受和问题关闭仍Unknown。本次授权执行已达到其停止分支；如后续更改数据或门槛，需要作为新协议修订记录，不是本轮结果。本记录不给新的自动实验指令。
''')
(R/'detailed.md').write_text('''# Detailed execution: data support gate failure

[Chinese complete ledger](detailed_cn.md) owns counts, source joins, exclusions and conformance. Frozen R00 scientific contract was accepted by the user's explicit instruction. Before reading discovery outcomes, source/protocol/config hashes were written to execution_freeze.json. The actual CPU discovery uses original answer positions t=answer_start−1,...,n−2 with next target input_ids[t+1], exact source/tokenizer identity and fixed target-independent SHA per token/dialogue.

85548positions =53390valid +1024special +20262no-letter +10872insufficient-future. No prefix>512 exclusion. After one occurrence/token/document:35546contexts.4024types have2targets; max minority support43<64before matching. Common source/answer-position/prefix-length strata permit at most23/class. No C/R selection or downstream measurement qualifies, all interventions NOT_RUN. Aggregate/source/hash receipts distinguish access, identity and scientific eligibility. EVAL/TEST not read; no tensors, training, model edits or allocation. GPU memory permission was unavailable but data failed first, so no resource inference is used.

The failed most-supported token's4TRAIN excerpts are explicitly posthoc illustrations, not feature evidence. Full4024row outputs and actual sources remain execution-side; selected top10and small receipts are curated. No mechanism figures, fictional C/R examples or bootstrap intervals. H1/H2/H3 untested; no scientific question closure. Existing conditions were not relaxed or silently replaced.
''')
# Every receipt and worker is small; no raw complete table or raw TRAIN imported into project.
for f in [O/'support_receipt.json',*list((O/'provenance').glob('*.json')),*list((O/'source').glob('*.py')),O/'examples/data_context_illustrations.json']:
 shutil.copy2(f,R/'provenance'/f.name)
(R/'provenance/run.sh').write_text('''#!/usr/bin/env bash
set -euo pipefail
source /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/scripts/runtime.sh
# Actual CPU entrypoint, frozen original output refuses overwrite after completion:
python /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/context_dependency_20261026/execution/source/discover_support.py
# Reproduction requires a new output destination while retaining original source/settings.
''')
write(R/'authorization.json',{'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorization':'用户：继续执行本协议。按已写好的边界完成候选发现、测量资格核验和有界干预，不新增训练或资源；资格不足就如实报告。','protocol_state_at_preparation':'DRAFT_NOT_EXECUTABLE','execution_state_after_instruction':'APPROVED_FOR_BOUNDED_DISCOVERY_QUALIFICATION_AND_INTERVENTION_WITH_STOP_GATES','source_protocol':str(R0/'protocol.md'),'source_protocol_cn':str(R0/'protocol_cn.md'),'scientific_hashes':freeze['scientific_body'],'result':'STOPPED_AT_DATA_ELIGIBILITY','authorization_not_resource_allocation':True})
(R/'execution_status.json').write_text(json.dumps({'task_state':'COMPLETE_AT_PRESPECIFIED_STOP','result_state':'INSUFFICIENT_DATA_SUPPORT','question_state':'FUNCTIONAL_QUESTION_UNANSWERED','discovery_completed':True,'C_R_feature_selection':'NOT_RUN','local_measurement_qualification':'NOT_RUN','intervention':'NOT_RUN','sequence_forwards':0,'training':0,'new_resources':0,'EVAL_read':False,'TEST_read':False},indent=2)+'\n')
(R/'README.md').write_text('''# Authorized bounded execution: data eligibility stop

[中文一页](summary_cn.md) · [English](summary.md) · [完整记录](detailed_cn.md) · [真实数据示例](examples_cn.md) · [小型证据清单](artifact_manifest.md).

Current outcome is insufficient document support, not a functional negative. All model interventions NOT_RUN. Frozen preparation protocol remains unchanged; explicit authorization and stop state are recorded here.
''')
print('Result records:',R);print('No model forward or intervention; all four illustrative TRAIN cases labelled non-mechanistic.')
