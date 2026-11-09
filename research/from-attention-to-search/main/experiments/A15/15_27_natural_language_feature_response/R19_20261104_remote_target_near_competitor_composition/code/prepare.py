from common import *
import copy,re,shutil
import numpy as np,pandas as pd
from scipy import sparse
from tokenizers import Tokenizer
assert not (R/'data/panel.jsonl').exists()
for d in ['data','cache','results','tables','figures','evidence','versions','inputs']: (R/d).mkdir(exist_ok=True)
C.mkdir(parents=True,exist_ok=True)
oldC=P/'main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior'
protected={str(f):sha(f) for root in [OLD,oldC] for f in root.rglob('*') if f.is_file()}
for f in [P/'main/focus/focus_near_far_object_fact_use.md',P/'main/focus/focus_near_far_object_fact_use_cn.md',P/'main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_10_near_far_fact_use_anchor.md',P/'main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_10_near_far_fact_use_anchor_cn.md']:protected[str(f)]=sha(f)
dump(R/'evidence/R18_protected_snapshot.json',dict(UTC=now(),files=protected))
t=Tokenizer.from_file(str(MODEL/'tokenizer.json'))
def enc(s):return t.encode(s,add_special_tokens=False)
old={x['id']:x for x in rows(OLD/'data/panel.jsonl')}
oscores={x['id']:x for name in ['smoke','heldout'] for x in rows(OLD/f'results/{name}.jsonl')}
families=[f for f in json.load(open(OLD/'data/families.json')) if f['split']=='heldout']
for i,f in enumerate(families):f['R19_split']='discovery' if i%4<2 else 'heldout'
dump(R/'data/families.json',families)
panel=[];legacy=[];baseline=[]
def make(source,key,cond,split,text=None,target=None,near=None):
 z=copy.deepcopy(source);z.update(id=key,condition=cond,split=split,R18_source_id=source['id'] if text is None or text==source['text'] else None,frame='legacy_main' if cond.startswith('main') else 'matched_far',near_label=near,mode=cond)
 if text is not None:z['text']=text
 e=enc(z['text']);z['token_ids']=e.ids;z['offsets']=e.offsets;assert len(e.ids)==320
 target=target or z['evidence_item'];z['evidence_item']=target
 # The far fact is before the near clause. Locate the item inside its original factual span.
 start=z['evidence_char_span'][0];end=start+len(target);assert z['text'][start:end]==target
 ev=[j for j,(a,b) in enumerate(e.offsets) if a<end and b>start];z['evidence_char_span']=[start,end];z['evidence_token_positions']=ev;z['evidence_token_ids']=[e.ids[j] for j in ev];z['evidence_last_position']=ev[-1];z['target_position']=319;z['target_token_id']=e.ids[319];z['target_token']=t.decode([e.ids[319]]);z['actual_distance']=319-ev[-1]-1
 for c in z['candidates']:
  full=enc(z['text']+c['text']).ids;assert full[:320]==e.ids and full[320:]==c['token_ids'];c['full_ids']=full
 if near is not None:
  mark='The other container holds the ';ns=z['text'].index(mark)+len(mark);ne=z['text'].index('.\n',ns);nn=[j for j,(a,b) in enumerate(e.offsets) if a<ne and b>ns];z.update(near_item=z['text'][ns:ne],near_char_span=[ns,ne],near_token_positions=nn,near_token_ids=[e.ids[j] for j in nn],near_actual_gap=319-nn[-1]-1)
 else:z.update(near_item=None,near_token_positions=[],near_token_ids=[],near_actual_gap=None)
 panel.append(z);return z
