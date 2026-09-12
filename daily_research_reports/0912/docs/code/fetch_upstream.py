"""Agent-side source download; actual transfer is NOT claimed to have run here.
Uses pinned transformers tag. Records file digests and LICENSE; never executes code.
"""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT="https://raw.githubusercontent.com/huggingface/transformers/v4.57.1/"
FILES=["src/transformers/models/qwen3/modeling_qwen3.py",
       "src/transformers/models/qwen3/configuration_qwen3.py","LICENSE"]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--output-dir",required=True);a=p.parse_args()
    out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);manifest=[]
    for name in FILES:
        target=out/Path(name).name
        if target.exists():raise FileExistsError(target)
        with urllib.request.urlopen(ROOT+name,timeout=30) as response:data=response.read()
        target.write_bytes(data)
        manifest.append({"path":name,"url":ROOT+name,"sha256":hashlib.sha256(data).hexdigest()})
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
if __name__=="__main__":main()
