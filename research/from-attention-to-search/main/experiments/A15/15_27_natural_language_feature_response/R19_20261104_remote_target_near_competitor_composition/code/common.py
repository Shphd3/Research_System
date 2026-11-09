from pathlib import Path
import json,hashlib,datetime,csv
R=Path(__file__).resolve().parents[1]
SYS=Path('/data/250010109/Research_System')
P=SYS/'Projects/from-attention-to-search'
C=P/'main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition'
OLD=R.parent/'R01_behavior'
D1=Path('/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1')
MODEL=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
SITES=['ATTN_SAE','MLPIN_SAE']
CONDS=['main16','main64','main128','nearN','nearA','nearB']
GROUPS=['high','middle','low','insufficient','zero']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
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
