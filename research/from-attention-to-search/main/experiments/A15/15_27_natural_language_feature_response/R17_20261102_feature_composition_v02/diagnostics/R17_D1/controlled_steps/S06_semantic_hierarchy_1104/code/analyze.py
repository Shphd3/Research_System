"""Frozen joint-pattern analysis; all fit/selection lives in select.py."""
from common import *
import numpy as np,itertools,math
from scipy import sparse
rng=np.random.default_rng(20261104);pp=rows(R/'data/panel.jsonl');ix={p['id']:i for i,p in enumerate(pp)};lookup={(p['family'],p['wording'],p['label']):i for i,p in enumerate(pp)}
sel=json.load(open(R/'results/selection.json'));assert sha(R/'results/selection.json')==json.load(open(R/'evidence/candidates_frozen.json'))['selection_sha256']
sources=[np.load(R/f'cache/{s}.npz') for s in ['discovery','remaining']];data={}
for s in SITES:
 data[s]={}
 for key in ['h','z','pre','topk_indices','cutoff32','cutoff33','reconstruction_relative_L2']:
  v=sources[0][s+'__'+key];a=np.empty((len(pp),)+v.shape[1:],dtype=v.dtype)
  for src in sources:
   vv=src[s+'__'+key]
   for j,id in enumerate(src['ids']):a[ix[str(id)]]=vv[j]
  data[s][key]=a
 data[s]['decoder_norm']=sources[0][s+'__decoder_norm'];sparse.save_npz(R/f'data/{s}_all_z_csr.npz',sparse.csr_matrix(data[s]['z']))
def cos(a,b):
 n=np.linalg.norm(a)*np.linalg.norm(b);return None if n<1e-12 else float(a@b/n)
def interval(v):
 v=np.array([a for a in v if a is not None],float)
 if not len(v):return [None,None]
 bt=v[rng.integers(len(v),size=(4096,len(v)))].mean(1);return [float(x) for x in np.quantile(bt,[.025,.975])]
def normrows(x):
 n=np.linalg.norm(x,axis=-1,keepdims=True);return np.divide(x,n,out=np.zeros_like(x),where=n>0)
def signp(v):
 v=np.array(v,float)
 if not len(v):return 1.
 signs=np.array(list(itertools.product([-1,1],repeat=len(v))));return float(np.mean((signs@v/len(v))>=v.mean()-1e-12))
