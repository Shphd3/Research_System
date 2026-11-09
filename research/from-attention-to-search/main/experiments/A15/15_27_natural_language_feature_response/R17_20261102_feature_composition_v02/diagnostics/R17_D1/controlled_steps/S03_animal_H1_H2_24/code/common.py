from pathlib import Path
import json, hashlib, datetime, csv
R = Path(__file__).resolve().parents[1]
S = Path('/data/250010109/Research_System')
C = S/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps'/R.name
OLD = R.parent/'S02_animal_cat_dog_12'
SITES = ['ATTN_SAE','MLPIN_SAE']
CONDS = ['P','cat','dog','N']
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8<<20),b''): h.update(b)
 return h.hexdigest()
def dump(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def rows(p): return [json.loads(l) for l in open(p) if l.strip()]
def jsonl(p,x):
 Path(p).write_text(''.join(json.dumps(a,ensure_ascii=False,allow_nan=False)+'\n' for a in x))
def table(p,rr,fields=None):
 rr=list(rr);p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 fields=fields or list(rr[0])
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rr)
