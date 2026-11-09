from load_data import *
from stats import *
import pandas as pd,sys,math
stage=sys.argv[1] if len(sys.argv)>1 else 'baseline';assert stage in ['baseline','controls'];frames=['baseline'] if stage=='baseline' else ['reverse','content','fixed_e','pos64'];pairrows=[];memberrows=[];factrows=[];contrastrows=[];supportrows=[];rawmembers=[]
for site in SITES:
 data,dn=load_site(site,stage=='controls');freq=pd.read_csv(R/f'data/{site}_reference_frequency.csv');groups=freq['group'].to_numpy();Cids=SPEC[site]['C']
 for frame in frames:
  for fam,dd in MAP[frame].items():
   needed=[dd[str(d)][g] for d in DISTS for g in 'AB']
   if any(pid not in data for pid in needed):continue
   split=META[needed[0]]['split'];template=META[needed[0]]['template']
   for g in 'AB':
    for lo,hi in PAIRS:
     lid=dd[str(lo)][g];rid=dd[str(hi)][g];l=data[lid];r=data[rid];x=l['z'];y=r['z'];sx=set(l['indices']);sy=set(r['indices']);common=sorted(sx&sy);enter=sorted(sy-sx);exit=sorted(sx-sy);union=sorted(sx|sy);delta=y-x;nl=np.linalg.norm(x);nr=np.linalg.norm(y);cl=np.linalg.norm(x[common]);cr=np.linalg.norm(y[common]);ql=x/nl;qr=y/nr;rp=dict(site=site,frame=frame,split=split,family=fam,template=template,gold=g,distance_left=lo,distance_right=hi,left_id=lid,right_id=rid,shared=len(common),entered=len(enter),exited=len(exit),retention=len(common)/32,Jaccard=len(common)/len(union),full_norm_left=float(nl),full_norm_right=float(nr),log_full_norm_ratio=float(np.log(nr/nl)),cosine_full=cosine(x,y),common_norm_left=float(cl),common_norm_right=float(cr),log_common_norm_ratio=float(np.log(cr/cl)) if cl>0 and cr>0 else None,cosine_common=cosine(x[common],y[common]),unit_full_change=float(np.linalg.norm(qr-ql)),raw_L1_change=float(np.sum(abs(delta))),raw_coordinate_sq_change=float(delta@delta),common_coordinate_sq_change=float(np.sum(delta[common]**2)),entered_coordinate_sq_change=float(np.sum(y[enter]**2)),exited_coordinate_sq_change=float(np.sum(x[exit]**2)))
     assert abs(rp['raw_coordinate_sq_change']-sum(rp[k] for k in ['common_coordinate_sq_change','entered_coordinate_sq_change','exited_coordinate_sq_change']))<1e-8
     pairrows.append(rp);rawmembers.append(dict(**{k:rp[k] for k in ['site','frame','split','family','gold','distance_left','distance_right','left_id','right_id']},shared_ids=list(map(int,common)),entered_ids=list(map(int,enter)),exited_ids=list(map(int,exit))))
     lr={int(f):i+1 for i,f in enumerate(np.argsort(-x,kind='stable')[:32])};rr={int(f):i+1 for i,f in enumerate(np.argsort(-y,kind='stable')[:32])}
     for atom in union:
      status='common' if atom in sx and atom in sy else 'entered' if atom in sy else 'exited';active_value=x[atom] if status=='exited' else y[atom];active_cut=l['cutoff32'] if status=='exited' else r['cutoff32'];active_rank=lr[atom] if status=='exited' else rr[atom];prel=float(l['pre_relu'][atom]);prer=float(r['pre_relu'][atom])
      memberrows.append(dict(site=site,frame=frame,split=split,family=fam,template=template,gold=g,distance_left=lo,distance_right=hi,left_id=lid,right_id=rid,atom=int(atom),group=str(groups[atom]),status=status,z_left=float(x[atom]),z_right=float(y[atom]),delta=float(delta[atom]),unit_left=float(ql[atom]),unit_right=float(qr[atom]),rank_left=lr.get(atom),rank_right=rr.get(atom),cutoff_left=l['cutoff32'],cutoff_right=r['cutoff32'],pre_relu_left=prel,pre_relu_right=prer,active_value_over_cutoff=float(active_value/active_cut),active_rank=active_rank,near_cutoff=bool(active_rank>=25 or active_value/active_cut<=1.25),prechange_over_cutoff=float(abs(prer-prel)/((l['cutoff32']+r['cutoff32'])/2)),was_subthreshold_positive=bool(status=='entered' and prel>0),still_subthreshold_positive=bool(status=='exited' and prer>0),abs_raw_change=float(abs(delta[atom])),abs_decoder_weighted_change=float(abs(delta[atom])*dn[atom])))
   for view in ['native','six','pre_relu','hidden','reconstructed']:
    values={};unit_delta={}
    for d in DISTS:
     pa,pb=[data[dd[str(d)][g]] for g in 'AB'];va=pa['z'] if view=='native' else pa['z'][Cids] if view=='six' else pa['pre_relu'] if view=='pre_relu' else pa['h'] if view=='hidden' else pa['reconstruction'];vb=pb['z'] if view=='native' else pb['z'][Cids] if view=='six' else pb['pre_relu'] if view=='pre_relu' else pb['h'] if view=='hidden' else pb['reconstruction'];delta=va-vb;na=np.linalg.norm(va);nb=np.linalg.norm(vb);rms=np.sqrt((na*na+nb*nb)/2);full_rms=np.sqrt((pa['z']@pa['z']+pb['z']@pb['z'])/2);relative=delta/rms if rms>1e-12 else np.full_like(delta,np.nan);ud=va/na-vb/nb if na>1e-12 and nb>1e-12 else np.full_like(delta,np.nan);values[d]=(delta,float(np.linalg.norm(delta)),float(rms),float(np.linalg.norm(relative)));unit_delta[d]=ud;strict=bool(np.all(pa['z'][Cids]>0) and np.all(pb['z'][Cids]>0));hd=pa['h']-pb['h'];rd=pa['reconstruction']-pb['reconstruction']
     factrows.append(dict(site=site,frame=frame,split=split,family=fam,template=template,distance=d,view=view,raw_delta_norm=float(np.linalg.norm(delta)),RMS_row_norm=float(rms),relative_separation=float(np.linalg.norm(relative)),full_scale_separation=float(np.linalg.norm(delta)/full_rms),unit_row_contrast_norm=float(np.linalg.norm(ud)),all_six_positive=strict,active_six_A=int(np.count_nonzero(pa['z'][Cids])),active_six_B=int(np.count_nonzero(pb['z'][Cids])),fact_reconstruction_relative_error=float(np.linalg.norm(hd-rd)/np.linalg.norm(hd)) if np.linalg.norm(hd)>1e-12 else None,relative_reconstruction_A=pa['relative_reconstruction_error'],relative_reconstruction_B=pb['relative_reconstruction_error']))
    for lo,hi in PAIRS:
     dl,al,sl,nl=values[lo];dr,ar,sr,nr=values[hi];strict=all(np.all(data[dd[str(d)][g]]['z'][Cids]>0) for d in [lo,hi] for g in 'AB');gain=float(dr@dl/(dl@dl)) if dl@dl>1e-12 else None;cos=cosine(dl,dr);full=dict(site=site,frame=frame,split=split,family=fam,template=template,distance_left=lo,distance_right=hi,view=view,raw_norm_left=al,raw_norm_right=ar,log_raw_ratio=float(np.log(ar/al)) if al>0 and ar>0 else None,scale_left=sl,scale_right=sr,log_total_scale_ratio=float(np.log(sr/sl)) if sl>0 and sr>0 else None,relative_separation_left=nl,relative_separation_right=nr,log_relative_ratio=float(np.log(nr/nl)) if nl>0 and nr>0 else None,raw_contrast_cosine=cos,unit_contrast_cosine=cosine(unit_delta[lo],unit_delta[hi]),projection_gain=gain,orthogonal_fraction=float(np.linalg.norm(dr-gain*dl)/np.linalg.norm(dr)) if gain is not None and np.linalg.norm(dr)>0 else None,all_six_positive=strict)
     if full['log_relative_ratio'] is not None:assert abs(full['log_relative_ratio']-(full['log_raw_ratio']-full['log_total_scale_ratio']))<1e-10
     contrastrows.append(full)
