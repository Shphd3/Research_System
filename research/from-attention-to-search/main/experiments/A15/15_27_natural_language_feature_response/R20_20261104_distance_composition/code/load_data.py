from common import *
PANEL=rows(R/'data/panel.jsonl');META={p['id']:p for p in PANEL};CFG=json.load(open(R/'config.json'));MAP=json.load(open(R/'data/condition_mapping.json'));SPEC=json.load(open(R/'data/R19_candidates.json'))['sites']
def load_site(site,include_new=False):
 out={}
 with np.load(R/f'cache/{site}_old_main.npz') as a:
  for i,pid in enumerate(a['ids']):out[str(pid)]={k:a[k][i].astype(float) if a[k].dtype.kind=='f' else a[k][i] for k in a.files if k not in ['ids','decoder_norm']}
  dn=a['decoder_norm'].astype(float)
 if include_new:
  for p in PANEL:
   if p['provenance']!='NEW_FORWARD':continue
   path=R/f'cache/new_rows/{p["id"]}.npz'
   if not path.exists():continue
   with np.load(path) as a:out[p['id']]={key.split('__',1)[1]:a[key][0].astype(float) if a[key].dtype.kind=='f' else a[key][0] for key in a.files if key.startswith(site+'__') and not key.endswith('__decoder_norm')}
 for p in out.values():
  z=np.zeros(30000,float);z[p['indices']]=p['values'];p['z']=z;p['indices']=p['indices'].astype(int);p['cutoff32']=float(p['cutoff32']);p['cutoff33']=float(p['cutoff33']);p['relative_reconstruction_error']=float(p['relative_reconstruction_error'])
 return out,dn
def behavior(include_new=False):
 out={b['id']:b for b in rows(R/'results/behavior_old.jsonl')}
 if include_new:
  for f in (R/'results/new_rows').glob('*.json'):b=json.load(open(f));out[b['id']]=b
 return out
