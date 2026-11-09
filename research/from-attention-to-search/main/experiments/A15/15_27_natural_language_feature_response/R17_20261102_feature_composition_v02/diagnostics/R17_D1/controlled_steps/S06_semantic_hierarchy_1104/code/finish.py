from common import *
import shutil,subprocess,sys,os
assert json.load(open(R/'evidence/verification.json'))['status']=='PASS'
ver=json.load(open(R/'results/verdict.json'));primary=json.load(open(R/'results/primary.json'))
# Factual scoped Anchor update only; preserves eight sections and researcher-owned acceptance.
ar=SYS/'Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
for aid,h,stem in [('15_27_06','H1','15_27_06_common_members_extra_responses_anchor'),('15_27_07','H2','15_27_07_conditional_relative_strength_anchor')]:
 rr=[r for r in primary if r['hypothesis']==h];entries='; '.join(f"{r['site']}/{r['domain']}: estimate={r['estimate']}, n={r['eligible']}/8, Holm p={r['p_holm']}" for r in rr)
 for cn in [False,True]:
  p=ar/(stem+('_cn' if cn else '')+'.md');t=p.read_text();assert 'S06 bounded result evidence' not in t
  if cn:para=f'\n### S06 bounded result evidence · 2026-11-04\n\n本轮完成384条、两套SAE、16模板簇的固定8/8划分、全部行为／H1／H2／改写对照与数值复核。{entries}。这些是激活坐标中的局部操作统计，完整列表复现、反例、跨措辞资格和AI分支判定由[本轮Summary]({C}/summary_cn.md)拥有。H1重叠子预测不能代替具体成员复现；H2不适用配对保持缺失资格。旧候选和S02–S05原件保留。本轮任务事实完成，科学接受、机制判断和关闭仍Unknown。\n'
  else:para=f'\n### S06 bounded result evidence, 2026-11-04\n\nCompleted384prefixes, two separate SAEs, sixteen frame clusters with fixed8/8split, native behavior, all H1/H2 and wording controls, and independent numerical replay. {entries}. These are local activation-coordinate statistics; [Summary]({C}/summary.md) owns candidate replication, counterexamples, cross-wording eligibility and bounded AI verdicts. H1 overlap is a subprediction, not a substitute for member events; H2 ineligible pairs remain ineligible. Original candidates and S02–S05 bytes preserved. Task completion does not change researcher acceptance, mechanism judgment or closure: Unknown.\n'
  t=t.replace('\n## 8.',para+'\n## 8.',1).replace('Current round: NOT RUN.','Current round: completed bounded S06; scientific acceptance Unknown.').replace('当前状态：NOT RUN。','当前状态：S06有界计算完成，科学接受Unknown。')
  p.write_text(t)
 # Expand existing bounded sync profiles, preserving their other sources.
 cfgpath=SYS/'sync/anchors/profiles.json';cfg=json.load(open(cfgpath));entry=next(e for e in cfg['entries'] if e['anchor_id']==aid and e['project']=='from-attention-to-search')
 rel=[str((C/n).relative_to(SYS)) for n in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','detailed.md','detailed_cn.md','casebook_cn.md','prior_audit.md','reproduce.md']]
 entry['sources']=list(dict.fromkeys(entry['sources']+rel));dump(cfgpath,cfg)
ledger=[]
for task,status,evidence,boundary in [
 ('source threads/memory/asset identity','DONE_VALID','evidence/referenced_threads.json;input_access.json;prior_audit.json','Named sources only; old files immutable'),
 ('protocol and data frozen before response','DONE_VALID','evidence/protocol_freeze.json;data/panel.jsonl','384rows/16frames, fixed8/8'),
 ('discovery then candidate freeze gate','DONE_VALID','evidence/candidates_frozen.json','64explicit discovery only; no heldout fitting'),
 ('native behavior all384rows','DONE_VALID','data/behavior_all.jsonl','Parents/negatives no gold; errors retained'),
 ('H1 supports/events/all comparisons','DONE_VALID','results/overlaps.csv;candidate_coverage.csv','Associations, no semantic feature naming'),
 ('H2 fixed/dynamic joint/rank patterns','DONE_VALID','results/joint_patterns.csv;rank_pairs.csv','Fixed-support eligibility separately reported'),
 ('lexical/syntax/crossdomain/negative controls','DONE_EXPLORATORY','results/wording_controls.csv;overlaps.csv','Property cues and varying positions remain'),
 ('random/shuffled/family references','DONE_VALID','results/matched_candidate_baselines.csv;family_pairing_controls.csv','Unmatched lists explicit; no threshold relaxation'),
 ('shared-parent structure/paired decomposition','DONE_VALID','results/shared_parent_geometry.csv;difference_decomposition.csv','No semantic direction claim'),
 ('TopK/preactivation/scale/reconstruction','DONE_VALID','results/preactivation_events.csv;row_metrics.csv','Coordinate differences not causal contributions'),
 ('old candidate unchanged retest','DONE_VALID','results/old_S03_candidates.csv','New selection never called old selection'),
 ('independent numerical audit','DONE_VALID','evidence/verification.json','Engineering verification is not scientific acceptance'),
 ('reports/cases/static figures','DONE_VALID','summary_cn.md;detailed_cn.md;casebook_cn.md;figures','AI operational verdict, researcher acceptance Unknown'),
 ('memory/local reading sync/package','DONE_VALID','evidence/final_delivery.json','Local delivery; no external publication')]:ledger.append(dict(task=task,status=status,evidence=evidence,boundary=boundary))
table(R/'evidence/coverage_ledger.csv',ledger)
dump(R/'large_files_index.json',dict(UTC=now(),not_in_package=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),contains='Full30000-dimensional preactivation/z plus h/ranks/cutoffs/reconstruction; weights excluded') for p in (R/'cache').glob('*.npz')],portable_complete=['384texts/tokens','all sparse z in each30000dictionary','all native candidate token scores','full summary CSVs','selected complete preactivations','scripts/config/figures'],excluded=['model/SAE weights','unselected full preactivation matrices','private conversation memory','unrelated files']))
dump(R/'evidence/completed.json',dict(UTC=now(),task_state='COMPLETED_BOUNDED_S06',data_rows=384,domains=2,SAEs=2,template_clusters=16,heldout_clusters=8,job_id=None,device='CPU',GPU_used=0,training=0,H3='NOT_RUN_BY_PROTOCOL',H4='NOT_RUN_BY_PROTOCOL',router='NOT_RUN_BY_PROTOCOL',scientific_acceptance='Unknown',question_closure='Unknown',next_experiment='NOT_RUN'))
# Refresh the existing derived map only for the two owned questions; no Graph or scientific state changes.
proj=SYS/'Projects/from-attention-to-search';mapfile=proj/'main/research_map.json';mapping=json.load(open(mapfile));relC=str(C.relative_to(proj))
for node in mapping['anchors']:
 if node['id'] not in ['15_27_06','15_27_07']:continue
 node['source_sha256']=sha(proj/node['source'])
 node['approach_cn']+=' S06补充384条自然层级文本、16模板簇固定8/8、两字典独立成员／联合强弱及改写留出。'
 node['evidence_state_cn']+=' S06有界观察完成，具体复现与不足逐类别/字典/措辞报告；旧结果不变。'
 node['boundary_cn']+=' S06为条件组合关联；H1重叠不替代成员事件，H2固定列表身份资格另列；词面/位置/重构仍限制语义推广。'
 for field in ['related_results','evidence_sources']:
  node[field]=list(dict.fromkeys(node.get(field,[])+[relC+'/summary.md',relC+'/summary_cn.md',relC+'/detailed_cn.md']))
 node['evidence_sources_sha256']={p:sha(proj/p) for p in node['evidence_sources'] if (proj/p).is_file()}
