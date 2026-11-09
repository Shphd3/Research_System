"""Descriptive tables/plots only. No fitting, reselection or interventions."""
from common import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
PANEL=rows(R/'data/panel.jsonl');SELECTION=json.load(open(R/'results/selection.json'))
def normalized(a):
 n=np.linalg.norm(a,axis=-1,keepdims=True)
 return np.divide(a,n,out=np.full_like(a,np.nan),where=n>0)
def val(x): return float(x) if np.isfinite(x) else None
def sign(x): return None if not np.isfinite(x) else 0 if abs(x)<=1e-8 else int(np.sign(x))
def arrdict(x): return {int(i):float(x[i]) for i in np.flatnonzero(x>0)}
def load(site,key):
 return np.concatenate([np.load(R/f'cache/{s}.npz')[site+'__'+key] for s in ['exploration','heldout_check']])
all_summary={};alltrans=[];allh2=[];allcandidates=[];allactive=[];allevents=[];allpairs=[];allfails=[];commonrows=[];counts=[]
for site in SITES:
 out=R/'results'/site;out.mkdir(exist_ok=True)
 sel=SELECTION['sites'][site];z=load(site,'z').astype(float);pre=load(site,'pre').astype(float);dn=np.load(R/'cache/exploration.npz')[site+'__decoder_norm'].astype(float)
 assert np.array_equal(dn,np.load(R/'cache/heldout_check.npz')[site+'__decoder_norm'])
 u=z*dn;active=z>0; norms=np.linalg.norm(u,axis=-1);setrows=[];trans=[];h2rows=[];candidates=[];pairs=[];fail=[];h1common=[]
 for ri,p in enumerate(PANEL):
  aset=np.flatnonzero(active[ri]).tolist();record=dict(**p,site=site,active_members=aset,active_count=len(aset),raw_L2=float(np.linalg.norm(z[ri])),weighted_L2=float(norms[ri]))
  setrows.append(record)
  for i in aset: allactive.append(dict(site=site,id=p['id'],family=p['family'],split=p['split'],condition=p['condition'],atom=i,z=z[ri,i],decoder_norm=dn[i],u=u[ri,i],preactivation=pre[ri,i]))
 h2=sel['H2'];qz=normalized(z[:,h2]);qu=normalized(u[:,h2]);h1=sel['H1_common']
 cqz=normalized(z[:,h1]);cqu=normalized(u[:,h1]);categorygroups=[('H1_common',h1),('H1_added_cat',sel['H1_added']['cat']),('H1_added_dog',sel['H1_added']['dog']),('H2',h2)]
 for group,ids in categorygroups:
  for ri,p in enumerate(PANEL):
   for i in ids:
    j=(h2 if group=='H2' else h1).index(i) if group in ['H1_common','H2'] else None
    candidates.append(dict(site=site,group=group,**{k:p[k] for k in ['id','family','split','condition']},atom=i,active=bool(active[ri,i]),z=z[ri,i],decoder_norm=dn[i],u=u[ri,i],preactivation=pre[ri,i],q_raw=val((qz if group=='H2' else cqz)[ri,j]) if j is not None else None,q_weighted=val((qu if group=='H2' else cqu)[ri,j]) if j is not None else None))
 for fi in range(6):
  offset=fi*4;pp=PANEL[offset];family=pp['family'];split=pp['split'];ss=[set(np.flatnonzero(active[offset+j])) for j in range(4)]
  common3=ss[0]&ss[1]&ss[2];common4=set.intersection(*ss);union3=set.union(*ss[:3]);union4=set.union(*ss)
  commonrows.append(dict(site=site,family=family,split=split,P_active=len(ss[0]),cat_active=len(ss[1]),dog_active=len(ss[2]),N_active=len(ss[3]),PCD_common=len(common3),PCD_union=len(union3),PCDN_common=len(common4),PCDN_union=len(union4),PCD_common_IDs=' '.join(map(str,sorted(common3))),PCDN_common_IDs=' '.join(map(str,sorted(common4))),PCD_common_over_P=f'{len(common3)}/{len(ss[0])}',PCD_common_over_union=f'{len(common3)}/{len(union3)}'))
  for a,b in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
   retained=ss[a]&ss[b];added=ss[b]-ss[a];lost=ss[a]-ss[b];ri=offset+a;rj=offset+b
   up=[i for i in sorted(retained) if z[rj,i]>z[ri,i]];down=[i for i in sorted(retained) if z[rj,i]<z[ri,i]];same=retained-set(up)-set(down)
   tr=dict(site=site,family=family,split=split,source=CONDS[a],destination=CONDS[b],source_count=len(ss[a]),destination_count=len(ss[b]),union_count=len(ss[a]|ss[b]),retained=len(retained),zero_to_positive=len(added),positive_to_zero=len(lost),retained_stronger=len(up),retained_weaker=len(down),retained_equal=len(same),retained_over_source=f'{len(retained)}/{len(ss[a])}',added_over_destination=f'{len(added)}/{len(ss[b])}',lost_over_source=f'{len(lost)}/{len(ss[a])}',added_over_inactive_source=f'{len(added)}/{30000-len(ss[a])}',retained_IDs=' '.join(map(str,sorted(retained))),added_IDs=' '.join(map(str,sorted(added))),lost_IDs=' '.join(map(str,sorted(lost))))
   trans.append(tr)
   for i in sorted(ss[a]|ss[b]):allevents.append(dict(site=site,family=family,split=split,source=CONDS[a],destination=CONDS[b],atom=int(i),event='zero_to_positive' if i in added else 'positive_to_zero' if i in lost else 'retained_stronger' if i in up else 'retained_weaker' if i in down else 'retained_equal',source_z=z[ri,i],destination_z=z[rj,i],source_u=u[ri,i],destination_u=u[rj,i],source_pre=pre[ri,i],destination_pre=pre[rj,i]))
  for i in h1:
   zz=z[offset:offset+4,i];uu=u[offset:offset+4,i];triple=bool((zz[:3]>0).all());contrast=float(uu[:3].min()-uu[3]);ok=triple and contrast>0
   h1common.append(dict(site=site,family=family,split=split,atom=i,triple_active=triple,min_PCD_minus_N_u=contrast,pattern=ok,P_u=uu[0],cat_u=uu[1],dog_u=uu[2],N_u=uu[3]))
   if not ok:fail.append(dict(site=site,hypothesis='H1_common',family=family,split=split,atom=i,reason='missing in P/cat/dog' if not triple else 'min(P,cat,dog) not stronger than N',observed=contrast,expected='triple active and min_PCD_minus_N_u > 0'))
  for label,ci in [('cat',1),('dog',2)]:
   for i in sel['H1_added'][label]:
    ok=z[offset,i]==0 and z[offset+ci,i]>0
    if not ok:fail.append(dict(site=site,hypothesis='H1_added_'+label,family=family,split=split,atom=i,reason='P active' if z[offset,i]>0 else 'fine inactive',observed=float(z[offset+ci,i]-z[offset,i]),expected='P z == 0 and fine z > 0'))
  selected_support_equal=bool(np.array_equal(active[offset+1,h2],active[offset+2,h2]));full_equal=ss[1]==ss[2]
  pair=dict(site=site,family=family,split=split,full_support_equal=full_equal,H2_selected_support_equal=selected_support_equal,H2_selected_all_both_active=bool(active[offset+1:offset+3,h2].all()) if h2 else False,cat_full_weighted_L2=norms[offset+1],dog_full_weighted_L2=norms[offset+2],cat_selected_raw_L2=float(np.linalg.norm(z[offset+1,h2])),dog_selected_raw_L2=float(np.linalg.norm(z[offset+2,h2])),cat_selected_weighted_L2=float(np.linalg.norm(u[offset+1,h2])),dog_selected_weighted_L2=float(np.linalg.norm(u[offset+2,h2])),H2_candidates=len(h2))
  nmatch=0;nvalid=0
  for j,i in enumerate(h2):
   a=offset+1;b=offset+2;delta=qu[a,j]-qu[b,j];dire=sel['H2_discovery_direction'][str(i)];obs=sign(delta);match=None if dire is None or dire==0 or obs is None else obs==dire
   if match is not None:nvalid+=1;nmatch+=int(match)
   h2rows.append(dict(site=site,family=family,split=split,atom=i,decoder_norm=dn[i],cat_z=z[a,i],dog_z=z[b,i],cat_u=u[a,i],dog_u=u[b,i],raw_difference=z[a,i]-z[b,i],weighted_difference=u[a,i]-u[b,i],cat_q_raw=val(qz[a,j]),dog_q_raw=val(qz[b,j]),raw_q_difference=val(qz[a,j]-qz[b,j]),cat_q_weighted=val(qu[a,j]),dog_q_weighted=val(qu[b,j]),weighted_q_difference=val(delta),cat_over_dog_u=val(u[a,i]/u[b,i]) if u[b,i]>0 else None,cat_over_dog_weighted_q=val(qu[a,j]/qu[b,j]) if np.isfinite(qu[b,j]) and qu[b,j]>0 else None,discovery_direction=dire,observed_direction=obs,direction_matches=match,full_support_equal=full_equal,selected_support_equal=selected_support_equal))
   if match is False:fail.append(dict(site=site,hypothesis='H2_weighted_q_direction',family=family,split=split,atom=i,reason='opposite or zero direction to frozen exploration mean',observed=val(delta),expected=dire))
  pair['direction_matches']=nmatch;pair['direction_defined']=nvalid;pairs.append(pair)
 for split in ['exploration','heldout_check']:
  fids=['F01','F02','F03'] if split=='exploration' else ['F04','F05','F06']
  for group,ids in categorygroups:
   for i in ids:
    if group=='H1_common':hits=sum(x['pattern'] for x in h1common if x['split']==split and x['atom']==i)
    elif group.startswith('H1_added_'):
     ci=1 if group.endswith('cat') else 2;hits=sum(z[fi*4,i]==0 and z[fi*4+ci,i]>0 for fi in range(6) if PANEL[fi*4]['split']==split)
    else:hits=sum(x['direction_matches'] is True for x in h2rows if x['split']==split and x['atom']==i)
    counts.append(dict(site=site,split=split,group=group,atom=i,matches=int(hits),families=3,ratio=f'{hits}/3'))
 table(out/'transitions.csv',trans);table(out/'candidate_values.csv',candidates,fields=['site','group','id','family','split','condition','atom','active','z','decoder_norm','u','preactivation','q_raw','q_weighted'])
 table(out/'H2_pairs.csv',pairs);table(out/'H2_directions.csv',h2rows,fields=['site','family','split','atom','decoder_norm','cat_z','dog_z','cat_u','dog_u','raw_difference','weighted_difference','cat_q_raw','dog_q_raw','raw_q_difference','cat_q_weighted','dog_q_weighted','weighted_q_difference','cat_over_dog_u','cat_over_dog_weighted_q','discovery_direction','observed_direction','direction_matches','full_support_equal','selected_support_equal'])
 table(out/'H1_common_patterns.csv',h1common,fields=['site','family','split','atom','triple_active','min_PCD_minus_N_u','pattern','P_u','cat_u','dog_u','N_u'])
 table(out/'pattern_failures.csv',fail,fields=['site','hypothesis','family','split','atom','reason','observed','expected']);jsonl(out/'active_sets_with_full_text.jsonl',setrows)
 def heatmaps(ids,name):
  if not ids:
   fig,ax=plt.subplots(figsize=(9,3));ax.text(.5,.5,'No eligible exploration candidates. No replacement selected.',ha='center');ax.axis('off')
  else:
   zz=z[:,ids];uu=u[:,ids];qr=normalized(zz);qw=normalized(uu);fig,axs=plt.subplots(2,2,figsize=(17,17));tick=[f'{p["family"]} {p["condition"]} '+('E' if p['split']=='exploration' else 'H') for p in PANEL]
   for ax,mat,title in zip(axs.flat,[zz,uu,qr,qw],['Raw activation z','Weighted u = z * decoder L2 norm','Relative raw z / L2(z_selected)','Relative weighted u / L2(u_selected)']):
    cm=plt.get_cmap('viridis').copy();cm.set_bad('#bdbdbd');im=ax.imshow(np.ma.masked_invalid(mat),aspect='auto',cmap=cm,vmin=0);fig.colorbar(im,ax=ax,shrink=.65)
    ax.set_xticks(range(len(ids)),ids);ax.set_yticks(range(24),tick,fontsize=9);ax.set_xlabel('Atom ID in this dictionary only');ax.set_title(title,fontsize=12);ax.axhline(11.5,color='red',lw=2)
    for ri in range(24):
     for j in range(len(ids)):ax.text(j,ri,'NA' if not np.isfinite(mat[ri,j]) else f'{mat[ri,j]:.2f}',ha='center',va='center',fontsize=8,color='white' if mat[ri,j]<np.nanmax(mat)*.55 else 'black')
   fig.suptitle(f'{site} | {name} | E: exploration F01-03; H: heldout F04-06\nFixed discovery candidates. P/cat/dog suffix: animal; N suffix: object. Gray: undefined norm.',fontsize=14)
  fig.tight_layout(rect=(0,0,1,.95));fig.savefig(R/f'figures/{site}_{name}.png',dpi=135);plt.close(fig)
 heatmaps(h1,'H1_common');heatmaps(h2,'H2_joint')
 fig,axs=plt.subplots(1,2,figsize=(13,4.8),sharey=True)
 for ax,c in zip(axs,['cat','dog']):
  tt=[t for t in trans if t['source']=='P' and t['destination']==c];xx=np.arange(6);bottom=np.zeros(6)
  for key,label,color in [('retained','P members retained','#3c8c76'),('zero_to_positive','zero P -> positive fine','#e1a540')]:
   vv=np.array([t[key] for t in tt]);ax.bar(xx,vv,bottom=bottom,label=label,color=color);bottom+=vv
   for j,v in enumerate(vv):ax.text(j,bottom[j]-v/2,str(v),ha='center',va='center',fontsize=10)
  for j,t in enumerate(tt):ax.text(j,33,f'lost {t["positive_to_zero"]}',ha='center',fontsize=9)
  ax.set_xticks(xx,[f'F{f:02d}\n'+('E' if f<=3 else 'H') for f in range(1,7)]);ax.set_ylim(0,37);ax.axvline(2.5,color='red',ls='--');ax.set_title(f'P -> {c}');ax.set_ylabel('Active members (native Top32)')
 axs[0].legend(loc='upper left',fontsize=8);fig.suptitle(site+' | Membership counts, not evidence of added functional information');fig.tight_layout();fig.savefig(R/f'figures/{site}_H1_transitions.png',dpi=150);plt.close(fig)
 summary=dict(selected=sel,full_support_equal_pairs=sum(p['full_support_equal'] for p in pairs),selected_support_equal_pairs=sum(p['H2_selected_support_equal'] for p in pairs),selected_all_both_active_pairs=sum(p['H2_selected_all_both_active'] for p in pairs),zero_norm_H2_samples=int((np.linalg.norm(u[:,h2],axis=-1)==0).sum()),active_counts=active.sum(-1).tolist(),reconstruction_relative_L2=load(site,'reconstruction_relative_L2').tolist(),failures=len(fail),heldout_failures=sum(x['split']=='heldout_check' for x in fail),same_support_pairs=pairs)
 all_summary[site]=summary;alltrans+=trans;allh2+=h2rows;allcandidates+=candidates;allpairs+=pairs;allfails+=fail
dump(R/'results/summary.json',all_summary)
table(R/'results/common_intersections.csv',commonrows);table(R/'results/active_values.csv',allactive);table(R/'results/member_transition_values.csv',allevents);table(R/'results/pattern_coverage.csv',counts)
table(R/'results/all_pattern_failures.csv',allfails,fields=['site','hypothesis','family','split','atom','reason','observed','expected'])
dump(R/'evidence/analysis_complete.json',dict(UTC=now(),selection_SHA256=sha(R/'results/selection.json'),exploration_rows=12,heldout_rows=12,SAEs=2,figures=6,training=0,probe=0,intervention=0,H3_H4='NOT_RUN',next='STOP_WAIT_FOR_JOINT_REVIEW'))
print(json.dumps({s:{k:v for k,v in x.items() if k in ['selected','full_support_equal_pairs','selected_support_equal_pairs','zero_norm_H2_samples','heldout_failures']} for s,x in all_summary.items()},indent=2))
