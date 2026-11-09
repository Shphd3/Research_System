"""Independent recomputation on actual paired cached vectors; no new forwards."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
from pathlib import Path
import json,hashlib,numpy as np
from scipy import linalg
from metrics import stream_cka
ROOT=Path(__file__).resolve().parents[1]
a=json.load(open(ROOT/'smoke_cache_index.json'));x=np.load(Path(a[0]['path'])/'geometry_layer7.npy').reshape(-1,1024).astype('float64');y=np.load(Path(a[-1]['path'])/'geometry_layer7.npy').reshape(-1,1024).astype('float64');x-=x.mean(0);y-=y.mean(0)
c=x.T@x/(len(x)-1);eig=linalg.eigvalsh(c)[::-1];sv=linalg.svdvals(x);err=float(np.linalg.norm(eig[:len(sv)]-sv**2/(len(x)-1))/np.linalg.norm(eig));tail=float(np.linalg.norm(eig[len(sv):])/np.linalg.norm(eig));gx=x@x.T;gy=y@y.T;gram=float(np.sum(gx*gy)/(np.linalg.norm(gx)*np.linalg.norm(gy)));moment=stream_cka(x,y,63)
assert err<1e-8 and tail<1e-8 and abs(gram-moment)<1e-8
f=json.load(open(ROOT/'freeze.json'));changed=[]
for name,h in f['files'].items():
 live=hashlib.sha256(Path(name).read_bytes()).hexdigest()
 if live!=h:
  archived=ROOT/'audit/frozen_sources'/Path(name).name
  assert hashlib.sha256(archived.read_bytes()).hexdigest()==h,('INITIAL_ARCHIVE_MISMATCH',name)
  changed.append(name)
out=dict(status='PASS',actual_smoke_states=[a[0]['tokens'],a[-1]['tokens']],rows=len(x),dimension=1024,covariance_eigenvalue_vs_direct_svd_relative_error=err,numerical_zero_tail_relative_norm=tail,actual_paired_cka_gram=gram,actual_paired_cka_stream=moment,cka_formula_absolute_error=abs(gram-moment),initial_frozen_sources_verified=len(f['files']),authorized_post_start_current_files_differ=changed,new_forwards=0,note='Implementation identity only;smallsmoke spectrum not scientific large-reference estimate. Initial bytes verified from live or archive;current amendments validated by separate source-freeze audit')
(ROOT/'audit/independent_cached_numerics_final.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
