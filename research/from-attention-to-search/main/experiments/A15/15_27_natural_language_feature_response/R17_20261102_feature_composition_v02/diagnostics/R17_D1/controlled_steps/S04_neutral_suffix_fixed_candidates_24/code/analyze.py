from common import *
import itertools,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plan=json.load(open(R/'frozen_plan.json'));sel=json.load(open(R/'data/S03_frozen_selection.json'))['sites'];panel=rows(R/'data/panel.jsonl');new=np.load(R/'cache/new.npz')
def value(v):return float(v) if np.isfinite(v) else None
def sign(v):return None if not np.isfinite(v) else 0 if abs(v)<=plan['direction_epsilon'] else int(np.sign(v))
def normalize(x):
 d=np.linalg.norm(x,axis=1,keepdims=True);return np.divide(x,d,out=np.full_like(x,np.nan),where=d>0),d[:,0]
def oldarr(site,k):return np.concatenate([np.load(OLD/f'cache/{sp}.npz')[site+'__'+k] for sp in ['exploration','heldout_check']])
def classify(metric,newdiff,ref,new_active,old_active,new_zero,old_zero,reference):
 if metric=='q_weighted' and (new_zero or (reference=='old_pair' and old_zero)):return 'zero_norm'
 if not new_active or (reference=='old_pair' and not old_active):return 'member_inactive'
 ns=sign(newdiff)
 if ref is None or ref==0:return 'no_reference'
 return 'zero_difference' if ns==0 else 'same' if ns==ref else 'opposite'
def transition(site,family,split,kind,src,dst,a,b,za,zb):
 a=set(a);b=set(b);keep=a&b;inc=sum(zb[i]>za[i] for i in keep);dec=sum(zb[i]<za[i] for i in keep)
 return dict(site=site,family=family,split=split,kind=kind,source=src,destination=dst,source_count=len(a),destination_count=len(b),retained=len(keep),zero_to_positive=len(b-a),positive_to_zero=len(a-b),retained_stronger=int(inc),retained_weaker=int(dec),retained_equal=len(keep)-int(inc)-int(dec),retained_fraction=f'{len(keep)}/{len(a)}',new_fraction=f'{len(b-a)}/{len(b)}',lost_fraction=f'{len(a-b)}/{len(a)}',retained_IDs=' '.join(map(str,sorted(keep))),new_IDs=' '.join(map(str,sorted(b-a))),lost_IDs=' '.join(map(str,sorted(a-b))))
