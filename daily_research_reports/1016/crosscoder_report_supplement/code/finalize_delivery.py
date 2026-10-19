from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,subprocess,shutil,csv
S=Path('/data/250010109/Research_System');E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder');R=E/'analysis/report_spectrum';D=S/'daily_research_reports/1016/crosscoder_report_supplement';PHI=S/'daily_research_reports/1016/crosscoder_phi_input_spectrum'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 shutil.copy2(Path(__file__),D/'code'/Path(__file__).name)
 for p in (R/'20261016_audit').glob('*'):
  if p.is_file():shutil.copy2(p,D/'provenance'/('audit_'+p.name))
 preservation=json.loads((D/'source_preservation_check.json').read_text());assert preservation['status']=='PASS' and preservation['declared_original_phrase_replacements']==3
 assert len(list((D/'figures').glob('*.png')))==8 and len(list((D/'figures').glob('*.pdf')))==8
 for f,n in [('report_cn.md',6),('appendix_cn.md',2)]:
  body=(D/f).read_text()
  for key in ['统计对象：','计算方法：','实际观察：','推断边界：']:assert body.count(key)==n
 assert '尚未填入经验谱结果' not in (D/'report_cn.md').read_text()
 spec=json.loads((D/'provenance/contribution_spectrum_summary.json').read_text());raw=json.loads((D/'provenance/raw_hidden_raw_hidden_summary.json').read_text())
 assert spec['groups_per_rule']==raw['groups_per_rule']==1119
 assert all(x['estimable_groups']==1119 and x['zero_variance_groups']==0 for x in spec['results'].values())
 assert all(x['estimable_groups']==1119 and x['insufficient_groups']==x['zero_variance_groups']==0 for x in raw['rules'].values())
 assert raw['sample_N_per_group']==128 and spec['N_positions']==131072
 f1=list(csv.DictReader((D/'data/figure1_plot_data.csv').open()))
 assert [round(float(x['group_equal_log10_frequency_sd']),9) for x in f1]==[.353310533,.604781172]
 checks={'created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_EXECUTION_AND_DELIVERY_NOT_SCIENTIFIC_APPROVAL','screenshot_source_preservation':preservation,'figures':8,'formats':['PNG','PDF'],'four_part_captions':8,'PNG_all_visually_inspected':True,'PDF_independently_rendered':False,'replot':json.loads((D/'provenance/replot_verification.json').read_text()),'contribution_groups_each':1119,'contribution_positions':131072,'raw_groups_each':1119,'raw_positions_each':128,'new_training_updates':0,'new_model_forwards':0,'graph_parameter_changes':0,'new_branches':0}
 assert checks['replot']['PNG_byte_identical']==8
 files=[str(p) for p in D.glob('*.md')]+[str(D/'sources/user_report_transcription_cn.md')]
 math=subprocess.run(['python',str(S/'tools/check_markdown_math.py')]+files,capture_output=True,text=True)
 assert math.returncode==0,math.stdout+math.stderr
 checks['math_source_check']=math.stdout.strip();checks['math_rendering_verified']=False
 links=0
 for p in D.rglob('*.md'):
  for target in re.findall(r'!?\[[^\]\n]*\]\(([^\)\n]+)\)',p.read_text()):
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
   dest=(p.parent/target.split('#')[0]).resolve();assert dest.exists(),(p,target);assert dest.is_relative_to(D.resolve()) or dest.is_relative_to(PHI.resolve()),(p,target);links+=1
 checks['local_links_verified']=links
 excluded=[str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and (p.suffix in ['.pt','.pth','.bin','.safetensors','.npy','.log','.ttf','.otf'] or '__pycache__' in p.parts)]
 assert not excluded,excluded;checks['forbidden_payloads']=excluded
 inventory=[{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p.name not in ['artifact_manifest.json','delivery_checks.json']]
 manifest={'created_at_utc':checks['created_at_utc'],'files':inventory,'inventory_excludes':['artifact_manifest.json','delivery_checks.json'],'scope':'Screenshot-preserving supplement; existing result redraw; new descriptive contribution/raw-hidden spectra, no training or graph changes','selected_evidence_exceptions':['eight PNG/PDF figure types','original user screenshot','small group spectra NPZ including sampling IDs and plotted CSV'],'source_receipts':['provenance/figures12_source_manifest.json','provenance/contribution_pre_compute_source_receipt.json','provenance/contribution_sample_cache_receipt.json','provenance/raw_hidden_frozen_config.json','provenance/raw_hidden_plot_provenance.json'],'execution_roots':[str(R/'20261016_spectrum'),str(R/'20261016_raw_hidden')],'scientific_approval':'Unknown','question_closure':'Unknown'}
 if PHI.exists():
  manifest['declared_external_supplement']={'path':str(PHI),'manifest_sha256':sha(PHI/'artifact_manifest.json'),'scope':'Frozen186phi group-winning raw spectra supplement; package this folder with the original if sharing both'}
 (D/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 for x in inventory:assert sha(D/x['path'])==x['sha256']
 checks['artifact_files_verified']=len(inventory);checks['artifact_manifest_sha256']=sha(D/'artifact_manifest.json')
 (D/'delivery_checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
 (R/'20261016_delivery.json').write_text(json.dumps({'report_root':str(D),'manifest_sha256':checks['artifact_manifest_sha256'],'checks':str(D/'delivery_checks.json'),'contribution_summary':str(R/'20261016_spectrum/spectrum_summary.json'),'raw_hidden_summary':str(R/'20261016_raw_hidden/raw_hidden_summary.json'),'graph_parameter_changes':0,'new_training_updates':0,'new_model_forwards':0,'scientific_approval':'Unknown'},indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'status':checks['status'],'files':len(inventory),'links':links,'figures':8,'report':str(D/'report_cn.md')},ensure_ascii=False))
if __name__=='__main__':main()
