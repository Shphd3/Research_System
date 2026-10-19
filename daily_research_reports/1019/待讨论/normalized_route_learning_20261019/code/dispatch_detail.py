from common import *

def run():
 rows=[];group_rows=[];winner_rows=[];expert_rows=[];st=stats();p=st['p'];pool=st['pool'];L=set(st['low'].tolist());H=set(st['high'].tolist());owners=np.load(PREV/'metrics/core/owners.npz')
 for split in ['train','eval']:
  c=loadcache(split);hits=np.bincount(c['feature_ids'].numpy(),minlength=FCOUNT);blocks=c['block_id'].numpy();ptr=c['feature_ptr'].numpy();ids=c['feature_ids'].numpy();z=c['feature_z'].numpy();names=[co['id'] for co in CFG['conditions'] if co['router']=='fixed']
  for co in CFG['conditions']:
   if co['router']=='learned':names.extend(co['id']+f'_seed{s}' for s in CFG['seeds'] if (ROOT/'metrics/exposure'/f'{split}_{co["id"]}_seed{s}.npz').exists())
  for name in names:
   f=ROOT/'metrics/exposure'/f'{split}_{name}.npz'
   if not f.exists():continue
   d=np.load(f);q=d['q'];counts=d['counts'];ne=d['N_e'];owner=d['owner'];route=routes(split,name) if '_seed' not in name else None
   if route is None:
    # End-model TRAIN route isn't saved separately, so context counts not invented.
    if split=='eval':route=np.load(ROOT/f'training/{name.split("_seed")[0]}/seed{name.split("_seed")[1]}/eval_epoch3.npz')['route']
   for i in pool:
    own=int(owner[i]);row=dict(split=split,condition=name,feature_id=int(i),TRAIN_p=p[i],original_split_hits=int(hits[i]),is_low=int(i in L),is_high=int(i in H),owner=own,assigned_reception_a=float(counts[i,own]/hits[i]) if own>=0 and hits[i]>0 else None)
    for e in range(8):row[f'expert{e}_hits']=int(counts[i,e]);row[f'expert{e}_q']=float(q[i,e]) if np.isfinite(q[i,e]) else None;row[f'expert{e}_q_over_TRAIN_p']=float(q[i,e]/p[i]) if p[i]>0 and np.isfinite(q[i,e]) else None
    rows.append(row)
   for e in range(8):expert_rows.append(dict(split=split,condition=name,expert=e,N_e=int(ne[e]),contexts=int(len(np.unique(blocks[route==e]))) if route is not None else None,low_types_seen=int((counts[list(L),e]>0).sum()),reliable_types_seen=int((counts[pool,e]>0).sum()),zero_exposure_types=int((counts[pool,e]==0).sum())))
   if '_seed' in name:continue
   group=name.split('_S')[0]
   for g in range(8):
    sel=np.flatnonzero(owner==g);total=int(hits[sel].sum())
    for e in range(8):group_rows.append(dict(split=split,condition=name,feature_list_group=g,actual_expert=e,feature_hit_events=int(counts[sel,e].sum()),denominator_group_hit_events=total,fraction=float(counts[sel,e].sum()/total) if total else None,unit='feature-hit events; tokens may hit multiple features/groups'))
   # Additional descriptive contribution diagnostic, no strategy selection.
   score=int(name[-1]);winner_ids=[];winning_shares=[]
   for start in range(0,len(hits) if False else len(c['target']),4096):
    stop=min(start+4096,len(c['target']));a,b=ptr[start],ptr[stop];ii=ids[a:b];zz=z[a:b].astype(np.float64);rr=np.repeat(np.arange(stop-start),np.diff(ptr[start:stop+1]));chosen=(owner[ii]==route[start:stop][rr]);ii=ii[chosen];rr=rr[chosen];vv=zz[chosen]*st['weights'][ii]
    if score==2:vv*=st['invm'][ii]
    if score==3:vv*=st['invpm'][ii]
    maxv=np.zeros(stop-start);np.maximum.at(maxv,rr,vv);sums=np.bincount(rr,weights=vv,minlength=stop-start);best=np.full(stop-start,FCOUNT);match=vv==maxv[rr];np.minimum.at(best,rr[match],ii[match]);winner_ids.extend(best.tolist());winning_shares.extend(np.divide(maxv,sums,out=np.zeros_like(maxv),where=sums>0).tolist())
   wi=np.array(winner_ids);valid=wi<FCOUNT;winner_rows.append(dict(split=split,condition=name,N=len(wi),zero_score_winner_N=int((~valid).sum()),winning_largest_contributor_H_fraction=float(np.isin(wi[valid],list(H)).mean()),winning_largest_contributor_L_fraction=float(np.isin(wi[valid],list(L)).mean()),winning_contributor_TRAIN_p_median=float(np.median(p[wi[valid]])),winning_contributor_score_share_median=float(np.median(np.asarray(winning_shares)[valid])),status='posthoc descriptive; winner=largest score term of selected group; no learning selection'))
 csvwrite(ROOT/'tables/routing_before_after.csv',rows);csvwrite(ROOT/'tables/group_to_actual_expert.csv',group_rows);csvwrite(ROOT/'tables/expert_load_contexts.csv',expert_rows);csvwrite(ROOT/'tables/winning_contributor_frequency.csv',winner_rows)
if __name__=='__main__':run()
