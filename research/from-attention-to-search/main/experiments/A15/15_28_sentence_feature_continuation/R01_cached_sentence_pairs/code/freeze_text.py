from prepare_sentence_pairs import *
from datetime import datetime, timezone
from collections import Counter
rows=json.loads((R/'data/sentence_candidates.json').read_text()); docs=json.loads((R/'data/documents.json').read_text())
# Text-only review by Codex /root, before any pair outcomes. Explicit repairs.
exclude={17,20,40,41,42,49,50,53,*range(92,102),133,140,141,173,204,205,207,208,209,247,260,284,347,355,361,362,*range(363,368),395,396,398,475,601,681,696,697,774,775,777}
merge={51:52,253:254,324:325,327:328,614:615}
consumed=set(merge.values())
tails={1:'Euclidean geometry',32:'The Indian genius',44:'This supplement',45:'Here are twenty',123:'• The intersection',134:'In geometric topology',146:'• The one-point',166:'In a topological',169:'A closed set',174:'"The impact',184:'Let A',185:'Then the difference',186:'More generally',221:'First,',224:'The definition',249:'The formula',268:'Deciding',270:'To begin',283:'Spatial vectors',333:'(1)',523:'For animals',526:'For algae',559:'The study',570:'Different cells',594:'Trilobites have',637:'The free-living',663:"Giant pandas",686:'Some body sites',702:'The point',755:'It is harmful',785:'The buffer'}
# These complete paragraphs have unambiguous within-prefix ends and starts.
whole={106,426,433,445,496,557,608}
manifest=[];review=[]
for r in rows:
 sid=r['sid'];d=docs[r['doc']];a,b=r['start'],r['end'];reason='accepted_complete_text_review'
 if sid in consumed: review.append(dict(candidate=sid,status='MERGED',reason='abbreviation_or_ellipsis',into=next(k for k,v in merge.items() if v==sid)));continue
 if sid in exclude:review.append(dict(candidate=sid,status='EXCLUDED',reason='list_label_caption_bibliography_formula_fragment_or_broken_sentence'));continue
 if sid in merge:b=rows[merge[sid]]['end'];reason='merged_abbreviation_or_ellipsis'
 elif sid in tails:a+=r['text'].index(tails[sid]);reason='heading_or_intro_removed_at_verified_text_boundary'
 elif r['auto_reason']!='candidate' and sid not in whole:
  review.append(dict(candidate=sid,status='EXCLUDED',reason=r['auto_reason']));continue
 text=d['prefix'][a:b]
 # Citation-attached sentence punctuation does not join consecutive sentences.
 splits=[m.end() for m in re.finditer(r'\.(?:\[[^\]\n]+\])+(?=\s+[A-Z])',text)]
 for needle in ['X. The concept','n. The result','X. One can','X. Let','n. Each packet']:
  if needle in text:splits.append(text.index(needle)+2)
 cuts=[0]+sorted(set(splits))+[len(text)]
 accepted=[]
 for x,y in zip(cuts,cuts[1:]):
  aa=a+x;bb=a+y
  while aa<bb and d['prefix'][aa].isspace():aa+=1
  if aa==bb:continue
  tx=d['prefix'][aa:bb]
  # Drop headed blocks from approved multi-sentence candidates; retain following clear prose only.
  if '[edit]' in tx:
   pp=tx.rfind('\n\n');aa+=pp+2;tx=d['prefix'][aa:bb]
  ids=[j for j,(s,e) in enumerate(d['token_offsets']) if e>aa and s<bb and not d['prefix'][s:e].isspace()]
  if not ids:continue
  positions=list(range(min(ids),max(ids)+1))
  out=dict(sid=len(manifest),candidate=sid,doc=r['doc'],seq_id=r['seq_id'],domain=r['domain'],start=aa,end=bb,positions=positions,text=tx,review=reason,complete=True)
  manifest.append(out);accepted.append(out['sid'])
 review.append(dict(candidate=sid,status='ACCEPTED_OR_REPAIRED',reason=reason,sentences=accepted))
# Token overlap can arise when a BPE token straddles a sentence boundary: exclude that boundary token from both.
counts=Counter((r['doc'],p) for r in manifest for p in r['positions']); overlap=[x for x,n in counts.items() if n>1]
for r in manifest:r['positions']=[p for p in r['positions'] if counts[(r['doc'],p)]==1]
assert all(r['positions'] for r in manifest)
(R/'data/sentence_manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in manifest))
dump(R/'data/text_review_decisions.json',review)
dump(R/'provenance/text_freeze.json',dict(timestamp=datetime.now(timezone.utc).isoformat(),processing_agent='Codex /root',model='unknown',candidates=len(rows),accepted_sentences=len(manifest),documents=len(set(r['doc'] for r in manifest)),by_domain=dict(Counter(r['domain'] for r in manifest)),review_counts=dict(Counter(r['status'] for r in review)),boundary_token_exclusions=overlap,manifest_sha256=sha(R/'data/sentence_manifest.jsonl'),decisions_sha256=sha(R/'data/text_review_decisions.json'),pair_outcomes_opened=False,boundary='First excerpt sentences without certified source start excluded, even when grammatical; ambiguous paragraph/formula/list fragments excluded. This restricts population, not proof of incomplete original sentences.'))
print((R/'provenance/text_freeze.json').read_text())
