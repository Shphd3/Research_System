from engine import *
import pandas as pd,time
start=time.time();rng=np.random.default_rng(PLAN['seed']+999);ownrows=[];betweenrows=[];Arows=[];Irows=[];pairrows=[];histrows=[];patternrows=[];mixrows=[];auditrows=[];bootsave={};componentrows=[];docrows=[];needs=[]
def loadnull(s,tag,mode):
 p=R/'cache'/f'{s}__{tag}__{mode}__long.npz'
 if not p.exists():p=R/'cache'/f'{s}__{tag}__{mode}.npz'
 return np.load(p),p.stem

def bootmeans(x,seed):
 rr=np.random.default_rng(seed);n=len(x);cnt=rr.multinomial(n,np.full(n,1/n),size=999);v=cnt@x/n;return v

def diag(x,source,site,mode,stat):
 q=rhat_ess(x);mixrows.append(dict(site=site,source=source,mode=mode,statistic=stat,**q));return q['Rhat']<=1.10 and q['ESS']>=100

def holm(rows,key='p_null',out='Holm_p'):
 values=np.array([r[key] for r in rows]);order=np.argsort(values);adj=np.maximum.accumulate([(len(rows)-j)*values[i] for j,i in enumerate(order)])
 for j,i in enumerate(order):rows[i][out]=float(min(1,adj[j]))

