from common import *
from remaining import run
if __name__=='__main__':
 run('cache_forward.py',['--stage','early'],'cache_A0_early_recovery.log')
 run('readability.py',[],'readability.log');run('figures.py',[],'figures.log');run('write_status.py',[],'write_status.log')
 run('student_dictionary.py',[],'student_dictionary.log');run('figures.py',[],'figures.log');run('write_status.py',[],'write_status.log')
 dump(R/'evidence/all_checks_complete.json',dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),judgment='Unknown'))
