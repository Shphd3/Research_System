from pathlib import Path
import json,time,sys,hashlib
E=Path(__file__).resolve().parents[1];sys.path.insert(0,str(E/'scripts'));import analyze as A
for phase,splits in [('PCA_DISCOVERY',['discovery']),('DEVELOPMENT',['development'])]:
 docs=[x for x in A.DOC if x['split'] in splits]
 while True:
  done=sum((E/'cache'/(x['doc_id']+'.npz')).exists() for x in docs)
  if done==len(docs):break
  print('WAIT',phase,done,len(docs),flush=True);time.sleep(20)
 if phase=='PCA_DISCOVERY':
  scripts={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (E/'scripts').glob('*.py')};(E/'audit/analysis_code_before_results.json').write_text(json.dumps({'sha256':scripts,'validation_response_statistics_opened':False,'effective_labels':str(E/'data/labels_effective_v1p1.jsonl')},indent=2)+'\n');A.fit();d,a,r=A.load(['discovery']);A.card_candidates(d,a,r);del a
 else:A.summaries('discovery');A.summaries('development')
print('READY_FOR_DISCOVERY_CONTEXT_REVIEW_AND_SELECTION_FREEZE',flush=True)
