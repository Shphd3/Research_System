from common import *
import shutil,subprocess,sys
assert json.load(open(R/'evidence/verification.json'))['status']=='PASS'
proj=SYS/'Projects/from-attention-to-search';ar=proj/'main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors'
for aid,stem in [('15_27_06','15_27_06_common_members_extra_responses_anchor'),('15_27_07','15_27_07_conditional_relative_strength_anchor')]:
 for cn in [False,True]:
  p=ar/(stem+('_cn' if cn else '')+'.md');t=p.read_text();assert 'S07 completed local intervention evidence' not in t
  if cn:
   t=t.replace('### S07 intervention supplement, authorized2026-11-04','### S07干预补充：2026-11-04研究者明确授权')
   start=t.index('After completed/saved S06,');end=t.index('\n',start)
   t=t[:start]+f'主S06完成并保存后，研究者授权对发现集固定组合临时删除／重组强弱。注入原表征加decoder线性改变量，保留原重构残差。按发现频率／强度／数量及实际扰动范数设对照，原留出文本读取完整候选分数、词表排名／分布与跨域变化。此补充检验局部输出敏感性，不判定唯一自然机制或真实概念转换。[S07完整协议]({C}/protocol_cn.md)。启动时状态NOT RUN；科研接受Unknown。'+t[end:]
   para=f'\n### S07 completed local intervention evidence · 2026-11-04\n\n主S06文件保留；完成96原留出前缀、14976干预条件。Attention动物alpha.5相对同成员等范数打乱的正确边际损失差0.00623nats，[0.00135,0.01340]，8家族，Holm p=.03125；主要条件仍16/16正确。共同大组删除经常增强正确边际并改变无关域分布，完整删除匹配不足；交通工具反侧预测未支持或共同支持不足。该结果只支持有界decoder方向敏感性。[干预Summary]({C}/summary_cn.md)拥有完整数值和AI分支判定；科学接受、唯一机制、关闭仍Unknown。\n'
  else:para=f'\n### S07 completed local intervention evidence, 2026-11-04\n\nS06files preserved;96original heldout prefixes,14976temporary edits. Attention animalalpha.5shows a.00623nat margin-loss excess over same-member norm-matched shuffle,95%family interval[.00135,.01340],8families,Holm p=.03125, while all16texts remain correct. Large common deletions often increase correct margins and broadly change other-domain distributions; complete deletion matching fails. Vehicle opposite-pattern prediction is unsupported or support-ineligible. This identifies bounded decoder-direction sensitivity, not unique natural mechanisms or concept conversion. [S07 Summary]({C}/summary.md) owns all comparisons and AI operational verdicts. Researcher acceptance/closure remain Unknown.\n'
  p.write_text(t.replace('\n## 8.',para+'\n## 8.',1))
 # Add only this completed round to the existing registered bounded reading profile.
 cfgpath=SYS/'sync/anchors/profiles.json';cfg=json.load(open(cfgpath));entry=next(e for e in cfg['entries'] if e['anchor_id']==aid and e['project']=='from-attention-to-search')
 entry['sources']=list(dict.fromkeys(entry['sources']+[str((C/n).relative_to(SYS)) for n in ['protocol.md','protocol_cn.md','summary.md','summary_cn.md','detailed.md','detailed_cn.md','casebook_cn.md','reproduce.md']]))
 dump(cfgpath,cfg)
# Update existing derived map sources/boundaries, not Graph or researcher-owned scientific states.
mp=proj/'main/research_map.json';mapping=json.load(open(mp));relC=str(C.relative_to(proj))
for node in mapping['anchors']:
 if node['id'] not in ['15_27_06','15_27_07']:continue
 node['source_sha256']=sha(proj/node['source']);node['evidence_state_cn']+=' S07干预96前缀/14976条件完成：Attention动物仅小的分数方向差，其他对照未支持或不足；删除大共同组非必要性证据。'
 node['boundary_cn']+=' S07为残差保留的decoder方向因果敏感性；主要条件不翻转答案，匹配和无关域作用限制语义定向。'
 for field in ['related_results','evidence_sources']:node[field]=list(dict.fromkeys(node.get(field,[])+[relC+'/summary.md',relC+'/summary_cn.md',relC+'/detailed_cn.md']))
 node['evidence_sources_sha256']={p:sha(proj/p) for p in node['evidence_sources'] if (proj/p).is_file()}
