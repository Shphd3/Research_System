import os
for k in ["OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS"]: os.environ[k]="2"
from pathlib import Path
import json,hashlib,time,csv
import numpy as np
ROOT=Path("/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response")
OLD=ROOT/"R11_three_domain_replication_20261030/qualified_three_domain_A02"
OUT=ROOT/"R12_spectral_semantic_granularity_20261031"
PROJECT=Path("/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031")
LEAVES={"math":["algebra","analysis"],"biology":["cell","ecology_evolution"]}
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(4<<20),b""):h.update(b)
 return h.hexdigest()
def dump(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+".tmp");tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+"\n");tmp.replace(p)
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]
def table(p,a):
 a=list(a);p=Path(p);p.parent.mkdir(exist_ok=True,parents=True)
 if not a:p.write_text("status\nEMPTY\n");return
 keys=list(dict.fromkeys(k for r in a for k in r))
 with p.open("w",newline="") as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(a)
def order(r):return hashlib.sha256(("R12|"+r["seq_id"]).encode()).hexdigest()
class Tokenizer:
 def __init__(self):
  j=json.load(open("/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json"));self.v={v:k for k,v in j["model"]["vocab"].items()};self.v.update({x["id"]:x["content"] for x in j.get("added_tokens",[])})
  bs=list(range(33,127))+list(range(161,173))+list(range(174,256));cs=bs[:];n=0
  for b in range(256):
   if b not in bs:bs.append(b);cs.append(256+n);n+=1
  self.bd={chr(c):b for b,c in zip(bs,cs)}
 def decode(self,ids):
  s="".join(self.v.get(int(i),"<unk>") for i in ids);return bytes(self.bd.get(c,ord(c) if ord(c)<256 else 63) for c in s).decode("utf-8",errors="replace")
 def token(self,i):return self.decode([int(i)])
def get_cache(r):return OLD/"forward"/("H" if r["split"]=="heldout" else "DV")/(r["seq_id"]+".npz")
def selected_array(rr):
 h=[];z=[];nm=[]
 for r in rr:
  a=np.load(get_cache(r));t=r["position"];h.append(a["h27"][t].astype(float));v=np.zeros(16384);lo,hi=a["CC_ptr"][t:t+2];v[a["CC_ids"][lo:hi]]=a["CC_z"][lo:hi];z.append(v);nm.append(float(a["nmse"][t,-1]))
 return np.array(h),np.array(z),np.array(nm)
