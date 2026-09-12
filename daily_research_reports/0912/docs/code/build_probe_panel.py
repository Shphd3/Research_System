"""Build a fixed causal-prefix panel from researcher-validated JSONL, offline only.
Required: sample_id,prefix,relation_label,format_label,block_id,split.
Optional: expected_continuation (validated token boundary, first target stored only).
No semantic labels are inferred, and no answer is appended to the model input.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np

def build_panel(records,encode,pad_id,max_length):
    required={"sample_id","prefix","relation_label","format_label","block_id","split"}
    seen=set();sequences=[];positions=[];rows=[];targets=[]
    for r in records:
        missing=required-set(r)
        if missing:raise ValueError(f"Missing fields {missing}")
        if r["sample_id"] in seen:raise ValueError("Duplicate sample_id")
        seen.add(r["sample_id"])
        if r["split"] not in {"discovery","calibration","confirmation"}:raise ValueError("Invalid split")
        ids=list(encode(r["prefix"]))
        if not ids or len(ids)>max_length:raise ValueError("Empty or oversized prefix; no silent truncation")
        target=-100
        if "expected_continuation" in r:
            full=list(encode(r["prefix"]+r["expected_continuation"]))
            if full[:len(ids)]!=ids or len(full)<=len(ids):
                raise ValueError("Prefix/continuation tokenization boundary changed; fix the record explicitly")
            target=full[len(ids)]
        sequences.append(ids);positions.append(len(ids)-1);rows.append(r);targets.append(target)
    if not rows:raise ValueError("No panel records")
    width=max(map(len,sequences));x=np.full((len(rows),width),pad_id,dtype=np.uint32);mask=np.zeros_like(x,dtype=bool)
    for i,seq in enumerate(sequences):x[i,:len(seq)]=seq;mask[i,:len(seq)]=True
    result={"input_ids":x,"attention_mask":mask,"positions":np.array(positions),"sample_ids":np.array([r["sample_id"] for r in rows]),
            "semantic_labels":np.array([r["relation_label"] for r in rows]),"format_labels":np.array([r["format_label"] for r in rows]),
            "block_ids":np.array([r["block_id"] for r in rows]),"split":np.array([r["split"] for r in rows]),"expected_next_ids":np.array(targets)}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--jsonl",required=True)
    p.add_argument("--tokenizer",required=True);p.add_argument("--output",required=True)
    p.add_argument("--max-length",type=int,default=2048);a=p.parse_args()
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(a.tokenizer,local_files_only=True,trust_remote_code=False)
    pad=tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    if pad is None:raise ValueError("Explicit pad or EOS ID required")
    rows=[json.loads(line) for line in Path(a.jsonl).read_text().splitlines() if line.strip()]
    result=build_panel(rows,lambda s:tok.encode(s,add_special_tokens=False),pad,a.max_length)
    # Mixed split files are too easy to fit and evaluate on accidentally.
    if len(set(result["split"]))!=1:raise ValueError("Build separate NPZ files for each split")
    np.savez_compressed(a.output,**result)
    Path(a.output).with_suffix(".manifest.json").write_text(json.dumps({"source_sha256":hashlib.sha256(Path(a.jsonl).read_bytes()).hexdigest(),
      "tokenizer":a.tokenizer,"prefix_only":True,"split":str(result["split"][0]),"records":len(rows)},indent=2),encoding="utf-8")
if __name__=="__main__":main()
