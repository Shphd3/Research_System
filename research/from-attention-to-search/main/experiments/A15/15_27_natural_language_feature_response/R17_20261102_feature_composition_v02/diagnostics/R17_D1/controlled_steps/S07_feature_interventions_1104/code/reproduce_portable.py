from pathlib import Path
import json,math,sys,numpy as np
r=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
base={x['id']:x for x in map(json.loads,open(r/'data/native_baselines.jsonl'))};count=0;maxscore=maxnorm=0.;maxid=0.
for x in map(json.loads,open(r/'results/conditions.jsonl')):
 count+=1;assert len(x['scores'])==len(x['candidate_vocab_ranks'])==4
 assert abs(sum(x['candidate_sequence_prob4'])-1)<1e-12
 v=np.array(x['scores']);q=np.exp(v-v.max());q/=q.sum();assert max(abs(q-x['candidate_sequence_prob4']))<1e-12
 for i in range(4):maxscore=max(maxscore,abs(math.log(x['candidate_vocab_prob'][i])+base[x['text_id']]['period_logp'][i]-x['scores'][i]))
 assert all(1<=k<=151936 for k in x['candidate_vocab_ranks']);assert min(x['new_z'],default=0)>=0
 assert abs(np.linalg.norm(np.array(x['old_z'],dtype=np.float32))-x['old_group_L2'])<1e-10 and abs(np.linalg.norm(x['new_z'])-x['new_group_L2'])<1e-10
 if x['arm'].startswith('strength') and x['arm']!='strength_single':maxnorm=max(maxnorm,abs(x['old_group_L2']-x['new_group_L2']))
 if x['arm']=='identity':maxid=max(maxid,max(abs(np.array(x['scores'])-x['baseline_scores'])))
 assert abs(float(np.float32(1)-np.float32(x['top20_mass']))-x['tail_mass'])<1e-12 and x['KL_new_vs_baseline']> -1e-4
assert maxscore<3e-6 and maxnorm<1e-9 and maxid<1e-4
print(json.dumps(dict(status='PASS',conditions=count,max_complete_score_probability_replay_error=maxscore,max_preserved_group_norm_error=maxnorm,max_identity_score_error=maxid)))