mapping['bounded_refresh_20261104_S06']=dict(UTC=now(),anchors=['15_27_06','15_27_07'],scope='factual completed round and evidence boundary only',scientific_acceptance='Unknown')
dump(mapfile,mapping)
for cn in [False,True]:
 p=proj/'main'/('research_map_cn.md' if cn else 'research_map.md')
 with p.open('a') as f:f.write(f'\n\n### S06 semantic hierarchy, 2026-11-04\n\n[H1/H2 bounded combination results]({relC.removeprefix("main/")}/summary_cn.md):384prefixes,16shared frame clusters, fixed8/8, two independent native dictionaries. Category/wording-specific membership and joint-strength replication are separated from behavior and causal claims. Scientific acceptance/closure Unknown; previous results preserved.\n')
html=Path('/data/250010109/MoE_Router/research_reading/20261031_project_map/research_map.html');html.parent.mkdir(parents=True,exist_ok=True)
render=subprocess.run([sys.executable,str(proj/'scripts/render_research_map.py'),'--data',str(mapfile),'--output',str(html)],capture_output=True,text=True);assert render.returncode==0,render.stderr
dump(R/'evidence/map_refresh.json',dict(UTC=now(),anchors=['15_27_06','15_27_07'],map_sha256=sha(mapfile),html=str(html),html_sha256=sha(html),published=False))
# Register actual outputs through the existing registry schema.
catpath=SYS/'assets/catalog.json';before=sha(catpath);cat=json.load(open(catpath));names=[('data_s06_sae_semantic_hierarchy_20261104','dataset','constructed_semantic_hierarchy_panel',['data/panel.jsonl','data/templates.json','frozen_plan.json']),('representation_s06_dual_sae_hierarchy_20261104','representation','native_prefix_dual_SAE_sparse_and_preactivation',['data/ATTN_SAE_all_z_csr.npz','data/MLPIN_SAE_all_z_csr.npz','cache/discovery.npz','cache/remaining.npz','evidence/candidates_frozen.json']),('analysis_s06_sae_semantic_hierarchy_20261104','analysis','frozen_H1_H2_joint_combination_analysis',['results/selection.json','results/hypothesis_statistics.csv','results/joint_patterns.csv','evidence/verification.json','evidence/completed.json'])]
for aid,category,kind,probes in names:
 assert not any(a['id']==aid for a in cat['assets'])
 cat['assets'].append(dict(id=aid,title_cn='S06 SAE特征组合与语义层级 '+category,category=category,kind=kind,payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=p,expected='file',required=True) for p in probes])],identity=dict(rows=384,families_per_domain=16,template_clusters=16,split='F01-08discovery/F09-16heldout',primary_anchors=['15_27_06','15_27_07'],model_asset='model_qwen3_0p6b_base_official_a5',SAEs=[v['asset_id'] for v in json.load(open(R/'frozen_plan.json'))['sites'].values()],data_sha256=sha(R/'data/panel.jsonl'),selection_sha256=sha(R/'results/selection.json'),scientific_acceptance='Unknown'),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'summary.md'),str(R/'frozen_plan.json')]))
