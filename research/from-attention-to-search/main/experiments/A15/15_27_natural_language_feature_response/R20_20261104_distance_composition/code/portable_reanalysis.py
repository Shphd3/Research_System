"""Optional complete offline statistical pipeline in an extracted packet; no model."""
import os,sys,runpy
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
R=Path(__file__).resolve().parents[1]
import common
common.OLD=R/'reference/R19'
runpy.run_path(str(R/'code/unpack_observations.py'),run_name='__main__')
steps=[('analyze.py','baseline'),('analyze.py','controls'),('frequency.py','baseline'),('frequency.py','controls'),('template_sensitivity.py',),('control_summary.py',),('describe.py',),('frequency_roles.py',),('offline_replay.py',)]
for step in steps:
 sys.argv=[str(R/'code'/step[0])]+list(step[1:]);print('OFFLINE STAGE',*step,flush=True);runpy.run_path(sys.argv[0],run_name='__main__')
print('COMPLETE OFFLINE STATISTICAL REANALYSIS; no model/SAE weights, forward,training or intervention.')
