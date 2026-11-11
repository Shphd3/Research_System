from pathlib import Path
import sys,json,time,datetime,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];R4=R.parent/'20261109_atom_concentration_regularizer';R3=R.parent/'20261109_teacher_routing_signal_concentration';REPO=Path('/data/250010109/Research_System');REPORT=REPO/'daily_research_reports/1111/meeting_report/a5_checks'
sys.path[:0]=[str(R4),str(R4/'vendor')]
SEED=20261110;N=2097152;VOCAB=151936

def dump(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=True)+'\n')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def table(df,name,note='AI分析；研究者判断Unknown。'):
 p=R/'results'/name;p.parent.mkdir(parents=True,exist_ok=True);df.to_csv(p.with_suffix('.csv'),index=False);p.with_suffix('.md').write_text('# '+name+'\n\nAI分析；研究者判断Unknown。\n\n'+note+'\n\n'+df.to_markdown(index=False,floatfmt='.9g')+'\n')
def event(check,conclusion,gpu_seconds=0,**kw):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();row=dict(time=now,check=check,conclusion=conclusion,gpu_seconds=gpu_seconds,judgment='Unknown',**kw)
 with (R/'evidence/events.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 mem=REPO/'.research/memory/conversations/1110-A5增益来源检查/memory.md'
 import re
 old=mem.read_text();mem.write_text(re.sub(r'^Latest update at:.*$', 'Latest update at: '+now,old,count=1,flags=re.M))
 with mem.open('a') as f:f.write(f'\n\n## {now} -- 检查{check}\n\n- Summary: AI分析：{conclusion}；研究者判断Unknown。\n- Current work: 本项GPU进程用时{gpu_seconds:.3f}秒；仅冻结模型前向／小探针。\n- Next action: 按原顺序推进未完成项，不改R04。\n- References: {R}/results；{R}/evidence/events.jsonl。\n')
 print(json.dumps(row,ensure_ascii=False),flush=True)
def tokens(split):return np.load(R4/f'data/{split}_tokens.npy',mmap_mode='r')
def docs(split):
 t=tokens(split);return np.cumsum((t[:N]==151645).astype(np.int32))
def erows(arm):
 root=R4 if arm in ['A5','A6'] else R3
 return {z['optimizer_step']:z for z in map(json.loads,(root/f'eval/{arm}.jsonl').read_text().splitlines())}
def position(arm,step):
 e=erows(arm).get(step,{})
 return Path(e.get('position_artifact') or R4/f'analysis/positions/{arm}/step{step:06d}.npz')
def model_path(arm,step):
 if arm=='A0' and step==500 and (R/'evidence/A0_500_restore.json').exists():return R/'data/A0_500_restored_state.pt'
 if arm in ['A5','A6']:return R4/f'runs/{arm}/weights/step_{step:06d}.pt'
 hits=[]
 for p in (R3/f'runs/{arm}').glob('*/*/manifest.json'):
  z=json.load(open(p))
  if z['optimizer_step']==step:hits.append(p.parent/'state.pt')
 assert hits,(arm,step)
 return hits[0]
def load_model(arm,step,device='cuda'):
 import torch
 from moe_baseline.model import DenseAlignedMoE,MoeConfig
 from routing import configure
 cfg=json.load(open((R4 if arm in ['A5','A6'] else R3)/f'arms/{arm}.yaml'))
 with torch.device('meta'):m=DenseAlignedMoE(MoeConfig.from_dict(cfg['model']))
 st=torch.load(model_path(arm,step),map_location='cpu',mmap=True,weights_only=False);m.load_state_dict(st['model'],assign=True);del st
 for b in m.blocks:
  for n,v in b.moe.named_buffers(recurse=False):
   if v.is_meta:setattr(b.moe,n,torch.zeros(v.shape,dtype=v.dtype))
 m.to(device).eval().requires_grad_(False);configure(m,cfg);return m,cfg

def register(aid,title,paths,identity,category='analysis'):
 import fcntl,subprocess
 paths=[Path(p) for p in paths];assert all(p.exists() for p in paths)
 with (REPO/'assets/.catalog.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);p=REPO/'assets/catalog.json';c=json.load(open(p))
  if aid not in {x['id'] for x in c['assets']}:
   c['assets'].append(dict(id=aid,title_cn=title,category=category,kind='r04_followup_a5_gain_checks',projects=['from-attention-to-search','moe-router-execution'],required_projects=[],storage_owner='MoE_Router',payload_status='SOURCE_FILES_PRESENT',locations=[dict(path=str(z),expected='file',required=True,probes=[]) for z in paths],identity=identity,source_paths=[str(R/'protocol_frozen_cn.md')]))
   q=p.with_suffix('.a5checks.tmp');q.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');q.replace(p)
 receipt=R/f'evidence/access_{aid}_{time.time_ns()}.json'
 subprocess.run([sys.executable,str(REPO/'tools/check_assets.py'),'--strict','--asset',aid,'--output',str(receipt)],cwd=REPO,stdout=__import__('subprocess').DEVNULL,check=True)