overlaps=[];triples=[];rawvalues=[];metrics=[];candidatevals=[];coverage=[];joint=[];decomp=[];ranks=[];nulls=[];wordcontrols=[];geometry=[];oldvals=[];randomcoverage=[];randomjoint=[];preevents=[];pairings=[];casechoices=[];scale=[]
for s in SITES:
 z=data[s]['z'].astype(float);b=z>0;pre=data[s]['pre'];dn=data[s]['decoder_norm'];norm=np.linalg.norm(z,axis=1);width=z.shape[1]
 for i,p in enumerate(pp):
  metrics.append(dict(site=s,id=p['id'],family=p['family'],split=p['split'],wording=p['wording'],label=p['label'],active=int(b[i].sum()),L1=float(z[i].sum()),L2=float(norm[i]),reconstruction_relative_L2=float(data[s]['reconstruction_relative_L2'][i]),positive_pre_not_selected=int(((pre[i]>0)&~b[i]).sum()),cutoff32=float(data[s]['cutoff32'][i]),cutoff33=float(data[s]['cutoff33'][i]),target_position=p['target_index_zero_based']))
  for a in np.flatnonzero(b[i]):rawvalues.append(dict(site=s,id=p['id'],family=p['family'],split=p['split'],wording=p['wording'],label=p['label'],feature_id=int(a),z=float(z[i,a]),preactivation=float(pre[i,a]),decoder_norm=float(dn[a]),u=float(z[i,a]*dn[a])))
 # All semantic pairings with matched frame and wording, preserving numerator/denominator/IDs.
 for family in [f'F{i:02d}' for i in range(1,17)]:
  for w in ['explicit','synonym','property']:
   for a,c in itertools.combinations(['animal','cat','dog','vehicle','car','bicycle','chair','stone'],2):
    i,j=lookup[(family,w,a)],lookup[(family,w,c)];inter=b[i]&b[j];union=b[i]|b[j];adom=pp[i]['domain'];cd=pp[j]['domain'];rel='within' if adom==cd and adom!='negative' else 'negative' if 'negative' in [adom,cd] else 'cross'
    overlaps.append(dict(site=s,family=family,split=pp[i]['split'],wording=w,a=a,b=c,relation=rel,intersection=int(inter.sum()),union=int(union.sum()),Jaccard=float(inter.sum()/union.sum()),intersection_over_a=float(inter.sum()/b[i].sum()),a_members=int(b[i].sum()),b_members=int(b[j].sum()),recruited=int((~b[i]&b[j]).sum()),lost=int((b[i]&~b[j]).sum()),shared_ids=json.dumps(np.flatnonzero(inter).tolist()),recruited_ids=json.dumps(np.flatnonzero(~b[i]&b[j]).tolist()),lost_ids=json.dumps(np.flatnonzero(b[i]&~b[j]).tolist())))
 # Discovery frequency baselines, independent sparse supports with identical k.
 freq=np.array(sel['sites'][s]['animal']['discovery_frequency_counts'],float);prob=(freq+.5)/(freq+.5).sum()
 for kind,weights in [('uniform',None),('frequency_weighted',prob)]:
  for rep in range(512):
   a=rng.choice(width,32,replace=False,p=weights);c=rng.choice(width,32,replace=False,p=weights);n=len(set(a)&set(c));nulls.append(dict(site=s,baseline=kind,rep=rep,intersection=n,union=64-n,Jaccard=n/(64-n),support_each=32,frequency_denominator=64))
 for d,labels in DOMAINS.items():
  ss=sel['sites'][s][d];Cids=ss['H2'];common=ss['common'];dirs=ss['directions'];fixedlists={'H1_common':common,'H2':Cids,**ss['events']}
  # Freeze-matched random lists solely against discovery active counts, no result-matching.
  randomsets={}
  for listname,ids in fixedlists.items():
   sets=[]
   for rep in range(256):
    chosen=[]
    for a in ids:
     pool=np.flatnonzero(abs(freq-freq[a])<=2);pool=np.setdiff1d(pool,np.array(ids+chosen,dtype=int));
     if not len(pool):break
     chosen.append(int(rng.choice(pool)))
    if len(chosen)==len(ids) and len(ids):sets.append(chosen)
   randomsets[listname]=sets
   randomcoverage.append(dict(site=s,domain=d,list=listname,wording='ALL',split='MATCH_AUDIT',observed=None,random_mean=None,random_p025=None,random_p975=None,valid_matches=len(sets),requested_matches=256,members=len(ids)))
  selected=sorted(set(a for v in fixedlists.values() for a in v))
  # Portable complete selected preactivation submatrix includes zero/non-selected states.
  np.savez_compressed(R/f'data/{s}_{d}_selected_pre.npz',ids=np.array([p['id'] for p in pp]),feature_ids=np.array(selected),pre=pre[:,selected],z=z[:,selected],decoder_norm=dn[selected])
  for family in [f'F{i:02d}' for i in range(1,17)]:
   for w in ['explicit','synonym','property']:
    ii=[lookup[(family,w,c)] for c in labels];x=z[ii];bb=x>0;split=pp[ii[0]]['split'];tr=bb.all(0);u=bb.any(0)
    triples.append(dict(site=s,domain=d,family=family,split=split,wording=w,triple_common=int(tr.sum()),triple_union=int(u.sum()),common_over_parent=float(tr.sum()/bb[0].sum()),triple_Jaccard=float(tr.sum()/u.sum()),common_ids=json.dumps(np.flatnonzero(tr).tolist())))
    for ln,ids in fixedlists.items():
     xx=x[:,ids];nn=np.linalg.norm(xx,axis=1);qq=normrows(xx);uu=xx*dn[ids];uq=normrows(uu)
     for k,c in enumerate(labels):
      for j,a in enumerate(ids):candidatevals.append(dict(site=s,domain=d,list=ln,id=pp[ii[k]]['id'],family=family,split=split,wording=w,label=c,feature_id=a,z=float(xx[k,j]),active=bool(xx[k,j]>0),preactivation=float(pre[ii[k],a]),cutoff32=float(data[s]['cutoff32'][ii[k]]),decoder_norm=float(dn[a]),u=float(uu[k,j]),fixed_list_L2=float(nn[k]),full_L2=float(norm[ii[k]]),q=None if nn[k]==0 else float(qq[k,j]),q_weighted=None if not np.linalg.norm(uu[k]) else float(uq[k,j])))
     for a in ids:
      ev=bool(bb[:,a].all()) if ln in ['H1_common','H2'] else bool((x[0,a]==0 and x[labels.index(ln.split('_')[0]),a]>0) if ln.endswith('recruit') else (x[0,a]>0 and x[labels.index(ln.split('_')[0]),a]==0))
      coverage.append(dict(site=s,domain=d,list=ln,feature_id=a,family=family,split=split,wording=w,event=ev))
    q=normrows(x[:,Cids]);qn=np.linalg.norm(x[:,Cids],axis=1);uq=normrows(x[:,Cids]*dn[Cids]);fullq=normrows(x)
    for a,c in [(0,1),(0,2),(1,2)]:
     key=labels[a]+'->'+labels[c];direction=np.array(dirs[key]['unit']);delta=q[c]-q[a];same=bool(np.array_equal(bb[a,Cids],bb[c,Cids]));positive=int((bb[a,Cids]&bb[c,Cids]).sum());eligible=same and positive>=2 and dirs[key]['norm']>1e-12
     mask=bb[a]&bb[c];dynamic=np.flatnonzero(mask);dq=normrows(x[[a,c]][:,dynamic]);dynlen=float(np.linalg.norm(dq[1]-dq[0]));dd=x[c]-x[a];den=float(dd@dd)
     joint.append(dict(site=s,domain=d,family=family,split=split,wording=w,pair=key,members=len(Cids),common_positive=positive,same_fixed_list_support=same,eligible=eligible,projection=float(delta@direction),weighted_projection=float((uq[c]-uq[a])@direction),delta_q_L2=float(np.linalg.norm(delta)),raw_fixed_L2_a=float(qn[a]),raw_fixed_L2_b=float(qn[c]),full_L2_a=float(norm[ii[a]]),full_L2_b=float(norm[ii[c]]),full_support_same=bool(np.array_equal(bb[a],bb[c])),dynamic_common_count=len(dynamic),dynamic_common_delta_q_L2=dynlen,delta_q=json.dumps(delta.tolist()),fixed_ids=json.dumps(Cids)))
     for part,m in [('retained_amplitude',mask),('recruited',~bb[a]&bb[c]),('lost',bb[a]&~bb[c])]:
      energy=float(dd[m]@dd[m]);decomp.append(dict(site=s,domain=d,family=family,split=split,wording=w,pair=key,part=part,members=int(m.sum()),squared_norm=energy,total_squared_norm=den,share=None if den==0 else energy/den))
      for at in np.flatnonzero(m):preevents.append(dict(site=s,domain=d,family=family,split=split,wording=w,pair=key,part=part,feature_id=int(at),a_z=float(x[a,at]),b_z=float(x[c,at]),a_pre=float(pre[ii[a],at]),b_pre=float(pre[ii[c],at]),a_cutoff=float(data[s]['cutoff32'][ii[a]]),b_cutoff=float(data[s]['cutoff32'][ii[c]]),a_zero_positive_pre=bool(x[a,at]==0 and pre[ii[a],at]>0),b_zero_positive_pre=bool(x[c,at]==0 and pre[ii[c],at]>0)))
    for pair in ss['rank_pairs']:
     a,c=pair['a'],pair['b'];aa=Cids.index(a);cc=Cids.index(c);dr=float((q[2,cc]-q[2,aa])-(q[1,cc]-q[1,aa]));ranks.append(dict(site=s,domain=d,family=family,split=split,wording=w,feature_a=a,feature_b=c,child1_order=float(q[1,cc]-q[1,aa]),child2_order=float(q[2,cc]-q[2,aa]),difference=dr,discovery_direction=pair['effect'],same_sign=dr*pair['effect']>0))
    # Shared-parent geometric null: enumerate all6 within-frame role permutations.
    observed=cos(x[1]-x[0],x[2]-x[0]);perms=[]
    for a,c,e in itertools.permutations(range(3)):perms.append(cos(x[c]-x[a],x[e]-x[a]))
    vals=[v for v in perms if v is not None];geometry.append(dict(site=s,domain=d,family=family,split=split,wording=w,shared_parent_cosine=observed,structural_role_null_mean=float(np.mean(vals)) if vals else None,structural_role_null_min=min(vals) if vals else None,structural_role_null_max=max(vals) if vals else None,actual_role_at_least_null_fraction=float(np.mean(np.array(vals)>=observed-1e-12)) if observed is not None else None,structural_permutations=6))
  for w in ['explicit','synonym','property']:
   for split in ['discovery','heldout']:
    fam=[f'F{i:02d}' for i in (range(1,9) if split=='discovery' else range(9,17))]
    # Coverage matched random references apply untouched to heldout and wording controls.
    for ln,ids in fixedlists.items():
     def cover(atoms):
      vv=[]
      for f in fam:
       x=z[[lookup[(f,w,c)] for c in labels]][:,atoms]
       if ln in ['H1_common','H2']:v=(x>0).all(0)
       else:
        child=labels.index(ln.split('_')[0]);v=(x[0]==0)&(x[child]>0) if ln.endswith('recruit') else (x[0]>0)&(x[child]==0)
       vv.extend(v.tolist())
      return float(np.mean(vv)) if vv else None
     obs=cover(ids);rv=[cover(at) for at in randomsets[ln]]
     randomcoverage.append(dict(site=s,domain=d,list=ln,wording=w,split=split,observed=obs,random_mean=float(np.mean(rv)) if rv else None,random_p025=float(np.quantile(rv,.025)) if rv else None,random_p975=float(np.quantile(rv,.975)) if rv else None,valid_matches=len(rv),requested_matches=256,members=len(ids)))
    # Paired family mismatch baseline for fixed-list sibling difference alignment.
    direction=np.array(dirs[labels[1]+'->'+labels[2]]['unit']);vals=[]
    for f in fam:
     x=z[[lookup[(f,w,c)] for c in labels]][:,Cids];q=normrows(x);vals.append(q)
    for k,f in enumerate(fam):
     i2=(k+1)%len(fam);a=vals[k];c=vals[i2];pairings.append(dict(site=s,domain=d,family=f,other_family=fam[i2],split=split,wording=w,matched_projection=float((a[2]-a[1])@direction),mismatched_projection=float((c[2]-a[1])@direction)))
    # Random-list direction fit uses discovery only, identical statistical operations; descriptive benchmark.
    for rep,ids in enumerate(randomsets['H2']):
     disc=[]
     for f in [f'F{i:02d}' for i in range(1,9)]:
      x=z[[lookup[(f,'explicit',c)] for c in labels]][:,ids];qq=normrows(x);disc.append(qq[2]-qq[1])
     dr=np.mean(disc,0);dr=dr/np.linalg.norm(dr) if np.linalg.norm(dr)>1e-12 else dr;vv=[];eligible=0
     for f in fam:
      x=z[[lookup[(f,w,c)] for c in labels]][:,ids];qq=normrows(x)
      if np.array_equal(x[1]>0,x[2]>0) and ((x[1]>0)&(x[2]>0)).sum()>=2:vv.append(float((qq[2]-qq[1])@dr));eligible+=1
     randomjoint.append(dict(site=s,domain=d,split=split,wording=w,rep=rep,eligible=eligible,mean_projection=float(np.mean(vv)) if vv else None,members=len(ids)))
  # Whole support lexical vs semantic distance, every family/control kept.
  for f in [f'F{i:02d}' for i in range(1,17)]:
   for label in labels:
    a=lookup[(f,'explicit',label)]
    for w in ['synonym','property']:
     c=lookup[(f,w,label)];inter=int((b[a]&b[c]).sum());uni=int((b[a]|b[c]).sum());wordcontrols.append(dict(site=s,domain=d,family=f,split=pp[a]['split'],label=label,to_wording=w,intersection=inter,union=uni,Jaccard=inter/uni,explicit_L2=float(norm[a]),control_L2=float(norm[c])))
  jj=[r for r in joint if r['site']==s and r['domain']==d and r['split']=='heldout' and r['wording']=='explicit' and r['pair']==labels[1]+'->'+labels[2]]
  neg=next((r for r in jj if r['projection']<=0),None);chosen=neg or min(jj,key=lambda r:r['projection']);casechoices.append(dict(site=s,domain=d,preselected_case='F09',counter_family=chosen['family'],projection=chosen['projection'],rule='first_nonpositive' if neg else 'no_nonpositive_case;least_positive'))
 # Old S03 candidate list stays old: report on new samples without selection changes.
 old=json.load(open(R/'data/S03_frozen_selection.json'))['sites'][s]
 for ln,ids in old.items():
  if not isinstance(ids,list):continue
  if not all(isinstance(a,int) for a in ids):continue
  for i,p in enumerate(pp):
   if p['domain']!='animal':continue
   for a in ids:oldvals.append(dict(site=s,old_list=ln,id=p['id'],family=p['family'],split=p['split'],wording=p['wording'],label=p['label'],feature_id=a,z=float(z[i,a]),preactivation=float(pre[i,a]),active=bool(z[i,a]>0)))
 scale.append(dict(site=s,decoder_norm_min=float(dn.min()),decoder_norm_max=float(dn.max()),max_abs_norm_minus1=float(abs(dn-1).max()),max_q_projection_weighting_difference=max(abs(r['projection']-r['weighted_projection']) for r in joint if r['site']==s)))
 print('ANALYZED',s,flush=True)