table(R/f'tables/{stage}_pair_metrics.csv',pairrows);table(R/f'tables/{stage}_member_values.csv',memberrows);table(R/f'tables/{stage}_fact_metrics.csv',factrows);table(R/f'tables/{stage}_fact_contrasts.csv',contrastrows);jsonl(R/f'results/{stage}_membership.jsonl',rawmembers)
p=pd.DataFrame(pairrows);f=pd.DataFrame(contrastrows);summ=[]
for (site,frame,split,lo,hi),q in p.groupby(['site','frame','split','distance_left','distance_right']):
 for field,log in [('shared',False),('entered',False),('Jaccard',False),('log_full_norm_ratio',True),('cosine_full',False),('log_common_norm_ratio',True),('cosine_common',False),('unit_full_change',False)]:summ.append(dict(site=site,frame=frame,split=split,distance_left=int(lo),distance_right=int(hi),metric=field,**summarize(q,field,log)))
for (site,frame,split,lo,hi,view),q in f.groupby(['site','frame','split','distance_left','distance_right','view']):
 for field,log in [('log_raw_ratio',True),('log_total_scale_ratio',True),('log_relative_ratio',True),('raw_contrast_cosine',False),('unit_contrast_cosine',False),('projection_gain',False)]:summ.append(dict(site=site,frame=frame,split=split,distance_left=int(lo),distance_right=int(hi),metric=view+'_'+field,**summarize(q,field,log)))
