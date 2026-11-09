from common import *
import shutil,fcntl,re,urllib.parse
assert not (R/'evidence/completed.json').exists(),'No overwrite'
v=json.load(open(R/'evidence/verification.json'));assert v['status']=='PASS'
for p,h in json.load(open(R/'evidence/old_immutable_before.json')).items():assert sha(p)==h
freeze=json.load(open(R/'evidence/bases_frozen_before_check.json'))
for p,h in freeze['matrix_SHA256'].items():assert sha(R/p)==h
assert sha(R/'results/top_loading_members.csv')==freeze['top_loading_SHA256']
dump(R/'evidence/visual_review.json',dict(UTC=now(),figures=6,review='All six rendered figures inspected at full scale and/or contact sheet. Raw projection labels repaired for close check points, without changing any data or direction; original PNGs retained execution-side in versions/figures_before_label_repair. Main labels,split/legend,limits and decomposition units readable.',source_data_unchanged=True,bases_and_atoms_unchanged=True,projection_scaling='Each basis uses display limits covering all24rows; limits do not refit basis. AC/AD panels have distinct means/axes.',meaning='Overall centered sample axes and signed paired differences are different; plots do not establish general semantic laws.'))
aid='analysis_r17_d1_s05_ac_ad_svd_geometry24_20261103'
dump(R/'evidence/completed.json',dict(UTC=now(),status='COMPLETED_S05_WAIT_FOR_JOINT_REVIEW',asset_id=aid,source='completed S04 neutral suffix',full_matrix_fits=8,paired_bootstrap_fits=216,exploration_families=3,check_families=3,model_forwards=0,SAE_updates=0,probe=0,training=0,interventions=0,new_texts=0,cross_dictionary_ID_alignment=False,decoder_space_mapping='NOT_RUN_OPTIONAL',old_S03_S04_files_unchanged=v['old_files_unchanged'],scientific_acceptance='Unknown',next_experiment=False,summary=str(C/'summary_cn.md')))
entry=dict(id=aid,title_cn='R17D1 S05：AC/AD总体SVD与父类到细类配对几何',category='analysis',kind='cache_only_svd_and_paired_activation_geometry',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=n,expected='file',required=True) for n in ['data/panel.jsonl','data/S04_frozen_activations.npz','frozen_plan.json','results/matrix_manifest.jsonl','cache/ATTN_SAE/raw_z/AC.npz','cache/ATTN_SAE/raw_z/AD.npz','cache/MLPIN_SAE/raw_z/AC.npz','cache/MLPIN_SAE/raw_z/AD.npz','results/paired_differences_summary.csv','results/top_loading_members.csv','evidence/completed.json','evidence/verification.json']])],identity=dict(parent_asset='analysis_r17_d1_s04_neutral_suffix_fixed24_20261103',frozen_H2_parent='analysis_r17_d1_s03_animal_h1_h2_24_dual_sae_20261103',data_SHA256=json.load(open(R/'frozen_plan.json'))['data_SHA256'],model='same frozen official Qwen3-0.6BBase as S04; no weight loading or forward in S05',sites=['native block27attention o_proj output before residual addition','native block27actual MLP input after residual add and post_attention_layernorm'],suffix='\nDescription:',target_token_id=25,base_fits=8,bootstrap_fits=216,per_matrix_shape=[6,30000],split='F01-03 exploration only for means,bases,top5;F04-06 projection only',scales=['raw_z primary','z times own decoder norm supplemental'],SVD_fields='X,centered,mean,singular_values,components,row_ids,row_indices,rank,rank_tol,near_zero_tol; null components not interpreted',paired_fields='delta_cat/dog [6,30000],components_cat/dog [6,3,30000],exploration/check means; retained/new/lost disjoint per family',dictionary_ID_alignment=False,causal_test=False,scientific_acceptance='Unknown',next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW'),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'protocol.md'),str(C/'summary_cn.md'),str(R/'code/fit.py'),str(R/'code/analyze.py')],notes_cn=['仅探索性几何，不认定语义相同或功能不同。','各组独立中心化总体轴，与有向fine-P差分开。','27有序探索家族bootstrap只有10种无序多重集，非置信区间。','全部旧结果保持，完成后停止。'])
with (S/'assets/.catalog_registration.lock').open('a') as lk:
 fcntl.flock(lk,fcntl.LOCK_EX);catalog=json.load(open(S/'assets/catalog.json'));assert not any(x['id']==aid for x in catalog['assets']);catalog['assets'].append(entry);tmp=S/'assets/catalog.s05.tmp';tmp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');tmp.replace(S/'assets/catalog.json')
files=[]
for folder in ['data','cache','results','code','figures','evidence']:
 for p in sorted((R/folder).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.log']:continue
  rel=p.relative_to(R);dest=C/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);assert sha(p)==sha(dest);files.append(dict(path=str(rel),source=str(p),bytes=p.stat().st_size,sha256=sha(p),role='user-requested generated reading copy; execution owns payload'))
shutil.copy2(R/'frozen_plan.json',C/'frozen_plan.json');files.append(dict(path='frozen_plan.json',source=str(R/'frozen_plan.json'),bytes=(R/'frozen_plan.json').stat().st_size,sha256=sha(R/'frozen_plan.json')))
dump(C/'payload_manifest.json',dict(UTC=now(),execution_owner=str(R),asset_id=aid,exception='Current user explicitly requests scripts,raw data,matrices,means and figures in new mainline child. Exact local reading copies; no model/SAE weights.',files=files))
bad=[];checked=0
for p in C.rglob('*.md'):
 for raw in re.findall(r'!?\[[^\]]*\]\(([^\n)]+)\)',p.read_text()):
  link=raw.strip().strip('<>')
  if link.startswith(('http:','https:','mailto:','#')):continue
  target=p.parent/urllib.parse.unquote(link.split('#')[0]);checked+=1
  if not target.exists():bad.append(dict(file=str(p),link=raw))
assert not bad,bad
dump(R/'evidence/delivery_checks.json',dict(UTC=now(),Markdown_links_checked=checked,broken_links=0,byte_exact_generated_copies=len(files),old_files_unchanged=v['old_files_unchanged'],figures_inspected=6,scientific_state_change=False,commit_push_publication='NOT_RUN'))
shutil.copy2(R/'evidence/delivery_checks.json',C/'evidence/delivery_checks.json')
with (C.parents[1]/'README.md').open('a') as f:f.write('''\n\n## 受控小例子：AC/AD总体方向与父类细类配对几何（S05）

用户授权在已完成S04中性后缀缓存上做本小步，无新模型前向。AC/AD各6×30000探索矩阵独立中心化；只用F01–03拟合均值、前1/2方向与前5系数成员，F04–06仅投影。两字典独立，原始及decoder范数加权尺度均报告。原始PC1绝对余弦Attention0.866、MLPIN0.963，前二维重叠0.726/0.931；探索均值猫−P/狗−P有向余弦0.754/0.773。第一轴大部分投影平方和来自家族中点间变化，不能当作父子差方向；F05沿自身AC第一轴的猫−P分量两接口均反号。成员强弱/支持更替、27成组bootstrap、完整谱/文本/成员值与失败均保留。[中文小结](controlled_steps/S05_AC_AD_svd_paired_geometry_24/summary_cn.md) · [Detailed与反例](controlled_steps/S05_AC_AD_svd_paired_geometry_24/detailed_cn.md) · [完整输入](controlled_steps/S05_AC_AD_svd_paired_geometry_24/data_casebook_cn.md)。仅候选几何现象，原H1/H2不改，未作语义/功能/因果确认。旧S03/S04保持，S05完成后停止等待审阅。
''')
print('S05_REGISTERED_AND_PLACED',aid,len(files),checked,flush=True)
