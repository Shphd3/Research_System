"""One approved 4-H100 allocation; gates run here before any formal update."""
from common import *
import subprocess,sys,datetime,traceback

def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def execute(script,args,gpu,log):
 p=ROOT/'logs'/log;p.parent.mkdir(exist_ok=True,parents=True);f=p.open('a');cmd=[sys.executable,str(ROOT/'code'/script),*args,'--device',f'cuda:{gpu}'];f.write('\n'+json.dumps(dict(start=stamp(),command=cmd))+'\n');f.flush();return subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2','MKL_NUM_THREADS':'2','PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION':'python'}),f

def queue(tasks,stage):
 pending=list(tasks);active={};records=[];deadline=datetime.datetime.fromisoformat(CFG['training_deadline_utc']).timestamp()
 while pending or active:
  for gpu in range(4):
   if gpu not in active and pending:
    script,args,tag=pending.pop(0)
    if time.time()>=deadline and (stage.startswith('training') or stage in ['target_background','target_adapt']):
     records.append(dict(task=tag,status='NOT RUN',reason='training window elapsed'));continue
    p,f=execute(script,args,gpu,tag+'.log');active[gpu]=(p,f,tag,time.monotonic());print('START',stage,tag,'GPU',gpu,flush=True)
  for gpu,(p,f,tag,t0) in list(active.items()):
   code=p.poll()
   if code is not None:
    f.close();records.append(dict(task=tag,exit_code=code,status='PROCESS_EXIT_SUCCESS' if code==0 else 'FAILED',seconds=time.monotonic()-t0));del active[gpu];print('FINISH',stage,tag,code,flush=True);write_json(ROOT/'provenance'/f'queue_{stage}.json',records)
  if active:time.sleep(2)
 return records

def main():
 start=time.monotonic();assert torch.cuda.is_available() and torch.cuda.device_count()==4
 names=[torch.cuda.get_device_name(i) for i in range(4)];assert all('H100' in n for n in names)
 write_json(ROOT/'provenance/runtime.json',dict(start=stamp(),gpu_names=names,torch=torch.__version__,cuda=torch.version.cuda,python=sys.version,profile=os.environ.get('RESOURCE_PROFILE'),image=os.environ.get('IMAGE_ID'),cpu_count=os.cpu_count(),cgroup_cpu=Path('/sys/fs/cgroup/cpu.max').read_text() if Path('/sys/fs/cgroup/cpu.max').exists() else None,cgroup_memory=Path('/sys/fs/cgroup/memory.max').read_text() if Path('/sys/fs/cgroup/memory.max').exists() else None,processor='Codex /root, current11109 conversation'))
 if not (ROOT/'provenance/preparation_receipt.json').exists():
  subprocess.run([sys.executable,str(ROOT/'code/prepare.py')],check=True)
 tasks=[]
 if not (ROOT/'smoke/receipt.json').exists():tasks.append(('train.py',['--smoke'],'smoke'))
 if not (ROOT/'provenance/profiles_receipt.json').exists():tasks.append(('profiles.py',[],'profiles'))
 r=queue(tasks,'engineering')
 if not (ROOT/'smoke/receipt.json').exists():write_json(ROOT/'provenance/pipeline_status.json',dict(status='BLOCKED',reason='engineering smoke failed',records=r));return
 smoke=json.load(open(ROOT/'smoke/receipt.json'));assert smoke['status']=='PASS';print('SMOKE_ESTIMATE',json.dumps(smoke),flush=True)
 # Primary whole pairs before references/extensions. Jobs are different runs, no distributed sharding.
 for seed in [11,22]:queue([('train.py',['--name',n,'--seed',str(seed)],n+f'_seed{seed}') for n in ['T_S0','T_S1','R11_S1']],'training_primary'+str(seed))
 queue([('train.py',['--name',n,'--seed',str(s)],n+f'_seed{s}') for n in ['Learned','LearnedLB'] for s in [11,22]],'training_references')
 queue([('train.py',['--name',n,'--seed',str(s)],n+f'_seed{s}') for n in ['T_S2','T_S3','R11_S0','R11_S2','R11_S3'] for s in [11,22]],'training_extensions')
 # Keep target scene ahead of spectra detail. No checkpoint exposed to target labels can stand in for background.
 target=json.load(open(ROOT/'config/target.json'))
 if 'feature_id' in target:
  queue([('train.py',['--name','T_S1','--seed','11','--background'],'target_background')],'target_background')
  if (ROOT/'target/background/complete.json').exists():
   p,f=execute('target.py',['--recommend'],0,'target_recommend.log');code=p.wait();f.close()
   if code==0:queue([('target.py',['--expert',str(e)],f'target_adapt{e}') for e in range(8)],'target_adapt')
 tasks=[('functional.py',['--name',co['id'],'--seed',str(s)],f'probe_{co["id"]}_{s}') for co in CFG['conditions'] for s in [11,22]];queue(tasks,'functional')
 tasks=[('functional.py',['--name',co['id'],'--seed',str(s),'--spectra'],f'spectra_{co["id"]}_{s}') for co in CFG['conditions'] for s in [11,22]];queue(tasks,'spectra')
 write_json(ROOT/'provenance/pipeline_status.json',dict(status='COMPUTATION_PHASE_EXITED',seconds=time.monotonic()-start,completed=stamp(),training_complete=len(list((ROOT/'training').glob('*/seed*/complete.json'))),target_adapt_complete=len(list((ROOT/'target/adapt').glob('expert*/complete.json'))),functional_complete=len(list((ROOT/'functional').glob('*/seed*/complete.json'))),spectra_complete=len(list((ROOT/'functional').glob('*/seed*/spectra_complete.json')))))
if __name__=='__main__':
 try:main()
 except Exception as ex:
  write_json(ROOT/'provenance/pipeline_fatal.json',dict(status='BLOCKED',error=repr(ex),traceback=traceback.format_exc(),utc=stamp()));raise