# Primary and control family statistics.
primary=[];family_effects=[];hypothesis=[]
for s in SITES:
 z=data[s]['z'].astype(float);b=z>0
 for d,labels in DOMAINS.items():
  for w in ['explicit','synonym','property']:
   for split in ['discovery','heldout']:
    fs=[f'F{i:02d}' for i in (range(1,9) if split=='discovery' else range(9,17))];within=[];cross=[];contrasts=[];matrices=[]
    for f in fs:
     rr=[r for r in overlaps if r['site']==s and r['family']==f and r['wording']==w];vv=[r['Jaccard'] for r in rr if r['a'] in labels and r['b'] in labels];cc=[r['Jaccard'] for r in rr if r['relation']=='cross'];a=float(np.mean(vv));c=float(np.mean(cc));within.append(a);cross.append(c);contrasts.append(a-c)
     labs=labels+DOMAINS[next(e for e in DOMAINS if e!=d)];x=b[[lookup[(f,w,l)] for l in labs]].astype(int);inter=x@x.T;J=inter/(x.sum(1)[:,None]+x.sum(1)[None,:]-inter);matrices.append(J)
     family_effects.append(dict(site=s,domain=d,hypothesis='H1',family=f,split=split,wording=w,estimate=a-c,eligible=True,within=a,cross=c))
    obs=float(np.mean(contrasts));mc=[]
    for rep in range(4095):
     v=[]
     for J in matrices:
      perm=rng.permutation(6);aa=perm[:3];cc=perm[3:];v.append(float(np.mean([J[aa[j],aa[k]] for j,k in [(0,1),(0,2),(1,2)]])-J[np.ix_(aa,cc)].mean()))
     mc.append(float(np.mean(v)))
    p=(1+int(np.sum(np.array(mc)>=obs-1e-12)))/4096;lo,hi=interval(contrasts)
    rec=dict(site=s,domain=d,hypothesis='H1',wording=w,split=split,estimate=obs,ci_low=lo,ci_high=hi,p=p,eligible=8,N=8,mean_within=float(np.mean(within)),mean_cross=float(np.mean(cross)),null_mean=float(np.mean(mc)),p_holm=None)
    hypothesis.append(rec)
    if w=='explicit' and split=='heldout':primary.append(rec)
    key=labels[1]+'->'+labels[2];jj=[r for r in joint if r['site']==s and r['domain']==d and r['wording']==w and r['split']==split and r['pair']==key];vv=[r['projection'] for r in jj if r['eligible']]
    for r in jj:family_effects.append(dict(site=s,domain=d,hypothesis='H2',family=r['family'],split=split,wording=w,estimate=r['projection'],eligible=r['eligible'],within=None,cross=None))
    lo,hi=interval(vv);h=dict(site=s,domain=d,hypothesis='H2',wording=w,split=split,estimate=float(np.mean(vv)) if vv else None,ci_low=lo,ci_high=hi,p=signp(vv),eligible=len(vv),N=8,mean_within=None,mean_cross=None,null_mean=0.,p_holm=None);hypothesis.append(h)
    if w=='explicit' and split=='heldout':primary.append(h)
