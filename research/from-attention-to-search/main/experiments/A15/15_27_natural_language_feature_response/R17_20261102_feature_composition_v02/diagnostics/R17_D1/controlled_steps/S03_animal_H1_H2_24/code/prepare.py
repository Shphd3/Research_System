from common import *
from tokenizers import Tokenizer
import shutil
assert not (R/'frozen_plan.json').exists(), 'No overwrite'
for d in ['data','evidence','cache','results','figures']: (R/d).mkdir(exist_ok=True)
shutil.move(R/'input_access.json', R/'evidence/input_access.json')
assert not json.load(open(R/'evidence/input_access.json'))['selected_required_failures']
cat=json.load(open(S/'assets/catalog.json'))['assets']
assetids={'ATTN_SAE':'sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z','MLPIN_SAE':'sae_qwen3_0p6b_e16_layer27_final_1b'}
saes={k:next(a for a in cat if a['id']==v) for k,v in assetids.items()}
model=json.load(open(OLD/'frozen_plan.json'))['model']
T=Tokenizer.from_file(str(Path(model)/'tokenizer.json'))
original=rows(OLD/'data/panel.jsonl'); source={(x['family'],x['fine_label']):x for x in original}
pb=['This object is an animal.','In this story, the object is an animal.','We are describing an object. It is an animal.','The note identifies this object as an animal.','An animal is the object described in this example.','The report calls the object an animal.']
nb=['This object is a chair.','In this story, the object is a chair.','We are describing an object. It is a chair.','The note identifies this object as a chair.','A chair is the object described in this example.','The report calls the object a chair.']
panel=[];diff=[]
for fi in range(1,7):
 family=f'F{fi:02d}';split='exploration' if fi<=3 else 'heldout_check'
 for cond in CONDS:
  old=source.get((family,cond));text=old['text'] if old else (pb if cond=='P' else nb)[fi-1]
  suffix='\nThe object is a' if cond=='N' else '\nThe animal is a'
  prefix=text+suffix
  if old: assert prefix==old['prefix']
  enc=T.encode(prefix,add_special_tokens=False); ids=enc.ids; pos=len(ids)-1
  labels=['animal'] if cond=='P' else ['animal',cond] if old else ['non_animal','chair']
  rec=dict(id=f'S03_{family}_{cond}',family=family,split=split,condition=cond,text=text,suffix=suffix,prefix=prefix,labels=labels,animal=True if cond!='N' else False,cat=True if cond=='cat' else False if cond in ['dog','N'] else None,dog=True if cond=='dog' else False if cond in ['cat','N'] else None,fine_status='UNSPECIFIED_NOT_NEGATIVE' if cond=='P' else cond if old else 'chair',source_S02_id=old['id'] if old else None,token_ids=ids,token_pieces=enc.tokens,token_offsets=enc.offsets,target_index_zero_based=pos,target_index_one_based=pos+1,target_token_id=ids[pos],target_token_piece=T.id_to_token(ids[pos]),target_token_text=T.decode([ids[pos]]),sampling='last visible prefix token before predicting next token; no continuation included')
  assert rec['target_token_text']==' a' and len(ids)<192
  if cond=='P': assert 'cat' not in text.lower() and 'dog' not in text.lower()
  if cond=='N': assert 'animal' not in prefix.lower() and 'chair' in text
  panel.append(rec)
 diff.append(dict(family=family,old_cat_dog_changed=False,P_vs_old='Replace animal referent with object, cat/dog with animal, and a/A with an/An; suffix unchanged.',N_vs_old='Replace animal referent with object, cat/dog with chair; suffix animal -> object for semantic consistency.',P_vs_N='class word animal/chair and a/an; suffix animal/object. These are lexical/format confounds.'))
