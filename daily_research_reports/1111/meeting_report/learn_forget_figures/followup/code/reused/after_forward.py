from lf_common import *
import subprocess
start=time.monotonic()
while not (R/'evidence/forward_complete.json').exists():
 if time.monotonic()-start>3600:raise TimeoutError('Forward receipt absent after1h;inspect forward.log')
 time.sleep(10)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4')
with (R/'logs/figure1.log').open('w') as log:p=subprocess.Popen([sys.executable,str(R/'code/figure1.py')],stdout=log,stderr=subprocess.STDOUT,env=env)
with (R/'logs/gradients.log').open('w') as log:rc=subprocess.run([sys.executable,str(R/'code/gradients.py')],stdout=log,stderr=subprocess.STDOUT,env=env).returncode
if rc:event('图2失败','请检查logs/gradients.log',returncode=rc)
ret=p.wait();subprocess.run([sys.executable,str(R/'code/report.py')],env=env,check=True)
dump(R/'evidence/after_forward_terminal.json',dict(figure1_returncode=ret,figure2_returncode=rc))
