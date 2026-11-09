from common import *
import shutil,re
# Copy only named small evidence; full text matrices, sparse caches and raw logs stay execution-side.
for folder in ['code','figures']:
 for f in (R/folder).iterdir():
  if f.is_file() and f.suffix in ['.py','.cpp','.png','.json']:
   dest=C/folder/f.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(f,dest)
for folder,names in {'tables':['text_pairing.csv','behavior_summary.csv','behavior_individual.csv','behavior_pairs.csv','membership_summary.csv','family_geometry.csv','frequency_coverage.csv','frequency_pair_changes.csv','fixed_member_values.csv','joint_pair_values.csv','single_member_marginals.csv','declared_sensitivities.csv','fact_aligned_vs_swapped.csv','reconstruction_quality.csv','common_member_coverage.csv','joint_pair_family_coverage.csv'], 'results':['primary_hypotheses.json','joint_hypotheses.json','case_selection.json','declared_sensitivities.json'], 'evidence':['verification.json','figure_review.json','candidates_and_joint_frozen.json','analysis_code_frozen_before_heldout.json','reference_validation.json','role_metadata_audit.json','pre_run_audits.json','design_result_resolution.json','output_asset_ids.json']}.items():
 for name in names:
  f=R/folder/name
  if name=='text_pairing.csv':f=R/'data/text_pairing.csv'
  if f.exists():
   assert f.stat().st_size<=2*1024*1024,f
   dest=C/folder/name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(f,dest)
shutil.copyfile(R/'config.json',C/'config.json')
for f in [R/'data/candidates.json',R/'data/ATTN_SAE_joint_directions.json',R/'data/MLPIN_SAE_joint_directions.json',R/'data/ATTN_SAE_reference_bins.json',R/'data/MLPIN_SAE_reference_bins.json']:
 dest=C/'config'/f.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(f,dest)
assets=[]
for f in C.rglob('*'):
 if f.is_file() and f.suffix in ['.json','.csv','.png','.svg']:
  rel=f.relative_to(C);origin=R/rel
  if str(rel)=='tables/text_pairing.csv':origin=R/'data/text_pairing.csv'
  if rel.parts[0]=='config':origin=R/'data'/f.name
  if f.name=='payload_manifest.json':continue
  assets.append(dict(path=str(f.relative_to(P)),purpose='R19 selected factual evidence: '+str(rel),origin=str(origin),sha256=sha(f),bytes=f.stat().st_size))
man=P/'main/curated_evidence.json';j=json.load(open(man));prefix=str(C.relative_to(P))+'/'
j['assets']=[a for a in j['assets'] if not a['path'].startswith(prefix)]+assets;dump(man,j)
print('CURATED',len(assets))
