from common import *
from analyze import TASKS,task_rows,labels,ba,train,score,nuis,choose
import pickle,itertools,re
from scipy.special import expit
from scipy.stats import spearmanr

def boot(y,B=2000,seed=1031):
 rng=np.random.default_rng(seed);return [np.array([rng.choice(np.flatnonzero(y==c),sum(y==c),replace=True) for _ in range(B)]) for c in [0,1]]
def stats(y,s,bb):
 ok=((s>=0).astype(int)==y).astype(float);b=.5*(ok[bb[0]].mean(1)+ok[bb[1]].mean(1));p=expit(s);loss=-np.mean([np.mean(np.log(np.clip(p[y==1],1e-15,1))),np.mean(np.log(np.clip(1-p[y==0],1e-15,1)))]);return ba(y,(s>=0).astype(int)),np.quantile(b,[.025,.975]).tolist(),float(loss),b

def ci(x):return np.quantile(x,[.025,.975]).tolist()
def p_boot(x):return min(1.,2*min((np.sum(x<=0)+1)/(len(x)+1),(np.sum(x>=0)+1)/(len(x)+1)))
def holm(pp):
 out=np.zeros(len(pp));run=0
 for rank,i in enumerate(np.argsort(pp)):run=max(run,min(1.,pp[i]*(len(pp)-rank)));out[i]=run
 return out