jsonl(R/'data/panel.jsonl',panel);jsonl(R/'data/text_differences.jsonl',diff)
shutil.copy2(OLD/'data/panel.jsonl',R/'data/S02_original_panel.jsonl')
shutil.copy2(OLD/'results/raw_scores.jsonl',R/'data/S02_original_behavior_scores.jsonl')
protected={str(p):sha(p) for root in [OLD,OLD.parent/'S01_explicit_singularity_36',C.parent/'S01_explicit_singularity_36',C.parent/'S02_animal_cat_dog_12'] for p in root.rglob('*') if p.is_file()}
dump(R/'evidence/old_steps_immutable_before.json',protected)
inputs={str(Path(model)/n):sha(Path(model)/n) for n in ['config.json','tokenizer.json','model.safetensors']}
assert inputs==json.load(open(OLD/'evidence/completed.json'))['input_SHA256']
sites={}
for k,a in saes.items():
 loc=next(l['path'] for l in a['locations'] if l['path'].endswith('sae_full_final.pt'))
 core='/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/source/e16_sae_core.py' if k=='ATTN_SAE' else a['identity']['loader_path']
 sites[k]=dict(asset_id=a['id'],path=loc,sha256=sha(loc),loader=core,loader_sha256=sha(core),k=32,n_latents=30000,encoding='native encoder(x), ReLU, Top32; active iff selected z>0; no input normalization, no decoder bias subtraction',hook='block27.self_attn.o_proj output before residual addition' if k=='ATTN_SAE' else 'block27.mlp forward_pre_hook actual input after residual addition and post_attention_layernorm')
selection=dict(H1_common=dict(min_triple_active_families=2,min_triple_min_weighted_gt_N_families=2,max_candidates=6,ranking='descending triple_active count, descending positive contrast count, descending mean(min(u_P,u_cat,u_dog)-u_N), ascending atomID'),H1_added=dict(min_zeroP_positiveFine_families=2,max_candidates_per_fine=6,ranking='descending zeroP-positiveFine coverage, descending mean fine u among zeroP-positiveFine rows, ascending atomID; cat and dog selected separately; opposite fine response reported, not a selection gate'),H2=dict(min_joint_cat_dog_active_families=2,max_candidates=6,ranking='descending joint cat/dog active coverage, descending mean min(u_cat,u_dog), ascending atomID; no fine difference ranking',direction='sign(mean exploration(q_cat-q_dog)); abs(mean)<=1e-8 is zero; q uses same fixed list and own L2 norm',normalizations=['q_raw=z_C/||z_C||2','q_weighted=u_C/||u_C||2'],zero_norm='undefined, serialize null and plot gray; no epsilon replacement',support_subsets=['entire SAE positive support exactly equal','selected H2-list positive support exactly equal; not equivalent to full support control']))
plan=dict(experiment='S03_animal_H1_H2_24',UTC=now(),authorization='Current direct user request authorizes this bounded 24-row frozen two-SAE descriptive analysis and <10MB daily discussion package. Stop for joint review.',model=model,input_SHA256=inputs,sites=sites,split={'exploration':['F01','F02','F03'],'heldout_check':['F04','F05','F06']},conditions=CONDS,rows=24,selection=selection,precision='FP32 CPU model and native SAE; FP64 analysis; saved BF16 LM weights promoted to FP32',physical_shape=[4,192],resource='existing CPU, 2 threads; no GPU job; 24 new prefixes, no new behavior scores',selection_gate='extract exploration only; select/freeze exact candidates+directions+code hashes; only then extract heldout_check',data_SHA256={p.name:sha(p) for p in (R/'data').iterdir()},scope_exclusions=['H3','H4','CrossCoder','training','probe','ablation','new prompt/data search','hypothesis rewrite','automatic next step'])
dump(R/'frozen_plan.json',plan)
dump(R/'evidence/data_audit.json',dict(UTC=now(),rows=24,families=6,conditions_per_family=4,old_cat_dog_rows_identical=12,old_behavior_score_rows_copied=13,P_cat_dog_labels_are_unknown=True,all_prefixes_end_same_token=True,text_differences=diff,model_ID_matches_S02=True))
print('DATA_AND_RULES_FROZEN',sha(R/'frozen_plan.json'),flush=True)
