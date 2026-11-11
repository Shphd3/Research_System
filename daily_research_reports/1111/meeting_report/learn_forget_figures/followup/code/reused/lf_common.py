from pathlib import Path
import os,sys,json,time,datetime,hashlib,fcntl
import numpy as np,pandas as pd,torch
from scipy import sparse
from scipy.stats import spearmanr
R=Path(__file__).resolve().parents[1];BASE=R.parent;REPO=Path('/data/250010109/Research_System');R4=BASE/'20261109_atom_concentration_regularizer';R5=BASE/'20261110_distill_self_atom_routing';R3=BASE/'20261109_teacher_routing_signal_concentration';REPORT=REPO/'daily_research_reports/1111/meeting_report/learn_forget_figures';REPORT.mkdir(parents=True,exist_ok=True);N=2097152
torch.set_num_threads(4)
def dump(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def table(d,name,note=''):
 p=R/'results'/name;p.parent.mkdir(parents=True,exist_ok=True);d.to_csv(p.with_suffix('.csv'),index=False);p.with_suffix('.md').write_text('# '+name+'\n\nAI分析；研究者判断Unknown。'+note+'\n\n'+d.to_markdown(index=False,floatfmt='.7g')+'\n')
def event(stage,text,**kw):
 z=dict(time_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stage=stage,conclusion=text,researcher_judgment='Unknown',**kw)
 with (R/'evidence/events.jsonl').open('a') as f:f.write(json.dumps(z,ensure_ascii=False)+'\n')
 print(json.dumps(z,ensure_ascii=False),flush=True)
def register(aid,paths,identity,category='analysis'):
 paths=list(map(Path,paths));assert all(p.exists() for p in paths)
 with (REPO/'assets/.catalog.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);p=REPO/'assets/catalog.json';c=json.load(open(p))
  if not any(a['id']==aid for a in c['assets']):
   c['assets'].append(dict(id=aid,title_cn=aid,category=category,kind='learn_forget_figures_20261111',projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(z),expected='file',required=True,probes=[]) for z in paths],identity=identity,source_paths=[str(R/'protocol_cn.md')]))
   q=p.with_suffix('.lf.tmp');q.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');q.replace(p)
 import subprocess
 subprocess.run([sys.executable,str(REPO/'tools/check_assets.py'),'--strict','--asset',aid,'--output',str(R/f'evidence/access_{aid}_{time.time_ns()}.json')],stdout=subprocess.DEVNULL,check=True)
def codes(split):return torch.load(R4/f'data/{split}_codes.pt',map_location='cpu',weights_only=False)
def features(split):
 d=codes(split);i=d['indices'].numpy();good=d['values'].numpy()>0;rr=np.broadcast_to(np.arange(N,dtype=np.int32)[:,None],i.shape)[good];F=sparse.csr_matrix((np.ones(good.sum(),np.float32),(rr,i[good])),shape=(N,30000));return F,d
def savefig(fig,name,note):
 import matplotlib.pyplot as plt
 fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(R/f'results/{name}.{ext}',dpi=160)
 plt.close(fig);(R/f'results/{name}_读法.md').write_text('AI分析；研究者判断Unknown。\n\n'+note+'\n')
def oldroot(a):return R5 if a in ['A8','A9','A9d'] else R4 if a in ['A5','A6'] else R3
def evals(a):return {x['optimizer_step']:x for x in map(json.loads,(oldroot(a)/f'eval/{a}.jsonl').read_text().splitlines())}
def artifact(a,s):return torch.load(evals(a)[s]['feature_artifact'],map_location='cpu',weights_only=False)
