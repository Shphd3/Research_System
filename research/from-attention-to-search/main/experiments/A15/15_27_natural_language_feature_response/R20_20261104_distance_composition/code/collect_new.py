from common import *
pp=[p for p in rows(R/'data/panel.jsonl') if p['provenance']=='NEW_FORWARD'];col={};constant={};inputs=[]
for p in pp:
 path=R/f'cache/new_rows/{p["id"]}.npz'
 with np.load(path) as a:
  for key in a.files:
   if key.endswith('__decoder_norm'):
    if key in constant:assert np.array_equal(constant[key],a[key])
    else:constant[key]=a[key].copy()
   else:col.setdefault(key,[]).append(a[key].copy())
 inputs.append(dict(id=p['id'],path=str(path),bytes=path.stat().st_size,sha256=sha(path)))
payload={key:np.concatenate(v,axis=0) for key,v in col.items()};payload.update(constant);payload['ids']=np.array([p['id'] for p in pp]);dest=R/'cache/new_all.npz';np.savez_compressed(dest,**payload)
with np.load(dest) as a:
 for key in col:
  for i,v in enumerate(col[key]):assert np.array_equal(a[key][i:i+1],v)
dump(R/'evidence/cache_consolidation.json',dict(UTC=now(),status='PASS',rows=len(pp),file=str(dest),sha256=sha(dest),bytes=dest.stat().st_size,transformation='Every original field/float retained; concatenate row axis, exact repeated decoder_norm arrays deduplicated once; original files remain unchanged.',inputs=inputs))
print('CONSOLIDATED',len(pp),dest.stat().st_size)
