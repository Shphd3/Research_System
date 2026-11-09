import os,sys,json,re,hashlib,unicodedata
from pathlib import Path
import numpy as np
sys.path.insert(0,'/data/250010109/dependency_packages/hf_transformers_qwen3')
from tokenizers import Tokenizer
R=Path(__file__).resolve().parents[1]
SRC=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027')
def dump(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lines(p):return [json.loads(x) for x in Path(p).read_text().splitlines()]
def classify(s):
 if not s or s.isspace():return 1
 if any(c.isalpha() or c.isnumeric() for c in s):return 0
 if all(c.isspace() or unicodedata.category(c).startswith('P') for c in s):return 2
 return 3
def candidates(text):
 ends=[]
 for m in re.finditer(r'[.!?][\"\u201d\u2019\)\]]*(?=\s|$)',text):
  pos=m.start();pre=text[:pos+1]
  if text[pos]=='.':
   if re.search(r'(?i)(?:\b(?:e\.g|i\.e|etc|vs|Dr|Mr|Mrs|Prof|Fig|Eq|No|U\.S|U\.K)|\b[A-Za-z])\.$',pre):continue
  ends.append(m.end())
 start=0;out=[]
 for end in ends+[len(text)]:
  if end<=start:continue
  a=start
  while a<end and text[a].isspace():a+=1
  if a<end:out.append((a,end,end in ends))
  start=end
 return out
def main():
 (R/'data').mkdir(exist_ok=True)
 tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')
 docs=lines(SRC/'data/documents.jsonl'); rows=[];texts=[]
 for di,d in enumerate(docs):
  enc=tok.encode(d['prefix'],add_special_tokens=False);assert enc.ids==d['token_ids']
  pieces=[tok.decode([i],skip_special_tokens=False) for i in enc.ids]
  d['token_offsets']=enc.offsets;d['token_surfaces']=pieces;d['token_class']=[classify(s) for s in pieces]
  for si,(a,b,terminal) in enumerate(candidates(d['prefix'])):
   reason='candidate'
   if si==0 and d['char_start']>0:reason='first_source_boundary_unverified'
   if not terminal:reason='trailing_fragment'
   text=d['prefix'][a:b]
   if '\n\n' in text:reason='paragraph_or_heading_needs_review' if reason=='candidate' else reason
   ids=[j for j,(s,e) in enumerate(enc.offsets) if e>a and s<b and not d['prefix'][s:e].isspace()]
   # Whitespace-only tokens between sentence endpoints remain included.
   pos=list(range(min(ids),max(ids)+1)) if ids else []
   row=dict(sid=len(rows),doc=di,seq_id=d['seq_id'],domain=d['domain'],start=a,end=b,positions=pos,text=text,auto_reason=reason)
   rows.append(row);texts.append(f"{row['sid']} | {d['domain']} | {d['seq_id']} | {reason} | {text.replace(chr(10),' [NL] ')}")
 dump(R/'data/documents.json',docs);dump(R/'data/sentence_candidates.json',rows)
 (R/'data/text_only_review.txt').write_text('\n'.join(texts)+'\n')
 dump(R/'provenance/preparation.json',dict(documents=len(docs),candidates=len(rows),token_alignment='exact all120',source_sha256=sha(SRC/'data/documents.jsonl'),outcome_access=False))
 print('Text-only candidates',len(rows))
if __name__=='__main__':main()
