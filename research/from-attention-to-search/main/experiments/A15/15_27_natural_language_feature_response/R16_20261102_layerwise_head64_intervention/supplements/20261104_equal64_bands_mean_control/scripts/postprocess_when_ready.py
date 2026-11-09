from pathlib import Path
import time,json,subprocess,sys
E=Path(__file__).resolve().parents[1];prev=-1
while True:
 n=len(list((E/'analysis/chunks').glob('*.npz')))
 if n!=prev:print(json.dumps({'completed_documents':n,'timestamp':time.time()}),flush=True);prev=n
 fail=[p for p in (E/'audit').glob('failure_*.json') if p.stat().st_mtime>(E/'freeze.json').stat().st_mtime]
 if fail:raise RuntimeError('GPU failure after current freeze: '+str(fail))
 if n==180 and all((E/f'terminal_rank{i}.json').exists() for i in range(2)):break
 time.sleep(30)
for name in ['analyze.py','casebook.py','render.py']:
 print('CPU_START',name,flush=True)
 with (E/'logs'/f'{name}.log').open('w') as f:subprocess.run([sys.executable,str(E/'scripts'/name)],stdout=f,stderr=subprocess.STDOUT,check=True)
 print('CPU_DONE',name,flush=True)
print('POSTPROCESS_DONE',flush=True)