primary.sort(key=lambda r:r['p']);running=0.
for rank,r in enumerate(primary):running=max(running,min(1.,r['p']*(len(primary)-rank)));r['p_holm']=running
behavior=rows(R/'results/behavior_discovery.jsonl')+rows(R/'results/behavior_remaining.jsonl');beh=[]
for split,w,d in itertools.product(['discovery','heldout'],['explicit','synonym','property'],DOMAINS):
 for label in DOMAINS[d]:
  rr=[r for r in behavior if r['split']==split and r['wording']==w and r['label']==label];fine=label not in DOMAINS
  beh.append(dict(split=split,wording=w,domain=d,label=label,N=len(rr),sibling_correct=sum(r['sibling_correct'] is True for r in rr) if fine else None,four_correct=sum(r['correct4'] is True for r in rr) if fine else None,sibling_accuracy=sum(r['sibling_correct'] is True for r in rr)/len(rr) if fine else None,preference_counts=json.dumps({c:sum(r['choice4']==c for r in rr) for c in ['cat','dog','car','bicycle']})))
verdict=[]
for s,d,h in itertools.product(SITES,DOMAINS,['H1','H2']):
 rr=[r for r in hypothesis if r['site']==s and r['domain']==d and r['hypothesis']==h and r['split']=='heldout'];ex=next(r for r in rr if r['wording']=='explicit')
 def adequate(w):return all(next(r for r in beh if r['split']=='heldout' and r['wording']==w and r['label']==l)['sibling_accuracy']>=.75 for l in DOMAINS[d][1:])
 enough=ex['eligible']>=6;local=bool(enough and adequate('explicit') and ex['estimate'] is not None and ex['ci_low']>0 and ex['p_holm']<=.05)
 ctrlok=all(r['eligible']>=6 and r['estimate'] is not None and r['ci_low']>0 and adequate(r['wording']) for r in rr)
 vs='LOCAL_SUPPORT' if local else 'INSUFFICIENT' if not(enough and adequate('explicit')) or ex['ci_low'] is None or ex['ci_low']<=0<=ex['ci_high'] else 'NOT_SUPPORTED'
 broad='SUPPORT_IN_THIS_PANEL' if local and ctrlok else 'INSUFFICIENT' if any(r['eligible']<6 or not adequate(r['wording']) for r in rr) else 'NOT_SUPPORTED'
 verdict.append(dict(site=s,domain=d,hypothesis=h,explicit_status=vs,cross_wording_status=broad,explicit_behavior_adequate=adequate('explicit'),synonym_behavior_adequate=adequate('synonym'),property_behavior_adequate=adequate('property'),scientific_acceptance='Unknown'))

