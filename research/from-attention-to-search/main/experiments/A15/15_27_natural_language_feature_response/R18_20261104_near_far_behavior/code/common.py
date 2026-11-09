from pathlib import Path
import json, hashlib, datetime
R = Path(__file__).resolve().parents[1]
SYS = Path('/data/250010109/Research_System')
C = SYS/'Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior'
MODEL = Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(8<<20),b''): h.update(b)
    return h.hexdigest()
def dump(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def rows(p): return [json.loads(s) for s in Path(p).read_text().splitlines() if s]
def jsonl(p,x): Path(p).write_text(''.join(json.dumps(z,ensure_ascii=False,allow_nan=False)+'\n' for z in x))
