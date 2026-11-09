from common import *
from analyze import TASKS,task_rows,labels,train,score,nuis,ba
from evaluate import holm
from scipy.stats import beta
import pickle,shutil

def exact_bounds(y,s):
 a=[]
 for c in [0,1]:
  n=int(sum(y==c));k=int(sum(((s>=0).astype(int)==y)&(y==c)));lo=0. if k==0 else float(beta.ppf(.0125,k,n-k+1));hi=1. if k==n else float(beta.ppf(.9875,k+1,n-k));a.append((lo,hi,k,n))
 return dict(exact_ci_low=float(np.mean([x[0] for x in a])),exact_ci_high=float(np.mean([x[1] for x in a])),class0_correct=a[0][2],class0_n=a[0][3],class1_correct=a[1][2],class1_n=a[1][3],interval='classwise97.5percent_ClopperPearson_Bonferroni_mean;fixed_fitted_model')

def run():
 start=time.time();a=OUT/'analysis';bs=np.load(a/'bases.npz');V=bs['V'];mu=bs['mean'];rr=rows(OUT/'data/selected_metadata.jsonl');hr=json.load(open(OUT/'data/H_label_review.json'));rv={(r['seq_id'],r['panel']):r for r in hr['records']}
 for r in rr:
  if r['split']=='heldout':r.update(rv[r['seq_id'],r['panel']])
 with open(OUT/'models/frozen.pkl','rb') as f:models=pickle.load(f)
 with open(a/'evaluation_state.pkl','rb') as f:ev=pickle.load(f)
 # Repair one diagnostic field that accidentally pointed to the last band, not full.
 p=a/'numerical_checks.csv';shutil.copy2(p,OUT/'provenance/numerical_checks_before_field_correction.csv');num=list(csv.DictReader(p.open()));rec=list(csv.DictReader((a/'reconstruction.csv').open()))
 for row in num:
  r=next(r for r in rec if r['task']==row['task'] and r['space']=='full');row['reconstruction_score_contrast']=r['reconstruction_score_class_difference'];assert abs(float(row['full_feature_score_contrast'])-float(row['reconstruction_score_contrast']))<1e-10
 table(p,num)
 exact=[];rob=[];matches=[];quant=[];checks=[];source=[];multi=[];bandshift=[];D=np.load(ROOT/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz')['decoder_model_scale']
 for task in TASKS:
  sd=models[task];d=ev[task];y=d['y'];S=(d['h']-mu)@V;hh=d['rows'];lookup={r['seq_id']:i for i,r in enumerate(hh)}
  for key,ss in d['scores'].items():exact.append(dict(task=task,condition=key,**exact_bounds(y,ss)))
  for name,X,mo in [('source_format',sd['nuisance_vectorizer'].transform([nuis(r) for r in hh]),sd['nuisance_model']),('lexical_TFIDF',sd['tfidf_vectorizer'].transform([r['prefix'] for r in hh]).toarray(),sd['tfidf_model'])]:exact.append(dict(task=task,condition=name,**exact_bounds(y,score(mo,X))))
  for r in hh:source.append(dict(task=task,seq_id=r['seq_id'],topic=r['topic'],platform=r['platform_family'],genre=r['genre'],position=r['position'],source_stratum=r['source_stratum']))
  # Independent CSR replay and direct score reconstruction, selected without outcomes.
  for r in sorted(hh,key=order)[:5]:
   i=lookup[r['seq_id']];zfile=np.load(get_cache(r));t=r['position'];v=np.zeros(16384);lo,hi=zfile['CC_ptr'][t:t+2];
   for k,zz in zip(zfile['CC_ids'][lo:hi],zfile['CC_z'][lo:hi]):v[int(k)]=float(zz)
   assert np.array_equal(v,d['z'][i]);m=sd['models']['standardized__full'];wpc=m['model'].coef_[0]/m['std'];direct=float((r0:=d['h'][i]-mu)@V@wpc +m['model'].intercept_[0]-m['mean']@wpc);expect=float(d['scores']['standardized__full'][i]);sk=float(m['model'].decision_function(((r0@V-m['mean'])/m['std'])[None])[0]);assert abs(direct-expect)<1e-10 and abs(sk-expect)<1e-10
   checks.append(dict(task=task,seq_id=r['seq_id'],CSR_exact=True,score_abs_error=abs(direct-expect),sklearn_score_abs_error=abs(sk-expect)))
  # Strict metadata matching; never relax empty cells.
  pairs=[];unused=set(np.flatnonzero(y==1).tolist())
  for i in sorted(np.flatnonzero(y==0),key=lambda j:order(hh[j])):
   options=[j for j in unused if hh[i]['platform_family']==hh[j]['platform_family'] and hh[i]['genre']==hh[j]['genre'] and abs(hh[i]['position']-hh[j]['position'])<=32]
   if options:
    j=min(options,key=lambda j:(abs(hh[i]['position']-hh[j]['position']),order(hh[j])));unused.remove(j);pairs.append((i,j))
  for name in ['full','head','middle','tail']:
   dif=[float(d['scores']['standardized__'+name][j]-d['scores']['standardized__'+name][i]) for i,j in pairs];matches.append(dict(task=task,band=name,matched_pairs=len(pairs),documents=2*len(pairs),total_documents=len(hh),coverage=2*len(pairs)/len(hh),mean_class1_minus_class0_score=float(np.mean(dif)) if dif else None,positive_pairs=int(sum(v>0 for v in dif)),status='SMALL_MATCHED_DESCRIPTION' if len(pairs)>=5 else 'INSUFFICIENT_STRICT_MATCHING',pair_ids=';'.join(hh[i]['seq_id']+'|'+hh[j]['seq_id'] for i,j in pairs)))
  # Prespecified perturbation sensitivity is not independent measurement evidence.
  q=np.load(a/('quantization_'+task+'.npz'))
  for k,name in enumerate(['head','middle','tail','full']):quant.append(dict(task=task,band=name,baseline=float(q['baseline'][k]),perturbed_min=float(q['balanced_accuracy'][:,k].min()),perturbed_max=float(q['balanced_accuracy'][:,k].max()),draws=30))
  dall=task_rows([r for r in rr if r['split']=='discovery'],task);vall=sd['V'];yv=labels(vall,task);hv,_,_=selected_array(vall);Sv=(hv-mu)@V
  # Necessary post-primary check: fixed ten subset seeds; all retained, no winner selection.
  for seed in range(1040,1050):
   rng=np.random.default_rng(seed);picked=[]
   if task=='coarse':
    for topic in sum(LEAVES.values(),[]):
     aa=[r for r in dall if r['topic']==topic];ix=rng.choice(len(aa),4,replace=False);picked.extend([aa[i] for i in ix])
   else:
    yy=labels(dall,task)
    for c in [0,1]:
     aa=[r for r,zz in zip(dall,yy) if zz==c];ix=rng.choice(len(aa),8,replace=False);picked.extend([aa[i] for i in ix])
   hd,_,_=selected_array(picked);Xd=(hd-mu)@V;yd=labels(picked,task)
   for band in ['head','middle','tail','full','head_middle','head_tail','head_next','head_random']:
    B=bs[band];C=sd['models']['standardized__'+band]['C'];m=train(Xd@B,yd,Sv@B,yv,'standardized',Cfixed=C);rob.append(dict(task=task,seed=seed,band=band,balanced_accuracy=ba(y,score(m,S@B)>=0),C=C,D=len(picked)))
  # Nearby equal-width bands are exploratory stability checks; primary remains fixed.
  hd,_,_=selected_array(sd['D']);Xd=(hd-mu)@V;yd=labels(sd['D'],task)
  for name,ix in [('middle_left',np.arange(464,528)),('middle_right',np.arange(496,560)),('tail_left',np.arange(944,1008))]:
   m=train(Xd[:,ix],yd,Sv[:,ix],yv);bandshift.append(dict(task=task,variant=name,PC_first=int(ix[0]+1),PC_last=int(ix[-1]+1),balanced_accuracy=ba(y,score(m,S[:,ix])>=0),C=m['C'],status='EXPLORATORY_POST_PRIMARY_BOUNDARY_CHECK'))
  # Fallback/common-token mix uses ORIGINAL frozen heads; token groups remain separate.
  mr=task_rows([r for r in rr if r['split']=='heldout' and r['panel']=='multi'],task)
  # task_rows selects primary explicitly, so construct secondary independently.
  mr=[r for r in rr if r['split']=='heldout' and r['panel']=='multi' and (task=='coarse' or (r['domain']==('math' if task=='math_fine' else 'biology') and r['fine_eligible']))]
  mh,_,_=selected_array(mr);MS=(mh-mu)@V;my=labels(mr,task)
  for band in ['full','head','middle','tail']:
   ss=score(sd['models']['standardized__'+band],MS@bs[band]);multi.append(dict(task=task,band=band,panel='multi_all',documents=len(my),balanced_accuracy=ba(my,ss>=0),status='TOKEN_STRATIFIED_TRANSFER_SENSITIVITY'))
   for token in sorted({r['token_id'] for r in mr}):
    ix=np.array([r['token_id']==token for r in mr]);yy=my[ix];multi.append(dict(task=task,band=band,panel='token_'+str(token),documents=int(sum(ix)),balanced_accuracy=ba(yy,ss[ix]>=0) if len(np.unique(yy))==2 else None,status='INSUFFICIENT_SINGLE_CLASS' if len(np.unique(yy))<2 else 'EXPLORATORY'))
 table(a/'finite_sample_bounds.csv',exact);table(a/'training_subset_sensitivity.csv',rob);table(a/'strict_source_position_matching.csv',matches);table(a/'quantization_summary.csv',quant);table(a/'source_position_inventory.csv',source);table(a/'nearby_band_sensitivity.csv',bandshift);table(a/'multi_token_transfer.csv',multi);table(OUT/'audits/independent_replay.csv',checks)
 # Interaction multiplicity is separately visible; not mixed into a stronger main claim.
 cc=list(csv.DictReader((a/'contrasts.csv').open()));inter=[r for r in cc if r.get('kind')=='shared_document_interaction']
 for r,q in zip(inter,holm([float(r['p']) for r in inter])):r['interaction_Holm4_p']=float(q)
 table(a/'granularity_interactions_Holm4.csv',inter)
 # Label and source split identities are checked using metadata only.
 families={s:{r['document_family'] for r in rr if r['panel']=='the' and r['split']==s} for s in ['discovery','development','heldout']}
 assert all(not families[x]&families[y] for x,y in [('discovery','development'),('discovery','heldout'),('development','heldout')])
 hnew={r['platform_family'] for r in rr if r['panel']=='the' and r['split']=='heldout' and r['source_stratum']=='new_platform_family'};dv={r['platform_family'] for r in rr if r['split']!='heldout'};assert not hnew&dv
 dump(OUT/'audits/independent_validation.json',{'status':'PASS_BOUNDED','direct_CSR_score_replays':len(checks),'family_overlap':False,'new_H_platform_overlap_with_DV':False,'finite_sample_interval_supplement':'Perfect empirical bootstrap is degenerate;use Bonferroni classwise exact document bounds alongside paired bootstrap.','diagnostic_field_correction':'numerical_checks reconstruction_score_contrast previously pointed to head_tail;corrected to full;no model,prediction or primary result changed.','training_subset_seeds':10,'boundary_variants':3,'primary_selection_unchanged':True,'H_exposed':True,'elapsed_seconds':time.time()-start})
 print('VALIDATED',len(checks),'direct replays;',len(rob),'subset rows;',len(matches),'matching rows;',time.time()-start,flush=True)
if __name__=='__main__':run()
