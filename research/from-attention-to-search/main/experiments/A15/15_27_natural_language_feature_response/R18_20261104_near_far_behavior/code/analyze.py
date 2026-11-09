from common import *
import math,csv
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
panel={p['id']:p for p in rows(R/'data/panel.jsonl')}
raw=rows(R/'results/smoke.jsonl')+rows(R/'results/heldout.jsonl')
assert len(raw)==len(panel)==444
(R/'tables').mkdir(exist_ok=True)
def table(name,rr):
    rr=list(rr)
    with (R/'tables'/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def wilson(k,n):
    z=1.959963984540054;q=k/n;den=1+z*z/n
    h=z*math.sqrt(q*(1-q)/n+z*z/(4*n*n))/den;m=(q+z*z/(2*n))/den
    return [m-h,m+h]
rng=np.random.default_rng(20261104)
def interval(v):
    v=np.asarray(v,float);x=v[rng.integers(0,len(v),(10000,len(v)))].mean(1)
    return np.quantile(x,[.025,.975]).tolist()
def clustered(ps,key):
    groups=sorted({p['template'] for p in ps});means=np.array([np.mean([p[key] for p in ps if p['template']==g]) for g in groups]);v=means[rng.integers(0,len(means),(10000,len(means)))].mean(1)
    return np.quantile(v,[.025,.975]).tolist()
byid={x['id']:x for x in raw};bygroup={};baseline=[]
tokenrecords=[]
for x in raw:
    p=panel[x['id']]
    for c in x['candidates']:
        for k,(tid,lp) in enumerate(zip(c['token_ids'],c['token_logprobs'])):
            tokenrecords.append(dict(id=x['id'],family=x['family'],mode=x['mode'],split=x['split'],planned_distance=x['planned_distance'],actual_distance=x['actual_distance'],gold=x['gold'],candidate=c['label'],candidate_text=c['text'],candidate_token_count=c['token_count'],token_index=k,token_id=tid,logprob=lp,total_logprob=c['total_logprob']))
    if x['mode']=='baseline': baseline.append(dict(family=x['family'],split=x['split'],template=x['template'],planned_distance=x['planned_distance'],A_minus_B=x['A_minus_B'],choice=x['choice'],A_total=x['candidates'][0]['total_logprob'],B_total=x['candidates'][1]['total_logprob']))
    else:bygroup.setdefault((x['family'],x['mode'],x['planned_distance']),[]).append(x)
pairs=[]
for (fam,mode,d),v in sorted(bygroup.items()):
    a=next(x for x in v if x['gold']=='A');b=next(x for x in v if x['gold']=='B');assert len(v)==2
    base=next(x for x in baseline if x['family']==fam and x['planned_distance']==d)
    itemdelta=lambda x:x['candidates'][0]['item_logprob']-x['candidates'][1]['item_logprob']
    pairs.append(dict(family=fam,split=a['split'],template=a['template'],mode=mode,planned_distance=d,actual_distance_A=a['actual_distance'],actual_distance_B=b['actual_distance'],A_under_A=a['candidates'][0]['total_logprob'],B_under_A=a['candidates'][1]['total_logprob'],A_under_B=b['candidates'][0]['total_logprob'],B_under_B=b['candidates'][1]['total_logprob'],choice_under_A=a['choice'],choice_under_B=b['choice'],correct_A=a['correct'],correct_B=b['correct'],paired_success=int(a['correct'] and b['correct']),accuracy=(int(a['correct'])+int(b['correct']))/2,margin_A=a['correct_margin'],margin_B=b['correct_margin'],mean_margin=(a['correct_margin']+b['correct_margin'])/2,fact_preference_shift=a['A_minus_B']-b['A_minus_B'],baseline_A_minus_B=base['A_minus_B'],item_only_paired_success=int(itemdelta(a)>0 and itemdelta(b)<0),candidate_tokens=a['candidates'][0]['token_count']))
table('family_pairs.csv',pairs);table('baseline.csv',baseline);table('token_scores.csv',tokenrecords)
summaries=[];templates=[]
for split in ['smoke','heldout']:
    for mode in sorted({x['mode'] for x in pairs if x['split']==split}):
        for d in sorted({x['planned_distance'] for x in pairs if x['split']==split and x['mode']==mode}):
            ps=[x for x in pairs if (x['split'],x['mode'],x['planned_distance'])==(split,mode,d)]
            n=len(ps);k=sum(x['paired_success'] for x in ps);lo,hi=wilson(k,n);ml,mh=interval([x['mean_margin'] for x in ps]);al,ah=interval([x['accuracy'] for x in ps]);cl,ch=clustered(ps,'paired_success')
            eligibility='CLEARS_BOUNDED_BEHAVIOR_GATE' if lo>.8 and n>=20 else 'NOT_PASSED_CURRENT_TASK' if hi<.8 else 'INSUFFICIENT'
            summaries.append(dict(split=split,mode=mode,planned_distance=d,actual_distance_min=min(x['actual_distance_A'] for x in ps),actual_distance_max=max(x['actual_distance_A'] for x in ps),families=n,templates=len({x['template'] for x in ps}),prompts=2*n,correct_A=sum(x['correct_A'] for x in ps),correct_B=sum(x['correct_B'] for x in ps),accuracy=np.mean([x['accuracy'] for x in ps]),accuracy_lo=al,accuracy_hi=ah,paired_success=k,paired_rate=k/n,paired_wilson_lo=lo,paired_wilson_hi=hi,template_cluster_lo=cl,template_cluster_hi=ch,mean_margin=np.mean([x['mean_margin'] for x in ps]),margin_lo=ml,margin_hi=mh,mean_fact_preference_shift=np.mean([x['fact_preference_shift'] for x in ps]),item_only_paired_success=sum(x['item_only_paired_success'] for x in ps),point_gate=k/n>=.8,evidence_eligibility=eligibility))
            for g in sorted({x['template'] for x in ps}):
                gs=[x for x in ps if x['template']==g];templates.append(dict(split=split,mode=mode,planned_distance=d,template=g,families=len(gs),paired_success=sum(x['paired_success'] for x in gs),mean_margin=np.mean([x['mean_margin'] for x in gs])))
table('distance_summary.csv',summaries);table('template_summary.csv',templates)
main=[x for x in pairs if x['split']=='heldout' and x['mode']=='main'];contrasts=[]
for d in [64,128]:
    v=[];m=[]
    for f in sorted({x['family'] for x in main}):
        near=next(x for x in main if x['family']==f and x['planned_distance']==16);far=next(x for x in main if x['family']==f and x['planned_distance']==d)
        v.append(far['paired_success']-near['paired_success']);m.append(far['mean_margin']-near['mean_margin'])
    lo,hi=interval(v);ml,mh=interval(m);contrasts.append(dict(far=d,near=16,families=len(v),switch_change=np.mean(v),switch_lo=lo,switch_hi=hi,margin_change=np.mean(m),margin_lo=ml,margin_hi=mh))
table('paired_distance_changes.csv',contrasts)
bs=[]
for d in [16,64,128]:
    q=[x for x in baseline if x['split']=='heldout' and x['planned_distance']==d]
    bs.append(dict(distance=d,families=len(q),A_preferred=sum(x['choice']=='A' for x in q),B_preferred=sum(x['choice']=='B' for x in q),mean_A_minus_B=np.mean([x['A_minus_B'] for x in q])))
table('baseline_summary.csv',bs)
out=dict(UTC=now(),summaries=summaries,distance_changes=contrasts,baseline=bs,scientific_acceptance='Unknown',SAE_next_step_authorization='NOT_GIVEN',stop=True)
dump(R/'results/summary.json',out)
plt.rcParams.update({'font.size':10})
fig,(ax,hx)=plt.subplots(1,2,figsize=(13,8),gridspec_kw={'width_ratios':[1,1.1]},layout='constrained')
for mode,col,label in [('main','#1c6497','Main fact wording'),('paraphrase','#d88115','Natural fact paraphrase')]:
    ss=[x for x in summaries if x['split']=='heldout' and x['mode']==mode];xs=np.array([x['planned_distance'] for x in ss]);ys=np.array([x['paired_rate'] for x in ss]);low=np.array([x['paired_wilson_lo'] for x in ss]);high=np.array([x['paired_wilson_hi'] for x in ss])
    ax.errorbar(xs,ys,yerr=[ys-low,high-ys],marker='o',capsize=5,color=col,label=label)
    for x,y,s in zip(xs,ys,ss):ax.annotate(f"{s['paired_success']}/{s['families']}",(x,y),xytext=(0,9 if mode=='main' else -18),textcoords='offset points',ha='center',color=col)
lure=next(x for x in summaries if x['split']=='heldout' and x['mode']=='lure')
ax.errorbar([132],[lure['paired_rate']],yerr=[[lure['paired_rate']-lure['paired_wilson_lo']],[lure['paired_wilson_hi']-lure['paired_rate']]],fmt='x',color='#a33333',capsize=5,label=f"Recent wrong-item foil at d=128 ({lure['paired_success']}/24)")
ax.axhline(.8,color='gray',ls='--',label='Operational threshold 80%');ax.set(xticks=[16,64,128],xlabel='Actual intervening token gap (main)',ylabel='Both fact versions answered correctly',ylim=(-.03,1.09),title='24 heldout families; 95% family Wilson intervals')
ax.legend(loc='lower left',fontsize=8);ax.grid(alpha=.15)
ax.text(.02,-.16,'Paraphrase near actual gaps:16–18.\nFoil marker offset horizontally for visibility; actual gap128.\nCandidate ranking; no SAE analysis or training.',transform=ax.transAxes,fontsize=9)
fs=sorted({x['family'] for x in main});mat=np.array([[next(x['paired_success'] for x in main if x['family']==f and x['planned_distance']==d) for d in [16,64,128]] for f in fs]);hx.imshow(mat,cmap=matplotlib.colors.ListedColormap(['#e9beb9','#447da0']),vmin=0,vmax=1,aspect='auto')
familymeta={x['family']:x for x in json.load(open(R/'data/families.json'))}
hx.set_yticks(range(len(fs)),[f"{f}  {familymeta[f]['A']} / {familymeta[f]['B']}" for f in fs],fontsize=9);hx.set_xticks(range(3),['16','64','128']);hx.set_xlabel('Actual gap; every row is one heldout family');hx.set_title('Main pairs:1=both correct;0=at least one fails')
for i in range(len(fs)):
    for j in range(3):hx.text(j,i,str(mat[i,j]),ha='center',va='center',color='white' if mat[i,j] else '#5a2929')
fig.savefig(R/'figures/distance_switch.png',dpi=180);plt.close(fig)
dump(R/'figures/provenance.json',dict(file='distance_switch.png',sources=['tables/distance_summary.csv','tables/family_pairs.csv'],unit='family;24heldout; repeated distances',uncertainty='family95%Wilson, template cluster sensitivity in table',scope='main and separate diagnostic conditions',sha256=sha(R/'figures/distance_switch.png')))
print(json.dumps(out,indent=2))