table(R/f'tables/{stage}_summaries.csv',summ)
b=behavior(stage=='controls');bs=[];bi=[]
for frame in frames:
 for fam,dd in MAP[frame].items():
  for d in DISTS:
   if not all(dd[str(d)][g] in b for g in 'AB'):continue
   aa,bb=[b[dd[str(d)][g]] for g in 'AB'];ma=META[dd[str(d)]['A']];split=ma['split'];item=[]
   for gold,x in zip('AB',[aa,bb]):
    im=(x['candidates'][0]['item_logprob']-x['candidates'][1]['item_logprob'])*(1 if gold=='A' else -1);item.append(im);bi.append(dict(frame=frame,family=fam,split=split,distance=d,gold=gold,id=x['id'],A_score=x['candidates'][0]['total_logprob'],B_score=x['candidates'][1]['total_logprob'],correct_margin=x['correct_margin'],correct=x['correct'],item_margin=im))
   bs.append(dict(frame=frame,family=fam,template=ma['template'],split=split,distance=d,paired=int(aa['correct'] and bb['correct']),mean_margin=(aa['correct_margin']+bb['correct_margin'])/2,item_paired=int(min(item)>0),mean_item_margin=float(np.mean(item))))
table(R/f'tables/{stage}_behavior_pairs.csv',bs);table(R/f'tables/{stage}_behavior_individual.csv',bi)
if stage=='baseline':
 primary=[]
 for si,site in enumerate(SITES):
  q=p[(p.site==site)&(p.split=='heldout')&(p.distance_left==16)&(p.distance_right==128)];v=q.groupby('family').retention.mean().to_numpy();lo,hi=interval(v,SEED+si);primary.append(dict(site=site,hypothesis='H1',N=len(v),value=float(v.mean()),lo=lo,hi=hi,p=sign_p(v-.9),template=sorted(q.template.unique().tolist())))
  q=f[(f.site==site)&(f.split=='heldout')&(f.view=='native')&(f.distance_left==16)&(f.distance_right==128)];v=q.log_relative_ratio.to_numpy();v=v[np.isfinite(v)];lo,hi=interval(v,SEED+si);bound=np.log(1.25)
  for h,pv in [('H2',max(sign_p(v+bound),sign_p(bound-v))),('H3',sign_p(-v-bound))]:primary.append(dict(site=site,hypothesis=h,N=len(v),value=float(np.exp(v.mean())),lo=float(np.exp(lo)),hi=float(np.exp(hi)),p=pv,template=sorted(q.template.unique().tolist())))
 for h,adj in zip(primary,holm([x['p'] if x['N']>=8 else 1. for x in primary])):
  h['holm_p']=adj
  if h['N']<8:h['verdict']='INSUFFICIENT'
  elif h['hypothesis']=='H1':h['verdict']='SUPPORTED' if h['lo']>=.9 and adj<=.05 else 'NOT_SUPPORTED' if h['hi']<.9 else 'INSUFFICIENT'
  elif h['hypothesis']=='H2':h['verdict']='SUPPORTED' if h['lo']>=.8 and h['hi']<=1.25 and adj<=.05 else 'NOT_SUPPORTED' if h['hi']<.8 or h['lo']>1.25 else 'INSUFFICIENT'
  else:h['verdict']='SUPPORTED' if h['hi']<.8 and adj<=.05 else 'NOT_SUPPORTED' if h['lo']>.8 else 'INSUFFICIENT'
 dump(R/'results/primary_hypotheses.json',primary)
 # Literal replay of old population, exact strict-support denominator and C-relative direction.
 expected=pd.read_csv(OLD/'tables/membership_summary.csv');replay=[];oldg=pd.read_csv(OLD/'tables/family_geometry.csv')
 for site in SITES:
  for lo,hi in PAIRS:
   actual=p[(p.site==site)&(p.split=='heldout')&(p.distance_left==lo)&(p.distance_right==hi)].groupby('family').shared.mean().mean();ref=expected[(expected.site==site)&(expected.split=='heldout')&(expected.kind=='distance')&(expected.role==f'{lo}_to_{hi}')].iloc[0];assert abs(actual-ref.mean_shared)<1e-10;replay.append(dict(site=site,pair=f'{lo}_{hi}',shared=float(actual),R19=float(ref.mean_shared)))
  q=f[(f.site==site)&(f.split=='heldout')&(f.view=='six')&(f.distance_left==16)&(f.distance_right==128)&f.all_six_positive];ex=oldg[(oldg.site==site)&(oldg.split=='heldout')&oldg.H2_eligible];assert len(q)==len(ex) and abs(q.unit_contrast_cosine.mean()-ex.relative_near_far_cosine.mean())<1e-10;replay.append(dict(site=site,strict_six_N=len(q),strict_six_cos=float(q.unit_contrast_cosine.mean())))
 for d in DISTS:assert sum(x['paired'] for x in bs if x['split']=='heldout' and x['distance']==d)==12
 dump(R/'evidence/R19_replay.json',dict(UTC=now(),status='PASS',checks=replay,all_three_full_candidate_paired_12_of_12=True,old_heldout_exposed=True))
 print('PRIMARY',json.dumps(primary),flush=True)
print('ANALYZED',stage,len(pairrows),len(memberrows),len(factrows),flush=True)
