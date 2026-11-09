from common import *
import shutil,fcntl,re,urllib.parse
import numpy as np
assert not (R/'evidence/completed.json').exists(),'No repeated finalization'
verification=json.load(open(R/'evidence/verification.json'));assert verification['status']=='PASS'
for p,h in json.load(open(R/'evidence/old_immutable_before.json')).items():assert sha(p)==h
plan=json.load(open(R/'frozen_plan.json'))
for p,h in plan['input_SHA256'].items():assert sha(p)==h
for ss in plan['sites'].values():assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
assert sha(OLD/'results/selection.json')==plan['selection_SHA256']
for tr in csv.DictReader(open(R/'results/actual_intersections.csv')):
 site=tr['site'];z=np.load(R/'cache/new.npz')[site+'__z'] if tr['context']=='new' else np.concatenate([np.load(OLD/f'cache/{sp}.npz')[site+'__z'] for sp in ['exploration','heldout_check']]);fi=int(tr['family'][1:])-1;ss=[set(np.flatnonzero(z[fi*4+j]>0)) for j in range(4)]
 assert int(tr['PCD_intersection'])==len(set.intersection(*ss[:3])) and int(tr['PCDN_intersection'])==len(set.intersection(*ss))
dump(R/'evidence/figure_review.json',dict(UTC=now(),figures=[p.name for p in sorted((R/'figures').glob('*.png'))],inspection='Four actual rendered figures inspected; full margins/titles/IDs/row labels and direction stars readable. Left-detail crop verifies MLPIN PNG row labels retained. No scientific/data changes.',sources=['cache/new.npz','original S03 cache/exploration.npz and heldout_check.npz','data/S03_frozen_selection.json','results/*/H2_old_new_pairs.csv'],units='raw z and weighted q on fixed lists; old/new cat-minus-dog differences',aggregation='one text row or one family/atom contrast; no inferential sample enlargement',boundary='Context-dependent response/sparsity; not incremental information or causality'))
aid='analysis_r17_d1_s04_neutral_suffix_fixed24_20261103'
dump(R/'evidence/completed.json',dict(UTC=now(),status='COMPLETED_S04_WAIT_FOR_JOINT_REVIEW',asset_id=aid,rows=24,body_changes=0,candidate_reselection=0,old_files_unchanged=verification['old_files_unchanged'],model_SAE_files_hash_reverified=True,training=0,probe=0,SVD=0,interventions=0,new_categories=0,extra_prompts=0,next_experiment=False,scientific_acceptance='Unknown',summary=str(C/'summary_cn.md')))
entry=dict(id=aid,title_cn='R17D1 S04：中性后缀24条原生行为与双SAE固定候选检查',category='analysis',kind='neutral_suffix_native_behavior_and_fixed_candidate_response',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=n,expected='file',required=True) for n in ['frozen_plan.json','data/panel.jsonl','data/S03_frozen_selection.json','cache/new.npz','results/behavior_raw.jsonl','results/all_H2_old_new_pairs.csv','results/H2_direction_counts.csv','evidence/completed.json','evidence/verification.json']])],identity=dict(parent_analysis='analysis_r17_d1_s03_animal_h1_h2_24_dual_sae_20261103',model_asset='model_qwen3_0p6b_base_official_a5',tokenizer_asset='tokenizer_qwen3_0p6b_base_official_a5',SAE_assets={k:ss['asset_id'] for k,ss in plan['sites'].items()},rows=24,families=6,suffix='\nDescription:',target_token_id=25,target_token_text=':',sampling='last visible suffix token without answers; independent native block27o_proj output and actual mlp-input hooks',encoding='original per-site ReLU Top32,30000 atoms; no extra input norm or decoder-bias subtraction',fields='NPZ ids; site__h,z,pre,topk_indices,decoder_norm,cutoff32,cutoff33,reconstruction_relative_L2. Candidate lists and old/new tables remain separate between dictionaries.',candidate_selection_SHA256=plan['selection_SHA256'],data_SHA256=plan['data_SHA256'],cache_SHA256=sha(R/'cache/new.npz'),behavior_SHA256=sha(R/'results/behavior_raw.jsonl'),model_updates=0,candidate_reselection=0,probe=0,intervention=0,scientific_acceptance='Unknown',next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW'),projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'protocol.md'),str(C/'summary_cn.md'),str(R/'code/run.py'),str(R/'code/analyze.py')],notes_cn=['S02/S03原件保持，24正文未改，后缀统一；不隔离某个词。','H2相对旧配对与原冻结探索方向分开；未激活不算比例方向复现。','原H1/H2额外信息及因果作用未验证；停止等待共同审阅。'])
with (S/'assets/.catalog_registration.lock').open('a') as lk:
 fcntl.flock(lk,fcntl.LOCK_EX);catalog=json.load(open(S/'assets/catalog.json'));assert not any(a['id']==aid for a in catalog['assets']);catalog['assets'].append(entry);tmp=S/'assets/catalog.s04.tmp';tmp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');tmp.replace(S/'assets/catalog.json')
# Requested data/scripts/raw outputs/figures: exact derived reading copies, execution retains ownership.
files=[]
for folder in ['data','cache','results','code','figures','evidence']:
 for p in sorted((R/folder).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.log']:continue
  rel=p.relative_to(R);dest=C/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);assert sha(p)==sha(dest)
  files.append(dict(path=str(rel),source=str(p),bytes=p.stat().st_size,sha256=sha(p),role='requested local generated reading copy; execution owns payload'))
for n in ['frozen_plan.json']:
 shutil.copy2(R/n,C/n);files.append(dict(path=n,source=str(R/n),bytes=(R/n).stat().st_size,sha256=sha(R/n)))
dump(C/'payload_manifest.json',dict(UTC=now(),execution_owner=str(R),asset_id=aid,exception='User requests24full prefixes, raw data, per-candidate tables, figures and Chinese conclusions in existing research line; exact small generated copies, no weights/checkpoints.',files=files))
checked=0;bad=[]
for p in C.rglob('*.md'):
 for link in re.findall(r'!?\[[^\]]*\]\(([^\n)]+)\)',p.read_text()):
  link=link.strip().strip('<>')
  if link.startswith(('http:','https:','mailto:','#')):continue
  target=p.parent/urllib.parse.unquote(link.split('#')[0]);checked+=1
  if not target.exists():bad.append(dict(file=str(p),link=link))
assert not bad,bad
dump(R/'evidence/delivery_checks.json',dict(UTC=now(),Markdown_links_checked=checked,broken_links=0,generated_payload_copies=len(files),all_source_hashes_match=True,old_files_unchanged=verification['old_files_unchanged'],actual_intersection_rows_replayed=24,figures_inspected=4,global_navigation='Inherited65issues before S04; no unrelated changes or claim of global clean',commit_push_publication='NOT_RUN'))
shutil.copy2(R/'evidence/delivery_checks.json',C/'evidence/delivery_checks.json')
with (C.parents[1]/'README.md').open('a') as f:f.write('''\n\n## 受控小例子：统一中性后缀与固定候选（S04）

用户授权在S03后只做下一小步：24正文/标签不变，四条件后缀统一为Description:，沿用两套原SAE和全部冻结候选，不筛选/训练/干预。新末尾冒号ID25，旧space-a ID264，完整语境变化不隔离单个词。原模型猫6/6、狗6/6、配对6/6切换；固定候选大量未再进入Top32，ATTN #14602猫狗全不激活，#3516仅F03/F05双侧激活且相对各自旧归一化方向反向；相对S03冻结探索方向另列。原H1/H2额外信息未验证。[中文小结](controlled_steps/S04_neutral_suffix_fixed_candidates_24/summary_cn.md) · [24条与原始分数](controlled_steps/S04_neutral_suffix_fixed_candidates_24/data_casebook_cn.md) · [指定两原子完整案例](controlled_steps/S04_neutral_suffix_fixed_candidates_24/focused_14602_3516_cn.md)。旧S02/S03原件保持；S04完成后停止，等待共同审阅；不做SVD或后续实验。
''')
print('S04_REGISTERED_PLACED',aid,len(files),checked,flush=True)