for site in SITES:
 direction=np.load(R/'data'/f'{site}__discovery_directions.npz');features=direction['features'];realdisc,discstem=loadnull(site,'discovery','position');marg=np.load(R/'data/discovery_marginals.npz');ber=np.load(R/'cache'/f'{site}__frequency_reference.npz')
 for mode in ['position','position_token3']:
  hold,stem=loadnull(site,'heldout',mode);qn=hold['qnull'];nullmean=qn.mean((0,1));realq=hold['realq'];own=direction['own'];between=direction['between'];real=realq.mean(1);discq=realdisc['realq'];discnull=realdisc['qnull'];discmean=discnull.mean((0,1));rdisc=discq.mean(1)-discmean
  constraints=rows(R/'evidence'/f'{stem}__constraints.jsonl');bad_margin=any(a['max_column_error']!=0 for a in constraints);ret_diff=float(np.mean([abs(a['retention_difference']) for a in constraints]));commonquality=(not bad_margin) and ret_diff<=.05
  auditrows.append(dict(site=site,mode=mode,split='heldout',rows_per_source=129,per_snapshot_strata=len(constraints)//4,checked_snapshots=sum(a['checks'] for a in constraints),max_column_error=max(a['max_column_error'] for a in constraints),row_degree=32,changed_trade_fraction=sum(a['changed_trades'] for a in constraints)/sum(a['proposals'] for a in constraints),proposals=sum(a['proposals'] for a in constraints),moved_edges=sum(a['moved_edges'] for a in constraints),mean_abs_retention_error=ret_diff,lowN_strata=sum(a['N']<8 for a in constraints)//4,total_strata=len(constraints)//4,locked_feature_edges=sum(a['locked_edge_fraction']*a['N']*32 for a in constraints)/4,total_edges=3*129*8*32))
  if mode=='position':
   # Document-level uncertainty for observed overlap, reusing the original S08 count-weighted graph.
   k=hold['realJ'];ki=hold['realI'];n=129;ww=np.triu(np.ones((n,n)),1);cc=np.zeros((n,n));rr=np.arange(n)
   for off in range(1,(n-1)//2+1):cc[rr,(rr+off)%n]=1
   rrng=np.random.default_rng(PLAN['seed']+SITES.index(site)*1000);bc=[rrng.multinomial(n,np.full(n,1/n),size=999).astype(float) for _ in DATASETS];bs=[]
   for j in range(6):
    a,b=(j,j) if j<3 else DP[j-3];mask=ww if j<3 else cc;km=k[a*n:(a+1)*n,b*n:(b+1)*n];u,v=bc[a],bc[b];num=np.einsum('bi,bi->b',u@(km*mask),v);den=np.einsum('bi,bi->b',u@mask,v);bs.append(num/den)
   bs=np.stack(bs,axis=1);bootsave[site+'__overlap_bootstrap']=bs
   jnull=hold['Jnull'].reshape(-1,6);berj=ber['Jnull'];inull=hold['Inull'].reshape(-1,6)
   for ab,(a,b) in enumerate(DP):
    for label,ix in [('within_A',a),('within_B',b),('cross',3+ab)]:
     truth=float(hold['realstats'][ix]);blo,bhi=np.quantile(bs[:,ix],[.025,.975]);ref=float(berj[:,ix].mean());exact=float(jnull[:,ix].mean());Arows.append(dict(site=site,A=DATASETS[a],B=DATASETS[b],comparison=label,N_discovery=128,N_heldout=129,positions_per_doc=8,document_pairs=8256,real_J=truth,real_CI_lo=float(blo),real_CI_hi=float(bhi),discovery_Bernoulli_J=ref,Bernoulli_MCSE=float(berj[:,ix].std(ddof=1)/16),real_minus_Bernoulli=truth-ref,heldout_fixed32_margin_J=exact,fixed32_null_SD=float(jnull[:,ix].std(ddof=1)),real_minus_fixed32_margin=truth-exact))
    gap=hold['realstats'][[a,b]].mean()-hold['realstats'][3+ab];bg=bs[:,[a,b]].mean(1)-bs[:,3+ab];ng=jnull[:,[a,b]].mean(1)-jnull[:,3+ab];fg=berj[:,[a,b]].mean(1)-berj[:,3+ab];bci=np.quantile(bg,[.025,.975]);Arows.append(dict(site=site,A=DATASETS[a],B=DATASETS[b],comparison='pooled_gap',N_discovery=128,N_heldout=129,positions_per_doc=8,document_pairs=8256,real_J=float(gap),real_CI_lo=float(bci[0]),real_CI_hi=float(bci[1]),discovery_Bernoulli_J=float(fg.mean()),Bernoulli_MCSE=float(fg.std(ddof=1)/16),real_minus_Bernoulli=float(gap-fg.mean()),heldout_fixed32_margin_J=float(ng.mean()),fixed32_null_SD=float(ng.std(ddof=1)),real_minus_fixed32_margin=float(gap-ng.mean())))
   for j in range(6):
    a,b=(j,j) if j<3 else DP[j-3];expI=np.mean(np.sum(marg[site+'__'+DATASETS[a]]*marg[site+'__'+DATASETS[b]],axis=1));ca=marg[site+'__'+DATASETS[a]]*128
    unbiased=float(np.mean(np.sum(ca*(ca-1)/(128*127),axis=1))) if a==b else expI
    Irows.append(dict(site=site,comparison='within_'+DATASETS[a] if a==b else DATASETS[a]+'/'+DATASETS[b],analytic_discovery_plugin_E_intersection=float(expI),discovery_unbiased_E_intersection=unbiased,MC_Bernoulli_mean_intersection=float(ber['Inull'][:,j].mean()),real_heldout_intersection=float(hold['real_intersections'][j]),fixed32_null_mean_intersection=float(inull[:,j].mean()),fixed32_null_intersection_range=float(np.ptp(inull[:,j])),real_J_linear_I_over64=float(hold['real_intersections'][j]/64),real_J_curvature=float(hold['real_curvature'][j]),null_J_curvature_mean=float(hold['curvature_null'].reshape(-1,6)[:,j].mean()),full_cross_real_J=None if a==b else float(hold['real_fullcross'][j-3]),full_cross_null_J=None if a==b else float(hold['fullcross_null'].reshape(-1,3)[:,j-3].mean())))
   for j in range(6):
    if not diag(hold['Jnull'][:,:,j],stem,site,mode,'J_'+str(j)):needs.append([site,'heldout',mode])
  # Own replicated residual patterns, not marginal-rate discrimination.
  ownboot=[]
  for d,ds in enumerate(DATASETS):
   v=own[d];center=hold['qdoc_null_mean'][d] if mode=='position_token3' else np.broadcast_to(nullmean[d],realq[d].shape);doc=(realq[d]-center)@v;observed=float(doc.mean());nullscore=np.einsum('csp,p->cs',qn[:,:,d]-nullmean[d],v);discscore=float(rdisc[d]@v);disc_nullscore=np.einsum('csp,p->cs',discnull[:,:,d]-discmean[d],v);boot=bootmeans(doc,PLAN['seed']+SITES.index(site)*10000+d);ownboot.append(boot);lo,hi=np.quantile(boot,[.025,.975]);p=float((1+(nullscore>=observed).sum())/257);mix=diag(nullscore,stem,site,mode,'own_'+ds);mixd=diag(disc_nullscore,discstem,site,'position','own_'+ds+'_discovery')
   if not mix:needs.append([site,'heldout',mode])
   if not mixd:needs.append([site,'discovery','position'])
   ownrows.append(dict(site=site,dataset=ds,mode=mode,N=129,discovery_N=128,pairs=276,discovery_excess_projection=discscore,heldout_real_projection=float(real[d]@v),heldout_null_projection=float(nullmean[d]@v),heldout_excess=observed,doc_CI_lo=float(lo),doc_CI_hi=float(hi),null_projection_SD=float(nullscore.std(ddof=1)),null_center_MCSE=float(nullscore.std(ddof=1)/16),p_null=p,Holm_p=None,mixing_pass=bool(mix and mixd and commonquality),discovery_norm=float(direction['norm'][d]),conditional_interval='Discovery direction and estimated null center fixed; not unconditional probability-estimation CI'))
   bootsave[site+'__'+mode+'__own__'+ds]=boot
   for di,i in enumerate(INDEX[ds+'__heldout']):docrows.append(dict(site=site,dataset=ds,mode=mode,id=PANEL[i]['id'],own_excess_projection=float(doc[di]),text=PANEL[i]['text']))
   for pairidx,(i,j) in enumerate(PAIRS):componentrows.append(dict(site=site,dataset=ds,mode=mode,feature_i=int(features[i]),feature_j=int(features[j]),discovery_real=float(discq[d,:,pairidx].mean()),discovery_null=float(discmean[d,pairidx]),discovery_excess=float(rdisc[d,pairidx]),heldout_real=float(real[d,pairidx]),heldout_null=float(nullmean[d,pairidx]),heldout_excess=float(real[d,pairidx]-nullmean[d,pairidx]),discovery_own_weight=float(v[pairidx])))
   for kk in range(25):histrows.append(dict(site=site,dataset=ds,mode=mode,active_candidate_members=kk,discovery_real=float(realdisc['realhist'][d,kk]),discovery_null=float(realdisc['histnull'][:,:,d,kk].mean()),heldout_real=float(hold['realhist'][d,kk]),heldout_null=float(hold['histnull'][:,:,d,kk].mean()),null_lo=float(np.quantile(hold['histnull'][:,:,d,kk],.025)),null_hi=float(np.quantile(hold['histnull'][:,:,d,kk],.975))))
   for kk,code in enumerate(list(hold['patterns'])+[-1]):patternrows.append(dict(site=site,dataset=ds,mode=mode,pattern_code=int(code),feature_ids='OTHER' if code==-1 else ','.join(str(features[i]) for i in range(24) if (int(code)>>i)&1),discovery_real=float(realdisc['realpat'][d,kk]),discovery_null=float(realdisc['patnull'][:,:,d,kk].mean()),heldout_real=float(hold['realpat'][d,kk]),heldout_null=float(hold['patnull'][:,:,d,kk].mean())))
  for ab,(a,b) in enumerate(DP):
   v=between[ab];centera=hold['qdoc_null_mean'][a] if mode=='position_token3' else nullmean[a];centerb=hold['qdoc_null_mean'][b] if mode=='position_token3' else nullmean[b];da=(realq[a]-centera)@v;db=(realq[b]-centerb)@v;ob=float(da.mean()-db.mean());ns=np.einsum('csp,p->cs',qn[:,:,a]-nullmean[a]-(qn[:,:,b]-nullmean[b]),v);dns=np.einsum('csp,p->cs',discnull[:,:,a]-discmean[a]-(discnull[:,:,b]-discmean[b]),v);ba=bootmeans(da,PLAN['seed']+100+ab);bb=bootmeans(db,PLAN['seed']+200+ab);bo=ba-bb;lo,hi=np.quantile(bo,[.025,.975]);p=float((1+(ns>=ob).sum())/257);mix=diag(ns,stem,site,mode,'between_'+str(ab));mixd=diag(dns,discstem,site,'position','between_'+str(ab)+'_discovery')
   if not mix:needs.append([site,'heldout',mode])
   if not mixd:needs.append([site,'discovery','position'])
   betweenrows.append(dict(site=site,A=DATASETS[a],B=DATASETS[b],mode=mode,N_A=129,N_B=129,discovery_excess_difference=float((rdisc[a]-rdisc[b])@v),heldout_A_excess=float(da.mean()),heldout_B_excess=float(db.mean()),heldout_difference=ob,doc_CI_lo=float(lo),doc_CI_hi=float(hi),null_SD=float(ns.std(ddof=1)),null_center_MCSE=float(ns.std(ddof=1)/16),p_null=p,Holm_p=None,mixing_pass=bool(mix and mixd and commonquality),discovery_norm=float(direction['between_norm'][ab])))
   bootsave[site+'__'+mode+'__between__'+str(ab)]=bo
  for j in direction['selected_pair_indices']:
   i,k=PAIRS[j]
   for d,ds in enumerate(DATASETS):
    doc=realq[d,:,j];center=hold['qdoc_null_mean'][d,:,j] if mode=='position_token3' else nullmean[d,j];bo=bootmeans(doc-center,PLAN['seed']+int(j));lo,hi=np.quantile(bo,[.025,.975]);p=marg[site+'__'+ds];prod=float(np.mean(p[:,features[i]]*p[:,features[k]]));rawdocs=int(np.sum(doc>0));pairrows.append(dict(site=site,dataset=ds,mode=mode,feature_i=int(features[i]),feature_j=int(features[k]),discovery_real=float(discq[d,:,j].mean()),discovery_product_marginal=prod,discovery_real_minus_product=float(discq[d,:,j].mean()-prod),discovery_degree_null=float(discmean[d,j]),heldout_real=float(real[d,j]),heldout_coactivating_documents=rawdocs,heldout_coactivating_positions=int(np.round(doc.sum()*8)),heldout_degree_null=float(nullmean[d,j]),heldout_excess=float(real[d,j]-nullmean[d,j]),doc_CI_lo=float(lo),doc_CI_hi=float(hi),sign_replicated=bool(rdisc[d,j]*(real[d,j]-nullmean[d,j])>0)))
# Two distinct six-test primary families; exploratory token models remain raw p.
for rr in [ownrows,betweenrows]:
 prim=[r for r in rr if r['mode']=='position'];holm(prim)
 for r in rr:
  point=r['heldout_excess'] if 'heldout_excess' in r else r['heldout_difference'];p=r['Holm_p'] if r['mode']=='position' else r['p_null']
  r['status']='INSUFFICIENT' if not r['mixing_pass'] or r['discovery_norm']<1e-12 else ('SUPPORTED_STATISTIC' if r['doc_CI_lo']>0 and p<.05 else ('NOT_SUPPORTED_DIRECTION' if point<0 and r['doc_CI_hi']<0 else 'INSUFFICIENT_OR_NO_DETECTED_EXCESS'))
table(R/'tables/A_overlap_references.csv',Arows);table(R/'tables/A_intersection_identity.csv',Irows);table(R/'tables/B_own_structure.csv',ownrows);table(R/'tables/B_dataset_differences.csv',betweenrows);table(R/'tables/B_selected_pairs.csv',pairrows);table(R/'tables/B_all276_components.csv',componentrows);table(R/'tables/B_member_count_distribution.csv',histrows);table(R/'tables/B_exact_pattern_distribution.csv',patternrows);table(R/'tables/null_mixing.csv',mixrows);table(R/'tables/null_constraints_summary.csv',auditrows);jsonl(R/'tables/heldout_document_scores.jsonl',docrows);np.savez_compressed(R/'tables/document_bootstraps.npz',**bootsave)
needs=sorted({tuple(x) for x in needs});dump(R/'evidence/mixing_extension_requests.json',dict(UTC=now(),conditions=[list(x) for x in needs],preallowed='same statistics/directions; preserve original files; longer burn500thin50 once'))
dump(R/'evidence/analysis_complete.json',dict(UTC=now(),status='COMPLETED',seconds=time.time()-start,source_sha256=sha(S08/'cache/activations.npz'),own_primary=6,between_primary=6,Arows=len(Arows),mixing_requests=len(needs),code_sha256=sha(__file__)))
print(pd.DataFrame(ownrows)[['site','dataset','mode','heldout_excess','doc_CI_lo','doc_CI_hi','Holm_p','mixing_pass','status']].to_string(index=False));print(pd.DataFrame(betweenrows)[['site','A','B','mode','heldout_difference','doc_CI_lo','doc_CI_hi','Holm_p','mixing_pass','status']].to_string(index=False));print('NEEDS',needs,flush=True)
