"""Posthoc spelling aids for actual token IDs. No linguistic/LM model is called."""
from pathlib import Path
import argparse,csv,json,re,hashlib
import numpy as np
from tokenizers import Tokenizer
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'));a=ap.parse_args();S=a.source
docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];pk=np.load(S/'analysis/position_keys.npz');rows=np.flatnonzero(np.array([docs[d]['split']=='heldout' for d in pk['document_index']]));tk=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');cache={};position_rows=[]
for rr in rows:
    d=int(pk['document_index'][rr]);p=int(pk['position'][rr]);t=int(pk['token_id'][rr]);ids=docs[d]['token_ids']
    if d not in cache:cache[d]=tk.decode(ids,skip_special_tokens=False)
    whole=cache[d];before=tk.decode(ids[:p],skip_special_tokens=False);through=tk.decode(ids[:p+1],skip_special_tokens=False);token=tk.decode([t],skip_special_tokens=False);word='';status=''
    if whole.startswith(before) and whole.startswith(through):
        lo,hi=len(before),len(through);piece=whole[lo:hi];matches=list(re.finditer(r'[A-Za-z0-9]',piece))
        if matches:
            anchor=lo+matches[0].start();left=anchor;right=anchor+1
            while left>0 and re.match(r"[A-Za-z0-9_'-]",whole[left-1]):left-=1
            while right<len(whole) and re.match(r"[A-Za-z0-9_'-]",whole[right]):right+=1
            word=whole[left:right];status='observed_word_spelling_posthoc'
        else:word=repr(piece);status='punctuation_or_whitespace'
    else:word='[byte fragment / unresolved]';status='prefix_byte_boundary_unresolved'
    position_rows.append(dict(global_row=int(rr),seq_id=docs[d]['seq_id'],domain=docs[d]['domain'],position=p,token_id=t,token_string=token,posthoc_word_spelling=word,spelling_status=status,not_available_as_complete_word_at_target=True))
for dirname in ['token_context_audit_20261030','near_single_domain_20261030']:
    O=S/'presentation_variants'/dirname;data=np.load(O/'heldout_position_composition_weights.npz');assert np.array_equal(data['global_rows'],rows);result=[]
    for group in ['math','biology']:
        weights=data[group];agg={}
        for r,w in zip(position_rows,weights):
            if w<=0:continue
            key=(r['token_id'],r['posthoc_word_spelling']);value=agg.setdefault(key,dict(weight=0.,positions=0,docs=set(),status=r['spelling_status']));value['weight']+=float(w);value['positions']+=1;value['docs'].add(r['seq_id'])
        for (token_id,word),v in agg.items():result.append(dict(feature_group=group,token_id=token_id,token_string=tk.decode([token_id],skip_special_tokens=False),posthoc_word_spelling=word,member_equal_high_event_share=v['weight'],distinct_positions=v['positions'],distinct_documents=len(v['docs']),spelling_status=v['status']))
    with (O/'actual_token_word_spellings.csv').open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    print(dirname,'word mappings',len(result))
O=S/'presentation_variants/token_context_audit_20261030'
with (O/'heldout_token_spelling_positions.csv').open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(position_rows[0]));w.writeheader();w.writerows(position_rows)
(O/'word_spelling_provenance.json').write_text(json.dumps({'script':str(Path(__file__).resolve()),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'deterministic decoded-prefix boundaries and contiguous alphanumeric spelling; unresolved bytes/punctuation retained; no model/parser; complete spellings are posthoc readability aids, not activation causes','positions':len(position_rows),'new_model_forwards':0},indent=2)+'\n')
