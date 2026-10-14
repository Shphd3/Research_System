"""One analysis process tree; preserve durable receipts on failure or resource ceiling."""
import sys,os,time,json,subprocess,signal,traceback
from pathlib import Path
import psutil

def put(path,x):
 p=Path(path);q=p.with_name(p.name+'.tmp');q.write_text(json.dumps(x,indent=2)+'\n');os.replace(q,p)
def main(out):
 out=Path(out);plan=json.loads((out/'execution_record.json').read_text());start=time.monotonic();p=subprocess.Popen([sys.executable,str(out/'code/analyze.py'),str(out)],start_new_session=True);maxrss=0;maxdisk=0;failure=None
 while p.poll() is None:
  try:
   proc=psutil.Process(p.pid);tree=[proc]+proc.children(recursive=True);rss=sum(v.memory_info().rss for v in tree if v.is_running());maxrss=max(maxrss,rss)
   # All generated outputs are under this run. Existing input cache is excluded.
   disk=sum(v.stat().st_size for v in out.rglob('*') if v.is_file());maxdisk=max(maxdisk,disk);elapsed=time.monotonic()-start
   if rss>plan['aggregate_rss_limit_bytes']:failure='AGGREGATE_RSS_LIMIT'
   elif disk>plan['new_disk_limit_bytes']:failure='NEW_DISK_LIMIT'
   elif elapsed>plan['formal_active_seconds_limit']:failure='FORMAL_ACTIVE_LIMIT'
   put(out/'resource_progress.json',{'elapsed_seconds':elapsed,'aggregate_rss_bytes':rss,'peak_aggregate_rss_bytes':maxrss,'new_disk_bytes':disk,'peak_new_disk_bytes':maxdisk,'analysis_pid':p.pid,'state':'RUNNING','failure':failure})
   if failure:os.killpg(p.pid,signal.SIGTERM);break
  except (psutil.NoSuchProcess,ProcessLookupError):pass
  time.sleep(1)
 if failure:
  try:p.wait(timeout=10)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL)
 rc=p.wait();receipt={'status':'COMPUTATION_EXITED' if rc==0 else 'PARTIAL_OR_FAILED','exit_code':rc,'failure':failure,'formal_active_seconds':time.monotonic()-start,'peak_aggregate_rss_bytes_sampled_1s':maxrss,'peak_new_disk_bytes_sampled_1s':maxdisk,'final_new_disk_bytes':sum(v.stat().st_size for v in out.rglob('*') if v.is_file()),'gpu_profile':'h100-4-reserved','cpu_affinity_limit':8,'no_model_inference':True,'no_training':True,'scientific_state':'UNKNOWN_PENDING_RESEARCHER_REVIEW'};put(out/'compute_completion_receipt.json',receipt);print(json.dumps(receipt),flush=True);return rc
if __name__=='__main__':sys.exit(main(sys.argv[1]))