allvalues=[];allh2=[];allcounts=[];allpatterns=[];alltrans=[];actives=[];sums={}
for site in SITES:
 out=R/'results'/site;out.mkdir(exist_ok=True)
 zn=new[site+'__z'].astype(float);zo=oldarr(site,'z').astype(float);pn=new[site+'__pre'].astype(float);po=oldarr(site,'pre').astype(float);dn=new[site+'__decoder_norm'].astype(float);assert np.array_equal(dn,np.load(OLD/'cache/exploration.npz')[site+'__decoder_norm'])
 z={'old':zo,'new':zn};u={key:v*dn for key,v in z.items()};pvs={'old':po,'new':pn};groups={'H1_common':sel[site]['H1_common'],'H1_added_cat':sel[site]['H1_added']['cat'],'H1_added_dog':sel[site]['H1_added']['dog'],'H2':sel[site]['H2']}
 values=[];h2=[];patterns=[];tr=[];nn={};qn={};qq={}
 for group,ids in groups.items():
  qn[group]={};qq[group]={};nn[group]={}
  for context in ['old','new']:
   qr,nr=normalize(z[context][:,ids]);qw,nw=normalize(u[context][:,ids]);qn[group][context]=qw;qq[group][context]=qr;nn[group][context]=nw
   for ri,p in enumerate(panel):
    for j,i in enumerate(ids):
     top32=bool(i in new[site+'__topk_indices'][ri]) if context=='new' else bool(zo[ri,i]>0)
     values.append(dict(site=site,context=context,group=group,id=p['id'],family=p['family'],split=p['split'],condition=p['condition'],atom=i,Top32=top32,active=bool(z[context][ri,i]>0),z=z[context][ri,i],decoder_norm=dn[i],u=u[context][ri,i],preactivation=pvs[context][ri,i],q_raw=value(qr[ri,j]),q_weighted=value(qw[ri,j]),list_raw_L2=float(nr[ri]),list_weighted_L2=float(nw[ri])))
 for context in ['old','new']:
  for ri,p in enumerate(panel):
   ids=np.flatnonzero(z[context][ri]>0).tolist();actives.append(dict(site=site,context=context,id=p['id'],family=p['family'],split=p['split'],condition=p['condition'],text=p['text'],prefix=p['old_prefix'] if context=='old' else p['prefix'],active_members=ids,values=[dict(atom=i,z=z[context][ri,i],decoder_norm=dn[i],u=u[context][ri,i],preactivation=pvs[context][ri,i]) for i in ids]))
  for fi in range(6):
   off=fi*4;p=panel[off];ss=[np.flatnonzero(z[context][off+j]>0).tolist() for j in range(4)]
   for a,b in itertools.combinations(range(4),2):tr.append(transition(site,p['family'],p['split'],context,CONDS[a],CONDS[b],ss[a],ss[b],z[context][off+a],z[context][off+b]))
   for group,ids in groups.items():
    if group=='H2':continue
    for i in ids:
     zz=z[context][off:off+4,i];uu=u[context][off:off+4,i]
     pattern=bool((zz[:3]>0).all() and uu[:3].min()>uu[3]) if group=='H1_common' else bool(zz[0]==0 and zz[1 if group.endswith('cat') else 2]>0)
     patterns.append(dict(site=site,context=context,family=p['family'],split=p['split'],group=group,atom=i,P_z=zz[0],cat_z=zz[1],dog_z=zz[2],N_z=zz[3],P_u=uu[0],cat_u=uu[1],dog_u=uu[2],N_u=uu[3],pattern=pattern,PCD_all_active=bool((zz[:3]>0).all()),min_PCD_minus_N_u=float(uu[:3].min()-uu[3])))
 for fi in range(6):
  off=fi*4;p=panel[off]
  for ci,c in enumerate(CONDS):tr.append(transition(site,p['family'],p['split'],'old_to_new',c,c,np.flatnonzero(zo[off+ci]>0),np.flatnonzero(zn[off+ci]>0),zo[off+ci],zn[off+ci]))
  a=off+1;b=off+2
  for j,i in enumerate(groups['H2']):
   old_act=bool(zo[a,i]>0 and zo[b,i]>0);new_act=bool(zn[a,i]>0 and zn[b,i]>0);oz=nn['H2']['old'][a]==0 or nn['H2']['old'][b]==0;nz=nn['H2']['new'][a]==0 or nn['H2']['new'][b]==0
   od=zo[a,i]-zo[b,i];nd=zn[a,i]-zn[b,i];oq=qn['H2']['old'][a,j]-qn['H2']['old'][b,j];nq=qn['H2']['new'][a,j]-qn['H2']['new'][b,j]
   rec=dict(site=site,family=p['family'],split=p['split'],atom=i,decoder_norm=dn[i],old_cat_z=zo[a,i],old_dog_z=zo[b,i],new_cat_z=zn[a,i],new_dog_z=zn[b,i],old_raw_delta=od,new_raw_delta=nd,old_raw_direction=sign(od),new_raw_direction=sign(nd),old_cat_u=u['old'][a,i],old_dog_u=u['old'][b,i],new_cat_u=u['new'][a,i],new_dog_u=u['new'][b,i],old_weighted_raw_delta=u['old'][a,i]-u['old'][b,i],new_weighted_raw_delta=u['new'][a,i]-u['new'][b,i],old_cat_q_raw=value(qq['H2']['old'][a,j]),old_dog_q_raw=value(qq['H2']['old'][b,j]),new_cat_q_raw=value(qq['H2']['new'][a,j]),new_dog_q_raw=value(qq['H2']['new'][b,j]),old_cat_q_weighted=value(qn['H2']['old'][a,j]),old_dog_q_weighted=value(qn['H2']['old'][b,j]),new_cat_q_weighted=value(qn['H2']['new'][a,j]),new_dog_q_weighted=value(qn['H2']['new'][b,j]),old_q_delta=value(oq),new_q_delta=value(nq),old_q_direction=sign(oq),new_q_direction=sign(nq),old_both_active=old_act,new_both_active=new_act,old_zero_norm=bool(oz),new_zero_norm=bool(nz),old_cat_active=bool(zo[a,i]>0),old_dog_active=bool(zo[b,i]>0),new_cat_active=bool(zn[a,i]>0),new_dog_active=bool(zn[b,i]>0),old_cat_list_weighted_L2=nn['H2']['old'][a],old_dog_list_weighted_L2=nn['H2']['old'][b],new_cat_list_weighted_L2=nn['H2']['new'][a],new_dog_list_weighted_L2=nn['H2']['new'][b],frozen_q_direction=sel[site]['H2_discovery_direction'][str(i)],frozen_raw_direction=sign(plan['old_raw_discovery_mean_difference'][site][str(i)]))
   for metric,ndiff in [('raw',nd),('q_weighted',nq)]:
    for ref in ['old_pair','S03_discovery']:
     rs=sign(od if metric=='raw' else oq) if ref=='old_pair' else rec['frozen_raw_direction' if metric=='raw' else 'frozen_q_direction']
     rec[metric+'_'+ref+'_status']=classify(metric,ndiff,rs,new_act,old_act,nz,oz,ref)
   h2.append(rec)
 for i in groups['H2']:
  for split in ['exploration','heldout_check']:
   rr=[x for x in h2 if x['atom']==i and x['split']==split]
   for metric,ref in itertools.product(['raw','q_weighted'],['old_pair','S03_discovery']):
    ct={s:sum(x[metric+'_'+ref+'_status']==s for x in rr) for s in ['same','opposite','member_inactive','zero_norm','no_reference','zero_difference']};assert sum(ct.values())==3
    allcounts.append(dict(site=site,atom=i,split=split,metric=metric,reference=ref,denominator=3,**ct,new_not_both_active_flags=sum(not x['new_both_active'] for x in rr),new_zero_norm_flags=sum(x['new_zero_norm'] for x in rr)))
 table(out/'candidate_values.csv',values);table(out/'H2_old_new_pairs.csv',h2);table(out/'H1_patterns.csv',patterns);table(out/'support_transitions.csv',tr)
 allvalues+=values;allh2+=h2;allpatterns+=patterns;alltrans+=tr
 pairinfo=[]
 for fi in range(6):
  a=fi*4+1;b=fi*4+2;ids=groups['H2'];pairinfo.append(dict(family=panel[a]['family'],split=panel[a]['split'],old_full_support_equal=bool(np.array_equal(zo[a]>0,zo[b]>0)),new_full_support_equal=bool(np.array_equal(zn[a]>0,zn[b]>0)),old_fixed_list_support_equal=bool(np.array_equal(zo[a,ids]>0,zo[b,ids]>0)),new_fixed_list_support_equal=bool(np.array_equal(zn[a,ids]>0,zn[b,ids]>0)),new_fixed_list_all_both_active=bool((zn[[a,b]][:,ids]>0).all())))
 table(out/'pair_support_controls.csv',pairinfo)
 sums[site]=dict(H2_fixed_ids=groups['H2'],new_active_counts=(zn>0).sum(1).tolist(),new_zero_norm_H2_rows=int((nn['H2']['new']==0).sum()),new_zero_norm_H1_common_rows=int((nn['H1_common']['new']==0).sum()),pairs=pairinfo,new_reconstruction_relative_L2=new[site+'__reconstruction_relative_L2'].tolist())
 # Compact side-by-side raw and relative panels, two frozen lists per dictionary.
 fig,axs=plt.subplots(2,2,figsize=(14,15));fig.subplots_adjust(left=.11,right=.96,bottom=.06,top=.89,hspace=.2,wspace=.28)
 for row,group in enumerate(['H1_common','H2']):
  ids=groups[group]
  for col,(mat,title) in enumerate([(zn[:,ids],group+' raw z'),(qn[group]['new'],group+' weighted q = u/L2(u_list)')]):
   ax=axs[row,col];cm=plt.get_cmap('viridis').copy();cm.set_bad('#bdbdbd');im=ax.imshow(np.ma.masked_invalid(mat),aspect='auto',cmap=cm,vmin=0);fig.colorbar(im,ax=ax,shrink=.6,fraction=.04,pad=.035)
   ax.set_xticks(range(len(ids)),ids,fontsize=9);ax.set_yticks(range(24),[p['family']+' '+p['condition'] for p in panel],fontsize=8);ax.set_title(title,fontsize=11);ax.axhline(11.5,color='red',lw=1.5);ax.set_xlabel('Frozen atom IDs in this dictionary only')
   for a in range(24):
    for b in range(len(ids)):ax.text(b,a,'NA' if not np.isfinite(mat[a,b]) else f'{mat[a,b]:.2f}',ha='center',va='center',fontsize=7,color='white' if mat[a,b]<np.nanmax(mat)*.55 else 'black')
 fig.suptitle(f'{site}: same neutral suffix Description: for all24 bodies\nS03 fixed candidates; upper12 exploration, lower12 check; gray = zero norm\nRaw/weighted values, norms and all four frozen lists are in candidate_values.csv',fontsize=11,y=.975)
 fig.savefig(R/f'figures/{site}_fixed_candidates.png',dpi=125,bbox_inches='tight',pad_inches=.2);plt.close(fig)
 ids=groups['H2'];oldraw=(zo[1::4][:,ids]-zo[2::4][:,ids]);newraw=(zn[1::4][:,ids]-zn[2::4][:,ids]);oldq=qn['H2']['old'][1::4]-qn['H2']['old'][2::4];newq=qn['H2']['new'][1::4]-qn['H2']['new'][2::4]
 fig,axs=plt.subplots(2,2,figsize=(14,8));fig.subplots_adjust(left=.08,right=.96,bottom=.08,top=.85,hspace=.38,wspace=.2)
 for ax,m,title,bound,fmt in zip(axs.flat,[oldraw,newraw,oldq,newq],['S03 raw cat-dog','S04 raw cat-dog','S03 normalized weighted cat-dog','S04 normalized weighted cat-dog'],[max(abs(oldraw).max(),abs(newraw).max())]*2+[max(np.nanmax(abs(oldq)),np.nanmax(abs(newq)))]*2,['.3f','.3f','.5f','.5f']):
  cm=plt.get_cmap('RdBu_r').copy();cm.set_bad('#bdbdbd');im=ax.imshow(np.ma.masked_invalid(m),aspect='auto',cmap=cm,vmin=-bound or -1,vmax=bound or 1);fig.colorbar(im,ax=ax,shrink=.7,fraction=.04,pad=.02);ax.set_xticks(range(len(ids)),ids,fontsize=9);ax.set_yticks(range(6),[f'F{i+1:02d}' for i in range(6)]);ax.set_title(title);ax.axhline(2.5,color='black',lw=1.5)
  for a in range(6):
   for b,i in enumerate(ids):
    rr=next(x for x in h2 if x['family']==f'F{a+1:02d}' and x['atom']==i);context='old' if title.startswith('S03') else 'new';star='' if rr[context+'_both_active'] else '*';text='NA' if not np.isfinite(m[a,b]) else format(m[a,b],fmt)+star;ax.text(b,a,text,ha='center',va='center',fontsize=8,color='white' if abs(m[a,b])>bound*.6 else 'black')
 fig.suptitle(f'{site}: old/new cat-minus-dog differences on exact S03 H2 list\nRed cat>dog; blue dog>cat; * member not bilateral positive; gray undefined\nBlack line: exploration F01-03 / check F04-06. Stars are not fixed-support replication.',fontsize=11,y=.98);fig.savefig(R/f'figures/{site}_H2_old_new_differences.png',dpi=135,bbox_inches='tight',pad_inches=.15);plt.close(fig)

