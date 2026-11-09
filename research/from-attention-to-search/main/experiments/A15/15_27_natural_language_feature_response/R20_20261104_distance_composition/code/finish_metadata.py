from common import *
import shutil,fcntl,re
ids=['dataset_r20_distance_composition_panel_20261104','representation_r20_distance_native_dual_sae_20261104','analysis_r20_distance_composition_20261104']
cat=SYS/'assets/catalog.json'
with cat.open('r+') as f:
 fcntl.flock(f,fcntl.LOCK_EX);j=json.load(f)
 for k,aid in enumerate(ids):
  assert not any(a['id']==aid for a in j['assets']),aid
  probes=[['data/panel.jsonl','data/condition_mapping.json','effective_config.json','evidence/construction.json'],['cache/ATTN_SAE_old_main.npz','cache/MLPIN_SAE_old_main.npz','cache/new_all.npz','evidence/cache_consolidation.json','evidence/full_complete.json'],['tables/baseline_fact_contrasts.csv','tables/control_family_differences.csv','results/primary_hypotheses.json','evidence/verification_all.json']][k]
  identity=dict(parent_R19='representation_r19_native_dual_sae_composition_20261104',model='model_qwen3_0p6b_base_official_a5',native_SAEs=[json.load(open(R/'config.json'))['sites'][s]['asset_id'] for s in SITES],dictionaries_separate=True,observed_conditions=372,old_main=144,new_literal_texts=192,same_text_position_id_conditions=36,new_control_forward_conditions=228,old_forward_calibrations=6,families=24,primary_old_heldout_families=12,old_heldout_exposed=True,native_features=30000,topk=32,gaps=[16,64,128],gap_definition='p-e-1; both endpoints excluded; evidence last item token',training=False,activation_interventions=False,scientific_acceptance='Unknown',panel_sha256=sha(R/'data/panel.jsonl'))
  j['assets'].append(dict(id=aid,title_cn=['R20距离配对文本与位置填充对照','R20两原生SAE完整距离观察缓存','R20距离组合及频率机会分析'][k],category=['dataset','representation','analysis'][k],kind='distance_paired_native_sae_observation_with_bounded_controls',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=x,expected='file',required=True) for x in probes])],identity=identity,projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'summary.md'),str(C/'protocol.md'),str(R/'effective_config.json')]))
 j.setdefault('catalog_amendments',[]).append(dict(UTC=now(),action='Register actual R20distance-only observations,lossless control cache and analysis; no training/interventions',asset_ids=ids));f.seek(0);f.write(json.dumps(j,ensure_ascii=False,indent=2)+'\n');f.truncate();fcntl.flock(f,fcntl.LOCK_UN)
for name in ['README.md','README_cn.md']:
 p=SYS/'assets'/name;s=p.read_text();s=re.sub(r'\*\*\d+ entries and (\d+) project/storage roots\*\*',lambda m:f'**{len(j["assets"])} entries and {m.group(1)} project/storage roots**',s);s+=f'\n[R20distance and native SAE combinations]({C/"summary.md"}):144old main conditions plus228bounded forward controls; all native code magnitudes/directions and frequency opportunities, no training or intervention.\n';p.write_text(s)
dump(R/'evidence/output_assets.json',dict(UTC=now(),ids=ids,actual_saved=True))
# Selected small evidence only; complete raw outputs remain execution-side or in packet.
for folder in ['code','figures']:
 for source in (R/folder).iterdir():
  if source.is_file() and source.suffix in ['.py','.png','.json']:
   dest=C/folder/source.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
for folder in ['tables','evidence','results']:
 for source in (R/folder).iterdir():
  if source.is_file() and source.suffix in ['.csv','.json'] and source.stat().st_size<=2*1024*1024:
   dest=C/folder/source.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
for source in [R/'config.json',R/'effective_config.json']:(C/source.name).write_bytes(source.read_bytes())
for source in (R/'data').glob('*_bins.json'):
 dest=C/'config'/source.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
small=[]
for dest in C.rglob('*'):
 if dest.is_file() and dest.suffix in ['.json','.csv','.png','.svg']:
  rel=dest.relative_to(C);origin=R/rel
  if rel.parts[0]=='config':origin=R/'data'/dest.name
  small.append(dict(path=str(dest.relative_to(P)),purpose='R20 selected auditable evidence: '+str(rel),origin=str(origin),sha256=sha(dest),bytes=dest.stat().st_size))
