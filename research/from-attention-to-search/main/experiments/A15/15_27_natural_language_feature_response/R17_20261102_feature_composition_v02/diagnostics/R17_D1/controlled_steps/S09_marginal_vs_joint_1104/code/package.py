from common import *
import zipfile,tempfile,subprocess,sys,shutil
assert json.load(open(R/'evidence/independent_verification.json'))['status']=='PASS'
(R/'README.md').write_text('''# S09 marginal frequencies and joint structure review packet

Start with summary_cn.md, the two primary figures and detailed_cn.md. English companions retain the same scope. Protocol and frozen_plan separate A-frequency explanation from B-exact-margin joint replication. Original S08files are unchanged; all771original selected texts/native sparse coordinates are copied identically into inputs for auditing, not re-sampled. Each source128discovery/129heldout, all8original main positions intact.

Included: original sparse inputs and selected question texts/metadata, fixed split/30000feature discovery marginals,24IDs/all276pair directions, all256conditional-null trace statistics per six conditions, Bernoulli traces, actual constraints/mixing diagnostics, all tables/figures/scripts and adverse cases. Each full original null file includes trace statistics and compact real kernels, but complete per-draw null support matrices are not saved. Eight full audit support snapshots per condition remain execution-side and are indexed in large_files_index.json. Model/SAE weights, full Arrow corpora and host compiled shared library are excluded. C++sampler source is included.

Run `python code/portable_replay.py` to replay78point values from these actual included sparse inputs, frozen directions and null traces, without a model, original execution path or compiled sampler. Reproduce full nulls from code/curveball.cpp and config as described in reproduce.md, in a new output copy because scripts refuse overwrite. Independent verification of all original80S08file hashes happened execution-side and is recorded; this packet does not contain the entire originalS08result tree.

A frequency reproduction ratio is descriptive, not a causal explained fraction. B conditional joint associations are not semantic/router mechanisms; formatting has not been independently matched. Conditional CIs and Monte Carlo diagnostics retain their scope. Scientific acceptance/closureUnknown; no automatic follow-up, commit/push/publication.
''')
files=[]
for p in R.rglob('*'):
 if not p.is_file() or '__pycache__' in p.parts:continue
 rel=p.relative_to(R)
 if rel.parts[0]=='cache' and (p.name.endswith('__audit_snapshots.npz') or p.suffix=='.so'):continue
 if p.name in ['payload_manifest.json','final_delivery.json']:continue
 files.append(p)
manifest=dict(UTC=now(),files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)],original_input_panel_sha256=sha(R/'inputs/data/panel.jsonl'),original_input_sparse_sha256=sha(R/'inputs/cache/activations.npz'),all771selected_texts=True,all_native_sparse_inputs=True,all_null_joint_traces=True,all_original_source_Arrow_or_weights=False,full_audit_support_matrices=False,excluded_index='large_files_index.json')
dump(R/'payload_manifest.json',manifest);files.append(R/'payload_manifest.json');zp=SYS/'daily_research_reports/1104/20261104_SAE_marginal_joint.zip';assert not zp.exists()
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(R)))
assert zp.stat().st_size<20_000_000
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='S09_review_') as dest:
  z.extractall(dest);target=Path(dest)
  for f in manifest['files']:assert sha(target/f['path'])==f['sha256']
  q=subprocess.run([sys.executable,str(target/'code/portable_replay.py')],capture_output=True,text=True);assert q.returncode==0,q.stdout+q.stderr;replay=json.loads(q.stdout)
receipt=dict(UTC=now(),status='PASS',archive=str(zp),bytes=zp.stat().st_size,MB=zp.stat().st_size/1e6,sha256=sha(zp),files=len(files),CRC='PASS',fresh_unzip_hashes='PASS',portable_point_replay=replay,original_S08_changed=0,all771selected_texts_and_native_sparse_inputs_included=True,all_null_trace_samples_included=True,full_null_audit_support_states_included=False,weights_included=False,published=False)
dump(R/'evidence/final_delivery.json',receipt);dump(zp.with_suffix('.manifest.json'),receipt);shutil.copy2(R/'evidence/final_delivery.json',C/'evidence/final_delivery.json');shutil.copy2(R/'README.md',C/'README.md');shutil.copy2(R/'code/package.py',C/'code/package.py');print(json.dumps(receipt))
