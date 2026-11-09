from engine import *
from stats_utils import boot_interval,sign_p,corr_audit,holm,cosine,cluster_interval
import pandas as pd,math
spec=json.load(open(R/'data/candidates.json'))['sites'];panel=rows(R/'data/panel.jsonl');lookup={p['id']:p for p in panel};behavior={z['id']:z for stage in ['smoke','discovery','heldout'] for z in rows(R/f'results/behavior_{stage}.jsonl')};pairing=list(csv.DictReader(open(R/'data/text_pairing.csv')))
frequency=[];members=[];components=[];vectors={};geometries=[];individual=[];hrecords=[];behavior_pairs=[]
for p in panel:
 b=behavior[p['id']];individual.append(dict(id=p['id'],family=p['family'],template=p['template'],split=p['split'],condition=p['condition'],gold=p['gold'],near_label=p['near_label'],near_item=p['near_item'],gap=p['actual_distance'],evidence_position=p['evidence_last_position'],target_position=p['target_position'],A_total=b['candidates'][0]['total_logprob'],B_total=b['candidates'][1]['total_logprob'],A_item=b['candidates'][0]['item_logprob'],B_item=b['candidates'][1]['item_logprob'],A_minus_B=b['A_minus_B'],correct_margin=b['correct_margin'],choice=b['choice'],correct=b['correct'],R18_source_id=p['R18_source_id']))
for split in ['discovery','heldout']:
 fs=sorted({p['family'] for p in panel if p['split']==split})
 for fam in fs:
  for co in CONDS:
   a,b=[behavior[f'{fam}_{co}_{g}'] for g in 'AB'];behavior_pairs.append(dict(family=fam,split=split,template=lookup[a['id']]['template'],condition=co,correct_A=a['correct'],correct_B=b['correct'],paired=int(a['correct'] and b['correct']),mean_margin=(a['correct_margin']+b['correct_margin'])/2))
  for near,role in [('N','neutral'),('O','opposite'),('C','congruent')]:
   aa=behavior[f'{fam}_near'+('N' if near=='N' else 'B' if near=='O' else 'A')+'_A'];bb=behavior[f'{fam}_near'+('N' if near=='N' else 'A' if near=='O' else 'B')+'_B'];behavior_pairs.append(dict(family=fam,split=split,template=lookup[aa['id']]['template'],condition='matched_'+role,correct_A=aa['correct'],correct_B=bb['correct'],paired=int(aa['correct'] and bb['correct']),mean_margin=(aa['correct_margin']+bb['correct_margin'])/2))
