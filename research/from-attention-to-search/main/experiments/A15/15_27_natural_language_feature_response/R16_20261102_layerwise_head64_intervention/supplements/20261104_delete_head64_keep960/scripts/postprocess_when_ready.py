from pathlib import Path
import time,json,subprocess,sys,os
E=Path(__file__).resolve().parents[1];start=time.time();print('Awaiting both complete document shards; bounded20minutes',flush=True)
while not all((E/f'terminal_rank{r}.json').exists() for r in [0,1]):
 failures=list((E/'audit').glob('failure_*.json'))
 if failures:raise RuntimeError('GPU stage failure recorded: '+str(failures))
 if time.time()-start>1200:raise TimeoutError('Shards not complete within postprocessing wait; inspect existing job, do not resubmit')
 time.sleep(5)
for rank in [0,1]:assert json.load(open(E/f'terminal_rank{rank}.json'))['complete']
for step in ['analyze','validate','render','write_report']:
 print('CPU_STAGE',step,flush=True)
 with (E/'logs'/f'{step}.log').open('w') as f:subprocess.run([sys.executable,'-W','ignore',str(E/'scripts'/f'{step}.py')],stdout=f,stderr=subprocess.STDOUT,check=True,cwd=E)
 print('CPU_STAGE_DONE',step,flush=True)
print('POSTPROCESS_COMPLETE_MANUAL_READING_PENDING',flush=True)
