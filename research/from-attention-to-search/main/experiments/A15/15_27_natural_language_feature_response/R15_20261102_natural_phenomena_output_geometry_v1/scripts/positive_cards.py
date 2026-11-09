from pathlib import Path
import json
import numpy as np
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'config.json'));a=np.load(E/'analysis/discovery_arrays.npz');docs=[json.loads(l) for l in (E/'data/documents.jsonl').read_text().splitlines() if json.loads(l)['split']=='discovery'];out=[]
for j,f in enumerate(cfg['candidate_features']):
 v=a['z'][:,j];pos=np.flatnonzero(v>0)
 for level in ['positive_high','positive_middle','positive_low']:
  if not len(pos):out.append({'object':'feature_'+str(f),'level':level,'status':'NOT_FOUND_POSITIVE'});continue
  ordered=pos[np.argsort(-v[pos] if level=='positive_high' else abs(v[pos]-np.median(v[pos])) if level=='positive_middle' else v[pos],kind='stable')];used=set()
  for ix in ordered:
   doc=docs[int(ix)//128]
   if doc['doc_id'] in used:continue
   used.add(doc['doc_id']);out.append({'object':'feature_'+str(f),'level':level,'row':int(a['rows'][ix]),'doc_id':doc['doc_id'],'response':float(v[ix]),'conditioning':'z>0;notall-positionmedian'} )
   if len(used)==3:break
(E/'analysis/discovery_positive_strength_cards.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in out));print('POSITIVE_STRENGTH_CARDS',len(out))