def main():
 t0=time.time();freeze=json.load(open(OUT/'freeze.json'))
 for p,h in freeze['sha256'].items():assert sha(p)==h,p
 with open(OUT/'models/frozen.pkl','rb') as f:state=pickle.load(f)
 rr=rows(OUT/'data/selected_metadata.jsonl');rv=json.load(open(OUT/'data/H_label_review.json'));reviews={(r['seq_id'],r['panel']):r for r in rv['records']}
 for r in rr:
  if r['split']=='heldout':r.update({k:v for k,v in reviews[r['seq_id'],r['panel']].items() if k not in ['seq_id','panel']})
 bs=np.load(OUT/'analysis/bases.npz');V=bs['V'];mu=bs['mean'];ev=bs['eigenvalues'];D0=np.load(ROOT/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz');D=D0['decoder_model_scale'];bias=D0['decoder_bias_model']
 dump(OUT/'provenance/H_opening.json',{'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'freeze_sha256':sha(OUT/'freeze.json'),'H_label_review_sha256':sha(OUT/'data/H_label_review.json'),'evaluate_code_sha256':sha(__file__),'prior_H_exposure':'R11 earlier study;R12 results exploratory'})
 metrics=[];contrasts=[];recons=[];predictions=[];features=[];freqgroup=[];feature_readouts=[];pairrows=[];corrections=[];texts=[];details={};coverage=[];numeric=[];boots={};p_primary=[];primary_rows=[];Tf=Tokenizer()
 fr=list(csv.DictReader((ROOT/'R10_domain_member_atlas_20261030/tables/all_dictionary_screen.csv').open()));assert len(fr)==16384
 rate=np.array([float(r['DCLM_feature_occurrence']) for r in fr]);hits=np.rint(rate*65536).astype(int);fg=np.where(hits<20,'reference_insufficient',np.where(rate<=.002593994140625,'low',np.where(rate<=.0134429931640625,'middle','high')))
 for task in TASKS:
  sd=state[task];hh=task_rows([r for r in rr if r['split']=='heldout'],task);y=labels(hh,task);h,z,nm=selected_array(hh);S=(h-mu)@V;rec=z@D+bias;res=h-rec;Sr=(rec-mu)@V;Se=res@V;bb=boot(y);scores={};bacc={};nc=(res*res).sum(1)/(h*h).sum(1)
  coverage.append(dict(task=task,D_documents=len(sd['D']),V_documents=len(sd['V']),H_documents=len(hh),H_class0=int(sum(y==0)),H_class1=int(sum(y==1)),H_positions=len(hh),target_token279=True,H_new_platform=int(sum(r['source_stratum']=='new_platform_family' for r in hh)),H_same_platform=int(sum(r['source_stratum']=='same_platform_new_document_family' for r in hh))))
  for key,m in sd['models'].items():
   space=key.split('__')[1];X=S@bs[space];s=score(m,X);a,ab,ll,b=stats(y,s,bb);scores[key]=s;bacc[key]=b;metrics.append(dict(task=task,condition=key,balanced_accuracy=a,ci_low=ab[0],ci_high=ab[1],balanced_log_loss=ll,C=m['C'],parameters=m['parameters'],H_documents=len(hh),eligibility='EXPLORATORY_EXPOSED_H'))
   if key.startswith('standardized__'):
    for r,yy,ss in zip(hh,y,s):predictions.append(dict(task=task,condition=key,seq_id=r['seq_id'],topic=r['topic'],platform=r['platform_family'],source_stratum=r['source_stratum'],label=int(yy),score=float(ss),correct=bool((ss>=0)==yy)))
  # Nuisance and lexical references have the same fixed document budget.
  NX=sd['nuisance_vectorizer'].transform([nuis(r) for r in hh]);TX=sd['tfidf_vectorizer'].transform([r['prefix'] for r in hh]).toarray()
  for name,X,mo in [('source_format',NX,sd['nuisance_model']),('lexical_TFIDF',TX,sd['tfidf_model'])]:
   s=score(mo,X);a,ab,ll,b=stats(y,s,bb);metrics.append(dict(task=task,condition=name,balanced_accuracy=a,ci_low=ab[0],ci_high=ab[1],balanced_log_loss=ll,C=mo['C'],parameters=mo['parameters'],H_documents=len(hh),eligibility='EXPLORATORY_EXPOSED_H'))
  # Primary full-space gate uses conditional D-label permutations; no H tuning.
  dr=sd['D'];yd=labels(dr,task);hd,zd,_=selected_array(dr);Sd=(hd-mu)@V;vr=sd['V'];yv=labels(vr,task);hv,zv,_=selected_array(vr);Sv=(hv-mu)@V;rng=np.random.default_rng(20261031+TASKS.index(task));perm=[]
  for k in range(99):
   m=train(Sd,rng.permutation(yd),Sv,yv,'standardized',Cfixed=sd['models']['standardized__full']['C']);perm.append(ba(y,score(m,S)>=0))
  np.savez_compressed(OUT/'analysis'/('permutation_'+task+'.npz'),balanced_accuracy=np.array(perm));pv=float((sum(x>=ba(y,scores['standardized__full']>=0)-1e-12 for x in perm)+1)/100)
  gate=dict(task=task,comparison='full_vs_conditional_label_permutation',difference=ba(y,scores['standardized__full']>=0)-.5,ci_low=float(np.quantile(bacc['standardized__full']-.5,.025)),ci_high=float(np.quantile(bacc['standardized__full']-.5,.975)),p=pv,interpretation='conditional refit reference;exposed H');contrasts.append(gate);primary_rows.append(gate);p_primary.append(pv)
  comps=[('middle','head','band_minus_head'),('tail','head','band_minus_head'),('head_middle','head_next','augmentation_vs_head_extension'),('head_tail','head_next','augmentation_vs_head_extension'),('head_middle','head_random','augmentation_vs_random'),('head_tail','head_random','augmentation_vs_random'),('head_middle','head','increment_over_head'),('head_tail','head','increment_over_head'),('head_next','head','increment_over_head'),('head_random','head','increment_over_head')]
  for a,b,kind in comps:
   ka='standardized__'+a;kb='standardized__'+b;diff=bacc[ka]-bacc[kb];inter=ci(diff);row=dict(task=task,comparison=a+'__minus__'+b,kind=kind,difference=ba(y,scores[ka]>=0)-ba(y,scores[kb]>=0),ci_low=inter[0],ci_high=inter[1],p=p_boot(diff));contrasts.append(row);boots[task+'__'+a+'__'+b]=diff
   if kind in ['band_minus_head','augmentation_vs_head_extension']:primary_rows.append(row);p_primary.append(row['p'])
   if kind=='increment_over_head':
    for r,yy,sa,sb in zip(hh,y,scores[ka],scores[kb]):
     if (sa>=0)!=(sb>=0):corrections.append(dict(task=task,addition=a,seq_id=r['seq_id'],topic=r['topic'],source=r['source_stratum'],change='corrected' if (sa>=0)==yy else 'new_error',old_score=float(sb),new_score=float(sa),prefix=r['prefix']))
  # Accuracy by source stratum, class and position bin, without retuning.
  for stratum in ['new_platform_family','same_platform_new_document_family']:
   mask=np.array([r['source_stratum']==stratum for r in hh]);ys=y[mask]
   for name in ['full','head','middle','tail','head_middle','head_tail']:
    if len(np.unique(ys))<2:continue
    ss=scores['standardized__'+name][mask];sb=boot(ys,seed=1032);a,ab,ll,_=stats(ys,ss,sb);metrics.append(dict(task=task,condition='source_'+stratum+'__'+name,balanced_accuracy=a,ci_low=ab[0],ci_high=ab[1],balanced_log_loss=ll,C=sd['models']['standardized__'+name]['C'],parameters=sd['models']['standardized__'+name]['parameters'],H_documents=int(mask.sum()),eligibility='SMALL_SOURCE_STRATUM_EXPLORATORY'))
  # Fixed original heads, separately refitted reconstruction and residual heads.
  for name in ['full','head','middle','tail','head_middle','head_tail']:
   m=sd['models']['standardized__'+name];B=bs[name];s=scores['standardized__'+name];sr=score(m,Sr@B);wpc=B@(m['model'].coef_[0]/m['std']);er=Se@wpc;err=float(np.max(np.abs(s-sr-er)));assert err<1e-8*max(1.,np.max(abs(s)));ar,ab,ll,_=stats(y,sr,bb);dscore=float(s[y==1].mean()-s[y==0].mean());drscore=float(sr[y==1].mean()-sr[y==0].mean());rescontrast=float(er[y==1].mean()-er[y==0].mean())
   recons.append(dict(task=task,space=name,original_BA=ba(y,s>=0),fixed_reconstruction_BA=ar,ci_low=ab[0],ci_high=ab[1],original_score_class_difference=dscore,reconstruction_score_class_difference=drscore,residual_score_class_difference=rescontrast,reconstructed_fraction_of_score_difference=drscore/dscore if abs(dscore)>1e-8 else None,mean_abs_score_change=float(np.mean(abs(sr-s))),score_additivity_max_abs=err,mean_normalized_squared_error=float(nc.mean()),cached_native_NMSE=float(nm.mean())))
  for name,X,m in [('refit_residual',Se,sd['residual_model']),('refit_reconstruction',Sr,sd['reconstruction_model'])]:
   ss=score(m,X);aa,ab,ll,_=stats(y,ss,bb);feature_readouts.append(dict(task=task,condition=name,balanced_accuracy=aa,ci_low=ab[0],ci_high=ab[1],balanced_log_loss=ll,parameters=m['parameters'],C=m['C']))
  ids=sd['features'];zz=z[:,ids[:12]];presence=(zz>0).astype(float)
  for name,X in [('feature_presence',presence),('feature_amplitude',zz),('feature_unit_amplitude',zz/np.maximum(np.linalg.norm(zz,axis=1,keepdims=True),1e-12))]:
   aa,ab,ll,_=stats(y,score(sd[name],X),bb);feature_readouts.append(dict(task=task,condition=name,balanced_accuracy=aa,ci_low=ab[0],ci_high=ab[1],balanced_log_loss=ll,parameters=sd[name]['parameters'],C=sd[name]['C']))
  p0=(z[y==0]>0).mean(0);p1=(z[y==1]>0).mean(0);mz0=z[y==0].mean(0);mz1=z[y==1].mean(0);a0=np.divide(mz0,p0,out=np.zeros(16384),where=p0>0);a1=np.divide(mz1,p1,out=np.zeros(16384),where=p1>0);dP=(p1-p0)*(a0+a1)/2;dA=(a1-a0)*(p1+p0)/2;assert np.max(abs((mz1-mz0)-(dP+dA)))<1e-10
  coeff=sd['feature_coeff'];signed=(mz1-mz0)*coeff;selset=set(ids[:12]);rowsall=[]
  for f in range(16384):
   row=dict(task=task,feature_id=f,D_frozen_top12=f in selset,reference_rate=float(rate[f]),reference_hits=int(hits[f]),frequency_group=fg[f],H_support0=int(np.sum(z[y==0,f]>0)),H_support1=int(np.sum(z[y==1,f]>0)),H_presence0=float(p0[f]),H_presence1=float(p1[f]),H_positive_mean0=float(a0[f]) if p0[f]>0 else None,H_positive_mean1=float(a1[f]) if p1[f]>0 else None,H_mean_z_difference=float(mz1[f]-mz0[f]),presence_component=float(dP[f]),positive_amplitude_component=float(dA[f]),signed_score_contribution=float(signed[f]),presence_score_contribution=float(dP[f]*coeff[f]),amplitude_score_contribution=float(dA[f]*coeff[f]));rowsall.append(row)
   if f in selset:features.append(row)
  table(OUT/'analysis'/('all_feature_decomposition_'+task+'.csv'),rowsall)
  for group in ['low','middle','high','reference_insufficient']:
   m=fg==group;freqgroup.append(dict(task=task,frequency_group=group,members=int(m.sum()),H_active=int(np.any(z[:,m]>0,axis=0).sum()),signed_net=float(signed[m].sum()),positive_score=float(signed[m][signed[m]>0].sum()),negative_score=float(signed[m][signed[m]<0].sum()),presence_component=float((dP*coeff)[m].sum()),amplitude_component=float((dA*coeff)[m].sum())))
  numeric.append(dict(task=task,reconstruction_NMSE_max_difference=float(np.max(abs(nc-nm))),full_feature_score_contrast=float(signed.sum()),reconstruction_score_contrast=recons[-1]['reconstruction_score_class_difference'],FP32_projection_relative_error=float(np.linalg.norm((h.astype(np.float32)-mu.astype(np.float32))@V.astype(np.float32)-S)/np.linalg.norm(S)),native_norm_mean=float(np.linalg.norm(h,axis=1).mean()),reference_vs_panel_presence_spearman=float(spearmanr(rate[hits>=20],(z[:,hits>=20]>0).mean(0)).statistic)))
  # Paired relation test controls member rates via D propensities and preserves H class/source.
  pairs=sd['pairs'];PX=np.c_[NX,y];rng=np.random.default_rng(701+TASKS.index(task));blocks={}
  for k,r in enumerate(hh):blocks.setdefault((int(y[k]),r['platform_family']),[]).append(k)
  permutable=sum(len(v) for v in blocks.values() if len(v)>1)
  for _,f,g,dphi,djoint in pairs:
   af=(z[:,f]>0).astype(float);ag=(z[:,g]>0).astype(float);prop=sd['propensity'];pf=np.full(len(y),prop[f]['constant']) if 'constant' in prop[f] else expit(score(prop[f],PX));pg=np.full(len(y),prop[g]['constant']) if 'constant' in prop[g] else expit(score(prop[g],PX));rf=af-pf;rg=ag-pg;value=float(np.mean(rf*rg));null=[]
   for k in range(499):
    xp=rg.copy()
    for ix in blocks.values():xp[ix]=rng.permutation(xp[ix])
    null.append(float(np.mean(rf*xp)))
   null=np.array(null);pv=(1+np.sum(np.abs(null-null.mean())>=abs(value-null.mean())-1e-15))/500
   ph=float(np.corrcoef(af,ag)[0,1]) if af.std()>0 and ag.std()>0 else None
   pairrows.append(dict(task=task,feature_a=f,feature_b=g,D_phi=dphi,H_phi=ph,H_joint=float(np.mean(af*ag)),H_marginal_product=float(af.mean()*ag.mean()),adjusted_product=value,permutation_center=float(null.mean()),adjusted_excess_over_null=float(value-null.mean()),p=float(pv),permutable_documents=permutable,H_documents=len(hh),status='EXPLORATORY' if permutable>=8 else 'INSUFFICIENT_PERMUTABLE_SOURCE_BLOCKS'))
  prod=np.stack([(z[:,f]>0)*(z[:,g]>0) for _,f,g,_,_ in pairs],1).astype(float) if pairs else np.empty((len(y),0))
  for name,X,mo in [('pair_product_additions',np.c_[z[:,ids[:12]],prod],sd['pair_aug']),('matched_single_additions',z[:,ids[:12+len(pairs)]],sd['single_aug'])]:
   aa,ab,ll,_=stats(y,score(mo,X),bb);feature_readouts.append(dict(task=task,condition=name,balanced_accuracy=aa,ci_low=ab[0],ci_high=ab[1],balanced_log_loss=ll,parameters=mo['parameters'],C=mo['C']))
  # Frozen D text-lexicon hypotheses and fixed high/median/low H cases.
  for probe in json.load(open(OUT/'analysis/text_hypotheses.json')):
   if probe['task']!=task:continue
   ss=scores['standardized__'+probe['band']];px=np.array([sum(len(re.findall(r'\b'+re.escape(t)+r'\b',r['prefix'].lower())) for t in probe['positive_terms'])-sum(len(re.findall(r'\b'+re.escape(t)+r'\b',r['prefix'].lower())) for t in probe['negative_terms']) for r in hh]);rho=float(spearmanr(px,ss).statistic) if px.std()>0 else None
   q=np.argsort(ss);case=[('low',q[0]),('median',q[len(q)//2]),('high',q[-1])]
   for kind,i in case:texts.append(dict(task=task,kind='band_'+probe['band']+'_'+kind,seq_id=hh[i]['seq_id'],topic=hh[i]['topic'],position=hh[i]['position'],score=float(ss[i]),prefix=hh[i]['prefix'],following_posthoc=hh[i]['following'],D_positive_terms=probe['positive_terms'],D_negative_terms=probe['negative_terms'],H_lexicon_score_correlation=rho))
  for f in ids[:3]:
   for kind,i in [('low',int(np.argmin(z[:,f]))),('median',int(np.argsort(z[:,f])[len(y)//2])),('high',int(np.argmax(z[:,f])))]:texts.append(dict(task=task,kind='feature_'+str(f)+'_'+kind,seq_id=hh[i]['seq_id'],topic=hh[i]['topic'],position=hh[i]['position'],z=float(z[i,f]),signed_contribution=float(z[i,f]*coeff[f]),prefix=hh[i]['prefix'],following_posthoc=hh[i]['following']))
  # Numerical reliability: BF16 half-ulp quantization interval; fixed heads only.
  rng=np.random.default_rng(991);quant=np.exp2(np.floor(np.log2(np.maximum(abs(h),2**-126)))-7);pert=[]
  for k in range(30):
   Hn=h+rng.uniform(-.5,.5,size=h.shape)*quant;Sn=(Hn-mu)@V
   pert.append([ba(y,score(sd['models']['standardized__'+name],Sn@bs[name])>=0) for name in ['head','middle','tail','full']])
  np.savez_compressed(OUT/'analysis'/('quantization_'+task+'.npz'),balanced_accuracy=np.array(pert),baseline=np.array([ba(y,scores['standardized__'+name]>=0) for name in ['head','middle','tail','full']]))
  details[task]={'rows':hh,'y':y,'scores':scores,'h':h,'z':z};print('EVAL',task,'H',len(hh),'full/head/mid/tail',[round(ba(y,scores['standardized__'+s]>=0),4) for s in ['full','head','middle','tail']],flush=True)
 # Correctly share document resampling when comparing fine and coarse task contrasts.
 universe=details['coarse']['rows'];rng=np.random.default_rng(1507);leafs={t:[i for i,r in enumerate(universe) if r['topic']==t] for t in sum(LEAVES.values(),[])}
 for task in ['math_fine','bio_fine']:
  for band in ['middle','tail']:
   deltas=[]
   for b in range(2000):
    draw=np.concatenate([rng.choice(v,len(v),replace=True) for v in leafs.values()]);vals=[]
    for tt in ['coarse',task]:
     dd=details[tt];lookup={r['seq_id']:i for i,r in enumerate(dd['rows'])};ix=np.array([lookup[universe[i]['seq_id']] for i in draw if universe[i]['seq_id'] in lookup]);yy=dd['y'][ix]
     vals.append(ba(yy,dd['scores']['standardized__'+band][ix]>=0)-ba(yy,dd['scores']['standardized__head'][ix]>=0))
    deltas.append(vals[1]-vals[0])
   dd=details[task];co=details['coarse'];point=(ba(dd['y'],dd['scores']['standardized__'+band]>=0)-ba(dd['y'],dd['scores']['standardized__head']>=0))-(ba(co['y'],co['scores']['standardized__'+band]>=0)-ba(co['y'],co['scores']['standardized__head']>=0));inter=ci(deltas);contrasts.append(dict(task=task,comparison=band+'_fine_minus_coarse_advantage',kind='shared_document_interaction',difference=point,ci_low=inter[0],ci_high=inter[1],p=p_boot(np.array(deltas))))
 for row,q in zip(primary_rows,holm(p_primary)):row['holm_p']=float(q)
 for row,q in zip(pairrows,holm([r['p'] for r in pairrows])):row['holm_p']=float(q)
 # Also BH for the specified relation family.
 pp=np.array([r['p'] for r in pairrows]);orderp=np.argsort(pp);q=np.minimum.accumulate((pp[orderp]*len(pp)/np.arange(1,len(pp)+1))[::-1])[::-1] if len(pp) else []
 for i,v in zip(orderp,q):pairrows[i]['BH_q']=float(min(1,v))
 for name,data in [('readout_metrics',metrics),('contrasts',contrasts),('reconstruction',recons),('predictions',predictions),('features_top12',features),('frequency_signed_contributions',freqgroup),('feature_and_residual_readouts',feature_readouts),('feature_relations',pairrows),('corrected_and_new_errors',corrections),('coverage',coverage),('numerical_checks',numeric)]:table(OUT/'analysis'/(name+'.csv'),data)
 dump(OUT/'analysis/text_examples.json',texts);np.savez_compressed(OUT/'analysis/bootstrap_contrasts.npz',**boots)
 # Spectrum audit uses fixed eigenvalues; no single-root semantic stability claim.
 gaps=np.abs(np.diff(ev))/np.maximum(ev[:-1],1e-30);dump(OUT/'audits/spectrum.json',{'orthogonality_max_abs':float(np.max(abs(V.T@V-np.eye(1024)))),'eigenvalue_head':float(ev[0]),'eigenvalue_tail':float(ev[-1]),'tail_head_ratio':float(ev[-1]/ev[0]),'negative_eigenvalues':int(sum(ev<0)),'near_relative_gap_lt_1percent':int(sum(gaps<.01)),'boundaries_relative_gap':{str(i):float(gaps[i-1]) for i in [64,480,544,960]},'warning':'Individual roots near degeneracy not semantically identified;interpret band/projected classifier axes.'})
 with open(OUT/'analysis/evaluation_state.pkl','wb') as f:pickle.dump(details,f)
 dump(OUT/'analysis/completion.json',{'elapsed_seconds':time.time()-t0,'tasks':3,'main_conditions':len(metrics),'new_model_forwards':0,'training_updates':0,'primary_H_documents':len(universe),'unique_evaluated_documents':len({r['seq_id'] for r in universe}),'H_positions':len(universe),'model_frozen_sha256':sha(OUT/'models/frozen.pkl'),'H_exposed':True,'status':'MAIN_EVALUATION_COMPLETE'})
 print('COMPLETE',time.time()-t0,flush=True)
if __name__=='__main__':main()
