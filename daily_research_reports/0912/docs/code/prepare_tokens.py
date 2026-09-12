"""Offline JSONL -> deterministic document split -> uint32 token shards.
Input records must have text, optionally id. Requires a locally available HF tokenizer.
Token stream uses EOS between documents; cross-document attention is permitted in
this first protocol, and must be identical across arms. No chat/SFT masking.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np

def split_for_text(text):
    normalized=" ".join(text.split())
    key=hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    bucket=int(key[:8],16)%1000
    return ("validation" if bucket<5 else "test" if bucket<10 else "train"),key

def write_shards(records,tokenize,eos_id,out_dir,shard_tokens=1_000_000,excluded_hashes=frozenset()):
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    if list(out.glob("*.bin")):raise FileExistsError("Refuse overwriting existing token shards")
    seen=set();buffers={k:[] for k in ("train","validation","test")};counts={k:0 for k in buffers}
    doc_counts={k:0 for k in buffers};index={k:0 for k in buffers};manifest=[]
    def flush(split,force=False):
        while len(buffers[split])>=shard_tokens or (force and buffers[split]):
            size=min(shard_tokens,len(buffers[split]));values=buffers[split][:size];del buffers[split][:size]
            array=np.asarray(values,dtype=np.uint32);name=f"{split}-{index[split]:05d}.bin"
            (out/name).write_bytes(array.astype("<u4").tobytes())
            manifest.append({"file":name,"tokens":size,"sha256":hashlib.sha256((out/name).read_bytes()).hexdigest()})
            index[split]+=1
    for rec in records:
        text=rec.get("text")
        if not isinstance(text,str) or not text.strip():continue
        split,key=split_for_text(text)
        if key in seen or key in excluded_hashes:continue
        seen.add(key);tokens=list(tokenize(text))+[int(eos_id)]
        if any(not isinstance(x,int) or x<0 or x>=2**32 for x in tokens):raise ValueError("Invalid token ID")
        buffers[split].extend(tokens);counts[split]+=len(tokens);doc_counts[split]+=1;flush(split)
    for split in buffers:flush(split,True)
    info={"dtype":"little-endian uint32","split_unit":"normalized whole-document SHA256",
          "deduplication":"exact normalized text only; NOT near-duplicate decontamination",
          "token_counts":counts,"document_counts":doc_counts,"eos_id":int(eos_id),"shards":manifest}
    (out/"manifest.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
    return info

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--jsonl",required=True)
    p.add_argument("--tokenizer",required=True);p.add_argument("--output-dir",required=True)
    p.add_argument("--exclude-hashes",help="one normalized-document SHA256 per line")
    a=p.parse_args()
    from transformers import AutoTokenizer # Optional, never silently downloads.
    tok=AutoTokenizer.from_pretrained(a.tokenizer,local_files_only=True,trust_remote_code=False)
    if tok.eos_token_id is None:raise ValueError("Tokenizer has no EOS; explicit validated choice needed")
    exclude=frozenset(Path(a.exclude_hashes).read_text().splitlines()) if a.exclude_hashes else frozenset()
    def records():
        with open(a.jsonl,encoding="utf-8") as f:
            for line in f:
                if line.strip():yield json.loads(line)
    info=write_shards(records(),lambda text:tok.encode(text,add_special_tokens=False),tok.eos_token_id,a.output_dir,excluded_hashes=exclude)
    info["tokenizer_source"]=a.tokenizer
    info["tokenizer_files_sha256"]={str(p.relative_to(a.tokenizer)):hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in Path(a.tokenizer).rglob("*") if p.is_file()}
    Path(a.output_dir,"manifest.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
if __name__=="__main__":main()
