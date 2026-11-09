from pathlib import Path
import json,hashlib,datetime,csv
R=Path(__file__).resolve().parents[1];MAIN=R.parent/'S06_semantic_hierarchy_1104';SYS=Path('/data/250010109/Research_System')
C=SYS/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps'/R.name
SITES=['ATTN_SAE','MLPIN_SAE'];DOMAINS={'animal':['animal','cat','dog'],'vehicle':['vehicle','car','bicycle']}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def rows(p):return [json.loads(l) for l in open(p) if l.strip()]
def jsonl(p,x):Path(p).write_text(''.join(json.dumps(v,ensure_ascii=False,allow_nan=False)+'\n' for v in x))
def table(p,rr):
 rr=list(rr);p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if not rr:p.write_text('');return
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