for name,rr in dict(overlaps=overlaps,triple_members=triples,active_values=rawvalues,row_metrics=metrics,candidate_values=candidatevals,candidate_coverage=coverage,joint_patterns=joint,difference_decomposition=decomp,rank_pairs=ranks,support_random_baselines=nulls,wording_controls=wordcontrols,shared_parent_geometry=geometry,old_S03_candidates=oldvals,matched_candidate_baselines=randomcoverage,matched_joint_baselines=randomjoint,preactivation_events=preevents,family_pairing_controls=pairings,family_effects=family_effects,hypothesis_statistics=hypothesis,behavior_summary=beh,verdict=verdict).items():table(R/f'results/{name}.csv',rr)
dump(R/'results/primary.json',primary);dump(R/'results/verdict.json',verdict);dump(R/'results/case_selection.json',casechoices);dump(R/'results/scale_sensitivity.json',scale)
jsonl(R/'data/behavior_all.jsonl',sorted(behavior,key=lambda x:ix[x['id']]))
dump(R/'evidence/analysis_complete.json',dict(UTC=now(),rows=len(pp),primary_tests=len(primary),code_sha256=sha(__file__),selection_sha256=sha(R/'results/selection.json'),preevent_rows=len(preevents),old_candidates_reselected=False,fit_on_holdout=0,training=0))
print('PRIMARY',json.dumps(primary),flush=True);print('VERDICT',json.dumps(verdict),flush=True)
