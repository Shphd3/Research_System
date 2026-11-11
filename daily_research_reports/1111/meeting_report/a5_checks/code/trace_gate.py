from common import *
import pandas as pd
rows=[]
for a in ['A5','A0','A1']:
 p=position(a,2000);d=np.load(p);orig=erows(a)[2000]['lm_loss'];raw=float(d['nll']);mean=float(d['loss'].astype(np.float64).mean());rows.append(dict(arm=a,original_training_eval=orig,cache_unquantized=raw,fp16_position_mean=mean,cache_minus_original=raw-orig,fp16_minus_cache=mean-raw,file=str(p),sha256=sha(p)))
p=R4/'analysis/positions_prior_claude/A1/step002000.npz'
prior={}
if p.exists():
 a=np.load(position('A1',2000));b=np.load(p);prior=dict(path=str(p),nll=float(b['nll']),loss_exact=bool(np.array_equal(a['loss'],b['loss'])),routes_exact=bool(np.array_equal(a['sel'],b['sel'])))
table(pd.DataFrame(rows),'input_gate_trace','源：原训练4rank评估JSONL与MIG复算的FP32完整状态缓存；A5为训练同次捕获。用户明确接受微小偏差后继续，未改R04。')
dump(R/'evidence/gate_accepted.json',dict(rows=rows,prior=prior,user_override='2026-11-10: 先追查一致性，然后核验后继续，不过这个差距很小我认为可以通过，请继续实验处理，推进检验',interpretation='A1差异已存在于R04既有一致性记录；如prior exact为真，确定性重算也复现相同缓存。源头是原四卡训练评估与单MIG重算间的数值差，具体kernel原因未识别；不是本轮fp16量化引入。不校正原数据，不宣称逐位复现。',status='PASS_WITH_USER_ACCEPTED_DEVIATION'))
event('启动门','A1既有MIG复算缓存与原训练评估微差已追溯并单列；按用户明确接受继续，原数据不改。',0)