manifest=P/'main/curated_evidence.json';j=json.load(open(manifest));prefix=str(C.relative_to(P))+'/';j['assets']=[a for a in j['assets'] if not a['path'].startswith(prefix)]+small;dump(manifest,j)
# Standing project map maintenance: add this owner, preserve all older judgments.
registry=json.load(open(P/'main/anchor_ownership.json'));owner=next(x for x in registry['anchors'] if x['id']=='15_27_12');mp=P/'main/research_map.json';j=json.load(open(mp));root=str(C.relative_to(P));sources=[C/name for name in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','detailed.md','detailed_cn.md']];assert not any(x['id']=='15_27_12' for x in j['anchors'])
j['anchors'].append(dict(id='15_27_12',line='A15',parent_id='15_27',title_cn='距离与回答处的SAE组合',question_cn='同一事实离答案更远时，成员、幅度和事实差异怎样变？',why_cn='旧方向相似不等于幅度不变；需完整码/截断与位置填充对照。',approach_cn='原12留出重算；两字典分开，全部Top32和六成员保留零；228补充条件，族单位区间和频率机会。',role_for_parent_cn='距离关联的观测与测量资格，不研究竞争错因或训练。',evidence_state_cn='R20全部完成：平均共同24.79/27.92，相对事实差异比1.0803/1.1989。H1≥90%保留未支持；H2Attention容差保持支持、MLP不足；H3≥20%衰减未支持。反转/办公/固定e均值>1；F28近距反转失败保留。',boundary_cn='真实事实差重构误差约.994/.984，码范数非总信息量；旧留出已暴露、模板共享，不能分离纯距离。无干预/训练；科学接受Unknown。',source=owner['path'],source_sha256=sha(A),related_results=[root+'/summary.md',root+'/summary_cn.md'],evidence_sources=[str(s.relative_to(P)) for s in sources],evidence_sources_sha256={str(s.relative_to(P)):sha(s) for s in sources},reviewed_on='2026-11-04',change_kind='Current user-authorized distance study and factual delivery only',related_questions=[dict(id='15_27_11',label_cn='原R19资产与六成员方向背景'),dict(id='15_27_10',label_cn='行为起点，原件保留')]))
j['registry_sha256']=sha(P/'main/anchor_ownership.json');j['counts'].update(anchors=len(registry['anchors']),parents=sum(not x.get('parent_id') for x in registry['anchors']),subanchors=sum(bool(x.get('parent_id')) for x in registry['anchors']));line=next(x for x in j['lines'] if x['id']=='A15');owners=[a for a in registry['anchors'] if a['line']=='A15'];line.update(owner_count=len(owners),subanchor_count=sum(bool(a.get('parent_id')) for a in owners),children_count=sum(not a.get('parent_id') for a in owners));j['refresh']['new_anchor_ids'].append('15_27_12');j['refresh']['groups'].append(dict(title_cn='距离与组合重组',question_cn='成员更替是否伴随事实差异减弱？',observation_cn='原R19重算与228对照完成，主要观察为更替而无平均幅度衰减；重构误差与识别边界保留。',ids=['15_27_12']));dump(mp,j)
profiles=SYS/'sync/anchors/profiles.json';j=json.load(open(profiles));assert not any(x['anchor_id']=='15_27_12' for x in j['entries']);src=[A,A.with_name(A.stem+'_cn.md'),FOCUS,FOCUS.with_name(FOCUS.stem+'_cn.md')]+[C/name for name in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','detailed.md','detailed_cn.md','dataset_guide.md','dataset_guide_cn.md','numeric_evidence.md','casebook.md','casebook_cn.md','frequency.md','frequency_cn.md','supplement_failures.md','artifacts.md','artifacts_cn.md','reproduce.md','reproduce_cn.md']]+sorted((C/'cases').glob('*.md'));j['entries'].append(dict(project='from-attention-to-search',anchor_id='15_27_12',sources=[str(s.relative_to(SYS)) for s in src]));dump(profiles,j)
for name in ['README.md','README_cn.md']:
 p=SYS/'sync/anchors'/name;s=p.read_text();s+='\n- [15_27_12: distance-associated SAE combinations](from-attention-to-search/15_27_12/README.md): R20 complete observations/controls, raw cases and limits; scientific acceptance Unknown.\n';p.write_text(s)
print('REGISTERED_AND_CURATED',ids,len(small))
