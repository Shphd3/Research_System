"""Replot all eight saved figures from small report evidence, without Torch/cache."""
from pathlib import Path
import argparse, tempfile, subprocess, shutil,sys,hashlib,json

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--font',type=Path,default=Path('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf'));a=ap.parse_args()
 a.output_dir.mkdir(parents=True,exist_ok=True)
 def link(source,destination):destination.parent.mkdir(parents=True,exist_ok=True);destination.symlink_to(source.resolve())
 with tempfile.TemporaryDirectory(prefix='crosscoder_plot_evidence_') as tmp:
  temp=Path(tmp);old=temp/'existing';contrib=temp/'contribution';raw=temp/'raw';contrib.mkdir();raw.mkdir()
  link(a.root/'data/full_group_controls.csv',old/'structure/full_group_controls.csv')
  link(a.root/'provenance/full_repair_summary.json',old/'structure/full_repair_summary.json')
  link(a.root/'data/learning_metrics_original.csv',old/'analysis_outputs/learning_metrics.csv')
  code="import importlib.util,sys;from pathlib import Path;s=importlib.util.spec_from_file_location('saved_figures12',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.R=Path(sys.argv[2]);m.run(Path(sys.argv[3]),Path(sys.argv[4]));assert 'torch' not in sys.modules"
  subprocess.run([sys.executable,'-I','-B','-c',code,str(a.root/'code/figures12.py'),str(old),str(a.output_dir),str(a.font)],check=True,stdout=subprocess.DEVNULL)
  for state in ['original','column_shuffled']:
   for rule in ['same_frequency','mixed_frequency']:
    name=state+'_'+rule+'_spectra.npz';link(a.root/'data'/name,contrib/name)
  link(a.root/'provenance/contribution_frozen_config.json',contrib/'frozen_config.json')
  link(a.root/'provenance/contribution_spectrum_summary.json',contrib/'spectrum_summary.json')
  subprocess.run([sys.executable,'-I','-B',str(a.root/'code/plot_spectrum.py'),'--root',str(contrib),'--out',str(a.output_dir),'--font',str(a.font)],check=True,stdout=subprocess.DEVNULL)
  for rule in ['same_frequency','mixed_frequency']:
   name=rule+'_raw_hidden_spectra.npz';link(a.root/'data'/name,raw/name)
  link(a.root/'provenance/raw_hidden_frozen_config.json',raw/'frozen_config.json')
  link(a.root/'provenance/raw_hidden_raw_hidden_summary.json',raw/'raw_hidden_summary.json')
  subprocess.run([sys.executable,'-I','-B',str(a.root/'code/plot_raw_hidden.py'),'--root',str(raw),'--out',str(a.output_dir),'--font',str(a.font)],check=True,stdout=subprocess.DEVNULL)
 comparisons=[]
 for p in sorted(a.output_dir.glob('*.png')):
  orig=a.root/'figures'/p.name
  comparisons.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'original_sha256':hashlib.sha256(orig.read_bytes()).hexdigest(),'byte_identical':p.read_bytes()==orig.read_bytes()})
 assert len(comparisons)==8 and all(x['byte_identical'] for x in comparisons),comparisons
 result={'status':'PASS','PNG_byte_identical':8,'no_model_training_cache_required':True,'runtime_dependencies':'Python, NumPy, Matplotlib and external CJK font; no Torch/GPU','comparisons':comparisons}
 (a.output_dir/'replot_verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