table(R/'tables/behavior_individual.csv',individual);table(R/'tables/behavior_pairs.csv',behavior_pairs)
for si,site in enumerate(SITES):
 freq=pd.read_csv(R/f'data/{site}_reference_frequency.csv');groups=freq['group'].to_numpy();Cids=spec[site]['C'];allv={};allz={};dn=None
 for stage in ['discovery','heldout']:
  pp,z,a=load_stage(stage,site);dn=a[site+'__decoder_norm'].astype(float)
  for i,p in enumerate(pp):allz[p['id']]=z[i];allv[p['id']]=(a[site+'__indices'][i],a[site+'__values'][i])
 # Per-row complete sparse activations with true positions and known reference labels.
 for pid,(ids,vals) in allv.items():
  p=lookup[pid]
  for f,v in zip(ids,vals):
   components.append(dict(site=site,id=pid,family=p['family'],split=p['split'],condition=p['condition'],gold=p['gold'],atom=int(f),z=float(v),reference_group=groups[f],reference_frequency=float(freq.iloc[f]['frequency']),reference_count=int(freq.iloc[f]['positive_positions']),reference_doc_coverage=int(freq.iloc[f]['document_coverage']),decoder_norm=float(dn[f]),target_token_id=p['target_token_id'],target_position=p['target_position']))
 # Member lists and group changes, independently of geometry eligibility.
 for pair in pairing:
  x=allz[pair['left']];y=allz[pair['right']];sx=set(np.where(x>0)[0]);sy=set(np.where(y>0)[0]);common=sx&sy;entered=sy-sx;exited=sx-sy;changed=sx|sy
  members.append(dict(site=site,**pair,intersection=len(common),union=len(changed),Jaccard=len(common)/len(changed) if changed else None,shared_ids=sorted(map(int,common)),entered_ids=sorted(map(int,entered)),exited_ids=sorted(map(int,exited)),shared_raw_left=[float(x[f]) for f in sorted(common)],shared_raw_right=[float(y[f]) for f in sorted(common)],entered_values=[float(y[f]) for f in sorted(entered)],exited_values=[float(x[f]) for f in sorted(exited)]))
  for group in GROUPS:
   ids=[f for f in changed if groups[f]==group];delta=y-x
   frequency.append(dict(site=site,family=pair['family'],split=pair['split'],kind=pair['kind'],role=pair['role'],group=group,left=pair['left'],right=pair['right'],shared=sum(groups[f]==group for f in common),entered=sum(groups[f]==group for f in entered),exited=sum(groups[f]==group for f in exited),active_left=sum(groups[f]==group for f in sx),active_right=sum(groups[f]==group for f in sy),abs_raw_change=float(sum(abs(delta[f]) for f in ids)),abs_decoder_weighted_change=float(sum(abs(delta[f])*dn[f] for f in ids)),atom_ids=sorted(map(int,ids))))
 for split in ['discovery','heldout']:
  fs=sorted({p['family'] for p in panel if p['split']==split})
  for fam in fs:
   zz={co:{g:allz[f'{fam}_{co}_{g}'][Cids].astype(float) for g in 'AB'} for co in CONDS};qq={co:{g:v/np.linalg.norm(v) if np.linalg.norm(v)>0 else v*np.nan for g,v in dd.items()} for co,dd in zz.items()};strict_main=all(np.all(zz[co][g]>0) for co in ['main16','main128'] for g in 'AB');strict_far=all(np.all(zz[co][g]>0) for co in ['nearN','nearA','nearB'] for g in 'AB');eps=1e-6;geo=dict(site=site,family=fam,split=split,template=lookup[f'{fam}_main16_A']['template'],C=Cids,C_size=len(Cids),strict_main=bool(strict_main),strict_far=bool(strict_far));arr={}
   for representation,vec in [('raw',zz),('relative',qq)]:
    d16=vec['main16']['A']-vec['main16']['B'];d64=vec['main64']['A']-vec['main64']['B'];d128=vec['main128']['A']-vec['main128']['B'];d0=vec['nearN']['A']-vec['nearN']['B'];ta=vec['nearA']['A']-vec['nearA']['B'];tb=vec['nearB']['A']-vec['nearB']['B'];T=(ta+tb)/2;N=((vec['nearA']['A']-vec['nearB']['A'])+(vec['nearA']['B']-vec['nearB']['B']))/2;I=ta-tb;opp=vec['nearB']['A']-vec['nearA']['B'];cong=vec['nearA']['A']-vec['nearB']['B'];err=float(np.nanmax(np.abs(opp-(T-N)))) if len(T) else 0;assert err<1e-10
    den=float(d0@d0);rT=float(T@d0/den) if den>eps**2 else None;rN=float(N@d0/den) if den>eps**2 else None;rO=float(opp@d0/den) if den>eps**2 else None;cA=cosine(ta,d0);cB=cosine(tb,d0);h1=(cA+cB)/2 if cA is not None and cB is not None else None
    geo.update({representation+'_'+k:v for k,v in dict(delta16_norm=float(np.linalg.norm(d16)),delta128_norm=float(np.linalg.norm(d128)),neutral_delta_norm=float(np.linalg.norm(d0)),target_alignment=h1,near_far_cosine=cosine(d16,d128),near_mid_cosine=cosine(d16,d64),target_projection=rT,near_projection=rN,opposite_projection=rO,interaction_norm=float(np.linalg.norm(I)),identity_error=err,pattern_loss=None if rO is None else 1-rO).items()})
    arr.update({representation+'_'+k:v for k,v in dict(delta16=d16,delta64=d64,delta128=d128,delta0=d0,T=T,N=N,I=I,opposite=opp,congruent=cong).items()})
    for j,f in enumerate(Cids):hrecords.append(dict(site=site,family=fam,split=split,atom=f,reference_group=groups[f],representation=representation,z16_A=float(vec['main16']['A'][j]),z16_B=float(vec['main16']['B'][j]),z128_A=float(vec['main128']['A'][j]),z128_B=float(vec['main128']['B'][j]),neutral_A=float(vec['nearN']['A'][j]),neutral_B=float(vec['nearN']['B'][j]),AA=float(vec['nearA']['A'][j]),BA=float(vec['nearA']['B'][j]),AB=float(vec['nearB']['A'][j]),BB=float(vec['nearB']['B'][j]),T=float(T[j]),N=float(N[j]),I=float(I[j]),neutral_delta=float(d0[j]),opposite_delta=float(opp[j])))
   bm={x['condition']:x for x in behavior_pairs if x['family']==fam};geo.update(neutral_paired=bm['matched_neutral']['paired'],opposite_paired=bm['matched_opposite']['paired'],congruent_paired=bm['matched_congruent']['paired'],neutral_margin=bm['matched_neutral']['mean_margin'],opposite_margin=bm['matched_opposite']['mean_margin'],behavior_loss=bm['matched_neutral']['mean_margin']-bm['matched_opposite']['mean_margin'])
   itemmargin=lambda co,g:(behavior[f'{fam}_{co}_{g}']['candidates'][0]['item_logprob']-behavior[f'{fam}_{co}_{g}']['candidates'][1]['item_logprob'])*(1 if g=='A' else -1)
   geo['item_behavior_loss']=(itemmargin('nearN','A')+itemmargin('nearN','B')-itemmargin('nearB','A')-itemmargin('nearA','B'))/2
   geo['H1_eligible']=bool(len(Cids)>=3 and strict_far and geo['relative_target_alignment'] is not None);geo['H2_eligible']=bool(len(Cids)>=3 and strict_main and geo['relative_near_far_cosine'] is not None);geo['H3_eligible']=bool(geo['H1_eligible'] and geo['relative_pattern_loss'] is not None);geometries.append(geo);vectors[site+'__'+fam]=arr
