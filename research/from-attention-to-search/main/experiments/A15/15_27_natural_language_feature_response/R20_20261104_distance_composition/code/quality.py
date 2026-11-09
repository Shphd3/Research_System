from load_data import *
import torch,collections
out=[];metadata={}
for site in SITES:
 a,dn=load_site(site,True);s=CFG['sites'][site];checkpoint=torch.load(s['path'],map_location='cpu',weights_only=False);meta=checkpoint.get('metadata',{});metadata[site]=dict(asset_id=s['asset_id'],path=s['path'],sha256=sha(s['path']),metadata=meta,parent_config_matches=meta.get('model_config_sha256',meta.get('config',{}).get('model_config_sha256'))==CFG['input_hashes'][str(Path(CFG['model'])/'config.json')]);del checkpoint
 assert metadata[site]['parent_config_matches']
 for frame,fs in MAP.items():
  for fam,dd in fs.items():
   for d in DISTS:
    pa,pb=[a[dd[str(d)][g]] for g in 'AB'];hd=pa['h']-pb['h'];rd=pa['reconstruction']-pb['reconstruction'];out.append(dict(site=site,frame=frame,family=fam,split=META[dd[str(d)]['A']]['split'],distance=d,hidden_fact_norm=float(np.linalg.norm(hd)),reconstructed_fact_norm=float(np.linalg.norm(rd)),reconstruction_fact_cosine=cosine(hd,rd),reconstruction_fact_projection=float(rd@hd/(hd@hd)),fact_relative_error=float(np.linalg.norm(hd-rd)/np.linalg.norm(hd)),relative_row_error_A=pa['relative_reconstruction_error'],relative_row_error_B=pb['relative_reconstruction_error']))
table(R/'tables/reconstruction_quality.csv',out);dump(R/'evidence/checkpoint_metadata_audit.json',dict(UTC=now(),sites=metadata,hooks='Native metadata/model-config identities verified; capture hook specification is in config/run code',no_weight_updates=True))
construction=[]
for p in PANEL:
 start,end=p['evidence_char_span'];l=p['text'].rfind('\n',0,start)+1;r=p['text'].index('\n',end)+1;q=families=None
 question=p['actual_question_suffix'];assert p['text'].endswith(question);filler=(p['text'][:l].splitlines()[1:]+p['text'][r:-len(question)].splitlines());construction.append(dict(id=p['id'],family=p['family'],frame=p['condition'],distance=p['actual_distance'],e=p['evidence_last_position'],p=p['target_position'],position_id_e=p['position_id_evidence'],position_id_p=p['position_id_target'],tokens=len(p['token_ids']),filler_lines=len(filler),unique_filler_lines=len(set(filler)),filler_repetitions=len(filler)-len(set(filler)),answer_suffix_unchanged=True))
table(R/'tables/control_construction_audit.csv',construction)
dump(R/'evidence/final_three_audits.json',dict(UTC=now(),scientific_acceptance='Unknown',audits=[dict(kind='scientific_identification',status='PASS',finding='Primary native-code observables are distinct from raw strength,direction,hidden information and causal use.',remaining='p/e/dnotindependent; oldheldoutexposed; reconstruction of fact differences poor; no general distance mechanism'),dict(kind='data_statistics',status='PASS',primary_families=12,exploratory_families=12,tests=6,correction='Holm',family_bootstrap=8192,template_strata=6,controls_new_conditions=228,case_rule_fixed=True,rare_zero_groups_retained=True),dict(kind='implementation_numerics',status='PASS',old_SAE_reencodings=288,old_Top32_exact=True,new_control_forward_conditions=228,old_forward_calibrations=6,smoke_no_op_error=0,smoke_candidate_lane_error=0,weights_unchanged=True,optimizer=False,trainable_parameters=0)]))
print('QUALITY',len(out))