mapping['bounded_refresh_20261104_S07']=dict(UTC=now(),anchors=['15_27_06','15_27_07'],scope='local causal sensitivity with controls and insufficiency preserved',scientific_acceptance='Unknown');dump(mp,mapping)
for cn in [False,True]:
 p=proj/'main'/('research_map_cn.md' if cn else 'research_map.md')
 with p.open('a') as f:f.write(f'\n\n### S07 combination interventions, 2026-11-04\n\n[Residual-preserving local effects and controls]({relC.removeprefix("main/")}/summary_cn.md):96unchangedheldoutprefixes,14976conditions; a small Attention-animal strength-direction effect, broad/common-deletion effects and failed matching remain distinct. No concept conversion or expert-routing conclusion; scientific acceptanceUnknown.\n')
html=Path('/data/250010109/MoE_Router/research_reading/20261031_project_map/research_map.html');p=subprocess.run([sys.executable,str(proj/'scripts/render_research_map.py'),'--data',str(mp),'--output',str(html)],capture_output=True,text=True);assert p.returncode==0,p.stderr
dump(R/'evidence/map_refresh.json',dict(UTC=now(),map_sha256=sha(mp),html_path=str(html),html_sha256=sha(html),published=False))
dump(R/'large_files_index.json',dict(UTC=now(),excluded_from_package=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),reason='All14976full1024-dimensional actual injection vectors; keyF09vectors portable') for p in [R/'cache/all_injected_deltas.npz']],included_small_cache=dict(path='cache/baseline_tail.npz',bytes=(R/'cache/baseline_tail.npz').stat().st_size),no_checkpoint_weights=True,no_full_vocabulary_logits_saved=True,all_conditions_scores_and_four_candidate_distributions_included=True,all_top20_and_tail_mass_included=True))
ledger=[dict(item=item,status=status,evidence=evidence,boundary=bound) for item,status,evidence,bound in [
 ('main completed and immutable','DONE_VALID','evidence/main_delivery_before_S07.json;verification.json','Original S06cache/text/results/package preserved'),
 ('discovery-only candidates/rules','DONE_VALID','data/selection.json;evidence/protocol_freeze.json','No selection on intervention outputs'),
 ('native hooks and residual injection','DONE_VALID','evidence/decoder_identity.json;calibration.json','Exact last-block scope only'),
 ('96baselines/14976edits','DONE_VALID','evidence/run_complete.json;results/conditions.jsonl','No model/SAE training'),
 ('deletion matching','DONE_EXPLORATORY','data/candidate_match_audit.csv;results/control_quality.csv','All common-group complete matches unavailable; specificity insufficient'),
 ('strength/dose/controls/single member','DONE_VALID','results/conditions.jsonl;primary.csv','Identity-changing/unmatched rows excluded only from fixed-support primary'),
 ('all4scores/ranks/top20/distributions','DONE_VALID','results/candidate_ranks_and_probabilities.csv;top20.jsonl','Constrained p4 vs full-vocabulary first-word probabilities distinct'),
 ('family statistics/counterexamples/offdomain','DONE_VALID','results/family_primary.csv;counterexamples.json;offdomain_effects.csv','Eight primary tests; secondary not rescue'),
 ('numerical independent replay','DONE_VALID','evidence/verification.json','No-op and full-hook tolerances retained'),
 ('reencoding diagnostic','DONE_EXPLORATORY','results/key_reencoding_diagnostic.csv','Posthoc quality diagnostic, not new primary'),
 ('figures/reports/portable package','DONE_VALID','evidence/final_delivery.json','Local delivery, scientific acceptance Unknown')]]
