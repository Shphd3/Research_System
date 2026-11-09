from common import *
import re,shutil,fcntl,subprocess,sys
assert json.load(open(R/'evidence/verification.json'))['status']=='PASS'
assert json.load(open(R/'evidence/figure_review.json'))['status']=='PASS'
out=json.load(open(R/'results/summary.json'));main=[x for x in out['summaries'] if x['split']=='heldout' and x['mode']=='main'];stamp=now()
P=SYS/'Projects/from-attention-to-search';base=P/'main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors';old=base/'15_27_10_near_far_fact_use'
newpaths={old/'anchor.md':base/'15_27_10_near_far_fact_use_anchor.md',old/'anchor_cn.md':base/'15_27_10_near_far_fact_use_anchor_cn.md'}
snapshot={}
for before,after in newpaths.items():
    assert not after.exists();arch=R/'versions'/('frozen_'+before.name);shutil.copy(before,arch);snapshot[str(before)]=dict(archive=str(arch),sha256=sha(arch),current=str(after))
    text=before.read_text();cn=before.name.endswith('_cn.md')
    result=', '.join(f"d{x['planned_distance']}={x['paired_success']}/24" for x in main)
    addition=(f'\nR18 completed all444prefixes. Main heldout paired successes: {result}. These are candidate rankings; all families, uncertainty and controls remain in [Summary]({C}/summary.md). Scientific acceptance and permission for SAE work remainUnknown; execution stops for joint review.\n' if not cn else f'\nR18全部444条完成；主留出成对正确：{result}。这是候选排序结果，完整家族、区间与对照由[Summary]({C}/summary_cn.md)保存；科学接受和SAE授权Unknown，执行停在共同审阅前。\n')
    text=text.replace('\n## 8.',addition+'\n## 8.',1)
    text=text.replace('../../../../../experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/protocol.md',str(C/'protocol.md'))
    after.write_text(text);before.unlink();before.symlink_to(after)
    ep=C/before.name;ep.unlink();ep.symlink_to(after)
dump(R/'evidence/frozen_owner_resolution.json',dict(UTC=stamp,reason='Post-run factual result update plus repository numbered-child placement repair. Scientific question/criteria unchanged; original bytes archived.',files=snapshot,registry_id='15_27_10',protocol_bodies_unchanged=True))
reg=P/'main/anchor_ownership.json';registry=json.load(open(reg));entry=next(x for x in registry['anchors'] if x['id']=='15_27_10');entry['path']=str(newpaths[old/'anchor.md'].relative_to(P));entry['companions']=[str(newpaths[old/'anchor_cn.md'].relative_to(P))];entry['experiment_roots']=[];entry['experiment_navigation_note']='R18 is physically inside the existing15_27parent experiment root; exact current question owned by15_27_10 and linked by its Protocol, avoiding overlapping filesystem ownership.';dump(reg,registry)
# Update only navigation added by this conversation.
for file in [P/'main/roadmap.md',P/'main/roadmap_cn.md']:
    s=file.read_text()
    for before,after in newpaths.items():s=s.replace(str(before.relative_to(P/'main')),str(after.relative_to(P/'main')))
    file.write_text(s)
