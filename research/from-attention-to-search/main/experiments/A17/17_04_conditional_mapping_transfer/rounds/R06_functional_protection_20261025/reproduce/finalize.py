from pathlib import Path
import csv,json,hashlib,datetime,shutil,fcntl,zipfile,math,statistics
ROOT=Path(__file__).resolve().parents[1];S=Path('/data/250010109/Research_System');P=S/'Projects/from-attention-to-search';OWN=json.load(open(ROOT/'provenance/ownership.json'));R=Path(OWN['round']);A=Path(OWN['anchor'])
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rows(name):return list(csv.DictReader(open(ROOT/'analysis'/name)))
def main():
 term=read(ROOT/'terminal.json');cfg=read(ROOT/'config/frozen.json');env=read(ROOT/'provenance/environment.json');budget=read(ROOT/'budget.json')
 freeze=read(ROOT/'provenance/freeze.json')
 assert all(sha(p)==v['sha256'] for p,v in freeze['files'].items())
 assert read(ROOT/'provenance/telemetry_repair.json')['status']=='PASS'
 saved=[]
 for meta in sorted((ROOT/'runs').glob('seed_*/old_*/*/checkpoints/step_*.json')):
  m=read(meta);p=Path(m['path']);assert p.is_file() and p.stat().st_size==m['bytes']
  if m['step']==240:assert sha(p)==m['sha256']
  parts=p.parts;m.update(method=p.parents[1].name,old_nonzero=int(p.parents[2].name.split('_')[1]),seed=int(p.parents[3].name.split('_')[1]),resume_capability='weights/Adam/RNG/scheduler/counters/data cursor and frozen order/projector identities; exact external resume qualified only first U step1->2')
  saved.append(m)
 write(ROOT/'analysis/checkpoints_manifest.json',{'members':saved,'count':len(saved),'endpoint_payload_hashes_independently_verified':sum(x['step']==240 for x in saved),'all_other_SHA_source':'recorded from actual atomic saves; current size/existence checked','full_base_saved':False,'required_inputs':cfg['input_assets']})
 # Auditable metrics-only implementation check; no new forward or training.
 count=proj=dn=finite_steps=0;firstorder_positive=0
 for p in (ROOT/'runs').glob('seed_*/old_*/*/metrics.jsonl'):
  method=p.parent.name
  for line in p.read_text().splitlines():
   m=json.loads(line);count+=1
   if method=='F' and m['projection_needed']:
    assert m['g_dot_desired']<=max(1e-10,abs(m['g_dot_candidate'])*1e-5);proj+=1
   if method=='D':assert abs(m['desired_norm']-m['functional_norm'])<=max(1e-9,m['functional_norm']*1e-6);dn+=1
   if method=='F' and 'probe_loss_change' in m:finite_steps+=1;firstorder_positive+=m['probe_loss_change']>0
 write(ROOT/'provenance/final_geometry_verification.json',{'status':'PASS','metric_rows':count,'harmful_F_cases':proj,'D_own_state_norm_matches':dn,'F_finite_loss_checks':finite_steps,'F_actual_probe_loss_increases':firstorder_positive,'numerical_tolerance':'g_dot_desired<=max(1e-10,abs(g_dot_candidate)*1e-5); D norm relative1e-6','finite_loss_increase_is_not_an_implementation_failure':True})
 # Actual output registration; lock and re-read to preserve unrelated concurrent additions.
 family='checkpoint_family_a17_r06_functional_20261025';analysis_id='analysis_a17_r06_functional_20261025'
 entry={'id':family,'category':'checkpoint_family','kind':'model_checkpoint_family','title_cn':'A17 R06功能导向保护实际保存检查点族','projects':['from-attention-to-search'],'required_projects':[],'storage_owner':'MoE_Router execution','payload_status':'MODEL_STATE_PRESENT',
 'identity':{'producer_protocol':str(R/'protocol.md'),'producer_job_id':'pt-f2wnbino','parent_model_asset_id':cfg['parent_model_asset_id'],'parent_adapter_asset_id':cfg['old_adapter_asset_id'],'data_asset_id':cfg['data_asset_id'],'representation_asset_id':'representation_a17_r05_native_prefix_20261023','source_freeze':str(ROOT/'provenance/freeze.json'),'source_freeze_sha256':sha(ROOT/'provenance/freeze.json'),'members_manifest':str(ROOT/'analysis/checkpoints_manifest.json'),'members_manifest_sha256':sha(ROOT/'analysis/checkpoints_manifest.json'),'actual_saved_members':saved,'trainable_names':[f'model.layers.27.self_attn.{q}_proj.weight' for q in ['q','k','v','o']],'trainable_parameters':6291456,'dtype':'float32','loader':str(ROOT/'source/engine.py'),'resume_qualification':'external-process first U step1->2 PASS; endpoint-specific replay NOT_CHECKED','full_base_saved':False},
 'locations':[{'path':str(ROOT),'expected':'directory','required':True,'role':'actual_saved_family','probes':[{'path':'analysis/checkpoints_manifest.json','expected':'file','required':True},{'path':saved[0]['path'],'expected':'file','required':True}]}],'source_paths':[str(R/'protocol.md'),str(ROOT/'config/frozen.json')],'notes_cn':['只登记本轮实际保存的状态；三个续训顺序共用一个旧终点。检查点不是完整Base，需登记的原始Base、旧适配器与投影身份。科研判断不由登记产生。']}
 an={'id':analysis_id,'category':'analysis','kind':'diagnostic_result_bundle','title_cn':'A17 R06完整配对行为与局部更新诊断','projects':['from-attention-to-search'],'required_projects':[],'storage_owner':'MoE_Router execution','payload_status':'ARRAY_FILES_PRESENT','identity':{'producer_job_id':'pt-f2wnbino','producer_protocol':str(R/'protocol.md'),'parents':cfg['input_assets'],'source_freeze_sha256':sha(ROOT/'provenance/freeze.json'),'analysis_script':str(ROOT/'ops/analyze.py'),'TEST_opened':False,'confirmation_scope':'exposed DEV; one old model, three continuation orders'},'locations':[{'path':str(ROOT/'analysis'),'expected':'directory','required':True,'role':'actual_analysis','probes':[{'path':'endpoints_36.csv','expected':'file','required':True},{'path':'verification.json','expected':'file','required':True}]}],'source_paths':[str(R/'summary.md')],'notes_cn':['按冻结240步终点与连续两次90%次要读数汇总；不挑最优检查点。']}
 lock=open(S/'assets/.catalog_registration.lock','a')
 with lock:
  fcntl.flock(lock,fcntl.LOCK_EX);cat=read(S/'assets/catalog.json');ids={x['id'] for x in cat['assets']}
  for e in [entry,an]:
   assert e['id'] not in ids,'refuse silent replacement of existing asset'
   cat['assets'].append(e)
  tmp=S/'assets/catalog.json.r06.tmp';write(tmp,cat);tmp.replace(S/'assets/catalog.json');fcntl.flock(lock,fcntl.LOCK_UN)
 write(ROOT/'provenance/output_registration.json',{'ids':[family,analysis_id],'actual_saved_states':len(saved),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 # Small reproducibility packet; every source corresponds to actual execution.
 repro=R/'reproduce';repro.mkdir(exist_ok=True)
 for p in (ROOT/'source').glob('*.py'):shutil.copy2(p,repro/p.name)
 for name in ['analyze.py','repair_telemetry.py','finalize.py']:shutil.copy2(ROOT/'ops'/name,repro/name)
 shutil.copy2(ROOT/'config/frozen.json',repro/'frozen.json');shutil.copy2(ROOT/'ops/run.sh',repro/'run.sh')
 for name in ['freeze.json','numeric_tests.json','external_process_replay.json','current_shape_cache_check.json','telemetry_smoke.json','environment.json','final_geometry_verification.json','imported_sources.json','history_lineage.json','output_registration.json']:
  shutil.copy2(ROOT/'provenance'/name,repro/name)
 (repro/'README_cn.md').write_text('# 可复现入口\n\n这是实际执行源码、配置和轻量回执的副本。原执行入口为执行根ops/run.sh，激活已存在依赖层后用source/entry.py运行source/engine.py。完整输入与冻结的逐步记录顺序位于原执行根provenance/，哈希在freeze.json。保护投影复用R05 basis_initial.pt。原始TRAIN/DEV、缓存和权重不入Git或轻包；所需资产ID见frozen.json。\n\n不要直接覆盖已有执行根重跑；engine拒绝已有terminal。复现实验需复制为独立执行根并取得相应授权。本轮训练已结束，不因交付而新增训练。分析重放：python ops/analyze.py（只读既有评价/标量）；不得再次执行finalize.py重复登记。原TensorBoard轴标签问题通过repair_telemetry.py从原JSON重建，原events全部保存于tensorboard_raw。\n')
 elapsed=term['training_wall_seconds'];ver=read(ROOT/'analysis/verification.json');ag=rows('method_means_12.csv');dec=rows('operational_decisions.csv');trend=rows('frequency_relative_gains.csv')
 detail='# R06 actual execution and evidence\n\n'
 detail+=f'Job pt-f2wnbino completed {ver["complete_runs"]}/36 fixed240-step runs. Training wallclock {elapsed:.3f}sec, below14400sec. One H100 reserved GPU; no retries, added resources or other Work/Codex tasks. Start {budget["training_start_utc"]}; terminal {term["utc"]}.\n\n'
 detail+='Preflight uses original acquired-old step1200/24000-target four-matrix adapter (SHA in config), exact official-a5 Base, original conditional_mapping_v1 old/reversed TRAIN4800/DEV1600 and registered layer27-input cache. Original old DEV replay800/800. Original new/joint R02 endpoint identities are traced via their saved verification manifest, six existing paths; their weights are not loaded or counted as matched controls. All actual inputs current strict access PASS. R05 source and basis are reused; dataset/schema/identity checks execute once in this job. TEST labels were not opened.\n\n'
 detail+='All runs use36new+36old input slots/step, 0/4/36 active old targets, denominator72, plus64labelled old TRAIN probes for every method. TRAIN probes use no DEV labels. Inactive old targets are replaced with dummy0 before zero-weighted loss. Full-vocabulary argmax and CE use151936logits; both DEV modes have800answers and four200-example cells. New exposure8640per complete run; total objective targets8640/9600/17280; probe-gradient label uses15360per run plus640reuses for10post-update diagnostics (16000total probe label uses). Runtime old_probe_targets counts gradient uses only; extra diagnostic label/input-token use is derived from fixed orders and lengths. Per-step input-token counts and per-phase timings are in metrics.jsonl. No mixed batches with changed denominators.\n\n'
 detail+='F uses the concatenated old-probe gradient across all four matrices, projecting only when g·d>0 and norm²>1e-24; D computes the same quantities on its own current state, matching its own F-candidate length without changing d direction. Adam moments advance once and are retained. S protects16paired initial full-weight rank-one coefficients per matrix (64total), not the full16-dimensional input/output subspace. It retains1200-step cosine horizon; last applied t239 coefficient='+str(.01+.09*(1+math.cos(math.pi*239/1200))/2)+'. No240-step rescaling.\n\n'
 detail+=f'Measurement validation: {ver["evaluations_recomputed"]} saved nonzero-step evaluations independently recomputed from per-item records, fixed denominators/cells verified. Source/config/order/contracts unchanged through terminal. Current12-example native/cache logits maxabs8.392333984375e-5 with identicalargmax under predeclared2e-4. Tiny-matrix known-good/bad/confusing checks pass. Fresh external process replays firstU step1->2 bitwise for weights/Adam/RNG/counters. This qualifies that shared recovery path, not every endpoint-specific resume.\n\n'
 detail+='Engineering deviation: the training writer emitted progress/optimizer_step on both update and token x-axes under one tag. Original scalar losses, optimizer counts and model results are unaffected. After training all original events were moved intact to tensorboard_raw; canonical tensorboard events were reconstructed from immutable step JSON and every tag checked finite, strictly monotonic and consistent with raw losses/counters. The immutable training source is preserved; this telemetry repair is documented rather than silently rewriting history. External inherited carriers.py/runtime.sh hashes were additionally recorded after startup, outside the original nine-file freeze; this provenance limitation is explicit.\n\n'
 detail+='All per-order endpoints, losses, first90% pairs, curves, paired contrasts, coverage, diagnostic step norms and probe finite changes are in tables/. Accumulated step lengths, accumulated squared lengths and mean/sum coefficient fractions are explicitly labelled; they are NOT endpoint net displacement. Finite probe loss can rise despite nonpositive first-order prediction. The script checks projection algebra on recorded scalars and actual loss changes separately. No geometric scalar substitutes for old/new function.\n\n'
 detail+=f'Actual saved checkpoint states: {len(saved)}; all240-step payload hashes independently rechecked. Members and digests: execution analysis/checkpoints_manifest.json; input/output IDs: reproduce/output_registration.json and frozen.json. Weights/Adam/RNG/scheduler/cursor/counters/orders/projector identities saved. Base payload is not duplicated; loading requires registered Base and inherited adapter/basis. Asset access registration is separate from scientific judgment.\n\n'
 detail+='R05 and R02 do not qualify as fixed-exposure F/D controls: R02 mixed uses half as many new answers, R05 uses20answers/step and no common64-probe protection; all36 paired conditions were therefore needed. Their original results were untouched. Addition checkpoints/data/numbers were not used. Main endpoint remains240; two consecutive90% is a secondary operating point. No stopping/seed/checkpoint/hyperparameter choice was based on observed success. The36scientific trajectories contain8640updates; one additional engineering replay update reproduced the already-saved step2 and is included in wallclock, not a new condition.\n\n'
 detail+='Plots average three continuation orders conditional on one acquired-old model; shading is observed minimum-to-maximum, not a confidence interval. x-axis counts new answer targets, because old objective/probe counts vary by design and are reported separately. Accuracy unit percent; CE nat per answer. SVG text is editable; PNG/PDF companions included. Missing conditions remain explicit in coverage.\n\n'
 detail+='Researcher scientific acceptance, mechanism closure and further execution remain Unknown; this bounded matrix ends here. Reproduce existing data analysis with ops/analyze.py; no further training is authorized by a finished report.\n'
 (R/'detailed.md').write_text(detail)
 cn='# R06实际执行、差异与可复核证据\n\n'
 cn+=f'已完成{ver["complete_runs"]}/36条240步轨迹；单卡H100 reserve作业pt-f2wnbino，训练墙钟{elapsed/60:.2f}分钟。开始UTC {budget["training_start_utc"]}，结束{term["utc"]}；没有追加步数、其他Work/Codex任务或资源扩额。\n\n'
 cn+='任务是可见模式的首末词映射，不是加法。沿用同一合格旧终点、原官方Base、原划分及末层Q/K/V/O范围。旧DEV800/800。旧终点、数据和缓存当前身份核验通过；R02六个新/混训端点的身份沿原回执追溯，未重复加载或冒充本轮对照。具体哈希与来源见reproduce/history_lineage.json和freeze.json。\n\n'
 cn+='每步新答案固定36；旧输入槽固定36，其中0/4/36个有监督，统一除72。各方法另用同一规则的64条旧TRAIN探针，计算旧平均损失梯度。0槽也有探针旧标签，所以不能叫无旧监督信息。每条完整轨迹有8640新答案、0/960/8640旧目标答案和15360旧探针梯度标签使用；另有10个固定检查步复用640次标签做更新后诊断，探针合计16000次标签使用；输入token与额外计算独立计数。\n\n'
 cn+='F约束的是Adam已提出的实际位移，使用四矩阵拼接后的旧梯度；D在自身状态保持原方向，仅匹配自身F候选长度。原Adam矩不修改。S复用旧完整权重的每矩阵16个秩一系数及原1200步调度，只截取前240步，不能扩大解释为保留完整左右子空间。\n\n'
 cn+='评价是全词表151936输出最大值，不将答案限制在三词列表；旧/新各800题、四格各200。主终点240步；连续两次新平均准确率≥90%的第二次读数为次要比较，未达到不删除。全部逐题记录、每步标量、逐种子曲线、配对差和成本保留，表格已从逐题记录独立复算。三个顺序共用一个旧模型，范围不是模型总体置信区间。\n\n'
 cn+='实现校验包括有害/有益/零梯度和方向幅度反例、旧模型资格、当前缓存形状原生重放，以及独立进程第1步恢复到第2步的权重、Adam、随机数与计数逐字节一致。当前12例缓存最大logit差8.3923e−5，小于冻结的2e−4且预测一致。其它终点未逐个外进程复放，不能扩大恢复资格。\n\n'
 cn+='发现并修复了一个TensorBoard轴标签工程错误：progress/optimizer_step曾混写更新步与token步。原损失JSON、检查点计数和科学计算不受影响；训练结束后完整保留原events到tensorboard_raw，从原逐步JSON重建规范events，逐标签核对有限性、步轴单调和损失一致。主源码冻结后未改写。外部继承的carriers.py/runtime.sh在启动后补记哈希，明确不冒充事前封存。详见deviations.md。\n\n'
 cn+=f'实际保存{len(saved)}个状态，全部240步终点另行核验payload哈希；保存四矩阵、Adam、RNG、调度、数据位置、曝光计数及顺序/投影身份。逐步位移长度和、平方和及终点净位移不可混用；本轮诊断表明确只报所计算的逐步统计，不凭它反推终点或功能。有限步旧探针损失与一阶预测分开报告。\n\n'
 cn+='英文详细记录在detailed.md，完整结果在summary_cn.md和tables/，所有回执及源码在reproduce/。本轮不读取TEST，不引入SAE/CrossCoder/MoE，不改R02/R05结果，不混入加法证据。科学机制接受与总问题关闭仍待研究者判断。\n'
 (R/'detailed_cn.md').write_text(cn)
 # Five-paragraph Chinese speaking brief from complete method-level data.
 index={(int(z['old_nonzero']),z['method']):z for z in ag}
 def pair(k,m):
  z=index.get((k,m));
  if z is None:return 'MISSING'
  return f"{float(z['old_accuracy_pct']):.2f}%／{float(z['new_accuracy_pct']):.2f}%"
 brief='# 固定新曝光：功能导向保护与旧监督配比\n\n'
 brief+='**会议问题。** 已形成的计算与剩余部分能否采用不同学习安排，保留已有能力？这次先检查参数更新的保护依据与旧监督组织，暂不引入上下文路由或新专家架构。\n\n'
 brief+='**已有证据。** A17输入含模式、甲乙口令和三词列表：旧模式甲取首、乙取尾，新模式反转。R02混训可共存，纯新续训旧规则丢失；但混训减少了新曝光。R05保护初始大奇异方向没有保旧。本轮沿用同一合格旧模型，不混入加法实验。\n\n'
 brief+='**本轮唯一问题。** 在新学习机会相同的条件下，按旧损失的局部影响约束更新，是否优于普通更新和Top-16保护；相对价值是否随旧监督减少而改变？每步固定36新答案、36旧槽、分母72，旧有效槽0/4/36。比较普通U、Top-16衰减S、旧损失导向F、只缩步长的D；所有方法另计算64旧TRAIN探针，F/D用这些旧标签。共36条轨迹，均240步，三个顺序共用一个旧起点。\n\n'
 observations=[]
 for k in [0,4,36]:observations.append(f'旧槽{k}时，U旧／新为{pair(k,"U")}，F为{pair(k,"F")}，S为{pair(k,"S")}，D为{pair(k,"D")}')
 brief+='**结果如何更新判断。** '+'；'.join(observations)+'。均值只纳入实际完成的240步结果，各档完成数见表；缺少顺序时不裁定门槛。F−U的旧改善还须逐顺序同向，且各顺序新下降≤5个百分点，才满足预定操作条件；与D比较后才能讨论方向选择的额外作用。完整配对判据、旧/新答案损失及首次连续两次90%的成本保留在结果表，避免用平均分掩盖取舍。\n\n'
 brief+='**边界与下一步。** 旧槽档位同时改变旧标签次数与旧目标权重；0槽的F/D仍使用旧探针标签。F只限制当前探针旧损失的一阶预测，不保证有限步或长期保持。当前只能更新这一旧模型、任务和预算下的判断，不证明独立功能模块、MoE必要性或自然语言feature频率机制。AI建议依据F相对D及重放档位的实际差别选择下一项问题；本轮已停止训练，不追加条件。\n\n'
 start=datetime.datetime.fromtimestamp(budget['training_start_epoch'],datetime.timezone(datetime.timedelta(hours=8)))
 day=S/'daily_research_reports'/start.strftime('%m%d');meeting=day/'meeting_report';meeting.mkdir(parents=True,exist_ok=True)
 brief+='[完整结果与曲线]('+str(R/'summary_cn.md')+') · [冻结协议]('+str(R/'protocol.md')+') · [实际差异]('+str(R/'deviations.md')+')\n'
 b=meeting/'meeting_brief_A17_R06_functional_protection_cn.md';b.write_text(brief)
 for name in ['README.md','README_cn.md']:
  f=day/name
  if not f.exists():f.write_text('# '+start.strftime('%Y-%m-%d')+'\n')
  with f.open('a') as h:h.write('\n- [A17 R06：固定新曝光的功能导向保护](meeting_report/meeting_brief_A17_R06_functional_protection_cn.md) — 36 paired continuations, existing one-parent setting.\n')
 # Small artifact index; payload remains execution-side.
 artifacts={'execution_root':str(ROOT),'job_id':'pt-f2wnbino','protocol':str(R/'protocol.md'),'source_freeze':str(ROOT/'provenance/freeze.json'),'source_freeze_sha256':sha(ROOT/'provenance/freeze.json'),'output_asset_ids':[family,analysis_id],'saved_checkpoint_manifest':str(ROOT/'analysis/checkpoints_manifest.json'),'saved_checkpoint_manifest_sha256':sha(ROOT/'analysis/checkpoints_manifest.json'),'actual_saved_states':len(saved),'actual_completed_runs':ver['complete_runs'],'scientific_trajectory_updates':sum(z.get('steps',0) or 0 for z in term['coverage']),'engineering_replay_updates':1,'TEST_opened':False,'weights_in_light_bundle':False,'meeting_brief':str(b),'scientific_judgment':'Unknown','freeze_sources_verified_end':True,'curated_files':{str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and p.name not in ['artifact_manifest.json','artifact_manifest.md','artifact_manifest_cn.md']}}
 write(R/'artifact_manifest.json',artifacts)
 md='# A17 R06 evidence index\n\n'+f'Job pt-f2wnbino; {ver["complete_runs"]}/36 runs, {len(saved)} actual saved states.\n\n'
 md+='- [Summary](summary.md) / [中文](summary_cn.md)\n- [Detailed](detailed.md) / [中文](detailed_cn.md)\n- [Frozen protocol](protocol.md)\n- [Deviations](deviations.md)\n- [Reproduce sources and receipts](reproduce/README_cn.md)\n- [Complete coverage](coverage.md)\n\n'
 md+='Execution payload: '+str(ROOT)+'. Actual weights/optimizer remain there. Assets: '+family+', '+analysis_id+'. Asset access and scientific eligibility are separate. Current strict output check follows registration. No Git publication was requested or performed in this round.\n'
 (R/'artifact_manifest.md').write_text(md);(R/'artifact_manifest_cn.md').write_text(md)
 prov={'input':'curves.csv and endpoints_36.csv from saved per-item DEV','primary_endpoint':240,'x':'36 * optimizer steps, cumulative new answer targets','aggregation':'equal-weight3continuation orders sharing1old model','uncertainty_band':'observed minimum-to-maximum of3orders, not confidence interval','smoothing':'none','TEST':False,'script':str(ROOT/'ops/analyze.py'),'script_sha256':sha(ROOT/'ops/analyze.py')}
 write(R/'figures/provenance.json',prov)
 # Complete the factual certificate without changing the Protocol.
 with (R/'execution_certificate.md').open('a') as f:f.write(f'\n## Terminal\n\n{term["status"]} at {term["utc"]}; {ver["complete_runs"]}/36 step240 runs, wallclock {elapsed:.3f}sec. Frozen bytes unchanged, other model tensors unchanged; output family registered. TensorBoard tag-axis repair preserves originalevents; canonical reconstructedevents all checked.\n')
 print(json.dumps({'round':str(R),'meeting_brief':str(b),'saved_states':len(saved),'training_seconds':elapsed,'asset_ids':[family,analysis_id]},ensure_ascii=False))
if __name__=='__main__':main()
