from common import *
import fcntl,re
ids=['dataset_r19_matched_remote_target_near_competitor_20261104','representation_r19_native_dual_sae_composition_20261104','analysis_r19_remote_target_near_competitor_20261104']
names=['R19远目标与近处词匹配文本矩阵','R19两原生SAE目标位置稀疏激活','R19远目标近处竞争组合与行为分析']
probes=[['config.json','data/panel_portable.jsonl','data/text_pairing.csv','evidence/construction.json'],['cache/discovery.npz','cache/heldout.npz','results/behavior_heldout.jsonl','data/candidates.json','evidence/verification.json'],['tables/family_geometry.csv','tables/membership_summary.csv','results/primary_hypotheses.json','results/joint_hypotheses.json','evidence/verification.json']]
cat=SYS/'assets/catalog.json'
with cat.open('r+') as f:
 fcntl.flock(f,fcntl.LOCK_EX);j=json.load(f)
 for k,aid in enumerate(ids):
  if any(x['id']==aid for x in j['assets']):continue
  identity=dict(model='model_qwen3_0p6b_base_official_a5',tokenizer='tokenizer_qwen3_0p6b_base_official_a5',parent_R18_dataset='dataset_r18_near_far_object_fact_pairs_20261104',families=24,discovery_families=12,representation_heldout_families=12,smoke_prefixes=4,formal_prefixes=288,total_prefixes=292,matched_supplements=96,prefix_tokens=320,target_position=319,gap='p-e-1; both endpoints excluded',training=False,activation_interventions=False,scientific_acceptance='Unknown')
  if k==0:identity['panel_sha256']=sha(R/'data/panel_portable.jsonl')
  else:identity.update(SAE_assets=[json.load(open(R/'config.json'))['sites'][site]['asset_id'] for site in SITES],dictionaries_separate=True,post_topk=32,native_features=30000,selection_sha256=sha(R/'data/candidates.json'),parent_dataset=ids[0])
  j['assets'].append(dict(id=aid,title_cn=names[k],category=['dataset','representation','analysis'][k],kind=['constructed_english_role_matched_factorial_panel','native_dual_sae_answer_prefix_top32','family_paired_membership_strength_joint_and_behavior'][k],payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(R),expected='directory',required=True,probes=[dict(path=p,expected='file',required=True) for p in probes[k]])],identity=identity,projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',source_paths=[str(C/'summary.md'),str(C/'protocol.md'),str(R/'config.json')]))
 j['catalog_amendments'].append(dict(UTC=now(),action='Register actually saved bounded R19 matched texts, native SAE sparse observations and analysis; no checkpoint training or scientific acceptance',asset_ids=ids));f.seek(0);f.write(json.dumps(j,ensure_ascii=False,indent=2)+'\n');f.truncate();fcntl.flock(f,fcntl.LOCK_UN)
for filename in ['README.md','README_cn.md']:
 f=SYS/'assets'/filename;s=f.read_text();s=re.sub(r'\*\*\d+ entries and 10 project/storage roots\*\*',f'**{len(j["assets"])} entries and 10 project/storage roots**',s)
 line='\n[R19 remote-target/near-word composition]('+str(C/'summary.md')+'):292prefixes, two separately encoded native SAEs, discovery12/heldout12families, matched factorial, membership/strength and marginal-controlled joint evidence; no training or intervention.\n'
 if 'R19 remote-target/near-word composition' not in s:s+=line
 f.write_text(s)
dump(R/'evidence/output_asset_ids.json',dict(UTC=now(),ids=ids,actual_saved=True,scientific_acceptance='Unknown'))
print('REGISTERED',ids)
