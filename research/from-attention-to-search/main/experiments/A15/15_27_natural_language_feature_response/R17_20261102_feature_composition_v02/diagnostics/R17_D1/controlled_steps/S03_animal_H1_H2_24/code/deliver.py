"""Register actual outputs, copy requested small evidence, and append the bounded mainline record."""
from common import *
import shutil, fcntl
assert not (R/'evidence/completed.json').exists(),'No repeated finalization'
ver=json.load(open(R/'evidence/verification.json'));assert ver['status']=='PASS'
freeze=json.load(open(R/'evidence/candidates_frozen_before_heldout.json'))
for n,d in freeze['code_SHA256'].items():assert sha(R/'code'/n)==d
for p,d in json.load(open(R/'evidence/old_steps_immutable_before.json')).items():assert sha(p)==d
for p,d in json.load(open(R/'frozen_plan.json'))['input_SHA256'].items():assert sha(p)==d
for ss in json.load(open(R/'frozen_plan.json'))['sites'].values():assert sha(ss['path'])==ss['sha256']
assetid='analysis_r17_d1_s03_animal_h1_h2_24_dual_sae_20261103'
dump(R/'evidence/completed.json',dict(UTC=now(),status='COMPLETED_S03_WAIT_FOR_JOINT_REVIEW',rows=24,families=6,exploration_families=3,heldout_families=3,SAEs=2,model_frozen=True,SAEs_frozen=True,old_steps_immutable_files=ver['old_files_unchanged'],old_model_SAE_hashes_reverified=True,feature_sites=2,CC=False,probe=0,interventions=0,training=0,H3_H4=False,new_data_beyond24=False,next_experiment=False,scientific_acceptance='Unknown',asset_id=assetid,summary_path=str(C/'summary_cn.md')))
plan=json.load(open(R/'frozen_plan.json'))
entry=dict(id=assetid,title_cn='R17D1受控S03：动物猫狗24条双SAE H1/H2描述性探索',category='analysis',kind='frozen_dual_sae_membership_and_relative_response',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=n,expected='file',required=True) for n in ['data/panel.jsonl','frozen_plan.json','cache/exploration.npz','cache/heldout_check.npz','results/selection.json','results/summary.json','results/pattern_coverage.csv','evidence/candidates_frozen_before_heldout.json','evidence/completed.json','evidence/verification.json']])],identity=dict(rows=24,families=6,conditions=CONDS,model_asset='model_qwen3_0p6b_base_official_a5',tokenizer_asset='tokenizer_qwen3_0p6b_base_official_a5',SAE_assets={k:x['asset_id'] for k,x in plan['sites'].items()},parent_data='data_analysis_r17_d1_s02_animal_cat_dog12_20261103',sampling='last visible prefix token space-a, ID264; same functional position in both native hooks',split=plan['split'],plan_SHA256=sha(R/'frozen_plan.json'),selection_SHA256=sha(R/'results/selection.json'),cache_SHA256={n:sha(R/'cache'/n) for n in ['exploration.npz','heldout_check.npz']},fields='NPZ ids, site__h, site__z, site__pre, site__decoder_norm, cutoff32/33, reconstruction_relative_L2. z final native Top32; pre complete linear encoder output. IDs not aligned between dictionaries.',trainable_parameters=0,probe=0,intervention=0,old_S01_S02_unchanged=True,scientific_acceptance='Unknown',next_step='NOT_RUN_WAIT_FOR_JOINT_REVIEW'),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'protocol.md'),str(C/'summary_cn.md'),str(R/'code/extract.py'),str(R/'code/analyze.py')],notes_cn=['只作六家族描述，未验证H1/H2的额外信息或模型作用。','N后缀animal/object变化与P指代词差异明确保留为竞争解释。','新结果独立S03目录，不覆盖S01/S02或原R17。'])
with (S/'assets/.catalog_registration.lock').open('a') as lk:
 fcntl.flock(lk,fcntl.LOCK_EX);catalog=json.load(open(S/'assets/catalog.json'));assert not any(a['id']==assetid for a in catalog['assets']);catalog['assets'].append(entry)
 tmp=S/'assets/catalog.s03.tmp';tmp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');tmp.replace(S/'assets/catalog.json')
# The user explicitly requested scripts, data, raw scores and figures in the new project subdirectory.
# These generated evidence copies are byte-identical and keep execution ownership.
copied=[]
for folder in ['data','code','cache','results','evidence','figures']:
 for p in sorted((R/folder).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.log']:continue
  rel=p.relative_to(R);dest=C/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);assert sha(p)==sha(dest)
  copied.append(dict(path=str(rel),source=str(p),sha256=sha(p),bytes=p.stat().st_size,role='user-requested generated evidence reading copy; execution owns source'))
shutil.copy2(R/'frozen_plan.json',C/'frozen_plan.json');copied.append(dict(path='frozen_plan.json',source=str(R/'frozen_plan.json'),sha256=sha(R/'frozen_plan.json'),bytes=(R/'frozen_plan.json').stat().st_size))
dump(C/'payload_manifest.json',dict(UTC=now(),execution_owner=str(R),asset_id=assetid,exception='Current user explicitly requests data/scripts/figures/raw outputs in this new experiment child; byte-identical local reading copies, no model/SAE weights.',files=copied))
main=C.parents[1]/'README.md';assert main.name=='README.md' and main.parent.name=='R17_D1'
with main.open('a') as f:f.write('''\n\n## 受控小例子：动物猫狗的H1／H2描述（S03）

用户在S02原生续写12/12后授权本步：原12条猫狗保持，加入P（animal、细类未知）与N（chair）共24条；F01–03探索、F04–06只检查固定候选。两套原生冻结SAE分别读取末尾` a`，候选先冻结再开放检查。观察到共同成员及换入换出、固定列表内比例变化，也保留未复现候选。两接口H2选定6成员支持相同均6/6对，全字典支持相同均0/6对；原H1/H2额外信息与功能未验证，N后缀与指代词差异仍是竞争解释。[中文小结](controlled_steps/S03_animal_H1_H2_24/summary_cn.md) · [24条全文](controlled_steps/S03_animal_H1_H2_24/data_casebook_cn.md) · [完整值与失败](controlled_steps/S03_animal_H1_H2_24/README.md)。S01/S02全部保留，不改假设；仅本步完成，等待共同审阅，不自动继续。
''')
print('REGISTERED_AND_PLACED',assetid,len(copied))
