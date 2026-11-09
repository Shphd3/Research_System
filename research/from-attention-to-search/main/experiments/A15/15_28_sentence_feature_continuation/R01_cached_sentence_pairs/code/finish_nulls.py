import os,subprocess,sys,json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
for name,args in [('SAE_biology',['incidence','SAE','1']),('CC_math',['incidence','CC','0']),('CC_biology',['incidence','CC','1']),('graph',['graph'])]:
 with open(R/'provenance'/f'null_{name}.log','w') as log:
  p=subprocess.run([sys.executable,str(R/'code/run_nulls.py'),*args],stdout=log,stderr=subprocess.STDOUT,env=os.environ)
 if p.returncode:raise SystemExit(f'{name} failed: {p.returncode}')
 print(name,'completed',datetime.now(timezone.utc).isoformat(),flush=True)
(R/'provenance/nulls_completed.json').write_text(json.dumps(dict(time=datetime.now(timezone.utc).isoformat(),status='ALL_5_NULL_JOBS_COMPLETED',draws_each=398)))
