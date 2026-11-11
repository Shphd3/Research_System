from common import *
import os,subprocess

def run(script,args,log):
 env=dict(os.environ,PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python',OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4')
 with (R/'logs'/log).open('a') as f:subprocess.run([sys.executable,str(R/'code'/script)]+args,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
if __name__=='__main__':
 run('cache_forward.py',['--stage','a6'],'cache_A6.log');run('check45.py',['5'],'check5.log');run('write_status.py',[],'write_status.log')
 run('cache_forward.py',['--stage','early'],'cache_A0_early.log');run('readability.py',[],'readability.log');run('figures.py',[],'figures.log');run('write_status.py',[],'write_status.log')
 run('student_dictionary.py',[],'student_dictionary.log');run('figures.py',[],'figures.log');run('write_status.py',[],'write_status.log')
 dump(R/'evidence/all_checks_complete.json',dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),judgment='Unknown'))