for f in families:
 fam=f['family'];split=f['R19_split']
 for d in [16,64,128]:
  for g in 'AB':make(old[f'{fam}_main_{d}_{g}'],f'{fam}_main{d}_{g}',f'main{d}',split)
  bs=old[f'{fam}_baseline_{d}_N'];baseline.append(dict(id=bs['id'],family=fam,split=split,distance=d,text=bs['text'],token_ids=bs['token_ids'],scores=oscores[bs['id']]))
 base=old[f'{fam}_lure_128_A'];text=base['text'];tl,tr=base['evidence_char_span'];mark='The other container holds the ';nl=text.index(mark)+len(mark);nr=text.index('.\n',nl);assert text[tl:tr]==f['A'] and text[nl:nr]==f['B']
 for near in ['N','A','B']:
  for g in 'AB':
   item=f[g];nearitem=('small object' if len(base['candidates'][0]['token_ids'])==3 else 'object') if near=='N' else f[near]
   actual=text[:tl]+item+text[tr:nl]+nearitem+text[nr:]
   z=make(base,f'{fam}_near{near}_{g}','near'+near,split,text=actual,target=item,near=near);z['gold']=g;z['actual_distance']=319-z['evidence_last_position']-1;assert z['actual_distance']==128
   oldid=f'{fam}_lure_128_{g}'
   if actual==old[oldid]['text']:z['R18_source_id']=oldid
   z['planned_distance']=128;z['opposite_near']=near in 'AB' and near!=g;z['congruent_near']=near==g
 for g in 'AB':
  a=old[f'{fam}_main_128_{g}'];b=old[f'{fam}_lure_128_{g}']
  legacy.append(dict(family=fam,gold=g,main_id=a['id'],lure_id=b['id'],same_target_fact=a['evidence_item']==b['evidence_item'],same_target_position=True,same_actual_gap=a['actual_distance']==b['actual_distance'],same_token_multiset=sorted(a['token_ids'])==sorted(b['token_ids']),same_filler_inventory=a['filler_inventory']==b['filler_inventory'],same_full_local_suffix=a['local_suffix']==b['local_suffix'],question_same=a['local_suffix']==b['local_suffix'].split('\n',1)[-1],near_item=f['B' if g=='A' else 'A'],main_scores=oscores[a['id']],lure_scores=oscores[b['id']],direct_single_factor_pair=False))
for fam,d in [('F01',16),('F02',128)]:
 for g in 'AB':make(old[f'{fam}_main_{d}_{g}'],f'SMOKE_{fam}_{g}','smoke','smoke')
jsonl(R/'data/panel.jsonl',panel);jsonl(R/'data/legacy_baselines.jsonl',baseline);jsonl(R/'data/R18_comparison_audit.jsonl',legacy)
pp={x['id']:x for x in panel};comparisons=[]
def add(kind,a,b,role):
 x,y=pp[a],pp[b];xx,yy=x['text'],y['text'];samefact=x['evidence_item']==y['evidence_item'];onlytarget=False;onlynear=False
 if not samefact:
  l,r=x['evidence_char_span'];ll,rr=y['evidence_char_span'];onlytarget=xx[:l]==yy[:ll] and xx[r:]==yy[rr:]
 if x.get('near_char_span') and y.get('near_char_span'):
  l,r=x['near_char_span'];ll,rr=y['near_char_span'];onlynear=xx[:l]==yy[:ll] and xx[r:]==yy[rr:]
 row=dict(kind=kind,role=role,family=x['family'],split=x['split'],left=a,right=b,gap_left=x['actual_distance'],gap_right=y['actual_distance'],target_position_equal=x['target_position']==y['target_position'],evidence_position_equal=x['evidence_last_position']==y['evidence_last_position'],target_fact_equal=samefact,near_item_equal=x['near_item']==y['near_item'],same_token_multiset=sorted(x['token_ids'])==sorted(y['token_ids']),only_target_word_changed=onlytarget,only_near_word_changed=onlynear)
 if kind=='content':assert onlytarget
 if kind=='competition':assert onlynear and samefact and row['gap_left']==row['gap_right']==128 and row['evidence_position_equal']
 if kind=='distance':assert samefact and row['same_token_multiset'] and row['near_item_equal']
 comparisons.append(row)
for f in families:
 fam=f['family']
 for co in CONDS:add('content',f'{fam}_{co}_A',f'{fam}_{co}_B',co)
 for g in 'AB':
  for d,e in [(16,64),(16,128),(64,128)]:add('distance',f'{fam}_main{d}_{g}',f'{fam}_main{e}_{g}',f'{d}_to_{e}')
  for near,role in [(('B' if g=='A' else 'A'),'neutral_to_opposite'),(g,'neutral_to_congruent')]:add('competition',f'{fam}_nearN_{g}',f'{fam}_near{near}_{g}',role)