jsonl(R/'results/membership_pairs.jsonl',members);table(R/'tables/frequency_pair_changes.csv',frequency);table(R/'tables/sparse_activations.csv',components);table(R/'tables/fixed_member_values.csv',hrecords);table(R/'tables/family_geometry.csv',geometries)
np.savez_compressed(R/'cache/paired_vectors.npz',**{key+'__'+k:v for key,arr in vectors.items() for k,v in arr.items()})
primary=[]
for si,site in enumerate(SITES):
 gg=[g for g in geometries if g['site']==site and g['split']=='heldout']
 for h,field in [('H1','relative_target_alignment'),('H2','relative_near_far_cosine')]:
  q=[g for g in gg if g[h+'_eligible']];v=[g[field] for g in q];lo,hi=boot_interval(v,2026110419+si);cl,ch=cluster_interval(v,[g['template'] for g in q]) if q else [None,None];primary.append(dict(site=site,hypothesis=h,N=len(q),mean=float(np.mean(v)) if v else None,lo=lo,hi=hi,p=sign_p(v) if len(q)>=8 else 1.,template_lo=cl,template_hi=ch,eligible=len(q)>=8,secondary=None))
 q=[g for g in gg if g['H3_eligible']];au=corr_audit([g['relative_pattern_loss'] for g in q],[g['behavior_loss'] for g in q],[g['template'] for g in q],2026110419+si);pl=boot_interval([g['relative_pattern_loss'] for g in q]);bl=boot_interval([g['behavior_loss'] for g in q]);base=np.mean([g['neutral_paired'] for g in gg]);eligible=len(q)>=8 and base>=.8
 primary.append(dict(site=site,hypothesis='H3',N=len(q),mean=au['rho'],lo=au['lo'],hi=au['hi'],p=au['p'] if eligible else 1.,template_lo=None,template_hi=None,eligible=bool(eligible),secondary=dict(association=au,pattern_loss_mean=float(np.mean([g['relative_pattern_loss'] for g in q])) if q else None,pattern_loss_CI=pl,behavior_loss_mean=float(np.mean([g['behavior_loss'] for g in q])) if q else None,behavior_loss_CI=bl,neutral_paired_rate=float(base),item_association=corr_audit([g['relative_pattern_loss'] for g in q],[g['item_behavior_loss'] for g in q],[g['template'] for g in q],2026110419+si+5))))