table(R/'results/H2_direction_counts.csv',allcounts);jsonl(R/'results/all_active_members.jsonl',actives)
table(R/'results/all_support_transitions.csv',alltrans);table(R/'results/all_H2_old_new_pairs.csv',allh2)
pc=[]
for site in SITES:
 for group in ['H1_common','H1_added_cat','H1_added_dog']:
  ids=sel[site]['H1_common'] if group=='H1_common' else sel[site]['H1_added']['cat' if group.endswith('cat') else 'dog']
  for i,sp,ctx in itertools.product(ids,['exploration','heldout_check'],['old','new']):
   rr=[x for x in allpatterns if x['site']==site and x['group']==group and x['atom']==i and x['split']==sp and x['context']==ctx];pc.append(dict(site=site,group=group,atom=i,split=sp,context=ctx,matches=sum(x['pattern'] for x in rr),families=3))
table(R/'results/H1_pattern_coverage.csv',pc)
# Native behavior, including P/N preferences with no correctness score.
behavior=rows(R/'results/behavior_raw.jsonl');br=[];cr=[];pairs=[];hist={x['id']:x for x in rows(R/'data/S02_original_behavior_scores.jsonl')}
for b in behavior:
 cat,dog=b['candidates'];br.append(dict(id=b['id'],family=b['family'],split=b['split'],condition=b['condition'],gold=b['gold'],cat_score=cat['total_logprob'],dog_score=dog['total_logprob'],delta=b['delta_cat_minus_dog'],choice=b['choice'],correct=b['correct']))
 for cc in b['candidates']:cr.append(dict(id=b['id'],family=b['family'],condition=b['condition'],label=cc['label'],text=cc['text'],token_ids=json.dumps(cc['candidate_token_ids']),token_count=cc['token_count'],token_logprobs=json.dumps(cc['token_logprobs']),total_logprob=cc['total_logprob']))