table(R/'data/text_pairing.csv',comparisons)
sitecfg=json.load(open(D1/'controlled_steps/S06_semantic_hierarchy_1104/frozen_plan.json'))['sites'];freqaudit=[]
for site in SITES:
 source=D1/site/'shared/frequency';ft=pd.read_csv(source/'frequency_table.csv');bounds=json.load(open(source/'frequency_boundaries.json'));meta=pd.read_parquet(source/'natural_positions.parquet');zz=sparse.load_npz(source/'natural_z.npz');mask=meta.split.to_numpy()=='discovery';counts=np.asarray((zz[mask]>0).sum(0)).ravel().astype(int);assert np.array_equal(counts,ft.positive_positions.to_numpy()) and sum(mask)==38400
 expected=np.full(30000,'insufficient',dtype='U12');expected[counts==0]='zero';ok=(counts>=20)&(ft.document_coverage.to_numpy()>=5);lo,hi=bounds['positive_count_edges'];expected[ok&(counts<lo)]='low';expected[ok&(counts>=lo)&(counts<hi)]='middle';expected[ok&(counts>=hi)]='high';assert np.array_equal(expected,ft.group.to_numpy())
 ft.to_csv(R/f'data/{site}_reference_frequency.csv',index=False);dump(R/f'data/{site}_reference_bins.json',bounds)
 sitecfg[site].update(reference_frequency_csv=str(source/'frequency_table.csv'),reference_frequency_sha256=sha(source/'frequency_table.csv'),reference_sparse_cache=str(source/'natural_z.npz'),reference_sparse_sha256=sha(source/'natural_z.npz'),reference_metadata=str(source/'natural_positions.parquet'),reference_metadata_sha256=sha(source/'natural_positions.parquet'))
 freqaudit.append(dict(site=site,reference_discovery_positions=int(sum(mask)),reference_all_positions=zz.shape[0],dictionary_size=zz.shape[1],counts_exact=True,bins_exact=True,bounds=bounds))
dump(R/'evidence/reference_validation.json',freqaudit)
cfg=dict(experiment='R19_REMOTE_TARGET_NEAR_COMPETITOR_COMPOSITION',UTC=now(),model=str(MODEL),seed=2026110419,sites=sitecfg,input_assets=['model_qwen3_0p6b_base_official_a5','tokenizer_qwen3_0p6b_base_official_a5','sae_a17_qwen_raw_o_proj_1b_valid_full_20261009t182142z','sae_qwen3_0p6b_e16_layer27_final_1b','dataset_r18_near_far_object_fact_pairs_20261104','representation_feature_composition_d1_dual_sae_20261103'],input_hashes={str(MODEL/x):sha(MODEL/x) for x in ['config.json','tokenizer.json','model.safetensors']},panel_sha256=sha(R/'data/panel.jsonl'),shape=[2,328],dtype='float32',device='cpu',threads=2,wall_ceiling_per_stage=3600,discovery=[f['family'] for f in families if f['R19_split']=='discovery'],heldout=[f['family'] for f in families if f['R19_split']=='heldout'],prefix_count=len(panel),new_prefixes=sum(x['R18_source_id'] is None for x in panel),primary_common_size=6,sensitivity_common_size=3,responsive_size=6,min_common_family_support=8,min_responsive_family_support=6,min_geometry_eligible=8,minimum_delta_norm=1e-6,bootstrap_draws=4096,conditional_family_signflips='all4096where12eligible,otherwiseexact2^N',association_permutations=9999,primary_holm_family=6,joint_holm_family=4,joint_binary_pairs_max=4,joint_amplitude_pairs_max=4,joint_pair_family_support=4,null_chains=4,null_draws=64,null_burn=100,null_thin=10,null_one_fallback_burn=500,null_one_fallback_thin=50,scientific_acceptance='Unknown',training=False,intervention=False,authorization='Current direct user explicitly authorizes this bounded SAE composition analysis and package; stop before interventions/training')
dump(R/'config.json',cfg);jsonl(R/'data/R18_scores.jsonl',[dict(oscores[x['R18_source_id']],R19_id=x['id']) for x in panel if x['R18_source_id']]);dump(R/'evidence/construction.json',dict(UTC=now(),prefixes=len(panel),new_prefixes=cfg['new_prefixes'],main_reused=144,opposite_reused=48,smoke=4,matched_far_rows=144,clean_comparisons=len(comparisons),legacy_unmatched_comparisons=len(legacy),all_prefix_tokens=320,far_evidence_position=190,target_position=319,splits=cfg['discovery'],heldout=cfg['heldout'],all_checks='PASS'))
for src in ['/tmp/r19_initial_assets_20261104.json','/tmp/r19_reference_assets_20261104.json']:shutil.copy(src,R/'evidence'/Path(src).name)
shutil.copy(D1/'controlled_steps/S09_marginal_vs_joint_1104/code/curveball.cpp',R/'code/curveball.cpp')
print('PREPARED',len(panel),'new',cfg['new_prefixes'],'pairs',len(comparisons))