adj=holm([x['p'] for x in primary])
for x,a in zip(primary,adj):
 x['holm_p']=a
 if not x['eligible']:x['verdict']='INSUFFICIENT'
 elif x['lo'] is not None and x['lo']>0 and a<=.05:
  if x['hypothesis']!='H3' or (x['secondary']['pattern_loss_CI'][0]>0 and x['secondary']['behavior_loss_CI'][0]>0):x['verdict']='SUPPORT_IN_THIS_PANEL'
  else:x['verdict']='LOCAL_SUPPORT_ONLY'
 elif x['hi'] is not None and x['hi']<0:x['verdict']='NOT_SUPPORTED'
 elif x['hypothesis']=='H3' and x['secondary']['behavior_loss_CI'][0] is not None and x['secondary']['behavior_loss_CI'][0]>0 and (x['secondary']['pattern_loss_CI'][0]>0 or x['secondary']['pattern_loss_CI'][1]<0):x['verdict']='LOCAL_SUPPORT_ONLY'
 else:x['verdict']='INSUFFICIENT'
dump(R/'results/primary_hypotheses.json',primary)
summ=[]
for site in SITES:
 for split in ['discovery','heldout']:
  for kind,role in sorted({(m['kind'],m['role']) for m in members}):
   q=[m for m in members if m['site']==site and m['split']==split and m['kind']==kind and m['role']==role];fs=sorted({m['family'] for m in q});v=[np.mean([m['Jaccard'] for m in q if m['family']==f]) for f in fs];lo,hi=boot_interval(v);summ.append(dict(site=site,split=split,kind=kind,role=role,families=len(fs),pairs=len(q),mean_Jaccard=float(np.mean(v)),lo=lo,hi=hi,mean_shared=float(np.mean([m['intersection'] for m in q])),mean_entered=float(np.mean([len(m['entered_ids']) for m in q])),mean_exited=float(np.mean([len(m['exited_ids']) for m in q]))))
table(R/'tables/membership_summary.csv',summ)
fsumm=[]
for site in SITES:
 groupref=pd.read_csv(R/f'data/{site}_reference_frequency.csv')
 for split in ['discovery','heldout']:
  for group in GROUPS:
   a=[x for x in components if x['site']==site and x['split']==split and x['reference_group']==group];fsumm.append(dict(site=site,split=split,group=group,reference_members=int(sum(groupref['group']==group)),observed_members=len({x['atom'] for x in a}),positions=len({x['id'] for x in a}),families=len({x['family'] for x in a}),active_instances=len(a),sum_raw_z=float(sum(x['z'] for x in a)),sum_per_atom_decoder_norm=float(sum(x['z']*x['decoder_norm'] for x in a)),candidate_common_members=sum(x['reference_group']==group and x['role']=='common' for x in spec[site]['selection']),candidate_responsive_members=sum(x['reference_group']==group and x['role']=='responsive' for x in spec[site]['selection'])))
table(R/'tables/frequency_coverage.csv',fsumm)
beh=[]
for split in ['discovery','heldout']:
 for co in list(CONDS)+['matched_neutral','matched_opposite','matched_congruent']:
  q=[x for x in behavior_pairs if x['split']==split and x['condition']==co];beh.append(dict(split=split,condition=co,families=len(q),correct_prompts=sum(x['correct_A']+x['correct_B'] for x in q),paired=sum(x['paired'] for x in q),paired_rate=float(np.mean([x['paired'] for x in q])),mean_margin=float(np.mean([x['mean_margin'] for x in q]))))
table(R/'tables/behavior_summary.csv',beh)
print('PRIMARY',json.dumps(primary,ensure_ascii=False),flush=True)
