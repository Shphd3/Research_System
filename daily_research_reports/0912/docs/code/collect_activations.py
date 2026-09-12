"""Collect ONE explicitly specified causal prediction position per record.
Input NPZ: input_ids[N,S], attention_mask[N,S], positions[N], sample_ids[N].
No tokenizer, chat template, answer-span, or pooling is guessed by this script.
"""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import torch
from model import Qwen3SAEForCausalLM

@torch.inference_mode()
def collect(model,inputs,batch_size=8,device="cpu"):
    ids=np.asarray(inputs["input_ids"])
    valid=np.asarray(inputs["attention_mask"],dtype=bool)
    pos=np.asarray(inputs["positions"],dtype=np.int64)
    names=np.asarray(inputs["sample_ids"]).astype(str)
    if ids.ndim!=2 or valid.shape!=ids.shape or pos.shape!=(len(ids),) or names.shape!=(len(ids),):
        raise ValueError("Invalid input panel shapes")
    if len(np.unique(names))!=len(names):
        raise ValueError("sample_ids must be unique")
    if np.any(pos<0) or np.any(pos>=ids.shape[1]) or not valid[np.arange(len(ids)),pos].all():
        raise ValueError("Each selected prediction position must be a valid prefix token")
    model.eval().to(device)
    acc={"raw_h":[],"h":[],"indices":[],"values":[],"reconstruction":[]}
    for a in range(0,len(ids),batch_size):
        x=torch.tensor(ids[a:a+batch_size].astype(np.int64),device=device)
        mask=torch.tensor(valid[a:a+batch_size],device=device)
        raw,h=model.forward_features(x,mask)
        row=torch.arange(len(x),device=device)
        p=torch.tensor(pos[a:a+batch_size],device=device)
        raw,h=raw[row,p],h[row,p]
        acc["raw_h"].append(raw.float().cpu().numpy())
        acc["h"].append(h.float().cpu().numpy())
        if model.sae is not None:
            out=model.sae(h)
            for k,v in [("indices",out.indices),("values",out.values),("reconstruction",out.reconstruction)]:
                acc[k].append(v.detach().cpu().numpy())
    result={k:np.concatenate(v) for k,v in acc.items() if v}
    result.update(sample_ids=names,positions=pos,selected_token_ids=ids[np.arange(len(ids)),pos])
    for key in ("semantic_labels","format_labels","block_ids","split","expected_next_ids"):
        if key in inputs:
            result[key]=np.asarray(inputs[key])
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint",required=True);p.add_argument("--panel",required=True)
    p.add_argument("--output",required=True);p.add_argument("--batch-size",type=int,default=8)
    p.add_argument("--device",default="cpu")
    a=p.parse_args()
    with np.load(a.panel,allow_pickle=False) as f:
        data=dict(f)
    model=Qwen3SAEForCausalLM.from_checkpoint(a.checkpoint)
    out=collect(model,data,a.batch_size,a.device)
    target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(target,**out)
    manifest={"panel_sha256":hashlib.sha256(Path(a.panel).read_bytes()).hexdigest(),
              "checkpoint":str(Path(a.checkpoint).resolve()),"representation":"final_post_RMSNorm",
              "position_semantics":"h_j predicts token j+1; no pooling", "records":len(out["sample_ids"]),
              "model_sha256":hashlib.sha256((Path(a.checkpoint)/"model.pt").read_bytes()).hexdigest()}
    target.with_suffix(".manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
if __name__=="__main__": main()
