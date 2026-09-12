"""External matched-triplet semantic audit. No cluster-to-meaning automatic labels.
Triplet CSV columns: anchor_id,positive_id,negative_id,block_id.
The positive must match the intended meaning across format; the negative must
match the nuisance format while changing that meaning, validated BEFORE scoring.
"""
import argparse,csv,json
from pathlib import Path
import numpy as np
import torch
from .feature_statistics import sparse_codes

def cosine_rows(a,b):
    return np.einsum("nd,nd->n",a,b)/(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1)).clip(1e-12)

def triplet_margins(x,sample_ids,triplets):
    x=np.asarray(x,dtype=np.float64)
    lookup={str(v):i for i,v in enumerate(sample_ids)}
    if len(lookup)!=len(sample_ids):raise ValueError("Duplicate sample IDs")
    a,p,n=[],[],[]
    for t in triplets:
        for key in ("anchor_id","positive_id","negative_id","block_id"):
            if key not in t:raise ValueError(f"Missing {key}")
        a.append(lookup[t["anchor_id"]]);p.append(lookup[t["positive_id"]]);n.append(lookup[t["negative_id"]])
    a,p,n=np.array(a),np.array(p),np.array(n)
    covered=(np.linalg.norm(x[a],axis=1)>0)&(np.linalg.norm(x[p],axis=1)>0)&(np.linalg.norm(x[n],axis=1)>0)
    values=cosine_rows(x[a],x[p])-cosine_rows(x[a],x[n])
    return values,covered,np.array([t["block_id"] for t in triplets])

def block_bootstrap(values,blocks,repetitions=1000,seed=17):
    values=np.asarray(values,dtype=float);blocks=np.asarray(blocks)
    if len(values)==0:return {"status":"INSUFFICIENT","reason":"No covered triplets"}
    unique=np.unique(blocks)
    # Equal block weighting: correlated paraphrases do not pretend to be new facts.
    means=np.array([values[blocks==b].mean() for b in unique])
    if len(unique)<2:return {"status":"INSUFFICIENT","reason":"Fewer than two independent blocks","mean":float(means.mean())}
    rng=np.random.default_rng(seed)
    boot=np.array([means[rng.integers(0,len(means),size=len(means))].mean() for _ in range(repetitions)])
    return {"status":"DESCRIPTIVE_NOT_A_VERDICT","mean":float(means.mean()),"ci95":np.quantile(boot,[.025,.975]).tolist(),
            "independent_blocks":len(unique),"bootstrap_repetitions":repetitions,"seed":seed}

@torch.no_grad()
def patch_feature_group(h,sae,feature_ids,scale=0.0):
    """h' = h + D(z'-z). Keeps actual reconstruction residual; not h' = D z'.
    This is an off-manifold intervention, NOT automatically a causal semantic label.
    """
    idx,val=sae.encode(h)
    selected=torch.isin(idx,torch.as_tensor(feature_ids,device=idx.device,dtype=torch.long))
    changed=val.clone();changed[selected]*=scale
    return h + (sae.decode(idx,changed)-sae.decode(idx,val))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--activations",required=True);p.add_argument("--triplets",required=True)
    p.add_argument("--representation",choices=["h","raw_h","z"],default="h")
    p.add_argument("--width",type=int);p.add_argument("--output",required=True)
    a=p.parse_args()
    with np.load(a.activations,allow_pickle=False) as f:d=dict(f)
    with open(a.triplets,newline="",encoding="utf-8") as f:triplets=list(csv.DictReader(f))
    if a.representation=="z":
        if not a.width:raise ValueError("--width required for z")
        x=sparse_codes(d["indices"],d["values"],a.width).toarray()
    else:x=d[a.representation]
    values,covered,blocks=triplet_margins(x,d["sample_ids"],triplets)
    report=block_bootstrap(values[covered],blocks[covered])
    report.update(total_triplets=len(values),covered_triplets=int(covered.sum()),coverage=float(covered.mean()),
                  representation=a.representation,interpretation="conditional on externally validated relation; no automatic semantic proof")
    Path(a.output).write_text(json.dumps(report,indent=2),encoding="utf-8")
if __name__=="__main__":main()