for fi in range(6):
 ff=f'F{fi+1:02d}';c=next(b for b in behavior if b['family']==ff and b['condition']=='cat');d=next(b for b in behavior if b['family']==ff and b['condition']=='dog');oc=hist[f'S02_{ff}_cat'];od=hist[f'S02_{ff}_dog']
 pairs.append(dict(family=ff,split=c['split'],new_cat_choice=c['choice'],new_dog_choice=d['choice'],new_cat_correct=c['correct'],new_dog_correct=d['correct'],new_choices_switch=c['choice']!=d['choice'],new_both_correct=c['correct'] and d['correct'],new_cat_input_delta=c['delta_cat_minus_dog'],new_dog_input_delta=d['delta_cat_minus_dog'],historical_S02_cat_delta=oc['delta_cat_minus_dog'],historical_S02_dog_delta=od['delta_cat_minus_dog'],historical_S02_both_correct=oc['correct'] and od['correct']))
table(R/'results/behavior.csv',br);table(R/'results/behavior_candidates.csv',cr);table(R/'results/behavior_pairs.csv',pairs)
table(R/'results/behavior_errors.csv',[b for b in br if b['correct'] is False],fields=list(br[0]))
bs=dict(cat_correct=sum(b['correct'] is True for b in behavior if b['condition']=='cat'),dog_correct=sum(b['correct'] is True for b in behavior if b['condition']=='dog'),scored=12,correct=sum(b['correct'] is True for b in behavior),pairs=6,choices_switch=sum(p['new_choices_switch'] for p in pairs),both_correct_pairs=sum(p['new_both_correct'] for p in pairs),P_preferences={x:sum(b['choice']==x for b in behavior if b['condition']=='P') for x in ['cat','dog']},N_preferences={x:sum(b['choice']==x for b in behavior if b['condition']=='N') for x in ['cat','dog']},P_N_correctness='NOT_DEFINED',candidate_token_ids={c['label']:c['candidate_token_ids'] for c in behavior[0]['candidates']},candidate_lengths={c['label']:c['token_count'] for c in behavior[0]['candidates']})
dump(R/'results/summary.json',dict(behavior=bs,sites=sums));dump(R/'evidence/analysis_complete.json',dict(UTC=now(),rows=24,behavior_rows=24,candidate_sequences=48,SAEs=2,H2_pairs=len(allh2),H2_count_rows=len(allcounts),candidate_values=len(allvalues),support_transition_rows=len(alltrans),selection_changed=False,scientific_acceptance='Unknown',next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW'))
print(json.dumps(bs,ensure_ascii=False,indent=2));print('S04_ANALYSIS_DONE',flush=True)
