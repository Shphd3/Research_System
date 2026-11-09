from common import *
import subprocess,sys
work=[['MLPIN_SAE','discovery','position'],['LOCK'],['ATTN_SAE','heldout','position'],['MLPIN_SAE','heldout','position'],['ATTN_SAE','heldout','position_token3'],['MLPIN_SAE','heldout','position_token3']]
for args in work:
 if args==['LOCK']:
  p=subprocess.run([sys.executable,str(R/'code/lock_directions.py')],check=True);continue
 fn='__'.join(args)
 with (R/'evidence'/f'{fn}.log').open('w') as f:
  p=subprocess.run([sys.executable,'-u',str(R/'code/run_null.py')]+args,stdout=f,stderr=subprocess.STDOUT)
 if p.returncode:
  dump(R/'evidence'/f'{fn}__failure.json',dict(UTC=now(),status='FAILED',returncode=p.returncode));print('FAILED',args,flush=True)
  if args[1]=='discovery':break
 else:print('STAGE_COMPLETE',args,flush=True)
