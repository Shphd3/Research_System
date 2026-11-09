"""Bind derived statistics to input fingerprints before the registered entrypoint reuses them."""
from pathlib import Path
import json,hashlib,os,argparse,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(16*1024*1024),b''):h.update(b)
 return h.hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def context():
 cfg=json.load(open(ROOT/'config.json'));man=json.load(open(ROOT/'manifest.json'));cache=json.load(open(ROOT/'cache_index.json'))
 current_panels={p.name:sha(p) for p in (ROOT/'data').glob('*') if p.is_file()}
 assert current_panels==cfg['panel_sha256'],'PANEL_BYTES_CHANGED_SINCE_FREEZE'
 return dict(checkpoints=[dict(tokens=r['tokens'],state=r['state_sha256'],manifest=r['manifest_sha256']) for r in man['checkpoints']],activation_cache_keys={str(r['tokens']):r['cache_key'] for r in cache},panels=current_panels,config_sha256=sha(ROOT/'config.json'),statistics_code_sha256=sha(ROOT/'scripts/analyze.py'),metrics_code_sha256=sha(ROOT/'scripts/metrics.py'),preprocessing='own reference mean;equal32positions/document;FP64covariance;SO(d)reference-onlyalignment;fixedR12labelsplit',interface='layer7finalresidual-post;layer0/3supplementat0.5/17/33B',guard_version=1)
def validate(expected,saved):
 if digest(expected)!=saved['context_key']:raise ValueError('DERIVED_CACHE_INPUT_IDENTITY_MISMATCH;refuse reuse under anothercheckpoint/text/position/layer/preprocessing')
def write(p,x):
 q=p.with_suffix('.partial');q.write_text(json.dumps(x,indent=2)+'\n');os.replace(q,p)
def execute(qualify=False,seal=False):
 out=ROOT/'analysis/cache_context.json';c=context();existing=list((ROOT/'analysis').rglob('*.npz'))
 if out.exists():
  saved=json.load(open(out));validate(c,saved)
  for path,h in saved.get('sealed_arrays',{}).items():
   assert sha(ROOT/'analysis'/path)==h,('DERIVED_ARRAY_CHANGED',path)
 else:
  if existing and not qualify:raise ValueError('UNQUALIFIED_DERIVED_CACHE:use frozen raw caches or explicitly audit the completed producer first')
  if qualify:
   assert json.load(open(ROOT/'analysis/completion.json'))['amendment_A01']=='COMPLETE_SO(d)_det+1'
   assert json.load(open(ROOT/'audit/final_measurement_consistency.json'))['status']=='PASS'
   assert len(list((ROOT/'analysis/stats').glob('*.npz')))==18
  saved=dict(context_key=digest(c),context=c,initial_binding='qualified completed run, after A01;no numerical values changed' if qualify else 'before first statistical fitting',bound_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),sealed_arrays={})
 if seal or qualify:
  saved['sealed_arrays']={str(p.relative_to(ROOT/'analysis')):sha(p) for p in existing};saved['sealed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 write(out,saved)
 # Negative identity checks are on copies and never mutate real caches.
 bad=json.loads(json.dumps(c));bad['checkpoints'][0]['state']='0'*64
 try:validate(bad,saved)
 except ValueError:pass
 else:raise AssertionError('wrong checkpoint accepted')
 bad=json.loads(json.dumps(c));bad['panels']['geometry.npz']='1'*64
 try:validate(bad,saved)
 except ValueError:pass
 else:raise AssertionError('wrong text/position accepted')
 print('DERIVED_CACHE_IDENTITY_PASS',saved['context_key'],len(saved.get('sealed_arrays',{})),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--qualify-completed',action='store_true');p.add_argument('--seal',action='store_true');a=p.parse_args();execute(a.qualify_completed,a.seal)