F=P/'main/focus/focus_near_far_object_fact_use.md';s=F.read_text().replace('`AUTHORIZED_BEHAVIOR_EXECUTION`','`BEHAVIOR_DELIVERED_WAIT_FOR_RESEARCHER_REVIEW`').replace('result_state: `NOT_RUN`','result_state: `PAIRED_BEHAVIOR_MEASURED_ALL_REGISTERED_CONDITIONS`')
for before,after in newpaths.items():s=s.replace(str(before),str(after))
s+=f'\n\n## Actual bounded endpoint, {stamp}\n\nMain paired successes: '+', '.join(f"d{x['planned_distance']}:{x['paired_success']}/24" for x in main)+f'. All444prefixes retained. [Summary]({C}/summary.md), [raw pairs]({R}/tables/family_pairs.csv). The researcher has not approved a next scientific stage.\n';F.write_text(s)
Fc=F.with_name(F.stem+'_cn.md');s=Fc.read_text();s+=f'\n\n完成状态：本轮444条和所有对照已完成；主留出'+', '.join(f"d{x['planned_distance']}={x['paired_success']}/24" for x in main)+f'。任务已交付待审阅，问题仍激活，设计冻结不变，结果已测量。科学接受、关闭、下一步授权Unknown。[Summary]({C}/summary_cn.md)。\n';Fc.write_text(s)
# Existing project standing authorization covers bounded collaborative-map maintenance.
mp=P/'main/research_map.json';mapping=json.load(open(mp));assert not any(x['id']=='15_27_10' for x in mapping['anchors'])
ev=[C/name for name in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','detailed.md','detailed_cn.md']]
mapping['anchors'].append(dict(id='15_27_10',line='A15',parent_id='15_27',title_cn='近远物品事实的行为利用',question_cn='局部提问相同，前文物品改变时，冻结模型能否在近远距离都正确切换答案？',why_cn='先确认当前受控任务中的模型行为，避免把固定token的feature上下文敏感性当成成功利用远处事实。',approach_cn='24留出家族、24物品对、六模板；主实际间隔16/64/128，固定320token；完整候选序列评分，A/B成对切换，另保留无事实基线、自然改写和近处错误物品诱饵。',role_for_parent_cn='自然语言上下文响应研究中的局部行为资格关卡；执行完成后停止，不替代SAE关联、功能机制或训练判断。',evidence_state_cn='全部444前缀完成；主成对正确'+', '.join(f"d{x['planned_distance']}={x['paired_success']}/24" for x in main)+'。完整家族、区间、先验及对照由Summary持有；下一步待研究者共同讨论。',boundary_cn='只测构造英语任务的候选排序；实际距离定义不等于学长按跨语境变化定义的长短程，不证明普遍记忆或SAE机制。无训练、SAE分析或激活干预；科学接受Unknown。',source=str(newpaths[old/'anchor.md'].relative_to(P)),source_sha256=sha(newpaths[old/'anchor.md']),related_results=[str((C/'summary.md').relative_to(P)),str((C/'summary_cn.md').relative_to(P))],evidence_sources=[str(x.relative_to(P)) for x in ev],evidence_sources_sha256={str(x.relative_to(P)):sha(x) for x in ev},reviewed_on='2026-11-04',change_kind='User-activated bounded behavior question and factual delivery; no scientific acceptance',related_questions=[dict(id='15_27_03',label_cn='旧R09固定目标的feature距离响应，观察对象不同'),dict(id='15_27_06',label_cn='共同成员研究的行为背景，不授予下一轮执行')]))
mapping['counts']['anchors']=len(registry['anchors']);mapping['counts']['parents']=sum(x.get('parent_id') is None for x in registry['anchors']);mapping['counts']['subanchors']=sum(x.get('parent_id') is not None for x in registry['anchors']);mapping['registry_sha256']=sha(reg)
for line in mapping['lines']:
    if line['id']=='A15':line['owner_count']+=1;line['subanchor_count']+=1
mapping['refresh']['new_anchor_ids']=list(dict.fromkeys(mapping['refresh'].get('new_anchor_ids',[])+['15_27_10']));mapping['refresh']['groups'].append(dict(title_cn='进入距离组合研究之前先测行为',question_cn='近远物品事实能否控制成对答案？',observation_cn='R18固定数据完成；全部家族和控制保留，下一步待共同讨论。',ids=['15_27_10']))
mapping['bounded_refresh_20261104_R18']=dict(UTC=stamp,scope='new user-activated local behavior guard and raw facts only',standing_authorization='Project AGENTS Collaborative Research Map',scientific_acceptance='Unknown');dump(mp,mapping)
q=subprocess.run([sys.executable,str(P/'scripts/build_research_map_reading.py')],text=True,capture_output=True);assert q.returncode==0,q.stdout+q.stderr
q=subprocess.run([sys.executable,str(P/'scripts/render_research_map.py'),'--data',str(mp),'--output','/data/250010109/MoE_Router/research_reading/20261104_project_map/research_map.html'],text=True,capture_output=True);assert q.returncode==0,q.stdout+q.stderr
dump(R/'evidence/completed.json',dict(UTC=stamp,execution='COMPLETED',prefixes=444,families=28,heldout_families=24,all_conditions_retained=True,training_updates=0,SAE_analysis=False,interventions=False,scientific_acceptance='Unknown',next_stage='STOP_WAIT_FOR_RESEARCHER_DISCUSSION',navigation_sync='PENDING_LOCAL_SYNC',job_id='NOT_APPLICABLE_LOCAL_CPU'))
aid='analysis_r18_near_far_object_fact_behavior_20261104';entry=dict(id=aid,title_cn='R18近远物品事实配对行为评分',category='analysis',kind='complete_candidate_sequence_paired_fact_switching',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=f,expected='file',required=True) for f in ['config.json','results/smoke.jsonl','results/heldout.jsonl','tables/family_pairs.csv','tables/distance_summary.csv','evidence/verification.json','evidence/completed.json']])],identity=dict(parent_dataset='dataset_r18_near_far_object_fact_pairs_20261104',model='model_qwen3_0p6b_base_official_a5',tokenizer='tokenizer_qwen3_0p6b_base_official_a5',prefixes=444,heldout_families=24,main_gaps=[16,64,128],full_candidate_chain=True,dtype='float32',device='cpu',training=False,SAE_analysis=False,intervention=False,scientific_acceptance='Unknown'),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'summary.md'),str(R/'config.json')])
with (SYS/'assets/.catalog_registration.lock').open('a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX);path=SYS/'assets/catalog.json';catalog=json.load(open(path));assert not any(x['id']==aid for x in catalog['assets']);catalog['assets'].append(entry);dump(path,catalog);count=len(catalog['assets'])
checkpath=SYS/'assets/checks/2026-11-04_r18_behavior_outputs.json';assert not checkpath.exists()
check=subprocess.run([sys.executable,str(SYS/'tools/check_assets.py'),'--strict','--asset','dataset_r18_near_far_object_fact_pairs_20261104','--asset',aid,'--output',str(checkpath)],text=True,capture_output=True);assert check.returncode==0,check.stdout+check.stderr
shutil.copy(checkpath,R/'evidence/output_access.json');dump(R/'evidence/analysis_registration.json',entry)
guide=SYS/'assets/README.md';s=guide.read_text();s=re.sub(r'registers \*\*\d+ entries',f'registers **{count} entries',s,count=1);s+='\n\n### R18 near/far object-fact behavior, 2026-11-04\n\nFrozen official Base model/tokenizer,444constructed English prefixes,24heldout families and exact16/64/128main gaps. [Selected current output access](checks/2026-11-04_r18_behavior_outputs.json) covers dataset_r18_near_far_object_fact_pairs_20261104 and analysis_r18_near_far_object_fact_behavior_20261104, not a whole-library refresh. [Canonical Summary]('+str(C/'summary.md')+') owns observations and boundaries; all raw scores remain execution-side. No SAE/training/intervention or further execution authorization.\n';guide.write_text(s)
profilepath=SYS/'sync/anchors/profiles.json';profiles=json.load(open(profilepath));assert not any(x['anchor_id']=='15_27_10' for x in profiles['entries']);sources=[*newpaths.values(),F,Fc,*[C/name for name in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','detailed.md','detailed_cn.md','dataset_guide.md','dataset_guide_cn.md','prior_context.md','prior_context_cn.md','cases_selected_cn.md','families_cn.md','artifacts.md','reproduce.md','reproduce_cn.md']]];profiles['entries'].append(dict(project='from-attention-to-search',anchor_id='15_27_10',sources=[str(p.relative_to(SYS)) for p in sources]));dump(profilepath,profiles)
for file,txt in [('README.md','\n- [A15_27_10: near/far object-fact behavior](from-attention-to-search/15_27_10/README.md): bounded behavior prerequisite; paired raw examples, all family outcomes, thresholds and uncertainty; no SAE/training/intervention, scientific acceptanceUnknown. Local reading copy.\n'),('README_cn.md','\n- [A15_27_10：近远物品事实行为](from-attention-to-search/15_27_10/README.md)：本轮行为前置关卡，含完整原文、逐家族数据、操作门槛与不确定性；无SAE／训练／干预，科学接受Unknown，仅本地阅读副本。\n')]:
    with (SYS/'sync/anchors'/file).open('a') as f:f.write(txt)
for name in ['source_recovery.json','token_leakage_audit.json','dataset_access.json','dataset_registration.json','frozen_owner_resolution.json','figure_review.json','completed.json','output_access.json','analysis_registration.json']:shutil.copy(R/'evidence'/name,C/'evidence'/name)
shutil.copy(R/'code/finish.py',C/'code/finish.py')
M=SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md';ms=M.read_text();ms=re.sub(r'^Latest update at: .+$','Latest update at: '+stamp,ms,count=1,flags=re.M);M.write_text(ms)
with M.open('a') as f:f.write(f'''\n\n## {stamp} -- 全部行为计算与事实记录完成，等待共同审阅

Processed by: Codex /root (harness: Codex desktop; model: GPT-6)

- Summary: 当前授权的444前缀、28家族（24留出）、三个主距离和全部基线／自然改写／近处错误物品对照完成，全部原始结果保留。结果及认识边界由Summary拥有；此处不授予科学接受。模型／tokenizer哈希保持，无SAE读取、训练或激活干预。
- Current work: 数值／token／完整评分复核PASS，图已查看。编号Anchor物理位置规范化，旧冻结字节执行侧留存，旧路径为同owner别名；协议正文未改。两个输出资产已登记且strict通过。按项目AGENTS已有协作地图站立授权新增本题导航及派生阅读／本地视图，既有科学结论不改。Anchor本地阅读副本正在最后同步；无commit／push／发布。
- Next action: 本轮完成即停止。研究者看逐家族数据及成功／失败全文，共同决定是否、在哪个任务条件进入SAE；不得自动改模板重测或启动下一轮。
- References: {C/'summary_cn.md'}；{C/'cases_selected_cn.md'}；{C/'artifacts.md'}；{R/'tables/family_pairs.csv'}；{R/'evidence/verification.json'}；{newpaths[old/'anchor.md']}。
''')
curated=P/'main/curated_evidence.json';cur=json.load(open(curated));cur['assets']=[x for x in cur['assets'] if not x['path'].startswith(str(C.relative_to(P))+'/')]
for sub in ['figures','tables','evidence']:
    for p in sorted((C/sub).glob('*')):
        if p.is_file() and p.suffix in ['.json','.csv','.png']:
            assert p.stat().st_size<=2*1024*1024,(p,'curated size')
            origin=R/p.relative_to(C)
            cur['assets'].append(dict(path=str(p.relative_to(P)),purpose='R18 selected behavioral evidence or provenance; no raw model/data cache',origin=str(origin),sha256=sha(p),bytes=p.stat().st_size))
dump(curated,cur)
dump(R/'output_manifest.json',dict(UTC=stamp,canonical_root=str(C),execution_root=str(R),dataset_asset='dataset_r18_near_far_object_fact_pairs_20261104',analysis_asset=aid,scientific_acceptance='Unknown',stop=True,files={str(p.relative_to(R)):dict(sha256=sha(p),bytes=p.stat().st_size) for sub in ['code','data','results','tables','figures','evidence'] for p in sorted((R/sub).glob('*')) if p.is_file()}));shutil.copy(R/'output_manifest.json',C/'manifest.json')
print('RECORDS_AND_REGISTRATION_COMPLETE; local sync still required')
