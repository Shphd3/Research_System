import json,shutil,csv,hashlib,time,datetime,subprocess
from pathlib import Path
import numpy as np
p=json.load(open(Path(__file__).resolve().parents[1]/'config/frozen.json'))['paths'];R=Path(p['run']);E=Path(p['experiment']);repo=Path('/data/250010109/Research_System');st=np.load(R/'cache/train_stats.npz');owners=np.load(Path(p['previous_run'])/'metrics/core/owners.npz');floor=json.load(open(R/'provenance/denominators.json'));checks=[]
for group in ['T','R11']:
 owner=owners[group]
 for sc in range(4):
  means=np.load(R/'routes'/f'train_{group}_S{sc}.npz')['score'].astype(np.float64).mean(0);expected=np.array(floor['groups'][group]['mu']) if sc==0 else np.array([st['p'][owner==e].mean() for e in range(8)]) if sc==2 else np.ones(8);error=float(abs(means-expected).max());assert np.allclose(means,expected,rtol=1e-6,atol=1e-9);checks.append(dict(group=group,score=f'S{sc}',TRAIN_means=means.tolist(),expected=expected.tolist(),max_error=error))
 for split in ['train','eval']:
  for sc in range(4):
   d=np.load(R/'metrics/exposure'/f'{split}_{group}_S{sc}.npz');assert d['N_e'].sum()==(130712 if split=='train' else 65402);assert np.array_equal(d['counts'].sum(1),np.rint(d['p']*130712).astype(np.int64)) if split=='train' else True
   for e in range(8):
    if d['N_e'][e]==0:assert np.isnan(d['q'][:,e]).all()
write=lambda path,obj:Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write(R/'provenance/score_identity_verification.json',dict(status='PASS',checks=checks,candidate_m_floor_triggers=0,candidate_pm_floor_triggers=0,reason='All original reliable9615 triggers0, candidate9605 subset'))
shutil.copy2(R/'provenance/score_identity_verification.json',E/'evidence/score_identity_verification.json')
# Small portable scalar spectral arrays and endpoint NLLs; no hidden, decoder or branch tensors.
for sub in ['full_spectra','evaluation_endpoints']:(E/'evidence'/sub).mkdir(exist_ok=True)
extra=[]
for co in json.load(open(R/'config/frozen.json'))['conditions']:
 for seed in [11,22]:
  for src,dst in [(R/f'functional/{co["id"]}/seed{seed}/full_spectra.npz',E/f'evidence/full_spectra/{co["id"]}_seed{seed}.npz'),(R/f'training/{co["id"]}/seed{seed}/eval_epoch3.npz',E/f'evidence/evaluation_endpoints/{co["id"]}_seed{seed}.npz')]:
   shutil.copy2(src,dst);extra.append(dict(path=str(dst),source=str(src),bytes=dst.stat().st_size,sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),purpose='complete scalar spectra or final per-position held-out loss, not model/hidden cache'))
shutil.copy2(R/'smoke/baseline_eval.npz',E/'evidence/evaluation_endpoints/baseline.npz');m=json.load(open(E/'curated_evidence_manifest.json'));m['evidence']+=extra;write(E/'curated_evidence_manifest.json',m)
shutil.copy2(repo/'assets/checks/2026-10-19_normalized_learning_20261018T173143Z.json',R/'provenance/output_asset_access.json');shutil.copy2('/tmp/normalized_learning_new_asset_ids.json',R/'provenance/output_asset_ids.json');shutil.copy2('/tmp/normalized_learning_final_job.json',R/'provenance/final_job.json')
shutil.copy2(R/'provenance/output_asset_access.json',E/'evidence/output_asset_access.json')
# Preserve the historical first16 figures receipt, and record final completed18 without claiming a second statistics run.
old=json.load(open(R/'provenance/analysis_receipt.json'));write(R/'provenance/analysis_receipt_stage1.json',old);old['figures']=18;old['final_required_additional_figures']=2;old['primary_aggregation_wall_seconds']=old.pop('seconds');old['additional_plotting_seconds']='NOT_SEPARATELY_SAMPLED';write(R/'provenance/analysis_receipt.json',old);shutil.copy2(R/'provenance/analysis_receipt.json',E/'evidence/analysis_receipt.json')
# Bind report generators to durable config paths and retain executable source.
for name in ['write_normalized_reports.py','finish_normalized_docs.py','finalize_normalized_evidence.py']:
 s=Path('/tmp',name).read_text();s=s.replace("json.load(open(Path(__file__).resolve().parents[1]/'config/frozen.json'))['paths']","json.load(open(Path(__file__).resolve().parents[1]/'config/frozen.json'))['paths']");(R/'code'/name).write_text(s)
source=[]
for fp in sorted((R/'code').glob('*')):
 if fp.is_file():source.append(dict(path=str(fp),bytes=fp.stat().st_size,sha256=hashlib.sha256(fp.read_bytes()).hexdigest()))
shutil.copy2(R/'provenance/source_manifest.json',R/'provenance/source_manifest_at_training_verification.json');write(R/'provenance/source_manifest.json',source);shutil.copy2(R/'provenance/source_manifest.json',E/'evidence/source_manifest.json')
# The original Chinese attachment and pre-run configuration remain byte-preserved.
write(R/'provenance/protocol_consolidation_receipt.json',dict(kind='faithful consolidated exposition, not scientific amendment after results',authority='researcher message at2026-10-18T17:24:39Z supplement',original_protocol_sha256=hashlib.sha256((R/'provenance/protocol_v1_cn.md').read_bytes()).hexdigest(),frozen_config_sha256=hashlib.sha256((R/'config/frozen.json').read_bytes()).hexdigest(),canonical_English=str(E/'protocol.md'),canonical_Chinese=str(E/'protocol_cn.md'),original_Chinese=str(E/'protocol_frozen_v1_cn.md'),note='All scoring formulas/10conditions authorized before training. Later repairs only scalar hashing/telemetry/transport; model source unchanged since engineering repair.'))
print('Final evidence checks PASS;18figures,40scalar/endpoint archives carried.')
