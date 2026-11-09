from common import *
import zipfile,tempfile,subprocess,sys,shutil
assert json.load(open(R/'evidence/independent_verification.json'))['status']=='PASS'
(R/'README.md').write_text('''# S08 natural-dataset SAE member overlap review packet

Start with summary_cn.md (Chinese), then detailed_cn.md, tables/overlap_summary.csv and figures/01_main_overlap.png /02_controls.png. English companions summary.md/detailed.md preserve the same measured scope. Protocol/frozen_plan and the timestamped fixed16amendment were saved before activations. Scientific acceptance/closure Unknown.

This packet includes all771selected original question texts and sampling positions/IDs, all native sparse SAE coordinates at10positions in two dictionaries, all30comparison estimates/document-bootstrap intervals, complete resample/null statistics, graph endpoints, code and key audits. It does not contain model/SAE weights, full source Arrow corpora or the derived dense kernel cache. Excluded objects have exact paths/revisions/hashes and sizes where applicable in data/sources.json, frozen_plan.json and large_files_index.json. No training or intervention occurred.

Run `python code/portable_replay.py` for model-free independent replay of all18main group means from the actual included sparse coordinates. To reproduce document CIs/control kernels, see reproduce.md and code/analyze.py. No git commit, push or external publication.
''')
# Root files and small evidence only. Dense kernels are explicitly excluded.
files=[]
for p in R.rglob('*'):
 if not p.is_file() or '__pycache__' in p.parts:continue
 rel=p.relative_to(R)
 if rel.parts[0]=='cache' and p.name!='activations.npz':continue
 if p.name in ['payload_manifest.json','final_delivery.json']:continue
 files.append(p)
manifest=dict(UTC=now(),files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)],excluded_index='large_files_index.json',all_selected_texts=True,all_native_sparse_coordinates=True,all_source_Arrow_files=False,model_weights=False)
dump(R/'payload_manifest.json',manifest);files.append(R/'payload_manifest.json')
zip_path=SYS/'daily_research_reports/1104/20261104_SAE_dataset_overlap.zip';assert not zip_path.exists()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(R)))
assert zip_path.stat().st_size<20_000_000
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='S08_review_') as temp:
  z.extractall(temp);tmp=Path(temp)
  for f in manifest['files']:assert sha(tmp/f['path'])==f['sha256']
  q=subprocess.run([sys.executable,str(tmp/'code/portable_replay.py')],capture_output=True,text=True);assert q.returncode==0,q.stdout+q.stderr;replay=json.loads(q.stdout)
receipt=dict(UTC=now(),status='PASS',archive=str(zip_path),bytes=zip_path.stat().st_size,MB_decimal=zip_path.stat().st_size/1e6,sha256=sha(zip_path),files=len(files),CRC='PASS',fresh_unzip_hashes='PASS',portable_main_mean_replay=replay,all771question_texts_and_sparse_coordinates_included=True,dense_kernel_included=False,model_or_SAE_weights_included=False,published=False)
dump(R/'evidence/final_delivery.json',receipt);dump(zip_path.with_suffix('.manifest.json'),receipt)
shutil.copy2(R/'evidence/final_delivery.json',C/'evidence/final_delivery.json');shutil.copy2(R/'README.md',C/'README.md')
print(json.dumps(receipt))