assert sha(catpath)==before;dump(catpath,cat)
check=subprocess.run([sys.executable,str(SYS/'tools/check_assets.py'),'--strict',*[x for aid,_,_,_ in names for x in ['--asset',aid]],'--output',str(R/'evidence/output_access.json')],capture_output=True,text=True);assert check.returncode==0,check.stdout+check.stderr
(R/'evidence/output_access_console.txt').write_text(check.stdout)
guide=SYS/'assets/sae_hierarchy_s06_20261104.md';guide.write_text(f'''# S06 semantic hierarchy assets

Actual384prefixes,16frames/domain, correlated across the two domains, fixed8/8discovery/heldout. Same verified official Qwen3-0.6B Base and separate final Attention-output/MLP-input30000/ReLU-Top32 SAE dictionaries. No training or causal intervention. The three IDs `{names[0][0]}`, `{names[1][0]}`, `{names[2][0]}` register data, actual sparse/full cached representations, and bounded analysis separately. Current strict access: [{R}/evidence/output_access.json]({R}/evidence/output_access.json). [Reading result]({C}/summary_cn.md). Full preactivation/h remains execution-side and is excluded from the<20MBpackage, while complete sparse z,384texts/tokens, all scores and summaries are included. Researcher acceptance/closure Unknown; access does not confer semantic or execution authority.
''')
# Canonical evidence receives the small final check/coverage records, not raw matrices.
(C/'evidence').mkdir(exist_ok=True)
for n in ['verification.json','prior_audit.json','coverage_ledger.csv','completed.json','protocol_freeze.json','candidates_frozen.json','output_access.json','figure_provenance.json','figure_review.json','position_audit.csv']:
 if (R/'evidence'/n).exists():shutil.copy2(R/'evidence'/n,C/'evidence'/n)
for n in ['large_files_index.json','reproduce.md']:shutil.copy2(R/n,C/n)
print('FINISH_RECORDS',check.stdout,flush=True)
