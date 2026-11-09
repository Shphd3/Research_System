from common import *
from tokenizers import Tokenizer
import shutil
import numpy as np
assert not (R/'frozen_plan.json').exists()
for name in ['data','cache','results','figures','evidence']: (R/name).mkdir(exist_ok=True)
prior=json.load(open(OLD/'frozen_plan.json'));selection=json.load(open(OLD/'results/selection.json'));M=Path(prior['model']);T=Tokenizer.from_file(str(M/'tokenizer.json'))
assert not json.load(open(R/'evidence/input_access.json'))['selected_required_failures']
suffix='\nDescription:';assert not any(w in suffix.lower() for w in ['animal','cat','dog','chair'])
panel=[];cs=[('cat',' cat.'),('dog',' dog.')];audit=[]
for o in rows(OLD/'data/panel.jsonl'):
 prefix=o['text']+suffix;enc=T.encode(prefix,add_special_tokens=False);pre=enc.ids;cands=[]
 for label,text in cs:
  full=T.encode(prefix+text,add_special_tokens=False).ids;assert full[:len(pre)]==pre
  ids=full[len(pre):];assert ids and len(full)<192
  cands.append(dict(label=label,text=text,token_ids=ids,token_pieces=[T.id_to_token(i) for i in ids],token_count=len(ids),full_input_token_ids=full))
 p={**o,'id':o['id'].replace('S03_','S04_'),'source_id':o['id'],'suffix':suffix,'prefix':prefix,'token_ids':pre,'token_pieces':enc.tokens,'token_offsets':enc.offsets,'target_index_zero_based':len(pre)-1,'target_index_one_based':len(pre),'target_token_id':pre[-1],'target_token_piece':T.id_to_token(pre[-1]),'target_token_text':T.decode([pre[-1]]),'old_suffix':o['suffix'],'old_prefix':o['prefix'],'old_token_ids':o['token_ids'],'old_target_index_zero_based':o['target_index_zero_based'],'old_target_token_id':o['target_token_id'],'old_target_token_text':o['target_token_text'],'candidates':cands,'behavior_gold':o['condition'] if o['condition'] in ['cat','dog'] else None,'sampling':'final token of Description: before any candidate; no generated continuation'}
 assert p['text']==o['text'] and p['labels']==o['labels'];panel.append(p)
 audit.append(dict(id=p['id'],source_id=o['id'],body_unchanged=True,body_is_complete_grammatical_sentence=True,neutral_label_prompt='Description: invites a description of any object, including animal or chair; not a yes/no question',suffix_identical=True,label_unchanged=True,old_index=o['target_index_zero_based'],new_index=p['target_index_zero_based']))
assert len(panel)==24 and len(set(p['suffix'] for p in panel))==1
assert len({tuple(c['token_ids']) for p in panel for c in p['candidates'] if c['label']=='cat'})==1
assert len({tuple(c['token_ids']) for p in panel for c in p['candidates'] if c['label']=='dog'})==1
jsonl(R/'data/panel.jsonl',panel)
shutil.copy2(OLD/'results/selection.json',R/'data/S03_frozen_selection.json')
shutil.copy2(OLD2/'results/raw_scores.jsonl',R/'data/S02_original_behavior_scores.jsonl')
shutil.copy2(OLD/'data/panel.jsonl',R/'data/S03_original_panel.jsonl')
protected={str(p):sha(p) for root in [OLD,OLD2,C.parent/OLD.name,C.parent/OLD2.name] for p in root.rglob('*') if p.is_file()}
dump(R/'evidence/old_immutable_before.json',protected)
for path,digest in prior['input_SHA256'].items():assert sha(path)==digest
for ss in prior['sites'].values():assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
refs={}
for site in SITES:
 old=np.load(OLD/'cache/exploration.npz');ids=selection['sites'][site]['H2'];z=old[site+'__z'].reshape(3,4,-1).astype(float)
 refs[site]={str(i):float((z[:,1,i]-z[:,2,i]).mean()) for i in ids}
plan=dict(experiment=R.name,UTC=now(),authorization='Direct current user request: one bounded suffix+native behavior check, same24 bodies and exact S03 candidates. Stop afterwards.',model=prior['model'],input_SHA256=prior['input_SHA256'],sites=prior['sites'],suffix=suffix,candidates=[dict(label=l,text=t,token_ids=panel[0]['candidates'][j]['token_ids'],token_count=panel[0]['candidates'][j]['token_count']) for j,(l,t) in enumerate(cs)],split=prior['split'],candidate_selection='NONE: reuse exact ordered S03 lists and discovery directions; no threshold/ranking changes',selection_SHA256=sha(R/'data/S03_frozen_selection.json'),old_raw_discovery_mean_difference=refs,old_cache_SHA256={sp:sha(OLD/f'cache/{sp}.npz') for sp in ['exploration','heldout_check']},data_SHA256={p.name:sha(p) for p in (R/'data').iterdir()},behavior='sum conditional logprob of all candidate tokens, including leading-space class token and final period; no length/neutral-prior correction. P/N no correct label.',score_delta='S_cat - S_dog; max sum wins; exact tie uses cat first, recorded',normalization='Per each exact frozen named list H1_common, H1_added_cat, H1_added_dog, H2: q_z=z/||z||2; q_u=u/||u||2. Zero norm undefined/null, no epsilon. Lists and denominator do not change when members become inactive.',H2_reference='Report both new vs same-family old direction and new vs frozen S03 discovery direction; raw metric uses old-only exploration mean fixed here, normalized weighted metric uses original S03 frozen direction.',H2_count_rule='For each site/atom/metric/reference/split, denominator3families. Exclusive priority: zero_norm (normalized metric only), member_inactive (either cat or dog not active under new suffix, also old for old-pair reference), no_reference (old difference zero/undefined), same/opposite/zero_difference. Report inactive/zero_norm marginal flags separately; raw and q differences still shown even if inactive.',direction_epsilon=1e-8,precision='CPU FP32 model/SAE and logsoftmax; FP64 score sum and offline analysis',physical_shape=[4,192],stop='24 prefix captures and24 two-candidate comparisons, then report; no extra prompts/data, feature selection, SVD, H3/H4, fitting, training or intervention')
dump(R/'frozen_plan.json',plan);dump(R/'evidence/data_audit.json',dict(UTC=now(),checks=audit,rows=24,same_families=True,bodies_changed=0,targets=[dict(id=p['id'],token=p['target_token_text'],token_id=p['target_token_id'],index=p['target_index_zero_based']) for p in panel],candidates=plan['candidates'],P_N_body_differences='P states animal, N states chair, with an/An vs a/A. Both use object referent; those body differences remain. P is not a cat/dog negative. Cat/dog bodies still use animal referent.',model_and_SAE_hashes_match_S03=True,selection_unchanged=True))
print('S04_FROZEN',sha(R/'frozen_plan.json'),plan['candidates'],[(p['id'],p['target_token_text'],p['target_token_id'],p['target_index_zero_based']) for p in panel],flush=True)