table(R/'evidence/coverage_ledger.csv',ledger)
dump(R/'evidence/completed.json',dict(UTC=now(),task_state='COMPLETED_BOUNDED_S07',prefixes=96,intervention_conditions=14976,model_or_SAE_training=False,weights_modified=False,GPU=0,job_id=None,main_unchanged=True,scientific_acceptance='Unknown',question_closure='Unknown',next_experiment='NOT_RUN'))
catpath=SYS/'assets/catalog.json';initial=sha(catpath);cat=json.load(open(catpath));aid='analysis_s07_dual_sae_interventions_20261104';assert not any(a['id']==aid for a in cat['assets'])
cat['assets'].append(dict(id=aid,title_cn='S07 双SAE组合删除/强弱干预及完整候选排名分布',category='analysis',kind='residual_preserving_native_last_block_decoder_interventions',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=p,expected='file',required=True) for p in ['frozen_plan.json','data/selection.json','results/conditions.jsonl','results/top20.jsonl','cache/all_injected_deltas.npz','cache/baseline_tail.npz','evidence/calibration.json','evidence/verification.json','evidence/completed.json']])],identity=dict(parent_asset='representation_s06_dual_sae_hierarchy_20261104',prefixes=96,conditions=14976,SAE_sites=['block27o_proj output','block27actualMLPinput'],residual_preserved=True,primary_tests=8,training=False,scientific_acceptance='Unknown'),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'summary.md'),str(R/'protocol.md')]))
assert sha(catpath)==initial;dump(catpath,cat)
p=subprocess.run([sys.executable,str(SYS/'tools/check_assets.py'),'--strict','--asset',aid,'--output',str(R/'evidence/output_access.json')],capture_output=True,text=True);assert p.returncode==0,p.stdout+p.stderr
(SYS/'assets/sae_interventions_s07_20261104.md').write_text(f'# S07 native decoder interventions\n\nAsset`{aid}`binds96unchangedS06heldoutprefixes and14976actualtemporaryedits, both original nativeSAE sites, full scores/ranks/top20 and all injected vectors. No model/dictionary training or checkpoint mutation. [Result]({C}/summary_cn.md); [current strict access]({R}/evidence/output_access.json). Large full injection arrays stay execution-side with exactsize/hash; keyexamples/allsummarydata portable. Local sensitivity, matching failures and broad offdomain effects do not establish unique natural mechanisms or expert routing. Scientific acceptanceUnknown.\n')
# Final curated evidence is small and explicitly manifested.
for folder in ['figures','code','data','evidence']:
 (C/folder).mkdir(exist_ok=True)
 for p in (R/folder).glob('*'):
  if p.is_file() and (folder!='evidence' or p.suffix in ['.json','.md','.csv']):shutil.copy2(p,C/folder/p.name)
shutil.copy2(R/'large_files_index.json',C/'large_files_index.json')
dump(C/'payload_manifest.json',dict(UTC=now(),execution_root=str(R),files=[dict(path=str(p.relative_to(C)),bytes=p.stat().st_size,sha256=sha(p)) for folder in ['data','results','figures'] for p in (C/folder).glob('*') if p.is_file()],full_raw_conditions_in_execution_and_package=True))
# One speaking entry points to the combined brief; earlier daily note remains preserved.
index=SYS/'daily_research_reports/1104/README_cn.md';t=index.read_text();t=t.replace('[SAE组合与语义层级：问题、模型、结果、边界、决策及原始证据](meeting_report/sae_feature_hierarchy_cn.md)','[SAE组合与语义层级及干预：问题、模型、结果、边界、决策与原始证据](meeting_report/sae_feature_hierarchy_with_interventions_cn.md)').replace('20261104_SAE_hierarchy_analysis.zip','20261104_SAE_hierarchy_with_interventions.zip');index.write_text(t)
print('S07_RECORDS_FINISHED',aid,flush=True)
