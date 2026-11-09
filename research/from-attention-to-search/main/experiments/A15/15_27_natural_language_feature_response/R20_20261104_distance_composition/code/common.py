from pathlib import Path
import json,csv,hashlib,datetime
from zoneinfo import ZoneInfo
import numpy as np
R=Path(__file__).resolve().parents[1]
SYS=Path('/data/250010109/Research_System');P=SYS/'Projects/from-attention-to-search'
OLD=R.parent/'R02_feature_composition'
OLD_C=P/'main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition'
C=P/'main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition'
A=P/'main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_12_distance_composition_anchor.md'
FOCUS=P/'main/focus/focus_distance_composition.md'
SITES=['ATTN_SAE','MLPIN_SAE'];GROUPS=['high','middle','low','insufficient','zero'];DISTS=[16,64,128];PAIRS=[(16,64),(64,128),(16,128)]
SEED=2026110420
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def local_now():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8), 'Asia/Shanghai')).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def rows(p):return [json.loads(s) for s in Path(p).read_text().splitlines() if s.strip()]
def jsonl(p,x):Path(p).write_text(''.join(json.dumps(z,ensure_ascii=False,allow_nan=False)+'\n' for z in x))
def table(p,x):
 x=list(x);p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if not x:p.write_text('');return
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(x[0]));w.writeheader();w.writerows(x)
def cosine(a,b):
 den=np.linalg.norm(a)*np.linalg.norm(b)
 return float(a@b/den) if den>1e-12 else None
def cid(frame,f,d,g):return f'{f}_main{d}_{g}' if frame=='baseline' or (frame=='fixed_e' and d==128) else f'{f}_{frame}_d{d}_{g}'
